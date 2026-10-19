# Handoff — painel local e API de agentes

## Escopo e autorização

Infraestrutura greenfield do workspace, sem episódio/ID de board. Assistente implementador
desta conversa; autorização direta de Andre para prosseguir após a entrega do núcleo e
indicação da próxima etapa de painel/agentes. Sem migração de conteúdo, publicação,
gastos ou alterações de contrato canônico de filme.

A atribuição de implementação desta etapa foi aceita/executada nesta conversa. Os campos
abaixo seguem a estrutura do template `shared/templates/agent-handoff-v2.json` em Markdown,
sem adicionar outro JSON operacional. A entrega não implica implantação ou aprovação.

## Fontes e versões

| Arquivo | SHA-256 base | SHA-256 entregue |
| --- | --- | --- |
| `scripts/production_db.py` | `06a08a5eb8b066de52a0faf9af42fbcfe857cf7ffe3d462df8670e1a80206594` | `705931f7cdbd90332be92f44dd025949dad0b028589876dcfd72152e08eae51b` |
| `docs/PRODUCTION_DATABASE.md` | `e8ce3a296cfd8de391f95ac5a0b0f5dd0f524291a70dc3280c1aa7b40dcfea17` | `9ed124f972a25bb1e87e6d6e5f49dbc83470d9d7bf1161be0690cce6042a0f91` |
| `scripts/production_web.py` | novo | `5279dd4f95416962d6d1e4863cea2d9fb80afbf5bf9ef390ce824155319e9d23` |
| `scripts/production_client.py` | novo | `a2e72c4b480b77117737758d454e03f55a163a1653cfa753b6ec8de6d135c177` |
| `tests/test_production_web.py` | novo | `10aa5613cf1363c74c443086c4e10cc8d58c8969e57dcc04de79e1389372a8e3` |
| `docs/PRODUCTION_LOCAL_PANEL.md` | novo | `56f4b566ba860f482b615b2ca231760e353096773fbf3410aa06941461988f89` |

Este handoff é novo. O handoff anterior permanece histórico, inclusive seus hashes de
versões anteriores. Nenhum commit, stage, merge ou push foi realizado nesta etapa.

## Entrega / evidência

- Painel HTML com formulários próprios, consultas e estado inicial realmente vazio.
- API com bearer por identidade, sem SQL arbitrário, caminhos de credencial/banco por
  request, provisionamento remoto ou fallback para legado.
- Cliente de agentes com leitura privada da credencial, proxies/redirects desabilitados
  e nenhuma repetição automática.
- Projetos acessíveis filtrados por identidade; snapshot por projeto em uma transação.
- Sessões temporárias sem cookies: handles apenas em POST, Origin exata e CSRF.
- Núcleo mantém todas as permissões, hashes, revisões e idempotência. Schema não mudou.
- Investigação read-only do painel legado revelou repositório separado, 95 entradas
  concorrentes e dependência de D1/importações antigas; por isso nenhum arquivo dele foi
  editado e a nova superfície é exclusivamente local. O painel publicado não foi conectado.

## Verificações realizadas

- 21 testes do núcleo passaram depois da mudança de consultas.
- 16 testes novos finais passaram: integração UI/API/client, isolamento, idempotência,
  revisões, CSRF, ausência de cookies, sessão expirada, timeout sem retry, validação,
  framing HTTP, fluxo completo e snapshot com commit concorrente em WAL.
- Testes HTTP foram feitos em memória com socket falso, sem listener ou processo servidor.
- Suíte completa executada: **335 testes, 4 falhas e 21 erros**. Permanecem referências
  ausentes do legado: `workspace.json`, `START_HERE.md`, `skills-lock.json`.
- `manage.py validate`, `resume`, `lint`: falharam pela ausência de `workspace.json`.
  Nenhum dado antigo foi reconstruído para fazê-los passar.
- `git diff --check`: passou.
- Duas revisões independentes read-only: primeira encontrou cookies compartilhados entre
  portas e corpo truncado; ambos corrigidos. Segunda não encontrou bloqueadores e pediu
  fortalecer o teste de framing. Teste fortalecido: comando autenticado válido truncado
  não chama `Application.handle` e não altera o banco; suíte web final passou.

## Preservação / limites

Não houve leitura de credenciais reais, banco operacional criado, porta reservada/aberta,
serviço instalado, job pago, chamada a provedor ou alteração de registros do filme.
Há exclusões concorrentes em `projects/andre-time-travel/docs/assistant-reviews/` e
alterações no sub-repositório `sites/movies-demandas`; não pertencem a esta entrega e
não foram revertidas, incorporadas ou atribuídas ao assistente.

Sem inspeção visual ou teste real de teclado no navegador. Sem rotação/revogação de
credenciais, paginação, acesso remoto, integração Cloudflare ou desligamento global do
legado. O servidor stdlib é um adaptador exclusivamente local, não servidor de produção.

## Fechamento / sucessor

Etapa técnica de painel/API/client concluída. Revisão de implantação e aceite operacional
pendentes. Responsável pelo próximo estágio: produtor/coordenador; nenhum novo executor
foi iniciado ou aceitou atribuição de ativação por este handoff.

Bloqueio específico para ativação: produtor define identidades operacionais, consulta e
reserva uma porta livre no registro canônico e conduz o teste de navegador local antes
de decidir o corte de gestão. Não exige recuperar JSON antigos. Se precisar de acesso
remoto, produtor deve definir hospedagem/autenticação/revogação antes de expor o serviço.

Detalhes de operação e exemplos: `docs/PRODUCTION_LOCAL_PANEL.md`.
