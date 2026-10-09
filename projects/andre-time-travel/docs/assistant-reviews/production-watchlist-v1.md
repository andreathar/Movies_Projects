# Production Watchlist v1 — The Table Between Centuries (`andre-time-travel`)

Date: 2026-10-09, 09:12–09:20 (UTC-3) · Author: producer-side assistant (read-only review) · Status: **REVIEW — no approval, task, manifest, ledger, memory, skill or art-director file was changed; no paid or external service was called; nothing staged or committed.**

All paths are relative to the workspace root `/mnt/data/Projects_SSD/Movies_Projects/` unless they start with `~/`. `P/` = `projects/andre-time-travel/`.

**Base state observed.** When I started, HEAD was `e0b2a31` and these were uncommitted: `P/memory/STATE.md`, `P/memory/session-log.json`, `skills/andre-time-travel/SKILL.md` (modified) and the art-director files (untracked). While I was reading, the art director's work was committed as **`7a38ebe`** ("refactor: add v2 English script proposal…", author `Andre Athar <andre@twlgames.com>`, 09:15:22). The commit contains exactly those 8 files. Hashes now: `STATE.md` 46e06ac0…, `session-log.json` 652d8715… (both match the handoff's `sha256After`), `SKILL.md` 1b648412…, handoff JSON 0bb12646…. The worktree is now clean except for this report.

**Checks run (read-only):** `manage.py status` and `manage.py validate` returned `ok` with 3 warnings (shared skills `film-character-continuity` and `film-dialogue-localization` changed since linking; source snapshots 18 and 19 missing). Unit tests: 10/10 OK, and the worktree was unchanged afterwards. I opened three images to check one claim (§4, I-13).

---

## 1. Whole picture (one page)

**Story.** Andre Athar, a real person and the user, sits at "his" table across from five people who do not know what came next: Caesar (Rome, early 44 BCE), Genghis Khan (campaign tent, 1227), Galileo (Arcetri, 1634), Napoleon (Saint Helena, 1816) and Oppenheimer (a fictional room near Trinity, 15 July 1945). The film runs about 240 s and is photorealistic. The historical figures never show a full face: eyes-only reactions and below-neck details are allowed. All dialogue is fictional, and factual anchors carry source IDs. There are two editions: all-English (E) and reviewed historical languages (H). Sources: `P/00_brief/brief.md`, `P/manifest.json` (`scope`), `P/docs/visual-contract.md`.

**Structure.** The film has 41 slots: an opening (IN-01..03, 12 s), five chapters of 7 slots each (42 s each, with the slot pattern 4/10/4/8/4/7/5) and an ending (OUT-01..03, 18 s). The slots sum to 240 s (`P/manifest.json` `chapterSlotSeconds`, `P/05_storyboard/shot-list.csv`, 41 rows). The script has 22 lines and 331 words, and all 22 have `approved=false` with no measured seconds (`P/01_script/dialogue-lines.csv`). Script v2 (`P/01_script/proposals/script-en-v2-proposal.md`) is a **proposal only**: it keeps the line IDs, cuts to 307 words, makes Napoleon the "hinge" and proposes unequal chapters.

**Pipeline stages** (`docs/REPEATABLE_WORKFLOW.md`, `series/andre-time-travel/FRAMEWORK.md` §5, `P/tasks/production-tasks.md`):
Brief → Script / fact-check → Decisions → Continuity (references, bibles) → Scratch track → Voice → Paid references → Element → Identity pilot → Speech route → Reforecast → Storyboard / animatic → Era and eye keyframes → Galileo first → the other four chapters → Opening/ending and English picture lock → Corrections → Edition H → QC and delivery.

**Who owns what.** Ownership comes from `agents/registry.json` and `P/agents/bindings.json`. No role is running (`activeProcesses: []`), and only the producer can submit paid jobs.

| Role | Tasks on the board (`P/tasks/board.json`) |
|---|---|
| producer | T01, T04, T10, T13–T17, T19 |
| continuity | T02, T03, T08 |
| historian | T05 |
| dialogue-sound | T06, T07, T09, T20 |
| storyboard | T11, T12 |
| editor | T18 |
| qc | T21 |
| art director | **not a registered role**. The handoff calls itself "art-director (review/proposal)" (`P/agents/handoffs/2026-10-09-art-director-review.json`). The session log says "not in registry". |
| Andre (human) | likeness, wardrobe, voice and script approval; the eight decisions in `P/docs/decision-sheet-andre-v1.md` |

