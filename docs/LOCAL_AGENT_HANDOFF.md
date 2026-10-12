# Edição local e passagem entre agentes

Andre (autor e aprovador) autorizou que os arquivos fiquem neste workspace e possam receber mudanças locais. Essa autorização permite trabalhar nas fontes atribuídas; não aprova automaticamente imagens, gastos ou publicação. Os limites inegociáveis estão em [AGENTS.md](../AGENTS.md) e não são repetidos aqui.

## Mapa de autoria

| Papel | Arquivos de trabalho possíveis | Entrega esperada |
|---|---|---|
| Produtor | Manifesto, board, aprovações, ledgers, registros da série | Integração, decisão de escopo e estado canônico coerente |
| Continuidade | `03_bibles/`, propostas de seleção e notas em `02_references/_review/` | Referências específicas e riscos de identidade/roupa/mesa |
| Historiador | Pesquisa, fontes e propostas de roteiro em `01_script/` | Fatos rastreáveis e diálogo explicitamente ficcional |
| Diálogo/som | Direção de fala, traduções, revisões de áudio e stems locais | IDs estáveis, texto revisado, duração medida e parecer de língua |
| Storyboard | `05_storyboard/source/atlas.json`, keyframes e revisões novas | Cobertura, enquadramento, direção e lacunas identificadas |
| Editor | Timelines, legendas e masters em novas versões | Montagem reproduzível com caminhos de mídia resolvidos |
| QC | Pareceres em pastas de revisão | Evidência sobre o arquivo exato e problemas reproduzíveis |

Esses caminhos indicam áreas possíveis; o agente atua somente no escopo atribuído. A atualização de aprovações, tarefas, gastos e registros canônicos é do produtor; revisores não submetem jobs, não alteram credenciais e não escrevem fora do projeto (AGENTS.md). Quem exerce cada papel em um episódio está na tabela de responsabilidades de [PARLEY_PROTOCOL.md](PARLEY_PROTOCOL.md); a tabela acima trata de funções, não de plataformas.

## Como entregar uma mudança

Copiar `shared/templates/agent-handoff.json` para `projects/<episodio>/agents/handoffs/<data>-<papel>-<assunto>.json`, com nome único. Preencher responsabilidade, caminhos relativos à raiz do workspace, hashes antes/depois, motivo, verificações e decisões pendentes. Não preencher resultado ou aprovação que não ocorreu.

Antes de salvar, reler o arquivo de destino. Se mudou desde o hash de partida, comparar as duas versões e integrar o trabalho concorrente; não restaurar cegamente uma cópia antiga. Dois agentes não devem editar ao mesmo tempo o mesmo JSON de direção. O coordenador distribui arquivos ou intervalos de edição.

As versões entregues do atlas, fotos de origem, downloads originais, respostas de provedores e ledgers históricos são preservados. Alterações de conteúdo criam nova versão. Um erro em registro canônico recebe correção explícita com nota e evidência; não apagar histórico para aparentar sucesso.

## Aprovações por versão

Usar `shared/templates/review-decision.json` para registrar a decisão real sobre um arquivo/hash e seu uso. Aprovação de semelhança, interpretação, idioma, keyframe, take, lote financeiro e master são decisões distintas. Um aceite de uma foto não aprova todos os derivados dela.

O inventário ajuda a detectar conteúdo que mudou; ele não autentica a pessoa que aprovou e não bloqueia edições. Uma mudança em fonte aprovada exige reavaliar seus derivados antes de gasto ou aceitação. V1/V2 dos cartões e os testes de voz continuam candidatos até decisão explícita.

## Retomada mínima

Ler [AGENTS.md](../AGENTS.md) e `memory/STATE.md` do episódio (`START_HERE.md` é apenas o índice para humanos), executar status/validação, conferir hashes do conjunto relevante e registrar o que realmente mudou. Não depender de mensagens antigas, `/tmp`, links assinados de provedores ou arquivos guardados somente em outra conta. Os caminhos do catálogo e do inventário levam aos arquivos locais.
