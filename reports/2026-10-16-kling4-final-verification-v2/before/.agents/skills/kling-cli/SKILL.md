---
name: kling-cli
version: 0.2.1
localization: pt-BR
localRevision: 2026-10-16-kling4-contract
description: >-
  Use a CLI oficial do Kling para descobrir modelos, gerar imagens e vídeos,
  gerenciar Elements e aplicar motion control. Exige modelo explícito e contratos
  atuais de who_am_i/tool_list; registra generationId, consulta query_tasks e
  preserva resultados sem repetir submissões incertas. Não concede autorização de gasto.
requires: node>=18
homepage_cn: https://klingai.com
homepage_global: https://kling.ai
---

# Kling — CLI oficial, imagens, vídeos, Elements e motion control

Adaptação em português da skill oficial `klingai-tech/skills` 0.2.1. A versão da skill
é independente da versão do executável. A revisão local concilia as instruções com
`AGENTS.md` e o manual do projeto; não modifica a API nem o pacote global. Histórico
upstream e hash anterior permanecem em `skills/registry.json` e no Git. Não reinstalar
por cima desta adaptação sem comparar as alterações.

## Idioma e contratos

Responda em português ao usuário deste projeto. Explique erros, riscos de custo e
pendências em linguagem natural. Preserve `generationId`, `creditsConsumed`, nomes
exatos de modelos, comandos, flags, enums, URLs e tags declaradas pelo servidor.
Respostas atuais usam camelCase; versões antigas podem usar os equivalentes snake_case.

Prompts criativos podem permanecer em inglês quando esse for o texto revisado da cena
ou a orientação do modelo. Não há evidência de que traduzir toda a instrução para
chinês melhore a geração. Explique a intenção em português e preserve as falas e o
idioma aprovado; não traduza cegamente marcadores como `<<<id>>>` ou nomes de slots.

## Apresentação de capacidades

Quando o usuário perguntar o que o Kling faz, ou concluir uma instalação/login já
solicitados, apresente o resumo abaixo em seu idioma. Mostrar este texto não exige
comando nem gasto. Só diga “pronto” se o estado tiver sido verificado; caso contrário,
diga “falta verificar a instalação/conexão”.

```text
Com o Kling você pode:
📷 Gerar imagens a partir de texto ou de imagens de referência.
🎬 Gerar vídeos a partir de texto ou animar imagens.
🧩 Criar e gerenciar personagens, animais e objetos como Elements reutilizáveis.
🎭 Aplicar movimentos de um vídeo ou da biblioteca a uma imagem de sujeito.
📤 Enviar arquivos locais pela CLI, quando houver autorização para upload.
Também é possível organizar anúncios, curtas e lotes de materiais com agentes e skills.
```

O resumo não comprova que todos os modelos estejam liberados para a conta. Para
capacidade exata, use a descoberta autenticada abaixo.

## Instalação, região e atualização

1. Localize o executável com `command -v kling` e identifique seu pacote e versão.
   A versão 0.2.1 da skill requer CLI 0.2.1+ para seu conjunto completo de comandos.
   Ler `package.json` do pacote instalado permite diagnóstico sem executar a CLI.
2. Se instalação/upgrade for necessária e estiver no escopo autorizado, confirme a
   região da conta antes de escolher o pacote; não instale ambos:

| Conta | Site | Pacote oficial |
|---|---|---|
| China | https://klingai.com | `@klingai/cli-cn` |
| Global | https://kling.ai | `@klingai/cli-global` |

Comando de instalação, somente para a região confirmada:
`npm i -g <pacote-da-região> --registry=https://registry.npmjs.org`.
Não instale uma alternativa nem atualize no meio de geração. Compare versão local e
publicada antes de propor upgrade; `npx skills add klingai-tech/skills` atualiza a skill,
não o executável, e pode sobrescrever a adaptação local. Atualizações exigem escopo
próprio; não são uma ação automática de início de sessão.

