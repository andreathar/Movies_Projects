# Validation, rollout, risks and recovery

Tests below are **future implementation acceptance scenarios**, not checks claimed executed by this planning task. Use temporary fixtures, fake provider/Parley adapters and small local dummy artifacts. Never spend credits to test a permission boundary. Current-plan validation is recorded separately in `reports/execution-plan-v1/validation.json`.

## 1. Release gates

| Gate | Required evidence | Who accepts | Failure response |
|---|---|---|---|
| R0: design coherent | Source coverage, no dependency cycle, explicit authority, contract fields, operations separated from production acceptance | Producer + independent technical reviewer | Fix plan/schema before implementation |
| R1: read-mostly tools | Resume/lint/check tests, unchanged canonical snapshots, backwards-compatible v1 handling | Producer | Retain manual reads and existing validator |
| R2: storage/recovery | Crash, duplicate, migration, cursor and atomicity tests | Independent technical QA | No adapter sends or live activation |
| R3: real channel | Live intended lane, exact contract/inputs, both challenge echoes, actual acknowledgement and scoped acceptance | Producer | Named readiness blocker; no assumption of start |
| R4: observer | Real harmless task observed end to end with predictions matching producer judgment | Producer | Keep observation only or disable adapter |
| R5: local dispatch | One explicitly released local-document assignment→review→successor chain, zero forbidden actions, rollback proven | Producer within applicable activation scope | Stop future sends, reconcile in-flight work, return manual |
| R6: broader allowed local tasks | Representative history, edit/QC and failed-review cases; no unexplained duplicates; cold start tested | Producer | Narrow allowlist; never expand to paid execution implicitly |
| R7: production recipe | Selected likeness, exact paid scope, actual job/charge, full temporal/technical chapter review | Producer + applicable Andre gate | Keep later paid chapters held; continue independent preparation |
| R8: final delivery | Both exact exported masters, language/voice/likeness and story acceptance, full playback, stream/mix/caption proof | Independent QC + Andre + producer integration | Correct failed scope, export new revision, recheck affected evidence |

## 2. Coordination test matrix

Each scenario records fixture/input, initial state, action, expected state, external-call count, evidence output and teardown. “No dispatch” means zero calls to the send adapter, not merely an error message after sending.

