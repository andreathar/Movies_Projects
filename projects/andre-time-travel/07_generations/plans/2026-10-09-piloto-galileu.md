# Piloto Galileu: disposição sobre o ombro (G-REF + G-KF + G-X01 + G-X02)

Projeto: andre-time-travel ("The Table Between Centuries"). Papel: producer, delegado de envio pago e ledgers (bot Produção e Créditos 9bfe6c7d).
Data: 2026-10-09, cerca de 12:50 (America/Sao_Paulo).
Status: **ESPECIFICAÇÃO PARA APROVAÇÃO DO ANDRE. Nenhum job enviado, nada gerado, ledgers inalterados.**
Plano-mãe: `07_generations/plans/2026-10-09-plano-regeneracao-nova-direcao.md` (IDs G-REF, G-KF, G-X01 e G-X02 iguais aos de lá).

## 0. Base: auditoria já registrada (não repetida aqui)
Este piloto executa a recomendação da auditoria local de encenação. Ler lá o diagnóstico e as evidências:
- `08_edit/reviews/holistic-staging-v1/findings.json`:
  - **F01**: o espaço muda entre fala e escuta.
  - **F02**: falta um plano de 3 a 5 s sobre o ombro com os dois na mesma mesa.
  - **F04**: proposta de mesa doméstica de cerca de 120 × 75 × 75 cm, com a conversa atravessando os 75 cm.
  - **F03**: a reação B deve vir depois de G-L04 (isso é da montagem, não deste piloto).
- `08_edit/reviews/holistic-staging-v1/DIRECTOR_HANDOFF.md`, itens 1 a 3, e `REPORT.md`.
- `memory/STATE.md`, seções "Holistic staging audit" e "NEW CREATIVE DIRECTION"; `memory/session-log.json`, evento `holistic_staging_audit` (nextCheckpoint).
- Também valem: D04 (mesa J26-2: anel e lasca; "a mesa viaja"), D09 (eixo: Andre à esquerda, olhando para a direita da câmera), a regra de zero rosto inteiro (AGENTS.md) e o guia `docs/prompt-playbook-kling.md` (§1, §3, §4).

## 1. Disposição fixa: quadro mestre, a mesma em todos os itens
- **Mesa**: carvalho J26-2 (`02_references/table/R1-J26-table-anchor_2.png`, sha256 3b25e4d2…). Doméstica, cerca de 120 cm de comprimento × 75 cm de profundidade × 75 cm de altura (proposta F04, ainda não aprovada).
- **Assentos**: Andre e Galileu frente a frente nos lados longos. Os dois estão sentados, e a conversa atravessa os **75 cm** do tampo. Ninguém fica na cabeceira.
- **Câmera**: atrás e um pouco à direita do Galileu, na altura dos olhos de quem está sentado (cerca de 115 a 120 cm do chão). Lente equivalente a cerca de 50 mm, travada, sem movimento, sem grande-angular.
- **Composição 16:9**:
  - **Terço direito**: ombro direito, parte de cima do braço e manga do Galileu (gibão de lã carvão escuro, punho de linho com mancha de tinta, como em J23 e R2-J12), **bem desfocados**, entrando pela borda direita.
  - **Cabeça, pescoço, orelha, cabelo, barba e queixo do Galileu inteiramente fora do quadro**, pela borda direita e pela de cima.
  - **Do centro ao terço esquerdo**: Andre **em foco**, sentado do outro lado, antebraços na borda de lá da mesa, olhando para a direita da câmera, na direção do ombro em primeiro plano.
- **Tampo**: o MESMO tampo une os dois (tábuas claras no sentido do comprimento). O anel de copo fica visível entre os dois; a lasca fica no canto mais próximo da câmera, se aparecer.
- **Luz e lugar**: Arcetri, 1634, a partir do plate `02_references/table/R1-J29-plate-arcetri-1634_1.png` (sha256 09ae1705…). Anoitecer frio pela janela de pedra à esquerda, chave suave vinda da esquerda da câmera, fundo desfocado. Sem texto legível.
- **Fala e escuta**: os keyframes de fala e de escuta saem do mesmo quadro mestre (G-KF-M). Só muda a expressão do Andre; câmera, mesa, cadeiras, ombro e luz ficam idênticos. Isso resolve F01.

## 2. Itens, custos e critérios

