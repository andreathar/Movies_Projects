# 18 · Guia de prompts: o que o Kling entende e o que este filme exige

> Atualização 16/10/2026: consultar [contrato V4 por interface](19-kling4-migration.md) e `shared/kling-capabilities.json` antes de escolher rota/custo. Tabelas e pilotos anteriores abaixo são evidência datada, sem liberação nova.

Pesquisa de 2026-10-13 (Claude, lane de preparação). Reúne a documentação oficial do Kling, as regras que os guias de terceiros concordam entre si e, acima de tudo, os prompts **já pagos e revisados neste projeto**. Nada aqui autoriza gasto, upload, Element ou aceite. Selos como no `README.md`: [LIVE] = schema do snapshot `who_am_i` 2026-10-12; [PROJETO] = job pago com ID no ledger; [OFICIAL] = kling.ai; [TERCEIROS] = tutoriais; [INFERÊNCIA] = conclusão minha.

## 1. Oito regras que valem para todos os modelos

1. **Prompt em inglês; só a fala no idioma-alvo.** Treino predominante EN/ZH; o guia oficial do VIDEO 3.0 traduz para inglês qualquer idioma de diálogo fora de ZH/EN/JA/KO/ES [OFICIAL]. Marcadores de contrato (`<<<id>>>`, `图片N`, `视频1`) ficam literais, sem tradução [LIVE].
2. **Em `image_to_video`, a imagem é o motor; o prompt é só movimento.** Fórmula oficial: `Sujeito + Movimento (+ Fundo + Movimento)`. Nunca redescreva a cena que já está no quadro; descrição que "desvia muito da imagem" provoca corte ou transição [OFICIAL, guia Image-to-Video]. Ação sem sujeito ("wear sunglasses") vira pan ou vídeo parado.
3. **Uma ação principal por plano, com ponto final.** "…holds there, then settles back" / "…falls silent after the last word". Ação aberta é a causa clássica de deriva e de geração presa [OFICIAL + TERCEIROS]. Física plausível: o guia oficial lista bolas quicando e arremessos como ainda difíceis.
4. **Câmera sempre explícita.** Sem instrução, o modelo improvisa [OFICIAL + TERCEIROS]. Padrão do filme: `Locked camera, no camera movement, one continuous shot, no cuts.` — a frase que segurou PILOT-01/02/04 [PROJETO].
5. **Ordem para `text_to_video`:** cena/ambiente → sujeitos → ações **em sequência** ("first… then… finally") → câmera → áudio e estilo [OFICIAL, guia VIDEO 3.0]. Em takes longos (até 15 s) marque os beats no tempo: "At the 4th second…", "In the final 3 seconds…" [OFICIAL].
6. **Exclusões vão no corpo do prompt.** Nenhum modelo v3/o1/omni do CLI declara `negative_prompt` [LIVE]. Escreva "No X, no Y" em frase própria e repita o que é crítico (`fixed`, `unchanged`, `never widens`).
7. **Fixe os dois defaults perigosos do `kling-video-v3_0`:** `prefer_multi_shots` (padrão **true**) e `enable_audio` (padrão **true**) [LIVE]. Corte inesperado e trilha não pedida são sempre esses dois, não o prompt (`14`).
8. **Tamanho:** 60–120 palavras em I2V, 100–200 em T2V/multi-shot [TERCEIROS]. Os prompts aprovados do projeto têm 55–95 palavras [PROJETO]. Mais que isso costuma ser redescrição de cena, não direção.

## 2. Tokens de referência: app ≠ CLI

| Quero referir | No app/web [OFICIAL] | No CLI deste projeto [LIVE] |
|---|---|---|
| Imagem de entrada N | `@Image1`, `@image` | `图片1`, `图片2`… (= `image_1`, `image_2`); em `kling-image-v3_0` também "image 1/N" |
| Element salvo | `@Nome` | `<<<323525046658711>>>` **e** `--elements '[{"id":"323525046658711","bindName":"Andre"}]'` |
| Vídeo de referência | `@video` | `视频1` (= `video_1`, só `omni_ref_video`) |
| Primeiro/último quadro | upload de start/end frame | `first_image` / `tail_image`; não há token no texto |

