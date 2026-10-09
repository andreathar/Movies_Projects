# FRAMEWORK — Andre × [Figure] conversation films

Series-level, reusable. Companion to `series.json` (constraints) and `../../docs/REPEATABLE_WORKFLOW.md` (local editing mechanics). This file says **what a good episode is and how we know it is done**; it does not carry any approval, budget, job or take from one episode to the next.

Version 1 · 2026-10-09 · derived from the review of *The Table Between Centuries* (`projects/andre-time-travel/docs/art-direction-review-v1.md`).

---

## 1. The format in one paragraph

Andre, in his own modern clothes, sits at **his** table across from someone who does not know what came next. The table travels with him; everything else belongs to the era. The other person is never shown as a full face — eyes, hands, cloth, props, an empty seat. Each conversation is short, fictional, and anchored in cited fact. Andre is a humane interlocutor, not a prosecutor and not a tour guide. The film is about what it costs to be remembered — and, by the end, about us.

## 2. Scene grammar (per encounter)

Every encounter has exactly these beats; lengths vary, order does not.

| Beat | Who | Purpose | Typical length |
|---|---|---|---|
| 1. First question | Figure (offscreen) | About themselves: name, work, heirs, laws | 2–4 s |
| 2. Consequence | Andre | What survived, honestly, with one complication | 7–12 s |
| 3. Second question | Figure | Escalates: from reputation toward conscience — or **turns on Andre** | 2–4 s |
| 4. Answer with a limit | Andre | Refuses a verdict; admits what knowing the future cannot do | 4–10 s |
| 5. Eye response | Figure (eyes only) | Tied to a specific word in beat 2 or 4 — never decorative | 3–5 s |
| 6. Table exit | Insert | Hand / stain / chip; sound bridge; match cut | 3–5 s |

Rules that make an episode work (evidence: v1 of the first film failed each of these before revision):
- **Vary the shape.** No two encounters may share the same question-pair pattern. Keep a repetition audit (key verbs, sentence shapes, answer lengths).
- **Andre must change.** Define his curve in one word per chapter before writing lines (e.g. *fluent · slower · warm · caught · silent*).
- **One hinge.** Exactly one figure asks Andre about *his* world. The ending answers that question — never introduce the ending's turn without it.
- **The last answer is a limit, not a lesson.** The strongest ending is Andre unable to answer.
- **Unequal chapters are fine.** Allocate seconds after the scratch track, not before.
- **Measured speech is the timing authority.** Word counts are placeholders; `measured_seconds` from real files drive the edit; never accelerate a performance to fit a slot.

## 3. Factual discipline

- Every non-fictional claim carries a source ID from the episode registry; every spoken line is labelled fictional. (`film-dialogue-localization` §1)
- No attributed quotations, no precise numbers without a source, no single-cause explanations of complex outcomes, no "everyone today thinks…".
- Historian pass (T05-equivalent) runs on the **frozen** script, **before** any translation or recording.
- Period cautions live in the brief table (one line per encounter) and are copied into the scene bible.

## 4. Visual contract (invariants across episodes)

| Element | Invariant | Episode-specific |
|---|---|---|
| Andre | Approved likeness set (real photos, versioned), one wardrobe canon per episode, grooming canon, tested angle envelope (front / ¾), gaze axis fixed at episode start | Wardrobe choice; light temperature per era |
| Table | His; travels; two repeatable marks (stain + chip) visible in every era; one locked anchor tile; match cuts on the **insert**, not the wide | Props (unreadable), the opposite seat |
| Figures | Zero full faces, ever, including reflections, silhouettes, pull-backs, background portraits; one eye identity per figure; expression B is a minimal delta of A; below-neck fragments exclude chin/neck | Costume, hands, props |
| Camera | One action + one camera behaviour per generation; no orbits, no portals over faces, no hand-to-mouth during speech; transitions off the face | Push-in vs locked |
| Environment | No extra people; no readable text; era-plausible seat/light/props | Palette |

## 5. Phases, gates, artefacts

