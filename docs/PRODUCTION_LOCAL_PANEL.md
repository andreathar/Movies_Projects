# Painel local e API de agentes — gestão nova

## Estado desta etapa

Implementação local ligada ao banco de `docs/PRODUCTION_DATABASE.md`, sem migração,
importação, fallback ou sincronização com JSON/D1. O painel oferece formulários de
operações e tabelas de consulta; não exige editar documentos JSON de gestão.

Arquivos:
- `scripts/production_web.py`: painel HTML sem JavaScript, sessão de navegador e API.
- `scripts/production_client.py`: cliente de agentes via API, sem proxies ou redirects.
- `scripts/production_db.py`: descoberta autorizada de projetos e snapshots consistentes.
- `tests/test_production_web.py`: integração sintética, sem abrir portas.

O painel anterior em `sites/movies-demandas` é um repositório separado com trabalho
concorrente. Não foi modificado, inicializado, publicado ou conectado ao novo banco.
Sua estrutura mistura D1, pacotes importados e JSON de revisão; sua implantação remota
não acessa o SQLite e filesystem desta máquina. Por isso esta etapa usa uma superfície
local separada. Para projetos novos, somente o banco novo deve ser usado; não cadastrar
os mesmos dados também no painel legado. Este documento não altera contratos canônicos
de produção de episódios nem afirma que o legado já foi desativado globalmente.

## Ativação local verificada

Após Andre autorizar prosseguir com o teste de navegador e ativação, foi inicializado
um banco operacional **sem projetos ou dados herdados**, com uma identidade bootstrap
`operador-local`. O processo local foi iniciado em `http://127.0.0.1:18741/` e a porta
18741 registrada no inventário canônico de serviços da máquina.

- Banco: `.production-db/management.sqlite3` (modo 600).
- Credencial do operador: `.production-db/operator.credential` (modo 600); não mostrar
  seu conteúdo em chat/logs. Uso direto pelo usuário somente no campo de senha local.
- Diretório runtime: `.production-db/` (modo 700, ignorado pelo Git).
- PID observado na ativação: 4036726; PID de execução em `.production-db/server.pid`.
- Log privado: `.production-db/server.log`, sem log de acesso ou credenciais.
- Teste: HTTP 200 na tela de login, integridade SQLite `ok`, zero projetos, tarefas,
  handoffs, decisões e aprovações. Somente uma identidade e o evento bootstrap.

Esse é um processo local temporário iniciado via `nohup`, não um serviço instalado;
não há autostart, daemon de sistema ou schedule. Disponibilidade futura deve ser
conferida: o processo não é garantido após reinício/logout da máquina. Para interromper,
primeiro confirmar que o PID registrado ainda corresponde a `scripts/production_web.py`
neste workspace (incluindo `/proc/<pid>/cwd`), então enviar SIGTERM somente a esse
processo. Nunca usar um PID antigo sem verificar, nem encerrar outros serviços.

## Iniciar explicitamente após interrupção

As instruções abaixo são para iniciar se o processo **não estiver rodando**; não executar
`init` de novo nem substituir banco/credencial existentes.

1. Inicializar banco e identidades pela CLI descrita em `docs/PRODUCTION_DATABASE.md`.
   Nada é semeado automaticamente. Cadastro de identidade gera somente uma credencial
   local privada, sem disponibilizá-la a agentes automaticamente.
2. **Consultar o registro canônico de portas e serviços e reservar uma porta livre** antes
   de iniciar. Nenhuma porta de operação foi escolhida ou reservada nesta entrega.
3. Executar manualmente, substituindo `PORTA_LIVRE` pela porta aprovada:

```sh
.venv/bin/python scripts/production_web.py \
  --db .production-db/management.sqlite3 --port PORTA_LIVRE
```

4. Abrir exatamente `http://127.0.0.1:PORTA_LIVRE/` no navegador. O endereço `localhost`
   não é um alias aceito pelo controle de Host desta versão.
