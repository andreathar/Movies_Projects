# Execution sequence, delegation packets and operating runbook

This is an implementation/production runbook to use under the applicable scope. Commands below were checked against installed skill/help for this plan, but are not all executed here. Do not invoke future `production_*.py` modules until implemented; they are proposed paths in the catalogue.

## 1. Sequencing and parallel work

W numbers identify existing workflow-map work; O numbers identify this plan's supporting packages. The catalogue contains an acyclic planning dependency graph. Repeated shot/chapter loops are instantiated with distinct exact input revisions, not by recursively re-running the whole graph. An unnecessary production/correction step may be satisfied by an explicit reviewed reuse or not-needed disposition; never generate merely to satisfy a planning edge.

| Wave | Work and deliverable | Can run alongside | Exit condition |
|---|---|---|---|
| 0: establish truthful baseline | W01–W08, W10–W13 as verify/reuse; W03 contradictions; O14/O20 inventory; O22 charge evidence | Review preparation and locating Galileo | Exact current inputs, owners and scope; prior completed work reused |
| 1: restore coordination and review delivered work | O01/O02 channel proof; W14–W18 independent still reviews; W43 full Galileo playback; W24 measured-guide review | W28 language/reviewer preparation; O03 schema design | Named accepted assignments and evidence-backed findings |
| 2: select and reconcile | W19/W20/W21/W22, W12 bible integration, W09/W23 timing, O21 crosswalk; W25 listen/voice choice | O04/O05 read-mostly tools; O15/O16/O26 active instructions/roles | Selected minimal image packet, scoped likeness and coherent bibles/beat sheets |
| 3: demonstrate rhythm and release envelope | W33 forecast, W34 scratch animatic, W31 envelope delta, W35/W36 packet | W26/W27 audio under applicable scope; W29 translations; O06–O11 implementation/tests | Reviewable animatic, exact next request and unresolved gates explicit |
| 4: prove end-to-end Galileo | W37–W45 scoped one-shot loop and chapter acceptance | Other-chapter local preparation; O12 observer rehearsal | Complete chapter recipe actually played and reviewed; no placeholder mislabeled accepted |
| 5: transfer method | W46 for C/K/N/O, W47 opening/ending; per-shot QC/accounting | W50 sound assets and W29/W30 language/sync proof; O13 only if activation authorized | All five coherent chapters and bookends available for cut |
| 6: assemble and repair | W48/W49 English cut; W51/W52/W53 measured correction pass | W56 historical conform preparation; O17/O18 backfill/recovery | Stable picture and final dialogue timing with defects closed or explicit |
| 7: finish both editions | W54–W58 color/mix/localization/captions/export; O24 rights | Independent reviewers prepare exact checks | Two exact local masters/stems/captions with actual metadata |
| 8: acceptance and archive | W59/W60/W61 full independent QC, Andre acceptance, delivered-copy verification | O25 workflow cold-start review | Both masters accepted; final state has evidence; archive restoration planned/tested within scope |
| 9: closure or continuation | W62, W63/W67 final closeout | None unless next story requested | Terminal stage or separately requested clean draft, with no inherited approvals |

Infrastructure is a supporting lane, not a precondition for every creative review. If Parley remains unavailable, the producer can perform or assign authorized work through a supported local collaboration mechanism, explicitly labeled as such. Never label Codex subagent receipt as a native Parley handshake.

## 2. Capacity and effort planning

Default allocation: producer integrates one delivery at a time; Claude performs one coherent research/continuity write assignment; terminal Codex performs one edit/QC write assignment. Specialists are assigned by role when needed, not kept spinning on duplicate whole-project reviews. Respect the actual native platform and concurrent-task limits. One producer submits one approved paid request at a time.

Plan in deliverable-sized sessions, not promised calendar dates. Initial review/configuration packets should fit one focused session; large media or language work is split by chapter/shot/line set. Collect actual acceptance delay, review time, provider latency, accepted-seconds yield and rework rate after the first two completed packets, then update a duration forecast. No reliable film completion date can be inferred from a count of slots or tasks.

Use an initial proposed 15-minute acknowledgement window during an agreed active session, configurable per assignment. An overdue result alerts once and retains producer ownership. Do not infer refusal from offline elapsed time or repeatedly wake a recipient who needs human permission. Work deadlines reflect scope and actual availability; no generic timer can prove abandonment.

## 3. Budget method before the next paid release

