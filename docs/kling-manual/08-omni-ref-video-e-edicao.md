# 08 · `omni_ref_video`: referências mistas e edição de vídeo

Ferramenta mais nova e mais flexível: texto + imagens + vídeo(s) + Elements (+ áudio) num único pedido [OFICIAL, descrição da ferramenta]. **Nunca usada no filme** [NÃO TESTADO].

> Achado [LIVE, 2026-10-09]: `omni_ref_video` existe no CLI 0.2.1 (`kling omni_ref_video --help`) e no servidor 1.3.3. À época **não aparecia** no `skills/kling-cli/SKILL.md` 0.2.0; a skill foi atualizada para **0.2.1** em 2026-10-12 e agora documenta a ferramenta. Este guia cobre o uso.

## Declaração viva [LIVE]

| Item | `kling-video-v3_0_omni` (padrão) | `kling-video-o1` |
|---|---|---|
| Slots | `image_1..7`, `video_1` | `image_1..7`, `video_1` |
| Duração | 3–15 s | 3–10 s |
| Resolução | 720p, 1080p, **4k** | 720p, 1080p |
| `aspect_ratio` | `auto`, 16:9, 9:16, 1:1 (padrão `auto`) | 16:9, 9:16, 1:1 |
| Áudio | `enable_audio` (true), `keepOriginalSound` (false) | não declara |
| Multi-shot | `prefer_multi_shots` (false) | não |
| Elements de imagem | até 7 | até 7 |
| Elements de vídeo | até 3 (1 se também há `video_1`) | não |
| Voz dos Elements | `voiceConsistency: true` | — |

Limites combinados (Elements + `image_` + `video_`): no máximo **8** itens no total; se houver **qualquer** `video_`, no máximo **4** entre Elements e imagens; sem vídeo, até **7**.

Divergência aberta: a descrição fala em `video_1..video_5` e `audio_1..audio_3`, e o CLI tem `--audio`, mas o `who_am_i` só declara `video_1` e nenhum `audio_N`. O preflight avisa (`OMNI_AUDIO_SLOT`). Não dependa de áudio de referência sem um teste.

## Comando-modelo [NÃO TESTADO]

```bash
kling omni_ref_video --model kling-video-v3_0_omni \
  --image ./estilo.png --video ./referencia.mp4 \
  --duration 5 --resolution 720p --aspect_ratio auto --imageCount 1 \
  --prefer_multi_shots false --enable_audio false --keepOriginalSound false \
  --rationale "Edit test: keep camera and motion of the reference clip, restyle with the image" \
  --skill-name kling-cli --skill-version 0.2.1 --poll 180 \
  "<prompt>"
```

`--image` repetível vira `image_1..`; `--video` vira `video_1`; `--audio` vira `audio_1..`; slots fora desse padrão: `--input nome=url|caminho`. Elementos: `--elements '[{"id":...,"bindName":...}]'` + `<<<id>>>` no prompt.

## Como citar as referências no prompt: **não confirmado**

Três convenções aparecem nas fontes; qual vale para o CLI nesta ferramenta não foi verificado:

1. `图片N` / `视频N` literais (usadas pelo projeto em `image_to_image`/`image_to_video`, playbook §1).
2. "image 1 / image N" (texto de `image_to_image`).
3. `@video`, `@image` (exemplos do app e das notas de lançamento do VIDEO 3.0 Omni [OFICIAL via terceiros]).

**Teste mínimo sugerido (precisa de autorização do producer):** 3 s, 720p, sem áudio, `imageCount 1`, 1 imagem + 1 vídeo curto, sem Element. Estimativa [INFERÊNCIA a partir da tabela de unidades ×10]: 0,9 U/s ≈ 9 cr/s com vídeo de entrada ⇒ ~27 cr; confirme com `creditsConsumed` e ledger. Rode o mesmo prompt trocando só a convenção de citação em jobs separados só se o primeiro falhar.

## Edição de vídeo (VIDEO 3.0 Omni) [OFICIAL via notas de lançamento 2026-06-17, lidas em skill de terceiros]

- Entrada de vídeo de **3 a 15 s**, saída até **15 s**; 4K de entrada e saída.
- Receita das amostras oficiais: **uma** intenção de edição por pedido; nomeie a mudança em uma oração; depois uma **lista do que não muda** (ângulo de câmera, trajetória, layout, posição); para algo composto, a cláusula física: "lighting and shadows match the target environment, natural, non-composited look, no sticker-like artifacts".

Exemplos de forma (adaptar; não executar):
- Trocar objeto mantendo movimento: "Replace the trophy in the video with the toy figurine shown in the reference image."
- Mudar atributo: "Change the colour of the parrot's feathers to match the reference image. Keep all other elements of the video unchanged."

### Para este filme

Possíveis usos [INFERÊNCIA, a testar]: limpar um elemento indesejado de um take aceito sem refazer a cena; trocar a época de um objeto na mesa; unificar luz entre takes. Risco: reprocessar um rosto aceito pode alterar a identidade. Só testar em take **descartável** e comparar com o original antes de qualquer aceitação.
Regra do projeto: o vídeo original aceito não é sobrescrito; o resultado entra como novo take com novo ID e sha256.

## Custos (unidades ×10 = créditos; ver `12`) [INFERÊNCIA a partir de OFICIAL]

Omni sem vídeo de entrada, sem áudio: 0,6/0,8 U/s (720p/1080p). Com áudio: 0,8/1,0. **Com vídeo de entrada, sem áudio: 0,9/1,2.** 4K: 3,0 U/s em qualquer configuração.
