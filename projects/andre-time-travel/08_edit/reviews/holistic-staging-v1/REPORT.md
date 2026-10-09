# Revisão holística — encenação, mesa e continuidade

Data: 2026-10-09T15:29:16.139976+00:00. Arquivos e sessão mudam durante a produção; os snapshots preservam o que foi examinado.

**Parecer:** existe uma base aproveitável de identidade, roteiro e cobertura, mas a presença dos dois personagens na mesma mesa ainda não foi demonstrada. Recomendo validar Galileu como conversa completa antes de replicar a encenação nos outros quatro capítulos. Não marquei tarefas ou takes como rejeitados/aprovados e não interrompi a sessão do diretor.

## A resposta à preocupação de Andre

Os planos solo são cobertura de diálogo: a outra pessoa aparece em planos separados de olhos/mãos/roupa e sua voz pode continuar sobre a imagem de Andre. Isso pode funcionar sem os dois rostos no mesmo quadro. Porém, o plano atual não prova que alguém será inserido posteriormente no vídeo. Composição digital não está validada como solução. Para a presença que os pôsteres sugerem, falta um plano compartilhado sobre o ombro, com a cabeça histórica fora do enquadramento.

A mesa parece grande sobretudo pela leitura espacial: muito tampo vazio, nenhum contracampo de ombro e, em alguns closes de escuta, o tampo parece estar ao lado/atrás de Andre. Não há evidência suficiente para medir comprimento e largura reais. A especificação atual dá material/marcas/altura, mas não fixa a planta e a distância entre as cadeiras.

## O que foi realmente verificado

- Nove arquivos originais de vídeo distintos: cinco pilotos e quatro novos vídeos de Galileu. Todos sondados e decodificados integralmente.
- Primeiro/meio/fim de cada vídeo (27 amostras) e um quadro de cada um dos nove eventos da prévia.
- Prévia de Galileu: **42 s / 1008 quadros / 1920 × 1080**, ampliada de fontes próximas de 720p; hash `b008ed2bc030945f2248bc75a063b96ccf766a8347d27f87a54c15763d14b10d`. Snapshot do arquivo em `snapshots/galileo-en-preview-v1.mp4`.
- Roteiro, CSV, bíblias, mapa de cenas, decisões, registros financeiros e estado operacional.
- Sessão Hermes **Art direction workflow for Andre Athar time-travel film**, id `20261009_081822_9a8c50`: evidência recente de trabalho, modelo registrado `gpt-6.1-sol`. Nenhuma conclusão de perda de contexto só pela duração. A sessão está associada a outra pasta; detalhes em `director-session.json`.
- A auditoria não substitui reprodução integral com áudio, revisão visual de todos os quadros, julgamento humano de semelhança ou aprovação do master.

## Evidências e correções

### P0 · F01 — O espaço da conversa muda entre fala e escuta

Na fala (4–14 s e 25,5–29,5 s), Andre apoia os antebraços na mesa à frente. Na escuta (18–21,5 s e 33,5–38,5 s), o tampo aparece lateral/atrás, com outro fundo e sem apoio visível dos braços. As imagens não estabelecem o mesmo arranjo de cadeiras. Isso é uma diferença observável de composição; não é uma medição 3D nem prova de dimensão física.

**Ação recomendada:** Rever E04/E08 antes de usar como escuta do mesmo diálogo; selecionar cobertura neutra da composição de fala ou produzir uma nova escuta a partir do mesmo keyframe, com a mesa e a cadeira nas mesmas posições.

**Evidência local:** `frames/E02-G-02-mid.png`, `frames/E04-G-04-mid.png`, `frames/E06-G-04-mid.png`, `frames/E08-G-07-mid.png`

### P0 · F02 — Falta um plano que estabeleça os dois na mesma mesa

Os nove eventos da prévia alternam Andre sozinho, olhos isolados e mão/torso de Galileu. Nenhum estabelece simultaneamente Andre e o ombro/mão do interlocutor na mesma geometria. Os planos separados podem sustentar diálogo, mas o espaço compartilhado ainda não foi demonstrado. Não existe no plano uma etapa comprovada de inserir uma pessoa por composição digital depois.

**Ação recomendada:** Validar um plano de 3–5 s sobre o ombro de Galileu, com Andre em foco, os dois sentados, trecho de mesa compartilhado e cabeça histórica integralmente fora do quadro. Usar como âncora; manter os closes isolados compatíveis.