`kling --version` e ajuda superior não fazem chamadas de geração, mas a CLI 0.2.1
executa uma migração de estado legado antes de tratar essas flags. Ajuda específica
(`kling <command> --help`) tenta obter `tools/list` pela rede e pode renovar a sessão.
Não descreva toda ajuda como estritamente offline.

## Login, sessão e único canal permitido

Use somente o executável `kling` para interagir com o serviço. Não monte HTTP/MCP
paralelo, não extraia cookies/tokens, não peça chaves AK/SK, não leia `.credentials`
ou armazenamento do navegador. Auditar código não autoriza contornar o cliente.

Login é `kling login`, via OAuth no navegador (DCR, código + PKCE). Ele pode limpar o
estado anterior. Ausência de login, 401 ou falha de renovação não autoriza nova
concessão automaticamente: informe e siga o escopo do usuário. Em agente/CI, use modo
não interativo; não permita que a CLI espere stdin. A renovação da sessão existente é
feita pela própria CLI. Não altere endpoints, permissões ou arquivos de credenciais.

- Pedido de logout: `kling logout`; pare depois do sucesso.
- Troca de conta explicitamente solicitada: `logout` → `login` → `who_am_i`.
  Falha em qualquer etapa interrompe a troca; não pule a etapa nem tente novos canais.
- Restrição de acesso/gray release não se resolve repetindo login ou geração.
- Não envie `feedback` silenciosamente: neste projeto é escrita externa e precisa
  estar coberta pela instrução do usuário/produtor. Uma única ocorrência não autoriza
  loop de feedback. Ele não reembolsa, corrige ou repete um job.

## Descoberta e decisão por modelo

```bash
kling tool_list -q --skill-name kling-cli --skill-version 0.2.1
kling who_am_i -q --skill-name kling-cli --skill-version 0.2.1
```

`tool_list` informa ferramentas, descrições e `inputSchema`. `who_am_i` informa os
modelos por ferramenta, `arguments`, valores, defaults, `inputs` e limites combinados.
Consulta de capacidades não gera mídia; pode usar/renovar a sessão existente. Nunca
faça uma geração vazia como teste de acesso. Salve apenas capacidades sanitizadas ao
criar snapshot; remova identidade e segredos.

A descoberta de 16/10/2026 na CLI Global instalada 0.2.1, MCP 1.3.3, lista
`kling-video-v4_0` em image_to_video/text_to_video/omni_ref_video. Nenhuma geração
foi testada nesta migração. `shared/kling-capabilities.json` e
`docs/kling-manual/19-kling4-migration.md` separam anúncio, interface, conta e teste.
Não instalar a CLI 0.2.0 do plugin externo sobre esta adaptação local.

V4 keyframes não declara Elements/enable_audio/multi-shot: nunca remover vínculo
facial nem prometer silêncio para trocar de modelo. V4 Omni aceita referências
mistas/áudio e Elements, mas exige prefer_multi_shots=true; câmera fixa e versões
já aprovadas exigem revisão própria. Só 720p/1080p nesta interface; 4K anunciado
não está habilitado. Preservar F1–F7 e escolher fallback explicitamente.

V4 exige `shotContract` local com manifesto tipado por uso/hash/proveniência,
evidência de review e element_get, beats temporais, elenco/companheiros/figurino/
mesa/eixo e plano de áudio. Metadados locais nunca viram flags. Vídeos diretos mais
video Elements compartilham 30 s; duração de entrada entra na cobrança. Preço/FPS/
Flash não verificados; HDR/extensão são futuros. Renovar schema e cotação por pedido.

