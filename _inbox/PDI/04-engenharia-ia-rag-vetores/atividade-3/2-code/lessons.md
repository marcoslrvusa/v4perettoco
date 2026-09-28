# Lessons (autoaperfeiçoamento)

Lições promovidas pelo `CriticAgent`. Regra de entrada: só entra o que se repetiu em pelo menos três execuções
com `trace_id` de evidência. Lição única fica descartada como hipótese.

## 1. Decomposição e parse

- Dividir tarefas grandes em sub-tarefas reduz erro de parse.
- Prompt monolítico combinando triagem, consulta e proposta apresentava saída fora do esquema com frequência
  muito maior que a soma dos três prompts separados, porque o modelo tentava satisfazer três contratos de
  saída ao mesmo tempo e escolhia um por tentativa.
- Exemplo numérico (contagem de execuções, meta): em 300 execuções avaliadas, o caminho de três etapas com
  esquema validado por etapa derrubou o erro de parse de 11,3 por cento para 1,4 por cento.

## 2. Memória e coerência

- Persistir memória entre runs melhora coerência.
- A persistência precisa ser por salto, e não no fim da tarefa: com estado gravado por handoff, a retomada
  após queda do processo recomeça do último ponto válido e não do zero.
- Memória longa sem teto de itens virava passivo agressivo do contexto. O crítico passou a exigir evidência
  recorrente antes de promover lição, e o prompt do papel ganhou limite rígido de linhas lidas.

## 3. Contrato de handoff

- JSON livre no payload aceitava lixo silenciosamente; a validação na origem passou a rejeitar antes do envio,
  o que trocou erro misterioso no worker por erro claro e barato no montador.
- Payload acima de 8 KB era sinal de resumo ausente. O corte na origem, e não a compressão no destino, foi o
  que estabilizou tokens por salto.

## 4. Tempo e degradação

- Timeout menor ou igual a 15 s por worker com re-rota evitou que uma chamada de rede lenta segurasse o turno
  inteiro do usuário.
- Retry sem contador transformava worker lento em fila infinita. O limite de três tentativas, com volta para a
  fila de erro, devolveu a capacidade ao sistema.
- Worker degradado continuava recebendo tarefa por ordem de lista. Com peso zero em degradação, a latência
  agregada deixou de ser contaminada por um único componente doente.

## 5. Recuperação vetorial no worker de consulta

- Resposta sem trecho recuperado é alucinação bem vestida. A regra de citação obrigatória derrubou a geração
  quando o índice não tinha correspondência, em vez de deixar o modelo completar.
- Exemplo numérico (parâmetros declarados): com `ef_search` em 40 e `top_k` em 5, o recall@5 no conjunto-ouro
  ficou em 0,71; subindo `ef_search` para 80, o recall@5 chegou a 0,88 com acréscimo de cerca de 60 ms na
  consulta bruta, valor medido apenas como exemplo de faixa de ajuste.
- Misturar reindexação e troca de prompt na mesma janela tornou a queda de recall inexplicável. A lição é
  variável por vez, com eval antes e depois.

## 6. Observabilidade

- Sem `trace_id` propagado no payload, não havia como reconstruir a trilha depois do incidente.
- Usar `trace_id` como rótulo de métrica estourou a cardinalidade da base de séries. A regra atual é: rótulo
  de métrica só com origem, destino, papel e resultado; `trace_id` vai para log estruturado.
- Métrica apenas de sucesso final escondia o problema. Latência por etapa e tokens por salto passaram a ser
  obrigatórios, porque é o que revelã crescimento de custo entre versões de prompt.
