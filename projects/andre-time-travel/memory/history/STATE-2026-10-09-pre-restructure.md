# Resume State — Andre Time Travel

## Retomada da conversa Codex — 2026-10-09T13:36:16.461392-03:00

O checkpoint mais recente desta conversa está em `CONTINUE_HERE.md` (mesma pasta). Dez frames ChatGPT IN/OUT concluídos. Andre informou que fechou o Hermes Desktop e vai explicar suas ideias no próximo áudio. Reestruturação de pastas permanece em discussão: nenhuma exclusão/movimentação foi autorizada. Não retomar automaticamente a produção paga a partir das próximas seções históricas.

## CHECKPOINT DE RETOMADA (diretor/produtor, 2026-10-09 ~13:20) — ler primeiro

`docs/checkpoint-2026-10-09-galileo-retomada.md` (sha256 4bc74206a4c56bc9c1d5fe9ff0813bba289976d5bc80db9ddca13a083492f483) consolida direção vigente, fontes canônicas, propostas a integrar, decisões pendentes e o próximo passo. Bloqueio da Fase A: `request.json` passa 5 imagens a `gemini-3-pro-image`, que declara só `image_1`/`image_2` (`logs/kling-discovery-checkpoint/`). Nenhum job submetido; D16 aguarda confirmação direta do Andre. Handoff: `agents/handoffs/2026-10-09-director-checkpoint-galileo.json`.

## NEW CREATIVE DIRECTION (Andre, 2026-10-09 12:35) — top priority, supersedes next actions below

