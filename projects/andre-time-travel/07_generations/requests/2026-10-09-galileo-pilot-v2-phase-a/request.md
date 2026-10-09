# Pedido para o Hermes: piloto Galileu v2, FASE A apenas

- **Status**: pacote montado pelo producer (bot Produção e Créditos 9bfe6c7d) em 2026-10-09, cerca de 13:05 (America/Sao_Paulo). **Nada foi submetido.** Quem executa é o Hermes.
- **Autorização**: `00_brief/decisions/D16-galileo-pilot-v2-phase-a.json` (sha256 `e79793a58063198f291669f368dcac76dfd0ec8fc3aea46da00ed691a08c1d0e`). Aprovação do Andre só da Fase A; as fases B e C **NÃO** estão aprovadas.
- **Plano aprovado**: `07_generations/plans/2026-10-09-piloto-galileu-v2.md` (sha256 `a6892aa197062e1f0a31d72573097f8d6c97db716f501d892527601f4a3c6cee`, igual ao citado na D16). Os prompts abaixo são os da v2 sem nenhuma edição de conteúdo, porque a D16 vale só para esse conteúdo exato. A Direção liberou depois a "nuca desfocada"; essa liberação **não** entra aqui, e a cabeça do Galileu fica fora do quadro. Usá-la exigiria uma nova revisão.

## TETO E REGRAS DE PARADA (obrigatórias)
- **Teto rígido: 23 cr acumulados nesta fase** (G-REF 20 + G-KF 3 × 1).
- **Antes de cada job**: se o gasto acumulado mais a estimativa do próximo job passar de 23, NÃO submeter. Parar e reportar.
- **Depois de cada job**: comparar o delta de saldo (`kling account` antes e depois) com a estimativa. Se o job cobrar acima do estimado (G-REF > 20, ou uma tentativa o1 > 1, como a cobrança de 41 já vista em LNOTE-R3-anomaly), **parar e avisar o Andre** antes de qualquer outro job, mesmo que o acumulado ainda esteja abaixo de 23.
- Sem retentativas além das listadas: G-REF tem 1 imagem, sem segunda; G-KF-M tem até 2 tentativas; G-KF-L tem 1. Se o G-REF não passar no aceite, parar (o pior caso de 40 da v2 não cabe no teto).
- Um job por vez: `python scripts/kling_batch.py --spec <spec> --only <JOB> --submit-only`, depois `--resume <JOB>`. Cada job leva saldo antes e depois e uma linha no `credit-ledger.csv`, feita pelo runner. Usar `auth` = `D16-galileo-pilot-v2-phase-a`.
- Aceite criativo é do Andre, ou da Edição a pedido dele. Passar no aceite técnico não aprova o resultado criativamente (limitação da D16).

## Disposição fixa (igual à do plano v2, §1 da v1)
- **Mesa**: doméstica de carvalho J26-2, cerca de **120 cm × 75 cm × 75 cm** de altura (proposta F04, não canônica). Andre e Galileu ficam frente a frente nos lados longos, e a conversa **atravessa os 75 cm** do tampo. Ninguém na cabeceira. Anel de copo visível entre os dois; lasca no canto mais próximo da câmera.
- **Câmera**: atrás e um pouco à direita do Galileu, na altura dos olhos de quem está sentado, lente de 50 mm, travada.
- **Terço direito**: ombro, braço e manga do Galileu (J23 + punho de R2-J12), **bem desfocados e parados**, só com respiração mínima. A cabeça, o pescoço, a orelha, o cabelo, a barba e o queixo ficam **fora do quadro**.
- **Centro-esquerda**: Andre em foco, olhando para a direita da câmera (D09).
- Os keyframes de fala e de escuta saem do **mesmo** quadro mestre; só muda a expressão.
- Luz e lugar: Arcetri 1634, anoitecer frio vindo da esquerda.

