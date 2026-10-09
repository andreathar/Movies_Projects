# Continuity Bible — DRAFT v1 — *The Table Between Centuries* (`andre-time-travel`)

Date: 2026-10-09, ~09:12–09:40 (UTC-3) · Role: script / continuity supervisor (read-only review) · **STATUS: PROPOSED.** This file approves nothing, changes no approval, task, manifest, ledger, bible, script or memory file, and calls no paid or external service. Nothing was staged or committed. Every "proposed rule" below needs a decision record in `00_brief/decisions/` before anyone treats it as canon.

Paths are relative to `projects/andre-time-travel/` (`P/`) unless they start with `inbox/`, `series/`, `skills/` or `docs/` at the workspace root.

## 0. Base state and what was inspected

- **Concurrent work.** While I was reading, the art director/producer integrated script v2 into canonical `01_script/script-en.md` and `dialogue-lines.csv`, recorded decisions D01–D10 in `00_brief/decisions/`, added a delegated-authority record to `00_brief/approvals.json`, prefixed every bible with `STATUS: PROPOSED`, quarantined the uncropped eye originals, labelled the inbox Kling render "composition forbidden", and produced a free edge-tts scratch track (`04_audio/scratch/edge-tts-v2/`). **This report is written against that newer state.** Where a file still holds v1 content, I say so (see CB-09).
- `manage.py status` currently returns `error: budget allocations disagree with snapshot ceiling` and warns that two shared skills changed. This comes from the concurrent edits; I did not touch anything that would cause it.
- **Read:** `AGENTS.md`, `skills/andre-time-travel/SKILL.md`, `film-character-continuity`, `film-editing-qc`, `kling-cli` (prompt constraints only; not run), `manifest.json`, `memory/STATE.md`, all of `03_bibles/`, `01_script/` (canonical script, CSV, language files, four translations, v2 proposal), `05_storyboard/shot-list.csv`, `source/atlas.json`, atlas v1 documents, `docs/visual-contract.md`, `docs/art-direction-review-v1.md`, `docs/decision-sheet-andre-v1.md`, `agents/handoffs/`, decisions D01–D10, `series/andre-time-travel/series.json` + `FRAMEWORK.md`, the sibling `docs/assistant-reviews/production-watchlist-v1.md` (to avoid duplicating it), and the R1 prompt files for J20/J26/J31.
- **Viewed as images (vision):** all 10 inbox files (9 photographs plus the Kling render), the six `_review` contact sheets, `R1-J04_1`, `R1-J06_1`, `R1-J08_1`, `R1-J26-table-anchor_2`, `R1-J31` Trinity plate, `R1-J19` eye crop, all four R2 Andre images, both R2 plates, all six R2 wardrobe sheets, and shot card `N-01`.
- `inbox/failed-clips/` holds only `.gitkeep`. **No failed clip or generation ID exists** (see §10).

---

## 1. Andre — likeness anchors

### 1.1 Reference status (what counts as identity)

| Set | Files | Status | Continuity notes (observed) |
|---|---|---|---|
| Real 2024 trio | `inbox/andre-reference-photos/20240202_015214/015259/015304.jpg`; crops in `02_references/andre/selected/` | **D01: identity truth.** `characterReferences=false`; Andre's own likeness approval still pending | One session, frontal and slightly ¾, **all smiling (no neutral mouth)**, grey pinstripe suit with a white striped shirt (≠ D02 wardrobe), plain grey wall, a cable and an outlet in frame. No glasses. In `015214` (arms crossed) at least one ring is visible on his left hand, and it reads dark-toned at this resolution. |
| Real 2021–2023 (6) | `IMG_2021*`, `IMG_20220321`, `20230817`, `IMG_20230220` | D01: grooming history only | **Contain third parties.** 2022 has people reflected and seen through glass; 2023-08 and 2023-02 are group photos, and two of the other men wear glasses. Hair reads lighter and more golden in 2023-02 and the beard fuller in 2023-08. **These must never enter an identity or Element slot.** |
| Synthetic R1 J01–J09 | `02_references/andre/synthetic/R1-*` | D01/D03: tone only | Sleek swept-back hair variant (rejected by D03). J06 sits in an unrelated warm-bokeh bar. Gaze is mixed (seated sheet: ~2 to camera-left, ~3 to camera, ~1 to camera-right). **The atlas still uses J08_1 for every X-02 card and J04_1/J06_1 for every X-04/X-07 card** (CB-17). |
| Synthetic R2 Andre | `R2-andre-profile-left/right`, `R2-andre-table-cinematic`, `R2-andre-seated-conversational` | Unapproved; **no provider IDs** | The "profiles" are synthetic (lower-confidence geometry). `table-cinematic` has the key from camera-left, the silver band on his left hand, and Andre **right of centre** looking camera-right (no lead room). `seated-conversational` is an **over-the-shoulder shot with a woman's head in the foreground plus background café faces** (CB-04). |
| Kling render | `inbox/andre-reference-photos/kling_20261008_IMAGE.png` | Labelled "composition forbidden" (README) | OTS two-shot. A **blurred second face (nose and lips) is in the foreground at top-left**. Andre looks down toward **camera-left**, the reverse of D09. Warm-bokeh "bar" look. |
| Wardrobe R2 | `02_references/wardrobe/R2-wardrobe-andre-modern.jpg` | **D02 artifact** | A labelled collage. Its top-left tile shows **another man's chin and lips** (CB-03). |

### 1.2 Proposed anchor list (descriptive, from the 2024 photos; no biometric claim)