| Intenção | Comando |
|---|---|
| Texto para imagem | `text_to_image` |
| Imagem de referência para imagem | `image_to_image` |
| Texto para vídeo | `text_to_video` |
| Animar imagem/keyframes | `image_to_video` |
| Referências mistas para vídeo | `omni_ref_video` |
| Reutilizar sujeitos | `element_create`, `element_list`, `element_get`, `element_update`, `element_delete` |
| Transferir movimento | `motion_control`, precedido de `motion_library_list` quando necessário |
| Consultar job | `query_tasks` |
| Saldo/membership | `account` |
| Upload autorizado | `file_upload` |

Se faltar saber se a intenção é imagem ou vídeo, esclareça antes de submeter.
Use `--model <nome-exato>` em toda geração; `--omni` e `--flash` antigos não substituem
isso. Não troque ferramenta, modelo, prompt ou referências após erro sem escopo para
essa alteração. Recomendações do servidor não concedem nova autorização.

## Validação antes de upload ou gasto

1. Confira modelo **na ferramenta escolhida**, parâmetros obrigatórios, enums,
   slots, quantidade e formato de mídia, limites individuais e `combinedItemCap`.
2. Defina explicitamente áudio, multi-shot e resolução quando declarados e relevantes.
   Omissão usa default; ausência de `enable_audio` não prova que o resultado será mudo.
3. Confira restrições nas descrições: tipo de Element, fonte de movimento, áudio
   mutuamente exclusivo, duração da entrada e da saída. Conflito ou ausência de
   informação bloqueia apenas a combinação afetada; não faça sonda paga.
4. Use `docs/kling-manual/tools/kling_preflight.py` para revisão offline. O snapshot
   é datado, não comprova acesso atual ou preço. O runner também consulta `who_am_i`
   antes de submeter. Essa checagem não substitui aprovação, cotação, inspeção integral
   de mídia ou restrições expressas apenas em texto pelo provedor.
5. Respeite `AGENTS.md`: somente o produtor envia pedido pago com autorização e teto
   específicos. `auth` é referência documental; não é credencial nem prova automática
   de autorização. Placeholder e `submissionBlocked` impedem o runner de enviar.

### Entradas e Elements

- `image_to_image`: repita `--image`, na ordem dos slots do modelo. Não exceda a lista.
- `image_to_video`: `--image` preenche slots que não sejam cauda; `--tailImage` preenche
  `tail_image`. Ou use `--input nome=arquivo` para cada slot, sem misturar as formas.
- `omni_ref_video`: imagens/vídeos somente nos slots declarados. A presença de `--audio`
  na ajuda não comprova suporte a áudio independente. `enable_audio=true` e
  `keepOriginalSound=true` são incompatíveis no contrato atual.
- Element: confirme `element_get` (tipo e recursos), suporte a `elements` no modelo e
  limitações da ferramenta. Vincule `--elements '[{"id":"123","bindName":"Andre"}]'`
  **e** `<<<123>>>` no prompt. Marcador sozinho não vincula identidade.
- Imagem Element usa cover + 1–3 imagens secondary; vídeo Element usa apenas video.
  Voice opcional depende do contrato. Tags devem vir da descrição atual da região,
  sem tradução. Não rejeite imagem Element apenas pelo nome do modelo.
- Update envia somente alterações. A CLI lê o Element e conserva o cover original;
  `--cover` não é aceito em update. `secondary` substitui a lista inteira: confirme o
  conjunto final quando houver adição/remoção. Exclusão requer instrução explícita
  para o Element identificado; não remova legado como limpeza incidental.

### Motion control

Exige uma imagem de sujeito e exatamente uma fonte: `--video` ou `--motionId`.
Verifique duração real do vídeo/biblioteca; não estime 5 segundos porque o texto pede
um movimento curto. `image_direction` admite referência de 3–10 s no contrato atual;
`motion_direction` segue o vídeo, sujeito às restrições declaradas. Quantifique duração
de entrada quando ela compõe a cobrança. No spec local, registre
`referenceDurationSeconds`, sem enviar esse campo como argumento à API.

## Submeter uma vez, registrar, retomar

