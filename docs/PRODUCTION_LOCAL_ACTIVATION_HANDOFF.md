# Handoff — teste de navegador e ativação local

## Escopo / autorização / sessão

Infraestrutura greenfield do workspace, sem episódio ou tarefa de produção de filme.
Andre autorizou prosseguir após a etapa painel/API indicar teste no navegador e ativação
local como sucessor. O assistente desta conversa aceitou/executou essa atribuição.
Sem importação, publicação remota, gasto ou alteração de gates canônicos do filme.

Registro estrutural equivalente ao template `shared/templates/agent-handoff-v2.json`,
em Markdown; não cria outro JSON de gestão de projeto.

## Resultado

- Painel operacional local: `http://127.0.0.1:18741/`, HTTP 200 confirmado.
- Processo observado: PID 4036726, listener **somente 127.0.0.1:18741**.
- Banco novo: `.production-db/management.sqlite3`, integridade `ok`, permissão 600.
- Identidade bootstrap: `operador-local`, não identidade pessoal verificada de Andre.
- Credencial gerada: `.production-db/operator.credential`, modo 600, nunca lida pelo
  assistente nem exibida em logs, chat ou screenshots. Diretório runtime modo 700.
- Contagem verificada logo após ativação: zero projetos, tarefas, handoffs, decisões e
  aprovações; uma identidade e um evento bootstrap. Sem conteúdo antigo ou fictício.
- Processo iniciado via nohup, sem autostart/serviço instalado. PID/log privados em
  `.production-db/server.pid` e `.production-db/server.log`. Disponibilidade não garantida
  após reinício da máquina; não reutilizar PID antigo sem verificar processo/workspace.
- Registro externo de portas atualizado: 18741 operacional; 18742 reservada para QA
  sintético temporário, sem listener ao concluir. Nenhum outro serviço foi interrompido.

## Arquivos / hashes SHA-256

| Arquivo | Base | Entregue |
| --- | --- | --- |
| `scripts/production_web.py` | `5279dd4f95416962d6d1e4863cea2d9fb80afbf5bf9ef390ce824155319e9d23` | `e73f9eafafeb6a1d8ad850917c88e493d263e6d343671e1ab34e3d5f4172555f` |
| `tests/test_production_web.py` | `10aa5613cf1363c74c443086c4e10cc8d58c8969e57dcc04de79e1389372a8e3` | `27ba5f0953cdcdf1a3dea21706b5e2bd4f5189e8df6315129287f43b39a4780c` |
| `docs/PRODUCTION_LOCAL_PANEL.md` | `56f4b566ba860f482b615b2ca231760e353096773fbf3410aa06941461988f89` | `d6471faeb056eae70233da2abbabdc2b9f06932c8409b4274ab66d03d4de355c` |
| `scripts/production_browser_check.py` | novo | `1b9f70bdb66120e2ea81576994cd77d4401b00e47ba39334236c7f8260966d23` |
| `scripts/production_browser_smoke.cjs` | novo | `dde4f0cff80c4ba282cb721c37f3ffe39e0bcbd7ada01209212636564e500af6` |
| `tests/test_production_browser_runner.py` | novo | `2a652c2e27d85e29a72dac3292da74443b987d2614edd1bc06ca204a91a85463` |

Configuração externa permitida pela rotina port-guard:
`/mnt/data/Projects_SSD/docs/ports-and-services.json` após:
`26414aa1ce65c790695910881564d29e6fc9fef0a43dbf79f31cde54eba89df5`.
Hash base desse inventário não foi coletado; foi preservada a lista anterior de quatro
serviços e acrescentadas apenas as entradas Movies. Esta configuração de máquina não
é JSON de gestão de filme. Este handoff também é novo.

## Testes / inspeções / correção

Teste real com Chromium headless em workspace temporário e credenciais sintéticas
separadas. Evidência final: `.production-db/browser-check-v4/result.json`, hash
`d2dcaba4020d39361fc0ff4b24a70a1b5b5060e5db1c8cfff66bfc2b4e99300f`.
Versions: Playwright 1.61.1, Chromium 149.0.7827.55, Node v24.18.0, Python 3.11.9.

15 verificações passaram: login por teclado, estado vazio, desktop, mobile sem overflow,
sem cookies/storage, executor distinto, aceite explícito, artefato, handoff, verificação
pelo produtor, integração fechada, mesma leitura pela API, nenhuma aprovação implícita,
nenhuma credencial refletida e logout. Screenshots de login/estado vazio desktop/mobile
e conclusão sintética guardados no mesmo diretório privado. Login desktop e estado vazio
desktop/mobile foram também inspecionados visualmente pelo assistente. Sem playback de
mídia ou aceite artístico.

O primeiro teste de navegador revelou que `Referrer-Policy: no-referrer` gera
`Origin: null` no POST nativo do Chromium e bloqueia login com 403. Corrigido para
`same-origin`; validação de Origin exata mantida. Regressão adicionada. Os relatórios
anteriores v1/v2 registram falha; v3 confirmou a correção; v4 confirmou o runner reforçado.

Revisão read-only independente apontou proteção insuficiente de fixture, possível browser
órfão em timeout e metadados insuficientes. Corrigidos: URL loopback, raiz temporária com
nonce do orquestrador, rejeição de symlinks/chaves públicas, criação exclusiva da proposta,
limpeza de grupos descendentes Linux e relatório com versões/hashes. Três testes unitários
de cleanup passaram. Não houve segunda revisão independente depois desses reforços.

Verificação final:
- **338 testes stdlib passaram**, incluindo 21 do núcleo, 16 da UI/API e 3 de cleanup.
- `manage.py validate`: passou; `manage.py resume`: passou.
- `manage.py lint`: ainda falha por hash divergente de `.serena/project.yml` e arquivos
  ausentes em `agents/generated/` referenciados pelo handoff antigo
  `2026-10-17-coordinator-skills-readiness-repair-v1.json`. Sem correção fora de escopo.
- `git diff --check`: passou.
- `ss`: somente listener operacional 18741; QA 18742 encerrado.

Os arquivos de legado antes ausentes reapareceram por trabalho concorrente, permitindo a
suíte geral passar. O assistente não restaurou nem importou esses dados. Alterações em
`scripts/manage.py`, README/START_HERE, skills-lock, workspace e no sub-repositório do
painel legado não pertencem a esta entrega. Nada foi staged, commitado, mergeado ou enviado
por esta sessão.

## Fechamento / sucessor

Etapa de infraestrutura local: concluída. Sem sincronização com D1/JSON, sem projeto novo
cadastrado automaticamente, sem credencial distribuída a agentes e sem executor de filme.

Próximo responsável: usuário/produtor. Condição objetiva para iniciar produção: entrar
com a credencial local, cadastrar o primeiro projeto novo e definir identidades/escopos.
Aguardando esse primeiro cadastro; não há atribuição de filme aceita ou iniciada pelo
assistente. O banco novo não recebe permissões/aprovações antigas.

Acesso remoto continua bloqueado até decisão de hospedagem, autenticação/revogação e
localização do banco. Não expor este servidor stdlib por túnel ou proxy.