- **Face:** oval-to-square jaw, straight prominent nose, defined level brows, light-brown/hazel irises, warm, slightly ruddy skin with visible texture. No glasses in any photo, so **never add glasses to Andre**.
- **Hair (D03):** short, dark-to-medium brown, textured, with volume at the front hairline. Not sleek, not swept back. Keep the colour as in the 2024 photos; don't push it darker than the photographs.
- **Beard (D03):** 3–5-day stubble joined to the moustache, trimmed at the jaw and neck. The same length in every chapter. **The beard must not grow or shrink between eras** (a common drift).
- **Age:** no source states it. The bible's "Mid-40s" is an impression and must not go into prompts as a fact (CB-30).
- **Build:** slim-to-medium. Seated framing only; height never shows.
- **Hands:** his own hands appear in the inserts (IN-01, X-07 tails, X-01 heads). The **ring finger and ring must match the real hand.** D02 asserts a "silver band left hand", but the only real hand photo (`015214`) shows a dark-toned ring. **Andre must confirm what he actually wears** before inserts are made (CB-14).
- **Expressions:** every real photo is a broad smile, so neutral, listening and speaking states have no photographic truth until the D08 session. Until then, any neutral face is a model guess.

## 2. Wardrobe

### 2.1 Andre (D02; no change on time travel)

The look is invariant in all 41 slots: a **deep-navy unstructured wool-blend blazer, worn open**, with notch lapels, patch pockets and **3 horn cuff buttons** (as drawn in the R2 sheet). Under it, a **charcoal garment-dyed cotton-linen shirt with horn buttons, top 1–2 buttons open, soft collar**, with about 1 cm of shirt cuff showing at the wrist. The **silver band is on the left ring finger (to be confirmed)**. No watch, no logos, no pocket square.

Not yet specified (propose): dark trousers (visible only in a wide), no belt-buckle shine. Andre arrives in the same state in every era: no dust, no rain, no sweat, the same collar spread, the same sleeve push.

- **D02's limitation applies:** if Andre shoots the D08 session in another outfit, D02 is void.
- **Colour drift under era light:** navy reads black under tungsten and brownish under firelight. Grade against a fixed blazer-plus-skin anchor per chapter so the jacket doesn't appear to change colour (CB-26).

### 2.2 Historical figures (below neck only; see §4 for the face rule)

| Figure | Bible spec (current) | Reference reality | Open conflicts |
|---|---|---|---|
| Caesar | Off-white tunic with *latus clavus*; cream *toga praetexta* with a purple border, **pinned with a round gold fibula**; signet ring on his **right** hand (`scene-bibles/caesar.md`) | J21: narrow border, iron ring, hands folded. R2: broad bands, gold fibula at the shoulder, laced sandals, chin and mouth visible | Narrow vs broad border; fibula on a toga, laced sandals, and which ring metal (iron/gold) → **historian check, don't assume**. |
| Genghis | Brown silk deel with wolf fur, lamellar chest, studded belt; **no conspicuous ring**; seat is a low stool/cushion (`table-and-continuity.md`) | J22: **blue** patterned silk, ring, bracelet, **kneeling on the floor**. R2: brown, armour, **two rings**, bracers, dagger, standing, beard and lips visible | Colour (blue vs brown); rings; seat height vs a 75 cm table (CB-15). |
| Galileo | Charcoal doublet with fabric buttons, white falling collar, dark gown, ink-smudged cuffs | J23 and R2 broadly match. **R2 shows the white beard and mouth** | Fine on garment; reference crop is non-compliant (CB-01). |
| Napoleon | Green Chasseurs coat with red piping, brass eagle buttons, Légion d'honneur ribbon + star, white waistcoat, **bare hand (no rings)** | J24: long coat, standing, hand in waistcoat, **several rings**. R2: short cropped coat, cross + star, chin and lips visible | Coat cut (long vs cropped); rings; standing vs seated. |
| Oppenheimer | Grey herringbone tweed, off-white shirt, dark knit tie, **silver pocket watch on chain** | J25: **wristwatch**, writing in a brown notebook. R2: pocket-watch chain, **wedding ring**, head silhouette under the bulb | Pocket watch vs wristwatch; ring; **hat** (the J19 eye base has a hat-brim shadow; no costume has a hat) (CB-20). |

## 3. The table (D04) — physical continuity

- **Locked anchor:** `02_references/table/R1-J26-table-anchor_2.png`, pale unpainted oak, about 4 wide planks with lengthwise grain, square legs with an apron. **Marks:** one main chip on the long front edge just right of the near corner (a smaller nick further along the same edge), and a pale ring stain on the second plank, left of centre.
- **Rule (D04):** the table is Andre's and travels with him. Stain and chip appear in every era. Match cuts happen on the insert, never on the wide.
- **Proposed additions (not yet decided):**
  1. **Andre's edge = the chipped long edge.** Seen from his chair, the chip is near his left-hand corner and the stain one plank in. *Verify this against the anchor's orientation before locking.*
  2. **Andre's half of the table stays empty except for his hands.** All era props sit on the figure's half, so the stain and chip are never covered.
  3. **Insert recipe:** Andre's **left hand** (ring visible) flat beside the stain, chip in the lower frame edge, same lens height and crop every time.
  4. **No wear progression.** Era props must leave no new marks (wax drips, ink, ash, oil, wet rings). The table resets to the anchor state at every cut, and the stain stays a single ring (CB-25).
  5. **Design drift to block:** the R2 Rome plate (X-trestle), the R2 present plate (trestle with stretcher), the `R2-andre-table-cinematic` slab, and every R2 wardrobe sheet (each a different dark table) **are not this table** (CB-05).

