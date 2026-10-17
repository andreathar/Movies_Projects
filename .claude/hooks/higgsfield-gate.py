#!/usr/bin/env python3
"""PreToolUse gate for Higgsfield: anything that is not read-only is producer-only.

Covers the installed CLI (``higgsfield`` / ``higgs``) and the Higgsfield MCP connector.
Read-only commands (account, model, cost estimates, list/get/wait) pass. Everything else
(generate, upload, soul-id create, project writes, auth login) needs the producer lane and
a fresh scope record; ``auth token`` is always refused. The MCP connector cannot generate:
the CLI behind this gate is the single paid channel, as for Kling.
"""

from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
import re
import shlex
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "higgsfield-gate"
MAX_BALANCE_AGE_SECONDS = 15 * 60
SCOPE_ENV = "HIGGSFIELD_SCOPE"
SCOPE_DEFAULT = "00_brief/higgsfield-scope.json"
REQUIRED_SCOPE = ("ceiling", "grantedBy", "balanceBefore", "balanceTimestamp")
PROGRAMS = {"higgsfield", "higgs"}
# `hf` is also the Hugging Face CLI; treat it as Higgsfield only for Higgsfield-only groups.
HF_ONLY_GROUPS = {
    "generate", "gen", "product-photoshoot", "marketplace-cards", "marketplace-card",
    "cards", "soul-id", "marketing-studio", "marketing", "ms",
}
WRAPPERS = {"env", "sudo", "time", "nohup", "command", "exec", "nice", "stdbuf", "timeout", "npx", "bunx", "pnpx"}
SHELLS = {"bash", "sh", "zsh", "dash"}
SEPARATORS = {"&&", "||", ";", "|", "&", "(", ")", "|&", ";;"}
VALUE_FLAGS = {"--workspace"}
READ_VERBS = {"list", "get", "status", "wait", "cost", "transactions", "resolve", "help", "version", "show"}
WRITE_VERBS = {
    "create", "workflow", "delete", "update", "archive", "unarchive", "publication", "train",
    "login", "logout", "token", "set", "add", "remove", "fetch", "generate", "submit", "run",
}
MCP_READ_EXACT = {
    "balance", "transactions", "models_explore", "jobs_wait", "job_display", "apps_search",
    "apps_describe", "ads_studio_quote", "ai_influencer_prepare", "resolve_project_assets",
    "resolve_explainer_preset", "tiktok_accounts", "tiktok_music_trending", "video_analysis_status",
    "video_analysis_jobs", "shorts_studio_status", "website_status",
}
MCP_READ_PATTERN = re.compile(
    r"^(?:(?:ads_studio|ai_influencer|shorts_studio|scene_builder_3d|project|website)_)?"
    r"(?:list|get|show|search|query)_"
)
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
DURATION = re.compile(r"^\d+(?:\.\d+)?[smhd]?$")


