# 16 · Fontes e grau de confiança

Data do levantamento: 2026-10-09. Selos como no README. "Li" = abri e usei o conteúdo; "só título" = apareceu em busca, **não li**.

## Fonte primária: o próprio CLI (confiança máxima, mas datada)

| Fonte | Onde | Obs. |
|---|---|---|
| `kling who_am_i` (mcpVersion 1.3.3) | `snapshots/who_am_i.sanitized.json` (sha256 `069bd2e4…47a1`) | removido `body.user` |
| `kling tool_list` | `snapshots/tool_list.json` (sha256 `50e342a9…50e8`) | 18 ferramentas |
| `kling <cmd> --help` (13 comandos) | `snapshots/cli_help/` | inclui descrições vivas do servidor |
| `kling account` | saída não arquivada | plano Ultra, saldo 31.621 às 15:04 |

## Fontes do projeto (li)

`AGENTS.md`; `skills/kling-cli/{SKILL.md, reference.md, api-examples.md}` (0.2.0); `skills/andre-time-travel/SKILL.md`; `projects/andre-time-travel/docs/prompt-playbook-kling.md`; `projects/andre-time-travel/credit-ledger.csv` (87 linhas); request da Fase A e template do keyframe; `docs/LOCAL_AGENT_HANDOFF.md`.

## Fontes da Kling (confiança alta quando lidas direto; aqui, lidas por via indireta)

| Fonte | Como cheguei | Confiança |
|---|---|---|
| Descrições de ferramentas do servidor (limites de imagem, Elements, `query_tasks`) | texto vivo no `--help` | alta |
| Tabela de API https://kling.ai/dev/pricing | transcrita em 2026-08-04 por uma skill de terceiros (`pricing.md`); **eu não abri a página** | média; a conversão ×10 é minha |
| Notas de lançamento: 4K (2026-04-23), Voice Control (2025-12-16), 3.0 Turbo e edição Omni (2026-06-17) em https://kling.ai/release-note | citadas na mesma skill; a página é dinâmica e meu fetch veio vazio | média |
| Guia do usuário do VIDEO 3.0 (https://kling.ai/quickstart/klingai-video-3-model-user-guide) e Prompt Guide (https://kling.ai/blog/kling-ai-prompt-guide) | citados no playbook do projeto | média |
| Documentação da API https://kling.ai/document-api/quickStart/productIntroduction/overview | página dinâmica; não consegui ler | — |

## Skills de plugin (li; origem desconhecida, tratar como [TERCEIROS])

`kling-ai-prompt-generator:kling-ai` (SKILL, `references/pricing.md`, `references/prompt-templates.md`) e `kling-ai:kling-ai-generate-image/video`. Fonte de modelos de prompt, vocabulário de câmera, regras de multi-shot e edição Omni. Cada afirmação aproveitada está marcada no manual.

## Terceiros que abri

| Fonte | Para quê | Confiança |
|---|---|---|
| Atlas Cloud, "Kling AI Lip Sync Tutorial" https://www.atlascloud.ai/blog/guides/kling-ai-lip-sync | Lip-sync: ≤ 60 s, CN/EN/JP/KR/ES, ~30° de rosto | baixa a média; é blog de revendedor |
| GitHub bytedance/LatentSync https://github.com/bytedance/LatentSync | Apache-2.0; 8 GB (v1.5) / 18 GB (v1.6) | média-alta para licença e VRAM |
| Pack de skill Kling https://cdn.jsdelivr.net/npm/@intentsolutionsio/klingai-pack@1.0.3/README.md | Panorama da API: câmera, negative prompt, máscaras, extensão, lip-sync | baixa; campos exatos não aparecem |
| Apiframe, tutorial image-to-video https://apiframe.ai/guides/kling-image-to-video-api-python-tutorial | Ideia de `multi_prompt`, `end_image`; **parâmetros do wrapper, não do Kling** | baixa |

## Terceiros que só vi no título (não li, não usei)

RunComfy (lipsync audio-to-video), CometAPI (kling advanced lip syn), Crazyrouter (API tutorial), laozhang.ai (guia da API), sync.so (what is LatentSync / MuseTalk), Pixazo (open source lip sync), arXiv 2410.10122 (LatentSync), hyper.ai (notebook LatentSync). Se alguém precisar deles, ler antes de citar.

## Conectores (descrições lidas, nada chamado)

Higgsfield (`dubbing`, `voice_change`, `upscale_video`, `video_analysis_create`), Jockey/TwelveLabs (`jockey_query`), Adobe (`media_enhance_speech`), ElevenLabs (instruções do servidor). Ver `15`.

## O que NÃO foi feito

Nenhuma geração, upload, criação/alteração de Element, `feedback`, login ou compra. Os únicos comandos do Kling executados foram `account`, `who_am_i`, `tool_list` e `--help`. Nenhum arquivo existente do projeto foi alterado.

## Dúvidas abertas (resolver com teste pequeno ou com a Kling)

1. Sintaxe de citação de referências em `omni_ref_video` (`08`).
2. Lip-sync no app: modelos suportados (guia oficial x blogs) (`10`).
3. Se `motion_control` transfere a boca da fala gravada (`09`).
4. Papel dos slots `image_1..7` em `image_to_video` (omni/o1): primeiro quadro ou referência? (`06`).
5. Limite real de proporção de entrada: texto diz 1:2; projeto viu 5:2 passar e 4:1 falhar (`04`).
6. Se o CLI devolve `creditsConsumed` na submissão (`12`).
