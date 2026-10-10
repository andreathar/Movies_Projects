# Project simplification and lifecycle audit — execution plan v1

10 October 2026 · Owner: Codex desktop producer · Requested by Andre.

## Outcome and present scope

Create a coherent project in which agents find one current rule per subject, know the next owner, and do not repeatedly read obsolete proposals. Audit the whole workspace before deciding what can be retired. Preserve the film and evidence already produced. A file missing from the workflow map is not automatically unused.

This deliverable is the **plan**, informed by a preliminary read-only inventory. It does not implement the cleanup, uninstall plugins, move/delete media, configure hooks, launch agents, commit, merge, or spend credits. Existing authorized film tasks remain separate. A dependable workflow is testable; perfection is not a guarantee.

Preliminary snapshot: about 4.0 GB in the working directory including local internals/runtime; filtered metadata walk found 207 Markdown, 468 JSON, 18 Python, 30 CSV, 91 MP4, 414 PNG and 452 JPG files. Counts exclude Git internals, virtual environments, node_modules and Python caches, and do not traverse directory symlinks. Counts are not a content audit or evidence that any file is redundant. Avoid reading credentials, private runtime databases or token-bearing logs into agent context.

## Inputs to reuse before doing new work

- Workspace `AGENTS.md`, `CLAUDE.md`, `workspace.json`, `docs/REPEATABLE_WORKFLOW.md`, `docs/PARLEY_PROTOCOL.md`, `docs/TOKEN_EFFICIENCY.md` and `docs/LOCAL_AGENT_HANDOFF.md`.
- Existing `docs/CLEANUP-INVENTORY-2026-10-09.md`: useful leads, some state observations now stale.
- Claude lane delivery `docs/consolidation-2026-10-09/consolidation-report.md` and associated handoff/diffs, read from the registered Claude worktree. Locate and hash current files; do not assume lane HEAD equals the main checkout or rerun completed consolidation.
- Film `memory/STATE.md`, board/manifest/approvals/decision records, `tasks/workflow-map-v1.md`, `tasks/production-tasks.md`, latest research/image handoffs and catalog.
- Series framework and continuation template; existing scripts/tests, skill registry, symlinks and plugin bindings.

## Phase 1 — establish the baseline

**Owner:** producer. **Input:** existing workspace and registered worktrees. **Output:** a dated audit folder under `reports/`, with inventory and base hashes.

1. Record Git branch/worktrees, tracked/untracked changes and assigned paths. Preserve other actors' edits; no clean/reset/staging operation implied.
2. Inventory all project paths including hidden project configuration, symlinks, sizes and categories. Classify runtime/cache directories by metadata rather than exposing contents. Do not follow links outside the workspace as though their targets were local duplicates.
3. Separate base checkout, lane deliveries, external shared skill targets and provider-installed plugins. Record external dependencies without attempting global cleanup.
4. Capture baseline validation and known warnings. Media hashes already verified can be reused where the bytes/version have not changed; hash ambiguous duplicate candidates as necessary.
5. Record recoverable originals for any later changed/moved document, including untracked files. Git alone does not protect untracked content, and no commit is assumed authorized.

**Pass:** inventory coverage and exclusions are explicit; concurrent edits and external scope boundaries are known.
**Next:** producer assigns one bounded documentation audit, reusing Claude's report.

## Phase 2 — trace authority, dependencies and obsolescence

**Owner:** producer; intended bounded support: Claude for documentation comparison, terminal Codex for read-only dependency review. Verify availability and accepted scope before dispatch.

