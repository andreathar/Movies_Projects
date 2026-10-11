# Coordinator protocol for Movies_Projects

## Purpose

This protocol defines how the coordinator role interacts with Agent Parley lanes in `Movies_Projects`. It turns the film's existing production map into deterministic, bounded coordination: read current state, claim work, send a structured assignment, verify outputs, and only then release dependent work.

This file is intentionally local to the project and complements the operational rules in `AGENTS.md`, `docs/LOCAL_AGENT_HANDOFF.md`, `docs/PARLEY_PROTOCOL.md`, and the production task board.

## 1. Active operating model

The coordinator is a human/agent dispatch role, not a policy override. It does not replace the producer role or Andre's approval gates.

- Producer owns canonical task records, paid submissions, and final approval authority.
- Lane roles own only the bounded outputs defined in their assigned work package.
- Coordinator owns coordination state: queue ordering, task routing, evidence verification, blocker declarations, and assignment handoffs.

## 2. Coordination loop

The coordinator follows this loop for every next step:

1. Read the current board and workflow map.
2. Find ready tasks with all dependencies satisfied and no open blocker.
3. Check the assigned lane has capacity and a valid allowed output path.
4. Read the exact input artifacts and their versions/hashes.
5. Create one assignment message with clear scope and acceptance criteria.
6. Send the task to the named lane via Parley mail.
7. Track acknowledgment.
8. Await the handoff and verify the output artifact.
9. Record the actual result in the coordinator's integration handoff, with any proposed decision in `proposedDecisions` and any proposed blocker in `blockers[]`.
10. Release the next dependent task or keep the blocker explicit.

No task moves forward on optimism alone. Movement requires evidence.

## 3. Ready task rules

A task is ready only when all of these are true:

- `board.json` lists it as `in_progress`, `blocked`, or `ready` and the natural dependency chain allows it.
- Every required upstream task has a recorded delivery or an explicit accepted condition.
- Required inputs exist at the path declared in the task spec.
- Any required decision record or approval file exists and is not older than the current task version.
- The lane responsible for the task has a valid role, clear allowed write path, and no live blocker from a previous assignment.

The coordinator must not infer readiness from a prior draft or from an unverified generator result.

## 4. Assignment message format

Each Parley assignment must contain the following fields.

### Required fields

- `taskId`: board task ID, such as `T12`.
- `workPackage`: work package label, such as `W14` or `W15`.
- `role`: the film role performing the work (e.g., `historian`, `continuity`, `editor`, `dialogue-sound`, `producer`, `qc`).
- `owner`: the target lane or participant name.
- `scope`: what exact output is expected.
- `inputs`: array of file paths with version or hash data.
- `allowedPaths`: files the lane may edit or create.
- `checks`: the minimum accepted verification steps.
- `blockers`: known blockers or constraints; if none, state `none`.
- `nextOwner`: who should receive the handoff after this task.
- `idempotencyKey`: unique task-version-key pair for deduplication.
- `deadline`: if set, the time limit for acknowledgement or completion.

### Example

```json
{
  "schemaVersion": "1.0",
  "taskId": "T12",
  "workPackage": "W15",
  "role": "continuity",
  "owner": "codex-edit-qc",
  "scope": "Review likeness evidence, proportions, expression and grooming for the selected detail-study set.",
  "inputs": [
    {
      "path": "projects/andre-time-travel/05_storyboard/keyframes/detail-studies-v1/manifest.json",
      "sha256": "<sha256>",
      "version": "detail-studies-v1"
    },
    {
      "path": "projects/andre-time-travel/memory/STATE.md",
      "sha256": "<sha256>",
      "version": "current"
    }
  ],
  "allowedPaths": [
    "projects/andre-time-travel/02_references/_review/",
    "projects/andre-time-travel/08_edit/reviews/"
  ],
  "checks": [
    "Compare exact candidate images against the current continuity matrix",
    "Record only evidence-backed observations",
    "Do not regenerate or replace originals",
    "Deliver a concise findings file with path and version references"
  ],
  "blockers": [
    "No Andre likeness approval is implied by starting this review."
  ],
  "nextOwner": "producer",
  "idempotencyKey": "T12-W15-v1",
  "deadline": "900s"
}
```

## 5. Handoff verification standard

A completed handoff is not accepted based on a human claim alone. The coordinator verifies the following:

- The assigned output files exist in the allowed path.
- The output file version matches the intended assignment.
- A SHA-256 hash is recorded.
- The checks listed in the assignment were performed.
- Any defects or blockers are explicit and not hidden.
- The next owner is named, or a blocker is recorded instead.

If verification fails, the coordinator must return the work to the same owner for repair, without assuming the issue is resolved.

## 6. Dependencies and role ordering

The structure of the project establishes a clear precedence chain.

### Core precedence

