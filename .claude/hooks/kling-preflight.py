#!/usr/bin/env python3
"""PreToolUse gate for paid Kling submissions: scope, balance, schema and identity."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "kling-preflight"
MAX_BALANCE_AGE_SECONDS = 15 * 60
GENERATION_VERBS = {
    "text_to_image",
    "image_to_image",
    "text_to_video",
    "image_to_video",
    "motion_control",
    "omni_ref_video",
    "element_create",
}
REQUIRED_SCOPE = (
    "ceiling",
    "grantedBy",
    "balanceBefore",
    "balanceTimestamp",
    "requestSha256",
    "modelInputSlots",
)
IMAGE_KEYS = ("images", "image_list", "inputs", "reference_images", "image_urls")


def cli_generation(tokens: list[str]) -> bool:
    """True when the executed program is the Kling CLI and a generation verb follows."""
    executable = next((token for token in tokens if not ("=" in token and not token.startswith("-"))), "")
    program = Path(executable).name
    return program.startswith("kling") and any(token in GENERATION_VERBS for token in tokens[1:])


def count_images(job: dict[str, Any]) -> int:
    total = 0
    for key in IMAGE_KEYS:
        value = job.get(key)
        if isinstance(value, list):
            total += len(value)
        elif isinstance(value, str) and value:
            total += 1
    for key, value in job.items():
        if key.startswith("image_") and key[6:].isdigit() and value:
            total += 1
    arguments = job.get("args")
    if total == 0 and isinstance(arguments, dict):
        total = count_images(arguments)
    return total


def selected_jobs(jobs: list[dict[str, Any]], only: list[str]) -> list[dict[str, Any]]:
    if not only:
        return jobs
    return [job for job in jobs if str(job.get("job")) in only]


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    if payload.get("tool_name") != "Bash":
        return 0
    command = str((payload.get("tool_input") or {}).get("command") or "")
    if "kling" not in command:
        return 0
    tokens = _common.split_command(command)
    if tokens is None:
        return _common.deny(root, HOOK, "command has unbalanced quoting; rewrite it plainly before any paid call")
    batch = _common.batch_invocation(tokens)
    if batch is not None:
        if batch["resume"]:
            return 0
        paid = True
    else:
        paid = cli_generation(tokens)
    if not paid:
        return 0
    if not _common.is_producer():
        return _common.deny(
            root,
            HOOK,
            "paid submission requires the producer lane holding kling:submit "
            f"({_common.PRODUCER_ENV}=1 on the base checkout)",
            command=command[:300],
        )
    if batch is None:
        return _common.deny(
            root,
            HOOK,
            "direct CLI generation is not allowed; submit through scripts/kling_batch.py with a scoped request",
            command=command[:300],
        )
    spec = batch["spec"]
    request = Path(spec) if spec and Path(spec).is_absolute() else (root / spec if spec else None)
    if request is None or not request.is_file():
        return _common.deny(root, HOOK, "cannot locate the request spec (--spec)", command=command[:300])
    scope_path = request.with_name("scope.json")
    scope = _common.load_object(scope_path)
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
        return _common.deny(root, HOOK, "balanceTimestamp must include the UTC offset (for example -03:00)")
    age = (datetime.now(timezone.utc) - observed).total_seconds()
    if age > MAX_BALANCE_AGE_SECONDS or age < -60:
        return _common.deny(root, HOOK, f"balanceTimestamp is {int(age)} s old; refresh the live balance by CLI first")
    if _common.sha256_of(request) != scope["requestSha256"]:
        return _common.deny(root, HOOK, "requestSha256 does not match the spec file; re-scope the exact request")
    jobs = _common.spec_jobs(root, str(request))
    if jobs is None:
        return _common.deny(root, HOOK, "spec is not a JSON list of jobs")
    chosen = selected_jobs(jobs, batch["only"])
    if not chosen:
        return _common.deny(root, HOOK, "no job selected by --only exists in the spec")
    try:
        slots = int(scope["modelInputSlots"])
        ceiling = int(scope["ceiling"])
        balance = int(scope["balanceBefore"])
    except (TypeError, ValueError):
        return _common.deny(root, HOOK, "modelInputSlots, ceiling and balanceBefore must be integers")
    for job in chosen:
        images = count_images(job)
        if images > slots:
            return _common.deny(
                root,
                HOOK,
                f"job {job.get('job')} passes {images} images but the declared schema accepts {slots} (R08)",
            )
    if ceiling <= 0 or balance < ceiling:
        return _common.deny(root, HOOK, f"ceiling {ceiling} is not covered by balance {balance}")
    return _common.allow(root, HOOK, request=str(request), jobs=len(chosen), ceiling=ceiling, balance=balance)


if __name__ == "__main__":
    raise SystemExit(main())
