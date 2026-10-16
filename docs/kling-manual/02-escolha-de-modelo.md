# 02 · Escolha de modelo: "quero X → use Y"

> Atualização 16/10/2026: consultar [contrato V4 por interface](19-kling4-migration.md) e `shared/kling-capabilities.json` antes de escolher rota/custo. Tabelas e pilotos anteriores abaixo são evidência datada, sem liberação nova.

Colunas de evidência: **[PROJETO]** = já pago e verificado aqui; **[LIVE]** = só existe na ficha de hoje; **[NÃO TESTADO]** = plausível, nunca rodado no filme.
Confirme sempre na ficha `03-modelos-ao-vivo.md`: este arquivo resume, não substitui.

## Imagem

| Quero | Ferramenta · modelo | Detalhes-chave | Evidência |
|---|---|---|---|
| Keyframe do Andre fiel à foto, com mesa e época | `image_to_image` · `kling-image-o1` + Element | `image_1`=foto real, `image_2`=mesa, `image_3`=época; ~1 cr por 2K | [PROJETO] D11 |
| Mesma coisa com `kling-image-v3_0_omni` | idem | derivou 2/2 com Element, não usar | [PROJETO] |
| Só olhos / expressão sutil de interlocutor | `image_to_image` · `gemini-3.1-flash-image`, `aspect_ratio 4:1` | "Edit image 1… change ONLY…"; identidade 5/5 | [PROJETO] R2 |
| Placa de cenário a partir de poucas referências | `image_to_image` · `gemini-3-pro-image` | **só 2 slots** (`image_1`, `image_2`); `img_resolution` obrigatório | [LIVE] + risco R08 |
| Mais de 2 referências (até 10) | `kling-image-o1`, `kling-image-v3_0`, `kling-image-v3_0_omni`, `gemini-3.1-flash-image`, `gpt-image2` | 10 slots (`image_1..10`) | [LIVE] |
| Separar sujeito / cena / estilo em slots | `kling-image-v2_1` | `subject_image_0..3`, `scene_image`, `style_image`; sem Elements | [LIVE] [NÃO TESTADO] |
| Imagem sem referência | `text_to_image` · qualquer; padrão `kling-image-v3_0_omni` | Element não funciona aqui | [LIVE] |
| 4K | `kling-image-v3_0_omni`, `gemini-3-pro-image`, `gemini-3.1-flash-image`, `gpt-image(2)` | `kling-image-o1`/`v3_0` vão só até 2K | [LIVE] |

## Vídeo

| Quero | Ferramenta · modelo | Detalhes-chave | Evidência |
|---|---|---|---|
| Animar keyframe do Andre (identidade) | `image_to_video` · `kling-video-v3_0` + Element | `prefer_multi_shots false`, 720p nos pilotos | [PROJETO] |
| Andre falando em inglês (voz presa ao Element) | `image_to_video` · `kling-video-v3_0`, `enable_audio true` | fala exata no prompt + pausa + silêncio; 8 s para ~7,8 s de fala | [PROJETO] PILOT-04/05 |
| Reação só dos olhos (formato 5:2) | `image_to_video` · `kling-video-v3_0_turbo` | 1 `first_image`, sem Element/áudio/multi-shot; entrada 4:1 foi rejeitada sem cobrar | [PROJETO] G-03/G-05 |
| Mão/objeto abaixo do pescoço | `image_to_video` · `kling-video-v3_0` ou `turbo` | cláusula "locked camera" | [PROJETO] |
| Quadro final controlado (início → fim) | `image_to_video` · `kling-video-v3_0` com `tail_image` (v2_5, v2_6 também) | `v3_0_turbo` não tem `tail_image` | [LIVE] [NÃO TESTADO] |
| Várias imagens de referência no mesmo vídeo | `image_to_video` · `kling-video-v3_0_omni` ou `kling-video-o1` (`image_1..7`) | tem `aspect_ratio`; papel dos slots não confirmado | [LIVE] [NÃO TESTADO] |
| Cena sem imagem | `text_to_video` · `kling-video-v3_0_omni` (padrão) | sem Elements | [LIVE] [NÃO TESTADO] |
| Vídeo de referência (estilo/câmera) ou editar vídeo | `omni_ref_video` · `kling-video-v3_0_omni` | `video_1`, até 7 Elements, vídeo-Element | [LIVE] [NÃO TESTADO] |
| Fazer o Andre repetir um movimento | `motion_control` · `kling-video-v3_0` | foto + um vídeo ou `motionId` | [LIVE] [NÃO TESTADO] |
| 4K ou mais de 10 s (até 15 s) | `kling-video-v3_0` ou `v3_0_omni` | `turbo` só 720p/1080p; `o1` e `v2_x` máx. 10 s | [LIVE] |
| Rascunho barato | resolução `720p`, sem áudio, `imageCount 1` | custo cresce linear com segundos | [OFICIAL] |

## Árvore de decisão rápida

1. Precisa de **identidade do Andre**? → tem que ter Element (`05`) → `image_to_image` ou `image_to_video` (nunca `text_to_*`).
2. Tem que **falar**? → `kling-video-v3_0` + `enable_audio true` + Element com voz. Idioma fora de EN/ZH/JA/KO/ES? → `10`.
3. É **só olhos/inserto**? → `turbo` com canvas 5:2 (`11`).
4. Quer **reproduzir um movimento**? → `motion_control` (`09`).
5. Tem **vídeo de referência**? → `omni_ref_video` (`08`).
6. Mais de 2 imagens de referência numa still? Não use `gemini-3-pro-image`.

## O que o CLI não faz [LIVE: nenhuma das 18 ferramentas cobre]

Lip-sync de vídeo existente, Avatar (foto + áudio), extensão de vídeo, upscale, Effects, criação/clonagem de Voz em biblioteca, Canvas Agent. Existem no app/API do Kling ou em outros serviços: `15-ferramentas-nao-listadas.md`.
