# 10 · Áudio, voz e sincronismo

> Atualização 16/10/2026: consultar [contrato V4 por interface](19-kling4-migration.md) e `shared/kling-capabilities.json` antes de escolher rota/custo. Tabelas e pilotos anteriores abaixo são evidência datada, sem liberação nova.

**D14 vale também para o inglês:** a voz Kling foi rejeitada como voz final e permanece guia. A edição inglesa vem primeiro; a edição histórica tem revisão e timing próprios. Capacidade de produzir uma trilha, áudio não nulo e voz vinculada ao Element não equivalem à aprovação por ouvido.

| Recurso | Contrato local |
|---|---|
| `enable_audio` | Somente modelos que declaram o parâmetro; definir explicitamente. v2.6 exige 1080p sem cauda. |
| Turbo | Não declara controle de áudio ou Elements. Os A/B retornaram AAC muito baixo; não prometer silêncio pela ausência do parâmetro. |
| Voz do Element | Amostra de voz é um recurso de entrada; não prova consistência de timbre no resultado. Readback e escopo de upload são separados. |
| `keepOriginalSound` | Preserva som do vídeo em rotas que o declaram. Não é áudio independente nem clonagem. |
| Omni com `video_1` | `enable_audio=false`; preservar som e gerar áudio nativo são opções diferentes. |
| Áudio externo | Nenhum slot `audio_N` nas rotas de vídeo do snapshot. Não anexar áudio a qualquer modelo. |
| Motion control | Usa vídeo de atuação e imagem. Uma hipótese de transferência de boca não é teste de dublagem aprovado. |

A matriz datada vem de `python3 scripts/production_plan.py routes`. API, app e CLI não são superfícies intercambiáveis. Não há ferramenta de treino Face Model, lip-sync ou V4 no snapshot desta integração. Publicidade ou uma skill remota com versão divergente não altera a CLI instalada.

Antes de ampliar fala visível: selecionar por ouvido uma voz entre os candidatos existentes, confirmar a rota compatível, fazer prova limitada e revisar dentes/boca/queixo, identidade, timing e termos falados. Nenhum serviço externo, clonagem ou nova voz foi autorizado pela implementação local. Não trocar para outro fornecedor para contornar um slot ausente.

O roteiro e os IDs permanecem no CSV inglês. Duração medida do áudio-guia ajuda a montar pausas; não é duração real de uma voz final futura. A G-L04 guia mede 8,616 s: não cabe em 3 s. Templates propõem 11 s como ponto de planejamento, sujeito à seleção e orçamento; não garantem cauda de silêncio exata. Não acelerar a fala para caber.

Revisão: ouvir todo o arquivo exato, conferir palavras/pronúncia e julgamento de timbre de Andre, depois sync visível e deriva. STT, RMS e folhas de quadros auxiliam, sem substituir audição e reprodução. D14 menciona cerca de 120 ms como alerta de deriva, não critério universal de aceite. Reação ocorre após a ideia que a causa; a pré-visualização local a coloca depois da fala inteira enquanto alinhamento por palavra permanece pendente.

Edição histórica exige alvo linguístico, tradução/retrotradução, pronúncia e revisor competente; suporte de idioma moderno não autentica dialeto histórico. Não sobrepor tradução a boca incompatível e chamar de master. Novas trilhas, processamento ou correções geram derivados preservando originais.