Historical plan values are observations, not live funds: the old 7,741 snapshot, later 6,981 allocation and 5,813 recorded balance have different times/scopes. Galileo's recorded 900 cap/810 stop and 348 ledger total include an unresolved 80-credit exposure. Verify current records before using any figure. Four past ElevenLabs opening tests do not authorize full-film audio.

Build a table per chapter/shot: needed accepted seconds, reusable accepted seconds, new generated seconds, expected usable fraction, model/route/settings, low/base/adverse cost, existing spent, unresolved exposure, proposed cap, stop threshold and final reserve. Keep external audio fees separate.

Suggested forecasting equations, populated from actual evidence:

`new usable seconds = max(0, required selected coverage - compatible accepted reuse)`

`planned generated seconds = new usable seconds / estimated usable fraction`

`remaining forecast = sum(route-specific observed cost for planned generation) + approved remaining audio/sync fees + exposure not already reflected in the live balance + correction reserve`

The unresolved 80-credit item is already included in the historical Galileo debit/348 total. Keep it visible as an attribution/recovery question; do not add it again as future spend or subtract it twice from a refreshed live balance. Include an additional exposure allowance only for a real unsettled charge not already reflected in the account reading, with that basis explicit. Compare each provider's balance and fees in its own unit rather than summing Kling credits and currency as though interchangeable.

Model cost by actual shot duration and route when rates are non-linear; do not extrapolate a single anomalous charge as a universal price. Use observed adverse cases where unexplained variance exists. If projected remaining costs exceed available authorized funds/reserve, reduce unnecessary coverage or surface a concrete scope decision before spending. Do not buy credits automatically or quietly lower core face/language/QC requirements.

## 4. Real Parley readiness commands

From the base repository, use read-only inspection first:

```bash
agent-parley status
agent-parley participant list
agent-parley doctor --json
```

If the intended participants are stopped, the user launches them in separate intended terminals, one terminal per participant:

```bash
agent-parley run claude --repo /mnt/data/Projects_SSD/Movies_Projects
```

```bash
agent-parley run codex --repo /mnt/data/Projects_SSD/Movies_Projects
```

The plan does not execute these launches or automatic approval-resume switches. Once launcher-managed, each lane uses the exact launcher-supplied CLI prefix from its own worktree, never changes into another lane to impersonate it, and reads current base contract/inputs by explicit path and hash when its branch is stale. A base commit or existing branch is not proof of worktree synchronization.

Before assignments, use the two-challenge report-readback handshake in the architecture document. Archive actual message/report IDs and hashes, and distinguish ack from scope acceptance and started work.

## 5. Initial delegation packets

These are ready-to-adapt assignment briefs, not messages already sent. Populate fresh hashes, actual live session identity and unused output revisions before dispatch. Each packet references the relevant source sections rather than pasting the whole plan.

### A. Claude: independent material review of current detail candidates

**Parent:** T12; W14, with light plausibility portion of W18 if capability is suitable. **Inputs:** current AGENTS/workflow contract; adopted research v2 and H01–H06 disposition; D20; detail-studies manifest and selected actual files; current table/axis decisions. **Read-only originals.** Own only a new `03_bibles/detail-planning/image-review-<revision>/` and own handoff. Compare all five encounters for clothing, footwear/floor, hands/sleeves, rear hair, props, room/source plausibility and documented uncertainties. Identify defect by file/hash/region, severity, source and recommended bounded correction; separate art choice from historical fact. No images, provider calls, paid work or canonical edits. Return report, source/output hashes, checks/limitations and explicit next recipient: producer for consolidation. First confirm assignment revision and exact input manifest; stop only affected items if a source is missing.

### B. Terminal Codex: independent visual continuity review

**Parent:** T12; W15–W17. Inputs are current image manifest, approved real Andre references, D02/D04/D09/D20, and producer review. Own only a new `08_edit/reviews/detail-images-<revision>/` plus own handoff. Compare likeness evidence, grooming, anatomy, table landmarks/seat geometry, left/right axis, eyelines and historical-face/reflection risk. Keep right-shoulder images as alternatives unless a valid axis decision changes selection. Return a ranked shortlist and bounded correction list with file/hash/region; do not grant Andre's likeness approval. Do not edit Claude's report, images or canonical state. Acknowledge revision and report actual review coverage. Successor: producer consolidates A and B, corrects only supported defects and prepares selected likeness packet.

### C. Terminal Codex: recover and review the exact Galileo candidate

