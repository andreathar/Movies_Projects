# 14 · Erros e troubleshooting

Regra geral do projeto: **sem retry automático e sem reenvio às cegas**. Se um job está incerto, consulte; reenviar é um job pago novo, com autorização própria.

## Mensagens do servidor [OFICIAL, tabela de `query_tasks`]

| Mensagem | Significa | Ação |
|---|---|---|
| The prompt/input media contains disallowed content | Moderação bloqueou | Revisar prompt/entrada. Não reenviar igual |
| Account inspiration credits are insufficient | Sem crédito | Avisar o producer. Nunca comprar crédito automaticamente |
| The selected model does not support this parameter combination | Combinação inválida | Rodar o preflight; ver a ficha `03`; trocar de modelo só com revisão |
| Generation timed out | Timeout | Consultar `query_tasks`; reenviar só se o usuário pedir, com os mesmos parâmetros |
| Service is temporarily unavailable | Falha de serviço | Idem |
| Parameter format is invalid | Argumento mal formado | Achar o campo; ver exemplo na ficha |

## Sintoma → causa provável → o que fazer

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Perdi o `generationId` (caso G-01 UNCERTAIN: 80 cr, sem ID) [PROJETO] | A chamada caiu/travou antes de devolver o ID; o CLI **não tem listagem de gerações** | O resultado pode estar em "My Creations" no app web (o Andre baixa). Prevenção: submeter com `--poll 0`, **anotar o ID**, e só depois `query_tasks --poll` |
| `query_tasks` não termina | Fila longa | Aguarde mais (`--poll 300`); não reenviar |
| URL de resultado inválida | Passaram 24 h | Verificar no app web; no futuro baixar na hora |
| Erro 401 / token inválido | Sessão expirou | **Uma** vez: `kling login`; se falhar, parar e avisar. Sem cookie, sem colar token, sem "login em loop" |
| Entrada 4:1 rejeitada, sem cobrança [PROJETO] | Proporção fora do limite | Preencher até 5:2 com barras pretas (`11` R4) |
| Imagens demais para o modelo | Slots insuficientes (`gemini-3-pro-image` tem 2) | Preflight `SLOT_COUNT`; escolher modelo com mais slots |
| `ARG_UNKNOWN` / argumento ignorado | Nome errado entre `imageCount` e `image_count` | Usar o nome declarado na ficha |
| Corte no meio do plano | `prefer_multi_shots` ficou true (padrão em `v3_0`) | `--prefer_multi_shots false` |
| Voz/trilha que ninguém pediu; custo maior | `enable_audio` ficou true | `--enable_audio false` ou pedir "no music" |
| Cabeça de interlocutor apareceu no still [PROJETO] | "Só ele no quadro" não bastou | Composição em terços + "nobody else, no silhouette, no hand, no shadow, no reflection" |
| Modelo colou a foto de referência no lugar da cena | Prompt de "escuta" com parede vazia | Derivar da imagem de fala aceita ("change only the expression") |
| Rosto do Andre deriva | `kling-image-v3_0_omni` com Element derivou 2/2 | Usar `kling-image-o1` + Element (D11) |
| Elementos acusam capa imutável | Regra do servidor | Criar outro Element; apagar o antigo só com confirmação |
| Element de vídeo recusado em `image_to_image` | Só `image_to_video` v3_0/v3_0_omni aceitam | Trocar de ferramenta no request |
| Olhar "centrado" no still | Pose do still | Dizer a direção do olhar no prompt do vídeo |
| Duas piscadas em vez de uma [PROJETO G-05] | Variação do modelo | Registrar, aceitar ou rejeitar na reprodução |
| Saldo caiu mais que o esperado | Jobs concorrentes ou `imageCount>1` | Ver `12` (um job por vez; ler `creditsConsumed`) |
| Extensão não bate com o conteúdo | Arquivo renomeado errado | Preflight `EXT_MISMATCH`; usar uma cópia com a extensão certa |

## Quando pedir ajuda à Kling

`kling feedback` serve para job travado, erro opaco, bloqueio de conteúdo duvidoso, anomalia de cobrança, resultado vazio ou parcial. Ele **não** refaz nem reembolsa. No projeto é escrita externa: só com ok do producer; guarde o texto enviado no ledger.

## Quando parar e avisar (não insistir)

Três falhas seguidas do mesmo comando; qualquer pedido de cobrança que não bate com o plano; qualquer saída com credenciais; página/ferramenta que pede login diferente do fluxo oficial.
