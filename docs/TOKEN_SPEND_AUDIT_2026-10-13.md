# Token-spend audit — 2026-10-13

Measured with Respan tracing (see `RESPAN_OBSERVABILITY.md`). Method: one-line prompt ("Reply with exactly: …") per agent in this repo, so **everything measured is fixed per-turn overhead** — paid on every turn of every lane, before any real work. `docs/TOKEN_EFFICIENCY.md` §8 said "tokens reais só quando o sistema fornecer medição" — the system now provides it.

## 1. Baseline: what a zero-work turn costs

| Agent | Input tokens / turn | Of which measured |
|---|---|---|
| Codex CLI 0.162 (gpt-6.1-sol) | **32,617** | base prompt 5.5k · developer block 14.8k (Skills index **10.3k**, Memory+profile+tips **4.2k**) · multi-agent 0.7k · AGENTS chain 3.5k · tools/MCP ≈8k |
| OpenCode 1.18 (muse-spark-1.1) | **32,258** | MCP tool schemas **12.8k** (measured by disabling) · built-in tools 5.7k · AGENTS chain ≈3.3k · system prompt + skills ≈10k |
| Claude Code 2.1 (fable) | 2 prompt (+cache) | hook omits cache-read tokens → not comparable; CLAUDE.md→@AGENTS.md chain alone is 4.9k |

At ~$0.04 per OpenCode turn and ~32k/turn on Codex, a 50-turn lane burns ~1.6M input tokens of pure overhead.

## 2. Measured reductions (same prompt, same repo)

| Change | Codex | OpenCode |
|---|---|---|
| Disable 6 MCP servers (5× Cloudflare + mcp-brasil) | — (not honored via `-c`) | 32,258 → **19,476 (−40%)** |
| `features.plugins=false` + `features.memories=false` | 32,626 → **21,284 (−35%)** | — |

## 3. Where the waste is

1. **ElevenLabs app plugin in Codex** — 42 `architect-*` skills ≈ 4.3k tok/turn. Never relevant to this repo.
2. **Codex memories** — 4.2k tok/turn of notes from *other* projects (Gerenciador_AI, Caiafa, Android, Unity). Cross-contamination risk as well as cost.
3. **Cloudflare MCP ×5 + mcp-brasil in OpenCode** — 12.8k tok/turn. This repo deploys nothing to Cloudflare.
4. **`~/.agents/skills` (36 Cloudflare/Workers skills)** — ≈4.4k tok/turn in Codex's index; also indexed by Claude Code.
5. **Instruction chain** — `CLAUDE.md` @imports `AGENTS.md` (2.8k) and `AGENTS.md` orders reads of `START_HERE.md` (1.3k), `README.md` (0.7k), `REPEATABLE_WORKFLOW.md`, `LOCAL_AGENT_HANDOFF.md`, `PARLEY_PROTOCOL.md`, `skills/andre-time-travel/SKILL.md`: ≈ 9–12k before the first task action. Context7 preamble is injected twice (global `~/.codex/AGENTS.md` + project `AGENTS.md`).
6. **Codex multi-agent prompt** (0.7k) when `features.multi_agent=true` — lanes never spawn sub-agents.

## 4. Strategies, ranked by tokens saved ÷ effort

