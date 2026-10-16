# Rollback restrito

Não houve commit. `authored-paths.json` e `preservation.json` delimitam as mudanças e seus hashes finais. `before/` preserva bytes de fontes alteradas antes da escrita; arquivos novos não tinham versão inicial. Antes de restaurar, conferir que o hash atual ainda é sha256After: conflito bloqueia somente aquele arquivo. Nunca usar reset/checkout da árvore inteira ou do submódulo sujo.

Restaurar somente as fontes deste refactor com backup e retirar somente os arquivos novos deste refactor. Para catálogos/adaptadores e snapshots frontend derivados sem backup byte a byte, restaurar suas fontes e regenerar com agent_catalog.py e ambos exportadores. A data/proveniência de coleta pode ser nova; nenhum dado salvo de demandas/aprovações do usuário foi alterado. Não prometer restauração byte a byte para esses derivados. Revisar o handoff de migração junto com os dois handoffs históricos preservados; restaurar fontes não equivale a ingerir ou aprovar uma entrega.
