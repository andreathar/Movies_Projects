#!/usr/bin/env python3
"""Stop gate for review roles: every reviewed clip or image set has a zero-face log."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "zero-face-gate"
REVIEW_ROLES = {"qc", "continuity"}
MEDIA_SUFFIXES = {".mp4", ".mov", ".webm", ".png", ".jpg", ".jpeg", ".webp"}
LOG_NAME = "zero-face-log.json"


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    film = _common.film_root(root)
    if payload.get("stop_hook_active"):
        return _common.allow(root, HOOK, note="second stop; not blocking again")
    missing: list[str] = []
    for path in _common.new_handoffs(root, film):
        document = _common.load_json(path) or {}
        role = str(document.get("agentRole") or _common.lane_role())
        if role not in REVIEW_ROLES and _common.lane_role() not in REVIEW_ROLES:
            continue
        for claim in document.get("claims") or []:
            if not isinstance(claim, dict):
                continue
            evidence = str(claim.get("evidence") or "")
            resolved = _common.resolve_evidence(root, film, evidence)
            if resolved is None:
                continue
            folder = resolved if resolved.is_dir() else resolved.parent
            is_media = resolved.is_dir() or resolved.suffix.lower() in MEDIA_SUFFIXES
            if is_media and not (folder / LOG_NAME).is_file():
                missing.append(f"{evidence} -> {folder.name}/{LOG_NAME}")
    if missing:
        return _common.deny(
            root,
            HOOK,
            "reviewed media without a zero-face-log.json listing frames and reflections inspected: "
            + "; ".join(missing),
        )
    return _common.allow(root, HOOK)


if __name__ == "__main__":
    raise SystemExit(main())
