#!/usr/bin/env python3
"""Verify the local workflow rehearsal and rendered atlas without provider calls."""
from __future__ import annotations

import argparse
import csv
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from manage import DEFAULT_ROOT, require, scoped_path, validate
from workflow import check_clean_draft, digest, now, write_new


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        self.paths.extend(value for key, value in attrs if key in {"src", "href"} and value)


def verify(root: Path, atlas_relative: str) -> dict:
    film = root / "projects/andre-time-travel"
    atlas = scoped_path(root, atlas_relative)
    catalog = json.loads((atlas / "catalog.json").read_text())
    manifest = json.loads((film / "manifest.json").read_text())
    require(catalog["approved"] is False, "rebuild must not grant approval")
    require(not catalog["overflowChecks"], "rendered text overflow")
    require(len(catalog["pages"]) == catalog["counts"]["totalCardImages"], "card count mismatch")
    for page in catalog["pages"]:
        require(scoped_path(atlas, page["image"]).is_file(), f"card missing: {page['id']}")
    with (film / "01_script/dialogue-lines.csv").open(newline="") as handle:
        lines = list(csv.DictReader(handle))
    with (atlas / "documents/dialogue-performance.csv").open(newline="") as handle:
        rendered_lines = list(csv.DictReader(handle))
    require({r["line_id"]: r["text_en"] for r in lines}
            == {r["line_id"]: r["text_en"] for r in rendered_lines}, "rendered dialogue drift")
    specs = json.loads((atlas / "documents/shot-specifications.json").read_text())["shots"]
    require([s["id"] for s in specs] == [s["id"] for s in manifest["shots"]], "shot order drift")
    source = json.loads((film / "05_storyboard/source/atlas.json").read_text())
    for shot in specs:
        require(shot["action"] == source["shotDirections"][shot["id"]]["action"],
                f"editable direction not rendered: {shot['id']}")
    require(sum(s["durationSeconds"] for s in specs) == manifest["scope"]["targetSeconds"],
            "rendered duration drift")
    inputs = json.loads((atlas / "evidence/build-inputs.json").read_text())
    for record in inputs["files"]:
        require(digest(scoped_path(root, record["path"])) == record["sha256"],
                f"build input changed: {record['path']}")
    parser = Links()
    parser.feed((atlas / "index.html").read_text())
    for value in parser.paths:
        url = urlsplit(value)
        require(not url.scheme and not url.netloc, f"external atlas dependency: {value}")
        target = (atlas / unquote(url.path)).resolve()
        require(target.is_relative_to(root) and target.is_file(), f"broken atlas link: {value}")
    pdf_pages = {}
    for pdf, key in (("reference-atlas.pdf", "boards"), ("storyboard-cards.pdf", "shots"),
                     ("performance-cards.pdf", "performanceCards")):
        result = subprocess.run(["pdfinfo", str(atlas / pdf)], capture_output=True,
                                text=True, check=True)
        count = int(re.search(r"^Pages:\s+(\d+)", result.stdout, re.M)[1])
        require(count == catalog["counts"][key], f"PDF page count differs: {pdf}")
        pdf_pages[pdf] = count
    original = json.loads((root / "reports/workflow-v1/originals-before.json").read_text())
    for record in original["files"]:
        require(digest(scoped_path(root, record["path"])) == record["sha256"],
                f"previous original or delivery changed: {record['path']}")
    localized = json.loads((root / "reports/workflow-v1/localized-bible-assets.json").read_text())
    for record in localized["images"]:
        require(digest(scoped_path(root, record["path"])) == record["sha256"],
                "localized source bytes differ")
    document = root / "docs/master_production_visual_bible.md"
    text = document.read_text()
    image_paths = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    require(len(image_paths) == localized["localImageLinks"], "visual bible image count drift")
    for value in image_paths:
        require(not Path(value).is_absolute() and not urlsplit(value).scheme,
                "visual bible still has a nonportable image link")
        path = (document.parent / value).resolve()
        require(path.is_relative_to(root) and path.is_file(), "visual bible image missing")
    management = validate(root)
    require(management["status"] == "ok", "management validation failed")
    draft = check_clean_draft(root, "drafts/workflow-rehearsal")
    return {
        "createdAt": now(), "status": "ok", "newPaidJobs": 0,
        "atlas": atlas_relative, "cardImages": len(catalog["pages"]),
        "canonicalDialogueLinesPreserved": len(lines), "shotDirectionsFromEditableSource": len(specs),
        "timelineSeconds": sum(s["durationSeconds"] for s in specs),
        "buildInputHashesMatched": len(inputs["files"]), "pdfPageCounts": pdf_pages,
        "localAtlasLinksResolved": len(parser.paths), "layoutOverflows": 0,
        "originalFilesUnchanged": len(original["files"]),
        "localizedBibleImageLinks": len(image_paths), "missingLocalDependenciesCopied": 1,
        "cleanContinuationRehearsal": draft, "management": management,
        "creativeApproval": False,
        "limits": ["No end-to-end movie, likeness, language or speech synchronization acceptance",
                   "Historical source snapshots 18 and 19 still uncached",
                   "R2 provider jobs and charges not independently verified",
                   "HTML links inspected statically; browser interaction not verified",
                   "Two V2 cards visually inspected separately; not full artistic acceptance"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atlas", default="projects/andre-time-travel/05_storyboard/preproduction-atlas-v2")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = verify(DEFAULT_ROOT, args.atlas)
        write_new(scoped_path(DEFAULT_ROOT, args.output), result)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
