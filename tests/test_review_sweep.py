"""Review sweep lists new or changed images and never touches them."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from review_sweep import pending, record  # noqa: E402


class ReviewSweepTests(unittest.TestCase):
    def test_new_and_changed_images_are_pending_until_recorded(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            image = root / "projects/f/02_references/andre/a.png"
            image.parent.mkdir(parents=True)
            image.write_bytes(b"one")
            self.assertEqual(len(pending(root, "f")), 1)
            record(root, "f", "projects/f/02_references/andre/a.png", "keep", "ok", None)
            self.assertEqual(pending(root, "f"), [])
            image.write_bytes(b"two")
            self.assertEqual(len(pending(root, "f")), 1)
            self.assertEqual(image.read_bytes(), b"two")


if __name__ == "__main__":
    unittest.main()
