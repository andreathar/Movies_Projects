# Refresh explícito dos snapshots — 2026-10-12

## Resultado e escopo

Atualizados somente os dois snapshots do frontend, usando cópias byte a byte dos exportadores existentes em uma pasta isolada desta tarefa. As fontes reais foram lidas da base Movies, conferidas antes/depois da geração e novamente antes/depois de cada substituição. Nenhuma divergência concorrente foi detectada entre os 136 arquivos protegidos da base e os 131 arquivos de frontend acompanhados. Os demais arquivos acompanhados foram preservados.

Base Git: `2a39a07b2072a4f96664ba6a10e4ac289e665f31`. Frontend Git: `dfb945f3aaaf5aaac20ed323cda66dd26d047bb9` (repositório independente, com mudanças preexistentes preservadas).

| Arquivo | SHA-256 final | Versão do conteúdo |
|---|---|---|
| production.json | `f228e6cb0491dd6b9e1b7b1f00b65efd6a9c876fe157f8c1c1f3e0941d5e1ab7` | `546a23649552d3dcd60c47308a705a7fa5227b78c42a1d79235eafe7545359d2` |
| workspace-reference.json | `945d194f2bb4db1fc740879b822bc0804318b00d3220852c95410b4098973d7f` | `08e7fc023c044e60c1c8251645375e2aadf90e0cbb69ee8060f014312fe46649` |

- `production.json`: apenas `collectedAt` e `provenance.repositoryHead` mudaram. As 12 fontes e o conteúdo de produção continuam iguais; os cinco encontros, roteiro, proposta visual e aprovações mantêm seus significados.
- `workspace-reference.json`: atualizaram-se coleta/proveniência, hashes de registry/catálogo/skill Kling e descrição/hash da entrada `kling-cli`. O texto chinês veio da fonte atual e foi mantido sem tradução. As outras skills, papéis e adaptadores permaneceram iguais.
- A referência Git dos dois pacotes agora é `2a39a07`; ela identifica a base, e os hashes em `sources` identificam as entradas exatas. Um futuro commit exigirá nova avaliação de frescor mesmo se o conteúdo não mudar.

## Verificação efetivamente executada nesta etapa

- `scripts/agent_catalog.py --check`: OK, 7 arquivos, `changed: []`; ativação continua pendente.
- Ambos os exportadores executados na cópia isolada com a raiz Movies explícita; ambos `--check` e `check-data` passaram ali e no checkout real após a substituição.
- 15 testes de modelo do frontend: passaram, incluindo preservação de demandas/comentários e reimportação idempotente, usando objetos sintéticos em memória.
- ESLint e TypeScript: passaram na cópia isolada idêntica das fontes do site.
- Build pelo helper instalado Sites `build-site.mjs`: passou; prebuild `check:data` e as cinco fases Vinext concluíram. Artefatos de build ficaram na tarefa.
- 24 testes stdlib de gestão e 8 de catálogo: passaram. A suíte completa de 92 testes não foi repetida; este registro não reaproveita o resultado anterior como se fosse novo.
- Os quatro testes de exportação que criam repositórios/commits sintéticos não foram repetidos. Os exportadores reais, checks de frescor e verificação reversa do patch foram exercitados.
- Patch incremental dos snapshots: `git apply --reverse --check` passou. Nenhum patch reverso foi aplicado.

Comandos, resultados, hashes dos logs, hashes das entradas preservadas e versões antes/depois estão em [checks](2026-10-12-frontend-snapshots-refresh-checks.json). Logs locais e backups: `/home/athar/Documents/Codex/2026-10-11/task-2/implementation/snapshot-refresh-20261012`. O fechamento de lint/validate/handoff é registrado separadamente em `final-verification.json` nessa pasta, após a criação do handoff; não se declara sua execução antecipadamente neste documento.

## Histórico, ownership e próxima ação

Criado `2026-10-12-agent-catalog-frontend-v4.json`, supersedendo v3 porque os hashes dos dois snapshots mudaram. v2 e v3 permanecem byte a byte preservados. O v4 revalida os hashes dos 44 caminhos herdados, sem reeditar declarações históricas ou fingir nova revisão semântica das entregas anteriores. Seus checks descrevem somente esta etapa.