**Evidência local:** `preview-audit.json`, `snapshots/manifest.json`

### P1 · F03 — A reação de Galileu antecede a frase que deveria provocá-la

E05 usa o olhar de resolução G-05 em 21,5–25,5 s. G-L04 começa em 25,5 s; a ideia final está legendada em 31,1–33,5 s. O roteiro associa a resolução a does not settle a question. A reação aparece antes de sua causa.

**Ação recomendada:** Reposicionar a reação B para durante o fim da frase ou imediatamente depois; usar escuta neutra na pergunta G-L03. Preservar tempos reais de fala e não acelerar rostos para caber.

**Evidência local:** `snapshots/08_edit/timelines/galileo-en-v1.json`, `snapshots/01_script/script-en.md`

### P1 · F04 — A mesa tem textura definida, mas a escala e os assentos não estão fechados

D04 fixa carvalho, três tábuas, anel e lasca. A bíblia dá altura aproximada de 75 cm, mas não largura/profundidade e não mostra planta de assentos/câmeras. Tampo vazio e perspectiva lateral ampliam a sensação de distância. Não é possível medir a mesa real a partir destes enquadramentos gerados.

**Ação recomendada:** Proposta para teste, não medida/aprovada: mesa doméstica de cerca de 120 × 75 × 75 cm, duas cadeiras em lados opostos do tampo de 75 cm, conversa próxima. Fixar planta, distância de borda e altura do olhar num único quadro mestre antes de variar planos.

**Evidência local:** `snapshots/00_brief/decisions/D04-table.json`, `snapshots/03_bibles/table-and-continuity.md`

### P1 · F05 — As bíblias de cena repetem falas antigas

C-L04, K-L04, G-L04 e N-L04 nas bíblias não coincidem com script-en.md/dialogue-lines.csv, apesar do cabeçalho de sincronização com v2. Exemplo decisivo: N-L04 canônica é Every day. We are still not sure who pays it.; a bíblia ainda traz o comentário antigo sobre guerras e grandeza, perdendo a virada do protagonista.

**Ação recomendada:** Gerar os textos derivados exclusivamente do CSV/roteiro vigente e anexar hash/versão; não permitir que bíblias antigas voltem a alimentar prompts de fala.

**Evidência local:** `snapshots/01_script/dialogue-lines.csv`, `snapshots/03_bibles/scene-bibles/caesar.md`, `snapshots/03_bibles/scene-bibles/genghis.md`, `snapshots/03_bibles/scene-bibles/galileo.md`, `snapshots/03_bibles/scene-bibles/napoleon.md`

### P1 · F06 — Registros parcialmente reconciliados; resumo e matriz ainda desatualizados

Na primeira checagem, às 15:26 UTC, o manifest tinha 5 takes e 0/41 slots mapeados. Durante a auditoria, o diretor atualizou o registro: na checagem de fechamento há 9 takes e os 7 slots de Galileu mapeados, ainda sem aceite final. Essa parte foi resolvida pelo trabalho concorrente do produtor. A abertura de STATE e a matriz de continuidade continuam com referências de etapas antigas. A prévia e a timeline auditadas permanecem byte a byte iguais; os problemas de encenação e de ordem da reação continuam presentes.

**Ação recomendada:** Preservar a reconciliação já feita; atualizar o resumo vigente e a matriz, sincronizar bíblias e separar aprovação de identidade, voz, encenação e filme final. Não tratar a lacuna inicial de registro como prova de tarefa esquecida.

**Evidência local:** `management-checks.json`, `snapshots/memory/STATE.md`, `snapshots/tasks/board.json`, `snapshots/03_bibles/continuity-matrix.csv`

### P1 · F07 — Sessão do diretor vinculada a diretório de outro projeto

A sessão Art direction workflow for Andre Athar time-travel film, id 20261009_081822_9a8c50, registra cwd /mnt/data/Projects_SSD/tranfere_gov_api. Os resultados recentes observados apontam para Movies_Projects; não foi constatada escrita cruzada neste exame. O modelo registrado no momento é gpt-6.1-sol, com mudança visível de modelo no histórico. Não foi confirmada a identificação Fable 5.1.

