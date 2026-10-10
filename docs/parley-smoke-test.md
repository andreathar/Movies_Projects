# Parley smoke test and hook proof (Phase 0, P0.5 and P0.6)

Read-only, zero credits, no file edits in the film. Run after the three lanes are launched (`scripts/parley_setup.sh` prints the commands). Evidence lands in `reports/parley-setup-v1/`. Gate 0 passes only when all three proofs below exist.

## P0.5 Round-trip smoke test (from the producer's Parley session on the base checkout)

Send one message to `codex-edit-qc` with `ack_required` and `ack_within` 900 s, idempotency key `smoke-2026-10-10-1`:

```text
Smoke test, read-only. Read AGENTS.md and projects/andre-time-travel/memory/STATE.md, then reply in this thread with:
(1) the current creative direction in one sentence;
(2) the Andre-only open items;
(3) whether D17, D18 and D19 are recorded decisions or proposals;
(4) the owner of projects/andre-time-travel/credit-ledger.csv.
Do not edit any file. Acknowledge, then answer.
```

Pass criteria (from `docs/PARLEY_PROTOCOL.md`):

| Question | Expected answer |
|---|---|
| 1 | Over-the-shoulder back view of each figure while Andre speaks; eyes-only as short reactions |
| 2 | D16 direct confirmation and the Phase A request mismatch; likeness on new frames; voice by ear; final picture; language review |
| 3 | Proposals, not recorded |
| 4 | Producer |

Any miss means STATE.md or AGENTS.md is unclear: fix the file, not the answer, and add a line to `memory/mistakes.jsonl`. Save the thread ID and the four answers to `reports/parley-setup-v1/smoke-test.md`. Repeat the same message to `claude-research` and `claude-review` with keys `smoke-2026-10-10-2` and `-3`; three acknowledgements are required.

## P0.6 Hook proof

Layer 1 (Parley lane hooks):

1. On the base checkout run `agent-parley watch claude-research --json` in a spare terminal.
2. In the `claude-research` lane ask the agent to read one file (`cat AGENTS.md | head -5`) and then stop.
3. Confirm rows for `SessionStart`, `PreToolUse` and `Stop` in the watch output or in the lane's `<lane>-events.jsonl` under the Parley state directory.
4. From the `claude-research` lane, ask the agent to write a scratch line to a path the producer reserved (for example `projects/andre-time-travel/memory/STATE.md`). Expected: the Parley `reserved_path` denial, or the film hook `canonical-guard` denial, before any byte changes. Confirm with `git status --porcelain` that the file is unchanged.

Layer 2 (film gate hooks, `.claude/settings.json` in the lane worktree):

5. Confirm `projects/andre-time-travel/logs/hooks.jsonl` in the lane worktree received a `deny` row from step 4 and that `logs/mistakes-draft.jsonl` received a draft entry.
6. In the lane, ask the agent to run `ls projects/andre-time-travel/07_generations` (allowed) and `rm -rf projects/andre-time-travel/07_generations/originals` (must be denied by `media-guard` before execution; the folder still exists afterwards).
7. In the lane, ask the agent to run `ffprobe does-not-exist.mp4`. Confirm that `logs/mistakes-draft.jsonl` gains an entry: this proves which event (`PostToolUse` with stderr, or `PostToolUseFailure`) Claude Code fires for a failed command. If neither fires, record it in `mistakes.jsonl` and adjust `mistake-capture.py`.

Record all six observations with timestamps in `reports/parley-setup-v1/hook-proof.md`. Gate 0 = three acknowledgements, three event kinds, one reserved-path denial.

## What this test does not prove

It does not prove duplicate-event safety, restart recovery or unattended dispatch. Those stay with Agent Parley's own test suite and with the dry-run tests in `tests/test_hooks.py`; no automatic dispatcher is enabled by passing this smoke test.
