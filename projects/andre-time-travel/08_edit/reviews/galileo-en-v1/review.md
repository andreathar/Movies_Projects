# Galileo English picture review — v1

**Status: assembled review candidate, not picture lock or final delivery.**

Artifact: `08_edit/picture-lock/galileo-en-preview-v1.mp4`  
SHA-256: `b008ed2bc030945f2248bc75a063b96ccf766a8347d27f87a54c15763d14b10d`.

## Executed checks
- FFprobe: exactly 42.000000 seconds, 1,008 decoded frames, 1920×1080 at 24 fps; H.264 picture, AAC audio and optional English mov_text subtitles.
- Full FFmpeg decode: exit 0, empty error output.
- Final encoded audio measured with ebur128: −16.2 LUFS integrated, 7.2 LU loudness range, −1.0 dB true peak.
- All seven primary G slots map to real footage: nine edit events / seven distinct source clips. Timeline and original media are retained; original source frames are not time-warped.
- Newly generated speech: all 289 video frames covered by readable face grids; STT matches G-L02. Both eye clips and the replacement insert also have qualified source reviews.
- Opening, immediately before/after each of eight hard cuts, and final frame inspected in the rendered-file contact sheet. No unexpected full-black frame, historical full face, nose tip/mouth/chin reveal or obviously stretched picture observed in these inspected joins. Eyes clips intentionally remain narrowly letterboxed.
- Final assembled audio transcribed locally; all four line meanings present. G-L04 still has a doubtful phrase around “keep relearning”; machine transcripts hear extra words. This is an ear-review/ADR item, not certified pronunciation. The affected section starts after source 4 seconds and is covered by the table insert, avoiding visible mouth mismatch in a future replacement.

## Editorial/continuity limitations
- The sources change framing and lighting between wider speech and closer listening angles. The traveling table is carried by the repeatable stain/chip/grain insert; matched physical geometry of all independently generated medium shots is **not** proven. Check this in playback rather than declaring perfect spatial continuity.
- Nine-event timing redistributes the storyboard's provisional slot handles while retaining its total 42 seconds. The G-L02 ending L-cuts over eyes; G-L03 overlaps the eye reaction; G-L04 continues over paper/hand.
- Quiet ambience is provisional: a short speech-free tail from G-L02 repeated with fades, not a separately recorded production room tone. No music.
- English subtitles contain the canonical script, not a transcript certification of the doubtful guide phrase.
- Export is a 1080p review container upscaled from native ~720p sources, not native 1080p generation. Default provider watermarks remain.

## Unpassed gates
Normal-speed end-to-end playback, perceived likeness on this new chapter, natural pacing, fine lip-sync inspection, final Andre dubbing, clean-master output selection and historical-language review are **not complete**. `voiceTests`, `finalPicture` and `finalMovieVerified` remain false. T13 must remain in progress; do not release all remaining chapters as if the chapter recipe were fully accepted.

Technical evidence: `08_edit/reviews/galileo-en-v1/technical-qc.json`; assembly transcript: `guide-transcript.json`; joins sheet: `joins-opening-ending.png`; complete FFmpeg command/log record: `08_edit/normalized/galileo-en-v1/build-log.json`. Separate guide line stems and mix: `04_audio/stems/dialogue/galileo-guide-v1/`.

## Accounting observation
Live CLI `account` at **2026-10-09T12:28:25-03:00** returned **5,813 available credits**. Galileo ledger total is 348, including the earlier uncertain 80-credit job whose ID remains unknown; this preview neither recovers that job nor establishes a refund. The distinct replacement cost 80 and G-L02 cost 108 by immediate balance delta. No extra generation/audio-service spend was required for this assembly.
