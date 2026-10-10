# Revisão independente — historical-details-v1

**Parecer: requer correções pontuais antes de servir como especificação factual de novas imagens ou foley.** As cinco fichas e quatro notas estão presentes. O material distingue diversas lacunas e preserva escolhas da produção; os achados abaixo tratam dos pontos em que essa cautela se perde. Esta revisão não aprova mídia, figurino, interpretação ou montagem.

Entrada: entrega FINAL da mensagem Parley **30**, que substitui o aviso parcial 23. Ficha na faixa **Claude, somente leitura**, caminho relativo `projects/andre-time-travel/03_bibles/detail-planning/historical-details-v1.md`, SHA-256 `037acbf25d39538717f262d8b0543887bbdd4fdfd4cbdb086a220537f5886341`. Linhas abaixo referem-se exclusivamente a essa versão. Relatório Parley associado: `2c4fc95cdbee414e`; sua parte de consolidação de workflow **não foi revisada**.

## Achados e correções necessárias

**H01 — Alta: piso de Arcetri, linhas 54 e 127.** A tabela admite que a terracota vem de um resumo de busca turístico, associado a uma sala de visitas de 1639 em diante. A recomendação posteriormente chama isso de piso original factual. A [página institucional do Museo Galileo](https://brunelleschi.imss.fi.it/itineraries/place/villagioiello.html), reconferida, não documenta esse piso em 1634. Manter o material da sala do encontro como **não documentado**; terracota e tábuas podem ser escolhas de arte identificadas como tais. O indício não sustenta sozinho exigir mudança de plate ou definir o timbre de G-F2.

**H02 — Alta: geometria de Longwood, linhas 364–365.** A ficha atribui 14×12 pés ao quarto de O'Meara, mas recomenda aplicar essas medidas ao estudo para substituir as de Las Cases, suspeitas de transcrição. A [edição digital de Las Cases, volume II](https://www.gutenberg.org/files/53968/53968-h/53968-h.htm) realmente apresenta 45×42 pés para duas câmaras A/B. A suspeita de erro não identifica uma medida correta, e quarto/estudo não são intercambiáveis sem conferir a planta. Identificar ambiente e data nas fontes e consultar o fac-símile antes de fixar medidas. Até lá, dimensão desconhecida; não corrigir números por plausibilidade. Afeta distâncias de câmera, mesa e espaço sob ela.

**H03 — Média: proveniência do retrato de Galileu, linhas 77–79.** A classificação conjunta como imagem de 1635/c.1640 encobre a data de BHC2701. O [catálogo do Royal Museums Greenwich](https://www.rmg.co.uk/collections/objects/rmgc-object-14175) identifica uma cópia de Cecconi de **1879**, baseada no original de Sustermans de **1636**. A própria lista G6 da ficha já registra a cópia: harmonizar a tabela com ela, distinguindo original, cópia e o outro retrato c.1640. O uso como referência iconográfica continua possível; não é observação direta do figurino de 1634.

**H04 — Média: calçado de Napoleão, linhas 350, 355 e 357.** Las Cases fornece um hábito de abril, enquanto a ficha marca como desconhecido o calçado de outubro–novembro. A recomendação “nunca bota” transforma um relato situado numa proibição absoluta. Manter sapatos como recomendação sustentada naquele hábito, sem apresentar a ausência de botas como fato de todo interior/data. Nenhuma variante fica aprovada por este parecer.

**H05 — Média: descrição visual do casaco, linha 427.** Na inspeção da imagem `R2-wardrobe-napoleon-uniform.jpg` em resolução original, há desgaste claro nas bordas e punhos. A descrição “novo, não gasto” não corresponde ao que se vê. Corrigir o inventário visual e separar esse desgaste dos conflitos documentais de botões e debrum. A vista frontal também não estabelece, sozinha, se a peça foi virada do avesso. SHA-256 da imagem: `a805454c3e1f3253ae25489c6d53094bfb275065f6587c42f4476caf82df5be0`.

**H06 — Média: rastreabilidade do handoff.** Os quatro registros de `baseFiles` trazem caminhos/papéis sem hashes, e `pendingDecisions` contém apenas escolhas de Galileu, embora o corpo apresente pendências nos cinco encontros. Incluir versão/checkout dos insumos e a lista completa de pendências para o produtor. Se o hash de início não foi registrado, declarar a lacuna; um hash calculado agora não prova qual base foi lida no início. Não alterar arquivos canônicos para resolver essas pendências.

## Conferências que ajudam a produção

| Encontro | Conferência e limite | Consequência para cobertura e foley |
|---|---|---|
| César | [Suetônio 45.3/46.1](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Suetonius/12Caesars/Julius*.html) sustenta o relato das mangas até os pulsos e da residência oficial na Via Sacra. Não prova ausência de outras propriedades. A referência visual conferida tem manga curta e broche. | Variantes de manga, broche e calçado precisam de seleção explícita; não acrescentar metais ao som por costume genérico. |
| Gengis Khan | Localizada a passagem que o handoff não reencontrara: [Rubruck](https://depts.washington.edu/silkroad/texts/rubruck.html) descreve a festa de Möngke em 7/6/1254. Confirmar o texto não o transforma em testemunho de Gengis em 1227. | Armadura, anéis e materiais de K-CO/K-MA seguem condicionais; nenhum tilintar presumido. |
| Galileu | Piso e calçado exatos continuam não documentados; ver H01/H03. | G-PE/G-F2 não têm material acústico fixado. Mesa/assento precisam permanecer coerentes com D04/D09 e a futura imagem do produtor. |
| Napoleão | Las Cases menciona tapete; o [plano apresentado pela Fondation Napoléon](https://www.napoleon.org/en/history-of-the-two-empires/images/habitation-of-the-emperor-napoleon-at-the-isle-of-st-helena-as-it-was-towards-the-end-of-1816) descreve umidade e tábuas. Tábuas estruturais não significam automaticamente piso aparente em todo cômodo. | Escolher o ambiente antes de resolver tapete/piso, N-PE/N-F2 e distâncias de ombro. H02/H04/H05 devem acompanhar a escolha. |
| Oppenheimer | O [NPS](https://www.nps.gov/articles/000/the-life-of-j-robert-oppenheimer-the-manhattan-project-years-1941-to-1946.htm) descreve roupa de trabalho em Los Alamos, sem estabelecer o traje da noite de 15/7/1945. A própria ficha mantém essa lacuna. | Tweed, relógio e objetos não recebem validação histórica para essa noite. Não criar ação/foley de acessório ausente da encenação escolhida. |

As descrições das duas instituições modernas são resumos institucionais; não foram reclassificadas como testemunhos de época. Os relatos antigos foram consultados em edições/traduções digitais, sem colação integral dos originais.

## Escopo e passagem de bastão

Leitura integral da ficha principal; conferência de hashes das quatro notas e inspeção seletiva de suas fontes, sem auditoria completa de toda a bibliografia. Os **16 hashes de imagens** coincidem com os informados. **Seis imagens** foram inspecionadas visualmente: plate de Galileu, roupas de César/Gengis/Oppenheimer e plate/roupa de Napoleão. Conferir hash não equivale a inspecionar ou aceitar imagem.

O [registro de evidências](historical-review-evidence.json) guarda os 33 insumos da linha de base, os 16 hashes de imagem, fontes e limites. O [handoff da revisão](../../../agents/handoffs/2026-10-09-editor-historical-details-review-v1.json) registra verificações e próximos responsáveis.

Entregar H01–H06 ao produtor e à faixa de pesquisa para correção delimitada. O produtor decide a integração e encaminha a Andre as escolhas que lhe cabem. Esta faixa não assume produção, não corrige a ficha alheia e não gera imagens. `coverage-plan.md`, `foley-cues.md`, Galileo v2 e registros canônicos permanecem preservados. D17–D19 continuam propostas; a escolha de olhos de 2 s continua restrita à edição de Galileu já entregue.