Responsável por esta entrega: Codex delegado, contribuição limitada de metadados/frontend. Próximo responsável: produtor da conversa principal, que deve revisar o diff e o handoff. Aceite do produtor e ingestão não foram registrados. Não se altera STATE/board para declarar integração que ainda não ocorreu. A etapa local de refresh está concluída; publicação e importação são ações posteriores com escopo próprio.

## Limites de sincronização

O site publicado não foi acessado, atualizado nem verificado nesta etapa. Nenhuma publicação, commit, push, deploy, reinício, instalação ou chamada Kling foi feita. Nenhum banco D1, demanda, comentário ou importação persistida foi lido ou escrito.

A referência de organização/skills só chegará à instância publicada após publicação autorizada de uma versão com esses arquivos. Produção já persistida exige revisão/importação explícita pelo fluxo do site; o frontend não sobrescreve demandas e comentários ao importar. Neste refresh o conteúdo de produção não mudou, portanto não há novas decisões/estados para importar. Build local válido não comprova estado publicado ou sincronização automática.

## A/B — proposta preliminar preservada, sem cotação ou autorização

Nenhuma especificação, script, skill ou aprovação Kling foi editada. `paidGenerationBatchApproved` continua `false`. Os handoffs Kling/v3 continuavam pendentes de revisão/ingestão no baseline. Referência: `projects/andre-time-travel/07_generations/plans/2026-10-12-kling-otimizacao/ab-teste-resolucao-modelo.json` e `docs/kling-manual/12-custos-e-ledger.md`; nenhuma capacidade ou preço ao vivo foi consultado.

| Variante básica | Configuração registrada | Estimativa documental, não cotada |
|---|---|---:|
| AB-01 | Kling `kling-video-v3_0_turbo`; 1 vídeo, 5 s, 1080p | 50 créditos |
| AB-02 | Kling `kling-video-v3_0`; 1 vídeo, 5 s, 1080p; Element Andre; áudio/multishot false | 40 créditos |

Soma estimada: 90 créditos; não é teto aprovado. APR real, preço/cobrança aplicável e teto formal continuam pendentes. Os placeholders de autorização não foram substituídos. AB-03/04 opcionais não fazem parte desta proposta básica; motion control fica separado.

Material previsto: o mesmo `02_references/keyframes/andre/KF-galileo-listening.jpg`, texto do prompt e, em AB-02, referência ao Element Andre já existente. Objetivo: comparar nitidez/pele, estabilidade da identidade, artefatos de movimento e custo; PILOT-01/720p serve apenas como referência histórica.

Pendências antes de uma eventual autorização:
1. AB-01 promete silêncio e usa marcador de Element, mas o schema salvo de Turbo não declara `enable_audio` nem `elements`, e o spec não vincula o Element. Resolver a incompatibilidade de texto/parâmetros sem presumir capacidade.
2. Os dois novos vídeos são 1080p; muda também o uso de Element. Este par não isola efeito da resolução. A afirmação de que resolução explica a diferença percebida continua hipótese, não conclusão experimental.
3. Os custos derivam de tabela com conversão inferida; confirmar a cobrança aplicável antes de fixar o teto. Nenhum saldo antigo é saldo ao vivo.
4. Critério proposto de parada: no máximo os dois jobs definidos, um por vez; não reenviar resultados incertos; parar diante de falha, cobrança incerta ou orçamento incompatível. Isso precisa constar do pedido revisado, sem conceder retries ou gasto.
5. Aceite de resultado exige playback e revisão de Andre; likeness/voz e aceite final mantêm gates próprios.
6. Motion control referencia movimento de 30 s, mas o orçamento usa aproximadamente 5 s/45 créditos. Duração e custo precisam de revisão separada; não juntar ao A/B de 90 créditos.

## Arquivos desta entrega

Modificados: `sites/movies-demandas/data/production.json`, `sites/movies-demandas/data/workspace-reference.json`.

Criados: este relatório, `reports/2026-10-12-frontend-snapshots-refresh-checks.json`, `projects/andre-time-travel/agents/handoffs/2026-10-12-agent-catalog-frontend-v4.json`.

Backups, patch incremental, logs e cópia de build são evidências locais da tarefa; não integram a publicação. Rollback futuro exige conferir os hashes atuais e preservar mudanças concorrentes, usando o patch incremental apenas após revisão.
