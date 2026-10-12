# Correção do README e revisão das três skills — 2026-10-12

Complemento da entrega `2026-10-12-agent-catalog-frontend-v1`. Escopo restrito: corrigir documentação e comparar as três divergências já conhecidas. Nenhum runtime, fonte de skill externa, registry hash, gitlink, mídia ou estado criativo foi alterado.

## README corrigido

`sites/movies-demandas/README.md` passou de `4b5ee2f505bcafaa3d25033cc146690edb6ffd19f8f9bf69384c114898f37b04` para `efc14de38a3d2703e204dc3e1cee836b6e1c2ad748fe16f690baaab22bc1718f`. Quatro passagens foram corrigidas após comparar seu hash com a entrega anterior:

- Remove a descrição limitada a quatro arquivos e a alegação de retrato já revisado.
- Explica `workspace.json`, as quatro fontes do filme, o `visualRestart` opcional e cada entrada de `sourceVersions`; o pacote `sources` é a lista exata de arquivos/hashes.
- Identifica `agents/generated/catalog.json` como catálogo derivado dos registros, briefs e SKILL.md efetivos.
- Distingue descrições resumidas/metadados exportados do corpo completo dos procedimentos e informa a conferência de hashes.

A geração permanece explícita. Os exportadores e dados não mudaram. `agent_catalog.py --check`, ambos exportadores `--check`, `check-data.mjs`, `git diff --check -- README.md` e a verificação reversa do patch passaram. Nenhum build, teste amplo ou browser QA foi repetido por uma mudança somente documental; a evidência anterior permanece histórica.

## Proveniência recuperada

As fontes correntes são os diretórios `/home/athar/.hermes/skills/creative/<nome>/SKILL.md`, alcançados pelos links `skills/<nome>` do Movies. Não há Git na árvore de origem. O histórico Git do Movies consultado guarda links simbólicos (modo 120000), não o conteúdo histórico das skills.

As três versões `sourceSha256` e também as três versões `previousSourceSha256` foram encontradas em `/home/athar/.hermes/.curator_backups/blobs/<sha256>`. Cada um dos seis blobs foi lido e teve o SHA-256 recalculado; todos coincidem com o registro. Os dois arquivos de backup de skills de agosto/setembro não continham essas skills. Não foram consultados segredos, configurações de backup ou bancos de sessões.

A comparação abaixo usa a versão `sourceSha256` registrada contra o arquivo atual. A versão declarada nos frontmatters permanece `1.0.0`; os hashes distinguem as revisões.

| Skill | Hash registrado (prefixo) | Hash atual (prefixo) | Linhas do diff |
|---|---|---|---|
| film-character-continuity | `56cd809def3f` | `0b4a8cdd8e43` | +31 / −3 |
| film-dialogue-localization | `933efa495fc4` | `8b519a026d64` | +28 / −7 |
| film-editing-qc | `68ba02d12247` | `1fcb9807423e` | +65 / −4 |

O registro indica rehash em 2026-10-09 11:28:02−03:00. Os mtimes atuais são posteriores nesse dia (12:06 para diálogo; 13:12 para continuidade/QC). Isso é apenas metadado de arquivo: não prova autoria, horário real de edição, aprovação ou instalação. A identidade dos bytes históricos é verificável; autoria de cada delta não foi estabelecida.

## Alterações relevantes e limites

**film-character-continuity:** acrescenta prioridade à composição e variantes de escuta derivadas do still aceito; detalha contagem/grades de todos os frames, incluindo a última grade parcial, e distingue revisão por frames de playback completo. Acrescenta prova do espaço compartilhado e eyelines a partir de um master, com cabeça histórica fora do enquadramento e variante de nuca condicionada à aprovação. Separação entre semelhança facial e de voz reforçada. Esses exemplos não aprovam nova composição ou gasto; as restrições do filme continuam prevalecendo.

**film-dialogue-localization:** separa likeness, articulação/sincronismo, transcrição e semelhança vocal; admite guia/scratch explicitamente autorizado sem transformar isso em aprovação da voz final. Diferencia áudio externo de áudio nativo com voz vinculada ao Element e propõe testar a fala nativa quando houver suporte declarado. Acrescenta STT local e tiras de articulação como evidência; erro de transcrição não vira rejeição automática. Risco operacional: exemplos dependem de capacidade atual do provedor e ferramentas locais; esta leitura não confirmou disponibilidade nem executou testes pagos, TTS ou STT.

**film-editing-qc:** acrescenta retomada pelas fontes após compactação, preservação de concorrência e integração canônica pelo produtor. Reforça evidência de autorização, persistência de intenção/ID antes da submissão, proteção contra reenvio duplicado e conciliação de cobranças ambíguas. Detalha limites de revisão por frames, compatibilidade de estados/esquemas no validador e posicionamento de reações depois da fala que as motiva. São orientações operacionais; sua presença no texto não comprova que todos os controles estejam implementados ou testados no runtime.

As diferenças são substantivas e predominantemente acrescentam salvaguardas/refinamentos. A revisão cobre apenas os SKILL.md responsáveis pelos avisos, não a história completa de receitas referenciadas, a qualidade de mídia ou compatibilidade de providers. Não representa adoção formal das revisões. As três divergências e os hashes registrados permanecem intactos, conforme o escopo somente leitura.

## Fechamento e preservação

O handoff v2 supersede a alegação de versão atual de v1, mantendo v1 byte a byte e reconferindo as demais fontes. O manifesto v2 complementa o manifesto original sem sobrescrever sua história. O arquivo concorrente `Movies_Projects.code-workspace`, observado como untracked, não foi aberto ou editado; as demais alterações anteriores também foram preservadas.

Não houve publicação, instalação/ativação de adaptadores, reinício de agentes/serviços, commit/push/merge ou mudanças nas skills externas. O gitlink sem `.gitmodules` não foi alterado. Produtor/base deve revisar o fechamento e decidir o tratamento futuro dos hashes de proveniência; nenhuma atualização foi feita apenas para silenciar avisos.

Evidência estruturada: `reports/2026-10-12-skill-provenance-review.json`. Diffs e patch incremental estão no workspace da tarefa em `deliverables/film-*.diff` e `deliverables/readme-correction.patch`.
