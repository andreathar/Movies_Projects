# Photo-session substitute v1

Written 2026-10-09. Andre said he cannot shoot now (`docs/photo-session-spec.md`: 8 stills + a 10 s clip, navy/charcoal, D02/D03). This inventories what already exists. No photo was copied into `approved/`. No image was generated. The first pass left `inbox/andre-reference-photos/instagram-andreathar/` alone. The Instagram pass below is a later look at the stills that were already on disk.

## Verdict

**0 of 8 frames are covered.** Element creation must wait. The 10-second clip cannot be faked. The Instagram pass does not raise that count.

A Kling Element built from the three 2024 photographs would learn a grey pinstripe blazer, an open toothy smile, and a wall with a cable and a window. It would not learn a profile, a three-quarter gaze to camera-right, both hands flat on the table, a small closed-mouth smile, or a front listening face. The synthetic turnaround already draws those angles, and D01 bars synthetic portraits from identity inputs. R3 (planned 400) and the pilot (planned 1,100) stay behind the Element.

## What was inspected

Real photographs, all in `inbox/andre-reference-photos/` (originals; crops only where noted). `02_references/andre/raw/` and `approved/` contain no images. `selected/` has three crops of the 2024 set. Synthetic files live under `02_references/andre/synthetic/`. Stills were looked at directly.

| File | What it actually is |
|---|---|
| `20240202_015214.jpg` (crop `selected/crop34_20240202_015214.jpg`) | Feb 2024. Front, open smile, grey textured blazer, white fine-stripe shirt, short textured hair, trimmed stubble. Arms crossed; a light metallic band on the left ring finger. Grey wall, white cable, small window. |
| `20240202_015259.jpg` (crop `…015259.jpg`) | Same session, same clothes, same smile. Hands not in frame. Same cable and window. |
| `20240202_015304.jpg` (crop `…015304.jpg`) | Same session again. Near-duplicate of 015259. |
| `20230817_203913.jpg` | Aug 2023. Bright blue three-piece suit, another man in frame, office mural. Not a reference plate. |
| `IMG_20230220_183202.jpg` | Feb 2023. Seated at a podcast table with two other people, headphones, grey t-shirt. |
| `IMG_20220321_103632.jpg` | Mar 2022. Wide-angle selfie, striped shirt, office and skyline behind him. |
| `IMG_20210818_105943_optimized.jpg` | Aug 2021. Standing, blue pinstripe suit, black shirt, fuller swept hair, open smile. |
| `IMG_20210722_151056_optimized.jpg` | Jul 2021. Headphones, zip polo, notebook, open smile. Not the table setup. |
| `IMG_20210428_141013_optimized.jpg` | Apr 2021. Seated at a pale table, one forearm on the wood, green screen, boom mic, wide lens. |
| `kling_20261008_IMAGE.png` | Synthetic style render, already marked composition-forbidden. Another figure at the left edge. Not a photograph. |

D01 already sets identity truth to the three 2024 photographs and treats 2021–2023 as grooming history. That split holds after this look: the older frames are different hair, different clothes, other people, or a wide lens. None is the navy/charcoal session.

Synthetic closest angles (not coverage): `R1-J01-andre-master-sheet_1.png` is a five-panel turnaround (true left profile, left three-quarter, front neutral, right three-quarter, true right profile) in navy and charcoal on a plain grey ground. `R1-J02` neutral front, `R1-J03` small closed-mouth smile, `R1-J04` listening three-quarter, `R1-J06` thoughtful three-quarter in warm bokeh, `R1-J08` seated three-quarter with one hand on the table and one on the chair, `R2-andre-profile-left.jpg` and `R2-andre-profile-right.jpg` (strong three-quarter, far eye still visible, not a true profile), `R2-andre-table-cinematic.jpg` (both hands on wood, mouth slightly open, concrete room). `R2-andre-seated-conversational.jpg` is disqualified by other faces in frame (combined priorities). D03 already downgrades the sleek R1 hair. These files stay tone references.

## The eight frames

