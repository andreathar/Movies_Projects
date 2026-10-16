# 00 · Regras do projeto e conflitos conhecidos

> Atualização 16/10/2026: consultar [contrato V4 por interface](19-kling4-migration.md) e `shared/kling-capabilities.json`. Evidências anteriores são datadas; anúncio não amplia a CLI atual.

O Kling (servidor e skill) e este projeto têm regras diferentes. Onde divergem, **vale o projeto** (AGENTS.md). Este arquivo só resume o que afeta o uso do Kling; a fonte é sempre o AGENTS.md.

## Limites que valem para qualquer processo [PROJETO]

| Regra | Efeito prático |
|---|---|
| Só o **producer/parent agent** envia pedido pago aprovado | Outros agentes preparam o `request.json` e rodam o preflight; não enviam |
| "Whole-film spending authorization is a ceiling, not batch approval" | Cada job precisa do seu `auth` (ex.: `D16-galileo-pilot-v2-phase-a`) |
| Só o CLI instalado e schemas ao vivo | Nada de HTTP direto, token, cookie, MCP paralelo |
| Sem login churn | `kling login` apaga o login anterior e reautoriza. 401 não autoriza reautenticação automática; seguir escopo do usuário |
| Sem retry automático e sem sonda paga | Job incerto = consultar `query_tasks`, nunca reenviar |
| Saldo histórico não vale | Rode `kling account` antes de trabalho pago |
| Nenhum rosto completo de figura histórica | Só olhos e detalhes abaixo do pescoço; inspecionar reflexos |
| Preservar originais; nunca sobrescrever, mover, apagar, commitar sem pedido | Use caminhos novos, sufixo `_r2` etc. |
| Sem credenciais em prompts, logs, skills, memória | Nunca cole `.credentials` nem tokens |
| ElevenLabs e outros serviços exigem escopo próprio | Ver `15-ferramentas-nao-listadas.md` |

## Conflitos entre o Kling e o projeto (decisão: vale o projeto)

1. **Troca "silenciosa" de ferramenta.** As descrições de `text_to_image` e `text_to_video` mandam trocar sozinho para `image_to_image`/`image_to_video` quando há Element. Aqui não: a ferramenta e o modelo ficam escritos no `request.json` e passam pelo preflight. Se houver Element, o request já nasce como `image_to_*`.
2. **`feedback` sem avisar.** A skill diz que a chamada não precisa ser comunicada. `kling feedback` envia dados à Kling (escrita externa). Aqui: só com ok do producer/Andre, e o resumo vai no ledger.
3. **Telemetria e rastreio.** A skill manda anexar `--skill-name kling-cli --skill-version 0.2.1`, `--rationale` e `--task-trace-id` aos comandos. São metadados sem efeito funcional [OFICIAL]; o `--rationale` deve ser uma frase em inglês verdadeira, sem dado sensível. O formato é o declarado pelo contrato atual; não presumir UUIDv7. `taskTraceId` é rastreio, não idempotência nem recuperação garantida de job.
4. **Escolha do modelo.** A CLI 0.2.1 exige `--model`. O modelo fica explícito: os padrões variam por ferramenta e os de `enable_audio` e `prefer_multi_shots` já surpreenderam (ver `06`).

## Divergências ainda abertas (não "consertadas", só registradas)

- `omni_ref_video` descreve `audio_1..3` e `video_1..5`, mas o `who_am_i` declara só `image_1..7` e `video_1` [LIVE]. Não enviar áudio independente enquanto a combinação não estiver declarada e coerente; geração paga não serve para descobrir compatibilidade.
- `text_to_image` declara `gpt-image-2` e `image_to_image` declara `gpt-image2` (sem hífen) [LIVE]. Use o nome exato de cada ferramenta.
- `gemini-3-pro-image` usa `image_count` (snake_case) e `img_resolution` obrigatório; os outros usam `imageCount` [LIVE]. O CLI aceita os dois formatos; a API crua não.
- O guia oficial de lip-sync cita só vídeos Kling 1.0/1.5 [OFICIAL, conflita com blogs que citam Kling 3.0]. Não está no CLI de qualquer jeito.
- Custos observados no projeto divergem da tabela (ver `12`).

## Quem decide o quê

- Escolha criativa de modelo, receitas novas, mudança de ferramenta: Codex propõe, Andre aprova quando muda aparência, identidade, voz ou custo.
- Este manual é referência técnica. Ele nunca substitui `decisions` (D01–D16), `approvals.json` ou o ledger.