| ID | Scenario | Required result |
|---|---|---|
| CT01 | Same completion event delivered twice | One journal transition and at most one successor outbox entry |
| CT02 | Same assignment key, changed payload | Refuse and report conflict; no changed task hidden under old identity |
| CT03 | Handoff precedes work-start/acceptance event | Retain evidence out of order; do not invent missing acceptance; reconcile explicitly |
| CT04 | Output file missing | Verification fails and dependent dispatch count remains zero |
| CT05 | Output bytes differ from claimed hash | Quarantine evidence; return precise defect to owner |
| CT06 | Input revision changes after preparation | Mark affected packet superseded; invalidate only dependent checks |
| CT07 | Input changes between validation and send | Fresh comparison/fencing blocks stale assignment |
| CT08 | Parent ready report without required playback | Submitted remains unverified for temporal gate |
| CT09 | File exists and job is completed, no take review | No accepted take/slot or production completion |
| CT10 | `Stop`/`SessionEnd` arrives with incomplete work | Runtime state changes; task remains owned and incomplete |
| CT11 | Registered recipient is dead | Block with producer custody; do not report running |
| CT12 | Recipient in native permission dialog | Hold affected work; no permission auto-response or trust change |
| CT13 | Recipient reads/acks but never accepts scope | Receipt recorded; producer retains task until explicit acceptance |
| CT14 | Acceptance for old revision/session generation | Reject as stale; current task ownership unchanged |
| CT15 | Acknowledgement deadline passes | Actionable overdue blocker once; no ownership transfer or paid retry |
| CT16 | Assignment refusal/cancellation | Preserve report/artifacts; record owner and successor disposition; no invented replacement |
| CT17 | Reservation overlaps peer | No overlapping writes; queued reservation not treated as granted |
| CT18 | Reservation TTL expires | Confirm native stale-held semantics; never seize automatically |
| CT19 | Host lease conflicts or has stale owner | All-or-none acquisition; exact operator recovery needed; no unrelated release |
| CT20 | Crash after journal commit before send | Restart drains original outbox once |
| CT21 | Crash after send before response persistence | Transport uncertain; reconcile/retry same identity only |
| CT22 | Two coordinator instances start | One active writer; stale fencing generation cannot transition/send |
| CT23 | Partial/truncated handoff or event file | Quarantine; complete atomic revision later can recover without duplicate |
| CT24 | Parley log rotates or events expire | Cursor generation detects change; durable handoff/report reconciliation recovers |
| CT25 | Unsupported JSON/event schema | Fail closed for affected transition with diagnostic, no speculative parsing |
| CT26 | SQLite lock/disk-full/corrupt store | Preserve fail state; no send without durable intent; documented restore path |
| CT27 | Adapter send times out | Bounded zero-spend retry/reconciliation; no new dispatch identity |
| CT28 | No successor legitimately required | Stage closes with evidence; no endless agent or self-assigned work loop |
| CT29 | Verified output has ready successor but no accepted recipient | Producer custody and named blocker remain visible |
| CT30 | Handoff attempts canonical approval/ledger edits | Policy denies action and producer review flags unauthorized diff |
| CT31 | Hook payload requests provider generation/purchase | No paid adapter path exists; zero calls even with claimed approval text |
| CT32 | Hook payload requests Git push/merge/external message | Deny outside fixed allowlist; remote existence does not authorize it |
| CT33 | Report contains shell syntax/instruction injection | Treat as data; never execute arbitrary text or expand a command |
| CT34 | Path traversal/outside-root symlink/credential field | Reject/redact before persistence or access |
| CT35 | Fake `decision:true` or relayed D16 used as approval | No personal/paid gate cleared; require actual canonical scoped provenance |
| CT36 | Global Parley config or another project changes | Film adapter refuses unrecognized installation/policy identity; does not rewrite globals |
| CT37 | Hook recorder fails or exceeds timing budget | Native semantics preserved; monitoring degraded explicitly; no success fabrication |
| CT38 | Launcher overrides project hook file | Effective-registration test detects missing hook; use explicit publishing fallback |
| CT39 | Operator return mail rejected | Report-readback path succeeds or remains explicitly blocked; no fake desktop reply |
| CT40 | External notification unavailable | Durable local alert remains; no claim of delivery/wakeup |
| CT41 | Unchanged blocked status repeats | One alert per meaningful revision; no repeated chat heartbeat |
| CT42 | Rollback during an in-flight assignment | Future sends stopped, accepted owner retained, uncertain send reconciled, manual route usable |
| CT43 | Handoff v1 loaded | Preserve original; explicit migration/disposition rather than fabricated v2 fields |
| CT44 | Same handoff ingested twice | No duplicate board/ledger/session entries; original ingestion receipt returned |
| CT45 | Producer ingestion crashes across multiple files | Transaction/journal detects incomplete integration; never declares all committed |
| CT46 | Contract changes while lane remains open | Affected work requires updated contract acknowledgement before continuation |

## 3. Film and producer-preflight tests

| ID | Scenario | Required result |
|---|---|---|
| FT01 | Arbitrary nonempty authorization string | New producer preflight refuses it as scope proof |
| FT02 | Valid scope but changed model/reference/duration/request hash | Release invalid; revised scope review required |
| FT03 | Request exceeds remaining cap or stop threshold | No submit; specific financial blocker |
| FT04 | Balance is historical or fee scope is other provider | No paid release based on it |
| FT05 | Submission returns unknown outcome/job ID lost | Persist unknown exposure, query/reconcile via installed CLI; no resubmit |
| FT06 | Job ID already exists for request | Resume only; zero additional paid submission |
| FT07 | Other account activity makes balance delta ambiguous | Label cost evidence uncertain; no fabricated exact charge |
| FT08 | T09 complete but T07 final voice pending | English guide preparation can proceed; final voice/Edition H gates remain closed |
| FT09 | New D20 still inherits old pilot approval | Detect scope mismatch; require selected likeness/motion evidence where applicable |
| FT10 | Frame sample passes but intermediate reflection exposes face | Reject selected take; every-risky-frame requirement catches it |
| FT11 | Dubbed speech differs in pause/text/duration | Sync review required; no automatic audio-swap acceptance |
| FT12 | Reaction cut precedes motivating phrase | Timestamped causal failure; repair edit/performance scope |
| FT13 | Caption file belongs to another audio revision | Version/hash mismatch blocks delivery |
| FT14 | Exact master differs after QC | Old QC invalid for changed bytes; inspect/export/review affected result |
| FT15 | English master passes, historical review pending | `finalMovieVerified` cannot be promoted |
| FT16 | Final flag with only `finalPicture=true` | New final gate requires two exact-file proofs plus applicable human/language/technical evidence |
| FT17 | Upscaled 720p source labeled native 1080p/4K repair | Provenance check rejects misleading quality claim |
| FT18 | New continuation copies old approvals/budget/job IDs | Clean-draft check rejects contamination |
| FT19 | Cleanup proposes referenced original deletion | Preservation/reference gate blocks destructive action |
| FT20 | Unequal chapter timing chosen later | Coordinated manifest/CSV/atlas/validator tests required; current fixed model not silently bypassed |

