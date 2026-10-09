# Session from stills — plan v1

Written 2026-10-09. Prepared only. Nothing was submitted to Kling, Higgsfield, or ElevenLabs. Nothing was copied into `02_references/andre/approved/`. Approvals, the credit ledger, bibles, and `STATE.md` were not edited.

Instagram is not an identity source for this plan. Every source is a file in `inbox/Photos-Andre-Suit/`.

## Folder

`inbox/Photos-Andre-Suit/` (`/mnt/data/Projects_SSD/Movies_Projects/inbox/Photos-Andre-Suit`).

13 photographs, all looked at. Andre is alone in every frame. Same sitting, 2024-02-02, grey wall, cable, small window:

| File | What it shows |
|---|---|
| `20240202_015201.jpg` | Front, open smile |
| `20240202_015214.jpg` | Front, open smile, arms crossed, silver band on the left ring finger |
| `20240202_015219.jpg` | Front, open smile, arms crossed, ring visible |
| `20240202_015231.jpg` | Front, open smile |
| `20240202_015259.jpg` | Front, open smile |
| `20240202_015304.jpg` | Front, open smile |
| `20240202_015310.jpg` | Front, open smile |
| `20240202_015328.jpg` | Front, closed mouth, serious/neutral, eyes on the lens |
| `20240202_015335.jpg` | Front, closed mouth, serious/neutral, eyes on the lens |
| `20240202_015341.jpg` | Front, closed mouth, neutral, eyes on the lens, slight tilt |
| `20240202_015347.jpg` | Front, small closed-mouth smile, eyes on the lens |
| `20240202_015410.jpg` | Front, open smile, head turned only slightly to his left |
| `20240202_015421.jpg` | Closed-mouth smile, head turned only slightly to his right |

Locked wardrobe for every generated frame: navy unstructured blazer worn open, charcoal open-collar shirt, no glasses, short textured hair, 3–5 day stubble. The photographs themselves are a grey pinstripe jacket and a light fine-stripe shirt. The six jobs keep the face from those photos and change the clothes to the locked navy/charcoal. They do not keep the grey pinstripe.

Frames 1 and 7 stay the real photos. Their clothes do not match the locked wardrobe. They are identity plates only, not costume plates. Do not generate replacements for them.

No file is a three-quarter, a profile, or a waist-up at a table with both hands flat on the wood.

Each inbox JPEG is stored 3216×1158 with EXIF orientation 6, so it displays as a tall portrait (long side / short side = 2.78). Live `image_to_image` help says inputs must be PNG/JPG, below 4K, ≤30MB, aspect no wider than 1:2. Working copies are upright JPEGs with the EXIF rotation already applied, long/short at or under 2:1, in `07_generations/requests/sources/`. Inbox originals were not overwritten. Nothing was written into `02_references/andre/approved/`.

| Working copy | Pixels | Long/short | Cut from |
|---|---|---|---|
| `sources/R3-session-02.jpg` | 1158×1920 | 1.658 | `20240202_015335.jpg`, upright box (0, 800, 1158, 2720) |
| `sources/R3-session-03.jpg` | 1158×1920 | 1.658 | same crop |
| `sources/R3-session-04.jpg` | 1158×1920 | 1.658 | same crop |
| `sources/R3-session-05.jpg` | 1158×1920 | 1.658 | same crop |
| `sources/R3-session-06.jpg` | 1158×2040 | 1.762 | `20240202_015214.jpg`, upright box (0, 680, 1158, 2720); both hands and the ring stay in frame |
| `sources/R3-session-08.jpg` | 1158×1920 | 1.658 | same crop as 02 |

## The eight frames

Covered means a real photo in this folder already shows that frame. Those two are not regenerated.

