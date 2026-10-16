# Mídia canônica, catálogo e lanes leves

`projects/andre-time-travel/asset-registry.csv` é o único catálogo ativo de mídia. IDs, tipos e estados de aprovação existentes foram preservados. O catálogo continha 290 IDs na reconciliação de 2026-10-13; referências distintas podem apontar ao mesmo arquivo canônico sem criar outra cópia. Aprovação de registro não aprova novos usos, derivados ou jobs.

A reparação técnica de 2026-10-13 normalizou campos e caminhos e consolidou 16 correções de hash já documentadas. O CSV integral anterior e todos os valores/provas estão em `reports/asset-registry/asset-registry-before-20261013.csv` e `repair-20261013.json`. Registros históricos não participam da resolução corrente. Quatro literais históricos de origem com extensão duplicada permanecem preservados, sem afirmar uma origem ainda não comprovada; os caminhos/hashes dos recortes atuais foram verificados.

## Uso e validação

Executar antes de entregar alterações de metadados:

```sh
.venv/bin/python scripts/manage.py assets validate
.venv/bin/python scripts/manage.py assets resolve --asset-id ID_EXISTENTE
```

Resolução recusa catálogo inválido, ID ambíguo, escape de raiz, referência de provedor como arquivo e ponteiro LFS não hidratado. O campo `hash_verified` de `resolve` é falso: essa chamada verifica resolução, não re-hasheia bytes. A auditoria de reparação registra as verificações de hash realizadas sobre os arquivos exatos. Não tratar execução, arquivo existente ou pasta chamada `approved` como aceite criativo.

## Perfil compartilhado

Em 2026-10-13 13:32 UTC, o perfil `shared-media` foi configurado no projeto Parley para **futuras lanes**, com raiz canônica Movies_Projects e o catálogo acima. O pool de spares permanece desativado. O inicializador que criava `.venv --without-pip` por lane foi removido. Isso não modifica o `.venv` canônico do produtor, restaura lanes excluídas ou cria permissões/grants.

O launcher materializa worktrees novas sem checkout inicial, aplica exclusões de mídia pelo índice e evita smudge LFS antes do checkout. Arquivos pesados são referenciados pela raiz canônica, com derivados em diretório da lane/tarefa. Não há fallback para clone completo, hidratação implícita, mount ou cópia de mídia. Ferramentas de gestão são stdlib; usar a instalação/ambiente já existente quando necessário. Acesso nativo depende das permissões reais do cliente: configuração de caminho não é comprovação de leitura e a implementação não impõe somente leitura no filesystem.

```sh
agent-parley workspace status --repo /CAMINHO/Movies_Projects --json
agent-parley workspace plan --repo /CAMINHO/Movies_Projects --json
agent-parley media doctor --repo /CAMINHO/Movies_Projects --sample inbox/andre-reference-photos/20230817_203913.jpg --json
```

`media doctor` mantém saída não-zero enquanto acesso nativo não for comprovado; uma leitura limitada do host não resolve esse limite. Nenhuma lane/grant novo foi criado para esses checks. O OpenCode existente usa worktree excluída; nova identidade/grant diagnósticos dependem de decisão explícita. Mensagens históricas59/65 não serão reenviadas.

## Frontend e rollback

O painel Movies exporta somente resumo, caminhos e hash do catálogo, usando `manage.py assets validate`; não mantém catálogo paralelo nem consulta credenciais. Contagens de referências e caminhos são separadas. `--check`, testes, tipos e build validam derivados; importação do pacote de produção no banco, publicação e aceites continuam etapas próprias. A aba Agents do console Parley usa estado do coordenador e distingue configuração e prova nativa; esse console não foi iniciado por esta entrega.

Rollback é seletivo e recusa drift. O backup do CSV restaura a forma histórica inválida apenas sob revisão; não rebobina imagens ou aprovações. O rollback de configuração remove o perfil futuro e restaura apenas o inicializador anterior, preservando identidades, grants e demais campos. A auditoria e handoff contêm hashes e limites. Não restaurar cegamente uma base inteira de coordenação.

## Arquivo delimitado de experimentos Kling — 2026-10-15

O catálogo recebeu 28 referências experimentais, todas com `approved=false`, mantendo as 290 linhas anteriores literalmente. [Galeria e proveniência](../projects/andre-time-travel/07_generations/downloads/2026-10-15-element-experiments-v1/index.html): 27 arquivos únicos, 24 novos (59.860.079 bytes), três locais reutilizados por hash; nove são previews sem originais. As capas da mesa/figurino apontam aos arquivos anteriores, sem nova cópia nem aceite. Os 318 IDs atuais são verificáveis por `manage.py assets validate`; contagem futura deve vir do catálogo. O painel exporta somente metadados/caminhos, sem mídia ou prompts.
