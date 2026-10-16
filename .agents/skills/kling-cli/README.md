# Skill Kling do projeto

Adaptação em português de `klingai-tech/skills` 0.2.1, com revisão local dos contratos.
Leia [SKILL.md](SKILL.md), [reference.md](reference.md) e [api-examples.md](api-examples.md).
A skill não é o executável: o pacote instalado é `@klingai/cli-global`.

Atualização upstream usa `npx skills add klingai-tech/skills`, mas pode substituir
esta tradução. Não execute durante produção nem sem comparar/preservar mudanças locais.
Proveniência e hashes estão no registry do projeto. Não altere credenciais para atualizar.

## Contrato V4 datado

Consultar `docs/kling-manual/19-kling4-migration.md` e `shared/kling-capabilities.json`. Exemplos legados não autorizam flags em outra rota. V4 exige shotContract local; o runner preserva o contrato no fingerprint/intent e não o envia como argumento. F8/F9 são propostas bloqueadas; 4K/HDR/extensão não estão liberados nesta CLI.
