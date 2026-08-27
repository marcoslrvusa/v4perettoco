# Circuit Breaker — Padrao

```
CLOSED --(N falhas)--> OPEN --(timeout)--> HALF_OPEN --(sucesso)--> CLOSED
                                  |--(falha)--> OPEN
```
- Retry sempre com backoff + jitter (evita retry storm).
- Fallback em Open (nao sobrecarrega servico caido).
