"""Temporary media fixtures; no provider calls, original media or credentials."""

import csv
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("shared_media_test", ROOT / "scripts/shared_media.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class SharedMediaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir="/tmp")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "canonical"
        self.film = self.root / "projects/film"
        self.film.mkdir(parents=True)
        self.output = self.base / "lane/outputs/job-1"
        self.media = self.film / "frame.png"
        self.media.write_bytes(b"synthetic")
        self.catalog = self.film / "asset-registry.csv"
        self.hash = hashlib.sha256(b"synthetic").hexdigest()
        self.row = ["frame-1", "image", "frame.png", "film", "synthetic fixture", self.hash, "false", "not approved"]
        self.save([self.row])

    def save(self, rows):
        with self.catalog.open("w", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(m.HEADER)
            writer.writerows(rows)

    def test_one_canonical_input_and_separate_output_without_copy(self):
        resolved = m.input_path(self.base / "lane", "frame.png", media_root=self.film)
        self.assertEqual(resolved, self.media)
        output = m.output_path(self.root, self.output, "frame-v2.png")
        self.assertEqual(output, self.output / "frame-v2.png")
        self.assertFalse(output.exists())
        self.assertFalse(self.output.exists())
        self.assertEqual(self.media.read_bytes(), b"synthetic")

    def test_traversal_drives_and_symlinks_are_not_a_bypass(self):
        for value in ("../frame.png", "/tmp/frame.png", "C:/frame.png", "x\\frame.png", "x//frame.png"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                m.input_path(self.film, value)
        (self.film / "escape").symlink_to(self.base, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            m.input_path(self.film, "escape/anything")
        with self.assertRaisesRegex(ValueError, "separate"):
            m.output_path(self.root, self.film, "new.png")
        self.output.mkdir(parents=True)
        (self.output / "escape").symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            m.output_path(self.root, self.output, "escape/new.png")

    def test_existing_output_or_hardlink_cannot_overwrite_original(self):
        self.output.mkdir(parents=True)
        target = self.output / "frame.png"
        target.hardlink_to(self.media)
        with self.assertRaisesRegex(ValueError, "already exists"):
            m.output_path(self.root, self.output, "frame.png")
        self.assertEqual(self.media.read_bytes(), b"synthetic")

    def test_multiline_quoted_csv_uses_parser_line_provenance(self):
        self.row[-1] = 'A note, with comma\nand "quotes"'
        self.save([self.row])
        report = m.read_catalog(self.root, "projects/film")
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["records"][0]["notes"], self.row[-1])
        self.assertEqual(report["records"][0]["line"], 3)

    def test_legacy_six_columns_propose_only_deducible_values(self):
        legacy = ["legacy-1", "image", "frame.png", "fixture source; sha256=" + self.hash, "false", "never approved"]
        self.save([legacy])
        before = self.catalog.read_bytes()
        report = m.read_catalog(self.root, "projects/film")
        self.assertEqual(report["errors"][0]["code"], "CSV_WIDTH")
        self.assertEqual(report["errors"][0]["columns"], 6)
        proposal = report["proposals"][0]
        self.assertEqual(proposal["candidate"]["path_base"], "film")
        self.assertEqual(proposal["candidate"]["sha256"], self.hash)
        self.assertEqual(proposal["candidate"]["approved"], "false")
        self.assertFalse(proposal["hash_verified"])
        self.assertFalse(proposal["applied"])
        self.assertEqual(self.catalog.read_bytes(), before)
        with self.assertRaisesRegex(ValueError, "registry invalid"):
            m.resolve_asset(self.root, "projects/film", "legacy-1")

    def test_ambiguous_or_missing_legacy_provenance_is_not_invented(self):
        self.save([["legacy", "image", "frame.png", "source without digest", "false", "note"]])
        self.assertEqual(m.read_catalog(self.root, "projects/film")["proposals"], [])
        (self.root / "frame.png").write_bytes(b"other")
        self.save([["legacy", "image", "frame.png", "source; sha256=" + self.hash, "false", "note"]])
        self.assertEqual(m.read_catalog(self.root, "projects/film")["proposals"], [])

    def test_duplicate_ids_bad_hash_and_approval_are_errors(self):
        row = self.row.copy()
        row[5], row[6] = "bad-hash", "unknown"
        self.save([self.row, row])
        report = m.read_catalog(self.root, "projects/film")
        self.assertEqual(report["status"], "error")
        self.assertIn("duplicated", str(report["errors"]))
        self.assertIn("sha256", str(report["errors"]))
        self.assertIn("approved", str(report["errors"]))

    def test_duplicate_ids_are_not_hidden_by_legacy_record_width(self):
        legacy = [self.row[0], "image", "frame.png", "source; sha256=" + self.hash, "false", "legacy"]
        self.save([legacy, self.row])
        report = m.read_catalog(self.root, "projects/film")
        self.assertEqual(report["duplicate_asset_ids"], {self.row[0]: 2})
        self.assertTrue(report["proposals"][0]["identity_conflict"])
        self.assertIn("duplicated", str(report["errors"]))
        with self.assertRaisesRegex(ValueError, "invalid"):
            m.resolve_asset(self.root, "projects/film", self.row[0])

    def test_catalog_symlink_cannot_read_outside_declared_root(self):
        self.catalog.unlink()
        self.catalog.symlink_to(self.base / "private.csv")
        with self.assertRaisesRegex(ValueError, "symlink"):
            m.read_catalog(self.root, "projects/film")

    def test_local_resolution_does_not_claim_hash_or_creative_acceptance(self):
        result = m.resolve_asset(self.root, "projects/film", "frame-1")
        self.assertEqual(result["path"], str(self.media))
        self.assertFalse(result["approved"])
        self.assertFalse(result["hash_verified"])
        self.media.write_text("version https://git-lfs.github.com/spec/v1\n")
        with self.assertRaisesRegex(ValueError, "LFS pointer"):
            m.resolve_asset(self.root, "projects/film", "frame-1")

    def test_cli_validate_resolve_and_output_preview_are_read_only(self):
        before = self.catalog.read_bytes()
        prefix = [sys.executable, str(ROOT / "scripts/manage.py"), "--root", str(self.base / "lane"), "assets"]
        for action, extra in (("validate", []), ("resolve", ["--asset-id", "frame-1"]), ("output", ["--output-root", str(self.output), "--path", "new.png"])):
            result = subprocess.run([*prefix, action, "--media-root", str(self.root), "--film", "projects/film", *extra], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "ok")
        self.assertEqual(self.catalog.read_bytes(), before)
        self.assertFalse(self.output.exists())

    def test_batch_reference_resolution_never_submits(self):
        prefix = [sys.executable, str(ROOT / "scripts/kling_batch.py"), "--film", "projects/film", "--media-root", str(self.root)]
        result = subprocess.run([*prefix, "--resolve-reference", "frame.png"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["path"], str(self.media))
        refused = subprocess.run([*prefix, "--submit-only"], capture_output=True, text=True)
        self.assertEqual(refused.returncode, 2)
        self.assertIn("not enabled", refused.stderr)

    def test_fingerprint_can_read_canonical_inputs_without_copying_them(self):
        spec = importlib.util.spec_from_file_location("release_fixture", ROOT / "scripts/kling_release.py")
        release = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(release)
        job = {"tool": "image_to_video", "model": "synthetic", "prompt": "fixture", "args": {}, "images": ["frame.png"]}
        canonical = release.fingerprint(self.film, job)
        shared = release.fingerprint(self.base / "lane", job, media_root=self.film)
        self.assertEqual(canonical, shared)
        self.assertFalse((self.base / "lane/frame.png").exists())


if __name__ == "__main__":
    unittest.main()
