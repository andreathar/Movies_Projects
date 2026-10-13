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
| Assumed opencode-otel → Respan would work (the guide implies it) | Check signal types: metrics/logs ≠ traces. OpenCode needed a custom plugin posting to `/api/v2/traces` (done, see Coding-agent tracing table). |
| `respan traces list` returned 405 right after verification (ingest still 200, bogus key → 403) | Server-side on Respan, not our config. Verification evidence = hook logs `rejectedSpans: 0` + dumped OTLP payloads in `…/state/respan_spans_turn_1.json`. Retry CLI later. |

### Next (updated 2026-10-13 15:15)
1. ~~OpenCode plugin~~ — done (`~/.config/opencode/plugins/respan-trace.ts` + worker).
2. ~~Per-scene tagging~~ — done (`scripts/lane_env.sh`, `.codex/respan.json`, `.claude/respan.json`, Gemini wrapped in `respan.workflow`).
3. Kling: hook local de submissão implementado em `scripts/kling_batch.py` / `scripts/kling_respan.py`; validação sintética, sem envio real de telemetria. Contrato e limites na seção abaixo; créditos não são moeda.
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

## Readiness check 2026-10-13 15:15
- Respan plan confirmed **Free** (platform billing page: current plan "Free"). Tracing only; gateway unused by decision. Free limits: 100k logs, 7-day retention, 412 logs/min — fine for lane traffic.
- Symlinks: repo `skills/` (5), `.claude/skills` (1), `.hermes/skills` (5), `.hermes/plans` (1) all resolve; user stores `~/.claude/skills` 7, `~/.hermes/skills` 3, `~/.agents/skills` 1 — 0 broken. `skills/registry.json` matches disk. `manage.py validate` exit 0, unit tests OK.
- Tracing: Claude Code hook, Codex notify hook, OpenCode plugin, Gemini SDK — all verified today with scene tags.
- Known: Respan read API (`respan traces list`) 405 since ~13:45; ingest 200; dashboard is the check until it recovers.


## Kling: submissão e custos por cena (2026-10-13)

`scripts/kling_batch.py` mantém o envio pela CLI e suas liberações existentes. Após
salvar a intenção e antes de enviar, o adaptador opcional `scripts/kling_respan.py`
abre `respan.workflow` com o nome da cena e uma task `kling.submit`. O span inclui a
submissão única e a persistência/reconciliação; polling, download e `--resume` ficam
fora dele e não emitem novamente a cobrança.

Ativação segue a chave já configurada no **ambiente do processo** (`RESPAN_API_KEY`).
`MOVIES_KLING_RESPAN=0` desativa sem importar o SDK. O runner não abre `.env`, cofres,
credenciais dos hooks ou bancos de sessões: o operador fornece o ambiente pelo seu
mecanismo existente. Sem chave, funciona sem tracing; sem SDK ou com erro de tracing,
preserva o resultado do provedor e emite aviso genérico. Não instala nem autentica.
`RESPAN_GATEWAY` não muda a rota Kling. Não usar os smoke tests pagos para verificar
este hook.

Tags seguem o padrão existente: `RESPAN_WORKFLOW_NAME` identifica a cena;
`RESPAN_METADATA` aceita somente `lane`, `role`, `scene`, `task` como identificadores
curtos. `task` é, por exemplo, `T13`, fornecido explicitamente; não é deduzido do nome
do job. O episódio vem da pasta do filme; projeto/script são fixos. Valores inválidos
ou livres são omitidos; workflow prevalece sobre `metadata.scene`. Sem cena válida,
usa `kling_batch`, sem fingir atribuição a uma cena. A intenção salva `costTrace`
com esses vínculos, `execution_id`, `job` e `cost_event_id` estável para o registro.
Isso é correlação declarada pelo operador, não autorização nem aceite artístico.

Os seguintes atributos `respan.metadata.*` de custo pertencem **somente à task**:

