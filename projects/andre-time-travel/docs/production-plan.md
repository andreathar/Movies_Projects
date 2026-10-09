# The Table Between Centuries — Andre Athar Film Production Plan

> **For Hermes:** Use the subagent-driven-development skill, if available, for bounded research and review tasks. Load `kling-cli`, `film-character-continuity`, `film-dialogue-localization`, and `film-editing-qc` before production. The parent agent alone owns paid submissions, approvals, and the credit ledger. This document is a production plan, not permission to execute placeholder commands.

**Goal:** Produce a photorealistic short in which Andre Athar visits five historical figures at a simple table, explains consequences and their contested legacies, and remains visually consistent throughout; the other characters are shown only through tightly cropped eyes, hands, and clothing.

**Architecture:** Research and dialogue → clean photographic character references → approved Element and face/speech pilot → audio-first storyboard/animatic → one controlled shot at a time → take review → local edit, sound, subtitles, and full-timeline QC. Reuse accepted picture across two language editions wherever mouths are not visible; do not regenerate the entire film for translation.

**Tech Stack:** Authenticated Kling CLI with live capability discovery; approved Andre voice clone and dialogue production in ElevenLabs; an explicitly approved, tested external-audio lip-sync path if necessary; local FFmpeg/ffprobe for inspection and finishing; a versioned shot/take/credit manifest. No new services, purchases, CLI upgrades, or credentials are implied.

---

## 1. Status, scope, and decisions recovered from the conversation

This continues the existing film discussion. It is not a restart of the CLI installation or the English skill translation.

### Confirmed brief

- Lead: **Andre Athar**, with his own approved likeness.
- Five encounters: **Julius Caesar, Genghis Khan, Galileo Galilei, Napoleon Bonaparte, J. Robert Oppenheimer**.
- A simple table is the visual motif. Andre talks about consequences and how these figures are remembered.
- Their **full faces never appear**. Emotional close-ups are restricted to eyes.
- The earlier clarification selected **photorealistic cinematic treatment, approximately four minutes**.
- The clarification requested **two editions: an all-English version and a historical-language version**. Native-language/dialect choices and actual voice support still require the gates below; they are not solved by automatic translation.
- Andre intends to prepare his voice clone in **ElevenLabs** and supply the missing references. Do not treat the clone or new photographs as already delivered.
- User authorization: *** remaining Kling credits may be used** for this film. This is a ceiling, not an instruction to burn credits before the character and script are approved.
- User also asked for specialized reusable skills. They have now been created in the active default Hermes profile; see Section 15.

### Verified in this planning continuation

- The read-only `kling account` result showed **7,741 available credits**. Recheck immediately before the first paid submission; balance can change independently.
- Existing Element IDs inspected through the CLI: `323415933655261` and `323336237505580`. Preserve these exact IDs. Read back ID/name/resource mapping before any later operation.
- The library contains assets labeled `Andre` and `Andre - Jazz Club`. The former's cover is an illustrated contact sheet; the latter's cover is a chapter/player screenshot, and its secondary resources include gray-haired male portraits. These are **not approved clean photographic production references**.
- This is a concrete reference-hygiene risk, **not proof of what caused the failed scene**. The failed clip and its exact generationId have not yet been supplied for diagnosis.
- Local `ffmpeg` and `ffprobe` are available.
- The prior planning continuation submitted **no paid Kling generations** and created no production Elements, film clips, voice samples, or rendered movie.

### Keep the film separate from the current repository

This film now lives in `Movies_Projects/projects/andre-time-travel/`. The Movies_Projects desktop project is anchored to the workspace root. TransfereGov is not a filmmaking dependency; its original plan is preserved in the workspace archive. No code, services, or data there are to be changed.

**Created film workspace:** `/mnt/data/Projects_SSD/Movies_Projects/projects/andre-time-travel/`

The folder structure, planning data, screenplay draft, and management documents are initialized. Photographs, voice samples, approved Elements, generated takes, animatics, and final movies are still pending. The plan below describes production work, not completed media.

## 2. Film concept and dramatic progression

**Working title:** *The Table Between Centuries*.

**Logline:** A traveler who knows what came next sits across from five people who do not. With each conversation, the question shifts from whether history remembers them to whether remembrance can justify the cost.

Andre is a curious, humane interlocutor—not an omniscient prosecutor and not a celebratory tour guide. Each figure asks something back. The eyes register a specific response to a particular line; they are not decorative reaction stock.

The same plain, unpainted wooden table links the chapters. Its edge, grain, and Andre's resting hand become match-cut anchors. Period changes happen around these anchors, not through a morph of Andre's face. Each setting is a fictional encounter grounded in its era; do not present the room, dialogue, or emotions as a documented event.

| Chapter | Proposed fictional encounter | Dramatic question | Emotional progression in the eyes | Research boundary |
|---|---|---|---|---|
| Caesar | Rome, early 44 BCE, before his assassination | Does victory leave a republic or personal power? | Command → calculation → uncertainty | Caesar's assassination was on March 15, 44 BCE; reforms, military achievements, and concentration of power are researched anchors.[1] |
| Genghis Khan | A campaign tent, 1227 | Can an empire connect people and destroy them at once? | Pride → resistance → guarded recognition | His empire continued expanding under successors; intercontinental exchange and destructive conquest must both be represented.[2][15] |
| Galileo | Arcetri, 1634, during house arrest | Does silencing a person settle a question? | Weariness → attention → quiet resolve | The 1633 trial and his residence under house arrest at Villa Il Gioiello anchor the setting; this is not a transcript of his trial.[3][12] |
| Napoleon | Saint Helena, 1816 | Can greatness be separated from its price? | Self-possession → wounded pride → reflection | His exile began in 1815; the Civil Code's enactment and later influence are distinct from a claim that he personally authored every provision.[4][17] |
| Oppenheimer | A fictional room near Trinity base camp, July 15, 1945 | Can technical success answer a moral question? | Anticipation → fear → stillness | Trinity occurred July 16, 1945.[5] The subsequent Hiroshima/Nagasaki events have separate sources.[18][19] The debate about use is separately documented.[9] |

**Period-design cautions:** no later capital/palace casually assigned to Genghis Khan; no post-trial Galileo placed in a pre-trial scene; no Saint Helena room presented as an exact archaeological reconstruction; no nuclear diagrams or construction instructions are needed. No contemporary movie actor is a reference for historical casting.

**Ending:** Back at the empty table in the present, Andre does not claim he has changed history. He asks what his own generation is leaving behind. Whether the encounters alter events is deliberately unresolved fictional storytelling, not an assertion about the historical record.

## 3. Visual contract: what must remain true in every frame

### Andre

1. His approved face, hair, facial hair, and visible accessories stay consistent.
2. Proposed wardrobe: a neutral modern dark shirt/jacket, unchanged across the five eras. Actual colors and garment details are locked only after his reference approval.
3. Keep the tested frontal/three-quarter angle envelope. No orbit shots, sudden profile changes, face-obscuring hands, or portal distortion over his face.
4. Use one principal action and one camera behavior per generation. Prefer a locked camera or a small tested push-in.
5. Andre generally looks camera-right; the interlocutor's eyes look camera-left. Preserve the screen axis unless an explicit neutral reset is approved.
6. Do not invent missing facial geometry from text or an AI-generated angle and call it a photographic reference.

