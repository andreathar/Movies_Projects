# Campos das respostas do Kling

A CLI retorna `{ ok, status, body }`; `status` externo é do envelope, enquanto
`body.status` é o estado da geração. Não confunda exit code, sucesso de consulta,
sucesso de geração e aceite artístico. CamelCase é o contrato atual; respostas
antigas podem usar snake_case. Veja [SKILL.md](SKILL.md) e [api-examples.md](api-examples.md).

## Descoberta

`who_am_i`: `body.availableModels[tool].models[]` contém `model`, `alias`,
`description`, `arguments[]`, `inputs[]` e eventualmente `combinedItemCap`.
Formatos legados podem apresentar listas diretamente; confirme antes de consumir.
`user.userId` é identidade da conta e deve ser omitido dos snapshots compartilhados.
`authMode` informa o modo de autenticação; `mcpVersion` identifica o contrato retornado.

- `arguments[]`: `name`, `required`, `default`, `allowedValues`, `description`,
  eventualmente `maxItems`. Não trate ausência de enum como autorização para qualquer
  combinação: descrições e servidor ainda podem impor regras.
- `inputs[]`: `name`, `required`, `description`. Recursos enviados ao serviço usam URLs;
  a CLI converte arquivos locais em URLs por upload autorizado.
- `combinedItemCap`: `{maxItems, inputPrefixes, arguments}`. Some os slots com os
  prefixos listados e os itens dos argumentos de lista indicados. Não some limites
  individuais como se fossem a permissão total.
- `tool_list`: `body.tools[]` traz `name`, `description` e `inputSchema`.
  Ajuda por comando tenta consultar esses dados e tem fallback estático.

## Submissão e consulta

As seis ferramentas de geração retornam `generationId`, `status` e, quando presente,
`creditsConsumed`. O ID é opaco e só pode vir da resposta real. Sem ID após envio,
a submissão é incerta; rastreio não substitui ID.

`query_tasks` devolve `generationId`, `status`, `createTime`, `finishTime`, `works[]`.
Os tempos podem ser timestamps em milissegundos; fim 0 pode significar não concluído.

| Categoria | Estados conhecidos |
|---|---|
| Em andamento | `submitted`, `pending`, `QUEUING`, `queueing`, `processing`, `RUNNING` |
| Sucesso a conferir | `COMPLETED`, `PARTIAL_COMPLETED`, `succeed`, `succeeded`, `success` |
| Falha/cancelamento | `FAILED`, `CANCELLED`, `CANCELED` |

Estados desconhecidos não são sucesso. Cada work pode ter seu próprio `status`,
`contentType` (`image`/`video`), `url`, `urlWithoutWatermark`, `coverUrl` e
`coverUrlWithoutWatermark`. URL padrão é a entrega normal; preserve links e bytes.
Vazio/parcial exige comunicar a limitação, não repetir submissão automaticamente.

Com `--poll`, o envelope pode conter `body.polled`, `body.timedOut` e
`body.generations[] = {generationId, status, result}`; `result` é o último corpo de
consulta. O timeout de consulta não comprova cancelamento da geração.

## Upload, Elements e movimentos

`file_upload` obtém `ticket`, `uploadUrl` e `expireAt`; a CLI envia o arquivo e
normaliza o resultado em `body.url`. Tickets são de uso único. Não compartilhe
bilhetes/URLs assinadas em logs públicos nem implemente upload HTTP por fora da CLI.

`element_create` retorna `id` persistente, não `generationId`; não use `query_tasks`
para Element. `element_list` pode listar só id/name; `element_get` fornece `name`,
`description`, `resource`, `tags`. Imagem: `cover` e `secondary[]`; vídeo: `video`;
`voice` opcional conforme contrato. `element_update` preserva o cover existente,
mescla campos e substitui a lista secondary inteira quando fornecida.
`element_delete` apaga o sujeito identificado e exige instrução específica.

`motion_library_list` pode trazer id, nome, URL, capa, duração em milissegundos e
presença de áudio. Registre unidade e duração real; converta ms para segundos uma vez.
`motion_control` retorna o mesmo contrato de geração. `keepOriginalSound=false`
remove a solicitação de reter som da referência; não é prova de silêncio final.

## Conta e operações auxiliares

`account` encaminha `query_membership_and_credits`. Campos: `userId`,
`membershipType` (`NORMAL`, `VIP`, `SVIP`, `SSVIP`, `SSSVIP`) e
`availableRemainCredits` (créditos visíveis, sem conversão). É observação pontual,
não cotação. Links de assinatura/recarga podem estar na descrição da ferramenta;
não os invente nem compre automaticamente.

`feedback` registra um relato; não reembolsa nem reenvia. `extra` pode associar
`generationId[]`, `modelVersion[]` e `taskTraceId[]`; flags repetíveis incluem
`--generationId`, `--modelVersion`, `--relatedTaskTraceId`.
`logout` tenta o logout no servidor e só então remove a sessão local; falha interrompe
a troca de conta.

## Contrato V4 datado

Consultar `docs/kling-manual/19-kling4-migration.md` e `shared/kling-capabilities.json`. Exemplos legados não autorizam flags em outra rota. V4 exige shotContract local; o runner preserva o contrato no fingerprint/intent e não o envia como argumento. F8/F9 são propostas bloqueadas; 4K/HDR/extensão não estão liberados nesta CLI.
