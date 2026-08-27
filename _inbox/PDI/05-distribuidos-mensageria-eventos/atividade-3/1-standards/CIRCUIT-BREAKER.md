# STANDARD — Circuit Breaker

## Estados
- **Closed:** tráfego normal; conta falhas.
- **Open:** após `failure_threshold` (ex: 5 em 10s) → bloqueia e retorna fallback.
- **Half-Open:** após `cooldown` (ex: 30s) → deixa 1 requisição testar; se ok, fecha.

## Parâmetros
- `failure_threshold=5`, `window=10s`, `cooldown=30s`, `success_to_close=2`.
