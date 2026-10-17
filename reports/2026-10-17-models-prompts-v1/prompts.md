# Scene prompt library — 16 structured drafts

**Research proposals only · 2026-10-17 · no upload/generation permission.** English prompts preserve the current English screenplay. English is a production choice here, not a claim that it always performs better than Portuguese. All dialogue is fictional, not a historical quotation. These are library IDs `P01`–`P16`, **not new board tasks, shots or approved takes**.

## Quick index

| Draft | Scene / purpose | Stage |
|---|---|---|
| P01 | Galileo principal composition still | Candidate baseline preparation |
| P02 | Galileo minimal listening-pose still | Candidate baseline preparation |
| P03 | Andre listens to G-L03 | Candidate baseline coverage |
| P04 | Andre speaks G-L04 | Proposed first speaking test, gated |
| P05 | Galileo eyes after the difficult line | Candidate baseline reaction, gated |
| P06 | Galileo hand releases tension | Future optional coverage; excluded from initial baseline |
| P07 | Caesar eyes register the precedent | Future encounter library |
| P08 | Khan foot settles after the difficult thought | Future alternate coverage |
| P09 | Andre answers Napoleon without superiority | Future encounter library |
| P10 | Andre cannot answer Oppenheimer's moral question | Future encounter library |
| P11 | Oppenheimer hands hold the silence | Future optional coverage |
| P12 | Opening hand/table contact | Future opening |
| P13 | Table-texture match-cut plate | Future transition/edit |
| P14 | Empty chair and final question | Future ending |
| P15 | Single subtle contact Foley | Separate future audio scope |
| P16 | Historically specific room tone | Separate future audio scope |

## Read before copying

The current source is `projects/andre-time-travel/05_storyboard/source/production-plan.json`, revision `galileo-baseline-2026-10-13`, active baseline `galileo-g03-g04-2026-10-13`: **G-L03/G-L04 first; first speaking test G-P04**. It is prepared, not artistically approved. Existing IN/OUT and references are studies, not approved first/last frames. Wardrobe, table/lasca/ring detail and likeness still have holds. P01–P05 are candidate preparations for that baseline, **not a sequence of five new jobs to submit**. Start with the producer's exact next authorized assignment; create coverage only if the accepted cut needs it. P06–P16 are future library ideas, not current production assignments.

`projects/andre-time-travel/01_script/dialogue-lines.csv` is the exact dialogue source for implementation; `script-en.md` v2 gives dramatic context. If they differ, stop and ask producer to reconcile rather than choosing or paraphrasing. Text below is checked against the current CSV. Review direction: `projects/andre-time-travel/docs/2026-10-09-direcao-encontros-fala-dificil.md`. Historian, lighting and dialogue/sound review remain required before production. This is text-only research, not media inspection or language/performance certification.

### Bind actual inputs, never filenames by implication

Before any future submission, the producer must replace every placeholder with **exact episode-relative path + SHA-256 + allowed use + explicit review state**, and bind the actual model's slots/IDs. Referencing a plan ID is not the same as approval to upload it.

| Placeholder | Intended role / existing source IDs | Required review |
|---|---|---|
| `[IDENTITY]` | Andre likeness; G-ID or separately selected real-photo version | Andre's likeness approval for this input/use; do not inherit approval for synthetic variants |
| `[WARDROBE]` | D02 / G-WARDROBE | Exact fabric, cut and color; current continuity holds resolved |
| `[TABLE]` | D04 / G-TABLE | Shape, wood, ring/lasca details and encounter continuity; no automatic mixing of variants |
| `[ROOM]` | G-ERA or the selected encounter bible/plate | Historical/material review; plate is not proof every depicted detail is historical |
| `[COMPOSITION]` | Selected final composition, replacing/reviewing G-IN/G-OUT studies as needed | Producer/director accepts geometry, eye line, light and crop per version |
| `[EYES]` | G-EYE-B or encounter-specific tight eye crop | No whole face/nose/mouth/chin; every-frame review required after motion |
| `[AUDIO]` | Exact line/guide, source version and duration | Scratch vs final clearly marked; no unapproved cloning/upload; measured timing and full listening separate |

No placeholder in this library is a real Element ID, file delivered by another agent or an approved upload. Existing source paths/hashes in the plan identify candidates, not approvals.

### Required global guard — append to every visual prompt

