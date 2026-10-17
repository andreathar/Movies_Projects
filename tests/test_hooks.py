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

    def test_nested_manifest_and_decision_lookalikes_are_allowed(self) -> None:
        for path in [
            f"{FILM}/05_storyboard/keyframes/detail-studies-v1/manifest.json",
            f"{FILM}/07_generations/downloads/v1/manifest.json",
            f"{FILM}/08_edit/reviews/galileo/decisions/notes.md",
            f"{FILM}/03_bibles/../03_bibles/x-v2.md",
        ]:
            result = self.run_hook("canonical-guard.py", self.write_payload("Write", file_path=path))
            self.assertEqual(result.returncode, 0, path)

    def test_canonical_path_outside_the_worktree_is_denied_by_suffix(self) -> None:
        outside = "/mnt/base-checkout/projects/andre-time-travel/tasks/board.json"
        result = self.run_hook("canonical-guard.py", self.write_payload("Write", file_path=outside))
        self.assertEqual(result.returncode, 2, result.stderr)
        scratch = "/tmp/scratch/notes.md"
        result = self.run_hook("canonical-guard.py", self.write_payload("Write", file_path=scratch))
        self.assertEqual(result.returncode, 0, result.stderr)


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

    def test_destructive_command_without_a_named_folder_is_denied(self) -> None:
        for command in [
            "git clean -fdx",
            "git reset --hard",
            "/bin/rm -rf projects/test-film/07_generations",
            "rm -rf projects/test-film",
            "find projects/test-film/07_generations -name '*.png' -delete",
            "rsync -a --delete /tmp/x/ projects/test-film/08_edit/",
        ]:
            result = self.run_hook("media-guard.py", self.write_payload("Bash", command=command))
            self.assertEqual(result.returncode, 2, command)

    def test_read_only_command_is_allowed(self) -> None:
        for command in [
            "ls projects/test-film/07_generations",
            "rm -f /tmp/scratch.txt",
            "rm -f /tmp/a; ls projects/test-film/07_generations",
            "git restore --staged projects/test-film/00_brief/approvals.json",
            "git status --short -- projects/test-film/08_edit",
        ]:
            result = self.run_hook("media-guard.py", self.write_payload("Bash", command=command))
            self.assertEqual(result.returncode, 0, command)