Problem Andre identified in delivered material: he sits at a simple table with the personalities, but they only ever appear as facial expressions (eyes). In his words: "they are at the table with him, but never appear at the table with him".
Direction: personalities appear seated at the table, seen from BEHIND and OUT OF FOCUS (body/shoulders/silhouette) while Andre speaks; intercut imagery shows what they became, how people talk about them today and how their actions reverberated, in an intimate tone. Compatible with the zero-full-face rule (AGENTS.md).
Next: (1) historian+continuity update bible/continuity proposals (full-body, back view, defocus, legacy/repercussion content with sources); (2) editor+qc frame-by-frame triage of generated material: keep / reuse / redo; (3) producer (paid delegate) regeneration plan with per-take cost estimate and total, live CLI balance. NO paid jobs; every job needs Andre's explicit approval. T13 Galileo preview stays a candidate pending this re-plan.
Eyes rule (director, 2026-10-09): historical eyes appear only as a short reaction (1.5-2 s, max 2 per chapter) AFTER a back-view beat; chapters stay ~42 s. Proposals: 03_bibles/*-v2-proposta (historian), scene-bibles/*-v3-proposta (dialogue). Plan v2 post-triage: 2,519 cr; Galileo pilot 161 (A 23/B 30/C 108), unapproved.

## Current state — Galileo review cut, 2026-10-09

`08_edit/picture-lock/galileo-en-preview-v1.mp4` is assembled: exactly 42 seconds, 1,008 frames, nine edit events from seven distinct clips covering G-01..G-07. Full decode passed; measured encoded mix −16.2 LUFS / −1.0 dB true peak. See `08_edit/reviews/galileo-en-v1/review.md`, technical QC, timeline and separate guide stems. Source frame-grid reviews remain `accepted_pending_full_playback`; this is NOT final picture lock. The new G-L02 matches canonical text by STT. The older G-L04 guide has doubtful words near “keep relearning”; those words are covered by the table for later ADR. Andre approved likeness but rejected final voice and permitted dubbing later (D14); voice/final-picture/final-movie gates stay false.

Live CLI balance observed at 2026-10-09T12:28:25-03:00: **5,813 credits**. Galileo ledger total **348** includes unresolved original G-01 80, distinct replacement 80, G-L02 108 and eyes 40+40. Do not resubmit an existing job. Crash-safe runner is submit-only plus individual stored-ID resume; tests cover flat and nested query response shapes. Lost-ID submission remains uncertain, not recovered or refunded.

T13 remains in progress pending normal-speed end-to-end playback, natural pacing, fine sync and table/angle review. Current forecast/envelope: `docs/budget-and-envelope-resume-v3.md`; remaining chapter releases are not frozen/accepted by this preview. No new audio-service purchase or final dubbing was made. Other agents share this checkout and have committed concurrent work; do not reset or overwrite it. Review the local movie before releasing all four remaining chapters, then record only concrete correction needs. Detailed earlier observations below are historical and can conflict with the current approved wardrobe/likeness/guide-voice decisions.

## Historical initial state
Reference phase R1 executed 2026-10-09 under APR-R1-references-2026-10-09 (Kling CLI, ceiling 774 credits). 7,741 -> 6,981 credits (760 spent, reconciled from balance deltas; per-job deltas in credit-ledger.csv are approximate). Produced and filed, ALL UNAPPROVED and labelled synthetic: Andre 5-angle turnaround sheet (J01), 10 expression close-ups (J02-J06), 6 seated-at-table frames (J07-J09), 11 eyes-only crops for the 5 figures (J11-J20, cropped locally; originals kept), 5 below-neck costume fragments (J21-J25), a proposed oak-table anchor (J26) and 6 empty era plates (J27-J32). Contact sheets in 02_references/_review/. Rejected: J01 image 2 (layout), J10 (full face visible). Voice 'Athar' (ElevenLabs PVC, id in 04_audio/voice-tests/VT-01.json) generated one English test line (96 ElevenLabs credits); NOT yet judged by ear. Real photo originals copied to inbox/andre-reference-photos (9 files + the user's Kling render, synthetic style ref). No Element created, no video generated, characterReferences approval still false.
Open: Andre must approve likeness and the grooming/wardrobe canon; still missing real profile/neutral/seated photographs; Oppenheimer-stillness eyes crop trims the lower lid; J07 take 2 hair drifts; manage.py/.venv tooling exists and was executed successfully in the atlas pass.

## Film contract
Andre Athar is the lead. Five conversations: Caesar, Genghis Khan, Galileo, Napoleon and Oppenheimer. Approximately four minutes, photorealistic, simple recurring table. Other figures' full faces appear in zero frames; approved eyes and below-neck details only. English and reviewed historical-language editions share safe footage.

## Budget and authority
The prior read-only snapshot was 7,741 Kling credits on 2026-10-08; it is not a fresh balance. Recheck before spending. Budget caps are planning allocations, not exact provider costs or phase approval. All creative/batch approvals remain false. External audio-service purchases are not authorized.

## Next actions
- T01: review/freeze brief and spending boundaries.
- T02: audit the supplied candidate images for provenance, quality and six-view coverage; request missing approved views and the failed clip/generation ID as needed.
- T05: review the sourced fictional English draft.
- Run the identity/speech pilot only after references, Element and exact shot specifications are approved.

## Known risks
Legacy Elements are not approved production assets. Reference contamination is a risk, not proof of the failed scene's cause. Native-language support/pronunciation and a face-preserving external-audio sync route are unverified. Do not silently use French as Napoleon's mother tongue.

## Canonical state
Read `../manifest.json`, `../tasks/board.json`, `../00_brief/approvals.json`, `decisions.json`, `risks.json`, and `../docs/production-plan.md`. The archive plan preserves history but does not override the current workspace.

## Reference inbox observation

At 2026-10-09T07:44:16-03:00, 10 image files were present in the reference inbox and recorded as unreviewed candidates with checksums. They were not moved, overwritten, uploaded, inspected for likeness or approved. Their real/synthetic provenance and consistency remain pending. The original SHA256SUMS.txt file, if present, is untouched.
## Workspace setup verification

Verified at 2026-10-09T07:54:30-03:00: stdlib tests, Ruff lint/format, workspace validation and migrated citation mapping passed. See `../../../reports/setup-verification.json`. Two source snapshots remain uncached. The Movies_Projects desktop project is registered, but the switch returned success while read-back still reported the old active project; the active chat switch is unverified. No paid jobs or media approvals were performed by this setup.

## Preproduction atlas v1 — 2026-10-09

Created `../05_storyboard/preproduction-atlas-v1/index.html`: 16 reference boards, 41 shot cards, 22 performance cards (79 PNG document layouts), three PDFs, an annotated script, timing/coverage files, continuity findings and 15 missing-keyframe briefs. These reuse existing synthetic references; this pass submitted zero new Kling image/video generations. All creative approvals stay pending. Table perspective and historical eye-state continuity remain review issues.

Four additional Athar/eleven_multilingual_v2 opening references completed and were archived in `../04_audio/voice-tests/codex-opening-v1/`. Returned cost 383.9616 ElevenLabs credits; MP3 container durations 8.359, 8.072, 7.001 and 6.922 seconds, all fully decoded. Not judged by ear or approved. The separate earlier VT-01 remains intact. No historical-language approval or lip-sync proof.

Kling account read returned 6,981 credits; R1 aggregate reconciliation is 760 credits against the 774 reference cap (14 remaining). Per-job ledger deltas are approximate. No spending beyond that phase is authorized by this atlas. Drive output folder and readback metadata are recorded in atlas evidence. Workspace tests/validation results are in `../../../reports/preproduction-atlas-v1-verification.json`.

## Visual bible & expanded script assets — 2026-10-09 session

Generated high-resolution photorealistic references via Antigravity image generation pipeline (0 Kling credits consumed):
- Andre left profile (`R2-andre-profile-left.jpg`) and right profile (`R2-andre-profile-right.jpg`) matching 2024 real photos.
- Andre seated at rustic table cinematic still (`R2-andre-table-cinematic.jpg`).
- Master wardrobe reference sheets for Andre modern attire and all 5 historical figures (below neck): Caesar (`R2-wardrobe-caesar-roman.jpg`), Genghis Khan (`R2-wardrobe-genghis-mongol.jpg`), Galileo (`R2-wardrobe-galileo-scholar.jpg`), Napoleon (`R2-wardrobe-napoleon-uniform.jpg`), Oppenheimer (`R2-wardrobe-oppenheimer-tweed.jpg`).
- Establishing scene environment plates: Present-Day empty table (`R2-plate-present-day-table.jpg`) and Rome 44 BCE villa atrium (`R2-plate-rome-villa.jpg`).
- Expanded Andre Character Bible (`03_bibles/character-andre.md`), Table and Continuity Bible (`03_bibles/table-and-continuity.md`), and all 5 Scene Bibles (`03_bibles/scene-bibles/`).
- Historical language translations with IPA phonetics and dubbing timing notes created in `01_script/translations/` (Classical Latin, Middle Mongol, 17th-century Tuscan, Corsican/French).
- Master visual production bible artifact compiled at `master_production_visual_bible.md`.


## Local workflow and continuation rehearsal — 2026-10-09

The user's local-editing and reusable-series request was implemented. Start with workspace `START_HERE.md`, `docs/REPEATABLE_WORKFLOW.md` and `docs/LOCAL_AGENT_HANDOFF.md`. The series contract is `series/andre-time-travel/series.json`. No agents, schedules or paid jobs were started by this validation pass.

Editable atlas directions now live at `../05_storyboard/source/atlas.json`; spoken text remains in canonical CSV/script. A new V2 rebuild contains 79 cards and three PDFs, preserving 22 lines, 41 shots and the 240-second plan. It is workflow proof, not newly generated movie imagery or a creative approval. V1 remains the archived/published atlas referenced in the film manifest. The renderer refuses existing output folders. Build hashes, source snapshot and catalogs are local.

Verified: 36 build input hashes, 169 gallery links, PDF page counts 16/41/22, no text overflow; two cards visually inspected. 382 prior media/delivery files remained byte-identical. Canonical creative flags and task status did not advance. `drafts/workflow-rehearsal` is an unregistered, test-only continuation with empty budget/runtime/chapters/jobs/takes/approvals. The current film remains active.

The visual bible previously linked 26 images from another tool's private working directory. All active links now resolve inside this workspace: 25 to already byte-identical files, one copied as `../02_references/andre/synthetic/R2-andre-seated-conversational.jpg`. Twelve R2 images are registered as unapproved local candidates. Their provider jobs, original model and charges are not independently proven by this pass. Prior notes describing the foundation as locked or the language edition as reviewed are not acceptance evidence. Four translation headers now explicitly say qualified review is pending; translated prose was preserved. Do not approve historical language fidelity from IPA notation alone.

Evidence: workspace `reports/workflow-v1/validation.json`, `tests.txt`, `overwrite-refusal.json`, `localized-bible-assets.json`, `originals-before.json` and `file-index.json`. Remaining gates: human likeness/wardrobe/table choice, factual and qualified language review, voice listening, pilot and speech-route proof, approved batch scope, exact-master playback. Historical snapshots 18/19 remain uncached. Shared skill symlinks and renderer runtime are machine dependencies, not copied vendor assets.


## Local Git versioning — 2026-10-09

At the user's explicit request, this workspace was initialized as a Git repository on `main`. Git LFS is installed/configured only for this repository to track image, audio, video, PDF and archive assets, including the supplied originals. `.gitignore` now excludes runtimes, caches and credentials rather than production media. Necessary empty directories have `.gitkeep` files. No GitHub remote, publication, global Git setting change or service purchase was made.

Read workspace `docs/VERSION_CONTROL.md` before staging changes. The initial version captures the current production baseline; a commit does not change creative or financial approval. Local skill symlinks remain symlinks, and a complete offline backup must preserve `.git/lfs/objects`. Setup checks are in `reports/git-setup-v1/`; the old workflow-v1 inventory remains a historical snapshot.

## Art direction review v1 — 2026-10-09

Read-only review of all materials plus vision inspection of the six contact sheets, the R2 master still, one 2024 photo, the inbox Kling render and one shot card. No approval flag, task state, manifest field or ledger changed; no paid job, Element, upload or TTS spend. New proposal files: `../docs/art-direction-review-v1.md` (inventory, 10 contradictions C1–C10, story/asset/workflow findings, P0–P2 plan, delegation table), `../docs/decision-sheet-andre-v1.md` (8 decisions that unblock T02/T03/T05/T07), `../01_script/proposals/script-en-v2-proposal.md` (line-ID-preserving rewrite: Andre arc, Napoleon as hinge, one "argue", shorter O-L04, new ending; one claim flagged NEEDS SOURCE) and `../../../series/andre-time-travel/FRAMEWORK.md` (reusable episode grammar, gates, asset requirements, ready definition). Canonical script, CSV, bibles, atlases, translations and registries untouched; `series.json` not yet linked to FRAMEWORK.md (producer). Handoff: `../agents/handoffs/2026-10-09-art-director-review.json`. Key blockers remain human: Andre's eight decisions; then historian T05 on v2; then scratch animatic (free local TTS) before any further paid references.

## Decisions executed under blanket authorization — 2026-10-09

Andre delegated budget/tool/subagent decisions ("i aprove all"; APR-blanket-2026-10-09). Director/producer agent recorded D01–D10 in `../00_brief/decisions/` (identity set = 2024 photos; wardrobe navy/charcoal; grooming as photographed; table anchor J26-2 + "the table travels" rule; eye bases per figure, Napoleon recast; screen axis Andre left→right; script v2 integrated; chapter timing deferred). Script v2 is canonical in `../01_script/script-en.md` + CSV (v1 kept in `reports/art-direction-v1/script-en-v1-before.md`); translations marked superseded; production-plan/visual bible marked DERIVED. Bibles headed PROPOSED, brands/readable props removed, matrix axis corrected. 22 full-face originals moved (git mv) to `../07_generations/originals/_quarantine-full-face/`; inbox Kling render labelled composition-forbidden; inbox voice file registered; checklist path fixed; `director` role added. Free edge-tts scratch for 22/22 lines measured (120.8 s speech / 240 s) in `../04_audio/scratch/edge-tts-v2/`; atlas v3 rebuilt (79 cards, 0 overflow, 0 Kling jobs). Budget plan v2 written; live balance 6,981; R2 reference scope (450 cap) authorized but NOT yet submitted. Two read-only subagents dispatched: historian review of v2 (T05) and speech-route/capability matrix (T09 discovery). Still Andre-only: photo session (D08), listening to voice renders (D06), likeness approval of the pilot.

## Historian + speech-route results applied; R2 reference batch executed — 2026-10-09

Historian (T05) verdict APPROVE WITH EDITS applied: [20] OSTI surrender source added to script and registry; snapshots 18/19/20 cached; registry 16 flagged (snapshot ≠ URL); scene bibles synced to v2 lines, unsourced claims softened (Trinity time ≈5:30 a.m., no casualty figure, no 1634 blindness, Zhongxing not Yinchuan, dictator 46–44 BCE). `screenplay` approval = true (APR-screenplay-v2). Speech-route matrix (`01_script/speech-route-matrix-v1.md`): Kling declares NO external-audio lip-sync input; plan = silent Kling clip + ElevenLabs lipsync (Veed → Sync 3), tested in the pilot; Latin and Corsican absent from ElevenLabs lists → Edition H fallback decision pending. R2 batch via new `scripts/kling_batch.py` (producer-only, no retry): 11 jobs / 12 works / **205 credits** (6981→6776), all reviewed at full resolution: Napoleon recast base chosen (R2-J01_2), five expression-B deltas accepted (identity preserved; gaze near-centre → video must drive camera-left), five hand/table inserts accepted (no faces, ring stain present, no readable text). 245 credits of the 450 cap unspent. Next: photo session (Andre) → Element → R3 Andre keyframes → pilot.


## Instagram photo retrieval — 2026-10-09 (partial, waiting for login)

User requested all photos from @andreathar. The public profile was reached in the browser; 24 post/reel links were observed before a sign-in/continue-watching wall. Saved under workspace `inbox/instagram-andreathar/2026-10-09-public/`: 8 photo-post grid previews and one larger version of the first post (1440×754), 9 byte-preserved files representing 8 posts. These are Instagram-served images, not certified camera originals or approved Andre identity references. No reel video, highlight story, tagged image, account credential or DM was collected. No paid service used.

This is NOT a complete profile archive. User login was requested in the open Instagram tab; continue only after authenticated access or a user-supplied official photo export. Permanent source URLs, dates, dimensions and checksums are in the local manifest/CSV; a gallery is in `index.html`. Handoff: `../agents/handoffs/2026-10-09-instagram-import.json`. Canonical film approvals and tasks unchanged.

## Image review sweep + beauty-polish policy — 2026-10-09

Andre asked for every new image to be reviewed and parallel, more beautiful Andre versions. Scope chosen by Andre: "cinematic polish only" (lighting, skin retouch keeping texture, grade, posture; same face and age), variant A, 300-credit ceiling (not yet an executed scope; live balance must be refreshed and a per-batch record written first), free local review each turn, paid variants only after his OK. Tool: `scripts/review_sweep.py` (lists unreviewed/changed images; `--record PATH --verdict ... --notes ...` appends to `08_edit/image-review-log.json`; no approvals). Test: `tests/test_review_sweep.py`. First pass logged 20 Andre images (3 real crops keep; R2 table still = best likeness, `variant-needed`; R1 close-ups/seated + R2 profiles = tone-only; R2 seated-conversational rejected). 103 other images still unreviewed. Polish variants must be new files beside the original, labelled synthetic; originals never edited; identity truth stays the 2024 photos (D01/D03).

R3 polish batch executed (APR-R3-andre-polish-2026-10-09): 3 polish-A images (table still, real crops 015259 and 015214), 20 credits each, live balance 6776 -> 6716, ledger rows added. Files: `07_generations/originals/R3-P0*` and copies in `02_references/andre/synthetic/`. Reviewed side by side: faithful, texture kept. Unapproved synthetic candidates; Andre must judge likeness. Remaining ceiling of this scope: 240.


## Instagram photos — authenticated verification completed, 2026-10-09

Supersedes the earlier waiting-for-login status. At Andre's direction, the existing authenticated Chrome session was used to enumerate all 353 published profile-grid posts: 286 photo posts and 67 video posts. A concurrent import completed `inbox/andre-reference-photos/instagram-andreathar/` with 289 post-photo files (including 3+2 carousel slides), one profile picture and 66 videos. This pass independently matched the full ID/type/carousel inventory, decoded all 290 images, checked unique SHA256 hashes and confirmed both carousel endpoints in the browser. No photos are missing from the observed published grid. This is not an account export; stories, highlights, archived posts, tagged third-party content and DMs are outside this result. Video CMN4kGWlUYu is missing in the other import; video playback was not reviewed.

Primary gallery and machine-readable records: workspace `inbox/instagram-andreathar/2026-10-09-chrome/`. Media remain in the existing import folder, without duplicate copies or edits. The earlier nine-file public batch is preserved and excluded from the main counts. Images are Instagram-served copies, not certified camera originals; no authenticity or likeness approval was granted. No film approval/task state or paid generation was changed by this pass. Handoff: `../agents/handoffs/2026-10-09-instagram-import.json`.


## Kling image archive verified — 2026-10-09

At Andre's request, all image results associated with the film's known generation IDs were reconciled into `07_generations/downloads/2026-10-09-v1/`: 90 images / 73 tasks. One missing original (R1-J01-andre-master-sheet work 2, 2752×1536 PNG) was downloaded into `07_generations/originals/download-2026-10-09-v1/`; 89 were already local. 72 tasks were confirmed by live CLI query; the old R3-galileo-speaking query returned exit 1 / status 400, with its local image preserved and decoded/hash-verified. No repeat query of that failed ID. No paid generation, upload, approval, ledger change, commit or remote publication by this pass.

All 90 catalogued files decode, ID/work pairs are unique, hashes and gallery links verify, and preexisting generation-area media were unchanged. Rejected/quarantined originals stay archived and hidden initially in the gallery. This is a project-ID archive, not proof of all account history; the installed CLI does not expose a history-list operation. New generations after the recorded cutoff require a new snapshot. Workspace validation passed; one existing test-fixture failure concerns T02's JPG being excluded from the test copy, not a missing production file. Evidence: the archive manifest, verification.json and agent handoff.

## Real-photo cinematic portrait suite — 2026-10-09

Andre uploaded 5 fresh portrait photographs (`.user_uploaded/media_1791552687*.jpg`), ingested untouched to `inbox/andre-reference-photos/20261009_user_portrait_01.jpg` through `05.jpg` and `projects/andre-time-travel/02_references/andre/selected/`.
A complete 5-angle cinematographic reference suite was generated matching his authentic facial anatomy, dental geometry, smile lines, stubble, and wardrobe (navy blazer / charcoal linen shirt):
- `R2-andre-cinematic-front-native.jpg`: Master frontal charismatic smile (Antigravity engine).
- `R2-andre-cinematic-threequarter-listening.jpg`: 3/4 right attentive listening (Kling R2-J01, 41 credits).
- `R2-andre-cinematic-profile-contemplative.jpg`: 70° chiaroscuro pensive profile (Kling R2-J02, 41 credits).
- `R2-andre-cinematic-frontal-subtle-smile.jpg`: Frontal subtle knowing smile (Kling R2-J03, 40 credits).
- `R2-andre-cinematic-seated-table-wide-take1.jpg` & `take2.jpg`: 16:9 oak table conversational master shot (Kling R2-J04, 70 credits).
Total Kling reference spend: 192 credits, appended to `credit-ledger.csv`. All images mirrored to brain artifacts and published in `andre_cinematic_portrait_suite.md`. Workspace tests and validation pass with 0 errors.


## Photos ingested, Element built, keyframes, pilot — 2026-10-09

Andre delivered `inbox/Photos-Andre-Suit` (13 real frontals, no clip/profiles; checksummed). Identity set v2 = 4 crops in `02_references/andre/approved/`; D02 wardrobe REVISED to grey pinstripe / white striped shirt as photographed. Kling Element **323525046658711** (cover+3, tag Characters, 180 cr) + Andre's PVC voice bound via element_update; read back OK. Still route (D11): kling-image-o1 + cover + Element holds likeness (omni drifted 2/2). 12 era keyframes accepted in `02_references/keyframes/andre/` (D12; 6 rejects filed; prompt lessons recorded). Pilot (D13): 5 kling-video-v3_0 720p takes in `06_pilot/` — identity baseline, gentle turn, expression, and TWO native-audio speech takes with the bound voice, verified by STT (G-L04, O-L04) and all-frame grids; all agent-accepted, 334 cr. Speech route for Edition E = Kling native audio; ElevenLabs lipsync is fallback; Edition H languages unsupported natively. Docs-derived prompt playbook: `../docs/prompt-playbook-kling.md`. Balance **6161** (spent today: R2 205, Element 180, R3 ≈98, pilot 334). Unexplained charge deltas logged (2×41 on images; 70 vs 30 on identical 5-s videos). Next: Andre plays the 5 pilot clips (likeness + voice by ear) → approve `pilot`/`speechRoute`/`characterReferences` → reforecast → Galileo chapter (T13).


## Five ChatGPT film posters — 2026-10-09

At Andre's request, five portrait 2:3 cinematic posters for **The Table Between Centuries**, starring **Andre Athar**, were generated with the built-in ChatGPT image tool using the approved real identity photograph and current local era keyframes. Files are `09_delivery/posters/chatgpt-v1/01-theatrical-hero.png` through `05-auteur-minimal.png`: five RGB PNGs at native 1024 × 1536. Directions: warm theatrical hero, double exposure, empty-chair intimate suspense, five-era architecture, and bone-white auteur edition. `index.html` compares them; `prompts.json` and `manifest.json` preserve prompts, reference paths/hashes, dimensions and checksums.

Parent visual review checked correct title/billing and no other full faces. All are synthetic marketing candidates; human likeness approval and official poster choice remain pending. Reference photographs and film stills were not edited. Lettering is baked into the raster files; future changes should create a new revision. No Kling/ElevenLabs jobs, canonical approvals/tasks/credit-ledger changes, commit or publication. Model name and built-in billing not exposed. Handoff: `agents/handoffs/2026-10-09-chatgpt-posters-v1.json`.


## Five over-the-shoulder encounter posters — 2026-10-09

Andre requested a more creative poster for each historical personality, with their shoulder softly out of focus and himself seated, gesticulating while explaining. Delivered five new candidates under `09_delivery/posters/chatgpt-v2-encounters/`: Caesar, Genghis Khan, Galileo, Napoleon, Oppenheimer. All are RGB PNG 1024 × 1536, 2:3, generated using the built-in ChatGPT image tool with the real identity cover, corresponding era keyframe, historical costume and table reference. Six image calls: five compositions plus one targeted correction to remove an unrequested human bust from Caesar's background. Rejected original preserved separately and excluded from gallery.

Parent visual review checked speaking gestures, seated pose, soft foreground shoulder, readable title/name/chapter and zero other visible faces. Galileo's generated thematic tagline A QUESTION SURVIVES. is marketing fiction, not a historical quote. Five posters remain synthetic candidates pending Andre's likeness review and selection. V1 preserved. Gallery, exact prompts/references, hashes and handoff are local; no Kling/ElevenLabs jobs, canonical task/approval/ledger changes, commit or publication. Handoff: `agents/handoffs/2026-10-09-chatgpt-posters-v2-encounters.json`.


## Holistic staging audit — 2026-10-09

Andre requested a holistic check of the director and the physical table conversation. Read `../08_edit/reviews/holistic-staging-v1/REPORT.md`, the visual viewer `index.html`, and `DIRECTOR_HANDOFF.md`. Review covered metadata/full decode of 9 unique original videos and the 42-second Galileo preview, with 27 original sample frames and one midpoint per 9 edit events. This was not full normal-speed playback, complete frame-by-frame visual clearance, voice acceptance or creative approval.

Main unresolved findings: no shared shot establishes both seated interlocutors; listening pilots read as a table alongside/behind Andre while speech shows forearms at the front; the resolution eye reaction precedes its motivating G-L04 line. Four scene bibles repeat older dialogue; the continuity matrix and opening of this file include stale-stage statements. Proposed next checkpoint is one 3–5-second over-shoulder conversation shot with historical head completely outside the frame, a fixed table/seat/camera plan and a corrected Galileo edit before repeating the setup for other chapters. This is a recommendation, not a paid batch or storyboard approval.

The Hermes director was active during review. Its local session metadata associates it with a different project directory, although observed outputs use Movies_Projects. No message, session change or interruption was issued. At the closing check, the producer had registered all 9 takes and mapped the 7 Galileo slots; preserve that concurrent progress. Preview/timeline remained unchanged from the audited hashes. This review modified only its own audit artifacts plus this appended memory entry/log/handoff; no task, manifest, approval, ledger, generation, commit or publication.


## ChatGPT IN/OUT frames for five encounters — 2026-10-09

Andre explicitly requested ten built-in ChatGPT keyframes (one IN/OUT pair per personality) and asked to inspect the existing character references. Delivered `../05_storyboard/keyframes/chatgpt-in-out-v1/`: Caesar, Genghis Khan, Galileo, Napoleon and Oppenheimer. Ten RGB PNGs, native 1672 × 941 (approximately 16:9). Each pair is a proposed short ~5-second over-shoulder conversational shot, not the endpoints of a whole 42-second chapter. Shared tabletop in front of Andre; historical head entirely outside the frame. OUT derives from its IN with controlled gesture/expression; face anchored by real approved identity photos. This is not a trained persistent avatar or verified video interpolation.

Eleven built-in image calls: ten deliverables plus one targeted Roman-background correction; the earlier Caesar draft is preserved in `rejected/`. Costume/eye inventories and current bibles examined. Genghis retains the R2 costume's lamellar detail in this version; the proposed no-armour alternative remains unresolved. All imagery remains synthetic candidates pending Andre likeness/art-direction review and a small video test. No canonical task/approval/take/ledger change, Kling/ElevenLabs job, purchase, commit, publication or director message. Built-in billing and model were not exposed. Gallery, requests, reference hashes, manifest and character-review notes are local; read README before integrating. Handoff: `../agents/handoffs/2026-10-09-chatgpt-in-out-v1.json`.
