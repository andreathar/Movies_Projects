# Relatório de consolidação documental — 2026-10-09

**Autor:** lane Claude (pesquisa, continuidade, documentação). **Pedido:** mensagem 21 do produtor (relayed de Andre). **Estado:** RASCUNHO para o produtor revisar e integrar; nada foi integrado na base, nada foi commitado. Sem gasto, geração, publicação ou outra delegação.

## 1. Escopo e limites cumpridos

- Editados (cópias de trabalho na lane, partindo das versões atuais da base): `START_HERE.md`, `docs/REPEATABLE_WORKFLOW.md`, `docs/PARLEY_PROTOCOL.md`, `docs/LOCAL_AGENT_HANDOFF.md`, `docs/VERSION_CONTROL.md`, `agents/README.md`.
- Novos: este relatório, `before/` (cópia exata das versões de partida) e `diffs/` (diff unificado de cada arquivo).
- **Não tocados:** `AGENTS.md`, `agents/registry.json`, manifest, board, approvals, ledger, `STATE.md`, session-log, roteiro. Propostas para AGENTS.md e registry estão só nas seções 6 e 7.
- Nada apagado. Históricos, snapshots, decisões e mídias intactos; o texto removido de cada documento está em `before/` e nos diffs.
- Base das versões de partida (checkout base, edições do produtor ainda não commitadas): ver §8.

## 2. Mapa de fonte canônica

Cada regra ou fato tem **um** lugar; os demais documentos apontam para ele.

| Assunto | Fonte canônica | Documentos que agora só apontam |
|---|---|---|
| Limites inegociáveis: rosto histórico, categorias de referência, diálogo ficcional, saldo e gasto, Kling pela CLI, emissor único, credenciais, escopo da memória, caminhos relativos | `AGENTS.md` | REPEATABLE_WORKFLOW, LOCAL_AGENT_HANDOFF, agents/README, PARLEY_PROTOCOL |
| Ordem de início de sessão | `AGENTS.md` "Session start" | START_HERE, LOCAL_AGENT_HANDOFF |
| Estado e retomada do filme | `memory/STATE.md` (+ manifesto, board, aprovações) | START_HERE |
| Processo reutilizável, etapas, contrato de tarefa, dependências, evidência de comunicação | `docs/REPEATABLE_WORKFLOW.md` | PARLEY_PROTOCOL |
| Mapa de autoria por função, formato de handoff, aprovação por versão | `docs/LOCAL_AGENT_HANDOFF.md` | REPEATABLE_WORKFLOW, agents/README |
| Commits, merges, integração entre lanes, worktrees, backup | `docs/VERSION_CONTROL.md` | REPEATABLE_WORKFLOW, PARLEY_PROTOCOL |
| Quem exerce cada papel neste episódio; mecânica do Parley; atribuições ativas | `docs/PARLEY_PROTOCOL.md` | REPEATABLE_WORKFLOW, LOCAL_AGENT_HANDOFF, agents/README, VERSION_CONTROL |
| Papéis e limites de cada função | `agents/registry.json` + `agents/*.md` | agents/README, START_HERE |
| Economia de contexto e de mensagens | `docs/TOKEN_EFFICIENCY.md` | REPEATABLE_WORKFLOW, START_HERE, PARLEY_PROTOCOL |

## 3. Repetição eliminada (antes → depois)

| Regra | Onde aparecia (antes) | Depois |
|---|---|---|
| Só o produtor emite jobs pagos | AGENTS; agents/README; LOCAL_AGENT_HANDOFF; REPEATABLE (tabela Lote e parágrafo de dependências); PARLEY (papéis e recurso `kling:submit`); MEMORY_AND_AGENTS; OPERATIONS | Texto completo só em AGENTS. REPEATABLE e LOCAL_AGENT_HANDOFF viram link; README mantém uma frase de lembrete; o recurso `kling:submit` fica no PARLEY (mecânica) |
| Reserva, nova tentativa e saldo de jobs | AGENTS; REPEATABLE ("ninguém reenvia um job…") | Só AGENTS |
| Commits, merge, push, integração | AGENTS; VERSION_CONTROL (ciclo + ponteiro); REPEATABLE (seção inteira); PARLEY | Seção única em VERSION_CONTROL (texto movido sem alterar palavras); REPEATABLE deixa um ponteiro; ponteiro circular entre os dois eliminado |
| Formato de entrega (handoff, hashes) | LOCAL_AGENT_HANDOFF; REPEATABLE (ciclo, passo 2); START_HERE | LOCAL_AGENT_HANDOFF; os outros dois apontam |
| Ordem de retomada | AGENTS; START_HERE (4 passos); LOCAL_AGENT_HANDOFF ("Retomada mínima": lia START_HERE antes do estado); STATE | AGENTS; START_HERE e LOCAL_AGENT_HANDOFF apontam (corrigida a inversão START_HERE-antes-de-STATE) |
| Quem é produtor/criador de imagens | REPEATABLE ("No filme atual é o Codex…"); PARLEY | Só a tabela de responsabilidades do PARLEY; REPEATABLE ficou sem nomes |
| Regra genérica de dependência de imagens | REPEATABLE; PARLEY | Regra genérica em REPEATABLE; PARLEY só declara o que é específico do episódio |