```text
PROJECT SAFETY AND CONTINUITY: Use only the explicitly bound, reviewed inputs and their assigned roles. Preserve Andre's real likeness, age, facial structure, skin texture, hair and assigned clothing; no beauty filter or invented accessories. Preserve the selected table, screen axis and physically motivated light. Never show a complete historical face in any frame, reflection, picture, monitor or transition; no historical profile or three-quarter face. Unless the shot explicitly requests the separately reviewed eyes-only crop, keep the entire historical head outside the image, not merely shadowed or blurred. Do not reveal it through reframing, motion or an inserted shot. No extra characters, subtitles, logos, invented text, face morphing, floating hands or unmotivated light. Follow the historical/material review; Andre's modern clothes and the traveling-table premise are deliberate exceptions, not permission for other anachronisms.
```

A card's **final prompt = its body + this guard**. The guard is an operating instruction, not technical enforcement. Negative fields are not universal. A model may ignore the crop; reject any unsafe output and do not assume a retry is authorized.

### Timing and route rules

- One main physical action and one camera behavior per shot. Cinematic style never overrides evidence or the crop.
- G-L03 guide is **2.832 s** and G-L04 guide **8.616 s** as recorded in the current plan; these are existing scratch measurements, **not newly listened-to or approved performances**. The baseline proposes about **11 s** for G-P04, subject to timing/contract/quote. Never compress the line to fit a cheap five-second clip.
- G-REACTION's **2 s is a proposed edit selection**, not a request for an unsupported 2-second Kling V4 generation. V4 declares a 3-second minimum; any eventual generation must leave reviewed handles and be trimmed in edit. Framework 3–5 s versus later 1.5–2 s reaction choices are not resolved globally by this library.
- V4 `image_to_video` is a framing-control candidate; its route does **not** declare audio switches. For visibly speaking Andre, choose an explicitly reviewed sync/audio route or a separately approved dubbing/sync process—do not certify a silent clip as a speaking take.
- V4 `omni_ref_video` has `prefer_multi_shots=true` fixed. A one-shot prompt is only intent. Any unwanted cut/reveal is a failure. For reaction crops, this route's multishot behavior is an explicit risk, not something we disable with an unsupported flag.
- Any duration, lens or camera geometry here is a creative proposal, not measured EXIF. Prompt prose does not guarantee exact word timing, pixel crop or audio retention.

## P01 — Galileo: main composition / still

**Use:** producer-only detail-image proposal, not an image-generation assignment. **Inputs:** `[IDENTITY]`, `[WARDROBE]`, `[TABLE]`, `[ROOM]`, reviewed composition geometry. **Candidate operation:** reference-image edit/generation; choose the exact available image-model schema rather than converting this to text-only identity generation.

```text
PURPOSE: Establish the principal Andre composition for G-L03/G-L04, not a new interpretation of his appearance.
SUBJECT AND SETTING: Andre sits on screen-left at the selected table in the reviewed Arcetri setting. His body and eyes address Galileo beyond frame-right. Galileo is entirely offscreen; do not add his shoulder, back, hair, reflection or head.
POSE: Quiet attentive posture, mouth at rest, hands low and naturally supported. Preserve all approved wardrobe and table details.
CAMERA: Locked eye-level medium framing matching the selected geometry and eye line. Do not infer a calibrated lens from a style reference.
LIGHT: Match the principal composition's approved window direction and shadow softness. G-ERA supplies contextual setting, not a conflicting light direction or automatic floor-material approval.
RESULT: One realistic still, no new props, no decorative gesture, no captions.
```

**Check:** likeness, cloth pattern, table defects/details, light and crop. Do not treat the result as an approved endpoint or generate it outside the producer conversation.

## P02 — Galileo: listening variant / minimal still edit

**Use:** optional derivative of an accepted P01 composition. **Inputs:** exact approved main still + identity/continuity evidence. **Candidate operation:** image-to-image with minimal edits; no silent source replacement.

```text
PURPOSE: Derive a listening pose while keeping the exact principal composition.
CHANGE ONLY: Relax Andre's mouth into a closed, neutral listening position and let his hands rest naturally below the dramatic focus. Keep his attention just off frame-right.
PRESERVE: Face identity, expression character, hair, wardrobe texture, head scale, seat, table geometry and marks, background arrangement, camera placement, exposure and light direction. Do not change perspective, beautify the face or add a second person. Galileo remains entirely offscreen.
RESULT: A restrained still for continuity comparison, not a different shot design.
```

**Check:** compare exact versions side by side; a visually similar regeneration is not proof that unchanged pixels/materials were preserved.

## P03 — Galileo: Andre listens during G-L03

