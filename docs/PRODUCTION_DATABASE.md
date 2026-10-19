# Gestão nova em banco — núcleo local v1

## Escopo e autoridade

Andre solicitou um plano de gestão em banco e depois esclareceu que o conteúdo atual
não será migrado: somente a estrutura anterior serve de referência. Em seguida autorizou
prosseguir. Esta entrega implementa **a primeira etapa: núcleo relacional local e CLI**.
Não substitui ainda o contrato operacional do filme, seus hooks, o painel ou os registros
legados. Não importa dados, cadastra projetos automaticamente, executa agentes, faz chamadas
a provedores, gasta créditos, publica ou aprova conteúdo artístico implicitamente.

Fontes novas:
- `scripts/production_schema.sql`: esquema relacional v1.
- `scripts/production_db.py`: comandos transacionais e CLI, usando apenas Python 3.11+ stdlib.
- `tests/test_production_db.py`: testes com estado sintético em diretórios temporários.

Não é necessário recuperar `workspace.json` para usar este núcleo. Nenhum banco real de
operação nem credencial de operador é criado pela instalação do código ou pelos testes.

## Modelo

Projetos, identidades, vínculos de papel por projeto, tarefas, dependências, escopo e
caminhos atribuídos, versões de artefatos, entradas de atribuição, handoffs, verificações,
dependências declaradas, decisões pendentes de acompanhamento, decisões, aprovações e
eventos de auditoria têm tabelas próprias. Não existe documento JSON de workspace.

JSON na saída da CLI é apenas transporte. O banco usa JSON somente no payload/resultado
imutável dos eventos de auditoria e para reproduzir o resultado de uma requisição repetida.
Não há arquivos JSON operacionais para manter manualmente.

IDs são globais dentro do banco; usar prefixos de projeto quando necessário. Datas de
auditoria são UTC. Caminhos de artefatos são relativos ao workspace; o endereço absoluto
da raiz é apenas uma âncora de implantação, não um caminho de mídia do projeto.

## Segurança e limites

- Inicialização cria uma identidade de operador e uma credencial aleatória em arquivo
  exclusivo, modo 600. O segredo não é retornado nem incluído no histórico; o banco guarda
  somente seu SHA-256. Não leia, cole ou versione esses arquivos.
- Possuir a credencial autentica a identidade local. Não existe argumento `--actor` ou
  papel autodeclarado por operação. Só o operador cadastra identidades, projetos e vínculos.
- O produtor de um projeto gere suas tarefas, verifica/integra handoffs e registra decisões.
  Outros membros só aceitam ofertas destinadas a eles e entregam no escopo aceito.
- Aprovações exigem a credencial de operador e registram versão/hash, finalidade e motivo.
  Isso identifica o operador local; não comprova externamente que Andre aprovou, nem libera
  gasto. O operador deve executar somente decisões que tenha autoridade real para registrar.
- O dono do sistema operacional que pode ler/escrever o banco ou as credenciais pode
  contornar a aplicação. **Não é sandbox nem autenticação remota.** Permissões de pasta,
  backups e segregação de contas continuam responsabilidade operacional.
- Escopo/caminhos restringem o registro de artefatos; não bloqueiam edições feitas por
  outros programas no filesystem. Os bytes são conferidos ao aceitar entradas, registrar,
  entregar, verificar, integrar e aprovar artefatos. Não há lock dos arquivos durante leituras.
- Ausência, erro de banco ou versão de esquema desconhecida recusam a operação. Não há
  fallback para JSON nem conexão com executores pagos.

## Inicialização explícita

Exemplo para execução **pelo operador**, após revisar este núcleo. Estes comandos são
instruções; esta entrega não os executa no workspace real:

```sh
mkdir -m 700 .production-db
.venv/bin/python scripts/production_db.py \
  --db .production-db/management.sqlite3 init \
  --owner operador --credential-out .production-db/operator.credential
```

O diretório `.production-db/` é ignorado pelo Git. Banco, credenciais e backups não devem
ser criados fora dele no checkout. O comando recusa banco ou credencial já existentes.
Por padrão a raiz é este workspace; `--root` permite outro workspace na inicialização.
Todas as operações seguintes precisam da mesma raiz. Não copiar o banco para outro
workspace e apontar para arquivos diferentes sob os mesmos caminhos relativos.

