# Agent Parley protocol for Movies_Projects — local work assignment active

Status: Andre directly authorized this conversation to decide assignments and notify both lanes on 2026-10-09. The local work division below is active. Broader memory phases and integration mechanisms remain proposals unless separately assigned. AGENTS.md and docs/LOCAL_AGENT_HANDOFF.md remain applicable.

## What Parley gives and what it does not
- Gives: lanes (`claude`, `codex`), mail between lanes, a decision log, advisory file reservations, status/reports. Service: `agent-parley up`; check: `agent-parley doctor`.
- Does not apply here: forge issues, claims on issue numbers and PRs (no Git remote). Use mail, reservations and reports only.
- Each lane works in its own Git worktree and branch (`parley/<project>/lane-N`). Ignored files (`.venv`, credentials, caches) are not in a lane worktree. Work reaches `main` only through an explicit merge that Andre has asked for.

## Lane roles
Lanes are tools, not film roles. The film role (producer, director, historian, ...) for a task is named in the first message of the thread and in the handoff `agentRole`. Role limits in `agents/*.md` and AGENTS.md apply unchanged: only the producer role submits approved paid Kling jobs, and only from the base checkout after a live balance refresh and a written scope. Reviewer roles never spend.

## Ownership (reserve before editing; release when the handoff is written)
| Resource | Owner role | Others |
|---|---|---|
| `manifest.json`, `tasks/board.json`, `00_brief/approvals.json`, `credit-ledger.csv`, `asset-registry.csv`, `00_brief/decisions/` | producer (director for decision records) | propose through a handoff; never edit |
| `01_script/`, `03_bibles/`, `05_storyboard/source/`, `08_edit/` new revisions | the role named in the task | new versioned files only |
| `memory/STATE.md`, `memory/session-log.json` | desktop/base producer integrates after reading fresh | lanes return handoffs; record base hash |
| Named resource `kling:submit` | producer only | one paid submission at a time |

## Close-out message (replaces re-reading the whole thread)
One mail per finished task, with an idempotency key: handoff path, claims with evidence paths, `andreOnlyGates`, next action and role. Decisions Andre made go in the log with `decision: true`; proposals never do.

## Proposed integration gate (Andre runs it; a lane cannot)
```bash
agent-parley verify set ".venv/bin/python scripts/manage.py validate && .venv/bin/python -m unittest discover -s tests"
```
Known baseline: validate reports ok with four shared-skill hash warnings; 29 tests pass. A passing gate is not creative acceptance. Do not run `participant merge` or `participant pr` until Andre asks.

## Smoke test (read-only, no spending, no file edits)
Prerequisites: `agent-parley up`; Claude and Codex each launched with `agent-parley run NAME --repo /mnt/data/Projects_SSD/Movies_Projects`; lane approvals resumed.
Message to `codex`: read AGENTS.md and `projects/andre-time-travel/memory/STATE.md`, then reply in one thread with (1) the current creative direction in one sentence, (2) the Andre-only open items, (3) whether D17–D19 are recorded decisions or proposals, (4) the owner of `credit-ledger.csv`.
Pass: (1) back-view over-the-shoulder with eyes only as short reaction; (2) includes D16 direct confirmation and the Phase A request mismatch; (3) proposals, not recorded; (4) producer. Any miss means STATE.md or AGENTS.md is unclear, so fix the file, not the answer.

## Active assignment — Andre direct authorization, 2026-10-09
- Producer/coordinator: Codex in the main desktop conversation, operating from the base checkout. This is NOT the Parley codex lane. Owns canonical manifest, board, approvals, ledger, asset registry, decision records, STATE and session-log integration. Lanes return handoffs instead of editing those shared records.
- Claude lane: continuity / research preparation. Finish and report the existing bible reconciliation without repeating completed work. Then prepare one new detail-planning document covering all five figures: feet/footwear/floor, rear hair/costume, left/right shoulder alternatives, fingers/hands/table. Read tasks/scene-detail-assets-v1.md and the shared dramatic-direction document. Map reusable assets, missing references, source-backed period details and uncertainties. Own only new files under 03_bibles/detail-planning/ plus its own handoff. No new media generation.
- Codex lane: editing / QC. First deliver the actual status and artifact paths for Galileo timeline/preview v2, including any incomplete verification. Finish remaining local rendering/QC if needed without duplicating completed work. Then independently review the Claude detail-planning handoff read-only and record findings in new files under 08_edit/reviews/detail-planning-v1/ plus its own handoff. Do not modify Claude's documents.
- Both may immediately read, research and write the assigned new local documents; producer-owned canonical state does not block this work. No forge issue is required in this local-only repository. Reserve assigned output paths through Parley where available; preserve current uncommitted work.
- D16/request-r2 remain an unapproved paid-test route, not a dependency of this zero-credit preparation. Assess whether new IN/OUT candidates supersede its purpose before proposing spending. Rear hair/shoulder studies were requested directly by Andre; no full historical face is permitted. Fixed table dimensions and general eye timing remain unresolved; the 2-second choice concerns the specific Galileo edit.
- No spending, paid audio/video/images, final acceptance, commits, merges, pushes or broad Phase 1–4 memory implementation in these assignments. Commit permission is unnecessary for delivering local files and hashes. Report a concrete blocker only for the operation it actually blocks; continue independent assigned work.
- Read this base-checkout protocol as the current assignment if the worktree copy is absent/stale. Do not write in another participant's checkout. Confirm receipt and scope by Parley, then return exact paths/hashes, checks run, remaining work and Andre-only decisions. Acknowledgement is not artistic approval.