## Referências (sha256 conferido com sha256sum em 2026-10-09)
| Papel | Caminho (relativo a projects/andre-time-travel) | sha256 |
|---|---|---|
| table | `02_references/table/R1-J26-table-anchor_2.png` | `3b25e4d226f3815b874e6d7a00c53237fb3181b8437d99c23097851bdd80e04b` |
| costume | `02_references/wardrobe/R1-J23-costume-galileo_belowneck.png` | `aa1a68bd89bf700bbc1832b6d5a244515d6fcfc2fe88d504bd5ba6fb62484b31` |
| sleeve | `02_references/inserts/R2-J12-insert-galileo_1.jpg` | `b59837cf94f1250b09a22a5bfa328ba9a0d4187b4bc3b06f0e0e10575f2a2267` |
| plate | `02_references/table/R1-J29-plate-arcetri-1634_1.png` | `09ae1705cccfee76315e4ddba8e3ffff6c0207abd659d14634ff40e0888e82d3` |
| framing | `07_generations/originals/R3-oppenheimer-speaking-o1_1.jpg` | `4c26297a7668e1460e85334e526a3813c4c8e55075eba76ab383af9b2f05bfbd` |
| cover | `02_references/andre/approved/cover_20240202_015341_hs34.jpg` | `fee8a6104fb499bbf87d8bb0b3df7b8960adc506d753e49f59a014c7a68cb1f5` |

- **Element do Andre**: `323525046658711` (bindName "Andre"), "Andre Athar - grey suit - identity v2 20261009". Decisão D11 (`00_brief/decisions/D11-element-and-still-route.json`); rota de still = kling-image-o1 + cover real + Element.
- J23 _belowneck: o sha256 correto é o do recorte (aa1a68bd…), corrigido no registro hoje (linha 277; as antigas ficam como histórico).
- R3-oppenheimer-speaking-o1_1.jpg serve **só** como guia de enquadramento: câmera, lente e escala do ombro. Nada dele deve ser copiado.

## Jobs, em ordem
| # | Job | Modelo | Parâmetros | Tentativas | Estimado | Acumulado máx. |
|---|---|---|---|---|---|---|
| 1 | G-REF-galileo-pilot-v2 | gemini-3-pro-image (image_to_image) | img_resolution 2k, aspect_ratio 16:9, image_count 1; sem Element | 1 | 20 | 20 |
| 2 | G-KF-M-galileo-pilot-v2-a1 | kling-image-o1 (image_to_image) | img_resolution 2k, aspect_ratio 16:9, imageCount 1, elements [{"id": "323525046658711", "bindName": "Andre"}] | 1 | 1 | 21 |
| 3 | G-KF-M-galileo-pilot-v2-a2 | kling-image-o1 | igual ao 2 | só se a1 for rejeitada | 1 | 22 |
| 4 | G-KF-L-galileo-pilot-v2-a1 | kling-image-o1 | igual ao 2 | 1 | 1 | 23 |

Se a1 for aceita, a2 não roda (acumulado final de 22).

- **Spec executável**: `request.json`. Contém só o G-REF, porque todas as referências já existem.
- **G-KF**: `request-gkf.template.json`. Os itens `<G-REF-accepted…>` e `<G-KF-M-accepted…>` são **marcadores**: o Hermes troca pelo caminho real do download aceito (e anota o sha256) antes de submeter. Não submeter com marcador.

