"""Offline input contract for this episode's editable reference atlas."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from manage import require, scoped_path


def load_inputs(root: Path, film: Path, source_path: Path) -> dict:
    source = json.loads(source_path.read_text(encoding="utf-8"))
    manifest = json.loads((film / "manifest.json").read_text(encoding="utf-8"))
    require(source["film"] == manifest["project"], "atlas belongs to a different episode")
    require(source["status"] == "draft_not_approved", "atlas is a draft, not an approval")
    with (film / "01_script/dialogue-lines.csv").open(newline="", encoding="utf-8") as f:
        lines = list(csv.DictReader(f))
    line_map = {row["line_id"]: row for row in lines}
    require(len(line_map) == len(lines), "duplicate canonical dialogue line IDs")
    script_path = film / "01_script/script-en.md"
    script_text = script_path.read_text(encoding="utf-8")
    for row in lines:
        require(row["text_en"] in script_text,
                f"canonical script and dialogue CSV disagree: {row['line_id']}")
    cues = source["performance"]
    ids = [row["line_id"] for row in cues]
    require(len(ids) == len(set(ids)), "duplicate performance line IDs")
    require(set(ids) == set(line_map), "performance and canonical dialogue IDs differ")
    scenes = source["scenes"]
    require(
        [s["key"] for s in scenes] == [s["key"] for s in manifest["chapters"]],
        "atlas scenes disagree with the canonical chapter order",
    )
    require(
        set(source["shotDirections"]) == {s["id"] for s in manifest["shots"]},
        "atlas and manifest shot IDs differ",
    )
    refs = list(source["andreReferences"].values())
    refs += [source["tableReference"], source["presentReference"]]
    for scene in scenes:
        refs += [scene[k] for k in ("platePath", "aPath", "bPath", "costumePath")]
    for shot in source["shotDirections"].values():
        refs += [shot["reference"], *shot["references"]]
    paths = {scoped_path(film, value) for value in refs}
    paths.add(scoped_path(root, source["realPhotoWorkspacePath"]))
    for path in paths:
        require(path.is_file(), f"missing atlas reference: {path.relative_to(root)}")
    runtime = {s["key"]: manifest["scope"]["chapterSeconds"] for s in scenes}
    runtime.update(opening=manifest["scope"]["openingSeconds"],
                   ending=manifest["scope"]["endingSeconds"])
    for cue in cues:
        require(
            0 <= cue["startSecondsProposed"] < cue["endSecondsProposed"]
            <= runtime[cue["chapter"]],
            f"performance window exceeds scene duration: {cue['line_id']}",
        )
        require("text_en" not in cue and "speaker" not in cue,
                "spoken text and speaker must come from canonical dialogue-lines.csv")
    return {
        "source": source, "manifest": manifest, "lines": lines,
        "cues": [{**cue, **line_map[cue["line_id"]]} for cue in cues],
        "references": sorted(paths),
        "inputFiles": [source_path, film / "manifest.json",
                       film / "01_script/dialogue-lines.csv", script_path],
    }
