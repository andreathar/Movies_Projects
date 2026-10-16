# Kling 4 utilizável · CLI Global 0.2.3 · 16/10/2026

Contrato atual: shared/kling-capabilities.json. Fonte executável: npm oficial @klingai/cli-global, versão latest 0.2.3 publicada em 16/10 às 07:22:33 UTC; atualização local autorizada a partir de 0.2.1. Integridade SHA-512 do tarball e bytes do bundle instalado coincidem com o registry. Node >=18; ambiente 24.18.0. Sem scripts lifecycle, login, grants ou leitura de credenciais. A autenticação existente funcionou em who_am_i/tool_list pós-update; os corpos dos schemas permaneceram idênticos. Modelos foram **listados**, nenhuma geração de qualidade foi testada.

Pacote oficial não contém CHANGELOG separado. README distribuído e diff do bundle confirmam suporte melhor a combinedItemCaps condicionais, argument.maxItems/elementSupport, ajuda de geração por modelo, inputs nomeados em image_to_image, áudio WAV e correções no transporte de upload. Estes últimos não foram testados com upload, proibido nesta tarefa. O repositório público da skill não ofereceu release notes da CLI; npm web retornou 403, mas registry oficial respondeu. Não tratar exemplos de Flash no README como acesso da conta: Flash não aparece na descoberta autenticada.

## Três rotas autenticadas, sempre model=kling-video-v4_0

| Rota | Inputs reais | Controles/limites úteis |
|---|---|---|
| image_to_video | first_image, tail_image, keyframe_1..10, todos opcionais no schema | Total 10 imagens. Cada imagem ≤30 MB e proporção 2:5–5:2. Sem timestamps de keyframe ou áudio/Element declarados. Projeto exige ao menos uma imagem. |
| text_to_video | Nenhum input | Proporções 16:9, 9:16, 1:1, 21:9. Schema default=16:9 contradiz texto “auto”; projeto exige proporção explícita. Sem vínculo de identidade, áudio ou multi-shot declarados. |
| omni_ref_video | image_1..10, video_1..5, audio_1..3 e Elements | Máximo 15 recursos no total, incluindo áudio e Elements. Até 7 Elements, no máximo 3 vídeo. prefer_multi_shots só aceita true; câmera fixa não qualificada. |

Nas três: duração 3–30 segundos inteiros, resolução 720p/1080p, imageCount de 1 a 4 no servidor. Projeto restringe a 1 saída por liberação, duration/resolution explícitos. 4K não habilitado na conta/interface. image_to_video segue o primeiro quadro: omitir aspect_ratio salvo pedido explícito, nunca auto. Omni aceita auto somente com imagem/vídeo direto, não apenas Element/áudio. Não há V4 em motion_control; essa rota continua com modelos V2.6/V3 explicitamente escolhidos e uma fonte video ou motionId, sem omni.

## Referências e Elements: papéis separados

Manifesto local shotContract v1 tipa cada referência: target, kind, source, sha256, provenance, use, review e reviewEvidence. URL também exige localEvidence dos bytes selecionados; hash local não autentica conteúdo remoto mutável. Imagem de composição não vira prova de identidade. Não colocar figurino, cenário ou prints em slot de identidade. Revisar elenco/companheiros, figurino e marcas da mesa contra os arquivos exatos antes da mudança.

Na rota Omni, prompt pode referir imagens como 图片1 e vídeos como 视频1 conforme a ficha atual; a função deve ser explícita: aparência/identidade, mesa, ambiente, câmera, movimento, voz ou primário de edição. Número de slot é mapeamento técnico, não aprovação. Não perder companheiros ao trocar figurino. Não substituir D04 _2 por table 1 _4_alt só pelo nome.

Element exige ID real e type do element_get, resources inspecionados, argumento elements com id/bindName/type e marcador <<<id>>> no prompt. Nome sozinho não vincula. Runner compara element_get corrente ao snapshot de ID/type/resource antes de saldo/upload/submissão. Tags são literais do catálogo regional. Não criar, renomear ou apagar Elements incidentalmente. Reutilizar mídia canônica e downloads existentes.

