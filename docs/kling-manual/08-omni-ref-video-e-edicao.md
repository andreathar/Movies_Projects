# 08 · Referências mistas e edição: contrato por rota

> Atualização 16/10/2026: consultar [contrato V4 por interface](19-kling4-migration.md) e `shared/kling-capabilities.json` antes de escolher rota/custo. Tabelas e pilotos anteriores abaixo são evidência datada, sem liberação nova.

Fonte operacional: snapshot `who_am_i.sanitized.json` de 2026-10-12, MCP 1.3.3. A descrição genérica de ferramentas não substitui os campos de cada modelo. Nenhum teste pago qualifica esta rota para o filme.

| Campo | `kling-video-v3_0_omni` | `kling-video-o1` |
|---|---|---|
| Slots | `image_1`…`image_7`, um `video_1` | mesmos slots |
| Saída declarada | 3–15 s; com vídeo, acima de 10 s não confirmado nesta rota | 3–10 s |
| Resolução | 720p, 1080p, 4k | 720p, 1080p |
| Áudio nativo | `enable_audio`; com `video_1` deve ser false | não declarado |
| Som original | `keepOriginalSound`; mutuamente exclusivo com áudio nativo | não declarado |
| Elements | imagem e vídeo, types vindos de `element_get` | só imagem |

Sem vídeo direto: imagens + Elements ≤7, no máximo três Elements de vídeo no Omni. Com `video_1`: imagens + Elements ≤4; um Element de vídeo só é permitido sem imagens e sem Elements de imagem. Conte os slots preenchidos, não o maior índice. `combinedItemCap` geral de oito não elimina os limites condicionais.

Vídeo direto desta rota: MP4/MOV, 3–10 s, até 200 MiB, 720–2160 px e 24–60 fps. Notas de atualização da API de desenvolvedor mencionam outros limites, mas não os transferimos para o transporte/modelo desta conta. Um Element criado a partir de vídeo é diferente de `video_1`: este último desliga áudio nativo; a voz vinculada ao Element não garante timbre final.

O schema declara os marcadores `图片X` e `视频1`, além de `<<<id>>>` com vínculo em `elements`. São tokens de contrato e permanecem assim. Não gastar para descobrir sintaxe já declarada. Não há `audio_1`, `audio_2` etc. nesta rota; a flag genérica `--audio` não habilita um slot ausente.

Use `production_plan.py routes` para a matriz derivada e `kling_preflight.py` para validar um spec. `inputFacts.video_1` registra duração/dimensões/fps/bytes quando a entrada é uma URL; mídia local é sondada com ffprobe. Fatos declarados de uma URL não provam o conteúdo remoto. O produtor confere arquivo e versão. Novas submissões usam o runner com liberação específica descrita em `../PRODUCTION_PLAN.md`, nunca sondas pagas.

Edição produz outro candidato com ID/hash próprios, sem sobrescrever original. Uma mudança localizada de objeto/luz pode alterar rosto, mesa e movimento; requer comparação integral e novo aceite. Custo é cotado por pedido: nenhuma conversão automática de unidades de outra API em créditos desta conta.
