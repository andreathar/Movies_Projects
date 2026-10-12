# Kling e plano mestre — relatório completo de implementação e bloqueios

Data: 12 de outubro de 2026. Entrega textual sanitizada. Este arquivo não incorpora imagens, áudio, vídeo, credenciais, identificadores de conta/Element/job do provedor, URLs assinadas ou caminhos absolutos da máquina.

## Resultado e escopo

A implementação local foi concluída no workflow já existente de Movies_Projects e no frontend correspondente. Mantivemos a integração Kling Global CLI atual, sem instalar alternativa, trocar provedor ou fazer downgrade. Código, documentação, templates, fontes canônicas e pré-visualização local foram integrados; nenhuma nova geração paga, upload, clonagem, credencial, grant, publicação ou deploy foi feito nesta implementação. A revisão complementar aqui documentada alterou somente testes e registros de entrega, sem reiniciar serviços.

O plano preserva o roteiro inglês, os IDs de falas, os cinco encontros, originais e D14. O A/B anterior está encerrado em 51 créditos declarados pelo provedor, sendo 27 + 24. Esse resultado não é cotação atual, saldo disponível, novo orçamento ou autorização para repetir os pedidos.

## O que foi implementado

- Fonte visual canônica selecionada por `workspace.json → projects[].productionPlan`, com fichas de planos, referências por função e hash, dependências, timing, geometria proposta e bloqueios. `tasks/board.json` continua sendo a autoridade dos estados de T01–T21. P0–P8 detalham etapas ligadas a essas tarefas; não são outro catálogo de tarefas.
- `scripts/production_plan.py`: validação/exportação offline, matriz de rotas, consulta dos registros locais de jobs, templates bloqueados, conferência de pedidos e hashes de revisão. A matriz contém 30 pares ferramenta/modelo do snapshot existente; não são 30 modelos únicos nem prova de disponibilidade atual.
- Sete famílias de templates: composição compartilhada, variante mínima, fala, escuta/reação, detalhe, motion control e primeiro/último quadro. As falas vêm do CSV canônico. Nomes técnicos, comandos, enums e tokens exigidos pela rota são preservados; instruções operacionais foram organizadas em português.
- Runner existente reforçado por validação de compatibilidade, liberação/cotação por pedido e proteção contra reenvio. O histórico permanece em intenções, recibos e ledger existentes; a consulta de jobs não cria outro livro de custos e cobre os registros de intenção disponíveis.
- Frontend derivado com abas Piloto, Planos, Referências, Etapas e Rotas e templates; revisão de importação e controles de atualidade por hashes. A interface não hospeda a mídia privada do filme.
- Pacote local Galileo de 16 segundos, usando somente imagens estáticas e vozes-guia existentes. Contém player, cartões, geometria e evidência técnica. Este relatório descreve o pacote, mas não o anexa nem envia sua mídia.

## Os seis planos cobrem apenas o piloto Galileo

Todas as seis fichas têm `encounter: G`. Elas preparam uma pequena sequência em torno de G-L03/G-L04; não constituem cobertura completa do capítulo Galileo ou dos outros quatro encontros.

| Ficha | Função | Família | Situação |
|---|---|---|---|
| G-MASTER | Composição compartilhada e espaço | F1 | Still proposto; não gerado nesta etapa |
| G-LISTEN-KF | Variante mínima para escuta | F2 | Keyframe proposto |
| G-P03 | Andre escuta durante G-L03 | F4 | 5 s de geração propostos, sem liberação |
| G-P04 | Fala G-L04 | F3 | 11 s de geração propostos, sem liberação |
| G-REACTION | Reação posterior à resposta | F4 | 3 s de geração propostos; 2 s no corte candidato |
| G-HAND-OPTION | Contato de mão opcional | F5 | 3 s propostos; não utilizado no animatic atual |

F6 e F7 são templates disponíveis para preparação futura, sem ficha ou job de execução no piloto atual. As durações de geração propostas são diferentes dos tempos de edição e não são orçamento.

