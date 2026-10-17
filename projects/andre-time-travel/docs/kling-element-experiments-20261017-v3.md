# Experimentos Kling — apresentação corrigida v3 · 17/10/2026

Esta revisão corrige somente associações de apresentação. [Abrir galeria v3](../07_generations/downloads/2026-10-17-element-experiments-v3/index.html) e [mapa de identidades/hashes](../07_generations/downloads/2026-10-17-element-experiments-v3/gallery.json). Os originais e os arquivos de revisão não foram movidos, copiados ou alterados.

## Correção e cadeia de fontes

O construtor histórico v2 unia observações e análises por posição em listas com ordens diferentes. Dois cartões trocavam vídeo/folhas, enquanto áudio e observações usavam o ID do título. A apresentação v3 faz uma união pelo `asset_id`, verifica caminho e SHA-256 do manifesto contra a análise e associa vídeo, folhas, áudio e ASR ao mesmo ID. Recusa IDs duplicados/ausentes, divergência de hash/caminho e cobertura de folhas inconsistente. Fonte mantida: `scripts/experiment_gallery.py`; `--check` verifica o derivado sem escrever.

| Asset ID | Vídeo/folhas corretos | Observação histórica preservada |
|---|---|---|
| `KEXP-W323866270650569-result` | Arquivo/derivados com este mesmo ID; SHA-256 `e92ede9824636ed255ffd6512ebd86214a2ad19c8ea825c2f4b20fed016dd100` | Sala simples, mulher real à esquerda, homem ao centro, Sarah à direita; mesa alta |
| `KEXP-W323869015528491-result` | Arquivo/derivados com este mesmo ID; SHA-256 `f67aa96db1b5d785c0de72011a94aa4549732741f0da8fd533c5ee0c936dc488` | Café, mesa baixa, Sarah à esquerda, mulher real à direita |

As duas folhas de abertura existentes foram inspecionadas para confirmar a associação ampla de cenário/elenco. Isso não repete nem amplia os claims históricos de todos os quadros, cortes tardios, identidade facial, áudio ou sincronismo. As observações de `review.json` já tinham os IDs corretos e não foram trocadas. Nenhum aceite artístico ou ingestão foi acrescentado.

[Galeria v1](../07_generations/downloads/2026-10-15-element-experiments-v1/index.html), [galeria v2 histórica](../07_generations/downloads/2026-10-15-element-experiments-v2/index.html), [observações originais](../07_generations/downloads/2026-10-15-element-experiments-v2/review.json) e [lições/templates v2](kling-element-experiments-20261015-v2.md) permanecem disponíveis. V3 substitui apenas a apresentação corrente, sem reescrever a evidência ou aprovar seus candidatos. Todos os hashes das fontes e dos derivados ligados estão em `gallery.json`.

## Rotas atuais e limites preservados

O projeto registra CLI Global 0.2.3 em 16/10; o trecho 0.2.1 nas lições v2 descreve sua captura histórica. Antes de preparar rotas, consultar [guia 20](../../../docs/kling-manual/20-kling4-features-cli-023.md) e [contrato de capacidades](../../../shared/kling-capabilities.json). Capacidade listada não é geração testada nem autorização de gasto.

O vínculo do candidato de luta com o web history continua não confirmado; preservar ProduceID e possível webHistoryId separadamente. `table 1`/_4_alt versus D04/_2 segue sem decisão. G-IN/G-OUT mantêm aprovação apenas de composição, e as outras cinco referências continuam pendentes. Playback, escuta, identidade, voz/idioma e aceites permanecem gates separados.
