#!/usr/bin/env python3
"""Stop gate: every delivery names its successor or an explicit stage end."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "successor-check"


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    film = _common.film_root(root)
    if payload.get("stop_hook_active"):
        return _common.allow(root, HOOK, note="second stop; not blocking again")
    orphans = []
    for path in _common.new_handoffs(root, film):
        document = _common.load_object(path) or {}
        if not _common.has_successor(document):
            orphans.append(path.name)
    if orphans:
        return _common.deny(
            root,
            HOOK,
            "handoff(s) without nextActions[] or stageComplete+stageCompleteReason: "
            + ", ".join(orphans)
            + "; a verified delivery ends with an accepted successor, a blocker with owner, or an explicit stage end",
        )
    return _common.allow(root, HOOK)


if __name__ == "__main__":
    raise SystemExit(main())
