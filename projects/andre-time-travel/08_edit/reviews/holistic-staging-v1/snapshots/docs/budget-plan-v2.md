# Budget plan v2 — 2026-10-09

Status: **producer decision under APR-blanket-2026-10-09**. Live Kling balance read via CLI at 2026-10-09T09:23:16-03:00: **6,981 credits** (SSVIP). ElevenLabs: 479.95 credits already spent on 5 test lines; no new ElevenLabs scope opened by this plan.

## Observed unit costs (evidence)
- R1 batch: 32 image jobs, 760 credits reconciled from balance deltas (ledger), 46 images delivered → **≈16.5 credits per image, ≈24 per job** (gemini-3-pro-image i2i 2K; 2-image jobs ≈ 40).
- Video has never been generated on this account: **no video unit cost is known.** The pilot establishes it.

## Allocation (ceiling 6,981; planning numbers, not prices)
| Phase | Cap | Purpose | Release condition |
|---|---|---|---|
| R2 references (images) | **450** | 5 figures × 2 eye states on one base each (≈10 imgs, Napoleon recast adds ≈2 candidates); 5 hand/table inserts on anchor J26-2; 2 spares | Decisions D04/D05 recorded (done); live balance re-read; prompts reviewed by continuity |
| R3 Andre keyframes (images) | **400** | 10 era keyframes (speaking/listening ×5) + 2 present-day | **After** photo session (D08) and Element (T04) |
| Identity + speech pilot (video) | **1,100** | Element creation; 4 restrained shots; 1 speech-route test; 2 corrections | Element verified; speech-route matrix read |
| Main footage (5 chapters + open/close) | **3,300** | 41 slots ≈ 35 paid video jobs + inserts | Pilot accepted by Andre; reforecast from real video cost |
| Corrections + Edition H picture variants | **1,300** | Measured gaps, mouth-visible language variants | Picture lock of Edition E |
| Final reserve | **431** | Not allocated | Producer only |
| **Total** | **6,981** | | |

Rules: each batch gets a scope record in `00_brief/approvals.json` with ceiling, balance before/after and per-job IDs; `creditsConsumed` recorded when returned, else reconciled from balance deltas and marked so; no retries without a new record; stop any batch at 90 % of its cap and reconcile before continuing.

## Next paid batch — R2 references (scope APR-R2-references-2026-10-09)
Submitted only by the producer agent, after the speech-route/capability matrix is read (live model tokens and reference limits). Order: Napoleon recast candidates (2) → approve one → expression deltas for all five (5) → five table inserts (5) → spares if needed. Every output: review full frame + crop, eyes-only rule, no readable text, no extra fingers; log to `credit-ledger.csv`; file under `07_generations/` with sidecars; crops to `02_references/history-eyes/<figure>/` as v2.
