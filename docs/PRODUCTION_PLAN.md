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

## Base ativa Galileo · 2026-10-13

Andre delegou a escolha da abordagem em `Sentinel_1f1c130dfa648191aad0d6afc0c49d7b`.
`activeBaseline` no plano existente é a única entrada ativa para G-L03/G-L04: sete
fontes por ID/hash, achados T12 consolidados, seis etapas com responsáveis/entradas/
dependências/aceite e decisões abertas. A seleção é proposta; não altera aprovações.
O primeiro teste de fala futuro é G-P04, após continuidade, timing e liberação específica.

O frontend mostra essa base local atual mesmo antes de importar o novo retrato de
produção; a exibição não modifica demandas, comentários ou aprovações persistidas.
O fluxo de revisão/importação continua disponível para o restante dos registros.
Takes anteriores permanecem nos caminhos originais como história. O animatic de 16 s
é evidência de timing, não atuação. A busca delimitada por Galileo v2 não encontrou
seus arquivos no projeto/drafts/reports e outputs conhecidos; recuperar se aparecer,
sem bloquear esta base ou reconstruir uma entrega não localizada por suposição.

## Comandos locais sem rede

```sh
python3 scripts/production_plan.py check --verify-media
python3 scripts/production_plan.py check-coherence
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

## Coerência cinematográfica offline

`python3 scripts/production_plan.py check-coherence` lê as fichas da fonte já apontada
por `workspace.json` e seus templates. `--shot ID --spec PEDIDO.json` confronta uma
ficha com um único pedido exato; sem `--spec`, placeholders continuam como pendências.
Não cria catálogo, referência, teste pago, job ou aprovação. O comando também alimenta
`manage.py lint`: erros documentais entram em `hard`, avisos em `advisory`, inclusive
os reconhecidos com justificativa. `resume` conserva essa contagem. Continua separado
de `check`/`check-request` e do runner; não é um novo gate de submissão. Executar os
controles existentes de contrato e liberação continua necessário.

O resultado preserva avisos com trechos de evidência. Somente `ERROR` causa saída 2:

| Classe | Exemplos | Tratamento |
|---|---|---|
| Erro documental determinístico | Durações estruturadas diferentes; segmentos com lacuna/sobreposição, NaN ou fora do total; binding duplicado/ausente; flags de inspeção contraditórias | Corrigir dados; não dispensável por override |
| Aviso semântico ou falta de prova | Câmera fixa e movimento no texto; duração textual; silêncio sem controle explícito; função/origem da referência; URL/placeholder sem hash confirmado | Revisar contexto; pode ter justificativa vinculada ao conteúdo |
| Limite informativo | Câmera fixa seguida de movimento em segmentos válidos; inspeção estática/parcial | Não confere execução, qualidade ou aceite |

Anotações opcionais pertencem a `shots[].coherence` na fonte existente. Não são
argumentos da API e não devem ser copiadas para `args`. Exemplo sintético de estrutura:

```json
{
  "segments": [
    {"startSeconds": 0, "endSeconds": 2, "camera": "locked"},
    {"startSeconds": 2, "endSeconds": 5, "camera": "moving"}
  ],
  "audioIntent": "post_dub",
  "referenceBindings": [
    {"slot": "first_image", "referenceId": "ID_JA_NO_CATALOGO", "role": "composition"}
  ],
  "inspection": {
    "method": "sampled_frames",
    "fullPlaybackCompleted": false,
    "fullFrameInspectionCompleted": false,
    "audioAuditionCompleted": false
  },
  "overrides": []
}
```

Segmentos descrevem toda a janela, em ordem, contíguos, de zero até
`proposedGenerationSeconds`/`args.duration`, tolerância de 0,001 s. `locked`/`moving`
descrevem intenção de câmera, não desempenho observado. Um plano fixo pode depois
mover: não há proibição global dessa sequência. O reconhecimento textual é limitado,
principalmente ao inglês e a alguns termos portugueses; negação ou escopo temporal
podem gerar falso positivo. A ausência de aviso não comprova coerência.

`audioIntent`: `silent`, `native_guide`, `external_audio`, `post_dub` ou `unspecified`.
Omissão significa não declarado. “No speech” não significa faixa sonora silenciosa.
Slots vêm do mapeador já existente do preflight e do snapshot; não se deduz suporte de
áudio pelo nome do modelo. `post_dub` não alega que dublagem ou sincronismo foram feitos.

Bindings apontam referências selecionadas pelo ID, sem copiar seus hashes/origens.
Função diferente da registrada exige revisão; não reclassifica o original. Caminho
igual não verifica bytes, URL/placeholder não prova versão. Usar `check --verify-media`
para os hashes locais; o produtor ainda precisa vincular o arquivo exato ao pedido.
Nenhuma inspeção visual ou autenticação de autoria é realizada por este comando.

`inspection.method` descreve somente a revisão visual: `not_reviewed`, `metadata_only`,
`sampled_frames`, `all_frames`, `full_playback`, `full_playback_and_frames`.
Audição é independente. Flags verdadeiras devem citar `evidence` (referência ao relato
existente); sua ausência avisa, sua presença não autentica a inspeção. O estado do
player não prova audição. Aprovação/incorporação continuam em `states` e
`approvalEvidence`, verificadas pelo mecanismo existente de escopo/hash; não são
inferidas de `COMPLETED`, arquivo presente ou inspeção técnica.

Override reconhece um aviso sem removê-lo: `{code, reason, reviewer, subjectSha256}`.
Usar o hash em `subjects` do relatório correspondente, que inclui ficha, catálogo de
referências e pedido, excluindo somente `coherence.overrides`. Alterar qualquer um
desses dados torna o reconhecimento obsoleto. `WARN` permanece `WARN`, com
`acknowledged=true` e justificativa. Isso não é aprovação do diretor nem liberação
financeira. Overrides de erro, sem motivo/revisor, obsoletos ou sem aviso falham.

O frontend aceita e mostra essas anotações opcionais na ficha, sempre como declarações.
Pacotes anteriores sem `coherence` continuam legíveis. Importar uma anotação ou uma
justificativa não muda os estados de aprovação, as demandas ou os comentários.

### Matriz de cobertura das propostas CINE-G-01/02

Esta matriz limita a interpretação das duas propostas existentes; não cria novos
pedidos. **Ambas estão não executadas, não testadas e sem aceite criativo.**

| Dimensão | CINE-G-01 — escuta sustentada | CINE-G-02 — escuta atenta | Evidência efetiva atual |
|---|---|---|---|
| Escuta e estabilidade no G-IN | Objetivo do ensaio | Objetivo do ensaio | Nenhuma saída destas propostas |
| Microajuste corporal | Respiração discreta | Inclinação aproximada após 2 s | Intenção textual, não atuação comprovada |
| Diálogo visível / articulação | Fora do escopo | Fora do escopo | Não validado |
| Voz / timbre / prosódia / dublagem | Áudio desligado | Áudio desligado | Não validado; D14 preservado |
| Sincronismo labial | Sem fala | Sem fala | Não validado |
| Movimento motivado de câmera | Câmera fixa | Câmera fixa | Não validado |
| Continuidade entre cortes | Plano único | Plano único | Não validado; duas variantes não são uma sequência montada |
| Identidade, mãos, mesa e rosto histórico ao longo do clipe | Critérios de revisão futura | Critérios de revisão futura | Imagem inicial não comprova todos os quadros; likeness depende de Andre |

Exemplos históricos orientam perguntas, não aprovam estas propostas: versões com
tilt/órbita e câmera fixa, texto de 3 s em resultados de 8/10 s, e cabeça já presente
na segunda referência mostram por que separar prompt, duração e entradas. A evidência
original (inclusive chips concatenados da interface e autoria desconhecida) deve ser
preservada, sem corrigir o texto retrospectivamente ou alegar causalidade pelo idioma.

## Revisão explícita de imagens no servidor local

Em Produção do filme → Base ativa, cada uma das sete referências tem “Revisar imagem”. Ampliar e comentar continuam sem efeito de aprovação. O diretor informa nome, escopo, parecer e decisão, e confirma o hash exato. Aprovar/rejeitar atualiza somente `references[].states.directorApproval` e `approvalEvidence`; solicitar alterações mantém `pending` e registra `gate: image_changes_requested`. Nenhuma dessas ações incorpora a imagem na obra, fecha tarefas, altera aprovações globais ou libera gastos.

O servidor local existente usa identidade local e origem/loopback restritos; a identidade declarada do revisor não é assinatura digital. A rota não é incluída no build publicado. Cada tentativa usa UUID idempotente e hash do plano lido ao abrir a revisão, além do hash dos bytes da imagem. Versão divergente retorna conflito, preserva o parecer e exige nova confirmação após atualização. Uma decisão substituída mantém sua evidência; os novos registros imutáveis ficam em `00_brief/decisions/image-reviews/`, no formato de `shared/templates/review-decision.json`, com hashes do artefato, plano anterior e tentativa. O plano é substituído atomicamente sob lock de revisão; o lock não impede edições externas não cooperantes.

Após salvar, a rota atualiza o export de produção. Se o export falhar, o aviso distingue decisão canônica salva de pacote pendente; a consulta local continua trazendo o registro canônico. A página inteira deve ser recarregada após mudança do arquivo de imagem; alterações de conteúdo nunca herdam a decisão antiga. Não apagar evidências para desfazer uma decisão: registrar uma decisão sucessora explícita; imagens já incorporadas precisam de reconciliação do produtor antes de rejeição ou alteração.

QA de escrita usa fixtures descartáveis, nunca falsas aprovações nos registros de produção. O harness de navegador só existe em dev com `MOVIES_REVIEW_QA=1`, em `/__local/reference-review-fixture`, com mídia e plano sintéticos em diretório temporário. A instância entregue ao diretor deve iniciar sem essa variável.

A gravação de uma decisão também atualiza somente o `sha256` do ponteiro já selecionado em `07_generations/plans/current-plan.json`, preservando caminho, adoção, histórico e estado sem liberação paga. Ponteiro divergente bloqueia uma nova decisão antes de gravar. Se a decisão foi salva mas a atualização do ponteiro foi interrompida, a repetição da mesma tentativa idempotente reconcilia esse checksum quando o ponteiro ainda corresponde ao plano anterior exato; nunca adota outro plano nem remove a evidência.
