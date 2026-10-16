# Reconciliação técnica v3 — catálogo Kling e descoberta no frontend

Esta entrega atualiza as alegações sobre a árvore atual por meio de um novo handoff que supersede `2026-10-15-qc-reference-review-controls-v2-reconciliation.json`. O handoff v2, o arquivo Kling v1 e suas evidências permanecem intactos, com `ingest.status=pending`. Nenhuma ingestão como produtor foi executada.

## Hashes conciliados e escopo

Todos os 34 caminhos e cinco arquivos de evidência das claims do handoff técnico v2 foram re-hasheados. Exatamente dois caminhos divergem: `sites/movies-demandas/scripts/export-workspace.mjs` e `sites/movies-demandas/data/workspace-reference.json`. As cópias anteriores preservadas no arquivo Kling têm hashes idênticos aos que v2 registrou. Os outros 32 caminhos e todas as cinco evidências históricas continuam iguais.

O diff do exportador é exclusivamente a inclusão dos caminhos “Experimentos Kling” e “Lições de Elements”. No JSON derivado, mudaram somente `paths`, o resumo do catálogo (290 → 318 IDs), o hash do CSV em `sources`, a data de coleta e a versão derivada. Nada desse delta altera decisões de produção. `audit-before.json` registra hashes esperados/atuais; `exporter.diff` mostra as duas linhas adicionadas.

O handoff de arquivo Kling v1 também teve todos os 110 caminhos e duas evidências re-hasheados, sem divergência. Seus resultados anteriores de lint são históricos; não foram reescritos para parecer atuais. O novo handoff técnico conserva os 34 caminhos de v2 com hashes atuais e identifica as cinco claims herdadas como evidência histórica, não como repetição dos antigos 225/86 testes.

Guardas de concorrência cobrem 151 arquivos, incluindo ambos os handoffs anteriores, as fontes de aprovação/plano, catálogo e mídias listadas pelo arquivo. Só o novo diretório de relatório e o novo handoff são escritos nesta reconciliação. Nenhum código, exportação, mídia, aprovação, configuração, board, STATE ou registro anterior é modificado.

## Onde Andre encontra o catálogo

URL do painel em execução: **http://127.0.0.1:5173/**.

Navegação verificada no navegador: **Organização → Pontos de entrada → Experimentos Kling**. A mesma seção contém **Lições de Elements**. O cartão exibe o caminho canônico e o botão **Copiar caminho**. O URL permanece `/`; a escolha da aba usa estado React e não tem URL próprio persistente.

**É descoberta por metadados, não uma galeria integrada ao frontend.** O cartão não contém link `<a>` para o HTML, player ou comando de abertura. A consulta de `http://127.0.0.1:5173/projects/andre-time-travel/07_generations/downloads/2026-10-15-element-experiments-v1/index.html` retornou **404**. `frontend-navigation.json` registra a observação; `gallery-http.json` guarda o status e um prefixo limitado da resposta.

A galeria utilizável permanece um arquivo local: [abrir HTML local](../../projects/andre-time-travel/07_generations/downloads/2026-10-15-element-experiments-v1/index.html). Caminho absoluto: `/mnt/data/Projects_SSD/Movies_Projects/projects/andre-time-travel/07_generations/downloads/2026-10-15-element-experiments-v1/index.html`. O HTML referencia a mídia canônica sem copiá-la. Servi-lo no painel exigiria uma implementação separada; nenhuma rota, servidor ou publicação foi criada aqui.

## Verificações e limite de freshness

A checagem de exportação `export-workspace.mjs --check` passa; `check-data.mjs` também. O teste de freshness de `export-production.mjs --check` falha por um motivo anterior e separado: o snapshot registra HEAD Git `b2aca0d5e4d70d40cf4d7d13d0af88249e37684f`, enquanto a árvore atual está em `3f1461118e8f8236b8179209f20ef56e97c991c2`. A comparação com um export temporário mostrou apenas `/collectedAt` e `/provenance/repositoryHead` diferentes; nenhum conteúdo de produção ou hash de fonte diverge. O arquivo de produção foi preservado para não ampliar a correção de dois hashes. O arquivo temporário de comparação foi removido.

Essa condição já existia no final de v2: seu `closeout.json` registra o HEAD atual, enquanto o hash de `production.json` permanece o mesmo desde a entrega anterior. Assim, uma claim histórica de exportação/testes continua sendo apenas histórica. O relatório não declara ambos os exporters atuais.

Resultados de handoff, lint, validação e resume após a criação do novo registro ficam em `closeout.json`. O novo record segue pendente de revisão do produtor. A checagem direta do v2 antigo continua mostrando os dois hashes obsoletos por desenho; o lint atual reconhece a supersessão explícita.

Próximo responsável: produtor desktop revisa a reconciliação e decide qualquer ingestão. Se quiser atualizar o snapshot de produção apenas para a proveniência Git, isso fica como ação separada com guardas de concorrência; não exige mudança criativa. G-IN/G-OUT e a mídia de origem permanecem intactos. Nenhum download, upload, geração, gasto, dispatch, commit ou alteração de serviço ocorreu nesta rodada.