Não copie a sintaxe `@` de tutoriais para o spec: o schema declara os tokens acima e o preflight só confere estes. Marcador sem `elements` dá `ELEMENT_NOBIND`; `elements` sem marcador dá `ELEMENT_MARKER` (`05`). `text_to_*` não aceita Element nem `图片N` [LIVE].

## 3. Anatomia do prompt do filme (cinco blocos, nesta ordem)

Derivada dos cinco prompts pagos que ficaram dentro do envelope aceito (PILOT-01/02/04, G-03/G-05) [PROJETO]:

```
[1 SUJEITO]  <<<id>>> | "The man in the reference image" | "An old man's tired eyes"
[2 AÇÃO]     uma ação, direção espacial, causa dramática, ponto final
[3 CÂMERA]   Locked camera, no camera movement, one continuous shot, no cuts.
[4 PRESERVAR] Preserve his face, hair, stubble, jacket, the table and the lighting exactly as in the image.
[5 EXCLUIR]  Nobody else enters the frame; no hands near his face. [+ sem rosto histórico, sem texto, sem reflexo]
[6 ÁUDIO]    só se enable_audio=true: fala exata, pausa, silêncio, "quiet room tone only, no music"
```

Regras internas:

- **Direção do olhar no vídeo, não no still.** O still parece centrado; "eyes toward camera-right" no prompt do vídeo resolve (D09) [PROJETO].
- **Reação depois da causa.** A direção de 2026-10-09 exige que a reação conclusiva não anteceda a frase que a motiva. Escreva a causa no prompt ("as if a quiet question reached him") e uma só mudança ("one restrained change, no repeated blinking") [PROJETO F4].
- **Figura histórica = nunca descreva o rosto.** Descreva o que **está** no quadro (olhos em faixa, ombro desfocado, nuca, mãos, gola) e feche a exclusão: "No nose tip, no mouth, no face, no hand, no text" (G-03). Em T2V sem imagem, descrever um rosto é convite para o modelo inventar um [INFERÊNCIA + regra do projeto].
- **"Só ele no quadro" não basta.** Já gerou cabeça de interlocutor. Use "nobody else, no silhouette, no hand, no shadow of a person, no reflection" [PROJETO].
- **Não repita o timbre quando a voz está no Element.** O guia oficial diz para não redefinir o tom de voz vinculado; descreva só ritmo e intenção ("plain, warm, unhurried") [OFICIAL + PILOT-04].

## 4. Fala com áudio nativo

Sintaxe oficial do VIDEO 3.0: `Personagem (nota de entrega, idioma): "linha"` — ex.: `Mom (softly, in a surprised tone): "…"`; sotaque/dialeto nomeado entre parênteses [OFICIAL]. O padrão que funcionou aqui é equivalente em prosa [PROJETO PILOT-04]:

> `<<<id>>>` speaks calmly in English to the unseen person across the table, in a plain, warm, unhurried voice. Andre says: "{linha exata do CSV}". He pauses briefly after "{palavra}", keeps his eyes on the person to camera-right, and falls silent after the last word. Quiet room tone only, no music.

- Linha **exata** de `01_script/dialogue-lines.csv`, uma ou duas frases; monólogos quebram o lip-sync [TERCEIROS, consenso].
- `duration` = segundos medidos do áudio-guia + ≥ 2 s de cauda; 8 s segurou 7,8 s; G-L04 mede 8,62 s → não cabe em menos de 11 [PROJETO]. Não acelere a fala para caber.
- Peça o silêncio explicitamente ("falls silent after the last word", "no music"); nunca presuma mudo. Turbo não declara controle de áudio e devolveu trilha baixa nos A/B [PROJETO].
- D14: a voz Kling é guia. Nenhum prompt torna a voz aprovada.

## 5. Multi-shot e beats temporais

- `prefer_multi_shots=true` + prosa com plano/contraplano = o modelo corta sozinho (implícito). Personalizado: `Shot 1 (3s): … Camera: static.` por bloco, somando a `duration` [OFICIAL via guia + TERCEIROS]; o formato textual de duração **não foi testado no CLI** [NÃO TESTADO] e a API de desenvolvedor usa um campo `multi_prompt` que o CLI não expõe [LIVE].
- Para este filme, multi-shot só em placas sem Andre (ambiente, mesa, objetos). Planos com identidade continuam `prefer_multi_shots=false`, um job por plano, por causa do gate de todos os quadros (`13`).
- Defina o estilo visual uma vez no início e repita o mesmo descritor de personagem em todos os planos; é a regra de consistência que todos os guias repetem [TERCEIROS].