| # | Strategy | Est. saving / turn | Effort |
|---|---|---|---|
| S1 | **Lean lane profile for Codex**: launch lanes with `-c features.plugins=false -c features.memories=false -c features.multi_agent=false` (or a dedicated `CODEX_HOME` for film lanes with a minimal `config.toml` — Parley already sets `CODEX_HOME`). | **−11k (−35%)** measured | low |
| S2 | **Per-project MCP for OpenCode**: in `~/.config/opencode/opencode.json` set the 6 MCP servers `"enabled": false`; re-enable per project via `.opencode/opencode.json` in the repos that need Cloudflare. | **−12.8k (−40%)** measured | low |
| S3 | **Disable the ElevenLabs plugin globally in Codex** (`[plugins."app-6a8d784b60cc81919aeafbfaeda5fbcf@openai-curated-remote"] enabled = false`) — enable only in ElevenLabs sessions. | −4.3k | trivial |
| S4 | **Move `~/.agents/skills` Cloudflare bundle out of the global roots** (e.g. into the Site_Athar / Cloudflare repos' `.agents/skills`). | −4.4k Codex, similar Claude | low |
| S5 | **Flatten the instruction chain**: make `AGENTS.md` self-sufficient for lanes (≤1.5k tok: role, forbidden actions, verify command, handoff template path) and move narrative/history to `docs/`. Drop the mandatory `START_HERE.md`+`README.md` reads; keep deep docs on-demand. Remove the duplicated Context7 block from the project `AGENTS.md` (global one already has it). | −5k to −8k first turn, −2k every turn | medium |
| S6 | **Right-size the model per lane** (Respan now shows cost per lane): Codex lanes run `gpt-6.1-sol` with `model_reasoning_effort = "high"` + `service_tier = "priority"` for QC/text tasks. Set `-c model_reasoning_effort=medium` for review lanes, keep high only for tooling. | −reasoning tokens, −priority surcharge | trivial |
| S7 | **Prompt caching**: Codex showed `cached_input_tokens: 0`. Stable prefix (system + AGENTS) only caches if it is byte-identical turn to turn — the memories block (dated, changing) defeats this. S1 also fixes it. | up to −50% cost on the remaining prefix | free with S1 |
| S8 | Tag spans per scene (`RESPAN_WORKFLOW_NAME=<scene-id>` in the lane shell, next to `MOVIES_LANE_NAME`) so Respan rolls cost up per scene and the policy's §8 comparison becomes a query, not a guess. | enables measurement | trivial |

Combined S1–S4 take a zero-work turn from ~32k to roughly **12–14k** on both Codex and OpenCode without touching the film workflow.

## 5. What NOT to cut
- Film gate hooks (`.claude/hooks/`), `manage.py validate`, handoff template — cheap, and they are the safety net.
- `kling-cli` skill and `andre-time-travel` SKILL — the only skills this repo actually uses.

## Mistake / Solution record
| Mistake | Solution |
|---|---|
| Assumed the project instruction files were the main overhead | Measure first: harness plugins/MCP/memories were 70% of the fixed cost; AGENTS chain ~10%. |
| `codex exec -c 'plugins."…".enabled=false'` changed nothing | Plugin skills come from the plugin cache; use `features.plugins=false` for lanes or disable the plugin in `config.toml`. |
| `codex exec -c mcp_servers.X.enabled=false` changed nothing | Those MCP servers weren't contributing in exec mode anyway; don't optimize what isn't measured. |
| OpenCode `/experimental/tool` doesn't list MCP tools | Measure MCP cost by A/B run with `OPENCODE_CONFIG_CONTENT='{"mcp":{…"enabled":false}}'`. |
| Policy (`TOKEN_EFFICIENCY.md` §8) said "no telemetry, don't spend to measure" | Four $0.04 turns bought a measured 35–40% reduction; update §8 to point at Respan. |

## 6. Applied 2026-10-13 14:27 (verified with the same one-line probe)

| Change | File | Before → After |
|---|---|---|
| S3 ElevenLabs plugin off (global Codex) | `~/.codex/config.toml` → `[plugins."app-6a8d784b60cc81919aeafbfaeda5fbcf@openai-curated-remote"] enabled = false` (backup `config.toml.bak-lean`) | Codex default: 32,626 → **27,152** |
| S1 Codex lean profile | `~/.codex/film.config.toml` (`features.plugins/memories/multi_agent = false`, `model_reasoning_effort = "medium"`). Use **`codex --profile film …`** in every Movies lane shell. | Codex lane: 32,626 → **21,278 (−35%)** |
| S2 OpenCode MCP off for this repo | `opencode.json` at repo root (6 servers `enabled: false`). Other repos untouched. | OpenCode: 32,258 → **19,473 (−40%)** |

Still pending (needs your decision, touches other repos): S4 move `~/.agents/skills` Cloudflare bundle; S5 flatten AGENTS chain; S6 reasoning effort is in the film profile already; S8 `RESPAN_WORKFLOW_NAME` per scene in lane shells.
Recommended edits outside this doc: `docs/PARLEY_PROTOCOL.md` §"Export in each lane shell" → add `codex --profile film`; `docs/TOKEN_EFFICIENCY.md` §8 → measurement source is now Respan.

### Mistake / Solution (apply phase)
| Mistake | Solution |
|---|---|
| Put `[profiles.film]` inside `~/.codex/config.toml` | Codex 0.162 refuses legacy inline profiles: profile lives in `~/.codex/<name>.config.toml`, selected with `--profile <name>`. |
| Put the OpenCode override in `.opencode/opencode.json` — not loaded, only −5k | Project config is `opencode.json` at the repo root. Verify with `grep 'loading path' ~/.local/share/opencode/log/opencode.log`. |
| — (finding) OpenCode indexes `~/.claude/skills` incl. `.trash/` and `~/.agents/skills` (duplicate-name warnings) | Empty `~/.claude/skills/.trash`; S4 applies to OpenCode too. |

## 7. S4 applied 2026-10-13 14:33 — Cloudflare removed everywhere (Andre: "remove all cloudflare we are not using")
Archived (reversible) to `~/_archive/cloudflare-2026-10-13/`: 10 skills from `~/.agents/skills` (agents-sdk, cloudflare, cloudflare-email-service, cloudflare-one, cloudflare-one-migrations, durable-objects, sandbox-sdk, turnstile-spin, workers-best-practices, wrangler) + their symlinks from `~/.claude/skills` and `~/.hermes/skills` (also one pre-existing dangling `herdr` link); 5 Cloudflare MCP servers deleted from `~/.config/opencode/opencode.json` (backup in archive); `cloudflare@claude-plugins-official` set to `false` in `~/.claude/settings.json` (backup in archive). Repo `opencode.json` now only disables `mcp-brasil`. `manage.py validate` exit 0.

| Probe | Start of day | Now |
|---|---|---|
| Codex film lane (`--profile film`) | 32,626 | **20,307 (−38%)** |
| Codex default | 32,626 | **26,177 (−20%)** |
| OpenCode (this repo) | 32,258 | **18,223 (−44%)** |

S4 alone was worth ~1k/turn (the estimate of 4.4k counted all 36 skills; only 10 were Cloudflare). The remaining fixed cost is the agents' own prompts/tools (Codex 5.5k base + ~8k tools; OpenCode 5.7k tools + system prompt), the AGENTS chain (S5), and the 26 remaining shared skills.

## 8. S5 + Parley wiring applied 2026-10-13 14:40
- `AGENTS.md` rewritten lean: 11,272 B (≈2.8k tok) → 7,375 B (≈1.8k tok). Every rule kept, narrative compressed, procedure stays in the linked docs. Full previous text: `docs/archive/AGENTS-full-2026-10-13.md`. `manage.py validate` 0, unit tests OK.
- Codex lane executable: `~/.local/bin/codex-film` (= `codex --profile film "$@"`), registered as Parley provider **`codex-film`** (adapter codex, home env `CODEX_HOME`). New Codex lanes: `agent-parley participant add <name> --provider codex-film`. The existing `codex` participant still uses the stock provider (re-creating it retires its worktree — producer's call).
- Agent Parley MCP server: nothing to insert anywhere. `agent-parley run <participant>` injects it per lane (Claude `--mcp-config`, Codex `-c mcp_servers.agent_parley.url=…`, OpenCode lane-private config overlay). Verified the `coordinate` skill is still indexed under the film profile (skills root `~/.agents/skills/coordinate` → Parley plugin).
- ~~Remaining duplicate: `~/.codex/AGENTS.md` Context7 block twice~~ — **correction 15:05**: the two `<!-- context7 -->` lines are the open/close markers of one block; nothing duplicated, nothing to cut.

| Probe (one-line reply) | Start of day | End of day |
|---|---|---|
| Codex film lane — input tokens | 32,617 (0 cached) | **19,574, of which 13,440 cached → ~6.1k billed full-price** |
| Codex default | 32,626 | 26,177 |
| OpenCode (this repo) | 32,258 | **17,280 (−46%)** |

The cache hit is the S7 effect: with memories/plugins off the prefix is byte-stable across turns, so OpenAI serves it from cache (cached input is billed at a fraction). Before today Codex cached 0 tokens on every turn.

### Mistake / Solution (S5 phase)
| Mistake | Solution |
|---|---|
| Nearly reported "6,139 tokens" from Codex's `tokens used` line as the new per-turn cost | That figure excludes cached input. Read `total_token_usage` in the rollout (`input_tokens` vs `cached_input_tokens`) or the Respan span; report both. |
| Assumed the duplicated Context7 block was in the project AGENTS.md | It is in `~/.codex/AGENTS.md` (global), appearing twice; Codex concatenates global + project instructions. |

## 9. Closing pass 2026-10-13 15:05
- `~/.claude/skills/.trash` (17 entries, 4.8 MB, indexed by OpenCode with duplicate-name warnings) → `~/_archive/cloudflare-2026-10-13/claude-skills-trash`.
- The 26 remaining `~/.agents/skills` are generic agent tooling (coordinate, browse, port-guard, secret-vault-injector, create-*…), not Cloudflare; left in place — pruning them is a cross-project decision.
- `scripts/gemini_generate.py` + `respan_smoke.py`: the Gemini call is wrapped in `respan.workflow(name=RESPAN_WORKFLOW_NAME)` with `customer_identifier="movies-projects"` and `RESPAN_METADATA` → verified locally via a captured span: `traceloop.workflow.name=S00-probe`, same metadata keys as the agent hooks. Image cost now rolls into the scene total.
- Respan read API (`traces list` / `logs list`) still returns 405 since ~13:45; ingest is 200. Platform-side; dashboard UI unaffected as far as we can tell.

| Mistake | Solution |
|---|---|
| Reported the Context7 block as duplicated in `~/.codex/AGENTS.md` | The markers delimit one block. Read the file before counting markers. |
| Used `Respan(app_name=…)` expecting it to set the workflow name | `app_name` → `service.name`. Workflow grouping needs `@respan.workflow(name=…)` around the call. |
| Tried to verify the SDK tag via `respan traces list` (405) | Attach an in-process OTel `SpanExporter` and read the span attributes locally. |
