"""Shared helpers for the film gate hooks.

Every hook reads one JSON payload from stdin, decides, appends one line to
``<film>/logs/hooks.jsonl`` and exits 0 (allow) or 2 (deny, reason on stderr).
Hooks never approve, spend, commit or merge; a denial is a refusal to proceed
with one tool call and a draft Mistake/Solution entry for the producer.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Any

PRODUCER_ENV = "MOVIES_PRODUCER_LANE"
LANE_NAME_ENV = "MOVIES_LANE_NAME"
LANE_ROLE_ENV = "MOVIES_LANE_ROLE"
STATUS_CMD_ENV = "MOVIES_PARLEY_STATUS_CMD"


def read_payload() -> dict[str, Any]:
    """Return the hook payload from stdin, or an empty object on bad input."""
    try:
        value = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def workspace_root(payload: dict[str, Any]) -> Path:
    """Locate the workspace: CLAUDE_PROJECT_DIR, then upward from cwd."""
    candidates = [os.environ.get("CLAUDE_PROJECT_DIR"), payload.get("cwd"), os.getcwd()]
    for candidate in candidates:
        if not candidate:
            continue
        current = Path(candidate).resolve()
        for folder in [current, *current.parents]:
            if (folder / "workspace.json").is_file():
                return folder
    return Path.cwd().resolve()


def film_root(root: Path) -> Path:
    """Return the active film's root folder, or the workspace when unknown."""
    try:
        workspace = json.loads((root / "workspace.json").read_text(encoding="utf-8"))
        active = workspace["activeFilm"]
        for project in workspace["projects"]:
            if project["id"] == active:
                return root / project["root"]
    except (OSError, KeyError, TypeError, ValueError):
        pass
    return root


def lane_name() -> str:
    return os.environ.get(LANE_NAME_ENV) or os.environ.get("AGENT_PARLEY_PARTICIPANT") or "unknown"


def lane_role() -> str:
    return os.environ.get(LANE_ROLE_ENV, "")


def is_producer() -> bool:
    return os.environ.get(PRODUCER_ENV, "") == "1"


def relative_to_root(root: Path, value: str | Path) -> str:
    """Workspace-relative POSIX path for ``value``; absolute form when outside."""
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_evidence(root: Path, film: Path, value: str) -> Path | None:
    """Resolve a handoff path written relative to the workspace or the film."""
    for base in [root, film]:
        candidate = base / value
        if candidate.exists():
            return candidate
    return None


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def log(root: Path, record: dict[str, Any]) -> None:
    film = film_root(root)
    folder = film / "logs"
    try:
        folder.mkdir(parents=True, exist_ok=True)
        with (folder / "hooks.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"ts": now_iso(), "lane": lane_name(), **record}) + "\n")
    except OSError:
        pass


def draft_mistake(root: Path, record: dict[str, Any]) -> None:
    """Append a draft Mistake/Solution entry for the producer to promote."""
    film = film_root(root)
    folder = film / "logs"
    entry = {
        "draft": True,
        "ts": now_iso(),
        "lane": lane_name(),
        "solution": "",
        "rule_added": "",
        **record,
    }
    try:
        folder.mkdir(parents=True, exist_ok=True)
        with (folder / "mistakes-draft.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass


def allow(root: Path, hook: str, **details: Any) -> int:
    log(root, {"hook": hook, "decision": "allow", **details})
    return 0


def deny(root: Path, hook: str, reason: str, **details: Any) -> int:
    log(root, {"hook": hook, "decision": "deny", "reason": reason, **details})
    draft_mistake(
        root,
        {
            "detected_by": f"hook {hook}",
            "mistake": reason,
            "error": reason,
            **{key: value for key, value in details.items() if isinstance(value, (str, int))},
        },
    )
    print(f"[{hook}] {reason}", file=sys.stderr)
    return 2


def parley_reservations() -> list[dict[str, Any]]:
    """Return reservation records from Agent Parley status, best effort.

    The command comes from ``MOVIES_PARLEY_STATUS_CMD`` or defaults to
    ``agent-parley status --json``. Any failure yields an empty list; the
    hook then checks only the producer-owned list.
    """
    command = os.environ.get(STATUS_CMD_ENV, "agent-parley status --json")
    try:
        completed = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        data = json.loads(completed.stdout)
    except (OSError, ValueError, subprocess.SubprocessError):
        return []
    found: list[dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            paths = value.get("paths") or value.get("path")
            owner = value.get("participant") or value.get("owner") or value.get("lane")
            if paths and owner:
                found.append({"owner": str(owner), "paths": [paths] if isinstance(paths, str) else list(paths)})
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(data)
    return found


def new_handoffs(root: Path, film: Path) -> list[Path]:
    """Handoff files added or modified in this checkout since the last commit."""
    handoffs = film / "agents" / "handoffs"
    try:
        completed = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all", "--", str(handoffs)],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return sorted(handoffs.glob("*.json")) if handoffs.is_dir() else []
    result: list[Path] = []
    for line in completed.stdout.splitlines():
        candidate = root / line[3:].strip().strip('"')
        if candidate.suffix == ".json" and candidate.is_file():
            result.append(candidate)
    return sorted(result)


def changed_project_files(root: Path, film: Path) -> list[str]:
    """Workspace-relative paths changed under the film, excluding handoffs and logs."""
    try:
        completed = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all", "--", str(film)],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    skipped = ("/agents/handoffs/", "/logs/")
    result = []
    for line in completed.stdout.splitlines():
        relative = line[3:].strip().strip('"')
        if not any(part in f"/{relative}" for part in skipped):
            result.append(relative)
    return result


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def handoff_problems(root: Path, film: Path, document: dict[str, Any]) -> list[str]:
    """Problems that make a handoff unfit to close a session."""
    problems: list[str] = []
    if not document.get("verification"):
        problems.append("verification[] is empty: name the checks actually run")
    for entry in document.get("changedFiles") or []:
        path = entry.get("path") if isinstance(entry, dict) else None
        expected = entry.get("sha256After") if isinstance(entry, dict) else None
        if not path or not expected:
            problems.append("changedFiles entry without path or sha256After")
            continue
        resolved = resolve_evidence(root, film, str(path))
        if resolved is None:
            problems.append(f"changedFiles path missing on disk: {path}")
        elif sha256_of(resolved) != expected:
            problems.append(f"sha256After does not match disk: {path}")
    for entry in document.get("claims") or []:
        if not isinstance(entry, dict):
            continue
        evidence, expected = entry.get("evidence"), entry.get("sha256")
        if evidence and expected:
            resolved = resolve_evidence(root, film, str(evidence))
            if resolved is not None and resolved.is_file() and sha256_of(resolved) != expected:
                problems.append(f"claim sha256 does not match disk: {evidence}")
    return problems


def has_successor(document: dict[str, Any]) -> bool:
    if document.get("nextActions"):
        return True
    return bool(document.get("stageComplete")) and bool(document.get("stageCompleteReason"))
