#!/usr/bin/env python3
"""PreToolUse guard: only the producer edits canonical records; respect lane reservations."""

from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "canonical-guard"
PRODUCER_OWNED = [
    "workspace.json",
    "AGENTS.md",
    "CLAUDE.md",
    "projects/*/manifest.json",
    "projects/*/tasks/board.json",
    "projects/*/00_brief/approvals.json",
    "projects/*/00_brief/decisions/*",
    "projects/*/credit-ledger.csv",
    "projects/*/asset-registry.csv",
    "projects/*/memory/STATE.md",
    "projects/*/memory/session-log.json",
    "projects/*/memory/mistakes.jsonl",
]
EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    if payload.get("tool_name") not in EDIT_TOOLS:
        return 0
    tool_input = payload.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not target:
        return 0
    relative = _common.relative_to_root(root, target)
    if not _common.is_producer() and any(fnmatch(relative, pattern) for pattern in PRODUCER_OWNED):
        return _common.deny(
            root,
            HOOK,
            f"{relative} is a producer-owned canonical record; lanes propose through a handoff",
            path=relative,
        )
    me = _common.lane_name()
    for reservation in _common.parley_reservations():
        if reservation["owner"] == me:
            continue
        for reserved in reservation["paths"]:
            reserved_relative = _common.relative_to_root(root, reserved).rstrip("/")
            if relative == reserved_relative or relative.startswith(reserved_relative + "/"):
                return _common.deny(
                    root,
                    HOOK,
                    f"{relative} is reserved by lane {reservation['owner']}; request the reservation first",
                    path=relative,
                )
    return _common.allow(root, HOOK, path=relative)


if __name__ == "__main__":
    raise SystemExit(main())
