# Kling — Elements, nomes e referências: lições de 15/10/2026

STATUS: PROPOSTA DE MÉTODO. Exemplos arquivados, sem aprovação de produção. [Galeria e evidências](../07_generations/downloads/2026-10-15-element-experiments-v1/index.html) · [catálogo completo](../07_generations/downloads/2026-10-15-element-experiments-v1/manifest.json).

## O que os exemplos mostram

| Exemplo / asset ID | Observação própria nas amostras | Regra prática proposta |
|---|---|---|
| `KEXP-W323866270650569-result` | Três personagens distintos; mesa com anel; olhares variam entre parceiros e câmera. | Nomear cada participante e escrever quem olha para quem, em qual momento. |
| `KEXP-W323868230505094-result` | Roupa cinza, café e efeito cósmico aparecem; as duas mulheres do `Video1` desaparecem das cinco amostras. | Em edição, especificar mudança e preservação: elenco, posições, mesa, enquadramento e movimento. O teste muda roupa, cenário e efeito juntos, portanto não mede cada causa isoladamente. |
| `KEXP-W323869015528491-result` | Neve, café e três personagens aparecem; mesa fica baixa/pequena e elenco se ajoelha; o plano termina mais próximo. | Uma referência de objeto não fixa tamanho, altura nem assentos. Definir geometria e comportamento de câmera. |
| `KEXP-E323980733525179-*` e `KEXP-E324018220506771-video` | Novo conjunto de cabelo mais longo, barba e camisa preta, com vistas complementares; vídeo dividido em corpo inteiro + retrato. | Versionar esse visual como experimento separado. Não aplicar ao filme o nome ou a aprovação de outro conjunto. O vídeo composto não é uma demonstração de tomada única limpa. |
| `KEXP-E323867570654831-*` | Secundárias de roupa incluem rostos de outra representação. | Futuras referências de figurino devem destacar roupa e detalhes sem introduzir uma segunda identidade facial; qualquer recorte/criação será outra tarefa autorizada. |

Isso é inspeção de 22 imagens e cinco quadros de cada vídeo, com decode integral; não é revisão temporal completa nem escuta. Andre disse que criar e nomear referências é uma estratégia de sucesso; não forneceu julgamento individual de aceite destes takes. Não atribuir a ele as observações desta tabela.

## Identidades e nomes sem perder a ligação técnica

Manter quatro campos diferentes: `asset_id` local estável, `elementId` retornado pelo provedor, `originalName` literal e `aliasProposto` legível. Renomear arquivo local não muda Element nem reescreve prompts anteriores. Nenhum Element foi renomeado nesta entrega.

| Element ID | originalName, preservado | aliasProposto para futuras versões |
|---|---|---|
| `323980733525179` | `Andre_Athar_Element` | `AA-ID-20261014-v01` |
| `324018220506771` | `Andre Athar_vr` | `AA-VIDREF-v01` |
| `323867570654831` | `Costume 1` | `WD-GREYTIE-v01` |
| `323854711683871` | `table 1` | `TB-J26ALT4-v01` |

Os aliases sugeridos têm até 20 caracteres, são distintos por função e não foram enviados à conta. Não usar `approved`, `canon` ou nome de um personagem histórico como atalho de aprovação. Ângulos em arquivos podem usar `front`, `sideHalf`, `closeUp`, `backWhole`; conservar também os nomes originais retornados por `resource.secondary[].name`.

`Andre Athar`, usado nos três vídeos de 13/10, tem ID não exposto e previews de cabelo curto/paletó escuro. Ele não pode ser substituído silenciosamente por `Andre_Athar_Element` ou `Andre Athar_vr`. Conservar literalmente `Blonde Lady`, `Sarah`, `Zen-style Café`, `Snowflake`, `Stellar Black Hole`, `Costume 1`, `table 1` e o slot `Video1` no arquivo histórico.

O nome `table 1` não significa mesa aprovada: sua capa tem o hash de `R1-J26-table-anchor_4_alt`; D04 escolhe `_2`. A capa de `Costume 1` é idêntica ao original sintético `R1-J25-costume-oppenheimer_1.png`. Os metadados originais e prompts desses dois arquivos estão ligados no catálogo; as restrições de uso e aprovações anteriores continuam válidas.

## O que foi verificado na documentação oficial

