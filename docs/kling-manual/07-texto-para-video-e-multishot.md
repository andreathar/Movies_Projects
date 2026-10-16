# 07 · Texto → vídeo e multi-shot (`text_to_video`)

> Atualização 16/10/2026: consultar [contrato V4 por interface](19-kling4-migration.md) e `shared/kling-capabilities.json` antes de escolher rota/custo. Tabelas e pilotos anteriores abaixo são evidência datada, sem liberação nova.

Nunca usado no filme até hoje [NÃO TESTADO]. Serve para cenas sem pessoa conhecida: ambientes vazios, objetos, atmosfera, imagens de época sem rosto. **Não aceita Element** nem `<<<id>>>` [OFICIAL]: se a cena precisa do Andre, é `image_to_video`.

## Modelos [LIVE]

| Modelo | Duração (s) | Resolução | `aspect_ratio` | Áudio | Multi-shot |
|---|---|---|---|---|---|
| `kling-video-v3_0_omni` (padrão) | 3–15 | 720p, 1080p, 4k | 16:9, 9:16, 1:1 | `enable_audio` (true) | `prefer_multi_shots` (false) |
| `kling-video-v3_0` | 3–15 | 720p, 1080p, 4k | idem | idem (true) | idem (**true**) |
| `kling-video-v3_0_turbo` | 3–15 | 720p, 1080p | idem | sem controle | não |
| `kling-video-o1` | 3–10 | 720p, 1080p | idem | não | não |
| `kling-video-v2_6` | 5 ou 10 | 720p, 1080p | idem | `enable_audio` | não |
| `kling-video-v2_5` | 5 ou 10 | 720p, 1080p | idem | `enable_audio`, `enable_asmr`, `audio_prompt`, `music_prompt` | não |

Todos: `imageCount` 1–4 (custo multiplica). Sempre passe `--model`.

## Fórmula de prompt [OFICIAL, guia do VIDEO 3.0 via playbook; NÃO TESTADO no CLI]

`Cena/ambiente → sujeito → ações em sequência → câmera → áudio e estilo`

O VIDEO 3.0 segue ações sequenciais ("primeiro… depois… por fim…") e linguagem de direção de fotografia. Prompts em inglês; só o diálogo vai no idioma-alvo.

```bash
kling text_to_video --model kling-video-v3_0_omni \
  --duration 5 --resolution 720p --aspect_ratio 16:9 --imageCount 1 \
  --prefer_multi_shots false --enable_audio false \
  --rationale "Empty-room atmosphere plate, no people, for edit rhythm" \
  --skill-name kling-cli --skill-version 0.2.1 --poll 180 \
  "A small domestic room at dusk, a pale oak table in the left third, empty chairs, window light slowly dimming. Locked camera, no camera movement, one continuous shot. Dust motes drift in the light. No people, no shadows of people, no reflections of people."
```
(Comando-modelo: **não executado**.)

## Multi-shot

- **Implícito**: `--prefer_multi_shots true` e o prompt descreve plano e contraplano; o modelo escolhe os cortes.
- **Personalizado**: dentro do prompt, um bloco por plano com duração e câmera. Estrutura sugerida pelos guias da Kling [OFICIAL via skills de terceiros; formato exato no CLI não testado]:

```
Shot 1 (3s): wide, empty oak table at dusk. Camera: static.
Shot 2 (4s): close on the ring stain, light shifts. Camera: slow push in.
Shot 3 (3s): hold on the table, silence. Camera: static.
```

- A soma dos planos precisa fechar a `duration` (3 + 4 + 3 = 10). Um multi-shot é **um único job** cobrado como um vídeo; não gere um job por plano a menos que o producer aprove separado.
- Use multi-shot só quando mudam local, tempo, escala ou informação. Para plano editorial único: `--prefer_multi_shots false`.

## Vocabulário de câmera que o modelo entende [OFICIAL via guia; TERCEIROS para a lista]

`static / locked off`, `slow push in`, `pull back`, `pan left/right`, `tilt up/down`, `orbit`, `tracking shot`, `crane up/down`, `low angle`, `POV`. Um movimento principal por plano de 5 s. Para este filme o padrão é **câmera travada**.

## Armadilhas

- Texto na imagem (letras) costuma deformar; diga "no readable text".
- Sem rosto de figura histórica: não descreva rostos; o modelo pode inventar um.
- Defaults de `v3_0`: `prefer_multi_shots=true` e `enable_audio=true`. Defina os dois.
- 4K custa ~30 cr/s [OFICIAL]. Trave composição e prompt em 720p/1080p antes.