Preços observados (detalhados no plano-mãe, §3):
| Tipo de job | Preço | Base |
|---|---|---|
| Imagem gemini-3-pro-image 2K | 20 cr por imagem | creditsConsumed=20 em `responses/R3-session-02..08`; job de 2 imagens = 40 (L002 a L009) |
| Imagem kling-image-o1 com Element | 1 cr | LR3-*-o1, 16 de 18 jobs (2 cobranças de 41 em LNOTE-R3-anomaly) |
| Vídeo kling-video-v3_0 720p sem áudio | 6 cr/s | LPILOT-03: 30 por 5 s; documentação: 6 cr/s; pior caso 14 cr/s |
| Vídeo kling-video-v3_0 720p com áudio e Element | 9 cr/s | `responses/G-02-andre-GL02.submit.json`: creditsConsumed=108 por 12 s; LPILOT-04: 72 por 8 s |

### G-REF: placa da disposição com o Galileu de costas (sem o Andre)
- **Modelo**: `kling image_to_image --model gemini-3-pro-image --img_resolution 2k --aspect_ratio 16:9 --image_count 2`.
- **Referências** (imagem 1 a 4):
  1. `R1-J26-table-anchor_2.png` (mesa);
  2. `02_references/wardrobe/R1-J23-costume-galileo_belowneck.png` (sha256 aa1a68bd…);
  3. `02_references/inserts/R2-J12-insert-galileo_1.jpg` (b59837cf…, manga e mão já aceitas, sem cabeça);
  4. `R1-J29-plate-arcetri-1634_1.png`.
- Sem Element: o Andre não aparece.
- **Prompt proposto:**
> Photorealistic cinematic film still, 16:9. A small domestic oak dining table about 120 cm long and 75 cm deep — exactly the table of image 1: pale wide planks with length-wise grain, the faint ring stain in the middle of the tabletop, the chipped near corner. Camera at seated eye height, locked, standard 50 mm lens, placed BEHIND and slightly to the right of a man seated on the near long side. In the RIGHT third of the frame, very close to the lens and strongly OUT OF FOCUS: only his right shoulder, upper arm and sleeve, and his forearm resting on the near edge of the table — dark charcoal wool doublet and ink-stained white linen cuff exactly as in images 2 and 3. His entire head, neck, ear, hair, beard and chin are OUTSIDE the frame beyond the right and top edges — no face, no profile, no silhouette of a head, no shadow or reflection of a face. Across the 75 cm tabletop, on the far long side, an EMPTY wooden chair faces the camera, in sharp focus, in the centre-left of the frame. Room and light from image 4: Arcetri 1634, cool dusk through a stone window from the left, soft and out of focus. No other people, no readable text or writing, no watermark, no wide-angle distortion.
- **Custo**: 2 imagens × 20 = **40 cr** (linha de base: R3-session-*, 20 cada).
- **Critério de aceite**:
  - zero cabeça, pescoço, perfil ou sombra de rosto do Galileu em todo o quadro, conferido em 100% de zoom;
  - ombro e manga desfocados no terço direito;
  - cadeira vazia em foco do outro lado, a cerca de 75 cm, num tampo único e contínuo;
  - anel visível e lasca coerente com D04;
  - mão com cinco dedos, sem anéis, figurino de J23;
  - sem texto legível.
  - Escolher 1 de 2. Se nenhuma servir, parar e não refazer sem novo OK.

### G-KF: keyframes da disposição com o Andre (mestre/fala e escuta)
- **Modelo**: `kling image_to_image --model kling-image-o1 --img_resolution 2k --aspect_ratio 16:9 --imageCount 1 --elements '[{"id":"323525046658711","bindName":"Andre"}]'`. É a rota D11 do playbook §1.
- **G-KF-M, mestre e fala.**
  - Referências:
    1. 图片1 = `02_references/andre/approved/cover_20240202_015341_hs34.jpg` (fee8a610…);
    2. 图片2 = G-REF escolhido;
    3. 图片3 = `R1-J26-table-anchor_2.png`;
    4. 图片4 = `R1-J29-plate-arcetri-1634_1.png`.
  - Prompt proposto:
