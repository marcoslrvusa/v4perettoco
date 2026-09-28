# Circuit Breaker: Padrão

```
CLOSED --(N falhas)--> OPEN --(timeout)--> HALF_OPEN --(sucesso)--> CLOSED
                                  |--(falha)--> OPEN
```
- Retry sempre com backoff + jitter (evita retry storm).
- Fallback em Open (não sobrecarrega serviço caído).

## 1. Escopo e não-escopo

**Escopo**: padrão de fronteira de resiliência aplicado a qualquer chamada remota síncrona do ambiente (LLM, CRM, serviço de Score, API de pagamento de terceiro). Cobre transição de estados, parâmetros, critérios de contagem de falha, política de retry, política de fallback, telemetria obrigatória e critérios de aceite.

**Não-escopo**: comunicação assíncrona sobre fila (ali o problema se resolve com `ack` tardio, `DLQ` e repetição, não com breaker), chamadas em lote onde o custo de um ciclo completo é aceitável, e proteção contra falha de processo (aqui entra `health check` e orquestrador, não breaker). Também ficam de fora: cache de resposta como substituto do fallback (é outra decisão, com invalidação própria) e balanço de carga entre réplicas (complementar, não concorrente).

## 2. Termos

| Termo | Definição operacional |
| --- | --- |
| `CLOSED` | Estado normal; tráfego passa e falhas são contadas na janela corrente |
| `OPEN` | Estado de bloqueio; nenhuma chamada sai, o fallback responde |
| `HALF_OPEN` | Estado de sondagem; uma única chamada de teste é liberada |
| Janela deslizante | Intervalo de tempo (10 s) que delimita quais falhas contam para o threshold |
| Threshold | Número de falhas na janela que dispara a abertura (5) |
| Cooldown (`cooldown`) | Espera em OPEN antes de liberar a sonda (30 s) |
| Sonda | Única chamada liberada em HALF_OPEN para testar o alvo |
| Fallback | Resposta local, determinística e marcada com `origem` |
| Retry storm | Pico de retentativas sincronizadas que agrava a falha do alvo |
| Head of line blocking | Primeira requisição parada segurando o progresso das seguintes |

## 3. Regra canônica

O breaker é uma máquina de três estados com uma janela de contagem. A transição de fechado para aberto ocorre quando o número de falhas dentro da janela atinge o threshold:

$F_{janela} \geq N \Rightarrow OPEN$

com $F_{janela}$ contando apenas eventos com marca temporal dentro dos últimos $W = 10$ s e $N = 5$. A transição de aberto para meio-aberto ocorre quando o tempo em OPEN supera o cooldown:

$t_{em\ OPEN} \geq C \Rightarrow HALF\_OPEN$

com $C = 30$ s. Em HALF_OPEN, exatamente uma chamada de teste é liberada; se ela tiver sucesso, o circuito fecha e o contador zera; se ela falha, o circuito volta a OPEN e o cooldown reinicia do zero. O fechamento exige `success_to_close = 2` sucessos consecutivos, para não fechar por sorte única.

**Invariantes da regra**: (i) em OPEN nenhuma chamada atravessa a fronteira; (ii) o contador zera em toda transição para CLOSED; (iii) falhas fora da janela nunca contam; (iv) a sonda é sempre única por janela de resfriamento.

## 4. Tabela de decisão

| Estado | Alvo saudável? | Falhas na janela | Tempo em OPEN | Ação |
| --- | --- | --- | --- | --- |
| CLOSED | sim | < 5 | n/a | Deixa passar, conta falhas |
| CLOSED | não | >= 5 | n/a | Vai para OPEN, marca `opened_at` |
| OPEN | n/a | n/a | < 30 s | Recusa e aciona fallback |
| OPEN | n/a | n/a | >= 30 s | Vai para HALF_OPEN, libera 1 sonda |
| HALF_OPEN | sim | n/a | n/a | Sucesso 1 de 2, mantém sondando |
| HALF_OPEN | sim | n/a | n/a | Sucesso 2 de 2, vai para CLOSED com contador zerado |
| HALF_OPEN | não | n/a | n/a | Volta para OPEN, cooldown reinicia |
| Qualquer | timeout de 800 ms estoura | soma na janela | n/a | Conta como falha igual a erro 5xx |

## 5. Exemplo numérico

