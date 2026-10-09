# Lighting & Look v1 — The Table Between Centuries

Date: 2026-10-09 · Role: director of photography / lighting consultant (review/proposal only)
Status: **PROPOSED — not approved; no approval, task, manifest, bible or prompt file changed; no paid or external call made.**
For: the art director (owner of `docs/art-direction-review-v1.md`) and the producer.

Read for this pass: `AGENTS.md`, `skills/andre-time-travel/SKILL.md`, `skills/kling-cli/` (SKILL, reference, filmmaking-workflow — read only), `manifest.json`, `memory/STATE.md`, `03_bibles/` (all), `01_script/script-en.md` + `proposals/script-en-v2-proposal.md`, `05_storyboard/shot-list.csv`, `source/atlas.json`, atlas v1 `next-image-batch.md`, `docs/production-plan.md` §8, `docs/visual-contract.md`, `docs/master_production_visual_bible.md` (workspace), `docs/art-direction-review-v1.md`, `docs/decision-sheet-andre-v1.md`, `agents/handoffs/`, all 32 prompts in `07_generations/requests/`.
Viewed: all six `_review/` contact sheets, `R2-andre-table-cinematic.jpg`, `R2-plate-rome-villa.jpg`, `R2-plate-present-day-table.jpg`, one real 2024 photo, atlas v2 card `O-03` and board `scene-galileo`.

**Concurrent changes observed at 09:2x (another agent, same checkout, uncommitted):** decisions `00_brief/decisions/D01–D10` now exist. Relevant here: D02 wardrobe = navy unstructured blazer + charcoal open-collar shirt; D03 grooming = short, textured, as in the 2024 photos; D04 table = `R1-J26-table-anchor_2` + the travels-with-Andre rule; D05 eye bases = Caesar tile 1 (J11), Genghis tile 4 (J13), Galileo tile 6 (J15), Oppenheimer tile 10 (J19), Napoleon **recast**; D07 script v2 integrated into canonical `script-en.md`; D09 screen axis fixed (matrix corrected). The scene-bible **lighting** lines I cite in §9 were not changed by that pass. This document is written against those decisions; it does not evaluate or ratify them.

Notation: **[E]** evidence from a file or image · **[R]** recommendation. Hex values marked *sampled* were measured locally from the named file (64×64 downsample, 5-colour quantise; real-photo skin from 16 px patches). All other hex values are designed targets. Kelvin values are lighting intent and grade neutral points; Kling does not take Kelvin as a parameter, so in prompts they become words.

---

## 1. Visual thesis — "He brings the morning with him"

The film is about one man who knows what came next, sitting across from five people who don't. Light should carry that difference, and it can do it with only two sources per shot.