**Medida honesta:** o total de palavras dos seis arquivos subiu (de ~4.650 para ~5.260) porque adicionei a tabela de fontes, a tabela de responsabilidades, rótulos de status e os ponteiros. O que diminuiu foi o número de lugares onde a mesma regra é escrita (de 3–7 para 1). REPEATABLE_WORKFLOW ficou menor (1.907 → 1.792 palavras).

## 4. Nomenclatura aplicada

Responsabilidades (tabela única no `PARLEY_PROTOCOL.md`):

| Quem | Papel neste episódio |
|---|---|
| Andre | Autor e aprovador |
| Codex da conversa desktop/base | Produtor/coordenador e criador das novas imagens (não é a lane codex do Parley) |
| Lane Claude | Pesquisa, continuidade e documentação |
| Lane Codex | Editor/QC |

- "Nome de plataforma não é papel permanente": os documentos de processo descrevem **funções**; só a tabela do episódio liga função a plataforma, e uma continuação troca só essa tabela.
- Termos retirados nos arquivos editados: "Hermes" (agents/README), "parent" (agents/README, LOCAL_AGENT_HANDOFF), contagem fixa "seven" (agents/README; o registro lista nove funções).
- Termos que continuam fora do meu escopo: ver §6 e §7.

## 5. PROPOSED × autorizado

O arquivo `PARLEY_PROTOCOL.md` misturava texto marcado como proposta com atribuições autorizadas. Agora cada seção tem um selo:

| Selo | Seções |
|---|---|
| `[ACTIVE]` (autorizado por Andre em 2026-10-09 pela conversa produtora) | Responsabilidades do episódio; propriedade de recursos; atribuição ativa; propriedade de imagens; divisão de entregas |
| `[MECHANICS]` (fato sobre o Parley, não autorização) | O que o Parley dá e não dá |
| `[PROPOSED]` (ninguém pode agir) | Mensagem de fechamento (prática informal, não adotada como regra); gate de integração `verify set`; teste de fumaça (não registrado como executado nem aprovado) |

Não foi criado consentimento: itens que dependem de Andre continuam como proposta (ver §9).

## 6. Propostas para `AGENTS.md` (não aplicadas)

1. **"producer/parent agent" (linha 20)** → "the producer (the coordinating session)", com uma frase de definição. "Parent" é herança da época de delegação via Hermes e aparece também em `agents/producer.md`, `dialogue-sound.md`, `continuity.md`, `qc.md`, `storyboard.md`, `editor.md`, `historian.md` e `STATE.md`. Mudar AGENTS.md sem mudar os briefs cria nova divergência; propor as duas mudanças juntas.
2. Acrescentar uma linha: "responsáveis de cada episódio: tabela em `docs/PARLEY_PROTOCOL.md`; este arquivo descreve funções, não plataformas".
3. Em "Local editing…": "The user authorizes agents" → "Andre authorizes agents".
4. Em "Local version control": se Andre decidir a pergunta de commits por tarefa (§9, C2), registrar a resposta aqui, em uma frase.
5. O parágrafo "Direção dramática compartilhada" é conteúdo do filme, não regra do workspace. Sugestão: manter só um ponteiro em AGENTS.md e manter o texto no documento do filme (que já existe).

## 7. Propostas para `agents/registry.json` e `bindings.json` (não aplicadas)