1. Build a reference graph across Markdown links, JSON/CSV path fields, script/config references, templates, skill links, manifests, catalogs and handoff hashes.
2. For every document, identify subject, authority, owner, consumer, current/superseded status, and whether the information exists elsewhere. Compare semantic rules, not only identical paragraphs.
3. Reconcile Claude's delivered consolidation against newer base changes. Do not copy an old proposed version over the recent image delivery or primary instructions.
4. Identify contradictory instructions and stale task reports separately from historical snapshots. Known leads: eye-duration variants; final voice versus guide-route completion; legacy bibles versus D20; old paid-test blockers; duplicated status; skill origins/hashes.
5. For scripts and tests, identify actual entry points, imports/callers and intended use. Lack of a recent invocation alone does not prove a script is dead.
6. Mark each item **active canonical**, **active supporting**, **superseded historical**, **reproducible generated**, **runtime/cache**, **external dependency**, or **uncertain**. Every retirement candidate gets evidence and a replacement or retention rationale.

**Pass:** no candidate is classified as removable merely for being old, absent from the map, or located under Hermes.
**Next:** producer resolves conflicts and creates an explicit change/move manifest.

## Phase 3 — design the smallest instruction set

**Owner:** producer; Claude may propose bounded document edits.

Target reading layers:

1. **Primary contract:** AGENTS.md contains concise invariants, authority, mandatory entry links and lifecycle rules. CLAUDE.md imports it rather than duplicating it. Other platform bridges only if actually used, preserving their native mechanisms.
2. **Current state:** workspace locator → film STATE → relevant board/approvals/handoff evidence. A snapshot does not compete with the canonical board.
3. **On-demand detail:** relevant workflow-map section, task brief, technical/provider manual and review evidence. Keep the 68-package inventory discoverable without requiring its entire contents for every tiny task.

Assign one canonical source per subject. Replace duplicated active instructions with short links; retain historical decisions and source evidence. Reconcile primary instructions whenever a governing rule or its required link changes. Progress-only updates belong in board/STATE/handoffs, not a new rule in AGENTS.md.

Measure baseline versus proposed required-read text volume and repeated paragraphs. Seek fewer unnecessary reads without removing identity, facial-safety, payment, timing or approval gates. File count/bytes are not a measurement of actual model tokens, and cleanup does not shrink already accumulated conversation history.

**Pass:** a new producer or lane can identify authority, scope, inputs, expected output and next step from the required entry path without reading the archive.
**Next:** integrate one documented change set at a time.

## Phase 4 — apply reversible local cleanup

**Owner:** producer integrates; workers only edit assigned proposed revisions.

- Start with links and contradictory active text, then simplify navigation. Consolidate before moving paths.
- Prefer logical retirement when moving would break catalogs, provenance hashes or delivered handoffs. If moving a document is justified, use an existing appropriate archive location, record old/new paths and update active references in the same change set.
- Never rewrite historical records to pretend the old state did not exist. Never silently update old handoff hashes to hide a changed source; create a new integration record with before/after hashes.
- Preserve real photos, generated originals, accepted/rejected takes, source snapshots, receipts/ledger, decisions, approvals and delivered reference atlases. Exact media duplicate detection does not grant deletion authority.
- Reproducible outputs may be candidates only after proving inputs and rebuild path, and preserving the last delivered version. Runtime/cache cleanup is separate from instruction simplification.
- Produce a deletion proposal only for demonstrably disposable items with scope and recovery. Permanent deletion, global uninstall, Git integration or publication is not part of this planning request.

**Pass:** no broken active path or lost provenance; every applied change has a rollback path and the main producer record is current.
**Next:** skill/plugin reconciliation and lifecycle design.

## Phase 5 — skills and plugins without damaging shared tools

**Owner:** producer.

1. Map actual project tasks to skills/plugins and identify which are local, linked, installed globally or referenced only by history.
2. Keep working continuity, localization, editing QC and research skills even if their source directory has a legacy application name.
3. Reconcile the four known registry warnings by reviewing the actual source/version changes; do not merely replace hashes to make warnings disappear.
4. Remove obsolete active references or redundant project-local bindings only after checking consumers. Retain shared installations used elsewhere; do not equate “not needed by this film” with “safe to uninstall globally.”
5. List uncertain tools separately with a concrete dependency question. No new plugin installations to compensate for unclear ownership.

**Pass:** one clear supported route per function, truthful registry/source records and no broken skill links.
**Next:** evaluate whether the existing coordinator supports the lifecycle needed.

