# Fluxo repetível — Andre viajando no tempo

Versão 2.1 (rascunho de consolidação), 9 de outubro de 2026. Escopo: pré-produção, edição local, rastreabilidade e preparação de novas histórias. O fluxo de geração e montagem ainda precisa ser provado pelo piloto e pelos masters do primeiro filme.

Este documento descreve o **processo reutilizável**. Não repete regras que têm fonte canônica: limites inegociáveis em [AGENTS.md](../AGENTS.md); autoria e formato de entrega em [LOCAL_AGENT_HANDOFF.md](LOCAL_AGENT_HANDOFF.md); commits, integração e backup em [VERSION_CONTROL.md](VERSION_CONTROL.md); responsáveis e mecânica dos lanes do filme atual em [PARLEY_PROTOCOL.md](PARLEY_PROTOCOL.md). Nomes de pessoas, plataformas e lanes aparecem só no protocolo do episódio. A política de economia de contexto e de mensagens (delta, uma fonte por assunto, resultado curto, verificação em lote sem reduzir QC) está em [TOKEN_EFFICIENCY.md](TOKEN_EFFICIENCY.md) e vale para este fluxo sem ser repetida aqui.

## O que permanece e o que muda

O registro [series.json](../series/andre-time-travel/series.json) mantém o protagonista, a exigência de aprovação da semelhança, a separação entre foto real e imagem sintética, a regra de nenhum rosto histórico completo e a separação entre diálogo ficcional e fatos documentados.

O estado de aprovação de mesa, figurino, identidade e voz deve ser consultado nas decisões do episódio; não se deve tratar todos como aprovados ou pendentes em bloco. Reutilizar um arquivo exige identificar sua versão e seu hash, a decisão que permite o uso e o escopo dessa decisão. Copiar o arquivo não transfere aceite nem autorização financeira.

As cinco épocas, os 240 segundos, as 41 tomadas e as duas edições são decisões deste filme. Cada continuação define seus próprios encontros, duração, estrutura, idiomas, referências, orçamento e testes. O modelo de rascunho não preenche esses campos por herança.

## Etapas e prova para avançar

| Etapa | Entrada | Saída verificável | Condição para avançar |
|---|---|---|---|
| Briefing | Objetivo dramático e restrições | Pergunta, arco de Andre, encontro, consequência, duração e idiomas | Escopo registrado pelo produtor |
| Pesquisa e roteiro | Fatos com fontes e intenção dramática | Roteiro completo e falas com IDs estáveis | Revisão factual; texto ficcional explícito; aceite do roteiro |
| Continuidade | Fotos reais, candidatos e referências separados | Bíblias de identidade, roupa, mesa, luz e câmera | Andre aprova a semelhança; referências selecionadas por versão |
| Voz | Texto revisado e escopo do serviço | Arquivos reais, duração medida e notas de interpretação | Escuta, pronúncia e língua revisadas; rota de sincronização testada |
| Piloto | Referências aprovadas e envelopes de câmera | Pequeno conjunto de tomadas com IDs, custos e revisão | Identidade, olhos, mãos, boca e continuidade sustentam o método |
| Decupagem e animatic | Áudio medido e resultado do piloto | Cobertura completa, cortes motivados e lacunas reais | Duração e cobertura viáveis; não acelerar fala para caber no rascunho |
| Lote | Requests concretos e revisão do saldo/parâmetros | Escopo aprovado, referências exatas e registro de submissão | Aprovação específica do lote; emissão somente como em [AGENTS.md](../AGENTS.md) |
| Produção | Requests aprovados | Respostas, originais, custo real ou explicitamente estimado, revisão por take | Aceite individual; job concluído não é take aceito |
| Montagem | Takes e áudio aceitos | Timeline, legendas, stems e masters versionados | Sem arquivo faltando; sincronização e duração conferidas |
| QC e arquivo | Arquivos finais exatos | Reprodução integral, revisão dos quadros de risco e hashes | Aceite de imagem, língua, som, créditos e entrega |

O gerenciador atual representa a estrutura do primeiro filme; não é ainda um planejador genérico de qualquer duração. A promoção de uma continuação exige criar um manifesto e tarefas coerentes com o seu próprio plano. O rascunho é deliberadamente uma etapa anterior.

## Ciclo de edição local

