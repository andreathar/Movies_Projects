# Galileo — pacote local G-L03/G-L04

**Candidato de pré-visualização · 16 s · sem gasto novo.** Fichas e referências estão na fonte canônica `05_storyboard/source/production-plan.json`; este pacote é derivado dela, não um segundo catálogo.

Abra `index.html` para revisar geometria, fichas, referências e vídeo, ou `animatic.mp4`. O render usa três imagens existentes e dois áudios-guia existentes, com faixa identificada como **voz-guia**. Não é vídeo de atuação, teste de sincronismo, voz final ou master. Os originais foram preservados. A reprodução/audição humana integral e o aceite permanecem pendentes.

G-L03 inicia em 0,5 s e dura 2,832 s; G-L04 inicia em 4,1 s e dura 8,616 s. A reação começa em 13,1 s, após a resposta inteira (fim em 12,716 s), para evitar F03. Sua duração de 2 s é uma proposta deste corte, não regra dos cinco encontros. As pausas são propostas; a voz não foi acelerada. Texto exato é lido do CSV inglês, sem nova fala. O áudio-guia de todos os 22 IDs foi medido novamente: total 120,792 s, sem transformar isso em duração final do filme.

As dimensões 120 × 75 × 75 cm, assentos 45 cm, câmera 117,5 cm e 50 mm são proposta D17. `geometry.svg` ilustra posição e eixo, não reconstrói medidas a partir das imagens. A cabeça histórica fica completamente fora; nuca não foi autorizada. O conjunto IN/OUT/olhos é candidato e não ganha aprovação por entrar neste animatic.

Próximo responsável: produtor desktop apresenta o pacote a Andre. Decisões concretas: composição/semelhança e ritmo; escolha de voz por ouvido; referência final para cada plano. Só depois preparar preço/teto por pedido. A disponibilidade de 66 vídeos de Andre no inventário não os qualifica como atuação: faltam triagem temporal, função e direitos por trecho. Novo upload/captura não foi feito.

Reconstrução local, sem rede: `python3 scripts/build_galileo_animatic.py --output projects/andre-time-travel/05_storyboard/animatics/galileo-g03-g04-v2` (nova pasta; não sobrescreve v1). Requer Pillow, ffmpeg/ffprobe já instalados. O builder verifica hashes de fontes antes de renderizar; renders não alteram aprovações.
