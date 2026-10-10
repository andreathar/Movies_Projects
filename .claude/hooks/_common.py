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
import re
import shlex
import subprocess
import sys
from typing import Any

PRODUCER_ENV = "MOVIES_PRODUCER_LANE"
LANE_NAME_ENV = "MOVIES_LANE_NAME"
LANE_ROLE_ENV = "MOVIES_LANE_ROLE"
SECRET_PATTERN = re.compile(
    r"((?:--?|\b)(?:token|api[-_]?key|secret|password|authorization|bearer)\s*[=: ]\s*)\S+",
    re.IGNORECASE,
)


def read_payload() -> dict[str, Any]:
    """Return the hook payload from stdin, or an empty object on bad input."""
    try:
        value = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError, ValueError):
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


def split_command(command: str) -> list[str] | None:
    """Tokenize a shell command; None when the quoting is unbalanced."""
    try:
        return shlex.split(command, comments=True)
    except ValueError:
        return None


def redact(text: str) -> str:
    return SECRET_PATTERN.sub(r"\1[redacted]", text)


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
    if not value:
        return None
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
    """Append a draft Mistake/Solution entry for the lane to copy into its handoff."""
    film = film_root(root)
    folder = film / "logs"
    entry = {
        "draft": True,
        "ts": now_iso(),
        "lane": lane_name(),
        "solution": "",
        "rule_added": "",
        **{key: (redact(value) if isinstance(value, str) else value) for key, value in record.items()},
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
    safe = {key: (redact(value) if isinstance(value, str) else value) for key, value in details.items()}
    log(root, {"hook": hook, "decision": "deny", "reason": redact(reason), **safe})
    draft_mistake(
        root,
        {
            "detected_by": f"hook {hook}",
            "mistake": reason,
            "error": reason,
            **{key: value for key, value in safe.items() if isinstance(value, (str, int))},
        },
    )
    print(f"[{hook}] {redact(reason)}", file=sys.stderr)
    return 2


def git_status_paths(root: Path, scope: Path) -> list[str] | None:
    """Workspace-relative changed paths under ``scope``; None when git is unavailable."""
    try:
        completed = subprocess.run(
            ["git", "status", "--porcelain", "-z", "--untracked-files=all", "--", str(scope)],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    entries = completed.stdout.split("\0")
    result: list[str] = []
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if len(entry) < 4:
            continue
        status, path = entry[:2], entry[3:]
        if status[0] in "RC":
            index += 1
        result.append(path)
    return result


def new_handoffs(root: Path, film: Path) -> list[Path]:
    """Handoff files added or modified in this checkout since the last commit."""
    handoffs = film / "agents" / "handoffs"
    paths = git_status_paths(root, handoffs)
    if paths is None:
        return sorted(handoffs.glob("*.json")) if handoffs.is_dir() else []
    result = [root / path for path in paths]
    return sorted(path for path in result if path.suffix == ".json" and path.is_file())


def changed_project_files(root: Path, film: Path) -> list[str]:
    """Workspace-relative paths changed under the film, excluding handoffs and logs."""
    paths = git_status_paths(root, film) or []
    skipped = ("/agents/handoffs/", "/logs/")
    return [path for path in paths if not any(part in f"/{path}" for part in skipped)]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def load_object(path: Path) -> dict[str, Any] | None:
    value = load_json(path)
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
        elif resolved.is_dir():
            problems.append(f"changedFiles path is a directory, list its files instead: {path}")
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


def batch_invocation(tokens: list[str]) -> dict[str, Any] | None:
    """Parse a ``kling_batch.py`` invocation into spec, only and mode fields."""
    if not any(token.endswith("kling_batch.py") for token in tokens):
        return None
    result: dict[str, Any] = {"spec": None, "only": [], "resume": None, "submit_only": False}
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "--submit-only":
            result["submit_only"] = True
        elif token == "--resume" and index + 1 < len(tokens):
            result["resume"] = tokens[index + 1]
            index += 1
        elif token.startswith("--resume="):
            result["resume"] = token.split("=", 1)[1]
        elif token in {"--spec", "--only"} and index + 1 < len(tokens):
            result[token[2:]] = tokens[index + 1]
            index += 1
        elif token.startswith("--spec=") or token.startswith("--only="):
            result[token[2:6]] = token.split("=", 1)[1]
        index += 1
    if isinstance(result["only"], str):
        result["only"] = [job for job in result["only"].split(",") if job]
    return result


def spec_jobs(root: Path, spec: str | None) -> list[dict[str, Any]] | None:
    """Jobs from a kling_batch spec (a JSON list); None when unreadable."""
    if not spec:
        return None
    path = Path(spec)
    document = load_json(path if path.is_absolute() else root / path)
    if isinstance(document, dict):
        document = document.get("jobs")
    if not isinstance(document, list):
        return None
    return [job for job in document if isinstance(job, dict)]
