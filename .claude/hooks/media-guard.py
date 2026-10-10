#!/usr/bin/env python3
"""PreToolUse guard: no destructive shell commands against the film tree or its evidence."""

from __future__ import annotations

from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "media-guard"
PROTECTED = [
    "projects/",
    "02_references",
    "04_audio",
    "05_storyboard",
    "06_pilot",
    "07_generations",
    "08_edit",
    "09_delivery",
    "inbox",
    "00_brief",
    "credit-ledger.csv",
    "asset-registry.csv",
]
ALWAYS_DENIED = [
    r"\bgit\s+clean\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+lfs\s+prune\b",
]
DESTRUCTIVE_WITH_PATH = [
    r"(^|[\s/])rm\s",
    r"(^|[\s/])mv\s",
    r"(^|[\s/])shred\s",
    r"(^|[\s/])truncate\s",
    r"\bgit\s+checkout\s+--",
    r"\bgit\s+rm\b",
    r"\bfind\b.*\s-delete\b",
    r"\brsync\b.*--delete\b",
]
SEPARATOR = re.compile(r"\s*(?:&&|\|\||;|\|)\s*")


def is_git_restore_of_index_only(segment: str) -> bool:
    return bool(re.search(r"\bgit\s+restore\b", segment)) and "--staged" in segment and "--worktree" not in segment


def destructive(segment: str) -> str | None:
    """Return the reason a single command segment is destructive, else None."""
    if any(re.search(pattern, segment) for pattern in ALWAYS_DENIED):
        return "history or worktree reset"
    if re.search(r"\bgit\s+restore\b", segment) and not is_git_restore_of_index_only(segment):
        if any(name in segment for name in PROTECTED):
            return "worktree restore over protected paths"
    if any(re.search(pattern, segment) for pattern in DESTRUCTIVE_WITH_PATH):
        touches = [name for name in PROTECTED if name in segment]
        if touches:
            return f"destructive command touches protected path(s) {', '.join(touches)}"
    return None


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    if payload.get("tool_name") != "Bash":
        return 0
    command = str((payload.get("tool_input") or {}).get("command") or "")
    for segment in SEPARATOR.split(command):
        reason = destructive(segment)
        if reason:
            return _common.deny(
                root,
                HOOK,
                f"{reason}; originals, references, media, evidence and ledgers are never "
                "moved, reset or deleted by agents",
                command=command[:300],
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