5. Entrar com **a sua própria** credencial local no campo de senha do painel. A regra de
   não colar credenciais em chat, logs, prompts ou repositórios continua válida. Este campo
   é apenas para entrada direta do usuário no formulário local; o assistente não deve ler
   credenciais reais para preencher a página. Não usar tokens em URL, argv ou localStorage.

O servidor só vincula `127.0.0.1`. O uso de HTTP é deliberadamente restrito ao loopback;
**não é servidor de produção, acesso LAN ou implantação Cloudflare**. Não publicar por
proxy/túnel nem remover essa restrição. Outros usuários/processos da mesma máquina não
são isolados pelo loopback; proteger arquivos e credenciais no sistema operacional.

## Fluxo no painel

Sem projetos, o painel mostra o estado vazio e oferece criação explícita. Após criar,
escolher o projeto na lista para ver tarefas, handoffs, versões, decisões, aprovações,
evidências e eventos. Cada operação é um formulário próprio; os campos usam IDs e revisões
exibidos nas consultas. Para listas, informar um item por linha, sem JSON.

Exemplo de declaração de verificação em handoff:

```text
leitura | passed | Comparei o arquivo exato com a entrega
playback | not_run | Esta atribuição não inclui vídeo
```

Isso registra declarações, não executa testes. A revisão real continua necessária.

Sequência: criar tarefa → oferecer com escopo/caminhos/entradas → destinatário entrar com
sua credencial e aceitar → registrar versão do arquivo → entregar → produtor verificar ou
devolver → integrar com sucessora aceita, bloqueio responsável ou etapa encerrada.

Um destinatário precisa ter vínculo no projeto antes da oferta, inclusive o operador se
pretender executar a tarefa. Não compartilhar a credencial do operador para simular aceite.
O banco não concede papéis porque um formulário esteja visível: todos são validados pelo
núcleo. Os formulários de aprovação não liberam gasto ou certificam identidade artística.

Cada formulário carrega um ID de requisição para impedir duplicação no reenvio. Para uma
nova operação, recarregar o painel. Conflito ou falha é recusado sem commit; recarregar o
estado e revisar antes de tentar novamente. Não há edição genérica de estado das tarefas.

## API e cliente de agentes

Todas as chamadas exigem `Authorization: Bearer <credencial>` da identidade atribuída.
A API não usa cookies, não tem CORS e recusa requisições com Origin de navegador. JSON
existe apenas no transporte HTTP e nos payloads de auditoria já previstos pelo núcleo.

| Método / caminho | Resultado |
| --- | --- |
| `GET /api/projects` | Projetos acessíveis à identidade |
| `GET /api/snapshot?project=ID` | Projeções do projeto na mesma transação de leitura |
| `GET /api/query?project=ID&kind=tasks` | Consulta específica permitida |
| `POST /api/commands` | Comando permitido e auditado |

Envelope do POST: `command`, `args`, `request_id`, `reason`, sem outros campos. As
operações são as mesmas oferecidas nos formulários. Inicialização, criação de identidades,
backup, SQL arbitrário e escolha de banco/raiz/credencial por request são proibidos.
Esses controles permanecem na CLI local do operador.

O agente pode usar a CLI original diretamente no mesmo filesystem ou este cliente HTTP:

```sh
.venv/bin/python scripts/production_client.py \
  --url http://127.0.0.1:PORTA_LIVRE \
  --credential .production-db/executor.credential projects

.venv/bin/python scripts/production_client.py \
  --url http://127.0.0.1:PORTA_LIVRE \
  --credential .production-db/executor.credential snapshot --project filme-novo

# Objeto efêmero no stdin: protocolo, não arquivo de gestão.
printf '%s' '{"task":"FN-T01","revision":2}' | \
  .venv/bin/python scripts/production_client.py \
    --url http://127.0.0.1:PORTA_LIVRE \
    --credential .production-db/executor.credential execute task-accept \
    --request-id aceite-001 --reason 'Aceite do escopo oferecido'
```

