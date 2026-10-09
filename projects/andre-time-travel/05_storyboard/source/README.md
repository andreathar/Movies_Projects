# Fontes editáveis do atlas

`atlas.json` contém referências explícitas e direções para as cinco cenas, 41 tomadas e 22 falas deste episódio. Campos como `question`, `action`, `light`, `sound`, `warning`, `intention`, `emphasis`, `pause` e `missingComposition` podem ser revisados localmente no escopo atribuído.

- Caminhos de referência são relativos ao filme, exceto `realPhotoWorkspacePath`, relativo à raiz do workspace.
- O texto falado e o nome do locutor vêm de `01_script/dialogue-lines.csv`. Atualizar também `script-en.md` ao mudar uma fala; não duplicar texto no JSON.
- Preservar IDs de cenas, tomadas e falas. Mudanças de estrutura precisam atualizar manifesto/CSV e fontes de direção juntos.
- Tempos são propostas de atuação, não medições. Não registrar duração medida sem um arquivo de áudio correspondente.
- Manter o estado de candidato. Este arquivo não é um payload Kling nem uma aprovação.

O procedimento de reconstrução, dependências e versionamento está em `docs/REPEATABLE_WORKFLOW.md` na raiz. O renderer não usa serviços externos.
