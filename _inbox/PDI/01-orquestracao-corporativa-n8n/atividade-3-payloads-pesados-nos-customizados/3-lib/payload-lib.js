// ============================================================
// payload-lib.js — Biblioteca reutilizável de nós Code JS
// PDI A3: Nós customizados / expressões avançadas
// Use como referência para colar (copiar) dentro de nós Code.
// ============================================================

// ------------------------------------------------------------
// 1) Chunking streaming — processa em lotes sem carregar tudo
// ------------------------------------------------------------
export function* chunk(items, size = 100) {
  for (let i = 0; i < items.length; i += size) {
    yield items.slice(i, i + size);
  }
}

// ------------------------------------------------------------
// 2) Normalização em UMA passada (O(n))
//    Filtra + dedupe + transforma no mesmo loop.
// ------------------------------------------------------------
export function normalizeStream(items, opts = {}) {
  const { dedupeKey = 'id', map = (j) => j } = opts;
  const seen = new Set();
  const out = [];

  for (const item of items) {
    const j = item.json || item;
    if (opts.filter && !opts.filter(j)) continue;

    const key = j[dedupeKey];
    if (key !== undefined) {
      if (seen.has(key)) continue;
      seen.add(key);
    }

    out.push({ json: map(j) });
  }
  return out;
}

// ------------------------------------------------------------
// 3) Dedupe por chave primitiva (nunca por objeto)
// ------------------------------------------------------------
export function dedupe(items, keyFn) {
  const seen = new Set();
  return items.filter((item) => {
    const key = keyFn(item.json);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

// ------------------------------------------------------------
// 4) Agregação com Map (O(n), evita busca por item)
// ------------------------------------------------------------
export function aggregate(items, keyFn, reduce) {
  const map = new Map();
  for (const item of items) {
    const key = keyFn(item.json);
    if (!map.has(key)) map.set(key, { key, count: 0, acc: undefined });
    const entry = map.get(key);
    entry.count += 1;
    entry.acc = reduce ? reduce(entry.acc, item.json) : entry.acc;
  }
  return [...map.values()];
}

// ------------------------------------------------------------
// 5) Memoização entre execuções ($getWorkflowStaticData)
// ------------------------------------------------------------
export function memoizeGlobal(key, computeFn) {
  const data = $getWorkflowStaticData('global');
  if (data[key] === undefined) data[key] = computeFn();
  return data[key];
}

// ------------------------------------------------------------
// 6) Saída para n8n (garante formato { json })
// ------------------------------------------------------------
export function toOutput(rows) {
  return rows.map((json) => ({ json }));
}

// ------------------------------------------------------------
// Exemplo de uso dentro de um nó Code:
//
//   const { chunk, normalizeStream, toOutput } = ...
//   const items = $input.all();
//   const normalized = normalizeStream(items, {
//     dedupeKey: 'id',
//     filter: (j) => j.score >= 70,
//     map: (j) => ({ id: j.id, name: String(j.name).toUpperCase() }),
//   });
//   return toOutput(normalized);
// ------------------------------------------------------------