**Exemplo numérico:** parâmetros declarados $N = 5$, $W = 10$ s, $C = 30$ s, timeout 800 ms, 200 req/s ao chamador. Durante 10 s passam 2.000 requisições. Se 5 delas estouram o timeout, a taxa é $5/2000 = 0{,}25\%$ e o breaker abre, o que significa que ele protege contra falha sistemática, não contra ruído de 1 em 200. Uma vez aberto, as 200 req/s seguintes são atendidas pelo fallback local em menos de 1 s, ou seja, zero requisições ao Score durante 30 s: $200 \times 30 = 6000$ chamadas evitadas por ciclo de abertura. Sem breaker, essas 6.000 chamadas estourariam o timeout de 800 ms em 4.800 s de thread-ocupação ($6000 \times 0{,}8 = 4800$ s) distribuídas sobre 100 threads, o que esgota o pool em menos de 48 s ($4800 / 100$).

Espera total em OPEN: 30 s de cooldown mais o tempo da sonda, limitado a 800 ms. Recuperação máxima (sem intervenção manual): 30.8 s após a última falha.

## 6. Código de referência

```python
import time

class CircuitBreaker:
    """Breaker de 3 estados com janela deslizante por contagem."""

    def __init__(self, fail_max=5, window=10.0, cooldown=30.0,
                 success_to_close=2):
        self.fail_max = fail_max
        self.window = window
        self.cooldown = cooldown
        self.success_to_close = success_to_close
        self.state = "CLOSED"
        self.falhas = []          # timestamps das falhas dentro da janela
        self.opened_at = 0.0
        self.sucessos = 0         # sucessos consecutivos em HALF_OPEN

    def _janela_valida(self):
        agora = time.time()
        corte = agora - self.window
        self.falhas = [t for t in self.falhas if t >= corte]
        return len(self.falhas)

    def allow(self):
        """Devolve True se a chamada pode ser feita agora."""
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if time.time() - self.opened_at >= self.cooldown:
                self.state = "HALF_OPEN"
                self.sucessos = 0
                return True        # libera a unica sonda
            return False           # recusa e cai no fallback
        return self.sucessos == 0  # HALF_OPEN: so a primeira chamada passa

    def success(self):
        if self.state == "HALF_OPEN":
            self.sucessos += 1
            if self.sucessos >= self.success_to_close:
                self.state = "CLOSED"
                self.falhas = []
                self.sucessos = 0
        else:
            self.state = "CLOSED"
            self.falhas = []
            self.sucessos = 0

    def failure(self):
        agora = time.time()
        self.falhas.append(agora)
        if self.state in ("HALF_OPEN",):
            self.state = "OPEN"
            self.opened_at = agora
            self.falhas = [agora]
            self.sucessos = 0
            return
        if self._janela_valida() >= self.fail_max:
            self.state = "OPEN"
            self.opened_at = agora
            self.sucessos = 0
```

## 7. Anti-padrões (o que o sênior reprovaria)

1. **Contador fixo sem janela**: cinco falhas acumuladas ao longo de um mês abrem o circuito hoje por um problema que já passou. Reprovado: exige janela deslizante.
2. **Fallback que chama rede**: se o fallback consulta outro serviço, ele falha junto com o alvo no momento exato em que é chamado. Reprovado: fallback deve ser local e determinístico.
3. **Retry antes do breaker**: em OPEN não há o que retentar; tentar transforma o fallback em ficção. Reprovado: ordenação obrigatória breaker, depois retry.
4. **Espera nula no retry**: `time.sleep(0)` não é backoff, é retry imediato com verniz. Reprovado: espera estritamente crescente e positiva.
5. **Abrir o breaker com 1 falha**: qualquer erro pontual (restart do alvo) derruba o circuito. Reprovado: threshold calibrado com histórico.
6. **Vários sondas em paralelo**: a sonda múltipla recria a sobrecarga que o breaker evita. Reprovado: uma única sonda por janela.
7. **Label de métrica com id de usuário ou URL completa**: explode a cardinalidade do coletor. Reprovado: apenas serviço alvo e estado.
8. **Estado compartilhado via banco no caminho crítico**: adiciona uma dependência nova exatamente onde se quer reduzir dependência. Reprovado: estado em memória por processo nesta fase.
9. **Sem `origem` na resposta de fallback**: cliente confunde dado degradado com dado real. Reprovado: campo explícito obrigatório.
10. **Fechar o circuito com um único sucesso**: recuperação por sorte vira recaída em seguida. Reprovado: dois sucessos consecutivos.
11. **Contar timeout e erro 5xx de forma diferente**: lentidão é o modo de falha mais comum e não pode ficar de fora da contagem.
12. **Logs de transição ausentes**: sem registro de hora exata, o pós-incidente vira adivinhação.

