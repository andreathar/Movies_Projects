# Plano de produção: fonte, preparação e execução

Andre autorizou implementar o plano mestre em 2026-10-12, às 08:29:50 UTC. A aprovação `APR-master-plan-local-2026-10-12` cobre código, organização, frontend e pré-visualização local com mídia existente. Não concede aprovação artística, gasto, upload de aparência/voz, clonagem, credenciais, publicação ou migração de provedor.

## Uma fonte por assunto

- `workspace.json` → `projects[].productionPlan`: fonte editável dos planos visuais, referências por função/hash, dependências, geometria, timing e bloqueios. Para este episódio: `05_storyboard/source/production-plan.json`.
- `tasks/board.json`: situação oficial de T01–T21. P0–P8 detalham a preparação e vinculam essas tarefas; não substituem o board.
- `01_script/script-en.md` e `dialogue-lines.csv`: texto inglês e IDs. Templates leem a fala do CSV, sem manter cópia editável paralela.
- Catálogos de IN/OUT e estudos: inventário completo das variantes existentes. A fonte visual seleciona apenas referências necessárias e cita esses catálogos.
- `00_brief/approvals.json` e decisões: escopos reais. Proposta, checagem técnica, aprovação do diretor e incorporação artística têm campos separados. Um render ou `COMPLETED` não promove nenhum deles.
- `07_generations/responses/*.intent/submit/response/balance.json` e `credit-ledger.csv`: jobs e custos; `production_plan.py jobs` apenas os apresenta. Os 51 créditos do A/B estão encerrados.
- Frontend: retrato derivado, com hashes e revisão de importação. Não contém mídia privada nem altera a aprovação canônica.

O plano mestre entregue e seu anexo ficam em `tasks/plans/master-production-v1/` como proposta datada, com nota da implementação autorizada. Regras em documentos antigos que conflitem com o schema por modelo, D14 ou o contrato atual não liberam pedidos.

## Comandos locais sem rede

```sh
python3 scripts/production_plan.py check --verify-media
python3 scripts/production_plan.py routes
python3 scripts/production_plan.py jobs
python3 scripts/production_plan.py review-hashes
python3 scripts/production_plan.py template --family F3 --shot G-P04
python3 scripts/manage.py validate
python3 scripts/manage.py lint
```

O template é uma **proposta bloqueada**, não um comando de geração. Slots com `<...>` precisam de seleção; a fala de G-P04 já vem do texto canônico. F1 composição, F2 variante mínima, F3 fala, F4 reação/escuta, F5 detalhe, F6 atuação e F7 primeiro/último quadro têm parâmetros por rota. Não transformar a recomendação de modelo em qualidade comprovada. `check --verify-media` confere arquivos e hashes, não faz inspeção visual, biometria ou escuta.

`manage.py validate/lint` inclui a consistência do plano sem copiar/decodificar mídia. O preflight valida tipos, slots, enums, limites combinados condicionais, tipo de Element quando declarado, exclusão de áudio nativo com vídeo Omni, cauda/áudio/resolução v2.6 e duração de motion. Para vídeos locais usa `ffprobe`; URLs exigem fatos registrados (`inputFacts`), cujo conteúdo não é baixado/verificado por esse campo. O produtor continua responsável por ligar esses fatos ao arquivo real e pelo readback do Element.

## Preparação, revisão e incorporação

`states.proposal` registra rascunho/proposta; `technicalCheck` registra pendente, estática, checada ou falha; `directorApproval` permanece pendente até evidência real; `incorporation` registra uso artístico. Aprovação exige artefato/hash/escopo correspondente. Uma mudança de conteúdo invalida a evidência. A implementação de software no checkout não é incorporação artística dos candidatos na obra.