### The historical figures

1. Eyes-only close-ups span the brow to just beneath the lower eyelids, with safe crop margins. No nose tip, mouth, full cheek/jaw, or complete face.
2. Other allowed coverage: hands, sleeve/torso below the neck, a prop, or an empty chair/table detail. Avoid head silhouettes and side profiles when they can reveal facial features.
3. No conventional reverse medium shot or two-shot revealing their face.
4. No face revealed in cups, windows, polished objects, glass, shadows with facial detail, or background portraits.
5. The eyes never zoom out into a full head. Do not ask the generator to discover a new composition during the shot.
6. Each figure has an approved eyes reference, costume fragment, and two restrained emotion states. These are fictional casting choices, not verified reproductions of the person's actual eyes.
7. Exclude extra background people: they add uncontrolled face/period/continuity risks without serving the scene.

### Table, camera, and light

- Lock table dimensions/proportions, grain direction, edge damage, prop positions, and Andre's seating position in a table bible.
- Give each chapter an era-specific ambient palette but preserve readable skin and the table's material identity.
- Prefer diffuse directional light over rapidly changing hard light on a face.
- Perform time transitions on the tabletop, hands, empty-chair detail, or environment plate. Add a sound bridge. Do not dissolve different facial geometries into each other.
- The final full-frame and final crop both require review; a tight requested crop in the prompt is not sufficient evidence.

## 4. Fix the character foundation before spending on the full film

### Required new reference packet

Andre supplies **six clean camera photographs**:

- `front-neutral`: straight-on, neutral expression.
- `three-quarter-left`: approximately the intended left three-quarter view.
- `three-quarter-right`: matching right three-quarter view.
- `profile-left` and `profile-right`: for geometry coverage, not permission for large head turns in every shot.
- `seated-waist-up`: the planned shirt/jacket, posture, and visible hands.

Use the same grooming and wardrobe, neutral background, soft light, sharp eyes, no beauty filter, no sunglasses, and a normal portrait capture distance rather than a close wide-angle selfie. Also useful: one small natural smile and a short neutral-to-speech clip, supplied as additional resources.

**If “generate other angles” means synthetic images:** retain that label and their provenance. They can help composition after approval, but they do not establish the geometry of an unseen side of the face. Prefer actual photographs whenever feasible.

Also obtain the earlier failed clip or its exact generationId. Do not spend on a speculative repair of an unidentified take.

### New production Element

- Create a new versioned Element only after the photographic set is approved. Do not delete the old assets.
- Recommended cover: clean frontal or gentle three-quarter portrait, no collage/UI/text.
- Select up to the currently permitted complementary resources. The documented image-Element route requires cover plus 1–3 secondaries; the full six-photo packet stays in the library, not all inside that limited group.
- Copy the exact live regional tag from discovery. Do not guess a tag or copy it from another region.
- Record its actual returned ID, selected resources, reference version, and approval. Read it back with `element_get` before marking it ready.
- Do not rely on its attached Kling voice for the two-edition plan unless that choice is separately approved; the agreed voice route is Andre's ElevenLabs clone.

### Character bible

`03_bibles/character-andre.md` records only approved observed traits and chosen production details: face/grooming, wardrobe, accessories, seated posture, allowed angles, light anchors, and forbidden distortions. Have Andre approve his own perceived likeness. This is human approval, not a claimed biometric identity score.

## 5. Language and speech strategy

### Two deliverables, one visual production

**Edition E — all English:** Andre and all five interlocutors speak English. It is the first script/animatic/picture-lock target.

**Edition H — historical-language conversations:** Both speakers use the approved language for that encounter. Add reviewed English subtitles. Reuse the same accepted eye/hand/listening/environment footage; only mouth-visible Andre segments need language-specific synchronized variants when the chosen route requires them.

| Encounter | Intended target, still subject to review | What must not be assumed |
|---|---|---|
| Caesar | Latin with a declared classical pronunciation convention | The provider/model/account inspected has not proved production-quality Latin support. Do not invent a language code or accept plausible-sounding pseudo-Latin. |
| Genghis Khan | A reviewed approximation of 13th-century Mongolian | Current documentation lists modern Mongolian for Eleven v4, but this does not certify period speech or the user's access to that model.[6] |
| Galileo | Italian with an explicitly reviewed period/region adaptation | Modern Italian TTS is not proof of reconstructed seventeenth-century Tuscan pronunciation.[6] |
| Napoleon | His Corsican/Tuscan-rooted childhood speech, with the exact target settled by a qualified reviewer | Do not silently call French his mother tongue. Fondation Napoléon describes a Corsican dialect akin to Tuscan and discusses Italian usage; adult French is a separately approved adaptation, not the same requirement.[8] |
| Oppenheimer | English | Keep his voice distinct from Andre's; do not clone a contemporary actor to obtain a recognizable movie imitation. |

For Latin, historical Mongolian, and Napoleon's childhood language, run a **small pronunciation/meaning test** and get a language reviewer before the full audio. An unverified target remains pending. If a target cannot be delivered adequately, present the alternatives—expert-recorded performance, declared modern-language adaptation, or delaying Edition H. Never quietly substitute a convenient language.

### ElevenLabs and lip-sync are separate gates

ElevenLabs model capabilities differ by model; select from the user's actual account and current documentation, not a generic promise of universal language support.[6]

ElevenLabs dubbing is an audio localization workflow; it must not be confused with a guarantee that the final video mouth movements match the translated speech.[7]

A concrete candidate external-audio path exists in ElevenLabs Image & Video documentation: **Sync 3** and **Sync Lipsync 2 Pro** take a source video and speech audio. Their availability, cost, and quality on Andre's beard/face have not been tested here; their facial-preservation descriptions are provider claims, not our results.[11]

**Speech-pilot decision:**

1. Obtain a short, consented Andre clone sample in English and one hard target-language sample.
2. Produce a controlled, approved Andre video with the new references.
3. If the candidate lip-sync path is available and its separate cost is approved, process only a short passage with final speech.
4. Inspect mouth, teeth, jaw, beard, cheeks, eyes, and audio timing over the entire processed clip. Keep the original beside it.
5. If it changes his likeness or cannot achieve acceptable synchronization, reject it. Try an explicitly approved alternative or use motivated L/J cuts over the listener's eyes and the tabletop.
6. That coverage fallback is a directing decision requiring approval; it must not reduce all five encounters to disconnected voiceover slides.

**No invented Kling lip-sync command:** the CLI discovery inspected for these routes did not establish an external speech-audio input for the selected image-to-video models. A generic `--audio` flag elsewhere is not evidence for a specific model. Refresh live declarations before production.

**Separate budgets:** 7,741 is the Kling balance. ElevenLabs cloning/TTS/dubbing/lip-sync, reviewers, music licenses, and any external tool charges are not funded by Kling credits and have no new purchase authorization from this plan.

