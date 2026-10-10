#!/usr/bin/env python3
"""PreToolUse guard: no destructive shell commands against media and evidence folders."""

from __future__ import annotations

from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "media-guard"
PROTECTED = [
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
DESTRUCTIVE = [
    r"(^|[\s;&|])rm\s",
    r"(^|[\s;&|])mv\s",
    r"(^|[\s;&|])shred\s",
    r"(^|[\s;&|])truncate\s",
    r"git\s+clean\b",
    r"git\s+reset\s+--hard",
    r"git\s+checkout\s+--",
    r"git\s+restore\b",
    r"git\s+rm\b",
    r"git\s+lfs\s+prune",
]


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    if payload.get("tool_name") != "Bash":
        return 0
    command = str((payload.get("tool_input") or {}).get("command") or "")
    destructive = any(re.search(pattern, command) for pattern in DESTRUCTIVE)
    touches = [name for name in PROTECTED if name in command]
    if destructive and touches:
        return _common.deny(
            root,
            HOOK,
            f"destructive command touches protected folder(s) {', '.join(touches)}; "
            "originals, references, media, evidence and ledgers are never moved or deleted by agents",
            command=command[:300],
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
