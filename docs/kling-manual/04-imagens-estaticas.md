# 04 · Imagens estáticas: `text_to_image` e `image_to_image`

> Atualização 16/10/2026: consultar [contrato V4 por interface](19-kling4-migration.md) e `shared/kling-capabilities.json`. Evidências anteriores são datadas; anúncio não amplia a CLI atual.

## Quando cada uma

- `text_to_image`: nasce só de texto. **Não aceita Element** (nem `<<<id>>>`) [OFICIAL].
- `image_to_image`: edita ou recompõe a partir de 1 a 10 referências (depende do modelo). É a ferramenta de qualquer still com identidade, mesa ou placa de época.

## Comando-modelo

```bash
kling image_to_image --model kling-image-o1 \
  --image 02_references/andre/approved/cover_20240202_015341_hs34.jpg \
  --image 02_references/table/R1-J26-table-anchor_2.png \
  --image 02_references/table/R1-J29-plate-arcetri-1634_1.png \
  --img_resolution 2k --aspect_ratio 16:9 --imageCount 1 \
  --elements '[{"id":"323525046658711","bindName":"Andre"}]' \
  --rationale "Andre keyframe at the oak table, Arcetri plate, identity from approved cover photo" \
  --skill-name kling-cli --skill-version 0.2.1 --poll 120 \
  "<<<323525046658711>>> with EXACTLY the face of 图片1 ..."
```

[PROJETO] Estrutura e marcador `图片N` vêm do playbook e do D11. `--poll 120` espera o resultado no mesmo comando; sem ele, use `kling query_tasks --poll 120 <generationId>`. O comando acima é modelo: **não executado**.

Regras do CLI [LIVE]:

- `--image` é repetível; a **ordem** preenche `image_1`, `image_2`, … na ordem dos slots do modelo.
- Argumentos em snake_case ou camelCase. `gemini-3-pro-image` declara `image_count` (snake) e `img_resolution` obrigatório.
- No prompt, as referências são `图片1`, `图片2`… (literal, não traduzir) ou "image 1/image N" conforme a declaração do modelo.

## Modelos de imagem hoje [LIVE]

| Modelo | Slots | Resoluções | Aspect ratios | Elements | Observação |
|---|---|---|---|---|---|
| `kling-image-o1` | 10 | 1k, 2k | auto + 8 | sim | rota provada do Andre (D11) |
| `kling-image-v3_0_omni` | 10 | 1k–4k | auto + 8 | sim; `story_mode` | padrão de `text_to_image`; derivou no teste |
| `kling-image-v3_0` | 10 | 1k, 2k | auto + 8 | sim | não testado no filme |
| `kling-image-v2_1` | slots nomeados (sujeito 0-3, cena, estilo) | 1k, 2k | 8 | não | não testado; entradas opcionais |
| `gemini-3.1-flash-image` | 10 | 0.5k–4k | 14 formatos, inclui 4:1, 1:8, 8:1 | não | provado para olhos 4:1 |
| `gemini-3-pro-image` | **2** | 1k–4k | 10 formatos | não | `image_count`, `img_resolution` obrigatório |
| `gpt-image2` (i2i) / `gpt-image-2` (t2i) | 10 | 1k–4k | 10 | não | `quality` low/medium/high; nome muda entre ferramentas |

`imageCount`: até 9 por pedido; **custo multiplica**. `kling-image-v3_0_omni` aceita `-1` (ver ficha; semântica não confirmada [NÃO TESTADO]).

## Padrões que funcionaram [PROJETO]

1. **Composição primeiro, em terços**, depois identidade, figurino, mesa, época/luz, expressão por último (playbook §1).
2. "Só ele no quadro" **não basta**: já gerou cabeça de interlocutor. Diga explicitamente "nobody else, no silhouette, no hand, no shadow of a person, no reflection".
3. Variante de escuta: edite o quadro de fala já aceito ("Edit 图片1 minimally… change only the expression"). Prompt de parede vazia fez o modelo colar a foto de referência.
4. Olhos (4:1): "Edit image 1. Keep EXACTLY the same person… Change ONLY the expression, subtly…" com `gemini-3.1-flash-image`. Olhar parece central em still; diga a direção do olhar no prompt do **vídeo**.

## Armadilhas

- Mais referências que slots: excedente é descartado ou rejeitado. O preflight acusa `SLOT_COUNT`. É o caso do request da Fase A (5 imagens para 2 slots em `gemini-3-pro-image`) [LIVE+PROJETO].
- Elements só em modelos que listam `elements` na ficha. Em `image_to_image` só Elements de **imagem**; Element de vídeo exige `image_to_video` (`05`) [OFICIAL].
- Proporção de entrada: o texto das ferramentas diz "não mais larga que 1:2", mas no projeto uma entrada **5:2** foi aceita em vídeo e uma **4:1** foi rejeitada sem cobrança (`11`). Trate 2,5:1 como limite prático [PROJETO]; o preflight dá WARN acima de 1:2 e ERROR acima de ~2,5:1.
- Extensão trocada (.png que é JPEG): ver `01`.
- Resultado expira em 24 h: baixar, calcular sha256, registrar no ledger.
