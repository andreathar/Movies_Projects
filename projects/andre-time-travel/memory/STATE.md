# Resume State — The Table Between Centuries (andre-time-travel)

Reconciled 2026-10-09 (memory restructure, Phase 0). This is the single resume surface. Keep it under ~80 lines: replace stale lines, do not append narrative. History lives in `history/`; full pre-restructure text: `history/STATE-2026-10-09-pre-restructure.md` (sha256 5e426020…27da). Not live data: re-verify against the canonical files below before acting.

Latest verified producer delivery (2026-10-10): research v2 / H01–H06 reviewed; D20 art choices; 25 detail-study slots covered by 26 candidate images. Start from `../agents/handoffs/2026-10-10-producer-detail-studies-v1.json`; gallery: `../05_storyboard/keyframes/detail-studies-v1/index.html`. `RESUME-PRODUCER-2026-10-09.md` holds remaining context; do not repeat completed research.

## Read order
1. `AGENTS.md` (rules) → `workspace.json` → this file.
2. `../manifest.json`, `../tasks/board.json`, `../00_brief/approvals.json`, `../00_brief/decisions/` (D01–D16 and D20; D17–D19 remain proposed topics).
3. `CONTINUE_HERE.md` (pt-BR conversation checkpoint, 13:36) and `../docs/checkpoint-2026-10-09-galileo-retomada.md` (director checkpoint, 13:10) for detail.
4. `.venv/bin/python scripts/manage.py status` for real pending state.

## Film contract
Andre Athar leads five conversations (Caesar, Genghis Khan, Galileo, Napoleon, Oppenheimer), ~240 s, photorealistic, one recurring oak table. Other figures' full faces: zero frames (eyes-only reactions and below-neck allowed; check reflections). English edition first; historical-language edition reuses safe footage.

## Current creative direction (Andre, 2026-10-09 12:35 — supersedes older plans)
Each figure sits at the table seen from BEHIND, out of focus, while Andre speaks (over-the-shoulder, historical head outside frame). Eyes-only reactions remain scene-specific; the 2 s choice belongs to the Galileo v2 candidate, not a universal timing rule. Legacy/repercussion intercuts in intimate tone. Chapters ≈42 s. Invariants: identity = 2024 photos + Element 323525046658711 (D01/D11); grey pinstripe jacket / white striped shirt (D02); table J26-2 with ring + chip (D04); Andre left, looking camera-right (D09); script v2 canonical (D07); Kling voice = guide only, dub later (D14).

## Production status
- Tasks (21): 7 completed (T01–T05, T08, T09); 3 in progress (T10 forecast, T12 keyframes, T13 Galileo); 11 blocked (T06, T07, T11, T14–T21).
- Galileo: `08_edit/picture-lock/galileo-en-preview-v1.mp4` = 42 s guide-voice CANDIDATE, decodes, −16.2 LUFS. Not accepted: no normal-speed playback, reaction precedes its motivating line (F03), pilots show a different table/seat from speech clips (F01). 9 takes registered, `accepted_pending_full_playback`.
- Approvals true: characterReferences, productionElement, screenplay, speechRoute, pilot. False: voiceTests, storyboard, paidBatch, finalPicture. `finalMovieVerified` false.
- New, unreviewed by Andre: ten ChatGPT IN/OUT frames (`../05_storyboard/keyframes/chatgpt-in-out-v1/`), ten posters (`../09_delivery/posters/`). Synthetic candidates; no video tested.

## Money (observation, not live)
- Último saldo observado pela CLI: 31.594 em 2026-10-12T02:01:50-03:00 (05:01:50 UTC), após o teste v3_0. É observação histórica; consultar novamente antes de gasto futuro.
- Galileo ledger 348 (cap 900, stop 810), incl. unresolved 80 (lost ID, not recovered). Whole-film authorization is a ceiling, not batch approval.
- Current plan pointers: `../07_generations/plans/2026-10-09-plano-regeneracao-nova-direcao-v3.md` (+ `-takes-v3.csv`) and `...piloto-galileu-v2.md`; forecast `../docs/budget-and-envelope-resume-v3.md` (2,129–2,249; estimate only). No external-audio spend authorized.
- Ledger: `../credit-ledger.csv` (88 linhas); última AB-MIN-02-v3_0-3s-720p, 27 créditos declarados pelo provedor. APR-kling-ab-min-2026-10-12: teto total 200; um job concluído, nenhum retry; Turbo bloqueado por preço não verificado (173 remanescentes condicionais).