## 6. Templates por rota (preencha `{}`; use `production_plan.py template` quando a família existir)

**Keyframe com identidade** · `image_to_image` · `kling-image-o1` + Element (D11) [PROJETO]
```
<<<323525046658711>>> with EXACTLY the face of 图片1. Single cinematic still. Andre screen-left, looking camera-right, seated at the pale oak table of 图片2 (ring stain and chipped corner kept). {environment from 图片3}. Medium shot, 50 mm, seated eye level. Grey pinstripe jacket, white striped shirt open collar. Historical interlocutor: only a blurred shoulder and sleeve in the right foreground, entire head beyond the frame. Soft key from camera-left, natural skin texture, no retouching. No historical face, head, profile, ear or reflection. Nobody else, no silhouette, no shadow of a person, no readable text, no watermark.
```

**Variante mínima do mesmo master** · `image_to_image` [PROJETO padrão que evitou colagem]
```
Edit 图片1 minimally. Keep EXACTLY the same person, composition, seat, oak table, marks, wardrobe and light. Change ONLY {the expression to quiet listening, mouth closed}. Do not add a character, object or text. Do not recompose.
```

**Escuta / reação** · `image_to_video` · `kling-video-v3_0` · `enable_audio false` · `prefer_multi_shots false` [PROJETO PILOT-01/02]
```
<<<323525046658711>>> sits still and listens to the unseen person across the table. {One change: he blinks once naturally, his chest rises with a slow breath, his eyes stay on the person to camera-right.} Locked camera, no camera movement, one continuous shot, no cuts. Preserve his face, hair, stubble, jacket, the table and the lighting exactly as in the image. Nobody else enters the frame; no hands near his face.
```

**Fala** · `image_to_video` · `kling-video-v3_0` · `enable_audio true` · Element com voz — ver §4.

**Olhos em faixa 5:2** · `image_to_video` · `kling-video-v3_0_turbo` · 1 `first_image`, sem Element [PROJETO G-03/G-05]
```
The image is an eyes-only strip letterboxed with black bars above and below; keep the black bars exactly as they are, never fill them, never reveal more of the face. {An old man's eyes}, looking toward camera-left at someone speaking. {One reaction after the line: a single slow blink, then stillness.} Locked camera, no zoom, no pull-back, the frame never widens: it stays this exact eyes-only strip from the eyebrows to just under the lower eyelids for the whole shot. No nose tip, no mouth, no face, no hand, no text. One continuous shot.
```
Observado: duas piscadas em vez de uma em G-05; registre, não esconda [PROJETO].

**Detalhe abaixo do pescoço (mãos/mesa/pés)** · `image_to_video` · `enable_audio false` [F5, NÃO TESTADO em vídeo]
```
Locked detail. {One contact action: the fingertips press once on the wood, then lift.} Keep anatomy, cloth, table grain, ring stain, chipped corner and light unchanged. No head, no face, no reflected face, no pull-back, no speech.
```

**Placa de ambiente sem pessoas** · `text_to_video` · `kling-video-v3_0_omni` · `enable_audio false` · `prefer_multi_shots false` [NÃO TESTADO]
```
{Room at dusk, pale oak table in the left third, empty chairs, window light slowly dimming}. Locked camera, no camera movement, one continuous shot. Dust motes drift in the light; nothing else moves. No people, no shadows of people, no reflections of people, no readable text.
```

**Referência mista / edição** · `omni_ref_video` · `kling-video-v3_0_omni` [OFICIAL padrão de edição; NÃO TESTADO]
```
Use 视频1 as the motion and camera reference. Replace {one thing} with 图片1. Keep the original camera angle, motion path, spatial layout, positioning and everything else unchanged. Lighting and shadows match the target environment, natural non-composited look, no sticker-like artifacts.
```
Uma intenção de edição por job; `enable_audio=false` com `video_1` [LIVE].

**Motion control** · `motion_control` · `kling-video-v3_0` [F6, NÃO TESTADO]
```
<<<323525046658711>>> performs only the movement of the reference video. Preserve identity, wardrobe, framing and environment of the image. {Performance intention.} No historical face, head, profile, ear or reflection. No extra person, no readable text, no camera cut or orbit.
```

