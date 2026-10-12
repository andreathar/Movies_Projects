# Implementação local do plano mestre — 12/10/2026

A implementação autorizada por Andre (“implemente”, referência recebida `Sentinel_f0a1320120308191a8233b16bf8df20c`, 08:29:50 UTC) está integrada ao workflow canônico e ao frontend local. Nenhum novo job pago, upload, voz, Element, grant, credencial, instalação de alternativa, publicação ou commit foi feito nesta etapa. Os 51 créditos do A/B pertencem aos dois jobs anteriores, encerrados.

## Entregas

- Fonte única selecionada por `workspace.json`: [production-plan.json](../projects/andre-time-travel/05_storyboard/source/production-plan.json). P0–P8 vinculam as tarefas T01–T21; o board mantém seus estados. Seis fichas, 13 referências triadas, dependências, fontes/hashes, geometria e bloqueios. Proposta, checagem, aprovação e incorporação são separadas.
- [Contrato e comandos](../docs/PRODUCTION_PLAN.md): `check`, `routes`, `jobs`, `template`, `check-request` e `review-hashes` são offline. As 30 combinações ferramenta/modelo derivam do snapshot existente, sem fingir disponibilidade ou preço atuais. Templates F1–F7 saem bloqueados e puxam texto inglês do CSV.
- Runner existente com validação condicional de inputs, Element, vídeo/audio/cauda, duração motion e limites combinados. Nova submissão exige liberação por job/payload/schema e evidência de cotação; estimativa e teto antigo não bastam. Duplicata/estado incerto bloqueia reenvio com outro nome. Jobs/custos continuam em intenções/recibos/ledger; não foi criado segundo livro de custos.
- [Pacote Galileo G-L03/G-L04](../projects/andre-time-travel/05_storyboard/animatics/galileo-g03-g04-v1/README.md): [player local](../projects/andre-time-travel/05_storyboard/animatics/galileo-g03-g04-v1/index.html), [MP4](../projects/andre-time-travel/05_storyboard/animatics/galileo-g03-g04-v1/animatic.mp4), quatro cartões, geometria e evidência de render. **16 s**, 24 fps; imagens/vozes-guia já existentes. G-L04 acaba em 12,716 s; reação inicia em 13,1 s. Falas não aceleradas. A inspeção estática dos quatro cartões confirmou labels legíveis e ausência de rosto histórico completo. Não equivale a escuta, atuação ou sincronismo aprovados.
- Frontend existente acrescido do painel de piloto, fichas, referências, etapas e capacidades/templates; snapshots atuais e importação com revisão explícita. Nomes técnicos, comandos, enums, schemas e tokens exigidos permanecem intactos. Instruções operacionais atualizadas em português; inglês criativo e arquivos históricos são preservados.

## Verificação executada

- **146 testes Python** e **24 testes frontend** passaram, sem provedores reais. Incluem falhas antes de submissão, schema incompatível, teto/cotação, retry renomeado, duração declarada alterada, revisão de ficha invalidada por mudança, dependências e importação preservando demandas/comentários.
- ESLint e TypeScript passaram. Build de cinco fases passou na cópia isolada com fontes idênticas ao checkout e o mesmo conteúdo de produção/catálogo. A atualização posterior de proveniência Git não alterou esse conteúdo; foi conferida pelos exportadores e `check:data`. Execuções em sequência, sem duplicação concorrente de builds.
- Catálogo `--check`, hash da mídia/plano, ambos exportadores `--check` e `check:data` passaram. Os 135 arquivos da cópia QA correspondem aos arquivos do frontend real.
- Navegador suportado em `127.0.0.1:5173`, com modo local nativo existente e D1 novo isolado: inicialização, cinco abas, busca Turbo, diálogo de diferenças e confirmação de importação funcionaram. Nova versão `6813956e…3479`; 21 tarefas e 9 demandas preservadas. Nenhum erro de console capturado. Aba original restaurada e servidor próprio encerrado.
- **Limite de UI:** captura de screenshot falhou no backend do navegador. QA por DOM/interação foi concluído; layout visual completo e viewport móvel não foram certificados. A imagem/áudio do animatic não foi enviada ao navegador nem a terceiros.

Evidência detalhada: [checks](2026-10-12-master-plan-implementation-checks.json). Logs, cópia QA, bases/patches e controles de concorrência: `/home/athar/Documents/Codex/2026-10-12/task/kling-plan-implementation`. A verificação final de `manage.py validate/lint/resume`, handoff e diffs será registrada em `final-verification.json` nessa área após a criação do handoff; este relatório não antecipa o resultado.

## Preservação e integração

Roteiro inglês, CSV, cinco encontros, D14 e fontes preservadas passaram por hash. Sem exclusão de mídia, originais ou histórico. Todos os 33 arquivos históricos acompanhados que não receberam alteração desta entrega, incluindo ledger/recibos A/B, mantêm os hashes do handoff anterior. O A/B continua v3=27 e Turbo=24 créditos, sem novo envio. Nenhuma aprovação artística ou tarefa foi promovida para concluída.

As alterações foram aplicadas com bases SHA-256 e reconferência no momento da escrita; mudanças concorrentes fariam abortar o lote. Durante o fechamento, um commit concorrente avançou o HEAD principal de `0592f54cce23f94dd061f1e490ad0b1412e84f77` para `0a6a7d33558f9f5110100c89dbaed0fb46897ba0`. Ele foi preservado; este executor não criou o commit. Os hashes de conteúdo implementado permaneceram iguais; somente coleta/referência Git dos snapshots foram atualizadas e reconferidas. HEAD do frontend `dfb945f3aaaf5aaac20ed323cda66dd26d047bb9`. Trabalho preexistente foi preservado. Catálogo recebeu apenas o novo hash de AGENTS; registry/adaptadores não foram redesenhados. Permanecem avisos conhecidos sobre hashes das três skills compartilhadas.

O novo handoff supersede `2026-10-12-kling-ab-min-v2.json` somente como visão atual dos hashes alterados pela implementação. O arquivo anterior e suas evidências financeiras permanecem intactos, sem reescrever afirmações históricas. Ingestão/revisão do produtor continua pendente; nenhum aceite foi inventado.

## Próximo responsável e limites

**Produtor da conversa principal:** revisar diff e handoff, apresentar o pacote Galileo a Andre e registrar decisões por versão/uso. **Andre/diretor:** composição/semelhança, geometria candidata e ritmo. **Andre + dialogue-sound:** escuta dos candidatos existentes, voz final e prova de dublagem/sync conforme D14. **Continuity/produtor:** qualificar atuação existente e readback do Element antes de eventual uso. Só depois preparar cotação e autorização para um pedido específico; nenhum novo gasto está liberado.

O animatic é uma pré-visualização estática. Os controles locais verificam consistência documental, não autenticam quem aprovou e não impõem teto atômico no servidor. Disponibilidade/preço/qualidade reais e operações manuais externas à CLI não são garantidos por estes checks. Publicação e importação em instância real permanecem fora do escopo; somente a base descartável da cópia QA recebeu importação neste trabalho.

A revisão automática inicialmente bloqueou um delta por ownership antigo do frontend. Após conferir que o refresh anterior estava concluído e reapresentar a atribuição atual, o mesmo lote foi aprovado e aplicado. A tentativa de enviar checkpoint diretamente à conversa principal permaneceu bloqueada por falta de autorização humana explícita para mensageria entre tarefas; este handoff e o encerramento da tarefa disponibilizam a entrega sem contornar esse bloqueio.