## Phase 6 — project-wide task lifecycle and hooks design

**Owner:** producer. **Status:** design only; implementation is a separate bounded work package after the scan identifies existing runtime capabilities.

Andre wants tasks connected from start to finish. Prefer one shared task lifecycle plus task data over a custom hook for every individual task. All known tasks should declare owner, dependencies, input revision, outputs, evidence, authority, next task/owner and stop conditions. Some tasks end a stage and legitimately have no successor.

Conceptual lifecycle: ready → dispatched → accepted → started → delivered → verified → successor accepted, blocked with owner, or stage complete. Failure, cancellation and stale-input states must be explicit. Workflow events are not proof that an external generation succeeded.

Hooks/adapters may publish start, delivery, failure and blocker events. A coordinator reconciles current evidence and dispatches only already-authorized work. Inspect existing Parley behavior before adding infrastructure. This local-only project does not need hosted forge issues to model dependencies. A service/adapter must exist and be tested before claiming events can wake this desktop chat; file edits do not do that automatically.

Required safeguards and tests before enabling any dispatcher:

- Duplicate completion event: one successor assignment, no duplicate paid request.
- Missing output, changed hash or failed review: no dependent start; defect returned to its owner.
- Recipient unavailable, approval dialog open or acknowledgement missing: producer retains ownership and a concrete blocker is recorded.
- Process restart: resume from persisted state without lost handoff or duplicate work.
- Input revision changes: invalidate only affected review evidence and tasks.
- No next task: legitimate stage completion, not perpetual self-generated work.
- Paid generation, purchases, commits/merges and artistic acceptance remain separate authority checks. No hook grants trust or bypasses a dialog.
- Run in dry-run mode first, using local dummy artifacts; no media generation, external writes or credits for testing.

**Pass:** behavior proven by replayable tests and an operator-visible audit trail. Until then, the documented producer handoff process remains the actual mechanism.
**Next:** rollout only within explicitly authorized implementation/activation scope, with rollback to manual dispatch.

## Phase 7 — validate the simplified project

**Owner:** producer; independent reviewer for the integrated change set where useful.

- Required project validation and unit tests, grouped once per coherent management/code change; investigate new errors without masking known baseline warnings.
- Check all active relative links, referenced artifacts, skill symlinks, schema contracts and newly recorded hashes. Preserve stale historical hash records as historical rather than treating them as live assertions.
- Check that archive content is not in mandatory startup reads and that the primary contract points to current procedures.
- Walk through a small fictional task: entry instructions → inputs → accepted assignment → output → verification → next owner/blocker. Exercise both success and failure routes.
- Verify media preservation and that no final acceptance/budget status changed accidentally.
- Compare required reading and duplicate instructions before/after, with exclusions and honest limits. Do not claim a percentage of token savings without token measurement.

**Pass:** checks and an independent cold-start walkthrough demonstrate the intended path; documentation alone is not claimed to enforce behavior.
**Next:** final cleanup report and a bounded return to film production.

## Phase 8 — close out and return to the film

Deliver an inventory, authority/dependency map, concise change manifest, archive/retirement list, unresolved questions and validation evidence. Update STATE and primary links once. Do not add another competing global resume document.

The film successor is **independent continuity review of the delivered image set**, followed by only necessary corrections and selected-shot preparation. Preserve the separate Galileo playback/bible reconciliation task. Do not regenerate images or repeat historical research merely because folder organization changed.

## Concrete outputs of the future audit

One dated folder under `reports/` should contain: inventory, authority/dependency map, before/after change manifest with rollback, validation results, and a concise final report. Reuse the current cleanup inventory and Claude consolidation report as inputs. The workflow map should link these outputs; no parallel task-status database is created by this plan.

## Decision boundary

The request here authorizes preparing this plan and the preliminary read-only inspection. It does not by itself execute the cleanup or install the proposed lifecycle system. During implementation, routine reversible edits within an authorized scope should not require repeated permission; destructive/global actions and new automation scope must remain explicit.
