# The Table Between Centuries — pôsteres dos cinco encontros (v2)

Nova direção solicitada por Andre: um cartaz para cada personalidade, com a câmera por cima do ombro dela em leve desfoque, Andre sentado em foco e gesticulando durante uma explicação.

Abra `index.html` para comparar os cinco. Cada PNG tem 1024 × 1536 px, proporção 2:3, RGB. O gerador integrado de imagens do ChatGPT produziu cinco composições e uma correção de cenário. As referências reais, os figurinos e os keyframes continuam preservados.

## Encontros e gestos

- **Julius Caesar — César — o peso do poder**: `01-caesar-over-shoulder.png`.
- **Genghis Khan — Gêngis Khan — o alcance de um império**: `02-genghis-over-shoulder.png`.
- **Galileo Galilei — Galileu — uma pergunta que permanece**: `03-galileo-over-shoulder.png`.
- **Napoleon Bonaparte — Napoleão — a pergunta devolvida**: `04-napoleon-over-shoulder.png`.
- **J. Robert Oppenheimer — Oppenheimer — o limite da resposta**: `05-oppenheimer-over-shoulder.png`.

## Revisão

O agente inspecionou todos os resultados: ombro do interlocutor desfocado, Andre sentado em foco, gesto de fala, título e nomes legíveis, nenhum outro rosto completo visível. O primeiro rascunho de César continha um busto humano no cenário e foi corrigido. Esse rascunho está em `rejected/`, fora da galeria, com marcação explícita para não ser reutilizado.

Galileu inclui a chamada “A QUESTION SURVIVES.” adicionada pelo gerador: texto temático de divulgação, não citação histórica. Cenários e figurinos são interpretações baseadas nos materiais do filme; não são afirmação de reconstrução histórica certificada.

A semelhança de Andre e a escolha dos cartazes permanecem pendentes de revisão do usuário. Nenhuma aprovação de filme, tarefa canônica ou crédito Kling foi alterado. Nenhum job Kling/ElevenLabs, commit ou publicação foi feito por este lote. O nome exato do modelo e o custo do recurso integrado não foram expostos.

## Continuação por outros agentes

`prompts.json` contém cada prompt e a ordem exata das referências, incluindo a correção de César. `manifest.json` registra hashes, dimensões e a revisão. Os textos estão integrados à imagem PNG: futuras mudanças devem produzir uma nova pasta de revisão, preservando esta v2 e a v1. A resolução é a nativa retornada pelo gerador, ainda sem preparação para impressão em grande formato.
