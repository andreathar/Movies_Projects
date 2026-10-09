# Session plates QC v1

Written 2026-10-09. Visual QC only, judged from the pictures. Nothing is approved. Nothing was copied into `02_references/andre/approved/`. No Kling job was submitted. The ledger was not edited.

Looked at `docs/photo-session-spec.md`, `docs/assistant-reviews/session-from-stills-plan-v1.md`, the two real identity photos named there, and the six downloaded plates. Submit responses `07_generations/responses/R3-session-02.response.json` through `R3-session-08.response.json` still record the create call as `QUEUING`. The pictures below are the completed downloads. Their sidecars stay `approved: false`.

Identity comparison is `inbox/Photos-Andre-Suit/20240202_015335.jpg` and `20240202_015347.jpg`: hazel eyes, thick dark brows, short textured hair with grey at the temples, trimmed stubble, straight nose.

## Verdicts

1. **Costume FAIL. Identity PASS.** `inbox/Photos-Andre-Suit/20240202_015335.jpg` is Andre, front, mouth closed, eyes on the lens, face clear, in the grey pinstripe and light striped shirt, so it is not a navy/charcoal costume plate.
2. **PASS.** `07_generations/originals/R3-session-02_1.jpg` is Andre in a left three-quarter (left side of the face toward camera), eyes off the lens to camera-right, mouth closed, navy blazer worn open over a charcoal open-collar shirt, with no other face and no broken geometry.
3. **PASS.** `07_generations/originals/R3-session-03_1.jpg` is Andre in a right three-quarter, eyes on the lens, mouth closed, same open navy blazer and charcoal open-collar shirt, alone, with clean features.
4. **PASS.** `07_generations/originals/R3-session-04_1.jpg` is Andre in a true left profile, nose pointing camera-right, far eye hidden, mouth closed, navy blazer open, charcoal shirt open at the collar, ear and jaw intact.
5. **PASS.** `07_generations/originals/R3-session-05_1.jpg` is Andre in a true right profile, nose pointing camera-left, far eye hidden, mouth closed, same open navy/charcoal wardrobe, with a normal ear and no second face.
6. **PASS.** `07_generations/originals/R3-session-06_1.jpg` is Andre, waist-up, mouth closed, eyes to camera-right, navy blazer worn open over a charcoal open-collar shirt, both hands flat on the wood with four fingers and a thumb each and the silver band on his left ring finger.
7. **Costume FAIL. Identity PASS.** `inbox/Photos-Andre-Suit/20240202_015347.jpg` is Andre, front, small closed-mouth smile, eyes on the lens, face clear, still in the grey pinstripe and light striped shirt.
8. **PASS.** `07_generations/originals/R3-session-08_1.jpg` is Andre, front, eyes on the lens, mouth closed in a listening expression, navy blazer worn open, charcoal shirt open at the collar, no other face and no melted features.

## Regeneration

No synthetic plate must be regenerated. Frames 1 and 7 stay the real photographs; do not generate costume replacements for them.

Close calls that are not fails: frame 3 is a mild three-quarter rather than a deep turn, and frame 8 has a very slight lift at the closed mouth that still reads as listening rather than the frame 7 smile. Generated skin is smoother than the phone photos. The faces still match the suit sitting.
