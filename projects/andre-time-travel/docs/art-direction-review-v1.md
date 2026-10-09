# Art Direction Review v1 — The Table Between Centuries

Date: 2026-10-09 · Role: art director (review/proposal only) · Status: **PROPOSED — no approval state changed, no paid job submitted**

Scope: everything in `projects/andre-time-travel/`, `inbox/`, `series/`, `docs/`, read in full; all six contact sheets, the R2 master still, one real 2024 photo, the user's Kling render and one shot card inspected with vision. Workspace `manage.py status/validate` and 10 unit tests pass. Git clean at `e0b2a31`.

Legend: **[E]** evidence-based finding (file/observation cited) · **[R]** recommendation.

---

## 1. Inventory

### 1.1 Present (counts verified by script)

| Area | What exists | State |
|---|---|---|
| Brief / research | `00_brief/brief.md`, 19 registered sources, 17 cached snapshots | Sources 18, 19 uncached (manage.py warning) |
| Script | `01_script/script-en.md` + `dialogue-lines.csv`: 22 lines, 331 words, stable IDs | `approved=false` on all 22; 0 measured durations |
| Language | `language-strategy.md`, 4 translation drafts (Latin, Middle Mongol, Tuscan, Corsican) with IPA | All headed "unreviewed proposal"; produced **before** EN script approval |
| Andre references | 9 real photos (2021–2024, SHA-256 recorded) + user Kling render; 3 selected 3/4 crops (2024); 21 R1 synthetic PNG (J01–J09); 4 R2 synthetic JPG | None approved. R1 has job IDs/charges; R2 has **no provider IDs** (STATE.md: "not independently proven") |
| Historical figures | 11 eyes crops (5 figures), 5 R1 + 5 R2 below-neck wardrobe, 6 contact sheets | Compliant crops; pairs inconsistent (see 3.2) |
| Table / plates | 4 table anchors (J26), 6 R1 era plates (J27–J32), 2 R2 plates | Anchors consistent; plates not match-cut-safe (see 3.3) |
| Bibles | `character-andre.md`, `table-and-continuity.md`, 5 scene bibles, `continuity-matrix.csv` | Written in "locked" voice while approvals are false (see 1.3) |
| Audio | VT-01 (7.15 s) + 4 codex refs (6.9–8.4 s), all line IN-L01, Athar PVC voice, `eleven_multilingual_v2`; 1 inbox MP3 (23.8 s) | 0 of 5 listened/approved; inbox file **unregistered**, content unknown |
| Storyboard | 41 shots / 240 s, atlas v1 (79 cards, 3 PDFs) + v2 rebuild, editable `source/atlas.json`, 15 keyframe briefs | Atlas is reference-collage, not keyframes; approved=false |
| Governance | manifest, board (21 tasks: 3 ready / 18 blocked), approvals (9× false), 7 role briefs, ledger (R1: 760/774 cap; balance 6,981 observed 2026-10-09), git (2 commits) | Sound. 0 takes, 0 video, 0 Elements, `06_pilot/08_edit/09_delivery` empty |

### 1.2 Missing

1. **Andre's decisions** — likeness set, wardrobe, grooming canon, table tile, one eye base per figure, voice pick, script sign-off. Everything downstream (18 tasks) is blocked on this. No single decision document exists; the asks are scattered across STATE.md, review-findings and bibles. **[E]**
2. Real photographs for profiles, neutral front, seated — only three usable 2024 frontals; the 2021–2023 photos predate the current grooming. **[E]** (STATE.md, character-andre ledger)
3. Era-specific Andre keyframes: 0 of 10; historical hand/table inserts: 0 of 5. **[E]** (next-image-batch.md)
4. Production Element, identity pilot, speech-route proof, measured audio for 21 of 22 lines, any scratch animatic. **[E]**
5. Historian sign-off (T05 ready, untouched); qualified language reviewers (T06). **[E]**
6. Provenance for the inbox voice file and for all R2 images. **[E]**

### 1.3 Contradictions (must be resolved before more spend)