## 6. English screenplay draft — approval required before recording

All dialogue below is **invented for this film**. It is not an attributed historical quotation. Its factual anchors are cited in the notes. Modern-reputation language is a deliberately limited dramatic synthesis—not a claim that all people today hold the same view.

The target is roughly a few short exchanges per 42-second chapter, leaving room for listening and eye reactions. **Actual approved audio duration, not a word-count estimate, controls the edit.** Tighten wording after scratch performance; do not cram it into the window by accelerating the voice.

### Opening — 12 seconds

**Andre, over the table/his arrival:**

> I wanted to ask history a question. Not what happened. What it felt like to hear what came next.

A hand rests on the wooden edge. Ambient present-day sound falls away. Cut through the table motif into Rome. No portal distorts his face.

### C — Julius Caesar

**C-L01 — Caesar, offscreen:**
> Does my name survive?

**C-L02 — Andre:**
> Your name survives. So do the reforms and the victories people study. But they also study how much power one man can hold—and what happens to a republic around him.

**C-L03 — Caesar, offscreen:**
> Then they remember a tyrant?

**C-L04 — Andre:**
> They argue about you. A brilliant commander. An ambitious ruler. I came to ask what victory leaves behind.

**Eye cue A:** focused confidence at “Your name survives.”

**Eye cue B:** the gaze holds, then loses a fraction of certainty at “what happens to a republic.” No caricatured rage.

**Factual note:** Military achievement, reforms, and his contested contribution to the Republic's transformation are grounded anchors; avoid making him the single cause of every later imperial development.[1]

### K — Genghis Khan

**K-L01 — Khan, offscreen:**
> Will my sons keep what I have made?

**K-L02 — Andre:**
> They will enlarge it. Routes across Eurasia will carry merchants, ideas, and knowledge. But conquest also leaves ruined cities and families who never return.

**K-L03 — Khan, offscreen:**
> And what will they call me?

**K-L04 — Andre:**
> A founder. A conqueror. They will argue about what your empire joined—and what it destroyed. None of those words can make the dead speak.

**Eye cue A:** controlled pride at “They will enlarge it.”

**Eye cue B:** hardened pupils soften into guarded stillness at “families who never return.” Use a restrained blink, not an unexplained tear.

**Factual note:** Attribute later expansion and exchange to the empire and its successors, not every later conquest personally to Genghis Khan. The scholarly account covers the connected-world legacy alongside destructive warfare.[2][15]

### G — Galileo Galilei

**G-L01 — Galileo, offscreen:**
> Am I finally believed?

**G-L02 — Andre:**
> People learn from you. They also turn you into a simple story: one scientist against a whole world. The truth is harder than that.

**G-L03 — Galileo, offscreen:**
> And what survives of the question?

**G-L04 — Andre:**
> Your observations. And the warning in your trial. Silencing a person does not settle a question.

**Eye cue A:** exhausted attention, not blindness, at “People learn from you.”

**Eye cue B:** quiet renewed resolve at “does not settle a question.”

**Factual note:** Keep the trial, sentence, and house-arrest context accurate. Do not invent him saying “And yet it moves,” or claim that every element of the later popular Galileo story is established by these sources.[3][12]

### N — Napoleon Bonaparte

**N-L01 — Napoleon, offscreen:**
> Does France keep my laws?

**N-L02 — Andre:**
> Your civil code outlives your throne. Other countries borrow from it. But a law can promise equality and still deny it to someone.

**N-L03 — Napoleon, offscreen:**
> And do they call me great?

**N-L04 — Andre:**
> Some do. Others ask about the wars and the power you kept for yourself. When they say greatness, they still argue about the price.

**Eye cue A:** pride at “outlives your throne.”

**Eye cue B:** wounded attention, then a contained downward glance at “still deny it to someone.”

**Factual note:** The code's lasting international influence and patriarchal constraints support the contrast; do not call its protections universal. The empire/exile chronology frames the location. Reputation lines remain dramatic interpretation.[4][17]

### O — J. Robert Oppenheimer

**O-L01 — Oppenheimer, offscreen:**
> Does the test work?

**O-L02 — Andre:**
> It works. Weeks later, atomic bombs strike Hiroshima and Nagasaki. People will argue about ending the war, about those who died, and about the fear that follows.

**O-L03 — Oppenheimer, offscreen:**
> Can you tell me whether it was right?

**O-L04 — Andre:**
> I can tell you what came next. That is not the same as answering the question.

**Eye cue A:** the anticipated triumph empties at the names of the cities.

**Eye cue B:** near-still eyes at “not the same as answering.” Hold the silence.

**Factual note:** Trinity and the two bombings have separate documented anchors.[5][18][19]

The contemporary debate is separately documented.[9]

Do not assert a single uncontested explanation of Japan's surrender, fabricate casualties, or present the famous later Oppenheimer quotation as a recorded spoken line at this fictional table.

### Ending — 18 seconds including a short credits tail

**Andre, at the empty table in the present:**

> I went looking for answers in the past. I came back with a question for us. What will they have to tell us about the things we are doing now?

Hold briefly. Fade on the table, not through a face. Include a concise fictionalization notice and production/source/voice credits. Full source notes can accompany delivery rather than crowding the dramatic frame.

## 7. Storyboard and timing inventory

**Target:** 12-second opening + five 42-second chapters + 18-second ending = **240 seconds**.

**Inventory:** **41 primary storyboard/edit slots**. This is **not** a promise of 41 paid jobs, 41 distinct generated assets, or an immutable final cut count. Longer slots may require multiple accepted clips/insert cuts; accepted pilot shots and neutral coverage can be reused if continuity holds. The final manifest tracks those mappings explicitly.

The shared chapter pattern is `[4, 10, 4, 8, 4, 7, 5]` seconds. The 10-second dialogue slot is a coverage window, **not a mandate for a risky uninterrupted 10-second facial performance**. Split it into shorter tested speaking/listening coverage if necessary, with revised cut mapping and no change to approved meaning.

