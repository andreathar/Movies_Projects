# Respan — tracing & gateway for Gemini calls

Set up 2026-10-13 following https://www.respan.ai/docs/agent-setup.md.

## What is wired
- `.env` → `RESPAN_API_KEY` (gitignored). `.env.example` documents it.
- venv packages: `respan-ai`, `respan-instrumentation-google-genai`, `google-genai`, `pillow`
  (installed with `uv pip install --python .venv/bin/python …` — the venv has no pip).
- `scripts/gemini_generate.py`: creates `Respan(instrumentations=[GoogleGenAIInstrumentor()])`
  **before** `genai.Client(...)`, so every `generate_content` call is exported as a trace.
  - Default (no `RESPAN_GATEWAY`): calls Google directly with `GEMINI_API_KEY`; trace goes to Respan.
  - `RESPAN_GATEWAY=1`: client uses `api_key=RESPAN_API_KEY` and
    `http_options={"base_url": "https://api.respan.ai/api/google/gemini"}`.
- `scripts/respan_smoke.py`: cheap text-model smoke test with the same wiring.

## Verify
```bash
cd scripts && ../.venv/bin/python respan_smoke.py                  # tracing
cd scripts && RESPAN_GATEWAY=1 ../.venv/bin/python respan_smoke.py # gateway
respan traces list --limit 5 --json                                 # expect error_count 0
respan logs list --limit 5 --all-envs true --json                   # gateway logs: model + tokens + cost
```
CLI: `@respan/cli` 0.17.0 installed globally via nvm (`npm install -g @respan/cli`).

## Status (2026-10-13)
- ✓ Tracing verified: trace `llm.gemini-3.8-flash`, error_count=0, span_count=1, 159 tokens.
- ✗ Gateway: wiring verified (request reaches Respan, auth OK) but returns 401 — no Gemini provider
  key / credits. **Decision 2026-10-13: gateway NOT used.** Respan has no free models or signup
  credits; gateway needs prepaid credits (min $10) or BYOK, and BYOK is Team-plan only ($199/mo).
  Tracing on the Free plan already gives prompt/model/tokens/cost per call, which is what we need.
  `RESPAN_GATEWAY=1` stays as an opt-in if credits are ever bought — no code change needed.

