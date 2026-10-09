# Reference & Character-Sheet Plan (draft for approval)

Status: PLAN ONLY. No paid job submitted, no photo uploaded, nothing approved. Written 2026-10-09.
Governs tasks T02, T03, T04 and (for eyes) T12. Authority: `AGENTS.md`, `docs/visual-contract.md`, `docs/reference-intake.md`.

## 1. What exists today (verified 2026-10-09)

| Item | Finding |
|---|---|
| Kling | `kling account` (CLI) reports 7,741 credits, Premier. Live balance matches the old snapshot; no production charges exist. |
| Kling image models (live `who_am_i`) | text_to_image: `kling-image-v3_0_omni` (default), `gemini-3.1-flash-image` (Nano Banana 2), `gemini-3-pro-image` (Nano Banana Pro, up to 4k), `gpt-image-2`. image_to_image: Nano Banana 2 (up to 10 refs), `gpt-image2` (up to 10 refs), plus the Kling models. **No price is declared anywhere**; every cost must be read from the returned `creditsConsumed`. |
| ElevenLabs voice | Voice **"Athar"**, id `xxSch4PcHFM1VKvYKjt2`, category `professional` (a PVC), labelled `pt` / `pt-brazilian`. It exists in the account. It is NOT yet proven for English, Latin, Italian or Mongolian (see section 5). |
| Andre photographs | 9 real camera photos copied (not moved) to `inbox/andre-reference-photos/` with `SHA256SUMS.txt`. Originals remain in `~/Pictures`. All unapproved. |
| Workspace tooling | `.venv` and `scripts/manage.py` do **not exist** (scripts/ is empty), so `manage.py status/validate` cannot run. Not created in this pass. |

## 2. Photo inventory and honest assessment

Best candidates (real photographs, phone main/selfie cameras):

| File | Use | Problems |
|---|---|---|
| `20240202_015214 / 015259 / 015304.jpg` | Primary identity set: near-frontal/slight 3/4, grey blazer over light shirt, plain wall, good light | Smiling; blazer is mid-tone grey, not "dark"; no profile. Same session, so one wardrobe and grooming state. |
| `IMG_20220321_103632.jpg`, `IMG_20230220_183202.jpg` | Secondary: frontal selfies, different year | Wide-angle selfie distortion; white shirt; grooming differs by year. |
| `IMG_20210722_151056_optimized.jpg` | Secondary: seated, headphones, dark navy shirt | Headphones occlude hair/ears; compressed. |
| `IMG_20210818_105943_optimized.jpg` | Wardrobe/posture only (dark suit, standing) | Face small. |
| `IMG_20210428_141013_optimized.jpg`, `20230817_203913.jpg` | Seated at a table | Face small, busy background. Table reference only. |

Gaps versus the plan's six-photo packet: **no clean profile-left, profile-right, neutral-expression or seated-waist-up photograph.** The plan forbids calling AI angles photographic evidence, so any profile/3-4 sheet panel is labelled `synthetic` and cannot replace new photographs. Identity matches across files are my visual impression only; **Andre must confirm every file is him and choose the grooming year.**

## 3. Deliverables

All generated files go to `02_references/andre/synthetic/` (never `raw/`/`approved/`) with a sidecar JSON per file: prompt, model token, source photo hashes, job/generation ID, `creditsConsumed`, `provenance: synthetic`, `approved: false`.