“Covered” means a real photograph that can stand in for that spec frame. Wardrobe on every real file is wrong (grey/pinstripe or older clothes, never the navy unstructured blazer and charcoal open collar). Even ignoring clothes, the angles and expressions are missing.

| # | Spec frame | Result | Closest file, and why it fails |
|---|---|---|---|
| 1 | Front, neutral, eyes to lens | **UNCOVERED** | Real 2024 set is an open smile. Closest drawing: `R1-J02-andre-closeup-neutral_1.png` (synthetic). |
| 2 | Left three-quarter, eyes to camera-right | **UNCOVERED** | No real three-quarter. Closest drawing: `R1-J04-andre-closeup-listening_1.png` (synthetic, listening, not a neutral gaze plate). |
| 3 | Right three-quarter | **UNCOVERED** | No real three-quarter. Closest drawing: the right three-quarter panel inside `R1-J01-andre-master-sheet_1.png` (synthetic). |
| 4 | Left profile | **UNCOVERED** | No real profile. Closest drawing: left panel of the same J01 sheet. The R2 “profile-left” still shows the far eye. |
| 5 | Right profile | **UNCOVERED** | No real profile. Closest drawing: right panel of the J01 sheet. |
| 6 | Seated, waist-up, both hands flat on the wood, looking camera-right | **UNCOVERED** | Closest real seating is `IMG_20210428` (2021, one arm, green screen) or `IMG_20230220` (other people). Closest drawing: `R2-andre-table-cinematic.jpg` (synthetic, mouth open, concrete room). |
| 7 | Front, small closed-mouth smile | **UNCOVERED** | 2024 smiles show teeth. Closest drawing: `R1-J03-andre-closeup-smile_1.png` (synthetic). |
| 8 | Front, listening / thoughtful | **UNCOVERED** | No real listening face. No synthetic front listening face either. `R1-J04` and `R1-J06` are three-quarter. |

## The 10-second clip

The clip does not exist, and it cannot be faked. The spec is a horizontal 10 s take, neutral for 2 s, then IN-L01 spoken, then a 2 s hold, no head turn, in this wardrobe. There is no such recording under `inbox/andre-reference-photos/` outside the Instagram folder, and none under `02_references/andre/`. A still, a turnaround sheet, or a stitched voice file is not that clip. Lip-sync for the pilot has nothing real to match.

## Facts Andre stated (checked, not edited)

`credit-ledger.csv` already contains the spend he named. 32 R1 rows sum to **760**. 11 R2 rows (`LR2-J01` through `LR2-J06` and `LR2-J10` through `LR2-J14`) sum to **205**. Total **965**. Last `balance_after` is **6776** (6981 → 6776 on the R2 block). Each row already has a generation id and a balance delta. Nothing was appended. No job id was invented.

`00_brief/approvals.json` already has `screenplay: true` (`APR-screenplay-v2-2026-10-09`). Every other creative flag is false (`characterReferences`, `productionElement`, `voiceTests`, `speechRoute`, `pilot`, `storyboard`, `paidBatch`, `finalPicture`). The file was not modified. No concurrent edit was in the way; both files were stable when re-read.

`scripts/manage.py status` (read-only): 21 tasks, 2 completed, 2 in progress, 17 blocked, 0 ready, balance snapshot not live. That status was not changed.

## Instagram pass

Andre asked us to use the public `@andreathar` stills because he cannot photograph himself. This pass looked at images only. The 40 mp4 files were not opened. `CATALOG.md` dates were used. Another agent may still be adding older posts; this is whatever was already on disk: 162 post stills plus `profile-picture.jpg`, post dates in the catalog running 2016-10-21 through 2024-12-05 for photos (the only 2025 item is a video).

Current likeness means 2022 onward. That is 21 photo posts. Each one was looked at. 2021 contact sheets were scanned for a profile, a closed mouth, or the navy/charcoal look, and the side-view tiles were opened. Nothing was copied into `approved/`.

**Usable candidates: 0 of 8.** A frame counts only when a still actually shows that angle and expression, with the eyes visible, the face large enough to crop, and a likeness from 2022 or later. Instagram does not have that for any of the eight.

