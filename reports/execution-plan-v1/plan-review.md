# Independent review of execution-plan-v1

Reviewer: requirements-audit subagent. Date: 2026-10-10. Scope: read-only review of README, documents 01–06, package catalogue and requirements matrix. Parent producer requested this review and owns integration/successor. No implementation, production, runtime activation or test suite was executed.

## Verdict: REVISIONS REQUIRED

The bundle covers the requested domains and is careful about authority, preserved evidence and runtime claims. Four package-readiness issues should be corrected before calling its machine-readable graph executable. These defects are in the proposed plan, not evidence that any unauthorized action occurred. All packages currently have execution disabled.

### R1 — Split scratch preparation from approved production release

**Files:** `projects/andre-time-travel/tasks/execution-plan-v1/work-packages.json`, W34 (around line 2792); corresponding `02-work-packages.md` W34 (line 537); README critical-path diagram.

W34 combines building the English scratch animatic with approval and hard-depends on W20 (Andre approves selected-new-still likeness) and W33 (a package including live provider refresh before paid release). This blocks local work with temporary/candidate stills on gates that do not govern making the scratch. T11's source specification explicitly permits temporary/approved stills; the workflow map says guide work is independent; the runbook also promises useful local preparation while separate gates remain unresolved. The README diagram likewise combines measured guide, final voice and language routes into one node feeding the animatic, despite its qualifying prose.

**Required revision:** Model a preparation predicate/substage for W34 using selected labeled candidates and measured guide timing, and a separate storyboard/production-readiness predicate that requires the applicable likeness and budget envelope. Do not make current account access a prerequisite for constructing the local scratch. Keep W20 and fresh paid scope enforced before the relevant production request. Update JSON, generated package prose and diagram consistently.

**Acceptance scenario:** With W24 measured guide and usable candidate selection ready, Andre's W20 decision pending and no fresh account reading, a zero-spend scratch assignment is eligible; W37/W38 remain ineligible for an unapproved production shot.

### R2 — Permit per-edition captions/export without completing the other edition

**Files:** `work-packages.json` W57 (around line 4735), W58 (4820); `02-work-packages.md` lines 905–937; `03-film-execution.md` line 67.

W57 and W58 aggregate both editions and depend on W56 historical conformation. As written, the package evaluator cannot dispatch English captions/export until all historical-language work is complete. That contradicts the plan's statement that Edition E can finish independently, and the user specification's English-first route. A combined final project gate is correct; a combined caption/export readiness gate overblocks the finished English film.

**Required revision:** Define per-edition instances or explicit `edition=E/H` readiness for W57–W60. English requires its own locked audio/picture/mix/caption evidence; H additionally requires W29/W30-H/W56. Aggregate both only for W61 and `finalMovieVerified` (or equivalent final task acceptance). Retain independent exact-file QC and personal acceptance for each edition.

**Acceptance scenario:** With English picture/sound/captions approved and H target/pronunciation unresolved, English export and QC can proceed. Historical export and combined finalMovieVerified remain blocked.

### R3 — Require reviewed localized inputs before the historical speech-route proof

**Files:** `work-packages.json` W30 (around line 2462) and W56; `02-work-packages.md` W30 line 473.

W30's done evidence requires both English and a representative difficult localized line, but dependencies are only W27 and W31. W27 concerns final dialogue from W25/W26; none of these packages requires the historical target/translation/pronunciation review of W28/W29. The critical H test can therefore be described ready before its actual reviewed line or audio exists, while English route proof is also forced to wait for the H proof under the same completion label.

**Required revision:** Separate scoped E and H instances/predicates. E consumes the final English sample, approved picture and relevant envelope. H consumes the specific W29 reviewed translation/version plus the actual approved test audio and target/route availability evidence. Preserve an explicit approved mouth-hidden fallback where chosen. Do not attach historical requirements to unrelated English preparation.

**Acceptance scenario:** W27 English material and W31 pilot envelope permit an E test. With W29 missing, H test remains blocked with the language/audio owner; no H speech approval or W56 readiness can be inferred from E's success.

