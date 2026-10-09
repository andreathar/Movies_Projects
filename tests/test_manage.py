"""End-to-end checks for offline movie workspace management."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "manage.py"


class WorkspaceValidationTests(unittest.TestCase):
    def run_cli(self, command: str, root: Path = ROOT) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), command],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )

    def test_status_reports_real_state_without_writes(self) -> None:
        files = [
            ROOT / "workspace.json",
            ROOT / "projects/andre-time-travel/manifest.json",
            ROOT / "projects/andre-time-travel/tasks/board.json",
            ROOT / "projects/andre-time-travel/00_brief/approvals.json",
        ]
        before = {path: path.read_bytes() for path in files}
        manifest = json.loads(before[files[1]])
        board = json.loads(before[files[2]])
        result = self.run_cli("status")
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["activeFilm"], "andre-time-travel")
        self.assertEqual(report["memoryBackend"], "local_project_files")
        self.assertFalse(report["paidGenerationAutomation"])
        self.assertEqual(report["projects"][0]["recordedTakes"], len(manifest["takes"]))
        expected_ready = [task["id"] for task in board["tasks"] if task["status"] == "ready"]
        self.assertEqual(
            [task["id"] for task in report["projects"][0]["readyTasks"]], expected_ready
        )
        self.assertEqual(before, {path: path.read_bytes() for path in files})

    def test_validate_checks_workspace_integrity(self) -> None:
        result = self.run_cli("validate")
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["projects"][0]["chapters"], 5)
        self.assertEqual(report["projects"][0]["storyboardSlots"], 41)
        self.assertEqual(report["projects"][0]["targetSeconds"], 240)
        # Ceiling equals the live balance observed when budget-plan-v2 was written (2026-10-09).
        self.assertEqual(report["projects"][0]["budgetCeiling"], 6981)

        scratch = Path(os.environ.get("TMPDIR", str(Path.home() / ".hermes/cache/scratch")))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="movies-tests-", dir=scratch) as temporary:
            fixture = Path(temporary) / "workspace"
            shutil.copytree(
                ROOT,
                fixture,
                symlinks=True,
                ignore=shutil.ignore_patterns(
                    ".venv",
                    ".git",
                    "__pycache__",
                    "inbox",
                    ".ruff_cache",
                    "02_references",
                    "04_audio",
                    "06_pilot",
                    "07_generations",
                    "08_edit",
                    "09_delivery",
                    "*.mp4",
                    "*.mov",
                    "*.wav",
                    "*.mp3",
                    "*.png",
                    "*.jpg",
                    "*.jpeg",
                    "*.webp",
                    "*.pdf",
                    "*.zip",
                    "reports",
                    "drafts",
                ),
            )
            workspace_data = json.loads((fixture / "workspace.json").read_text())
            for relative in workspace_data["requiredDirectories"]:
                (fixture / relative).mkdir(parents=True, exist_ok=True)
            skill_data = json.loads((fixture / "skills/registry.json").read_text())
            for skill in skill_data["skills"]:
                if skill["type"] == "machine_local_symlink":
                    link = fixture / skill["path"]
                    link.unlink()
                    link.symlink_to(skill["source"], target_is_directory=True)
            manifest_path = fixture / "projects/andre-time-travel/manifest.json"
            board_path = fixture / "projects/andre-time-travel/tasks/board.json"
            manifest_original = manifest_path.read_text()
            board_original = board_path.read_text()

            missing = fixture / "inbox/andre-reference-photos"
            missing.rmdir()
            bad = self.run_cli("validate", fixture)
            self.assertEqual(bad.returncode, 2)
            self.assertIn("missing directory", " ".join(json.loads(bad.stdout)["errors"]))
            missing.mkdir()

            duplicate = json.loads(manifest_original)
            duplicate["shots"][1]["id"] = duplicate["shots"][0]["id"]
            manifest_path.write_text(json.dumps(duplicate))
            bad = self.run_cli("validate", fixture)
            self.assertEqual(bad.returncode, 2)
            self.assertIn("shot", " ".join(json.loads(bad.stdout)["errors"]).lower())
            manifest_path.write_text(manifest_original)

            inconsistent_approval = json.loads(manifest_original)
            inconsistent_approval["approvals"]["pilot"] = True
            manifest_path.write_text(json.dumps(inconsistent_approval))
            bad = self.run_cli("validate", fixture)
            self.assertEqual(bad.returncode, 2)
            self.assertIn("approvals disagree", " ".join(json.loads(bad.stdout)["errors"]))
            manifest_path.write_text(manifest_original)

            unrecorded_take = json.loads(manifest_original)
            unrecorded_take["shots"][0]["takeIds"] = ["unrecorded-job"]
            manifest_path.write_text(json.dumps(unrecorded_take))
            bad = self.run_cli("validate", fixture)
            self.assertEqual(bad.returncode, 2)
            self.assertIn("unrecorded take", " ".join(json.loads(bad.stdout)["errors"]))
            manifest_path.write_text(manifest_original)

            wrong_budget = json.loads(manifest_original)
            wrong_budget["budget"]["phaseCaps"]["final_reserve"] += 1
            manifest_path.write_text(json.dumps(wrong_budget))
            bad = self.run_cli("validate", fixture)
            self.assertEqual(bad.returncode, 2)
            self.assertIn("budget", " ".join(json.loads(bad.stdout)["errors"]).lower())
            manifest_path.write_text(manifest_original)

            wrong_dependency = json.loads(board_original)
            wrong_dependency["tasks"][0]["dependsOn"] = ["NONEXISTENT"]
            board_path.write_text(json.dumps(wrong_dependency))
            bad = self.run_cli("validate", fixture)
            self.assertEqual(bad.returncode, 2)
            self.assertIn("dependency", " ".join(json.loads(bad.stdout)["errors"]).lower())
            board_path.write_text(board_original)

            workspace = json.loads((fixture / "workspace.json").read_text())
            workspace["projects"][0]["manifest"] = "/outside-workspace/manifest.json"
            (fixture / "workspace.json").write_text(json.dumps(workspace))
            bad = self.run_cli("validate", fixture)
            self.assertEqual(bad.returncode, 2)
            self.assertIn("relative", " ".join(json.loads(bad.stdout)["errors"]).lower())


if __name__ == "__main__":
    unittest.main()
