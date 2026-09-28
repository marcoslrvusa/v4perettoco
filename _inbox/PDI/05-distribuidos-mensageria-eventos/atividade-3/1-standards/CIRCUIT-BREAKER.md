# STANDARD: Circuit Breaker

## Estados
- **Closed:** tráfego normal; conta falhas.
- **Open:** após `failure_threshold` (ex: 5 em 10s) → bloqueia e retorna fallback.
- **Half-Open:** após `cooldown` (ex: 30s) → deixa 1 requisição testar; se ok, fecha.

## Parâmetros
- `failure_threshold=5`, `window=10s`, `cooldown=30s`, `success_to_close=2`.

## 1. Escopo

Padrão de proteção da fronteira entre chamador e dependência remota. Aplica-se a qualquer saída de rede síncrona: serviço de Score, LLM, CRM, API de terceiro. O padrão decide, com base no histórico recente, se uma chamada vale a pena ser feita. Não é otimismo, é gestão de risco com memória.

**Não-escopo**: chamadas sobre fila (ali valem `ack` tardio e `DLQ`), operações locais (não há o que proteger), e balanceamento de carga entre réplicas (fase posterior, complementar). Breaker não conserta erro de contrato, não conserta payload errado e não substitui `health check` do orquestrador: ele endereça lentidão e indisponibilidade da dependência, que é justamente o modo de falha que mais escala.

## 2. Máquina de estados

```
          falhas >= 5 em 10s
   CLOSED ─────────────────────► OPEN
     ▲                            │
     │  2 sucessos consecutivos   │ após cooldown >= 30s
     │                            ▼
     └──── HALF_OPEN ◄────────────┘
              │
              │ falha na sonda
              └──────────────► OPEN (cooldown reinicia)
```

Regras de transição, com a condição exata que a implementação deve testar:

| De | Para | Condição | Efeito colateral |
| --- | --- | --- | --- |
| CLOSED | OPEN | `len(falhas_na_janela) >= 5` | Grava `opened_at = agora` |
| OPEN | HALF_OPEN | `agora - opened_at >= 30` | Libera exatamente 1 chamada |
| HALF_OPEN | CLOSED | 2 sucessos consecutivos | Zera `falhas` e `sucessos` |
| HALF_OPEN | OPEN | Qualquer falha da sonda | Reinicia `opened_at` e limpa janela |
| CLOSED | CLOSED | Sucesso | Zera contador de falhas |

Detalhe que separa implementação amadora de produção: em OPEN, `allow()` deve devolver `False` antes de qualquer tentativa de conexão, inclusive antes de resolver DNS. Se a recusa acontecer depois de abrir socket, o breaker protege menos do que promete e ainda gasta descoberta de nome no caminho de erro.

## 3. Fórmulas

**Condição de abertura:**

Em linguagem de conjuntos: `contar(falhas t_i tais que t_i >= agora - W) >= N`, com $W = 10$ s e $N = 5$. Cada $t_i$ é o instante de uma falha (timeout ou exceção). Falhas mais antigas que $W$ são descartadas antes da comparação, o que torna a janela deslizante e não acumulativa.

**Condição de sondagem:** $t_{agora} - t_{abertura} >= C$, com $C = 30$ s.

**Taxa de falha implícita na calibração:** $r = N / (\lambda \cdot W)$

**Exemplo numérico:** com $\lambda = 200$ req/s e $W = 10$ s, a janela contém 2.000 chamadas. Com $N = 5$, o breaker abre a partir de $r = 5/2000 = 0{,}25\%$ de falha. Se o histórico real mostrar taxa de erro base de 0,5%, o threshold de 5 abriria o circuito com ruído saudável; nesse caso o correto é subir para $N = 11$ (0,5% x 2.000 = 10, arredondado para cima com folga), mantendo $W$.

**Janela efetiva**: o instante da abertura é `opened_at`, e não a última falha, porque o cooldown mede quanto tempo o circuito fica bloqueado a partir da decisão, não a partir do evento.

**Custo de abrir:** $C_{abertura} = \lambda \cdot C = 200 \times 30 = 6000$ chamadas evitadas

Essas 6.000 chamadas, com timeout de 800 ms, ocupariam 4.800 s de tempo de thread ($6000 \times 0{,}8$). Distribuídas em 100 threads, esgotariam o pool em 48 s. Abrir em 5 falhas, portanto, evita o esgotamento que a própria abertura causaria se fosse tardia.

