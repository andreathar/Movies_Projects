# Agent Parley protocol for Movies_Projects — PROPOSED

Status: proposal for Andre's review (2026-10-09). Nothing here is configured. Parley coordinates agents; it grants no creative, spending or approval authority. AGENTS.md and `docs/LOCAL_AGENT_HANDOFF.md` still win on any conflict.

## What Parley gives and what it does not
- Gives: lanes (`claude`, `codex`), mail between lanes, a decision log, advisory file reservations, status/reports. Service: `agent-parley up`; check: `agent-parley doctor`.
- Does not apply here: forge issues, claims on issue numbers and PRs (no Git remote). Use mail, reservations and reports only.
- Each lane works in its own Git worktree and branch (`parley/<project>/lane-N`). Ignored files (`.venv`, credentials, caches) are not in a lane worktree. Work reaches `main` only through an explicit merge that Andre has asked for.

## Lane roles
Lanes are tools, not film roles. The film role (producer, director, historian, ...) for a task is named in the first message of the thread and in the handoff `agentRole`. Role limits in `agents/*.md` and AGENTS.md apply unchanged: only the producer role submits approved paid Kling jobs, and only from the base checkout after a live balance refresh and a written scope. Reviewer roles never spend.

## Ownership (reserve before editing; release when the handoff is written)
| Resource | Owner role | Others |
|---|---|---|
| `manifest.json`, `tasks/board.json`, `00_brief/approvals.json`, `credit-ledger.csv`, `asset-registry.csv`, `00_brief/decisions/` | producer (director for decision records) | propose through a handoff; never edit |
| `01_script/`, `03_bibles/`, `05_storyboard/source/`, `08_edit/` new revisions | the role named in the task | new versioned files only |
| `memory/STATE.md`, `memory/session-log.json` | whoever closes a task, after reading the file fresh | record base hash in the handoff |
| Named resource `kling:submit` | producer only | one paid submission at a time |

## Close-out message (replaces re-reading the whole thread)
One mail per finished task, with an idempotency key: handoff path, claims with evidence paths, `andreOnlyGates`, next action and role. Decisions Andre made go in the log with `decision: true`; proposals never do.

## Proposed integration gate (Andre runs it; a lane cannot)
```bash
agent-parley verify set ".venv/bin/python scripts/manage.py validate && .venv/bin/python -m unittest discover -s tests"
```
Known baseline: validate reports ok with four shared-skill hash warnings; 29 tests pass. A passing gate is not creative acceptance. Do not run `participant merge` or `participant pr` until Andre asks.

## Smoke test (read-only, no spending, no file edits)
Prerequisites: `agent-parley up`; Claude and Codex each launched with `agent-parley run NAME --repo /mnt/data/Projects_SSD/Movies_Projects`; lane approvals resumed.
Message to `codex`: read AGENTS.md and `projects/andre-time-travel/memory/STATE.md`, then reply in one thread with (1) the current creative direction in one sentence, (2) the Andre-only open items, (3) whether D17–D19 are recorded decisions or proposals, (4) the owner of `credit-ledger.csv`.
Pass: (1) back-view over-the-shoulder with eyes only as short reaction; (2) includes D16 direct confirmation and the Phase A request mismatch; (3) proposals, not recorded; (4) producer. Any miss means STATE.md or AGENTS.md is unclear, so fix the file, not the answer.
