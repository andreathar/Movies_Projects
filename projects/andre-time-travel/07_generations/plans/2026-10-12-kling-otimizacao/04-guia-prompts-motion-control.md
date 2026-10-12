# 04 · Guia de prompts — motion control e movimento de posição A→B

Objetivo: quando o personagem tiver que **sair de uma posição e chegar a outra**, acertar a
ferramenta e o prompt na primeira tentativa. Nada aqui gasta crédito; são fórmulas e comandos
preparados.

> Regra do filme que manda em tudo: a imagem-sujeito do `motion_control` precisa ter **pessoa ou
> animal claro**. Rosto completo de figura histórica é proibido → **motion control com rosto =
> Andre**. Figuras (olhos, insertos abaixo do pescoço) só entram em `image_to_video`, e mesmo assim
> sem rosto.

## 1. Qual ferramenta para "sair de A e chegar a B"

| Situação | Ferramenta | Por quê |
|----------|-----------|---------|
| Quero controlar **início E fim** exatos do deslocamento | `image_to_video` · `first_image` **+ `tail_image`** (`v3_0`, `v2_5`, `v2_6`) | os dois quadros ancoram a posição inicial e a final; o modelo interpola o caminho |
| Tenho uma **performance real gravada** cujo jeito de andar/mexer quero transferir | `motion_control` (`v3_0`/`v2_6`) | transfere o movimento do vídeo para a imagem-sujeito |
| Ação simples sem quadro final definido (levantar, inclinar, virar a cabeça) | `image_to_video` normal | uma ação dirigida pelo prompt |
| Repetir o mesmo gesto em vários takes | `motion_control` (+ `motion_library`) | movimento salvo reaproveitável |
| Editar um vídeo já existente | `omni_ref_video` | v2v |

**Para "andar de A para B" com controle, prefira `first_image` + `tail_image`.** `motion_control`
entra quando o **modo** do movimento (a performance) importa mais que a posição exata.

## 2. Capacidades observadas — reconferir no catálogo atual

`motion_control` · `kling-video-v3_0` (padrão):
- Inputs: `image`* (sujeito), `video` (opcional). Args: `prompt`*, `motionId` (opcional),
  `motionDirection`*, `resolution` (default **720p**), `keepOriginalSound` (default **true**),
  `elements` (no máximo **1**).
- Fonte de movimento: **exatamente uma** — `video` **ou** `motionId` (nunca as duas, nunca nenhuma).
- `motionDirection`: `image_direction` segue a **imagem** e **só aceita movimento de 3–10 s**;
  `motion_direction` segue o **vídeo**.
- `v2_6` é igual, **sem `elements`**.

Registro anterior da biblioteca (`motion_library_list`), não reconsultado nesta auditoria: **"Motion 1"**
(`id 323365585657985`, **30 s**, `hasAudio: true`). 30 s **não** cabe em `image_direction` →
com ele, use **`motion_direction`**.

`image_to_video` para A→B: `v3_0` tem `first_image`* + `tail_image` + `elements` (até 3),
`prefer_multi_shots` (default true) e `enable_audio` (default true). `v2_6` exige 1080p para
`tail_image` e **não** suporta áudio com tail image.

## 3. Doutrina do prompt (o que escrever e o que NÃO escrever)

**Princípio central:** no `motion_control` **o movimento vem da fonte** (vídeo/`motionId`), não do
texto. O prompt descreve **cena, expressão e contexto**, e fixa o que **não pode mudar**. Se você
re-escrever o movimento em detalhe, ele compete com a fonte e o resultado serpenteia.

