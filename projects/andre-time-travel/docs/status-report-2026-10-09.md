# Relatório completo — "The Table Between Centuries" (Andre Athar)

Data: 2026-10-09 ~12:20 (-03). Fontes: `manage.py status`, `tasks/board.json`, `approvals.json`, `credit-ledger.csv`, `memory/STATE.md`, pastas do projeto e leitura visual. Nada neste relatório foi inventado; o que não está provado aparece como pendente.

## 1. Resumo executivo

| Item | Situação |
|---|---|
| Filme final (dois masters) | **Não existe.** `finalMovieVerified = false`. Nenhuma versão completa foi montada e assistida. |
| Pré-produção | **Pronta**: roteiro v2 aprovado, bíblias, atlas (3 versões), storyboard de 41 planos, áudio-guia grátis para 22/22 falas. |
| Identidade do Andre | **Element Kling criado** (`323525046658711`, a partir de fotos reais) com a voz "Athar" ligada. 12 keyframes de época aceitos. |
| Piloto | **5 takes de vídeo** feitos (incluindo 2 com fala nativa verificada por STT); aceitos pelo agente. |
| Capítulo Galileo (T13) | **Em andamento**: 4 clipes revisados (G-01, G-02, G-03, G-05), prévia em `08_edit/picture-lock/galileo-en-preview-v1.mp4`. Todos "aceitos pendente reprodução completa". |
| Capítulos Caesar, Genghis, Napoleon, Oppenheimer, abertura e final | **Não iniciados** (T14–T18 bloqueadas). |
| Saldo Kling vivo | **5.813** créditos (lido agora). Partiu de 7.741 (snapshot histórico). |
| Tarefas | 7 concluídas, 2 em andamento, 12 bloqueadas (de 21). |

Atenção: outro agente está trabalhando neste mesmo checkout agora (Galileo; há `.kling-producer.lock` e arquivos G-* não commitados). Não toquei neles.

## 2. Tarefas (board)

Concluídas: T01 brief/limites, T02 referências recebidas, T03 bíblias, T04 Element do Andre, T05 roteiro em inglês checado, T08 piloto de identidade, T09 rota de fala.
Em andamento: T12 keyframes de época/olhos, T13 Galileo.
Bloqueadas: T06 idiomas históricos, T07 amostras de voz, T10 reprevisão de custos, T11 storyboard/animatic, T14–T17 capítulos restantes, T18 abertura/final, T19 reserva de correção, T20 edição histórica, T21 entrega/verificação.

## 3. Aprovações (`approvals.json`)

Verdadeiras: `characterReferences`, `productionElement`, `screenplay`, `speechRoute`, `pilot` (todas registradas pelo agente produtor sob a autorização geral do Andre).
Falsas: `voiceTests`, `storyboard`, `paidBatch`, `finalPicture`.
Ressalva: a aprovação de semelhança e a voz por ouvido são decisões que só o Andre pode tomar. Os registros dizem que os clipes do piloto aguardam ele assistir. Trate `characterReferences/pilot` como "aceitas pelo agente, falta o seu olhar".

## 4. O que está pronto, por área

**Roteiro e pesquisa**: `01_script/script-en.md` + CSV v2 (22 falas, Napoleon como ponto de virada, um único "argue", novo final), revisão do historiador (aprovado com edições aplicadas), 20 fontes registradas/capturadas (2 snapshots não em cache), 4 traduções com IPA marcadas como **superadas e sem revisão qualificada** (precisam ser refeitas a partir do v2).

**Bíblias**: personagem Andre, mesa/continuidade e 5 bíblias de cena (cabeçalho PROPOSED; decisões D01–D13 em `00_brief/decisions/`). Look canônico revisado: terno cinza risca de giz / camisa branca listrada, como nas fotos reais.

**Referências visuais** (todas sintéticas e não aprovadas, exceto as fotos reais):
- Andre: 62 arquivos (fotos reais aprovadas, recortes, 3 pacotes sintéticos R1/R2, perfis, suíte cinematográfica de 5 ângulos, 3 polimentos R3).
- Olhos históricos (só olhos, sem rostos completos): 30 arquivos, 5 figuras.
- Mesa e 6 placas de época: 22; roupas abaixo do pescoço: 16; 5 inserções de mão/mesa.
- 12 keyframes de época com o Andre (falando e ouvindo), aceitos.
- 22 originais com rosto completo estão em quarentena (`07_generations/originals/_quarantine-full-face`).