## Open Andre-only gates and decisions (do not self-approve)
1. D16 = approval to spend up to 23 Kling credits on Phase A of the Galileo test: 3 reference images for one over-the-shoulder shot (Andre seated, Galileo's blurred back in front, head out of frame). Recorded as "relayed via Grok Architect Bot". Needs Andre's direct confirmation. Do not spend on it as it stands.
2. D16-r2: `request.json` passes 5 images to `gemini-3-pro-image`, which declares `image_1`/`image_2` only. Fix = new request-r2 (recommended: 2 inputs, cost ≤23), then Andre re-confirms.
3. Proposed, NOT yet recorded: D17 = fixed table layout (table ~120x75 cm, Andre and Galileo on opposite long sides, camera behind-right of Galileo, 50 mm, seated eye height; canonize only after the first test shot is accepted); D18 = allow Galileo's blurred nape (no ear, cheek, beard, profile or reflection) in later phases B/C; D19 = record the eye-reaction rule (1.5-2 s, max 2 per chapter, only after a back-view beat). Producer ownership is defined by AGENTS.md / PARLEY_PROTOCOL. D20 selects no armour for the new Genghis studies only.
4. Likeness review of IN/OUT frames and posters; voice by ear; final picture/movie; qualified language review (Edition H).
5. Andre delegated dark-wardrobe archiving: 18 images logically retired with original paths preserved; 10 bibles reconciled to D02. See `../agents/handoffs/2026-10-09-dark-wardrobe-archive.json`. No deletion, commit/push or paid batch authorized. Claude receipt/review remains unverified.

## Hard cautions
- No automatic retries; one `kling_batch.py --submit-only`, then individual `--resume`. Never resubmit an existing job.
- Other agents share this checkout. Uncommitted entries include handoffs, media and checkpoints; inspect actual Git status rather than reuse an old count. Do not clean, restore or reset; record base hashes before editing shared files.
- Andre says he closed Hermes Desktop; unverified. Producer authority for paid submission stays with the parent/producer only.
- Four shared-skill hash warnings from `validate` are known; do not revert them.

## Known stale items (fix via proper owners; Phase 2 lint targets)
- `tasks/board.json` T13 blocker predates the back-view direction, D16 and the Phase A mismatch.
- `manifest.json` `state` string and `manifest.approvals` duplicate `approvals.json` (match today).
- Scene bibles v1 §3 repeat old dialogue (F05); v2/v3 proposals exist for four chapters, Oppenheimer has no v3. `continuity-matrix.csv` has stale-stage lines (F06).
- `session-log.json` mixes timezones and lacks entries for several deliveries (see handoffs).

## Shared direction
GitHub publication (2026-10-10): Andre authorized this push to private `andreathar/Movies_Projects`; producer integrated remote initialization in `c6b11a8`, and push reported 937 LFS objects uploaded (~1.6 GB). `main` tracks `origin/main`; details and scope: `../../../docs/VERSION_CONTROL.md`. This repository task has no production successor or new creative approval.
Primary instructions now require workflow-map reading and explicit successor ownership; root CLAUDE.md references AGENTS.md. Separate worktrees/open sessions are not automatically synchronized by this edit.
New detail images are created by Codex in the main desktop conversation. Lanes prepare/review only assigned work; image-dependent work waits for explicit delivery with paths and versions. See `../../../docs/PARLEY_PROTOCOL.md`.
All agents read `../docs/2026-10-09-direcao-encontros-fala-dificil.md`: personal perspective, difficult line and motivated reaction; historian checks material culture, lighting owns motivated light (detail later), dialogue-sound owns subtle foley and lip sync. Roles configured, not launched; no new spending approval.

## Next actions
- Teste CLI mínimo (2026-10-12): um take adicional de teste, fora dos 9 takes de produção, `AB-MIN-02-v3_0-3s-720p_1`, sem aceite. Decode íntegro e 73 quadros inspecionados estaticamente; falhas de prompt (piscar/boca/entrada à direita). Playback com escuta e semelhança por Andre pendentes. Produtor retém a revisão e o bloqueio de preço Turbo; ver `../agents/handoffs/2026-10-12-kling-ab-min-v1.json`.
- Auditoria CLI (2026-10-12): CLI oficial global 0.2.1 mantida; captura JSON, preflight e contabilidade revisados, skill em português. Consulta autenticada MCP 1.3.3 não listou V4. Planos antigos A/B/motion continuam bloqueados; o novo escopo mínimo separado executou um v3_0 por 27 créditos, com Turbo bloqueado por preço. Ver `../agents/handoffs/2026-10-12-kling-cli-audit-v2.json`; produtor revisa/ingere, permissões globais continuam fora do escopo.
- Comprehensive execution plan (planning only): `../tasks/execution-plan-v1/README.md`; 96 work packages, 129 traced requirements, Parley/hook design and staged verification. Producer owns execution kickoff; live audit found both film lanes stopped and native approval setup incomplete. No dispatcher activated or production approval changed.
- Requested cleanup audit plan: `../tasks/plans/project-cleanup-plan-v1.md`. Preliminary inventory only; execution/retirement/global uninstall/hook activation not performed. Reuse existing Claude consolidation before new auditing.
- Workflow map: `../tasks/plans/workflow-map-v1.md` covers all 21 board tasks, 68 work packages and the five chapter checklists. Next ready work is independent image continuity review; producer owns dispatch until a reviewer accepts. Map created, no new lane dispatch or automatic hook configured.
- Detail studies: generation and static producer review complete; see gallery and `review.md`. Andre likeness review and video continuity remain pending. Left shoulders are principal D09 candidates; right shoulders are axis alternatives, not current cut selections.
- Old D16/r2 test: reassess need before seeking a new paid scope; it does not block local preparation or the delivered built-in image batch.
- Producer: select the smallest useful image subset for the next shot; reconcile table/wardrobe/axis with the edit before any separately scoped paid video request.
- Editor: Galileo timeline v2 reported delivered; do not rebuild it by default. Full-file normal-speed playback with audio and timeline/bible reconciliation still required before acceptance.
- Dialogue-sound/continuity: integrate scene-bible v3 and matrix v2 as one revision each with hashes.
- Research: Claude v2 is adopted at `../03_bibles/detail-planning/historical-details-v2.md`; producer review and sound/coverage revision at `../08_edit/reviews/detail-planning-v2/`. H01–H06 closed for corrections; G-F2/N-PE/N-F2 resolved as conditional specifications, no audio produced. Arcetri floor and Longwood dimensions remain unproven. New imagery is delivered as candidates, not film acceptance.
- Memory work: Phases 1–4 of the memory/handoff plan (handoff v2, role briefs, `manage.py resume/lint`, backfill) await design review: `../../../docs/superpowers/specs/2026-10-09-memory-handoff-design.md`.
