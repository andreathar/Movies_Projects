# 17 · Auditoria da integração CLI — 2026-10-12

A instalação efetiva é `@klingai/cli-global` **0.2.1**: executável `kling`, bundle
JavaScript `dist/cli.js`, cliente fino sobre MCP via Streamable HTTP e OAuth.
O pacote aponta para repositório corporativo da Kuaishou; não há source TypeScript
completo no pacote instalado. O bundle distribuído permitiu auditar o comportamento.
A skill vem de `klingai-tech/skills`, é distribuída separadamente e está vendorizada
em `.agents/skills/kling-cli`; `skills/kling-cli` aponta para ela por symlink.

Fontes públicas: [pacote oficial](https://www.npmjs.com/package/%40klingai/cli-global),
[skill oficial](https://github.com/klingai-tech/skills/blob/main/SKILL.md),
[exemplos oficiais](https://github.com/klingai-tech/skills/blob/main/api-examples.md).
A comparação delegada não encontrou alternativa comprovadamente superior para os
mesmos créditos/Elements/autenticação. Clientes de API de desenvolvedor ou outros
provedores trocam contratos/cobrança e não demonstram migração transparente.

## Video 4.0

`who_am_i` foi consultado na sessão existente, somente para descoberta. O catálogo
MCP 1.3.3 retornou **nenhum modelo V4** nas ferramentas de vídeo consultadas. O
snapshot sanitizado e a ficha contêm os nomes exatos observados. Documentação pública
menciona V4 Preview e o bundle tem exemplos V4, mas isso não comprova liberação à conta.
Nenhuma geração foi usada como teste. A listagem pode mudar; não conclui acesso no site.

## Correções locais

- O runner captura stdout/stderr em arquivo temporário privado: `process.exit()` da
  CLI podia truncar JSON em pipe mesmo com exit 0. A consulta de catálogo confirmou
  JSON incompleto em pipe e completo em arquivo. Não foi alterado o pacote global.
- Validação por schema vivo antes da submissão/upload, reutilizando preflight offline.
  Valida slots, aliases duplicados, limites `elements.maxItems` e `combinedItemCap`,
  conflitos de áudio, defaults críticos e fontes/duração informada de motion.
- Contrato local unificado: `inputs` nomeados e `elements` no topo são encaminhados,
  bools viram `true`/`false`; mistura de entradas ou valores conflitantes falha fechada.
- Placeholder/rascunho bloqueado não chama o serviço. A interface CLI local exige um
  job por `--submit-only`; intenção e schema ficam gravados antes do envio.
- Sem ID/timeout continua como `SUBMISSION_UNKNOWN`; não há retry automático. Resume
  consulta o ID salvo, trata erro de consulta e não anuncia sucesso sem artefato.
- Cobrança declarada e delta de saldo ficam separados; delta não preenche custo por job.
- Diagnósticos do wrapper redigem tokens/cookies e query strings assinadas. URLs de
  artefatos necessárias à retomada ficam no registro operacional privado.
- Downloads têm timeout, limite de tamanho, HTTPS, recusa de vazio e preservação de
  originais/hash. Isso não substitui decodificação, revisão audiovisual ou aceite.
- Documentação da skill foi adaptada a português; contratos, prompts revisados e
  tokens técnicos foram preservados. Não há nexo demonstrado entre chinês e bugs.

## Limites e pendências

O preflight agora aplica também limites condicionais e tipos de Element declarados, proíbe áudio nativo com vídeo Omni, verifica v2.6 cauda/áudio/resolução e mede vídeos locais com ffprobe. Não interpreta toda descrição futura, autentica direitos/aceite ou confirma a verdade de metadados declarados de uma URL. O produtor ainda confere Element, referências e preço.

Novos envios exigem liberação documental exata por pedido no formato de `docs/PRODUCTION_PLAN.md`: payload/schema/cotação/teto/validade/escopo de upload. `auth` aponta esse registro, sem autenticar a pessoa que aprovou. Deduplicação por conteúdo recusa renomear um pedido já enviado/incerto. Não há teto imposto pelo servidor ou garantia de idempotência do provedor; `taskTraceId` continua apenas correlação.

Nenhuma segurança global foi alterada. A inspeção **somente de metadados** encontrou
permissões amplas no arquivo de credenciais e log do CLI (modo 0664; diretórios 0775).
O conteúdo não foi lido. A escrita de credenciais do bundle não fixa modo 0600 nem
faz substituição atômica. Correção de permissões/armazenamento exige tarefa específica
por estar fora do escopo autorizado. A redação do wrapper não cobre logs globais.

`archive_kling_images.py` é auxiliar de acervo, não gerador. Sua consulta agora reutiliza
a captura segura do runner, com timeout de 60 s. Não foi executado contra o serviço
nem baixou mídia nesta auditoria. Falha de consulta continua sem motivar geração nova;
originais existentes são preservados.

Os specs antigos não liberam novos jobs. Os dois A/B posteriores terminaram em 51 créditos declarados, conforme recibos canônicos. A/B antigo não isolava resolução; 90 créditos eram estimativa não cotada. Referência motion de 30 s não pode ser orçada como 5 s.
Nenhuma aprovação, ledger antigo, mídia, login, grant, pacote global ou publicação
foi modificado pela revisão.
