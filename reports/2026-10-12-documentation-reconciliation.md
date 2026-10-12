# Reconciliação documental — 2026-10-12 UTC

Autorização: Andre pediu “corrija tudo e pode remover tudo para trás. agora vamos fazer quase tudo de novo”. Esta entrega corrige as divergências documentais demonstradas. Andre esclareceu depois: preservar originais, decisões e entregas; manter roteiro e cinco encontros e refazer planejamento visual/cenas. Nenhuma exclusão foi executada. O plano novo está em `drafts/andre-time-travel-visual-restart-v1/README.md`, com fontes e escopo em `scope.json`.

Escopo executado: centralizar startup em AGENTS; alinhar a referência ao remoto já documentado; distinguir skill externa, manifesto declarativo e runtime; substituir pressupostos desatualizados por evidência datada; marcar setup/smoke antigos como históricos, sem executá-los. Sem mudança de flags, grants, hooks, serviços, mídia, gastos, aprovações ou estados de tarefas. Edição local; nenhum commit/merge/push.

## Cadeia do handoff

O registro `projects/andre-time-travel/agents/handoffs/2026-10-11-structure-naming-merge-v1.json` foi preservado byte a byte (SHA-256 `d895c30d481db87e4b053811013ba01d927320518a2e51e475cd2eebd9550789`). Seus dois erros eram a mesma versão antiga de `agents/coordinator.md`: o hash `601e8e5f23c326534f37f4ba6667288786fd0113961743f74d71a9bcadf739b3` foi reconfirmado no objeto Git `2f96351622bac02142a8d7bf18100ed07da75b70`; o hash pré-correção `e8f901a3f948d4c51bc22d6895c114df8d2157d9a91212b594f8674bbbe36027` foi reconfirmado em `d5bd9cf70a279588e255a939ef13523f2caa0ca0`.

O delta entre essas duas versões tem apenas as duas correções de caminho abaixo. Esta entrega altera adicionalmente o texto de startup, com hash próprio na tabela final. Não se reescreve a evidência histórica como se tivesse sido produzida na versão atual.

```diff
--- 2f96351622bac02142a8d7bf18100ed07da75b70
+++ d5bd9cf70a279588e255a939ef13523f2caa0ca0
@@ -7,7 +7,7 @@
 ## Startup
 
 1. Read workspace `AGENTS.md`, `workspace.json`, active film `memory/STATE.md`.
-2. Load `tasks/board.json`, `tasks/workflow-map-v1.md`, `00_brief/approvals.json`, `00_brief/decisions/`.
+2. Load `tasks/board.json`, `tasks/plans/workflow-map-v1.md`, `00_brief/approvals.json`, `00_brief/decisions/`.
 3. Inspect `docs/PARLEY_PROTOCOL.md` section "Lane roster v2" for active lane roster and dispatch contract shape.
 4. Review `docs/COORDINATOR_PROTOCOL.md` for dispatch logic, readiness rules and dependencies.
 5. Read existing `agents/handoffs/` directory for handoff patterns and decision consolidation.
@@ -18,7 +18,7 @@
 ### Read
 
 - `tasks/board.json` → task status, ownership, dependencies, blockers, deliverables.
-- `tasks/workflow-map-v1.md` → production flow, readiness conditions, immediate queue, work packages W01–W68.
+- `tasks/plans/workflow-map-v1.md` → production flow, readiness conditions, immediate queue, work packages W01–W68.
 - `memory/STATE.md` → current creative direction, approvals true/false, money, Andre-only gates.
 - All handoffs in `agents/handoffs/` → verify delivery hashes, extract blocking conditions, prepare next assignment.
 - `00_brief/decisions/D01–D20` → explicit decisions made; D17–D19 are proposals not yet recorded.
```

Os cinco artefatos do handoff anterior foram conferidos antes da edição. Quatro ainda coincidiam; somente coordinator divergia. O novo handoff conserva evidência dos três artefatos que permanecem intocados e registra as versões atuais dos dois alterados. A relação `supersedes` significa substituição das claims sobre a árvore atual após esta revisão de versões, não aprovação artística, ingestão ou alteração do registro original. O novo handoff fica `pending_producer_review` / `pending`.

| Artefato anterior | Hash registrado | Hash antes deste lote |
|---|---|---|
| `agents/coordinator.md` | `601e8e5f23c326534f37f4ba6667288786fd0113961743f74d71a9bcadf739b3` | `e8f901a3f948d4c51bc22d6895c114df8d2157d9a91212b594f8674bbbe36027` |
| `agents/registry.json` | `ea102925226952a39ceb6a26fe12d8e97f9c90012b57a998f85f7ada82085da9` | `ea102925226952a39ceb6a26fe12d8e97f9c90012b57a998f85f7ada82085da9` |
| `docs/COORDINATOR_PROTOCOL.md` | `a1cad27b73cdcb5f4184d7862799ba55a6e11f7fe9c8125356349cd8e376ddfd` | `a1cad27b73cdcb5f4184d7862799ba55a6e11f7fe9c8125356349cd8e376ddfd` |
| `reports/2026-10-11-structure-naming-agents-review.md` | `6dcc1f3d4e7e6b9ce66f3bb85dae145dc4fd574c286cae5ae7f2b1740e7ab780` | `6dcc1f3d4e7e6b9ce66f3bb85dae145dc4fd574c286cae5ae7f2b1740e7ab780` |
| `skills/registry.json` | `f82911ffa2226e9b73eeabe5541a48b8d5feae32836b66f9e5ac45e2c02f570e` | `f82911ffa2226e9b73eeabe5541a48b8d5feae32836b66f9e5ac45e2c02f570e` |

