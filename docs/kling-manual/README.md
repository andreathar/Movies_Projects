# Manual do Kling — Movies_Projects

> Atualização 16/10/2026: consultar [contrato V4 por interface](19-kling4-migration.md) e `shared/kling-capabilities.json` antes de escolher rota/custo. Tabelas e pilotos anteriores abaixo são evidência datada, sem liberação nova.

**Status: PROPOSTA de Claude (2026-10-09) para revisão do Codex e da Andre. Nada aqui é aprovação, decisão ou autorização de gasto.**
Pasta nova, só arquivos novos: nada existente foi alterado, movido ou apagado, e nenhum commit foi feito.

Objetivo: uma solução por processo que o Kling permite, para o filme *The Table Between Centuries* e para os próximos. Escrito em português; comandos, nomes de modelos e argumentos ficam em inglês, exatamente como o CLI os aceita.

## Como usar (30 segundos)

1. Precisa gerar algo? Abra **02-escolha-de-modelo.md**, ache o processo, vá ao guia numerado.
2. Antes de qualquer pedido pago: monte o `request.json`, rode `python3 -I docs/kling-manual/tools/kling_preflight.py <request.json>`. Se der ERROR, não envie.
3. Quem **envia** gasto é só o producer (AGENTS.md). Este manual não muda isso.

## Selos de evidência (leia sempre)

| Selo | Significa |
|---|---|
| **[LIVE]** | Visto hoje (2026-10-09) no próprio CLI: `who_am_i`, `tool_list`, `--help`, `account`. Sem gasto. |
| **[PROJETO]** | Teste pago do projeto, com job ID em `07_generations/` ou no ledger. |
| **[OFICIAL]** | Documentação do Kling (kling.ai) ou texto de ferramenta que o servidor Kling entrega. |
| **[TERCEIROS]** | Blog, tutorial ou agregador. Pode estar errado ou velho. Só serve de pista. |
| **[INFERÊNCIA]** | Conclusão minha, não confirmada por fonte. Está dita como tal. |
| **[NÃO TESTADO]** | Comando/receita montado, nunca executado. Teste pequeno e autorizado antes de depender. |

## Índice

| Arquivo | Para quê |
|---|---|
| 00-regras-do-projeto.md | Limites do AGENTS.md e três conflitos entre o servidor Kling e o projeto |
| 01-setup-diagnostico.md | Verificar conta, modelos e ferramentas **sem gastar** |
| 02-escolha-de-modelo.md | Tabela "quero X → use Y" |
| 03-modelos-ao-vivo.md | Ficha automática de todos os modelos e argumentos (gerada) |
| 04-imagens-estaticas.md | `text_to_image` e `image_to_image` |
| 05-elements.md | Criar, ligar e manter personagens (Elements) |
| 06-imagem-para-video.md | `image_to_video` (quadro inicial/final, Element, falas) |
| 07-texto-para-video-e-multishot.md | `text_to_video`, multi-shot, duração |
| 08-omni-ref-video-e-edicao.md | `omni_ref_video`: referências mistas e edição de vídeo |
| 09-motion-control.md | Transferir movimento de um vídeo/biblioteca para uma imagem |
| 10-audio-voz-dublagem.md | Áudio nativo, voz, idiomas, lip-sync, Edição H |
| 11-receitas-do-filme.md | Receitas prontas para as cenas do filme |
| 12-custos-e-ledger.md | Tabela de custo, o que foi observado, como registrar |
| 13-qc-e-aceitacao.md | Como inspecionar e aceitar um take |
| 14-erros-e-troubleshooting.md | Erro → causa provável → o que fazer |
| 15-ferramentas-nao-listadas.md | O que existe fora do registry do projeto (aviso ao Codex) |
| 16-fontes.md | Links e grau de confiança |
| 17-integracao-cli.md | Auditoria da integração CLI (2026-10-12) |
| 18-guia-de-prompts.md | Como escrever prompts que o Kling entende e o filme exige; templates por rota; checklist |
| snapshots/ | `who_am_i` sanitizado (sem userId), `tool_list`, `--help` de cada comando, com sha256 |
| tools/ | `kling_model_sheet.py` (gera o 03), `kling_preflight.py` (valida request.json offline) e `test_kling_tools.py` (15 testes: `python3 -I tools/test_kling_tools.py`) |

## Manutenção

- O 03 é gerado: `python3 -I tools/kling_model_sheet.py snapshots/who_am_i.sanitized.json > 03-modelos-ao-vivo.md`.
- Quando o Kling mudar (versão do MCP, modelos novos): rode `kling who_am_i`, remova `body.user`, substitua o snapshot, regenere o 03 e rode o preflight em um request conhecido.
- Snapshot atual: `mcpVersion 1.3.3`, CLI `kling 0.2.1`, skill `kling-cli 0.2.1`.

## Auditoria da integração (2026-10-12)

Consulte [17 · Integração CLI](17-integracao-cli.md) para a revisão dos helpers, da captura JSON, das limitações de custo e da consulta de disponibilidade V4. Esta revisão não aprova produção nem transforma snapshots em capacidades atuais.

Versão atual e funções utilizáveis: [CLI 0.2.3 + guia V4](20-kling4-features-cli-023.md). Snapshots anteriores continuam históricos.