**Existing relationship:** G-P03 / G-L03. **Inputs:** reviewed listening composition, exact scratch/approved guide. **Candidate:** conservative image-to-video framing; historical voice is offscreen and may be placed in edit under a separately reviewed audio plan.

```text
INTENT: Andre receives a real question rather than preparing a grand speech.
FRAME: Keep the reviewed Andre composition fixed. Galileo stays entirely offscreen to frame-right throughout.
ACTION: Andre listens with subtle breath and a stable eye line; no nodding loop, smile cue or anticipatory triumph. His mouth remains closed. Keep hands low.
SOUND INTENT: The only line is Galileo's offscreen question: “And what survives of the question?” Andre does not mouth or repeat it. Respect the exact supplied performance and its pause; do not invent a reply here.
CAMERA AND LIGHT: Locked camera; unchanged principal light and table detail.
ENDING: Leave a natural listening handle for the next response. No concluding reaction before G-L04.
```

**Check:** line ownership, no accidental lip movement/voice from Andre, continuous room/eye-line match. This is not a request to generate unapproved historical voice identity.

## P04 — Galileo: Andre delivers G-L04

**Existing relationship:** G-P04, baseline's proposed first speaking test. **Inputs:** final approved composition, identity/wardrobe/table, exact G-L04 guide or reviewed speech plan. **Candidate:** a route with declared native sync/audio support; V4 Omni is listed but its mandatory smart multishot and audio-reference limits require producer review. No automatic motion control in this initial baseline.

```text
INTENT: A direct, human answer that becomes quietly firm; Andre is speaking to someone, not lecturing an audience.
FRAME: Andre remains on screen-left in the approved composition. Galileo is entirely outside frame-right; never cut or reverse to show him.
EXACT DIALOGUE, ANDRE ONLY: “Your observations. And one lesson from your trial that people keep relearning: silencing a man does not settle a question.”
PERFORMANCE: Small natural pause after “observations.” One understated low hand movement, only if it fits the reviewed timing. Preserve Andre's individual conversational manner. Do not add, omit, repeat or accelerate words. Finish the thought, close his mouth naturally and leave a short settling handle.
CAMERA AND LIGHT: Fixed framing and eye line; no push-in, orbit, cutaway or light change. Preserve all selected continuity details.
SOUND: Audible synchronized provisional dialogue, explicitly a scratch performance; restrained room tone, no score or extra speaker. It is not the final approved voice.
```

**Check:** exact complete line; natural pace, mouth/teeth/hands, likeness through every frame; sync and actual audio listened to. If the selected route cannot accept the guide as intended, stop and redesign the contract—do not silently swap to a voice-style reference or assume transcript-locked dubbing. Full line beats a preset duration.

## P05 — Galileo: eyes respond after the difficult line

**Existing relationship:** G-REACTION / G-EYE-B. **Inputs:** independently reviewed eyes-only image, timing/alignment to final words of G-L04. **Candidate:** conservative image-to-video, not automatic V4 Omni. **Edit:** approximately 2 s selection is local proposal; route-compliant source length/handles remain a separate decision.

```text
FRAME: Extreme horizontal eye-strip of Galileo, cropped at all times so only the eyes, eyelids and minimal surrounding skin are visible. No nose, mouth, chin, cheek profile or wider head. No zoom-out, camera drift, cut or reflection.
EMOTIONAL CAUSE: The entire line ending “does not settle a question” has just been heard before the selected concluding reaction. Do not resolve the expression before its cause.
ACTION: A restrained shift from exhausted attention to quiet renewed resolve. Very small eye focus adjustment and natural moisture, no tear, glowing eyes, theatrical brow jump or repeated blinking. Do not portray blindness.
LIGHT AND SOUND: Preserve the accepted scene's direction and softness of light. No new speech, music or symbolic sound. Retain a still handle after the change.
```

**Check:** crop and reflections every frame, plus reaction placement in the actual edit. A still crop is not video approval.

## P06 — Optional Galileo hand detail — outside initial baseline

**Status:** future coverage idea only; the active baseline excludes hand/foot/back inserts unless a cut proves the need. Existing hand studies have unresolved table/wardrobe details. **Inputs:** newly reviewed hands/table/material versions; no use of pending studies as if accepted.