| # | Spec | Result | File | What is still missing |
|---|---|---|---|---|
| 1 | Front, neutral, eyes to lens | **Covered. Identity plate only, not a costume plate.** | `20240202_015335.jpg` (same coverage: `015328`, `015341`) | Clothes stay grey pinstripe and a light striped shirt. They do not match navy/charcoal. Do not generate. |
| 2 | Left three-quarter, eyes to camera-right | **Generate** | `sources/R3-session-02.jpg` from `015335` | Angle, gaze, and navy/charcoal clothes. Face stays. |
| 3 | Right three-quarter | **Generate** | `sources/R3-session-03.jpg` from `015335` | Angle and navy/charcoal clothes. Face stays. |
| 4 | Left profile | **Generate** | `sources/R3-session-04.jpg` from `015335` | True profile and navy/charcoal clothes. The far side of the head is synthesized. |
| 5 | Right profile | **Generate** | `sources/R3-session-05.jpg` from `015335` | True profile and navy/charcoal clothes. Same limit as frame 4. |
| 6 | Seated, waist-up, both hands flat on the wood, looking camera-right | **Generate** | `sources/R3-session-06.jpg` from `015214` | Hands flat on a wood table, eyes camera-right, mouth closed, navy/charcoal clothes. Face and ring stay. |
| 7 | Front, small closed-mouth smile | **Covered. Identity plate only, not a costume plate.** | `20240202_015347.jpg` | Clothes stay grey pinstripe and a light striped shirt. They do not match navy/charcoal. Do not generate. |
| 8 | Front, listening / thoughtful | **Generate** | `sources/R3-session-08.jpg` from `015335` | Listening expression and navy/charcoal clothes. Face stays. |

**2 of 8 are real photographs. 6 still need a synthetic plate.**

Request files: `07_generations/requests/R3-session-01.json` through `R3-session-08.json`. Frames 1 and 7 have `"command": null`.

## Credit estimate (the six jobs only)

Model `gemini-3-pro-image`, `image_to_image`, `img_resolution 2k`, `image_count 1`. The last three jobs at those settings (ledger `LR3-P01`, `LR3-P02`, `LR3-P03`) each reconciled to **20 credits**. The live schema does not publish a price. This pass did not re-read a live price, so the estimate stays **120**.

| Job | Frame | Estimate |
|---|---|---|
| R3-session-02 | Left three-quarter | 20 |
| R3-session-03 | Right three-quarter | 20 |
| R3-session-04 | Left profile | 20 |
| R3-session-05 | Right profile | 20 |
| R3-session-06 | Seated, hands on the table | 20 |
| R3-session-08 | Front, listening | 20 |
| **Total** | | **120** |

Frames 1 and 7 cost 0. Read `kling account -q` before spending. The ledger balance after the R3 polish block was 6716; that figure is not a fresh read. Run each command once from the workspace root. Do not retry. Outputs are synthetic and stay out of `approved/` until Andre accepts them.

The 10-second speaking clip is not in this folder. No image-to-video job is prepared.

## Producer commands

Run from `/mnt/data/Projects_SSD/Movies_Projects`. The prompt is the final argument. `--poll 0` submits once and returns the id.

### R3-session-02

```bash
kling image_to_image --model gemini-3-pro-image --image projects/andre-time-travel/07_generations/requests/sources/R3-session-02.jpg --img_resolution 2k --aspect_ratio 3:4 --image_count 1 --poll 0 -q --skill-name kling-cli --skill-version 0.2.0 --rationale "Synthetic left three-quarter plate from Andre real face in 015335; navy charcoal wardrobe, angle and gaze only." "Synthetic reference plate, not a photograph. Use image 1 as the only identity source. Keep this exact face, age, eyes, short textured hair, and 3-5 day stubble. Replace the grey pinstripe jacket and the light striped shirt with a deep navy unstructured blazer worn open, soft shoulders, and a charcoal open-collar shirt with the top one or two buttons open. Change the angle: left three-quarter, left side of the face toward the camera, eyes looking camera-right off the lens. Mouth stays closed and neutral. Plain matte wall, soft light from one side, eyes sharp, natural skin texture. No other people, no text, no watermark, no glasses, no watch."
```

### R3-session-03

```bash
kling image_to_image --model gemini-3-pro-image --image projects/andre-time-travel/07_generations/requests/sources/R3-session-03.jpg --img_resolution 2k --aspect_ratio 3:4 --image_count 1 --poll 0 -q --skill-name kling-cli --skill-version 0.2.0 --rationale "Synthetic right three-quarter plate from Andre real face in 015335; navy charcoal wardrobe, angle only." "Synthetic reference plate, not a photograph. Use image 1 as the only identity source. Keep this exact face, age, eyes, short textured hair, and 3-5 day stubble. Replace the grey pinstripe jacket and the light striped shirt with a deep navy unstructured blazer worn open, soft shoulders, and a charcoal open-collar shirt with the top one or two buttons open. Change the angle: right three-quarter. Eyes stay toward the lens. Mouth stays closed and neutral. Plain matte wall, soft light from one side, eyes sharp, natural skin texture. No other people, no text, no watermark, no glasses, no watch."
```