Nos exemplos seguintes, definir um helper no shell evita repetir argumentos:

```sh
pdb() {
  .venv/bin/python scripts/production_db.py \
    --db .production-db/management.sqlite3 \
    --credential .production-db/operator.credential "$@"
}
pdb project-create --project filme-novo --title 'Filme novo' \
  --request-id projeto-001 --reason 'Início autorizado de projeto vazio'
pdb identity-add --user executor --credential-out .production-db/executor.credential \
  --request-id identidade-001 --reason 'Cadastro local autorizado'
pdb member-add --project filme-novo --user executor --role contributor \
  --request-id membro-001 --reason 'Executor limitado a este projeto'
pdb task-create --project filme-novo --id FN-T01 --title 'Preparar proposta' \
  --request-id tarefa-001 --reason 'Primeira atribuição'
pdb task-offer --task FN-T01 --revision 1 --to executor \
  --scope 'Preparar apenas a proposta no caminho atribuído, sem gastos' \
  --allowed-path proposals/primeira.md \
  --request-id oferta-001 --reason 'Oferta para aceite explícito'
```

Não é criado um processo executor. A credencial deve chegar ao destinatário por um canal
local seguro autorizado; não é passada a agentes automaticamente. O executor usa sua própria
credencial para `task-accept --task FN-T01 --revision 2`, com `--request-id` e `--reason`.
O retorno indica a nova revisão 3. Criar o arquivo é trabalho do executor, fora desta CLI.
Depois ele registra `artifact-add --task FN-T01 --revision 3 --id FN-A01
--path proposals/primeira.md`, novamente com request ID e motivo próprios.

Cada oferta recebe uma versão de atribuição; saídas anteriores não são adotadas por uma
nova oferta, mesmo na mesma tarefa. É necessário registrá-las explicitamente de novo sob o
escopo aceito. Oferta sem `--allowed-path` não permite cadastrar saídas. `--input <artifact-id>` repetível
fixa versões de entrada já cadastradas; `--depends-on <task-id>` em `task-create` fixa
pré-requisitos. As dependências só apontam para tarefas existentes do mesmo projeto e
não podem ser alteradas nesta versão: isso impede introduzir ciclos. Oferta e aceite
exigem dependências concluídas.

## Entrega, correção e sucessor

Fluxo de tarefas: `ready → offered → active → delivered → completed`.
O produtor retém a responsabilidade até o destinatário aceitar a oferta. Tarefas ainda
não entregues podem receber `task-block --owner ... --condition ...` e depois nova oferta.

Com a credencial do executor:

```sh
# Acrescentar os argumentos globais --db e --credential antes do subcomando.
# Exemplo de argumentos do subcomando, não uma execução automática:
# handoff-submit --task FN-T01 --revision 3 --id FN-H01 \
#   --scope 'Proposta inicial' --limitations 'Sem aceite artístico' \
#   --artifact FN-A01 --check leitura passed 'Arquivo exato conferido pelo executor' \
#   --request-id entrega-001 --reason 'Entrega para revisão'
```

`--check NAME RESULT EVIDENCE` é repetível; resultados: `passed`, `failed`, `not_run`.
São declarações do autor, não testes executados automaticamente. Ao menos uma saída e uma
verificação explícita são necessárias. `--dependency` referencia tarefas do projeto;
`--open-decision` referencia decisões que ainda exigem acompanhamento. Campos não devem
inventar evidência, execução ou aceite. A submissão não conclui a tarefa.

O produtor executa `handoff-verify --handoff FN-H01 --revision 1`, registrando no motivo
quais verificações realmente fez e quais limitações aceita. O sistema confere os hashes,
mas **não conclui se testes declarados, playback ou revisão artística são suficientes**.

Se houver falhas ou bytes alterados, `handoff-return` devolve o handoff pendente, preserva
seu histórico e reabre a tarefa para o executor aceito. Usar novos IDs de artefato/handoff
na reentrega; `artifact-add --supersedes <id>` preserva a relação entre versões. Consultar
as novas revisões antes de agir. Arquivos originais não são alterados pela CLI.

