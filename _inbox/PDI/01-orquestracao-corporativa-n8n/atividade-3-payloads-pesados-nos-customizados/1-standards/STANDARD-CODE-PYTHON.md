# Standard: Nós Code Python em Payloads Pesados

> **Objetivo:** regra única para nós `Code` com linguagem **Python** dentro do n8n,
> usando apenas a biblioteca padrão (não há pip install garantido no runtime).

## Escopo e não-escopo

**Escopo:** nós `n8n-nodes-base.code` com `language: 'python'` que fazem enriquecimento,
agregação, contagem ou classificação sobre listas recebidas de um nó anterior,
especialmente quando a etapa anterior já reduziu o volume (dedupe e filtro feitos
em JS). Inclui também o contrato de entrada/saída do nó: `_input[0]['json']` na
entrada, lista de `{'json': ...}` na saída.

**Não-escopo:** (a) processamento de 100k itens diretamente em Python sem redução
prévia: a ordem canônica da trilha é JS reduz, Python calcula; (b) qualquer pacote
fora da stdlib (`pandas`, `numpy`, `requests`, `pydantic`); (c) E/S de arquivo e de
rede dentro do nó, que pertencem a nós nativos do n8n.

## Termos

| Termo | Significado operacional neste standard |
|---|---|
| stdlib | Biblioteca padrão do Python que acompanha o interpretador, sem instalação |
| `_input` | Variável injetada pelo n8n com os itens da etapa anterior |
| Passada única | Um `for` percorrendo a lista inteira uma vez |
| Contador (`Counter`) | Estrutura da stdlib que conta ocorrências por chave em O(n) |
| Mapa acumulador (`defaultdict`) | Mapa que cria valor inicial automático, evitando `if` de existência |
| Lote (chunk) | Fatia enviada do nó JS ao nó Python, com checkpoint entre lotes |
| Tratamento granular | `try/except` dentro do laço, por item, nunca no bloco inteiro |

## Regras de ouro

1. **Python no n8n roda com stdlib.** `collections`, `itertools`, `functools`,
   `json`, `re`, `datetime` são seguros. Pandas/Numpy NÃO são garantidos.
2. **Nunca faça `json.loads` dentro do loop**: decodifique o payload 1x.
3. **Use `itertools` para stream de chunks**: evita materializar listas inteiras.
4. **Dedupe com `dict`/`set` de chaves primitivas**: nunca lista de objetos.
5. **Agregação com `collections.Counter`/`defaultdict`**: O(n) em vez de O(n²).
6. **Trate item a item com `try/except` granular**: um item ruim não derruba o batch.

Cada regra tem um custo correspondente. A regra 5, por exemplo, substitui o padrão
ingênuo de procurar a chave dentro de uma lista de pares a cada item:

$$C_{ingenuo}(n) = n \cdot k \quad \text{com} \quad k \approx \frac{n}{2} \quad \Rightarrow \quad \frac{n^2}{2}$$

$$C_{counter}(n) = n \cdot c \quad \text{com} \quad c \approx 3 \quad \text{(hash, comparação, incremento)}$$

## Exemplo numérico

**Exemplo numérico:** lote de $n = 10.000$ linhas vindas do JS, 3 categorias
(`B2B`, `B2C`, `Outro`), 1% de linhas com `score` não numérico.

- `Counter` sobre a chave: 10.000 iterações, 3 entradas no dicionário final.
- Soma por categoria com `defaultdict(int)`: mais 10.000 iterações.
- Linhas com `score` inválido: 100, cada uma capturada por `TypeError` no
  `try/except` interno e contada como 0 sem interromper o lote.
- Custo total: $\approx 20.000 \times 3 = 60.000$ operações.
- Na versão proibida (procurar a categoria numa lista de pares a cada linha):
  $\approx \frac{10000^2}{2} = 5 \times 10^{7}$ comparações, cerca de 800 vezes mais.

## Tabela de decisão

| Se | E | Então |
|---|---|---|
| A agregação é por contagem | Chaves de baixa cardinalidade | `Counter(iterable)` |
| A agregação é por soma | Chaves conhecidas no início | `defaultdict(int)` + laço de soma |
| A agregação é por média | Precisa de soma e contagem | `defaultdict(lambda: [0, 0])` e divide ao final |
| O payload vem como string | Sempre | `parse_payload` 1x antes de qualquer laço |
| Um campo é opcional | Pode faltar ou ser de tipo errado | `row.get(chave)` + `try/except` no acumulador |
| O lote é grande demais para a memória | n > limite do worker | Chunking no JS antes, Python recebe lote |
| Precisa de fatiar um iterável | Sem materializar a lista | `itertools.islice` |
| Precisa de agrupar | Ordem não importa | `itertools.groupby` só após `sorted` pela chave |
| O resultado vai para outro nó | Sempre | `return [{'json': ...}]`, nunca `print` |

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

Variante agregada, mantendo o mesmo contrato de saída:

```python
from collections import Counter, defaultdict

counts = Counter()
totals = defaultdict(int)

for row in result:
    tipo = row.get('tipo') or 'sem_tipo'
    counts[tipo] += 1
    try:
        totals[tipo] += float(row.get('score') or 0)
    except (TypeError, ValueError):
        totals[tipo] += 0

return [{'json': {
    'processed': len(result),
    'byTipo': dict(counts),
    'somaScore': dict(totals),
}}]
```