## 4. Hard rule — zero historical full faces (audit)

### 4.1 Reference files that already violate or invite a violation

| File | Problem | Cited by |
|---|---|---|
| `wardrobe/R2-wardrobe-caesar-roman.jpg` | Chin and mouth at the top edge | `caesar.md` wardrobe anchor |
| `wardrobe/R2-wardrobe-genghis-mongol.jpg` | Beard and lips | `genghis.md` |
| `wardrobe/R2-wardrobe-galileo-scholar.jpg` | **Beard, moustache and mouth clearly visible**; framed picture on the back wall; readable generated text | `galileo.md` |
| `wardrobe/R2-wardrobe-napoleon-uniform.jpg` | Chin and lower lip | `napoleon.md` |
| `wardrobe/R2-wardrobe-oppenheimer-tweed.jpg` | **Head silhouette and neck under the bulb**; readable "U.S. ARMY / TRINITY TEST DATA", "LUCKY STRIKE"; polished lighter | `oppenheimer.md` |
| `scene-bibles/oppenheimer.md` (wardrobe row) | "bulb directly above conceals the upper head in deep shadow" **writes a head silhouette into the spec** | — |
| `andre/synthetic/R2-andre-seated-conversational.jpg`, `inbox/.../kling_20261008_IMAGE.png` | OTS second head (the Kling render shows a blurred face) | Kling render now labelled |

FRAMEWORK rows say "below-neck fragments exclude chin/neck" and "including … silhouettes". **Every R2 historical wardrobe sheet fails its own bible's rule** and must be cropped or replaced before it is used as an input (CB-01, CB-02).

### 4.2 Script and storyboard lines that would force or invite a face

- **No spoken line requires seeing a figure.** All figure lines are marked offscreen in v2.
- **X-01 "sleeve/hand suggests [figure]"** (all chapters). Generators tend to complete the head above a seated torso and tilt up. Require the frame top at mid-chest with a locked camera, and check for **cast head shadows** on the table or wall (worst in O: an overhead bulb throws the head shadow straight onto the table).
- **X-03/X-05 eyes.** Two risks: crop creep (nose bridge, nose tip, cheek) when a 4:1 strip becomes a 16:9 video frame (CB-29), and any push or pull. Use a locked camera, allow one blink, inspect every frame.
- **X-02/X-04/X-07 Andre singles.** In these the camera sits near the figure's eyeline, so **any window, glass, mirror or polished surface behind Andre reflects the figure** (G window, N shutters/panes, O window, the present-day glass wall) (CB-18). Also watch Andre's catchlights in extreme close-ups.
- **X-06 table inserts:** reflective props seen from above can mirror the figure leaning over them: C oil lamp, bronze stylus, fibula, ring · K liquid in the bowl, brass belt fittings · G ink surface in a brass inkwell, brass compass, candlestick · N brass candlestick, eagle buttons, star · O silver pocket watch, metal ashtray, lighter (R2), bulb glass (CB-19).
- **OUT-02 empty chair:** no ghost, silhouette or face in the glass wall.
- **Oppenheimer's glasses:** no project file gives him glasses; the eye prompts say "no glasses". **Don't add them.** If a historian later wants them, the lenses become a reflection surface and need their own rule.

## 5. Axis, eyeline and seating

- **Decided (D09):** Andre sits screen-left and looks camera-right. The figure's eyes sit screen-right and look camera-left. The `continuity-matrix.csv` outlier has been corrected.
- **Inserts (proposed):** with the camera on the same side, **Andre's hands enter from frame-left and the figure's hands from frame-right.**
- **Floor plan is undefined (CB-16).** The references disagree:
  - In the era plates, the figure's chair is on the far or right side.
  - In `R2-andre-table-cinematic`, Andre faces the lens from a long side and looks right, which puts the figure at a corner.
  - In the R2 present plate, the chairs face each other across the table, shot end-on.

  **Proposal:** opposite long sides, figure offset toward Andre's front-right, about 1.2 m apart. Then Andre's 15–35° camera-right look is geometrically true and one top-down plan serves all eras.
- **Gaze discipline under v2 performance:** Napoleon is "caught" and Oppenheimer is "silent". Andre's eyes may drop, but **must not cross to camera-left**. Eye-base gaze for the figures is camera-left in all decided crops (D05).

## 6. Light and time of day

**Geometry note.** One motivated source on the camera side of the axis lights Andre from camera-left and the figure from camera-right. This means the bible (Andre key camera-left) and every R1 eye prompt ("light from the right") are **consistent**. However:
- `napoleon.md`'s "marine daylight falling over his left shoulder" puts the key on the far side and contradicts this (CB-08).
- The era wides show their windows on the far wall, which makes them backlight.

| Chapter | Bible says | Atlas / plates / eye bases say | Proposed (follows the decided eye base, because D05 crops embed their light) |
|---|---|---|---|
| Present (IN/OUT) | Soft cool **morning** window light | R1-J32 bright day; **R2 plate is blue-hour dusk** | Pick one; the opening and ending should match unless a time shift is intended (CB-23). |
| Caesar | **Morning sun** through the compluvium/colonnade; morning birds | J27 plate, atlas and J11 base: **oil lamp, dark interior**. R2 plate: open daylight peristyle | **Warm oil-lamp interior** (matches the J11_1 base), or regenerate the base. |
| Genghis | Hearth firelight | J13 base: firelight from the right. J28 plate: daylight through the roof ring plus fire | Firelight dominant; decide whether the roof ring is lit (time of day). |
| Galileo | **Dusk** + candlelight; crickets, bells | J15 base, J29 plate and atlas: **soft cool daylight** | **Daytime cool window light** (matches J15), or redo the base. |
| Napoleon | Grey sea daylight | J30, atlas: same. Eye base: **recast pending** | Grey daylight from camera-side. Brief the recast to match. |
| Oppenheimer | **Night**, thunderstorm, rain on tin, overhead tungsten | J31 plate: **daylight window**. J19 base and atlas: **pale pre-dawn from a right-hand window + hat-brim shadow**. R2: night tent canvas | **Pre-dawn** (matches J19). Then the date reads **16 July, not 15** (CB-07), the rain and thunder move to "distant" or are dropped, and the overhead bulb stays off-face. |