O framework preserva Julius Caesar, Genghis Khan, Galileo Galilei, Napoleon Bonaparte e J. Robert Oppenheimer. A expansão para os cinco encontros está planejada na etapa P6, depois de provar o piloto, a voz/sincronismo e a continuidade. Nenhuma ficha dos demais encontros foi criada por herança dessas seis.

## O que continua candidato

As seis fichas estão em `proposal: proposed`, `technicalCheck: pending`, `directorApproval: pending` e `incorporation: not_incorporated`. A triagem estática das referências usa `static_checked`; isso registra inspeção estática, sem aprovar semelhança, atuação ou uso final.

São candidatos: seleção IN/OUT/olhos, composição, aparência no novo uso, enquadramento, luz, gesto, reação, ritmo, pausas, durações propostas, cobertura opcional e escolhas de rota por função. Nenhum desses campos comprova qualidade futura ou aceite criativo.

A geometria de mesa 120 × 75 × 75 cm, assento 45 cm, câmera 117,5 cm e lente 50 mm é uma proposta, sem calibração física ou EXIF comprovado. IN/OUT têm geometria visual semelhante; não são um master 3D verificado. A regra adotada mantém a cabeça histórica inteiramente fora, sem presumir aprovação de nuca e sem permitir rosto completo em reflexos.

No animatic, G-L03 começa em 0,5 s e dura 2,832 s. G-L04 começa em 4,1 s e dura 8,616 s, terminando em 12,716 s. A reação começa em 13,1 s, depois da resposta inteira. As vozes mantêm velocidade original. Esse posicionamento não é alinhamento por palavra aprovado por ouvido. Os quatro cartões foram inspecionados e a decodificação técnica passou; reprodução integral com escuta, sincronismo e aceite artístico seguem pendentes.

## Aprovação de implementação, aprovação artística e liberação de produção

São decisões diferentes:

1. **Implementação local:** autoriza código, organização, documentação, frontend e pré-visualização com mídia existente. Não libera gasto, upload, voz final ou aceite artístico. O runner recusa uma aprovação desse tipo como autorização de job.
2. **Aprovação artística:** registra a decisão real do diretor sobre artefato/versão/uso. Proposta e autochecagem técnica não bastam. O validador rejeita incorporação sem aprovação específica; uma ficha alterada depois de revisada invalida sua evidência de conteúdo. Não foi concedida nova aprovação artística.
3. **Liberação de um pedido pago:** exige entrada `kind: kling_job_release`, `status: approved`, job, fingerprint do payload, hash do schema, limite de um job, teto, validade, evidência da decisão e cotação correspondente. Upload de referência local exige escopo explícito adicional. Não existe nova liberação paga nesta entrega.

O runner não concede a decisão humana nem consulta automaticamente todos os campos artísticos do plano a partir de um spec arbitrário. Cabe ao produtor garantir que a liberação real corresponda à revisão artística necessária. Os arquivos verificam consistência documental; não autenticam a identidade de quem aprovou. O status `COMPLETED`, render local ou importação no frontend nunca concede aceite artístico.

## Bloqueios e testes efetivamente demonstrados

Os testes usam diretórios temporários, evidências sintéticas, URLs inválidas de exemplo e transporte simulado. Nenhum teste abaixo chamou Kling real, enviou referência ou consumiu créditos. Nesta revisão foram acrescentados sete testes de integração ao runner; todos passaram. Não foi reproduzida falha funcional que exigisse alterar o código de produção.