1. Ler o estado canônico e delimitar arquivos com o coordenador.
2. Registrar hashes de partida e a entrega no formato de [LOCAL_AGENT_HANDOFF.md](LOCAL_AGENT_HANDOFF.md) (modelo `shared/templates/agent-handoff.json`).
3. Editar fontes, preservando IDs. Atualizar roteiro e CSV juntos quando mudar fala; manter manifesto e lista de tomadas coerentes quando mudar duração.
4. Validar insumos. Regenerar os derivados em uma pasta nova; o gerador recusa sobrescrita.
5. Comparar os arquivos resultantes, revisar cortes/enquadramentos e registrar a decisão com caminho, hash, versão e escopo. Mudança de conteúdo requer nova revisão dos derivados afetados.
6. O produtor integra o trabalho, resolve conflitos e atualiza aprovações/tarefas somente com evidência. Uma aprovação antiga permanece como histórico, mas não prova aceite de uma versão nova.
7. Atualizar a memória local e criar um novo inventário. Se os hashes iniciais mudaram durante a edição, comparar o trabalho concorrente antes de integrar.

Os snapshots e templates auxiliam esse procedimento; não existe um bloqueio distribuído de arquivos nem detecção automática de toda dependência artística. A coordenação de autoria e a decisão humana continuam necessárias.

## Reconstruir o atlas deste episódio

As direções e referências foram extraídas para `projects/andre-time-travel/05_storyboard/source/atlas.json`. As falas continuam vindo de `01_script/dialogue-lines.csv`; o gerador confere se cada fala existe no roteiro. Ele recusa IDs inconsistentes, referências ausentes, caminhos externos e intervalos de fala fora da cena.

```bash
python3 scripts/build_preproduction_atlas.py \
  --source 05_storyboard/source/atlas.json \
  --output 05_storyboard/preproduction-atlas-v3 \
  --revision v3
```

Use sempre um nome ainda inexistente. V1 é a entrega original; V2 é a reconstrução usada para validar a nova fonte editável. O renderer continua específico do filme de cinco encontros: uma continuação usa o método e desenha suas próprias fontes/diagramação.

Requisitos locais já observados: Python 3.11+, Pillow 10.2.0, ReportLab 4.1.0, `pdftoppm` e fontes DejaVu Sans. As ferramentas de gestão e os testes usam apenas a biblioteca padrão e a `.venv` do projeto. O renderer usa o `python3` com as bibliotecas de imagem disponíveis nesta máquina. Nenhum requisito foi instalado nesta etapa; em outra máquina é preciso prover esses requisitos e reconectar os links de skills.

Cada render salva `evidence/build-inputs.json`, com hashes dos insumos, e uma cópia de `atlas-source.json`. O catálogo identifica a versão e mantém `approved: false`. Os PDFs são documentos de revisão, não resultados novos do Kling.

## Iniciar outra continuação

```bash
.venv/bin/python scripts/workflow.py new-draft \
  --id andre-episodio-02 --title "Título de trabalho a definir"
.venv/bin/python scripts/workflow.py check-clean-draft --path drafts/andre-episodio-02
```

O primeiro comando cria arquivos editáveis, diretórios, tarefas iniciais e memória em `drafts/andre-episodio-02`. Não altera o filme ativo, não registra produção e não copia arquivos de mídia. O segundo confirma apenas a limpeza do ponto de partida; depois de preencher o roteiro, o rascunho já não é vazio e essa checagem deixa de ser a validação apropriada.

Quando o briefing estiver definido, o produtor prepara manifesto, plano de tomadas, fontes e tarefas do novo episódio, escolhe um destino livre em `projects/`, preserva o rascunho, registra-o em `workspace.json`, `memory/projects.json` e no registro da série, e executa os testes. A seleção de `activeFilm` deve refletir a produção realmente em trabalho. Nunca copiar saldo, jobs, takes, `approved: true` ou orçamento de outro episódio.

## Inventário e recuperação

```bash
.venv/bin/python scripts/workflow.py index --output reports/workflow-v2/file-index.json
.venv/bin/python scripts/workflow.py verify --index reports/workflow-v2/file-index.json
```

O inventário inclui fontes, mídia, requests/respostas, documentos, código, modelos e evidência local. Não copia credenciais, runtimes, caches nem destinos externos de symlinks. Arquivos novos são listados separadamente; ausências e alterações retornam erro para revisão. O snapshot não é automaticamente reescrito.

O ZIP V1 é uma apresentação autocontida, não um backup restaurável de toda a produção. Para transferir o trabalho completo, preservar o workspace e seus originais; comparar o inventário depois da cópia. As skills ligadas a perfis externos e o ambiente Python precisam ser resolvidos na outra máquina. O Git local com LFS foi habilitado posteriormente a pedido do usuário; preservar também `.git/lfs/objects` no backup e seguir `docs/VERSION_CONTROL.md`. Não há sincronização de nuvem, geração em segundo plano ou agendamento habilitado.

