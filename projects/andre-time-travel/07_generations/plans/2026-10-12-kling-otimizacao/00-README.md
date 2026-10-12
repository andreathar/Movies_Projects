# Kling — hipóteses de otimização, ainda bloqueadas

Revisão de 2026-10-12. Nenhuma submissão/upload foi feita nesta auditoria. Os specs
são rascunhos e contêm `submissionBlocked` e `auth` placeholder. Não estão prontos
para execução. O produtor precisa revisar pedido e orçamento e registrar o escopo
específico antes de remover o bloqueio. Flags de aprovação do filme não foram alteradas.

A CLI efetiva é `@klingai/cli-global` 0.2.1, independente da skill 0.2.1. Nenhuma
alternativa avaliada demonstrou ser substituta claramente melhor para a mesma
conta/créditos/Elements. Não instalar nem migrar por causa deste pacote.

## O que foi corrigido

- Turbo não declara `elements` nem `enable_audio` no snapshot consultado. AB-01 perdeu
  o marcador sem binding e não promete silêncio. Isso não prova silêncio ou fidelidade.
- AB-01 e AB-02 são ambos 1080p e mudam modelo/Element/controle de áudio. Não isolam
  resolução. Um par 720p/1080p deve manter modelo, entrada, prompt, Element, áudio e
  multi-shot iguais; sem seed controlável ainda existe variação estocástica.
- **90 créditos era estimativa histórica, não cotação.** Nenhum preço atual foi obtido.
- Motion 1 é descrito no registro anterior como **30 s**. Os 45/60 créditos calculados
  para 5 s foram retirados. O texto do prompt não recorta a referência.
- Não há prova de que a resolução seja a causa principal da diferença para a interface.
  Qualidade depende também de modelo, configuração, identidade, movimento e seleção.

## Estado das propostas

| Arquivo | Estado e dependência |
|---|---|
| `ab-teste-resolucao-modelo.json` | Bloqueado; desenho de comparação, compatibilidade, custo e autorização pendentes |
| `motion-control-specs.json` | Bloqueado; duração real/recurso, adequação visual, custo e autorização pendentes |
| `03-politica-de-resolucao.md` | Hipótese revisada; não muda resolução de produção automaticamente |
| `04-guia-prompts-motion-control.md` | Guia criativo; exemplos não são comandos autorizados |
| `01-upgrade-skill.md` | Registro histórico do upgrade upstream; adaptação portuguesa posterior preservada |
| `02-regerar-ficha-modelos.md` | Procedimento de snapshot; consulta atual não listou V4 |

A ficha em `docs/kling-manual/03-modelos-ao-vivo.md` é um snapshot datado. O servidor
MCP 1.3.3 retornou catálogo autenticado sem V4 em 2026-10-12. Documentação pública
sobre V4 Preview não garante liberação nessa conta.

## Próximo passo e dono

Produtor: preparar uma comparação pequena e controlada com referência revisada,
parâmetros explícitos, duração medida, fonte/data da estimativa ou cotação e teto
específico. Andre conserva os gates de semelhança, voz e aceite pertinentes.

A pré-checagem é offline:

```bash
python3 -B docs/kling-manual/tools/kling_preflight.py <spec> --json
```

É esperado que estes rascunhos falhem enquanto estiverem bloqueados. Depois de todo
escopo conferido, o produtor usa `scripts/kling_batch.py` com `--submit-only` para
um job e `--resume JOB` para consultar. Essa documentação não manda executá-los agora.
