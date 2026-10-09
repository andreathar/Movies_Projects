# 06 · Imagem → vídeo (`image_to_video`)

Ferramenta central do filme: o quadro (still aprovado) dá o visual; o prompt dá só o movimento.

## Modelos e o que cada um aceita [LIVE]

| Modelo | Slots de mídia | Duração (s) | Resolução | Outros argumentos | Elements |
|---|---|---|---|---|---|
| `kling-video-v3_0` (padrão) | `first_image`*, `tail_image` | 3–15 | 720p, 1080p, **4k** | `prefer_multi_shots` (padrão **true**), `enable_audio` (padrão **true**), `imageCount` | sim (imagem e vídeo) |
| `kling-video-v3_0_omni` | `image_1*`…`image_7` | 3–15 | 720p, 1080p, 4k | `aspect_ratio`, `prefer_multi_shots` (false), `enable_audio` (true) | sim |
| `kling-video-v3_0_turbo` | `first_image`* | 3–15 | 720p, 1080p | só `duration`, `resolution`, `imageCount` | **não** |
| `kling-video-o1` | `image_1*`…`image_7` | 3–10 | 720p, 1080p | `aspect_ratio` | sim (só imagem) |
| `kling-video-v2_6` | `first_image`*, `tail_image` | 5 ou 10 | 720p, 1080p | `enable_audio` | não |
| `kling-video-v2_5` | `first_image`*, `tail_image` | 5 ou 10 | 720p, 1080p | `enable_audio`, `enable_asmr`, `audio_prompt`, `music_prompt` | não |

\* obrigatório. `imageCount` 1–4 = quantos vídeos por pedido (custo multiplica).

## Os dois padrões que mudam tudo [LIVE + PROJETO]

- **`prefer_multi_shots` = true** em `v3_0`: o modelo pode cortar em vários planos. Para um plano editorial único, `--prefer_multi_shots false`.
- **`enable_audio` = true**: gera áudio e **custa mais** (~+50%, ver `12`). Para tomada muda, `--enable_audio false`.

## Comando-modelo (plano único, mudo) [PROJETO: parâmetros provados; comando não executado]

```bash
kling image_to_video --model kling-video-v3_0 \
  --image 07_generations/originals/<keyframe-aceito>.png \
  --duration 5 --resolution 720p --imageCount 1 \
  --prefer_multi_shots false --enable_audio false \
  --elements '[{"id":"323525046658711","bindName":"Andre"}]' \
  --rationale "Silent listening shot of Andre from approved keyframe, locked camera" \
  --skill-name kling-cli --skill-version 0.2.0 --poll 180 \
  "<<<323525046658711>>> sits listening. He blinks once and breathes slowly. Locked camera, no camera movement, one continuous shot, no cuts. Preserve his face, hair, stubble, jacket, the table and the lighting exactly as in the image. Nobody else enters the frame; no hands near his face."
```

Com quadro final: `--tailImage ./fim.png` junto de `--image`; ou endereçar os slots pelo nome, `--input first_image=./a.png --input tail_image=./b.png` (essa forma **não combina** com `--image`/`--tailImage`) [LIVE]. `tail_image` existe em `v3_0`, `v2_5`, `v2_6`; não em `turbo`.

## Como escrever o prompt (padrão do projeto)

1. `<<<id>>>` + **uma** ação, com direção e resultado.
2. "Locked camera, no camera movement, one continuous shot, no cuts."
3. "Preserve his face, hair, stubble, jacket, the table and the lighting exactly as in the image."
4. "Nobody else enters the frame; no hands near his face."
5. Direção do olhar escrita no vídeo ("eyes toward camera-left"), porque no still ela parece central.

Envelope **testado**: escuta parada com piscada e respiração; virada de poucos graus e volta; atenção→gravidade sob luz dura de cima (PILOT-01/02/03). **Não testado**: perfil, giros grandes, gestos de mão, movimento de câmera [PROJETO]. Não peça sem um teste novo e autorizado.

## Fala com áudio nativo (voz presa ao Element, D13) [PROJETO]

`--enable_audio true`, Element com `.mp3` de voz, e no prompt:

> `<<<id>>>` speaks calmly in English to the unseen person across the table, in a plain, warm, unhurried voice. Andre says: "<linha canônica exata>". He pauses briefly after "<palavra>", keeps his eyes on the person to camera-right, and falls silent after the last word. Quiet room tone only, no music.

- Fale/pausa/silêncio e nome do falante no mesmo parágrafo; **não** repita o tom da voz no prompt (a voz já está no Element) [OFICIAL via playbook].
- Duração = segundos medidos no scratch + ≥ 2 s de cauda. 8 s segurou 7,8 s de fala. Verificado por STT (`13`).
- Idiomas nativos: EN, ZH, JA, KO, ES (+ sotaques/dialetos). Latim, mongol, toscano e córsego **não** são suportados → `10`.

## Rotina de submissão (para o producer)

1. Preflight sem ERROR. 2. `kling account` (saldo antes). 3. Enviar com `--poll`. 4. Anotar `generationId` e `creditsConsumed` da resposta. 5. Se travou: `kling query_tasks --poll 120 <generationId>`, **nunca reenviar**. 6. Baixar (24 h), sha256, `13`, ledger.

## Erros comuns

- Corte inesperado dentro do plano → `prefer_multi_shots` ficou true.
- Trilha/voz que ninguém pediu → `enable_audio` ficou true.
- [INFERÊNCIA] Rosto deriva em takes longos ou ações grandes → reduzir duração/ação, manter 720p no piloto e `imageCount 1`.
- Entrada 4:1 rejeitada → `11` (canvas 5:2 com barras pretas).
