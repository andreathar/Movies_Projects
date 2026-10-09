# Scene Bibles — integrated revision r1 (Caesar, Genghis, Galileo, Napoleon; Oppenheimer pending)

> **STATUS: PROPOSED — not approved.** New file; nothing was overwritten. Integrates the four `*-v3-proposta.md` dialogue-sound files into ONE revision, with §3 reduced to **line IDs only** (no spoken text) anchored to the hash of `01_script/dialogue-lines.csv` (corrects audit F05). Author role: dialogue-sound/continuity, 2026-10-09. Nothing here is approved unless it cites a decision ID in `00_brief/decisions/`; decisions this file relies on: D01 identity set, D02 wardrobe, D03 grooming, D04 table + travel rule, D05 eye bases, D09 screen axis. Likeness approval (pilot) remains Andre's. **D16–D19 are not touched, and D17/D18/D19 are proposals only.**

## 0. Provenance, hashes and rules

**Canonical dialogue source (read-only):**

| File | sha256 |
|---|---|
| `01_script/dialogue-lines.csv` (all line text lives here) | `d14322550e9f52db6b88a8db3e5ace84e3b666900046edf9532c237f2f1a83f6` |
| `01_script/script-en.md` | `a0217c6f2e8d73efce91ea34c1e8fbd01acc7aa381f6d191c10112af1ef711e1` |

**Rule — no dialogue text in this file.** §3 cites line IDs and a few trigger anchors in §1 are quoted fragments of the canonical lines (each machine-checked to occur in the CSV at the hash above). If the CSV hash changes, re-verify every anchor before using this file; **on any conflict the CSV wins**. All line audio is edge-tts v2 scratch/guide (`approved=false`); slot seconds are proposals and approved audio controls the edit.

**Base files (preserved, not edited):**

| File | sha256 now | Notes |
|---|---|---|
| `caesar.md` (v1) | `ea0f972b3d8bc9bf77ef3a49e30b4bc76b14158bdc04b65525a44274017c9e52` | v1 hash at v3 authoring: `cf01c1abf8acf63a01a9afe4b3096beb41f6dee840fc08b747088582fe91328f` |
| `genghis.md` (v1) | `27d2b59bca35a33fbc2ee4bd38ff293f5d482606f73a955a6623812cadfc2084` | v1 hash at v3 authoring: `8c3a56400ed32301e86d39412a169048d78c7af36d516a422b7e08c7140ce042` |
| `galileo.md` (v1) | `15fe262629e0170c5d7f33c9ea48adb18fdb739401aed1a0ccd10195850d2516` | v1 hash at v3 authoring: `76126a010e9adb305970bc22927979d1e85b2485c8e0b7b52db56978dd8d4f00` |
| `napoleon.md` (v1) | `7dbb63e5252efab4e9ba564f8bfef73ab422bc7c3cde9be36c31da7b30eb8a2f` | v1 hash at v3 authoring: `c318bdba1065d5b1cc657c7ad0522ec2400291bd184471b9f65c215727c88bc8` |
| `oppenheimer.md` (v1) | `f64813d94f57695313eb78401ccd24a54f15286f7f5a66f0ea2ef0b09ceac2a5` | no v3 exists |
| `caesar-v3-proposta.md` | `72448c774ce1d01fed2a79aad7ee57e517f26ad15197f9b610354cda0f0bf17b` | integrated here |
| `genghis-v3-proposta.md` | `0b9ce9eef87e606b18a4040f09f63b6e794f2a5baf15752f5df2c87e973f2c92` | integrated here |
| `galileo-v3-proposta.md` | `706c6dfa0d0b42d63b241329378471d515f318206ece701d868224977171ced4` | integrated here |
| `napoleon-v3-proposta.md` | `4aeb5c0df40e6481ac5df6e6970fe49e374a4ca13f78ceceeca50130ac0bad66` | integrated here |
| `caesar-v2-proposta.md` / `genghis-v2-proposta.md` / `galileo-v2-proposta.md` / `napoleon-v2-proposta.md` / `oppenheimer-v2-proposta.md` | `da36061d6648…` / `521b48552306…` / `7605a5078f83…` / `a370dc888467…` / `ba10a8516c7f…` | historian+continuity back-view/legacy proposals; consulted, not copied |
| `../table-and-continuity-v2-proposta.md` | `6dfce7227859eec4fff0c2718ad0e70fabf83d7e99defdbec1b65247078db9eb` | geometry/grammar source for BV-O/BV-R/BV-W |

**Why the v1 hashes differ from the v3 headers:** v1 files were changed by the D02 wardrobe reconciliation committed in `0f291c1` (Andre Framing reference path + a "Wardrobe reconciliation" note per file). The v3 proposals cite the older hashes, but their carried §2/§4 were machine-compared with the *current* v1 §2/§4 and are identical, so no content was lost. §2 and §4 below are copied from the **current** v1 files.