**Navy blazer and charcoal shirt: not in this set.** No still shows the D02 look (navy unstructured blazer, charcoal open collar, top buttons open). The nearest tailored clothes are grey, and the shirt under them is black or light, not charcoal:

- `C3_oyvcsZRj_1.jpg` (2024-03-02) — grey pinstripe blazer, black buttoned shirt, another man in a navy suit.
- `C20LWcKvUud_1.jpg` (2024-02-01) — grey suit, light shirt, yellow badge, standing beside his mother.
- `C0ywdFYsfTI_1.jpg` (2023-12-13) — grey blazer, black shirt, event selfie.

| # | Spec frame | Result | Closest Instagram file |
|---|---|---|---|
| 1 | Front, neutral, eyes to lens | **UNCOVERED** | No 2022+ neutral front. Every recent front face is an open smile (`C0ywdFYsfTI_1.jpg`, `C3_oyvcsZRj_1.jpg`, `CbXiyYxOuWf_1.jpg`) or the eyes are hidden (`DDLzY7WsuJH_1.jpg`, sunglasses). `profile-picture.jpg` is eyes-to-lens and closed-mouth, but black-and-white, split by a hard shadow, with a fuller beard. Not a color plate of the current face. |
| 2 | Left three-quarter, eyes to camera-right | **UNCOVERED** | `CpYFfbeucFa_1.jpg` (2023-03-04) is the closest 2022+ off-axis face: head turned, gaze off camera, short hair and stubble. It does not qualify. The mouth is open mid-word, headphones cover the ears, and a title card sits on the frame. The same shot is also `CqVd2F1L-cd_1.jpg` inside a poster. Gaze reads toward frame-left, which is the other side from camera-right. |
| 3 | Right three-quarter | **UNCOVERED** | `Cq1RyU_MHX8_1.jpg` (2023-04-09) is the closest: a near-profile on a stage, nose toward frame-left, both eyes still readable. The mouth is open, a microphone is in front of the face, and the backdrop is covered in logos. |
| 4 | Left profile | **UNCOVERED** | No true profile in 2022+. `CoFMV4_O79d_1.jpg` is a side view with a VR headset over the face. `Cq1RyU_MHX8_1.jpg` never reaches a profile. 2021 side views that were opened (`CO-eK57sFdW_1.jpg`, `COZZi_GsKBz_1.jpg`) are still three-quarter selfies, not profiles. |
| 5 | Right profile | **UNCOVERED** | Same gap. No right profile on the account in the files that are here. |
| 6 | Seated, waist-up, both hands flat, looking camera-right | **UNCOVERED** | `C3-jVaEM6zB_1.jpg` (2024-03-01) puts him at a meeting table, but as a wide selfie: one hand near the edge, open smile, two other men, text across the top. `CPvymwCs4AF_1.jpg` (2021-06-05) is the only hands-on-a-table picture found, and it fails: he is small in a wide green-screen shot, one fist in the air, white shirt, readable wall text. |
| 7 | Front, small closed-mouth smile | **UNCOVERED** | 2022+ smiles show teeth (`C0ywdFYsfTI_1.jpg` is the latest clean one, Dec 2023, grey blazer). The best closed mouth on the account is `COZZi_GsKBz_1.jpg` (2021-05-03): three-quarter, not front, wide-lens, laundry room, and a year before the preferred likeness. |
| 8 | Front, listening / thoughtful | **UNCOVERED** | No front listening face. `CpYFfbeucFa_1.jpg` is the closest mood, and it is a three-quarter talking into a mic. |

The 10-second clip still cannot be faked. Skipping the mp4s was deliberate: none of them was checked, and a public clip is not the specified take (neutral, then IN-L01, then a hold, navy/charcoal, no head turn).

**Element must wait.** A reduced still set from these files would be open smiles, wrong clothes, and often a second person or a graphic in the crop. It would not give a profile, a camera-right three-quarter, both hands flat on the wood, a small closed-mouth smile, or a front listening face. That is not enough to start the Element, the R3 keyframes, or the pilot.