**Áudio**: guia gratuito edge-tts de 22/22 falas (120,8 s de fala em 240 s); testes de voz ElevenLabs (VT-01 + 4 de abertura), **nenhum ouvido/aprovado**; stems de guia de Galileo.

**Piloto** (`06_pilot`): 5 vídeos kling-video-v3_0 720p, 5 revisões; fala verificada por STT nas linhas G-L04 e O-L04.

**Galileo**: G-01 inserção de mão, G-02 Andre falando (GL02), G-03/G-05 olhos A/B; timeline `galileo-en-v1.json`, prévia MP4. Marca d'água do provedor presente: é corte de revisão, não master.

**Storyboard**: atlas v1/v2/v3 (79 cartões, 3 PDFs, zero overflow), lista de 41 planos, pacote ZIP v1.

**Marketing**: 5 pôsteres teatrais (v1) e 5 pôsteres de encontro "por cima do ombro" (v2), 2:3, candidatos sintéticos.

**Polimento do Andre (pedido de hoje)**: 3 versões A faithful (mesa, fotos 015259 e 015214), 60 créditos, revisadas lado a lado, fiéis. Aguardam o seu julgamento.

**Ferramentas e processo**: `scripts/review_sweep.py` (varredura de imagens, log em `08_edit/image-review-log.json`), `kling_batch.py`, `manage.py`, `workflow.py`; modelo de continuação para novos episódios; Git local com LFS. Testes unitários e `manage.py validate` passam (avisos só de skills compartilhadas).

## 5. Orçamento

- Saldo vivo: 5.813. Teto planejado do filme: 6.981 (base antiga; reprevisão T10 pendente).
- Gasto por escopo no ledger: R1 952, R2 205, R3 polimento 60, R3 keyframes 281, piloto 334, Galileo 348, blanket 120 (Element 180 relatado em STATE). Soma do ledger é **aproximada**; a diferença real 7.741 → 5.813 é 1.928. O ledger tem cobranças inexplicadas registradas (2×41 em imagens; 70 vs 30 em vídeos idênticos) e um job de Galileo com ID perdido (80 créditos, "UNCERTAIN").
- ElevenLabs: ≈480 créditos de teste; nada comprado.

## 6. Pendências e riscos

**Só o Andre pode**: assistir os 5 clipes do piloto (semelhança e voz por ouvido); julgar as 3 versões polidas e os pôsteres; escolher pôster; sessão de fotos de perfil/neutro/sentado (D08, ainda faltam).
**Produção**: reprevisão de custos (T10); animatic de áudio primeiro (T11); capítulos Caesar/Genghis/Napoleon/Oppenheimer; abertura e final; reproduzir arquivos completos de cada clipe aceito (hoje só grades de quadros).
**Idiomas**: Edição H sem rota nativa; alvos/revisores (T06) e revisão linguística qualificada pendentes; não aprovar fidelidade só por IPA.
**Riscos**: marca d'água do provedor nos clipes; deriva leve de composição na mesa; 202 imagens ainda sem revisão visual no log; 2 snapshots de fontes sem cache.
**Estado git**: há mudanças não commitadas de outros agentes (Galileo, `kling_batch.py`, testes). Commit só do que for atribuído a cada agente.

## 7. Próximos passos recomendados

1. Andre assiste o piloto e a prévia de Galileo e responde: semelhança OK? voz OK? polimento A OK?
2. Fechar Galileo (reprodução completa, remover marca d'água na entrega) como capítulo-modelo.
3. Reprevisão T10 com o saldo 5.813, depois T11 animatic gratuito.
4. Repetir Caesar → Genghis → Napoleon → Oppenheimer com a mesma gramática; fotos de perfil (D08).
5. Rodar a varredura de imagens nas 202 pendentes (revisão grátis).
