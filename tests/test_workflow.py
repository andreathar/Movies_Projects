"""Regression scenarios for offline handoff, source edits and episode isolation."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from atlas_inputs import load_inputs  # noqa: E402
from workflow import check_clean_draft, inventory, new_draft, verify  # noqa: E402


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        template = self.root / "shared/templates"
        template.mkdir(parents=True)
        shutil.copy2(ROOT / "shared/templates/continuation.json", template)

    def test_new_episode_does_not_inherit_previous_approval_cost_or_layout(self):
        existing = self.root / "projects/old"
        existing.mkdir(parents=True)
        state = existing / "manifest.json"
        state.write_text(json.dumps({"approved": True, "balance": 7741,
                                    "jobs": ["REAL-OLD-JOB"], "chapterCount": 5}))
        before = state.read_bytes()
        result = new_draft(self.root, "continuation-test", "Ensaio", True)
        checked = check_clean_draft(self.root, result["path"])
        self.assertEqual(checked["inheritedApprovals"], 0)
        self.assertFalse(checked["runtimeAndChapterCountInherited"])
        self.assertEqual(state.read_bytes(), before)
        self.assertFalse(result["registeredAsActiveFilm"])
        with self.assertRaisesRegex(ValueError, "never overwrite"):
            new_draft(self.root, "continuation-test", "Again")

    def test_accidental_inherited_approval_is_rejected(self):
        result = new_draft(self.root, "continuation-test", "Ensaio", True)
        approval = self.root / result["path"] / "00_brief/approvals.json"
        data = json.loads(approval.read_text())
        data["creativeApprovals"]["characterReferences"] = True
        approval.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "inherited approvals"):
            check_clean_draft(self.root, result["path"])

    def test_inventory_detects_changed_missing_and_added_files_without_writing(self):
        media = self.root / "projects/episode"
        media.mkdir(parents=True)
        (media / "frame.bin").write_bytes(b"original image placeholder")
        (media / "line.txt").write_text("Original line")
        index = "reports/baseline.json"
        inventory(self.root, index)
        self.assertEqual(verify(self.root, index)["status"], "ok")
        original = (self.root / index).read_bytes()
        (media / "frame.bin").unlink()
        (media / "line.txt").write_text("Edited line")
        (media / "new.txt").write_text("New local work")
        result = verify(self.root, index)
        self.assertEqual(result["status"], "changed")
        self.assertEqual(result["missing"], ["projects/episode/frame.bin"])
        self.assertEqual(result["changed"], ["projects/episode/line.txt"])
        self.assertEqual(result["addedSinceSnapshot"], ["projects/episode/new.txt"])
        self.assertEqual(original, (self.root / index).read_bytes())
        with self.assertRaisesRegex(ValueError, "snapshot filename"):
            inventory(self.root, index)

    def test_paths_cannot_escape_workspace(self):
        with self.assertRaisesRegex(ValueError, "identifier"):
            new_draft(self.root, "../another-project", "Bad")
        with self.assertRaisesRegex(ValueError, "relative"):
            inventory(self.root, "../outside.json")
        with tempfile.TemporaryDirectory() as elsewhere:
            (self.root / "drafts").symlink_to(elsewhere, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "escapes"):
                new_draft(self.root, "escape-test", "Bad")

    def atlas_fixture(self):
        source_film = ROOT / "projects/andre-time-travel"
        film = self.root / "projects/andre-time-travel"
        for relative in ("manifest.json", "01_script/dialogue-lines.csv", "01_script/script-en.md",
                         "05_storyboard/source/atlas.json"):
            target = film / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_film / relative, target)
        source_path = film / "05_storyboard/source/atlas.json"
        data = json.loads(source_path.read_text())
        references = list(data["andreReferences"].values())
        references += [data["tableReference"], data["presentReference"]]
        for scene in data["scenes"]:
            references += [scene[k] for k in ("platePath", "aPath", "bPath", "costumePath")]
        for shot in data["shotDirections"].values():
            references += [shot["reference"], *shot["references"]]
        for path in [film / r for r in references] + [self.root / data["realPhotoWorkspacePath"]]:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"reference placeholder; no media generation")
        return film, source_path, data

    def test_local_direction_and_canonical_dialogue_edits_reach_render_inputs(self):
        film, source_path, data = self.atlas_fixture()
        original = load_inputs(self.root, film, source_path)
        self.assertEqual(len(original["cues"]), 22)
        data["shotDirections"]["C-02"]["action"] = "Hold a quiet breath before replying."
        source_path.write_text(json.dumps(data))
        dialogue = film / "01_script/dialogue-lines.csv"
        dialogue.write_text(dialogue.read_text().replace("Does my name survive?", "What survives?"))
        script = film / "01_script/script-en.md"
        script.write_text(script.read_text().replace("Does my name survive?", "What survives?"))
        edited = load_inputs(self.root, film, source_path)
        self.assertEqual(edited["source"]["shotDirections"]["C-02"]["action"],
                         "Hold a quiet breath before replying.")
        cue = next(c for c in edited["cues"] if c["line_id"] == "C-L01")
        self.assertEqual(cue["text_en"], "What survives?")
        self.assertFalse(edited["manifest"]["approvals"]["screenplay"])

    def test_script_and_csv_cannot_silently_diverge(self):
        film, source_path, _ = self.atlas_fixture()
        dialogue = film / "01_script/dialogue-lines.csv"
        dialogue.write_text(dialogue.read_text().replace("Does my name survive?", "What survives?"))
        with self.assertRaisesRegex(ValueError, "script and dialogue CSV disagree"):
            load_inputs(self.root, film, source_path)

    def test_missing_reference_and_stale_line_mapping_fail_before_rendering(self):
        film, source_path, data = self.atlas_fixture()
        missing = film / data["tableReference"]
        missing.unlink()
        with self.assertRaisesRegex(ValueError, "missing atlas reference"):
            load_inputs(self.root, film, source_path)
        missing.write_bytes(b"restored placeholder")
        stale = copy.deepcopy(data)
        stale["performance"].pop()
        source_path.write_text(json.dumps(stale))
        with self.assertRaisesRegex(ValueError, "dialogue IDs differ"):
            load_inputs(self.root, film, source_path)

    def test_dialogue_cannot_be_silently_forked_inside_atlas_source(self):
        film, source_path, data = self.atlas_fixture()
        data["performance"][0]["text_en"] = "Untracked alternate line"
        source_path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "canonical dialogue"):
            load_inputs(self.root, film, source_path)


if __name__ == "__main__":
    unittest.main()