### R4 — Separate adapter implementation from live participant restoration

**Files:** `work-packages.json` O01 (around line 5730), O07 (6310); `02-work-packages.md` O01/O07; `06-runbook-and-sequence.md` waves 1–3.

O01 combines read-only capability inventory with user terminal restoration and current session/worktree proof. O07 adapter implementation hard-depends on completed O01, which makes the software build and fake-fixture tests depend on the user restoring stopped lanes. The design specifically calls for fake adapters and offline tests before live rehearsal; actual native channel proof belongs to O02/O12/R3–R4.

**Required revision:** Split O01's inventory evidence from live restoration, or add dependency predicates. O07/O08/O09 development may use the recorded supported capability snapshot and mocked transports. O02 plus live recipient/approval proof must remain hard requirements for real-channel rehearsal and activation.

**Acceptance scenario:** Stopped lanes/native approval gap blocks real sends/handshake/observer rehearsal but does not block implementation and deterministic fake-adapter tests.

## Nonblocking design clarifications

1. **Instance expansion:** The catalogue notes instantiate W35–W42 per selected shot, while W45 is “each complete chapter” and W46 must follow the first accepted Galileo W45. Specify `W45[G] -> W46 preparation/release -> W45[C/K/N/O]` semantics in the schema design, and distinguish W47 opening/ending preparation from paid production. Otherwise a future evaluator could read W45 as an all-chapter aggregate and create an implicit circular gate. The prose already explains the intended sequence; the missing part is explicit machine scope.
2. **Remaining-cost arithmetic:** The runbook includes unresolved exposure in forecast. The known80 was already charged in the observed balance. Preserve it as an unresolved accounting item, but do not add an already-debited item again to a future-spend forecast compared against the current remaining balance. Only additional unreflected liability belongs in remaining-cost exposure; gross episode-cost views can include all charges once.
3. **Source labels:** INV requirement rows mostly cite generic AGENTS/production-tasks paths even where the specific source is the dramatic-direction document or local workflow. The package/appendix evidence supplies detail, so coverage is present; sharper source citations would make a later audit faster.

## Coverage assessment

- T01–T21: all21 represented in requirements matrix with package mappings and preserved canonical-board authority.
- W01–W68: all68 present in the96-package catalogue and detailed package document.
- Cleanup: all8 phases have CLEAN01–CLEAN08 mappings; inventory, semantic consolidation, preservation, skill scope, lifecycle, validation and film successor are retained.
- Memory/handoff: all4 pending phases have MEM01–MEM04 mappings; phase0 stays delivered; v1 compatibility, read-mostly tools, ingestion/backfill/current plan and producer ownership are explicit.
- Creative/delivery: likeness, zero historical full faces, table/wardrobe/axis, difficult-line causality, source-fiction separation, sound/light, language reviewers, captions, selected-shot scope, exact final master tests and preservation are covered. Final language/audio/likeness judgments are not replaced by unit tests.
- Operational: native events versus proposed film events are distinct; actual dead lanes and off external notifications are explicit; report-readback acknowledges operator return-mail limitation; no automatic paid path; event deduplication, ownership, crash recovery, exact input revision, outbox and rollback have concrete future tests.
- Current claims: the bundle consistently labels dispatcher/modules/events proposed and distinguishes installed-source capability from runtime-tested execution. This review did not independently rerun live Parley diagnostics; those claims are attributed to the separate captured audit. No unsupported media acceptance found.
- Domain limits: the baseline explicitly excludes semantic review of every historical file and full media playback; the plan does not claim the film is done. Parent's planned final validation/source-index/STATE pointer additions are not treated as missing deliverables in this interim review.

## Review disposition and successor

Producer should apply R1–R4 coherently to machine catalogue, derived package text and relevant diagrams/runbook, then request a focused read-only recheck of those changes. Existing scope controls, payment boundaries and final two-master acceptance must remain intact. Parent /root owns this revision task; no other actor was dispatched by this review.
