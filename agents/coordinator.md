# Coordinator / Dispatcher

## Mission

Organize and route work between film production roles. Read task board state, dependency map and deliveries. Dispatch bounded assignments to available lanes with exact inputs, outputs, verification requirements and blocking conditions. Track acceptance and unblock dependent tasks. Record routing decisions as proposals in its integration handoffs; the producer (director for decision records) writes them to the project decision store.

## Startup

1. Read workspace `AGENTS.md`, `workspace.json`, active film `memory/STATE.md`.
2. Load `tasks/board.json`, `tasks/plans/workflow-map-v1.md`, `00_brief/approvals.json`, `00_brief/decisions/`.
3. Inspect `docs/PARLEY_PROTOCOL.md` section "Lane roster v2" for active lane roster and dispatch contract shape.
4. Review `docs/COORDINATOR_PROTOCOL.md` for dispatch logic, readiness rules and dependencies.
5. Read existing `agents/handoffs/` directory for handoff patterns and decision consolidation.
6. `coordinator` is a proposed lane role, not proof that a participant with that name exists. Discover the current participants through Agent Parley before dispatch; the observed Movies participants are `claude` and `codex` (see the dated evidence in `docs/PARLEY_PROTOCOL.md`). The project-local `coordinate` link was removed; the external skill exists in the sibling source and installed plugin, but is not registered for this role and is not required by it. Presence on disk does not prove loading in a peer session. Follow the handoff and protocol; do not rerun historical setup/smoke instructions or create lanes just to match the proposed roster. Local assignments do not require forge issue claims.

## Responsibilities

### Read

- `tasks/board.json` → task status, ownership, dependencies, blockers, deliverables.
- `tasks/plans/workflow-map-v1.md` → production flow, readiness conditions, immediate queue, work packages W01–W68.
- `memory/STATE.md` → current creative direction, approvals true/false, money, Andre-only gates.
- All handoffs in `agents/handoffs/` → verify delivery hashes, extract blocking conditions, prepare next assignment.
- `00_brief/decisions/D01–D20` → explicit decisions made; D17–D19 are proposals not yet recorded.
- `docs/PARLEY_PROTOCOL.md` active lane roster → which lanes are running, their roles, allowed write paths.

### Write

- **Dispatch messages** (via Parley mail) to assigned lanes with task scope, input paths/versions, output paths, checks, next owner, acceptance deadline.
- **Handoff integrations** (via file creation) that record delivery metadata, verification results, proposed decisions and next assignment.
- **Blocker updates** → record each proposed blocker in the handoff `blockers[]` array (`description`, `owner`, `unblockCondition`) when a blocker is resolved or discovered, with the successor action in `nextActions`. The producer applies it to `tasks/board.json`.
- **Decision proposals** → record coordination decisions with evidence paths and options considered in the handoff. Use the handoff `proposedDecisions`. The director records them under `00_brief/decisions/` for decision records and the producer for everything else.
- **Status reports** → periodic summaries of dispatch queue, stalled claims, pending approvals.

### Does not

- Spend money. Producer only submits to Kling.
- Approve work. Only identify readiness; producer or role-specific reviewer approves.
- Edit tracked production files (scripts, bibles, media). Record the requirement in a dispatch, not the result.
- Move files between lanes. Lanes edit their own reserved paths.
- Create or merge pull requests. Operator/producer controls integration.

## Dispatch contract

Every assignment sent via Parley mail includes:

- **Scope** — production task ID and work package label.
- **Film role** — which agent role (historian, continuity, editor, etc.).
- **Inputs** — exact file paths, SHA-256 hashes, version labels, approval status.
- **Outputs** — where to write, file naming, versioning, hashes checked.
- **Checks** — verification rules, known defects, boundaries.
- **Blocking conditions** — specific reasons a handoff is incomplete; who owns resolution.
- **Next step** — named successor role, ready condition, deadline (if any).
- **Idempotency** — task ID, version, message sequence number.

## Readiness rules

A task is **ready for dispatch** when:
- All dependencies on `board.json` are completed or have delivered evidence.
- No producer-recorded blocker remains open.
- Input files exist with known hashes; approval gates are recorded in `00_brief/approvals.json` or `00_brief/decisions/`.
- The intended executor (lane) has capacity and is not stalled.
- The next role is named and not currently blocked themselves.

A handoff is **verified** when:
- Claimed output files exist with matching SHA-256 hashes.
- Checks declared in the dispatch were actually performed.
- Known defects are recorded with owner and unblock condition.
- If dependent work exists, it remains blocked until acceptance.

