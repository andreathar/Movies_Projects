# 01 · Setup e diagnóstico sem custo

Tudo aqui é leitura. Nenhum comando desta página gera mídia nem consome crédito.

## Os comandos (CLI `kling` 0.2.1) [LIVE]

O CLI espelha 1:1 as 18 ferramentas MCP do servidor (snake_case), mais `login`, `tool_list` e `account` (= `query_membership_and_credits`).

| Comando | Faz | Custo |
|---|---|---|
| `kling account` | Plano e créditos disponíveis | 0 |
| `kling who_am_i` | Identidade + **modelos, argumentos, slots de input, valores permitidos** | 0 |
| `kling tool_list` | Lista as ferramentas e seus schemas | 0 |
| `kling <comando> --help` | Ajuda local + declaração viva do servidor | 0 |
| `kling element_list` / `element_get <id>` | Lê Elements | 0 [NÃO TESTADO hoje] |
| `kling motion_library_list` | Biblioteca de movimentos salvos | 0 [NÃO TESTADO hoje] |
| `kling query_tasks [--poll N] <generationId>` | Estado/resultado de um job | 0 |
| `kling file_upload <arquivo>` | Ticket de upload (o CLI já faz upload automático ao usar `--image <caminho>`) | 0 |
| `kling login` / `logout` | Autenticação | 0, mas **não usar sem necessidade** (ver `00`) |
| `kling feedback ...` | Reporta problema à Kling | 0, é escrita externa (ver `00`) |

Geram e **cobram**: `text_to_image`, `image_to_image`, `text_to_video`, `image_to_video`, `omni_ref_video`, `motion_control`. `element_create/update/delete` alteram a conta (custo em crédito não verificado por mim): só com pedido do producer.

## Rotina antes de qualquer trabalho pago

1. `kling account` → anote saldo e hora. (Hoje 15:04: plano **Ultra**, saldo **31.621** [LIVE]. O ledger do projeto ainda não registra esse saldo: o producer deve registrar.)
2. `kling who_am_i` → compare com `snapshots/who_am_i.sanitized.json`. Mudou `mcpVersion` (hoje **1.3.3**) ou a lista de modelos? Regenere o 03 e reavalie as receitas.
3. `kling <ferramenta> --help` da ferramenta que vai usar, se o CLI mudou de versão.
4. Monte o `request.json` e rode:

```bash
python3 -I docs/kling-manual/tools/kling_preflight.py \
  projects/andre-time-travel/07_generations/requests/<pasta>/request.json
```

ERROR = não enviar. WARN = decidir conscientemente. O preflight **não estima custo**.

## O que olhar no `who_am_i`

Para cada ferramenta há `defaultModel` e `models[]`. Cada modelo traz:

- `arguments[]`: `name`, `required`, `default`, `allowedValues`, `description`.
- `inputs[]`: os slots de mídia (`first_image`, `image_1..N`, `video_1`...). **O número de slots é o limite real de referências.**
- Em `omni_ref_video`: `combinedItemCap(s)` e `elementSupport` (quantos Elements, se aceita vídeo).

Regras de leitura:

- Argumento sem `default` e `required: false` simplesmente não vai se você não passar.
- **Defaults que mudam o resultado e o custo** (vigentes hoje [LIVE]): `enable_audio=true` em todos os vídeos que o declaram; `prefer_multi_shots=true` em `kling-video-v3_0` (mas `false` em `v3_0_omni`); `img_resolution=4k` em `kling-image-v3_0_omni` (image_to_image) mas `2k` na maioria. Defina sempre explicitamente.
- O CLI aceita `--duration`, `--imageCount`, `--image_count` (snake ou camel). A API crua exige o nome declarado.

## Limites de mídia de entrada [OFICIAL via descrição das ferramentas]

- Imagens: **PNG ou JPG**, abaixo de 4K, ≤ 30 MB, proporção "não mais larga que 1:2" segundo o texto. Na prática do projeto, 5:2 passou e 4:1 foi rejeitado (ver `11`).
- Arquivos locais passados com `--image ./arquivo` são enviados automaticamente. URLs de jobs anteriores do Kling podem ser reutilizadas sem baixar; URLs de resultado **expiram em 24 h**.
- Upload manual (`file_upload`): o `Content-Type` do arquivo precisa ser `image/png`, `image/jpeg` ou `video/mp4`. Reaproveite a URL devolvida em vez de reenviar o mesmo arquivo.
- **Achado do preflight** [PROJETO]: dois arquivos de referência têm extensão trocada (`02_references/table/R1-J26-table-anchor_2.png` é JPEG; `07_generations/originals/R3-oppenheimer-speaking-o1_1.jpg` é PNG). Não se sabe se o upload se importa; renomear uma **cópia** é barato, sobrescrever o original não.

## Pastas de trabalho

Onde cada coisa vive no projeto (resumo, ver AGENTS.md): `02_references/` entradas, `07_generations/requests/<data-fase>/` pedidos, `07_generations/originals/` downloads aceitos, `credit-ledger.csv` custos. Nada disso é criado por este manual.