1. Ligações pessoa↔função hoje só existem em prosa (tabela do PARLEY). Proposta: em `projects/<episódio>/agents/bindings.json` (hoje lista só as nove funções e `activeProcesses: []`), acrescentar `assignments`: função → rótulo do participante, checkout, estado e data. A prosa do protocolo viraria uma cópia legível.
2. `executionMode: "explicit_parent_delegation"` → `"explicit_producer_delegation"`. Verificar antes `manage.py validate` e os testes, que podem ler o valor.
3. O registro não tem uma função de **criação de imagens**; hoje isso está só na tabela do episódio. Decisão do produtor/Andre: acrescentar função ou continuar como responsabilidade do produtor.
4. "Pesquisa, continuidade e documentação" (lane Claude) mapeia para as funções `historian` + `continuity`; **não** proponho função nova. Proposta: permitir vários papéis por participante em `assignments`.
5. Não renomear `.hermes/plans` e `.hermes/skills`: constam de `workspace.json` (`requiredDirectories`) e os testes usam `~/.hermes/cache/scratch`.

## 8. Arquivos, hashes e verificação

Versões de partida (checkout base, com edições não commitadas do produtor) e finais (lane):

| Arquivo | SHA-256 antes (base) | SHA-256 depois (lane) |
|---|---|---|
| `START_HERE.md` | `cf9ec2e9c25df5422f9084ade323592cb3b28a5f0604bc507b9d568230f1dd5e` | `7a22370adcc866b84163e3d683243cb5321e22eaf8de468a9bbaac5d18b5ad72` |
| `docs/REPEATABLE_WORKFLOW.md` | `1e97ea4ade5940508e12f246a44822b90631b6636e67fc397fcb99415849f70b` | `7c1b0052b5691d4f4d91a8fcf795465fb784973f6610d50330e1adf710f3073d` |
| `docs/PARLEY_PROTOCOL.md` | `967e8d6df052ca5a2a85abb49a0c00491907abbc15df7d25e4909d3d54771845` | `54c7c5d40b07274892b793c021d7248383c5786f1df3463215748fc7b6d3a233` |
| `docs/LOCAL_AGENT_HANDOFF.md` | `53342efdc8296d6a4754947740faa599409cb38228c06ce801a96559e8fdb717` | `101797f6977efe7649f50e00dd1f862cf0549ebfbb5f8eb10526160200c477f6` |
| `docs/VERSION_CONTROL.md` | `6ca63f3d0342f212c61bf9e2b61316612146b7200ef7fff8b73f5bc5096d8dfb` | `b9f82f8052e881ff1b92ae7f575eb28670f2170ef125febf658eeab928e98795` |
| `agents/README.md` | `6afbe3c25c9f845ce47492d9ab551cd32538270bbca43867a1f122f79fa30c18` | `22299f651beb60078c29639a9814ab7207ab5261d614987bb32ddb386bef71d0` |

Arquivos lidos e não alterados (hash no momento da leitura): `AGENTS.md` `733b96bd3327dd85efa5ff64d284c6278b1cdf4d6ffc8dda266df55c15eba22d`; `agents/registry.json` `2f7ff27c4e02c646fc8b628c049b2911c7bc69a83c5b8736fb9af00a8a9e4c1e`; `projects/andre-time-travel/agents/bindings.json` `18da11a071dc055ffd30cd454f09c0e42d572181594cec01278bc02d7583e52d`.

**Links:** verificação dos links relativos de Markdown nos seis arquivos editados contra o conteúdo da lane e da base. 65 links (última checagem, depois dos deltas); todos resolvem. Os três para `docs/TOKEN_EFFICIENCY.md` resolvem **só na base** (o arquivo ainda não existe na lane). Referências escritas só em código (`` `caminho` ``), como `tasks/scene-detail-assets-v1.md`, existem apenas na base, não na lane.

**Executado na worktree da lane** (a `.venv` existe lá): `.venv/bin/python scripts/manage.py validate` → `status: ok`, 0 erros e 4 avisos já conhecidos (hash dos skills compartilhados `kling-cli`, `film-character-continuity`, `film-dialogue-localization`, `film-editing-qc`); `.venv/bin/python -m unittest discover -s tests` → 29 testes, OK. Isso mostra que a estrutura do workspace continua válida; **não** prova que a prosa dos documentos está correta nem substitui a revisão do produtor. O produtor deve repetir os dois comandos na base depois de integrar. Nenhum arquivo canônico foi alterado pela execução (`git status` da lane só mostra os arquivos listados acima).