O animatic de Galileo usa imagens estáticas e guias existentes. Seu player e labels preservam essa condição. O builder recusa sobrescrever preview existente, verifica hashes e cria derivados em nova revisão. Limita threads e não chama geração, STT, instalação ou serviços externos. Roteiro, áudios e imagens de origem são preservados. A reação vem após a resposta inteira; alinhamento de palavras por ouvido continua pendente.

## Liberação obrigatória antes de um novo envio

O runner agora recusa apenas `auth` em texto livre. Para um novo envio, o produtor precisa registrar uma entrada `kind: "kling_job_release"`, `status: "approved"` em `00_brief/approvals.json`, com:

- `id` igual ao `auth` do spec e `decisionEvidence` com `path` relativo ao filme e `sha256` da decisão real;
- `scope.job`, `payloadSha256`, `schemaSha256`, `maxJobs: 1`, `maxCredits`, `expiresAt` com fuso;
- `scope.quote`: `basis` igual a `official_panel` ou `provider_quote`, `unit: "Kling credits"`, `credits`, `payloadSha256`, `verifiedAt`, `expiresAt`, `evidence` com caminho/hash;
- `allowReferenceUploads: true` somente se o escopo real inclui upload dos arquivos locais exatos desse pedido.

Para preparar a revisão, `production_plan.py check-request --spec PEDIDO.json` retorna o fingerprint e o hash do schema somente quando o preflight offline passa; não concede liberação. `review-hashes` identifica o conteúdo de cada ficha, excluindo seus estados/evidência de aprovação. A decisão de uma ficha usa `artifact.selector` com seu ID e `artifact.sha256` com esse hash, além do revisor e escopo; referências usam hash do arquivo.

Não existe liberação paga nova nesta entrega. `shared/templates/kling-job-release.json` documenta o formato com estado pendente e campos vazios. Nunca preencher esse template como aprovação por conta própria. Uma estimativa, unidade de API de desenvolvedor, diferença de saldo ou teto antigo não satisfaz a cotação.

O fingerprint normaliza aliases e referências locais por hash, excluindo nome do job/nota/auth. A intenção anterior com conteúdo idêntico bloqueia envio sob outro nome, inclusive após timeout. Repetição deliberada do mesmo conteúdo exige reconciliação e revisão técnica explícita do mecanismo; esta versão não oferece bypass de retry. O produtor não deve mudar um caractere para contornar o bloqueio.

A ordem é: bloqueio de rascunho/evidência existente → identidade do conteúdo → liberação/cotação → schema ao vivo e igualdade com a revisão → saldo suficiente → intenção durável → envio único → recibo/ID → reconciliação → consulta posterior com `--resume`. Erro ou ausência de ID permanece incerto. Uma cotação rejeitada não faz chamada de conta, descoberta, upload ou geração. A retomada de IDs antigos não exige nova liberação, pois não submete.

**Limites técnicos:** estes arquivos verificam consistência documental e não autenticam quem aprovou. Não são novos grants ou permissões do sistema. Não impedem uso manual externo do executável. Preço/teto são verificações locais; o provedor não oferece aqui um teto atômico no servidor. Se a cobrança declarada superar o teto, o runner registra o resultado e encerra com erro, sem novo envio. Defaults, regras textuais e capacidades futuras ainda exigem revisão; snapshot não prova disponibilidade atual.

## Atualização do frontend e checagens

O exportador existente incorpora a fonte selecionada via `production_plan.py export`; valida o plano e todos os hashes de textos consumidos. O frontend mostra fichas, funções das referências, preparação/dependências, timeline candidata, rotas/templates e pendências, sem conceder aprovações. Snapshots antigos persistidos exigem revisão/importação; demandas e comentários são preservados.

`export-production.mjs --check` e `export-workspace.mjs --check` com a raiz Movies verificam freshness contra as fontes locais. `check:data` verifica a integridade do pacote incluído, sem alegar freshness de um workspace remoto ausente. Antes da entrega: testes stdlib e frontend, lint, tipos, exports e build, em sequência. Nunca executar smoke tests de geração para conferir esses controles.