def tokenize(command: str) -> list[str] | None:
    """Shell tokens with operators split out; None when the quoting is unbalanced."""
    lexer = shlex.shlex(command.replace("\n", " ; "), posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:
        return None


def segments(tokens: list[str]) -> list[list[str]]:
    result: list[list[str]] = [[]]
    for token in tokens:
        if token in SEPARATORS:
            result.append([])
        else:
            result[-1].append(token)
    return [segment for segment in result if segment]


def invocations(command: str, depth: int = 0) -> list[list[str]] | None:
    """Argument lists (after the program) for every Higgsfield invocation in ``command``."""
    tokens = tokenize(command)
    if tokens is None:
        return None
    found: list[list[str]] = []
    for segment in segments(tokens):
        index = 0
        while index < len(segment):
            token = segment[index]
            name = Path(token).name
            if ASSIGNMENT.match(token) or token in WRAPPERS or token.startswith("-") or DURATION.match(token):
                index += 1
                continue
            if name in SHELLS and depth < 3:
                rest = segment[index + 1:]
                for position, item in enumerate(rest):
                    if item in {"-c", "-lc", "-ic", "-xc"} and position + 1 < len(rest):
                        nested = invocations(rest[position + 1], depth + 1)
                        if nested is None:
                            return None
                        found.extend(nested)
                        break
                break
            program = "@higgsfield/cli" if token.startswith("@higgsfield/cli") else name
            if program in PROGRAMS or program == "@higgsfield/cli":
                found.append(segment[index + 1:])
            elif name == "hf" and positionals(segment[index + 1:])[:1] and positionals(segment[index + 1:])[0] in HF_ONLY_GROUPS:
                found.append(segment[index + 1:])
            break
    return found


def positionals(arguments: list[str]) -> list[str]:
    result: list[str] = []
    skip = False
    for argument in arguments:
        if skip:
            skip = False
        elif argument in VALUE_FLAGS:
            skip = True
        elif argument.startswith("-"):
            continue
        else:
            result.append(argument)
    return result


def classify(arguments: list[str]) -> tuple[str, str]:
    """Return ("read" | "token" | "paid", label) for one invocation."""
    if any(argument in {"-h", "--help", "--version", "-v"} for argument in arguments):
        return "read", "help"
    pos = positionals(arguments)
    if not pos or pos[0] in {"help", "version"}:
        return "read", "help"
    label = " ".join(pos[:3])
    if pos[0] == "auth" and len(pos) > 1 and pos[1] == "token":
        return "token", label
    if len(pos) > 1 and pos[1] in READ_VERBS:
        return "read", label
    if len(pos) > 2 and pos[2] in READ_VERBS and pos[1] not in WRITE_VERBS:
        return "read", label
    return "paid", label


def mcp_read_only(tool_name: str) -> bool:
    suffix = tool_name.rsplit("__", 1)[-1]
    return suffix in MCP_READ_EXACT or bool(MCP_READ_PATTERN.match(suffix))


def scope_problem(root: Path, label: str, arguments: list[str]) -> str | None:
    """Why the producer's scope record does not cover this call; None when it does."""
    configured = os.environ.get(SCOPE_ENV)
    path = Path(configured) if configured else _common.film_root(root) / SCOPE_DEFAULT
    if not path.is_absolute():
        path = root / path
    scope = _common.load_object(path)
    if scope is None:
        return f"missing scope record {_common.relative_to_root(root, path)} (template: shared/templates/higgsfield-scope.json)"
    missing = [field for field in REQUIRED_SCOPE if field not in scope]
    if missing:
        return f"scope record lacks {', '.join(missing)}"
    if "relay" in str(scope["grantedBy"]).lower():
        return "grantedBy is a relayed approval; Andre must confirm directly"
    try:
        observed = datetime.fromisoformat(str(scope["balanceTimestamp"]))
    except ValueError:
        return "balanceTimestamp is not an ISO timestamp"
    if observed.tzinfo is None:
        return "balanceTimestamp must include the UTC offset (for example -03:00)"
    age = (datetime.now(timezone.utc) - observed).total_seconds()
    if age > MAX_BALANCE_AGE_SECONDS or age < -60:
        return f"balanceTimestamp is {int(age)} s old; run `higgsfield account status` and refresh the scope first"
    try:
        ceiling, balance = int(scope["ceiling"]), int(scope["balanceBefore"])
    except (TypeError, ValueError):
        return "ceiling and balanceBefore must be integers"
    if ceiling <= 0 or balance < ceiling:
        return f"ceiling {ceiling} is not covered by balance {balance}"
    allowed = scope.get("jobTypes")
    pos = positionals(arguments)
    if isinstance(allowed, list) and allowed and pos[:2] == ["generate", "create"]:
        if len(pos) < 3 or pos[2] not in allowed:
            return f"job type {pos[2] if len(pos) > 2 else '?'} is not listed in scope jobTypes"
    return None


def gate_cli(root: Path, command: str) -> int:
    found = invocations(command)
    if found is None:
        if "higgs" in command.lower():
            return _common.deny(root, HOOK, "command has unbalanced quoting; rewrite it plainly before any Higgsfield call")
        return 0
    for arguments in found:
        kind, label = classify(arguments)
        if kind == "read":
            continue
        if kind == "token":
            return _common.deny(root, HOOK, "`auth token` prints credentials; never read or echo them", command=command[:300])
        if not _common.is_producer():
            return _common.deny(
                root,
                HOOK,
                f"`higgsfield {label}` creates, uploads or spends; it requires the producer lane "
                f"({_common.PRODUCER_ENV}=1 on the base checkout) and a scope record",
                command=command[:300],
            )
        problem = scope_problem(root, label, arguments)
        if problem:
            return _common.deny(root, HOOK, problem, command=command[:300])
    return _common.allow(root, HOOK, invocations=len(found)) if found else 0


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    tool = str(payload.get("tool_name") or "")
    tool_input: dict[str, Any] = payload.get("tool_input") or {}
    if tool == "Bash":
        command = str(tool_input.get("command") or "")
        lowered = command.lower()
        if "higgs" not in lowered and not re.search(r"\bhf\b", lowered):
            return 0
        return gate_cli(root, command)
    if tool.startswith("mcp__") and "higgsfield" in tool.lower():
        if mcp_read_only(tool):
            return 0
        return _common.deny(
            root,
            HOOK,
            f"{tool.rsplit('__', 1)[-1]} would create, change or spend through the Higgsfield connector; "
            "use the CLI behind this gate (producer lane + scope record)",
            tool=tool,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