## Runtime e skill: evidência, não ativação

A inspeção anterior registrada em `/home/athar/Documents/Codex/2026-10-11/task-2/deliverables/parley-rebuild-evidence.json` contém a thread `PARLEY-TOOLS-20261012T0140Z`: 49/51 Codex → Claude, 50/52 Claude → Codex, com recibos. Foram observadas chamadas de 18/19 ferramentas por lane; `retire` foi excluída. Não comprova todos os ramos nem um handoff real de issue. Nenhum novo teste ou mensagem foi enviado nesta correção.

Em 2026-10-12T02:07Z, `agent-parley status --json`, `participant list --json` e `issue list --json` confirmaram serviço ready, participantes existentes claude/codex, nenhuma issue e nenhuma reserva ativa nas duas lanes. Idle e processo vivo não são aceite de nova tarefa.

A fonte externa `../agent-parley/plugins/agent-parley/skills/coordinate/SKILL.md` e o plugin instalado em `/home/athar/.codex/plugins/cache/agent-parley/agent-parley/0.18.0/skills/coordinate/SKILL.md` existem e têm SHA-256 `3693db0b21a838b019f1a9efef3cab6d7e88ff8144ea2c29b13417c4a394c2e3`. Isso não prova carregamento na sessão de um peer. Registro de papéis e manifesto continuam sem ativação adicional.

## Arquivos desta correção

Base Git: `fde47d6d20215fe6fcd40658c7354330f58caf4e`. A comparação do registry deve mostrar somente `coordinator.notes`; a do manifesto de plugin, somente `description`. As salvaguardas atuais de atlas v3 e publicação privada continuam em START_HERE.

| Caminho | SHA-256 antes | SHA-256 depois |
|---|---|---|
| `AGENTS.md` | `e8846485869d9f0d6341c81e7da8cd05f138fbccb59c3e3a3c5fb66c38d604df` | `4bfa5e5ae1cb413fe1882dc3f38b237e44eb0a5866bccf3426fe2e250553f4bc` |
| `START_HERE.md` | `e3ee5f23640bbe747092409f04d45ef43549e7d8547e857e18bef4c0c850f0b8` | `396779375f36c26be06e1261661b61fe2cc9f54a186c47b5058482f9bae07e79` |
| `agents/coordinator.md` | `e8f901a3f948d4c51bc22d6895c114df8d2157d9a91212b594f8674bbbe36027` | `eb4122374da37cd414c1512fc440d89e5f1c073f384b90307f08326e0f8912d5` |
| `agents/registry.json` | `ea102925226952a39ceb6a26fe12d8e97f9c90012b57a998f85f7ada82085da9` | `2f2e7eb2dd24e1ed6f13ca6877901d1ff5085fe5076260b9b111f3bbc5f664f4` |
| `.agents/plugins/agent-parley/plugin.json` | `61eaed407a54f3646312a44e6dd436409311f7bf95b18d288d7a915b857f2826` | `1149a2ae3afe257f039d2b3ea127f29b9691ac048ad764c6bab50ac87b9ac468` |
| `docs/PARLEY_PROTOCOL.md` | `a561819dcf4d62c0f6859e6ab0e288ff6502ef1ae884e38f0a47e0408fc04883` | `e9801936734e16a8deb4387cd486df637e3056f64d3dcf7b249b86f19c3ff9f0` |
| `docs/PLAN-parley-integration-v1.md` | `bbbe737c04b21e18980e4bf9de235c19ea4f7cfc74d016d4be4732a147d51670` | `5d60f4fd3246f8a1b38a7e41b788e3a4a9d6cc6d08b71c939d6923a8c10ff366` |

## Preservação, verificação e sucessor

Os quatro arquivos já modificados sob `.agents/skills/kling-cli/` foram preservados; não atualizar hashes do registry de skills para ocultar esse trabalho concorrente. Manifesto, board, aprovações, STATE, session-log e handoff anterior foram comparados por hash e permanecem iguais ao início deste lote. Originais, mídia, decisões, pesquisas, patches e trabalho das lanes não foram removidos nem movidos.

Verificação do lote: `validate` ok (quatro avisos já existentes de hashes de skills), 84 testes stdlib passaram, `lint` sem hard errors e `handoff check` ok. Resultados também constam em `verification[]` do novo handoff; sucesso técnico não é aceite artístico. A cópia anterior dos sete documentos e o diff do lote ficam no workspace desta tarefa, em `deliverables/correcoes-before-20261012.json` e `correcoes-documentais-20261012.patch`. Recuperação por trechos, sem sobrescrever mudanças concorrentes.

Próximo responsável: produtor/base, para revisar a proposta de cobertura por encontro, detalhar o proof shot de Galileu e incorporar a nova direção na retomada. Escopo confirmado por resposta direta: mesmo roteiro e cinco encontros, novo planejamento visual e cenas, acervo preservado. Nenhuma nova atribuição foi enviada às lanes.

Durante a validação apareceram commits concorrentes `d54c3899fc1ddf7c1c4bef303868364b1ee30c1f` (documentação e alterações Kling preexistentes) e `65d56f1c22068a1371891288d21cf3dbf19cfd45` (primeira versão deste relatório/handoff). Esta tarefa não executou commit/push nem atribui autoria operacional desses atos; preservou-os. As atualizações de escopo e resultados são edições posteriores, sem reescrever o histórico.
