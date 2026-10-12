#!/usr/bin/env python3
"""PostToolUse and PostToolUseFailure recorder: a failed shell command becomes a draft mistake."""

from __future__ import annotations

from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "mistake-capture"
ERROR_PATTERN = re.compile(
    r"Traceback \(most recent call last\)|\b[A-Za-z]+Error\b|\berror:|No such file|command not found|"
    r"Permission denied|STOP: non-completed",
)


def failure(payload: dict) -> tuple[bool, str]:
    """Return (failed, error text) for either hook event."""
    if payload.get("hook_event_name") == "PostToolUseFailure":
        return True, str(payload.get("error") or payload.get("tool_response") or "tool failed")
    response = payload.get("tool_response")
    if not isinstance(response, dict):
        return False, ""
    code = response.get("exit_code", response.get("exitCode"))
    stderr = str(response.get("stderr") or "")
    if isinstance(code, int) and not isinstance(code, bool) and code != 0:
        return True, stderr or f"exit code {code}"
    if response.get("is_error") or response.get("interrupted"):
        return True, stderr or "tool reported an error"
    if ERROR_PATTERN.search(stderr):
        return True, stderr
    return False, ""


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    if payload.get("tool_name") != "Bash":
        return 0
    failed, error = failure(payload)
    if not failed:
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
