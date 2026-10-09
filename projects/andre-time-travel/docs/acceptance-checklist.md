# Final Film Acceptance

These are future acceptance criteria, not completed checks.


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
ffprobe -v error -show_format -show_streams -of json "projects/andre-time-travel/09_delivery/film-en.mp4"
ffmpeg -v error -i "projects/andre-time-travel/09_delivery/film-en.mp4" -f null -
ffmpeg -hide_banner -i "projects/andre-time-travel/09_delivery/film-en.mp4" -filter_complex ebur128=peak=true -f null -
```

Repeat against `film-historical.mp4`, then inspect the exact masters visually/audibly. A clean decode is not evidence of good likeness or meaningful eye acting.

