# Roteiro de Domínio: Atividade 3 (Circuit Breaker e Retry/Backoff)

12 perguntas que um coordenador faria, com respostas curtas para defesa no presencial. As cinco primeiras cobrem o essencial; as sete seguintes são as adversariais, do tipo "por que não X", "quanto custa", "quem decide", "e se cair no meio da noite" e a de negócio em R$.

## 1. Quando o breaker abre e o que acontece depois?
Acima de 5 falhas em 10s ele abre; em OPEN o fallback responde; após 30s uma sonda half-open testa e fecha se ok.

## 2. Por que timeout de 800ms?
Para o Pagamento não segurar thread esperando o Score; sem resposta nesse prazo conta como falha e cai no breaker.

## 3. O que o fallback devolve?
Score em cache ou default, resposta de degradação graciosa em menos de 1s, explícita em vez de 5xx.

## 4. Por que backoff com jitter e não retry imediato?
Retry imediato multiplica a carga no serviço já lento; backoff de 0.1 a 0.4s com ruído espalha as retentativas.

## 5. Como você prova a resiliência?
Simula queda, o breaker abre no limite, o fallback cobre 100% do outage e o half-open reabilita; meta de 99,9% de disponibilidade do Pagamento.

## 6. Por que não simplesmente aumentar o pool de threads?
Porque pool maior só adia o problema: **Exemplo numérico:** com 100 threads e latência de 10 s a capacidade é 10 req/s contra 200 req/s de demanda, e a fila cresce 190 req/s; com 500 threads a capacidade sobe para 50 req/s e a fila ainda cresce 150 req/s, com cinco vezes mais memória presa. Além disso, mais threads significa mais conexões no alvo doente, o que agrava a causa raiz. O breaker resolve a decisão (não tentar), o pool resolve o recurso, e recurso não conserta decisão.

## 7. Qual é o custo disso em latência para o cliente saudável?
Praticamente nenhum: em CLOSED a chamada passa direto e o único acréscimo é a leitura de estado em memória, ordem de microssegundos. O custo aparece só quando o circuito está aberto, e ali a resposta vem em menos de 1 s, contra 800 ms de timeout mais fila sem proteção. Em outras palavras, o cliente saudável não paga e o cliente em incidente paga menos.

## 8. E se o próprio fallback ficar lento ou cair?
Ele não pode: fallback é local, determinístico e sem chamada de rede, e isso é invariante do padrão. Se alguém implementar fallback consultando outro serviço, o fallback falha junto com o alvo no momento exato em que é chamado, o que é anti-padrão listado no standard. A verificação é o teste T9: derruba-se toda a rede no teste e o fallback continua respondendo em menos de 1 s.

## 9. Quem decide os parâmetros e quem pode mudá-los?
O time do serviço chamador decide, com base em 7 dias de histórico de falhas reais; os parâmetros vivem em configuração e são trocáveis sem deploy, porque calibrar em constante de código transforma todo ajuste em release. Mudança de threshold exige registro no ADR-053 com a razão nova. A revisão é trimestral ou depois de cada incidente que envolva abertura anormal.

## 10. Se cair no meio da noite, o que o plantão faz primeiro?
Três checagens, nesta ordem: estado do breaker (métrica `breaker_state`), cobertura do fallback (`breaker_fallback_total` crescendo significa que o cliente está protegido) e fila de entrada do chamador. Se o fallback está cobrindo, não se aciona ninguém para restaurar às pressas, espera-se a recuperação automática via half-open. Só se aciona o time do chamado quando o breaker não abriu em incidente real ou quando o fallback também começar a falhar.

## 11. Como isso se conecta com fila e mensageria, que é o tema da trilha?
É a fronteira síncrona da mesma disciplina: em fila, a proteção se faz com `ack` tardio, repetição e `DLQ`; em chamada síncrona, com breaker, timeout e fallback. Os dois compartilham a regra central: nunca reprocessar sem idempotência. O retry desta atividade é idempotente porque a chamada ao Score é de leitura; se fosse de escrita, seria obrigatório chave de idempotência antes de qualquer retentativa, sob pena de duplicar efeito colateral.

## 12. Qual o impacto disso no negócio, em R$ ou horas?
**Exemplo numérico:** 1.000 pagamentos por hora em pico, 2% de abandono adicional quando a página de pagamento falha, 10 minutos de indisponibilidade: aproximadamente 3 pagamentos perdidos ($1000 / 6 \times 10 \times 0{,}02$). Somando eventos semanais ao longo do trimestre, a perda passa a ser relevante, e há o custo reputacional e o custo de horas de plantão que não entram nessa conta. Do lado do custo da solução, o esforço estimado é de 15 h (meta) e a infraestrutura adicional é praticamente zero, porque o padrão roda no mesmo processo.
