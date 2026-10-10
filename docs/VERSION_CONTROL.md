# Versionamento do projeto

O workspace usa **Git com Git LFS**, na branch `main`. A inicialização local foi solicitada pelo usuário em 9 de outubro de 2026. Em 10 de outubro de 2026, Andre autorizou o envio para o repositório privado [andreathar/Movies_Projects](https://github.com/andreathar/Movies_Projects), configurado como `origin`; `main` acompanha `origin/main`.

A primeira publicação integrou o commit remoto `65976e5` ao histórico local `5c50da9`, preservando `initial.txt`, por meio do merge `c6b11a8`. O push informou 937 objetos LFS enviados (~1,6 GB). Essa autorização cobre esta publicação; futuros commits, integrações e envios continuam sujeitos ao escopo da tarefa. A visibilidade privada foi verificada nesta entrega; não é uma configuração imutável.

## O que fica no histórico

- Roteiros, falas, bíblias, fontes do atlas, código, templates e documentação.
- Estado de produção, tarefas, aprovações, inventários, proveniência e evidências.
- Fotos de entrada, referências sintéticas, áudios, imagens, PDFs e pacotes de apresentação. A mídia é armazenada com **Git LFS**; os arquivos continuam normais e editáveis na pasta do projeto.
- Links de skills e diretórios necessários à produção. O destino externo de um symlink não é copiado para o repositório.

Ambientes Python, caches, arquivos temporários de editor e credenciais usuais são ignorados. Atributos de texto preservam os bytes e finais de linha para não invalidar hashes de proveniência. Fotos e vozes pessoais versionadas estão incluídas no repositório privado autorizado; publicar em outro destino ou alterar a visibilidade exige uma decisão específica.

## Ciclo de trabalho dos agentes

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

## Integração entre lanes
Seguir a seção Worktrees, commits e integração de [REPEATABLE_WORKFLOW.md](REPEATABLE_WORKFLOW.md). Uma sessão coordenadora integra uma entrega por vez, após conferir diff, base, trabalho não commitado e evidências. Alterações salvas e commits não sincronizam automaticamente outras worktrees. Commit, merge e publicação são ações distintas, com autorizações distintas. O botão Publish Branch não é necessário à colaboração local. O ciclo de comandos acima descreve o procedimento quando autorizado; não concede autorização permanente de commit.
