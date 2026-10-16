# 11 · Receitas de preparação do filme

> Atualização 16/10/2026: consultar [contrato V4 por interface](19-kling4-migration.md) e `shared/kling-capabilities.json`. Evidências anteriores são datadas; anúncio não amplia a CLI atual.

A fonte ativa é `workspace.json` → `productionPlan`. O plano mantém roteiro inglês, cinco encontros, identidade por uso, mesa D04, D09, zero rostos históricos completos e D14. As receitas anteriores continuam no histórico Git; os valores antigos eram observações/estimativas, não cotações de novos pedidos.

As sete famílias editáveis ficam em `shared/templates/kling-shot-families.json`, validadas pelo mesmo preflight do runner. `production_plan.py template --family F3 --shot G-P04` produz um spec bloqueado para envio, lendo a linha exata do CSV. Não remover o bloqueio sem fechar referências, schema, cotação e liberação do pedido.

| Família | Função e verificação |
|---|---|
| F1 | Composição compartilhada: separar foto real, mesa e ambiente; cabeça histórica fora. |
| F2 | Variante mínima de escuta/fala a partir do mesmo master; não mudar assento, mesa ou luz. |
| F3 | Fala inglesa exata com voz nativa apenas guia; duração medida + pausas; conferir boca e dublagem posterior. |
| F4 | Escuta/reação motivada; recorte seguro contínuo; nunca confundir ausência de controle com silêncio. |
| F5 | Contato de mão/pé/mesa; anatomia e materiais; sem presumir que Element facial resolve props. |
| F6 | Atuação: vídeo qualificado, duração real, orientação e direitos; não orçar 30 s como 5 s. |
| F7 | Primeiro/último quadro compatíveis em rota com cauda declarada; não tratar toda segunda imagem como tail. |

Galileo local: G-L03/G-L04, IN/OUT candidatos e olhos B depois da frase. As imagens antigas com mesa atrás ou eixo invertido ficam fora desse corte. Os detalhes das mãos são opcionais e ainda precisam de continuidade material; não produzir planos só para preencher inventário. Rosto histórico completo continua proibido inclusive em reflexos.

A/B encerrado: v3_0 27 + Turbo 24 = 51 créditos declarados. Uma amostra por modelo não estabelece ranking. Não há terceiro job nem teto herdado. `production_plan.py jobs` lê intenções/recibos existentes; novas receitas exigem preço por pedido e revisão. Nenhum exemplo deste manual autoriza sonda paga, criação de Element ou upload.