1. **The witness light (Andre's).** A soft, neutral-cool, daylight-toned key from camera-left. It is literally the morning window of the present-day room where the film starts and ends. Andre carries it into every century. It never changes direction, softness or exposure on his face; only the grade around it moves. This is the likeness anchor (§3).
2. **The era flame (theirs).** Each century has its own practical source on the **far side of the table, beyond the interlocutor**: oil lamp → hearth → candle → shuttered sea-window with a dying candle → bare tungsten bulb. In Andre's coverage it only edges him from camera-right/behind. It warms his cheek and shoulder but never takes over his face.
3. **The future falls on the past.** In the reverse eye shots, the witness light comes from behind camera and becomes their frontal light: Andre's knowledge lands on their eyes. Their own era flame only rims them. The last thing you see in each pair of eyes is light from the present. The audience never needs this explained, but they will feel it.
4. **The flame climbs toward daylight.** In script order (C → K → G → N → O, verified in `manifest.json`), the era sources follow humanity's technology of light: oil, open fire, wax and glass, overcast daylight, electricity. Their colour temperature rises toward the witness light: ~1850 K → ~1900 K + 7000 K skylight → 1850 K + 9000 K dusk → 6500 K → 2700 K bulb against ~10 000 K pre-dawn. By Trinity, the window behind the bulb is nearly the colour of Andre's light. The past has caught up with the present. Then we cut to the present, where only the witness light remains.
5. **The face history withheld.** The zero-full-face rule becomes the film's signature, not its limitation. Historical figures exist as **light on material**: an eye strip lit by the future, a hand in raking flame, a sleeve's texture. Darkness takes the place of the face. We light the absence deliberately (§5), and we light it so a QC shadow-lift can never recover a face.
6. **The table is the constant surface.** The table travels with Andre (art-direction-review C4, decision D4). It always takes the witness light from the same side and the era light from the other. A match cut on the insert therefore reads as *"the same light, a different room arrived around it."* (§6).

Ending payoff: in the last shot the morning has advanced (`master_production_visual_bible.md` §6). The first warm, flame-coloured light the present has shown lands on **the empty chair opposite**, where the next visitor from the future will sit (v2 OUT-L01 "One day someone will sit across from us"). Under v1 it still works, as the "they" made visible.

---

## 2. Lighting plot (one geography for every chapter)

Plan view. Andre sits on the west side and the interlocutor on the east, across the long axis of the J26 table. All coverage cameras stay on the south side of the 180° line.

```
                 N (upstage, far side of the line)
                       ┌ era practical (E–NE, beyond interlocutor,
                       │  at or BELOW shoulder height except bulb/toono)
   ANDRE (W) ═════════ TABLE ═════════ FIGURE (E)
        ▲                                  ▲
   witness light (SW, low-south,       Cam B (SW) on figure: witness light
   soft, ~35–40° off Andre's nose,      is behind camera → frontal-soft on
   15–20° above eye line)               eyes; era practical → camera-right rim
   Cam A (SE) on Andre: witness = camera-left key; era practical = camera-right edge
                 S (camera side)
```

**[E] Existing assets are already consistent with this geography.** Every Andre prompt (J01–J09) asks for "soft diffused key light from camera-left", and every eye prompt (J10–J20) asks for era light "from the right". For a single world-fixed source on the camera side of the line, that pair is geometrically correct. So no existing reference has to be discarded for direction alone. This plot only adds the far-side era practical and defines who keys whom.

Rules that follow from the plot:
- **Shadow safety.** Era practicals behind the figure stay at or below their shoulder height (lamp, candle, hearth). Then the figure's head shadow falls up and back onto the wall behind them, never onto the table or across Andre. Overhead sources (toono shaft, Trinity bulb) hang **over the table centre or slightly behind the figure**, so the head shadow drops into their own lap. Any shadow with a head silhouette on table, wall or Andre is a reject (visual-contract §4).
- **No profile silhouettes.** The figure is never between a practical and a visible wall at an angle that can draw a nose or chin outline.
- **Andre is never backlit into silhouette.** The era edge on him is capped at +½ stop over his key on the cheek. If more is needed, it goes on hair and shoulder, not skin.

---

## 3. The Andre anchor (constant in all seven sections)

| Parameter | Value | Why |
|---|---|---|
| Direction | Camera-left, 35–40° off his nose line, 15–20° above eye line | Matches every R1 prompt and the bible; broad-side soft key gives the most faithful likeness and the fewest generator surprises |
| Quality | Large, soft, wrapping (≈1.2 m diffusion at 1.5 m equivalent); no hard edges on the face | Production plan §"Table, camera, light": diffuse directional light over hard changing light on a face |
| Colour | ~5000 K intent ("neutral daylight-toned"). In-grade it reads slightly cool against warm eras and neutral in the present | It is the present-day window; the one constant temperature in the film |
| Key:fill on face | Varies by chapter (§4) only through negative fill on camera-right. Key exposure on the face is fixed (skin ~60–65 IRE on the lit cheek in MCU) | His face never gets darker; the room does |
| Catchlight | One soft rectangle at **10–11 o'clock** in both eyes, always. The era practical may add a small point at **2 o'clock** | Strongest single identity-continuity cue across eras |
| Bounce | Pale oak table gives a faint warm under-fill (≤ −2 stops). This is "the table light", the only light he and the table share in every era | Ties Andre to the motif; lifts eye sockets without a frontal fill |
| Never | Moving flame shadows on his face; top light that blacks out eye sockets; coloured gels on skin above ~30 % saturation; any reflection in his eyes other than light shapes | Likeness stability and the zero-face rule (his corneas face the interlocutor) |

Skin reference **[E]**: the real 2024 photo under flat indoor light samples at `#E09A8C` / `#F0B3A6` / `#EBAE9C` (cheeks, forehead). These are the identity hues. Grade targets per era are in §4. The rule is to keep the *hue* within ±5° of the skin-tone line on the vectorscope in every chapter. Only luminance and saturation move.

**Reusable prompt block (≈30 words; append to any Andre face-bearing still or keyframe):**
> Soft neutral daylight-toned key light from camera-left at eye height, one soft catchlight in each eye, [ERA] warm glow from behind camera-right edging his cheek and shoulder, natural skin tone.

For image-to-video, the keyframe already carries the light, so use only: *"Keep the existing soft camera-left key and [era] edge light constant; no flicker on the face."* (kling-cli filmmaking-workflow §6: emphasise motion and do not re-describe the image.)

---

## 4. Per-chapter look

Common camera grammar (all chapters, unless noted):
- **Andre MCU/MS:** 50 mm-equivalent look, camera at his eye height, 2–3° down. Locked. The film's only face move is a 3–5 % push-in on **O-04** (see O). The visual contract allows "a small tested push-in"; this needs a pilot test before use.
- **Eyes ECU:** 100 mm macro look, camera on their eye line, locked, horizontal strip (brow to just under the lower lids) *inside* a 16:9 frame (§5).
- **Inserts (hand/stain/chip):** 40 mm look, lens 15 cm above the table surface, same crop and same J26 geometry in every era. Locked, or a 1–2 % lateral drift at most.
- **Wides/plates:** 32–35 mm look at seated eye height (~120 cm), front-left three-quarter on J26 (fixes C3).
- **Grain:** request a *clean* image from Kling ("fine detail, no heavy grain") and add grain in post per chapter. Generated grain flickers between takes and fights compression and identity detail.
- Lens terms are guidance for the generator, not physical parameters (kling-cli §6).

### IN — Present day, opening (IN-01…03, 12 s)
- **Script-verified:** "A hand rests on the wooden edge. Ambient present-day sound falls away." The master visual bible and table bible both say *morning* light.
- **Key source:** tall window **screen-left of Andre** (the origin of the witness light), early overcast morning, about 30 min after sunrise.
- **Kelvin:** window 5600–6000 K; room bounce 5000 K; grade neutral 5600 K.
- **Ratio:** 2:1. **Palette:** concrete `#8E9290` · window `#DCE3E6` · oak `#B08B62` · shadow `#2A3236` · skin target `#D2A28E`. *Sampled:* J32 `#CDD5D7 #AAB0B0 #89857F`; R2 present `#132022 #29383B #4A5F66 #6F8790 #B7CBD4` (dusk-blue, see L4).
- **Atmosphere:** none, clean air. **Texture:** finest grain (35 mm fine at 15 %), no halation. The present is the sharpest image in the film.
- **Movement:** locked. IN-01 hand enters into a still frame.

### C — Julius Caesar, Rome, early 44 BCE (C-01…07)
- **Script-verified:** the script gives no time of day. Sources conflict (L1); I recommend **evening, lamp-lit interior**. This matches J27, the eye prompts, the atlas ("warm, diffuse oil-lamp direction") and the table bible's terracotta lamp prop. Drop the noon peristyle.
- **Key source (era):** one terracotta oil lamp on a stand behind the interlocutor's right shoulder at table height, plus a second smaller lamp low on the far wall for fresco glow.
- **Kelvin:** lamp ~1850 K; fresco bounce ~2200 K; witness 5000 K. Grade neutral **~2800 K**, so the lamp reads gold-amber rather than orange and the witness reads faintly cool.
- **Ratio:** 3:1 (fluent, confident Andre). **Palette:** shadow `#1E0E07` · terracotta `#7A3A1E` · fresco red `#9C3B2A` · lamp gold `#D9A055` · toga cream `#E8DCC2` · Tyrian accent `#5B1E3A` · skin target `#C98A66`. *Sampled J27:* `#2B1106 #612D16 #834D2C #A0673A #C58C4E`.
- **Eyes height:** camera 3–5° below Caesar's eye line (subtle authority).
- **Atmosphere:** very light lamp haze (oil smoke) only above head height; no dust motes across faces. **Texture:** 35 mm medium grain 25 %, warm halation on the flame only.

### K — Genghis Khan, campaign ger, summer 1227 (K-01…07)
- **Script-verified:** "Tent-lit table" (shot list K-01). The scene bible has a hearth with smoke drafting to the roof ring (*toono*), and the J28 plate shows an open toono. That makes the "steppe overcast" a top shaft through the toono, not an exterior.
- **Key source (era):** low hearth fire beyond the figure (camera-right in Andre coverage), plus a cool overcast shaft from the toono falling **behind** the figure into the smoke. Never on Andre's face, and never as a hard top light on the table where it could print a head shadow.
- **Kelvin:** hearth 1900–2000 K; toono shaft ~7000 K; witness 5000 K. Grade neutral ~3000 K.
- **Ratio:** 5:1, the darkest Andre (slower, graver).
- **Palette:** smoke black `#15100B` · felt umber `#4A3424` · hearth `#D9772B` · ember `#F2A64A` · toono overcast `#9AA3A8` · deel accent (see L7) `#2C4A7A` or `#4A3020` · skin target `#C4865F`. *Sampled J28:* `#181008 #2E1C0F #40291A #614432 #A07F68`.
- **Eyes height:** level, eye-to-eye.
- **Atmosphere:** the film's heaviest haze, as visible strata in the toono shaft only. Keep Andre's face clean (production plan: "do not obscure Andre with smoke or flames"). Firelight on the eyes is *steady*, a slow breathing ±⅓ stop, never visible flicker (atlas: "No moving flame shadow across eyes").
- **Texture:** heaviest grain (35 mm 500T-style, 35 %), slight shadow lift to `#15100B` rather than crushed black.

### G — Galileo, Arcetri, late 1634 (G-01…07) — production-first chapter
- **Script-verified:** the scene bible says "late 1634", "dusk", "brass candle lantern", "cool Tuscan evening blue with warm candlelight". The plate and atlas say cool window light (L2). I recommend **winter dusk, blue hour, plus one candle**: the two sources meet and are reconciled for the first time.
- **Key source (era):** a small stone window behind the figure carrying deep blue-hour sky, and one beeswax candle on the far half of the table near the (unreadable) papers.
- **Telescope:** I recommend **no telescope at the window**. It is not in the script or bibles, and it is exactly the "simple story" iconography G-L02 criticises.
- **Kelvin:** candle ~1850 K; window ~9000 K; witness 5000 K. Grade neutral ~4000 K, so both extremes stay visible: amber pool against blue stone.
- **Ratio:** 3:1, warm and gentle. This is the quietest, most painterly chapter, where Andre is warm. **Palette:** walnut shadow `#231810` · stone `#7C726E` · plaster `#C9C3B8` · dusk window `#5E7A96` · candle `#E8B169` · linen `#EDE6D6` · iron-gall ink `#1C1A1F` · skin target `#C49480`. *Sampled J29:* `#231810 #4A3D34 #7C726E #A4A4A8 #D3D9E0`.
- **Eyes height:** camera 2–3° above his eye line (age, weight), soft frontal witness light. Clouding in the iris is allowed, blindness is not (atlas board).
- **Atmosphere:** candle bloom (1/8 diffusion look), no haze. **Texture:** fine 35 mm 20 %, soft highlight roll-off.

### N — Napoleon, Longwood, Saint Helena, 1816 (N-01…07) — the hinge
- **Script-verified:** the setting is **Saint Helena exile, not a campaign tent.** The manifest, scene bible and shot list ("Sea-worn light at plain table") all agree, so a campaign-lantern look would contradict the script.
- **Key source (era):** an overcast Atlantic window through **fixed wooden shutters** (the J30 render shows modern-looking louvres; ask for period plank shutters, half-open). Plus a brass candlestick with a *guttering* wick that dies across the chapter.
- **Kelvin:** window ~6500–7000 K; candle ~1800 K, fading; witness 5000 K. Grade neutral ~5500 K. This is the first chapter where the era light is **as cool as Andre's**.
- **Ratio:** 2:1, flat with nowhere to hide. This is where the questions turn on Andre (v2 N-L03 "And you. Where you come from…") and he is "caught". The light stops protecting him. With v2 now canonical (D07), in N-04/N-07 the shutter side rises +⅓ stop so the era light briefly matches the witness light on his face. It is the only chapter where the past lights him as strongly as the present.
- **Palette:** damp black `#1F2324` · sea grey `#828F96` · mould green `#5F6B5A` · plaster `#B9BDB6` · chasseur green `#24382C` · brass `#8C6A3A` · candle stub `#C8955A` · skin target `#B99486`. *Sampled J30:* `#252727 #394142 #535A5C #828F96`.
- **Eyes height:** starts 3° low (pride) and goes level at N-05 (bruised).
- **Atmosphere:** humid sea-haze, low contrast, slight veiling glare; no visible slat stripes on skin (hard bars read as a prison cliché and break the soft-key rule). **Texture:** medium grain 30 %, blacks lifted to `#1F2324`, saturation −15 %.

### O — Oppenheimer, near Trinity, 15/16 July 1945 (O-01…07)
- **Script-verified:** O-L01 "Does the test work?", so the scene is **before** the detonation and **no flash appears in the chapter**. The atlas already forbids "flash, mushroom cloud or reflected face". The bibles say night thunderstorm and rain on a tin roof; the plate, eye prompts and atlas say pre-dawn (L3). Reconcile as **the last hour before 05:29, storm just passed**: wet glass, dripping eaves, deep cobalt in the window.
- **Key source (era):** one bare tungsten bulb hanging over the table centre, slightly toward the figure. It is the only electric light and the only hard source in the film. It falls hard on table, notebook and hands, but **not as Andre's face key**: his face stays on the soft witness light, and the bulb only hits his hair and shoulder from above-behind. The bible's "harsh top-down tungsten carving noir shadows" on Andre is rejected (L3).
- **Kelvin:** bulb ~2700 K; window ~10 000 K; witness 5000 K. Grade neutral ~4300 K.
- **Ratio:** 6:1, but the catchlight never disappears. Andre goes silent; the room goes dark around a lit face.
- **Palette:** shack night `#1B1714` · pine `#6B5444` · tungsten pool `#F0B060` · pre-dawn `#2F4566` · cobalt window `#4C6FA0` · tweed `#6E6A64` · cuff `#E4E1DA` · skin target `#B58C78`. *Sampled J31:* `#2C221D #423834 #615550 #786E6C #9BA0AD` (too bright a window for "pre-dawn"; regenerate darker).
- **Eyes height:** dead level and symmetrical.
- **Camera:** the film's single face move, a 3–5 % push-in on O-04 while Andre listens to "Can you tell me whether it was right?". It needs a pilot test first; if it fails, lock off.
- **Atmosphere:** faint dust in the bulb cone; no smoke on faces (cigarettes stay unlit and unbranded, L/C5). **Texture:** sharper, harder contrast, grain medium 25 %, saturation −20 %, slight cyan in the shadows. This is the most "modern" historical image.
- **Bulb rule:** the bulb hum is allowed one dip (generator or storm) at O-06 → O-07, which is the exit light event (§6). Never strobe; that is a photosensitivity risk and an instability risk for the generator.

### OUT — Present day, ending (OUT-01…03, 18–22 s)
- **Script-verified:** "Andre, at the empty table in the present", "Fade on the table, not through a face". The master bible says the morning light "has advanced slightly".
- **Key source:** the same screen-left window, now with a low sun break. One warm patch (~3800 K) crosses the far half of the table and lands on **the empty chair opposite** in OUT-02. Andre's face stays on the soft window key.
- **Ratio:** 3:1. **Palette:** as IN, plus sun patch `#E9B97A`. **Texture:** as IN. **Movement:** locked. The OUT-03 fade is on wood, to black, over 48 frames.

---

## 5. Lighting what we may not show: eyes-only and below-neck

The hard rule (AGENTS.md, visual-contract §Historical figures): no historical figure's full face in any frame, including reflections, shadows, silhouettes and background portraits. Eyes-only (brow to just under the lower lids) and below-neck are allowed.

### 5.1 Eyes-only: "the slit of light"
- **Crop first, light second.** The safe crop (brow to lower lids) is the rule. Light only reinforces it: a horizontal **band of soft frontal witness light** across the eyes, falling off **≥2½ stops by the cheekbone**. If the generator widens the frame, the extra area is near-black rather than a face. Darkness never substitutes for the crop; the review still checks the full frame (visual-contract last bullet).
- **QC addition:** for every eye take, inspect the full frame with shadows lifted +2 stops (a temporary grade node, not the master). If a nose, mouth or jaw becomes recoverable, reject. Add this line to the QC zero-face check that the art director's delegation table already proposes.
- **Catchlights carry story.** One soft rectangle at **10–11 o'clock** (the witness light, i.e. Andre) plus the era flame's point at **2 o'clock**. Catchlights contain **only light shapes, never figures**. Andre's silhouette reflected in their corneas is technically his own likeness but forbidden for simplicity, and Andre's own corneas must never show the interlocutor.
- **Expression by light, not by motion.** In the B state of each pair, the era rim drops ⅓ stop (Caesar, Genghis, Napoleon) or the witness band narrows slightly (Galileo, Oppenheimer). The face does less and the light does the rest. This also helps one identity per figure (C6): the same eyes, with a different light.
- **No flicker on eyes.** Steady light at most a slow ±⅓-stop breath. This contradicts the "flickering oil-lamp" wording in J10/J11 (L6).
- **Framing inside 16:9:** keep the band at about 28–35 % of frame height, centred on the upper third, with the rest falling into era darkness. This is more beautiful than a letterbox strip and survives any later reframe.

### 5.2 Below-neck: Dutch still-life
- **Raking era light**, 10–20° above the table plane from the far-side practical. Wool, felt, linen, tweed and skin texture appear only under grazing light. This is where each era's material richness lives.
- **The top edge is the danger edge.** The frame's top sits at mid-chest or lower for seated torsos, and a soft flag (an unlit zone) darkens the collar line so even the neck base sinks. The R1 costume crops start at the collarbone, which is too high for motion: a single breath or lean can bring the chin in. For video, crop at the sternum.
- **Hands are the actors.** One hand, one action (the next-image-batch already scripts it: press, loosen, rest, stop). Key the hand with the era practical and let the witness light fill it faintly from camera side. The present literally touches their hand.
- **Shadow audit** for every insert: no head shadow on the table, wall, chair back or Andre's hand (§2).
- **Reflective props** (Napoleon brass, Oppenheimer watch, Galileo compass, Caesar bronze) stay matte or angled down. A watch crystal or brass boss can mirror a face. Prefer brushed and patinated finishes in prompts.

---

## 6. Transition lighting between centuries

The mechanism is a hard match cut on the insert: the same hand, ring stain, chip, lens height and crop (art-direction-review §3.3, decision D4). The witness light on the hand and table is **identical on both sides of the cut**. Only the era side changes, so the cut reads as "the room changed around the same light". Each exit gets **one** motivated light event in its last 12–24 frames. It is generated as the single allowed "[ONE ENVIRONMENT/LIGHT CHANGE]" (production plan §8, table-transition skeleton) or done in the grade, never as a morph.

| Cut | Exit light event (last ~1 s) | Arrival state (first frame) | Sound bridge (from bibles) |
|---|---|---|---|
| IN-03 → C-01 | Window light dims as if a cloud passed | Lamp already burning steadily, gold | present room tone falls away |
| C-07 → K-01 | Lamp flame bows in a draft | Hearth glow, smoke strata in the toono shaft | steppe wind |
| K-07 → G-01 | Smoke drifts across the toono shaft, light dims | Still candle, blue window | crickets / distant bell |
| G-07 → N-01 | Candle flame leans and settles | Overcast shutter light, grey | wind and sea against shutters |
| N-07 → O-01 | The guttering candle goes out (smoke wisp, no face) | Bulb already on, hard pool | rain dripping off tin |
| O-07 → OUT-01 | Bulb dips once with the generator hum, then cut | Present morning window, the cleanest frame | silence, then room tone |

The flash the film never shows: the cut from O-07's dipping bulb to the white morning window is the closest the film comes to Trinity's light. It is implied, never depicted. **[Director decision]** if anyone wants a literal white-out; I advise against it (atlas forbids flash; it tells Oppenheimer's answer in picture; photosensitivity risk).

Grade at cuts: no dissolves through faces. A 6–8-frame grade ease on the *arrival* insert only (from the previous chapter's neutral to the new one) is allowed, since it sits on a hand and table and not a face.

---

## 7. Colour-grade plan and LUT direction

- **Pipeline:** treat Kling outputs as display-referred Rec.709 / gamma 2.4 (verify on first accepted take). Grade in a wide working space (DaVinci Wide Gamut/Intermediate or ACEScct), output Rec.709 g2.4 masters plus a web sRGB derivative. Keep it consistent with the two-master plan in the art-direction review §8.
- **One show LUT, never per-shot LUTs:** a soft print-film emulation (2383-style toe and shoulder, mild cyan-teal shadow, warm highlight) applied at **40–60 % strength** after the chapter CDL. Working name: `TBC_show_print_v1.cube`, *proposed only, not created*.
- **Per-chapter CDL (in a `.ccc`, one ID per chapter):** sets the neutral point (Kelvin values in §4), black level, saturation and the shadow tint listed. Andre's skin is protected by a hue-vs-hue / hue-vs-sat qualifier node *after* the CDL that holds his skin hue within ±5° of the skin-tone line and caps saturation at the chapter target.
- **Node order:** input transform → balance (per shot, to match the chapter keyframe) → chapter CDL → skin protect → show LUT (40–60 %) → grain (per chapter, §4) → output transform. Grain goes after the LUT so its structure is identical across chapters.
- **Exposure anchor:** Andre's lit cheek at 60–65 IRE in every chapter. Eye strips: the iris catchlight just under clip and lower lid at 35–45 IRE. Inserts: oak mid-tone at 45–50 IRE (J26 sampled oak `#503A23 #8B6C50 #B49980`).
- **Arc check:** play the five chapter keyframes side by side. The background warmth should fall steadily from C to O while Andre's face looks like the same man in the same light. If his face shifts more than the room, the grade is wrong.

---

## 8. Prompt rewrites (prompt-ready; for the art director to adopt or edit)

Constraints respected (kling-cli SKILL + filmmaking-workflow): one primary action, one camera behaviour, lighting as a short anchor, no style lists. Image-to-video prompts describe motion and preserve the keyframe rather than re-describing it. No Element binding in `text_to_image`; Element markers are written as `<<<APPROVED_ELEMENT_ID>>>` placeholders exactly like production-plan §8, to be replaced only by a recorded approved ID together with the live-schema `--elements` binding. No invented IDs, no readable text, no brand names. Verify the live model's prompt length limit and reference-marker wording before use. **None of these are approved or submitted.** They are drafts for the next scoped request (P1-2/P1-3/P1-4 in the art-direction review).

### P1 — Eyes template (J11–J20 family; regenerate as one identity, two states)
Original (J11, Caesar):
> "…Roman man in his mid-fifties, deep-set dark brown eyes, strong straight brows, fine crow's feet. Expression: cold command and total self-assurance, steady unblinking stare. Warm flickering oil-lamp light from the right, dark background."

Improved (light block replaces the last sentence; the crop and safety text above it in J11 stays unchanged):
> "…Expression: cold command and total self-assurance, steady unblinking stare. Soft neutral daylight-toned light from the front-left lays a band of light across both eyes with one soft catchlight at ten o'clock; a warm steady oil-lamp glow from behind camera-right rims the brow with a tiny point catchlight at two o'clock. Below the lower eyelids the skin falls quickly into deep shadow. Catchlights show only light shapes, never a figure. No flicker."

Era substitutions for the rim clause: Genghis "steady hearth-fire glow and a faint cool skylight above"; Galileo "a single candle glow and deep blue dusk from a window behind"; Napoleon "dim grey sea-light from a shuttered window behind"; Oppenheimer "a bare tungsten bulb glow from above-behind and deep blue pre-dawn". Delete "a soft shadow of a hat brim falling across the upper forehead" from J19/J20 unless the hat is canon; the rendered tiles do not show it anyway.
For the B state, change only the expression clause and "rim drops slightly dimmer". Supply the D05 base tile (J11 / J13 / J15 / J19) as the image reference so the identity stays the same (C6). For the Napoleon recast, D05's target (≈47, dark brows, sea-mist pallor, heavier lids) suits this light: the grey shutter rim plus the frontal witness band gives the pallor without desaturating the iris.

### P2 — Andre era keyframe (applies to all 10 Andre briefs in `next-image-batch.md`)
Original (C — Andre speaking):
> "Warm, diffuse oil-lamp direction; steady exposure on skin. Ochre plaster and muted red."

Improved (image_to_image with approved Element, still):
> "Photorealistic cinematic medium close-up of <<<APPROVED_ELEMENT_ID>>> seated at the approved oak table in a lamp-lit Roman room at evening, in the left half of frame, looking camera-right toward an unseen listener, mouth relaxed and closed. Soft neutral daylight-toned key light from camera-left at eye height, one soft catchlight in each eye, warm oil-lamp glow from behind camera-right edging his cheek and shoulder, natural skin tone. Ochre plaster and muted red falling into darkness behind him. Same collar, lapels and sleeve length. No other person, no reflection, portrait, mirror or text."

The other eras keep this structure and swap only the room clause and the edge-light clause (§4 sources): "felt tent with low hearth fire and smoke", "stone study at blue dusk with one candle", "damp shuttered room in grey sea-light with a guttering candle", "pine shack before dawn under one bare bulb". The K version adds "no moving flame shadow on his face".

### P3 — Trinity plate (J31) and the O chapter time of day
Original (J31):
> "Plain wooden room of a 1945 New Mexico desert base: pine plank walls, an iron-framed window showing pale pre-dawn desert, a bare bulb, dusty light."

Improved (also fixes the end-on axis, C3):
> "Wide frame at seated eye height, three-quarter view from the front-left matching image 1. Plain pine-plank room of a 1945 desert base in the last hour before dawn after a storm: one bare tungsten bulb hanging above the table centre casting a warm hard pool on the wood, the rest of the room falling into darkness, a small window showing deep cobalt sky and wet glass. No lightning, no flash, no sunrise yet."

### P4 — Rome plate (replace R2 villa as the Caesar environment; refine J27)
Original (scene bible setting, used as anchor `R2-plate-rome-villa.jpg`):
> "compluvium skylight pouring warm Mediterranean morning sun onto terracotta tile floor"

The R2 render shows noon, an open peristyle, a trestle table that is not J26, and an open codex, which is anachronistic for 44 BCE. Improved (J27 family):
> "Wide frame at seated eye height, three-quarter view from the front-left matching image 1. Interior of a Roman house in early 44 BCE at evening: plaster walls with faded red fresco bands, one terracotta oil lamp on a bronze stand beyond the far end of the table giving a warm pool of light, a second small lamp low on the far wall, the corners falling into darkness, faint lamp haze above head height. Nothing on the table."

### P5 — Match-cut insert, image-to-video (IN-03 → C-01 pair; same template for all six cuts)
Original (production-plan table-transition skeleton):
> "Close view of the approved wooden tabletop and Andre's resting hand, same grain and edge position. [ONE ENVIRONMENT/LIGHT CHANGE OR PHYSICAL ACTION]. No face enters the frame. Locked camera. No altered hand anatomy or changing table geometry."

Improved, exit shot IN-03 (keyframe = approved present-day insert):
> "Andre's hand rests on the oak table beside the pale ring stain and the chipped near corner. The soft window light from the left slowly dims as if a cloud passes, then holds. The hand stays still. Locked camera at table height. Keep the grain, stain, chip and hand anatomy exactly. No face, no reflection."

Arrival shot C-01 (keyframe = approved Rome insert on the same geometry):
> "The same hand rests beside the ring stain and the chipped corner; beyond it, at the far edge, a cream wool sleeve with a purple border rests near a warm oil lamp. The lamp flame burns steadily. The far hand presses lightly into the wood, then stops. Locked camera at table height. No head, neck or face enters the frame; no shadow of a head on the table."

### Further rewrites (lower priority)
- **J06/J07 "soft out-of-focus amber bokeh in the dark background"** reads as a modern bar (art-direction-review §3.1). Replace with: "background falls into soft darkness with only a faint warm glow far behind camera-right." Bokeh discs are a contemporary lens signature and belong to no era.
- **J32/J09 present day:** original "present-day empty modern room with a tall window, soft cool daylight". Improved: "…a tall window on the left side of frame, soft overcast early-morning daylight, pale concrete walls, quiet." This keeps the witness light motivated (L4).
- **J30 Napoleon plate:** "a shuttered window with grey sea light" → "half-open plank wooden shutters with grey Atlantic overcast light, a brass candlestick with a short guttering candle on a side table; no louvres."
- **J28 Genghis plate:** "dim amber light" → "low hearth fire beyond the table, smoke rising through a cool grey shaft of daylight from the roof ring, the felt walls falling into darkness; no chair of non-Mongol style." This matches the art-direction-review note on the Chinese-style chair.
- **Eye image-to-video (O-03, production-plan skeleton):** add "Light stays constant; catchlights do not move; one slow partial blink, then the gaze loses focus slightly." This is one action, keeps the light locked and tells the reaction through light.
- **Below-neck video crops (J21–J25 lineage):** "cropped from the collarbone down" → "cropped from mid-chest down, the collar line falling into shadow; raking [era] light across the fabric texture; matte, unpolished metal."

---

## 9. Lighting continuity contradictions found

| # | Contradiction | Evidence | Recommendation |
|---|---|---|---|
| L1 | **Caesar time of day**: morning sun vs evening lamp | `scene-bibles/caesar.md` "compluvium… warm Mediterranean morning sun"; `table-and-continuity.md` "Warm Mediterranean sunlight slicing through marble colonnade" + terracotta lamp; `R2-plate-rome-villa.jpg` noon open peristyle (also trestle table ≠ J26, open codex); vs `R1-J27` prompt "warm lamplight, evening", eye prompts "oil-lamp", atlas "oil-lamp direction" | Evening, lamp (P4). Retire R2 villa as the anchor. The scene bible cites it. |
| L2 | **Galileo light**: dusk + candle vs cool daylight | Scene bible "dusk… brass candle lantern… cool Tuscan evening blue with warm candlelight"; table bible "Tuscan dusk"; J29 "soft cool winter daylight"; eye prompts "cool daylight"; R1-J08 "1630s-evening warm candle-and-window"; atlas "soft cool window light… **page readable**" (also conflicts with the no-readable-text rule C5) | Winter blue hour + one candle. Change the atlas wording to "page detail soft, unreadable". |
| L3 | **Oppenheimer**: night storm + harsh top tungsten vs pre-dawn window | Scene bible "stormy desert night", Andre "harsh top-down tungsten light carving dramatic noir shadows"; table bible "rain drumming on tin roof"; vs J19/J20/J31 "pre-dawn", atlas "dusty pre-dawn blue… No flash" | Last hour before dawn, storm just passed. Bulb hard on the table only; Andre stays on the soft key (production plan prefers diffuse light on faces). No flash. |
| L4 | **Present day**: morning vs dusk vs white office; window side | Master bible/table bible "soft morning"; `R2-plate-present-day-table.jpg` blue hour (*sampled* `#132022…#B7CBD4`) with glazing **screen-right**; J32 bright midday; J09 white office (AD §3.1) | Early overcast morning, window screen-left of Andre (the witness-light origin). Pick one plate after D4. |
| L5 | **Screen axis in data vs bible** | `continuity-matrix.csv` camera_axis "Andre right / interlocutor left" for all five chapters; bible/visual-contract "Andre screen-left, looking camera-right"; R2 master places him right of centre (AD C2) | **Resolved during this pass by D09** (matrix corrected to the bible). The lighting plot (§2) uses D09. `lighting_anchor` in the matrix is still empty; §3 + §4 are proposed content for it. |
| L6 | **Flicker on eyes** | J10/J11 "Warm **flickering** oil-lamp light"; atlas K "No moving flame shadow across eyes"; production plan "rapidly changing hard light on a face" discouraged | Steady flame, at most a slow breath (P1). |
| L7 | **Genghis palette and posture** | Scene bible "heavy dark brown patterned silk deel"; R1-J22 and R2 costume render **blue** silk; J22 shows the figure **kneeling on the floor**, but the shot list needs a hand on the table (table height); J28 chair style (AD §3.2) | Decide the deel colour before the palette locks (`#2C4A7A` blue or `#4A3020` brown). Seat the figure at table height. |
| L8 | **Warm key on Andre in Caesar/Galileo bibles** | Caesar bible "Soft warm natural key light from camera-left"; Galileo "warm candlelight on his face" — the era colour on his key. The character bible says direction stays constant and colour "adapts gently" | Keep his key neutral (witness) and put the era colour on the edge (§3). Otherwise the likeness drifts with every flame. |
| L9 | **Seated reference tiles disagree on key side** | `andre-seated_contact.jpg`: the Galileo-ish tile is lit from a window behind camera-right; the bokeh tiles are front-lit; the office tiles are lit by a large window camera-left. The prompts all say "key from camera-left" | Not usable as a light reference. Use the R2 master and the anchor block for P1-4. |
| L10 | **Plate light axes** | J31 window on axis behind the table (backlight); J32 window at the far wall on axis. Both end-on (AD C3) | Regenerate the plates three-quarter from front-left with the era practical beyond the far end (P3/P4 pattern). |
| L11 | **Brief-to-script mismatches in this assignment** (for the record) | The brief suggested a "campaign tent lantern" for Napoleon, a "telescope-window" for Galileo and a "Trinity flash" for Oppenheimer. Script/manifest: Napoleon is at **Saint Helena** (no tent); no telescope anywhere in the script or bibles; Oppenheimer's chapter is **before** the test and the atlas forbids a flash | Followed the script: shuttered sea-window + guttering candle; no telescope; flash only implied by the O→OUT cut. |

---

## 10. Hand-off notes

- **Zero-spend next steps** for the art director/continuity: (a) adopt §2/§3 as a lighting section in the bibles v2, PROPOSED; (b) add a `light anchor`, `catchlight` and `era practical position` field to `source/atlas.json` cards when atlas v3 is built (the AD review already requests a "light anchor" field); (c) add the +2-stop shadow-lift inspection to the QC zero-face checklist.
- **Paid steps that this document informs but does not authorise:** P1-2 eye bases (§8 P1), P1-3 inserts (P5), P1-4 Andre era keyframes (P2), plate regenerations (P3/P4). Each needs Andre's D1–D5 answers, a new producer scope and a fresh balance read through the CLI.
- **Nothing here is an approval.** Likeness, language, voice, and final picture remain separate gates. No canonical file was edited. This file is the only file created in this pass.
