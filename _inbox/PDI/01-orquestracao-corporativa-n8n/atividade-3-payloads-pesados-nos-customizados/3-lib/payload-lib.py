# ============================================================
# payload_lib.py — Biblioteca reutilizável de nós Code Python
# PDI A3: Nós customizados / expressões avançadas
# Apenas stdlib — sem dependências externas.
# ============================================================
import json
from collections import Counter, defaultdict
from itertools import islice

# ------------------------------------------------------------
# 1) Chunking streaming (itertools.islice)
# ------------------------------------------------------------
def chunk(iterable, size=100):
    it = iter(iterable)
    while True:
        batch = list(islice(it, size))
        if not batch:
            break
        yield batch

# ------------------------------------------------------------
# 2) Dedupe por chave primitiva (O(n))
# ------------------------------------------------------------
def dedupe(rows, key='id'):
    seen = set()
    result = []
    for row in rows:
        k = row.get(key)
        if k in seen:
            continue
        seen.add(k)
        result.append(row)
    return result

# ------------------------------------------------------------
# 3) Agregação com Counter/defaultdict (O(n), nunca O(n²))
# ------------------------------------------------------------
def aggregate(rows, key='tipo', value=None):
    counts = Counter(r.get(key) for r in rows)
    totals = defaultdict(int)
    if value:
        for r in rows:
            try:
                totals[r.get(key)] += r.get(value) or 0
            except TypeError:
                pass
    return {
        'counts': dict(counts),
        'totals': dict(totals),
    }

# ------------------------------------------------------------
# 4) Decodifica payload 1x (vem como string)
# ------------------------------------------------------------
def parse_payload(payload):
    if isinstance(payload, str):
        return json.loads(payload)
    if isinstance(payload, dict) and 'rows' in payload and isinstance(payload['rows'], str):
        payload['rows'] = json.loads(payload['rows'])
    return payload

# ------------------------------------------------------------
# 5) Saída para n8n
# ------------------------------------------------------------
def to_output(data):
    return [{'json': data}]

# ------------------------------------------------------------
# Exemplo de uso dentro de um nó Code Python:
#
#   data = parse_payload(_input[0]['json'])
#   rows = dedupe(data.get('rows', []), key='id')
#   agg = aggregate(rows, key='tipo')
#   return to_output({'count': len(rows), 'aggregation': agg})
# ------------------------------------------------------------