| Slot ID | Chapter | Target seconds | Picture / dramatic purpose | Mouth / face restriction |
|---|---|---:|---|---|
| IN-01 | opening | 4 | Present-day table grain; Andre's hand enters | No opponent; no face needed |
| IN-02 | opening | 4 | Andre's approved three-quarter view; opening question | Andre only; tested speech or offscreen overlap |
| IN-03 | opening | 4 | Table match cut; Rome atmosphere arrives | Transition away from face |
| C-01 | caesar | 4 | Arrival/table edge; sleeve/hand suggests Caesar | Opponent below neck only |
| C-02 | caesar | 10 | Andre answers C-L01; opening consequence | Andre only; split if speech test requires |
| C-03 | caesar | 4 | Eye response to name/power | Eyes-only safe crop |
| C-04 | caesar | 8 | Andre listens to C-L03, begins answer | Andre only |
| C-05 | caesar | 4 | Eye uncertainty at republic/legacy | Eyes-only safe crop |
| C-06 | caesar | 7 | Table/hand tension; C-L04 continues | No face; motivated L-cut |
| C-07 | caesar | 5 | Andre's restrained closing look; table transition | Andre only; no facial morph |
| K-01 | genghis | 4 | Tent-lit table; a resting sleeve/hand | Opponent below neck only |
| K-02 | genghis | 10 | Andre on succession/exchange | Andre only; split if speech test requires |
| K-03 | genghis | 4 | Eye pride at enlarged empire | Eyes-only safe crop |
| K-04 | genghis | 8 | Andre on destruction; listens to K-L03 | Andre only |
| K-05 | genghis | 4 | Eye reaction to missing families | Eyes-only safe crop |
| K-06 | genghis | 7 | Hand loosens on table; K-L04 overlaps | No face |
| K-07 | genghis | 5 | Andre holds the consequence; match cut | Andre only; transition off face |
| G-01 | galileo | 4 | Quiet table, paper/hand, Arcetri atmosphere | Opponent below neck only |
| G-02 | galileo | 10 | Andre answers about remembrance | Andre only; split if speech test requires |
| G-03 | galileo | 4 | Eye attention through weariness | Eyes-only safe crop |
| G-04 | galileo | 8 | Andre on the harder story; listens to G-L03 | Andre only |
| G-05 | galileo | 4 | Eye resolve at “question” | Eyes-only safe crop |
| G-06 | galileo | 7 | Paper/hand stillness; G-L04 overlaps | No face |
| G-07 | galileo | 5 | Andre's quiet respect; table cut | Andre only; no facial morph |
| N-01 | napoleon | 4 | Sea-worn light at plain table; sleeve/book | Opponent below neck only |
| N-02 | napoleon | 10 | Andre on the code's survival | Andre only; split if speech test requires |
| N-03 | napoleon | 4 | Eye pride | Eyes-only safe crop |
| N-04 | napoleon | 8 | Andre on exclusions; listens to N-L03 | Andre only |
| N-05 | napoleon | 4 | Eye pride bruised by the cost | Eyes-only safe crop |
| N-06 | napoleon | 7 | Hand stops over book/table; N-L04 overlaps | No face |
| N-07 | napoleon | 5 | Andre closes without verdict; table cut | Andre only; no facial morph |
| O-01 | oppenheimer | 4 | Sparse night-lit table near test setting | Opponent below neck only |
| O-02 | oppenheimer | 10 | Andre on the test and two cities | Andre only; split if speech test requires |
| O-03 | oppenheimer | 4 | Anticipation drains from the eyes | Eyes-only safe crop |
| O-04 | oppenheimer | 8 | Andre listens to O-L03 before answering | Andre only |
| O-05 | oppenheimer | 4 | Eye stillness at the moral question | Eyes-only safe crop |
| O-06 | oppenheimer | 7 | Hand/table; O-L04 and a deliberate pause | No face |
| O-07 | oppenheimer | 5 | Andre acknowledges uncertainty; present-day cut | Andre only; no facial morph |
| OUT-01 | ending | 6 | Present-day Andre begins the closing thought | Andre only; tested speech coverage |
| OUT-02 | ending | 6 | Empty opposite chair/table; final thought overlaps | No invented historical face |
| OUT-03 | ending | 6 | Table hold/fade; concise credit tail | No face |

Timing is a target to validate with real audio. Reaction words are editorial anchors, not a command to force a blink at an exact generated timestamp. Trim acceptable handles to align reactions with the actual performance.

## 8. Model selection and prompt system

### Read-only discovery before each production phase

These are discovery templates, not paid submissions:

```bash
kling account --quiet --skill-name kling-cli --skill-version 0.2.0
kling who_am_i --quiet --skill-name kling-cli --skill-version 0.2.0
kling tool_list --quiet --skill-name kling-cli --skill-version 0.2.0
kling image_to_image --help --skill-name kling-cli --skill-version 0.2.0
kling image_to_video --help --skill-name kling-cli --skill-version 0.2.0
```

Parse complete JSON stdout before reducing it; live tool groups may contain `{defaultModel, models[]}`. Preserve exact tokens and read both model-level inputs and tool restrictions. Discovery, not an expensive job, resolves compatibility.

### Candidates observed, not ranked by unmeasured quality or price

| Route | Intended role | Selection gate |
|---|---|---|
| Compatible `image_to_image` with live-declared Elements | Approved Andre keyframes | Exact model token, image Element type, combined input count, tags, and binding all verified |
| `image_to_video` / `kling-video-v3_0` | Main face-bearing clips when its explicit Element/reference route is valid | Pilot must pass likeness, motion, framing, and actual charge review |
| `image_to_video` / `kling-video-v3_0_turbo` | Animate a single approved keyframe; potential neutral/cutaway route | It is a distinct strategy when direct Element binding is absent; needs approval, not a silent substitute |
| `image_to_video` / `kling-video-v3_0_omni` | Additional compatible reference input only when the shot needs it | Check live input slots and shared limits; more references are not automatically better |
| `omni_ref_video` or motion control | Only a justified pilot alternative for performance | Resolve live type/input conflicts first; not a default requirement for a seated low-motion film |

Some live descriptions disagree on video-Element compatibility in mixed-reference/motion routes. Pause that route rather than spending credits to guess. Image Elements and controlled keyframes are the preferred starting point.

### Shot prompt contract

Every approved shot specification includes: shot ID, one dramatic action, framing, one camera behavior, screen direction, exact reference/Element versions, intended duration/aspect/mode, allowed motion, negative constraints, and the review checklist.

**Andre face-bearing prompt skeleton, not an executable command:**

> Photorealistic cinematic medium close-up of <<<ACTUAL_APPROVED_ELEMENT_ID>>> seated at the approved plain wooden table in the approved scene. Preserve the approved face, grooming, wardrobe and seated posture. He looks camera-right toward an offscreen listener and [ONE RESTRAINED ACTION]. Locked camera, [APPROVED SOFT LIGHT], minimal head movement within the tested angle. No other visible face, no face obstruction, no sudden profile, no camera orbit, no changing beard or facial geometry, no text or UI. Composition matches the approved keyframe.

When the selected route supports direct binding, supply the matching live-schema `elements` binding as well as the marker. Replace placeholders only from recorded approved assets; never submit them literally. Describe speaking only after the actual speech path has passed its pilot.

**Historical eye prompt skeleton:**

> Extreme close-up of the approved [FIGURE] eyes reference only, framed from brow to immediately below lower eyelids. Gaze camera-left. [ONE SUBTLE REACTION TO THE LINE]. Locked camera, no pull-back, no widening frame, no nose tip, mouth, cheek/jaw reveal, face reflection, extra person, modern accessories or text. Preserve the same eye appearance and light direction as the approved keyframe.

**Table transition skeleton:**

> Close view of the approved wooden tabletop and Andre's resting hand, same grain and edge position. [ONE ENVIRONMENT/LIGHT CHANGE OR PHYSICAL ACTION]. No face enters the frame. Locked camera. No altered hand anatomy or changing table geometry.

Local editing can accomplish the era transition more reliably than asking one paid shot to morph a character and a whole room at once. Keep provider media-input restrictions intact; do not download/reupload a previous output merely to bypass a required-input conflict.

