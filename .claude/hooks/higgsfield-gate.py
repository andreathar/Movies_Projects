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
import hashlib
import json
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
REQUIRED_SCOPE = ("ceiling", "grantedBy", "balanceBefore", "balanceTimestamp", "jobTypes", "uploadScope", "allowedOperations", "commandSha256")
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
            if name in SHELLS:
                if depth >= 3:
                    return None  # Do not assume a deeper shell is read-only.
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
    if any(argument in {"-h", "--help", "--version", "-v"} for argument in arguments) and all(not a.startswith("-") or a in {"-h", "--help", "--version", "-v", "--json"} for a in arguments):
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


SCALAR_FLAGS = {"--prompt", "--negative-prompt", "--duration", "--resolution", "--aspect-ratio", "--seed", "--quality", "--image-count", "--img-resolution", "--wait-timeout", "--wait-interval", "--generate-audio", "--mode", "--format", "--strength", "--should-texture"}
BOOLEAN_FLAGS = {"--wait", "--json"}
MEDIA_FLAGS = {"--image", "--video", "--audio", "--start-image", "--end-image",
               "--image-references", "--video-references", "--audio-references"}


def command_digest(arguments: list[str]) -> str:
    """Bind approval to exact CLI argv after the executable, not just a model name."""
    return hashlib.sha256(json.dumps(arguments, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def paid_arguments(arguments: list[str]) -> list[str]:
    """Remove only recognized global options before a plain command group."""
    args = list(arguments)
    while args and args[0].startswith("-"):
        if args[0] == "--json":
            args.pop(0)
        elif args[0] == "--workspace" and len(args) > 1:
            del args[:2]
        else:
            return []
    if args and args[0] == "gen":
        args[0] = "generate"
    return args


def scoped_media_problem(root: Path, arguments: list[str], operation: str, scope: Any) -> str | None:
    values = []
    if operation == "upload:create":
        if len(arguments) < 3 or any(a not in {"--image", "--video", "--audio"} for a in arguments[3:]):
            return "uploadScope requires one exact file and optional media-type flag"
        values.append(arguments[2])
    else:
        index = 3
        while index < len(arguments):
            token = arguments[index]
            key, equal, value = token.partition("=")
            key = key.replace("_", "-")
            if key in MEDIA_FLAGS:
                if not equal:
                    index += 1
                    value = arguments[index] if index < len(arguments) else ""
                if not value or value.startswith("--"):
                    return "uploadScope cannot verify a missing media value"
                values.append(value)
            elif key in SCALAR_FLAGS:
                if not equal:
                    index += 1
                    if index >= len(arguments) or arguments[index].startswith("--"):
                        return "ambiguous scalar parameter value in scoped command"
            elif key in BOOLEAN_FLAGS:
                if equal:
                    return "ambiguous boolean flag in scoped command"
            else:
                return "uploadScope cannot verify this unknown option/operand"
            index += 1
    if not values:
        return None
    if not isinstance(scope, dict) or set(scope) != {"files", "mediaIds"} or not isinstance(scope["files"], list) or not isinstance(scope["mediaIds"], list):
        return "uploadScope does not authorize media inputs (local files auto-upload)"
    files = {}
    for item in scope["files"]:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"} or not isinstance(item["path"], str) or not isinstance(item["sha256"], str) or not re.fullmatch(r"[a-f0-9]{64}", item["sha256"]):
            return "uploadScope file records require exact path and SHA-256"
        path = Path(item["path"])
        if path.is_absolute() or ".." in path.parts or not item["path"]:
            return "uploadScope files must be workspace-relative"
        target = (root / path).resolve()
        if not target.is_relative_to(root.resolve()) or str(target) in files:
            return "uploadScope contains an escaped or duplicate path"
        files[str(target)] = item["sha256"]
    if any(not isinstance(v, str) or not re.fullmatch(r"[a-fA-F0-9-]{36}", v) for v in scope["mediaIds"]):
        return "uploadScope mediaIds must be explicit UUIDs"
    for value in values:
        path = Path(value)
        target = (root / path).resolve() if not path.is_absolute() else path.resolve()
        if operation != "upload:create" and value in scope["mediaIds"]:
            continue
        expected = files.get(str(target))
        if not expected or not target.is_relative_to(root.resolve()) or not target.is_file() or _common.sha256_of(target) != expected:
            return "uploadScope does not cover the exact media path/hash or ID"
    return None


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
    ceiling, balance = scope["ceiling"], scope["balanceBefore"]
    if type(ceiling) is not int or type(balance) is not int:
        return "ceiling and balanceBefore must be integers"
    if ceiling <= 0 or balance < ceiling:
        return f"ceiling {ceiling} is not covered by balance {balance}"
    if not isinstance(scope["grantedBy"], str) or not scope["grantedBy"].strip() or "REPLACE" in scope["grantedBy"].upper():
        return "grantedBy must cite the direct grant, not a template placeholder"
    args = paid_arguments(arguments)
    if len(args) < 3 or args[:2] not in (["generate", "create"], ["upload", "create"]):
        return "unsupported scoped operation; only explicit generate:create or upload:create is implemented"
    operation = ":".join(args[:2])
    operations = scope["allowedOperations"]
    if not isinstance(operations, list) or operation not in operations or any(not isinstance(x, str) or x not in {"generate:create", "upload:create"} for x in operations):
        return "operation is not listed in allowedOperations"
    allowed = scope["jobTypes"]
    if not isinstance(allowed, list) or any(not isinstance(v, str) or not re.fullmatch(r"[a-zA-Z0-9_]+", v) for v in allowed) or len(set(allowed)) != len(allowed):
        return "jobTypes must be an explicit unique list"
    if operation == "generate:create" and (not allowed or args[2] not in allowed):
        return "job type is not listed in scope jobTypes"
    if scope["commandSha256"] != command_digest(arguments):
        return "commandSha256 does not match the exact CLI arguments"
    return scoped_media_problem(root, args, operation, scope["uploadScope"])



def gate_cli(root: Path, command: str) -> int:
    if "$" in command or "`" in command or "\\" in command:
        return _common.deny(root, HOOK, "ambiguous shell expansion in Higgsfield command")
    found = invocations(command)
    if found is None:
        if "higgs" in command.lower() or re.search(r"\bhf\b", command.lower()):
            return _common.deny(root, HOOK, "command has unbalanced quoting; rewrite it plainly before any Higgsfield call")
        return 0
    for arguments in found:
        kind, label = classify(arguments)
        if kind == "read":
            pos = positionals(arguments)
            if pos[:2] in (["generate", "cost"], ["gen", "cost"]) and any(a.split("=", 1)[0].replace("_", "-") in MEDIA_FLAGS for a in arguments):
                return _common.deny(root, HOOK, "media-bearing cost lookup is not established read-only; no implicit upload is allowed")
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
        plain = _common.plain_command(command)
        if plain is None or not plain or Path(plain[0]).name not in PROGRAMS | {"hf"} or len(found) != 1:
            return _common.deny(root, HOOK, "paid/writing Higgsfield commands must be one plain invocation; wrapped, chained or ambiguous commands are refused")
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
