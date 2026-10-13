---
plan: implementation-plan
scene: G-P03          # Galileo, "Escuta durante G-L03", family F4, 5 s, image_to_video
task: T13
version: 1
status: blueprint-not-released
created: 2026-10-13
machine_readable: implementation-plan-G-P03-v1.json
consumer: orchestration skill (future; see "Orchestration note")
paid_actions_authorized: none
---

# Implementation plan — G-P03 (Galileo listening beat)

Why this scene: it is the smallest packet on the board (5 s, one reference, no speech) and
matches workflow-map §4 priority 5 ("next minimal shot packet, measured timing and cost scope").
Nothing here submits, uploads or spends. Every step is gated; a failed gate stops the chain.

## Inputs (hash-pinned)
| Input | Path | sha256 | State |
|---|---|---|---|
| G-IN (composition) | 05_storyboard/keyframes/chatgpt-in-out-v1/03-galileo-in.png | 4bd1e7dd…b28d4 | static_checked, director pending |
| Upstream shot | G-LISTEN-KF (selected reaction keyframe) | — | proposed, not approved |
| Template | `production_plan.py template --family F4 --shot G-P03` | — | `first_image` is still a placeholder |

## Steps
| # | Step | Owner → executor | Gate (pass condition) | Command / evidence |
|---|---|---|---|---|
| 1 | Register G-IN and G-LISTEN-KF in the asset registry | producer → Codex lane | `asset_contract.py check` exits 0 | `.venv/bin/python scripts/asset_contract.py check` |
| 2 | Director review of G-IN/G-OUT and geometry, recorded by hash and use | Andre / director | `directorApproval=approved` with evidence | decision record (no inheritance from the A/B pilot) |
| 3 | Select the keyframe and bind `first_image` with a role binding | producer → Claude lane | no `INPUT_ROLE_UNDOCUMENTED` | `coherenceReferenceBindings` in the plan |
| 4 | Strict coherence check | producer → any lane | zero errors, zero unresolved WARN/INFO | `production_plan.py check-coherence --shot G-P03 --strict` |
| 5 | Exact request, live schema, price quote, specific ceiling | producer | `payloadSha256` set; quote recorded | `check-request`, then Kling schema/price query (read-only) |
| 6 | Release approval `kling_job_release` | Andre | explicit approval for this payload hash | only then may `kling_batch.py` run |
| 7 | Submit, collect, hash outputs into the registry | producer | output hashes mapped by `asset_contract.py` | per-scene cost row tagged `RESPAN_WORKFLOW_NAME=G-P03` |
| 8 | Independent review of the result (playback + frames) | QC lane (different model from author) | findings logged; no self-approval | handoff record |

## Stop conditions
- Any step 1–5 failure: fix the evidence, never weaken a validator or override an ERROR.
- Step 6 without Andre's explicit approval: stop. No inherited approval.
- Right-shoulder framing (violates D09) or a revealed full face in the eyes-only crop: reject.

## Known blockers today (from the plan)
1. Appearance/composition of G-IN/G-OUT still candidate (Andre / director).
2. No price quote or specific release for this payload (producer).
3. Strict check currently reports `INPUT_ROLE_UNDOCUMENTED` on this shot.

## Orchestration note
The requested consumer was `gcp-pipeline-orchestration`; the only copy found on this machine
(`~/.gemini/skills`, `~/.copilot/skills`) targets Google Cloud Composer/Airflow data pipelines,
and no `create-implementation-plan` skill is installed locally. This plan is therefore
runner-neutral: the JSON sibling carries steps, owners, gates and commands so any orchestrator
(Agent Parley lanes today) can consume it. Decide separately whether to adapt or replace the skill.

## Next hook
Resolve blocker 3 first (bind `first_image`; it is a producer decision), then run step 4 again.
