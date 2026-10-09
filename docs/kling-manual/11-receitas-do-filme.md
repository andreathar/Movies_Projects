# 11 · Receitas para *The Table Between Centuries*

Cada receita aponta o processo, o modelo, a evidência e o que ainda falta. Nenhuma delas autoriza gasto. Comandos completos estão nos guias numerados; aqui só a decisão e os pontos de atenção. Evidência = o que foi pago e verificado no projeto, salvo indicação.

## R1 · Keyframe do Andre numa época (still)
`image_to_image` · `kling-image-o1` · Element Andre · 2K · 16:9 · ~1 cr [PROJETO, D11]
Entradas: `image_1` foto real aprovada (capa), `image_2` mesa J26, `image_3` placa da época. Composição em terços primeiro, depois rosto (`图片1`), figurino D02, mesa, luz, expressão. Ver `04`.
Atenção: "só ele no quadro" não basta; escreva "nobody else, no silhouette, no hand, no shadow of a person, no reflection".

## R2 · Variante de escuta
Mesmo modelo, partindo do quadro de fala **já aceito**: "Edit 图片1 minimally… change only the expression". Parede vazia sem referência fez o modelo colar a foto de entrada [PROJETO].

## R3 · Placa sobre o ombro, sem Andre (Fase A do Galileu)
Hoje: `request.json` com `gemini-3-pro-image` e **5 imagens para 2 slots** (preflight: ERROR `SLOT_COUNT`) [LIVE + PROJETO, risco R08].
Opções, nenhuma decidida por mim:
1. **request-r2 com 2 entradas** no mesmo modelo (~20 cr por imagem, 1 imagem): escolher as 2 que mais importam (candidatas: âncora da mesa e placa de Arcetri) e descrever o resto em texto. Menor mudança; precisa de confirmação direta do Andre (D16).
2. Mesmo conteúdo em modelo com 10 slots (`kling-image-o1`, ~1 cr/imagem; ou `gemini-3.1-flash-image`, ~15 cr). Mudança de modelo exige revisão nova.
3. Dividir em duas etapas (placa vazia → composição).
Em qualquer caso: rodar o preflight, esperar ERROR zero.

## R4 · Só olhos do interlocutor
Still: `image_to_image` · `gemini-3.1-flash-image` · `aspect_ratio 4:1` · ~15 cr [PROJETO R2].
Vídeo: a entrada 4:1 foi **rejeitada sem cobrança**. Preencher para 5:2 com barras pretas (sem esticar):

```bash
ffmpeg -i olhos_4x1.png -vf "scale=1516:-2,pad=1516:604:0:(oh-ih)/2:black" olhos_5x2.png
```
Depois `image_to_video` · `kling-video-v3_0_turbo` · 5 s · 720p · `first_image` única (40 cr) com "locked framing, preserve the black bars" [PROJETO G-03/G-05]. Nenhum Element, nenhum áudio. Direção do olhar no prompt do vídeo.

## R5 · Inserto abaixo do pescoço (mão que pressiona e para)
`image_to_video` · `v3_0_turbo` · 10 s · 720p = 80 cr [PROJETO G-01 v2], com a cláusula de câmera travada. Variante com gesto controlado: `motion_control` com gravação da própria mão (`09`) [NÃO TESTADO].

## R6 · Andre ouvindo (mudo)
`image_to_video` · `kling-video-v3_0` · 5 s · 720p · Element · `prefer_multi_shots false` · `enable_audio false` = 30 cr pela tabela [PROJETO]. Ação: piscada e respiração, ou virada de poucos graus e volta. Perfil, giro grande, mão no rosto, câmera móvel: **não testados**.

## R7 · Andre falando em inglês
`image_to_video` · `kling-video-v3_0` · 8 s · 720p · `enable_audio true` · Element com voz = 72 cr [PROJETO PILOT-04]. Duração = fala medida + ≥ 2 s. STT contra o texto canônico (`13`).

## R8 · Imagem de época, sem rosto
Duas rotas [NÃO TESTADAS]: (a) animar uma placa existente (R1-J27…J32) com `image_to_video` muito sutil; (b) `text_to_video` de ambiente vazio (`07`). Sempre "no people, no reflections of people".

## R9 · Match-cut da mancha da mesa
Ideia [INFERÊNCIA]: terminar um take no detalhe da mancha de anel usando `tail_image` (`kling-video-v3_0`) para ligar o plano seguinte (D04). Teste 5 s, 720p, mudo = 30 cr.

## R10 · Outras línguas
Boca escondida primeiro (R4/R5/costas); depois testes de `motion_control` com a fala gravada do Andre; só então serviços externos (`10`, `15`).

## Pacote de testes pequenos propostos (pedir autorização ao producer; custos pela tabela do `12`)

| # | Pergunta | Config mínima | Custo estimado |
|---|---|---|---|
| T1 | `tail_image` fecha no detalhe da mesa sem estragar identidade? | v3_0, 5 s, 720p, mudo | 30 |
| T2 | Sintaxe de citação em `omni_ref_video` | v3_0_omni, 3 s, 720p, 1 img + 1 vídeo curto, sem áudio | ~27 |
| T3 | `motion_control` transfere boca e voz da fala do Andre? | v3_0, 5 s, 720p, `keepOriginalSound true` | ~45 |
| T4 | Element da mesa estabiliza J26-2? | 1 still `kling-image-o1` com Element Items | 1 + criação do Element |

Total dos T1–T3: ~100 créditos, 0,3% do saldo de 31.621. Cada um é um job separado, com `auth` próprio, rodado **um por vez** (`12`, seção 4).
