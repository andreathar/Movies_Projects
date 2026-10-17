# Coordination procedure

Scope: bounded coordination under `AGENTS.md`, [PARLEY_PROTOCOL.md](PARLEY_PROTOCOL.md), [LOCAL_AGENT_HANDOFF.md](LOCAL_AGENT_HANDOFF.md) and the current board. [Team map](../agents/README.md) defines concise role/process/path names; [role contract](../agents/CONTRACT.md) defines modes and evidence. Neither role names nor this procedure start participants or grant permissions.

## 1. Scope → Assign

Complete mandatory startup. Read current dependencies, approvals, blockers and exact input versions. Inspect only relevant/new handoffs, expanding to dependency evidence as necessary. The workflow map's dated tables are not live board status.

A task may be offered only when its actual prerequisites are satisfied, its recorded blocker is resolved by the authorized owner, applicable approvals match its content/version/use, and an available participant can perform the required checks. File existence, a completed generator job or acknowledgement alone is insufficient. Do not bypass a production blocker because an upstream task merely delivered files. Independent local preparation may continue only within its existing authorized scope.

Discover real participants; never route to proposed roster names. In a live launcher-managed lane use its exact supplied CLI prefix, own worktree and injected identity. Outside such a lane do not impersonate `claude`, `codex` or `operator`, start services, relaunch clients or install plugins to make dispatch work. Report unavailable coordination to the producer; do independent assigned local work where possible.

Send one 150–250-word assignment per coherent output, with `ack_required`, `ack_within` 900 seconds unless explicitly varied, and an idempotency key. Keep payloads below Parley's message limit; link exact local specs for detail. Use this format (angle-bracket values are placeholders, not existing tasks or a send-ready message):

```text
subject: <task-or-topic> / <role> / <version> / Assign
owner: <discovered participant>; role: <stable role ID>; mode: review|edit
scope: <goal and explicit producer authorization>
episodeRoot: projects/<episode>
task/package: <existing IDs if assigned; otherwise not applicable>
inputs: <workspace-relative paths, versions, SHA-256, review state>
allowedPaths: <exact editable outputs; empty for findings-only review>
checks: <required tools, tests and evidence; separate media/language gates>
constraints: <no spend, external writes, substitutes or canonical edits>
nextOwner: <named successor and readiness condition>
ackWithin: 900 seconds; completionDeadline: <explicit or not set>
idempotencyKey: <topic>-<version>-<sequence>
```

A retry of the same send reuses its key; changed scope/version gets a new key and states what it supersedes. Acceptance must confirm role, inputs, mode, paths and checks. Mail acknowledgement is not necessarily scope acceptance. Producer owns ready work until accepted. Existing local film assignments need no forge issue or invented issue number.

## 2. Make → Check

The accepted owner reads only required evidence, reserves assigned outputs through available Parley and performs the bounded work. Reservations are advisory; they grant no authority and are not filesystem locks. Stop overlapping edits on conflict. Do not edit another participant's checkout or assume a successful reservation proves native filesystem/tool access.

Review-only adapters return findings to the parent and do not create files. An explicit edit assignment delivers new versioned artifacts plus an episode handoff from `shared/templates/agent-handoff-v2.json`. Preserve base hashes, original media, provider results and concurrent edits.

Coordinator verifies:

- Claimed outputs are within assigned paths and match exact versions/hashes.
- Declared checks actually ran, with evidence and limitations; no fabricated playback or language review.
- Relevant existing findings were dispositioned, not hidden or re-audited without cause.
- Dependencies, Andre-only gates and decisions remain separate from delivery.
- Successor is named, or a blocker has owner, evidence and unblock condition.

Missing tools/checks are `not_run`; required full-media QC stays incomplete. Request a bounded repair from the current owner when evidence fails. Do not automatically grant tools, regenerate media or resubmit jobs.

## 3. Integrate → Close

Coordinator returns a proposed integration handoff under `projects/<episode>/agents/handoffs/`. Proposed decisions go in `proposedDecisions`; blockers in `blockers[]` with `description`, `owner`, `unblockCondition`; successor in `nextActions`. It never edits board, approvals, ledger, decision store, STATE, session-log or mistakes.

Desktop producer checks the delivery (`manage.py handoff check`), reviews diffs/claims and ingests only verified evidence (`manage.py handoff ingest`). Director records authorized decisions. Integration is not approval of media, spending, commit or publication.

Close only with an accepted successor, a precise owned blocker or a genuinely closed stage. If release of file reservations is appropriate after delivery, coordinate it explicitly; responsibility still stays with the producer/current owner until accepted transfer. Record actual checks/hashes once and communicate material changes only.

## 4. Unavailable peers and escalation

Inspect status when a routing decision or changed event requires it, not on a timer. After a needed question use one scoped event wait where available. If it expires, or the peer is offline/paused, report the blocker and owner; do not loop, repeatedly wake a peer or invent a response. No periodic report, background schedule, Telegram/email notification, new transport, supervision setting or external contact is authorized by this procedure.

Andre remains the operator for runtime/permission/integration decisions. If an existing capability refuses an action, report the exact refusal and minimum operator decision; no alternate route or trust change. Separate role approval, technical checks, human acceptance and model/provider activation. Proposed roles or historical successful messages prove no current runtime readiness.