| Risco | Resultado demonstrado | Evidência de teste |
|---|---|---|
| Referência local ausente | O runner interrompe antes de descoberta, saldo, upload ou geração. | `test_absent_reference_blocks_runner_before_discovery` |
| Referência local alterada após liberação/cotação | Mudar os bytes muda o fingerprint; a liberação deixa de corresponder. Zero chamadas ao provedor. | `test_changed_local_reference_blocks_runner_before_discovery` |
| Fonte preservada ou pacote desatualizado | Hash divergente do roteiro falha; fontes de plano divergentes são rejeitadas; exportadores `--check` detectam deriva e não escrevem. | `test_preserved_source_drift_is_error`; testes frontend de fonte obsoleta e idempotência/deriva do export |
| Combinação incompatível | Turbo com controles não declarados é recusado pelo preflight. Nesse teste, só ocorre uma chamada **simulada** de descoberta `who_am_i`; saldo/upload/geração não ocorrem e não há intenção de envio. | `test_incompatible_model_blocks_after_only_readonly_discovery` |
| Liberação paga pendente | `status: pending` impede qualquer descoberta/saldo/envio. Aprovação de implementação também não libera job. | `test_pending_release_blocks_runner_before_discovery`; `test_missing_scope_stops_runner_before_any_provider_call` |
| Aprovação artística ausente ou ficha alterada | Incorporação sem aprovação falha; aprovação de ficha exige hash e selector corretos, e deixa de valer se o conteúdo mudar. | `test_incorporation_is_not_technical_check`; `test_approval_without_hash_evidence_fails`; `test_shot_approval_is_bound_to_content_and_exact_selector` |
| Cotação obsoleta/inválida | Cotação expirada para antes de descoberta. Outros testes recusam payload diferente, data futura, evidência alterada, estimativa, moeda/unidade inadequada e custo acima do teto. | `test_expired_quote_blocks_runner_before_discovery`; `test_expired_or_wrong_payload_quote_is_blocked`; `test_changed_price_evidence_blocks`; `test_quote_cannot_be_estimate_wrong_currency_or_above_cap` |
| Dupla submissão | Evidência de envio/resultado/intenção impede repetir o mesmo job; conteúdo idêntico também bloqueia outro nome, incluindo intenção sem recibo. | `test_all_evidence_markers_fail_closed`; `test_renamed_intent_only_blocks_runner_before_discovery`; `test_legacy_intent_and_equivalent_input_alias_detected` |
| Transporte incerto | Timeout simulado registra intenção e resultado incerto. Nova tentativa no mesmo nome, renomeação e retomada sem ID não fazem novo envio; estado continua `SUBMISSION_UNKNOWN`. | `test_uncertain_transport_is_durable_with_actual_release_gate`; `test_timeout_uncertainty_is_durable_and_never_retried` |
| Duração/Element/audio incompatíveis | Cobertos limite combinado condicional, vídeo Omni com áudio nativo, mistura de tipos de Element, v2.6 cauda/áudio/resolução e referência de 30 s tratada indevidamente como 5 s. | Testes de `ConditionalContractTests` e contrato Kling |
| Custo e saldo confundidos | Cobrança declarada zero prevalece sobre variação de saldo; cobrança desconhecida permanece desconhecida, sem aprovação artística inferida. | `test_provider_zero_charge_beats_concurrent_balance_delta`; `test_unknown_charge_stays_blank_not_balance_delta`; `test_readonly_registry_keeps_unknown_charge_and_no_acceptance` |

Os nomes acima estão em `tests/test_kling_release.py`, `tests/test_kling_contract.py`, `tests/test_kling_batch.py`, `tests/test_production_plan.py` e nos testes de modelo/export do frontend.

É importante distinguir **zero submissões** de **zero chamadas de descoberta**: o preflight ao vivo consulta capacidades antes de validar a combinação, mas antes de saldo/upload/geração. Referência ausente/alterada, liberação pendente, cotação vencida e evidência prévia barram o pedido ainda antes dessa descoberta. Nos testes, até a descoberta é simulada.

## Limites que os testes não transformam em garantias

- URLs remotas são vinculadas pelo URL exato; o fingerprint não baixa nem comprova os bytes remotos. `inputFacts` registra fatos declarados; o produtor deve vinculá-los à mídia real. Alterar esses fatos invalida a liberação testada.
- Snapshot, schema e guias são datados. Presença de uma rota não comprova preço, disponibilidade atual, áudio silencioso, semelhança ou qualidade. Ausência de controle de áudio no Turbo não garante silêncio.
- Cotação/teto são verificações locais. Não há teto atômico imposto no servidor por esse mecanismo. Cobrança reportada acima do teto é registrada e sinalizada, sem autorizar novo envio.
- A deduplicação não é uma garantia universal do provedor nem um detector de toda equivalência semântica. Ela protege os registros e fingerprints conhecidos; não deve ser contornada mudando prompt ou nome.
- Os controles não impedem invocação manual externa do executável. Não foram criadas permissões ou credenciais para ampliar acesso.
- Conferência de hashes, duração, decode e inspeção de cartões não substituem escuta, revisão temporal, avaliação de semelhança ou aceite humano.

