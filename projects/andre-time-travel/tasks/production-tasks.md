# Production Tasks

Canonical machine-readable board: `board.json`. This checklist is the detailed execution specification; task statuses live only in the board. No production task has been marked complete by workspace setup.


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