## 7. Checklist do prompt antes do preflight

1. Idioma: inglês; fala no idioma-alvo e idêntica ao CSV (ID da linha anotado no spec).
2. Tokens: `<<<id>>>` ↔ `elements`; `图片N` ↔ slots preenchidos, na ordem; nada de `@`.
3. Uma ação, uma causa, um ponto final. Direção espacial escrita (camera-left/right).
4. Frase de câmera presente. Para o filme: travada.
5. Lista de preservação + exclusões (rosto histórico, outra pessoa, mãos no rosto, texto, reflexo).
6. `prefer_multi_shots` e `enable_audio` definidos explicitamente; áudio coerente com o texto (silêncio pedido quando ligado).
7. `duration` = fala medida + ≥ 2 s; olhos/escuta 3–5 s; nada acima do envelope testado (perfil, giro grande, gesto de mão, câmera em movimento) sem teste autorizado.
8. Nenhuma palavra que descreva o rosto de uma figura histórica.
9. Rodar `python3 -I docs/kling-manual/tools/kling_preflight.py <spec> --json`; preflight valida contrato, não qualidade.

## 8. Antipadrões observados (não repetir)

| Prompt | O que aconteceu | Correção |
|---|---|---|
| "Only him in frame" | cabeça de interlocutor | exclusão explícita de silhueta/mão/sombra/reflexo [PROJETO] |
| Escuta "contra parede vazia" a partir da foto | modelo colou a foto de referência | derivar do keyframe aceito, "change only…" [PROJETO] |
| Element em `kling-image-v3_0_omni` | rosto derivou 2/2 | `kling-image-o1` [PROJETO] |
| Entrada 4:1 | rejeitada sem cobrança | canvas 5:2 com barras pretas [PROJETO] |
| Repetir timbre com voz no Element | redundante; guia oficial desaconselha | só ritmo e intenção [OFICIAL] |
| Redescrever a cena em I2V | corte/transição | só sujeito + movimento [OFICIAL] |
| Ação sem fim ("he looks around") | deriva/presa | "…then settles back" [TERCEIROS consenso] |
| `v3_0` sem fixar defaults | corte e trilha não pedidos | `--prefer_multi_shots false --enable_audio false` [LIVE] |

## 9. O que existe só no app e não entra no spec

Canvas Agent, `@`-sintaxe, Voice Control (`[Personagem] @Voz`), Avatar 2.0, Multi-shot personalizado com campo de duração, Face Model/lip-sync de vídeo existente, V4. Ver `15-ferramentas-nao-listadas.md`. Uma skill ou blog que os cite não altera o CLI 0.2.1 instalado.

## 10. Fontes consultadas (2026-10-13)

- [OFICIAL] Guia VIDEO 3.0 — kling.ai/quickstart/klingai-video-3-model-user-guide (estrutura, `Personagem (nota): "linha"`, beats temporais, Element 2–4 imagens, idiomas).
- [OFICIAL] Guia VIDEO 3.0 Omni — kling.ai/quickstart/klingai-video-3-omni-model-user-guide (`@Image`/`@Element`, ≤7 imagens, ≤4 com vídeo, `Shot N (Ns)`).
- [OFICIAL] Guia Image-to-Video — kling.ai/quickstart/image-to-video-guide (`Subject + Movement`, desvio da imagem causa corte).
- [OFICIAL] V3 vs O3 — kling.ai/blog/kling-v3-vs-o3-comparison-guide (V3 = prompt-led; Omni = reference-led).
- [TERCEIROS] atlabs.ai, magichour.ai, morphic.com, imagine.art, veed.io, rundiffusion, flick.art, scenario.com, atlascloud.ai (consenso: câmera explícita, ponto final, 1–2 frases de fala, mesmo descritor em todos os planos). Divergem em resolução e limites; não usados para números.
- Skill `kling-ai-prompt-generator` (verificada 2026-08-04 pelo autor) e `kling-cli` 0.2.1 local.
- [LIVE] `snapshots/who_am_i.sanitized.json` (MCP 1.3.3, 2026-10-12). [PROJETO] `07_generations/requests/*.prompt.txt`, ledger, `06`, `11`, `14`.