## Atualização e verificação do frontend

A fonte de produção permanece no Movies. Os exportadores existentes geram os dois snapshots do site; a interface lê esses dados derivados. O processo é:

1. Revisar a mudança na fonte canônica e seus hashes. Se as fontes do catálogo mudarem, atualizar o catálogo pelo gerador existente e revisar seu diff.
2. No diretório do frontend, executar os dois exportadores com a raiz Movies explícita:

```sh
node scripts/export-production.mjs /caminho/Movies_Projects
node scripts/export-workspace.mjs /caminho/Movies_Projects
node scripts/export-production.mjs /caminho/Movies_Projects --check
node scripts/export-workspace.mjs /caminho/Movies_Projects --check
npm run check:data
```

3. Conferir testes de modelo/export, lint, TypeScript e build em sequência. `--check` compara contra as fontes atuais e falha sem escrever; `check:data` verifica a integridade interna dos pacotes, não a atualidade de um workspace remoto ausente.
4. Caso exista um retrato persistido na aplicação, usar **Fontes e histórico → Revisar atualização**, conferir diferenças e confirmar a importação. O snapshot incluído numa versão não substitui silenciosamente o retrato persistido. Demandas/comentários são preservados; a importação não altera arquivos do filme nem concede aprovação.
5. Publicação, deploy ou importação numa instância real exigem escopo próprio. Não foram feitos nesta entrega.

Nesta implementação, os candidatos foram gerados em cópia isolada, as fontes/destinos foram hash-guarded e os checks passaram no checkout real. Um commit concorrente avançou o HEAD principal; ele foi preservado. Os snapshots receberam apenas a coleta/proveniência Git nova, mantendo o mesmo conteúdo. Não houve reset, rebase ou commit feito por este executor.

O QA de navegador usou o modo de desenvolvimento nativo numa cópia isolada com banco local novo. Funcionaram carregamento, cinco abas, filtro Turbo, diálogo de diferenças e importação explícita. Foram preservadas 21 tarefas e nove demandas da base de teste; não houve erro de console capturado. A captura de screenshot falhou no backend do navegador: o QA por DOM/interação não certifica layout visual completo ou viewport móvel. O servidor próprio foi encerrado ao fim da implementação e não foi reiniciado nesta revisão.

## Resultados de verificação e o que foi repetido

- Fechamento original: **146 testes Python**, **24 testes frontend**, ESLint, TypeScript e build passaram. Gestão, catálogo, handoff, integridade e ambos os checks de freshness passaram. Permaneceram três avisos conhecidos de hashes das skills compartilhadas.
- Revisão complementar: **67 testes Kling e 12 testes do plano passaram novamente**, incluindo sete novos casos de integração. Total de 79 testes pertinentes executados nesta revisão. A suíte completa de 146 e o build não foram apresentados como novas execuções; código de produção/frontend não mudou.
- O ajuste complementar é de cobertura e evidência. Não foi necessário corrigir código de produção para os cenários pedidos. Histórico, mídia e registros de custo foram preservados.

## Bloqueios atuais e próximo responsável

| Responsável | O que falta | Evidência necessária |
|---|---|---|
| Produtor | Revisar a integração e o handoff | Diff, checks e fontes correspondentes; ingestão real, sem presumir aceite |
| Andre / diretor | Composição, semelhança, geometria candidata e ritmo | Decisão sobre versões e usos específicos |
| Andre + dialogue-sound | Voz final e prova de dublagem/sync | Escuta dos candidatos existentes e decisão conforme D14 |
| Continuity / produtor | Qualificar atuação e Element antes de eventual uso | Trecho adequado, direitos/função, duração e readback autorizado |
| Produtor | Preparar eventual novo job | Pedido exato, schema, cotação atual, teto e autorização específica; sem herdar o A/B |

A implementação está entregue; a produção artística e a execução paga continuam condicionadas às decisões acima. Este relatório textual é a única peça destinada à Library nesta revisão. Nenhuma nova mídia com aparência ou voz foi anexada.
