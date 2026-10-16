# Experimentos Kling — arquivo de 15/10/2026

[Abrir galeria local](index.html) · [Prompts e entradas](prompts.json) · [Catálogo completo](manifest.json) · [Recursos CSV](resources.csv) · [Próximo lote](next-batch-inventory.json) · [Lições e templates](../../../docs/kling-element-experiments-20261015-v1.md).

Lote limitado a três testes de 13/10 e quatro Elements recentes próprios. Todos os novos registros permanecem experimentais, sem aprovação de produção.

- 28 papéis de recurso, 27 arquivos únicos: 22 imagens, quatro MP4 (três resultados + referência de 8 s), um MP3 já local. Dois papéis `video`/`voice` do Element de vídeo apontam ao mesmo MP4.
- 24 arquivos novos, **59.860.079 bytes (57,09 MiB)**. Três arquivos existentes reutilizados por SHA-256; nenhuma cópia em lane.
- Transferência medida pelo script: **68.098.885 bytes**, sob teto de 300 MiB. Dois downloads transitórios do navegador, somando 21.898.092 bytes, foram removidos após confirmar hashes idênticos aos canônicos. Transferência conhecida total: 89.996.977 bytes; transferências falhas/overhead do navegador não foram medidos. Espaço inicial: cerca de 557 GB livres; saldo final em `evidence/storage.json`.
- 13 imagens de recursos próprios e nove previews de fontes históricas/biblioteca. Esses nove previews **não são originais**; qualidade indicada por recurso.
- Sem geração, upload, criação/edição/exclusão de Element, gasto, login novo, alteração de credencial ou dispatch de agente.

## Relação entre os testes

| ID de histórico web | Resultado | Entradas por nome literal |
|---|---|---|
| `323866270650569` | Três personagens à mesa | `Andre Athar`, `table 1`, `Blonde Lady`, `Sarah` |
| `323868230505094` | Edição de figurino/café/efeito | `Video1` = resultado acima; `Costume 1`, `Andre Athar`, `Zen-style Café`, `Stellar Black Hole` |
| `323869015528491` | Cena de café com neve | `Andre Athar`, `table 1`, `Blonde Lady`, `Sarah`, `Zen-style Café`, `Snowflake` |

`VIDEO 3.0 Omni`: primeiro/terceiro 720p, segundo 1080p; os três arquivos medem 361 quadros a 24 fps, 15,041667 s de vídeo, com AAC. Isso descreve bytes observados. Seed, flags históricas de áudio/Multi-Shot, cobrança e payload original não foram expostos.

Os IDs numéricos da interface foram recusados por `query_tasks` (`Invalid generationId.`); **não** foram registrados como `generationId`. O CLI não lista o histórico da conta. O navegador permitiu ler prompts/chips e observar URLs de mídia; os bytes foram baixados desses URLs sem credenciais adicionais. `prompts.json` preserva segmentos exatos do DOM, pontuação e nomes; `[@nome]` é uma notação legível, não a serialização original.

## Achados que mudam o próximo pedido

O teste inicial conserva os três estilos de personagem nas amostras. A edição seguinte transfere roupa e cenário, mas deixa o homem sozinho. O teste com neve conserva o elenco, porém altera escala da mesa, assentos e cobertura. Por isso, explicitar preservação e mudar um fator por vez é uma proposta baseada nesses exemplos, ainda sem novo teste.

`table 1` é a variante `_4_alt`, não a `_2` escolhida em D04. `Costume 1` usa como capa o original sintético de Oppenheimer já local; seus prompts/modelo/opções foram recuperados dos metadados locais. Os Elements mais novos mostram cabelo longo e camisa preta; não substituem a identidade/roupa do filme. `Andre Athar`, usado nos vídeos antigos, não aparece no inventário próprio atual e não foi confundido com os novos nomes.

## Evidência e limites

`review/` contém duas folhas com as 22 imagens e amostras de cinco quadros por vídeo. Os quatro vídeos passaram decode completo, registrado em `evidence/decode.json`. Todos os arquivos catalogados têm SHA-256 verificado. Inspeção de amostras não é revisão de todos os quadros, playback completo, escuta ou aceite de semelhança.

`evidence/element_get-*.json` preserva nomes, IDs, descrições, tags e recursos exatos; `who_am_i.sanitized.json` omite identidade da conta. Não há credenciais/cookies/tokens de autenticação. URLs CDN e nomes de arquivos são metadados de origem, não chaves de acesso. Nenhuma URL de recurso deste lote retornou expiração; falha no exportador do navegador não foi rotulada como expiração.

Lacunas: `generationId`/workIndex e serialização/settings dos três testes; IDs/originais das referências web; prompts-fonte da maioria dos recursos novos; histórico completo da conta; julgamento individual de Andre. Cada lacuna está descrita no manifesto.

Seis itens antigos vistos no histórico e o Element de produção foram apenas inventariados. `Costumes_Athar_2` (`324019350521447`) e teste de kung fu (`324018500502140`) apareceram durante a sessão e foram registrados para a próxima rodada, sem download. Este é um recorte observado, não um inventário completo da conta.

Próximo: produtor desktop revisa este pacote com Andre, confirma quais testes representam seu aprendizado e escolhe outro lote se necessário. G-IN/G-OUT e demais aprovações permanecem intactos; `v2-reconciliation` não foi ingerido.

## Integração e validação

318 IDs no catálogo ativo (290 linhas anteriores preservadas + 28 novas com `approved=false`). O exportador existente do painel recebeu somente dois caminhos de descoberta; o JSON derivado foi regenerado e passou `--check`. Não houve redesign, cópia de mídia para o frontend ou publicação.

Passaram: hashes dos 28 papéis/27 arquivos, decode dos quatro vídeos, catálogo, `manage.py validate`, `production_plan.py check --verify-media`, 13 testes shared-media, cinco testes de exportação e `check-data.mjs`. `manage.py resume` executado. `manage.py lint` registra dois apontamentos: os hashes do exportador e do JSON derivado mudaram em relação ao handoff técnico `v2-reconciliation` ainda pendente. O handoff anterior não foi alterado/ingerido/supersedido; cabe ao produtor reconciliar essa revisão. Os avisos de skills compartilhadas e de coerência já existentes permanecem registrados.
