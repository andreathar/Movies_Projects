# 15 · Ferramentas úteis que não estão listadas no projeto (aviso ao Codex)

"Listado" = presente em `skills/registry.json` (kling-cli, film-character-continuity, film-dialogue-localization, film-editing-qc, grounded-citations, andre-time-travel) ou nos docs do projeto. Tudo abaixo está **fora** disso. Nada foi chamado, comprado ou enviado: li só descrições/schemas. Qualquer uso respeita o AGENTS.md: escopo próprio para qualquer serviço que não seja o CLI do Kling, e nenhum upload de mídia do filme a terceiros sem autorização do Andre.

## A. Lacunas dentro do próprio Kling

| Item | Situação | Por que importa |
|---|---|---|
| **`omni_ref_video`** (referências mistas, edição de vídeo, vídeo-Element, voz de Element) | Existe no CLI 0.2.1 e no servidor 1.3.3 [LIVE]. Documentado no `skills/kling-cli/SKILL.md` **0.2.1** (skill atualizada em 2026-10-12) | Resolvido: skill alinhada ao CLI. Ver `08` |
| Modelos novos: `kling-video-v3_0_turbo`, `kling-video-v3_0_omni`, `kling-image-v3_0_omni`, `gemini-3.1-flash-image`, `gpt-image2` | Na ficha de hoje [LIVE] | `03` |
| **Lip Sync, Avatar 2.0, extensão de vídeo, upscale, Effects, biblioteca de vozes (Voice Control), Canvas Agent / storyboard** | App web e/ou API do Kling; **nenhuma das 18 ferramentas do CLI** [LIVE] | Dublagem, vídeos longos, acabamento. Só pelo app com o Andre, ou fora das regras (API com chave) |
| Parâmetros de API não expostos no CLI: `negative_prompt`, `cfg_scale`, `camera_control`, máscaras de movimento (motion brush), `multi_prompt` (plano a plano em JSON), callbacks | Citados por guias de terceiros [TERCEIROS]; **não aparecem** em nenhuma ficha de modelo [LIVE] | O CLI não oferece negative prompt: tudo vai em frases positivas no prompt ("locked camera", "nobody else enters") |
| Download sem marca (`urlWithoutWatermark`) e a marca "AI Generated" que segue a conta | Descrição de `query_tasks` [OFICIAL] | Decidir qual versão é original (`13`) |
| Elements: capa imutável; vídeo-Element de 3–60 s; voz `.mp3` | `element_create/update` [OFICIAL] | `05` |

**Fora das regras (só para ficar claro):** as API oficiais exigem par de chaves (AK/SK) e JWT; aggregators (fal.ai, PiAPI, kie.ai, Apiframe...) têm contas, preços e IDs próprios. O AGENTS.md proíbe HTTP direto, AK/SK e credenciais fora do `kling login`. Notebooks e tutoriais de API que encontrei são **referência conceitual**, não receita executável aqui.

## B. Conectores que existem na sessão do Claude (o Codex pode não ter)

