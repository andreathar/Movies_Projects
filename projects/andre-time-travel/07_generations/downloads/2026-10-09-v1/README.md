# Arquivo local de imagens Kling

Conferência concluída em 09/10/2026 11:08:46 -03.

- **90 imagens de 73 trabalhos** registrados neste filme.
- **1 imagem baixada neste passe**: `R1-J01-andre-master-sheet`, resultado 2, PNG de 2752 × 1536.
- **89 imagens já estavam locais**, vinculadas aos respectivos IDs e resultados.
- **72 trabalhos confirmados por consulta atual ao CLI**. O trabalho antigo `R3-galileo-speaking` retornou erro (exit 1, status 400); sua imagem local foi validada por decodificação e SHA-256, sem repetir a consulta.
- 90 imagens decodificadas, 90 pares únicos de ID/índice, 273 links locais conferidos. Os 90 arquivos de mídia existentes na área de gerações antes da operação permaneceram byte a byte intactos.
- 13 resultados estão em rejeitados/quarentena e ficam ocultos inicialmente na galeria. Arquivar não aprova uso criativo.

## Acesso

Abrir `index.html` para a galeria; `images.csv` para edição/consulta tabular; `manifest.json` para IDs, índice do resultado, resolução, hashes, caminhos relativos ao workspace e ressalvas. `SHA256SUMS.txt` usa caminhos relativos à raiz do projeto.

Os arquivos existentes mantêm sua organização em `07_generations/originals/`, `_quarantine-full-face/` e `07_generations/rejected/`. A imagem recuperada fica em `07_generations/originals/download-2026-10-09-v1/`. A galeria aponta para esses arquivos, sem duplicá-los.

## Escopo e repetição

Este arquivo cobre os IDs presentes nos registros do filme no instante `scopeCutoff` do manifesto. O CLI instalado não oferece listagem geral de todo o histórico da conta: gerações feitas fora deste projeto, sem IDs locais, não estão comprovadamente incluídas. Gerações posteriores precisam de novo snapshot.

A consulta de status foi feita exclusivamente pelo CLI instalado. Somente o URL de mídia primário retornado pelo CLI foi usado no download faltante. Nenhum token, cookie ou URL temporário de resultado foi salvo nestes novos registros. Nenhum job pago, upload, compra, commit ou publicação foi realizado por este passe.

Para uma próxima coleta, usar `python3 scripts/archive_kling_images.py --snapshot NOME-NOVO`. O utilitário usa o Python com Pillow documentado para renderização, consulta cada ID uma vez, preserva arquivos locais, recusa sobrescrita de snapshots e para ao primeiro erro. Não cria gerações nem tenta novamente jobs com falha. Esta execução registrou separadamente a falha de consulta antiga e prosseguiu apenas com IDs ainda não consultados.

A validação do workspace passou. A suíte geral apresentou uma falha no fixture de `test_manage`: a cópia de teste exclui a imagem JPG que a tarefa T02 agora declara como entrega concluída. O arquivo real está presente; isso não é uma falha dos downloads. Detalhes em `verification.json`.