### 1. G-REF (20 cr)
- **Imagens, em ordem**: 1 = mesa J26-2; 2 = J23 _belowneck; 3 = R2-J12 (manga e punho); 4 = plate Arcetri; 5 = R3-oppenheimer-speaking-o1_1 (só enquadramento).
- **Prompt final**:
> Photorealistic cinematic film still, 16:9. A small domestic oak dining table about 120 cm long and 75 cm deep — exactly the table of image 1: pale wide planks with length-wise grain, the faint ring stain in the middle of the tabletop, the chipped near corner. Camera at seated eye height, locked, standard 50 mm lens, placed BEHIND and slightly to the right of a man seated on the near long side. In the RIGHT third of the frame, very close to the lens and strongly OUT OF FOCUS: only his right shoulder, upper arm and sleeve, and his forearm resting on the near edge of the table — dark charcoal wool doublet and ink-stained white linen cuff exactly as in images 2 and 3. His entire head, neck, ear, hair, beard and chin are OUTSIDE the frame beyond the right and top edges — no face, no profile, no silhouette of a head, no shadow or reflection of a face. Across the 75 cm tabletop, on the far long side, an EMPTY wooden chair faces the camera, in sharp focus, in the centre-left of the frame. Room and light from image 4: Arcetri 1634, cool dusk through a stone window from the left, soft and out of focus. No other people, no readable text or writing, no watermark, no wide-angle distortion. Use image 5 ONLY as a guide for camera position, lens and the scale/blur of the foreground shoulder; do not copy any person, face, clothing, room or light from image 5. The foreground man is completely still except for a barely visible breath.
- **Aceite**:
  - zero cabeça, pescoço, perfil ou sombra de rosto do Galileu, em zoom de 100%;
  - ombro e manga desfocados, ocupando 25 a 35% da borda direita;
  - cadeira vazia em foco do outro lado, a cerca de 75 cm, num tampo único e contínuo;
  - anel visível e lasca coerente com D04;
  - mão com 5 dedos, sem anel, figurino J23;
  - nada de pessoa, roupa ou sala copiado da imagem 5;
  - sem texto legível; conteúdo essencial nos 92% centrais.
  - **Se reprovar, parar** (não há segunda imagem).

### 2–3. G-KF-M, mestre e fala (1 cr por tentativa, até 2)
- **Imagens**: 图片1 = cover do Andre; 图片2 = G-REF aceito; 图片3 = mesa J26-2; 图片4 = plate Arcetri; 图片5 = R3-oppenheimer-speaking-o1_1 (enquadramento). Mais o Element.
- **Prompt final**:
> Photorealistic cinematic film still, 16:9, 2K. Keep EXACTLY the composition, camera position, lens, table, out-of-focus shoulder and room of 图片2; change nothing in the right third. Place <<<323525046658711>>> in the EMPTY chair across the table: the man's face must be EXACTLY the face in 图片1 — same face shape, nose, brow, eye colour, short textured dark-brown hair, light stubble, mid-forties — no beautification, no different actor. He sits on the far long side, about 75 cm away across the same tabletop, in the centre-left of the frame, IN SHARP FOCUS, forearms resting on his edge of the table, body and gaze turned toward camera-RIGHT at the man whose shoulder is in the foreground. Wardrobe exactly as in 图片1: mid-grey pinstripe suit jacket open over a white finely striped shirt, open collar, no tie. The table is the oak table of 图片3: pale wide planks, faint ring stain between the two men. Light from 图片4, soft key from camera-left. The foreground man's head, neck and face stay completely OUTSIDE the frame; his shoulder and sleeve stay soft and out of focus. Exactly two people. No face reflections, no text, no watermark. Expression: attentive, mid-thought, lips slightly parted, neutral pre-speech mouth. Match the camera height, lens and foreground-shoulder framing of 图片5, but keep the head of the foreground man fully outside the frame and keep everything else from 图片2/图片3/图片4.
- **Aceite**:
  - semelhança do Andre igual à dos KF R3 aprovados (fotos de 2024 como verdade, D01);
  - mesma disposição do G-REF: mesmo tampo, ombro no terço direito, cabeça histórica fora;
  - Andre em foco, ombro desfocado, olhar para a direita da câmera;
  - exatamente 2 pessoas, sem texto.

### 4. G-KF-L, escuta (1 cr, 1 tentativa)
- **Imagens**: 图片1 = G-KF-M aceito; 图片2 = cover do Andre. Mais o Element.
- **Prompt final**:
> Edit 图片1 minimally. Keep EXACTLY the same composition, camera, table, foreground shoulder, light and the face of <<<323525046658711>>> (identity as in 图片2). Change ONLY his expression: listening, mouth closed, calm steady attention, a hint of weight in the eyes. Foreground man's head stays outside the frame.
- **Aceite**: idêntico ao mestre, mudando só a expressão (sobrepor os dois e comparar mesa e ombro); boca fechada; cabeça histórica fora.

## Depois da fase A
O Hermes entrega os caminhos e o sha256 dos resultados, os deltas de saldo e as linhas do ledger. O producer reconcilia. As fases B (G-X01, 5 s, 30 cr) e C (G-X02, 12 s, 108 cr) precisam de **nova aprovação** do Andre.
