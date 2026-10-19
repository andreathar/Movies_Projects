"""Greenfield management tests; all state and credentials live in temporary directories."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from production_db import ManagementError, Store, credential, main


class ProductionDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.db = self.root / "management.sqlite3"
        self.owner_file = self.root / "owner.credential"
        self.store = Store.initialize(self.db, self.root, "operator", self.owner_file)
        self.owner = credential(self.owner_file)
        self.sequence = 0

    def run_command(self, command, token=None, **args):
        self.sequence += 1
        return self.store.execute(token or self.owner, command, args,
                                  request_id=f"request-{self.sequence}", reason="Synthetic test")

    def project(self, name="new-film"):
        self.run_command("project-create", project=name, title="New clean film")
        return name

    def member(self, user="maker", role="contributor", project="new-film"):
        path = self.root / f"{user}.credential"
        self.sequence += 1
        self.store.add_identity(self.owner, user, path, request_id=f"identity-{self.sequence}", reason="Test enrollment")
        self.run_command("member-add", project=project, user=user, role=role)
        return credential(path)

    def assignment(self, task="T1", user="maker", token=None, path="delivery.txt"):
        self.run_command("task-create", project="new-film", id=task, title="Bounded output")
        self.run_command("task-offer", task=task, revision=1, to=user, scope="Write test output only",
                         allowed_path=[path])
        self.run_command("task-accept", token=token, task=task, revision=2)

    def delivery(self):
        self.project()
        maker = self.member()
        self.assignment(token=maker)
        (self.root / "delivery.txt").write_text("Original synthetic delivery")
        self.run_command("artifact-add", token=maker, task="T1", revision=3, id="A1", path="delivery.txt")
        self.run_command("handoff-submit", token=maker, id="H1", task="T1", revision=3,
                         scope="Test output", limitations="No artistic review or paid action",
                         artifact=["A1"], check=[["readback", "passed", "Compared exact fixture bytes"]])
        return maker

    def query(self, kind):
        return self.store.query(self.owner, "new-film", kind)

    def test_empty_initialization_and_no_legacy_dependency(self):
        self.assertFalse((self.root / "workspace.json").exists())
        with sqlite3.connect(self.db) as c:
            for table in ("projects", "tasks", "decisions", "approvals", "handoffs"):
                self.assertEqual(c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0], 0)
            self.assertEqual(c.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        self.assertEqual(self.db.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.owner_file.stat().st_mode & 0o777, 0o600)
        before = self.db.read_bytes()
        with self.assertRaises(FileExistsError):
            Store.initialize(self.db, self.root, "other", self.root / "other.credential")
        self.assertEqual(before, self.db.read_bytes())

    def test_failed_init_preserves_existing_credential(self):
        other_db = self.root / "other.sqlite3"
        original = self.owner_file.read_bytes()
        with self.assertRaises(FileExistsError):
            Store.initialize(other_db, self.root, "other", self.owner_file)
        self.assertEqual(original, self.owner_file.read_bytes())
        self.assertFalse(other_db.exists())

    def test_authentication_and_project_permissions(self):
        self.project()
        maker = self.member()
        with self.assertRaisesRegex(ManagementError, "invalid credential"):
            self.run_command("project-create", token="forged", project="x", title="x")
        with self.assertRaisesRegex(ManagementError, "operator credential"):
            self.run_command("project-create", token=maker, project="x", title="x")
        with self.assertRaisesRegex(ManagementError, "permission denied"):
            self.run_command("task-create", token=maker, project="new-film", id="T1", title="x")
        self.project("other-film")
        with self.assertRaisesRegex(ManagementError, "permission denied"):
            self.store.query(maker, "other-film", "events")
        with self.assertRaisesRegex(ManagementError, "unsupported query"):
            self.store.query(self.owner, "new-film", "identities")

    def test_idempotent_requests_and_mismatching_replay(self):
        self.project()
        args = dict(project="new-film", id="T1", title="Test")
        first = self.store.execute(self.owner, "task-create", args, request_id="stable", reason="Once")
        second = self.store.execute(self.owner, "task-create", args, request_id="stable", reason="Once")
        self.assertEqual(first, second)
        self.assertEqual(len(self.query("tasks")), 1)
        with self.assertRaisesRegex(ManagementError, "different content"):
            self.store.execute(self.owner, "task-create", {**args, "title": "Changed"}, request_id="stable", reason="Once")

    def test_stale_versions_and_explicit_acceptance(self):
        self.project()
        maker = self.member()
        other = self.member("other")
        self.run_command("task-create", project="new-film", id="T1", title="Test")
        self.run_command("task-offer", task="T1", revision=1, to="maker", scope="Bounded review")
        task = self.query("tasks")[0]
        self.assertEqual(task["responsible_id"], "operator")
        self.assertEqual(task["state"], "offered")
        with self.assertRaisesRegex(ManagementError, "only the offered recipient"):
            self.run_command("task-accept", token=other, task="T1", revision=2)
        self.run_command("task-accept", token=maker, task="T1", revision=2)
        with self.assertRaisesRegex(ManagementError, "stale revision"):
            self.run_command("task-block", task="T1", revision=2, owner="maker", condition="New evidence")
        self.assertEqual(self.query("tasks")[0]["responsible_id"], "maker")

    def test_concurrent_same_revision_has_one_winner(self):
        self.project()
        self.member()
        self.run_command("task-create", project="new-film", id="T1", title="Test")
        def offer(index):
            try:
                self.store.execute(self.owner, "task-offer", dict(task="T1", revision=1, to="maker", scope="Bounded review"),
                                   request_id=f"race-{index}", reason="Concurrency test")
                return "committed"
            except ManagementError:
                return "rejected"
        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertCountEqual(list(pool.map(offer, (1, 2))), ["committed", "rejected"])
        self.assertEqual(self.query("tasks")[0]["revision"], 2)

    def test_dependency_integrity_and_transaction_rollback(self):
        self.project()
        self.member()
        self.run_command("task-create", project="new-film", id="T1", title="First")
        self.run_command("task-create", project="new-film", id="T2", title="Second", depends_on=["T1"])
        count = len(self.query("events"))
        with self.assertRaisesRegex(ManagementError, "dependencies"):
            self.run_command("task-offer", task="T2", revision=1, to="maker", scope="Review")
        self.assertEqual(len(self.query("events")), count)
        with self.assertRaises(ManagementError):
            self.run_command("task-create", project="new-film", id="T3", title="Broken", depends_on=["missing"])
        self.assertEqual([v["id"] for v in self.query("tasks")], ["T1", "T2"])
        self.project("other-film")
        self.run_command("task-create", project="other-film", id="X1", title="Other")
        with self.assertRaisesRegex(ManagementError, "cross-project"):
            self.run_command("task-create", project="new-film", id="T3", title="Broken", depends_on=["X1"])

    def test_full_handoff_closure_does_not_approve_artifact(self):
        maker = self.delivery()
        self.assertEqual(self.query("tasks")[0]["state"], "delivered")
        with self.assertRaisesRegex(ManagementError, "permission denied"):
            self.run_command("handoff-verify", token=maker, handoff="H1", revision=1)
        with self.assertRaisesRegex(ManagementError, "verified"):
            self.run_command("handoff-integrate", handoff="H1", revision=1, closed=True)
        self.run_command("handoff-verify", handoff="H1", revision=1)
        self.assertEqual(self.query("tasks")[0]["state"], "delivered")
        with self.assertRaisesRegex(ManagementError, "choose accepted"):
            self.run_command("handoff-integrate", handoff="H1", revision=2)
        self.run_command("handoff-integrate", handoff="H1", revision=2, closed=True)
        self.assertEqual(self.query("tasks")[0]["state"], "completed")
        self.assertEqual(self.query("handoffs")[0]["closure"], "closed")
        self.assertEqual(self.query("approvals"), [])
        self.assertEqual(self.query("handoff_checks")[0]["result"], "passed")
        with self.assertRaisesRegex(ManagementError, "stale"):
            self.run_command("handoff-integrate", handoff="H1", revision=2, closed=True)

    def test_successor_requires_actual_accepted_assignment(self):
        maker = self.delivery()
        self.run_command("handoff-verify", handoff="H1", revision=1)
        self.run_command("task-create", project="new-film", id="T2", title="Independent next task")
        self.run_command("task-offer", task="T2", revision=1, to="maker", scope="Next bounded work")
        with self.assertRaisesRegex(ManagementError, "accepted active"):
            self.run_command("handoff-integrate", handoff="H1", revision=2, successor="T2")
        self.run_command("task-accept", token=maker, task="T2", revision=2)
        self.run_command("handoff-integrate", handoff="H1", revision=2, successor="T2")
        self.assertEqual(self.query("handoffs")[0]["successor_task_id"], "T2")

    def test_closure_with_owned_blocker(self):
        self.delivery()
        self.run_command("handoff-verify", handoff="H1", revision=1)
        with self.assertRaises(ManagementError):
            self.run_command("handoff-integrate", handoff="H1", revision=2, blocker_owner="maker", condition=" ")
        self.run_command("handoff-integrate", handoff="H1", revision=2, blocker_owner="maker", condition="Await new assignment")
        self.assertEqual(self.query("handoffs")[0]["closure"], "blocked")

    def test_exact_bytes_required_at_verification_and_integration(self):
        self.delivery()
        path = self.root / "delivery.txt"
        original = path.read_bytes()
        path.write_text("Changed after submission")
        with self.assertRaisesRegex(ManagementError, "bytes changed"):
            self.run_command("handoff-verify", handoff="H1", revision=1)
        self.assertEqual(self.query("handoffs")[0]["state"], "submitted")
        path.write_bytes(original)
        self.run_command("handoff-verify", handoff="H1", revision=1)
        path.unlink()
        with self.assertRaisesRegex(ManagementError, "missing"):
            self.run_command("handoff-integrate", handoff="H1", revision=2, closed=True)

    def test_paths_scope_and_database_root_anchor(self):
        self.project()
        maker = self.member()
        self.assignment(token=maker)
        with self.assertRaisesRegex(ManagementError, "outside the assignment"):
            self.run_command("artifact-add", token=maker, task="T1", revision=3, id="A1", path="other.txt")
        for path in ("../escape", "/absolute", "a/../delivery.txt", "./delivery.txt", "a\\b"):
            with self.assertRaises(ManagementError):
                self.store._local_path(path)
        with tempfile.TemporaryDirectory() as elsewhere:
            self.root.joinpath("escape").symlink_to(elsewhere, target_is_directory=True)
            with self.assertRaisesRegex(ManagementError, "escapes"):
                self.store._local_path("escape/output.txt")
            wrong = Store(self.db, Path(elsewhere))
            with self.assertRaisesRegex(ManagementError, "anchor"):
                wrong.query(self.owner, "new-film", "tasks")

    def test_approval_is_operator_only_scoped_and_immutable(self):
        maker = self.delivery()
        with self.assertRaisesRegex(ManagementError, "operator credential"):
            self.run_command("approval-record", token=maker, id="APR1", artifact="A1", purpose="composition", outcome="approved")
        self.run_command("approval-record", id="APR1", artifact="A1", purpose="composition", outcome="approved")
        self.run_command("approval-record", id="APR2", artifact="A1", purpose="composition", outcome="rejected", supersedes="APR1")
        self.assertEqual(len(self.query("approvals")), 2)
        self.run_command("decision-record", project="new-film", id="D1", title="First decision")
        self.run_command("decision-record", project="new-film", id="D2", title="Explicit correction", supersedes="D1")
        with sqlite3.connect(self.db) as c:
            for statement in ("DELETE FROM events", "UPDATE events SET reason='hidden'",
                              "DELETE FROM approvals", "UPDATE decisions SET title='changed'",
                              "UPDATE artifact_versions SET sha256='changed'"):
                with self.assertRaises(sqlite3.IntegrityError):
                    c.execute(statement)
        raw = self.db.read_bytes()
        self.assertNotIn(self.owner.encode(), raw)
        self.assertNotIn(maker.encode(), raw)

    def test_reassignment_does_not_adopt_old_outputs(self):
        self.project()
        maker = self.member()
        self.assignment(token=maker)
        (self.root / "delivery.txt").write_text("Original assignment")
        self.run_command("artifact-add", token=maker, task="T1", revision=3, id="A1", path="delivery.txt")
        self.run_command("task-block", task="T1", revision=3, owner="maker", condition="Replace scope")
        self.run_command("task-offer", task="T1", revision=4, to="maker", scope="New scope",
                         allowed_path=["other.txt"])
        self.run_command("task-accept", token=maker, task="T1", revision=5)
        with self.assertRaisesRegex(ManagementError, "belong to this assignment"):
            self.run_command("handoff-submit", token=maker, id="H1", task="T1", revision=6,
                             scope="Invalid reuse", limitations="Synthetic", artifact=["A1"],
                             check=[["test", "passed", "Original output only"]])
        self.assertEqual(self.query("handoffs"), [])

    def test_rejection_survives_missing_file_and_approvals_have_one_leaf(self):
        self.delivery()
        self.run_command("approval-record", id="P1", artifact="A1", purpose="test", outcome="approved")
        (self.root / "delivery.txt").unlink()
        self.run_command("approval-record", id="P2", artifact="A1", purpose="test", outcome="rejected", supersedes="P1")
        with self.assertRaisesRegex(ManagementError, "current leaf"):
            self.run_command("approval-record", id="P3", artifact="A1", purpose="test", outcome="rejected", supersedes="P1")
        with self.assertRaisesRegex(ManagementError, "explicitly superseded"):
            self.run_command("approval-record", id="P4", artifact="A1", purpose="test", outcome="rejected")
        self.assertEqual(len(self.query("approvals")), 2)

    def test_return_and_repair_preserve_original_handoff(self):
        maker = self.delivery()
        (self.root / "delivery.txt").write_text("Corrected synthetic delivery")
        self.run_command("handoff-return", handoff="H1", revision=1)
        self.assertEqual(self.query("handoffs")[0]["state"], "returned")
        self.assertEqual(self.query("tasks")[0]["revision"], 5)
        self.run_command("artifact-add", token=maker, task="T1", revision=5, id="A2",
                         path="delivery.txt", supersedes="A1")
        self.run_command("handoff-submit", token=maker, id="H2", task="T1", revision=5,
                         scope="Corrected output", limitations="No artistic review", artifact=["A2"],
                         check=[["readback", "passed", "Compared corrected bytes"]])
        self.run_command("handoff-verify", handoff="H2", revision=1)
        self.run_command("handoff-integrate", handoff="H2", revision=2, closed=True)
        self.assertEqual([h["state"] for h in self.query("handoffs")], ["returned", "integrated"])
        self.assertEqual(self.query("artifact_versions")[1]["supersedes"], "A1")

    def test_handoff_cannot_claim_another_tasks_outputs(self):
        maker = self.delivery()
        self.assignment(task="T2", token=maker, path="other.txt")
        with self.assertRaisesRegex(ManagementError, "belong to this assignment"):
            self.run_command("handoff-submit", token=maker, id="H2", task="T2", revision=3,
                             scope="Invalid", limitations="Test only", artifact=["A1"],
                             check=[["test", "not_run", "Explicitly not run"]])
        self.assertEqual(len(self.query("handoffs")), 1)

    def test_input_version_is_rechecked_before_acceptance(self):
        self.delivery()
        self.run_command("task-create", project="new-film", id="T2", title="Use precise input")
        self.run_command("task-offer", task="T2", revision=1, to="maker", scope="Review A1", input=["A1"])
        (self.root / "delivery.txt").write_text("Changed input")
        maker = credential(self.root / "maker.credential")
        with self.assertRaisesRegex(ManagementError, "bytes changed"):
            self.run_command("task-accept", token=maker, task="T2", revision=2)
        self.assertEqual(self.query("tasks")[1]["state"], "offered")

    def test_invalid_handoff_check_rolls_back_all_changes(self):
        self.project()
        maker = self.member()
        self.assignment(token=maker)
        (self.root / "delivery.txt").write_text("Fixture")
        self.run_command("artifact-add", token=maker, task="T1", revision=3, id="A1", path="delivery.txt")
        with self.assertRaises(sqlite3.IntegrityError):
            self.run_command("handoff-submit", token=maker, id="H1", task="T1", revision=3,
                             scope="Output", limitations="Synthetic", artifact=["A1"],
                             check=[["test", "invented", "Invalid status"]])
        self.assertEqual(self.query("handoffs"), [])
        self.assertEqual(self.query("tasks")[0]["state"], "active")

    def test_backup_restore_and_fail_closed_when_missing(self):
        self.delivery()
        backup = self.root / "backup.sqlite3"
        self.store.backup(self.owner, backup)
        restored = Store(backup, self.root)
        self.assertEqual(restored.query(self.owner, "new-film", "tasks"), self.query("tasks"))
        with sqlite3.connect(backup) as c:
            self.assertEqual(c.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(c.execute("PRAGMA foreign_key_check").fetchall(), [])
        with self.assertRaises(FileExistsError):
            self.store.backup(self.owner, backup)
        missing = self.root / "missing.sqlite3"
        with self.assertRaises(sqlite3.OperationalError):
            Store(missing, self.root).query(self.owner, "new-film", "tasks")
        self.assertFalse(missing.exists())

    def test_cli_and_credentials_never_echo_secret(self):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = main(["--db", str(self.db), "--root", str(self.root), "--credential", str(self.owner_file),
                         "project-create", "--project", "new-film", "--title", "Clean", "--request-id", "cli-1", "--reason", "Explicit test"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["after"]["id"], "new-film")
        self.assertNotIn(self.owner, output.getvalue() + errors.getvalue())
        self.owner_file.chmod(0o644)
        with self.assertRaisesRegex(ManagementError, "private"):
            credential(self.owner_file)


if __name__ == "__main__":
    unittest.main()