## Image ownership and dependencies — Andre clarification, 2026-10-09
The Codex producer in the main desktop conversation creates the new scene-detail images. Claude prepares research/specifications and the Codex lane reviews/edits only as explicitly assigned. Neither lane generates substitutes, initiates an image batch, or delegates new work independently under this assignment.
Work requiring the new pictures waits for an explicit producer delivery with paths, versions/hashes and review status. A checklist, prompt, placeholder or previous IN/OUT set is not delivery of the new detail images. Candidate delivery is not final approval. Research, existing bible handoff, and already-assigned Galileo editing with existing footage may continue independently; do not replace its media with assumed new assets.
The producer chooses further delegation and sends scoped assignments. Lanes report blocked dependencies and continue only independent assigned work; do not claim dependent shots complete before the images exist.

## Refinamento das entregas
A divisão efetiva está em `projects/andre-time-travel/tasks/scene-detail-assets-v1.md`, seção Delegação efetiva: Claude pesquisa cultura material; Codex lane prepara cobertura e foley depois do Galileo, além da revisão; Codex desktop gera imagens. Esta divisão refina as atribuições anteriores e evita duplicação.

## Mapa de tarefas e passagem ao sucessor — 2026-10-10
Consultar [workflow do filme](../projects/andre-time-travel/tasks/workflow-map-v1.md), com responsabilidades, dependências e fila imediata. A regra de fechamento está em [REPEATABLE_WORKFLOW.md](REPEATABLE_WORKFLOW.md#fechamento-e-sucessor-obrigatório). Esse mapa não envia mensagens, inicia lanes nem transforma pacotes planejados em atribuições aceitas. O produtor continua responsável pelo próximo trabalho pronto até confirmar o aceite. Usar mensagens/handoffs locais; não exigir forge issues neste repositório sem remote.

## Lane roster v2, dispatch contract and film gate hooks — proposed 2026-10-10

Status: implemented on branch `claude/wizardly-clarke-23j2kj` as a proposal ([plan](PLAN-parley-integration-v1.md)). It becomes the active protocol only when Andre merges it and runs Phase 0 (`scripts/parley_setup.sh`, [smoke test and hook proof](parley-smoke-test.md)). Earlier sections stay valid until then.

### Roster (lanes are tools; the film role is named per assignment)

| Lane | Provider | Roles it may hold | Allowed write paths (reserve first) | Never |
|---|---|---|---|---|
| `claude-research` | claude | historian, continuity preparation, dialogue text work | `03_bibles/detail-planning/`, `03_bibles/scene-bibles/*-vNEXT.md`, `01_script/translations/` proposals, `00_brief/research/`, own handoff | media, canonical records, logging a proposal as a decision |
| `codex-edit-qc` | codex | editor, QC, coverage review, tooling | `08_edit/reviews/`, `08_edit/timelines/*-vNEXT.json`, `08_edit/normalized/`, `09_delivery/qc/`, `scripts/` and `tests/` when assigned tooling, own handoff | re-render by default, another lane's documents, accepting takes |
| `claude-review` | claude (second account if needed) | independent continuity, lighting, facial safety | `02_references/_review/`, `08_edit/reviews/<topic>-independent/`, own handoff | substitutes, paths reserved by `codex-edit-qc` |
| producer (not a lane) | Codex desktop, base checkout | producer, director, image creator | canonical records, `07_generations/`, `05_storyboard/keyframes/` | dependent work before evidence; spending on a relayed approval |

Andre is the `operator` (CLI only): `say`, `participant merge`, `verify set`. `participant merge` and `participant pr` stay unused until he asks.

### Identity for the film gate hooks

Export in each lane shell before `agent-parley run`: `MOVIES_LANE_NAME=<lane>` and `MOVIES_LANE_ROLE=<film role>`. Only the producer's base-checkout shell exports `MOVIES_PRODUCER_LANE=1`. Without it a session is treated as a lane: canonical records and paid submission are refused (`.claude/hooks/`, tests in `tests/test_hooks.py`). Paid submission goes only through `scripts/kling_batch.py` with a `scope.json` beside the spec; direct CLI generation verbs are refused. Review roles record a `zero-face-log.json` under `09_delivery/qc/<set>/` or `08_edit/reviews/<topic>/` listing each inspected file by path and hash. The hooks log to `projects/<episode>/logs/hooks.jsonl` and draft mistakes to `logs/mistakes-draft.jsonl` (both untracked; a lane copies its drafts into the handoff `mistakes[]`); they never approve, spend, commit, merge or wake the desktop conversation. Parley's own `reserved_path` denial, not the film hooks, enforces lane reservations.

### Dispatch contract (one `send_message` per assignment, 150–250 words)

`ack_required`, `ack_within` 900 s, idempotency key `<task>-<version>-<n>`. Body: goal; film role; parent board task and W package; input paths with SHA-256; allowed output paths; definition of done with the evidence files required; constraints (no media, no spending, no canonical edits); next owner on completion. A deadline that passes unacknowledged returns the task to the producer with the recipients' reasons; the producer records a blocker with owner or re-offers to a fit lane. A delivery is accepted only when `manage.py handoff check` passes on the lane's handoff and the checks it names were run; the producer then runs `handoff ingest`.

### Reservations and supervision

Producer: canonical set with no TTL plus the named resource `kling:submit`, once per session. Lanes: output folders per assignment, TTL 3600 s, released at handoff. Supervision `stalled_after` and `claim_idle_after` are lengthened to one working day so human gates never trigger wake, offer and release.
