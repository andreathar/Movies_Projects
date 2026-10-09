# Piloto Galileu v2, pós-triagem: disposição sobre o ombro (G-REF + G-KF + G-X01 + G-X02)

Projeto: andre-time-travel. Papel: producer, delegado de envio pago e ledgers (bot Produção e Créditos 9bfe6c7d).
Data: 2026-10-09, cerca de 13:00 (America/Sao_Paulo).
Status: **ESPECIFICAÇÃO PARA APROVAÇÃO DO ANDRE. Nenhum job enviado.**
Versão anterior preservada: `2026-10-09-piloto-galileu.md` (v1). Esta v2 mantém da v1 a disposição (§1), os prompts-base e os critérios, e aplica só as mudanças abaixo. Plano total: `2026-10-09-plano-regeneracao-nova-direcao-v2.md`.

## O que mudou em relação à v1
- **Decisões da Direção:**
  - G-X01 com **5 s**;
  - fala do piloto = **G-L02**;
  - ombro do Galileu **parado, só com respiração mínima** (sem gesto);
  - figurino = **J23 _belowneck mais a manga de R2-J12**;
  - mesa de 120×75×75 cm continua **proposta** (F04), sem virar medida canônica.
- **Triagem da Edição** (`08_edit/reviews/2026-10-09-revisao-nova-direcao/`):
  - **Modelo de enquadramento**: `07_generations/originals/R3-oppenheimer-speaking-o1_1.jpg` (SERVE; sha256 4c26297a…), único quadro já sobre o ombro. Entra como referência de câmera e escala do ombro, e só disso. Ele mostra a nuca; o piloto continua com a cabeça histórica fora do quadro, salvo decisão em contrário.
  - **Figurino**: J23 _belowneck é SERVE (aa1a68bd…, hash corrigido no registro hoje); R2-J12 também.
  - **Marca d'água**: G-01 e G-02 têm marca KlingAI, removível com crop de ~1,08x. Os vídeos novos podem vir marcados, então o conteúdo essencial precisa ficar nos 92% centrais.
  - **Montagem**: G-02 (REAPROVEITAR) fica como contraplano frontal da mesma fala, com crop de 1,08x. Não substitui o G-X02, que é a prova da disposição pedida.
  - **R2-wardrobe-galileo-scholar.jpg** mostra boca e barba: **não usar** em prompt sem cortar 30% do topo. A v2 não usa.

## Itens v2

### G-REF: 1 imagem (antes 2)
- **Modelo**: `kling image_to_image --model gemini-3-pro-image --img_resolution 2k --aspect_ratio 16:9 --image_count 1`.
- **Referências**:
  1. imagem 1 = `02_references/table/R1-J26-table-anchor_2.png`;
  2. imagem 2 = `02_references/wardrobe/R1-J23-costume-galileo_belowneck.png`;
  3. imagem 3 = `02_references/inserts/R2-J12-insert-galileo_1.jpg`;
  4. imagem 4 = `02_references/table/R1-J29-plate-arcetri-1634_1.png`;
  5. **imagem 5 = `07_generations/originals/R3-oppenheimer-speaking-o1_1.jpg` (só enquadramento)**.
- **Prompt**: o mesmo da v1, mais este trecho ao final:
> Use image 5 ONLY as a guide for camera position, lens and the scale/blur of the foreground shoulder; do not copy any person, face, clothing, room or light from image 5. The foreground man is completely still except for a barely visible breath.
- **Custo**: **20** (base: R3-session-*, 20 por imagem). Pior caso: 40, se a única imagem falhar e for preciso a segunda.
- **Aceite**: igual à v1. Mais estas checagens:
  - ombro e manga ocupando 25 a 35% da borda direita, como no modelo;
  - nada de Andre ou de Oppenheimer copiado da imagem 5;
  - conteúdo essencial nos 92% centrais.

### G-KF: 3 tentativas (antes 6)
- **Modelo e rota**: os mesmos da v1 (`kling-image-o1`, Element 323525046658711).
- **Mestre (G-KF-M)**: referências da v1 mais **图片5 = R3-oppenheimer-speaking-o1_1.jpg** como guia de enquadramento. Acrescentar ao prompt:
> Match the camera height, lens and foreground-shoulder framing of 图片5, but keep the head of the foreground man fully outside the frame and keep everything else from 图片2/图片3/图片4.
  - Até **2 tentativas**.
- **Escuta (G-KF-L)**: derivada do mestre, como na v1. **1 tentativa.**
- **Custo**: **3** (LR3-*-o1, 1 cada). Pior caso: 43, com uma cobrança de 41 (LNOTE-R3-anomaly). Se o primeiro delta passar de 1, parar.
- **Aceite**: igual à v1.

### G-X01: 5 s (decidido)
- **Modelo**: `kling-video-v3_0`, `--duration 5 --resolution 720p --prefer_multi_shots false --enable_audio false`, Element. Parte de G-KF-L.
- **Prompt**: o da v1, trocando a frase do primeiro plano por:
> The foreground man stays completely still — no gesture, no turn — only a barely visible breath lifts his shoulder.
- **Custo**: **30** (LPILOT-03, 6 cr/s). Pior caso: 70 (14 cr/s).
- **Aceite**: igual à v1, mais conteúdo essencial nos 92% centrais (para o crop da marca).

### G-X02: fala G-L02 com 12 s (decidido)
- **Modelo**: `kling-video-v3_0`, `--duration 12 --enable_audio true`, Element. Parte de G-KF-M.
- **Prompt**: o da v1, com a mesma troca de frase do primeiro plano.
- **Custo**: **108** (creditsConsumed=108 em G-02-andre-GL02, mesma configuração). Pior caso: 108.
- **Aceite**: igual à v1, mais os 92% centrais. Na montagem, intercalar com G-02 cortado em 1,08x, se a Edição quiser.

## Custo do piloto
| Item | v1 (5 s) | v2 normal | v2 pior caso |
|---|---|---|---|
| G-REF | 40 | 20 | 40 |
| G-KF | 6 | 3 | 43 |
| G-X01 (5 s) | 30 | 30 | 70 |
| G-X02 (12 s) | 108 | 108 | 108 |
| **Total** | **184** | **161** | **261** |

- O G-X01 está fixado em 5 s; se voltar a mudar, cada segundo vale ±6 cr (pior caso ±14).
- Saldo 5.813. O Galileu passa de 348 para 509 (pior caso 609), abaixo da parada de 810.

**Fases**: as mesmas da v1, cada uma com OK explícito do Andre.
1. **A**: G-REF + G-KF, ≤23 cr (pior caso 83).
2. **B**: G-X01, 30 cr.
3. **C**: G-X02, 108 cr.

## Dúvidas que restam
1. A nuca desfocada (como no modelo de Oppenheimer) pode aparecer? A especificação segue com a cabeça fora do quadro, por ser mais seguro.
2. A mesa de 120×75×75 cm vira canônica depois do piloto?
3. A bíblia de costas (Personagens) ainda não saiu. Seguimos com J23 e R2-J12 (decisão desta rodada).
