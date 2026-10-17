#!/usr/bin/env python3
"""PreToolUse gate: a job already submitted or closed is never submitted again."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "no-retry"
TERMINAL = ("completed", "failed", "succeed", "accepted", "rejected", "reconciled", "canceled", "cancelled")
STORED_KINDS = ("intent", "submit", "response")


def ledger_jobs(film: Path) -> dict[str, str]:
    """Map shot/job ids in credit-ledger.csv to their charge status."""
    ledger = film / "credit-ledger.csv"
    jobs: dict[str, str] = {}
    if not ledger.is_file():
        return jobs
    with ledger.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            job = (row.get("shot_id") or "").strip()
            if job:
                jobs[job] = (row.get("charge_status") or "").lower()
    return jobs


def stored(film: Path, job: str) -> bool:
    responses = film / "07_generations" / "responses"
    return any((responses / f"{job}.{kind}.json").exists() for kind in STORED_KINDS)


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    film = _common.film_root(root)
    if payload.get("tool_name") != "Bash":
        return 0
    command = str((payload.get("tool_input") or {}).get("command") or "")
    if "kling_batch.py" not in command:
        return 0
    if _common.proven_read_only(command):
        return 0
    tokens = _common.split_command(command)
    if tokens is None:
        return _common.allow(root, HOOK, note="unbalanced quoting; preflight decides")
    batch = _common.batch_invocation(tokens)
    if batch is None or batch["resume"]:
        return 0
    jobs = _common.spec_jobs(root, batch["spec"]) or []
    names = [str(job.get("job")) for job in jobs if job.get("job")]
    if batch["only"]:
        names = [name for name in names if name in batch["only"]]
    ledger = ledger_jobs(film)
    closed = sorted(
        name
        for name in names
        if stored(film, name) or any(word in ledger.get(name, "") for word in TERMINAL)
    )
    if closed:
        return _common.deny(
            root,
            HOOK,
            f"job(s) already submitted or closed: {', '.join(closed)}; "
            "a new hypothesis needs a new job id and a new scoped request, never a resubmission",
            command=command[:300],
        )
    return _common.allow(root, HOOK, jobs=",".join(names))


if __name__ == "__main__":
    raise SystemExit(main())