## Estratégia de chunking

O n8n entrega o payload por inteiro ao nó Python. Para payloads muito grandes,
**faça o chunking na camada JS antes** (veja `payload-lib.js`) e envie chunk a
chunk ao Python: cada chamada processa um lote pequeno e grava progresso
(`mt_job_progress`, da atividade 2).

```
JS: chunk 1/10 ──▶ Python: enrich ──▶ checkpoint
JS: chunk 2/10 ──▶ Python: enrich ──▶ checkpoint
... retomável se cair (retoma do chunk X, não do zero)
```

A razão de a fronteira ficar no JS é que o JS já paga o custo do `JSON.parse` e do
dedupe; o Python herda um lote menor e sem duplicatas. Se a ordem fosse invertida,
o interpretador Python carregaria o volume bruto, que é justamente o que este
standard busca evitar.

**Exemplo numérico:** payload de 100.000 itens com 40% de duplicatas. Fronteira
correta (JS dedupe, depois Python): Python recebe 60.000 itens já únicos, em lotes
de 1.000. Fronteira invertida: Python receberia 100.000 itens em um único nó, com
o custo adicional de um `json.loads` de um documento muito maior.

## Anti-patterns

| Anti-pattern | Problema |
|---|---|
| `[r for r in rows if ...]` em 100k | Aloca lista inteira |
| `.count(x)` ou `list.index()` no loop | O(n²) |
| `json.loads(row['payload'])` por item | Re-parse desnecessário |
| `datetime.now()` por item | Custo + imprecisão; use uma vez |
| Tratar exceção no batch todo | Um item ruim mata o job |
| `if chave in dict` seguido de `dict[chave] = ...` | Dois acessos; use `defaultdict` |
| `sorted()` repetido a cada iteração | O(n log n) aplicado várias vezes |
| `pandas` / `numpy` / `pip install` | Runtime do n8n não garante a instalação |
| `print()` para debug em produção | E/S de stdout sem estrutura, invisível para o monitoring |
| Concatenar strings em laço (`s += x`) | Quadrático em CPython por realocação; use `list` + `''.join` |

## Telemetria

O nó Python devolve, junto com os dados, as mesmas métricas do nó JS para que o
monitoring não precise tratar duas linguagens:

| Métrica | Origem | Uso |
|---|---|---|
| `processed` | `len(result)` | Volume efetivamente entregue |
| `inputRows` | `len(rows)` antes do dedupe | Base para calcular a taxa de duplicação |
| `skipped` | contador de `continue` + exceções capturadas | Itens descartados por regra ou por erro |
| `durationMs` | `Date.now()` no nó JS anterior, ou `time.perf_counter()` | Comparação entre execuções |
| `stdlibOnly` | `True` fixo | Confirmação visual de que nenhum import proibido entrou |

Cardinalidade: uma linha por execução. Não emitir uma linha por item ou por categoria
aberta: categorias vêm do dado do cliente e podem ter milhares de valores distintos.

## Plano de teste

| # | Caso | Entrada | Critério de aceite |
|---|---|---|---|
| T1 | Lista vazia | `[]` | `processed = 0`, sem exceção |
| T2 | Payload string JSON | `'{"rows": [...]}'` | Decodificado 1x e processado |
| T3 | Payload já é lista | `[...]` | Nenhum `json.loads` chamado |
| T4 | Campo `score` como texto | `"abc"` | Conta como 0, lote não falha |
| T5 | Campo `id` ausente | `{}` | Item descartado ou agrupado em `sem_tipo` |
| T6 | Unicode | `"São Paulo"`, `"ação"` | Sai íntegro, sem erro de codec |
| T7 | Lote de 1.000 itens | Payload do JS | Processa e devolve agregação correta |
| T8 | 10 lotes sequenciais | Chunking da atividade 2 | Progresso consistente, retomável |
| T9 | Import proibido | Tentativa de `import pandas` | Falha no self-test antes do push |
| T10 | Contrato de saída | Qualquer caso | Lista de `{'json': ...}`, nunca `None` |

**Critério de aceite geral:** T1 a T10 passam, nenhum `import` fora da stdlib
aparece no diff e a cópia no workflow confere com `3-lib/payload-lib.py`.

## Checklist de adesão (antes de publicar o nó)

- [ ] Apenas stdlib (sem import que exige pip)
- [ ] Decodificação JSON feita 1x
- [ ] Dedupe/agregação com `set`/`dict`/`Counter` (O(n))
- [ ] `try/except` por item quando campos são opcionais
- [ ] Retorno no formato que o próximo nó espera (`{ json: ... }`)
- [ ] Nenhum `.count()`, `.index()` ou `in` sobre lista dentro do laço
- [ ] Nenhum `datetime.now()` chamado por item
- [ ] Concatenação de strings via `list` + `join`, se houver laço textual
- [ ] Chunking feito no JS antes, com lote de 1.000 por padrão
- [ ] Exceções contadas em `skipped`, não silenciadas
- [ ] Métricas `processed` e `inputRows` emitidas
- [ ] Casos T1 a T10 executados
- [ ] Cópia conferida contra `3-lib/payload-lib.py`
- [ ] `npx --yes n8nac skills validate` verde no workflow