## 9. Conflitos e decisões que exigem Andre

- **C1. Quem atualiza `STATE.md` e o session-log.** O texto antigo do protocolo dizia "quem fechar a tarefa"; a atribuição ativa dá a integração ao produtor. Mantive a segunda (consistente com este pedido). Confirmar.
- **C2. Commits por tarefa.** O ciclo de VERSION_CONTROL lia como rotina; AGENTS diz que não se faz commit sem autorização; STATE guarda a pergunta como pendente. Documentei "somente com pedido de Andre ou do produtor, sem autorização permanente". Andre decide se quer uma permissão permanente.
- **C3. Partes ainda PROPOSED:** gate `verify set`, teste de fumaça, mensagem de fechamento. Adotar, ajustar ou descartar?
- **C4. Autorização do papel "documentação" da lane Claude.** Registrei como "mensagem 21 do produtor, relayed do pedido de Andre". Confirmar que Andre quer isso registrado como atribuição ativa.
- **C5. Conflito com o resumo existente:** `docs/MEMORY_AND_AGENTS.md` ainda diz que há "Seven role briefs" e usa "parent"/Hermes; `docs/OPERATIONS.md`, `docs/SAFETY.md` e `docs/MEMORY_AND_AGENTS.md` repetem regras de AGENTS.md. Fora do meu escopo; proposta: reduzir cada um a um ponteiro para AGENTS.md e ao registro, com a mesma técnica.

## 10. O que não verifiquei

- Se `scripts/manage.py`, `scripts/workflow.py` e os testes aceitam as mudanças de termos propostas na §7.
- O caminho base dos comandos de atlas em REPEATABLE_WORKFLOW (`--source 05_storyboard/source/atlas.json` vs caminho completo): manteve-se como estava.
- Os briefs individuais em `agents/*.md` além de procurar "parent"/"Hermes".
- Se a base mudou desde a minha leitura: os hashes de partida foram conferidos de novo logo antes de eu copiar os arquivos.

## 11. Delta 1 — alinhamento com o Contrato obrigatório do AGENTS (mensagens 25 e 27)

Li a seção "Contrato obrigatório de organização" do `AGENTS.md` da base (hash na leitura: `5ff4402ddd6753773cf73bb983f1bf612d35137535eeb34a07d159deff7cece7`; hoje difere do `733b96bd…` da §8 por causa desse delta) e `docs/TOKEN_EFFICIENCY.md` (`9729b3b9…`).

- **Entrada e invariantes:** os documentos consolidados já apontam para o AGENTS.md como fonte das invariantes; não criei constituição paralela. Confere com o contrato: papel do produtor, lanes limitadas pelo `PARLEY_PROTOCOL.md`, imagens novas só na conversa produtora, commit/merge/publicação/gasto/aceite como autorizações distintas.
- **TOKEN_EFFICIENCY:** entrou por link em REPEATABLE_WORKFLOW, START_HERE e PARLEY_PROTOCOL; o texto não foi copiado.
- **Limite de garantia:** os meus documentos descrevem regras operacionais. Nenhum afirma que hooks, permissões ou gates impedem violação. A única menção a mecanismo é "reservas Parley são consultivas, não bloqueios" (PARLEY_PROTOCOL).
- **Divergência a reconciliar na integração:** a §6 (propostas para AGENTS.md) foi escrita antes do contrato. A proposta 2 ("tabela de responsabilidades") já está atendida pelo contrato (linha "Neste episódio: Codex da conversa desktop/base…"); retirar. As propostas 1, 3, 4 e 5 continuam válidas.

## 12. Delta 2 — regras antigas, documentos arquivados e ferramentas sem uso no filme (mensagem 29)

Método: leitura e `grep` na base, sem alterar nada; dependências conferidas em `scripts/manage.py` e nos arquivos de registro. Classes: **A** = manter ativo; **H** = referência histórica (manter, só marcar como histórica); **D** = candidato a desativação **para este filme**. "Remover a referência do filme" e "desinstalar a ferramenta para todos os projetos" são ações distintas; esta seção só trata da primeira e **não propõe desinstalar nada global**.

### 12.1 Regras e documentos antigos ou substituídos