## 7. Transitions between centuries — what carries across

Carries across every cut: the **table (stain + chip)**, **Andre's left-hand gesture on the insert**, Andre's wardrobe and grooming, and his posture.

Never carries across: era props, chairs, figure costume pieces, wear marks, or light colour on the wood.

D04 requires an insert match cut, **but no slot is reserved for it** (CB-24). Proposal: X-07 ends on the locked insert (last 1–1.5 s), and the next X-01 opens on the identical insert in the new era, before the figure's sleeve enters from frame-right.

| Boundary | Sound bridge (bible) | Conflicting source | Proposal |
|---|---|---|---|
| IN-03 → C-01 | Present room tone falls away | — | Silence beat → Rome. |
| C-07 → K-01 | "Sound bridge into Mongolian steppe wind" | Rome: "morning birds, market" (bible) vs "small flame, room tone" (atlas) | Lamp flicker → steppe wind on the felt. |
| K-07 → G-01 | "Quiet match cut" | — | Fire crackle out → room air in. |
| G-07 → N-01 | "Table match cut into Saint Helena" | Galileo: "crickets, church bells" (bible) vs "quiet air, one paper movement" (atlas) | Paper → shutter wind. |
| N-07 → O-01 | "Table cut to desert night" | Napoleon: "wind and sea spray" (bible) vs "sea stays outside" (atlas). Oppenheimer: "rain on tin, thunder" (bible) vs "sparse desert wind" (atlas) | Decide O weather with §6. |
| O-07 → OUT-01 | "Cut back to present" | — | ≥4 s O silence (v2) → present room tone. |

## 8. Dialogue continuity, language, subtitles

- **Canonical text is now v2** (D07), but **scene-bible dialogue tables, slot cue words, `source/atlas.json` performance/cues and `manifest.json`/`shot-list.csv` descriptions are still v1.** Examples: K-05 "missing families", O-02 "the test and two cities", C-05 "republic/legacy", every scene-bible C/K/G/N/O-02 and -04 quote (CB-09).
- **New dialogue gap (CB-11):** v2 N-L03 "do they still argue about **the price**?" has no antecedent. In v1, Andre said "the price" in N-L04, which v2 replaced. In v2 nobody mentions a price or an argument earlier in the chapter.
- **Cue-to-slot misalignment (CB-10).** Scratch durations come from `04_audio/scratch/edge-tts-v2/provenance.json`, which is faster than the planned deliberate delivery.
  - **O:** O-L02 runs 11.86 s, longer than the 10 s O-02 slot. Its cue A ("Hiroshima") lands about 2 s into the line, roughly 8 s before O-03.
  - **Early cue A:** cue A also falls early in C-L02, K-L02 and N-L02, so the X-03 eye reaction would come late unless it is cut in mid-line as an L-cut.
  - **K:** cue B ("no longer there") now ends **K-L02, before K-03**, so the cue order is inverted.
  - **G:** cue B ("does not settle") ends G-L04, which falls in G-06, **after** G-05.
  - **First-question placement disagrees:** the scene bibles put X-L01 inside X-02; atlas performance puts it at 0.3–4.5 s, over X-01.
  - **Fix:** a v2 line-to-slot map, built from measured audio, before any keyframe.
- **Voices:** all five figures share one scratch voice (`en-GB-RyanNeural`) and Andre has a US scratch voice. That is fine for timing, but don't judge characterization from it. The final figure voices must be five distinct ones, none an actor imitation (`language-strategy.md`). Andre's clone is labelled pt-BR and untested in English (D06 pending).
- **Edition H:** all four translations are **superseded** (D07), so no current historical-language text exists.
  - The Edition H language for IN-L01/OUT-L01 is not defined; English is presumably intended, but no file states it.
  - Napoleon's target (Corsican vs French) is open.
  - Latin and other languages run longer than English, and footage is shared. **Picture timing must fit the longest language,** and Andre's mouth-visible shots need per-language variants or approved L/J cuts.
- **Subtitles:**
  - Edition E: none required (optional SDH).
  - Edition H: English subtitles for every non-English line from both speakers; Oppenheimer's chapter is English. Timed from measured audio.
  - Placement: lower safe area, never over the eye strip in X-03/X-05 or over Andre's mouth during sync-critical lines.
  - Burned-in vs sidecar: undecided.
  - Reviewer: the T06 language reviewer.
  - The fictionalization notice goes in the end credits (script, Ending).

## 9. Props per figure (era sanity, not new facts — historian T05 decides)