| # | Contradiction | Evidence |
|---|---|---|
| C1 | `character-andre.md` declares wardrobe "strictly invariant" (navy blazer / charcoal shirt) and calls R1-J02…J09 the "Approved Expression Suite" | `approvals.json` characterReferences=false; `review-findings.md` §1 "costume not locked"; real 2024 photo shows **grey blazer, white pinstripe shirt, shorter textured hair** — the synthetic canon is a stylistic departure Andre has not chosen |
| C2 | Screen-axis rule "Andre screen-left, looking camera-right" | Cited master anchor `R2-andre-table-cinematic.jpg`: subject **right of centre**. Seated suite: 2 tiles gaze camera-left, 3 to-camera, 1 camera-right. Close-ups mixed. The rule and the assets disagree |
| C3 | Table bible: grain, edge, torso-to-edge distance "identical across all eras" | Era plates: Trinity and present-day are shot **end-on along the long axis**, the other four corner-diagonal; tone varies warm→grey; edge damage not matched. Table anchors (J26 ×4) **are** consistent (ring stain + near-corner chip) |
| C4 | Table bible calls the table a "timeless medium across five centuries" | Every era plate carries the **same ring stain**, including Rome 44 BCE → the imagery says *the table is Andre's and travels with him*. The bible never states which reading is intended |
| C5 | Table bible: "pack of unfiltered cigarettes", review-findings: no readable invented writing | Oppenheimer scene bible: "Lucky Strike", notebook "stamped TRINITY TEST DATA"; Galileo bible: *Dialogo* manuscript sheets; Galileo costume image contains generated writing |
| C6 | Visual contract: "each figure has an approved eyes reference… two restrained emotion states" | Eye pairs change identity between states (Genghis brow colour/age, Galileo iris hue/scale, Oppenheimer brow/gaze, Caesar option 2 reverses direction). Age plausibility in the brief's own terms: Napoleon pair reads younger/fairer than 47; Genghis state A reads ~50 vs ~65 in 1227 |
| C7 | Visual contract forbids reverse/over-shoulder two-shots | The user's own Kling render in the inbox **is** an OTS two-shot with a second head in foreground — it is filed as "style reference" without a "composition forbidden" label |
| C8 | `acceptance-checklist.md` verification commands | Point to `/mnt/data/Projects_SSD/Andre_Time_Travel/09_delivery/` — path does not exist; real path is `projects/andre-time-travel/09_delivery/` |
| C9 | Reference hygiene rule (no contamination) | Uncropped **full-face** originals of synthetic historical figures (J11–J20, plus rejected J10) sit in `07_generations/originals/` next to production references |
| C10 | Four sources of truth for the script | `script-en.md`, `production-plan.md §6`, `master_production_visual_bible.md §6`, atlas `director-script-en.md` — only the first + CSV are canonical per START_HERE, but the others are not marked derived |

---

## 2. Story analysis

**Premise [E]:** strong and specific. One traveller, one table, five people who do not know what comes next. Logline is clean. The decision to keep the mechanism unexplained is right for four minutes.

**Time-travel logic [E/R]:** the only logic the film needs is *what is constant*. The imagery already answers it (C4): the table is Andre's and comes with him. **[R]** State it in the bible, and let the opening prove it (his hand on the ring stain in the present → the same stain in Rome). Nothing else needs explaining; the figures accept him because the film's grammar does.

**Andre's motivation [E]:** IN-L01 states it well ("what it felt like to hear what came next"). **Problem:** the ending ("I came back with a question for us") is a pivot that nothing at the table triggers. No figure ever asks Andre about *his* time. The turn inward is asserted, not earned.

**Andre's arc [E]:** flat. His five answers have the same confidence, the same length (16–30 words), the same shape. The script's best moment — O-L04, Andre unable to answer — is the climax, but nothing erodes him on the way there.

**Structure / repetition [E]:** five chapters × one template: *legacy question → "yes, but…" → label question → "they argue" + aphorism*. "argue" appears 4× (C-L04, K-L04, N-L04, O-L02). Napoleon duplicates Caesar (ruler · laws/reforms · "great?/tyrant?" · "the price"). Equal 42 s allocations lock the monotony in.

**Timing [E]:** 331 words ≈ 144 s at a deliberate 2.3 w/s → ~96 s for silence and eyes; healthy overall. But C-L02 (30 words ≈ 13 s) does not fit its 10 s slot C-02 before pauses — the review already notes answers cross cuts. Word count is not the authority; a scratch track is (see 5, P0-4).

**Strongest scenes [E]:**
- **Galileo** — G-L03 "And what survives of the question?" is the only question not about the asker. The quietest, lowest-motion chapter; correct choice as first chapter to produce (T13).
- **Oppenheimer** — O-L03/O-L04: the traveller who knows everything cannot answer. This is the film.
- **Khan** — K-L04 "None of those words can make the dead speak" is the best single line.

