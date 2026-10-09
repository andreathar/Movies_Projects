# Dez frames de conversa — entrada e saída

Cinco pares criados com a ferramenta de imagens do ChatGPT: César, Gengis Khan, Galileu, Napoleão e Oppenheimer. Abra `index.html` para alternar personagens e comparar IN/OUT com o controle deslizante ou lado a lado.

Cada par propõe **um plano curto de aproximadamente cinco segundos**, com câmera fixa sobre o ombro do interlocutor. Não são os extremos de um capítulo inteiro de 42 segundos e não substituem a decupagem. As imagens são candidatas: não aprovam semelhança, figurino, continuidade histórica, animação ou uma nova despesa.

## Uso e continuidade

- IN: Andre escutando, mãos apoiadas na mesa. OUT: gesto/expressão posterior na mesma composição; Oppenheimer termina em quietude, sem gesto elevado.
- Usar a imagem OUT somente como referência de término se a rota de vídeo escolhida declarar suporte; esta entrega não consultou nem validou essa capacidade do Kling. Se houver somente imagem inicial, o OUT funciona como referência visual de movimento e revisão.
- Não dissolver rostos ou simplesmente interpolar estes PNGs e chamar o resultado de vídeo validado. A passagem precisa de teste de identidade, mãos, cenário e enquadramento em movimento.
- Os arquivos nativos são RGB PNG de 1672 × 941, aproximadamente 16:9, sem recorte, redimensionamento ou upscale. Não são 1920 × 1080 nativos.
- O rosto real foi condicionado pelas fotos aprovadas e por um frame de composição comum. Isso não criou um avatar treinado permanente. Andre ainda deve avaliar o próprio rosto em cada par.
- As imagens não contêm tipografia de pôster. O personagem histórico aparece por ombro, manga e mão; cabeça inteira fora de quadro. Um vídeo derivado precisa continuar respeitando a regra em todos os frames.

## Arquivo e proveniência

`manifest.json` identifica pares, arquivos, dimensões, hashes, limites e avaliações; `prompts.json` e `requests/` preservam os textos exatos e os hashes das referências. Caminhos de referência são relativos à raiz do filme. `generation-records.json` registra apenas resultados reais retornados; o nome do modelo e a cobrança da ferramenta embutida não foram expostos.

Foram 11 chamadas da ferramenta embutida: dez imagens entregues e uma correção de cenário de César. O rascunho anterior está em `rejected/`; não é candidato de uso. Nenhum job de Kling ou ElevenLabs, recarga, compra, vídeo, voz, publicação ou commit foi feito nesta entrega.

As fotografias e as referências anteriores foram preservadas. `CHARACTER_REVIEW.md` registra diferenças entre os materiais consultados. Esta pasta é uma proposta independente; o produtor decide sua integração ao storyboard e ao manifesto canônico sem apagar o trabalho dos demais agentes.
