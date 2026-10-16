# Entrega Kling 4, 2026-10-16

Implementado em main, sem commit. CLI Global instalada 0.2.1 / Node 24.18.0. Descoberta autenticada who_am_i e tool_list confirmaram o ID real kling-video-v4_0 em três ferramentas; sem geração testada. Plan.md registra inventário e ordem de migração; inventory.json mapeia 498 fontes relacionadas. Preservados media/originais, prompts históricos, snapshots 12/10, IDs/proveniência e decisões G-IN/G-OUT.

## Mudanças
- Contrato canônico separa provider, interface, versão do cliente, catálogo da conta, anúncio e geração testada. Rotas live limitam V4 a 720p/1080p. Publicação full-model, 4K/HDR/extensões, Flash e preço não viram flags ou acesso presumido.
- V4 keyframes não declara Element/áudio; Omni exige multi-shot=true. V3 continua disponível por escolha explícita, sem fallback silencioso nem remoção de referências.
- F8/F9 e shotContract v1 bloqueados até resolver referências tipadas, hashes/proveniência/uso e evidências, Element ID/type/resources, beats, companions/figurino/mesa/eixo, diálogo medido e estratégia de áudio. Não alterados F1–F7. Identidade não é inferida da aprovação de composição.
- Preflight V4 liga live who_am_i e tool_list ao schemaSha256, exige Element corrente equivalente ao snapshot de referência, aplica limites combinados e mede vídeo/áudio local. Metadados ficam fora das flags; contrato integra o payload hash, invalidando liberações anteriores. Som de fonte exige stream de áudio; vídeo mudo não fornece voz. Native guide/idioma/sync/voz final têm gates distintos.
- Custos continuam desconhecidos até cotação por payload. Vídeos diretos + video Elements somam até 30 s e sua duração entra na cobrança; saldo não vira cobrança por job. Nenhum orçamento antigo reutilizado.
- Dez briefs, skills locais, registros, sete derivados inativos, manual e playbook ativo atualizados. Frontend Organização agora mostra modelo listado, limites por rota, preço desconhecido e escopos de aprovação. Exportadores/snapshots sincronizados; galeria continua HTML canônico com cartão path-only.

## Validação real versus sintética
Live: apenas CLI who_am_i/tool_list. Local: build de produção, lint, TypeScript, check:data, ambos exportadores --check, catálogo --check, workspace validate, plano --verify-media e assets validate. Testes sintéticos: 243 Python, 16 ferramentas do manual e 87 frontend; 18 regressões V4 dentro da suíte Python. Nenhum teste pago/upload ou job. 24 hashes de mídia dos arquivos v1/v2 reconferidos. Logs e códigos reais em test-results.json/checks; todos passaram. Uma falha intencional impressa por fixture do gate pertence ao teste negativo; resultado final da suíte foi OK.

## Pendências preservadas
Revisão do produtor dos handoffs 15/10 continua pendente; nenhuma ingestão. G-IN/G-OUT aprovados para composição, cinco refs pendentes. Table 1 aponta a _4_alt, D04 aprova _2. Figurino perdeu companheiros em testes. Fight sem áudio e ProduceID divergente; prompts/settings/oponente exigem histórico autenticado. Não houve reprodução/escuta humana, aprovação artística, idioma/voz/sync ou teste de qualidade V4. Preços/FPS/Flash seguem desconhecidos. Três warnings prévios de hashes de skills externas persistem, sem copiar/editar fontes globais.

## Próximo dono
Produtor desktop revisa a mudança e as pendências históricas, escolhe por plano a rota e as referências exatas. Um teste futuro precisa de cotação, scope/release e autorização própria. Rollback restrito em rollback.md, backups das fontes e hashes finais em preservation.json. Nenhum serviço reiniciado, commit, publicação ou gasto.
