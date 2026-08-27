# PDI — Apresentacao: Nós Customizados e Expressões Avançadas n8n

> **Formato:** 15-18 slides | **Tempo:** 20-25 min
> **Audiencia:** Tech Lead + Squad de Automacao

---

## Slide 1: Titulo

```
PDI: NÓS CUSTOMIZADOS E EXPRESSÕES AVANÇADAS
              N8N ENTERPRISE

        Marcos Perettoco — Tech Lead
        Agosto 2026 | FV Marketing / V4
```

---

## Slide 2: O Problema

**Payloads pesados travam porque os nós Code são escritos "do jeito mais fácil"**

- `JSON.parse` repetido dentro do loop → parse desnecessário por item
- `map().filter()` encadeado em 100k itens → 2+ arrays intermediários
- Busca por item (`.find`, `indexOf`) dentro do loop → O(n²)
- `{ ...item }` em cada iteração → pressão de GC / OOM
- Mesma lógica copiada entre dezenas de workflows

**Sintomas reais (atividade 1):** ADPLAN JS timeout 25min; OOM em payloads grandes.

---

## Slide 3: Diagnóstico

```
Nó Code "faz tudo":
  carrega payload inteiro em memória
  re-parseia JSON a cada etapa
  percorre com complexidade O(n²)
  repete código entre workflows
  expressões inline difíceis de manter
```

**Causa raiz:** não existe uma camada padrão de transformação — cada nó reinventa.

---

## Slide 4: A Solução — 3 Frentes

```
┌──────────────────────────────────────────────────┐
│  FRENTE 1: Nós Code JS avançados                │
│  Streaming + chunk + dedupe + memoização (O(n)) │
├──────────────────────────────────────────────────┤
│  FRENTE 2: Nós Code Python no n8n               │
│  Enriquecimento/agregação com stdlib            │
├──────────────────────────────────────────────────┤
│  FRENTE 3: Expressões avançadas + biblioteca    │
│  $('node'), JSONata, static data, 3-lib única   │
└──────────────────────────────────────────────────┘
```

---

## Slide 5: Antes vs Depois

| Antes | Depois |
|-------|--------|
| JSON.parse no loop | Parse 1x na entrada |
| O(n²) (find/indexOf) | O(n) com Set/Map |
| 2+ passadas (map/filter) | UMA passada (filtra+dedupe+transforma) |
| Cópia de objeto por item | Cópia mínima de campos |
| Código duplicado | Biblioteca `3-lib/` única |
| Memória estoura | Streaming + chunking |

---

## Slide 6: Frente 1 — JS Payload Normalizer

```
Webhook /nos/js-normalizer
  → Parse and Chunk (streaming, chunk 1000)
    → Normalize in One Pass (O(n), dedupe Set)
      → Return Metrics (duração, itens/s)
```

- Parse 1x — nunca dentro do loop
- Filtro barato antes de transformação cara
- Dedupe por chave primitiva (`Set`), não por objeto
- Cópia mínima (só os campos necessários)

---

## Slide 7: Frente 2 — Python Payload Enricher

```
Webhook /nos/python-enricher
  → Parse Payload (decode 1x)
    → Enrich Python (set + Counter/defaultdict)
      → Return Summary
```

- Só stdlib (`collections`, `itertools`) — sem pip
- Dedupe O(n) com `set`
- Agregação O(n) com `Counter`/`defaultdict`
- Chunking na camada JS antes, Python enriquece lote a lote

---

## Slide 8: Frente 3 — Expressões & Memo Playground

```
Manual Trigger
  → Generate Sample Data (500 leads)
    → Filter High Score (IF, expressão {{ $json.score }})
      → Memoize Reference ($getWorkflowStaticData)
        → Output Result
```

- Expressão condicional em parâmetros de nós
- `$getWorkflowStaticData('global')` — valor estável cacheador entre execuções
- Referências entre nós (`$('Node').item.json...`)

---

## Slide 9: Biblioteca 3-lib (fonte da verdade)

```
3-lib/
├── payload-lib.js   → chunk, normalizeStream, dedupe, aggregate, memoizeGlobal
└── payload-lib.py   → chunk, dedupe, aggregate, parse_payload, to_output
```

**Regra:** nunca editar um nó Code sem atualizar a lib — a lib é o padrão.

---

## Slide 10: Entregas Concretas

```
PDI/
├── 1-standards/     → 3 padrões (JS, Python, expressões)
├── 2-workflows/     → 3 workflows .workflow.ts (validados com n8nac)
├── 3-lib/           → payload-lib.js + payload-lib.py
├── 4-retrofit/      → Plano de retrofit ADPLAN, PRO ANALISES, CC
├── 5-monitoring/    → Queries de performance + alertas
├── 6-automation/    → deploy-custom-nodes.sh (com gate)
└── 7-apresentacao/  → Este deck
```

---

## Slide 11: Retrofit dos workflows existentes

| Workflow | Correção | Esforço |
|----------|---------|---------|
| ADPLAN | Streaming + dedupe (JS) | 30 min |
| PRO ANALISES | Parse 1x + validação | 10 min |
| CC Collector | Dedupe + agregação O(n) | 20 min |
| CC Metrics | Dedupe + agregação O(n) | 20 min |

Fase 1: Publicar workflows novos (1 dia)
Fase 2: Retrofit (2 dias)
Fase 3: Validação com payload simulado (1 dia)

---

## Slide 12: Métricas de Sucesso

| Métrica | Antes | Meta |
|---------|-------|------|
| Payload 100k itens | OOM / timeout | Streaming < 2 GB pico |
| Complexidade normalização | O(n²) | O(n) |
| Re-parse de JSON | Múltiplos | 1x na entrada |
| Código duplicado | Alto | `3-lib/` única |
| Expressões | Inline, não testáveis | Padronizadas |

---

## Slide 13: Próximos Passos

```
Homologação:
  Seg: Revisar 1-standards + 3-lib
  Ter: Push 3 workflows (n8nac push)
  Qua: Testar com payload 100k + medir itens/s
  Qui: Retrofit ADPLAN + PRO ANALISES + CC
  Sex: Dashboard de performance (5-monitoring)
```

---

## Slide 14: Perguntas?

```
"Payload pesado não trava mais:
  processa em stream, dedupe em O(n),
  código uma vez, biblioteca única."
```

---

## Slide 15: Anexo — Anti-Patterns

| Anti-pattern | Problema |
|---|---|
| `JSON.parse` no loop | Parse desnecessário por item |
| `filter().map()` encadeado | 2 passadas + arrays intermediários |
| `indexOf`/`find` no loop | O(n²) |
| `{...item}` em cada iteração | Pressão de GC / OOM |
| Lógica duplicada em nós Code | Manutenção caótica |
| Python com pandas (sem garantia) | Quebra no runtime do n8n |