| Campo | Fonte / significado |
|---|---|
| `cost_provider`, `cost_unit` | `Kling`, `Kling credits` |
| `credit_quote`, `credit_quote_basis` | `intent.release.quote`: cotação específica validada, `provider_quote` ou `official_panel`; estimativas não são promovidas |
| `credit_charge`, `credit_charge_basis` | Resultado de `reconcile`, mesmo valor de `*.balance.json`/ledger; só `provider_reported` aceita valor confirmado, inclusive zero |
| `submission_state`, `generation_id` | Resultado local da submissão / ID retornado; ID ausente ou inválido não é inventado |
| `cost_event_id`, `execution_id`, `job` | Correlação persistida antes do envio; chave de deduplicação e execução |
| `currency_conversion` | `none`: nenhuma taxa de conversão foi definida |

Saldo e variação de saldo **não são cobrança por job**. Ausência de cobrança fica
`unknown` e sem número, não zero. Cotação não se soma à cobrança. Um erro de submissão
pode ter cobrança confirmada e ela continua visível. ID conhecido não significa job
concluído. O ledger/recibos são a fonte de verdade; Respan é uma projeção opcional.
Nenhum segundo ledger, preço, aprovação ou evento contábil é criado pelo tracing.

Para consolidar a cena, agrupar por provedor/unidade e deduplicar por `cost_event_id`
antes de somar `credit_charge`. Separar cobertura conhecida/desconhecida e mostrar
cotações à parte. Tokens são uso, créditos Kling são saldo consumido, moeda é custo
financeiro: não existe um total escalar válido somando os três. O hook não preenche
campos padrão de custo monetário/LLM do Respan com créditos. Conversão futura exige
base explícita (compra/plano, moeda, taxa e vigência); não foi implementada aqui.

Falhas do SDK antes/depois do callback, ao anotar ou ao flush não repetem a operação.
Erros locais de persistência retornam ao chamador, sem vazarem no decorator; cancelamento
antes do envio não inicia geração. Intenção durável e bloqueio de duplicatas continuam
valendo. SDK/exportador pode perder spans ou retransmitir o mesmo span: não se promete
entrega remota exatamente uma vez. Não repetir geração para recuperar telemetria;
usar recibos e chave do evento. Falha entre envio/recibo/ledger pode deixar tracing
incompleto; `--resume` conserva a recuperação contábil existente, sem backfill Respan.
Cobranças reveladas apenas em consultas posteriores continuam dependendo da
reconciliação existente/manual, não são inventadas nem reaplicadas por este hook.

Privacidade: funções decoradas não recebem argumentos e retornam `None`; payload,
prompt, imagens, comandos, rationale, respostas brutas, saldo da conta e mensagens
de erro não são atributos. Auto-instrumentação está desativada explicitamente.
Correlação usa lista permitida, não exporta todo `RESPAN_METADATA`. Testes usam mocks
e, para o SDK instalado, exportador em memória com sockets bloqueados. Não houve
chamada paga, upload ou exportação real nesta validação.

