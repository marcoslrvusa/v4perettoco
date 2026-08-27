# Standard — Nós Code JavaScript em Payloads Pesados

> **Objetivo:** regra única para escrever nós `Code` (JS) que processam payloads
> pesados (10k+ itens) de forma streaming, incremental e com memória controlada.

## Princípios

1. **Nunca carregue o payload inteiro em memória** — processe em chunks com
   geradores (`function*`) ou iteração incremental.
2. **Uma única normalização por campo** — evite re-processar o mesmo item em
   múltiplas passadas (complexidade O(n²) é proibida em listas grandes).
3. **Reduza cópias de objetos** — `{ ...item }` para cada item em um loop de 100k
   gera pressão enorme no GC. Use mutação controlada ou Stream/Transform.
4. **Parse de JSON 1x na entrada** — o payload chega como string; parses só na
   primeira etapa, nunca dentro de loops.
5. **Saia cedo** — se o item não passou no filtro, descarte antes de normalizar.
6. **Use `$getWorkflowStaticData('global')`** para memoização entre execuções.

## Template recomendado

```javascript
// runOnceForAllItems — recebe TODOS os itens de uma vez
const items = $input.all();
const seen = new Set();
const out = [];

for (const item of items) {
  // 1) Filtro barato primeiro
  if (!item.json || !item.json.id) continue;

  // 2) Chave de dedupe — evita Set de objetos inteiros (custo alto)
  const key = String(item.json.id);
  if (seen.has(key)) continue;
  seen.add(key);

  // 3) Transformação mínima — evita spread grande desnecessário
  const j = item.json;
  out.push({
    json: {
      id: j.id,
      name: normalizeName(j.name),
      ts: parseDate(j.ts),
    },
  });
}

return out;
```

## Anti-patterns

| Anti-pattern | Problema |
|---|---|
| `items.map(...)` em 100k itens | Aloca array inteiro novo + cópias |
| `items.filter(...).map(...)` encadeado | Duas passadas + 2 arrays intermediários |
| `JSON.parse` dentro do loop | Parse desnecessário por item |
| `{ ...item }` em cada iteração | Pressão de GC / OOM |
| Buscar por item (`.find`/`.includes` em array) | O(n²) |

## Decisões de configuração

- `mode: 'runOnceForAllItems'` — quando o nó precisa do contexto completo
  (dedupe, ordenação, agregação).
- `mode: 'runOnceForEachItem'` — quando o processamento é independente por item.
  Em payloads pesados prefira `runOnceForAllItems` + loop para controlar memória.

## Checagem (antes de publicar)

- [ ] Nenhum `JSON.parse` dentro de loop
- [ ] Nenhuma busca por item dentro de loop (O(n²))
- [ ] Dedupe com `Set` de chave primitiva, não de objeto
- [ ] Cópias de objeto limitadas ao mínimo de campos necessários
- [ ] Memória: teste com payload de 100k antes de publicar