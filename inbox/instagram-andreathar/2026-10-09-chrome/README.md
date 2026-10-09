# Acervo de fotografias — @andreathar

Conferência realizada em 9 de outubro de 2026, usando a sessão do Chrome indicada por Andre.

## Resultado verificado

- **353 publicações** encontradas na grade autenticada: **286 de fotos e 67 de vídeo**.
- **289 imagens de posts** disponíveis: 286 publicações, com dois slides adicionais no carrossel `B9W5JjKDL8l` e um adicional no carrossel `B1PcWyIDBe6`.
- **Uma foto de perfil**, catalogada separadamente: 290 imagens no total.
- As 290 imagens foram decodificadas integralmente e têm hashes diferentes. Não há imagem faltante no catálogo das publicações de fotos.
- Os dois carrosséis foram percorridos no navegador; o botão de próximo slide desapareceu após o terceiro e o segundo slide, respectivamente.
- Os 353 códigos de publicação, tipos e indicadores de carrossel do catálogo local coincidem com o inventário coletado no navegador.

Os arquivos de mídia foram produzidos por uma importação local concorrente em `inbox/andre-reference-photos/instagram-andreathar/`. Esta conferência não baixou nem duplicou essas mídias. O primeiro lote público menor, em `inbox/instagram-andreathar/2026-10-09-public/`, foi preservado como evidência histórica; ele não deve ser somado à contagem principal.

## Onde abrir e editar

- `index.html`: galeria local com filtro por ano, data ou código de publicação; clicar numa imagem abre o arquivo preservado.
- `photos.csv`: inventário editável das 290 imagens, com caminhos relativos ao workspace, dimensões, fontes e hashes.
- `manifest.json`: inventário completo, procedência, contagens e limites da verificação.
- `browser-verification.json`: evidência da conferência autenticada e dos carrosséis.
- `SHA256SUMS.txt`: hashes de todas as mídias da importação, com caminhos relativos à raiz do workspace.

Para reconstruir os derivados, executar `python3 scripts/catalog_instagram.py` na raiz do projeto. Esse utilitário usa Pillow, disponível no Python do sistema nesta máquina; a `.venv` mínima das ferramentas de gestão não contém Pillow. O utilitário só lê a mídia, recusa divergências do inventário observado e atualiza os derivados nesta pasta. Em futuras coletas, criar uma nova pasta de evidência antes de alterar o inventário esperado.

## Limites e continuidade

**A coleta das fotos publicadas na grade do perfil está completa para o inventário observado.** Isso não é uma exportação integral da conta: stories, destaques, posts arquivados, conteúdo marcado de terceiros e mensagens não foram incluídos.

São cópias servidas pelo Instagram, preservadas como recebidas; não são arquivos certificados de câmera. A palavra “originals” usada pelo catálogo da importação significa cópias sem edição local, não certificação de autenticidade. Nenhuma foto foi aprovada automaticamente como identidade de Andre ou referência de produção. Seleção, verificação visual de autenticidade e aprovação de semelhança continuam separadas.

A importação existente também contém **66 vídeos**, sem validação de reprodução neste passe. Um post de vídeo, `CMN4kGWlUYu`, está sem arquivo no catálogo original. Essa lacuna não afeta a cobertura das fotografias solicitadas.

Datas foram preservadas como registradas pelo catálogo da importação e podem diferir do dia mostrado pela interface em outro fuso horário. Nenhuma senha, cookie, código de verificação ou URL temporária de CDN foi incluída nestes novos registros. Nenhuma chamada paga foi feita por este passe.
