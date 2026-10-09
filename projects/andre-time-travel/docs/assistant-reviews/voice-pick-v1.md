# Voice pick v1 — recommendation only

Written 2026-10-09. Andre asked for one name among the six D6 files. This does **not** set `voiceTests` to true. `00_brief/decisions/D06-voice.json` stays provisional. No ElevenLabs call, no new render.

## Pick

**`IN-L01-athar-v2-ref-3.mp3`**

Path: `projects/andre-time-travel/04_audio/voice-tests/codex-opening-v1/IN-L01-athar-v2-ref-3.mp3`

Duration (ffprobe): **7.001 s** (container 7.000816 s, 44.1 kHz mono, 128 kb/s).

Why this one: it says the opening line as one continuous thought, in a steady low voice, with only short breaths. That is the intimate, present-day read at the table. The other four line reads plant a long hold that turns the same sentence into a small performance.

## How it was judged

Local only. `ffprobe` and `ffmpeg` (`volumedetect`, `astats`, `silencedetect` at −40 dB / 0.25 s). Pitch from 16 kHz autocorrelation on voiced frames (70–280 Hz). Transcript from the cached faster-whisper **base** model (CPU, int8), not a paid API. This is acoustic evidence plus a transcript. It is not a human ear for vowel color, so the Brazilian label on the Athar clone is not cleared or condemned here. Accent stays Andre’s call.

All five line reads transcribed as the IN-L01 sentence, language `en`, probability ≥ 0.993. Levels are dry studio TTS: no room, no other voices.

| File | Duration | Mean / peak | Median pitch | Pace | Long gaps (>0.28 s) |
|---|---|---|---|---|---|
| VT-01 | 7.184 s | −28.5 / −4.6 dB | 82.7 Hz | 168 wpm | 0.36 s after “question”; **0.98 s** after “happened” |
| ref-1 | 8.359 s | −24.0 / −1.3 dB | 85.2 Hz | 146 wpm | 0.42 s; **0.82 s** after “happened”; **0.74 s** after “hear” |
| ref-2 | 8.072 s | −24.9 / −2.5 dB | 88.7 Hz | 150 wpm | 0.46 s; **0.86 s** after “happened”; 0.54 s after “hear” |
| **ref-3** | **7.001 s** | **−24.2 / −3.3 dB** | **89.0 Hz** | **173 wpm** | 0.44 s after “question”; 0.56 s after “happened” |
| ref-4 | 6.922 s | −26.7 / −2.7 dB | 84.8 Hz | 176 wpm | 0.30 s; **1.04 s** after “happened”; 0.32 s after “hear” |
| inbox PVC | 23.798 s | −20.3 / −2.1 dB | 158.5 Hz | 136 wpm | several; see label below |

ref-3’s pitch tracker spiked a few frames (p90 203 Hz). The body of the voice is the 89 Hz median, interquartile range about 16 Hz, same family as the other four line reads.

## Why the other five lost

1. **`VT-01_athar_multilingual-v2_en_IN-L01.mp3`** (7.184 s) — same line, lowest and quietest of the five, but a 0.98 s hole after “happened” stages the second sentence. That is the theatrical beat this pick avoids.
2. **`IN-L01-athar-v2-ref-1.mp3`** (8.359 s) — slowest (146 wpm) and three pauses, including 0.74 s before “what came next.” It performs the line.
3. **`IN-L01-athar-v2-ref-2.mp3`** (8.072 s) — same performed shape as ref-1, with a wider pitch swing (p90 about 122 Hz). More melodic than a man talking across a table.
4. **`IN-L01-athar-v2-ref-4.mp3`** (6.922 s) — brisk on paper, then a 1.04 s hold after “happened,” the longest reveal in the set.
5. **`inbox/andre-voice/ElevenLabs_2026-10-09T10_42_57_Athar_pvc_sp100_s50_sb75_v4.mp3`** (23.798 s) — **not the opening line.** Label: English comic anecdote, present tense, about standing still while a man in a suit walks a pig on a leash, the pig wearing a little hat. Transcript: “Okay, so you have to hear this. I am literally still dying. So we’re just standing there right and this man walks past full suit, very serious, walking a pig on a leash. With a little hat on, the pig, not the man. That pig had more confidence than anyone I’ve ever met.” Delivery is casual, and the pitch sits near 158 Hz with a wide range (interquartile about 83 Hz), about an octave above the five line reads. Useful as a sample of a looser Athar PVC take. It is the wrong text and the wrong weight for the table.

`voiceTests` remains false until Andre accepts a file by ear.
