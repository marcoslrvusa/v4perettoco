# Standard — Nós Code Python em Payloads Pesados

> **Objetivo:** regra única para nós `Code` com linguagem **Python** dentro do n8n,
> usando apenas a biblioteca padrão (não há pip install garantido no runtime).

## Regras de ouro

1. **Python no n8n roda com stdlib.** `collections`, `itertools`, `functools`,
   `json`, `re`, `datetime` são seguros. Pandas/Numpy NÃO são garantidos.
2. **Nunca faça `json.loads` dentro do loop** — decodifique o payload 1x.
3. **Use `itertools` para stream de chunks** — evita materializar listas inteiras.
4. **Dedupe com `dict`/`set` de chaves primitivas** — nunca lista de objetos.
5. **Agregação com `collections.Counter`/`defaultdict`** — O(n) em vez de O(n²).
6. **Trate item a item com `try/except` granular** — um item ruim não derruba o batch.

## Template recomendado

```python
import json
from datetime import datetime

# n8n injeta o input em _input
data = _input[0]['json']

# 1) Decodifica 1x (payload vem como string)
rows = data.get('rows')
if isinstance(rows, str):
    rows = json.loads(rows)

# 2) Dedupe + normalização em uma passada
seen = set()
result = []
for row in rows:
    key = row.get('id')
    if key in seen:
        continue
    seen.add(key)

    out = {
        'id': key,
        'ts': row.get('ts'),
    }
    result.append(out)

return [{'json': {'count': len(result), 'items': result}}]
```

## Estratégia de chunking

O n8n entrega o payload por inteiro ao nó Python. Para payloads muito grandes,
**faça o chunking na camada JS antes** (veja `payload-lib.js`) e envie chunk a
chunk ao Python — cada chamada processa um lote pequeno e grava progresso
(`mt_job_progress`, da atividade 2).

```
JS: chunk 1/10 ──▶ Python: enrich ──▶ checkpoint
JS: chunk 2/10 ──▶ Python: enrich ──▶ checkpoint
... retomável se cair (retoma do chunk X, não do zero)
```

## Anti-patterns

| Anti-pattern | Problema |
|---|---|
| `[r for r in rows if ...]` em 100k | Aloca lista inteira |
| `.count(x)` ou `list.index()` no loop | O(n²) |
| `json.loads(row['payload'])` por item | Re-parse desnecessário |
| `datetime.now()` por item | Custo + imprecisão; use uma vez |
| Tratar exceção no batch todo | Um item ruim mata o job |

## Checagem (antes de publicar)

- [ ] Apenas stdlib (sem import que exige pip)
- [ ] Decodificação JSON feita 1x
- [ ] Dedupe/agregação com `set`/`dict`/`Counter` (O(n))
- [ ] `try/except` por item quando campos são opcionais
- [ ] Retorno no formato que o próximo nó espera (`{ json: ... }`)