**Gate status (all closed).**
- The nine creative flags are all `false`, `paidGenerationBatchApproved=false` and `externalAudioServiceBudgetApproved=false` (`P/00_brief/approvals.json`, mirrored in `P/manifest.json`).
- The only paid scope ever granted is `APR-R1-references-2026-10-09`, reference images with a 774-credit ceiling. It does not cover video, an Element, likeness approval or ElevenLabs purchases.
- The board has 3 tasks ready (T01, T02, T05) and 18 blocked. There are 0 takes, 0 video, 0 Elements, and `finalMovieVerified=false`. `P/06_pilot/`, `P/07_generations/accepted/`, `P/08_edit/*`, `P/05_storyboard/keyframes/*` and `P/05_storyboard/animatics/` are all empty.
- Money: the Kling snapshot of 7,741 (2026-10-08) became an observed **6,981 on 2026-10-09** after R1 reconciled at 760 credits, leaving 14 in the R1 phase cap (`P/manifest.json` `budget.referenceBatchAccounting`, `P/credit-ledger.csv` L001–L032). Neither figure is a live balance.
- About **480 ElevenLabs credits** were spent: VT-01 95.9904 (`P/04_audio/voice-tests/VT-01.json`) plus 383.9616 for the atlas tests (`P/manifest.json`).

**What exists.**
- 9 real photographs and 1 Kling render in `inbox/andre-reference-photos/`, plus 3 selected 2024 crops in `P/02_references/andre/selected/`.
- 32 R1 Kling jobs: Andre variants, 11 eyes-only crops, 5 costume fragments, 4 table anchors and 6 era plates.
- 12 R2 images with unverified provenance.
- Bibles written in "locked" language.
- Atlas v1 (79 cards) and a v2 rebuild.
- 5 English voice tests (none heard), 1 unregistered inbox voice file, 4 unreviewed translation drafts.
- **No failed clip.** `inbox/failed-clips/` contains only `.gitkeep`.

---

## 2. Critical path and what blocks each blocked task

### 2.1 Board critical path (dependency chain from `P/tasks/board.json`)

```
T02 ─► T03 ─► T04(+T01) ─► T08 ─► T09(+T07) ─► T10 ─► T11(+T05,T07) ─► T12 ─► T13 ─► T14..T17 ─► T18 ─► T19 ─► T20(+T06,T07) ─► T21
T05 ─► T06 ───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
T05 + T01 ─► T07
```

