> Implementação local autorizada por Andre em 2026-10-12 08:29:50 UTC (“implemente”). O texto abaixo é a proposta entregue; estado operacional atual em `05_storyboard/source/production-plan.json` e `tasks/board.json`. Não concede gasto ou aceite artístico.

# Famílias de prompts — propostas para preparar os pacotes

Complemento do [plano mestre](PLANO-MESTRE.md), seção 7. **Não são prompts aprovados, specs executáveis ou novos testes autorizados.** Não substituem o playbook canônico. Os campos entre colchetes exigem referência selecionada e decisão; não podem ser enviados como estão. Nenhuma hipótese abaixo é uma melhoria já comprovada.

Cada prompt será acompanhado, fora do texto criativo, por ferramenta/modelo, slots exatos, args declarados, hashes, line_id, versões, autorização e preço. Use `<<<id>>>` apenas com ID real e `elements` compatível; marcador sozinho não vincula nada. Os tokens `图片1`, `图片2`, `视频1` são mantidos quando declarados pela rota. Nomes `@` do app não são substitutos automáticos.

## F1 — Master espacial com identidade e referências por função

Rota candidata: I2I compatível com as imagens e eventual Element de imagem. Na ficha: `image_1` identidade real, `image_2` mesa, `image_3` ambiente; ajustar a quantidade à ferramenta. Para o personagem histórico, selecionar uma referência segura de corpo/roupa se necessária, nunca inferir que o Element do Andre descreve os dois.

```text
Single cinematic film still. [APPROVED SHOT SIZE AND CAMERA POSITION].
Andre occupies [APPROVED SCREEN POSITION], seated [POSITION AND DISTANCE]
across the shared table from [SAFE BODY/SHOULDER DESCRIPTION].
[EXACT IDENTITY MARKER IF SUPPORTED] matches the approved person in 图片1.
Keep the photographed grooming and wardrobe: [APPROVED DETAILS].
Use the construction, ring stain and chipped corner of the table in 图片2.
Use the setting and motivated light of 图片3, with [APPROVED LIGHT DIRECTION].
[APPROVED SEAT HEIGHT, EYELINES AND PROPORTIONS].
The historical figure's [EXACT SAFE CROP] remains outside the facial reveal boundary.
No additional people or face reflections. [APPROVED INITIAL PERFORMANCE STATE].
```

Aceite: conferir geometria, likeness, escala, limites do crop, contato e luz. Não chamar dimensão proposta de fato histórico. O prompt não substitui master visual aprovado.

## F2 — Variante mínima de fala ou escuta

Rota candidata: I2I, primeiro input=master selecionado. Instrução de identidade adicional só se suportada e necessária.

```text
Edit 图片1 minimally. Preserve the camera, table, seats, wardrobe,
lighting and the identity of every visible subject.
Change only Andre's performance to [APPROVED LISTENING OR PRE-SPEECH STATE].
He looks toward [ESTABLISHED EYELINE].
Keep the historical figure within the same approved safe framing.
Do not change the placement of bodies, hands or objects except [NAMED NECESSARY DELTA].
```

Aceite: comparação lado a lado e sobreposição quando útil. A variant não recebe aceite pela semelhança do nome do arquivo; mudanças acidentais de mesa/assento invalidam sua função.

## F3 — Fala inglesa de Andre com guia nativa

Rota candidata do piloto: I2V V3, keyframe selecionado, Element compatível, áudio ligado e multi-shot desligado. A amostra de voz associada não garante timbre aprovado. A ficha define início da fala e handles com base na interpretação medida, não em uma promessa de precisão do prompt.

Exemplo restrito à linha **G-L04 existente**:

```text
<<<323525046658711>>> addresses the unseen Galileo along the established
eyeline, with [DIRECTOR-APPROVED PERFORMANCE INTENTION].
Andre says in English: "Your observations. And one lesson from your trial
that people keep relearning: silencing a man does not settle a question."
He pauses briefly after "observations" and becomes silent after the final word.
Maintain the approved posture, face, grooming, wardrobe, table and light.
Locked camera, one continuous editorial shot, no cuts.
No other speaker is heard during this line. [APPROVED ROOM AMBIENCE POLICY].
No music. Preserve the safe framing of any historical body or shoulder.
```