| Phase | Entry | Output artefacts | Gate (who) |
|---|---|---|---|
| 0 Brief | Dramatic question, figures, runtime, editions | `00_brief/brief.md` with per-figure dramatic question + eye progression + research boundary | Producer freezes scope |
| 1 Script | Brief | `script-en.md` + `dialogue-lines.csv` (stable IDs), repetition audit, Andre curve | Historian citations → Andre approves |
| 2 Decisions | Script, reference candidates | **Decision sheet** (identity set, wardrobe, grooming, table tile, eye bases, voice, photo session) | Andre answers → producer records `review-decision.json` per item |
| 3 Continuity | Decisions | Bibles v-next headed `STATUS: PROPOSED/DECIDED`, continuity matrix, quarantine of any full-face originals | Continuity reviewer |
| 4 Scratch | Approved script | Free local TTS scratch for every line; `measured_seconds` filled; still animatic; chapter allocation | Dialogue-sound + editor; no paid audio yet |
| 5 Voice | Scratch timing | Approved clone renders, dry stems, durations measured; hardest phrase tested per language | Andre listens; language reviewer where applicable |
| 6 References (paid) | Decisions + scoped approval | Real photo session; Element; eye bases; table inserts; era keyframes — each with job ID, charge, hash | Producer submits; continuity reviews every image |
| 7 Pilot (paid) | Element + keyframes | 4 restrained shots + 1 speech-route test; full temporal review | Continuity + Andre likeness approval |
| 8 Production (paid) | Pilot + reforecast + batch approval | Takes per shot ID; accepted/rejected with reasons; ledger reconciled | Producer; "COMPLETED ≠ accepted" |
| 9 Edit | Accepted takes + stems | Picture lock, subtitles, stems, per-edition timelines | Editor |
| 10 QC / Delivery | Exact masters | ffprobe + full decode + loudness; full human playback; zero-face log; likeness sign-off; delivery folder | Independent QC + Andre |

Two rules on order: **script freeze before translation**; **speech-route discovery (read-only) in phase 4**, paid speech test in phase 7.

## 6. Asset requirements (per episode)

- Andre: ≥ 6 real views in the episode canon (front, both ¾, both profiles, seated) + 10 s neutral-to-speech clip; plain background; no wide-angle; originals untouched, hashes recorded.
- Per figure: 1 approved eye base + 1 delta; 1 below-neck costume fragment; 1 hand/table insert on the locked table geometry.
- Per era: 1 environment wide (axis free), 1 Andre speaking keyframe, 1 Andre listening keyframe, 1 insert.
- Table: 1 anchor tile; inserts share lens height, crop and marks.
- Audio: 1 approved render per line per edition; dry stems; measured durations.
- Documents: brief, script + CSV, bibles, decision sheet + decisions, atlas (editable JSON → rendered revision), shot list, ledger, manifest.

## 7. Document hygiene

- Every bible, atlas and plan carries `STATUS: PROPOSED` until it cites a decision ID; "approved", "locked", "invariant" are forbidden words in a PROPOSED document.
- The script has **one** editable home (script + CSV). Any other copy is headed `DERIVED — do not edit`.
- Full-face originals of synthetic figures never share a folder with references.
- Style references that violate the contract (e.g. an over-shoulder two-shot) are labelled `composition forbidden — style/tone only`.
- Paths in checklists must exist in the workspace.

## 8. Quality criteria — "ready" definition

An episode is ready when **all** are true and evidenced:

1. All approval flags true, each with a decision record (file + hash + scope).
2. 100 % of lines measured from real audio and approved; no accelerated speech.
3. 100 % of shots mapped to accepted local takes with hashes; no provider-URL dependencies.
4. Zero-face gate logged per restricted shot (normal speed + frame-by-frame + reflections/silhouettes).
5. Andre's written likeness approval for every face-bearing shot and the final cut.
6. Both masters: `ffprobe`, full decode, EBU R128 measured, full human playback; runtime within ±5 % of target or re-approved.
7. Edition H: every mouth-visible segment lip-sync-verified or covered by an approved cut strategy; subtitles checked against localized audio.
8. Ledger reconciles with the live balance; unknowns listed.
9. Delivery folder complete: masters, captions, stems, sources/rights, manifest, fictionalization notice.

## 9. Starting the next episode

```bash
.venv/bin/python scripts/workflow.py new-draft --id andre-episodio-NN --title "…"
```
Then, in order: brief table (one row per figure) → Andre's one-word curve → script with repetition audit → decision sheet → scratch. Do not touch paid references before the decision sheet is answered. Nothing from a previous episode is approved by inheritance; reuse requires file + hash + decision.
