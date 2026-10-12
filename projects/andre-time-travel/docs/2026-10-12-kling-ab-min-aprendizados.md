# Adendo de investigação — v2

A revisão abaixo é histórica. O segundo e último job Turbo foi posteriormente autorizado até 300 créditos, cotado em 24 na UI e concluído por 24; total observado 51. Consulte `../08_edit/reviews/2026-10-12-kling-ab-min-v2/README.md` para piscadas, áudio, comparação e propostas de template. Sem aceite artístico.

# Receita e limites do ensaio mínimo Kling

Evidência desta revisão: `../08_edit/reviews/2026-10-12-kling-ab-min-v1/review.json`. Não é preset artístico aprovado nem conclusão comparativa entre modelos.

1. Para `kling-video-v3_0` nesta conta/schema, especificar `duration=3`, `resolution=720p`, `imageCount=1`, `enable_audio=true`, `prefer_multi_shots=false` foi aceito. Uma entrada `first_image`, nenhum Element. O job custou 27 créditos declarados. Conferir schema, tarifa e saldo novamente em novo escopo; não transformar este valor em cotação universal.
2. Turbo não expõe os mesmos controles de áudio/multishot/Elements no schema observado. Mesma imagem e mesmo texto não isolam todas as variáveis. Comparação futura é exploratória e requer explicitar diferenças, amostra mínima e incerteza, sem prometer silêncio por prompt.
3. “Uma piscada”, “boca fechada” e “ninguém entra” falharam neste take. Diminuir densidade de ações e revisar entrada fora de quadro são hipóteses de próximo prompt, não consertos testados. Evitar pôr o número de piscadas como garantia técnica. Não regenerar automaticamente.
4. Preflight/CLI íntegros verificam contrato e rastreabilidade; não garantem atuação, identidade, continuidade ou áudio correto. Conclusão de job não é aprovação de take. Metadata, decode, todos os quadros estáticos, playback com áudio, semelhança e aceite são evidências distintas.
5. A fonte tinha extensão .jpg e conteúdo PNG. Foi copiada byte a byte com extensão .png para envio; original preservado, hash idêntico. Validar assinatura/formato real sem sobrescrever o arquivo do usuário.
6. Um único upload foi reutilizável; houve um único envio e uma consulta de retomada. ID persistido antes do polling. Nunca executar de novo scripts “once” ou reusar o spec aprovado como novo job.
7. API UNITS não são créditos consumer sem conversão documentada. Não submeter para descobrir preço; Turbo parou antes do segundo job. Teto documental não é um max-cost implementado no servidor; jobs submetidos não podem ser cancelados conforme o guia MCP.

Prompt enviado em inglês para manter o texto controlado do ensaio; intenção em português: Andre escuta a pessoa fora do quadro à direita, pisca uma vez, respira suavemente e mantém boca fechada; câmera fixa, uma tomada, aparência/cenário preservados, ninguém entra, sem fala/música, ambiente discreto se houver áudio. O idioma inglês não é uma exigência de schema demonstrada nem correção de bug da CLI. O texto exato fica em `../07_generations/requests/AB-MIN-02-v3_0-3s-720p.prompt.txt`.

Fontes de preço/limite consultadas: [guia vídeo 3](https://kling.ai/quickstart/klingai-video-3-model-user-guide), [guia MCP](https://kling.ai/app/mcp/guide) e [nota API Turbo](https://kling.ai/document-api/apiReference/updateNotice?date=2026-02-11). A interface `https://kling.ai/app?designerRouteName=video` exibiu Sign In, portanto não verificou tarifa da conta e não houve login novo.
