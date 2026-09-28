# Roteiro de Demo: Orquestração Multi-agente com Handoffs e Isolamento

Abra o deck (index.html) e percorra os slides na ordem.

## Pré-requisitos

1. Ambiente com Python 3.11 ou superior e as dependências do diretório `2-code/` instaladas.
2. Variável de ambiente do provedor de modelo configurada na sessão do terminal.
3. Base vetorial de homologação acessível, com a coleção de exemplo já populada.
4. Seed: carregar o lote de demonstração com o script de popular da atividade, que insere 20 documentos de
   exemplo e registra a contagem esperada de chunks.
5. Cofre de credenciais aberto apenas para o worker de consulta; os demais workers iniciam sem essa
   credencial, e é justamente isso que será mostrado.

**Saída esperada do pré-requisito:** contagem de chunks impressa e igual à declarada no seed.
**Se falhar:** não iniciar a demo. Verificar conectividade com a base e conferir se o seed foi aplicado na
coleção certa. Rollback do seed: script de remoção do lote de demonstração, que apaga apenas os documentos
marcados como `demo`.

1. Slide de Resumo: abra com o problema de negócio e o blast radius. Clique no slide 1 e diga a frase de
   abertura: o entregável é o padrão de fronteira entre papéis, não um chatbot.
   Saída esperada: público entende que houve problema de produção, não de modelagem.
   Critério de falha: alguém perguntar "isso é só um framework?" antes do slide 4.
   Se der errado: voltar ao slide 1 e citar a contagem de execuções com erro de parse.

2. Slide do ADR: defenda a opção escolhida vs as rejeitadas (trade-offs). Clique no slide 4 e percorra a
   matriz de decisão linha a linha.
   Saída esperada: o público aceita que "mais mensagens" é o preço pago por fronteira e teste.
   Critério de falha: aparecer dúvida sobre por que não usar um agente único.
   Se der errado: abrir a fórmula de hops do slide 13 e mostrar que o custo de salto é limitado por conta.

3. Slide do contrato de handoff: clique no slide 12 e mostre a rejeição de mensagem inválida.
   Saída esperada: mensagem sem `trace_id` é barrada na origem com erro explícito.
   Critério de falha: aceitar payload acima de 8 KB sem aviso.
   Se der errado: executar em terminal o exemplo de validação do `handoff_schema.py` e mostrar a exceção.

4. Execução da jornada feliz: rode em terminal o comando de demonstração da triagem para consulta até
   proposta com o `trace_id` de exemplo do seed.
   Saída esperada: três etapas concluídas, dois saltos registrados e resposta com citação de chunk.
   Critério de falha: qualquer etapa acima de 15 s ou resposta sem trecho citado.
   Se der errado: conferir o `trace_id` no log estruturado e reiniciar a partir do último handoff válido, sem
   repetir efeito externo.

5. Slide de matemática de hops: clique no slide 13 e feche a conta na lousa com os números do slide.
   Saída esperada: público vê 8 saltos como teto derivado de 30 s, e não como número escolhido a olho.
   Critério de falha: ninguém conseguir repetir a conta.
   Se der errado: refazer com valores redondos: 30 menos 0,8 dividido por 3,35.

6. Timeout forçado: ative a falha simulada no worker de consulta para que ele não responda dentro de 15 s.
   Saída esperada: re-rota para o worker de fallback, `fallback_triggered` incrementa e o estado da tarefa
   é preservado.
   Critério de falha: o fluxo ficar pendurado além de 15 s ou perder o resultado das etapas anteriores.
   Se der errado: interromper o consumidor, verificar o teto de timeout configurado e reiniciar o worker.

7. Cadeia cíclica: force o classificador a alternar entre dois workers na mesma intenção.
   Saída esperada: aborto com erro `loop_detectado` após `max_hops` saltos.
   Critério de falha: mais de 8 saltos consumidos.
   Se der errado: conferir o valor de `max_hops` derivado da fórmula e reiniciar o supervisor.

8. Base vetorial vazia: execute a consulta com termo sem correspondência na coleção de exemplo.
   Saída esperada: status `sem_suporte`, zero texto gerado, registro do motivo no log.
   Critério de falha: qualquer resposta prosa sem citação.
   Se der errado: bloquear a publicação e revisar a regra de citação obrigatória.

9. Slide de isolamento: clique no slide 20 e mostre que o worker de triagem não alcança a base vetorial.
   Saída esperada: tentativa de acesso negada por política de rede.
   Critério de falha: qualquer leitura bem-sucedida fora do worker de consulta.
   Se der errado: remover a credencial daquele worker e repetir o teste antes de continuar.