| Ferramenta | O que faz (descrição do conector) | Uso possível no filme | Custo/escopo/risco |
|---|---|---|---|
| **Higgsfield · `dubbing`** | Traduz a fala, sintetiza no idioma-alvo e sincroniza a boca. 18 idiomas: eng, cmn, fra, hin, ita, jpn, kor, por, rus, tur, spa, deu, ara, pol, ind, fil, swe, fin | Edição dublada (PT, ES, IT, FR...) de takes com boca visível | Créditos próprios do Higgsfield; **upload do vídeo** = escrita externa; sem latim, mongol, córsego; qualidade não testada |
| Higgsfield · `voice_change` | Troca a voz mantendo timing e imagem | Substituir voz-guia do Kling | idem |
| Higgsfield · `upscale_video` (ByteDance 1080p/2K/4K ou Topaz 1080p/2160p) | Sobe resolução e restaura. "Não suporta pré-cálculo de custo" | Entrega em 2K/4K a partir de 720p barato | Custo imprevisível; pode alterar rostos aceitos |
| Higgsfield · `video_analysis_create` | Análise cena a cena de um clipe (mais precisa em clipes curtos) | Triagem automática | Upload externo |
| Higgsfield · `motion_control`, `reframe`, `remove_background`, `outpaint_image` | Outras edições sobre mídia existente | Reenquadrar 16:9→9:16 para social; limpar fundo | Créditos próprios |
| **ElevenLabs** (`creative_generate_speech`, `creative_transcribe_audio`, `creative_design_voice`, `creative_list_voices`) | Voz sintética, transcrição, voz projetada por descrição | Rascunho de dublagem em outros idiomas; STT multilíngue no QC; o playbook já cita ElevenLabs como fallback da Edição H | AGENTS.md: escopo e custo próprios. Voz sintética de figura histórica precisa de decisão registrada |
| **Jockey / TwelveLabs** (`jockey_add_media`, `jockey_search`, `jockey_query`) | Busca e perguntas fundamentadas sobre clipes indexados | Segunda opinião: "algum quadro mostra rosto de frente?"; achar o take certo entre dezenas | **Upload para terceiros.** Não substitui a grade local de quadros (`13`) |
| **Adobe · `media_enhance_speech`** | Separa áudio em fala limpa, fundo (música/ambiente) e reverb | Remover a música ou trilha que o Kling mistura à fala; extrair trilha limpa para a dublagem | Exige subir o arquivo ao Adobe |
| Adobe · `video_metadata`, `video_resize`, `video_create_quick_cut`, `video_render`, `video_render_frame`, tratamento de imagem (cor, grão, expansão generativa) | Listadas no conector; **não avaliadas** por mim | Possíveis: unificar grão/cor entre takes; extrair quadros | Não validei contrato nem custo |
| HyperFrames (HeyGen), Hugging Face, Mermaid, Cloudflare, Gmail/Drive/Calendar | No ambiente do Claude; fora do escopo do filme | Hugging Face: buscar modelos abertos; Mermaid: diagramas do fluxo | Sem relação direta com geração |

Somente descrições foram lidas (nenhuma chamada). **Quem pode chamar**: o Claude desta sessão; o Codex só se tiver esses conectores. Registre a decisão de uso em `decisions` antes de gastar.

## C. Locais (gratuitos), já na máquina do Andre [LIVE, leitura apenas]

| Ferramenta | Estado | Uso |
|---|---|---|
| `ffmpeg`/`ffprobe` | instalados. Filtros presentes: `ebur128`, `loudnorm`, `tile`, `minterpolate`, `vidstabdetect/transform`, `deshake` | QC, grades de quadros, loudness, conformar fps, estabilizar |
| `exiftool` | instalado | Verificar extensão/EXIF das referências |
| `git-lfs` | instalado | Já usado pelo projeto |
| `faster-whisper` 1.2.1, `numpy`, `Pillow` no `.venv` | presentes | STT de QC; análises simples de imagem |
| **Ausentes**: `sox`, `mediainfo`, ImageMagick, `torch`, `cv2`/mediapipe/insightface | — | Sem detecção de rosto automática no `.venv`: a checagem "nenhum rosto completo" continua visual |
| GPU: **RTX 3060 Laptop, 6 GB** | — | Modelos locais de lip-sync/upscale típicos exigem ≥ 8 GB: descartados. Vale para o objetivo do Andre de treinar LLMs localmente: a mesma placa limita o que roda aqui |

## D. Resumo para o Codex (ordem sugerida)

1. **Atualizar a skill local** (`omni_ref_video`, modelos novos, defaults) e o hash em `skills/registry.json` (producer). Este manual cobre o conteúdo; a skill é sua para decidir.
2. **Adotar o preflight** (`tools/kling_preflight.py`) antes de qualquer pedido pago. Já pegou o erro de 5 imagens para 2 slots da Fase A.
3. **Corrigir o ledger** (janelas de saldo sobrepostas) e passar a registrar `creditsConsumed` (`12`).
4. **Testes pequenos T1–T3** (`11`) para fechar as dúvidas que mais mudam o filme: `tail_image`, `omni_ref_video`, `motion_control` como rota de lip-sync.
5. Para a Edição H: decidir primeiro a rota A (boca escondida); só então escopo para Higgsfield/ElevenLabs.
