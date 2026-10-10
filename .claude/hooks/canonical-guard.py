#!/usr/bin/env python3
"""PreToolUse guard: only the producer edits canonical records, in any checkout."""

from __future__ import annotations

from fnmatch import fnmatchcase
from pathlib import Path, PurePosixPath
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


def parts_match(parts: tuple[str, ...], pattern: str) -> bool:
    """Match path parts one by one so ``*`` never crosses a slash."""
    wanted = pattern.split("/")
    return len(parts) == len(wanted) and all(
        fnmatchcase(part, token) for part, token in zip(parts, wanted)
    )


def is_canonical(relative: str) -> bool:
    """True when the path, or any suffix of an outside path, names a canonical record."""
    parts = PurePosixPath(relative).parts
    if parts and parts[0] == "/":
        parts = parts[1:]
    for start in range(len(parts)):
        suffix = parts[start:]
        if any(parts_match(suffix, pattern) for pattern in PRODUCER_OWNED):
            return True
    return False


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
    if not _common.is_producer() and is_canonical(relative):
        return _common.deny(
            root,
            HOOK,
            f"{relative} is a producer-owned canonical record; lanes propose through a handoff",
            path=relative,
        )
    return _common.allow(root, HOOK, path=relative)


if __name__ == "__main__":
    raise SystemExit(main())