```text
FRAME: A fixed below-neck detail of Galileo's hands resting on the exact selected table edge; his entire head and face stay outside the image. Match the reviewed sleeve, wood, ring and edge-defect continuity rather than inventing historical jewelry.
CAUSE: Place this detail only after the selected difficult thought has landed in the reviewed edit.
ACTION: Fingers slowly release a small existing tension against the wood; one readable change, then stillness. No clenched-fist flourish or table strike.
LIGHT AND SOUND: Same motivated light as the principal shot. Only a faint, physically synchronized skin or cloth contact if contact is visible; no amplified dramatic effect.
CAMERA: Fully locked. No reveal, tilt or cut.
```

**Check:** historian/materials, hands anatomy and contact. Do not add this merely because a model can generate it.

## P07 — Caesar: eyes hear the precedent

**Future encounter C; not current Galileo work.** **Inputs:** reviewed C eye crop, matched room-light direction and approved dialogue timing. **Source trigger:** C-L04, “Could the republic survive you? They are still asking it — about other men.” This is invented dialogue, not a quotation attributed to Caesar.

```text
FRAME: Locked extreme horizontal crop containing only Caesar's eyes, eyelids and minimal surrounding skin. The nose, mouth, chin and head profile never enter. No bust, portrait, reflection or inserted wider view.
STATE BEFORE: Focused confidence, not a villainous stare.
CAUSE AND CHANGE: Certainty begins to slip only when the offscreen thought reaches “survive you?”; let him listen through “other men.” The realization is that he became a precedent, not a signal for caricatured rage.
ACTION: A minute interruption in steady eye focus, then held attention. Do not add a tear, violent blink or exaggerated brow performance.
LIGHT: Match the reviewed Roman setting and its actual motivated source; no automatic torch/fire/electric-light cliché.
CAMERA AND AUDIO: No movement or new dialogue. Any offscreen line uses the exact separately reviewed performance.
```

**Check:** the script's nuanced legacy is not reduced to a visual claim of uncontested guilt; full face must remain absent.

## P08 — Khan: restrained foot contact, not a stomp

**Future encounter K; alternate coverage proposal, not a replacement for scripted eye cues.** **Inputs:** reviewed period footwear, hem, ground material and exact location; deliberate tabletop/Andre exceptions do not approve other objects.

```text
FRAME: Fixed close view below the knees of the seated historical interlocutor, focused on one shoe's contact with the reviewed ground surface. No head, face, portrait or reflective reveal.
STATE BEFORE: Controlled confidence. Do not stage a battle, celebration or spectacle.
CAUSE: After Andre's fictional words “cities that are no longer there,” let one foot stop a small prior balancing movement. The weight settles once; then stillness. Do not stomp, scrape angrily or suggest a pre-cue reaction.
MATERIAL AND SOUND: Preserve the reviewed shoe construction, robe/trouser hem, floor/ground and light source. A subtle contact sound only if justified by that actual material; do not assume a wooden floor or modern boot sole.
CAMERA: Locked, no upward tilt or cut. Keep the gesture human and ambiguous, not a cartoon of a conqueror.
```

**Check:** historian must validate material choices; never turn the gesture into a fabricated historical fact or generalize later imperial acts as his personal actions.

## P09 — Napoleon: Andre loses the superior position

**Future encounter N.** **Inputs:** reviewed N composition, Andre identity/clothing, actual N-L03/N-L04 performance timing. **Candidate:** approved audio/sync-capable dialogue workflow.

```text
FRAME: Andre alone in the reviewed table composition, listening toward Napoleon entirely offscreen. Fixed camera and consistent room light; no reverse shot of the historical head.
CAUSE: After Napoleon's offscreen question ends, “And you. Where you come from — do they still argue about the price?”, allow Andre an unforced beat of recognition.
EXACT DIALOGUE, ANDRE: “Every day. We are still not sure who pays it.”
PERFORMANCE: He cannot keep a morally superior distance. Speak plainly, slower than a polished explanation, then let the eyes dip slightly after “who pays it.” No self-satisfied grin, heroic posture or added explanation.
SOUND: Natural synchronized provisional speech and quiet location ambience. No new line, slogan or emotional score.
ENDING: Leave a still handle rather than introducing another historical reaction or camera move.
```

**Check:** N-L03 is the screenplay hinge; preserve the words and ownership. Do not generate both voices from an unreviewed single speaker identity.

## P10 — Oppenheimer: Andre cannot answer the moral question

**Future encounter O.** **Inputs:** exact O-L03/O-L04 source and timing; approved room/Andre composition. Do not insert a bomb-test spectacle or casualty imagery.