## 4. Tabela de decisão

| Situação | Estado atual | Falhas na janela | Tempo em OPEN | Decisão |
| --- | --- | --- | --- | --- |
| Tráfego normal, sem falha | CLOSED | 0 | n/a | Passa |
| Erro pontual (restart do alvo) | CLOSED | 1 | n/a | Passa, conta |
| Timeout de 800 ms | CLOSED | soma | n/a | Passa, conta |
| Quinta falha em 10 s | CLOSED | 5 | n/a | Vai para OPEN |
| Chamada logo após abrir | OPEN | n/a | < 30 s | Recusa, fallback |
| Fim do cooldown | OPEN | n/a | >= 30 s | Vai para HALF_OPEN |
| Primeira chamada em sondagem | HALF_OPEN | n/a | n/a | Libera 1 |
| Segunda chamada em sondagem | HALF_OPEN | n/a | n/a | Recusa, espera a sonda |
| Sonda responde ok | HALF_OPEN | n/a | n/a | Sucesso 1 de 2 |
| Segunda sonda ok | HALF_OPEN | n/a | n/a | Fecha, zera contador |
| Sonda falha | HALF_OPEN | n/a | n/a | Reabre, cooldown reinicia |
| Fallback acionado | OPEN | n/a | n/a | Resposta local marcada |

## 5. Exemplo numérico de calibragem

**Exemplo numérico:** cenário declarado: $\lambda = 200$ req/s, latência mediana do alvo de 120 ms, p95 de 400 ms, timeout 800 ms, taxa de erro observada de 0,1%. Em 10 s passam 2.000 requisições e espera-se $2000 \times 0{,}001 = 2$ falhas naturais por janela. Com $N = 5$, há margem de 3 falhas acima do ruído antes da abertura, o que equivale a detectar falha sistemática em aproximadamente 25 s de outage real ($5 / 0{,}001 / 200 = 25$). Se a meta for detectar mais rápido, baixar $N$ para 3 reduz a detecção para 15 s, mas reduz a folga contra ruído para apenas 1 falha. A escolha é um trade-off explícito entre tempo de detecção e falso positivo, e por isso os parâmetros vivem em configuração, não em constante de código.

## 6. Código mínimo de referência

```python
import time

class CircuitBreaker:
    def __init__(self, fail=5, reset=30):
        self.fails = 0; self.fail_max = fail; self.reset = reset
        self.state = "CLOSED"; self.opened_at = 0
    def allow(self):
        if self.state == "OPEN":
            if time.time() - self.opened_at > self.reset:
                self.state = "HALF_OPEN"; return True
            return False
        return True
    def success(self): self.fails = 0; self.state = "CLOSED"
    def failure(self):
        self.fails += 1
        if self.fails >= self.fail_max:
            self.state = "OPEN"; self.opened_at = time.time()
def call_with_breaker(breaker, fn, fallback):
    if not breaker.allow(): return fallback()
    try:
        r = fn(); breaker.success(); return r
    except Exception:
        breaker.failure(); return fallback()
```

Leitura crítica do código acima: `allow()` é o único ponto que nega acesso, `success()` zera o contador (sem isso a segunda falha pós-recuperação abriria de novo), e `call_with_breaker()` devolve o resultado do fallback na exceção, de modo que o chamador nunca propaga a falha bruta. A versão de produção acrescenta janela deslizante por timestamp e `success_to_close`, como está no `RESILIENCIA.md`.

## 7. Anti-padrões

1. **Abrir sem janela**: contador desde o boot abre por eventos antigos. Reprovado.
2. **Fechar com 1 sucesso**: recaída imediata. Reprovado: exige 2 sucessos.
3. **Fallback em rede**: falha junto no pior momento. Reprovado: local.
4. **Retry em OPEN**: desperdiça tentativa e esconde a degradação. Reprovado.
5. **Timeout ausente**: lentidão não gera falha, logo o breaker nunca abre. Reprovado: timeout é pré-requisito do padrão.
6. **Contar apenas exceção de rede**: timeouts e erros 5xx devem contar igualmente. Reprovado.
7. **Estado em banco no caminho crítico**: dependência nova onde se quer menos dependência. Reprovado nesta fase.
8. **Um breaker global para todas as dependências**: falha do Score abriria o circuito do LLM. Reprovado: uma instância por alvo.
9. **Sem métrica de transição**: impossível auditar o pós-incidente. Reprovado.
10. **Labels com alta cardinalidade**: explode o coletor. Reprovado: alvo e estado apenas.
11. **Cooldown menor que o tempo de recuperação típico do alvo**: sonda falha sempre, circuito fica oscilando. Reprovado: calibrar contra o tempo de restart real do alvo.
12. **Não registrar a abertura**: sem hora, sem causa, sem aprendizado. Reprovado.