**Weakest [E]:**
- **Napoleon** — redundant with Caesar; the slot is the natural place to turn the questions on Andre.
- **C-L04** "I came to ask what victory leaves behind" — Andre states the theme instead of letting Caesar feel it.
- **OUT-L01** "What will they have to tell us about the things we are doing now?" — "they" is unanchored; the sentence is the film's last and its clunkiest.

---

## 3. Creative asset analysis

### 3.1 Andre
- **Strengths [E]:** R1 close-up suite holds facial structure and beard well across 10 tiles; `R2-andre-table-cinematic.jpg` is the best tonal anchor in the package (key from camera-left, concrete void, pale oak, hands flat, ring on left hand). Table/hands composition is already the film's look.
- **Gaps [E]:** gaze axis not controlled (C2); J07 take 2 hair volume drifts (STATE.md, confirmed on sheet); two tiles (J06) sit in a warm bokeh bar environment unrelated to any era; present-day tiles use a bright white office, not the concrete present-day plate. The synthetic canon (sleek swept-back hair, navy/charcoal) ≠ the 2024 photographs (textured hair, grey/pinstripe). This is not an error — it is an **undecided look**. R2 anchors have the weakest provenance in the package and the heaviest weight in the bible.

### 3.2 Historical figures
- **Strengths [E]:** all 11 crops obey brow-to-lower-lid; 5 costume fragments exclude the head completely; hands are anatomically clean on the sheets inspected.
- **Gaps [E]:** no figure has one eye identity with two expressions — each pair is two castings. Oppenheimer-stillness trims the lower lid. Napoleon fragment carries several rings and the hand-in-waistcoat pose (iconic, acceptable, but decide); Genghis wears blue patterned silk with a conspicuous ring; Galileo's sheet has invented readable writing; the ger plate seats the Khan on a Chinese-style chair.

### 3.3 Table and plates
- **Strengths [E]:** J26 anchors ×4 share species, planks, ring stain and the near-corner chip — a lockable motif exists.
- **Gaps [E]:** plates were generated as wides with their own camera axis; the match cut, as drawn, happens on the wide. **[R]** Move the match cut to the **insert** (hand + ring + chip, locked lens height, same crop) and let the wides breathe. Then the axis change on Trinity/present-day becomes a deliberate bookend choice rather than a continuity break.

### 3.4 Voice and dialogue
- **[E]** Five ElevenLabs renders of the same line exist; none has been heard. The voice is labelled `pt / pt-brazilian` and used for English — accent is the first thing to judge. No scratch exists for the other 21 lines, so no edit can be timed.

### 3.5 Storyboard atlas
- **[E]** Cards are clean and honest (ID, timecode, action, frame/camera, reference, "keyframe gap"). They lack: motion envelope (what moves, for how long), light anchor, gaze direction, and the reference *hash/version*. The atlas is a review document, not a request payload — which it says.

---

## 4. Workflow validation

**Mapped process (as documented and as practised):** Brief → Research/Script → Continuity (refs → bibles → Element) → Voice → Pilot → Storyboard/Animatic → Approved batch → Production (take review) → Edit → QC/Delivery. Gates, ledger, hashes, atlas rebuild and role briefs exist and work (tests, validate, overwrite refusal all verified in `reports/`).

**Bottlenecks and gaps [E]:**

| # | Issue | Effect |
|---|---|---|
| W1 | **Human decision latency.** 18/21 tasks block on T02/T03 (Andre). The asks are scattered; no form to answer | Project has been "waiting for references and approval" since creation |
| W2 | **Docs outrun approvals.** Bibles and the master visual bible are written as locked ("strictly invariant", "Approved Expression Suite") | Downstream agents inherit false certainty (C1, C5, C6) |
| W3 | **Translation before script freeze.** Four translations were drafted from an unapproved EN script | Any line change (this review proposes several) invalidates them |
| W4 | **Speech route is the largest technical unknown** but is scheduled after Element + pilot (T09 after T08) | Risk discovered late, after reference spend |
| W5 | **No scratch animatic.** Timing is word-count; "audio-first" is a rule with no audio | Slot allocations are guesses; C-L02 already overflows |
| W6 | **Reference contamination risk** (C9) and unlabelled forbidden composition (C7) | Wrong image in an identity slot = wasted paid job |
| W7 | **Script has four homes** (C10) | Edits drift; atlas builder validates CSV only |
| W8 | **No creative-decision owner.** Registry has producer/continuity/historian/dialogue-sound/storyboard/editor/qc — no director/art director | "Which eye base?" "Which table?" have no assignee except "Andre" |
| W9 | **QC checklist stale path** (C8); take-review template never exercised (0 takes) | First real take will hit an untested gate |