> Photorealistic cinematic film still, 16:9, 2K. Keep EXACTLY the composition, camera position, lens, table, out-of-focus shoulder and room of 图片2; change nothing in the right third. Place <<<323525046658711>>> in the EMPTY chair across the table: the man's face must be EXACTLY the face in 图片1 — same face shape, nose, brow, eye colour, short textured dark-brown hair, light stubble, mid-forties — no beautification, no different actor. He sits on the far long side, about 75 cm away across the same tabletop, in the centre-left of the frame, IN SHARP FOCUS, forearms resting on his edge of the table, body and gaze turned toward camera-RIGHT at the man whose shoulder is in the foreground. Wardrobe exactly as in 图片1: mid-grey pinstripe suit jacket open over a white finely striped shirt, open collar, no tie. The table is the oak table of 图片3: pale wide planks, faint ring stain between the two men. Light from 图片4, soft key from camera-left. The foreground man's head, neck and face stay completely OUTSIDE the frame; his shoulder and sleeve stay soft and out of focus. Exactly two people. No face reflections, no text, no watermark. Expression: attentive, mid-thought, lips slightly parted, neutral pre-speech mouth.
- **G-KF-L, escuta, derivado do mestre** (lição do playbook: escuta sai do quadro de fala aceito).
  - Referências: 图片1 = G-KF-M aceito; 图片2 = cover.
  - Prompt proposto:
> Edit 图片1 minimally. Keep EXACTLY the same composition, camera, table, foreground shoulder, light and the face of <<<323525046658711>>> (identity as in 图片2). Change ONLY his expression: listening, mouth closed, calm steady attention, a hint of weight in the eyes. Foreground man's head stays outside the frame.
- **Custo**: até 3 tentativas do mestre + até 3 da escuta = **6 cr**, a 1 cr cada (linhas LR3-*-o1). Risco já visto: uma tentativa pode cobrar 41 (LNOTE-R3-anomaly). Teto de alerta: 46 cr. Se o primeiro delta passar de 1, parar e reconciliar.
- **Critério de aceite**:
  - semelhança do Andre igual à dos KF R3 aprovados, com as fotos de 2024 como verdade (D01);
  - disposição pixel a pixel coerente com G-REF: mesmo tampo, ombro no terço direito, cabeça histórica fora;
  - Andre em foco e ombro desfocado;
  - olhar para a direita da câmera (D09);
  - escuta idêntica ao mestre, mudando só a expressão (sobrepor os dois e comparar mesa e ombro);
  - exatamente 2 pessoas, sem texto.

### G-X01: plano sobre o ombro, 3 a 5 s (escuta, durante G-L01)
- **Modelo**: `kling image_to_video --model kling-video-v3_0 --image <G-KF-L> --duration 5 --resolution 720p --imageCount 1 --prefer_multi_shots false --enable_audio false --elements '[{"id":"323525046658711","bindName":"Andre"}]'`.
- **Prompt proposto:**
> <<<323525046658711>>> listens to the man seated across the table, whose out-of-focus shoulder and sleeve fill the right third of the frame. He breathes, blinks once, and gives a very small nod; his forearms stay on the table. The foreground man is almost still — only a slight breath moves his shoulder. Locked camera, no camera movement, one continuous shot, no cuts. Preserve his face, hair, stubble, jacket, the table, the foreground shoulder and the lighting exactly as in the image. The foreground man's head never enters the frame; nobody else enters the frame; no hands near his face.
- **Custo**: 6 cr/s (base LPILOT-03, 30 cr por 5 s). **3 s = 18; 4 s = 24; 5 s = 30.** Pior caso a 14 cr/s: 42, 56 ou 70.
- **Critério de aceite**:
  - grade de todos os quadros (§4 do playbook: 11×11 para 5 s) sem nenhum quadro com cabeça, orelha, perfil ou reflexo do Galileu;
  - ombro permanece desfocado e no terço direito;
  - mesa, anel e cadeiras sem deriva;
  - identidade do Andre estável do começo ao fim;
  - sem corte interno nem movimento de câmera;
  - decodificação completa pelo FFmpeg;
  - Andre assiste em velocidade normal e percebe, sem explicação, dois interlocutores próximos na mesma mesa (critério do DIRECTOR_HANDOFF).

