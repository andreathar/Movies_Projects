#!/usr/bin/env python3
"""PostToolUse recorder: a failed shell command becomes a draft Mistake/Solution entry."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "mistake-capture"


def failed(response: object) -> tuple[bool, str]:
    if not isinstance(response, dict):
        return False, ""
    code = response.get("exit_code", response.get("exitCode"))
    stderr = str(response.get("stderr") or "")
    if isinstance(code, int) and code != 0:
        return True, stderr or f"exit code {code}"
    if response.get("is_error") or response.get("interrupted"):
        return True, stderr or "tool reported an error"
    return False, ""


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    if payload.get("tool_name") != "Bash":
        return 0
    is_failure, error = failed(payload.get("tool_response"))
    if not is_failure:
        return 0
    command = str((payload.get("tool_input") or {}).get("command") or "")
    _common.draft_mistake(
        root,
        {
            "detected_by": f"hook {HOOK}",
            "mistake": f"command failed: {command[:200]}",
            "command": command[:300],
            "error": error[-500:],
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
