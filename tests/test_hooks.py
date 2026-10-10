"""Dry-run tests for the film gate hooks under .claude/hooks (cleanup plan Phase 6)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".claude" / "hooks"
FILM = "projects/test-film"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(fixture: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *arguments],
        cwd=fixture,
        check=True,
        capture_output=True,
        timeout=20,
    )


def build_fixture(fixture: Path) -> None:
    (fixture / "workspace.json").write_text(
        json.dumps(
            {
                "activeFilm": "test-film",
                "projects": [{"id": "test-film", "root": FILM}],
            }
        ),
        encoding="utf-8",
    )
    film = fixture / FILM
    for relative in [
        "logs",
        "agents/handoffs",
        "03_bibles",
        "tasks",
        "memory",
        "00_brief/decisions",
        "07_generations/originals",
        "07_generations/requests/shot-a",
        "08_edit/reviews",
    ]:
        (film / relative).mkdir(parents=True, exist_ok=True)
    (film / "tasks/board.json").write_text('{"tasks": []}\n', encoding="utf-8")
    (film / "memory/STATE.md").write_text("# state\n", encoding="utf-8")
    (film / "credit-ledger.csv").write_text(
        "entry_id,recorded_at,provider,generation_id,shot_id,take_id,credits_consumed,"
        "charge_status,balance_after,authorization_ref,notes\n"
        "L001,2026-10-09T07:43:57-03:00,Kling,JOBDONE123456,G-01,,20,status COMPLETED,"
        "7721,APR-X,\"note\"\n",
        encoding="utf-8",
    )
    git(fixture, "init", "-q")
    git(fixture, "add", "-A")
    git(fixture, "commit", "-q", "-m", "base")


def write_handoff(fixture: Path, name: str, **overrides: object) -> Path:
    film = fixture / FILM
    changed = film / "03_bibles/new-bible-v2.md"
    changed.parent.mkdir(parents=True, exist_ok=True)
    if not changed.exists():
        changed.write_text("bible\n", encoding="utf-8")
    document: dict[str, object] = {
        "schemaVersion": "2.0",
        "episode": "test-film",
        "agentRole": "continuity",
        "assignment": "test",
        "contributorKind": "registry-role",
        "readFirst": ["AGENTS.md"],
        "baseFiles": [],
        "changedFiles": [
            {
                "path": f"{FILM}/03_bibles/new-bible-v2.md",
                "sha256After": sha256(changed),
                "reason": "test",
            }
        ],
        "claims": [],
        "verification": ["python3 -m unittest"],
        "nextActions": [{"role": "producer", "action": "integrate"}],
        "blockers": [],
        "andreOnlyGates": [],
        "proposedDecisions": [],
        "mistakes": [],
        "paidJobsSubmitted": 0,
        "canonicalStateChanged": False,
        "ingest": {"status": "pending", "by": None, "at": None},
    }
    document.update(overrides)
    path = film / "agents/handoffs" / name
    path.write_text(json.dumps(document, indent=2), encoding="utf-8")
    return path


class HookTestCase(unittest.TestCase):
    def setUp(self) -> None:
        scratch = Path(os.environ.get("TMPDIR", tempfile.gettempdir()))
        self._temporary = tempfile.TemporaryDirectory(prefix="movies-hooks-", dir=scratch)
        self.fixture = Path(self._temporary.name) / "workspace"
        self.fixture.mkdir()
        build_fixture(self.fixture)
        self.film = self.fixture / FILM

    def tearDown(self) -> None:
        self._temporary.cleanup()

    def run_hook(
        self,
        script: str,
        payload: dict[str, object],
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("MOVIES_")
        }
        environment["CLAUDE_PROJECT_DIR"] = str(self.fixture)
        environment.update(env or {})
        return subprocess.run(
            [sys.executable, str(HOOKS / script)],
            input=json.dumps(payload),
            cwd=self.fixture,
            env=environment,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )

    def write_payload(self, tool: str, **tool_input: object) -> dict[str, object]:
        return {
            "hook_event_name": "PreToolUse",
            "tool_name": tool,
            "tool_input": tool_input,
            "cwd": str(self.fixture),
        }

    def log_lines(self) -> list[dict[str, object]]:
        path = self.film / "logs/hooks.jsonl"
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class CanonicalGuardTests(HookTestCase):
    def test_lane_write_to_board_is_denied_and_logged(self) -> None:
        result = self.run_hook(
            "canonical-guard.py", self.write_payload("Write", file_path=f"{FILM}/tasks/board.json")
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("producer", result.stderr)
        self.assertEqual(self.log_lines()[-1]["decision"], "deny")

    def test_producer_write_to_board_is_allowed(self) -> None:
        result = self.run_hook(
            "canonical-guard.py",
            self.write_payload("Edit", file_path=str(self.film / "tasks/board.json")),
            env={"MOVIES_PRODUCER_LANE": "1"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_lane_write_to_bible_is_allowed(self) -> None:
        result = self.run_hook(
            "canonical-guard.py", self.write_payload("Write", file_path=f"{FILM}/03_bibles/x-v2.md")
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_path_reserved_by_another_lane_is_denied(self) -> None:
        stub = self.fixture / "status-stub.py"
        stub.write_text(
            "import json; print(json.dumps({'reservations': [{'participant': 'codex-edit-qc',"
            " 'paths': ['projects/test-film/08_edit/reviews/']}]}))\n",
            encoding="utf-8",
        )
        result = self.run_hook(
            "canonical-guard.py",
            self.write_payload("Write", file_path=f"{FILM}/08_edit/reviews/findings.md"),
            env={
                "MOVIES_PARLEY_STATUS_CMD": f"{sys.executable} {stub}",
                "MOVIES_LANE_NAME": "claude-research",
            },
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("codex-edit-qc", result.stderr)


class MediaGuardTests(HookTestCase):
    def test_destructive_command_on_media_folder_is_denied(self) -> None:
        for command in [
            "rm -rf projects/test-film/07_generations/originals",
            "git reset --hard HEAD -- projects/test-film/08_edit",
            "mv projects/test-film/02_references/andre /tmp/x",
            "git clean -fdx projects/test-film/05_storyboard",
        ]:
            result = self.run_hook("media-guard.py", self.write_payload("Bash", command=command))
            self.assertEqual(result.returncode, 2, command)

    def test_read_only_command_is_allowed(self) -> None:
        for command in ["ls projects/test-film/07_generations", "rm -f /tmp/scratch.txt"]:
            result = self.run_hook("media-guard.py", self.write_payload("Bash", command=command))
            self.assertEqual(result.returncode, 0, command)


class KlingPreflightTests(HookTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request_dir = self.film / "07_generations/requests/shot-a"
        self.request = self.request_dir / "request.json"
        self.request.write_text(
            json.dumps({"model": "kling-image-o1", "images": ["a.png", "b.png"]}),
            encoding="utf-8",
        )
        self.scope = self.request_dir / "scope.json"
        self.valid_scope = {
            "ceiling": 23,
            "grantedBy": "Andre Athar (chat, direct)",
            "balanceBefore": 5813,
            "balanceTimestamp": datetime.now(timezone.utc).isoformat(),
            "requestSha256": sha256(self.request),
            "modelInputSlots": 2,
        }
        self.command = f"python3 scripts/kling_batch.py --submit-only --spec {self.request}"

    def submit(self, producer: bool = True) -> subprocess.CompletedProcess[str]:
        env = {"MOVIES_PRODUCER_LANE": "1"} if producer else {}
        return self.run_hook("kling-preflight.py", self.write_payload("Bash", command=self.command), env)

    def test_valid_scope_passes(self) -> None:
        self.scope.write_text(json.dumps(self.valid_scope), encoding="utf-8")
        result = self.submit()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unrelated_command_is_ignored(self) -> None:
        result = self.run_hook("kling-preflight.py", self.write_payload("Bash", command="ls"))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_scope_fields_are_denied(self) -> None:
        for field in self.valid_scope:
            scope = dict(self.valid_scope)
            del scope[field]
            self.scope.write_text(json.dumps(scope), encoding="utf-8")
            result = self.submit()
            self.assertEqual(result.returncode, 2, field)
            self.assertIn(field, result.stderr)

    def test_stale_balance_relayed_grant_and_schema_overflow_are_denied(self) -> None:
        stale = dict(self.valid_scope)
        stale["balanceTimestamp"] = (
            datetime.now(timezone.utc) - timedelta(minutes=16)
        ).isoformat()
        relayed = dict(self.valid_scope)
        relayed["grantedBy"] = "relayed via Grok Architect Bot"
        overflow = dict(self.valid_scope)
        overflow["modelInputSlots"] = 1
        wrong_hash = dict(self.valid_scope)
        wrong_hash["requestSha256"] = "0" * 64
        for name, scope in [
            ("stale", stale),
            ("relayed", relayed),
            ("overflow", overflow),
            ("hash", wrong_hash),
        ]:
            self.scope.write_text(json.dumps(scope), encoding="utf-8")
            result = self.submit()
            self.assertEqual(result.returncode, 2, name)

    def test_lane_without_kling_submit_is_denied(self) -> None:
        self.scope.write_text(json.dumps(self.valid_scope), encoding="utf-8")
        result = self.submit(producer=False)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("kling:submit", result.stderr)


class NoRetryTests(HookTestCase):
    def test_resume_of_terminal_job_is_denied(self) -> None:
        command = "python3 scripts/kling_batch.py --resume JOBDONE123456"
        result = self.run_hook("no-retry.py", self.write_payload("Bash", command=command))
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_resume_of_unknown_job_is_allowed(self) -> None:
        command = "python3 scripts/kling_batch.py --resume JOBNEW987654"
        result = self.run_hook("no-retry.py", self.write_payload("Bash", command=command))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_submit_of_plan_with_recorded_job_is_denied(self) -> None:
        spec = self.film / "07_generations/requests/plan.json"
        spec.write_text(
            json.dumps({"jobs": [{"id": "G-01", "generation_id": "JOBDONE123456"}]}),
            encoding="utf-8",
        )
        command = f"python3 scripts/kling_batch.py --submit-only --spec {spec}"
        result = self.run_hook("no-retry.py", self.write_payload("Bash", command=command))
        self.assertEqual(result.returncode, 2, result.stderr)


class StopHookTests(HookTestCase):
    def stop_payload(self, active: bool = False) -> dict[str, object]:
        return {
            "hook_event_name": "Stop",
            "stop_hook_active": active,
            "cwd": str(self.fixture),
        }

    def test_edits_without_handoff_block_the_stop_once(self) -> None:
        (self.film / "03_bibles/new-bible-v2.md").write_text("bible\n", encoding="utf-8")
        result = self.run_hook("handoff-check.py", self.stop_payload())
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("handoff", result.stderr)
        again = self.run_hook("handoff-check.py", self.stop_payload(active=True))
        self.assertEqual(again.returncode, 0, again.stderr)

    def test_valid_handoff_allows_the_stop(self) -> None:
        write_handoff(self.fixture, "2026-10-10-continuity-test.json")
        result = self.run_hook("handoff-check.py", self.stop_payload())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_handoff_with_changed_hash_or_missing_verification_blocks(self) -> None:
        path = write_handoff(self.fixture, "2026-10-10-continuity-test.json")
        (self.film / "03_bibles/new-bible-v2.md").write_text("edited after\n", encoding="utf-8")
        result = self.run_hook("handoff-check.py", self.stop_payload())
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("sha256", result.stderr)
        (self.film / "03_bibles/new-bible-v2.md").write_text("bible\n", encoding="utf-8")
        write_handoff(self.fixture, path.name, verification=[])
        result = self.run_hook("handoff-check.py", self.stop_payload())
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("verification", result.stderr)

    def test_no_edits_allows_the_stop(self) -> None:
        result = self.run_hook("handoff-check.py", self.stop_payload())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_successor_check_requires_next_action_or_stage_end(self) -> None:
        write_handoff(self.fixture, "2026-10-10-continuity-test.json", nextActions=[])
        result = self.run_hook("successor-check.py", self.stop_payload())
        self.assertEqual(result.returncode, 2, result.stderr)
        write_handoff(
            self.fixture,
            "2026-10-10-continuity-test.json",
            nextActions=[],
            stageComplete=True,
            stageCompleteReason="archive delivered",
        )
        result = self.run_hook("successor-check.py", self.stop_payload())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_zero_face_gate_requires_log_for_reviewed_media(self) -> None:
        clip = self.film / "07_generations/originals/G-01-take.mp4"
        clip.write_bytes(b"\x00")
        claims = [{"statement": "reviewed", "evidence": f"{FILM}/07_generations/originals/G-01-take.mp4", "sha256": sha256(clip)}]
        write_handoff(self.fixture, "2026-10-10-qc-test.json", agentRole="qc", claims=claims)
        result = self.run_hook("zero-face-gate.py", self.stop_payload(), env={"MOVIES_LANE_ROLE": "qc"})
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("zero-face-log.json", result.stderr)
        (clip.parent / "zero-face-log.json").write_text(
            json.dumps({"files": [clip.name], "framesInspected": 120, "reflectionsChecked": True}),
            encoding="utf-8",
        )
        result = self.run_hook("zero-face-gate.py", self.stop_payload(), env={"MOVIES_LANE_ROLE": "qc"})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_zero_face_gate_ignores_non_review_roles(self) -> None:
        clip = self.film / "07_generations/originals/G-01-take.mp4"
        clip.write_bytes(b"\x00")
        claims = [{"statement": "noted", "evidence": f"{FILM}/07_generations/originals/G-01-take.mp4", "sha256": sha256(clip)}]
        write_handoff(self.fixture, "2026-10-10-historian-test.json", agentRole="historian", claims=claims)
        result = self.run_hook("zero-face-gate.py", self.stop_payload(), env={"MOVIES_LANE_ROLE": "historian"})
        self.assertEqual(result.returncode, 0, result.stderr)


class MistakeCaptureTests(HookTestCase):
    def test_failed_command_appends_a_draft_entry(self) -> None:
        payload = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "python3 scripts/kling_batch.py --resume X"},
            "tool_response": {"stdout": "", "stderr": "KeyError: 'works'", "exit_code": 1},
            "cwd": str(self.fixture),
        }
        result = self.run_hook("mistake-capture.py", payload, env={"MOVIES_LANE_NAME": "codex-edit-qc"})
        self.assertEqual(result.returncode, 0, result.stderr)
        drafts = (self.film / "logs/mistakes-draft.jsonl").read_text(encoding="utf-8").splitlines()
        entry = json.loads(drafts[-1])
        self.assertEqual(entry["lane"], "codex-edit-qc")
        self.assertIn("KeyError", entry["error"])
        self.assertEqual(entry["solution"], "")

    def test_successful_command_writes_nothing(self) -> None:
        payload = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "ls"},
            "tool_response": {"stdout": "x", "stderr": "", "exit_code": 0},
            "cwd": str(self.fixture),
        }
        result = self.run_hook("mistake-capture.py", payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.film / "logs/mistakes-draft.jsonl").exists())

    def test_layer_two_denial_also_drafts_a_mistake(self) -> None:
        self.run_hook(
            "canonical-guard.py", self.write_payload("Write", file_path=f"{FILM}/tasks/board.json")
        )
        drafts = (self.film / "logs/mistakes-draft.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertIn("canonical-guard", json.loads(drafts[-1])["detected_by"])


class SettingsTests(unittest.TestCase):
    def test_settings_register_every_hook_script(self) -> None:
        settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
        commands = [
            hook["command"]
            for event in settings["hooks"].values()
            for group in event
            for hook in group["hooks"]
        ]
        for script in sorted(HOOKS.glob("*.py")):
            if script.name.startswith("_"):
                continue
            self.assertTrue(any(script.name in command for command in commands), script.name)
        for command in commands:
            self.assertIn("$CLAUDE_PROJECT_DIR", command)


if __name__ == "__main__":
    unittest.main()