A [Element Library](https://kling.ai/quickstart/klingai-element-library-3-user-guide) descreve Elements de imagem com uma referência principal e 1–3 complementares, recomenda vista frontal principal e vistas/detalhes complementares, e usa `@` para chamar referências no app. Separa personagens, figurinos, objetos, cenas e efeitos; nomear um recurso não equivale a vinculá-lo tecnicamente.

O [guia VIDEO 3.0](https://kling.ai/quickstart/klingai-video-3-model-user-guide) distingue referência de Element e quadro inicial/final e documenta o controle Multi-Shot. Portanto, nem o segundo recurso é automaticamente OUT, nem a tela atual do compositor prova o ajuste usado num teste anterior.

Na CLI instalada 0.2.1, o `tool_list` consultado em 15/10 exige binding de Elements e marcador `<<<id>>>`; o modelo deve declarar compatibilidade. Guardar os marcadores literais `<<<id>>>`, `图片N`, `Video1` e nomes de slots quando existirem na fonte. O histórico web expôs chips, não a serialização original: `[@nome]` nos exemplos locais é apenas notação legível e não um payload pronto para CLI.

O plugin instalado prescreve CLI 0.2.0; o projeto prescreve preservar a CLI global 0.2.1 existente e não atualizar durante o trabalho. Foi usada a instalação existente; nenhuma instalação/downgrade. A capacidade efetiva foi consultada ao vivo. Catálogo de modelos não prova settings passados nem custo.

## Templates para preparar um pedido futuro

Rascunhos somente; preencher IDs reais, compatibilidade, inputs e escopo financeiro antes de qualquer submissão.

**Referências por função:**

```json
{
  "identity": {"asset_id": "<ID local>", "elementId": "<ID real>", "originalName": "<literal>", "sha256": "<hash>"},
  "costume": {"asset_id": "<ID local>", "elementId": "<ID real>", "originalName": "<literal>"},
  "prop": {"asset_id": "<mesa exata>", "version": "<versão>"},
  "scene": {"asset_id": "<ambiente>"},
  "editSource": {"asset_id": "<vídeo exato>", "slot": "Video1"},
  "preserve": ["cast", "identity", "seating", "table geometry", "camera", "timing"],
  "changeOnly": ["<uma alteração mensurável>"],
  "approval": false
}
```

**Edição de figurino — notação do app:**

```text
In [@Video1], change only the clothes worn by [@PERSON] to [@COSTUME].
Keep the same three people, their identities, the seated positions,
table dimensions and height, room, camera framing, motion and timing.
Do not remove or replace either companion. Keep all other clothing unchanged.
```

Testar a roupa separadamente antes de acrescentar ambiente e efeito torna a comparação interpretável. Esses critérios ainda precisam ser demonstrados em outro resultado; não foram executados aqui.

**CLI — binding simbólico a validar, não enviar:**

```text
elements = [{"id":"<ID real do personagem>","bindName":"<nome literal>"},
            {"id":"<ID real do figurino>","bindName":"<nome literal>"}]
prompt = "<<<ID real do personagem>>> wears <<<ID real do figurino>>> ..."
```

As reticências e placeholders tornam isso deliberadamente não executável. O CLI/live schema define ferramenta, modelo, slots e limites. O prompt histórico não deve ser convertido para esses tokens supondo IDs ausentes.

Para o filme, aplicar o método às referências já escolhidas, mantendo identidade `323525046658711`, D02, D04, eixo e as aprovações G-IN/G-OUT. Não incorporar estes exemplos pessoais como figurino, rosto, mesa ou composição da produção. A revisão técnica `v2-reconciliation` continua pendente e não foi ingerida.

## Registro mínimo por próximo teste

Salvar antes do envio: prompt exato, bindings/slots ordenados, nomes originais, hashes/versões e parâmetros explícitos. Depois: `generationId` real, índice do work conforme resposta, bytes/hashes, cobrança declarada e observação por arquivo/tempo. Campos desconhecidos ficam `null` com motivo. Aprovação de semelhança, roupa, composição e voz permanece separada.

Próximo responsável: produtor desktop revisa o catálogo e combina com Andre quais itens recém-aparecidos entram no próximo lote. Bloqueio concreto: faltam IDs/originais das referências antigas de biblioteca e pedidos originais dos três testes web. O lote seguinte não foi iniciado nem autorizado a gerar mídia.
