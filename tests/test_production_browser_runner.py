"""Socket-free cleanup tests for explicit browser QA; no browser dependency required."""
from pathlib import Path
import signal
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from production_browser_check import descendant_groups, stop_browser_tree


class BrowserCleanupTests(unittest.TestCase):
    def test_captures_detached_browser_groups_not_own_group(self):
        with patch("production_browser_check.os.getpgid", side_effect=[101, 202, 303]), \
                patch("production_browser_check.os.getpgrp", return_value=101), \
                patch("production_browser_check.Path.read_text", side_effect=["2", "3", ""]):
            self.assertEqual(descendant_groups(1), {202, 303})

    def test_terminates_detached_children_even_when_parent_exits_first(self):
        process = Mock(pid=100)
        with patch("production_browser_check.descendant_groups", return_value={100, 200}), \
                patch("production_browser_check.os.killpg") as kill:
            stop_browser_tree(process)
        sent = {(call.args[0], call.args[1]) for call in kill.call_args_list}
        self.assertEqual(sent, {(100, signal.SIGTERM), (200, signal.SIGTERM),
                                (100, signal.SIGKILL), (200, signal.SIGKILL)})

    def test_parent_timeout_still_kills_and_waits(self):
        process = Mock(pid=100)
        process.wait.side_effect = [subprocess.TimeoutExpired("synthetic", 5), 0]
        with patch("production_browser_check.descendant_groups", return_value={100}), \
                patch("production_browser_check.os.killpg") as kill:
            stop_browser_tree(process)
        self.assertEqual(kill.call_args_list[-1].args, (100, signal.SIGKILL))
        self.assertEqual(process.wait.call_count, 2)


if __name__ == "__main__":
    unittest.main()
