# Model policy per lane — Movies_Projects

Model choice is a config decision per lane, not each CLI's default. Changing a model = editing the file below + a traced probe (`scripts/lane_env.sh` + one-line task) + a note in `docs/TOKEN_SPEND_AUDIT_2026-10-13.md`.

| Lane (Parley participant) | Provider | Model | Where it is pinned | Why |
|---|---|---|---|---|
| `codex` | `codex-film` (`~/.local/bin/codex-film` = `codex --profile film`) | `gpt-6.1-sol`, reasoning **medium** | `~/.codex/film.config.toml` (`model`, `model_reasoning_effort`, `[features] plugins/memories/multi_agent = false`) | Paid; lean profile makes the prefix cacheable (13.4k of 19.6k cached on probe). High reasoning only for tooling tasks: `codex-film -c model_reasoning_effort=high`. |
| `claude` | `claude` | Claude Code default (`"model": "fable"` in `~/.claude/settings.json`) | user settings; per-lane override: `export ANTHROPIC_MODEL=<id>` in the lane shell before `agent-parley run` | Paid; use for historian/continuity/dialogue text where quality matters. |
| `opencode` | `opencode` | **`opencode/big-pickle`** (free, OpenCode-hosted) | repo `opencode.json` (`model`, `small_model`) — project scope, other repos keep their own default | $0 per turn; verified 2026-10-13: follows 3-step read/report tasks correctly (muse-spark-1.1 did not). Use for mechanical/QC/review work first. |
| producer (desktop Codex) | — | unchanged | — | Not a lane; this policy does not touch it. |

Gemini images: `scripts/gemini_generate.py` `--model` (default `gemini-3-pro-image`; `gemini-3.1-flash-image` cheaper). Kling: model chosen per job in the spec; see `docs/PRODUCTION_PLAN.md`.

## Rules
1. A lane never changes its own model; only the producer edits the pin.
2. Free first: if Big Pickle completes the task with evidence, the paid lanes do not repeat it.
3. Every pin change is probed and the per-turn tokens/cost recorded in the audit doc before lanes use it.
4. Respan shows agent models as "None" until a model mapping exists — compare by tokens, not $, for Codex/Claude.