| Item | O que encontrei | Classe | Dependência / cuidado | Ação sugerida (fora do meu escopo editável) |
|---|---|---|---|---|
| `README.md` raiz, linha 14 | Chama `projects/andre-time-travel/docs/production-plan.md` de "canonical production plan" | H | O próprio plano diz "DERIVED — do not edit dialogue here"; o roteiro canônico é `01_script/`. `manifest.json` (`sourcePlan`) também aponta para ele | Trocar o rótulo no README para "plano derivado"; manter o campo `sourcePlan` |
| `production-plan.md` | Contém a instrução operacional "For Hermes: Use the subagent-driven-development skill…" | H | Instrução de ferramenta que não vale mais; arquivos `reports/*` guardam hashes dele | Banner "histórico/derivado" no topo; não apagar |
| `docs/archive/production-plan-2026-10-08.md` | Arquivado; só aparece em índices de inventário (`reports/art-direction-v1/file-index.json`), não é citado como atual | H | Hash em snapshots | Manter como está |
| `memory/decisions.json` | Já marcado "superseded"; citado por `session-log.json`, handoffs e inventários | H | `scripts/manage.py:77` exige **`memory/projects.json`**, não `decisions.json` | Manter |
| `memory/projects.json` (campo `decisions`) | Ainda aponta para `memory/decisions.json` (superado); a fonte atual é `00_brief/decisions/` | A (arquivo) / corrigir campo | O arquivo é obrigatório em `manage.py`; **não conferi** se o validador lê o campo `decisions` | O produtor corrige o campo (arquivo canônico dele) e roda `validate` |
| `docs/budget-plan-v2.md` | Usa o saldo de 6.981 créditos de 9/10 de manhã; hoje a leitura registrada é 5.813 (STATE) e o plano atual é `budget-and-envelope-resume-v3.md` | H | Os três documentos desta linha e da seguinte aparecem em `session-log.json`, `D06-voice.json`, `manifest.json` e snapshots (o `grep` não separa qual cita qual) | Banner "substituído por v3; saldo não é ao vivo" |
| `docs/status-report-2026-10-09.md` (12:20) e `docs/decision-sheet-andre-v1.md` | Instantâneos; as decisões D01–D16 estão hoje em `00_brief/decisions/` | H | Citados por snapshots e revisões | Banner de data; manter |
| `docs/assistant-reviews/*-v1.md` | Rascunhos que as bíblias v2/v3 e os handoffs superaram, mas ainda servem de evidência (ex.: `continuity-bible-draft-v1.md` item CB-15) | H | Evidência citada por bíblias | Manter |
| `skills/README.md` | Diz "The workspace is not Git-initialized or project-skill-trusted"; o Git local existe desde 9/10 | H (texto) | Registro `skills/registry.json` | Atualizar frase; o produtor decide |
| `docs/MEMORY_AND_AGENTS.md`, `docs/OPERATIONS.md`, `docs/SAFETY.md` | "Seven role briefs" (o registro lista nove), "parent", "Hermes", "Git history … not changed by workspace setup" (stale) e repetição de regras do AGENTS | A, com texto a reduzir | Linkados por START_HERE e WORKSPACE | Reduzir a ponteiros (C5) |
| `agents/*.md` (briefs) | "Review/read-only role by default … closing tasks assigned to the **parent**" em seis briefs (dialogue-sound, continuity, qc, storyboard, editor, historian); `producer.md`: "parent/producer" | A, com termo antigo | Registry/bindings | Trocar "parent" por "producer" junto com a mudança no AGENTS.md |
| `workspace.json` `requiredDirectories` (`.hermes/plans`, `.hermes/skills`) | Termo e diretórios herdados do Hermes | A | `tests/test_manage.py` e `test_kling_batch.py` usam `~/.hermes/cache/scratch` | **Não renomear**; documentar só |
| `docs/archive/` e `reports/*/file-index*.json` | Fotografias de hash de momentos passados | H | Servem à verificação de integridade | Não editar |

### 12.2 Skills ligadas ao filme (`skills/registry.json`)

