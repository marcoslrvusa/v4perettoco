# Standard: Nós Code JavaScript em Payloads Pesados

> **Objetivo:** regra única para escrever nós `Code` (JS) que processam payloads
> pesados (10k+ itens) de forma streaming, incremental e com memória controlada.

## Escopo e não-escopo

**Escopo:** nós `n8n-nodes-base.code` com `language: 'javaScript'` que recebem 10.000
itens ou mais em `$input.all()` ou `$input.first().json`, com qualquer combinação de
filtro, dedupe, normalização, agregação ou enriquecimento. Cobreme também os nós que
recebem payload como string JSON e precisam decodificá-lo uma única vez.

**Não-escopo:** (a) transformações de um único item que cabem em expressão `{{ ... }}`,
cobertas pelo `STANDARD-EXPRESSIONS.md`; (b) chamadas de rede e gravação em banco,
que pertencem aos nós nativos HTTP/Supabase; (c) geração de conteúdo por IA, fora
desta trilha; (d) custom nodes TypeScript compilados, deliberadamente descartados
como alternativa (ver README, Decisões e tradeoffs).

## Termos

| Termo | Significado operacional neste standard |
|---|---|
| Item | Objeto `{ json: ... }` no formato que o n8n passa entre nós |
| Passada | Um laço `for` percorrendo a lista inteira uma única vez |
| Chave de dedupe | Campo primitivo (`id`, `slug`) que identifica o item de forma única |
| Cópia mínima | Novo objeto contendo somente os campos que o downstream consome |
| Lote (chunk) | Fatia do payload processada como unidade, default 1000 itens |
| Sair cedo | `continue` antes de qualquer transformação cara quando o item falha no filtro |
| Memoização | Reúso de valor estável gravado em `$getWorkflowStaticData('global')` |

## Princípios

1. **Nunca carregue o payload inteiro em memória**: processe em chunks com
   geradores (`function*`) ou iteração incremental.
2. **Uma única normalização por campo**: evite re-processar o mesmo item em
   múltiplas passadas (complexidade O(n²) é proibida em listas grandes).
3. **Reduza cópias de objetos**: `{ ...item }` para cada item em um loop de 100k
   gera pressão enorme no GC. Use mutação controlada ou Stream/Transform.
4. **Parse de JSON 1x na entrada**: o payload chega como string; parses só na
   primeira etapa, nunca dentro de loops.
5. **Saía cedo**: se o item não passou no filtro, descarte antes de normalizar.
6. **Use `$getWorkflowStaticData('global')`** para memoização entre execuções.

Esses seis princípios não são sugestão de estilo: cada um corresponde a um modo de
falha observado (OOM, timeout, event loop bloqueado) e a um item do checklist de
adesão ao final deste documento. Quando dois princípios parecerem conflitar na
prática, o desempate é: primeiro estabilizar a memória (1 e 3), depois o custo
computacional (2 e 4), depois a manutenção (5 e 6).

## Template recomendado

```javascript
// runOnceForAllItems: recebe TODOS os itens de uma vez
const items = $input.all();
const seen = new Set();
const out = [];

for (const item of items) {
  // 1) Filtro barato primeiro
  if (!item.json || !item.json.id) continue;

  // 2) Chave de dedupe: evita Set de objetos inteiros (custo alto)
  const key = String(item.json.id);
  if (seen.has(key)) continue;
  seen.add(key);

  // 3) Transformação mínima: evita spread grande desnecessário
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

Adaptação do template para entrada que chega como string (caso dos webhooks da
atividade 3): mova o `JSON.parse` para antes do laço e proteja-o, porque um JSON
quebrado não pode virar lista vazia em silêncio.

```javascript
const raw = $input.first().json;
let rows = raw.payload;
let parseError = null;

if (typeof rows === 'string') {
  try {
    rows = JSON.parse(rows);
  } catch (e) {
    parseError = String(e && e.message ? e.message : e);
    rows = [];
  }
}
if (!Array.isArray(rows)) rows = rows && rows.rows ? rows.rows : [];

// o nó de saída precisa expor parseError: zero silencioso é pior que erro explícito
```

## Regra canônica

Todo nó Code JS de payload pesado deve se enquadrar em exatamente um destes formatos:

**Formato A, passada única (padrão):**

```javascript
// 1 entrada + 1 laço + 1 saída. Nada de pipeline encadeado.
const rows = decodificar($input.first().json);   // parse 1x, fora do laço
const seen = new Set();
const out = [];

