"""Regression scenarios for conventional-commit changelog automation."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from changelog import (  # noqa: E402
    HEADER,
    bullet,
    categorize,
    check,
    entries,
    merge,
    release,
)

COMMITS = [
    {"sha": "a" * 40, "subject": "feat(serena): add changelog automation (#7)", "body": ""},
    {"sha": "b" * 40, "subject": "fix: stop duplicating media in the inbox (#8)", "body": ""},
    {"sha": "c" * 40, "subject": "chore: bump dependencies", "body": ""},
    {"sha": "d" * 40, "subject": "docs: refresh the read order", "body": ""},
    {"sha": "e" * 40, "subject": "refactor: split the asset contract", "body": ""},
    {"sha": "f" * 40, "subject": "fix!: drop the legacy registry format", "body": ""},
]


class CategorizeTests(unittest.TestCase):
    def test_types_map_to_sections(self):
        self.assertEqual(categorize("feat: add a thing")[:2], ("Added", False))
        self.assertEqual(categorize("fix: repair a thing")[:2], ("Fixed", False))
        self.assertEqual(categorize("perf: speed up a thing")[:2], ("Changed", False))
        self.assertEqual(categorize("sec: harden a thing")[:2], ("Security", False))

    def test_noise_types_are_skipped(self):
        for subject in ("chore: bump", "docs: note", "test: cover", "ci: run", "style: tidy"):
            self.assertIsNone(categorize(subject))

    def test_breaking_marker_on_footer_or_bang(self):
        self.assertEqual(categorize("fix!: drop it")[:2], ("Fixed", True))
        self.assertEqual(categorize("feat: add it", "BREAKING CHANGE: gone")[:2], ("Added", True))

    def test_unknown_type_with_breaking_is_still_recorded(self):
        self.assertEqual(categorize("tweak!: change meaning")[0], "Changed")

    def test_description_keeps_a_trailing_pr_reference(self):
        section, _, description = categorize("fix: close the gap (#12)")
        self.assertEqual(section, "Fixed")
        self.assertTrue(description.endswith("(#12)"))


class EntryTests(unittest.TestCase):
    def setUp(self):
        self.collected = entries(COMMITS)

    def test_noise_is_dropped(self):
        self.assertEqual(len(self.collected), 4)
        self.assertNotIn("chore", " ".join(entry["description"] for entry in self.collected))

    def test_bullet_formats_breaking_and_pr(self):
        added = next(entry for entry in self.collected if entry["section"] == "Added")
        self.assertEqual(bullet(added), "- add changelog automation (#7)")
        self.assertEqual(added["pr"], "7")
        breaking = next(entry for entry in self.collected if entry["breaking"])
        self.assertTrue(bullet(breaking).startswith("- **BREAKING** "))


class MergeTests(unittest.TestCase):
    def setUp(self):
        self.base = f"{HEADER}\n## [Unreleased]\n"

    def test_entries_are_grouped_in_canonical_order(self):
        updated, added = merge(self.base, entries(COMMITS))
        self.assertEqual(added, 4)
        headings = [line for line in updated.split("\n") if line.startswith("### ")]
        self.assertEqual(headings, ["### Added", "### Changed", "### Fixed"])

    def test_repeating_the_merge_changes_nothing(self):
        once, _ = merge(self.base, entries(COMMITS))
        twice, added = merge(once, entries(COMMITS))
        self.assertEqual(added, 0)
        self.assertEqual(once, twice)

    def test_existing_hand_written_entries_are_preserved(self):
        seeded = self.base + "\n### Added\n- hand written entry\n"
        updated, added = merge(seeded, entries(COMMITS))
        self.assertEqual(added, 4)
        self.assertIn("hand written entry", updated)

    def test_unreleased_heading_is_created_when_missing(self):
        updated, added = merge(HEADER, entries(COMMITS))
        self.assertEqual(added, 4)
        self.assertIn("## [Unreleased]", updated)

    def test_spacing_after_the_heading_and_trailing_newline(self):
        updated, _ = merge(self.base, entries(COMMITS))
        self.assertIn("## [Unreleased]\n\n### Added\n- ", updated)
        self.assertTrue(updated.endswith("\n"))
        self.assertFalse(updated.endswith("\n\n"))


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.text, _ = merge(f"{HEADER}\n## [Unreleased]\n", entries(COMMITS))

    def test_release_moves_entries_and_dates_the_section(self):
        updated, count = release(self.text, "1.2.0", "2026-10-18", "https://example.test/acme/app")
        self.assertEqual(count, 4)
        self.assertIn("## [1.2.0] - 2026-10-18", updated)
        self.assertIn("## [Unreleased]", updated)
        self.assertIn("[Unreleased]: https://example.test/acme/app/compare/v1.2.0...HEAD", updated)
        self.assertIn("[1.2.0]: https://example.test/acme/app/releases/tag/v1.2.0", updated)
        self.assertIn("## [1.2.0] - 2026-10-18\n\n### Added", updated)

    def test_release_requires_a_patch_version_and_entries(self):
        with self.assertRaisesRegex(ValueError, "MAJOR.MINOR.PATCH"):
            release(self.text, "v1.2", "2026-10-18", "")
        with self.assertRaisesRegex(ValueError, "no entries"):
            release(f"{HEADER}\n## [Unreleased]\n", "1.2.0", "2026-10-18", "")

    def _release(self, text, version, day, url="https://example.test/acme/app"):
        return release(text, version, day, url)[0]

    def test_second_release_links_against_the_previous_version(self):
        first = self._release(self.text, "0.1.0", "2026-01-01")
        seeded = first.replace("## [Unreleased]\n", "## [Unreleased]\n\n### Fixed\n- later fix\n", 1)
        second = self._release(seeded, "0.2.0", "2026-02-01")
        self.assertIn("[0.2.0]: https://example.test/acme/app/compare/v0.1.0...v0.2.0", second)
        self.assertIn("[Unreleased]: https://example.test/acme/app/compare/v0.2.0...HEAD", second)
        self.assertIn("[0.1.0]: https://example.test/acme/app/releases/tag/v0.1.0", second)

    def test_older_sections_keep_their_blank_lines(self):
        first = self._release(self.text, "0.1.0", "2026-01-01")
        seeded = first.replace("## [Unreleased]\n", "## [Unreleased]\n\n### Fixed\n- later fix\n", 1)
        second = self._release(seeded, "0.2.0", "2026-02-01")
        self.assertIn("## [0.1.0] - 2026-01-01\n\n### Added", second)
        self.assertIn("## [0.2.0] - 2026-02-01\n\n### Fixed", second)
        self.assertEqual(second.count("[Unreleased]:"), 1)
        self.assertEqual(second.count("[0.1.0]:"), 1)
        self.assertEqual(second.count("[0.2.0]:"), 1)


class CheckTests(unittest.TestCase):
    def test_valid_file_has_no_problems(self):
        text, _ = merge(f"{HEADER}\n## [Unreleased]\n", entries(COMMITS))
        self.assertEqual(check(text), [])

    def test_empty_section_is_reported(self):
        problems = check(f"{HEADER}\n## [Unreleased]\n\n### Fixed\n\n## [1.0.0] - 2026-01-01\n")
        self.assertIn("empty section: Fixed", problems)

    def test_bad_version_and_date_are_reported(self):
        problems = check(f"{HEADER}\n## [Unreleased]\n\n### Added\n- x\n\n## [1.0] - today\n")
        self.assertTrue(any("MAJOR.MINOR.PATCH" in problem for problem in problems))
        self.assertTrue(any("non-ISO date" in problem for problem in problems))

    def test_out_of_order_versions_are_reported(self):
        text = (f"{HEADER}\n## [Unreleased]\n\n### Added\n- x\n\n"
                "## [1.0.0] - 2026-01-01\n\n### Added\n- y\n\n"
                "## [2.0.0] - 2026-02-01\n\n### Added\n- z\n")
        self.assertIn("released versions are not in descending order", check(text))


if __name__ == "__main__":
    unittest.main()
