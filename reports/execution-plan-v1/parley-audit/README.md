# Agent Parley and hooks: inspected capabilities and proposed film dispatcher

Audit date: 2026-10-10. Scope: Movies_Projects / andre-time-travel. Reviewer: delegated Parley architecture audit; canonical integration remains with the desktop producer. This is a **plan and read-only source audit**, not an installed dispatcher, successful live handshake, changed native permissions, restored lane, or production approval. Only this report directory was written.

## 1. Decision and immediate operational truth

Use the existing daily Agent Parley installation for authenticated lane identity, separate worktrees, mail, advisory reservations, reports, and supported lifecycle observations. Add a **project-owned, local dispatcher** that understands film task dependencies, exact artifact revisions, role assignments, artistic gates, and the mandatory successor rule. Do not replace the daily service or turn film tasks into forge issue numbers merely to fit Parley.

The producer's current live CLI evidence takes precedence over source capability: daily 0.18.0/schema 12 was consistent and ready at the reported 2026-10-10T14:35Z observation; `claude` and `codex` were both dead, there were no claims, notifications and inbound were off, and native bridge approval setup was incomplete. These are **parent-reported live observations**, to be linked to the parent's saved evidence, not independently reproduced in this sub-audit. No native Parley tools are exposed to this desktop audit session. Installed functionality does not establish working participants.

Three distinct layers must stay visible:

1. **Observation:** a native hook, process probe, or report exists.
2. **Coordination:** a named recipient received an assignment and accepted its exact scope.
3. **Production acceptance:** the producer verified the deliverable and the applicable human/media/financial gates are satisfied.

A `Stop` event proves none of layer 3. A ready report is an agent claim. A message acknowledgement alone proves review of that message, not acceptance of all its proposed work. An accepted scoped assignment must identify its input hashes, owner, write set, and completion test.

## 2. Installation and evidence boundaries

Daily executable resolves to `/home/athar/.local/share/uv/tools/agent-parley/bin/agent-parley`. Audited installed source root:

`/home/athar/.local/share/uv/tools/agent-parley/lib/python3.12/site-packages/agent_parley/`

Development checkout remains `/mnt/data/Projects_SSD/agent-parley`; daily and development commands/state/ports must remain distinct. Fourteen inspected installed Python files currently match the corresponding development checkout files byte-for-byte. This permits using those development tests as pointers to intended behavior; it does **not** make development state or test results live daily-service evidence. No upstream tests were executed in this task. See `source-evidence.json` for SHA-256 observations.

Project-local inspection found `.claude/settings.local.json` with permissions entries but **no hook groups**; `.codex/hooks.json`, `.codex/config.toml`, `.agent-parley`, `scripts/dispatcher.py`, and `scripts/coordination/` absent. This is not proof that launcher-injected hooks are absent: the launcher injects session-specific settings independently. Project scripts/tests contain no implemented film dispatcher discovered in the scoped search. Workflow documentation explicitly calls the dispatcher unimplemented.

The older “no remote” wording in `docs/PARLEY_PROTOCOL.md` and workflow-map v1 is stale. `docs/VERSION_CONTROL.md:3–5` now records the authorized private GitHub publication; the parent live inspection confirms origin. The intended **local mail/reservations/reports coordination policy** remains usable. Correct the obsolete factual rationale without inferring ongoing authorization for forge issues, PRs, merges, commits, pushes, or changes in repository visibility.

## 3. Exact existing hooks and capabilities

Source references below are relative to the installed source root unless explicitly prefixed `workspace:` or `dev:`. These are inspected source contracts, not claims about every installed native-client version.

