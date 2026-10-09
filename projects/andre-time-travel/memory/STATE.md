# Resume State — The Table Between Centuries (andre-time-travel)

Reconciled 2026-10-09 (memory restructure, Phase 0). This is the single resume surface. Keep it under ~80 lines: replace stale lines, do not append narrative. History lives in `history/`; full pre-restructure text: `history/STATE-2026-10-09-pre-restructure.md` (sha256 5e426020…27da). Not live data: re-verify against the canonical files below before acting.

## Read order
1. `AGENTS.md` (rules) → `workspace.json` → this file.
2. `../manifest.json`, `../tasks/board.json`, `../00_brief/approvals.json`, `../00_brief/decisions/D01–D16` (the only decision namespace).
3. `CONTINUE_HERE.md` (pt-BR conversation checkpoint, 13:36) and `../docs/checkpoint-2026-10-09-galileo-retomada.md` (director checkpoint, 13:10) for detail.
4. `.venv/bin/python scripts/manage.py status` for real pending state.

## Film contract
Andre Athar leads five conversations (Caesar, Genghis Khan, Galileo, Napoleon, Oppenheimer), ~240 s, photorealistic, one recurring oak table. Other figures' full faces: zero frames (eyes-only reactions and below-neck allowed; check reflections). English edition first; historical-language edition reuses safe footage.

## Current creative direction (Andre, 2026-10-09 12:35 — supersedes older plans)
Each figure sits at the table seen from BEHIND, out of focus, while Andre speaks (over-the-shoulder, historical head outside frame). Eyes only as a short reaction (1.5–2 s, max 2 per chapter) AFTER a back-view beat. Legacy/repercussion intercuts in intimate tone. Chapters ≈42 s. Invariants: identity = 2024 photos + Element 323525046658711 (D01/D11); grey pinstripe jacket / white striped shirt (D02); table J26-2 with ring + chip (D04); Andre left, looking camera-right (D09); script v2 canonical (D07); Kling voice = guide only, dub later (D14).

## Production status
- Tasks (21): 7 completed (T01–T05, T08, T09); 3 in progress (T10 forecast, T12 keyframes, T13 Galileo); 11 blocked (T06, T07, T11, T14–T21).
- Galileo: `08_edit/picture-lock/galileo-en-preview-v1.mp4` = 42 s guide-voice CANDIDATE, decodes, −16.2 LUFS. Not accepted: no normal-speed playback, reaction precedes its motivating line (F03), pilots show a different table/seat from speech clips (F01). 9 takes registered, `accepted_pending_full_playback`.
- Approvals true: characterReferences, productionElement, screenplay, speechRoute, pilot. False: voiceTests, storyboard, paidBatch, finalPicture. `finalMovieVerified` false.
- New, unreviewed by Andre: ten ChatGPT IN/OUT frames (`../05_storyboard/keyframes/chatgpt-in-out-v1/`), ten posters (`../09_delivery/posters/`). Synthetic candidates; no video tested.

## Money (observation, not live)
- Last Kling balance read: 5,813 at 2026-10-09T12:28:25-03:00. Refresh by CLI before any paid work.
- Galileo ledger 348 (cap 900, stop 810), incl. unresolved 80 (lost ID, not recovered). Whole-film authorization is a ceiling, not batch approval.
- Current plan pointers: `../07_generations/plans/2026-10-09-plano-regeneracao-nova-direcao-v3.md` (+ `-takes-v3.csv`) and `...piloto-galileu-v2.md`; forecast `../docs/budget-and-envelope-resume-v3.md` (2,129–2,249; estimate only). No external-audio spend authorized.
- Ledger: `../credit-ledger.csv` (87 rows); last row G-L02 at 12:10:15. Handoffs after that report no paid jobs.

## Open Andre-only gates and decisions (do not self-approve)
1. D16 (Phase A, cap 23 cr) is recorded as "relayed via Grok Architect Bot". Needs Andre's direct confirmation. Do not spend on it as it stands.
2. D16-r2: `request.json` passes 5 images to `gemini-3-pro-image`, which declares `image_1`/`image_2` only. Fix = new request-r2 (recommended: 2 inputs, cost ≤23), then Andre re-confirms.
3. Proposed, NOT yet recorded: D17 table/seat/camera geometry, D18 blurred nape allowed in phases B/C, D19 eye-reaction rule. Also pending: Genghis armour choice, owner of manifest/board/approvals/ledger (director proposes the producer session).
4. Likeness review of IN/OUT frames and posters; voice by ear; final picture/movie; qualified language review (Edition H).
5. Andre will send an audio with ideas (incl. folder cleanup). No move/delete/rename of folders, Git reset/commit/push, or approval change is authorized.

## Hard cautions
- No automatic retries; one `kling_batch.py --submit-only`, then individual `--resume`. Never resubmit an existing job.
- Other agents share this checkout. 14 uncommitted entries exist (handoffs, IN/OUT frames, checkpoints). Do not clean, restore or reset; record base hashes before editing shared files.
- Andre says he closed Hermes Desktop; unverified. Producer authority for paid submission stays with the parent/producer only.
- Four shared-skill hash warnings from `validate` are known; do not revert them.

## Known stale items (fix via proper owners; Phase 2 lint targets)
- `tasks/board.json` T13 blocker predates the back-view direction, D16 and the Phase A mismatch.
- `manifest.json` `state` string and `manifest.approvals` duplicate `approvals.json` (match today).
- Scene bibles v1 §3 repeat old dialogue (F05); v2/v3 proposals exist for four chapters, Oppenheimer has no v3. `continuity-matrix.csv` has stale-stage lines (F06).
- `session-log.json` mixes timezones and lacks entries for several deliveries (see handoffs).

## Next actions
- Andre: answer items 1–2 above (confirm D16 / r2), then D18.
- Producer: build request-r2 with hash, refresh live balance, record D16 confirmation; own board/manifest/ledger updates.
- Editor: Galileo timeline v2 (0 cr) per checkpoint §5; qc: normal-speed playback of preview.
- Dialogue-sound/continuity: integrate scene-bible v3 and matrix v2 as one revision each with hashes.
- Memory work: Phases 1–4 of the memory/handoff plan (handoff v2, role briefs, `manage.py resume/lint`, backfill) await design review: `../../../docs/superpowers/specs/2026-10-09-memory-handoff-design.md`.