- `continuity` owns bible and identity lock logic before most creative review.
- `historian` approves factual and script integrity before dialogue or voice scope.
- `dialogue-sound` is blocked until script and voice route are confirmed.
- `storyboard` is blocked until script, timing, and keyframe decisions converge.
- `producer` gates paid work and final scene packaging.
- `qc` verifies exact exported files after the film is assembled.

### Common dependency patterns

- `T06`/`T07` depend on `T05` script approval and `T01` boundaries.
- `T11` depends on measured guide timing, historical script clarity, and cost freeze.
- `T12` depends on `T03`, `T08`, `T11` and is a gate for chapter generation.
- `T13` depends on `T09`, `T10`, `T12` and becomes the critical gate for all later chapter tasks.
- `T18` depends on all four chapter results.
- `T20` and `T21` depend on final corrections and historical-language work, not just script completion.

These are operational, not theoretical; the coordinator must respect them exactly.

## 7. Lane-specific routing templates

The coordinator routes by role with specific output expectations.

### Historian

- Input: approved script and historical research notes.
- Output: reviewed factual notes, source-cited corrections, risk notes.
- Gate: changes must not silently alter the approved script.

### Continuity

- Input: approved elements, bibles, keyframes, image reviews.
- Output: continuity matrix updates, dress/pose/historical-material comparison findings, candidate acceptance or rejection.
- Gate: no unreviewed image implies acceptance.

### Dialogue-sound

- Input: script, timing, configured voice route, approved lines.
- Output: guide timing, voice tests, dry dialogue, language plan, review files.
- Gate: no language target is accepted without explicit reviewer and approval.

### Storyboard

- Input: timing, script, keyframes, detail-study review.
- Output: scene coverage, animatic timing, shot list updates.
- Gate: selected shots and exact timing only after continuity and script checks.

### Editor

- Input: accepted chapters, animatics, audio tracks.
- Output: edits, review notes, timeline files, final masters.
- Gate: technical playback is required; not just source clips.

### QC

- Input: final masters and exported assets.
- Output: exact review reports, defect list, acceptance or rejection.
- Gate: face safety, sync, captions and full playback must be checked.

### Producer

- Input: all canonical records, approvals, budgets, board state.
- Output: canonical state updates, budget reconciliation, paid-go/no-go decisions.
- Gate: no paid job or final approval without Andre or recorded scope.

## 8. Blocker handling

A blocker must be precise and attributable.

### Required blocker fields

- `taskId`
- `ownerRole`
- `ownerName`
- `reason`
- `unblockCondition`
- `evidencePath`

Example:

```json
{
  "taskId": "T12",
  "ownerRole": "producer",
  "ownerName": "desktop-producer",
  "reason": "Selected image subset is not yet approved by Andre for likeness.",
  "unblockCondition": "Andre reviews the selected subset and records approval in the decision log.",
  "evidencePath": "projects/andre-time-travel/00_brief/decisions/D20-likeness-review.json"
}
```

The coordinator must never leave a blocker as “waiting on something” without a named owner and a clear condition.

## 9. Decision proposals

The coordinator does not write the decision store or the board. Every coordination decision is proposed in its integration handoff, not just in the thread. The director records decision records under `00_brief/decisions/` and the producer applies board changes (`docs/PARLEY_PROTOCOL.md` ownership table; the film gate hooks refuse lane writes there).

Record:

- Which task was dispatched
- Which lane received it
- Which inputs were used
- What evidence was checked
- The acceptance or rejection reason
- Which task is now unblocked or deferred

The coordinator saves only under `projects/andre-time-travel/agents/handoffs/`. The proposals it contains are applied by their owners under `projects/andre-time-travel/00_brief/decisions/` and `tasks/board.json`.

## 10. Non-goals and guardrails

The coordinator must not:

- Create new paid generation requests without a producer-scoped approval.
- Re-run a failed generator job without explicit authorization.
- Claim a task as complete without evidence.
- Dispatch work to a lane outside its allowed write paths.
- Delete originals or archival sources.
- 
Assume a staged workflow and never “skip ahead” to the next milestone by inference.

## 11. Minimum coordination checklist

Before closing any task, the coordinator must confirm:

- Did the handoff path and version match the task assignment?
- Was the exact artifact reviewed and hash recorded?
- Did we identify the next owner or a precise blocker?
- Was the output consistent with the production board and not a duplicate of an older result?
- Did the next task become eligible only after the conditions were satisfied?

## 12. Practical summary

The coordinator in this repo is not a general-purpose task manager. It is a narrow operational role that makes the existing project workflow explicit:

- track dependencies,
- issue bounded assignments,
- verify evidence,
- protect producer-approved gates,
- and keep every next task either clearly owned or blocked.

This makes the project’s distributed work manageable while staying faithful to `AGENTS.md`, `LOCAL_AGENT_HANDOFF.md`, and the Agent Parley model.

