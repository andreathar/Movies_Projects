# Handoff — núcleo greenfield de gestão v1

## Escopo / sessão

- Episódio: nenhum; infraestrutura de workspace, sem herdar o filme anterior.
- Papel: assistente implementador desta conversa, não produtor canônico de um filme.
- Autorização: pedido direto de gestão em banco; esclarecimento de Andre para começar do
  zero, preservando somente estrutura como referência; autorização subsequente para prosseguir.
- Parent task: nenhum ID atribuído; não foi inventado ID de board.
- Formato: campos operacionais equivalentes ao template `shared/templates/agent-handoff-v2.json`,
  registrados em Markdown para não introduzir outro documento JSON de gestão.

## Entrega e hashes SHA-256

| Arquivo | Hash após entrega |
| --- | --- |
| `scripts/production_db.py` | `06a08a5eb8b066de52a0faf9af42fbcfe857cf7ffe3d462df8670e1a80206594` |
| `scripts/production_schema.sql` | `e56467f9cf6932a0b2a3cbb45bd1c6e1c80ea76024ea1a047a6159a0679ffecd` |
| `tests/test_production_db.py` | `ed5d90e6d1048ba4d10eebc0f77e2d916fc715ed3a17029ff46b98dff7efdc3c` |
| `docs/PRODUCTION_DATABASE.md` | `e8ce3a296cfd8de391f95ac5a0b0f5dd0f524291a70dc3280c1aa7b40dcfea17` |

Esses quatro arquivos são novos, sem versão anterior. `.gitignore` recebeu somente uma
regra `.production-db/` e seu comentário, sem modificar outras regras. Este handoff também
é novo. Nenhum arquivo concorrente foi incluído, staged, revertido ou commitado.

Entregue: SQLite local, CLI transacional, papéis, ofertas/aceites, atribuições versionadas,
artefatos com hashes, handoffs e devoluções, decisões, aprovações encadeadas, auditoria,
idempotência e snapshot. Sem dependências Python externas.

## Verificações executadas

- Testes específicos finais: **21 passaram**, execução via
  `.venv/bin/python -m unittest discover -s tests -p test_production_db.py -v`.
- Suíte stdlib completa: **317 testes, 4 falhas e 21 erros**. Os erros dependem do
  `workspace.json` ausente; falhas também incluem referências antigas ausentes em skills,
  `START_HERE.md` e `skills-lock.json`. Não declarar workspace válido.
- `manage.py resume`: falhou com `FileNotFoundError` para `workspace.json`.
- `manage.py lint`: status error por filme ativo indisponível, mesmo arquivo ausente.
- `git diff --check`: passou. Arquivos novos também foram exercitados pelos testes Python.
- Revisão read-only independente por reviewer: identificou três brechas. Corrigidas com
  regressões: vínculo de saída à versão da oferta, rejeição mesmo sem arquivo, cadeia
  única de aprovações. As correções passaram nos testes finais; não houve segunda revisão
  independente após essas correções.
- Restauração de snapshot testada com banco e credenciais fictícios temporários.
- Nenhum banco operacional, identidade real, credencial real, mídia ou chamada paga criado.

## Limites e pendências

- Esta etapa não adapta painel, agentes, hooks ou ferramentas do legado. Não ocorreu corte
  de produção nem ativação do novo banco como fonte canônica do workspace.
- Credenciais locais não isolam usuários do sistema operacional. Revogação/rotação e
  autenticação remota ainda não têm implementação.
- Verificações declaradas pelo executor não são certificação automática de qualidade.
- O fechamento por bloqueio é histórico; a versão atual não despacha sucessores nem
  atualiza automaticamente bloqueios. Dependentes aguardam conclusão antes do aceite.
- Nenhum conteúdo antigo foi importado ou reconstruído; os arquivos antigos não foram
  apagados por esta entrega. Estado canônico de filme não foi editado.

## Fechamento e próximo responsável

Etapa técnica do núcleo: concluída, pendente revisão/integração pelo produtor. Aceitação
artística e ativação operacional: não solicitadas por este handoff nem alegadas.

Próxima etapa permanece sob responsabilidade do produtor/coordenador: revisar os limites,
atribuir painel e adaptadores ao novo banco e definir identidade operacional e sua gestão
antes de inicializar o ambiente real. Nenhum destinatário aceitou essa atribuição nesta
entrega; salvar este documento não representa próximo trabalho iniciado.

Bloqueio de ativação: **produtor/coordenador**, desbloqueado quando houver revisão do
núcleo e atribuição explícita da integração, com identidade/autorização de operador definida.
Não depende de recuperar dados ou JSON antigos. Não houve gasto, commit, merge ou publicação.