10. Slide de índice vetorial: clique no slide 16 e explique o dimensionamento de memória com os números do
    exemplo.
    Saída esperada: público entende por que a coleção é particionada por cliente.
    Critério de falha: dúvida sobre a origem do número de 1,8 GB.
    Se der errado: mostrar a conta dimensão x 4 x quantidade de chunks na lousa.

11. HNSW contra IVFFlat: clique no slide 17 e defenda a escolha pela matriz de critérios.
    Saída esperada: decisão lida como tradeoff de RAM e escrita, não como preferência de moda.
    Critério de falha: aparecer como se HNSW fosse sempre melhor.
    Se der errado: citar o cenário de escrita massiva em que IVFFlat seria a escolha correta.

12. Ajuste de recall: alterne `ef_search` entre 40 e 80 na consulta de demonstração e compare a contagem de
    citações relevantes no conjunto-ouro.
    Saída esperada: recall@5 maior com `ef_search` maior e acréscimo de latência visível no painel.
    Critério de falha: melhora de recall sem qualquer custo de latência, o que indicaria medição errada.
    Se der errado: conferir se o mesmo lote de avaliação está sendo usado nas duas rodadas.

13. Retentativa e idempotência: reenvie a mesma mensagem com o mesmo `trace_id` e `seq`.
    Saída esperada: descarte silencioso do duplicado, efeito externo executado uma única vez.
    Critério de falha: duas propostas ou dois registros idênticos.
    Se der errado: limpar o registro de idempotência do teste e repetir a partir de um `trace_id` novo.

14. Queda de processo: mate o consumidor no meio de um lote e suba de novo.
    Saída esperada: retomada pelo último handoff válido, sem replays completos.
    Critério de falha: perda de trabalho já gravado.
    Se der errado: verificar se o `XACK` estava acontecendo antes da gravação de estado.

15. Slide de métricas: clique no slide 21 e mostre cardinalidade de rótulo sem `trace_id`.
    Saída esperada: painel estável, sem explosão de séries.
    Critério de falha: série única com milhares de valores distintos.
    Se der errado: remover o rótulo e recarregar o painel antes de continuar a apresentação.

16. Slide de falha e recuperação: clique no slide 19 e percorra a tabela de sintome até tempo de recuperação.
    Saída esperada: cada linha com detecção, mitigação e recuperação.
    Critério de falha: alguma linha sem forma de detecção.
    Se der errado: complementar com o runbook do README.

17. Slide de matemática de sucesso composto: clique no slide 14 e feche a conta de 0,79 ao cubo.
    Saída esperada: público entende a origem dos 49 por cento e a exigência de 98,3 por cento por etapa.
    Critério de falha: confundir sucesso por etapa com sucesso de tarefa.
    Se der errado: refazer na lousa com dois valores de `p` diferentes.

18. Slide de custo: clique no slide 15 e feche a conta de R$ 0,14 por consulta.
    Saída esperada: público vê que o custo unitário é parecido e o retrabalho que é o que mudou.
    Critério de falha: número sem parâmetros declarados.
    Se der errado: repetir a conta destacando preço por milhão de tokens e quantidade de tokens.

19. Slide de Validação/Rollout: mostre como provamos em produção. Clique no slide 6 e liste os casos com
    critério de aceite.
    Saída esperada: validação entendida como conjunto de testes executáveis.
    Critério de falha: validação lida como "testamos manualmente e gostamos".
    Se der errado: abrir o plano de teste do standard e citar o caso de unicode e texto vazio.

20. Slide de Riscos: apresente o plano de mitigação. Clique no slide 8 e ligue cada risco à mitigação.
    Saída esperada: público vê teto de saltos, modelo leve no supervisor e fila com backpressure.
    Critério de falha: risco listado sem detecção associada.
    Se der errado: citar o modo de falha correspondente na tabela do README.

21. Fecho: clique no slide 22 e declare os números finais e o status de homologação.
    Saída esperada: comparação de 49 por cento para 97 por cento, com meta declarada de 95 por cento.
    Critério de falha: apresentar meta como fato medido.
    Se der errado: corrigir na hora dizendo que a marca é meta e apontar a janela de medição.

22. Perguntas e compromisso: clique no slide 23 e encerre com os três próximos passos e com o que ficou de
    propósito fora de escopo.
    Saída esperada: público sai sabendo o que é próximo e o que não entra.
    Critério de falha: ficar sem resposta sobre a alternativa mais barata.
    Se der errado: responder com a opção de agente único e o motivo de ela ter sido rejeitada.

Material de apoio: pdi-engenharia-ia-rag-vetores-a3-report.pdf (dossiê completo).

## Rollback da demo

- Desligar as flags de falha simulada antes de sair do ambiente.
- Remover o lote `demo` da base vetorial.
- Restaurar `ef_search` e `top_k` para os valores de homologação declarados.
- Conferir que nenhum efeito externo foi disparado mais de uma vez durante a apresentação.