for (const row of rows) {
  if (!row || !row.id) continue;                 // filtro barato primeiro
  const key = String(row.id);
  if (seen.has(key)) continue;                   // dedupe indexado
  seen.add(key);
  out.push({ json: minimizar(row) });            // cópia mínima
}
return out;
```

**Formato B, gerador de lotes (quando a memória não comporta a lista inteira):**

```javascript
function* lotes(rows, tamanho) {
  for (let i = 0; i < rows.length; i += tamanho) {
    yield rows.slice(i, i + tamanho);
  }
}
```

A regra formal é: para $n$ itens, o nó executa no máximo $c \cdot n$ operações, com
$c$ constante pequena (hash, comparação, projeção de campos). Qualquer construção
que introduza um laço aninhado sobre a mesma lista viola o standard, mesmo que
pareça mais legível:

```javascript
// PROIBIDO: laço aninhado implícito sobre a mesma lista
const unicos = rows.filter((r, i) =>
  rows.findIndex((x) => x.id === r.id) === i);   // O(n²) mascarado de "limpeza"
```

## Exemplo numérico

**Exemplo numérico:** payload de $n = 100.000$ itens, 5% inválidos, 15% duplicados.

- Itens percorridos: 100.000 (uma passada).
- Descartados pelo filtro barato: 5.000 (custo: 1 comparação cada).
- Descartados pelo `Set`: 14.250 (custo: hash + lookup cada).
- Objetos criados: 80.750, cada um com 3 campos em vez dos 12 originais.
- Operações totais de ordem grande: $\approx 100.000 \times 4 = 400.000$.
- Na versão proibida (`.findIndex` dentro de `filter`): $\approx \frac{100000^2}{2}
  = 5 \times 10^{9}$ comparações, cerca de 50 s a 10 ns cada, contra cerca de 4 ms
  na versão canônica.

## Tabela de decisão

| Se | E | Então |
|---|---|---|
| A lista tem >= 10.000 itens | Precisa de dedupe | `Set` de chave primitiva em passada única |
| A lista tem >= 10.000 itens | Não precisa de dedupe | Ainda assim, uma passada só, com filtro no mesmo laço |
| O nó precisa de agregação | Chaves são baixas cardinalidades | `Map` acumulador, uma passada |
| O nó precisa de ordenação | n grande | `sort` uma vez, nunca reordenar por etapa |
| O payload chega como string | Sempre | `JSON.parse` no nó de entrada, protegido por `try/catch` |
| O processamento é independente por item | Sem estado entre itens | `runOnceForEachItem` é aceitável, mas prefira `runOnceForAllItems` para controlar memória |
| O nó precisa de contexto completo (dedupe global, total) | Sempre | `runOnceForAllItems` |
| O valor é estável entre execuções | Configuração/limiar | `memoizeGlobal` com chave versionada |
| O downstream só consome 3 campos | Sempre | Cópia mínima explícita, nunca `{ ...row }` |

## Anti-patterns

| Anti-pattern | Problema |
|---|---|
| `items.map(...)` em 100k itens | Aloca array inteiro novo + cópias |
| `items.filter(...).map(...)` encadeado | Duas passadas + 2 arrays intermediários |
| `JSON.parse` dentro do loop | Parse desnecessário por item |
| `{ ...item }` em cada iteração | Pressão de GC / OOM |
| Buscar por item (`.find`/`.includes` em array) | O(n²) |
| `JSON.stringify(item)` como chave de dedupe | Serialização por item, mais lenta que primitiva e propensa a colisão de ordem de campos |
| `new Map(items.map(i => [i.id, i]))` construído duas vezes | Mapa reconstruído, memória dobrada sem necessidade |
| `await` dentro de laço de 100k itens | 100k promessas encadeadas, latência multiplicativa |
| `console.log` de item inteiro por iteração | E/S de log dominando o tempo total de execução |
| Mutar `$input.all()` diretamente | Estado compartilhado entre nós, efeito colateral imprevisível |

## Decisões de configuração

- `mode: 'runOnceForAllItems'`: quando o nó precisa do contexto completo
  (dedupe, ordenação, agregação).
- `mode: 'runOnceForEachItem'`: quando o processamento é independente por item.
  Em payloads pesados prefira `runOnceForAllItems` + loop para controlar memória.

Por que essa preferência: em `runOnceForEachItem` o n8n instância o contexto do nó
uma vez por item, o que adiciona overhead fixo por item em payloads de 100k e impede
dedupe global, já que cada item enxerga apenas a si mesmo. O custo de `runOnceForAllItems`
é um array de referências na memória, muito menor que uma execução de contexto por item.

| `mode` | Custo fixo | Dedupe global | Quando escolher |
|---|---|---|---|
| `runOnceForAllItems` | 1 execução + array de referências | Sim | Padrão da trilha |
| `runOnceForEachItem` | 1 execução por item | Não | Só quando n for pequeno e o item não depender de vizinhos |

Outras configurações relevantes do nó:

| Parâmetro | Valor adotado | Justificativa |
|---|---|---|
| `language` | `javaScript` | Runtime mais previsível para CPU intensiva; Python fica para agregação (ver `STANDARD-CODE-PYTHON.md`) |
| `jsCode` com `return` de array | `{ json }` explícito | Contrato estável para o próximo nó |
| Tempo de execução do workflow | `executionOrder: 'v1'` | Sem paralelismo implícito entre nós, para `durationMs` significativo |

## Telemetria

Todo nó de transformação termina emitindo um objeto de métrica com cardinalidade
controlada (uma linha por execução, não por item):

| Métrica | Tipo | Cardinalidade | Alerta |
|---|---|---|---|
| `processedItems` | inteiro | 1 por execução | Queda abrupta vs baseline |
| `deduped` | inteiro | 1 por execução | `deduped / total > 50%` sugere produtor duplicando |
| `durationMs` | inteiro | 1 por execução | `> 60.000` (regressão) |
| `itemsPerSecond` | inteiro | 1 por execução | Queda > 50% vs média de 24 h |
| `totalItems` | inteiro | 1 por execução | `= 0` em payload que deveria ter dados |

Grave via nó Supabase na tabela opcional `mt_payload_metrics` (`5-monitoring/QUERIES.md`).
Não emitir métrica por item: 100.000 linhas por execução destrói qualquer painel.

## Plano de teste

| # | Caso | Entrada esperada | Critério de aceite |
|---|---|---|---|
| T1 | Payload vazio `[]` | `processedItems = 0`, sem exceção | `success: true` |
| T2 | Payload nulo / ausente | Fallback para `[]` | Não lança erro |
| T3 | Itens sem `id` | Descartados pelo filtro barato | Não entram na saída |
| T4 | Duplicatas exatas | Mantém a primeira ocorrência | `deduped` correto |
| T5 | Unicode e acentos em `name` | `String(row.name)` preserva `ç`, `ã`, `é` | Sem `?` na saída |
| T6 | `score` como string numérica | `Number(row.score)` converte | Saída numérica |
| T7 | Limite de 100k itens | Processa sem OOM | Pico < 2 GB (meta) |
| T8 | JSON malformado como string | `catch` sinaliza erro de parse | Flag de erro visível, não `[]` silencioso |
| T9 | Execução duas vezes seguidas | Métrica de duração coerente | Sem estado vazando entre execuções |
| T10 | Regressão de complexidade | Comparar `durationMs` de T7 antes/depois do retrofit | Ganho medido e registrado |

**Critério de aceite geral:** os 10 casos passam, `n8nac skills validate` acusa
`Workflow is valid` e o checklist de adesão abaixo está integralmente marcado.

## Checklist de adesão (antes de publicar o nó)

- [ ] Nenhum `JSON.parse` dentro de loop
- [ ] Nenhuma busca por item dentro de loop (O(n²))
- [ ] Dedupe com `Set` de chave primitiva, não de objeto
- [ ] Cópias de objeto limitadas ao mínimo de campos necessários
- [ ] Memória: teste com payload de 100k antes de publicar
- [ ] Filtro barato executado antes de qualquer transformação
- [ ] Uma única passada para filtrar + deduzir + transformar
- [ ] `mode` escolhido de forma consciente (`runOnceForAllItems` por padrão)
- [ ] Nenhum `console.log` por item no código que vai para produção
- [ ] Nenhum `await` dentro de laço de lista grande
- [ ] Métricas `durationMs` e `itemsPerSecond` emitidas ao final
- [ ] Casos T1 a T10 executados e resultados anotados
- [ ] Cópia das funções conferida contra `3-lib/payload-lib.js`
- [ ] `npx --yes n8nac skills validate` verde no workflow que contém o nó
