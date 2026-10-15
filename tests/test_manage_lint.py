"""Checks for the read-only lint, resume and handoff subcommands of manage.py."""

from __future__ import annotations

import datetime as dt
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "manage.py"
FILM = "projects/film"
APPROVALS = {"pilot": True, "paidBatch": False, "finalPicture": False}


class CoherenceLintIntegrationTests(unittest.TestCase):
    def test_errors_and_acknowledged_warnings_keep_their_severity(self):
        spec = importlib.util.spec_from_file_location("manage_coherence", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        findings = {"items": [
            {"shotId": "S", "level": "ERROR", "code": "DURATION_REQUEST", "msg": "mismatch"},
            {"shotId": "S", "level": "WARN", "code": "CAMERA_MIXED", "msg": "review", "acknowledged": True},
            {"level": "INFO", "code": "INSPECTION_LIMIT", "msg": "partial"},
        ]}
        hard, advisory = [], []
        with mock.patch.object(module, "production_plan_report", side_effect=[{"errors": [], "status": "ok"}, findings]):
            module.lint_production_plan(ROOT, hard, advisory)
        self.assertEqual(len(hard), 1)
        self.assertIn("DURATION_REQUEST", hard[0])
        self.assertEqual(len(advisory), 1)
        self.assertIn("CAMERA_MIXED", advisory[0])
        self.assertIn("não é aprovação", advisory[0])

    def test_unconfigured_or_invalid_plan_does_not_load_coherence(self):
        spec = importlib.util.spec_from_file_location("manage_coherence", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for report in ({"errors": [], "status": "not_configured"}, {"errors": ["broken"], "status": "error"}):
            with mock.patch.object(module, "production_plan_report", return_value=report) as read:
                hard, advisory = [], []
                module.lint_production_plan(ROOT, hard, advisory)
                self.assertEqual(hard, report["errors"])
                self.assertEqual(advisory, [])
                read.assert_called_once_with(ROOT)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_workspace(root: Path) -> Path:
    """Create a minimal synthetic workspace with one film and return the film directory."""
    film = root / FILM
    (root / "AGENTS.md").write_text("# AGENTS\n", encoding="utf-8")
    write_json(
        root / "workspace.json",
        {
            "activeFilm": "film",
            "projects": [
                {
                    "id": "film",
                    "root": FILM,
                    "manifest": f"{FILM}/manifest.json",
                    "tasks": f"{FILM}/tasks/board.json",
                    "state": f"{FILM}/memory/STATE.md",
                }
            ],
        },
    )
    write_json(
        film / "manifest.json",
        {
            "approvals": dict(APPROVALS),
            "budget": {
                "verifiedBalanceSnapshot": 6981,
                "snapshotObservedDate": "2026-10-09",
                "snapshotIsLiveBalance": False,
            },
        },
    )
    write_json(
        film / "00_brief/approvals.json",
        {"creativeApprovals": dict(APPROVALS), "andreOnlyGates": ["likeness"]},
    )
    write_json(film / "00_brief/decisions/D01-identity.json", {"gate": "identity"})
    write_json(film / "00_brief/decisions/D02-table.json", {"id": "D02", "gate": "table"})
    write_json(
        film / "tasks/board.json",
        {
            "tasks": [
                {
                    "id": "T01",
                    "title": "Done",
                    "ownerRole": "producer",
                    "status": "completed",
                    "dependsOn": [],
                    "blocker": None,
                },
                {
                    "id": "T02",
                    "title": "Blocked properly",
                    "ownerRole": "editor",
                    "status": "blocked",
                    "dependsOn": ["T01"],
                    "blocker": "Awaiting Andre's likeness decision",
                },
                {
                    "id": "T03",
                    "title": "Ready",
                    "ownerRole": "qc",
                    "status": "ready",
                    "dependsOn": [],
                    "blocker": None,
                },
            ]
        },
    )
    (film / "memory").mkdir(parents=True, exist_ok=True)
    (film / "memory/STATE.md").write_text(
        "# Resume State\n\nFirst headline line.\n\n## Section\n", encoding="utf-8"
    )
    write_json(
        film / "memory/session-log.json",
        {"entries": [{"at": "2026-10-09T07:24:04-03:00"}, {"at": "2026-10-09T08:00:00-03:00"}]},
    )
    (film / "agents/handoffs").mkdir(parents=True, exist_ok=True)
    (film / "07_generations/plans").mkdir(parents=True, exist_ok=True)
    return film


def v2_handoff(root: Path, changed: list[Path]) -> dict[str, Any]:
    """Return a valid v2 handoff whose changedFiles and claims point at real files."""
    relative = [str(path.relative_to(root)) for path in changed]
    return {
        "schemaVersion": "2.0",
        "episode": "film",
        "agentRole": "editor",
        "assignment": "Test assignment",
        "contributorKind": "registry-role",
        "readFirst": ["AGENTS.md"],
        "baseFiles": [{"path": relative[0], "sha256Before": "0" * 64}],
        "changedFiles": [
            {"path": item, "sha256After": sha256(path), "reason": "created"}
            for item, path in zip(relative, changed)
        ],
        "claims": [
            {"statement": "File exists", "evidence": relative[0], "sha256": sha256(changed[0])}
        ],
        "verification": ["sha256sum compared"],
        "blockers": [],
        "andreOnlyGates": [],
        "proposedDecisions": [],
        "mistakes": [],
        "paidJobsSubmitted": 0,
        "canonicalStateChanged": False,
        "ingest": {"status": "pending", "by": None, "at": None},
        "nextActions": [{"role": "producer", "action": "ingest"}],
    }


class ManageCliMixin:
    def run_cli(self, root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), *arguments],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def run_json(self, root: Path, *arguments: str) -> tuple[int, dict[str, Any]]:
        result = self.run_cli(root, *arguments)
        if not result.stdout.strip():
            raise AssertionError(result.stderr)
        return result.returncode, json.loads(result.stdout)


class LintTests(ManageCliMixin, unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="manage-lint-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.film = build_workspace(self.root)

    def snapshot(self) -> dict[Path, bytes]:
        return {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}

    def test_clean_fixture_has_no_hard_findings_and_known_advisories(self) -> None:
        before = self.snapshot()
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 0, report)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["film"], "film")
        self.assertEqual(report["hard"], [])
        advisory = " ".join(report["advisory"])
        self.assertIn("R06", advisory)
        self.assertIn("current-plan", advisory)
        self.assertIn("mistakes.jsonl", advisory)
        self.assertEqual(before, self.snapshot())

    def test_lint_does_not_depend_on_validate(self) -> None:
        validate = self.run_cli(self.root, "validate")
        self.assertEqual(validate.returncode, 2)
        self.assertEqual(self.run_cli(self.root, "lint").returncode, 0)

    def test_manifest_approval_divergence_is_hard(self) -> None:
        manifest = json.loads((self.film / "manifest.json").read_text())
        manifest["approvals"]["pilot"] = False
        write_json(self.film / "manifest.json", manifest)
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 2)
        self.assertEqual(report["status"], "error")
        self.assertIn("approvals", " ".join(report["hard"]))

    def test_duplicate_and_legacy_decision_ids_are_hard(self) -> None:
        write_json(self.film / "00_brief/decisions/D01-duplicate.json", {"gate": "x"})
        write_json(
            self.film / "memory/decisions.json",
            {"decisions": [{"id": "LEGACY-D02"}, {"id": "D02"}]},
        )
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 2)
        hard = " ".join(report["hard"])
        self.assertIn("D01", hard)
        self.assertIn("D02", hard)
        self.assertNotIn("LEGACY-D02", hard)

    def test_handoff_ingest_and_hash_checks(self) -> None:
        deliverable = self.film / "docs/review.md"
        deliverable.parent.mkdir(parents=True)
        deliverable.write_text("review\n", encoding="utf-8")
        handoff = v2_handoff(self.root, [deliverable])
        write_json(self.film / "agents/handoffs/2026-10-10-good.json", handoff)
        write_json(
            self.film / "agents/handoffs/2026-10-09-legacy.json",
            {"schemaVersion": "1.0", "reviewStatus": "pending_producer_review"},
        )
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 0, report)
        advisory = " ".join(report["advisory"])
        self.assertIn("2 handoff", advisory)
        self.assertIn("2026-10-10-good.json", advisory)
        self.assertIn("2026-10-09-legacy.json", advisory)

        film_relative = dict(handoff)
        film_relative["changedFiles"] = [
            {"path": "docs/review.md", "sha256After": sha256(deliverable), "reason": "created"}
        ]
        write_json(self.film / "agents/handoffs/2026-10-10-good.json", film_relative)
        self.assertEqual(self.run_cli(self.root, "lint").returncode, 0)

        deliverable.write_text("changed\n", encoding="utf-8")
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 2)
        self.assertIn("2026-10-10-good.json", " ".join(report["hard"]))

        ingested = dict(film_relative)
        ingested["ingest"] = {"status": "ingested", "by": "producer", "at": "2026-10-10T10:00:00-03:00"}
        write_json(self.film / "agents/handoffs/2026-10-10-good.json", ingested)
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 0, report)
        self.assertNotIn("2026-10-10-good.json", " ".join(report["hard"]))
        deliverable.write_text("review\n", encoding="utf-8")

        missing = dict(handoff)
        missing["changedFiles"] = [
            {"path": "docs/absent.md", "sha256After": "0" * 64, "reason": "created"}
        ]
        missing["claims"] = []
        write_json(self.film / "agents/handoffs/2026-10-10-good.json", missing)
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 2)
        self.assertIn("absent.md", " ".join(report["hard"]))

    def test_current_plan_pointer(self) -> None:
        plan = self.film / "07_generations/plans/plan.md"
        plan.write_text("plan\n", encoding="utf-8")
        pointer = self.film / "07_generations/plans/current-plan.json"
        write_json(pointer, {"path": "07_generations/plans/plan.md", "sha256": sha256(plan)})
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 0, report)
        self.assertNotIn("current-plan", " ".join(report["advisory"]))

        write_json(pointer, {"path": "07_generations/plans/plan.md", "sha256": "f" * 64})
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 2)
        self.assertIn("current-plan", " ".join(report["hard"]))

        write_json(pointer, {"path": "07_generations/plans/gone.md", "sha256": "f" * 64})
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 2)
        self.assertIn("gone.md", " ".join(report["hard"]))

    def test_superseded_handoff_is_history_not_a_live_hash(self) -> None:
        deliverable = self.film / "docs/review.md"
        deliverable.parent.mkdir(parents=True)
        deliverable.write_text("review\n", encoding="utf-8")
        stale = v2_handoff(self.root, [deliverable])
        deliverable.write_text("changed\n", encoding="utf-8")
        write_json(self.film / "agents/handoffs/2026-10-10-stale.json", stale)
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 2)
        self.assertIn("2026-10-10-stale.json", " ".join(report["hard"]))

        successor = v2_handoff(self.root, [deliverable])
        successor["supersedes"] = ["2026-10-10-stale.json", "2026-10-10-missing.json"]
        write_json(self.film / "agents/handoffs/2026-10-11-successor.json", successor)
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 0, report)
        advisory = " ".join(report["advisory"])
        self.assertIn("2026-10-10-stale.json", advisory)
        self.assertIn("superseded", advisory)
        self.assertNotIn("2026-10-10-stale.json", " ".join(report["hard"]))
        self.assertNotIn("2026-10-10-missing.json", advisory)

    def test_mistakes_without_rules_are_advisory_after_seven_days(self) -> None:
        today = dt.date.today()  # noqa: DTZ011
        old = (today - dt.timedelta(days=10)).isoformat()
        recent = (today - dt.timedelta(days=1)).isoformat()
        lines = [
            {"id": "M01", "date": old, "rule_added": ""},
            {"id": "M02", "date": recent, "rule_added": ""},
            {"id": "M03", "date": old, "rule_added": "R10"},
        ]
        (self.film / "memory/mistakes.jsonl").write_text(
            "".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8"
        )
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 0, report)
        advisory = " ".join(report["advisory"])
        self.assertNotIn("mistakes.jsonl missing", advisory)
        self.assertIn("M01", advisory)
        self.assertNotIn("M02", advisory)
        self.assertNotIn("M03", advisory)

    def test_mixed_session_log_offsets_are_advisory(self) -> None:
        self.assertNotIn("offset", " ".join(self.run_json(self.root, "lint")[1]["advisory"]))
        write_json(
            self.film / "memory/session-log.json",
            {"entries": [{"at": "2026-10-09T07:24:04-03:00"}, {"at": "2026-10-09T11:00:00+00:00"}]},
        )
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 0)
        self.assertIn("offset", " ".join(report["advisory"]))

    def test_git_status_unavailable_outside_repository(self) -> None:
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 0)
        self.assertIn("git status unavailable", report["advisory"])

    def test_generic_blocker_with_completed_dependency_is_advisory(self) -> None:
        board = json.loads((self.film / "tasks/board.json").read_text())
        board["tasks"][1]["blocker"] = "Awaiting dependency completion and applicable approval"
        board["tasks"].append(
            {
                "id": "T04",
                "title": "No blocker text",
                "ownerRole": "qc",
                "status": "in_progress",
                "dependsOn": ["T01"],
                "blocker": None,
            }
        )
        board["tasks"].append(
            {
                "id": "T05",
                "title": "Generic but nothing done",
                "ownerRole": "qc",
                "status": "blocked",
                "dependsOn": ["T03"],
                "blocker": "Awaiting dependency completion and applicable approval",
            }
        )
        write_json(self.film / "tasks/board.json", board)
        code, report = self.run_json(self.root, "lint")
        self.assertEqual(code, 0, report)
        advisory = " ".join(report["advisory"])
        self.assertIn("T02", advisory)
        self.assertIn("T04", advisory)
        self.assertNotIn("T05", advisory)