## 9. Credit plan — allocate the full ceiling, spend by evidence

The verified planning balance is **7,741 Kling credits**. Allocations below sum to that exact ceiling; they are phase caps, **not provider price quotes or predictions of a zero remaining balance**.

| Phase | Credits allocated | Purpose | Release condition |
|---|---:|---|---|
| A — identity and speech validation | 1,161 | Clean-reference pilot, controlled route comparison, essential test retakes | References and candidate shot specifications approved |
| B — references and storyboard | 774 | Missing approved scene/eye/table keyframes; avoid unnecessary variants | Pilot passes; script and framing contract approved |
| C — main five-chapter footage | 3,483 | Prioritized, chapter-by-chapter initial coverage | Actual pilot charges support a feasible coverage forecast |
| D — targeted corrections and language-dependent picture | 1,935 | Rejected face shots, missing reactions, approved alternate-language picture needs | Picture gap identified with exact reason and replacement specification |
| E — final quality reserve | 388 | Only justified final replacement/enhancement where the underlying take is already sound | Rough cut and full QC expose a concrete issue |
| **Total** | **7,741** | Full authorized ceiling | No top-up/purchase implied |

### Forecast after the pilot

Record actual charge per accepted face clip, eye clip, table/insert clip, and necessary keyframe. Distinguish charge from cost per usable second; a failed/rejected take still affects the budget.

Compute with Python from the real ledger:

- `forecast_initial_coverage = sum(actual_or_quoted_cost_for_each_unfilled_asset)`
- `effective_cost_per_accepted_second = total_charged / accepted_usable_seconds`
- `remaining_balance = current_account_balance`, reconciled against recorded charges.

If coverage does not fit Phase C plus deliberately released reserve, reduce unnecessary alternates, reuse compatible accepted pilot/listening footage, and favor motivated neutral cutaways. Do not silently discard a chapter, shorten the film below the agreed scope, or accept face damage. Present the measured constraint and get approval for any changed scope.

### Spending rules

1. Start with approved individual pilot shots, not a mass film batch.
2. An approved phase/shot manifest may authorize specified first submissions. Failed-job retries, changed prompts/models/references, and additional variants remain explicit decisions; never silently resubmit.
3. Record the returned generationId immediately. If a submission result is uncertain, query the original job; do not repeat the request to recover its ID.
4. Use returned `creditsConsumed` when present. Otherwise mark unknown and reconcile account changes; never invent a per-shot charge.
5. Check remaining balance after a completed/reconciled batch, not just at the end of the film.
6. Reallocate unused phase caps only with a recorded quality reason. Prioritize likeness failures, forbidden-face reveals, dialogue synchronization, and missing story coverage over cosmetic upgrades.
7. Spending all remaining credits is allowed if useful. Do not generate filler or force a purchase to obtain an exact zero.
8. No production job is currently submitted; all accepted-take fields begin null.

## 10. Step-by-step execution, with hard acceptance gates

A step is a small editorial/inspection action; generator waits, recordings, translation review, and full-playback QC naturally take longer than a coding task. Do not present a speculative completion schedule as guaranteed.

### Task 01 — Freeze the brief and spending boundaries

**Objective:** Make the two editions, visual restrictions, and provider-specific spending scope explicit.

**Create:** `00_brief/brief.md`, `00_brief/approvals.json`.

- Confirm the working title/tone and approximately four-minute target.
- Preserve the five selected figures and eyes-only rule.
- Record the 7,741-credit snapshot; refresh it before spending.
- Record the user's separate ElevenLabs/other-service spending scope, if any.
- Do not launch production until those scopes are clear.

**Pass:** Brief and paid-shot approval boundaries are recorded; no silent assumptions about external fees.

### Task 02 — Receive references and the failed scene

**Objective:** Obtain the actual face evidence rather than another style description.

**Create:** `02_references/andre/raw/`, `asset-registry.csv`.

- Receive the six main photographs and any speech/extra expression resources.
- Record file provenance and photograph versus synthetic status.
- Receive failed clip/generationId, if recoverable; inspect the exact failure window.
- Load every proposed reference and flag layout/UI/lighting/occlusion problems.

**Pass:** Andre approves the raw-to-selected reference packet; unresolved failure cause stays labeled unresolved.

### Task 03 — Lock the character and table bibles

**Objective:** Define the visual invariants every chapter reuses.

**Create:** `03_bibles/character-andre.md`, `03_bibles/continuity-matrix.csv`, `02_references/table/`.

- Select wardrobe, grooming, accessories, seated posture, and safe angles.
- Approve the table and repeatable hand/edge composition.
- Record forbidden motions and the eyes-only crop/reflection rules.

**Pass:** Approved traits are concrete, visually inspectable, and not invented from an unapproved illustration.

### Task 04 — Create and verify the new Andre Element

**Objective:** Obtain a clean, versioned production subject without destroying previous assets.

**Create/update:** `asset-registry.csv`, `manifest.json`.

- Read live creation/binding restrictions and tags.
- Create once from the approved cover and permitted secondaries.
- Read back the exact returned ID and all resources; inspect them.
- Record voice route separately; do not silently switch away from ElevenLabs.

**Pass:** User-approved resources and verified compatible bindings are recorded. Old Elements remain untouched.

### Task 05 — Fact-check and approve the English script

**Objective:** Lock the five conversations and consequences before media costs grow.

**Create:** `00_brief/research.md`, `01_script/script-en.md`, `01_script/dialogue-lines.csv`.

- Review the draft lines with the cited claims and fictionalization boundaries.
- Give every spoken line its stable ID, speaker, emotion, and target scene window.
- Tighten wording after a scratch performance, preserving meaning and historical nuance.
- Approve opening, five emotional turns, and ending.

**Pass:** All five chapters are present; no invented quotation, unsupported precise number, or unanimous-reputation claim slips into narration.

### Task 06 — Resolve historical-language targets and reviewers

**Objective:** Turn “native language” into precise, achievable production requirements.

**Create:** `01_script/language-matrix.csv` and per-language reviewed scripts.

- Declare Latin pronunciation, Mongolian approximation, Galileo's Italian adaptation, and Napoleon's childhood-language target.
- Inspect actual ElevenLabs account/model access and test short phrases.
- Obtain translation/back-translation and pronunciation review.
- Record any alternative needing explicit approval; do not silently choose French for Napoleon.

**Pass:** Each target has confirmed support plus review, or an explicit pending/blocker status. Edition E can proceed independently; Edition H cannot be called complete while this is unresolved.

### Task 07 — Approve voice samples and dry dialogue

**Objective:** Freeze speech meaning and timing before final picture.

**Create:** `04_audio/voice-tests/`, `04_audio/en/`, `04_audio/historical/`.

- Use Andre's approved clone for Andre and distinct consented/designed voices for the others.
- Test names, one neutral line, and one emotional line in each required language.
- Export dry line/speaker tracks; measure actual durations with ffprobe.
- Keep dialogue, ambience, and music separate.

**Pass:** Voice/meaning/pronunciation are approved and each chapter can fit its target without unnatural acceleration. No new external purchase occurs automatically.