class KlingPreflightTests(HookTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request_dir = self.film / "07_generations/requests/shot-a"
        self.request = self.request_dir / "request.json"
        self.write_spec([["a.png", "b.png"]])
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

    def write_spec(self, image_lists: list[list[str]]) -> None:
        jobs = [
            {
                "job": f"G-0{index + 1}-test",
                "tool": "image_to_image",
                "model": "kling-image-o1",
                "auth": "APR-X",
                "note": "",
                "args": {},
                "images": images,
                "prompt": "p",
            }
            for index, images in enumerate(image_lists)
        ]
        self.request.write_text(json.dumps(jobs), encoding="utf-8")

    def submit(self, producer: bool = True, command: str | None = None) -> subprocess.CompletedProcess[str]:
        env = {"MOVIES_PRODUCER_LANE": "1"} if producer else {}
        payload = self.write_payload("Bash", command=command or self.command)
        return self.run_hook("kling-preflight.py", payload, env)

    def test_valid_scope_passes(self) -> None:
        self.scope.write_text(json.dumps(self.valid_scope), encoding="utf-8")
        result = self.submit()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unrelated_and_read_only_commands_are_ignored(self) -> None:
        for command in [
            "ls",
            "grep -rn text_to_video skills/kling-cli/SKILL.md",
            f"python3 scripts/kling_batch.py --resume G-01-test",
            "kling query_tasks --id abc",
        ]:
            result = self.run_hook("kling-preflight.py", self.write_payload("Bash", command=command))
            self.assertEqual(result.returncode, 0, command)

    def test_plain_read_only_mentions_are_not_submissions(self) -> None:
        for command in [
            "grep -n scope scripts/kling_batch.py",
            "rg kling_batch.py docs",
            "sed -n '1,30p' scripts/kling_batch.py",
            "cat scripts/kling_batch.py",
            "head -n 10 scripts/kling_batch.py",
            "echo scripts/kling_batch.py",
        ]:
            for hook in ("kling-preflight.py", "no-retry.py"):
                with self.subTest(command=command, hook=hook):
                    result = self.run_hook(hook, self.write_payload("Bash", command=command))
                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_ambiguous_wrapped_chained_and_executable_reads_stay_denied(self) -> None:
        self.scope.write_text(json.dumps(self.valid_scope), encoding="utf-8")
        for command in [
            "grep scope scripts/kling_batch.py; python3 scripts/kling_batch.py --submit-only",
            "python3 scripts/kling_batch.py --resume DONE && kling text_to_video",
            "python3 scripts/kling_batch.py --resume DONE\nkling text_to_video",
            "bash -c 'python3 scripts/kling_batch.py --resume DONE'",
            "env FOO=1 python3 scripts/kling_batch.py --resume DONE",
            "sed -n '1e' scripts/kling_batch.py",
            "sed -i 's/a/b/' scripts/kling_batch.py",
            "rg --pre=anything kling_batch.py docs",
            "echo $(python3 scripts/kling_batch.py --submit-only)",
            "echo `python3 scripts/kling_batch.py --submit-only`",
            "python3 scripts/kling_batch.py --resume DONE --submit-only",
            "kling generate create unknown_model",
            "kling unknown_operation",
            "env FOO=1 kling text_to_video --prompt x",
        ]:
            for producer in (False, True):
                with self.subTest(command=command, producer=producer):
                    result = self.submit(producer=producer, command=command)
                    self.assertEqual(result.returncode, 2, result.stderr)

    def test_default_batch_mode_is_a_paid_submission(self) -> None:
        self.scope.write_text(json.dumps(self.valid_scope), encoding="utf-8")
        default_mode = f"python3 scripts/kling_batch.py --spec {self.request}"
        self.assertEqual(self.submit(producer=False, command=default_mode).returncode, 2)
        self.assertEqual(self.submit(producer=True, command=default_mode).returncode, 0)

    def test_list_spec_image_count_is_checked_per_selected_job(self) -> None:
        self.write_spec([["a.png"], ["a.png", "b.png", "c.png"]])
        scope = dict(self.valid_scope)
        scope["requestSha256"] = sha256(self.request)
        self.scope.write_text(json.dumps(scope), encoding="utf-8")
        base = f"python3 scripts/kling_batch.py --submit-only --spec {self.request}"
        self.assertEqual(self.submit(command=f"{base} --only G-01-test").returncode, 0)
        self.assertEqual(self.submit(command=f"{base} --only G-02-test").returncode, 2)
        self.assertEqual(self.submit(command=f"python3 scripts/kling_batch.py --spec {self.request}").returncode, 2)

    def test_unbalanced_quote_and_naive_timestamp_are_denied(self) -> None:
        self.scope.write_text(json.dumps(self.valid_scope), encoding="utf-8")
        self.assertEqual(self.submit(command=f"{self.command}  # don't retry").returncode, 0)
        result = self.submit(command=f'{self.command} --only "G-01-test')
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("quot", result.stderr)
        naive = dict(self.valid_scope)
        naive["balanceTimestamp"] = datetime.now().replace(tzinfo=None).isoformat()
        self.scope.write_text(json.dumps(naive), encoding="utf-8")
        result = self.submit()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("offset", result.stderr)

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


class HiggsfieldGateTests(HookTestCase):
    SCOPE = "projects/test-film/00_brief/higgsfield-scope.json"

    def write_scope(self, **overrides: object) -> None:
        scope: dict[str, object] = {
            "ceiling": 40,
            "grantedBy": "Andre direct, chat 2026-10-17",
            "balanceBefore": 847,
            "balanceTimestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            "jobTypes": ["nano_banana_2"],
            "allowedOperations": ["generate:create"],
            "uploadScope": "none",
            "commandSha256": hashlib.sha256(json.dumps(
                ["generate", "create", "nano_banana_2", "--prompt", "x"],
                ensure_ascii=False, separators=(",", ":"),
            ).encode()).hexdigest(),
        }
        scope.update(overrides)
        path = self.fixture / self.SCOPE
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(scope), encoding="utf-8")

    def bash(self, command: str, producer: bool = False) -> subprocess.CompletedProcess[str]:
        env = {"MOVIES_PRODUCER_LANE": "1"} if producer else None
        return self.run_hook("higgsfield-gate.py", self.write_payload("Bash", command=command), env)

    def test_read_only_and_unrelated_commands_pass_for_every_lane(self) -> None:
        for command in [
            "higgsfield account status",
            "higgsfield --json generate cost nano_banana_2 --prompt 'a quiet table'",
            "higgsfield generate wait 0f1e2d3c",
            "higgsfield model list --video",
            "higgsfield preset list soul-v2 --query create",
            "higgsfield project --workspace w1 list",
            "higgsfield marketing-studio avatars list",
            "higgsfield generate create --help",
            "higgsfield",
            "cd /tmp && timeout 20 higgsfield account status",
            "ls ~/.claude/skills/higgsfield-generate && grep -r higgsfield docs",
            "echo higgsfield generate create nano_banana_2",
            "hf download org/model",
        ]:
            with self.subTest(command=command):
                result = self.bash(command)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_paid_or_writing_commands_are_denied_without_the_producer_lane(self) -> None:
        for command in [
            "higgsfield generate create nano_banana_2 --prompt 'x'",
            "higgs gen create seedance_2_0 --prompt x --image ./a.png",
            "higgsfield generate workflow reframe --video ./v.mp4",
            "higgsfield product-photoshoot create --mode restyle --prompt x",
            "higgsfield soul-id create --name A --image ./a.png",
            "higgsfield upload create ./input.png",
            "higgsfield project delete abc",
            "higgsfield auth login",
            "cd /tmp && higgsfield generate create nano_banana_2 --prompt x",
            "FOO=1 npx -y @higgsfield/cli generate create nano_banana_2 --prompt x",
            "bash -c 'higgsfield generate create nano_banana_2 --prompt x'",
            "higgsfield account status; higgsfield generate create nano_banana_2 --prompt x",
            "hf generate create nano_banana_2 --prompt x",
        ]:
            with self.subTest(command=command):
                result = self.bash(command)
                self.assertEqual(result.returncode, 2, command)
                self.assertIn("producer lane", result.stderr)
        self.assertTrue(any(line["hook"] == "higgsfield-gate" for line in self.log_lines()))

    def test_auth_token_is_denied_even_for_the_producer(self) -> None:
        result = self.bash("higgsfield auth token", producer=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("credentials", result.stderr)

    def test_unbalanced_quote_is_denied(self) -> None:
        result = self.bash("higgsfield generate create nano_banana_2 --prompt 'oops")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.bash("hf gen create nano_banana_2 --prompt 'oops").returncode, 2)
        self.assertEqual(self.bash("higgsfield generate cost nano_banana_2 --image ./fixture.png").returncode, 2)

    def test_producer_needs_a_fresh_scope_record(self) -> None:
        command = "higgsfield generate create nano_banana_2 --prompt 'x'"
        result = self.bash(command, producer=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing scope record", result.stderr)
        self.write_scope()
        self.assertEqual(self.bash(command, producer=True).returncode, 0)

    def test_scope_failures_are_denied(self) -> None:
        command = "higgsfield generate create nano_banana_2 --prompt 'x'"
        stale = (datetime.now(timezone.utc) - timedelta(hours=1)).astimezone().isoformat(timespec="seconds")
        for overrides, expected in [
            ({"balanceTimestamp": stale}, "old"),
            ({"balanceTimestamp": "2026-10-17T10:00:00"}, "UTC offset"),
            ({"grantedBy": "relayed via another bot"}, "relayed"),
            ({"ceiling": 900}, "not covered"),
            ({"ceiling": 0}, "not covered"),
            ({"jobTypes": ["seedance_2_0"]}, "jobTypes"),
        ]:
            with self.subTest(overrides=overrides):
                self.write_scope(**overrides)
                result = self.bash(command, producer=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn(expected, result.stderr)

    def scope_for_command(self, command: str, **overrides: object) -> None:
        import shlex
        overrides["commandSha256"] = hashlib.sha256(json.dumps(
            shlex.split(command)[1:], ensure_ascii=False, separators=(",", ":"),
        ).encode()).hexdigest()
        self.write_scope(**overrides)

    def test_alias_job_types_and_exact_argv_are_enforced(self) -> None:
        for program in ("higgsfield", "higgs", "hf"):
            for group in ("generate", "gen"):
                good = f"{program} {group} create nano_banana_2 --prompt x"
                self.scope_for_command(good)
                self.assertEqual(self.bash(good, producer=True).returncode, 0)
                changed = good.replace("--prompt x", "--prompt changed")
                self.assertEqual(self.bash(changed, producer=True).returncode, 2)
                bad = good.replace("nano_banana_2", "other_model")
                self.scope_for_command(bad)
                result = self.bash(bad, producer=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn("jobTypes", result.stderr)
        for value in ([], None, "*", ["*"], ["nano_banana_2", "nano_banana_2"]):
            self.write_scope(jobTypes=value)
            self.assertEqual(self.bash("higgsfield generate create nano_banana_2 --prompt x", producer=True).returncode, 2)

    def test_uploads_and_implicit_uploads_require_exact_media_hashes(self) -> None:
        media = self.fixture / "fixture.png"
        media.write_bytes(b"synthetic fixture, never uploaded")
        allowed = {"files": [{"path": "fixture.png", "sha256": sha256(media)}], "mediaIds": []}
        for flag in ("--image", "--start-image", "--end-image", "--video", "--audio", "--image-references", "--video_references", "--audio-references"):
            command = f"higgsfield generate create nano_banana_2 --prompt x {flag} ./fixture.png"
            self.scope_for_command(command)
            self.assertEqual(self.bash(command, producer=True).returncode, 2)
            self.scope_for_command(command, uploadScope=allowed)
            self.assertEqual(self.bash(command, producer=True).returncode, 0)
            denied = {"files": [{"path": "fixture.png", "sha256": "0" * 64}], "mediaIds": []}
            self.scope_for_command(command, uploadScope=denied)
            self.assertEqual(self.bash(command, producer=True).returncode, 2)
        upload = "higgsfield upload create ./fixture.png --image"
        self.scope_for_command(upload, uploadScope=allowed)
        self.assertEqual(self.bash(upload, producer=True).returncode, 2)  # operation not granted
        self.scope_for_command(upload, uploadScope="none", allowedOperations=["upload:create"])
        self.assertEqual(self.bash(upload, producer=True).returncode, 2)
        self.scope_for_command(upload, uploadScope=allowed, allowedOperations=["upload:create"])
        self.assertEqual(self.bash(upload, producer=True).returncode, 0)
        media.write_bytes(b"changed after approval")
        self.assertEqual(self.bash(upload, producer=True).returncode, 2)

    def test_media_ids_paths_unknown_options_and_operations_fail_closed(self) -> None:
        uuid = "12345678-1234-1234-1234-123456789abc"
        command = f"higgsfield generate create nano_banana_2 --image={uuid}"
        self.scope_for_command(command)
        self.assertEqual(self.bash(command, producer=True).returncode, 2)
        self.scope_for_command(command, uploadScope={"files": [], "mediaIds": [uuid]})
        self.assertEqual(self.bash(command, producer=True).returncode, 0)
        for suffix in ("--image ../outside.png", "--image https://example.invalid/photo.png", "--assets x", "--unknown-input x", "--params x"):
            command = "higgsfield generate create nano_banana_2 " + suffix
            self.scope_for_command(command, uploadScope={"files": [], "mediaIds": []})
            self.assertEqual(self.bash(command, producer=True).returncode, 2)
        for command in ("higgsfield soul-id create example", "higgsfield project delete example", "higgsfield auth login", "higgsfield generate workflow example"):
            self.scope_for_command(command)
            self.assertEqual(self.bash(command, producer=True).returncode, 2)

    def test_paid_wrappers_chains_expansion_and_scope_shape_stay_denied_for_producer(self) -> None:
        for command in (
            "env FOO=1 higgsfield generate create nano_banana_2 --prompt x",
            "bash -c 'higgsfield generate create nano_banana_2 --prompt x'",
            "cd /tmp && higgsfield generate create nano_banana_2 --prompt x",
            "higgsfield account status; higgsfield generate create nano_banana_2 --prompt x",
            "higgsfield generate create nano_banana_2 --prompt $(echo x)",
            "higgsfield generate create nano_banana_2 --prompt --help",
        ):
            self.scope_for_command(command)
            self.assertEqual(self.bash(command, producer=True).returncode, 2, command)
        command = "higgsfield generate create nano_banana_2 --prompt x"
        for overrides in ({"ceiling": True}, {"balanceBefore": 99.5}, {"grantedBy": ""}, {"allowedOperations": []}, {"allowedOperations": [None]}, {"allowedOperations": [["generate:create"]]}):
            self.write_scope(**overrides)
            self.assertEqual(self.bash(command, producer=True).returncode, 2, overrides)

    def test_mcp_connector_is_read_only(self) -> None:
        for tool in [
            "mcp__claude_ai_Higgsfield__balance",
            "mcp__claude_ai_Higgsfield__list_projects",
            "mcp__claude_ai_Higgsfield__get_preferences",
            "mcp__claude_ai_Higgsfield__show_generations",
            "mcp__claude_ai_Higgsfield__models_explore",
            "mcp__claude_ai_Higgsfield__ads_studio_list_brands",
            "mcp__claude_ai_Higgsfield__scene_builder_3d_get_project",
            "mcp__claude_ai_Kling__who_am_i",
        ]:
            with self.subTest(tool=tool):
                self.assertEqual(self.run_hook("higgsfield-gate.py", self.write_payload(tool)).returncode, 0)
        for tool in [
            "mcp__claude_ai_Higgsfield__generate_image",
            "mcp__claude_ai_Higgsfield__generate_video_batch",
            "mcp__claude_ai_Higgsfield__execute_preset",
            "mcp__claude_ai_Higgsfield__media_upload",
            "mcp__claude_ai_Higgsfield__apps_invoke",
            "mcp__claude_ai_Higgsfield__publish_project",
            "mcp__claude_ai_Higgsfield__create_voice",
            "mcp__claude_ai_Higgsfield__ai_influencer_generate",
        ]:
            with self.subTest(tool=tool):
                result = self.run_hook(
                    "higgsfield-gate.py", self.write_payload(tool), {"MOVIES_PRODUCER_LANE": "1"}
                )
                self.assertEqual(result.returncode, 2, tool)
                self.assertIn("CLI behind this gate", result.stderr)


class NoRetryTests(HookTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.spec = self.film / "07_generations/requests/plan.json"
        jobs = [
            {"job": name, "tool": "image_to_video", "model": "kling-video-v3_0", "auth": "APR-X",
             "note": "", "args": {}, "images": [], "prompt": "p"}
            for name in ["G-01", "G-02-new"]
        ]
        self.spec.write_text(json.dumps(jobs), encoding="utf-8")
        responses = self.film / "07_generations/responses"
        responses.mkdir(parents=True, exist_ok=True)
        (responses / "G-02-new.intent.json").write_text("{}", encoding="utf-8")

    def test_submit_of_job_closed_in_ledger_is_denied(self) -> None:
        command = f"python3 scripts/kling_batch.py --submit-only --spec {self.spec} --only G-01"
        result = self.run_hook("no-retry.py", self.write_payload("Bash", command=command))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("G-01", result.stderr)

    def test_submit_of_job_with_stored_intent_is_denied(self) -> None:
        command = f"python3 scripts/kling_batch.py --submit-only --spec {self.spec} --only G-02-new"
        result = self.run_hook("no-retry.py", self.write_payload("Bash", command=command))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("G-02-new", result.stderr)

    def test_submit_of_fresh_job_and_resume_query_are_allowed(self) -> None:
        jobs = json.loads(self.spec.read_text(encoding="utf-8"))
        jobs.append(dict(jobs[0], job="G-03-fresh"))
        self.spec.write_text(json.dumps(jobs), encoding="utf-8")
        for command in [
            f"python3 scripts/kling_batch.py --submit-only --spec {self.spec} --only G-03-fresh",
            "python3 scripts/kling_batch.py --resume G-01",
            f"python3 scripts/kling_batch.py --submit-only --spec {self.spec} --only G-03-fresh  # don't",
        ]:
            result = self.run_hook("no-retry.py", self.write_payload("Bash", command=command))
            self.assertEqual(result.returncode, 0, command)


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

    def test_zero_face_gate_accepts_a_qc_folder_log_and_ignores_empty_or_text_evidence(self) -> None:
        clip = self.film / "07_generations/originals/G-01-take.mp4"
        clip.write_bytes(b"\x00")
        report = self.film / "08_edit/reviews/notes.md"
        report.write_text("notes\n", encoding="utf-8")
        claims = [
            {"statement": "reviewed", "evidence": f"{FILM}/07_generations/originals/G-01-take.mp4", "sha256": sha256(clip)},
            {"statement": "empty", "evidence": "", "sha256": ""},
            {"statement": "text", "evidence": f"{FILM}/08_edit/reviews", "sha256": ""},
        ]
        write_handoff(self.fixture, "2026-10-10-qc-test.json", agentRole="qc", claims=claims)
        env = {"MOVIES_LANE_ROLE": "qc"}
        result = self.run_hook("zero-face-gate.py", self.stop_payload(), env=env)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertNotIn("08_edit/reviews", result.stderr)
        qc_log = self.film / "09_delivery/qc/galileo-v2/zero-face-log.json"
        qc_log.parent.mkdir(parents=True)
        qc_log.write_text(
            json.dumps({"files": [{"path": f"{FILM}/07_generations/originals/G-01-take.mp4", "sha256": sha256(clip)}], "framesInspected": 120, "reflectionsChecked": True}),
            encoding="utf-8",
        )
        result = self.run_hook("zero-face-gate.py", self.stop_payload(), env=env)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_stop_hooks_survive_a_directory_in_changed_files(self) -> None:
        write_handoff(
            self.fixture,
            "2026-10-10-continuity-test.json",
            changedFiles=[{"path": f"{FILM}/03_bibles", "sha256After": "0" * 64, "reason": "folder"}],
        )
        result = self.run_hook("handoff-check.py", self.stop_payload())
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("directory", result.stderr)

    def test_zero_face_gate_ignores_non_review_roles(self) -> None:
        clip = self.film / "07_generations/originals/G-01-take.mp4"
        clip.write_bytes(b"\x00")
        claims = [{"statement": "noted", "evidence": f"{FILM}/07_generations/originals/G-01-take.mp4", "sha256": sha256(clip)}]
        write_handoff(self.fixture, "2026-10-10-historian-test.json", agentRole="historian", claims=claims)
        result = self.run_hook("zero-face-gate.py", self.stop_payload(), env={"MOVIES_LANE_ROLE": "historian"})
        self.assertEqual(result.returncode, 0, result.stderr)


class MistakeCaptureTests(HookTestCase):
    def test_failed_command_appends_a_draft_entry(self) -> None:
        placeholder = "placeholder-value-" + "redaction-check"
        payload = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "python3 scripts/kling_batch.py --resume X " + "--" + "token=" + placeholder},
            "tool_response": {"stdout": "", "stderr": "Traceback (most recent call last):\nKeyError: 'works'", "interrupted": False},
            "cwd": str(self.fixture),
        }
        result = self.run_hook("mistake-capture.py", payload, env={"MOVIES_LANE_NAME": "codex-edit-qc"})
        self.assertEqual(result.returncode, 0, result.stderr)
        drafts = (self.film / "logs/mistakes-draft.jsonl").read_text(encoding="utf-8").splitlines()
        entry = json.loads(drafts[-1])
        self.assertEqual(entry["lane"], "codex-edit-qc")
        self.assertIn("KeyError", entry["error"])
        self.assertEqual(entry["solution"], "")
        self.assertNotIn(placeholder, json.dumps(entry))

    def test_post_tool_use_failure_event_is_recorded(self) -> None:
        payload = {
            "hook_event_name": "PostToolUseFailure",
            "tool_name": "Bash",
            "tool_input": {"command": "ffprobe missing.mp4"},
            "error": "Command exited with code 1: missing.mp4: No such file",
            "cwd": str(self.fixture),
        }
        result = self.run_hook("mistake-capture.py", payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        drafts = (self.film / "logs/mistakes-draft.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertIn("No such file", json.loads(drafts[-1])["error"])

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
        root_bindings = (
            "$CLAUDE_PROJECT_DIR",
            "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}",
        )
        for command in commands:
            self.assertTrue(
                any(binding in command for binding in root_bindings),
                command,
            )
        failure_commands = [
            hook["command"]
            for group in settings["hooks"].get("PostToolUseFailure", [])
            for hook in group["hooks"]
        ]
        self.assertTrue(any("mistake-capture.py" in command for command in failure_commands))


if __name__ == "__main__":
    unittest.main()