**What works and must be preserved:** producer-only spending; approvals as separate booleans; hash/inventory discipline; atlas rebuild from JSON; "COMPLETED ≠ accepted"; eyes-only contract; fictional-dialogue labelling; separate ElevenLabs/Kling scopes.

---

## 5. Prioritised improvements

**P0 — unblock, zero spend (this week)**

| ID | Change | Why it matters | Owner |
|---|---|---|---|
| P0-1 | **Decision sheet for Andre** (`docs/decision-sheet-andre-v1.md`): 8 decisions, each with the options already on disk | Collapses W1; one 15-minute session unblocks T02/T03/T05/T07 | producer prepares · Andre decides |
| P0-2 | **Script v2** (`01_script/proposals/script-en-v2-proposal.md`): break the template, give Andre an arc, make Napoleon the hinge, fix the ending, one use of "argue" | Fixes the film's central weakness (flat protagonist, repetition) before anything is recorded or translated | historian reviews · Andre approves |
| P0-3 | **Reconcile documents**: mark all bibles `STATUS: PROPOSED` until a decision ID; resolve C1–C10; state the table rule ("the table is Andre's, it travels; the ring stain is proof"); strip brand names / readable props; quarantine full-face originals under `07_generations/originals/_quarantine-full-face/` (move, keep hashes); label the Kling render "composition forbidden"; fix the checklist path; mark non-canonical script copies "DERIVED — do not edit" | Removes false certainty (W2, W6, W7) | continuity + producer |
| P0-4 | **Scratch animatic with free local TTS** (no ElevenLabs/Kling spend): render all 22 lines, `ffprobe` durations into `dialogue-lines.csv`, cut a still animatic from atlas cards, re-allocate chapter seconds (unequal is fine) | Replaces word-count with measured speech (W5); exposes overflows before paid picture | dialogue-sound + editor |
| P0-5 | **Speech-route discovery, read-only**: refresh Kling CLI declarations for external-audio input; confirm ElevenLabs lip-sync route availability on the account; write the capability matrix | Pulls W4 forward; no spend | dialogue-sound |
| P0-6 | **Listen** to the five voice renders + inbox file; register the inbox file; pick one or reject all | 480 ElevenLabs credits already spent, zero judgement recorded | Andre + dialogue-sound |

**P1 — small, scoped spend (after P0 decisions)**

| ID | Change | Why | Owner |
|---|---|---|---|
| P1-1 | **Photo session spec** for Andre: front, both ¾, both profiles, seated waist-up; chosen wardrobe + grooming; soft neutral light; plain background (no cables); 85 mm-equivalent; plus a 10 s neutral-to-speech clip | Real angles beat synthetic ones (skill rule); unblocks the Element | continuity specifies · Andre shoots |
| P1-2 | **One eye base per figure**: regenerate only the five inconsistent pairs as *one identity, two minimal expression deltas* (lid/brow/catchlight), same crop scale, gaze camera-left; fix Oppenheimer lower-lid trim | C6; cheapest fix with the biggest continuity gain (≈10 images) | storyboard requests · producer submits under new scope |
| P1-3 | **Table lock**: pick one J26 tile; generate the **5 hand/table inserts** on that geometry (already briefed); accept wides as-is | Match cut moves to the insert (3.3); era wides stop needing to match | continuity + producer |
| P1-4 | **Era-specific Andre keyframes** (10) only after P1-1 and wardrobe decision | Already briefed in `next-image-batch.md`; do not generate them on the undecided look | storyboard + producer |

**P2 — pilot and production (unchanged order, tightened)**
Element → 4-shot identity pilot (locked front listening · gentle turn · one expression · visible speech) → speech-route test on one accepted clip → reforecast → Galileo first → remaining chapters → opening/ending → corrections → Edition H → masters.

**Not recommended:** expanding to more figures, adding a visible "portal", reverse shots of any kind, extending runtime, generating more Andre portraits on the current undecided look, or further translation work before EN v2 freeze.

---

## 6. Delegation (bounded; execution requires explicit assignment — nothing was spawned)