**Ação recomendada:** Reancorar a sessão no projeto Movies_Projects antes do próximo bloco de trabalho, carregar o checkpoint atual e tornar explícito o escopo de arquivos. Não reiniciar ou trocar modelo apenas pelo tempo decorrido; avaliar artefatos e estado atual.

**Evidência local:** `director-session.json`

### P2 · F08 — A prévia ainda precisa de acabamento e aceitação temporal

Vozes são guias, dublagem final não aprovada; frase G-L04 tem pronúncia duvidosa registrada. Olhos aparecem em faixa com bordas pretas grandes; não cortar/expandir revelando face. Há marca d’água dos originais. A saída 1920×1080 é ampliada de fontes ~720p. Esta auditoria decodificou os arquivos e examinou quadros, mas não ouviu/assistiu a prévia integralmente em tempo real.

**Ação recomendada:** Uniformizar a apresentação da faixa de olhos, finalizar a dublagem alinhada, revisar todos os quadros arriscados e reproduzir o arquivo final inteiro. Manter prévia e master final distintos.

**Evidência local:** `preview-audit.json`, `snapshots/08_edit/reviews/G-02-andre-GL02.json`, `snapshots/00_brief/decisions/D14-dub-strategy.json`

## O que preservar

O roteiro canônico funciona como arco: Andre começa mais seguro e termina reconhecendo um limite. O momento em que Napoleão lhe devolve a pergunta é importante. Preserve isso ao sincronizar as bíblias. Os takes de fala G-02 e PILOT-04 podem continuar como candidatos; os pilotos de escuta não precisam ser apagados, mas a aprovação de identidade não garante sua compatibilidade espacial com esse diálogo. Os inserts e olhos oferecem cobertura útil, desde que ligados a uma encenação comprovada e às palavras certas.

## Próximo teste concreto

1. Registrar uma planta simples: dois sentados em lados opostos, distância íntima, mesma mesa, fonte de luz e linha de olhar. Uma mesa de 120 × 75 × 75 cm é uma proposta de teste, não uma medida inferida nem uma decisão já aprovada.
2. Criar um keyframe horizontal 16:9 sobre o ombro, sem tipografia: ombro/manga histórica à direita e desfocados; cabeça inteira fora de quadro; Andre à esquerda, em foco, sentado, com cotovelos e borda visíveis; mesa compartilhada ocupa apenas o necessário.
3. Derivar fala e escuta do mesmo arranjo. Não tentar consertar a geometria simplesmente sobrepondo alguém aos takes antigos.
4. Testar apenas 3–5 segundos desse enquadramento, conforme escopo e saldo registrados pelo produtor. Esta auditoria não submeteu geração.
5. Montar Galileu com a reação de resolução no fim de G-L04; ver e ouvir a conversa inteira. Se a presença parecer convincente, usar como padrão dos outros encontros.

## Handoff e coordenação

O diretor segue trabalhando. Este documento é um parecer com snapshots, não uma ordem enviada ao Hermes nem uma pausa executada. Antes de aplicar qualquer correção, reler as versões atuais, comparar os hashes e integrar alterações concorrentes. Não reiniciar o projeto, descartar originais ou refazer todos os vídeos. Reancorar a sessão no Movies_Projects e carregar um checkpoint de uma página é mais útil que confiar no título antigo da sessão ou trocar de modelo sem diagnóstico.

## Verificação de gestão

Workspace válido; 29 testes passaram nesta checagem (a falha de fixture relatada anteriormente já não ocorreu). Permanecem quatro avisos de hashes de skills compartilhadas. Isso não verifica composição, atuação ou montagem. Ledger local registra 348 créditos na etapa Galileu, incluindo 80 do job original sem ID recuperável, e saldo posterior 5813: são registros históricos, não saldo consultado agora. Nenhum job, compra, mensagem externa, alteração de sessão, commit ou publicação foi executado por esta auditoria.

## Fechamento com produção concorrente

Conferência em 2026-10-09T15:34:47.517055+00:00: o produtor já registrou os 9 takes e mapeou os 7 slots de Galileu. Sua revisão local também reconhece que a geometria física não está comprovada e que a reprodução integral ainda está pendente. A prévia e a timeline são idênticas às cópias analisadas. Não atribuir a lacuna inicial de registros a perda de memória; manter os achados visuais, dramáticos e de documentos derivados. Evidência: `snapshots/final-check/` e `management-checks.json`.
