# 05 · Elements: personagem, objeto e voz reutilizáveis

Element = sujeito salvo na conta Kling (imagens ou vídeo, mais voz opcional). É o mecanismo oficial de consistência [OFICIAL]. No projeto, o Andre é o Element **323525046658711** (nome de ligação `Andre`).

## Onde um Element funciona [LIVE + OFICIAL]

| Ferramenta · modelo | Elements de imagem | Elements de vídeo |
|---|---|---|
| `text_to_image`, `text_to_video` (todos) | **não** | **não** |
| `image_to_image` · modelos que listam `elements` (`kling-image-o1`, `v3_0_omni`, `v3_0`) | sim | **não** |
| `image_to_video` · `kling-video-v3_0`, `v3_0_omni`, `o1` | sim | só `v3_0` e `v3_0_omni` |
| `image_to_video` · `v3_0_turbo`, `v2_5`, `v2_6` | não | não |
| `motion_control` · `kling-video-v3_0` | sim (declara `elements`) | não confirmado |
| `omni_ref_video` · `v3_0_omni` | até 7 | até 3 (1 se também há `video_1`); `voiceConsistency: true` |
| `omni_ref_video` · `kling-video-o1` | até 7 | não |

Se a ficha do modelo não tem o argumento `elements`, não passe. O preflight acusa.

## Ligar um Element

```bash
--elements '[{"id":"323525046658711","bindName":"Andre"}]'
```

e no prompt, o marcador exato `<<<323525046658711>>>`, uma ou mais vezes. Sem marcador, o preflight dá `ELEMENT_MARKER`. Sem `elements`, `<<<id>>>` dá `ELEMENT_NOBIND`.
Não descarte o ID para usar só a imagem de capa: a ferramenta instrui a passar o ID e, se quiser, a capa como auxiliar [OFICIAL].

## Criar [NÃO TESTADO por mim; só o producer, com ok]

```bash
kling element_create --name "Table J26-2" --description "oak table, pale wide planks, faint ring stain, chipped near one corner" \
  --tag Items --cover ./cover.jpg --secondary ./angle1.jpg --secondary ./angle2.jpg
```

Regras [OFICIAL, descrição de `element_create`]:

- **Imagem**: 1 capa + 1 a 3 secundárias. **Vídeo**: um único vídeo (3 a 60 s, > 23,8 fps, lado menor ≥ 700 px, ≤ 3840×2160, sem HDR, SAR vazio/1:1/0:1). Não misture.
- **Voz** opcional: arquivo `.mp3` do usuário. É assim que a voz do Andre ficou presa ao Element (D13).
- **Tag** obrigatória, uma ou mais de: `Characters`, `Animals`, `Items`, `Costumes`, `Scenes`, `Effects`, `Others`.

## Atualizar e apagar

- `element_update` **sobrescreve tudo**: campo omitido ou vazio é apagado. Sempre `element_get` primeiro e reenvie o payload completo. O CLI faz isso e preserva a capa.
- **A capa não pode ser trocada** depois de criada (o servidor rejeita). Capa nova = criar outro Element (e só apagar o antigo com confirmação explícita; no projeto, Elements legados não se movem nem se apagam).
- Secundárias: a lista inteira é substituída, de 1 a 3. Para "adicionar" a uma lista já com 3, é preciso retirar uma. Mostre a lista atual ao producer antes.
- `element_delete`: só com confirmação explícita do usuário.

## Ideias para este filme [INFERÊNCIA, NÃO TESTADO]

- **Element de objeto para a mesa** (`Items`): J26-2 é o fio condutor (mancha de anel = chave do match-cut, D04). Um Element com 3 ângulos pode estabilizar a mesa entre cenas. Teste primeiro com 1 still barata.
- **Element de figurino** (`Costumes`) para insertos abaixo do pescoço de cada figura histórica. Sem rosto na capa.
- **Figuras históricas**: nenhum Element com rosto completo (regra do projeto).
- Cota por plano: a tabela de planos de um guia de terceiros diz 500 Elements para Ultra [TERCEIROS, 2026-05-21]; confirme `element_list`.

## Problemas conhecidos

- Em `image_to_image`, Element de **vídeo** é recusado (a ferramenta manda usar `image_to_video` v3_0/v3_0_omni).
- Com `kling-image-v3_0_omni` o Element derivou 2/2 no teste do Andre [PROJETO]; por isso a rota é `kling-image-o1`.
- Marcador de imagem do prompt é `图片N` literal (não traduzir) [PROJETO]; marcador de Element é `<<<id>>>`.
