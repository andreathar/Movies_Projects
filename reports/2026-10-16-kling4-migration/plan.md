# Migração Kling 4 — plano e inventário, 2026-10-16

Escopo autorizado: auditar e refatorar fontes, templates, agentes, skills, adaptador, custos, frontend e verificações. Sem geração paga, uploads, criação/alteração de Elements, login/grants, reinício de serviços, commit ou publicação. Responsável por integração/aceite: produtor desktop. Filme: The Table Between Centuries (`andre-time-travel`).

## Estado inicial
Base main 629c23d; somente submódulo frontend já sujo. Inventário inicial de hashes preservado em base-hashes.json. Handoffs de 15/10 v3 de controles e v2 de experimentos seguem pending_producer_review / ingest pending. Parley: serviço not ready, projeto dormant, duas lanes stopped/dead, zero reservas e zero issues; nenhuma lane reiniciada/assumida. Esta tarefa trabalha na base, sem atribuir identidade de lane.

CLI instalado @klingai/cli-global 0.2.1, Node 24.18.0. who_am_i/tool_list autenticados em 16/10 retornaram sucesso, MCP 1.3.3. `kling-video-v4_0` listado em image_to_video/text_to_video/omni_ref_video; nenhum teste de geração. Plugin externo fixa CLI 0.2.0/skill 1.0.5, contrato distinto da adaptação local 0.2.1; não reinstalar/downgrade. Usado somente CLI já instalado, conforme AGENTS.md.

## Ordem de implementação
1. Preservar snapshots históricos; registrar descoberta sanitizada datada com provider/interface/versão e origem. Separar anúncio, catálogo da conta, teste de geração e aprovação.
2. Validar V4 de acordo com sua rota real: 3–30 s, 720p/1080p, até 10 imagens/keyframes; Omni até 15 recursos incluindo áudio/Elements e até 3 video Elements. Omni exige multi-shot=true; não substituir câmera fixa/V3 silenciosamente. Medir áudio/vídeo e contabilizar durações de entrada. Nunca converter tokens em caracteres.
3. Contrato de futuro pedido: referências tipadas e hash/proveniência/uso, Element inspecionado, beats temporais, continuidade de elenco/figurino/mesa, som/diálogo e gates por versão. Metadados locais não viram flags. Fingerprint inclui o novo contrato; liberação financeira antiga não é reutilizável.
4. Templates V4 bloqueados e dirigidos por rota; manter F1–F7 e pilotos legados. Atualizar skill local e briefs/registro; regenerar derivados sem ativação. Documentação ativa aponta à evidência atual sem reescrever prompts/outputs históricos.
5. Sincronizar frontend por exportadores: mostrar acesso listado, rotas/limites, preço desconhecido e aprovações distintas. Galeria existente continua canônica e path-only; servir mídia não integra este refactor.
6. Rodar testes sintéticos de runner/preflight/contrato, suíte Python/frontend, lint/types/build, check:data e exportadores/checks de plano/mídia. Registrar limitações e diffs/hash guards. Não ingerir entregas antigas.

## Dependências e pendências preservadas
G-IN/G-OUT são aprovados apenas para composição, cinco referências restantes pendentes. Element “table 1” usa _4_alt, D04 aprova _2: divergência impede novo uso equivalente. Edições de figurino perderam companheiros. Fight local sem áudio, ProduceID diferente da história; prompt/oponente/settings não reconstruídos. Histórico autenticado e reprodução/escuta humana permanecem necessários. Créditos e orçamento antigos são históricos; cotação atual por payload e liberação específica são necessárias.

## Fontes e limites
Anúncio oficial: https://kling.ai/blog/kling-4-ai-video-model (30/09/2026); página https://kling.ai/dev/model-release/kling-4 retorna somente shell nesta leitura. Higgsfield Cinema Studio 4.0 é outro provider/interface. Full-model publicado não prova CLI/conta: 4K anunciado, mas CLI atual não habilita; HDR e extensão de 2 minutos coming soon; FPS/preço/Flash não verificados. Qingque legado é guia 1.5 Custom Face, sem autoridade sobre 4.0.

## Rollback
Sem commit. Restaurar somente arquivos deste refactor usando os backups/hash iniciais da entrega, após conferir ausência de alterações concorrentes. Preservar submódulo sujo, registros canônicos e arquivos históricos. Novos templates/snapshots podem ser retirados sem alterar mídia. Produtor revisa handoff antes de integrar; nenhum resultado técnico aprova take, idioma ou gasto.