| Surface | Installed contract / source | Correct use and limits |
|---|---|---|
| Common lifecycle events | `roster.py:16–40`: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PermissionRequest`, `Stop`, `SessionEnd` | Claude and Codex adapters declare none unavailable. Capture actual execution before claiming native-client compatibility. |
| Mandatory/delivery subset | `roster.py:39–41`; `checkpoints.py:53–60` | Required hooks: SessionStart/PreToolUse/Stop. Context delivery: SessionStart/UserPromptSubmit/PreToolUse/Stop. PostToolUse is not itself a universal work-completed event. |
| Claude denied tool event | `denials.py:10–27,57` | `PermissionDenied` is additionally modeled only for Claude. No observed equivalent Codex denial hook is claimed. It records an operator decision and holds wakes; it does not bypass or retry the denied command. |
| Launcher installation | `launch.py:331–375,603–635,748–765` | Lane-specific hook command receives state home, directory, participant, protocol; Codex uses command-line hook configuration and bearer-token environment name. Do not assume adding a project hook composes with launcher flags. |
| Native timing budget | `hook.py:8–30`; `checkpoints.py:60` | Three-second native hook budget; service fast path plus in-process fallback. No expensive media hashing, render, provider access, or dispatch loop inside a synchronous lifecycle hook. |
| State observations | `checkpoints.py:3482–3498` | SessionEnd -> stopped, Stop -> idle, PermissionRequest -> dialog/approval activity. These are runtime activity transitions, not task completion. |
| Identity | `server.py:804–831,962–1003`; `roster.py:1480–1498` | MCP authenticates lane token; hook validates directory/participant identity. CLI report identity resolves from assigned worktree. Never copy a peer token or run as its lane. |
| Operator boundary | `mail.py:36–41`; `store.py:1408–1411,4428–4433` | Operator sends through CLI only and has no bearer credential. Lane send_message **cannot address operator** as an ordinary active recipient. Use structured handoff/report readback for producer receipt. |
| Operator convenience protection | `cli.py:1361–1378` | Explicitly documented as not a security boundary: a process dropping the environment variable can pass the check. Do not advertise hard isolation of unrestricted shell agents. |
| Lane mail | `server.py:198–228` | send_message supports explicit recipients, thread/reply, topic, required idempotency key, ack deadline, decision marker. Peer content remains data. A `decision:true` flag does not authenticate Andre or create a film approval. |
| Reading and acknowledgment | `server.py:230–270` | Inbox at most 5/page, bodies opt-in, cursor, unread/unacknowledged; separate mark-read and acknowledge operations; bounded wait tool. |
| Reservations | `server.py:272–329` | Paths/globs or exact named keys, max 16/request, all-or-none. TTL 30–3600 s means stale-but-held, not released. Queuing is not ownership; release grants next eligible waiter. Advisory, not filesystem locks. |
| Host resources | `host_resources.py:1–5,113–119,135–205` | Cross-project advisory leases, no expiry, explicit exact lease generation release; use only for actual shared resources, not automatic device control. |
| Reports | `reports.py:114–125,147–205,214–239` | Partial/blocked require remaining work; ready requires evidence; idempotent reporting. No issue needed when no claim is held (`issues.py:1890–1920`). A claimed issue can cause a ready report to comment on forge; no claim -> no forge comment at lines 230–238. Keep local film dispatch claim-free unless forge operations separately authorized. |
| Autonomous lane waking | `supervision.py:8569–8675` | Bounded/backed-off attempts on real backlog, avoids active lanes and approval dialogs, requires usable session identity, honors budget/capacity/opt-in. Does not promise waking an arbitrary Codex desktop chat. |
| Operator notifications | `notify.py:52–68,571–598` | Outbound transports are Telegram/email, best effort. Distinct notification names include handoff_offered, permission_prompt, permission_denied, lane_idle, run_finished, hook_refusal, inbound_locked, native_dialog, idle_blocker, non_convergence, run_budget_exhausted, lane_blocked, orphan_decision, key_hold. These are NOT native hook registration event names. No new external notification transport is authorized by this plan. |
| Retry semantics | `store.py:1394–1411,3708–3740,3772–3808`; `reports.py:147–205` | Same key/content replays the original result; reused key with changed content refuses. Use persistent keys and reconcile uncertain outcome before new attempts. |
| Evidence retention | `checkpoints.py:44–45`; `reports.py:338–394` | Native hook history is bounded (262,144 bytes and 14 days constants). Export needed evidence before retention discards it. A film audit cannot rely only on transient Parley history. |

`Notification` appears in a checkpoint settling set (`checkpoints.py:50–52`), but is not in the declared seven common native event registrations. Do not advertise it as an installed general hook without inspecting the applicable adapter/client and captured execution.

## 4. Proposed architecture and ownership

The dispatcher belongs to Movies_Projects, not user-global Agent Parley. Proposed files are future implementation locations, not existing deliverables:

- `scripts/coordination.py`: narrow CLI with `validate`, `reconcile`, `ingest`, `plan`, `dispatch`, `ack`, `complete`, `status`, `stop`; exact final names determined during implementation.
- `scripts/coordination/`: schema, event store, readiness evaluator, Parley adapter, outbox, evidence validation, projection renderer. Prefer stdlib to avoid extra dependencies.
- `shared/templates/assignment.json` and `shared/templates/coordination-event.json`: versioned project contracts; extend existing handoff template by reference, not parallel incompatible copies.
- `projects/andre-time-travel/tasks/assignments/`: immutable, producer-authored assignment packets and accepted/revised/revoked receipts.
- `projects/andre-time-travel/agents/handoffs/`: immutable executor deliverables, review findings, hashes, successors or blockers.
- `.runtime/coordination/andre-time-travel/`: ignored local SQLite journal/outbox and lock; minimal runtime state, no provider credentials; owner-only access. Explicit exports go under episode logs/evidence with relative project paths.
- `tests/test_coordination_*.py`: project acceptance tests with fake Parley transport and disposable temp directories.

The producer remains the sole writer of canonical approvals, decisions, manifest, board, ledger, asset registry, STATE and session log. The runtime maintains assignment/delivery state in its own journal, derives readiness from canonical inputs, and proposes canonical updates for producer application. It must not silently become a second production board.

Film roles remain independent of execution lanes: continuity/historian can use `claude`; editor/QC can use `codex`; lighting/dialogue specialist work is bounded and assigned only if needed. Creator self-check and independent QC remain separate assignments. One lane gets one coherent active write scope at a time by default. Do not launch new agents on every hook or grant subordinate delegation by default.

Every assignment contains: local work-package ID (distinct from T01–T21 and provider job IDs), parent task ID, episode, film role, exact participant/session generation, authorization reference, contract revision hash, input artifact paths/hashes, allowed new-output paths, prohibited canonical writes, deliverable schema, expected evidence, hard gates, deadlines, successor, stop condition and zero-spend flag. The receiving lane must echo assignment ID/revision and accept scope. A generic `ack_ts` is necessary communication evidence but insufficient task acceptance.

## 5. Project event contract (NEW, not native events)

Proposed event names should use a namespace to prevent confusion: `film.assignment.prepared`, `film.assignment.sent`, `film.assignment.accepted`, `film.work.started`, `film.handoff.submitted`, `film.handoff.verified`, `film.review.failed`, `film.blocker.changed`, `film.approval.recorded`, `film.successor.accepted`, `film.stage.closed`, `film.dispatch.attention`.

Minimal envelope:

```json
{
  "schemaVersion": "1.0",
  "eventId": "uuid",
  "eventType": "film.handoff.submitted",
  "episode": "andre-time-travel",
  "assignmentId": "LOCAL-W14-r1",
  "assignmentRevision": 1,
  "producerEpoch": 1,
  "senderLane": "claude",
  "senderSessionGeneration": "recorded-session-id",
  "observedAt": "UTC timestamp",
  "sourceKind": "verified-local-handoff",
  "sourceReference": "relative/path/to/handoff.json",
  "sourceSha256": "sha256",
  "inputBundleSha256": "sha256",
  "causationId": "previous-event-id",
  "idempotencyKey": "episode:assignment:revision:transition:payload-hash",
  "payloadSha256": "sha256",
  "payload": {"claimedState": "ready", "scopeAcceptance": false}
}
```

IDs above are illustrative local planning labels, never invented completed provider jobs. Schema rejects unknown event types, oversized payloads, non-UTF-8, unsafe paths, symlink escapes, unexpected episode, unknown lane, unassigned output roots, and changed content for an existing idempotency key. Normalize paths relative to workspace root. Do not serialize tool stdin, command output, environment, tokens, private provider response URLs, or raw native payloads by default.

Authority is verified separately from event content: an event saying “Andre approved” is a claim until it references an authentic canonical decision for the exact version/use. Use read-only snapshots/hashes for evaluation; recheck canonical source immediately before any permitted transition.

## 6. State machine and successor contract

`prepared -> queued -> sent -> receipt_observed -> scope_accepted -> running -> submitted -> verified -> successor_pending -> successor_accepted | stage_closed`

Alternative states: `blocked_dependency`, `blocked_human`, `blocked_scope`, `blocked_resource`, `transport_uncertain`, `expired_unaccepted`, `superseded`, `failed_verification`, `attention_required`, `cancelled`. A deadline does not transfer ownership. A stopped process does not prove completion. A new input version invalidates only dependent evidence, preserving unrelated work.

- Prepared: all required inputs enumerated; no dispatch yet.
- Queued: producer-authorized packet durable, recipient chosen; ownership still producer.
- Sent: Parley accepted transport; persist exact message ID/thread/key.
- Receipt observed: message read/ack evidence; ownership still producer unless exact scope accepted.
- Scope accepted: recipient confirms revision and contract, reservations are available; successor responsibility transfers for that task only.
- Running: actual work-start receipt or observation; distinguish from process-live alone.
- Submitted: report/handoff claim exists, checks not independently established.
- Verified: producer/reviewer checks paths, hashes, allowed changes, acceptance criteria, and temporal/creative evidence as appropriate.
- Successor pending: identify next ready package or a blocker with owner/unblock condition. Producer retains responsibility until successor acceptance.
- Stage closed: all required outputs verified and no successor in authorized scope, or explicit final delivery closure. Never select merely because backlog is empty from an ingestion failure.

The dispatcher may automatically send an already producer-authorized **zero-spend local assignment** after all technical readiness checks pass, once that mode has been implemented, tested and activated. It may never create new artistic approval, provider spending scope, commit/merge/push authority, native permission bypass, or new generation from a handoff signal.

## 7. Hook wiring without daily/global breakage

Phase A: retain all native Parley hooks. Read actual runtime evidence and use explicit completion wrappers to publish project handoffs. No new hook writes or service restarts are required to make the plan reviewable.

Phase B: in a disposable project/lane fixture, prove native hook composition with launcher-injected flags for each intended native client. Capture effective registered groups and actual SessionStart/PreToolUse/PostToolUse/Stop events. If project hooks are overridden, do not edit the installed package or weaken trust. Use an explicit local handoff publisher plus observation adapter, or scope a separate launcher enhancement with its own review and isolated dev test.

Phase C: approved project hook adapter only appends a small sanitized observation or writes a bounded spool envelope and exits. Target its own work to <=100 ms p95 as a future measured budget; preserve native hook output/exit semantics. A failed recorder reports degraded monitoring, not production success. All media hashing and dependency evaluation run outside the native hook deadline.

Phase D: the dispatcher consumes new events and periodically reconciles at startup/recovery and when evidence says a gap exists. Avoid fixed chat heartbeats and repeated unchanged inbox scans. A low-frequency local safety reconciliation, if chosen for runtime reliability, is explicitly part of the installed project service and does not start AI turns without backlog/authorization. Its interval and operation must be documented/tested rather than inferred from this planning request.

Hook mappings:

- SessionStart -> validate lane/session, compare AGENTS/assignment revision, require refreshed acceptance if affected rules changed.
- PreToolUse -> native Parley reservation/branch guards continue; optional project adapter records permitted activity metadata only. Do not run provider CLI or hash whole media trees.
- PostToolUse -> progress observation; only explicit validated handoff publication can create handoff-submitted.
- Stop -> reconcile this lane's outstanding assignment, not mark it completed or immediately launch a successor.
- PermissionRequest / supported PermissionDenied -> park affected assignment, show specific human action, no automated approval.
- SessionEnd -> reconcile liveness and ownership; retain work and reservations according to native contracts; no implicit orphan takeover.

Do not register invented native events called `TaskCompleted`, `AfterHandoff`, or `SuccessorReady`. Those belong only to the new film event schema.

## 8. Durable queue, deduplication and crash safety

Use one local SQLite database with WAL, foreign keys, bounded busy timeout, integrity checks and explicit schema migrations in a disposable copy before rollout. Runtime tables: `events`, `source_cursors`, `assignments`, `assignment_transitions`, `outbox`, `deliveries`, `review_receipts`, `blockers`, `leases`, `dead_letters`, `settings_versions`. Track canonical source hashes, not copies pretending to be authority.

Unique event key: source + source generation + event identifier; unique transition key: episode + assignment + revision + transition + payload digest. In one transaction, ingest event, evaluate against the saved input snapshot, record planned transition, and create at most one outbox action. Separate sender drains outbox, records Parley result, and marks transport delivered. Store argument digest so a same-key/different-body retry fails visibly.

Crash after send but before recording response: set `transport_uncertain`; query existing Parley mail/report records or retry with the identical supported idempotency key. Never make a fresh key simply to escape uncertainty. Transport retries are bounded and confined to zero-spend communication; they are unrelated to forbidden automatic paid-generation retries.

Single active dispatcher holds a process lock plus durable generation/fencing counter. A recovered process increments producer epoch; stale workers cannot commit new transitions. This is protection against dispatcher races, not a hostile-agent security claim. Claim outbox rows with compare-and-swap; two workers must produce one transport action. Native hook logs may rotate, so cursor tracks source identity/generation, not byte offset alone. Unreadable/truncated input enters quarantine; reconciliation scans durable local handoffs/report IDs to recover missed observations.

File handoffs publish via temp write, fsync, atomic rename into their final unique revision path; verify source/target hashes before integration. Do not treat file creation or size stability as completion if the declared digest or required fields are missing. Large media lives as artifacts; event rows hold paths/digests only.

## 9. Failure and escalation matrix

| Failure | Required state and response | Resume condition |
|---|---|---|
| Participant dead/unmanaged/no native identity | blocked_scope or attention_required; producer keeps assignment | User-terminal launch/restoration, current contract receipt, authenticated scope acceptance |
| Native bridge approval missing | specific manual setup blocker; no changes to trust/permission settings by dispatcher | User resolves native setup in terminal, or explicitly authorizes separately scoped configuration |
| Service unavailable/version or schema drift | hold outbound dispatch; preserve queue; read-only diagnosis | Compatible service and identity verified; reconcile uncertain sends |
| Hook absent or client ignores config | degraded monitoring; retain explicit handoff path | Actual event proof or approved fallback, not configuration inventory alone |
| Report ready but artifact missing/hash differs | failed_verification, no successor dispatch | Owner supplies corrected immutable revision or truthful blocker |
| Duplicate/reordered hook/mail event | replay original transition; no duplicate assignment | Automatic no-op with diagnostic count |
| Peer cannot reply to operator | expected delivery limitation; reports/handoff readback | Producer reads exact durable return artifact; no fake native two-way success |
| Changed approvals or input source after queue | superseded/blocked_scope | Reevaluate new version; producer reissues only affected scope |
| Reservation collision | blocked_resource; no overlapping write | Correct reservation grant and fresh base hashes |
| Recipient silent after deadline | expired_unaccepted, producer remains owner; one meaningful alert | Reassign only after cancellation/scope fencing, or recipient accepts current revision |
| Long render still running | running with process/artifact evidence, not heartbeat churn | Completion result or bounded failure; no duplicate render |
| Storage full/SQLite corruption | stop transitions, mark degraded and retain raw queue | Verified restore and replay in read-only mode before enabling dispatch |
| External spend attempted in assignment | reject by action allowlist, alert producer | Exact producer-owned approved request handled outside dispatcher |
| Permission denial | park the affected action, preserve reason | Human decision through native controls; no rewording to evade denial |
| Artistic or language gate absent | blocked_human only for dependent action | Exact scoped human/qualified-review record |

## 10. Acceptance tests (must be implemented, then executed)

Existing Parley test source provides patterns, not completed tests for this project: `dev:tests/test_hook_client.py:121,139,360,431`; `test_supervision.py:211,411,597,1055,1106,1378,1412,1450`; `test_retry_safety.py:38,48,65,82,196,226`; `test_bridge.py:1214,1274,3728,3772`. No claim of passing these tests in this audit.

| ID | Test fixture / action | Pass evidence |
|---|---|---|
| C01 | Rehydrate empty runtime from 21-task board with stale scopes | Readiness blocked where semantics conflict; no implicit rewrite/approval |
| C02 | Same handoff/Stop delivered 100 times | One submitted event/transition; one successor draft; no second message |
| C03 | Same idempotency key, different input hash | Explicit refusal and unchanged original record |
| C04 | Two dispatcher workers race same outbox row | One send; fenced old producer cannot advance state |
| C05 | Crash before send / after send / before ack commit | Restart recovers exactly one logical delivery and original key |
| C06 | Events out of order: Stop before handoff, acceptance before local sent receipt | Reconciles source evidence; no inferred completion or owner loss |
| C07 | Sender claims wrong lane/session/episode or stale revision | Quarantine/refusal, unaffected tasks continue |
| C08 | Relative path escapes, absolute path, symlink to external sensitive file | Rejected without reading/disclosing target |
| C09 | Native payload contains token or private URL | Output event excludes value; logs contain no sensitive payload |
| C10 | Ready report missing output or wrong digest | No verified state, no successor; exact repair owner |
| C11 | File exists but still being written | Not accepted until explicit final publication and correct digest |
| C12 | Scope accepted without all required inputs or reserved paths | Assignment stays blocked, no write task released |
| C13 | Hash changes after readiness evaluation | Pre-dispatch compare-and-swap refuses stale packet |
| C14 | Ack only, no exact scope-acceptance receipt | Producer retains responsibility |
| C15 | Dead/unknown/busy/dialog/capacity-exhausted lane | No blind launch; appropriate reason and no ownership transfer |
| C16 | Operator mailbox reply refused | Readback route reports limitation; durable handoff accepted only after verification |
| C17 | Film approval false / stale / different artifact | Dependent production action rejected, local research unaffected |
| C18 | Paid CLI/HTTP, commit/merge/push or permission mutation action in queue | Refused by narrow action allowlist; no external action occurred |
| C19 | Hook recorder timeout or crash | Native client semantics preserved; monitoring marked degraded |
| C20 | Stop with no report | Remains unfinished, no fabricated completion |
| C21 | SessionEnd during outstanding work | Ownership retained with named recovery/blocker |
| C22 | Hook history rotates; restart cursor stale | Gap identified and local report/handoff reconciliation recovers retained truth |
| C23 | Missing native hook or disabled trust | No automatic configuration rewrite; explicit blocked activation |
| C24 | stdout/error with Unicode, long messages, >4096-byte body | Bounded body with local evidence reference; no truncation of task authority |
| C25 | One verified task has no accepted successor | Close-out fails unless named blocker or legitimate stage-closed record exists |
| C26 | Episode continuation template created | No inherited approvals, provider IDs, runtime, owners or spending |
| C27 | Existing non-Parley project activity and daily state | Baseline unchanged outside assigned Movies_Projects paths |
| C28 | Normal two-lane local review dry run | Inputs -> accepted scope -> output/hashes -> independent verification -> accepted next owner, all evidenced |

Run film stdlib tests and `manage.py validate` after management/schema integration. These are separate from real native-hook smoke tests, media playback, language review and Andre's likeness/voice acceptance.

## 11. Delivery milestones and rollback

M0: source/live inventory and policy divergences recorded (this audit + parent evidence). M1: producer reconciles stale task scopes and chooses exact zero-spend first assignments. M2: restored lanes accept current contract in user terminals; collect real identity/read/ack/report evidence. M3: pure planner, schemas and event journal implemented with fake transport; read-only readiness output passes tests. M4: completion publisher and tested native hook observation adapter installed only within explicit project scope. M5: shadow mode consumes events and proposes actions, sends nothing; compare with producer decisions over one real handoff. M6: enable bounded zero-spend local dispatch for one assignment family after successful rehearsal. M7: broaden only to validated families; retain producer/human gates and meaningful-change notifications.

Required evidence at each milestone: versions/hashes, exact test results, native client/runtime identity, effective hook composition, failures and limits, next owner or blocker. No task is labeled “automation complete” until M6 end-to-end successor acceptance is demonstrated.

Rollback: set project dispatcher mode to disabled and stop only its recorded process generation; preserve journal/outbox/evidence for reconciliation; cancel pending **unsent** messages, record uncertain deliveries rather than assume cancellation; release only exact owned leases after work stops. Restore project hook adapter configuration from saved pre-change digest after confirming no concurrent edits; never revert native/global configuration or the daily Parley installation. Return to manual producer dispatch and explicit handoff readback. No media, original, ledger entry, approval or historical event is deleted.

## 12. Outstanding producer decisions / factual limits

- Link this source audit to parent CLI evidence; do not describe dead lanes as ready.
- Fix the no-remote documentation divergence in an authorized management pass, preserving local-first policy.
- Choose whether a future project dispatcher runs only during active producer sessions or as an explicitly installed local service. Neither mode is activated by this report.
- Restore lane usability without automatic trust changes; test exact native-client versions before promising hook support.
- Decide and prove a completion-notification surface for the desktop producer. Native operator mail is not a return mailbox, and native Telegram/email notification is currently off. A durable local report plus visible dashboard during an active session is viable; automatic desktop awakening needs a separately supported, explicitly configured mechanism.
- Any hard prevention claim must name and test its enforcement boundary. Unrestricted agents plus advisory reservations are not OS isolation; the dispatcher only constrains actions routed through it.

Memory used only to identify likely installation-isolation and operator-mail pitfalls. All source capability claims above were rechecked against installed files. Memory reference for the parent final answer if used: `MEMORY.md:44–48` and `MEMORY.md:96`; rollout IDs `01a12496-faf7-7062-be9f-bab9ba48c26e`, `01a12218-4ca7-79d2-af30-dc09597e22c3`.
