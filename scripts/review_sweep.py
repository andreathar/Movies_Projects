"""Free, local sweep that lists images not yet visually reviewed.

Reads the review log at projects/<film>/08_edit/image-review-log.json (created on
first --record). Never generates media, spends credits or modifies images.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
SKIP_PARTS = {"_review", "preproduction-atlas-v1", "atlas", ".git", "node_modules", "_quarantine-full-face"}
SKIP_PREFIXES = ("05_storyboard",)
LOG_NAME = "08_edit/image-review-log.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def scan(root: Path, film: str) -> list[Path]:
    project = root / "projects" / film
    found = []
    for path in sorted(project.rglob("*")):
        rel = path.relative_to(project)
        if path.suffix.lower() not in IMAGE_SUFFIXES or not path.is_file():
            continue
        if SKIP_PARTS & set(rel.parts) or rel.parts[0] in SKIP_PREFIXES:
            continue
        found.append(path)
    inbox = root / "inbox" / "andre-reference-photos"
    if inbox.is_dir():
        found += [p for p in sorted(inbox.iterdir()) if p.suffix.lower() in IMAGE_SUFFIXES]
    return found


def load_log(root: Path, film: str) -> dict:
    path = root / "projects" / film / LOG_NAME
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"schemaVersion": "1.0", "episode": film, "reviews": []}


def pending(root: Path, film: str) -> list[dict]:
    reviewed = {(r["path"], r["sha256"]) for r in load_log(root, film)["reviews"]}
    out = []
    for path in scan(root, film):
        digest = sha256(path)
        rel = path.relative_to(root).as_posix()
        if (rel, digest) not in reviewed:
            out.append({"path": rel, "sha256": digest, "bytes": path.stat().st_size})
    return out


def record(root: Path, film: str, rel: str, verdict: str, notes: str, beauty_variant: str | None) -> dict:
    target = root / rel
    entry = {
        "path": rel,
        "sha256": sha256(target),
        "reviewedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "verdict": verdict,
        "notes": notes,
        "beautyVariant": beauty_variant,
        "approval": "none",
    }
    log = load_log(root, film)
    log["reviews"].append(entry)
    path = root / "projects" / film / LOG_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--film", default="andre-time-travel")
    parser.add_argument("--record", metavar="PATH", help="append a review entry for PATH")
    parser.add_argument("--verdict", choices=["keep", "keep-tone-only", "reject", "variant-needed"])
    parser.add_argument("--notes", default="")
    parser.add_argument("--beauty-variant", help="relative path of a polished parallel version, if any")
    args = parser.parse_args()
    if args.record:
        if not args.verdict:
            parser.error("--record requires --verdict")
        print(json.dumps(record(ROOT, args.film, args.record, args.verdict, args.notes, args.beauty_variant), indent=2))
        return 0
    items = pending(ROOT, args.film)
    print(json.dumps({"unreviewedCount": len(items), "unreviewed": items}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
