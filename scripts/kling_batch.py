#!/usr/bin/env python3
"""Producer-only Kling batch submitter for Movies_Projects.

Submits ONE approved job through the installed `kling` CLI, polls, archives the
request/response, downloads works to 07_generations/originals, and appends a
credit-ledger row reconciled from account balance deltas. Never retries.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TELEMETRY = ["--skill-name", "kling-cli", "--skill-version", "0.2.0"]


def run(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = proc.stdout.strip()
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"ok": False, "raw": out, "stderr": proc.stderr[-2000:], "rc": proc.returncode}


def account() -> int | None:
    data = run(["kling", "account", "-q", *TELEMETRY])
    try:
        return int(data["body"]["availableRemainCredits"])
    except Exception:
        return None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def submit(film: Path, job: str, tool: str, model: str, prompt: str, args: dict[str, str],
           images: list[str], auth: str, note: str, poll: int = 300) -> dict:
    req_dir = film / "07_generations/requests"
    res_dir = film / "07_generations/responses"
    orig = film / "07_generations/originals"
    for d in (req_dir, res_dir, orig):
        d.mkdir(parents=True, exist_ok=True)
    if (res_dir / f"{job}.response.json").exists():
        raise SystemExit(f"{job}: response already exists; never resubmit")
    (req_dir / f"{job}.prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    before = account()
    cmd = ["kling", tool, "--model", model, "--poll", str(poll), "-q", *TELEMETRY,
           "--rationale", f"Film reference batch {auth}: {note}"]
    for img in images:
        p = (film / img) if not img.startswith("http") else None
        if p is not None and not p.is_file():
            raise SystemExit(f"missing reference: {img}")
        cmd += ["--image", str(p) if p else img]
    for k, v in args.items():
        cmd += [f"--{k}", str(v)]
    cmd.append(prompt)
    started = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    data = run(cmd)
    (res_dir / f"{job}.response.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    gens = (data.get("body") or {}).get("generations") or []
    gen_id = gens[0].get("generationId") if gens else data.get("body", {}).get("generationId")
    status = gens[0].get("status") if gens else data.get("body", {}).get("status")
    works = []
    if gens:
        for i, w in enumerate((gens[0].get("result") or {}).get("works") or [], start=1):
            url = w.get("urlWithoutWatermark") or w.get("url")
            if not url:
                continue
            ext = ".png" if "png" in url.lower() else ".jpg"
            target = orig / f"{job}_{i}{ext}"
            urllib.request.urlretrieve(url, target)
            meta = {"job": job, "generationId": gen_id, "tool": tool, "model": model,
                    "options": args, "refs": images, "prompt": prompt,
                    "provenance": "synthetic_fictional_casting", "approved": False,
                    "sha256": sha256(target), "url": url, "note": note, "created": started}
            (orig / f"{job}_{i}.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
            works.append(str(target.relative_to(film)))
    after = account()
    delta = (before - after) if (before is not None and after is not None) else None
    ledger = film / "credit-ledger.csv"
    with ledger.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow([f"L{job}", started, "Kling", gen_id or "", job, "", delta if delta is not None else "",
                    f"reconciled_from_balance_delta ({before}->{after}); status {status}", after or "",
                    auth, f"{model} {tool} {json.dumps(args)} x{len(works)} works; {note}"])
    return {"job": job, "generationId": gen_id, "status": status, "works": works,
            "creditsDelta": delta, "balanceBefore": before, "balanceAfter": after,
            "error": None if data.get("ok", True) else data}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--film", default="projects/andre-time-travel")
    ap.add_argument("--spec", required=True, help="JSON file with job list")
    ap.add_argument("--only", help="comma-separated job ids to run")
    a = ap.parse_args()
    film = (ROOT / a.film).resolve()
    jobs = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    only = set(a.only.split(",")) if a.only else None
    results = []
    for j in jobs:
        if only and j["job"] not in only:
            continue
        r = submit(film, j["job"], j["tool"], j["model"], j["prompt"], j.get("args", {}),
                   j.get("images", []), j["auth"], j.get("note", ""))
        print(json.dumps(r))
        results.append(r)
        if r["status"] != "COMPLETED":
            print("STOP: non-completed status; no automatic retry", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