## 8. Telemetria

| Métrica | Tipo | Labels (cardinalidade baixa) | Alerta |
| --- | --- | --- | --- |
| `breaker_state_transitions_total` | contador | alvo, de, para | Transição para OPEN em horário comercial |
| `breaker_state` | gauge | alvo | Igual a OPEN por mais de 5 min |
| `breaker_fallback_total` | contador | alvo, motivo | Mais de 10/min de forma contínua (meta) |
| `breaker_window_failures` | gauge | alvo | Perto do threshold (4 de 5) |
| `breaker_probe_duration_ms` | histograma | alvo | p95 da sonda acima de 800 ms |
| `retry_attempts_total` | contador | alvo, tentativa | Crescimento sustentado em 3 janelas |
| `call_duration_ms` | histograma | alvo | p95 acima de 800 ms |

Tracing distribuído: toda chamada carrega o `span` pai do chamador; o `span` do fallback recebe o atributo `fallback.reason` com o motivo (`breaker_open`, `timeout`, `error`). Isso permite responder, em uma consulta, "quantas requisições do cliente X foram atendidas por fallback ontem", sem varrer logs. Cardinalidade controlada: proibido incluir identificador de usuário, id de transação ou query string nos labels.

## 9. Plano de teste

| # | Caso | Passo | Critério de aceite |
| --- | --- | --- | --- |
| T1 | Abertura | Simular 5 timeouts de 800 ms em menos de 10 s | Estado vira OPEN e métrica de transição emitida |
| T2 | Fallback | Com OPEN, executar 100 chamadas | 100% recebem fallback em < 1 s; zero chamadas ao alvo |
| T3 | Recuperação | Restaurar alvo e aguardar 30 s | Sonda liberada; 2 sucessos fecham o circuito com contador zerado |
| T4 | Recidiva | Falhar a sonda | Volta para OPEN e cooldown reinicia do zero |
| T5 | Janela | Causar 4 falhas, esperar 11 s, causar 1 nova | Não abre (janela expirou; contagem volta a 1) |
| T6 | Retry | Medir esperas entre 4 tentativas | Esperas na faixa declarada, sempre > 0, com jitter |
| T7 | Falso positivo | Reiniciar processo em horário de pico | Contador inicia zerado; nenhuma abertura por resíduo |
| T8 | Concorrência | 50 threads com falha simultânea | Estado final consistente; apenas 1 sonda em voo |
| T9 | Fallback local | Derrubar toda rede no teste | Fallback continua respondendo (não depende de rede) |
| T10 | Tipagem | Forçar exceção não tratada | Nenhum caminho termina em 5xx sem passar por fallback |

Cada caso tem pré-requisito (alvo simulado em processo, sem rede externa), execução determinística e rollback (novo `CircuitBreaker()` zera o estado). Critério de aceite global: os 10 casos passam em modo `--self-test` sem intervenção manual.

## 10. Checklist de adesão

1. O breaker cobre a chamada inteira, incluindo leitura da resposta.
2. Timeout explícito menor que o do chamador e contabilizado como falha.
3. Janela deslizante de 10 s implementada, não contador desde o boot.
4. Threshold de 5 calibrado com histórico real de falhas.
5. Cooldown de 30 s e uma única sonda por janela.
6. Dois sucessos consecutivos para fechar o circuito.
7. Fallback local, determinístico e marcado com `origem`.
8. Retry com backoff exponencial, teto e jitter, apenas em CLOSED.
9. Métricas de transição, fallback, janela e latência com cardinalidade baixa.
10. Alerta para OPEN prolongado e para ausência de transição em incidente.
11. 10 casos de teste executáveis sem rede externa.
12. Parâmetros configuráveis sem deploy, com a razão de cada valor documentada.
13. Runbook com mitigação, rollback e responsável definido.
14. Nenhum erro vira 5xx sem tipagem e sem registro.
15. Revisão de código confirmando ausência de dependência de rede no fallback.

## 11. Referências

- Curso: "Microservices: Resilience Patterns with Resilience4j" (Udemy).
- Vídeo: "Circuit Breaker Pattern Explained" (YouTube, Fireship).
- Documento oficial: Microsoft Learn, "Circuit Breaker pattern" (learn.microsoft.com).
- Documento oficial: Resilience4j Documentation (resilience4j.readme.io).