### G-X02: Andre fala G-L02 sobre o ombro
- **Modelo**: `kling image_to_video --model kling-video-v3_0 --image <G-KF-M> --duration 12 --resolution 720p --imageCount 1 --prefer_multi_shots false --enable_audio true --elements '[{"id":"323525046658711","bindName":"Andre"}]'`.
- **Duração**: G-L02 mediu 9,38 s no scratch, mais 2 s de cauda, total 12 s (regra do playbook).
- **Prompt proposto** (padrão D13 do G-02, adaptado à disposição):
> <<<323525046658711>>> speaks warmly in English to the old man seated across the table, whose out-of-focus shoulder and sleeve fill the right third of the frame; amused at the myth and respectful of the man, in a plain, unhurried voice. Andre says: "Believed, taught — and turned into a simple story: one man against the whole world. The truth was harder, and more interesting." He pauses briefly after "story", keeps his eyes on the man to camera-right, and falls silent after the last word, a small smile fading. The foreground man stays still and out of focus; his head never enters the frame. Quiet room tone only, no music. Locked camera, no camera movement, one continuous shot, no cuts. Preserve his face, hair, stubble, jacket, the table, the foreground shoulder and the lighting exactly as in the image. Nobody else enters the frame; no hands near his face.
- **Custo**: 12 s × 9 = **108 cr**. A base é G-02-andre-GL02 (creditsConsumed=108, mesma configuração).
- **Critério de aceite**:
  - todos os critérios de G-X01;
  - transcrição local (STT faster-whisper) igual ao texto canônico de G-L02;
  - voz só como guia (D14, dublagem depois; não é aprovação de voz);
  - boca sem artefato;
  - silêncio depois da última palavra;
  - loudness medido.
  - Se for aceito, substitui G-02 na prévia; G-02 continua como candidato.

## 3. Custo total

| Item | 3 s | 4 s | 5 s |
|---|---|---|---|
| G-REF (2 imagens) | 40 | 40 | 40 |
| G-KF (até 6 tentativas o1) | 6 | 6 | 6 |
| G-X01 (sobre o ombro, sem áudio, 6 cr/s) | 18 | 24 | 30 |
| G-X02 (fala de 12 s, 9 cr/s) | 108 | 108 | 108 |
| **Total** | **172** | **178** | **184** |
| Pior caso (G-X01 a 14 cr/s; 1 tentativa o1 a 41) | 236 | 250 | 264 |

- O total de 154 do plano-mãe somava só G-REF, G-KF e G-X02. O plano sobre o ombro de 3 a 5 s pedido agora acrescenta **18 a 30 cr**.
- **Variante enxuta**: G-REF com 1 imagem (20) e G-KF com até 4 tentativas (4) dá **150, 156 ou 162** para 3, 4 ou 5 s.
- Saldo vivo confirmado: **5.813** (`kling account`, 12:37). Mesmo o pior caso cabe com folga.
- O escopo do Galileu (teto de 900, parada em 810) já tem 348 gastos. O piloto levaria a 520–612, ainda abaixo do ponto de parada.

**Ordem de envio proposta (portões):**
1. **Fase A**: G-REF (40), escolha do Andre, depois G-KF (≤6), aprovação dos stills.
2. **Fase B**: G-X01 (18–30). Andre assiste.
3. **Fase C**: G-X02 (108), só se G-X01 passar no critério de dois interlocutores.

Cada envio usa `scripts/kling_batch.py --submit-only` e depois `--resume JOB`, um por vez, com saldo antes e depois e linha no ledger. **Cada fase precisa do OK explícito do Andre.**

## 4. Dúvidas para o Andre ou a Direção
1. Aprovar a mesa de 120 × 75 × 75 cm como medida canônica? Hoje é só proposta (F04); D04 cobre só aparência.
2. Duração do G-X01: 3, 4 ou 5 s? A sugestão é 5 s, que dá margem de corte e é o custo já testado.
3. Para a fala, usar G-L02 (12 s, 108 cr) ou uma fala mais curta? G-L04 tem 8,62 s e geraria 99 cr, mas o take atual dela já tem problema de ADR.
4. O ombro pode ficar parado (respiração) ou deve ter um gesto mínimo? Gesto aumenta o risco de a cabeça entrar no quadro.
5. A bíblia de costas (Personagens) ainda não saiu. Seguir com o figurino de J23 e R2-J12 ou esperar?
6. Não inspecionei as imagens de referência pixel a pixel neste passo: o acesso local recusou a leitura de imagem. As referências contam como aceitas pelo registro (R2-J12 "ACCEPTED candidate"; J23 sem aprovação formal). A Edição ou Personagens deve conferir J23 antes da Fase A.
7. Observação de registro: em asset-registry.csv, a fonte de R1-J23 cita sha256=d2824def…, mas o arquivo atual em `02_references/wardrobe/` tem aa1a68bd… (provavelmente o recorte abaixo do pescoço, não o original). Não alterei o registro; fica para quem cuida do ledger conferir.