**Escreva (nesta ordem):**
1. `<<<id>>>` + âncora de identidade ("keep the same face, hair, stubble, jacket").
2. Âncora de cena/luz/figurino ("preserve the table and the lighting exactly as in the image").
3. Expressão/direção do olhar no **começo e no fim** ("starts attentive; ends quiet and still,
   eyes on the person to camera-right").
4. Restrições: "one continuous shot, no cuts", "no camera movement" (se travada) ou o movimento de
   câmera desejado, "nobody else enters the frame", "no hands near his face", "no face morph".
5. Áudio, se houver: "quiet room tone only, no music".

**Não escreva:**
- Passo a passo de braços/pernas (a fonte manda). No `motion_control`, no máximo ancore **início e
  fim** do deslocamento, **alinhados ao vídeo**.
- Direção contrária à do vídeo de origem (perna esquerda vs direita, girar para o lado oposto).
- Nome de figura histórica nem descrição de rosto de figura.
- Frases que peçam corte/câmera móvel quando a fonte é travada.

Idioma: **inglês** (como o resto do projeto; é também idioma de áudio nativo suportado).

## 4. Regras de entrada (decisivas para a qualidade da transferência)

- **Imagem-sujeito**: nítida, bem iluminada, enquadramento compatível com o vídeo (corpo inteiro
  para caminhada). Prefira um keyframe de corpo inteiro já aprovado.
- **Vídeo de movimento**: um sujeito só, corpo e rosto visíveis, luz limpa. MP4/MOV. 3–10 s para
  `image_direction`.
- **Orientação tem que bater**: se o sujeito encara a câmera-direita, o vídeo de movimento também
  deve tender a esse lado. `image_direction` conserva a orientação da imagem; `motion_direction`
  conserva a do vídeo — escolha a que casa com a cena.
- **Direitos**: prefira **gravação própria** (a mão do próprio Andre, a caminhada do próprio
  Andre). A biblioteca da conta é aceitável; vídeo de terceiros tem risco de direitos.
- **Áudio**: `keepOriginalSound` default **true** traz o som do vídeo. Para não reter o áudio da referência, `false`; confirmar silêncio no QC.

## 5. Exemplos didáticos — não executar sem revisão e autorização

### T1 · `motion_control` com movimento salvo (`motionId`) — o caso A→B sem gravar nada

```bash
kling motion_control --model kling-video-v3_0 \
  --image projects/andre-time-travel/02_references/keyframes/andre/KF-<shot>-fullbody.jpg \
  --motionId 323365585657985 \
  --motionDirection motion_direction \
  --resolution 1080p --keepOriginalSound false \
  --elements '[{"id":"323525046658711","bindName":"Andre"}]' \
  --rationale "Transfer a recorded A-to-B movement onto the approved Andre keyframe; silent shot" \
  --skill-name kling-cli --skill-version 0.2.1 --poll 300 \
  "<<<323525046658711>>> keeps his exact face, hair, stubble and the mid-grey pinstripe jacket. He starts seated at the near side of the oak table and ends standing beside the chair, eyes staying on the person to camera-right. Preserve the table and the lighting exactly as in the image. One continuous shot, no cuts, nobody else enters the frame, no hands near his face, no face morph. Quiet room tone only, no music."
```

> O caminho do deslocamento vem do movimento salvo. O prompt só fixa quem é, onde começa/termina e
> o que não muda. Use `motion_direction` porque "Motion 1" tem 30 s (> 10 s).

### T2 · `motion_control` com gravação própria (`--video`)

```bash
# 1) subir o vídeo de movimento (mesmo mecanismo do --image; retorna URL pública)
kling file_upload projects/andre-time-travel/07_generations/inputs/MC-andre-walk-A-to-B.mp4 -q \
  --skill-name kling-cli --skill-version 0.2.1
# 2) aplicar
kling motion_control --model kling-video-v3_0 \
  --image projects/andre-time-travel/02_references/keyframes/andre/KF-<shot>-fullbody.jpg \
  --video <URL-do-file_upload> \
  --motionDirection image_direction \
  --resolution 1080p --keepOriginalSound false \
  --elements '[{"id":"323525046658711","bindName":"Andre"}]' \
  --rationale "Transfer the performer's own A-to-B walk (clean rights) onto the approved keyframe" \
  --skill-name kling-cli --skill-version 0.2.1 --poll 300 \
  "<mesmo prompt do T1>"
```

> A gravação precisa ter **3–10 s** para `image_direction`. Se tiver mais, use `motion_direction`.

### T3 · A→B controlado por primeiro/último quadro (mais determinístico)

```bash
kling image_to_video --model kling-video-v3_0 \
  --image     projects/andre-time-travel/02_references/keyframes/andre/KF-<shot>-A-seated.jpg \
  --tailImage projects/andre-time-travel/02_references/keyframes/andre/KF-<shot>-B-standing.jpg \
  --duration 5 --resolution 1080p --imageCount 1 \
  --prefer_multi_shots false --enable_audio false \
  --elements '[{"id":"323525046658711","bindName":"Andre"}]' \
  --rationale "A-to-B blocking locked by first and last frame; silent shot" \
  --skill-name kling-cli --skill-version 0.2.1 --poll 180 \
  "<<<323525046658711>>> rises from the chair at the near side of the table and comes to a stand beside it, in one continuous movement, ending exactly as in the final frame. His eyes stay on the person to camera-right. Locked camera, no camera movement, one continuous shot, no cuts. Preserve his face, hair, stubble, jacket, the table and the lighting exactly as in the image. Nobody else enters the frame; no hands near his face."
```

> Regra do T3: o **último quadro manda no fim do movimento**. Vale `v3_0`, `v2_5`, `v2_6`.
> `v2_6` exige 1080p e não aceita áudio com tail image. `turbo` **não** tem `tail_image`.

### T4 · Movimento simples sem quadro final (`image_to_video` puro)

Uma ação, com direção e resultado; cláusulas de travamento e preservação. Envelope testado:
piscada, respiração, virada de poucos graus. **Giros grandes/andar: não testado** — exigem quadros
(tail) ou fonte de movimento (motion_control), não confie só no texto.

## 6. Exemplos preenchidos (Andre, este filme)

- **Andre levanta e sai do quadro** → T3 (A = sentado, B = de pé fora do quadro) ou T1 (movimento
  salvo). Nunca peça "walk out of frame" só no texto.
- **Andre inclina sobre a mesa e volta** → T1/T4. É pequeno o bastante para texto; manter 3–5 s.
- **Andre entra e senta** → T3 com B = sentado.
- **Mão que pressiona e para (inserto, sem rosto)** → `image_to_video` `turbo` (feito: G-01) ou
  `motion_control` com gravação da própria mão, **se** a imagem-sujeito tiver pessoa/animal claro.

## 7. Armadilhas (checar antes de submeter)

- "Motion 1" tem 30 s → `image_direction` **falha**. Use `motion_direction`.
- `keepOriginalSound` default **true** → vem áudio não pedido. Para não reter o áudio da referência, `false`; confirmar silêncio no QC.
- `elements` no `motion_control` tem **limite 1** (e só no `v3_0`).
- Movimento grande + duração longa → deriva de identidade [INFERÊNCIA]. Teste 3–5 s em 720p antes de 1080p.
- Orientação invertida entre imagem e vídeo → resultado torto. Alinhe antes.
- Reflexo que revele rosto de figura histórica → descartar (regra do projeto).
- `turbo` não aceita `tail_image` nem `elements`.

## 8. Perguntas de teste — orçamento pendente

| # | Pergunta | Config | Custo |
|---|----------|--------|-------|
| MC-01 | `image_direction`/`motion_direction` transfere um A→B e segura a identidade? | `motion_control` `v3_0` · 720p · `keepOriginalSound false` · Element | sem cotação; referência registrada = 30 s |
| MC-02 | Mesmo teste em produção | idem · 1080p | sem cotação; referência registrada = 30 s |
| T3-mini | `tail_image` fecha A→B sem estragar identidade? | `image_to_video` `v3_0` · 5 s · 1080p · mudo | 40 era estimativa histórica para 5 s, não cotação |

Uma pergunta por job, **um job por vez** (`12`, seção 4). Rascunhos bloqueados em
`motion-control-specs.json`.

## Correção de orçamento (auditoria 2026-10-12)

O motionId deste pacote referencia 30 s segundo o registro anterior, não 5 s. O prompt não encurta esse ativo. As antigas estimativas de 45/60 créditos não se aplicam. Mesmo usando a taxa histórica de 9/12 cr/s apenas como hipótese, seriam 270/360 para 30 s; isso **não é preço confirmado**. Uma referência curta precisa de arquivo/ID próprio, duração medida e aprovação específica. Não criar/uploadar esse ativo durante diagnóstico.