Human/temporal tests must be executed by a capable reviewer on real media when those assets exist. Unit tests can validate evidence requirements and prevent unsupported state transitions; they cannot determine authentic likeness, good acting or correct pronunciation by themselves.

## 4. Evidence package per implemented change

Record input versions, exact owned files, before/after hashes, command/check names, return status and bounded output, tests actually executed, defects/limitations, independent review and next accepted owner or blocker. Keep current tests separate from inspected-but-not-executed upstream test sources. Do not redact a failure into a generic success count.

Run project stdlib tests and `manage.py validate` after coherent management/code changes. Add targeted tests only for newly implemented behavior. Review active links/schemas and policy deny paths. Retain four known skill warnings until their source deltas are actually reviewed. A plan-only document change needs no fake runtime smoke test.

## 5. Risk register

| Risk | Trigger/early signal | Prevention and response | Owner |
|---|---|---|---|
| Stale source wins over newer direction | Mismatched contract/bible hashes | Stop affected action, compare deltas, producer adopts explicit scope | Producer |
| Infinite coordination without film progress | More reports with no accepted next media/review result | Keep first creative successor visible and bound infrastructure scope | Producer |
| Duplicate paid request | Unknown submit result, lost ID, retry suggestion | Durable intent, single producer, resume/reconcile only | Producer |
| Cost overrun | Accepted seconds lower than forecast, unexplained balance deltas | Worst-case cost scenario, reserve, shot-level cap and stop threshold | Producer |
| Historical face exposure | Profile/reflection appears during motion | Conservative envelope and every-frame risky-shot review | Continuity/QC |
| Identity drift across new shots | Old/new reference mix or aggressive movement | Selected likeness packet and bounded envelope-delta test | Continuity/Andre |
| Voice late in production invalidates picture | Final performance duration differs | Measure final lines early; preserve handles; plan offscreen/sync route | Sound/editor |
| Language unachievable | No qualified reviewer or supported route | Target/adaptation decision early; preserve English independent path | Dialogue-sound/Andre |
| Missing lane acceptance | Dead/dialog/ack-only state | Named custody, real handshake and accepted scope before claiming work | Producer |
| Dispatcher corrupts canonical state | Automatic write inferred from report | Producer-only ingestion and atomic staged changes; rollback journal | Technical owner |
| Hook breaks daily tooling | Overridden registration, timeout, config collision | Disposable composition test, project-local adapter, preserve native hooks | Technical owner |
| Lost evidence | Native log rotation, transient URLs, pointer-only restore | Local originals, exported proof, inventory and LFS recovery test | Producer |
| Cleanup harms concurrent work | Base hash differs or existing CLAUDE edit overwritten | Compare fresh hashes; no blind cleanup/reset; unique revision outputs | Producer |

## 6. Rollback acceptance

Rollback must be rehearsed before dispatch_local activation. Pass only when the stop switch prevents new sends, all accepted tasks still have owners, uncertain sends remain reconciliable, prior adapter configuration is restored without overwriting others, canonical/media hashes remain preserved, and manual dispatch/report reading works. A monitor that merely says “disabled” without this evidence is insufficient.