| Role | Task | Input | Deliverable | Review criteria |
|---|---|---|---|---|
| **Producer** | P0-1 assemble decision sheet; P0-3 fix checklist path, mark derived scripts; register inbox voice file; add `director` role to `agents/registry.json` (creative decisions, no spending) | This review, STATE.md, approvals.json | Decision sheet filled with Andre's answers → `review-decision.json` entries per decision | Each decision maps to a file + hash; no approval flag flipped without a decision record |
| **Historian** | T05 on **script v2**: verify every factual anchor in the new lines (three-weeks / three-days spacing, "war ends that summer" needs a surrender source), confirm nothing reads as an attributed quotation | `script-en-v2-proposal.md`, source registry | Claim-level citation table; cache sources 18, 19; add surrender source | Every non-fictional claim has a source ID; every fictional line is marked |
| **Continuity** | P0-3 bible reconciliation (C1–C6, C9), P1-1 photo spec, P1-3 table pick, eye-base selection proposal | Contact sheets, real photos, bibles | Bibles v2 headed PROPOSED with decision slots; `_quarantine-full-face/` move log; photo spec one-pager | No bible sentence asserts an approval that `approvals.json` does not hold |
| **Dialogue-sound** | P0-4 scratch TTS + measurements; P0-5 capability matrix; P0-6 listening notes | Script v2 (after historian), local TTS, ffprobe | `dialogue-lines.csv` measured_seconds filled; `04_audio/scratch/`; `01_script/speech-route-matrix.md` | Durations from files, not estimates; matrix states confirmed / unverified / unavailable per route |
| **Storyboard** | Re-time `source/atlas.json` to measured durations; add gaze, motion envelope, light anchor, reference hash fields; rebuild atlas **v3** | Measured CSV, decisions | `preproduction-atlas-v3/` + diff vs v2 | Builder passes; every card has gaze + envelope; v1/v2 untouched |
| **Editor** | Still animatic from v3 cards + scratch audio; propose unequal chapter allocation (e.g. N 32 s, O 48 s, OUT 22 s) | Atlas v3, scratch stems | `08_edit/timelines/animatic-v1.*` + allocation note | Plays end-to-end; no speech accelerated; silences intentional |
| **QC** | Exercise the take-review template on one existing R1 image as a dry run; update acceptance checklist path; add "reflection / silhouette / background-portrait" line to the zero-face check | Templates, checklist | Filled dry-run review; checklist v2 | Template usable without edits on first real take |

---

## 7. Scene and dialogue refinements

Full proposal with line IDs, rationale and a per-line "keep/change" table: `01_script/proposals/script-en-v2-proposal.md`. Summary of intent:

1. **Andre gets a curve**: fluent (Caesar) → slower (Khan) → warm (Galileo) → caught off guard (Napoleon asks about *his* world) → cannot answer (Oppenheimer).
2. **Napoleon becomes the hinge**: N-L03 turns the question on Andre; chapter shortened. This earns the ending.
3. **One "argue"**, placed where it hurts (N-L03/N-L04).
4. **O-L04** cut to twelve words. Silence does the rest.
5. **Ending** closes the circle on "what came next".
6. **Visual rule**: the table travels with Andre; match cuts on the insert; nothing readable on the table; era-specific seat, never an era-specific table.

---

## 8. Readiness — how the team knows the film is done

Reusable version in `series/andre-time-travel/FRAMEWORK.md`. For this film, "ready" means **all** of:

- `approvals.json`: all nine flags true, each backed by a `review-decision.json` with file + hash.
- `dialogue-lines.csv`: 22/22 `measured_seconds` from real files; 22/22 `approved=true`.
- `shot-list.csv`: 41/41 `accepted_take_id` resolving to local originals with hashes.
- Zero-face gate: every restricted shot inspected at normal speed **and** frame-by-frame, including reflections, silhouettes, pull-backs; log per shot.
- Likeness gate: Andre's written approval of every face-bearing shot and of the final edit.
- Two masters: `ffprobe` + full decode + EBU R128 measured; both fully played by a human; durations 240 s ± 5 % unless re-approved.
- Edition H: every mouth-visible segment either lip-sync-verified or covered by approved L/J cuts; subtitles reviewed against localized audio.
- Ledger reconciles to live balance; unknowns listed, not hidden.
- Delivery folder holds masters, captions, stems, sources/rights notes, manifest — not provider URLs.
