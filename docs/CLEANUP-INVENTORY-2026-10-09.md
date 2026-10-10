# Limpeza do workflow — inventário local

Escopo: filme e suas referências de documentação. Revisão em andamento com Claude; este inventário não é uma desinstalação nem uma declaração de que a consolidação foi integrada.

## Decisões de organização

- Manter regras vigentes nos pontos de entrada existentes; substituir repetições por referências. Preservar decisões e documentos antigos como histórico identificado, sem apresentá-los como instruções atuais.
- Parley é o mecanismo de coordenação escolhido para este filme. Baton Pass não é necessário como segundo fluxo ativo; manter sua instalação compartilhada até avaliar uso em outros projetos.
- Carregar skills conforme a tarefa. Não remover ferramentas globais apenas porque não participam deste filme. Retirar uma referência do workflow e desinstalar um plugin são operações diferentes.
- Arquivos originais e imagens de figurino escuro continuam preservados; arquivamento lógico não equivale a apagar arquivos.

## Evidência local e encaminhamento

| Item | Verificação | Encaminhamento |
| --- | --- | --- |
| `skills/andre-time-travel` | Procedimento próprio do filme | Manter ativo |
| `skills/kling-cli` | Link para `../.agents/skills/kling-cli` | Manter ativo; registro de origem precisa de reconciliação |
| Continuidade, localização de diálogo e QC | Links para skills no perfil Hermes | Manter: são dependências do filme, mesmo com o aplicativo Hermes fechado |
| `skills/grounded-citations` | Link para skill de pesquisa do perfil Hermes | Manter disponível para pesquisa histórica |
| `.claude/skills` e `.hermes/skills` | Bindings por links simbólicos | Não são cópias duplicadas do conteúdo; não apagar por contagem de pastas |
| `skills/registry.json` | Origem de Kling ainda aponta para o perfil Hermes | Produtor deve reconciliar origem e hash com a instalação local, sem apenas revalidar hashes para ocultar avisos |
| `memory/STATE.md` do filme | Ainda contém papéis pendentes, lanes não iniciadas e próximos passos do teste antigo | Produtor deve conciliar com protocolo e evidências atuais; saldo antigo está explicitamente marcado como observação histórica |

## Divisão e limite da revisão

Claude consolida documentos atribuídos e entrega o mapa de regras vigentes, históricas e substituídas. O produtor revê e integra, incluindo correções dos registros centrais sob sua responsabilidade. Nenhum agente deve apagar histórico ou ampliar a tarefa para configurações globais por conta própria.

Esta passada inspecionou links, registro de skills e documentação local. Não avaliou o uso de todos os plugins nos demais projetos, não desinstalou ferramentas e não instalou bloqueios técnicos. Remover arquivos do disco, por si só, não prova redução dos tokens de uma sessão já aberta.