**What this revision changes vs v1 (summary, no dialogue text):** (1) §3 now cites line IDs only; the four `*-L04` lines are played whole in their slot instead of being split around the eyes; (2) §1 eye-cue triggers are re-anchored on the canonical lines and moved to AFTER a back-view beat (rule above); (3) the v1 eyes-only slots become back-view holds, table inserts or Andre beats; (4) §2/§4 are carried unchanged (every `02_references/…` path cited in them was checked to exist), with open flags listed under each chapter's "Open flags" rather than silently fixed.

## Eye-cue placement rule (applies to every cue in each chapter’s §1 and §3)

Source: Andre's creative direction of 2026-10-09 12:35 as recorded in `memory/STATE.md` ("Current creative direction") and carried by the dialogue-sound assignment; consistent with the editor+QC triage `08_edit/reviews/2026-10-09-revisao-nova-direcao/review.md`. **D19 (the eye-reaction rule) is PROPOSED, not recorded**; D17 (table layout) and D18 (Galileo's blurred nape) are also proposed only. Nothing below cites them as decisions.

1. **Order: back view → eyes.** The figure's first presence in each chapter is from behind (slot `x-01`). Each eye insert is immediately preceded by a back-view beat (≥ ~1.5 s) in which the figure's back/shoulder is the subject (BV-O / BV-R / BV-W / BL-n grammar: `../table-and-continuity-v2-proposta.md` and each figure's `-v2-proposta.md` §1; all still proposals). Never open a chapter or a beat on the eyes, and never cut to the eyes straight from Andre's close shot.
2. **Short.** One eye insert = 1.5–2 s (hard max 2.5 s). At most two eye inserts per chapter (cue A, cue B). The editor lane reports (Parley message 8; I could not verify it) that Andre chose in chat to limit Galileo's eyes B to 2 s; this is not a recorded decision.
3. **Trigger = what the eyes react to.** The trigger phrase lands over the back-view beat (or BV-O); the eyes come after it, as the reaction (reaction never precedes its cause — audit F03). Andre's line may continue offscreen over the eyes (J-cut); the line is never cut or re-ordered to make room for the eyes.
4. **Holds and sustained stillness** named in the canonical cue are played by the figure's back (the body stops moving), not by lengthening the eye shot.
5. Unchanged: D05 eye bases, eyes-only safe crop, eyes screen-right with gaze camera-left (D09); zero full face, profile or reflection of any historical figure.

---

# Chapter C — Julius Caesar

**Chapter:** C — Julius Caesar  
**Fictional Setting:** Rome, early 44 BCE (prior to the Ides of March, 44 BCE)  
**Location:** Private atrium in a Roman domus / villa on the Palatine Hill  
**Target Duration:** 42 seconds  
**Slots (proposal, editor to confirm):** `C-01` (~4s), `C-02` (~12s), `C-03` (~3s), `C-04` (~9s), `C-05` (~4s), `C-06` (~5s), `C-07` (~5s) — total 42s

## §1 Dramatic progression & emotional arc

- **Core Question:** *Does victory leave behind a republic or personal power?*
- **Caesar's Motivation:** Preoccupied with his legacy, reforms, and ultimate stature after the civil wars and appointment as dictator (46–44 BCE)[1].
- **Eye Cue Progression (eyes-only safe crop; short reaction after a back-view beat — rule above):**
  - **Cue A (`C-02`, inside the line, J-cut, eyes 1.5–2 s):** *Focused confidence.* Trigger: `C-L02` "It survives." lands on BV-O → back-view beat (~1.5 s; toga shoulder lifts slightly) while Andre continues offscreen → **eyes A, 1.5–2 s** under the rest of `C-L02` → back to BV-O for its last sentence.
  - **Cue B (`C-05`, eyes 1.5–2 s):** *Certainty slips — he hears that he became a precedent; no caricatured rage.* Trigger: `C-L04` "survive you?", held still through "other men". At the trigger the toga shoulder in the foreground stops moving (the slip, played from behind) and stays still; `C-05` = back-view beat (~2 s, stillness) → **eyes B, 1.5–2 s**, after `C-L04` has ended.

## §2 Visual Contract & Atmosphere

> **R2 references (2026-10-09, accepted candidates, decision D05/D04):** eyes state A base → `02_references/history-eyes/caesar/` (R1 base per D05); eyes state B → `R2-J02-eyes-caesar-uncertainty-B_1_eyescrop.png`; hand/table insert → `02_references/inserts/R2-J10-insert-caesar_1.jpg`. Gaze in stills reads near-centre; video prompts must set camera-left.

| Attribute | Production Requirement | Reference Anchor |
|---|---|---|
| **Setting Plate** | Classical Roman villa atrium: fluted Roman stone columns, compluvium skylight pouring warm Mediterranean morning sun onto terracotta tile floor, stucco wall with faded Pompeian red murals. | `02_references/table/R2-plate-rome-villa.jpg` |
| **Table Props** | Wooden diptych wax tablet with Latin text incisions, bronze stylus, terracotta oil lamp with subtle olive oil flame. | Table Bible |
| **Caesar Wardrobe (Below Neck Only)** | Fine off-white wool tunic with broad purple *latus clavus* stripe; heavy cream wool *toga praetexta* with Tyrian purple border pinned at the shoulder with a round gold fibula. Right hand resting on table with Roman signet ring. | `02_references/wardrobe/R2-wardrobe-caesar-roman.jpg` |
| **Caesar Eyes Reference** | Extreme close-up (macro crop from brow to lower eyelids, zero nose, mouth, or jaw). Mediterranean Roman bone structure, piercing dark brown irises, stern brow. | `02_references/history-eyes/caesar/R1-J11-eyes-caesar-command_1_eyescrop.png` & `R1-J12-eyes-caesar-uncertainty_1_eyescrop.png` |
| **Andre Framing** | Medium close-up, seated screen-left, looking camera-right. Grey pinstripe jacket, white finely striped shirt, open collar, no tie (D02). Soft warm natural key light from camera-left. | `02_references/andre/approved/cover_20240202_015341_hs34.jpg` |

---

## §3 Dialogue & timing (Edition E - English) — line IDs only

Line text: `01_script/dialogue-lines.csv` sha256 `d14322550e9f52db6b88a8db3e5ace84e3b666900046edf9532c237f2f1a83f6`. BV-O / BV-R / BV-W / BL-n per the v2 continuity proposal (not approved).

| Slot | ~s | Line ID | Speaker | Action |
|---|---|---|---|---|
| `C-01` | 4 | — | Ambient / back view | Caesar's first presence is from behind: BV-O phase 1 — toga-draped LEFT shoulder/arm and purple border in the right third, head out of frame, Andre at the table (BV-W in phase 2). Ambient Roman morning birds and distant market hum. |
| `C-02` | ~12 | `C-L01`<br>`C-L02` | Caesar (O.S.)<br>Andre | C-L01 over BV-R starting on the toga border, BL-1 → rack to Andre. C-L02 over BV-O, uninterrupted. Eye cue A inside C-L02 (§1): trigger on BV-O → back-view beat ~1.5 s → eyes A 1.5–2 s (gaze camera-left) under Andre O.S. → BV-O for the last sentence. |
| `C-03` | ~3 | — | Caesar (back) | Back-view hold as the end of C-L02 lands (no eyes). Optional legacy intercut per `caesar-v2-proposta.md`. Replaces the v1 eyes-only slot. |
| `C-04` | ~9 | `C-L03`<br>`C-L04` (whole) | Caesar (O.S.)<br>Andre | C-L03 over back view BL-1. C-L04 over BV-O, uninterrupted, played whole (v1 split it around the eyes — removed). At the cue-B trigger the foreground toga shoulder stops moving; stillness held through the end of C-L04. |
| `C-05` | 4 | — | Caesar (back → eyes) | Back-view beat ~2 s (stillness) → eye cue B, 1.5–2 s. No rage. Gaze camera-left. |
| `C-06` | ~5 | — | Table | Close-up of table, hand tension on wood (insert R2-J10). No dialogue — v1 placed the end of C-L04 here; removed. |
| `C-07` | 5 | — | Andre | Andre's restrained closing look. Sound bridge into Mongolian steppe wind. |

## §4 Historical Anchor & Research Citations

- **Assassination Context:** March 15, 44 BCE (Ides of March). The scene is set in early 44 BCE when Caesar held supreme power as *dictator (46–44 BCE)[1]*.[1]
- **Reforms & Senate Dynamics:** Reforms included the Julian calendar, provincial reorganization, and debt relief, balanced against the disenfranchisement of traditional senatorial republican norms.[1]

> Wardrobe reconciliation: D02 governs new production. Dark-shirt synthetic studies are retired; see `02_references/legacy/retired-dark-wardrobe/manifest.json`. The approved photo anchors face and clothing, not seated table geometry.

### Open flags (carried, NOT resolved here)

- Fibula: `caesar-v2-proposta.md` proposes removing the "round gold fibula" (a toga is draped; no source found) and using a *sella curulis* (backless stool) — flagged for historian/art-director; the §2 text below is v1 and still names the fibula.
- Wreath: v2 proposes the laurel wreath worn (sourced: Suetonius 45); not in §2 below.
- Core question echoes the removed v1 phrase "what victory leaves behind" — cosmetic; wording kept as carried.

---

# Chapter K — Genghis Khan

**Chapter:** K — Genghis Khan  
**Fictional Setting:** A military campaign ger (yurt), Western Xia / Zhongxing (Xi Xia capital)[15] campaign, summer 1227  
**Location:** Central headquarters tent on the arid steppe borderlands  
**Target Duration:** 42 seconds  
**Slots (proposal, editor to confirm):** `K-01` (~4s), `K-02` (~13s), `K-03` (~4s), `K-04` (~9.5s), `K-05` (~3.5s), `K-06` (~4s), `K-07` (~4s) — total 42s

## §1 Dramatic progression & emotional arc

- **Core Question:** *Can an empire connect the world and destroy it at the same time?*
- **Khan's Motivation:** Near the end of his life (he died in August 1227); anxious about whether his sons (Jochi, Chagatai, Ögedei, Tolui) will preserve his united realm (*Yeke Monggol Ulus*).
- **Eye Cue Progression (eyes-only safe crop; short reaction after a back-view beat — rule above):**
  - **Cue A (`K-02`, inside the line, J-cut, eyes 1.5–2 s):** *Controlled pride.* Trigger: `K-L02` "larger than you can picture" lands on BV-O → back-view beat (~1.5 s; shoulders square) under Andre O.S. → **eyes A, 1.5–2 s** under the same sentence → back to BV-O for the last sentence of `K-L02`.
  - **Cue B (`K-03`, eyes 1.5–2 s):** *A single restrained blink; no tear.* Trigger: `K-L02` "no longer there"; the canonical note adds stillness through `K-L04` "the dead speak". `K-03` = back-view beat (~2 s; the body settles after the trigger) → **eyes B, 1.5–2 s, one restrained blink**. The stillness through "the dead speak" is carried by the motionless back through `K-04`/`K-05` — no further eye shot. **OPEN (P-K, Andre/director):** option 2 would keep the trigger from behind only and move the blink to after "the dead speak" (spreading the eye beats over `K-02` and `K-05`).

## §2 Visual Contract & Atmosphere

> **R2 references (2026-10-09, accepted candidates, decision D05/D04):** eyes state A base → `02_references/history-eyes/genghis/` (R1 base per D05); eyes state B → `R2-J03-eyes-genghis-recognition-B_1_eyescrop.png`; hand/table insert → `02_references/inserts/R2-J11-insert-genghis_1.jpg`. Gaze in stills reads near-centre; video prompts must set camera-left.

| Attribute | Production Requirement | Reference Anchor |
|---|---|---|
| **Setting Plate** | Nomad ger interior: thick multi-layered wool felt walls, willow lattice frame (*khana*), stone hearth fire pit casting warm amber flickering light, smoke gently drafting toward the central roof ring (*toono*). | `02_references/table/R1-J28-plate-tent-1227_1.png` |
| **Table Props** | Coarse stoneware tea/kumis bowl, rolled leather map scroll tied with rawhide string, sheep tallow candle in iron saucer. | Table Bible |
| **Genghis Wardrobe (Below Neck Only)** | Heavy dark brown patterned silk deel lined with wolf fur trim; boiled hardened leather lamellar armor chest plate with antique brass studs; wide studded leather belt with nomad pouch; rough calloused hand resting on table. | `02_references/wardrobe/R2-wardrobe-genghis-mongol.jpg` |
| **Genghis Eyes Reference** | Extreme close-up macro crop (brow to lower eyelids, zero nose, mouth, or beard). Sun-weathered, wind-creased steppe warrior brow, intense dark golden-brown irises, steady unblinking focus. | `02_references/history-eyes/genghis/R1-J13-eyes-genghis-pride_1_eyescrop.png` & `R1-J14-eyes-genghis-recognition_1_eyescrop.png` |
| **Andre Framing** | Seated screen-left, looking camera-right. Grey pinstripe jacket and white finely striped shirt (D02) catching warm, flickering ember tones from the hearth. | `02_references/andre/approved/cover_20240202_015341_hs34.jpg` |

---

## §3 Dialogue & timing (Edition E - English) — line IDs only

Line text: `01_script/dialogue-lines.csv` sha256 `d14322550e9f52db6b88a8db3e5ace84e3b666900046edf9532c237f2f1a83f6`. BV-O / BV-R / BV-W / BL-n per the v2 continuity proposal (not approved).

| Slot | ~s | Line ID | Speaker | Action |
|---|---|---|---|---|
| `K-01` | 4 | — | Ambient / back view | Khan's first presence is from behind: BV-O phase 1 — fur-trimmed shoulder and sleeve in the right third, head out of frame (BV-W in phase 2). Steppe wind howling softly outside. |
| `K-02` | ~13 | `K-L01`<br>`K-L02` | Khan (O.S.)<br>Andre | K-L01 over BV-R on the fur trim, BL-1 → rack to Andre. K-L02 over BV-O. Eye cue A inside K-L02 (§1): back-view beat ~1.5 s after the trigger → eyes A 1.5–2 s (gaze camera-left) under Andre O.S. → BV-O for the last sentence. |
| `K-03` | 4 | — | Khan (back → eyes) | Back-view beat ~2 s (body settles after the cue-B trigger) → eye cue B, 1.5–2 s: a single restrained blink. No tear. |
| `K-04` | ~9.5 | `K-L03`<br>`K-L04` (whole) | Khan (O.S.)<br>Andre | K-L03 over back view BL-1. K-L04 over BV-O, uninterrupted, played whole. The back stays motionless through the end of K-L04 (canonical stillness, played from behind). |
| `K-05` | ~3.5 | — | Khan (back) | Back-view hold, no eyes (replaces the v1 eyes-only slot). Optional legacy intercut per `genghis-v2-proposta.md`. |
| `K-06` | ~4 | — | Table | Hand loosens on the table grain (insert R2-J11). No dialogue — v1 placed the end of K-L04 here; removed. |
| `K-07` | 4 | — | Andre | Andre holds the consequence; quiet match cut. |

## §4 Historical Anchor & Research Citations

- **Succession & Imperial Growth:** The division among his sons and the continued expansion under Ögedei and Kublai Khan created the Pax Mongolica, facilitating unprecedented Afro-Eurasian trade and transmission of technology.[2][15]
- **Human Cost of Warfare:** The siege warfare against Khwarazm, Western Xia, and Jin resulted in massive civilian casualties and demographic disruption, documented as an integral facet of his historical legacy.[2][15]

> Wardrobe reconciliation: D02 governs new production. Dark-shirt synthetic studies are retired; see `02_references/legacy/retired-dark-wardrobe/manifest.json`. The approved photo anchors face and clothing, not seated table geometry.

### Open flags (carried, NOT resolved here)

- **Armour — ANDRE/ART-DIRECTOR DECISION PENDING.** `genghis-v2-proposta.md` proposes dropping the lamellar armour for table scenes (no source places armour at a tent table) in favour of a light monochrome robe + dark outer coat; this conflicts with `R2-wardrobe-genghis-mongol.jpg` and with the §2 text below, which is v1 and still names the armour.
- Headwear: v2 records the leather warming cap as sourced (NPM Taipei portrait); not in §2 below. Stool ~45 cm, no backrest (v2; CB-15 resolved).
- J22 blue-vs-brown drift noted in `genghis-v2-proposta.md` (wardrobe ref).

---

# Chapter G — Galileo Galilei

**Chapter:** G — Galileo Galilei  
**Fictional Setting:** Villa Il Gioiello, Arcetri (hills overlooking Florence), late 1634  
**Location:** Private stone study during his lifelong papal house arrest following the 1633 Inquisition trial  
**Target Duration:** 42 seconds  
**Slots (proposal, editor to confirm):** `G-01` (~3s), `G-02` (~12.5s), `G-03` (~4s), `G-04` (~12s), `G-05` (~4s), `G-06` (~3s), `G-07` (~3.5s) — total 42s. The Galileo v2 timeline (editor lane) governs actual timings; it follows the director checkpoint §5 and Andre's chat choices, not this table.

## §1 Dramatic progression & emotional arc

- **Core Question:** *Does silencing a person settle a scientific question?*
- **Galileo's Motivation:** Aged 70, physically exhausted, failing eyesight, isolated in his villa after abjuring his Copernican views before the Holy Office in Rome; desperately wondering whether posterity vindicates his life's work or merely treats him as an heretic.
- **Eye Cue Progression (eyes-only safe crop; short reaction after a back-view beat — rule above):**
  - **Cue A (`G-03`, eyes 1.5–2 s):** *Exhausted attention (not blindness), brightening.* Trigger: `G-L02` "more interesting". `G-L02` plays whole; `G-03` = back-view beat (~2 s; gown shoulders ease) → **eyes A, 1.5–2 s**, brightening as the reaction.
  - **Cue B (`G-05`, eyes 1.5–2 s; reported cap 2 s):** *Quiet renewed resolve.* Trigger: `G-L04` "does not settle a question". `G-L04` plays whole in `G-04`; `G-05` = back-view beat (~2 s) → **eyes B, 1.5–2 s**. Fixes the v1/preview order in which the resolve eyes came before the end of `G-L04` (audit F03).

## §2 Visual Contract & Atmosphere

> **R2 references (2026-10-09, accepted candidates, decision D05/D04):** eyes state A base → `02_references/history-eyes/galileo/` (R1 base per D05); eyes state B → `R2-J04-eyes-galileo-resolve-B_1_eyescrop.png`; hand/table insert → `02_references/inserts/R2-J12-insert-galileo_1.jpg`. Gaze in stills reads near-centre; video prompts must set camera-left.

| Attribute | Production Requirement | Reference Anchor |
|---|---|---|
| **Setting Plate** | Tuscan stone study: vaulted plaster ceiling, arched stone window revealing cypress trees and dusk sky over the hills of Arcetri, brass candle lantern, bookshelves with bound manuscripts. | `02_references/table/R1-J29-plate-arcetri-1634_1.png` |
| **Table Props** | Hand-written manuscript sheets of astronomical diagrams, always out of focus or turned away — no legible invented text (review-findings §4), brass ink pot, goose quill pen, brass drafting compass. | Table Bible |
| **Galileo Wardrobe (Below Neck Only)** | Heavy dark charcoal wool doublet with neat rows of fabric buttons; wide white linen falling collar resting across shoulders; dark scholar's gown; white linen sleeve cuffs with faint brown iron-gall ink smudges; aged, trembling hands resting on papers. | `02_references/wardrobe/R2-wardrobe-galileo-scholar.jpg` |
| **Galileo Eyes Reference** | Extreme close-up macro crop (brow to lower eyelids, zero nose, mouth, or white beard). Aged Tuscan scholar eyes, heavy crow's feet, slight , deep sunken sockets, profound weariness. | `02_references/history-eyes/galileo/R1-J15-eyes-galileo-weariness_1_eyescrop.png` & `R1-J16-eyes-galileo-resolve_1_eyescrop.png` |
| **Andre Framing** | Seated screen-left, looking camera-right. Cool Tuscan evening blue ambient light with warm candlelight on his face and hands. | `02_references/andre/approved/cover_20240202_015341_hs34.jpg` |

---

## §3 Dialogue & timing (Edition E - English) — line IDs only

Line text: `01_script/dialogue-lines.csv` sha256 `d14322550e9f52db6b88a8db3e5ace84e3b666900046edf9532c237f2f1a83f6`. BV-O / BV-R / BV-W / BL-n per the v2 continuity proposal (not approved).

| Slot | ~s | Line ID | Speaker | Action |
|---|---|---|---|---|
| `G-01` | 3 | — | Ambient / back view | Galileo's first presence is from behind: BV-O phase 1 — dark academic gown over the LEFT shoulder/arm in the right third, head out of frame (BV-W in phase 2). Soft Tuscan evening crickets and church bells. |
| `G-02` | ~12.5 | `G-L01`<br>`G-L02` | Galileo (O.S.)<br>Andre | G-L01 over BV-R on the gown shoulder, BL-1 → rack to Andre. G-L02 over BV-O, uninterrupted. |
| `G-03` | 4 | — | Galileo (back → eyes) | Back-view beat ~2 s → eye cue A, 1.5–2 s: exhausted attention, not blindness, brightening after the cue-A trigger. Gaze camera-left. |
| `G-04` | ~12 | `G-L03`<br>`G-L04` (whole) | Galileo (O.S.)<br>Andre | G-L03 over back view BL-1. G-L04 over BV-O, uninterrupted, played whole (v1 split it around the eyes — removed). Guide audio of G-L04 has doubtful words (ADR later; see STATE.md). |
| `G-05` | 4 | — | Galileo (back → eyes) | Back-view beat ~2 s → eye cue B, 1.5–2 s: quiet renewed resolve after the cue-B trigger. |
| `G-06` | ~3 | — | Table | Paper and hand stillness (insert R2-J12). No dialogue — v1 placed the end of G-L04 here; removed. |
| `G-07` | ~3.5 | — | Andre | Andre's quiet respect; table match cut into Saint Helena. |

## §4 Historical Anchor & Research Citations

- **Inquisition Sentence & House Arrest:** Condemned in Rome on June 22, 1633; forced to recite the formal abjuration; confined under house arrest first in Siena and then at Villa Il Gioiello in Arcetri until his death in 1642.[3][12]
- **Scientific Legacy:** Published *Discorsi e dimostrazioni matematiche intorno a due nuove scienze* in Leiden in 1638 while under house arrest, establishing foundational principles of kinematics and material strength.[3]

> Wardrobe reconciliation: D02 governs new production. Dark-shirt synthetic studies are retired; see `02_references/legacy/retired-dark-wardrobe/manifest.json`. The approved photo anchors face and clothing, not seated table geometry.

### Open flags (carried, NOT resolved here)

- **Historian flags (historian-review-v2 §4), carried text NOT changed:** (a) §1 Motivation says "failing eyesight" and §2 "Eyes Reference" says "slight , " (a gap where a word was removed) — eyesight failure is dated 1636–1638, not late 1634, so the eyes should read as weariness, not impairment (matches the script's cue A "not blindness"); (b) §4 "house arrest first in Siena" is supported only by a source not yet in the registry; (c) §4 *Discorsi* (Leiden, 1638) is mis-cited to [3], which does not mention it.
- Gown: `galileo-v2-proposta.md` proposes charcoal → near-black gown (minor); the producer's pilot uses the charcoal doublet sleeve from R2-J12. Armchair: low-backed, with arms (Sustermans portrait c. 1640).
- Back-view geometry and nape (BV-W / blurred nape) depend on D17/D18 — proposed, not recorded.

---

# Chapter N — Napoleon Bonaparte

**Chapter:** N — Napoleon Bonaparte  
**Fictional Setting:** Longwood House, Island of Saint Helena (South Atlantic), autumn 1816  
**Location:** Damp, unadorned private study overlooking the bleak windswept plateau  
**Target Duration:** 42 seconds  
**Slots (proposal, editor to confirm):** `N-01` (~4s), `N-02` (~12s), `N-03` (~3s), `N-04` (~9.5s), `N-05` (~4s), `N-06` (~4.5s), `N-07` (~5s) — total 42s

## §1 Dramatic progression & emotional arc

- **Core Question:** *Can historical greatness be separated from the human price of ambition?*
- **Napoleon's Motivation:** Stripped of his imperial throne, confined to an isolated volcanic rock by the British Empire; obsessively dictating his memoirs to Las Cases, seeking assurance that his civil achievements (especially the Civil Code) will outlive the military catastrophes of Waterloo and the Russian campaign.
- **Eye Cue Progression (eyes-only safe crop; short reaction after a back-view beat — rule above):**
  - **Cue A (`N-02`, inside the line, J-cut, eyes 1.5–2 s):** *Pride.* Trigger: `N-L02` "outlives your throne" lands on BV-O → back-view beat (~1.5 s; shoulders lift) under Andre O.S. → **eyes A, 1.5–2 s** → back to BV-O for the last sentence of `N-L02`.
  - **Cue B (`N-05`, eyes 1.5–2 s):** *Not wounded pride — attention: he watches Andre fail to be superior; contained downward glance.* Trigger: `N-L04` "who pays it" (the canonical cue already says "after"). `N-L04` plays whole in `N-04`; `N-05` = back-view beat (~2 s) → **eyes B, 1.5–2 s**: contained downward glance.

## §2 Visual Contract & Atmosphere

> **R2 references (2026-10-09, accepted candidates, decision D05/D04):** eyes state A base → `02_references/history-eyes/napoleon/` (R2-J01-eyes-napoleon-recast_2_eyescrop.png); eyes state B → `R2-J06-eyes-napoleon-reflection-B_1_eyescrop.png`; hand/table insert → `02_references/inserts/R2-J13-insert-napoleon_1.jpg`. Gaze in stills reads near-centre; video prompts must set camera-left.

| Attribute | Production Requirement | Reference Anchor |
|---|---|---|
| **Setting Plate** | British colonial exile parlor: damp whitewashed wood-paneled walls, peeling mould-stained floral wallpaper, sea-mist whistling through wooden shutter louvers, dull Atlantic gray daylight. | `02_references/table/R1-J30-plate-sthelena-1816_1.png` |
| **Table Props** | Worn, cracked leather-bound volume of *Code Civil des Français*, pewter ink pot, brass candlestick with guttering wick, hand-drawn map of Europe. | Table Bible |
| **Napoleon Wardrobe (Below Neck Only)** | Dark forest-green wool tailcoat of the Chasseurs-à-Cheval with red wool piping along lapels; brass eagle buttons with patina; scarlet ribbon and silver star of the Légion d'Honneur on chest; white piqué waistcoat; hand resting heavily upon the Code Civil tome. | `02_references/wardrobe/R2-wardrobe-napoleon-uniform.jpg` |
| **Napoleon Eyes Reference** | Extreme close-up macro crop (brow to lower eyelids, zero nose, mouth, or chin). Piercing gray-blue irises, sharp Corsican brow, hooded lids, deep exhaustion mixed with imperial intensity. | `02_references/history-eyes/napoleon/R1-J17-eyes-napoleon-selfpossession_1_eyescrop.png` & `R1-J18-eyes-napoleon-reflection_1_eyescrop.png` |
| **Andre Framing** | Seated screen-left, looking camera-right. Cool, diffuse marine daylight falling over his left shoulder, capturing his solemn gaze. | `02_references/andre/approved/cover_20240202_015341_hs34.jpg` |

---

## §3 Dialogue & timing (Edition E - English) — line IDs only

Line text: `01_script/dialogue-lines.csv` sha256 `d14322550e9f52db6b88a8db3e5ace84e3b666900046edf9532c237f2f1a83f6`. BV-O / BV-R / BV-W / BL-n per the v2 continuity proposal (not approved).

| Slot | ~s | Line ID | Speaker | Action |
|---|---|---|---|---|
| `N-01` | 4 | — | Ambient / back view | Napoleon's first presence is from behind: BV-O phase 1 — coat shoulder/sleeve in the right third, head out of frame (BV-W in phase 2; costume N-A/N-B pending, see `napoleon-v2-proposta.md`). Wind and sea spray against shutters. |
| `N-02` | ~12 | `N-L01`<br>`N-L02` | Napoleon (O.S.)<br>Andre | N-L01 over BV-R on the coat shoulder, BL-1 → rack to Andre. N-L02 over BV-O. Eye cue A inside N-L02 (§1): back-view beat ~1.5 s after the trigger → eyes A 1.5–2 s (gaze camera-left) under Andre O.S. → BV-O for the last sentence. |
| `N-03` | ~3 | — | Napoleon (back) | Back-view hold as the end of N-L02 lands (no eyes). Optional legacy intercut per `napoleon-v2-proposta.md`. Replaces the v1 eyes-only slot. |
| `N-04` | ~9.5 | `N-L03`<br>`N-L04` (whole) | Napoleon (O.S.)<br>Andre | N-L03 over back view BL-1; the body leans slightly toward the table, head stays away from camera. N-L04 over BV-O, uninterrupted, played whole. Hinge: the only question about Andre's world; N-L03/N-L04 are the single permitted use of "argue" (see `napoleon-v2-proposta.md`). |
| `N-05` | 4 | — | Napoleon (back → eyes) | Back-view beat ~2 s → eye cue B, 1.5–2 s: not wounded pride — attention; contained downward glance after the cue-B trigger. |
| `N-06` | ~4.5 | — | Table | Hand stops over book and table (insert R2-J13). No dialogue — v1 placed the end of N-L04 here; removed. |
| `N-07` | 5 | — | Andre | Andre closes without verdict; table cut to desert night. |

## §4 Historical Anchor & Research Citations

- **Exile & Setting:** Exiled to Saint Helena aboard HMS Northumberland in October 1815; resided at Longwood House from December 1815 until his death in May 1821.[4]
- **The Napoleonic Code:** Promulgated in 1804 as the *Code Civil des Français*, establishing legal equality and freedom of conscience while simultaneously institutionalizing severe patriarchal restrictions and curtailing women's legal rights.[4][17]
- **Linguistic Reality:** His childhood mother tongue was Corsican (an Italo-Romance dialect closely related to Tuscan); he spoke Italian before learning French at age 9 at Autun and Brienne, retaining an accent throughout his life.[8]

> Wardrobe reconciliation: D02 governs new production. Dark-shirt synthetic studies are retired; see `02_references/legacy/retired-dark-wardrobe/manifest.json`. The approved photo anchors face and clothing, not seated table geometry.

### Open flags (carried, NOT resolved here)

- **Costume — DECISION PENDING:** `napoleon-v2-proposta.md` offers N-A (green Chasseur-colonel coat, bicorne on the table; recommended for recognisability) or N-B (Longwood home dress: cream piqué waistcoat, smoking jacket, red slippers). §2 below is v1 (green tailcoat with Légion d'Honneur ribbon/star) and is not decided.
- Eye base: D05 updated 2026-10-09 — Napoleon base = `R2-J01-eyes-napoleon-recast_2_eyescrop.png`, B delta = `R2-J06`. The §2 "Eyes Reference" cell below still lists the superseded R1-J17/J18 pair (history only per D05).

---

# Chapter O — J. Robert Oppenheimer — PENDING (no v3 exists; none invented)

`oppenheimer.md` (v1, sha256 `f64813d94f57695313eb78401ccd24a54f15286f7f5a66f0ea2ef0b09ceac2a5`) stays the only bible for this chapter and is **not integrated**. Findings from reading it against the CSV (no text copied):

- O-L01..O-L03 appear in v1 §3 as in the CSV; `O-L04` is **split** across `O-04` (start) and `O-06` (end) with the eye-cue-B slot `O-05` between them, so the cue-B eyes precede the end of `O-L04` — the same cause-after-effect order that audit F03 flagged for Galileo.
- v1 cue A/B are 4 s each and quoted as holds ("absolute paralysis", "prolonged silence"); under the new direction the hold should be carried by the back view and the eyes reduced to 1.5–2 s after a back-view beat (rule above). A v3 for this chapter needs the same restructure as the other four.
- `oppenheimer-v2-proposta.md` (historian+continuity) marks the Hiroshima–Nagasaki line as **PENDING ANDRE DECISION**; any §1 trigger on that line must wait for it.
- No Oppenheimer v3 was written, no triggers were chosen, and no slot timings were proposed.

# Cross-chapter open items (for producer / Andre; none applied)

1. **Canonical script notes** (`script-en.md`, NOT edited): the proposals P-ALL / P-C / P-K / P-G / P-N in `agents/handoffs/2026-10-09-dialogue-sound-l04-scene-bibles.json` (`pendingDecisions`) remain unapplied; they change eye-cue wording only, no dialogue and no CSV.
2. **P-K option 1 vs 2** (Genghis cue B placement) — Andre/director.
3. **Wardrobe/costume decisions** that make §2 stale: Genghis armour, Napoleon N-A/N-B, Caesar fibula (see each chapter's flags). Not mine to decide.
4. **Historian flags** on carried §1/§2/§4 text (Galileo eyesight, Siena, *Discorsi* citation) — historian-review-v2 §4 recommends the corrections; they are listed, not applied, because this task is integration only.
5. **Editor:** confirm slot seconds and the J-cuts for cue A inside `C-02`/`K-02`/`N-02`; Galileo v2 timeline follows the checkpoint, not these proposals.
6. **Producer:** register this file/hash (and `continuity-matrix-v2.csv`) in the manifest if wanted; I did not touch manifest, board, approvals, ledger, STATE or decisions.
7. All line audio is scratch/guide; the G-L04 guide takes have doubtful words (ADR later).