```text
FRAME: Andre in the reviewed intimate table composition. Oppenheimer remains entirely offscreen; no historical face in a photograph, reflection or cutaway.
CAUSE: The offscreen question “Can you tell me whether it was right?” has ended. Andre does not answer before the question.
EXACT DIALOGUE, ANDRE: “I can tell you what came next. I can't tell you that.”
PERFORMANCE: Honest limitation rather than a dramatic verdict. Let the first sentence be factual and the second quieter, without whispering into inaudibility. Natural mouth synchronization; no added words or famous quotations.
CAMERA AND LIGHT: Locked, motivated source consistent with the reviewed setting. No flash, nuclear glow or transformation of the room.
SOUND AND ENDING: Audible provisional dialogue, then allow the edit to preserve the screenplay's at least four seconds of silence before the scene cut. If this shot cannot hold it, the separate accepted reaction shot must carry that silence; do not silently shorten the requirement.
```

**Check:** no assertion that the film settles the historical/moral debate. The later famous Oppenheimer quotation is not dialogue at this fictional table.

## P11 — Oppenheimer: nearly motionless hands and silence

**Future encounter O, optional alternate framing.** **Inputs:** reviewed hands/wardrobe/table, exact end of O-L04. **Purpose:** a quiet consequence, not a duplicate decorative insert.

```text
FRAME: Locked detail of Oppenheimer's hands on the selected table, entirely below neck. Nothing reflective reveals his head or face. Preserve reviewed sleeves and material detail; no cigarette or prop unless actually specified and accepted.
CAUSE: Andre has finished “I can't tell you that.”
ACTION: Almost no movement. A tiny release of finger pressure, if any, followed by held stillness. Do not add a fist, tremor loop, tear falling into frame or symbolic object.
SOUND: Keep at least four seconds of near-silence before the scene cut in the final edit, with only credible low room tone. No heartbeat, blast, crescendo or dramatic Foley sting.
LIGHT AND CAMERA: Unchanged motivated light; fixed crop with a natural lead-in and tail. Silence is the dramatic action, not missing content to fill.
```

**Check:** counted silence in the edit, not merely a duration adjective in the prompt. It may share/carry P10's silence; do not accidentally require two unrelated four-second holds.

## P12 — Opening: hand and table before the cut

**Future opening.** **Inputs:** accepted present-day table, Andre hand/wardrobe and opening performance. Face transformation is forbidden.

```text
FRAME: Quiet fixed detail of Andre's hand resting on the approved wooden table edge in the present. No historical person or face is shown. Match his real skin, hand proportions and assigned sleeve.
ACTION: The hand comes to rest once, transferring a little weight into the wood. No tapping loop or supernatural distortion.
SOUND INTENT: Present-day ambience gently recedes. The exact opening narration, if included by the approved audio plan, is: “I wanted to ask history a question. Not what happened — what it felt like to hear what came next.” Do not place all this speech into a short insert or accelerate it.
LIGHT: Preserve the approved present-day source and real wood detail.
ENDING: Hold a stable wood-texture frame for an editorial cut. Do not generate a portal, warp the hand/face, or attempt the whole time-travel transition in this one clip.
```

**Check:** table/contact continuity and speech duration. The original 12-second chapter label is a planning target, not an approval to retime actual audio.

## P13 — Transition: matched table texture, separate shots

**Future edit proposal.** **Inputs:** separately accepted exit and entry table shots for the two locations. Create/choose each plate under its own scope; do not upload both to force an unreviewed morph.

```text
PURPOSE: Supply one side of a hard editorial match cut, not an interpolated time-travel effect.
FRAME: The selected table's wood detail fills the approved crop. Reproduce the exact edge, grain direction and camera geometry needed for this side of the cut. There are no faces or identifiable heads in frame.
ACTION: One minimal settling movement or complete stillness, as selected by the editor; no camera orbit or zoom.
LIGHT: Preserve this location's motivated light. Do not combine the two eras' sources into a new impossible lighting setup.
ENDING: Provide a clean stable handle. No dissolving wood, face/body morph, teleporting object, portal, title or automatic location change inside the generation.
```

**Check:** use the actual selected table version for each side; changes in location/light can be editorial, but table identity and source provenance cannot be guessed.

## P14 — Ending: the empty chair holds the question

**Future ending.** **Inputs:** accepted present-day room/table/chair composition, final narration timing. Empty historical chairs do not need fabricated historical portraits.

