#!/usr/bin/env python3
"""Read-only audit of credit-ledger.csv balance-delta windows (stdlib only).

Usage: python3 -B -I ledger_overlap_audit.py LEDGER.csv OUT_PROPOSAL.csv
Never modifies the ledger. Output is a PROPOSAL for the producer to review.
"""
import csv
import re
import sys

ledger, out = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(ledger, newline="", encoding="utf-8")))
WIN = re.compile(r"\((\d+)->(\d+)")

items = []
for i, r in enumerate(rows):
    m = WIN.search(r["charge_status"])
    c = r["credits_consumed"]
    try:
        cv = float(c)
    except ValueError:
        cv = None
    items.append({"i": i, "id": r["entry_id"], "t": r["recorded_at"], "credits": cv,
                  "win": (int(m.group(1)), int(m.group(2))) if m else None,
                  "status": r["charge_status"].split(" ")[0].rstrip(";"), "shot": r["shot_id"]})

recon = [x for x in items if x["win"] and x["status"] == "reconciled_from_balance_delta"]
total = sum(x["credits"] for x in items if x["credits"] is not None)
total_recon = sum(x["credits"] for x in recon)

# union of [low, high] balance intervals for reconciled rows
ivs = sorted((x["win"][1], x["win"][0]) for x in recon)
union, cur = 0, None
for lo, hi in ivs:
    if cur is None:
        cur = [lo, hi]
    elif lo <= cur[1]:
        cur[1] = max(cur[1], hi)
    else:
        union += cur[1] - cur[0]
        cur = [lo, hi]
if cur:
    union += cur[1] - cur[0]

# classify each reconciled row
flag = {}
for a in recon:
    alo, ahi = a["win"][1], a["win"][0]
    contained_by, contains, same = [], [], []
    for b in recon:
        if a is b:
            continue
        blo, bhi = b["win"][1], b["win"][0]
        if (alo, ahi) == (blo, bhi):
            same.append(b["id"])
        elif blo <= alo and ahi <= bhi:
            contained_by.append(b["id"])
        elif alo <= blo and bhi <= ahi:
            contains.append(b["id"])
    flag[a["id"]] = (same, contained_by, contains)

with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["entry_id", "recorded_at", "credits_in_ledger", "window", "overlap_class", "related_entries",
                "proposed_action"])
    n_flag = 0
    for a in recon:
        same, cby, cont = flag[a["id"]]
        if same:
            cls, rel = "IDENTICAL_WINDOW", same
            act = "concurrent jobs share one balance drop; split window among entries (cost per job unknown) or mark charge_status=shared_window"
        elif cby:
            cls, rel = "CONTAINED_IN_OTHER", cby
            act = "window includes another job's charge; keep only this job's own share (credits - contained entries) as uncertain"
        elif cont:
            cls, rel = "CONTAINS_OTHERS", cont
            act = "this window already includes the listed entries; subtract their credits to avoid double count"
        else:
            continue
        n_flag += 1
        w.writerow([a["id"], a["t"], a["credits"], f"{a['win'][0]}->{a['win'][1]}", cls, ";".join(rel), act])

print(f"rows={len(rows)} ledger_sum={total:g} reconciled_rows={len(recon)} reconciled_sum={total_recon:g}")
print(f"union_of_reconciled_windows={union} flagged_rows={n_flag}")
if recon:
    first = max(x["win"][0] for x in recon)
    last = min(x["win"][1] for x in recon)
    print(f"reconciled balance span {first}->{last} = {first - last} (real drop, if contiguous)")
print("non-reconciled statuses:", sorted({x["status"] for x in items if x not in recon}))