Não há auto-retry. Após timeout, conferir estado e usar o mesmo ID/conteúdo se for preciso
recuperar a resposta, sem inventar um novo ID e duplicar efeitos. Não há executor de
agentes, submissão de mídia ou integração com serviços pagos.

## Controles e limites

- Host exato para reduzir DNS rebinding; vínculo somente no loopback IPv4.
- Navegador: Origin exata, CSRF por sessão, expiração fixa de 30 minutos, logout e limite
  de tentativas de login. **Não há cookies**: cookies de loopback seriam enviados também a
  serviços vizinhos em outras portas. O identificador de sessão segue somente em campos
  ocultos de formulários POST para a mesma origem. Navegação de projetos também usa POST;
  GET sempre mostra login. Não usar URL/storage para guardar sessão.
- Credencial fica somente na memória da sessão do servidor após o login, não no HTML,
  URL ou log de acesso. O handle temporário e CSRF ficam nos formulários e são sensíveis;
  não compartilhar HTML autenticado. Não há logs de requisição, persistência de sessão
  ou script de terceiros.
- Escapamento de HTML, CSP sem scripts/frames, no-store e Referrer-Policy same-origin.
  A política no-referrer foi substituída após teste real: ela produz Origin:null em POSTs
  nativos do Chromium, impedindo login. A validação de Origin continua exata.
- Corpo limitado a 64 KiB; sem transfer-encoding, content-length duplicado ou corpo truncado.
- Permissões, hashes, transações, revisões e idempotência são os do mesmo núcleo SQLite.
- Snapshot por projeto é consistente; seleção de projeto/autenticação são verificações
  separadas e não prometem um snapshot global de todos os projetos.
- Não há paginação de eventos, revogação/rotação de credenciais nem autenticação remota.
  Painel é uma primeira superfície local, não um substituto de infraestrutura multiusuário.
- Testes de aplicação/adaptador HTTP em memória e teste real com Chromium headless.
  O teste de navegador usa banco e credenciais sintéticos temporários, processo loopback
  encerrado ao final e evidência final em `.production-db/browser-check-v4/` (inclui versões
  de ferramentas, hashes dos scripts e screenshots). A porta 18742 é reservada para QA
  temporário; não é o painel operacional.
  Foram verificados teclado no login, desktop, mobile sem overflow, identidades separadas,
  fluxo completo e API no mesmo banco. Não houve playback de mídia nem aceite artístico.

## Repetir QA sem tocar no banco operacional

Após checar a porta reservada 18742, executar com o módulo Playwright já instalado:

```sh
.venv/bin/python scripts/production_browser_check.py \
  --port 18742 --playwright-module /CAMINHO/INSTALADO/playwright \
  --output .production-db/browser-check-NOVA-REVISAO
```

O destino deve ser novo. O runner Linux cria credenciais sintéticas privadas em um
workspace temporário, exige um nonce de execução, recusa symlinks de credenciais e URL
fora do loopback, usa criação exclusiva da proposta e encerra servidor/browser ao final.
Em timeout, encerra também os grupos descendentes conhecidos do Chromium. O teste não
aceita caminho de credencial operacional. Não captura call logs de Playwright que possam
conter campos de senha. Versões e hashes ficam no relatório `result.json` de QA, não em
um novo registro operacional de projeto.

## Próximo responsável / ativação

O assistente desta conversa implementou painel/API/client como sucessor do núcleo.
A ativação local de infraestrutura está concluída, com banco vazio e bootstrap local;
não foi criada identidade de Andre nem distribuída credencial a agentes. A próxima ação
pertence ao usuário/produtor: entrar com a credencial local e cadastrar o primeiro projeto
novo e suas identidades/atribuições. Nenhum projeto, aprovação ou permissão antiga foi
herdado. O assistente não abriu ou aceitou uma atribuição de produção de filme.

Se a operação desejada for remota, o bloqueio pertence ao produtor: definir hospedagem,
autenticação/revogação e localização do banco antes de expor qualquer endpoint. Não basta
apontar o painel Cloudflare para localhost, espelhar D1 ou recriar os JSON antigos.