```text
FRAME: A quiet locked view of the empty chair across the approved present-day table, keeping the table motif readable. No human face, reflection, supernatural silhouette or new figure appears.
ACTION: Stillness. Let absence carry the meaning; no chair movement or ghost reveal.
SOUND INTENT: If assigned by the audio plan, Andre's exact offscreen narration is: “I went looking for answers. I came back with their question. One day someone will sit across from us, knowing what came next. What will they have to tell us?” Preserve its measured delivery; do not compress it into a preset clip duration.
LIGHT: Consistent present-day room light, no artificial sunset time lapse.
ENDING: Hold the chair, then let the edit select the table detail and fade on wood. Do not fade or dissolve through a face. Credits and the fictionalization notice are added in edit, not generated as unstable on-screen text.
```

**Check:** final chapter timing includes credits; a pretty empty-chair clip is not a finished ending or approved voice performance.

## P15 — Foley: one small contact, no melodrama

**Separate future audio proposal; not a Kling video prompt.** **Inputs:** actual accepted visual gesture, material specification and editor's cue point. **Candidate:** `mirelo_text_to_audio` or another explicitly reviewed SFX tool; its schema/duration/fees must be checked before use.

```text
SOURCE: One quiet fingertip contact and a very short cloth movement against the reviewed table material, synchronized to the supplied visible gesture.
CHARACTER: Intimate natural Foley, low intensity, no exaggerated slap, scrape, sub-bass, heartbeat, musical note or emotional sting.
SPACE: Match the actual room's scale and microphone perspective. Keep the sound dry enough for the editor to place it; do not invent a cathedral echo or outdoor wind.
TIMING: Leave clean pre-roll and decay around the single cue; the editor supplies and verifies the exact contact time and duration. No repeated loop, speech, music or extra impacts.
DELIVERY INTENT: Isolated sound effect for review, not a final approved mixed soundtrack.
```

**Check:** synchronization by listening against the actual picture; silent or invalid inputs do not justify guessing a floor or contact sound.

## P16 — Ambience: specific room, useful silence

**Separate future audio proposal.** **Inputs:** historian/lighting/sound-approved environment and actual shot duration. Use existing recorded/accepted ambience where suitable before proposing another paid tool.

```text
ENVIRONMENT: [REVIEWED_LOCATION_AND_PERIOD], from the approved sound brief, with only sources actually plausible for that room, time and weather.
TEXTURE: Quiet sustained room tone, subtle natural spatial depth, no close speech or recognizable words. Use the approved source list; do not automatically add electrical hum, clocks, horses, crowds, candles crackling or wind.
DYNAMICS: Leave space for the intimate fictional conversation. No music, swell, dramatic event or forced emotional cue. Preserve meaningful silence, especially after the Oppenheimer exchange.
TIMING AND DELIVERY: Duration and loop handles as specified by the editor; no sudden seams or impacts. Provide material for sound review, not a final mix or language validation.
```

**Check:** period/source plausibility and listening at intended playback level. “Cinematic” is not permission to fill every pause.

## Provider adaptation checklist

| Destination | How to adapt these drafts without inventing support |
|---|---|
| Kling reference image generation | Bind reviewed photos to the actual ordered inputs; confirm model ID spelling for T2I versus I2I; no unsupported universal negative field |
| Kling V4 image-to-video | Approved safe first frame; only declared arguments; ≤10 total endpoint/middle images; no timestamp/audio flags assumed |
| Kling V4 Omni | Bind real `图片X` / `视频X` / `音频X` roles or actual `<<<id>>>` Element references; combined ≤15, fixed smart multishot, compatible audio switches; no transcript-lock claim |
| Higgsfield reference image model | Use exact live `job_type` and model schema; do not copy Kling Element syntax or legacy Nano Banana IDs |
| Higgsfield Cinema4 workflow | Use `workflow get cinematic_studio_video_4_0`; references require `mode=omni_reference`; `t2v` rejects references; audio is `generate_audio`, not `enable_audio`; preset/user lighting is blocked by contradictory captured `light_id` rules until reconciled |
| Audio/SFX | Give an audio-specific prompt and measured duration; do not send scene direction as spoken TTS text; fees and voice rights require their own scope |

**Before production:** producer records exact inputs/versions, actual schema and quote, budget ceiling, validity and upload scope. Kling paid work remains producer-only through `scripts/kling_batch.py` plus a matching `kling_job_release`. Higgsfield/other providers require their own authorization; this library grants none. Detail images remain producer-created. After any authorized generation, preserve originals and IDs/cost evidence; independently inspect decode, complete playback/listening, every risky frame/reflection, likeness, dialogue and timing. Andre accepts likeness/voice/artistic result separately. A generated clip never starts the next task or becomes an accepted take by existing.
