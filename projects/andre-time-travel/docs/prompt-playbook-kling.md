# Kling prompt playbook — The Table Between Centuries (v1, 2026-10-09)

Evidence-based: every rule below either comes from Kling's official docs (cited) or from a paid test in this workspace (job ID in `07_generations/`). Refresh `kling who_am_i` before each batch; tokens below are live as of today.

Sources: Kling VIDEO 3.0 User Guide (kling.ai/quickstart/klingai-video-3-model-user-guide, Feb 2026) · Kling AI Prompt Guide (kling.ai/blog/kling-ai-prompt-guide, Aug 2026) · `kling-cli` skill `references/filmmaking-workflow.md` · live `who_am_i` snapshot `logs/kling-discovery-2026-10-09/`.

## 1. Stills (Andre keyframes) — `image_to_image`, model `kling-image-o1`

Proven route (D11): `image_1` = real cover photo, `image_2` = table anchor, `image_3` = era plate, `--elements '[{"id":"323525046658711","bindName":"Andre"}]'`, `<<<323525046658711>>>` in prompt. `kling-image-v3_0_omni` with Element only drifted 2/2 → not used.

Prompt order (docs: Subject → Action → Scene → Camera → Light; ours adds composition first because the model drops it otherwise):
1. **Composition first, in thirds**: "the man occupies the LEFT third; the RIGHT two-thirds show only the empty table and out-of-focus room — nobody else, no silhouette, no hand, no shadow of a person, no reflection."  (Lesson: "only person in frame" alone produced an interlocutor head once — R3-oppenheimer-speaking-o1.)
2. Identity: "`<<<id>>>` with EXACTLY the face of 图片1 — same face shape, nose, brow, eye colour, short textured dark-brown hair, light stubble, mid-forties." Use the live marker `图片N`; do not translate it.
3. Wardrobe as photographed (D02): grey pinstripe jacket open, white finely striped shirt, open collar, no tie.
4. Table: "oak table of 图片2: pale wide planks, faint ring stain, chipped near corner" (the stain is the match-cut key, D04).
5. Setting/light from 图片3, "soft and out of focus"; key from camera-left; "no beautification".
6. Expression last, one clause.
- Listening variants: derive from the accepted speaking frame ("Edit 图片1 minimally… change only the expression"). A bare-wall "listening" prompt made o1 paste the reference photo (R3-present-listening-o1-v2).
- Cost observed: 1 credit per 2K o1 image (two unexplained 41-credit deltas logged).

## 2. Eyes-only deltas — `image_to_image`, `gemini-3.1-flash-image`, `aspect_ratio 4:1`

"Edit image 1. Keep EXACTLY the same person… Change ONLY the expression, subtly, as a real face would in one second: …" Identity held 5/5 (R2-J02…J06). Gaze reads near-centre in stills → say "gaze toward camera-left" in the **video** prompt.

## 3. Video — `image_to_video`, model `kling-video-v3_0`

Settings proven in the pilot: `--duration 5|8 --resolution 720p --imageCount 1 --prefer_multi_shots false --elements [...]` and `<<<id>>>` in the prompt. `prefer_multi_shots` defaults **true** — always set false for one editorial shot (skill §5).

Prompt pattern (image supplies look; prompt supplies motion — docs §"Image-to-Video"):
> `<<<id>>>` + ONE action with direction and outcome + "Locked camera, no camera movement, one continuous shot, no cuts. Preserve his face, hair, stubble, jacket, the table and the lighting exactly as in the image. Nobody else enters the frame; no hands near his face."

Envelope proven (PILOT-01/02/03): still listening with blink/breath; a few-degree turn toward camera-right and back; attention→gravity under hard top light. Not tested: profiles, large turns, hand gestures, camera moves — do not request them without a new test.

### Speech (D13) — native audio + bound voice
`--enable_audio true`; Element carries Andre's `.mp3` voice (docs: "voice tone can be bound during subject creation… not recommended to set the tone again in the prompt"). Pattern that worked twice (PILOT-04/05, verified by STT):
> `<<<id>>>` speaks calmly in English to the unseen person across the table, in a plain, warm, unhurried voice. Andre says: "<exact canonical line>". He pauses briefly after "<word>", keeps his eyes on the person to camera-right, and falls silent after the last word. Quiet room tone only, no music.

- Keep speaker name, line and delivery adjacent (docs §"Character Voice Binding").
- Duration = measured scratch seconds + ≥2 s tail; 8 s held G-L04 (7.8 s speech) and O-L04 with a 3.5-s gap.
- Native audio languages per docs: Chinese, English, Japanese, Korean, Spanish + accents. Latin / Mongol / Tuscan / Corsican are **not** supported → Edition H needs the ElevenLabs lipsync fallback or mouth-hidden coverage.
- Costs observed (balance deltas, 720p, Element bound): 5 s no-audio 70, 70, 30; 8 s native audio 72, 92. Docs list 6 cr/s (no audio) / 9 cr/s (audio) / +2 cr/s voice control; the 70 vs 30 split for identical jobs is unexplained — plan at 14 cr/s worst case.

### Interlocutor shots
- Eyes-only: original 4:1 input was rejected without charge. Pad the crop (no stretch) to a 5:2 canvas with black bars, then `kling-video-v3_0_turbo` (single first_image, no Element), locked framing and explicit preservation of bars. G-03/G-05 both returned 121 video frames, 1516×604, 5.041667 s; FFmpeg full decodes passed. G-05 full sequential grids show eyes-only framing held, with two blinks instead of one; accepted pending full-speed playback. These are output observations, not guaranteed behavior.
- Below-neck inserts: hand presses, then stops. Same lock-camera clause.
- Figures' lines: offscreen only. Never prompt a figure's face.

## 4. Review protocol used (and required)
`ffprobe` + full decode; first/mid/last frame triptych; all-frame face-crop grid (11×11 for 5 s) — a sampled strip is triage, the full grid is the gate for face-bearing shots; STT transcript (faster-whisper base.en, in `.venv`) for every speech take, compared to `dialogue-lines.csv`; loudness via `ebur128`. Human full-speed playback + Andre's likeness/voice approval remain separate gates.
