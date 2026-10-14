"""Check both no-shell gates and failure propagation with offline fixtures."""

from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


PATH = Path(__file__).resolve().parents[1] / "scripts/parley_verify.py"
SPEC = importlib.util.spec_from_file_location("parley_verify", PATH)
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)


class VerificationTests(unittest.TestCase):
    def test_both_commands_are_argument_lists_without_shell(self):
        with patch.object(verify.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(verify.verify(Path("/fixture"), "/python"), 0)
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args_list[0].args[0],
                         ["/python", "-B", "scripts/manage.py", "validate"])
        self.assertEqual(run.call_args_list[1].args[0],
                         ["/python", "-B", "-m", "unittest", "discover", "-s", "tests"])
        self.assertTrue(all(c.kwargs == {"cwd": Path("/fixture"), "check": False}
                            for c in run.call_args_list))

    def test_either_failure_is_preserved_and_neither_check_is_skipped(self):
        for statuses, expected in [([7, 0], 7), ([0, 1], 1), ([7, 1], 7), ([-15, 0], 1)]:
            with self.subTest(statuses=statuses), patch.object(verify.subprocess, "run") as run:
                run.side_effect = [subprocess.CompletedProcess([], c) for c in statuses]
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(verify.verify(Path("/fixture"), "/python"), expected)
                self.assertEqual(run.call_count, 2)

    def test_missing_first_executable_still_runs_second_gate_and_fails(self):
        with patch.object(verify.subprocess, "run") as run:
            run.side_effect = [OSError("fixture missing executable"), subprocess.CompletedProcess([], 0)]
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(verify.verify(Path("/fixture"), "/python"), 127)
            self.assertEqual(run.call_count, 2)

    def test_real_child_success_and_failure_propagate(self):
        for validation, test_failure, expected in [(0, False, 0), (7, False, 7), (0, True, 1)]:
            with self.subTest(validation=validation, test_failure=test_failure), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "scripts").mkdir()
                (root / "tests").mkdir()
                (root / "scripts/manage.py").write_text(
                    "from pathlib import Path\nimport sys\n"
                    "Path('validation-ran').write_text('ran')\n"
                    f"raise SystemExit({validation})\n")
                (root / "tests/test_fixture.py").write_text(
                    "from pathlib import Path\nimport unittest\n"
                    "class Fixture(unittest.TestCase):\n"
                    " def test_gate(self):\n"
                    "  Path('unittest-ran').write_text('ran')\n"
                    f"  self.assertFalse({test_failure})\n")
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(verify.verify(root, sys.executable), expected)
                self.assertTrue((root / "validation-ran").is_file())
                self.assertTrue((root / "unittest-ran").is_file())


if __name__ == "__main__":
    unittest.main()
