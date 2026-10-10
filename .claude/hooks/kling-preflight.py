#!/usr/bin/env python3
"""PreToolUse gate for paid Kling submissions: scope, balance, schema and identity."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re
import shlex
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "kling-preflight"
MAX_BALANCE_AGE_SECONDS = 15 * 60
GENERATION_VERBS = (
    "text_to_image",
    "image_to_image",
    "text_to_video",
    "image_to_video",
    "motion_control",
    "omni_ref_video",
    "element_create",
)
REQUIRED_SCOPE = (
    "ceiling",
    "grantedBy",
    "balanceBefore",
    "balanceTimestamp",
    "requestSha256",
    "modelInputSlots",
)
IMAGE_KEYS = ("images", "image_list", "inputs", "reference_images", "image_urls")


def is_paid_submission(command: str) -> bool:
    if "kling_batch.py" in command and "--submit-only" in command:
        return True
    return "kling" in command and any(verb in command for verb in GENERATION_VERBS)


def request_path(command: str, root: Path) -> Path | None:
    tokens = shlex.split(command)
    for index, token in enumerate(tokens):
        if token in {"--spec", "--request", "--plan"} and index + 1 < len(tokens):
            candidate = Path(tokens[index + 1])
            return candidate if candidate.is_absolute() else root / candidate
        for flag in ("--spec=", "--request=", "--plan="):
            if token.startswith(flag):
                candidate = Path(token[len(flag):])
                return candidate if candidate.is_absolute() else root / candidate
    return None


def count_images(request: dict) -> int:
    total = 0
    for key in IMAGE_KEYS:
        value = request.get(key)
        if isinstance(value, list):
            total += len(value)
        elif isinstance(value, str):
            total += 1
    for key in sorted(request):
        if re.fullmatch(r"image_\d+", key) and request[key]:
            total += 1
    if total == 0:
        for value in request.values():
            if isinstance(value, dict):
                total = max(total, count_images(value))
    return total


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    if payload.get("tool_name") != "Bash":
        return 0
    command = str((payload.get("tool_input") or {}).get("command") or "")
    if not is_paid_submission(command):
        return 0
    if not _common.is_producer():
        return _common.deny(
            root,
            HOOK,
            "paid submission requires the producer lane holding kling:submit "
            f"({_common.PRODUCER_ENV}=1 on the base checkout)",
            command=command[:300],
        )
    request = request_path(command, root)
    if request is None or not request.is_file():
        return _common.deny(root, HOOK, "cannot locate the request file (--spec/--request)", command=command[:300])
    scope_path = request.with_name("scope.json")
    scope = _common.load_json(scope_path)
    if scope is None:
        return _common.deny(root, HOOK, f"missing scope.json beside {request.name}")
    missing = [field for field in REQUIRED_SCOPE if field not in scope]
    if missing:
        return _common.deny(root, HOOK, f"scope.json lacks {', '.join(missing)}", scope=str(scope_path))
    if "relay" in str(scope["grantedBy"]).lower():
        return _common.deny(root, HOOK, "grantedBy is a relayed approval; Andre must confirm directly (R07)")
    try:
        observed = datetime.fromisoformat(str(scope["balanceTimestamp"]))
    except ValueError:
        return _common.deny(root, HOOK, "balanceTimestamp is not an ISO timestamp")
    if observed.tzinfo is None:
        observed = observed.replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - observed).total_seconds()
    if age > MAX_BALANCE_AGE_SECONDS or age < -60:
        return _common.deny(root, HOOK, f"balanceTimestamp is {int(age)} s old; refresh the live balance by CLI first")
    if _common.sha256_of(request) != scope["requestSha256"]:
        return _common.deny(root, HOOK, "requestSha256 does not match request file; re-scope the exact request")
    request_document = _common.load_json(request) or {}
    images = count_images(request_document)
    try:
        slots = int(scope["modelInputSlots"])
    except (TypeError, ValueError):
        return _common.deny(root, HOOK, "modelInputSlots must be an integer copied from the live schema")
    if images > slots:
        return _common.deny(root, HOOK, f"request passes {images} images but the declared schema accepts {slots} (R08)")
    try:
        ceiling = int(scope["ceiling"])
        balance = int(scope["balanceBefore"])
    except (TypeError, ValueError):
        return _common.deny(root, HOOK, "ceiling and balanceBefore must be integers")
    if ceiling <= 0 or balance < ceiling:
        return _common.deny(root, HOOK, f"ceiling {ceiling} is not covered by balance {balance}")
    return _common.allow(root, HOOK, request=str(request), ceiling=ceiling, balance=balance)


if __name__ == "__main__":
    raise SystemExit(main())