- **Caesar:** wax diptych + bronze stylus + terracotta oil lamp (table bible). `caesar.md` asks for "Latin text incisions" on the tablet, which conflicts with the v2/FRAMEWORK "no readable text" rule. **The R2 Rome plate shows a bound codex-style book instead of a wax tablet**; keep the bible's tablet.
- **Genghis:** coarse bowl, rolled leather/sheepskin map, tallow candle. The R2 sheet adds a **dagger** that no bible lists. The map is a design choice; the historian should confirm.
- **Galileo:** manuscript sheets (unreadable), brass inkwell, **quill: table bible says "brass quill pen", scene bible "goose quill"** (R2 shows a feather) → use goose quill. **"Brass astrolabe/compass" (table bible) vs "brass drafting compass" (scene bible; J23 shows dividers)** → pick one. R2 shows readable "DE MOTU TERRAE" / "Dialogo" → remove.
- **Napoleon:** leather Civil Code volume with a **readable spine in R2** → unreadable; brass candlestick. `napoleon.md` adds a hand-drawn map of Europe and a pewter ink pot that the table bible omits → reconcile.
- **Oppenheimer:** notebook (closed, unmarked), unbranded cigarettes, silver pocket watch, metal ashtray, telephone cable. R2 adds a **lighter** and readable text/branding; J25 has a **wristwatch**; the eye base implies a **hat**.

## 10. Failed clip

There is no artifact: `inbox/failed-clips/` contains only `.gitkeep`, although the workspace `README.md` says it should hold "the earlier broken-face take and a note with its exact generation ID". Any cause is therefore a **hypothesis, not a finding**. The evidence that exists points to:

1. **Contaminated legacy Elements.** `docs/production-plan.md` §1 says the cover of `Andre` is an illustrated contact sheet, and the cover of `Andre - Jazz Club` is a player screenshot with grey-haired male portraits as secondaries (IDs 323415933655261 and 323336237505580).
2. **Two-face composition.** The user's own render is an OTS frame with a second face in the foreground, which invites identity blending.
3. **Reversed axis and a warm-bokeh "bar" look** in that render, which match the "Jazz Club" Element name.

Supply the clip or ID, or close the item as unrecoverable. Do not spend on a speculative repair.

---

## 11. Per-slot continuity table (all 41 slots)

Legend:
- **Characters:** A = Andre, F = figure. Ⓢ = speaks on screen; (os) = offscreen voice.
- **Face-rule risk:** H / M / L.
- **Axis:** `A SL→CR` = Andre screen-left, looking camera-right. `F SR→CL` = figure's eyes screen-right, looking camera-left. "neutral" = insert.
- **Wardrobe:** "A-D02" = the §2.1 look.
- **Table:** "anchor" = J26_2 state, stain + chip visible, Andre's half empty.
- **Light:** values are the §6 proposals; ⚠ marks an open conflict.
- **Line-to-slot:** v1 placement; v2 needs re-timing (CB-10).