## 8. Telemetria obrigatória

- `breaker_state` (gauge, label `alvo`): estado atual, alerta se OPEN por mais de 5 minutos.
- `breaker_state_transitions_total` (contador, labels `alvo`, `de`, `para`): cada transição; alerta em qualquer transição para OPEN.
- `breaker_window_failures` (gauge, label `alvo`): falhas na janela corrente; alerta em 4 de 5 para dar margem de manobra.
- `breaker_fallback_total` (contador, labels `alvo`, `motivo`): motivo em `breaker_open`, `timeout`, `error`.
- `breaker_probe_duration_ms` (histograma, label `alvo`): latência da sonda; p95 acima de 800 ms indica alvo ainda degradado.
- `call_duration_ms` (histograma, label `alvo`): alimenta a calibragem de timeout.

Cardinalidade máxima aceitável: 3 labels por métrica, com domínio limitado (alvo em dezenas, estado em três, motivo em três). Regra prática: se uma métrica pode gerar mais de 10 mil séries, ela está errada por design.

Tracing: atributo `fallback.reason` no `span` de fallback, e `breaker.state` no `span` de entrada, permitem cruzar dados de latência com decisões do breaker numa única consulta.

## 9. Plano de teste e critérios de aceite

| Caso | Configuração | Ação | Aceite |
| --- | --- | --- | --- |
| Abertura | `fail=5`, `reset=30` | 5 exceções em 1 s | Estado OPEN em menos de 10 s |
| Recusa | Estado OPEN | 10 chamadas | Todas retornam fallback, zero chamadas de rede |
| Sonda | Aguardar 31 s | 1 chamada | Estado HALF_OPEN e exatamente 1 chamada em voo |
| Fechamento | Sonda ok | 1 sucesso a mais | Estado CLOSED, contador zerado |
| Recidiva | Sonda falha | 1 exceção | Volta a OPEN, `opened_at` reiniciado |
| Janela | `window=10` | 4 falhas, espera 11 s, 1 falha | Não abre |
| Timeout | `timeout=800` | Alvo a 5 s | Falha contabilizada, abre |
| Concorrência | 50 threads | Falha simultânea | No máximo 1 sonda em voo |
| Isolamento | Dois breakers | Falhar só um alvo | O outro permanece CLOSED |
| Fallback local | Sem rede | Chamada em OPEN | Resposta OK em < 1 s |

Critério de aceite global: os 10 casos passam em modo `--self-test`, determinístico, sem rede externa e com rollback trivial (nova instância zera o estado).

## 10. Checklist de adesão

1. Uma instância de breaker por dependência (alvo), nunca uma global.
2. `allow()` recusa antes de abrir conexão ou resolver nome.
3. Janela deslizante de 10 s com descarte explícito de eventos antigos.
4. `failure_threshold = 5` justificado com histórico de erro real.
5. `cooldown = 30 s` compatível com o tempo de restart do alvo.
6. `success_to_close = 2` para evitar fechamento por sorte.
7. Timeout de 800 ms configurado e contabilizado como falha.
8. Fallback local, determinístico e com `origem` explícito.
9. Retry com backoff e jitter apenas em CLOSED, nunca em OPEN.
10. Métricas de estado, transição, janela, fallback e latência no ar.
11. Alerta de OPEN prolongado e de ausência de transição em incidente.
12. Testes dos 10 casos executáveis sem rede.
13. Parâmetros em configuração, trocáveis sem deploy.
14. Runbook com mitiga, rollback e responsável.
15. Revisão de código atestando que nenhum erro vira 5xx sem tipagem.

## 11. Referências

- Curso: "Microservices: Resilience Patterns with Resilience4j" (Udemy).
- Vídeo: "Circuit Breaker Pattern Explained" (YouTube, Fireship).
- Documento oficial: Microsoft Learn, "Circuit Breaker pattern" (learn.microsoft.com).
- Documento oficial: Resilience4j Documentation (resilience4j.readme.io).