### Task 08 — Approve a restrained four-shot identity pilot

**Objective:** Prove stability at the actual planned camera, light, and motion before full production.

**Create:** `06_pilot/originals/`, `06_pilot/pilot-review.json`, ledger entries.

- `PIL-01`: locked frontal/near-frontal listening, short duration.
- `PIL-02`: a gentle tested three-quarter head change, no orbit.
- `PIL-03`: the planned emotional close-up, minimal movement.
- `PIL-04`: controlled visible-speech candidate for the separate sync test.
- Start in the relatively restrained Galileo-style setup; do not use a busy time portal as the likeness test.
- Approve stills before animation and log actual charges. Compare a second route only if it answers a real question within Phase A.

**Pass:** Andre approves likeness; every face-bearing frame is clean; angle/expression transitions are stable. If the pilot repeatedly fails, stop and revise the references/strategy rather than consuming the whole budget.

### Task 09 — Prove the speech route in both edition strategies

**Objective:** Verify that the voice plan does not break the face.

**Create:** `06_pilot/speech-variants/`, corresponding review entries.

- Process only an approved short clip with real English dialogue using an available, separately approved sync tool.
- Test one difficult historical-language sample rather than producing five full localized chapters blindly.
- Inspect the processed clip in full, including areas outside the mouth.
- Approve the primary sync route or a deliberate L/J-cut coverage fallback.

**Pass:** No unacceptable mouth mismatch or likeness damage. A failed route is not marked good because its job completed.

### Task 10 — Reforecast costs and freeze the production envelope

**Objective:** Use measured charges and accepted seconds to protect completion.

**Create/update:** `credit-ledger.csv`, `manifest.json`, `03_bibles/continuity-matrix.csv`.

- Compute actual costs and coverage forecast in Python.
- Lock model/settings, reference versions, safe motions, and speech strategy.
- Set chapter/shot release caps from the real forecast, not generic pricing memories.

**Pass:** Feasible forecast for all five chapters, or a surfaced scope decision before further spending.

### Task 11 — Approve the storyboard and audio-first animatic

**Objective:** Test pacing and the conversations as a film before final video batches.

**Create:** `05_storyboard/keyframes/`, `05_storyboard/animatic-en.mp4`, `05_storyboard/animatic-historical.mp4` when its audio is ready.

- Build the 41-slot inventory using actual dialogue and temporary/approved stills.
- Confirm screen axis, eye-crop safety, prop positions, and the table motif.
- Check every emotional reaction against the triggering line.
- Make the local animatic before requesting extra costly variants.

**Pass:** The story works at target pacing and all five encounters feel conversational. Label these files animatics/previsualization, not finished movies.

### Task 12 — Approve era and eye keyframes

**Objective:** Obtain stable scene anchors without rendering unnecessary full historical faces.

**Create:** `02_references/history-eyes/`, `03_bibles/scene-bibles/`, approved keyframes.

- Approve one environment/table anchor and the necessary Andre angles per chapter.
- Approve each figure's eyes-only appearance and two restrained reaction states.
- Use original fictional historical casting, not modern film-actor portraits.
- Do not pay for five full historical-face Elements unless an actual compatible shot requirement justifies them.

**Pass:** Period/style/geometry are coherent and no keyframe violates the framing contract.

### Task 13 — Produce Galileo as the first complete chapter

**Objective:** Validate the end-to-end chapter recipe before all five are submitted.

**Create:** accepted/rejected G takes and `08_edit/picture-lock/galileo-en-preview.mp4`.

- Submit approved shots individually; persist each returned generationId/charge.
- Poll via successive CLI calls; retain all actual output URLs and originals.
- Review every output before acceptance, then assemble the 42-second chapter with real audio.
- Validate eye reactions, speech strategy, face stability, table continuity, and actual cost.

**Pass:** A complete, reviewed chapter exists—not seven successful but incompatible job statuses.

### Task 14 — Produce Caesar coverage

**Objective:** Transfer the tested recipe into Rome without losing Andre or revealing Caesar.

**Create:** C accepted/rejected takes, scene preview, ledger entries.

- Review the changed light/costume/props against the locked bible.
- Produce only unfilled C slots and necessary speech variants.
- Validate the eye cues against C-L02/C-L04 and inspect reflections.

**Pass:** All C story requirements mapped to accepted footage with costs reconciled.

### Task 15 — Produce Genghis Khan coverage

**Objective:** Preserve nuance and continuity in the tent-lit chapter.

**Create:** K accepted/rejected takes and preview.

- Keep tent movement/light restrained; do not obscure Andre with smoke or flames.
- Use approved eye casting and below-neck costume cues.
- Validate succession/conquest wording and the translated audio if ready.

**Pass:** All K slots and narrative beats accepted; no period/camera/framing drift.

### Task 16 — Produce Napoleon coverage

**Objective:** Deliver the law/power contrast without a modern actor imitation or language substitution.

**Create:** N accepted/rejected takes and preview.

- Use approved Saint Helena-inspired, explicitly fictional room design.
- Check law/exclusion line timing and pride-to-reflection eye beats.
- Keep the historical-language status visible; English completion is not evidence that Corsican/Italian-rooted speech is done.

**Pass:** All N slots accepted and edition mappings accurate.

### Task 17 — Produce Oppenheimer coverage

**Objective:** Finish the dramatic escalation through silence rather than spectacle.

**Create:** O accepted/rejected takes and preview.

- Keep the setting sparse; no need to show a blast or technical bomb details.
- Align the two eye reactions with the city names and moral-question line.
- Protect natural pauses and do not use triumphant music over the consequence.

**Pass:** All O slots accepted, factual wording checked, and quiet ending retains its impact.

### Task 18 — Produce opening/ending and lock the English picture

**Objective:** Connect the chapters with the table motif and close on present responsibility.

**Create:** IN/OUT takes, `08_edit/picture-lock/film-en-picture-lock.mp4`.

- Reuse compatible clean pilot/neutral footage where it serves the approved composition.
- Normalize streams before editing mixed clips.
- Keep time transitions off faces; preserve the screen axis and color anchors.
- Inspect a full rough cut and list only concrete replacement needs.

**Pass:** Five chapters plus opening/ending play coherently; every edit slot maps to real accepted media.

### Task 19 — Spend the correction reserve on measured gaps

**Objective:** Fix rejected frames or missing coverage, not decorate an already unstable face.

**Create/update:** replacement takes, reviews, credit ledger, manifests.

- Rank gaps: likeness damage → forbidden face exposure → sync → missing story coverage → hands/table → cosmetic polish.
- State exact rejected shot/frame range and one revised hypothesis per replacement.
- Obtain applicable paid retry/change approval; do not silently regenerate.
- Reconcile charges and read remaining balance before releasing more reserve.

**Pass:** Replacement targets are solved or openly blocked; no fabricated accepted status.

### Task 20 — Assemble and verify the historical-language edition

**Objective:** Reuse the picture safely while honoring reviewed speech and captions.

**Create:** `08_edit/picture-lock/film-historical-picture-lock.mp4`, per-language subtitles.

