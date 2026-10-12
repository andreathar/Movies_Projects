> **Resume order (2026-10-09):** for agents, read `AGENTS.md`, then `projects/andre-time-travel/memory/STATE.md` (the single resume surface). This page is the pt-BR human index of deliverables and editing locations. Original text below is unchanged.

# Andre viajando no tempo — comece por aqui

Este projeto é a fonte local de trabalho da série. O filme ativo é **The Table Between Centuries**. A pasta do Google Drive contém uma entrega anterior; não é sincronizada automaticamente com as edições locais.

O histórico é mantido em Git com Git LFS para mídia, com publicação autorizada no GitHub privado. Leia [Versionamento e colaboração](docs/VERSION_CONTROL.md) para o destino, a evidência do envio e as regras de commit.

## Para ver os materiais

- [Atlas visual entregue, versão 1](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/index.html): galeria, 79 cartões e quatro testes de voz.
- [Referências em PDF](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/reference-atlas.pdf).
- [41 cartões de tomadas](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/storyboard-cards.pdf).
- [22 cartões de interpretação](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/performance-cards.pdf).
- [Roteiro comentado](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/documents/director-script-en.md).
- [Problemas observados e lacunas de cobertura](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/documents/review-findings.md).
- [Bíblia visual ampliada com todas as imagens locais](docs/master_production_visual_bible.md): propostas R1/R2, figurinos e traduções; conteúdo pendente de revisão.
- [Atlas V2 reconstruído a partir das fontes editáveis](projects/andre-time-travel/05_storyboard/preproduction-atlas-v2/index.html): prova de reconstrução do workflow, sem novas gerações pagas.
- Atlas V3 já existe em `projects/andre-time-travel/05_storyboard/preproduction-atlas-v3/`. É documento derivado, com `approved: false`. A próxima renderização precisa de uma pasta nova; o renderer recusa sobrescrever a v3.
- [ZIP de apresentação da versão 1](projects/andre-time-travel/05_storyboard/The-Table-Between-Centuries-Preproduction-v1.zip): cópia para consulta, não backup completo nem fonte de edição.

As imagens são cartões montados com referências existentes. Sua presença aqui não significa aprovação de semelhança, roupa, época ou tomada. Os áudios são testes, ainda sem aceite de interpretação/pronúncia.

## Para um agente continuar o trabalho

1. Ler [AGENTS.md](AGENTS.md), [workspace.json](workspace.json), [estado atual](projects/andre-time-travel/memory/STATE.md), [manifesto](projects/andre-time-travel/manifest.json), [tarefas](projects/andre-time-travel/tasks/board.json) e [aprovações](projects/andre-time-travel/00_brief/approvals.json).
2. Ler o [procedimento local](skills/andre-time-travel/SKILL.md), o [fluxo repetível](docs/REPEATABLE_WORKFLOW.md) e o [contrato de edição local](docs/LOCAL_AGENT_HANDOFF.md).
3. Executar o status e a validação antes de editar. Consultar os papéis em [agents/registry.json](agents/registry.json).
4. Escolher somente arquivos do escopo atribuído; registrar o hash inicial e a entrega. Preservar trabalho simultâneo e versões entregues.

## Onde editar

| Material | Fonte editável | Resultado derivado |
|---|---|---|
| Falas e roteiro | [script-en.md](projects/andre-time-travel/01_script/script-en.md) e [dialogue-lines.csv](projects/andre-time-travel/01_script/dialogue-lines.csv), mantidos juntos | Cartões de fala e roteiro comentado |
| Direção, intenção, referência de cada quadro e lacunas | [atlas.json](projects/andre-time-travel/05_storyboard/source/atlas.json) | Nova pasta de atlas com PDFs, PNGs, CSVs e galeria |
| Geometria, identidade e continuidade | [03_bibles](projects/andre-time-travel/03_bibles) | Revisões e propostas para aprovação |
| Plano de duração e tomadas | Manifesto + [shot-list.csv](projects/andre-time-travel/05_storyboard/shot-list.csv), pelo produtor | Cobertura, animatic e orçamento |
| Voz | [Testes e proveniência](projects/andre-time-travel/04_audio/voice-tests/codex-opening-v1/provenance.json) | Revisão auditiva e futuras gravações aprovadas |
| Próxima história | [Modelo de continuação](shared/templates/continuation.json) | Rascunho independente em `drafts/` |

Não edite PDFs/PNGs para corrigir o conteúdo de origem. As decisões de cena ficam no JSON; a diagramação fica no gerador local. Originais de fotos, respostas de provedores e mídia gerada são preservados.

## Verificação e retomada

```bash
.venv/bin/python scripts/manage.py status
.venv/bin/python scripts/manage.py validate
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/workflow.py verify --index reports/workflow-v1/file-index.json
```

O índice registra caminhos relativos, tamanho, categoria e SHA-256 de cada arquivo no escopo. Mudanças locais posteriores aparecem como mudanças; gere um novo índice depois da revisão. Uma verificação íntegra não concede aprovação criativa.

O [resultado legível da validação](reports/workflow-v1/README.md), o [relatório detalhado](reports/workflow-v1/validation.json) e o [ensaio de continuação](drafts/workflow-rehearsal/README.md) distinguem o que foi executado localmente do que ainda precisa de piloto, revisão humana e mídia final.