### A. Andre (the only full-face character sheet)
1. **Master turnaround sheet** (16:9 or 21:9): front, 3/4-left, 3/4-right, profile-left, profile-right, in the film wardrobe on neutral grey, even soft light. Panels outside the photographed angles are flagged.
2. **Face close-ups**: neutral, slight smile, listening, concerned, thoughtful (5).
3. **Seated waist-up at plain wooden table**, hands visible, camera-right gaze (the film's hero frame), 3 variants.
4. **Wardrobe/hands detail**: jacket, hands on table (match-cut anchor), 2-3 images.
Candidate volume: ~25-35 images across 6-8 jobs, not hundreds. Quantity beyond this adds drift, not usefulness.

### B. Historical figures: eyes + below-the-neck ONLY
Per `visual-contract.md`, **no full-face sheets for Caesar, Genghis, Galileo, Napoleon, Oppenheimer**, and no reflections. Per figure: 2 eyes-only crops (brow to just below lower lids) for two emotion states, 1 costume fragment (collar/sleeve/hands), 1 prop. 5 figures x 4 = ~20 images, original fictional casting, no modern actor likeness.

### C. Table and scene anchors
Plain wooden table (grain, edge damage, prop positions), 1 empty-room plate per era, no people. ~10 images.

Everything lands in the existing folders: `02_references/andre/synthetic`, `02_references/history-eyes/<name>`, `02_references/table`, `02_references/wardrobe`.

## 4. Model strategy (from live schema + current docs)

Docs and vendor guides agree on one pipeline: build a locked multi-angle sheet, reuse the identical descriptor text, feed the best views to the video model as references. Several vendor percentages are unverified; I use only the workflow, not the numbers.

| Job | Model | Why |
|---|---|---|
| Andre master sheet and close-ups | `gemini-3-pro-image` (Nano Banana Pro), image_to_image if listed, else the 2k/4k route, with 3 photos as refs | Highest fidelity multi-reference; 4k. Fall back to `gemini-3.1-flash-image` (up to 10 refs, cheaper-tier) |
| Second opinion on likeness | `gpt-image2`, quality `high`, same refs | Different model family; compare, keep the better. Only if job 1 is borderline. |
| Eyes, costume, table, scenes (no Andre face) | `gemini-3.1-flash-image` (Nano Banana 2) text_to_image | Cheap, no identity risk |
| Production Element (T04) | Kling image Element from approved cover + 1-3 secondaries | Only after Andre approves the photos; read back with `element_get` |

Rules: one deviation per job; `imageCount` is the cost multiplier so start at 2-4; CLI only; no auto-retry; stop after the first job to read the real charge before queueing the next.

## 5. ElevenLabs "Athar" voice: readiness checklist

PVCs auto-train on Flash v2.5, Turbo v2.5 and Multilingual v2; support for other models must be fine-tuned in My Voices; PVC verification proves the voice is the owner's. So: the voice exists and is professional-grade, but "ready" needs:
1. Confirm which models are enabled for it in My Voices (Multilingual v2 / Eleven v4 for English and Italian).
2. One short English test line (Andre's own text, consented voice) and one Italian line. Small TTS cost; **needs your scope** (ElevenLabs is outside the Kling budget).
3. Latin, historical Mongolian and Napoleon's Corsican/Tuscan target remain unverified and need a reviewer (T06). Do not substitute French.
4. A pt-BR label may bias English accent; judge by listening, you decide.

## 6. Gates and the questions I need answered

1. Confirm the nine inbox files are you, and which grooming/wardrobe is canon (2024 blazer or a dark shirt).
2. **Spend approval for batch R1** (suggested cap 250 credits of the 774 references phase; first job of 2-4 images, then re-evaluate from the real charge). Approval is for R1 only, not the whole film.
3. **Upload approval**: running image_to_image uploads your face photos to Kling and the model providers behind it (Google/OpenAI). Local-only generation is not possible with these models.
4. Separate scope for ElevenLabs test lines.
5. Ideally, shoot the six clean photographs described in `reference-intake.md`; the synthetic sheet is a stopgap for composition and prompt design.

## 7. Execution order after approval
1. Register the 9 photos in `asset-registry.csv` (done as unapproved).
2. You pick 3 primary photos; I build a contact sheet for your sign-off.
3. R1 job 1 (Andre master sheet, Nano Banana Pro, 2 images). Record generation ID and charge in `credit-ledger.csv`. Review every output at full resolution.
4. Continue jobs 2-8 only if job 1 is acceptable.
5. Non-face batches (eyes, costume, table) in a second approved batch.
6. You approve likeness; only then T04 Element creation.
7. Update `memory/STATE.md` with verified facts.
