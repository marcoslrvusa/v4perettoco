# Roteiro de Demo: Resiliência com Circuit Breaker e Retry/Backoff

Abra o deck (index.html) e percorra os slides na ordem.

1. Slide de Resumo: abra com o problema de negócio e o blast radius.
2. Slide do ADR: defenda a opção escolhida vs as rejeitadas (trade-offs).
3. Slide de Validação/Rollout: mostre como provamos em produção.
4. Slide de Riscos: apresente o plano de mitigação.

## Pré-requisitos

5. Confirme o ambiente: Python 3.10+ instalado, pasta `2-code/` acessível e nenhum serviço externo sendo usado (as falhas são simuladas dentro do processo). Comando: `python3 -c "import sys; print(sys.version)"`. Saída esperada: versão 3.10 ou superior. Critério de falha: versão menor que 3.10. Se falhar, interrompa a demo: o objetivo é mostrar resiliência, não configurar ambiente.
6. Rode o auto-teste do breaker antes de qualquer explicação: `python3 2-code/circuit_breaker.py`. Saída esperada: execução sem exceção não tratada. Critério de falha: stack trace na tela. Se falhar, faça rollback mental: explique o padrão pelo deck e adie a parte ao vivo.
7. Rode o auto-teste do retry: `python3 2-code/retry.py`. Saída esperada: execução limpa. Critério de falha: qualquer erro importando `random` ou `time`. Se falhar, verifique o `PYTHONPATH` da pasta da atividade.

## Passo ao vivo

8. Slide de Modelo mental: abra o diagrama de estados e explique que o breaker é um amortecedor com memória. Clique na aresta `CLOSED -> OPEN` e nomeie a condição exata, `falhas >= 5 em 10 s`. Critério de falha: se a coordenadora perguntar "por que memória" e você citar apenas performance, recoloque o foco: a memória serve para decidir se a chamada vale a pena, e decidir não tentar é mais barato que processar o que vai falhar.
9. Slide de Arquitetura: percorra a ordem dos estágios na sequência exata, timeout, breaker, retry, fallback. Destaque que inverter a ordem produz os dois anti-padrões clássicos: retry antes do breaker amplifica a falha, fallback antes do timeout máscara a lentidão.
10. Demonstre a abertura ao vivo: rode `python3 - <<'PY'` e no corpo do script crie um `CircuitBreaker(fail=5, reset=30)`, chame `failure()` cinco vezes e imprima `breaker.state`. Saída esperada: `OPEN`. Critério de falha: estado diferente de `OPEN` após a quinta falha. Se falhar, mostre a condição `self.fails >= self.fail_max` no código e repita uma vez.
11. Demonstre a recusa em OPEN: com o mesmo breaker, chame `allow()` imediatamente após a abertura. Saída esperada: `False`. Critério de falha: `True`, o que indicaria que o breaker não está recusando antes de abrir conexão, exatamente a falha que o standard proíbe.
12. Demonstre o cooldown: traga a discussão para 30 s de espera e explique que na demo vocês não vão esperar 30 s ao vivo; o teste T3 do plano cobre isso em execução automatizada. Diga o número: sem espera, a sonda nunca ocorre; com ela, a recuperação máxima é 30.8 s (30 s de cooldown mais 800 ms de sonda).
13. Slide de Matemática do backoff: mostre a fórmula e a conta fechada, tentativas de 0.2 a 1.7 s. Compare com retry imediato: 3.2 s de espera acumulada e 4 chamadas simultâneas no alvo doente. Critério de falha: se alguém perguntar o que impede a sincronização, responda jitter, `random.uniform(0, 0.1)`.
14. Slide de Matemática da abertura: feche a conta das 6.000 chamadas evitadas ($200 \times 30$) e os 4.800 s de thread que isso representa. Esse é o slide que prova que abrir cedo é cálculo, não covardia.
15. Slide de Modos de falha: escolha o modo que não gera erro, lentidão sem timeout, e explique por que ele é o mais perigoso: nada marca falha e o breaker nunca abre. Conclua que timeout é pré-requisito do padrão.
16. Slide de Fallback: abra `score_fallback` e mostre o campo `origem=cache`. Diga que fallback mentiroso é o risco de negócio mais sério: decisão de crédito com dado degradado vira problema jurídico.
17. Slide de Observabilidade: mostre as métricas e explique a regra de cardinalidade: três labels por métrica, teto de 10 mil séries, proibido id de usuário ou URL completa como label.
18. Slide de Operação: percorra os sete passos do runbook e cite quem aciona em cada um: plantão do chamador mitiga, time do chamado ataca causa raiz, coordenação entra quando o orçamento de erro passa de 50%.
19. Slide de SLO: feche a conta do orçamento de erro, 259,2 s por mês, e o consumo de um outage de 10 minutos sem breaker, 600 s. Repita a frase-chave: orçamento de erro é limite de risco, não meta de bonificação.
20. Slide de Validação: liste os critérios de aceite CA-1 a CA-5 e diga que todos rodam sem rede externa. Critério de falha: qualquer CÁ que dependa de internet, porque isso torna a demonstração não reprodutível.
21. Slide de Riscos: retome a mitigação de fallback mentiroso e a de parâmetro mal calibrado, com a afirmação de que a calibragem usa 7 dias de histórico e é revisada trimestralmente.
22. Slide de Próximos Passos: feche com a sequência em quatro etapas (instrumentar, aplicar em todas as saídas, externalizar parâmetros, bulkhead) e com a reversão trivial de cada uma.
23. Perguntas e defesa: use o `ROTEIRO-DOMINIO.md` como banco de respostas; se a pergunta sair do roteiro, responda com invariante e número, nunca com opinião.

## Rollback e encerramento

24. Se qualquer demonstração ao vivo corromper o estado, faça rollback com uma nova instância: `CircuitBreaker()` zera contador, estado e `opened_at`. Não reinicie o ambiente por causa disso.
25. Encerre reforçando a frase de abertura: sem breaker, uma API lenta vira fila que derruba o próprio serviço; com ele, a degradação é graciosa em milissegundos e a recuperação é automática.

Material de apoio: pdi-distribuidos-mensageria-eventos-a3-report.pdf (dossiê completo).