## Mistake / Solution record
| Mistake | Solution |
|---|---|
| `.venv/bin/pip` missing (venv created `--without-pip`) | Use `uv pip install --python .venv/bin/python <pkgs>` |
| Smoke test used `gemini-2.5-flash` → 404 "no longer available to new users" | Use `gemini-3.8-flash` (Google's suggested replacement). The 404 was still traced (error_count=1) — useful proof that errors are captured. |
| `respan … --json` prints a trailing `Page 1 \| Total: N` line → `json.load` fails | Strip the last non-JSON line (`head -n -1`) or grep the fields you need. |
| Gateway 401 "add your Google Gemini AI API key in Settings -> Providers" | Not a code bug: Respan needs provider credentials or credits before it can proxy Gemini. |
| Assumed the gateway would work on the Free plan | Check plan gating first: Respan Free = tracing only in practice; gateway = credits ($10+) or Team-plan BYOK. Tracing was the real goal (token/cost tracking), so gateway was unnecessary. |
| API key pasted into chat | Rotate it at platform.respan.ai → API keys after setup and update `.env`. |

## Coding-agent tracing (added 2026-10-13 afternoon)
Goal: one Respan dashboard with token spend of all 3 agents (Codex, Claude Code, OpenCode).

| Agent | Status | How it's wired |
|---|---|---|
| Claude Code 2.1.x | ✓ verified (2 spans accepted, `rejectedSpans: 0`) | `~/.claude/settings.json` → `hooks.Stop` runs `TRACE_TO_RESPAN=true node …/@respan/cli/dist/hooks/claude-code.cjs`. Log: `~/.claude/state/respan_hook.log`. |
| Codex CLI 0.162 | ✓ verified (2 spans accepted) | `~/.codex/config.toml` → top-level `notify = ["<node>", "…/dist/hooks/codex-cli.cjs"]`. Log: `~/.codex/state/respan_hook.log`. |
| OpenCode 1.18 | ✓ verified (custom plugin, spans accepted) | `~/.config/opencode/plugins/respan-trace.ts` spawns detached `~/.config/opencode/respan/worker.cjs` on `session.idle`; worker reads `~/.local/share/opencode/opencode.db` (SQLite, read-only) and POSTs OTLP spans. Log: `~/.config/opencode/state/respan_trace.log`. Backfill: `node ~/.config/opencode/respan/worker.cjs <sessionID> --all`. (`opencode-otel` was unusable: metrics/logs only.) |

Credentials: `~/.respan/credentials.json` (`{"default": {"apiKey": …}}`, chmod 600) — both hook runtimes read it, so no key in agent configs. Backups: `~/.codex/config.toml.bak-respan`, `~/.claude/settings.json.bak-respan`.
Spans carry `gen_ai.request.model`, `gen_ai.usage.prompt_tokens/completion_tokens`, `llm.usage.total_tokens`. Sample: Codex "say hi" = **32,617 prompt tokens** (system prompt + AGENTS.md); Claude Code = 2 prompt / 8 completion (cache-read tokens not counted — treat Claude numbers as lower bounds).
Debug env: `CODEX_RESPAN_DEBUG=true`, `CC_RESPAN_DEBUG=true`. Reprocess all turns: delete `…/state/respan_state.json`.

Re-verify: `respan traces list --limit 5 --json` → expect `claude-code` and `codex-cli` traces, error_count 0.

### Mistake / Solution (agents)
| Mistake | Solution |
|---|---|
| `codex exec` hung for 3 min: "Reading additional input from stdin…" | When run from a non-TTY shell (Desktop Commander, cron, hooks) always `codex exec "…" < /dev/null`. |
| Followed docs page (Python `respan_hook.py` + `.bashrc` env) | `@respan/cli` ships newer Node runtimes in `dist/hooks/`; use those and put `TRACE_TO_RESPAN=true` inline in the hook command instead of shell rc files. |
| Assumed opencode-otel → Respan would work (the guide implies it) | Check signal types: metrics/logs ≠ traces. OpenCode needs a custom plugin posting to `/api/v2/traces` — see Next. |
| `respan traces list` returned 405 right after verification (ingest still 200, bogus key → 403) | Server-side on Respan, not our config. Verification evidence = hook logs `rejectedSpans: 0` + dumped OTLP payloads in `…/state/respan_spans_turn_1.json`. Retry CLI later. |

### Next
1. OpenCode: write a small OpenCode plugin (`~/.config/opencode/plugins/respan.ts`) that on `session.idle` posts an OTLP span (model + usage from `session.messages`) to `https://api.respan.ai/api/v2/traces` — closes the 3rd agent.
2. Tag spans per movie task: set `RESPAN_WORKFLOW_NAME=<scene-id>` / `RESPAN_METADATA` in the Parley launcher so cost rolls up per scene.
3. Kling calls: wrap `kling_batch.py` / `kling_release.py` with Respan `@workflow`/`@task`.
| Plugin did async fetch+POST inside the `session.idle` handler → nothing sent | `opencode run` exits right after the reply, killing in-flight work. Spawn a detached worker (`stdio: "ignore", detached: true, unref()`), same as @respan/cli hooks. |
| Expected OpenCode sessions under `~/.local/share/opencode/storage/` | OpenCode ≥1.18 stores sessions in `opencode.db` (SQLite: `session`, `message`, `part`; JSON in `data` columns). Read with `node:sqlite` (Node 24). |
| Queried `select data from session` | `session` is a wide table (title, directory, agent, model, tokens_*…); only `message`/`part` have `data`. |

Audit of per-turn overhead and reduction strategies: `docs/TOKEN_SPEND_AUDIT_2026-10-13.md`.

## Per-scene cost roll-up (added 2026-10-13 14:55)
- Lane shell: `source scripts/lane_env.sh <lane> <role> <scene-id> [episode]` → exports `MOVIES_LANE_NAME`, `MOVIES_LANE_ROLE`, `RESPAN_WORKFLOW_NAME=<scene-id>`, `RESPAN_METADATA={lane,role,scene,episode}`. Verified on all three agents: root span `traceloop.workflow.name = <scene-id>`, metadata carries lane/role/scene/episode.
- Project defaults for the Respan hooks: `.codex/respan.json` and `.claude/respan.json` (`customer_id: movies-projects`, `project`, `episode`) — known keys become span fields, extra keys become metadata. The OpenCode worker gets the same tags from the env vars (it doesn't read those files).
- In Respan: filter traces by Workflow Name = scene → sum of tokens/cost across Codex, Claude Code and OpenCode turns for that scene. Gemini image calls (`gemini_generate.py`) are not yet tagged — pass `RESPAN_WORKFLOW_NAME` through the SDK init when needed.

| Mistake | Solution |
|---|---|
| Looked for a per-lane config knob in the hook runtimes | They already read `RESPAN_WORKFLOW_NAME` / `RESPAN_METADATA` / `RESPAN_CUSTOMER_ID` env and `<cwd>/.codex|.claude/respan.json`; no code change needed, just a sourced env helper. |
