# Economia de contexto e coordenação

Política operacional solicitada por Andre em 2026-10-09. Aplica-se à conversa produtora e às lanes. Não altera permissões, aprovações, inspeção de mídia ou tarefas atribuídas. Não há economia percentual medida; regras abaixo são alvos de operação, não limites técnicos.

## 1. Uma fonte por assunto
STATE é entrada curta de retomada. Workflow guarda regras estáveis. Brief da tarefa guarda escopo. Handoff guarda resultado/evidência. Mensagens apontam esses arquivos; não repetem o histórico do filme. Não criar novo resumo global por interação. Atualizar checkpoint em mudança de fase ou risco de perda de contexto, preservando histórico necessário.

## 2. Ler o mínimo suficiente
Cumprir a leitura inicial obrigatória de AGENTS; durante a mesma tarefa, reler apenas arquivos alterados/relevantes. Usar buscas específicas, trechos, hashes e diffs. Saídas extensas ficam em arquivos; retornar resumo e caminhos. Consultar esquema completo do provedor apenas quando necessário à rota/modelo; filtrar campos sem esconder erros ou condições. Não economizar omitindo pré-verificações obrigatórias de gastos ou aprovação.

## 3. Mensagens consolidadas
Uma atribuição por entrega coerente: objetivo, dono, entradas, saídas permitidas, critério de pronto e restrições. Alvo de 150–250 palavras. Complementar somente quando uma decisão nova muda a execução; novas mensagens dizem exatamente o que substituem. Confirmação curta, preferencialmente acknowledgement nativo. Sem ciclos de agradecimento ou recapitulação. Resultado em até 200 palavras + arquivo detalhado quando necessário: feito, evidência, pendente e próxima dependência. Bloqueio só com causa concreta, impacto e menor decisão necessária.

## 4. Delegar por responsabilidade
Um dono de implementação e revisão independente quando o risco justifica. Não pedir aos três agentes a mesma pesquisa ou o mesmo resumo. Não iniciar agente para trabalho menor que a passagem de contexto. Lanes que terminaram relatam a entrega e aguardam; não inventam tarefas, monitoramento, ciclos periódicos ou documentação extra. Ajustes de runtime exigem escopo próprio: esta política não muda hooks, notificações ou supervisão.

## 5. Consultar por evento
Produtor consulta status quando precisa decidir, quando o usuário pede ou quando chega uma entrega. Evitar polling de estados inalterados. Usar espera de evento quando disponível e adequada; não programar heartbeat para acompanhar atividade normal. Separar enviado, recebido, concluído e verificado sem repetir toda essa explicação a cada mensagem.

## 6. Verificação proporcional e reutilizável
Registrar comando/checagem, resultado e versão/hash verificado. Após mudanças de gestão executar validate e testes exigidos pelo projeto, agrupando alterações coerentes em um lote. Não repetir a mesma suíte para cada parágrafo. Correção apenas de texto: revisar diff e links; código/gestão/mídia exigem suas verificações próprias. Nova mudança relevante invalida a evidência afetada. Revisão do produtor inspeciona artefatos/diffs e riscos; não repete toda a pesquisa sem motivo. Inspeção temporal, rosto, sincronismo e escuta não são substituídos por resumos ou hashes.

## 7. Conversa com Andre
Uma atualização para descoberta, decisão ou bloqueio real; cumprir as atualizações exigidas pelo ambiente sem narrar cada ferramenta. Resposta final direta, sem reler o histórico. Em voz, explicar o resultado; caminhos e documentação ficam na tela. Corrigir ambiguidade uma vez e incorporar a resposta, sem reapresentar aprovações já dadas.

## 8. Avaliar a economia
Comparar a próxima entrega concluída com uma anterior de escopo semelhante usando contagens disponíveis de mensagens, chamadas, leituras repetidas e testes repetidos. Tokens reais só quando o sistema fornecer medição; chamadas são indicadores, não tokens. Meta qualitativa: mais trabalho útil por troca, preservando revisão e rastreabilidade. Não instalar telemetria, abrir tarefa recorrente ou gastar para medir. Rever a política no encerramento de um lote se houver evidência de desperdício.