- Replace audio by stable line IDs.
- Use separately accepted speech variants only where Andre's mouth is visible.
- Adjust pauses/eye/prop handles where translation needs them; do not time-warp facial speech to hide a mismatch.
- Obtain language review of audio and subtitles against each other.

**Pass:** Every chapter's language requirement is fulfilled or explicitly approved as an adaptation; pending ancient-language work prevents an “all done” claim.

### Task 21 — Finish, deliver, and independently verify both masters

**Objective:** Deliver working movies, not a folder of links or a plan claimed as a movie.

**Create:** `09_delivery/film-en.mp4`, `09_delivery/film-historical.mp4`, captions, stems, QC, final manifest.

- Export explicit target settings: 16:9, 1920×1080 delivery, 24 fps, H.264/yuv420p picture and compatible AAC audio; these are chosen delivery targets, not provider output assumptions.
- Target intelligible dialogue; proposed web mix target is about −16 LUFS integrated with true peak at/below −1 dBTP. Measure the result and adjust; do not report the targets as measurements.
- Preserve clean originals/highest accepted source quality. Do not call a 4K upscale a likeness repair.
- Verify stream metadata, full decode, subtitle timing, all joins, and end-to-end playback for both editions.
- Obtain Andre's final perceived-likeness and story approval.
- Package local downloadable files, subtitles, stems, research/rights notes, and ledger; provider URLs alone are insufficient archival delivery.

**Pass:** Section 13 is satisfied on the actual final files. Report blockers instead of creating a plausible-looking completion report.

## 11. Take tracking and safe job orchestration

### Manifest fields

For each shot/take keep:

- stable chapter/shot/take IDs and planned editorial duration;
- approval and version of the exact prompt/parameters;
- live-declared model token, mode, duration, aspect ratio, input count;
- character/table/eye reference versions and exact actual Element IDs;
- generationId, submission time, state, returned charge or unknown;
- every output URL/file and any partial-completion state;
- full-frame review, likeness approval, crop/reflection/speech checks;
- accepted take ID, real in/out points, usable duration, rejection reason;
- language variant and reuse mappings;
- account reconciliation, not just an estimated cost.

Initial accepted-take IDs and actual charges are **null**, not invented placeholders masquerading as results.

### Interactive job lifecycle

- Submit once through the CLI with actual approved values and metadata flags.
- Immediately persist/report its actual generationId and any returned `creditsConsumed`.
- Poll with individual `kling query_tasks ACTUAL_ID --skill-name kling-cli --skill-version 0.2.0` calls. Do not launch background polling or a long one-shot polling loop.
- Treat COMPLETED/PARTIAL_COMPLETED as “ready to inspect,” never “approved.”
- On failure, describe the actual error and request the applicable retry decision. Feedback is not a refund or proof of repair.
- Download accepted outputs promptly for archival/editing. Do not download/reupload them merely to bypass a model's input-source restrictions.
- Read back exact external assets after create/update before claiming success. Never touch secrets or credential files.

## 12. Risks and rejected shortcuts

| Risk / tempting shortcut | Why it is excluded | Safer route |
|---|---|---|
| Reuse current Andre Elements without auditing resources | Illustrated/UI/mixed-trait references are not approved clean photos | New photographic packet and versioned Element |
| Generate new angles from the existing illustration | May reproduce a coherent but inaccurate synthetic face | Photograph missing angles; approve any synthetic variant separately |
| One prompt for a four-minute film or all five eras | Hard to control framing, temporal identity, speech, and corrections | Individually approved keyframes/shots and local edit |
| Full reverse shots / camera orbit | May reveal forbidden faces and exceed angle evidence | Andre-only close-ups, fixed eye crops, below-neck inserts |
| Simultaneous face motion, portal morph, speech, and changing light | Adds several failure variables to the principal risk | One action; transitions off face; speech gate |
| “Elements guarantee consistency” | No tested guarantee; artifacts can still appear during motion | Full temporal pilot and take review |
| “Upscaling repairs identity” | Detail enhancement does not establish correct facial geometry | Regenerate/replace the damaged shot with clean references |
| Native Kling audio as the automatic final voice | Not equivalent to the approved ElevenLabs clone | Approved external-audio sync or approved L/J-cut strategy |
| ElevenLabs language list treated as period-language certification | Model support and historical authenticity are different | Reviewer + small actual voice test + precise adaptation label |
| French silently substituted for Napoleon's native speech | Does not fulfill the recovered mother-tongue request | Resolve Corsican/Tuscan-rooted target; adult French only by approval |
| Automatic dub copied over visibly different mouth movements | Creates a second edition with obvious mismatch | Separate speech variants or approved hidden-mouth coverage |
| All credits spent immediately or exact shot prices invented | Risks incomplete coverage and unexplained charges | Pilot-derived forecast, reconciled ledger, staged reserve |
| Mass retry after a missing submission response | May duplicate paid jobs | Query/preserve original ID; pause uncertainty |
| Sampling a few frames as proof no historical face appears | A single violating frame can occur between samples | Full playback plus frame inspection of every restricted shot |
| New purchases or infrastructure built into TransfereGov | Outside this request and mixes unrelated projects | Dedicated film workspace; explicit separate purchase authorization |

## 13. Final acceptance checklist

### Story and coverage

- [ ] Exactly the five named encounters are present, with opening and ending.
- [ ] Each has an actual exchange, a consequence/reputation theme, and eye reactions tied to specific lines.
- [ ] No historical dialogue is mislabeled a real quotation.
- [ ] No single-cause simplification, unsupported casualty number, or universal-reputation assertion is presented as settled fact.
- [ ] Final duration is approximately four minutes; any changed target was explicitly approved.

### Character and framing

- [ ] Andre approves his likeness in every face-bearing shot and in the final edit.
- [ ] No temporal face/beard/jaw/teeth/eye distortion survives.
- [ ] Hair, wardrobe, accessories, angle envelope, eyelines, and table geometry match the bible.
- [ ] Other historical faces appear in **zero frames**, including reflections or brief pull-backs; only approved eyes/body-detail coverage is used.
- [ ] Transitions do not blend or distort facial geometry.

### Speech and editions

- [ ] Andre's voice is the approved clone/performance; other voices are distinct and authorized.
- [ ] English edition has intelligible dialogue and correct visible synchronization.
- [ ] Historical-language targets, adaptations, pronunciation, and subtitles have actual review records.
- [ ] Historical edition has independently verified mouth synchronization where visible.
- [ ] No edition with pending translation/voice support is represented as finished.

### Technical and accounting

- [ ] Every final slot/cut maps to real accepted assets and correct in/out points.
- [ ] Full decoding succeeds for both masters; no corrupt frames, accidental black/silent gaps, or clipped phrase endings.
- [ ] Final stream dimensions, frame rate, codecs, duration, audio loudness/peak, and subtitle timing are inspected/measured.
- [ ] Both exact delivered files receive a full playback, not only source-clip spot checks.
- [ ] Actual charges and remaining balance reconcile; unknowns are surfaced.
- [ ] Local masters, captions, stems, sources/rights notes, and manifest are downloadable and archived.
- [ ] `final_movie_verified` is true only after all applicable checks, not because the plan or provider jobs exist.