Para integrar um handoff verificado, `handoff-integrate --handoff ... --revision ...` exige
**exatamente uma** alternativa:
- `--successor <task-id>`: outra tarefa do mesmo projeto já aceita e ativa;
- `--blocker-owner <identity-id> --condition 'condição objetiva'`;
- `--closed`: etapa realmente encerrada, com justificativa no motivo.

Uma tarefa sucessora dependente da conclusão desta ainda não pode ser aceita. Nesse caso,
registrar o bloqueio com responsável e condição, concluir a entrega, então oferecer a
sucessora quando a dependência estiver satisfeita. A versão inicial preserva esse bloqueio
como evidência histórica; não oferece um dispatcher nem resolução automática de bloqueios.

Integração conclui a tarefa, mas não gera aprovação. `decision-record` registra decisão e
justificativa; `--supersedes` corrige explicitamente sem sobrescrever. `approval-record`
exige artefato, finalidade e resultado `approved|rejected`; correções têm novo ID e
`--supersedes`. Aprovações de um mesmo artefato/finalidade formam uma cadeia única; uma
correção deve apontar para a última versão. Rejeição é permitida mesmo que o arquivo tenha
sumido ou mudado, para não impedir revogação; aprovação positiva exige bytes íntegros.
Consultas retornam o histórico inteiro, não apenas a decisão vigente.

## Concorrência, consultas e backup

Toda mutação exige `--request-id` único por identidade e `--reason` não vazio. Repetir o
mesmo comando/conteúdo/ID retorna o resultado anterior sem duplicar; reutilizar ID com outro
conteúdo falha. Provisionamento de credencial é exceção: repetição é recusada para não
substituir segredos. Uma interrupção nesse provisionamento pode deixar um arquivo órfão;
conferir o cadastro antes de qualquer recuperação manual, sem sobrescrever credenciais.

Transações `BEGIN IMMEDIATE` serializam mutações. Mudanças de tarefas/handoffs exigem a
revisão esperada; conflito exige recarregar, não repetir cegamente. Eventos de mudança e
estado são confirmados na mesma transação; auditoria não admite UPDATE/DELETE pela API.

```sh
pdb query --project filme-novo --kind tasks
pdb query --project filme-novo --kind handoffs
pdb query --project filme-novo --kind events
pdb backup --output .production-db/backup-001.sqlite3
```

Outras consultas: `artifact_versions`, `decisions`, `approvals`, `task_dependencies`,
`task_allowed_paths`, `task_inputs`, `handoff_artifacts`, `handoff_checks`,
`handoff_dependencies`, `handoff_open_decisions`. Não há consultas arbitrárias de SQL nem
exportação de hashes de credenciais.

Backup usa a API de snapshot SQLite e recusa sobrescrita; inclui hashes de identidade e
portanto deve ser privado. Credenciais e arquivos de evidência precisam de backup separado.
Para ensaiar restauração: abrir uma cópia do snapshot com a mesma raiz e credencial,
conferir `PRAGMA integrity_check`, `PRAGMA foreign_key_check` e consultar tarefas/eventos.
Nunca substituir silenciosamente o banco ativo. Relocação da raiz e rotação/revogação de
credenciais ainda não têm comando; exigem etapa própria antes de operação multiusuário.

## Verificação e próximo estágio

```sh
.venv/bin/python -m unittest discover -s tests -p test_production_db.py -v
```

Os testes criam apenas bancos/credenciais temporários. Cobrem fluxo, isolamento,
autorização, concorrência, idempotência, preservação, hashes e restauração.

Etapa entregue: núcleo local, ainda **não é corte de produção**. O produtor mantém a
próxima etapa: revisar este desenho e atribuir integração do painel/CLI de agentes,
identidades operacionais (incluindo revogação), gates e jobs/despesas antes de ativar o
novo sistema como fonte canônica. Nenhum executor dessa etapa foi iniciado ou aceitou
atribuição nesta entrega. O painel D1 e os registros antigos continuam intocados; não
há sincronização ou escrita dupla criada por este núcleo.
