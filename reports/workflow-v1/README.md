# Resultado da validação local do workflow

9 de outubro de 2026. O projeto agora tem uma entrada única em `START_HERE.md`, fontes editáveis, passagem entre agentes, registro da série, modelo limpo de continuação e inventário verificável de arquivos. Nenhum job pago foi submetido nesta etapa.

## Executado e verificado

- Reconstrução do atlas V2: 79 PNGs, três PDFs com 16/41/22 páginas, 41 direções de tomada vindas da fonte editável, 22 falas canônicas preservadas e duração planejada de 240 segundos.
- 36 hashes de insumos do renderer conferidos; 169 links da galeria resolvidos localmente; nenhum overflow de texto registrado. Dois cartões V2 foram inspecionados visualmente. Interação no navegador não foi verificada.
- 382 arquivos anteriores de fotos, referências, áudio, respostas/originais de geração, atlas V1 e ZIP V1 permaneceram idênticos.
- 26 imagens da bíblia visual passaram a usar caminhos internos. 25 já tinham cópias locais idênticas por hash; uma imagem de Andre sentado foi copiada para `02_references/andre/synthetic/R2-andre-seated-conversational.jpg`.
- 12 candidatos R2 foram registrados com checksums e `approved: false`, sem inventar job, preço ou aceite. Os títulos de quatro traduções foram corrigidos para explicitar a revisão pendente; o texto traduzido foi preservado.
- O rascunho `drafts/workflow-rehearsal` não herdou orçamento, duração, encontros, jobs, takes, progresso ou aprovação, e não alterou o filme ativo.
- A suíte de 10 testes cobre leitura sem mutação, coerência de estado, dependências, referências ausentes, alteração/perda/adição de arquivos, proteção de caminhos, recusa de sobrescrita, edições locais e divergência entre roteiro/CSV.

## Evidência

- [validation.json](validation.json): checagens dos arquivos reais e do ensaio.
- [tests.txt](tests.txt): resultado da suíte local.
- [lint.txt](lint.txt): verificações dos módulos de gestão e validação.
- [overwrite-refusal.json](overwrite-refusal.json): tentativa de reusar a pasta V2 recusada, sem alteração dos arquivos.
- [localized-bible-assets.json](localized-bible-assets.json): correspondência por hash entre os arquivos referenciados e as cópias locais.
- [originals-before.json](originals-before.json): hashes da entrega e dos originais anteriores.
- [file-index.json](file-index.json): inventário completo do escopo local; verificar com `scripts/workflow.py verify`.

As cópias `before/` guardam os arquivos anteriores às correções. Elas são histórico, não pontos de entrada atuais, e podem conter os antigos links externos.

## Ainda não validado

Semelhança de Andre em movimento, roupa/mesa finais, sincronização, interpretação das vozes, precisão dos idiomas históricos, revisão de cada candidato R2, custo de futuros lotes e masters completos. Os registros de geração/cobrança do R2 não foram verificados nesta etapa; copiar arquivos não comprova sua origem declarada. As fontes históricas 18 e 19 continuam sem snapshot local.

O método local de organização, edição, reconstrução e passagem está operacional. A aceitação artística e o fluxo audiovisual completo continuam dependendo das etapas de aprovação e do piloto.
