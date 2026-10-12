# Versionamento local do projeto

O workspace é um repositório **Git local**, na branch inicial `main`, preparado para uso futuro com GitHub. A inicialização foi solicitada pelo usuário em 9 de outubro de 2026. Não há remoto configurado nem publicação na nuvem.

## O que fica no histórico

- Roteiros, falas, bíblias, fontes do atlas, código, templates e documentação.
- Estado de produção, tarefas, aprovações, inventários, proveniência e evidências.
- Fotos de entrada, referências sintéticas, áudios, imagens, PDFs e pacotes de apresentação. A mídia é armazenada com **Git LFS**; os arquivos continuam normais e editáveis na pasta do projeto.
- Links de skills e diretórios necessários à produção. O destino externo de um symlink não é copiado para o repositório.

Ambientes Python, caches, arquivos temporários de editor e credenciais usuais são ignorados. Atributos de texto preservam os bytes e finais de linha para não invalidar hashes de proveniência. Fotos e vozes pessoais estão somente neste repositório local; publicar o projeto exige uma decisão específica de destino e visibilidade.

## Ciclo de trabalho dos agentes

Os comandos de leitura e de validação (`git status`, `git diff`, `manage.py validate`, testes) podem ser usados sempre. As linhas `git add` e `git commit` descrevem o procedimento **quando Andre ou o produtor autorizam um commit**; o documento não concede autorização permanente (regra em [AGENTS.md](../AGENTS.md)). Sem autorização, entregue arquivos e hashes em um handoff.

```bash
git status --short
git diff
.venv/bin/python scripts/manage.py validate
.venv/bin/python -m unittest discover -s tests -v
git add -- caminho/do/arquivo outro/caminho
git diff --cached --stat
git diff --cached
git commit -m "Descreva a mudança concreta"
```

Preparar apenas os arquivos do próprio escopo. Confirmar o diff antes do commit, principalmente quando outros agentes estiverem trabalhando na mesma pasta. Não usar `reset --hard`, limpeza de arquivos ou troca de branch com alterações compartilhadas sem uma necessidade e autorização específicas.

Um commit é um registro de versão, não uma aprovação artística nem financeira. Continuam valendo os controles do manifesto, board e aprovações. As pastas de entregas V1/V2 permanecem preservadas; editar as fontes e criar uma versão nova dos derivados.

## Inspeção do histórico

```bash
git log --oneline --decorate -10
git show --stat HEAD
git diff HEAD -- caminho/do/arquivo
git lfs ls-files
git lfs fsck
```

Para recuperar uma versão, primeiro conferir o conteúdo e salvar qualquer trabalho atual. Não restaurar automaticamente toda a pasta sobre edições de outro agente.

## Outra máquina e backup

O Git LFS foi ativado apenas na configuração deste repositório. Uma máquina nova precisa de Git LFS e dos requisitos locais de execução. Recriar a `.venv` com `python3 -m venv .venv`; as ferramentas de gestão usam a biblioteca padrão. Para o renderer, consultar as bibliotecas/fontes em `docs/REPEATABLE_WORKFLOW.md`.

Sem um servidor LFS, preservar a pasta **completa**, incluindo `.git/lfs/objects`, em um backup. Uma cópia só do histórico Git ou um `git bundle` não inclui os objetos LFS. `git lfs fsck` verifica os objetos locais; um clone/checkout com LFS indisponível pode conter apenas ponteiros no lugar das mídias. Os links de skills externos continuam dependentes do perfil da máquina.

Inventários antigos são fotografias de um momento: edições documentadas desde então aparecem como mudanças. Use um novo nome de snapshot para registrar o estado posterior, sem reescrever o inventário antigo. O relatório da inicialização fica em `reports/git-setup-v1/`.

## Worktrees, commits e integração entre lanes
As sessões trabalham em pastas/branches separadas. Um arquivo salvo na base pode ser consultado por caminho explícito antes do commit, mas não aparece automaticamente nas outras cópias. Commit na base também não atualiza branches de participantes. Dependências devem identificar versão/hash; não usar caminhos de outra lane para editar ou assumir sua identidade.

Commits registram entregas coerentes, não cada pequeno ajuste. Antes de registrar: conferir escopo, alterações concorrentes, arquivos preparados e validação pertinente. Respeitar a autorização vigente para commit; na ausência dela, entregar arquivos e hashes sem bloquear a preparação. Não presumir permissão de merge/push a partir de permissão de commit.

O produtor prepara integração de UMA entrega por vez. Conferir base da branch, mudanças locais, diff, caminhos sobrepostos e evidências; preservar trabalho não commitado. Incorporar pelo mecanismo autorizado, resolver divergências de conteúdo sem escolher cegamente uma versão e verificar o resultado integrado antes da entrega seguinte. Andre acompanha e autoriza conforme o escopo vigente; não precisa resolver sozinho conflitos técnicos.

Changes indica alterações, não necessariamente conflitos. Publish Branch publica remotamente, não integra à main. Colaboração local não exige publicação. Commit e validação técnica não são aceite artístico. Reservas de arquivos ajudam a coordenar; não são bloqueios físicos nem garantia de ausência de conflitos.

Responsáveis e lanes do filme atual: [PARLEY_PROTOCOL.md](PARLEY_PROTOCOL.md). O ciclo de comandos desta página não concede autorização permanente de commit, merge ou publicação.
