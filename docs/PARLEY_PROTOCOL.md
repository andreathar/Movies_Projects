# Agent Parley protocol for Movies_Projects — episode assignments and lane mechanics

Revision r2 (consolidation draft, 2026-10-09, lane claude; replaces nothing until the producer integrates it). Base revision hash and a before/after summary are in `docs/consolidation-2026-10-09/consolidation-report.md`.

This file holds **only** what is specific to Parley lanes and to the current episode's assignments. Rules are not repeated here; follow their canonical homes:

| Topic | Canonical source |
|---|---|
| Non-negotiable boundaries (faces, references, dialogue, spending, Kling, credentials, memory scope, paths) | [AGENTS.md](../AGENTS.md) |
| Authorship map, handoff format, approvals by version | [LOCAL_AGENT_HANDOFF.md](LOCAL_AGENT_HANDOFF.md) |
| Commits, merges, integration, backups | [VERSION_CONTROL.md](VERSION_CONTROL.md) |
| Reusable process, task contract, dependencies, communication evidence | [REPEATABLE_WORKFLOW.md](REPEATABLE_WORKFLOW.md) |
| Context and message economy | [TOKEN_EFFICIENCY.md](TOKEN_EFFICIENCY.md) |
| Film role briefs and limits | [agents/README.md](../agents/README.md), `agents/registry.json` |

**Status legend.** `[ACTIVE]` = authorized by Andre on 2026-10-09 through the producer conversation. `[PROPOSED]` = not authorized, not configured, no lane may act on it. `[MECHANICS]` = a fact about how Parley works, not an authorization.

## Responsibilities in this episode (andre-time-travel) `[ACTIVE]`
This table is the **only** place that binds a tool/platform to a role. A platform name is not a permanent role; a later episode replaces these rows and nothing else in the workflow docs.

| Person / session | Responsibility in this episode |
|---|---|
| Andre | Author and approver. Only Andre approves likeness, creative acceptance, voice, final picture and language review, and confirms spending gates. |
| Codex, main desktop conversation (base checkout) | Producer / coordinator and creator of the new images. Owns canonical manifest, board, approvals, ledger, asset registry, decision records, `STATE.md` and session-log integration, and the one-delivery-at-a-time integration. **This is not the Parley `codex` lane.** |
| Claude lane (`claude`, own worktree) | Research, continuity and documentation. Delivers new documents and handoffs; edits no canonical record. |
| Codex lane (`codex`, own worktree) | Editor / QC. Edits existing authorized footage into new revisions; reviews other lanes' deliveries read-only. |

The film role (producer, director, historian, …) for a task is named in the first message of the thread and in the handoff `agentRole`. Role limits in `agents/*.md` and AGENTS.md apply unchanged.

## What Parley gives and what it does not `[MECHANICS]`
- Gives: lanes, mail between lanes, a decision log, advisory file reservations, status and reports. Service: `agent-parley up`; check: `agent-parley doctor`.
- Does not apply here: forge issues, claims on issue numbers and PRs (no Git remote). Use mail, reservations and reports only.
- Each lane works in its own Git worktree and branch (`parley/<project>/lane-N`). Ignored files (`.venv`, credentials, caches) are not in a lane worktree. A file saved in the base checkout is not visible in a lane until it is read by explicit path or integrated; a commit in the base does not update lane branches. Work reaches `main` only as described in [VERSION_CONTROL.md](VERSION_CONTROL.md).
- Reservations are advisory, not locks. Mail and a handoff on disk do not prove the recipient read them (see "Evidência de comunicação" in REPEATABLE_WORKFLOW.md).

## Ownership of resources `[ACTIVE]`
Reserve before editing; release when the handoff is written.

| Resource | Owner | Others |
|---|---|---|
| `manifest.json`, `tasks/board.json`, `00_brief/approvals.json`, `credit-ledger.csv`, `asset-registry.csv`, `00_brief/decisions/` | Producer (the director role for decision records) | Propose through a handoff; never edit |
| `memory/STATE.md`, `memory/session-log.json` | Producer integrates | Lanes report in their handoff and mail, with the base hash they read |
| `01_script/`, `03_bibles/`, `05_storyboard/source/`, `08_edit/` | The role named in the task | New versioned files only; never overwrite delivered revisions |
| Named resource `kling:submit` | Producer only | One paid submission at a time (see AGENTS.md) |

*Change in this revision:* the previous table let "whoever closes a task" edit `STATE.md` and `session-log.json`. That contradicted the later active assignment that gives their integration to the producer, so the producer-integrates rule is kept. Flagged in the consolidation report as a point for Andre to confirm.