### Planned technical verification commands

These target future real files; they have not been run on a finished movie because none exists yet.

```bash
ffprobe -v error -show_format -show_streams -of json "/mnt/data/Projects_SSD/Movies_Projects/projects/andre-time-travel/09_delivery/film-en.mp4"
ffmpeg -v error -i "/mnt/data/Projects_SSD/Movies_Projects/projects/andre-time-travel/09_delivery/film-en.mp4" -f null -
ffmpeg -hide_banner -i "/mnt/data/Projects_SSD/Movies_Projects/projects/andre-time-travel/09_delivery/film-en.mp4" -filter_complex ebur128=peak=true -f null -
```

Repeat against `film-historical.mp4`, then inspect the exact masters visually/audibly. A clean decode is not evidence of good likeness or meaningful eye acting.

## 14. Machine-readable planning inventory

This is planning state, not a completed-production manifest. Validation must check sums/counts, unique IDs, the five chapter identities, and empty production results. It intentionally contains no fake generation IDs, URLs, costs, accepted takes, voice samples, or rendered-file claims.

```json
{
  "schemaVersion": "1.0",
  "project": "andre-time-travel",
  "workingTitle": "The Table Between Centuries",
  "state": "planned_waiting_for_references_and_approval",
  "lead": "Andre Athar",
  "scope": {
    "visualStyle": "photorealistic_cinematic",
    "targetSeconds": 240,
    "openingSeconds": 12,
    "chapterSeconds": 42,
    "endingSeconds": 18,
    "primaryStoryboardSlots": 41,
    "slotCountIsPaidJobCount": false,
    "interlocutorFullFaceAllowed": false,
    "editions": ["all_english", "reviewed_historical_languages"]
  },
  "chapterSlotSeconds": [4, 10, 4, 8, 4, 7, 5],
  "chapters": [
    {"id": "C", "key": "caesar", "person": "Julius Caesar", "setting": "Rome, early 44 BCE", "slotIds": ["C-01", "C-02", "C-03", "C-04", "C-05", "C-06", "C-07"], "languageReview": "pending", "acceptedTakeId": null},
    {"id": "K", "key": "genghis", "person": "Genghis Khan", "setting": "Campaign tent, 1227", "slotIds": ["K-01", "K-02", "K-03", "K-04", "K-05", "K-06", "K-07"], "languageReview": "pending", "acceptedTakeId": null},
    {"id": "G", "key": "galileo", "person": "Galileo Galilei", "setting": "Arcetri, 1634", "slotIds": ["G-01", "G-02", "G-03", "G-04", "G-05", "G-06", "G-07"], "languageReview": "pending", "acceptedTakeId": null},
    {"id": "N", "key": "napoleon", "person": "Napoleon Bonaparte", "setting": "Saint Helena, 1816", "slotIds": ["N-01", "N-02", "N-03", "N-04", "N-05", "N-06", "N-07"], "languageReview": "pending", "acceptedTakeId": null},
    {"id": "O", "key": "oppenheimer", "person": "J. Robert Oppenheimer", "setting": "Fictional room near Trinity, July 15, 1945", "slotIds": ["O-01", "O-02", "O-03", "O-04", "O-05", "O-06", "O-07"], "languageReview": "pending", "acceptedTakeId": null}
  ],
  "openingSlotIds": ["IN-01", "IN-02", "IN-03"],
  "endingSlotIds": ["OUT-01", "OUT-02", "OUT-03"],
  "budget": {
    "provider": "Kling",
    "verifiedBalanceSnapshot": 7741,
    "refreshBeforeSpend": true,
    "phaseCaps": {
      "identity_and_speech_validation": 1161,
      "references_and_storyboard": 774,
      "main_five_chapter_footage": 3483,
      "targeted_corrections_and_language_picture": 1935,
      "final_quality_reserve": 388
    },
    "actualProductionCharges": [],
    "externalAudioServiceBudgetApproved": false,
    "topupAuthorized": false
  },
  "approvals": {
    "characterReferences": false,
    "productionElement": false,
    "screenplay": false,
    "voiceTests": false,
    "speechRoute": false,
    "pilot": false,
    "storyboard": false,
    "paidBatch": false,
    "finalPicture": false
  },
  "takes": [],
  "finalMovieVerified": false
}
```

## 15. Reusable skills created for this workflow

These are original, general filmmaking procedures, not copies of the Kling vendor skill and not Andre-specific job logs. They reside only in the active default Hermes profile.

- `film-character-continuity` — reference audits, clean-photo capture, versioned Elements, safe camera/motion envelopes, full temporal likeness review, and surgical face-drift diagnosis.
- `film-dialogue-localization` — sourced fictional dialogue, native-language versus working-language distinctions, voice consent/tests, audio-first timing, translation review, and separate lip-sync acceptance.
- `film-editing-qc` — shot/take/charge ledgers, eyes-only restrictions, accepted-asset assembly, multilingual finishing, full-file verification, and honest delivery status.

The Kling filmmaking reference now points to these skills and includes the reference-contamination lesson. Skill loading and formatting are checked separately from film production; creating the skills does not establish that any pilot or final film has passed.

## 16. What is needed next

**Immediate production dependency:** Andre's six clean photographs, approved wardrobe, and a short consented voice-clone sample. The failed clip/generationId is also needed to diagnose the earlier face break accurately.

**Approval dependency:** Script/tone; the precise historical-language targets/reviewer strategy; any separate ElevenLabs lip-sync cost; and the small initial pilot manifest.

The next paid work, once those gates pass, is the **controlled identity/speech pilot—not all five chapters at once**. The full remaining-credit allocation is reserved for this film, with quality-driven releases and actual charge reconciliation.

## Sources

[1] https://www.britannica.com/biography/Julius-Caesar-Roman-ruler
[2] https://www.britannica.com/place/Mongol-empire
[3] https://catalogue.museogalileo.it/multimedia/GalileosTrialBis.html
[4] https://www.napoleon.org/en/young-historians/napodoc/chrono-consulat-1er-empire
[5] https://www.osti.gov/opennet/manhattan-project-history/Events/1945/trinity.htm
[6] https://elevenlabs.io/docs/overview/models
[7] https://elevenlabs.io/docs/eleven-creative/products/dubbing
[8] https://www.napoleon.org/en/history-of-the-two-empires/articles/bullet-point-21-what-was-napoleons-mother-tongue
[9] https://www.osti.gov/opennet/manhattan-project-history/Events/1945/debate.htm
[11] https://elevenlabs.io/docs/eleven-creative/playground/image-video
[12] https://catalogue.museogalileo.it/indepth/VillaGioiello.html
[15] https://worldhistoryconnected.press.uillinois.edu/5.2/may.html
[17] https://www.britannica.com/topic/Napoleonic-Code
[18] https://www.osti.gov/opennet/manhattan-project-history/Events/1945/hiroshima.htm
[19] https://www.osti.gov/opennet/manhattan-project-history/Events/1945/nagasaki.htm
