# 01 · Atualizar a skill do Kling 0.2.0 → 0.2.1 (preparado, sem crédito)

**Executado em 2026-10-12 (sem crédito).** Skill agora `version: 0.2.1` com
`omni_ref_video`; telemetria alinhada; `skills/registry.json` re-hasheado e catálogo derivado
regenerado. Detalhes no fim deste arquivo.

## Estado atual (verificado 2026-10-12)

| Item | Valor |
|------|-------|
| CLI `kling` instalada | `0.2.1` |
| Última publicada (CN e global) | `0.2.1` — **já é a mais avançada** |
| Pacote instalado | `@klingai/cli-global@0.2.1` (região correta: credencial `[kling.ai]`) |
| Servidor MCP | `1.3.3` |
| **Skill empacotada em `.agents/skills/kling-cli`** | **`version: 0.2.0` (defasada)** |
| Tool ausente na skill | `omni_ref_video` (existe no CLI e no `tool_list`) |
| `--skill-version` passado nos scripts/docs | `0.2.0` (desatualizado) |

**Conclusão:** a CLI não precisa de upgrade. A **skill** precisa.

## Passo 1 — atualizar os arquivos da skill (toque no ambiente, sem crédito)

```bash
# sobrescreve por content-hash; no-op se já estiver atual. Vale na PRÓXIMA sessão.
npx skills add klingai-tech/skills
```

Conferir depois:

```bash
sed -n '1,4p' .agents/skills/kling-cli/SKILL.md      # espera version: 0.2.1
grep -c omni_ref_video .agents/skills/kling-cli/SKILL.md   # espera > 0
```

## Passo 2 — alinhar a telemetria `--skill-version` (edição local, sem crédito)

A regra da skill diz: o valor de `--skill-version` **vem do frontmatter da própria skill**.
Só trocar `0.2.0` → `0.2.1` **depois** do Passo 1, para não ficar inconsistente.

Arquivos que contêm `0.2.0` (verificar com `grep -rn '"0.2.0"' scripts/ docs/kling-manual/`):

- `scripts/kling_batch.py:27` — `TELEMETRY = [... "--skill-version", "0.2.0"]`
- `scripts/archive_kling_images.py:31` — idem
- `docs/kling-manual/00-regras-do-projeto.md:24` (texto explicativo)
- `docs/kling-manual/04`, `06`, `07`, `08`, `09` (exemplos de comando)

> Telemetria pura: não afeta resultado, autenticação ou rollout. Correção de higiene.

## Passo 3 — refresh do hash no registro da skill

`skills/registry.json` guarda `sourceSha256` de `.agents/skills/kling-cli`. Depois do Passo 1 o
hash muda e o lint pode acusar divergência. Atualizar o `sourceSha256` (e registrar a procedência)
via o fluxo normal de skills do workspace; **não** editar o hash à mão sem recomputar sobre o
conteúdo real. Ver `docs/AGENT_CATALOG.md` para o procedimento de regeneração de derivados.

## Verificação (read-only)

```bash
.venv/bin/python scripts/manage.py lint
skills/tools/... # regenerar/validar derivados do catálogo, se aplicável
```

## Rollback

Os arquivos da skill são versionados no repositório; um `git checkout -- .agents/skills/kling-cli`
restaura a versão anterior. A CLI em si não é alterada por este passo.

## Não fazer

- Não instalar a outra região (`@klingai/cli-cn`) — a conta é global.
- Não trocar endpoints, variáveis de ambiente ou `.env` — não existe superfície de configuração.
- Não ler nem imprimir `.credentials`.

## Resultado da execução (2026-10-12, sem crédito)

- **Passo 1** — `npx skills update kling-cli -p -y`: skill atualizada para `version: 0.2.1`;
  `omni_ref_video` presente (13 ocorrências no `SKILL.md`). `skills-lock.json` atualizado
  (`computedHash` novo). Toque também em `SKILL.md`, `reference.md`, `api-examples.md`, `.gitignore`.
- **Passo 2** — telemetria `--skill-version 0.2.0` → `0.2.1` em `scripts/kling_batch.py`
  (L27) e `scripts/archive_kling_images.py` (L31) e nos exemplos de `docs/kling-manual/{00,04,06,07,08,09}`;
  notas narrativas de `README`, `15` e `08` atualizadas para refletir o alinhamento.
- **Passo 3** — `skills/registry.json`: `sourceSha256` → `878472489b25ff7a64c5e79f8d420bf6f5b4d5b5a651c18df777b8262b2ee084`
  (era `52de319a…`) com entrada de proveniência (`github_update`). Derivado
  `agents/generated/catalog.json` regenerado.

**Verificação:** `tools/check-kling-drift.sh` → skill 0.2.1, `omni_ref_video: present`, telemetria
0.2.1; `scripts/agent_catalog.py --check` → `changed: []`.

**Não alterado (intencional):** `docs/kling-manual/snapshots/who_am_i.sanitized.json` mantém
`skill: kling-cli 0.2.0` — é artefato histórico de 2026-10-09 (integridade do snapshot).
