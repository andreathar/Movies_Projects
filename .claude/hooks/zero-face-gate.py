#!/usr/bin/env python3
"""Stop gate for review roles: every reviewed clip or image set has a zero-face log."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "zero-face-gate"
REVIEW_ROLES = {"qc", "continuity"}
MEDIA_SUFFIXES = {".mp4", ".mov", ".webm", ".png", ".jpg", ".jpeg", ".webp"}
LOG_NAME = "zero-face-log.json"
LOG_FOLDERS = ("09_delivery/qc", "08_edit/reviews", "02_references/_review")


def media_files(resolved: Path) -> list[Path]:
    if resolved.is_file():
        return [resolved] if resolved.suffix.lower() in MEDIA_SUFFIXES else []
    if resolved.is_dir():
        return sorted(p for p in resolved.iterdir() if p.is_file() and p.suffix.lower() in MEDIA_SUFFIXES)
    return []


def log_entries(document: Any) -> set[str]:
    """Names and paths listed under ``files`` in a zero-face log."""
    names: set[str] = set()
    if not isinstance(document, dict):
        return names
    for entry in document.get("files") or []:
        if isinstance(entry, str):
            names.add(entry)
        elif isinstance(entry, dict) and entry.get("path"):
            names.add(str(entry["path"]))
    return names


def covered(root: Path, film: Path, media: Path, logs: list[Path]) -> bool:
    """A media file is covered by a log beside it or by a QC log that lists it."""
    if (media.parent / LOG_NAME).is_file():
        return True
    relative = _common.relative_to_root(root, media)
    for log in logs:
        names = log_entries(_common.load_json(log))
        if media.name in names or relative in names or any(relative.endswith(name) for name in names if name):
            return True
    return False


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    film = _common.film_root(root)
    if payload.get("stop_hook_active"):
        return _common.allow(root, HOOK, note="second stop; not blocking again")
    logs = [path for folder in LOG_FOLDERS for path in (film / folder).rglob(LOG_NAME)]
    missing: list[str] = []
    for path in _common.new_handoffs(root, film):
        document = _common.load_object(path) or {}
        role = str(document.get("agentRole") or "")
        if role not in REVIEW_ROLES and _common.lane_role() not in REVIEW_ROLES:
            continue
        for claim in document.get("claims") or []:
            if not isinstance(claim, dict):
                continue
            evidence = str(claim.get("evidence") or "")
            resolved = _common.resolve_evidence(root, film, evidence)
            if resolved is None:
                continue
            for media in media_files(resolved):
                if not covered(root, film, media, logs):
                    missing.append(_common.relative_to_root(root, media))
    if missing:
        return _common.deny(
            root,
            HOOK,
            "reviewed media without a zero-face-log.json (beside the file, or under 09_delivery/qc/ "
            "listing it by path) with frames and reflections inspected: " + "; ".join(missing),
        )
    return _common.allow(root, HOOK)


if __name__ == "__main__":
    raise SystemExit(main())
