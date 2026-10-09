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
1. D16 = approval to spend up to 23 Kling credits on Phase A of the Galileo test: 3 reference images for one over-the-shoulder shot (Andre seated, Galileo's blurred back in front, head out of frame). Recorded as "relayed via Grok Architect Bot". Needs Andre's direct confirmation. Do not spend on it as it stands.
2. D16-r2: `request.json` passes 5 images to `gemini-3-pro-image`, which declares `image_1`/`image_2` only. Fix = new request-r2 (recommended: 2 inputs, cost ≤23), then Andre re-confirms.
3. Proposed, NOT yet recorded: D17 = fixed table layout (table ~120x75 cm, Andre and Galileo on opposite long sides, camera behind-right of Galileo, 50 mm, seated eye height; canonize only after the first test shot is accepted); D18 = allow Galileo's blurred nape (no ear, cheek, beard, profile or reflection) in later phases B/C; D19 = record the eye-reaction rule (1.5-2 s, max 2 per chapter, only after a back-view beat). Also pending: Genghis armour choice, owner of manifest/board/approvals/ledger (director proposes the producer session).
4. Likeness review of IN/OUT frames and posters; voice by ear; final picture/movie; qualified language review (Edition H).
5. Andre delegated dark-wardrobe archiving: 18 images logically retired with original paths preserved; 10 bibles reconciled to D02. See `../agents/handoffs/2026-10-09-dark-wardrobe-archive.json`. No deletion, commit/push or paid batch authorized. Claude receipt/review remains unverified.

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

## Shared direction
All agents read `../docs/2026-10-09-direcao-encontros-fala-dificil.md`: personal perspective, difficult line and motivated reaction; historian checks material culture, lighting owns motivated light (detail later), dialogue-sound owns subtle foley and lip sync. Roles configured, not launched; no new spending approval.

## Next actions
- Codex storyboard: shared checklist `../tasks/scene-detail-assets-v1.md` — five characters, feet/floor, back/hair, left/right shoulder alternatives and fingers/table. Planning only; no generation yet.
- Andre: answer items 1–2 above (confirm D16 / r2), then D18.
- Producer: build request-r2 with hash, refresh live balance, record D16 confirmation; own board/manifest/ledger updates.
- Editor: Galileo timeline v2 (0 cr) per checkpoint §5; qc: normal-speed playback of preview.
- Dialogue-sound/continuity: integrate scene-bible v3 and matrix v2 as one revision each with hashes.
- Parley: service is up; lanes claude/codex are defined but not launched. Proposal and smoke test: `../../../docs/PARLEY_PROTOCOL.md` (nothing configured; Andre launches lanes and decides the merge gate).
- Memory work: Phases 1–4 of the memory/handoff plan (handoff v2, role briefs, `manage.py resume/lint`, backfill) await design review: `../../../docs/superpowers/specs/2026-10-09-memory-handoff-design.md`.