Compatibilidade conferida com `respan-ai 4.2.4` e OpenTelemetry `1.45.1`; API pública
`Respan`, `workflow`, `task`, `flush` e atributos de span, conforme o
[repositório oficial](https://github.com/respanai/respan#workflow-and-task-decorators).
O frontend mantém o contrato existente de recibos/registro; não recebe campos
monetários novos nem exige refresh de snapshots por este hook.

Antes da primeira geração **separadamente autorizada**, confirmar cena/tarefa no
ambiente e chave disponível sem imprimi-la. Depois, comparar o ID/quote/charge/unidade
na task com a intenção e recibo locais, conferir agrupamento da cena e ausência de
conteúdo sensível. Repetir somente `--resume` do job existente para verificar que não
aparece novo evento de custo. Essa verificação remota permanece pendente; o teste
sintético não comprova ingestão, dashboard ou agregação financeira em produção.

## Dashboard reading 2026-10-13 15:30 (Metrics page, Today)
117 requests, 3 errors (gemini-2.5-flash 404, gateway 401, +1). Top models: **None 109**, gemini/gemini-3.8-flash 5, keywordsai/cache 2 (Respan's own cache marker — Respan = ex-Keywords AI), gemini-2.5-flash 1.
- "None" = every span from the agent hooks (Codex `gpt-6.1-sol`, Claude Code `claude-fable-5-1`, OpenCode `muse-spark-1.1`). The spans DO carry `gen_ai.request.model` (verified in the dumped payloads) — Respan just doesn't recognise those model IDs in its catalog, so the Metrics page buckets them as None and **computes no $ cost for them**. Token counts are intact. Gemini resolves because its model is in the catalog.
- Consequence for the per-scene price: tokens per agent/scene are exact; the $ column is only right for Gemini (and OpenCode, whose worker sends OpenCode's own `cost`). Codex/Claude $ must come from a local price table (SQL editor or report script) until Respan maps the models.
- Logs page: "Oops… something went wrong"; Traces page freezes the tab; CLI `traces list` 405 since ~13:45 — platform-side degradation of the read path; ingest 200 all day. Re-check tomorrow.

| Mistake | Solution |
|---|---|
| Assumed Respan would price any model string carried in `gen_ai.request.model` | It prices only catalog models. Check "Top models by requests" after the first run of a new agent/model: a "None" bucket means no $ will be computed → add the model mapping in Respan settings (if offered) or keep a local price table. |

## Real lane test 2026-10-13 15:40–15:55 — scene `s00-respan-lane-test`
Three Parley lanes launched from the base checkout with `source scripts/lane_env.sh <lane> <role> s00-respan-lane-test` + `agent-parley run <p> --output-task s00-respan-lane-test --task "<read-only smoke task: status, read audit doc, file one 3-finding report, DONE>"`. Roster rebuilt first: `opencode` retired/re-added (worktree was gone), `codex` added on provider **`codex-film`**, `claude` reused (lane-4).

| Lane | Outcome | Respan (scene-tagged, accepted) |
|---|---|---|
| codex (codex-film) | report **ready**, 3 findings citing doc lines; Parley MCP `list_participants` worked, `status`/`report` MCP tools absent → used CLI (fine) | 9 spans/turn: `openai.chat` gpt-6.1-sol 40,848 prompt / 5 completion + Reasoning + 6× `Tool: exec` |
| claude (lane-4) | report **ready**, 3 findings; flagged that the Claude lane carries claude.ai connectors as deferred tools (ElevenLabs ≈200, Cloudflare Dev Platform, Gmail, Swagger, HF, Desktop Commander) | `claude.chat` claude-fable-5-1 162 prompt (cache-read omitted) / 4,112 completion + ToolSearch + 6× Bash |
| opencode (muse-spark-1.1) | report **partial** with placeholder text `a\nb\nc` — model did not follow the task; stopped | 2 turns captured: 26,851+62 ($0.0051) and 49,863+1,243 ($0.0136) |

Per-scene roll-up works end to end (workflow name + lane/role/scene/episode metadata on every span). Dashboard read path still 405/erroring on Respan's side; evidence from hook logs (`rejectedSpans: 0`) and local payload dumps.

Lane launch recipe that works from a non-TTY shell (Desktop Commander, cron): `script -qfec "agent-parley run <p> …" /tmp/<p>.typescript` under `nohup … &`.

### Mistake / Solution (lane test)
| Mistake | Solution |
|---|---|
| `--output-task S00-…` refused | Task ids must match `[a-z0-9][a-z0-9_-]{0,38}`: lowercase scene ids (`s00-…`). Use the same lowercase id for `RESPAN_WORKFLOW_NAME`. |
| `agent-parley run codex` → "stdin is not a terminal" | Native TUIs need a pty: wrap in `script -qfec "…" <log>`. |
| OpenCode lane blocked on "Permission required: access external directory …/Movies_Projects" (lane reads the shared checkout from its worktree) | `permission.external_directory: {"/mnt/data/Projects_SSD/Movies_Projects/**": "allow"}` in `~/.config/opencode/opencode.json` (copied into the lane-private config) and repo `opencode.json`. |
| `opencode` participant had a dead worktree; `restore` refused while a 16 h idle session was attached | `participant stop` → `retire` (branch had no commits) → `add --provider opencode`. |
| Tried `agent-parley report show --as <lane>` / `mail list` from base checkout | Reports are read with `participant show <lane>` (Summary / Reported verification); mail only from a lane worktree. |
| Expected muse-spark-1.1 to follow a 4-step task | It filed `a\nb\nc`. For film lanes pick a stronger OpenCode model or keep OpenCode for mechanical tasks; cost per turn is low but output was useless. |
| Claude lane audit: assumed only the repo's MCP config mattered | claude.ai connectors sync into Claude Code as deferred tools; review the connector list for the lane account, not just `.mcp.json`. |

## First real chain 2026-10-13 16:01–16:20 — scene `t12-detail-studies-v1-review`
Workflow-map priority 1 (independent review of detail-studies-v1) dispatched to 3 lanes per `docs/MODEL_POLICY.md`: Big Pickle mechanical pass → Claude materials review → Codex-film continuity review. All three reports `ready`; deliverables + hashes in `projects/andre-time-travel/agents/handoffs/2026-10-13-t12-detail-studies-v1-independent-review-dispatch.md`. Per-scene spans accepted for all three agents (Codex 26 spans/turn, Claude 57 spans/turn).

| Mistake | Solution |
|---|---|
| `launch2.sh` set `TASK=` without `export` → `script -c` subshell saw an empty `--task`; all three lanes started with no task (Codex did a generic startup check, muse-spark burned ~$0.016) | `export TASK=…` before `script`. Verify `agent-parley status` TASK column shows the task text within 30 s of launch. |
| OpenCode lane ran muse-spark despite the repo `opencode.json` pin | Parley copies the **global** `~/.config/opencode/opencode.json` into the lane-private config, and the worktree carries only the *committed* repo config. Pin the model globally (`opencode/big-pickle`) and commit the repo pin. |
| `pkill -f 'agent-parley run'` killed my own shell (its command line contained the pattern) → fixes silently didn't apply | Use `agent-parley participant stop <p>` only, or `pkill -f` with a pattern that can't match the caller. Re-check each fix with a separate command. |
| Lanes write to `outputs/<output-task>/…` in their worktree, not to the path given in the task text | That is Parley's shared-media rule (derivatives confined to the lane output root). Read deliverables from `~/.local/state/agent-parley/projects/<id>/<lane>/outputs/<task>/`; the producer integrates. |
| Lane worktrees have no `.venv` → `manage.py status` exits 2 inside a lane | Tell lanes to run project tools from the shared checkout's `.venv`. |

## Mistake / Solution — production checklist (2026-10-13)

| Mistake | Solution |
|---|---|
| Plan was to turn every WARN/INFO into ERROR; `overrides` only dismiss WARN, so this would make documented false positives unfixable and break 8 tests that encode the design. | Added `unresolved_ambiguity()` + `check-coherence --strict`: any WARN/INFO without a valid reviewed override blocks as an error. ERRORs still cannot be overridden. Real plan now reports 6 open `INPUT_ROLE_UNDOCUMENTED`. |
| Session lost its link to the repo (`/mnt/data/...` not found in the cloud container; no shell tool). | Checked connected folders, listed the path (skeleton), requested folder access once, then used the device shell. Always verify the link before assuming paths. |
| Registry/hash contract was assumed covered because `production_plan.py` hashes files; 32 detail-study PNGs were absent from the registry. | `scripts/asset_contract.py check` fails until every manifest hash is registered; proposal rows (approved=false) in `reports/detail-studies-v1-registry-proposal.csv`, canonical registry untouched. |
| Agent roles had skills but no delegation field; coordinator had none at all. | `delegatesTo`/`escalatesTo` per role, enforced by `manage.py validate` ("cannot be automated"). |