## Voz, áudio, fala e continuidade

Omni declara até 3 áudios, cada 5–30 s e ≤50 MB; guia público descreve referência de voz. Exigir voiceContentReview=reviewed_voice_only: música ou ambiente não são um substituto. CLI 0.2.3 reconhece .mp3 e .wav; suporte de tipo não prova qualidade nem adequação do conteúdo. Referências usam 音频1 conforme schema atual.

Escolher estratégia: native_guide com enable_audio=true e keepOriginalSound=false; retain_source com a combinação inversa e stream de áudio confirmado em video_1; postproduction com ambos false; uncontrolled_review_required nas rotas sem controles. Campos ausentes não garantem vídeo mudo. Fala exata, idioma, speaker, duração e pausas devem estar revisados; medição e revisão de idioma são pré-requisitos, não promessa de sincronismo. Voz de Element não equivale a aceite da voz final. Idiomas/acentos anunciados não aprovam tradução histórica nem dispensam escuta humana. Fight local é mudo e não fornece voz; manter ProduceID/prompt desconhecidos como lacuna.

## Keyframes, beats, câmera e edição

Keyframes são estados visuais em slots ordenados; o schema atual não oferece timestamp por imagem. Beat start/end/action é intenção local, repetida de modo claro no prompt, e não um bloqueio temporal do servidor. Planejar causa antes da reação, gesto/contato e pausa após fala. IN/OUT precisam de compatibilidade geométrica, eixo, elenco, mesa, figurino e luz. Evitar forçar 30 segundos quando a atuação pede um plano menor. Revisar todos os quadros e reflexos quanto a rostos históricos.

Omni pode orientar recriação/edição com vídeo, mas a ficha atual não declara um flag primary_edit nem ferramenta dedicada de edição destrutiva. Identificar vídeo primário no manifesto/prompt e explicitar o que deve mudar e o que deve permanecer; video_1 sozinho não prova preservação pixel a pixel. O anúncio full-model de cinco vídeos/um principal não é um parâmetro wire inventado. Multi-shot=true obrigatório limita o uso para planos fixos. F9 é proposta bloqueada; usar V3 por escolha explícita quando a receita exige câmera fixa ou vínculo não suportado por V4 keyframes.

Vídeos diretos: cada 3–30 s, ≤300 MB e proporção 2:5–5:2. Vídeos diretos mais video Elements totalizam no máximo 30 s. Duração de entrada compõe a cobrança por segundo; registrar billing.inputVideoSeconds e inputVideoDurationIncluded=true. Preço atual é desconhecido: cotação exata, limite e aprovação por payload/schema novos. Nunca herdar orçamento ou cobrar diferença de saldo como custo por job.

## Anunciado versus acessível

[Guia oficial full-model](https://kling.ai/blog/kling-4-ai-video-model) anuncia 4K, 10 keyframes, 8.000 tokens e referências multimodais; tokens não são caracteres. [Anúncio de lançamento](https://kling.ai/blog/kling40-kling-visual-realism-creative-control-introducing-storytelling?tab=all) mantém HDR e extensão até dois minutos como futuros. Nesta CLI/conta: 720p/1080p; nenhum preço/FPS/Flash validado, nenhum schema público API 4.0 confirmado. Higgsfield Cinema Studio 4.0 e interface web têm contratos próprios; Qingque 1.5 Custom Face é legado.

## Controles e próximo gate

Preflight: docs/kling-manual/tools/kling_preflight.py + scripts/kling_contract.py. Runner: scripts/kling_batch.py; fingerprint/release: scripts/kling_release.py; templates bloqueados: F8/F9 e shared/templates/kling-shot-contract.json. Rotas e frontend derivam dos snapshots atuais, sem gerar ou aprovar. G-IN/G-OUT continuam aprovados somente para composição; G-ID/G-WARDROBE/G-TABLE/G-ERA/G-EYE-B seguem pendentes no conjunto ativo. Os antigos handoffs e suas decisões não foram ingeridos. Próximo dono: produtor desktop revisa arquivos/versões e resolve os gates antes de qualquer proposta paga.