No projeto, prepare o spec no formato documentado em `api-examples.md` e use
`scripts/kling_batch.py --spec CAMINHO --only JOB --submit-only`. O runner consulta
capacidades, guarda intenção durável e hash do schema antes da submissão, preserva
`generationId`/resposta e reconcilia antes de consultar ou baixar. Retome com
`scripts/kling_batch.py --resume JOB`: uma consulta, sem geração.

A CLI pode truncar JSON grande quando usa `process.exit()` com stdout em pipe. O
runner captura stdout/stderr em arquivos temporários privados e verifica JSON e
código de saída. Exit 0 sozinho não comprova resultado completo.

Sem ID ou após timeout/falha de transporte, o estado é **SUBMISSION_UNKNOWN**:
pode ter havido cobrança. Preserve evidência, nunca reenvie automaticamente, nem
mude o nome do job para contornar o marcador. `taskTraceId` serve para correlação,
**não é chave de idempotência nem recuperação garantida**. Não derive ID fictício.

`query_tasks` usa o ID real; estados são insensíveis a maiúsculas. `QUEUING`,
`RUNNING`, `submitted` e `processing` são intermediários. `COMPLETED`,
`PARTIAL_COMPLETED`, `succeed`, `succeeded` e `success` exigem conferir `works`.
Parcial não é lote completo. Sucesso sem URL é `RESULT_EMPTY`, não entrega concluída.
Falha de consulta não é falha comprovada da geração. Continue a consulta apenas
quando útil/autorizado, relatando mudança relevante; não use background ou loops de
submissão. Limite de espera não cancela automaticamente o job.

`--poll N` existe no cliente, mas no projeto prefira submissão separada da consulta,
para persistir o ID antes de esperar. Use intervalos razoáveis e informe o usuário
quando o limite de espera terminar; nunca transforme isso em retry pago.

## Créditos, download e erros

- `creditsConsumed`, quando retornado, é cobrança declarada do provedor, inclusive 0.
  Registre origem. Diferença de saldo é observação da conta, sujeita a concorrência,
  renovação e outras operações; não a some como custo certo por job.
- Estimativa, cotação e cobrança são coisas distintas. Não converta unidades da API
  de desenvolvedor em créditos desta conta sem confirmação. Saldo histórico não é atual.
- Exiba `works[].url` com link clicável. Imagem pode ser embutida; vídeo pode ter player.
  Use a URL padrão; variante sem marca só se solicitada/aplicável. Links podem expirar.
- Preserve downloads originais, metadados e SHA-256; não promova arquivo a aprovado
  por existir. O runner limita transferência, recusa URL não HTTPS/arquivo vazio e
  conserva originais existentes. Hash/download não comprovam decodificação ou QC.
- Não prometa que um erro genérico não cobrou. Apenas uma rejeição de validação
  inequivocamente anterior à submissão pode ser tratada como tal; nenhuma correção
  autoriza repetir uma submissão incerta.
- Saldo insuficiente: informe. Links comerciais só se retornados pelo servidor;
  não invente URL, compre créditos, altere plano ou abra login como solução.
- Diagnósticos podem conter prompts/URLs; sanitize antes de compartilhar. Não leia
  logs de credenciais. Redação do wrapper não é garantia sobre logs globais da CLI.

## Telemetria e referências

Use `--skill-name kling-cli --skill-version 0.2.1` ao invocar esta skill. Isso não
concede acesso. `rationale` é frase curta em inglês sobre intenção real, sem dados
sensíveis; confira suporte na ferramenta. `taskTraceId` é metadado de rastreio; siga o
formato declarado, sem presumir UUIDv7 ou idempotência.

Campos: [reference.md](reference.md). Exemplos e contrato local:
[api-examples.md](api-examples.md). Regras/custos do projeto:
`docs/kling-manual/00-regras-do-projeto.md` e `12-custos-e-ledger.md`.