| Slot | t (s) | Characters / audio | Face-rule risk | Wardrobe | Props (figure's half) | Table | Light | Axis | Transition in → out |
|---|---|---|---|---|---|---|---|---|---|
| IN-01 | 0–4 | A hand only; present room tone | L | A-D02 cuff + band | none (vase? ⚠CB-23) | anchor, clean | present ⚠ morning vs dusk | neutral; A hand from frame-left | Fade-in → insert continues |
| IN-02 | 4–8 | A Ⓢ/(os) IN-L01 | M (glass wall behind A, CB-18) | A-D02 | — | anchor | present, key camera-left | A SL→CR | — → IN-03 |
| IN-03 | 8–12 | Table insert; IN-L01 tail; sound falls away | L | A hand | none | anchor | present → Rome | neutral | **Locked insert match cut** → C-01 |
| C-01 | 12–16 | F below neck; C-L01 (os)? ⚠ | **H** (head completion, sun/lamp head shadow) | F toga, ring (right hand) | wax diptych, stylus, oil lamp | anchor + C props | oil lamp ⚠ vs morning sun | neutral; F hand from frame-right | Insert (same as IN-03) → C-02 |
| C-02 | 16–26 | A Ⓢ C-L02 | M (polished/bronze behind A) | A-D02 | — | anchor (edge in frame) | warm, key camera-left | A SL→CR | — → C-03 |
| C-03 | 26–30 | F eyes A "It survives" ⚠ cue early | M (crop creep) | — | — | — | warm lamp from camera-right (J11_1) | F SR→CL | — |
| C-04 | 30–38 | A listens C-L03 (os), begins C-L04 | M | A-D02 | — | anchor | as C-02 | A SL→CR | — |
| C-05 | 38–42 | F eyes B "survive you?" | M | — | — | — | as C-03 | F SR→CL | — |
| C-06 | 42–49 | Hand(s) on table; C-L04 tail (os) | **H** (oil, bronze, ring, fibula reflections) | whose hand? ⚠CB-24 | as C-01 | anchor | as C-01 | neutral | — |
| C-07 | 49–54 | A closing look → insert tail | M | A-D02 | — | anchor | as C-02 | A SL→CR | Lamp flicker/steppe wind bridge → **insert** → K-01 |
| K-01 | 54–58 | F below neck; K-L01 (os)? | **H** | F deel ⚠ blue/brown; no ring? | bowl, map, tallow candle | anchor + K props | firelight from camera-right | neutral | Insert → — |
| K-02 | 58–68 | A Ⓢ K-L02 (9.2 s scratch) | M | A-D02 (navy under fire) | — | anchor | amber, key camera-left; no flicker across eyes | A SL→CR | — |
| K-03 | 68–72 | F eyes A "larger than you can picture" ⚠ | M | — | — | — | fire from camera-right (J13) | F SR→CL | — |
| K-04 | 72–80 | A listens K-L03, starts K-L04 | M | A-D02 | — | anchor | as K-02 | A SL→CR | — |
| K-05 | 80–84 | F eyes B ⚠ cue now in K-L02 (CB-10) | M | — | — | — | as K-03 | F SR→CL | — |
| K-06 | 84–91 | Hand loosens; K-L04 tail | **H** (liquid in bowl, brass fittings) | ⚠ whose hand | as K-01 | anchor | as K-01 | neutral | — |
| K-07 | 91–96 | A holds → insert | M | A-D02 | — | anchor | as K-02 | A SL→CR | Fire out/room air → **insert** → G-01 |
| G-01 | 96–100 | F below neck; G-L01 (os)? | **H** | F doublet, collar, inked cuffs | manuscripts (unreadable), inkwell, goose quill, compass | anchor + G props | cool daylight ⚠ vs dusk | neutral | Insert → — |
| G-02 | 100–110 | A Ⓢ G-L02 | **M–H** (window behind A reflects F, CB-18) | A-D02 | — | anchor | cool day, key camera-left | A SL→CR | — |
| G-03 | 110–114 | F eyes A "more interesting" | M | — | — | — | cool day from camera-right (J15) | F SR→CL | — |
| G-04 | 114–122 | A listens G-L03, starts G-L04 | M–H | A-D02 | — | anchor | as G-02 | A SL→CR | — |
| G-05 | 122–126 | F eyes B ⚠ cue "does not settle" falls in G-06 | M | — | — | — | as G-03 | F SR→CL | — |
| G-06 | 126–133 | Hand + blank page; G-L04 tail | **H** (ink surface, brass) | ⚠ whose hand | as G-01 | anchor | as G-01 | neutral | — |
| G-07 | 133–138 | A respect → insert | M | A-D02 | — | anchor | as G-02 | A SL→CR | Paper → shutter wind → **insert** → N-01 |
| N-01 | 138–142 | F below neck (seated, not standing); N-L01 (os)? | **H** | F green coat ⚠ cut; no rings | Code volume (unreadable spine), candlestick, (map? ink pot? ⚠) | anchor + N props | grey sea light, camera side | neutral | Insert → — |
| N-02 | 142–152 | A Ⓢ N-L02 | **M–H** (shutter glass behind A) | A-D02 | — | anchor | grey, key camera-left (**not** "over left shoulder", CB-08) | A SL→CR | — |
| N-03 | 152–156 | F eyes A "outlives your throne" ⚠ early | M (**recast pending**, D05) | — | — | — | grey from camera-right | F SR→CL | — |
| N-04 | 156–164 | A listens to N-L03 ("And you…"), N-L04 | M–H | A-D02 | — | anchor | as N-02 | A SL→CR (eyes may drop, not cross) | — |
| N-05 | 164–168 | F eyes B "after who pays it" | M | — | — | — | as N-03 | F SR→CL | — |
| N-06 | 168–175 | Hand stops above book | **H** (brass candlestick, buttons, star) | ⚠ whose hand | as N-01 | anchor | as N-01 | neutral | — |
| N-07 | 175–180 | A closes → insert | M | A-D02 | — | anchor | as N-02 | A SL→CR | Wind → O weather ⚠ → **insert** → O-01 |
| O-01 | 180–184 | F below neck; O-L01 (os)? | **H** (overhead source = head shadow on table; head silhouette spec, CB-02) | F tweed, tie, watch ⚠ pocket vs wrist; hat? | closed notebook, unbranded pack, pocket watch, ashtray, cable | anchor + O props | pre-dawn ⚠ vs night/tungsten | neutral | Insert → — |
| O-02 | 184–194 | A Ⓢ O-L02 (11.9 s scratch > slot) | **M–H** (window behind A) | A-D02 | — | anchor | pre-dawn, key camera-left | A SL→CR | — |
| O-03 | 194–198 | F eyes A "Hiroshima" ⚠ ~8 s late | M (hat-brim continuity) | — | — | — | pre-dawn window camera-right (J19) | F SR→CL | — |
| O-04 | 198–206 | A listens O-L03, O-L04 | M–H | A-D02 | — | anchor | as O-02 | A SL→CR | — |
| O-05 | 206–210 | F eyes B "I can't tell you that" | M | — | — | — | as O-03 | F SR→CL | — |
| O-06 | 210–217 | Hand loses tension; ≥4 s silence | **H** (watch, ashtray, lighter, bulb glass) | ⚠ whose hand | as O-01 | anchor | as O-01 | neutral | — |
| O-07 | 217–222 | A acknowledges → insert | M | A-D02 | — | anchor | as O-02 | A SL→CR | Silence → present room tone → **insert** → OUT-01 |
| OUT-01 | 222–228 | A Ⓢ OUT-L01 (9.7 s scratch, spans OUT-02) | M (glass wall) | A-D02 | — | anchor (vase = IN state) | present = IN-02 | A SL→CR | Insert → — |
| OUT-02 | 228–234 | Empty chair (screen-right); OUT-L01 (os) | L–M (no ghost/silhouette/reflection) | — | none | anchor | present | chair screen-right | — |
| OUT-03 | 234–240 | Table hold, fade, credits | L | — | none | anchor | present | neutral | Fade on wood, never through a face |

## 12. Continuity breaks and ambiguities (with citations)

Severity: **C** = critical (blocks generation), **H** = high, **M** = medium, **L** = low.

| ID | Sev | Finding | Evidence |
|---|---|---|---|
| CB-01 | C | Four R2 "below-neck" wardrobe sheets show chin, mouth or beard, and the scene bibles cite them as anchors. | `02_references/wardrobe/R2-wardrobe-{caesar-roman,genghis-mongol,galileo-scholar,napoleon-uniform}.jpg`; wardrobe rows in `03_bibles/scene-bibles/*.md`; FRAMEWORK "exclude chin/neck" |
| CB-02 | C | The Oppenheimer spec writes a head silhouette into the frame; the R2 sheet shows the head, neck and readable text. | `scene-bibles/oppenheimer.md` wardrobe row; `R2-wardrobe-oppenheimer-tweed.jpg`; `docs/visual-contract.md` figures §2 |
| CB-03 | H | The D02 wardrobe artifact contains another man's lower face plus text labels, so it is unsafe as an image input for Andre's beard or identity. | `R2-wardrobe-andre-modern.jpg`; `00_brief/decisions/D02-wardrobe.json` |
| CB-04 | H | OTS/third-face composition references remain in the Andre folder. | `andre/synthetic/R2-andre-seated-conversational.jpg`; inbox Kling render (labelled) |
| CB-05 | H | Table design drift: R2 plates and every R2 wardrobe sheet use other tables. | `table/R2-plate-rome-villa.jpg`, `R2-plate-present-day-table.jpg`, `R2-andre-table-cinematic.jpg`, R2 wardrobe; D04 |
| CB-06 | H | Light and time of day conflict in C, G, O and present (see §6). The D05 eye bases already embed lamp / day / pre-dawn light. | `scene-bibles/*.md` §2; `table-and-continuity.md` §3; `source/atlas.json` scenes.light; eye prompts in `history-eyes/*/*.json`; era plates |
| CB-07 | M | Oppenheimer setting: "night of July 15" vs pre-dawn light (which would be 16 July); weather (storm vs dry pre-dawn). | `manifest.json` chapter O; `oppenheimer.md`; `07_generations/requests/R1-J31…`, `R1-J20…` |
| CB-08 | M | Napoleon key "over his left shoulder" contradicts the camera-left key geometry. | `scene-bibles/napoleon.md` Andre Framing; `character-andre.md` §3 |
| CB-09 | H | Canonical v2 script vs v1 text in the scene bibles, atlas source, manifest and shot-list descriptions. | `01_script/script-en.md`, `dialogue-lines.csv` (v2) vs `scene-bibles/*.md` §3, `05_storyboard/source/atlas.json` performance/cueA/cueB, `manifest.json` shots, `shot-list.csv` |
| CB-10 | H | v2 cue words don't land in the X-03/X-05 windows; O-L02 overflows O-02; the X-L01 placement disagrees between bible and atlas. | `04_audio/scratch/edge-tts-v2/provenance.json`; `atlas.json` performance; scene bibles §3; `manifest.json` chapterSlotSeconds; D10 |
| CB-11 | M | N-L03 "the price" has no antecedent after the v2 rewrite. | `dialogue-lines.csv` N-L02..N-L04; v1 in `reports/art-direction-v1/script-en-v1-before.md` (per script header) |
| CB-12 | M | Edition H has no current text; IN/OUT language and the Napoleon target are undecided. | D07; `01_script/translations/*` headers; `language-matrix.csv`; `language-strategy.md` |
| CB-13 | M | Prop contradictions: quill (brass vs goose), astrolabe vs compass, pocket watch vs wristwatch, lighter, readable text (tablet incisions, Code spine, Galileo sheets, Oppenheimer pack/notebook), codex book in Rome, Napoleon map/ink pot, Genghis dagger. | `table-and-continuity.md` §3; `scene-bibles/*.md`; R1-J23/J25, R2 sheets/plates; v2 visual rule 4 |
| CB-14 | M | Jewellery is undecided or contradictory (Genghis/Napoleon rings, Oppenheimer ring, Caesar ring hand/metal); Andre's "silver band" is unverified against his real hand. | `table-and-continuity.md`; J22/J24 contact; R2 Oppenheimer; D02; `inbox/.../20240202_015214.jpg` |
| CB-15 | M | Genghis seat "low stool/cushion" can't reach a travelling 75 cm table; J22 kneels; the J28 plate has a Chinese-style chair. | `table-and-continuity.md` §1/§3; `historical-costumes_contact.jpg`; `era-plates_contact.jpg` |
| CB-16 | H | No floor plan: opposite long sides vs corner vs ends; which edge carries the chip and stain on Andre's side is undefined. | `R2-andre-table-cinematic.jpg`; era plates; R2 present plate; `R1-J26-table-anchor_2.png`; `07_generations/requests/R1-J26…` ("near-left front edge") |
| CB-17 | M | Atlas Andre references contradict D09 or the table geometry. J08_1 (all X-02 cards) has Andre right of centre with the table behind his gaze; J04/J06 are studio or bar backgrounds. | `05_storyboard/source/atlas.json` shotDirections; `R1-J08…_1.png` |
| CB-18 | H | **New:** windows or glass behind Andre in his singles can reflect the off-camera figure (G, N, O, present). | Plates `R1-J29/J30/J31/J32`, `R2-plate-present-day-table.jpg`; visual contract figures §4 |
| CB-19 | H | Reflective props on the table in every era (list in §4.2). | `table-and-continuity.md` §3; scene bibles |
| CB-20 | M | Oppenheimer hat: the eye base has a hat-brim shadow; no costume has a hat. | `history-eyes/oppenheimer/R1-J19…json` prompt; J25; R2 |
| CB-21 | L | The N and O eyes are both pale blue in adjacent chapters (Galileo's also read pale); Napoleon recast pending. | `historical-eyes_contact.jpg`; D05 |
| CB-22 | M | Ambience conflicts (Rome, Galileo, Napoleon, Oppenheimer) between the bibles and the atlas. | `scene-bibles/*.md` §3; `source/atlas.json` scenes.sound; `table-and-continuity.md` §2 |
| CB-23 | M | Present-day open/close state undefined: vase, chair count, morning vs dusk. | `table-and-continuity.md` §3; `R1-J32…png` vs `R2-plate-present-day-table.jpg` |
| CB-24 | M | X-06 hand ownership is ambiguous (the atlas uses figure costume refs but the action text mentions Andre); no slot is reserved for the D04 insert match cut. | `source/atlas.json` C-06…O-06; `manifest.json` shots; D04 |
| CB-25 | L | No rule against era props marking the table (wax, ink, ash, oil, wet rings). | `table-and-continuity.md` |
| CB-26 | L | Navy blazer colour will shift under the era palettes; no grade anchor is defined. | `character-andre.md` §3 lighting |
| CB-27 | L | Scratch track uses one voice for all figures and a US voice for Andre; final timing will shift. | `04_audio/scratch/edge-tts-v2/provenance.json`; D06 |
| CB-28 | M | Failed clip absent; causes are hypotheses only (§10). | `inbox/failed-clips/`; `README.md`; `docs/production-plan.md` §1 |
| CB-29 | M | 4:1 eye strips vs 16:9 video frames: the frame either crops beyond brow/lid or needs letterboxing. Undefined. | `history-eyes/*` (strip format); `manifest.json` framingRestriction "Eyes-only safe crop" |
| CB-30 | L | Andre's age and hair colour in the bible are unsourced impressions; the 2023 photos show lighter hair. | `character-andre.md` §1; inbox photos |

## 13. Pre-generation checklist — paste into every shot-prompt review

```
SHOT ______  CHAPTER ______  REVIEWER ______  DATE ______   (all boxes must be ✔ or "N/A + reason")

IDENTITY / REFERENCES
[ ] Andre identity inputs = only D01 real photos (or the approved Element) — no R1/R2 synthetic, no 2021–23 photos, no group photos, no Kling render
[ ] No image input shows a second person's head/face (OTS, background people, R2 wardrobe chins/mouths, quarantined originals)
[ ] Figure eye input = the D05 base (or its approved minimal delta); Napoleon = approved recast only
[ ] Each reference listed with path + sha256 + decision ID

ANDRE
[ ] Grooming D03: short textured hair, 3–5-day stubble — same length as the previous accepted shot
[ ] Wardrobe D02: navy blazer open, 3 horn cuff buttons, charcoal shirt 1–2 buttons open, band on left ring finger (as confirmed by Andre), no watch/logo
[ ] No glasses, no hand over mouth/chin during speech, no portal/morph/glow over face
[ ] Angle within the tested envelope (front/¾); one action + one camera behaviour; no orbit

FACE RULE (figures)
[ ] Below-neck frame top ≤ mid-chest; no chin/neck/beard/mouth; no head silhouette; no head shadow on table/wall
[ ] Eyes shot: brow to just under lower lid; no nose tip/nostril/mouth; locked camera, no pull-back; ≤1 blink; gaze camera-LEFT
[ ] No reflective surface can show a face: windows/glass behind Andre, polished brass/silver, watch, ashtray, lighter, liquids, ink, oil, bulb glass, mirrors, portraits
[ ] Prompt contains "no other people, no faces, no reflections of faces, no portraits, no text"

AXIS / GEOMETRY
[ ] Andre screen-LEFT looking camera-RIGHT (15–35°); figure eyes screen-RIGHT looking camera-LEFT
[ ] Inserts: Andre's hands from frame-left, figure's from frame-right; camera on the same side of the line
[ ] Seating per the floor plan (once decided); table edge distance to Andre's torso unchanged

TABLE (D04)
[ ] Same pale oak J26_2: planks, grain direction, ring stain + chip visible and in the same place
[ ] Andre's half empty except hands; era props only on the figure's half; nothing readable
[ ] No new marks (wax/ink/ash/oil/wet rings); no table design change (trestle/slab/dark wood = reject)

LIGHT / TIME
[ ] Chapter light = the decided chapter light (§6), source on the camera side: Andre keyed camera-left, figure camera-right
[ ] No moving flame/shadow across eyes; skin readable; blazer colour graded to the chapter anchor
[ ] Time of day and date consistent with the chapter (e.g. O pre-dawn ⇒ 16 July)

PROPS / COSTUME (figure)
[ ] Only bible-listed props for this era; prop variants resolved (quill, compass, watch, rings, hat)
[ ] No anachronistic carry-over from another era

DIALOGUE / TIMING
[ ] Shot covers the v2 line(s) mapped to it (canonical CSV text, not bible v1 text)
[ ] Cue word for an eye reaction lands inside this shot (or the planned L-cut is noted)
[ ] Mouth visible only if the speech route is approved; otherwise neutral mouth / offscreen line
[ ] Edition H: picture length fits the longest language version; subtitle-safe area free of eye strip/mouth

TRANSITION
[ ] If X-07/X-01: ends/opens on the locked insert (hand + stain + chip, same lens height & crop)
[ ] Sound bridge per §7; no dissolve through any face

REVIEW AFTER GENERATION (not optional)
[ ] Full playback at normal speed + frame-by-frame for every frame of X-01/X-03/X-05/X-06 and any shot with glass/metal
[ ] First and last frame checked for face/axis/table/wardrobe drift; accept/reject recorded with reason
```

---

*End of draft. Owner of any adoption: continuity + producer, via decision records. Suggested first decisions:*
- *CB-01/02/03 (crop or replace the R2 sheets)*
- *CB-06/07 (chapter light and date, following the D05 eye bases)*
- *CB-16 (floor plan and chip side)*
- *CB-09/10 (v2 line-to-slot map from the scratch track)*