This is the longest chain: 14 sequential tasks. Every one of them sits behind **human decisions** (Andre's likeness, wardrobe and script) before the first paid step (T04 Element) can start.

### 2.2 The practical critical path (the art director's ordering, which I recommend; see §4, I-10)

1. Andre answers D1–D8 plus the items in §3 that the sheet misses.
2. The producer records the decisions using `shared/templates/review-decision.json`.
3. The historian runs T05 on the frozen script (v1 or v2), caches sources 18 and 19, and adds a surrender source.
4. Script v2 is integrated into `script-en.md` and the CSV together, if approved.
5. A **free local-TTS scratch** is recorded and measured, and a still animatic is cut. **No task ID exists for this step yet**; the board puts the animatic (T11) after T10.
6. Andre's photo session happens (T02 "six main photographs").
7. A new paid reference scope is approved (eye bases, table inserts, Andre keyframes).
8. T03 → T04 Element → T08 pilot → T09 speech route → T10 reforecast → T11/T12 → T13 Galileo → T14–T17 → T18 → T19 → T20 → T21.

### 2.3 What blocks each of the 18 blocked tasks

Every board `blocker` field holds the same generic string, "Awaiting dependency completion and applicable approval" (`P/tasks/board.json`). The concrete blockers below come from the specifications in `P/tasks/production-tasks.md` and the evidence cited.

| Task | Depends on | Concrete blocker today (evidence) |
|---|---|---|
| T03 Lock bibles | T02 | No wardrobe, grooming, table or gaze-axis decision (`P/docs/decision-sheet-andre-v1.md` D2–D4). The bibles assert "strictly invariant" and "Approved Expression Suite" while `characterReferences=false` (`P/03_bibles/character-andre.md` lines 23, 68). |
| T04 Andre Element | T01, T03 | Needs an approved photo set (D1/D8). Only 3 usable 2024 frontals; `P/02_references/andre/raw/` and `approved/` are empty. APR-R1 explicitly excludes "new Kling Element (T04)" (`P/00_brief/approvals.json`). T01 is not closed. |
| T06 Language targets | T05 | Script not frozen. 4 drafts exist, made from the unapproved v1 (`P/01_script/translations/*.md`, headed "unreviewed proposal"). No reviewer is named (`P/01_script/language-matrix.csv`, `reviewer` empty). The Napoleon target is undecided: Target A Corsican vs Target B French (`P/01_script/translations/corsican-napoleon.md`). |
| T07 Voice samples | T01, T05 | 0 of 5 renders heard (`VT-01.json` `approved:false`; `P/04_audio/voice-tests/codex-opening-v1/provenance.json` `audioQualityReviewed:false`). The voice is labelled `pt / pt-brazilian` but used for English. The inbox MP3 is unlabelled and unregistered. No ElevenLabs scope (`externalAudioServiceBudgetApproved=false`). |
| T08 Identity pilot | T03, T04 | No Element, no approved references, no pilot spending scope. The Phase A cap is 1,161 but unreleased (`P/manifest.json` `phaseCaps`). |
| T09 Speech route | T07, T08 | No route has been proven. The Kling external-audio input is unverified, and ElevenLabs Sync is untested and unfunded (`P/01_script/language-strategy.md` "ElevenLabs and lip-sync are separate gates"). |
| T10 Reforecast | T08, T09 | No pilot charges exist to forecast from (`P/docs/production-plan.md` §9 "Forecast after the pilot"). |
| T11 Storyboard / animatic | T05, T07, T10 | No measured audio. The atlas is a reference collage, not keyframes (`P/05_storyboard/preproduction-atlas-v1/documents/review-findings.md` #5). `P/05_storyboard/animatics/` is empty. |
| T12 Era and eye keyframes | T03, T08, T11 | No single eye identity per figure (review-findings #2; decision D5). 0 of 15 missing-keyframe briefs funded (`…/documents/next-image-batch.md`). `P/05_storyboard/keyframes/*` is empty. |
| T13 Galileo chapter | T09, T10, T12 | Everything above, plus no batch approval (`paidBatch=false`). |
| T14 Caesar | T13 | The Galileo recipe has not been validated. |
| T15 Genghis Khan | T13 | Same, plus the ger plate seats the Khan on a Chinese-style chair (`P/docs/art-direction-review-v1.md` §3.2). |
| T16 Napoleon | T13 | Same, plus the language target and the ring and hand-in-waistcoat props are undecided (review-findings #4). |
| T17 Oppenheimer | T13 | Same, plus the factual anchors 18 and 19 (Hiroshima, Nagasaki) are uncached, and the scene bible names a "Lucky Strike" brand and a stamped "TRINITY TEST DATA" prop (art-direction review C5). |
| T18 Opening/ending, English picture lock | T13–T17 | No takes. The ending line is weak, and v2 rewrites it (OUT-L01). |
| T19 Correction reserve | T18 | Nothing to correct yet. The reserve phases D (1,935) and E (388) are planned against the 7,741 snapshot, not the 6,981 observed. |
| T20 Edition H | T06, T07, T19 | No reviewed language, no lip-sync route, no subtitles. |
| T21 Masters and QC | T19, T20 | No masters. The checklist commands point to the non-existent `/mnt/data/Projects_SSD/Andre_Time_Travel/09_delivery/` (`P/docs/acceptance-checklist.md` lines 45–47). |

The three ready tasks are open for these reasons:
- **T01**: the ElevenLabs and other-service scope was never recorded. The task spec says "Record the user's separate ElevenLabs/other-service spending scope".
- **T02**: there is no Andre-approved photo packet, and the failed clip or generation ID is missing (`inbox/failed-clips/` is empty).
- **T05**: untouched. It is now ambiguous whether it applies to v1 or v2.

---

## 3. Decisions still pending (prioritized, with a recommended default)

The defaults are proposals. None of them is approved.

### Priority 0 — these unblock T02, T03, T05, T07 (Andre; prepared in `P/docs/decision-sheet-andre-v1.md`)

| # | Decision | Evidence | Recommended default |
|---|---|---|---|
| D1 | Identity photo set | `P/02_references/andre/selected/crop34_20240202_*.jpg`. The 2021–23 photos predate the current grooming (`P/asset-registry.csv`, real_photograph rows). | **C, then A.** Shoot the new session (D8). Until then the three 2024 frontals are the only identity truth. Never use R2 or R1 synthetics as identity evidence. |
| D2 | Wardrobe canon | The 2024 photo shows a grey blazer and pinstripe shirt. The synthetics show navy and charcoal (`P/docs/art-direction-review-v1.md` C1). The inbox Kling render is registered as a "wardrobe style reference (… navy jacket …)" (`P/asset-registry.csv` `andre-kling-render-20261008`), which nudges the choice toward B. | Andre's free choice. **Whichever he wears at the D8 shoot becomes the canon.** If undecided, take A, since the photos already prove it. |
| D3 | Hair and beard canon | AD §3.1. `STATE.md` notes that J07 take 2's hair drifts. | **A (as photographed).** Real photos must match the Element. |
| D4 | Table anchor and the "table travels with Andre" rule | AD C3/C4. Bible line 5 calls it a "timeless medium". | **B** (`P/02_references/table/R1-J26-table-anchor_2.png`, already used in the keyframe briefs), and **yes** to the rule. Match cuts happen on the insert, not the wide shot. |
| D5 | One eye base per figure | `P/02_references/_review/historical-eyes_contact.jpg`. Review-findings #2. | Pick the tile whose gaze matches the camera-left screen axis (visual contract §Andre 5). Drop Caesar's reversed option. Fix the Oppenheimer lower-lid trim (`STATE.md`). |
| D6 | Voice | 5 renders plus the inbox file. The voice is labelled pt-BR (`VT-01.json`). | Listen before any further ElevenLabs spend. If the accent is unacceptable for Edition E, record **that** decision rather than rendering more variants. |
| D7 | Script v2 (N-L03 hinge, O-L04 "I can't tell you that.", unequal chapters) | `P/01_script/proposals/script-en-v2-proposal.md` | **B: approve v2 for the historian and the scratch track, with notes.** Lock the time allocation only after the scratch (see I-15). |
| D8 | Photo session commitment | Decision sheet D8; `P/docs/reference-intake.md` | **A** with a date. It is the cheapest identity improvement available. |

### Priority 1 — missing from the decision sheet but blocking soon

| # | Decision | Evidence | Recommended default |
|---|---|---|---|
| X1 | **Screen and gaze axis** (Andre looks camera-right; the figures' eyes look camera-left) | The rule is in `P/docs/visual-contract.md` and `P/03_bibles/character-andre.md`. The assets disagree (AD C2). | Keep the written rule. Make it a checked field for every new reference and keyframe. |
| X2 | **New paid reference scope** | APR-R1 has 14 credits left (`P/manifest.json`). The AD's P1-2/P1-3/P1-4 asks for about 10 eye images, 5 inserts and 10 Andre keyframes. The plan's phase B release condition is "Pilot passes", but R1 already drew phase B before any pilot (`P/docs/production-plan.md` §9). | Write a new, narrow approval with an explicit image list after D1–D5. Refresh the balance through the CLI first. Decide whether it draws on phase A or a re-labelled phase B. Do not treat the whole-film ceiling (`P/memory/decisions.json` D03) as batch approval. |
| X3 | **ElevenLabs scope** (T01) | About 480 credits spent. `externalAudioServiceBudgetApproved=false`. APR-R1 covered "small ElevenLabs test lines" only. | **No further ElevenLabs spend until script freeze and the scratch track.** Use free local TTS for timing. Record the scope explicitly to close T01. |
| X4 | **Napoleon language target** (T06) | `corsican-napoleon.md` offers A (Corsican) and B (French). STATE.md and the strategy forbid silently using French. | Corsican or Tuscan-rooted per the brief. Defer until the English script is frozen and a reviewer is named. |
| X5 | **Edition H: go, or defer** | `P/01_script/language-matrix.csv`: every row unverified, no reviewer. | Explicitly **defer H behind Edition E picture lock**, and say so in the manifest notes so that E is never blocked on H. |
| X6 | **The failed clip** | Required by T02. `inbox/failed-clips/` is empty. | Andre either supplies the clip or generation ID, or declares it unrecoverable in writing ("cause unresolved") so that T02 can close. |
| X7 | **R2 images as a category** (12 files) | Registered as "generation route reported by another session, not verified" (`P/asset-registry.csv` LOCAL-R2-*). The AD calls R2 the weakest provenance with the heaviest weight in the bible. | Mark them **style/tonal reference only**, never identity or continuity anchors, until a provider and job record is found. |
| X8 | **Props and costume details** (Napoleon's rings and hand-in-waistcoat; Genghis's ring and silk; readable manuscript, brand and stamp) | Review-findings #4; AD C5 | Remove brands and readable text. Allow one ring per figure at most. Keep the hand-in-waistcoat only if Andre wants the icon. |
| X9 | **Treating full-frame eye originals** | AD C9/P0-3 proposes *moving* them into `_quarantine-full-face/`. AGENTS.md says to preserve originals and never move legacy items silently. | Do **not** move them without Andre's explicit OK. A registry flag `contract_unsafe_full_frame` plus a README in `P/07_generations/originals/` achieves the same hygiene. See I-13 for what they actually show. |
| X10 | **A creative-decision role** | AD W8; `agents/registry.json` has no director or art-director role. | The producer adds a non-spending `director` role, or records that Andre holds it. |
| X11 | **Re-sequence the board** (scratch animatic and read-only speech-route discovery before paid references) | FRAMEWORK §5 phase 4 and `skills/andre-time-travel/SKILL.md` (new section) conflict with T11 depending on T10. | The producer adds a scratch/animatic task with a new ID, or records that T11 has a pre-pilot draft phase. Do not invent the ID here. |
| X12 | **Accept or revert the shared-skill edits and re-hash `skills/registry.json`** | See I-2 | Producer review of the two global skill diffs, then update `sourceSha256`, or ask the owner to revert. |
| X13 | **Link FRAMEWORK.md in `series/andre-time-travel/series.json`** | The handoff's pendingDecisions; series.json has no reference to it. | Link it as `framework`, with status "proposal". |
| X14 | **Label the inbox Kling render "composition forbidden — style/tone only"** | AD C7; its `P/asset-registry.csv` note does not include that label. | Yes. |

---

## 4. Inconsistencies found

| # | Inconsistency | Evidence | Severity / suggested owner |
|---|---|---|---|
| I-1 | **`skills/andre-time-travel/SKILL.md` was edited (+3 lines, "Art direction and episode grammar") but is missing from the AD handoff's `changedFiles` and `ownedPaths` and from the session-log entry.** It is now committed in `7a38ebe`. The new text also mixes path bases: `projects/andre-time-travel/docs/art-direction-review-v1.md` (workspace-rooted) next to `docs/decision-sheet-andre-v1.md` (project-rooted), and a workspace `docs/decision-sheet-andre-v1.md` does not exist. | `git show 7a38ebe -- skills/andre-time-travel/SKILL.md`; `P/agents/handoffs/2026-10-09-art-director-review.json`; `P/memory/session-log.json` last entry | Medium. Producer/AD: amend the handoff and fix the path. |
| I-2 | **Two global profile skills were rewritten at 09:06:58–59** (`~/.hermes/skills/creative/film-character-continuity/SKILL.md` plus a new `references/preproduction-audit.md`, and `~/.hermes/skills/creative/film-dialogue-localization/SKILL.md`). This is about 90 s after the AD's handoff timestamp (09:05:23). The content echoes the AD review (decision sheet, free local-TTS scratch, "speech-route discovery scheduled late"). No handoff records it, and `skills/registry.json` hashes are now stale, which produces the two new validate warnings. AGENTS.md: "do not copy vendor/profile skills here" and "store project state in local film memory, not global user memory". I cannot prove who made the edit; the timing and content point to the same session. | `manage.py validate` warnings; `stat` mtimes; `skills/registry.json` `sourceSha256`; grep hits in those files | **High.** Unrecorded writes outside the workspace. The producer reviews and either re-hashes or reverts (X12). |
| I-3 | The AD handoff's `verification` says validate warnings are only "uncached sources 18,19". That was true before I-2 and is stale now, but it was committed that way. | Handoff line 56 vs. the current `manage.py validate` | Low. Note it in the next handoff. |
| I-4 | **Sources 18 and 19 are the Hiroshima and Nagasaki pages**, the only anchors for O-L02 in both v1 and v2. They have `snapshotStatus: not_found_in_current_cache` and empty titles. In addition, **0 of 19 sources are `evidenceValidated`**. Source 4 is a children's timeline ("…for 6 years old") used for Napoleon. Sources 6, 7 and 11 are vendor docs, not history. v2 adds "The war ends that summer [NEEDS SOURCE]". | `P/00_brief/research/source-registry.json`; v2 proposal, O factual note | **High for T05.** The historian caches 18 and 19, validates the evidence, and adds a surrender source and a stronger Napoleon source. |
| I-5 | **`P/asset-registry.csv` is malformed: 43 R1 rows have 6 fields instead of 8.** The provider/sha text lands in `path_base`, "false" in `source`, the notes in `sha256`, and `approved`/`notes` are missing. `manage.py validate` does not detect this. | Python `csv.reader` count: (6, synthetic_andre_variant) 17, costume 5, eyes 11, table/plate 10 | **High for tooling.** Any script that reads `approved` from these rows gets nothing. Producer fix in a new revision. |
| I-6 | **Double registration of the 10 inbox images** as `andre-photo-*`/`andre-kling-render-*` and as `candidate-*`. The `andre-photo-*` rows use `../../inbox/...` with `path_base=workspace` (which escapes the workspace) and an empty `sha256` column (the hash sits in `source`). | `P/asset-registry.csv` rows 4–23 | Medium |
| I-7 | **Unregistered media:** the 3 selected crops (`P/02_references/andre/selected/crop34_*`), `VT-01_athar_multilingual-v2_en_IN-L01.mp3`, the inbox voice MP3, the 6 review contact sheets, and the 07_generations/originals full frames (including the eye strips). | `grep` count of 0 in `P/asset-registry.csv` for each | Medium. Producer. |
| I-8 | **ElevenLabs accounting is split:** 95.9904 (VT-01, in `STATE.md` and `VT-01.json`) plus 383.9616 (manifest) = 479.952. `P/credit-ledger.csv` has no ElevenLabs rows, and `P/manifest.json` budget lists only the 383.96. `externalAudioServiceBudgetApproved=false` while APR-R1 included "small ElevenLabs test lines". | Files cited | Medium. Close it together with X3. |
| I-9 | **The phase plan is not reconciled.** Phase caps still sum to the 7,741 snapshot (`P/manifest.json` `phaseCaps`), not the 6,981 observed. Phase B was spent before Phase A, against the plan's release condition. `manage.py status` reports `budgetCeiling: 7741`. | `P/docs/production-plan.md` §9; `P/manifest.json` | Medium. Fix at the T10 reforecast; flag it now. |
| I-10 | **The board's order contradicts the new framework and skill.** FRAMEWORK §5 and SKILL.md say "cut a free local-TTS scratch before any paid audio or picture", but on the board the animatic (T11) depends on T10 (after pilot and reforecast), and no scratch task exists. Likewise, speech-route discovery is pulled forward in FRAMEWORK but remains behind T08 on the board (T09). | `P/tasks/board.json`; `series/andre-time-travel/FRAMEWORK.md` §5; `skills/andre-time-travel/SKILL.md` | **High (process).** The producer re-sequences (X11). |
| I-11 | **The board's deliverables point at derived atlas files instead of each task's spec outputs.** T02 points to `review-findings.md`, but the spec requires `02_references/andre/raw/` and the asset registry, and `raw/` is empty while the photos sit in `inbox/`. T05 points to the derived `director-script-en.md` instead of the canonical `script-en.md` and CSV (AD C10). T01 stays "ready" although the brief and approvals files exist; the real open item is the ElevenLabs scope. | `P/tasks/board.json`; `P/tasks/production-tasks.md` | Low/medium |
| I-12 | **`STATE.md` has a stale "Next actions"** section (T01/T02/T05 only), which contradicts its own last section (decision sheet → historian on v2 → scratch). The "Current state" paragraph also lists "manage.py/.venv tooling exists" as *Open*. The session log has no event for the R1 paid run itself (32 jobs, 760 credits), for VT-01 or for the R2 generation; they appear only indirectly. Timestamps mix UTC and −03:00. | `P/memory/STATE.md` lines 1–17, 70–72; `P/memory/session-log.json` | Low. Producer, next memory update. |
| I-13 | **AD C9 overstates the problem.** It says "Uncropped full-face originals … (J11–J20, plus rejected J10)". I opened J11_1, J19_1 and the rejected J10_1. They are 4128×1024 eye strips that also show the nose bridge, cheeks, ear and hat brim, **not full faces**. They still exceed the brow-to-lower-lid contract, and by the project's own J10 rejection standard ("nose/beard/ear visible (full-face violation)", `P/07_generations/rejected/R1-J10-eyes-caesar-command.reason.txt`) they would fail. So the hygiene concern stands; only the label is wrong. Moving the files is a separate decision (X9). | Files cited; `PIL` sizes | Medium. Correct the wording in any bible or handoff that says "full-face". |
| I-14 | The acceptance checklist uses the non-existent `/mnt/data/Projects_SSD/Andre_Time_Travel/09_delivery/` (inherited from `docs/archive/production-plan-2026-10-08.md`). Confirmed (AD C8). | `P/docs/acceptance-checklist.md` lines 45–47 | Low. Fix before T21. |
| I-15 | **The v2 timing math doesn't add up.** v2's chapter headings sum to 12+40+42+42+32+48+22 = **238 s**, but its own note moves 10 s from Napoleon to Oppenheimer (+6) and the ending (+4), which keeps Caesar at 42 and gives **240 s**. The decision sheet asks for N 32 / O 48 / OUT 22 without Caesar's value. The manifest still says 42 per chapter and 18 for the ending. | v2 proposal (headings and "Timing note"); `P/manifest.json` `chapterSeconds`/`endingSeconds` | Low. Resolve after the scratch track. |
| I-16 | **Bibles assert approvals that don't exist** (AD C1/W2, confirmed). `character-andre.md` says "Status: Visual identity foundation established", "strictly invariant" and "Approved Expression Suite". The table bible says "identical across all eras" while the plates differ in axis. | `P/03_bibles/character-andre.md` lines 6, 23, 68; `P/03_bibles/table-and-continuity.md` | Medium. Continuity, bibles v2 "PROPOSED". |
| I-17 | **The brief and v2 disagree on Napoleon's eye beat.** The brief says "Self-possession → wounded pride → reflection"; v2 says B is "not wounded pride — attention". Also, `STATE.md` describes the translation as "Corsican/French", while the strategy forbids silently using French; the file offers French as Target B. | `P/00_brief/brief.md` table; v2 N section; `P/01_script/translations/corsican-napoleon.md` | Low. Settle via D7 and X4. |
| I-18 | The AD role is unregistered but owns committed files. `series.json` is not linked to FRAMEWORK.md (the handoff lists this as producer work). | `agents/registry.json`; `series/andre-time-travel/series.json` | Low (X10, X13) |
| I-19 | **The commit `7a38ebe` was authored as the user** ("Andre Athar") with the message "refactor: …". I can't tell whether the user or an agent ran it. AGENTS.md says agents must not commit silently and that a commit is not approval. It contains proposal files only; no approval files changed. | `git log -1 7a38ebe` | Info. The producer confirms who committed. |

---

## 5. Risks

| Area | Risk | Evidence | Mitigation |
|---|---|---|---|
| **Budget** | 7,741 is a 2026-10-08 snapshot. The 6,981 from 2026-10-09 is not live either. Per-row ledger deltas are approximate (J01: 2 images for 20 credits; J02: 2 images for 40). 30 credits went to the rejected J10. The remaining APR-R1 allowance (14) is effectively zero. A whole-film ceiling (`P/memory/decisions.json` D03) could be misread as batch approval. ElevenLabs has its own unscoped spend of about 480. | `P/manifest.json`; `P/credit-ledger.csv`; `P/00_brief/approvals.json` | Refresh through the CLI before any paid step. Each new phase gets its own APR with an explicit list. Forecast from pilot charges (T10). Add ElevenLabs rows to the ledger. |
| **Likeness** | The look is undecided: the synthetic canon differs from the 2024 photos. R2 anchors have no provider IDs but carry the most weight in the bible. Gaze is uncontrolled. Only 3 frontal photos exist; there are no real profiles or seated shots. | AD §3.1; `P/asset-registry.csv` LOCAL-R2-*; STATE.md "Open" | D1–D3, D8 before the Element. Only real photos count as identity. Andre's written approval for every face-bearing shot (FRAMEWORK §8.5). |
| **Historical-face rule** | Eye-strip originals exceed the crop (I-13). Prop-reflection risk in an Oppenheimer room full of glass and metal. Background portraits, silhouettes, pull-backs. The inbox render is an over-the-shoulder two-shot (C7). The ger plate composition. | Visual contract §figures 4; `P/docs/risks-and-shortcuts.md` "Sampling a few frames" | Flag or segregate the originals (X9). Frame-by-frame review of every restricted shot. Label the render "composition forbidden". |
| **Language review** | Four translations were drafted from an unfrozen script, so any v2 change invalidates them. No reviewer exists. Provider support for Latin and Middle Mongol is unverified. IPA is not validation. The Napoleon target is open. | `P/01_script/language-matrix.csv`; translation headers; STATE.md "Do not approve historical language fidelity from IPA notation alone" | Freeze the English script first, then name reviewers, then run a short pronunciation test. Explicitly defer H (X5). Mark the drafts `superseded_by` if v2 is adopted. |
| **Voice** | The clone is labelled pt-BR and used for English. Five renders have never been heard. The provenance of the inbox file is unknown. | `VT-01.json`; decision sheet D6 | Listen first (D6). Use a free local scratch for timing. |
| **Inbox references not approved** | All 10 images are `approved=false` and pending classification. The Kling render is marked synthetic but recommended for "wardrobe" style. Two legacy Kling Elements (323415933655261, 323336237505580) are hygiene risks. | `P/asset-registry.csv`; `P/docs/reference-intake.md` | No inbox file is used as a reference until it has a decision record. Leave the legacy Elements untouched and unused. |
| **Failed-clip analysis** | It cannot happen: no clip or generation ID was ever delivered. The "reference contamination" theory is explicitly unproven. | `inbox/failed-clips/` (only `.gitkeep`); STATE.md "Known risks" | X6: supply it, or close it as unrecoverable. Don't spend on a speculative repair (`P/docs/reference-intake.md`). |
| **Speech route** | This is the biggest technical unknown and it is scheduled late (T09 after T08). | AD W4; `P/01_script/language-strategy.md` | Read-only capability discovery now (no spend). The L/J-cut fallback needs a directing decision. |
| **Concurrency and integrity** | Two agents share one checkout. Unrecorded writes went outside the workspace (I-2). The committed handoff is stale (I-1, I-3). The asset registry is malformed (I-5). | §4 | Coordinate file ownership before the next edit. Re-hash. Producer-owned registry repair. |
| **Fact risk** | O-L02 depends on uncached sources 18 and 19. v2 adds an unsourced surrender claim. No source has been validated. | I-4 | T05 must cover v2 claim by claim. |

---

## 6. Recommended next 5 actions (zero spend, ordered)

1. **Andre's decision session (about 15 minutes):** answer D1–D8 in `P/docs/decision-sheet-andre-v1.md`, plus X1 (gaze axis), X3 (no more ElevenLabs for now), X5 (defer Edition H) and X6 (failed clip: supply it or close it). The producer records each answer with `shared/templates/review-decision.json`, including file, hash and scope. This is the gate for T02, T03, T05 and T07.
2. **Producer integrity pass** in a new revision, without overwriting history, coordinating with the art director first:
   - repair the 43 malformed rows and the double inbox registration in `P/asset-registry.csv` (I-5, I-6);
   - register the missing media (I-7);
   - add ElevenLabs rows to the ledger (I-8);
   - review the global skill edits, then re-hash `skills/registry.json` (I-2, X12);
   - amend the handoff for SKILL.md (I-1);
   - fix the checklist path (I-14);
   - label the inbox render (X14).
3. **Historian T05 on the chosen script (v2 if D7 = A or B):** cache sources 18 and 19, set `evidenceValidated`, add a surrender source and a stronger Napoleon source, and produce a claim-by-claim table (I-4).
4. **Producer re-sequences the board:** add a scratch/animatic task and a read-only speech-route discovery step before any paid reference, replace the generic `blocker` strings with the concrete blockers in §2.3, and update STATE.md "Next actions" (I-10, I-11, I-12). Then the dialogue-sound role records a **free local-TTS scratch** of all 22 lines and fills `measured_seconds`, and the editor makes a still animatic to settle the chapter allocation (I-15).
5. **Only after 1–4:** refresh the Kling balance through the CLI and draft (do not submit) a new narrow paid-reference approval covering eye bases, the 5 table inserts and Andre keyframes in the decided look, as an explicit image list with a ceiling (X2). Andre's photo session (D8) happens in parallel and feeds T04.

---

## 7. Addendum — concurrent integration observed 09:17–09:20 (read-only; not yet committed)

Right after §1–§6 were written against `7a38ebe` and a clean tree, `git status` showed a large **uncommitted** integration in progress by another session, most likely the director/art director. In outline, `git diff --stat` covers 22 tracked files with +374/−315 lines, plus 22 staged renames. **Parts of §2–§4 are therefore partly superseded and should be re-read against the final commit.** Facts observed:

| Change | Evidence | Watch point |
|---|---|---|
| **New approval `APR-blanket-2026-10-09`** ("delegated_decision_authority", quoted as *"you are perfectionist and you make the budget,tools and subagents decisions. i aprove all"*). It excludes Andre's own pilot likeness approval, voice selection by ear, and purchases. | `git diff P/00_brief/approvals.json` | **I cannot verify this quote.** It is not in any file I read before 09:17. The producer/user should confirm that it is Andre's words and that he intends it to cover *personal* canon choices (wardrobe, grooming). The creative boolean flags are unchanged. |
| **Decision records D01–D10** written at 09:18:43, all with reviewer "Andre Athar (blanket authorization) executed by director/producer agent". D01: the 2024 photos are the identity set. **D02: wardrobe B, navy/charcoal.** D03: grooming A (2024). D04: table `_2` plus the travel rule. D05: eye bases (Caesar tile 1, Genghis 4, Galileo 6, Oppenheimer 10, **Napoleon recast**). D06: voice provisional. D07: v2 integrated into the canonical script. D08: photo session required from Andre. D09: screen axis. D10: timing deferred. | `P/00_brief/decisions/D01…D10*.json`. The D01 artifact hash ea0d9f2b… matches the file on disk. | **D02's artifact is `R2-wardrobe-andre-modern.jpg`, an R2 image with unverified provenance, which D01 itself downgrades to "tone/style reference".** D02 also pairs a synthetic wardrobe with real-photo grooming (D03), and asks Andre to own and wear that outfit. These are personal-likeness choices; I recommend Andre confirm D02 and D03 explicitly (they map to my D2/D3). D09 resolves my X1. D10 matches my I-15 recommendation. |
| **The canonical script and CSV were changed to v2 before T05** (e.g. IN-L01 now uses an em dash). The four translations and the bibles were edited, and `reports/art-direction-v1/script-en-v1-before.md` was saved. | `git diff P/01_script/dialogue-lines.csv`; diff stat | The order differs from FRAMEWORK §3 ("historian pass on the **frozen** script before any translation or recording"). `screenplay` stays false per D07. The historian must still cover I-4 (sources 18 and 19, surrender source). Rebuild the atlas as v3 (v1/v2 stay untouched). |
| **22 eye-strip originals (J11–J20 PNG and JSON) staged as renames into `P/07_generations/originals/_quarantine-full-face/`**, with a README. | `git diff --cached --stat` | This executes my X9 under the blanket authority. Bytes are preserved (0 insertions/deletions). The folder name repeats the overstated "full-face" label (I-13): they are eye strips that also show nose, cheek and ear. Check that `asset-registry.csv` and any atlas `build-inputs.json` paths still resolve. Delivered atlases v1/v2 must not be rebuilt in place. |
| **Scratch audio** `P/04_audio/scratch/edge-tts-v2/*.mp3` created at 09:19–09:20. | Directory listing | **`edge-tts` is not local TTS. It sends the text to Microsoft's online speech service.** It is free, but script text leaves the machine, which differs from the "free *local* TTS" wording in FRAMEWORK/SKILL.md/D06. The producer should record this as an external-service use, or switch to an offline engine. It is scratch timing only, not a voice approval. |
| `agents/registry.json` gains a `director` role (no paid authority, `creativeDecisionAuthority: true`); `agents/director.md` is new. `series.json` now links `framework`. The acceptance checklist and production plan were edited, and the `inbox/…/README-kling_20261008_IMAGE.md` label was added. | Diff and untracked list | These resolve X10, X13, X14 and probably I-14 and I-18 (re-verify after the commit). |
| D05/D08 state that **"eye bases and table inserts proceed"** before the photo session. | D05, D08 | This implies an upcoming **paid** Kling batch. Before any submission: refresh the live balance through the CLI, write a per-batch scope record with an explicit image list and ceiling (my X2), producer-only submission, no retries. The 14 credits left in APR-R1 do not cover it. |

Still open after this integration, as far as can be seen without the final commit: I-2 (global skill edits / registry hashes), I-4 (sources 18 and 19), I-5/I-6/I-7 (registry malformation and gaps; `asset-registry.csv` is among the modified files, so re-check it), I-8 (ElevenLabs accounting), I-10 (board sequencing; `board.json` was **not** modified), I-12 (STATE.md "Next actions"), X3 (ElevenLabs scope), X5 (Edition H), X6 (failed clip), and Andre's own listening (D6) and photo session (D8).

---

*This watchlist is a review document. It changes no gate, grants no approval and invents no task ID; X1–X14 and I-1–I-19 are labels local to this file.*
