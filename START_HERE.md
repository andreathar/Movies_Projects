> **Ordem de retomada (2026-10-09):** agentes leem `AGENTS.md` (regras e ordem de início) e depois `projects/andre-time-travel/memory/STATE.md` (única superfície de retomada). Esta página é o índice em português para pessoas: entregas, onde editar e qual documento é a fonte de cada assunto. Revisão consolidada em 2026-10-09; texto anterior preservado no histórico Git e em `docs/consolidation-2026-10-09/`.

# Andre viajando no tempo — comece por aqui

Este projeto é a fonte local de trabalho da série. O filme ativo é **The Table Between Centuries**. A pasta do Google Drive contém uma entrega anterior; não é sincronizada automaticamente com as edições locais.

O histórico agora é mantido em Git local com Git LFS para mídia. Leia [Versionamento e colaboração](docs/VERSION_CONTROL.md) antes de preparar um commit. Não há remoto ou publicação no GitHub.

## Para ver os materiais

- [Atlas visual entregue, versão 1](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/index.html): galeria, 79 cartões e quatro testes de voz.
- [Referências em PDF](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/reference-atlas.pdf).
- [41 cartões de tomadas](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/storyboard-cards.pdf).
- [22 cartões de interpretação](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/performance-cards.pdf).
- [Roteiro comentado](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/documents/director-script-en.md).
- [Problemas observados e lacunas de cobertura](projects/andre-time-travel/05_storyboard/preproduction-atlas-v1/documents/review-findings.md).
- [Bíblia visual ampliada com todas as imagens locais](docs/master_production_visual_bible.md): propostas R1/R2, figurinos e traduções; conteúdo pendente de revisão.
- [Atlas V2 reconstruído a partir das fontes editáveis](projects/andre-time-travel/05_storyboard/preproduction-atlas-v2/index.html): prova de reconstrução do workflow, sem novas gerações pagas.
- [ZIP de apresentação da versão 1](projects/andre-time-travel/05_storyboard/The-Table-Between-Centuries-Preproduction-v1.zip): cópia para consulta, não backup completo nem fonte de edição.

As imagens são cartões montados com referências existentes. Sua presença aqui não significa aprovação de semelhança, roupa, época ou tomada. Os áudios são testes, ainda sem aceite de interpretação/pronúncia.

## Para um agente continuar o trabalho

A ordem de início é a de [AGENTS.md](AGENTS.md), seção "Session start" — não é repetida aqui. Depois dela, ler o [procedimento local](skills/andre-time-travel/SKILL.md) e executar o status/validação antes de editar. Escolher somente arquivos do escopo atribuído; registrar o hash inicial e a entrega; preservar trabalho simultâneo e versões entregues.

### Qual documento é a fonte de cada assunto

| Assunto | Fonte única |
|---|---|
| Regras inegociáveis (rostos, referências, diálogo, gasto, Kling, credenciais, memória) | [AGENTS.md](AGENTS.md) |
| Estado e retomada do filme | [STATE.md](projects/andre-time-travel/memory/STATE.md), com [manifesto](projects/andre-time-travel/manifest.json), [tarefas](projects/andre-time-travel/tasks/board.json) e [aprovações](projects/andre-time-travel/00_brief/approvals.json) |
| Processo reutilizável, tarefas e dependências | [REPEATABLE_WORKFLOW.md](docs/REPEATABLE_WORKFLOW.md) |
| Quem edita o quê, formato de entrega, aprovação por versão | [LOCAL_AGENT_HANDOFF.md](docs/LOCAL_AGENT_HANDOFF.md) |
| Commits, integração entre lanes, backup | [VERSION_CONTROL.md](docs/VERSION_CONTROL.md) |
| Responsáveis deste episódio e mecânica dos lanes | [PARLEY_PROTOCOL.md](docs/PARLEY_PROTOCOL.md) |
| Economia de contexto e mensagens | [TOKEN_EFFICIENCY.md](docs/TOKEN_EFFICIENCY.md) |
| Papéis e limites de cada função | [agents/README.md](agents/README.md) e [agents/registry.json](agents/registry.json) |
| Relatório da consolidação documental (mapa completo, antes/depois, conflitos) | [consolidation-report.md](docs/consolidation-2026-10-09/consolidation-report.md) |

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