Quebra de linha aqui é tipográfica; comparar o texto final falado com o CSV canônico antes de enviar. Não adicionar estilo de timbre conflitante com o recurso de voz. Aceite separado: texto ouvido, articulação, identidade, interpretação, guia e futura dublagem. Nenhum desses critérios é provado pela presença de AAC.

## F4 — Escuta e reação motivada

Rota depende de identidade/binding/áudio necessários. O A/B não comprovou que a ordem “piscar uma vez” seja obedecida. Quando a reação exata consta do roteiro, ela continua requisito até revisão explícita.

```text
[SUBJECT OR EXACT BOUND ID] listens toward [ESTABLISHED EYELINE].
At first [INITIAL STATE]. In response to [CANONICAL WORD/IDEA OR EDITORIAL CUE],
[ONE DIRECTOR-APPROVED CHANGE OF PERFORMANCE].
[CANONICAL GESTURE IF THE SCRIPT REQUIRES ONE].
Finish in [STATE THAT MATCHES THE NEXT SHOT].
Keep the camera and approved composition stable throughout.
Preserve identity, wardrobe, shared-space geometry and lighting.
[SUPPORTED AUDIO POLICY, WITH SPEECH OFFSCREEN OR ABSENT AS PLANNED].
```

Não se presume que a ferramenta entenda um marcador temporal como sync garantido. O editor confere o cue na montagem com o áudio real; reação conclusiva não antecede a causa. Trocar inventário de microgestos por intenção é hipótese de direção, não correção demonstrada.

## F5 — Olhos, mão, pés ou detalhe da mesa

Rota candidata: I2V com keyframe de crop aprovado; motion_control só se a imagem e a fonte atenderem ao sujeito exigido pelo contrato. Para cada take, escolher um detalhe, não todos.

```text
Preserve exactly the approved framing of [EYES / HAND ON TABLE / FEET ON FLOOR].
[ONE MOTIVATED ACTION] begins from [INITIAL CONTACT OR GAZE STATE],
then settles into [END STATE].
Keep the same anatomy, material, garment edge, table or floor scale and light.
The camera stays locked; no widening, upward tilt or new reflection.
[EXPLICIT SAFE FACIAL CROP BOUNDARY].
[SOUND EVENT TO BE GENERATED ONLY IF SUPPORTED, OR FOLEY PLANNED IN POST].
```

Se a família de olhos usa barras de segurança, preservá-las e conferir todos os quadros; barras não garantem comportamento do modelo. Som de contato será alinhado ao gesto na pós quando essa for a rota escolhida.

## F6 — Atuação por vídeo

Rota candidata: motion_control com **uma** imagem e **uma** fonte qualificada (`video` ou `motionId`). A ficha determina orientação e eventual binding facial permitido. Não acrescentar outro áudio ou video_1 da ferramenta Omni.

```text
[EXACT FACIAL ELEMENT MARKER ONLY WHEN SUPPORTED] retains the approved face.
Preserve the subject image's grooming, wardrobe, props, setting and lighting.
The performance follows the selected reference video within the approved
orientation and framing. [APPROVED EMOTIONAL CONTEXT CONSISTENT WITH THAT VIDEO].
Maintain [CONTINUITY CONSTRAINTS THAT DO NOT CONTRADICT THE SOURCE MOTION].
```

Não redescrever braços/pernas em conflito com a referência, nem afirmar que o prompt controla duração. `keepOriginalSound` é configurado fora do texto e significa conservar som da fonte, não transferir uma voz escolhida. Lip-sync e identidade seguem como critérios a provar.

## F7 — Âncoras A→B ou edição com vídeo direto

São duas rotas distintas; não unir seus payloads.

**A→B por first/tail:**

```text
Move from the approved initial state to the approved final state in one
continuous [NAMED ACTION], following [APPROVED DIRECTION].
Preserve identity, wardrobe, table, seat positions, lighting and screen axis.
[SINGLE CAMERA BEHAVIOUR]. Keep the historical face outside the approved boundary.
```

**Edição Omni com vídeo direto:**

```text
In 视频1, change only [SPECIFIC EDIT], using 图片1 for [REFERENCE FUNCTION].
Preserve the original action, camera trajectory, timing, identities and
placement of everything not explicitly changed.
Make contact, light and shadows consistent with the existing scene.
```

O contrato arquivado de vídeo direto exige `enable_audio=false`; eventual som original é decidido separadamente. Não usar a edição de um rosto já aceito sem comparar integralmente original e derivado. Uma instrução de preservação não garante preservação.