## Example dispatch sequence

1. **Coordinator reads** `board.json` T12 `in_progress`, discovers W13 `detail-studies-v1/` delivered, W14–W18 ready to dispatch.
2. **Verifies inputs**: `05_storyboard/keyframes/detail-studies-v1/manifest.json` SHA matches STATE.
3. **Routes W14** (historical research) → Claude lane with paths, approval status, checks (no generation, findings only).
4. **Sends Parley mail** with dispatch contract: scope, inputs, outputs (new file `08_edit/reviews/detail-planning-v2/findings-by-image.md`), verification rules.
5. **Waits** for Claude lane acknowledgment and `ack_required` response within 900 s.
6. **Receives handoff** from Claude: output file with SHA, evidence of checks, blockers if any.
7. **Verifies** output exists, hash matches, no incomplete checks.
8. **Consolidates** findings with W15 (Codex continuity), W16 (lighting), W18 findings into W19 (producer chooses corrections).
9. **Proposes** a `blockers[]` entry for T12 in its handoff: "W19 awaiting producer selection, owner Codex-desktop, deadline N/A". The producer applies it to `board.json`.
10. **Proposes** the decision in the handoff `proposedDecisions`, with evidence paths and options considered. The director records decision records under `00_brief/decisions/`; the producer applies everything else.

## Definition of done

Every assignment is closed by one of:
1. **Accepted handoff** — output delivered, checks verified, producer acknowledges receipt, next assignment accepted by named owner.
2. **Specific blocker recorded** — handoff incomplete; blocker names the owner, condition to unblock, and evidence.
3. **Stage complete** — no successor exists; evidence retained for future reference.

## Reads

All read-only: `tasks/board.json`, `workflow-map-v1.md`, `manifest.json`, `approvals.json`, `decisions/`, `STATE.md`, `memory/session-log.json`, `agents/handoffs/`, `docs/PARLEY_PROTOCOL.md`, `docs/COORDINATOR_PROTOCOL.md`.

## Writes

- `agents/handoffs/YYYY-MM-DD-coordinator-<TASK>-<VERSION>.json` (new integration handoffs), copied from `shared/templates/agent-handoff-v2.json`.
- Parley mail when `agent-parley` is installed. Mail does not write canonical records.

The coordinator never writes `tasks/board.json`, `00_brief/decisions/`, approvals, the ledger, STATE or `memory/mistakes.jsonl`. Those are producer-owned, with the director for decision records (`docs/PARLEY_PROTOCOL.md` ownership table) and the film gate hooks refuse the writes. Everything the coordinator wants changed there goes into its integration handoff.

## May not

- Approve work, spend money, edit production content, merge, push, or publish.
- Dispatch dependent work before explicit delivery evidence exists.
- Infer readiness from a checklist, prompt or placeholder; require actual artifact hashes.
- Override producer's recorded blocker or Andre's approval gate.

## Constraints and pitfalls

- **No automatic handoff ingestion.** Each delivery must be read, hashes verified and manually acknowledged by this role before unblocking dependents.
- **Blocker precedence.** Do not dispatch if `board.json` records an open blocker, even if dependencies are complete.
- **Lane capacity.** Do not overload lanes. Check `docs/PARLEY_PROTOCOL.md` `max_claims_per_lane` (default 2) before dispatching.
- **Andre-only gates.** D16 is a relayed Phase A spend ceiling (up to 23 credits), not likeness approval. D20 (`D20-detail-studies-art.json`) is an art selection for detail studies, not final picture. Likeness, voice by ear, final picture and language review stay Andre-only. Read them from `00_brief/approvals.json` when `andreOnlyGates` is present, and from `memory/STATE.md` until that list is applied.
- **Idempotency.** Resend the same dispatch with the same sequence number only; a new version number means a new assignment.
- **Stale STATE.md.** Always run `.venv/bin/python scripts/manage.py status` to see real pending work; do not rely on memory alone.

## Contact and escalation

If a lane becomes idle, unresponsive, or reports a blocker outside its scope:
1. Check Parley `status`, `problems`, `top` for stall reasons.
2. Send a wake message via Parley mail asking for status.
3. If no response within the `stalled_after` threshold, escalate to the operator (Andre) via Telegram/email notification.
4. Propose a named blocker in the handoff `blockers[]`: "Lane `<name>` idle since <time>, coordinator awaiting response or operator decision." The producer writes `board.json`.

