# 10 · Áudio, voz, idiomas, lip-sync e dublagem

Regra-mãe do projeto: **o Kling dá voz-guia, não a voz final** quando o idioma é difícil; a edição em inglês vem primeiro e a dublagem depois (D13/D14). Este guia mostra o que cada rota realmente cobre.

## 1. Áudio nativo dentro do vídeo (CLI) [LIVE + PROJETO]

| Controle | Onde | Efeito |
|---|---|---|
| `enable_audio` | `image_to_video`/`text_to_video` v2_x e v3_0* ; `omni_ref_video` v3_0_omni | Gera áudio sincronizado. **Padrão true.** Custo ~+50% |
| Voz presa ao Element | `element_create --voice arquivo.mp3` | Voz consistente do Andre (D13). Não repetir o timbre no prompt |
| `keepOriginalSound` | `motion_control`, `omni_ref_video` v3_0_omni | Mantém o som do vídeo-fonte. Padrão: true em motion_control, false em omni |
| `audio_prompt`, `music_prompt`, `enable_asmr` | só `kling-video-v2_5` | Efeito sonoro, música, ASMR descritos por texto |
| (sem controle de áudio) | `v3_0_turbo`, `kling-video-o1` | Turbo sai sem áudio configurável; o1 não declara |

Idiomas de fala nativa: **EN, ZH, JA, KO, ES** (+ sotaques/dialetos) [OFICIAL via playbook]. Latim, mongol, toscano, córsego: **fora**.

Voice Control (biblioteca de vozes com `[Personagem] @NomeDaVoz`; amostra de 5–30 s; até 200 vozes; só chinês e inglês; +2 cr/s) é recurso do **app/API** [OFICIAL, nota de 2025-12-16 via terceiros]. Não está no CLI: aqui o equivalente é o `.mp3` no Element.

## 2. Fala em inglês: receita provada [PROJETO]

Ver `06` (seção "Fala com áudio nativo") e `11`. Pontos: linha canônica exata entre aspas, pausa, silêncio no fim, "quiet room tone only, no music", duração = fala medida + ≥ 2 s. Verificar por STT contra `dialogue-lines.csv` (`13`).

## 3. Rotas de lip-sync / dublagem para outros idiomas

| Rota | O que faz | Está no CLI/registry? | Evidência | Riscos |
|---|---|---|---|---|
| **A. Boca escondida** (costas, sobre o ombro, só olhos, plano abaixo do pescoço) | Dispensa lip-sync: o áudio é trocado em pós | Sim, é cobertura de câmera | [PROJETO] Fase A r2, G-03/G-05 | Limita direção; é a opção mais barata e segura |
| **B. `motion_control` com a fala gravada do Andre** | A boca do keyframe segue a gravação (voz real dele com `keepOriginalSound`) | Sim (`motion_control`) | [INFERÊNCIA] — ver `09` | Não testado; identidade e boca precisam de teste curto |
| **C. Kling Lip Sync (app/API)** | Dado um vídeo + áudio ou texto, sincroniza a boca | **Não** (nenhuma das 18 ferramentas) | Guia oficial: só vídeos Kling 1.0/1.5 [OFICIAL]; blogs dizem Kling 3.0, ≤ 60 s, CN/EN/JP/KR/ES [TERCEIROS]. **Conflito não resolvido** | Idiomas do Kling não cobrem latim/mongol/toscano/córsego; app/API fora do escopo do CLI |
| **D. Kling Avatar 2.0** | Uma foto + um áudio ⇒ pessoa falando até 5 min, 1080p/48 fps | **Não** | [OFICIAL via skill]; idiomas listados EN/JA/KO/ZH; sincroniza com qualquer áudio dado, "confirmado em campo com polonês" [TERCEIROS] | Rosto frontal obrigatório; só para o Andre |
| **E. ElevenLabs** (TTS, voz projetada, transcrição; fluxo com lipsync no conector completo) | Cria a voz no idioma-alvo e/ou sincroniza | Fora do registry; o playbook já cita como fallback da Edição H | [PROJETO] cita; ver `15` | Exige escopo/custo próprio (AGENTS.md); voz sintética de figura histórica |
| **F. Higgsfield** (`dubbing`, `voice_change`) | `dubbing` traduz a fala, sintetiza no idioma-alvo e sincroniza a boca no vídeo. 18 idiomas: eng, cmn, fra, hin, ita, jpn, kor, por, rus, tur, spa, deu, ara, pol, ind, fil, swe, fin. `voice_change` troca a voz mantendo timing | Fora do registry | [LIVE: descrição das ferramentas no conector da minha sessão; qualidade **não testada**, nada foi chamado] | Serviço pago separado; sem latim, mongol ou córsego; `ita` é italiano moderno, não toscano histórico; exige subir o vídeo (escrita externa) |
| **G. Open-source local** (ex.: LatentSync) | Lip-sync de um vídeo com novo áudio | Fora do registry | LatentSync: Apache-2.0; 8 GB VRAM (v1.5) ou 18 GB (v1.6) para inferência; treinado em 512×512 [TERCEIROS, README no GitHub] | **Esta máquina tem RTX 3060 Laptop com 6 GB de VRAM [LIVE: `nvidia-smi`]: abaixo dos 8 GB do v1.5 e dos 18 GB do v1.6.** Rodar local não é viável sem GPU maior ou nuvem. O `.venv` do projeto também não tem torch. Qualidade em rosto fotorreal e idiomas raros **não testada**; MuseTalk e outros: licença não verificada |

Prioridade sugerida [INFERÊNCIA]: **A** (zero custo extra) → **B** (testar barato) → **E/F** (serviço externo, com escopo e custo aprovados) só se a Edição H realmente precisar de boca visível. **G** fica descartada nesta máquina.

## 4. Fluxo de dublagem (D14)

1. Congelar o roteiro em inglês. 2. Rascunho com TTS local gratuito antes de gastar em imagem/áudio pago. 3. Medir a duração das falas. 4. Cada take de vídeo = fala medida + cauda. 5. Traduzir e revisar o idioma por humano (validação de idioma é gate separado). 6. Gerar áudio do idioma-alvo (voz do Andre real, ou sintética aprovada). 7. Sincronizar (rotas A–G) e rodar o QC.

## 5. Prompt de fala (formas aceitas)

- Projeto (provado): ver `06`.
- Formato de atribuição citado em guias [TERCEIROS]: `[Speaker: Nome] "texto" in a calm warm voice` e `Background ambient: ...`. Em `image_to_video` com Element, mantenha o formato do projeto.

## 6. Cuidados

- Todo diálogo é fictício; âncoras factuais mantêm fonte; nunca inventar citação (AGENTS.md).
- Voz de figura histórica: o projeto mantém falas das figuras **fora de quadro**. Qualquer voz sintética nova precisa de decisão registrada.
- Sempre ouvir a faixa inteira e medir loudness (`13`). Áudio gerado pode vir com música que ninguém pediu.