### R3-session-04

```bash
kling image_to_image --model gemini-3-pro-image --image projects/andre-time-travel/07_generations/requests/sources/R3-session-04.jpg --img_resolution 2k --aspect_ratio 3:4 --image_count 1 --poll 0 -q --skill-name kling-cli --skill-version 0.2.0 --rationale "Synthetic left profile plate from Andre real face in 015335; navy charcoal wardrobe, angle only." "Synthetic reference plate, not a photograph. Use image 1 as the only identity source. Keep this exact face, age, short textured hair, and 3-5 day stubble. Replace the grey pinstripe jacket and the light striped shirt with a deep navy unstructured blazer worn open, soft shoulders, and a charcoal open-collar shirt with the top one or two buttons open. Change the angle to a true left profile: nose points camera-right, the far eye is not visible, mouth stays closed and neutral. The unseen side of the head follows this same face. Plain matte wall, soft light from one side, natural skin texture. No other people, no text, no watermark, no glasses, no watch."
```

### R3-session-05

```bash
kling image_to_image --model gemini-3-pro-image --image projects/andre-time-travel/07_generations/requests/sources/R3-session-05.jpg --img_resolution 2k --aspect_ratio 3:4 --image_count 1 --poll 0 -q --skill-name kling-cli --skill-version 0.2.0 --rationale "Synthetic right profile plate from Andre real face in 015335; navy charcoal wardrobe, angle only." "Synthetic reference plate, not a photograph. Use image 1 as the only identity source. Keep this exact face, age, short textured hair, and 3-5 day stubble. Replace the grey pinstripe jacket and the light striped shirt with a deep navy unstructured blazer worn open, soft shoulders, and a charcoal open-collar shirt with the top one or two buttons open. Change the angle to a true right profile: nose points camera-left, the far eye is not visible, mouth stays closed and neutral. The unseen side of the head follows this same face. Plain matte wall, soft light from one side, natural skin texture. No other people, no text, no watermark, no glasses, no watch."
```

### R3-session-06

```bash
kling image_to_image --model gemini-3-pro-image --image projects/andre-time-travel/07_generations/requests/sources/R3-session-06.jpg --img_resolution 2k --aspect_ratio 3:2 --image_count 1 --poll 0 -q --skill-name kling-cli --skill-version 0.2.0 --rationale "Synthetic seated table plate from Andre real face in 015214; navy charcoal wardrobe, hands, gaze, and closed mouth." "Synthetic reference plate, not a photograph. Use image 1 as the only identity source. Keep this exact face, age, eyes, short textured hair, 3-5 day stubble, and the silver band on the left ring finger. Replace the grey pinstripe jacket and the light striped shirt with a deep navy unstructured blazer worn open, soft shoulders, and a charcoal open-collar shirt with the top one or two buttons open. Close the mouth to neutral. Uncross the arms. Seat him waist-up at a plain wooden table with both hands flat on the wood, fingers relaxed, looking camera-right. Plain matte wall, soft light from one side, eyes sharp, natural skin texture. No other people, no text, no watermark, no glasses, no watch."
```

### R3-session-08

```bash
kling image_to_image --model gemini-3-pro-image --image projects/andre-time-travel/07_generations/requests/sources/R3-session-08.jpg --img_resolution 2k --aspect_ratio 3:4 --image_count 1 --poll 0 -q --skill-name kling-cli --skill-version 0.2.0 --rationale "Synthetic listening front plate from Andre real face in 015335; navy charcoal wardrobe, expression only." "Synthetic reference plate, not a photograph. Use image 1 as the only identity source. Keep this exact face, age, eyes, short textured hair, and 3-5 day stubble. Replace the grey pinstripe jacket and the light striped shirt with a deep navy unstructured blazer worn open, soft shoulders, and a charcoal open-collar shirt with the top one or two buttons open. Keep the front angle and the eyes on the lens. Change only the expression to listening and thoughtful: attentive, calm, a slight softness in the brow, mouth closed, not a smile and not a blank stare. Plain matte wall, soft light from one side, eyes sharp, natural skin texture. No other people, no text, no watermark, no glasses, no watch."
```
