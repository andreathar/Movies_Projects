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
