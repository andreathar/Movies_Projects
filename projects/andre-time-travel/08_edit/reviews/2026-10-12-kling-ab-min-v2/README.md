# Investigação v3_0 e segundo teste Turbo — 12/10/2026

**Dois jobs concluídos, nenhum retry, 51 créditos declarados (27 + 24). Sem aceite artístico.** A nova autorização limita o único Turbo a 300 créditos, separadamente dos 27 já pagos. A cotação consumer de 24 foi conferida na interface oficial autenticada com a mesma imagem, prompt, 3 s, 720p, uma saída. Nenhum login iniciado. A CLI foi o único canal de submissão; upload anterior reutilizado. Não há terceiro job autorizado.

## Primeiro vídeo: piscadas e áudio

Inspeção dos 73 recortes numerados dos olhos confirma cinco ciclos, contra `he blinks once naturally`. A 24 fps, intervalos aproximados (início do fechamento → reabertura, ±1 quadro):

| Evento | Quadros | Segundos |
|---|---|---|
| 1 | 5–10 | 0,208–0,417 |
| 2 | 21–25 | 0,875–1,042 |
| 3 | 44–49 | 1,833–2,042 |
| 4 | 53–58 | 2,208–2,417 |
| 5 | 61–66 | 2,542–2,750 |

Três ciclos concentram-se nos últimos 0,92 s desse conjunto. Não se infere causa médica nem taxa geral do modelo. O relato do usuário, às 05:26 UTC, confirmou piscadas excessivas e “nada no audio”. A revisão anterior tinha faixas aproximadas; esta usa recortes numerados para delimitá-las melhor.

A faixa AAC existe, tem 44,1 kHz e dois canais idênticos; 134.144 amostras decodificadas por canal (~3,0418 s), todas não nulas. RMS −55,38 dBFS; pico −33,51 dBFS. `silencedetect`, limiar −40 dBFS e duração mínima 0,10 s: 95,56% do tempo detectado abaixo do limiar. A −35 dBFS: ~99,92%; a −60 dBFS: nenhum intervalo de 0,10 s. São critérios técnicos escolhidos, não limites universais de audibilidade. Somar para mono conserva o nível, portanto não há cancelamento entre canais.

**Não é silêncio digital absoluto; é uma trilha de sinal muito baixo.** “Nada audível” é o relato do usuário. O agente não realizou escuta semântica nem playback integral em velocidade normal. Ausência de fala/música era pedida: `No speech or music; subtle quiet room ambience only if audio is generated.` Portanto este não era um teste positivo de fala nem de som destacado. `enable_audio=true` entregou AAC e custo total declarado de 27; isso não prova ambiente útil, nem identifica uma cobrança indevida ou uma taxa separada de áudio. Original não normalizado, amplificado ou alterado.

## Turbo e comparação limitada

Original `07_generations/originals/AB-MIN-01-turbo-3s-720p_1.mp4`; SHA-256 `15b7b004e70444d2d85cbc5f8e3b8363a86485629515eedb9ad2b2cc4a66d968`, 1.802.051 bytes. H.264 1276×720, 24 fps, 73 quadros, 3,041995 s; AAC estéreo 44,1 kHz. Decode completo sem erros.

As sete folhas cobrem todos os quadros. Vi dois ciclos de piscar (~5–10 e 61–66), boca aparentemente fechada e uma forma estreita desfocada na extrema direita perto do fim. Não observei segundo rosto completo. A melhora de cinco para duas piscadas descreve estas amostras; o Turbo ainda não cumpriu “uma vez”. Nenhum vencedor geral ou aceite de identidade foi estabelecido.

Áudio Turbo: canais idênticos, RMS −60,46 dBFS, pico −43,81 dBFS; 100% abaixo de −40 dBFS. Há sinal não nulo, mas ainda mais baixo. Sem escuta própria. O Turbo não expõe `enable_audio` nem `prefer_multi_shots` no schema observado, portanto o A/B não controla essas variáveis da mesma forma.

## Melhorias de template — propostas não geradas

- Separar intenção visual de teste sonoro. Para imagem de escuta sem som necessário, escolher áudio desligado somente quando o modelo/schema permitir e a tarifa for conferida. Para testar áudio, pedir um evento sonoro reconhecível e avaliá-lo por ouvido; track AAC não é critério de sucesso.
- Trocar o inventário de microgestos por uma intenção de atuação: ouvir atentamente com olhar assentado, lábios em repouso e respiração suave. Não impor imobilidade total. Omitir contagem de piscadas é hipótese para um futuro prompt, não correção comprovada.
- Descrever a borda direita como espaço vazio pode ser mais direto do que introduzir a ideia de uma pessoa entrando. Uma amostra não prova que a formulação anterior causou a intrusão.
- Conservar prompt e imagem nos dois jobs já executados. Rascunho futuro em `template-proposals.json`, sem alteração retroativa do payload enviado. Inglês preserva a comparação; não é requisito demonstrado da API.

Detalhes: `blink-analysis.json`, `audio-analysis.json`, `v3-review.json`, `turbo/review.json`, `turbo-price-evidence.json`. Métricas do primeiro vídeo e relato humano são fontes separadas. Revisões v1 e originais ficam preservados. Próximo responsável: produtor/Andre para playback com escuta e decisão artística; nenhuma repetição automática.