**Parent:** T13; W43/W44. Queue after B or assign first if it is the more valuable available task; do not overlap two broad active scopes on one lane. Locate existing v2 handoff, timeline, preview and QC in the registered editor worktree. Verify hashes and provenance before copying any deliverable for producer integration. Play the complete candidate with audio at normal speed; report timecoded F01/F03 and bible/line/sync findings. Separate v1 from v2 evidence and guide from final voice. No rerender by default and no new generation. Own a new review folder/handoff only. Successor: producer dispositions the minimal repair and current recipe scope. If playback capability is unavailable, report that specific blocker rather than claiming review from metadata.

### D. Technical worker: handoff contract and read-mostly tooling

**Parent:** supporting workflow; O03/O04/O05/O26. Inputs: memory/handoff design, current v1 template, manager/tests, this architecture, real audit gaps. Own only specifically assigned proposed schema/module/test files in isolated scope; producer owns governing/canonical updates. Preserve v1 compatibility and raw history. First deliver schema/migration design, then implement only accepted design with fake fixtures. Prove missing/stale evidence, wrong role, duplicate ingest and partial-failure behavior. No dispatcher activation, global Parley changes, paid runner calls or trust changes. Successor: independent QA, then producer integration; O06–O13 remain separate bounded packages.

### E. Dialogue/sound: make existing speech work reviewable

**Parent:** T06/T07/T11; W24/W25/W28. Inspect 22 measured scratch tracks, four existing voice tests, script/CSV and language matrix. Own a new timing/review-proposal folder plus handoff. Report actual durations and performance needs, prepare a small voice-by-ear packet, and define each historical-language target/reviewer requirement. Do not render paid voice or silently choose languages. Successor: Andre on exact voice judgment and producer on production timing; language reviewer acceptance remains distinct.

## 6. Send and receipt pattern

Installed `say` supports explicit `--key`, `--ack`, `--within` and `--json`. A future operator send uses an argument array or correctly quoted body, with a persistent key tied to immutable assignment revision. No scheduled/repeating flags are needed. CLI acknowledgement deadlines expose overdue status; the project monitor must supply its own scoped alert/custody logic rather than assume native escalation.

Illustrative command shape, with placeholders to resolve rather than execute literally:

```text
agent-parley say <live-participant> <bounded-assignment-body> --subject <subject> --key <immutable-key> --ack --within 15m --json
```

Recipient writes native report from its own assigned worktree using `report --state partial|blocked|ready --summary ...`, required remaining/evidence fields and `--idempotency-key`. Ready is a claim, not verification. The producer reads the resulting report/handoff via supported status/report interfaces and verifies files; ordinary native reply to operator is not assumed.

Reserve actual output paths before editing when available. Release according to the applicable handoff/integration protocol and current ownership; do not blindly release ready work held under an issue claim. This project remains claim-free for local film coordination unless forge behavior is separately adopted.

## 7. Meaningful monitoring rhythm

At assignment: inspect live readiness and exact input revision once. During work: react to actual progress, blocker, input change or completion; use native bounded waits when reachable. On completion: read one consolidated report/handoff, verify its evidence, then make the successor action concrete. When a recipient is unavailable, record a named blocker and continue independent work. Avoid repeated empty status polling, duplicate research, repeated whole-suite tests and periodic “still waiting” messages.

Archive relevant hook evidence with installed `agent-parley events export --since <window> --output <new-file>` only within the scoped local evidence task; sanitize private runtime details. Exported events corroborate observations. They do not prove media acceptance.

## 8. Producer integration checklist

1. Confirm assignment/revision, output owner and allowed paths; compare fresh base hashes and concurrent work.
2. Verify all claimed files and hashes, source/evidence scope, checks actually performed and declared limitations.
3. Check applicable decisions, unresolved human gates and whether any output invalidates dependent evidence.
4. Integrate one coherent delivery under current local-edit/Git authority; preserve originals and other worktrees.
5. Update only justified canonical fields; leave unverified jobs, take acceptance, language and final flags pending.
6. Record new handoff/ingestion/session event and concise STATE update. Adopt governing workflow changes through AGENTS and platform entry links when implemented.
7. Run grouped appropriate checks, report actual results, and secure successor acceptance or explicit blocker/terminal stage.

## 9. Present handoff and next ownership

The requested planning stage ends with the versioned bundle and verified audit integration. **Desktop producer retains the next execution package.** No Parley lane has accepted a new production assignment in this planning turn. For native Parley execution, the present concrete blocker is stopped film lanes plus the native approval setup gap; unlock is intended terminal restoration and verified scoped handshake. For new dispatcher implementation/activation, execution starts only under an explicit implementation assignment based on this reviewable plan. Existing authorized local reviews can still proceed independently. No new production or background work is claimed running after delivery of the plan.
