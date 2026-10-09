# Combined priorities v1 — AI movie assistant

Merged from three read-only reviews in this folder:
`production-watchlist-v1.md`, `continuity-bible-draft-v1.md`, `lighting-and-look-v1.md`.
Written 2026-10-09 ~09:30 (UTC-3), while the art director was editing the scene bibles, script, board and manifest (uncommitted). Re-check each item against the live files before acting.

Andre confirmed the blanket approval is genuine and covers paid batches (see `blanket-approval-confirmation.md`). Live balance refresh and ledger entries are still required.

## P0 — fix before any paid generation

1. **Face rule in references.**
   - The Caesar, Genghis, Galileo and Napoleon R2 below-neck sheets show chin, mouth or beard. The Oppenheimer spec and its R2 sheet put a head silhouette in frame. Crop or replace them, and stop citing them as costume anchors (continuity CB-01, CB-02).
   - Rewrite the Oppenheimer bible line "conceals the upper head in deep shadow" so no head enters the frame.
2. **Andre identity inputs.** The D02 wardrobe sheet contains another man's chin and lips. `R2-andre-seated-conversational.jpg` shows foreground and café faces. The 2021–2023 photos include other people. Keep all of these out of identity slots (CB-03, CB-04).
3. **One time of day per chapter.** Bible, atlas, plates and eye prompts disagree for Caesar, Galileo, Oppenheimer and the present day. Recommended: follow the light already baked into the chosen D05 eye crops.
   - **Caesar:** evening oil lamp.
   - **Galileo:** winter dusk window plus one candle.
   - **Oppenheimer:** pre-dawn, bare bulb plus cobalt window; this makes the date 16 July.
   - **Present day:** morning, window screen-left.
   - The R2 morning plates for Rome and the present day are retired.
4. **Map the v2 lines to their slots.** The scene-bible dialogue tables, atlas and shot list still quote v1. Eye-reaction cues no longer land in their slots:
   - Oppenheimer's answer runs 11.9 s against a 10 s slot.
   - Genghis's second cue comes before his first reaction shot.
   - Galileo's cue falls after his reaction shot.

   Build the v2 line-to-slot map before any keyframe (CB-09, CB-10).
5. **Floor plan and table.** Define the seating geometry. Decide which edge of Andre's side carries the chip and ring stain. Reserve a slot for the table close-up match cut that D04 requires. Remove the plates that use other tables (CB-05, CB-16, CB-24).
6. **Reflections.** Add "no reflections of the seated figure" checks for windows behind Andre. Make the metal and liquid props matte or angle them away: brass inkwell, candlestick, pocket watch, ashtray, kumis bowl, oil lamp (CB-18, CB-19).
7. **Budget hygiene.** Refresh the Kling balance through the CLI. Log the ~480 untracked ElevenLabs credits. Recompute the reference allowance (14 credits left).

## P1 — before keyframes and the pilot

8. **Andre's light block.** Use one key light for Andre in every era: soft, neutral, about 5000 K, from camera-left, catchlight at 10–11 o'clock. Era light only edges him. Apply it to all 10 era keyframe briefs (lighting §8).
9. **Eye prompts J11–J20.** Remove "flickering". Use a frontal soft band of light with the era glow as a rim, fixed catchlights and no moving flame shadow.
10. **Napoleon's light.** "Light over his left shoulder" breaks the D09 screen axis. Re-set the Saint Helena light to shutter daylight plus a dying candle.
11. **No readable text:** Code Civil spine, Galileo's manuscripts, Oppenheimer's notebook and cigarette pack. Use a wax tablet for Caesar, not a book.
12. **Props and costume.** Lock the prop variants: goose vs brass quill, compass vs astrolabe, pocket watch vs wristwatch, Oppenheimer's hat, rings. Genghis's robe needs one colour, blue or brown. His seat must reach a 75 cm table.
13. **Andre's ring.** D02 says silver; the real hand photo shows a dark ring. Andre should confirm.
14. **Script.** Napoleon's "do they still argue about the price?" refers to a price nobody mentions earlier in his chapter. Add a setup line or change the line. The historian check (T05) must cover v2; `historian-review-v2.md` now exists, so check it.
15. **Sound bridges.** Settle the ambience per transition: rain vs desert wind, crickets vs quiet air. Decide the state of the present-day vase so the opening and ending match.

## P2 — housekeeping

16. **Asset registry.** 43 R1 rows have 6 of 8 fields, and the 10 inbox images are registered twice. Teach validate to catch this.
17. **Sources.** Cache the Hiroshima and Nagasaki sources (18, 19) that anchor O-L02. Mark the validated sources. Source v2's claim marked "needs source".
18. **Records.** Record the skill edits: the project `SKILL.md`, plus the global film-character-continuity and film-dialogue-localization skills.
19. **Historical-language edition.** All four translations are superseded by v2. Decide the language for the opening and ending, and Napoleon's language (Corsican or French).
20. **Scratch TTS.** `edge-tts` is a cloud service, not local. Document it, or switch to a local engine.

## Only Andre can do

- Confirm wardrobe, grooming and ring, and schedule the photo session (D08) for neutral and speaking expressions.
- Listen to the 6 voice files, and identify the unlabelled inbox recording.
- Provide the failed clip, or declare it unrecoverable (T02).
