#!/usr/bin/env python3
"""Stop gate: a session that changed film files ends with a valid handoff."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "handoff-check"


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    film = _common.film_root(root)
    if payload.get("stop_hook_active"):
        return _common.allow(root, HOOK, note="second stop; not blocking again")
    changed = _common.changed_project_files(root, film)
    handoffs = _common.new_handoffs(root, film)
    if not changed and not handoffs:
        return _common.allow(root, HOOK, note="no film edits this session")
    if not handoffs:
        return _common.deny(
            root,
            HOOK,
            f"{len(changed)} film file(s) changed but no new handoff under agents/handoffs/; "
            "write one from shared/templates/agent-handoff-v2.json with base and result hashes",
            changed=len(changed),
        )
    problems: list[str] = []
    for path in handoffs:
        document = _common.load_json(path)
        if document is None:
            problems.append(f"{path.name}: not a JSON object")
            continue
        problems.extend(f"{path.name}: {problem}" for problem in _common.handoff_problems(root, film, document))
    if problems:
        return _common.deny(root, HOOK, "; ".join(problems), handoffs=len(handoffs))
    return _common.allow(root, HOOK, handoffs=len(handoffs), changed=len(changed))


if __name__ == "__main__":
    raise SystemExit(main())