## Critério de validação do modelo

O ensaio local prova organização, acesso, edição rastreável, reconstrução, recusa de sobrescrita, integridade e isolamento de uma continuação. Ele não prova semelhança em movimento, voz convincente, sincronização labial, precisão dos idiomas históricos, preço futuro ou qualidade final. Esses pontos devem aparecer como pendentes até o piloto, a escuta/revisão e o QC dos arquivos exatos.

## Coordenação reutilizável entre sessões

### Responsabilidade e ponto de direção
Cada episódio nomeia, na tabela de responsabilidades do seu protocolo ([PARLEY_PROTOCOL.md](PARLEY_PROTOCOL.md)), quem é autor/aprovador, quem produz e coordena (e em qual checkout), quem pesquisa e documenta, quem edita e revisa, e quem cria as imagens-base. Nome de ferramenta ou plataforma não é papel de filme; uma continuação troca essa tabela e mais nada. A conversa produtora recebe as decisões de Andre, distribui tarefas delimitadas e integra entregas. Uma lane no terminal não herda automaticamente o histórico da conversa principal.

O produtor concentra manifesto, board, aprovações, ledger, registro de assets, decisões e integração da memória. Demais agentes entregam propostas e evidências sem alterar esses registros em paralelo.

### Divisão que prepara as imagens
- História e cultura material: fatos, calçados, piso, cabelo, mangas, objetos e fontes de luz possíveis, com fontes e incerteza.
- Storyboard/continuidade: espaço compartilhado, mesa, eixo, alternativas de ombro, anatomia e rosto histórico protegido.
- Iluminação: fonte motivadora e continuidade entre planos; uma fonte plausível não equivale a design aprovado.
- Diálogo/som: voz-guia, sincronismo, duração medida, contato de pés/dedos, tecido, respiração e silêncio.
- Criador de imagens: integra referências e produz candidatos versionados; demais agentes não geram substitutos sem atribuição.
- Editor/QC: monta material existente autorizado e revisa arquivos exatos. Operação do Kling e capacidade de inspeção visual são avaliadas separadamente por evidência, não pelo fornecedor do agente.

A ficha de encontro relaciona intenção, fala difícil, palavra/ideia causadora, reação corporal e efeito sobre Andre. Humor e opinião pessoal são escolhas dramáticas; não são fatos ou citações atribuídas. Usar apenas os detalhes úteis à cena, sem obrigar cinco encontros a repetir os mesmos planos.

### Contrato de tarefa e dependências
Toda atribuição informa objetivo, dono, entradas e versões, saídas e caminhos permitidos, dependências, verificação e limites. Classificar como preparação independente ou trabalho dependente de mídia. Checklist, prompt e placeholder não comprovam imagem entregue. A entrega de mídia informa caminhos relativos, hashes, versões e estado candidato/aprovado para o uso específico. Não transferir aprovação de um rosto ou still automaticamente para vídeo.

Gates de um teste pago não bloqueiam pesquisa e preparação independentes. Autorização para planejar não libera geração paga; as regras de emissão, saldo e nova tentativa estão em [AGENTS.md](../AGENTS.md).

### Worktrees, commits e integração
Movido para [VERSION_CONTROL.md](VERSION_CONTROL.md), seção "Worktrees, commits e integração entre lanes", que passa a ser a única fonte. Regra de uso neste fluxo: dependências identificam versão e hash; ninguém edita em outra lane nem assume a identidade dela.

### Evidência de comunicação
Distinguir plugin instalado, serviço pronto, participante iniciado, mensagem aceita, recebida/reconhecida e tarefa concluída. Branch existente não prova agente ativo. Só declarar comunicação testada após ida e volta verificadas. Não contornar diálogos de confiança. Um handoff em disco não prova leitura pelo destinatário. Checkpoints preservam estado; não fundem conversas.

Responsáveis e mecânica do episódio: [PARLEY_PROTOCOL.md](PARLEY_PROTOCOL.md). Edição e entrega: [LOCAL_AGENT_HANDOFF.md](LOCAL_AGENT_HANDOFF.md). Versionamento e integração: [VERSION_CONTROL.md](VERSION_CONTROL.md). Essas regras podem ser usadas com outro coordenador além do Parley. Atribuições, autorizações e medidas de cena não passam automaticamente à próxima continuação.
