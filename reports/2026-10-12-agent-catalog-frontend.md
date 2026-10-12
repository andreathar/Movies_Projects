# Fontes únicas, adaptadores e frontend — 2026-10-12

## Resultado aplicado

O consumidor confirmado é `sites/movies-demandas`, a Central de Demandas de Movies_Projects. O catálogo agora deriva descrições e responsabilidades dos registros, briefs e SKILL.md efetivos. A fonte Kling foi corrigida para `.agents/skills/kling-cli`; a proveniência antiga ficou em `provenanceHistory`. A tradução inglesa e seus contratos foram preservados. CLAUDE.md e READMEs não afirmam mais que todas as skills estão espelhadas em Claude.

`workspace.json` aponta para o escopo visual já entregue. O exportador verifica seus seis hashes de entrada e os cinco encontros C/K/G/N/O. O painel apresenta roteiro e encontros preservados, novas cenas em planejamento, nenhuma execução registrada nesse escopo e aceites anteriores limitados às suas versões. Board, manifesto, aprovações, roteiro, CSV, STATE, ledger, registro de assets e entrega anterior mantiveram os hashes de base.

Os snapshots têm fontes/hashes, fingerprint do conteúdo, data de coleta e base Git. Repetição com entradas idênticas preserva bytes; `--check` recusa deriva sem escrever. Os resumos de papéis e títulos das tarefas oficiais deixaram de ser cópias manuais no frontend. Rótulos de apresentação continuam locais. O build valida o pacote incluído; atualidade contra Movies requer os exportadores com `--check`. A UI preserva demandas/comentários e exige revisão antes de trocar um retrato persistido.

Também foi corrigido um erro de lint preexistente no carregamento inicial, usando a resposta assíncrona e descartando o resultado após desmontagem. Autenticação, origem e controle de revisão do backend foram preservados.

## Preparado, sem ativação

Seis adaptadores derivados de historian/continuity/qc, para Claude e Codex, estão em `agents/generated/`; nenhum foi registrado em pastas de descoberta ou em configuração de usuário. Producer/director/coordinator continuam governança. Claude segue o frontmatter observado nos plugins do cliente 2.1.296; TOMLs Codex são sintaticamente válidos para o formato preparado, mas descoberta/carregamento no cliente 0.162.1 não foram executados. Nenhum modelo, sessão, lane, MCP, grant ou permissão foi ativado. Os textos operacionais não são uma barreira de segurança.

## Verificação realizada

- Python: 92 testes passaram, incluindo 8 do catálogo. Após abreviar a descrição exibida e acrescentar origem efetiva ao catálogo, os 8 testes afetados passaram novamente.
- Frontend: 19 testes passaram (modelo, compatibilidade de snapshots anteriores, escopo visual, referências, deriva, idempotência e falhas de fontes/links).
- `manage.py validate`: OK; apenas três avisos preexistentes de hashes de skills compartilhadas. Não foram regravados para esconder divergências.
- `agent_catalog.py --check`, os dois exportadores `--check` e verificação dos pacotes incluídos: OK.
- TypeScript, ESLint e build Vinext: passaram. As telas renderizaram com os mesmos pacotes verificados.
- QA em Chrome: visão geral, Produção, Skills, filtro Kling, origem/hash, cinco encontros, distinção de planejamento/execução/aceite e Fontes com versão Git/fingerprint. Evidência DOM e duas capturas no workspace desta tarefa.
- Preview em cópia isolada com dependências já instaladas e banco D1 sintético. A ausência inicial da tabela foi corrigida aplicando somente a migração existente nesse banco de teste. HTTP 200 e inicialização local confirmados. Nenhuma escrita no site publicado; aba original restaurada. Servidor temporário encerrado.

## Concorrência e revisão

Baseline Movies: `2db8713bd74ae1fe9410b9281660a8abbc4df948`. Durante a tarefa apareceu o commit concorrente `f16cd363f8b36eda88636efbb464b169d179368c` contendo a primeira parte deste lote; foi preservado. Esta execução não fez commit, push, merge ou deploy. Ajustes posteriores do gerador/catálogo e o fechamento ficam para revisão. Frontend baseline: `dfb945f3aaaf5aaac20ed323cda66dd26d047bb9`.

O frontend é um repositório separado, registrado no pai como gitlink sem `.gitmodules`. A estrutura Git foi preservada; revisar os dois repositórios separadamente. O novo handoff substitui a alegação de versões atuais do handoff documental anterior, mantendo o arquivo histórico intacto e reconferindo seus demais artefatos. Não registra ingestão nem aceite do produtor.

## Pendências com responsável

1. Produtor/base: revisar este lote e integrar a retomada; publicar o frontend somente quando autorizado. A versão publicada continua anterior. Depois de publicar, revisar/importar o snapshot atualizado em contas com retrato persistido.
2. Produtor + responsável pelo cliente: validar carregamento e registro único dos adaptadores antes de ativá-los. Não presumir descoberta automática do Codex.
3. Responsável pelas skills compartilhadas: revisar as divergências de film-character-continuity, film-dialogue-localization e film-editing-qc. Seus hashes históricos permanecem.
4. Produtor/direção: revisar a proposta visual e atribuir a próxima prova de cobertura. A confirmação do escopo não é aprovação de nova mídia ou orçamento.

## Reversibilidade e preservação

`implementation/baseline.json`, backups seletivos e `deliverables/fontes-frontend-files.json` registram hashes antes/depois. Patches separados e cópias finais ficam no workspace da tarefa. Para uma reversão futura, comparar o hash atual com `after` antes de restaurar um arquivo individual; interromper se houver mudança posterior. Não usar reset/clean, não reverter o commit concorrente automaticamente e não apagar arquivos novos que possam ter recebido trabalho. O gitlink não substitui a revisão do repositório frontend.

Nenhum original, mídia, decisão, patch histórico ou lane foi removido. As evidências anteriores de Parley continuam em `deliverables/parley-final-report.md` e `deliverables/parley-rebuild-assessment.md`; esta implementação não substitui um teste ao vivo de runtime por presença no catálogo.
