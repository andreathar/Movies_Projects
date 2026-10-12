# Kling — exemplos de contrato e uso pela CLI

Use somente a CLI instalada; os JSONs abaixo explicam estruturas e não autorizam
HTTP/MCP direto. Nomes/limites reais vêm de `who_am_i` e `tool_list` da conta. Todos
os exemplos são didáticos; não executá-los como teste pago ou upload de diagnóstico.

## Envelope do serviço

Uma ferramenta de geração recebe modelo e parâmetros declarados, por exemplo:

```json
{
  "model": "<modelo declarado>",
  "arguments": [
    {"name": "prompt", "value": "a quiet coastal sunset"},
    {"name": "imageCount", "value": "1"}
  ],
  "inputs": [
    {"name": "<slot declarado>", "inputType": "URL", "url": "https://example.invalid/reference.png"}
  ]
}
```

`arguments[].value` é string; `elements` também viaja como JSON serializado em string.
A CLI cuida dessa tradução. Slots `input`, `image_1` e `first_image` não são sinônimos
universais. `model` é explícito. `taskTraceId` e `rationale` só seguem o contrato atual;
o primeiro não garante deduplicação, o segundo não interfere na autorização local.

Resposta de submissão sintética:

```json
{"ok":true,"status":200,"body":{"generationId":"EXAMPLE_ONLY","status":"submitted","creditsConsumed":10}}
```

Consulta completa sintética:

```json
{"ok":true,"status":200,"body":{"generationId":"EXAMPLE_ONLY","status":"COMPLETED","works":[{"status":"COMPLETED","contentType":"video","url":"https://example.invalid/output.mp4"}]}}
```

Nunca consulte `EXAMPLE_ONLY` no serviço. Use exclusivamente o ID retornado no job real.

## Mapeamento de entradas

| Ferramenta | CLI |
|---|---|
| `text_to_image`, `text_to_video` | prompt posicional e `--model`; referências somente se o contrato permitir |
| `image_to_image` | prompt e `--image` repetível, por ordem de slots |
| `image_to_video` | `--image` nos slots não terminais e `--tailImage` na cauda; ou `--input nome=valor` repetível |
| `omni_ref_video` | `--image` → `image_N`; `--video` → `video_N`; outros slots via `--input` se declarados |
| `motion_control` | `--image` e uma fonte: `--video` ou `--motionId` |

Não misture `--input` com `--image`/`--tailImage` em image_to_video.
Não passe áudio independente se não houver slot declarado. Limites individuais e
`combinedItemCap` devem ser atendidos ao mesmo tempo. Na CLI 0.2.1, algumas rotas
validam parâmetros depois do upload; o projeto antecipa a checagem pelo preflight.

Comandos ilustrativos, apenas depois de modelo, entradas, custo e escopo conferidos:

```bash
kling image_to_video --model <model> \
  --input first_image=./first.jpg --input tail_image=./last.jpg \
  --duration 5 --resolution 1080p --enable_audio false --prefer_multi_shots false \
  "A restrained single continuous shot"

kling omni_ref_video --model <model> --image ./ref.jpg --video ./clip.mp4 \
  --keepOriginalSound true --enableAudio false "Follow the camera movement in video 1"

kling motion_control --model <model> --image ./subject.png --motionId <id-real> \
  --motionDirection image_direction "Preserve the subject appearance"
```

Nenhum modelo é implicitamente compatível com todos esses exemplos. Áudio, duração,
Element e cauda devem existir na declaração escolhida. Cliques/downloads resultantes
não equivalem a aprovação artística.

## Formato do spec local do runner

O spec do projeto é uma lista de jobs. Não confunda `args` (objeto local) com
`arguments[]` (envelope remoto). Exemplo bloqueado, seguro para pré-checagem offline:

```json
[{
  "job":"EXAMPLE-DRAFT",
  "tool":"image_to_video",
  "model":"kling-video-v3_0",
  "auth":"REPLACE-WITH-AUTHORIZED-APR-ID",
  "submissionBlocked":"Exemplo sem autorização nem mídia revisada",
  "prompt":"<<<123>>> makes a small head movement",
  "args":{"duration":"5","resolution":"720p","imageCount":"1","enable_audio":false,"prefer_multi_shots":false},
  "inputs":{"first_image":"https://example.invalid/first.jpg"},
  "elements":[{"id":"123","bindName":"Andre"}]
}]
```

- Use `images` **ou** `inputs`. `inputs` é aceito para image_to_video, omni_ref_video e
  motion_control; image_to_image continua com `images` em ordem.
- `elements` pode ficar no topo ou em `args`; valores conflitantes são recusados.
  Bool nativo é serializado como `true`/`false`, não como `True`/`False` de Python.
- `prompt` fica no topo. Não coloque flags do cliente (`poll`, `image`, `input`,
  `rationale`, telemetria etc.) em `args`; eles pertencem à montagem controlada.
- Motion exige `referenceDurationSeconds` no spec para revisão; esse campo não vai
  para a API. Não é medição automática nem uma ordem de cortar a referência.
- `submissionBlocked` conserva o plano em rascunho. Só o produtor o remove após
  revisar o pedido, escopo, mídia, durações e orçamento. String em `auth` não aprova nada.

Pré-checagem offline:

```bash
python3 -B docs/kling-manual/tools/kling_preflight.py request.json --json
```

Após aprovação específica, o produtor usa `--submit-only` para um job selecionado e
`--resume JOB` para uma consulta. Sem JSON válido ou ID, registre incerteza e pare.
Não use trace ID, job novo ou mudança de prompt para reenviar silenciosamente.

## Elements, conta e feedback

`element_create` de imagem usa `--cover` e 1–3 `--secondary`; de vídeo usa `--video`.
Escolha tags na descrição atual, sem traduzir tokens. `element_get <id>` fornece o
recurso completo. Em update não envie `--cover`; a CLI conserva o original.
`secondary` substitui a lista completa. Exclusão exige instrução para o id exato.

`kling account` retorna saldo e membership. `creditsConsumed` da submissão, quando
existe, é registrado como declarado pelo provedor. Variação de saldo não é cobrança
atribuível com certeza ao job. Estimativas precisam de fonte, data, duração de entrada
quando tarifada e hipótese; não são cotação nem teto garantido pela API.

`feedback` só deve ser enviado dentro do escopo autorizado. As categorias vêm do
schema; `triggerMode=user_initiated` é usado quando o usuário pediu o relato, e
`agent_initiated` não é permissão para escrita silenciosa neste projeto.

## Autenticação e evidência

A CLI administra OAuth e renovação. Não leia tokens ou `.credentials`, não faça
login/logout como diagnóstico incidental. Captura local pode conter dados da conta;
compartilhe só capacidades sanitizadas. Veja [reference.md](reference.md) para os
campos e [SKILL.md](SKILL.md) para o fluxo completo.
