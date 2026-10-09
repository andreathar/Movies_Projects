# Revisão editorial/QC: nova direção (personagens de costas e desfocados + legado/repercussão)

Data: 2026-10-09 · Papel: editor + QC (somente leitura) · Projeto: `projects/andre-time-travel`
Base: `memory/STATE.md` § NEW CREATIVE DIRECTION (Andre, 2026-10-09 12:35), `docs/LOCAL_AGENT_HANDOFF.md`, `agents/bindings.json`.
Detalhe por arquivo: `review.csv` (234 linhas = todos os arquivos de mídia do escopo, inclusive cópias idênticas).

## Método
- Vídeos: 9 originais únicos (5 pilotos + G-01/G-02/G-03/G-05) com quadros extraídos a 2 fps e mosaicos com timecode; detecção de cena (limiar 0,2): nenhum corte interno nos originais. Preview de 42 s a 1 fps; cortes detectados em 4 / 14 / 18 / 21,5 / 25,5 / 29,5 / 33,5 / 38,5 s, batendo com `build-log.json` (E01–E09). Os 9 normalizados recebem a classificação do original de onde vieram.
- Imagens: 154 imagens únicas (por SHA-256), todas vistas; cópias idênticas herdam o parecer. Topos dos figurinos foram ampliados para checar a regra de zero rosto.
- Quadros extraídos em `/tmp` (fora do projeto). Não houve geração, gasto nem mudança em arquivo existente.
- Fora do escopo: pôsteres em `09_delivery/`, cartões do atlas em `05_storyboard/` e evidências de `08_edit/reviews/holistic-staging-v1/`.

## Contagens
| Classe | Linhas do CSV (234) | Únicos: imagens (154) | Únicos: vídeos originais (9) + normalizados (9) + preview (1) |
|---|---|---|---|
| SERVE | 65 | 45 | 0 |
| REAPROVEITAR | 160 | 100 | 19 |
| REFAZER | 9 | 9 | 0 |

Os 45 SERVE únicos são, na maior parte, fotos reais de identidade (14), plates/âncora (7), figurinos limpos (5), inserts de mãos (5), presente (4), polimentos D02 (2), folhas de contato/QC (7) e **um único quadro já na nova gramática** (R3-oppenheimer-speaking-o1). Nenhum vídeo serve como está.

## Principais achados
1. **Não existe nenhum plano de costas e desfocado de personagem em vídeo.** Todo o capítulo Galileu (42 s) mostra Galileu apenas como olhos (E03+E05 = 8 s) e mão (E01/E07/E09 = 11,5 s, o mesmo clipe usado 3 vezes). Andre aparece sempre sozinho, muitas vezes ao lado de uma mesa vazia (PILOT-01/02/05, todos os 12 keyframes), o que reforça a ausência.
2. **Material mais aproveitável para a nova direção:**
   - `07_generations/originals/R3-oppenheimer-speaking-o1_1.jpg`: nuca/ombro desfocado em primeiro plano enquanto Andre fala, figurino D02. Serve como modelo e como frame inicial para OTS.
   - `R2-andre-seated-conversational.jpg`: só como referência de composição (café moderno).
   - `R3-galileo-speaking_1.jpg` e `R3-test-omni-galileo-speaking_1.jpg`: planos gerais com espaço em primeiro plano para o personagem de costas.
   - Contraplanos frontais G-02, PILOT-04 e KF-*-speaking: a câmera já está no lugar do personagem.
3. **Olhos** (19 recortes + G-03/G-05): passam a REAPROVEITAR como beat curto (1,5–2 s), só depois de estabelecer o personagem de costas. Continuidade: dois tipos de César (R2-J02-B e R1-J11_2 divergem); Gengis R1-J14 parece mais velho; Oppenheimer R1-J20 com pálpebra inferior cortada (preferir R2-J05-B); Galileu R1-J16 com esclera avermelhada.
4. **Problemas técnicos:**
   - Marca "KlingAI" em G-01 (todos os quadros) e "KlingAI 3.0" em G-02, portanto também em E01/E02/E07/E09 e no preview. Remover com crop de ~1,08x.
   - G-05 tem uma piscada em ~3,0 s.
   - Os fundos não casam: G-02/PILOT-04 têm janela e estante, PILOT-01/02 têm pedra escura.
   - PILOT-03 e KF-oppenheimer-listening estão escuros demais.
5. **Regra de zero rosto nas referências de figurino:** R2-wardrobe-genghis (boca/barba), R2-wardrobe-galileo (boca, barba e ponta do nariz), R2-wardrobe-napoleon (queixo) e R2-wardrobe-oppenheimer (silhueta do queixo) precisam de corte no topo antes de entrar em prompt. Os originais R1-J21..J25 também mostram queixo; as versões `_belowneck` estão limpas.
6. **Figurino superado:** cerca de 36 refs sintéticas de Andre usam blazer marinho e camisa escura (anterior ao D02). Ficam só como referência de expressão/luz.
7. **REFAZER (9):**
   - R1-J10 ×2 (rosto visível; já rejeitado)
   - J01 img 2 ×2 (rejeitado)
   - R2-plate-rome-villa (exterior com mesa fora da âncora)
   - R2-wardrobe-andre-modern (figurino superado)
   - R3-present-listening-o1-v2 (díptico quebrado)
   - R2-J01-eyes-napoleon-recast_1 (meio rosto com nariz)
   - sonda de pôster nano (cadeira vazia)

## Lacunas para a nova direção (nada disso existe hoje)
- **Plano de costas e desfocado por personagem (0 de 5):** nuca, ombros e silhueta sentados à mesa com Andre falando em foco. Pelo menos 1 OTS e 1 plano geral de dois por capítulo.
- **Referências de figurino vistas de costas (0 de 5):** todas as refs são frontais. Elas são necessárias para gerar as costas com consistência (toga/púrpura, deel/armadura, gibão e gola, casaca verde, tweed).
- **Imagens de legado e repercussão (0):** o que cada um se tornou, como se fala deles hoje e como seus atos ecoaram, em tom intimista. Não existe nenhuma imagem desse tipo; o historiador precisa propor o conteúdo com fontes.
- **Plano que estabeleça os dois à mesa:** mesmo achado do holistic-staging-v1, agora com a solução (personagem de costas).
- **Planta fixa de mesa, cadeira e câmera por capítulo**, para que contraplano e plano de costas casem com os fundos já gerados.

## Próximo passo sugerido (sem gasto)
O produtor deve usar este CSV para estimar quais vídeos podem ser remontados e quais exigem nova geração (OTS de costas ×5, gerais ×5, legado ×N). Toda geração continua dependendo da aprovação explícita de Andre. O preview de Galileu (T13) segue como candidato e precisa ser remontado.
