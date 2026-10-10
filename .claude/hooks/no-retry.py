#!/usr/bin/env python3
"""PreToolUse gate: never resubmit or re-resume a job the ledger already closed."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import re
import shlex
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

HOOK = "no-retry"
TERMINAL = ("completed", "failed", "succeed", "accepted", "rejected", "reconciled", "canceled", "cancelled")
JOB_PATTERN = re.compile(r"[A-Za-z0-9_-]{8,}")


def ledger_jobs(film: Path) -> dict[str, str]:
    ledger = film / "credit-ledger.csv"
    jobs: dict[str, str] = {}
    if not ledger.is_file():
        return jobs
    with ledger.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            job = (row.get("generation_id") or "").strip()
            if job:
                jobs[job] = (row.get("charge_status") or "").lower()
    return jobs


def job_ids_in_spec(path: Path) -> set[str]:
    document = _common.load_json(path) or {}
    found: set[str] = set()

    def walk(value: object) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in {"generation_id", "generationId", "job_id", "jobId"} and isinstance(child, str):
                    found.add(child)
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(document)
    return found


def main() -> int:
    payload = _common.read_payload()
    root = _common.workspace_root(payload)
    film = _common.film_root(root)
    if payload.get("tool_name") != "Bash":
        return 0
    command = str((payload.get("tool_input") or {}).get("command") or "")
    if "--resume" not in command and "--submit-only" not in command:
        return 0
    jobs = ledger_jobs(film)
    tokens = shlex.split(command)
    candidates: set[str] = set()
    for index, token in enumerate(tokens):
        if token == "--resume" and index + 1 < len(tokens):
            candidates.add(tokens[index + 1])
        elif token.startswith("--resume="):
            candidates.add(token.split("=", 1)[1])
        elif token in {"--spec", "--plan", "--request"} and index + 1 < len(tokens):
            spec = Path(tokens[index + 1])
            candidates |= job_ids_in_spec(spec if spec.is_absolute() else root / spec)
    closed = sorted(
        job for job in candidates if job in jobs and any(word in jobs[job] for word in TERMINAL)
    )
    if closed:
        return _common.deny(
            root,
            HOOK,
            f"job(s) already closed in credit-ledger.csv: {', '.join(closed)}; "
            "a new hypothesis needs a new scoped request, never a resubmission",
            command=command[:300],
        )
    return _common.allow(root, HOOK, candidates=json.dumps(sorted(candidates)))


if __name__ == "__main__":
    raise SystemExit(main())