class ResumeTests(ManageCliMixin, unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="manage-resume-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.film = build_workspace(self.root)

    def test_resume_digest_shape(self) -> None:
        deliverable = self.film / "docs/review.md"
        deliverable.parent.mkdir(parents=True)
        deliverable.write_text("review\n", encoding="utf-8")
        for name in ["2026-10-08-a.json", "2026-10-09-b.json", "2026-10-10-c.json"]:
            write_json(
                self.film / "agents/handoffs" / name,
                {"schemaVersion": "1.0", "reviewStatus": "pending_producer_review"},
            )
        handoff = v2_handoff(self.root, [deliverable])
        handoff["ingest"] = {
            "status": "ingested",
            "by": "producer",
            "at": "2026-10-10T10:00:00-03:00",
        }
        write_json(self.film / "agents/handoffs/2026-10-10-d.json", handoff)
        (self.film / "memory/mistakes.jsonl").write_text(
            json.dumps({"id": "M01", "date": "2026-10-01", "rule_added": ""}) + "\n"
            + json.dumps({"id": "M02", "date": "2026-10-01", "rule_added": "R01"}) + "\n",
            encoding="utf-8",
        )
        code, report = self.run_json(self.root, "resume")
        self.assertEqual(code, 0, report)
        self.assertEqual(report["activeFilm"], "film")
        self.assertEqual(
            report["readOrder"],
            [
                "AGENTS.md",
                "workspace.json",
                f"{FILM}/memory/STATE.md",
                f"{FILM}/manifest.json",
                f"{FILM}/tasks/board.json",
                f"{FILM}/00_brief/approvals.json",
                f"{FILM}/00_brief/decisions/",
                f"{FILM}/tasks/plans/workflow-map-v1.md",
            ],
        )
        self.assertEqual(report["stateHeadline"], "First headline line.")
        self.assertEqual(report["taskCounts"], {"completed": 1, "blocked": 1, "ready": 1})
        self.assertEqual(
            report["openTasks"],
            [
                {
                    "id": "T02",
                    "title": "Blocked properly",
                    "ownerRole": "editor",
                    "status": "blocked",
                    "blocker": "Awaiting Andre's likeness decision",
                }
            ],
        )
        self.assertEqual(report["creativeApprovals"], APPROVALS)
        self.assertEqual(report["andreOnlyGates"], ["likeness"])
        self.assertEqual(
            report["balance"], {"snapshot": 6981, "observedDate": "2026-10-09", "isLive": False}
        )
        self.assertEqual(
            report["recentHandoffs"],
            [
                {
                    "name": "2026-10-09-b.json",
                    "reviewStatus": "pending_producer_review",
                    "ingest": None,
                },
                {
                    "name": "2026-10-10-c.json",
                    "reviewStatus": "pending_producer_review",
                    "ingest": None,
                },
                {"name": "2026-10-10-d.json", "reviewStatus": None, "ingest": "ingested"},
            ],
        )
        self.assertEqual(report["openMistakes"], 1)
        lint_advisory = self.run_json(self.root, "lint")[1]["advisory"]
        self.assertEqual(report["lint"], {"hard": 0, "advisory": len(lint_advisory)})

    def test_resume_without_optional_files(self) -> None:
        code, report = self.run_json(self.root, "resume")
        self.assertEqual(code, 0, report)
        self.assertEqual(report["openMistakes"], 0)
        self.assertEqual(report["recentHandoffs"], [])


class HandoffTests(ManageCliMixin, unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="manage-handoff-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.film = build_workspace(self.root)
        self.deliverable = self.film / "docs/review.md"
        self.deliverable.parent.mkdir(parents=True)
        self.deliverable.write_text("review\n", encoding="utf-8")
        self.path = self.film / "agents/handoffs/2026-10-10-test.json"
        self.handoff = v2_handoff(self.root, [self.deliverable])
        write_json(self.path, self.handoff)

    def test_check_valid_v2_handoff(self) -> None:
        code, report = self.run_json(self.root, "handoff", "check", str(self.path))
        self.assertEqual(code, 0, report)
        self.assertEqual(
            report, {"status": "ok", "version": "2.0", "errors": [], "advisory": []}
        )

    def test_check_reports_missing_fields_and_hash_mismatch(self) -> None:
        broken = dict(self.handoff)
        del broken["readFirst"]
        broken["contributorKind"] = "someone"
        broken["verification"] = []
        broken["blockers"] = [{"description": "x"}]
        broken["paidJobsSubmitted"] = "0"
        broken["ingest"] = {"status": "done"}
        broken["nextActions"] = []
        broken["claims"] = [
            {"statement": "s", "evidence": "docs/review.md", "sha256": "0" * 64}
        ]
        write_json(self.path, broken)
        code, report = self.run_json(self.root, "handoff", "check", str(self.path))
        self.assertEqual(code, 2)
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["version"], "2.0")
        errors = " ".join(report["errors"])
        for token in [
            "readFirst",
            "contributorKind",
            "verification",
            "blockers",
            "paidJobsSubmitted",
            "ingest",
            "nextActions",
            "claims",
        ]:
            self.assertIn(token, errors)

    def test_check_accepts_stage_complete_instead_of_next_actions(self) -> None:
        done = dict(self.handoff)
        done["nextActions"] = []
        done["stageComplete"] = True
        done["stageCompleteReason"] = "Phase closed"
        write_json(self.path, done)
        self.assertEqual(self.run_cli(self.root, "handoff", "check", str(self.path)).returncode, 0)
        del done["stageCompleteReason"]
        write_json(self.path, done)
        code, report = self.run_json(self.root, "handoff", "check", str(self.path))
        self.assertEqual(code, 2)
        self.assertIn("stageCompleteReason", " ".join(report["errors"]))

    def test_check_legacy_handoff_is_advisory_only(self) -> None:
        legacy = self.film / "agents/handoffs/2026-10-09-legacy.json"
        write_json(
            legacy,
            {
                "schemaVersion": "1.0",
                "episode": "film",
                "agentRole": "editor",
                "changedFiles": [],
                "reviewStatus": "pending_producer_review",
            },
        )
        code, report = self.run_json(self.root, "handoff", "check", str(legacy))
        self.assertEqual(code, 0, report)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["version"], "legacy")
        self.assertEqual(report["errors"], [])
        advisory = " ".join(report["advisory"])
        self.assertIn("readFirst", advisory)
        self.assertIn("ingest", advisory)
        self.assertNotIn("episode", advisory)

    def test_ingest_writes_only_the_ingest_object(self) -> None:
        before = json.loads(self.path.read_text(encoding="utf-8"))
        others = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        del others[self.path]
        code, report = self.run_json(
            self.root, "handoff", "ingest", str(self.path), "--by", "producer"
        )
        self.assertEqual(code, 0, report)
        self.assertEqual(report["status"], "ok")
        self.assertTrue(report["ingested"])
        text = self.path.read_text(encoding="utf-8")
        self.assertTrue(text.endswith("}\n"))
        after = json.loads(text)
        self.assertEqual(after["ingest"]["status"], "ingested")
        self.assertEqual(after["ingest"]["by"], "producer")
        stamp = dt.datetime.fromisoformat(after["ingest"]["at"])
        self.assertIsNotNone(stamp.tzinfo)
        expected = dict(before)
        expected["ingest"] = after["ingest"]
        self.assertEqual(after, expected)
        self.assertEqual(list(after), list(before))
        self.assertEqual(
            others,
            {
                path: path.read_bytes()
                for path in self.root.rglob("*")
                if path.is_file() and path != self.path
            },
        )

        code, report = self.run_json(
            self.root, "handoff", "ingest", str(self.path), "--by", "producer"
        )
        self.assertEqual(code, 2)
        self.assertIn("already ingested", report["errors"])
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8")), after)

    def test_check_and_ingest_refuse_paths_outside_the_handoff_folder(self) -> None:
        approvals = self.film / "00_brief/approvals.json"
        original = approvals.read_bytes()
        for arguments in [
            ("handoff", "check", str(approvals)),
            ("handoff", "ingest", str(approvals), "--by", "producer"),
        ]:
            code, report = self.run_json(self.root, *arguments)
            self.assertEqual(code, 2, report)
            self.assertIn("agents/handoffs", " ".join(report["errors"]))
        self.assertEqual(approvals.read_bytes(), original)

    def test_ingest_refuses_invalid_handoff_without_writing(self) -> None:
        self.deliverable.write_text("changed\n", encoding="utf-8")
        original = self.path.read_bytes()
        code, report = self.run_json(
            self.root, "handoff", "ingest", str(self.path), "--by", "producer"
        )
        self.assertEqual(code, 2)
        self.assertEqual(report["status"], "error")
        self.assertNotIn("ingested", report)
        self.assertEqual(self.path.read_bytes(), original)


class RealWorkspaceTests(ManageCliMixin, unittest.TestCase):
    def test_resume_runs_against_real_root(self) -> None:
        code, report = self.run_json(ROOT, "resume")
        self.assertEqual(code, 0)
        self.assertEqual(report["activeFilm"], "andre-time-travel")
        self.assertEqual(
            set(report),
            {
                "activeFilm",
                "readOrder",
                "stateHeadline",
                "taskCounts",
                "openTasks",
                "creativeApprovals",
                "andreOnlyGates",
                "balance",
                "recentHandoffs",
                "openMistakes",
                "lint",
            },
        )
        self.assertEqual(report["balance"]["isLive"], False)

    def test_lint_runs_against_real_root(self) -> None:
        result = self.run_cli(ROOT, "lint")
        self.assertIn(result.returncode, {0, 2}, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["film"], "andre-time-travel")
        self.assertEqual(set(report), {"status", "hard", "advisory", "film"})
        self.assertIn("R06", " ".join(report["advisory"]))


if __name__ == "__main__":
    unittest.main()