## Active assignment — Andre's direct authorization, 2026-10-09 `[ACTIVE]`
- Both lanes may read, research and write their assigned **new** local documents at once. Producer-owned canonical state does not block this. Reserve output paths through Parley; preserve uncommitted work.
- **Claude lane — research, continuity, documentation.**
  1. Finish and report the existing bible reconciliation; do not repeat completed work.
  2. Material-culture sheets for the five figures in `03_bibles/detail-planning/historical-details-v1.md` (Galileo first): footwear/feet/floor, rear hair, collar/sleeves/hands, plausible light sources, local references, verified sources and degree of certainty. Observed or documented material is kept apart from proposals; footwear is never guessed. No technical camera or foley plan.
  3. Documentation audit and consolidation (producer message 21, relayed from Andre's request): updated workflow documents, canonical-source map and a before/after report. Editable scope: `START_HERE.md`, the five workflow/protocol/handoff/versioning docs (not AGENTS.md), `agents/README.md` and the new report; proposals for AGENTS.md and the registry go in the report only.
  4. Own only new files under `03_bibles/detail-planning/`, the consolidation report, the working copies named above, and its own handoffs.
- **Codex lane — editing and QC.** Galileo timeline/preview v2 is delivered (status and artifact paths in its handoff). It then prepares coverage and foley planning under `08_edit/reviews/detail-planning-v1/`, and reviews the Claude lane's detail-planning handoff read-only, without modifying Claude's documents.
- **D16 / request-r2** remain an unapproved paid-test route and are not a dependency of this zero-credit preparation. Fixed table dimensions and general eye timing remain unresolved; the 2-second choice applies to the specific Galileo edit only. D17–D19 are proposals, not recorded decisions.
- No spending, paid generation, final acceptance, commits, merges, pushes or broad memory phases under these assignments. Commit permission is not needed to deliver local files and hashes. A blocker is reported only for the operation it blocks; independent assigned work continues.
- Read this base-checkout file as the current assignment if the worktree copy is absent or stale. Do not write in another participant's checkout. Confirm receipt and scope by Parley, then return exact paths and hashes, checks run, remaining work and Andre-only decisions. Acknowledgement is not artistic approval.

## Image ownership and dependencies `[ACTIVE]`
The Codex producer in the main desktop conversation creates the new scene-detail images (Andre's clarification, 2026-10-09). No lane generates substitutes, starts an image batch or delegates new work on its own. Work that needs the new pictures waits for an explicit producer delivery with paths, versions/hashes and review status; the general dependency rule is in REPEATABLE_WORKFLOW.md ("Contrato de tarefa e dependências"). Candidate delivery is not final approval. The producer chooses further delegation and sends scoped assignments.

## Delivery division `[ACTIVE]`
The effective split of the detail work is in `projects/andre-time-travel/tasks/scene-detail-assets-v1.md`, section "Delegação efetiva". It refines, and does not duplicate, the assignments above.

## Close-out message `[PROPOSED practice, already followed informally]`
One mail per finished task with an idempotency key: handoff path, claims with evidence paths, `andreOnlyGates`, next action and role. Decisions Andre made go in the decision log with `decision: true`; proposals never do. Not adopted as a rule until Andre or the producer says so.

## Integration gate `[PROPOSED — Andre runs it; a lane cannot]`
```bash
agent-parley verify set ".venv/bin/python scripts/manage.py validate && .venv/bin/python -m unittest discover -s tests"
```
Known baseline (reported earlier, to be re-run before use): validate reports ok with four shared-skill hash warnings; 29 tests pass. A passing gate is not creative acceptance. Do not run `participant merge` or `participant pr` until Andre asks.

## Smoke test `[PROPOSED — not recorded as run or passed]`
Read-only, no spending, no file edits. Prerequisites: `agent-parley up`; Claude and Codex each launched with `agent-parley run NAME --repo /mnt/data/Projects_SSD/Movies_Projects`; lane approvals resumed.
Message to `codex`: read AGENTS.md and `projects/andre-time-travel/memory/STATE.md`, then reply in one thread with (1) the current creative direction in one sentence, (2) the Andre-only open items, (3) whether D17–D19 are recorded decisions or proposals, (4) the owner of `credit-ledger.csv`.
Pass: (1) back-view over-the-shoulder with eyes only as a short reaction; (2) includes D16 direct confirmation and the Phase A request mismatch; (3) proposals, not recorded; (4) producer. Any miss means `STATE.md` or AGENTS.md is unclear, so fix the file, not the answer.