| Skill | Uso real no filme | Classe | Observação |
|---|---|---|---|
| `andre-time-travel` (projeto) | AGENTS.md "Session start" item 3 | A | Fonte canônica do procedimento |
| `kling-cli` | produtor (registry) e AGENTS.md | A | **Divergência:** o link `skills/kling-cli` agora aponta para `.agents/skills/kling-cli`, uma **cópia versionada no Git** (SKILL.md 40.830 bytes), diferente da fonte `~/.hermes/skills/kling-cli` (SKILL.md 20.382 bytes, mais um diretório `references/`). `skills/registry.json` ainda registra a fonte Hermes e hashes antigos. O AGENTS.md diz "do not copy vendor/profile skills here". **Qual versão é a atual: não verifiquei** |
| `film-character-continuity`, `film-dialogue-localization`, `film-editing-qc` | vários papéis (continuity, director, storyboard, dialogue-sound, editor, qc, lighting) | A | Geram os 4 avisos de "shared skill changed since linking" no `validate` |
| `grounded-citations` | papel `historian` (registry) | A | **Não está** na lista de skills do "Session start" do AGENTS.md; propor acrescentar |

### 12.3 Plugins e ferramentas fora do filme

Inventário de **plugins do Claude Code** instalados globalmente (`~/.claude/plugins/installed_plugins.json`, 13): `adobe-for-creativity`, `agent-parley`, `agent-sdk-dev`, `ai-plugins`, `claude-code-setup`, `cloudflare`, `code-modernization`, `context7`, `feature-dev`, `github`, `playwright`, `superpowers`, `typescript-lsp`.

| Item | Referências no filme (arquivos fora de `reports/`) | Classe | Observação |
|---|---|---|---|
| `agent-parley` | 1 (`PARLEY_PROTOCOL.md`) | A | Coordenação já adotada |
| `superpowers` | 2 (`STATE.md`, handoff da Fase 0), ambas só como parte do caminho `docs/superpowers/specs/` do desenho de memória | A (processo dos agentes) | Não é parte da produção do filme |
| `adobe-for-creativity`, `cloudflare`, `code-modernization`, `ai-plugins`, `claude-code-setup`, `agent-sdk-dev`, `feature-dev`, `typescript-lsp`, `playwright`, `github`, `context7` | Playwright, feature-dev, typescript: 0. Adobe: 5 arquivos (2 do plano v3 usam "adobe" como material de muro; 3 são o manual do Kling e seu handoff listando a ferramenta como opção). Cloudflare e HyperFrames: só `docs/kling-manual/15-ferramentas-nao-listadas.md`. context7: 1 menção em `review-findings.md` (**não conferi** o contexto) | D **para o filme** | Nenhuma referência a **remover do filme**. Desativar por projeto ou desinstalar global é decisão de Andre, fora desta entrega |
| Conectores de geração paga vistos na minha sessão (Kling MCP, Higgsfield, ElevenLabs, HyperFrames, Clipkit, Adobe) | Higgsfield e Adobe só como **opções listadas** em `docs/kling-manual/15-ferramentas-nao-listadas.md` e em um handoff; ElevenLabs aparece em 74 arquivos (testes de voz, D06, D14) | Kling MCP: **proibido** pelo AGENTS ("No direct HTTP/MCP bypass"); ElevenLabs: A **só com escopo próprio**; Higgsfield, HyperFrames, Clipkit, Adobe: D para o filme | Desativação é decisão do operador/Andre; nada foi configurado |
| **Baton Pass** (`baton-pass-netheremp` 0.8.0) | **0** no repositório e nos documentos do filme | D (redundante com Parley) | Plugin do Codex em `~/.codex/plugins/cache/openai-curated-remote/`; `~/.codex/config.toml` não o cita; **não consegui confirmar se está habilitado**. Oferece handoff entre agentes ("new-game", "save-state", "baton-pass", "foresight", "party-check", "hindsight"), o que sobrepõe lanes, reservas, mensagens, handoffs JSON e relatórios do Parley. **Remover a referência do filme: não há nenhuma. Desinstalar o plugin: decisão global, não proposta aqui** |

### 12.4 O que o inventário não prova

- "Sem referência no filme" não prova que o **Codex lane** ou a conversa produtora não usem o plugin; só olhei o repositório e o meu ambiente.
- Não abri o conteúdo dos arquivos de `reports/` além de procurar citações (são fotografias de hash).
- Não verifiquei se `scripts/manage.py validate` falharia ao trocar o campo `decisions` de `memory/projects.json`.
- A base fará o inventário dos links locais; os caminhos que cito acima valem para o checkout base no momento da leitura.
