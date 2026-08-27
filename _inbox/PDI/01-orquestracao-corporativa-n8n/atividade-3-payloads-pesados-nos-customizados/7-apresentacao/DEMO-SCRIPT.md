# Script de Demonstracao — Nós Customizados e Expressões Avançadas n8n (PDI-NOS-CUSTOMIZADOS)

> Homologacao simulada. NENHUM passo publica em producao.

## Setup

```bash
npx n8nac env status --json

tree _inbox/PDI/01-orquestracao-corporativa-n8n/atividade-3-payloads-pesados-nos-customizados/
```

## Passo 1 — Validar Workflows (n8nac, sem push)

```bash
npx -y n8nac skills validate "2-workflows/[CC] NOS - JS Payload Normalizer.workflow.ts"
npx -y n8nac skills validate "2-workflows/[CC] NOS - Python Payload Enricher.workflow.ts"
npx -y n8nac skills validate "2-workflows/[CC] NOS - Expressions & Memo Playground.workflow.ts"
# Todos devem acusar: ✅ Workflow is valid
```

## Passo 2 — Mostrar a biblioteca reutilizavel (3-lib)

- `3-lib/payload-lib.js` → `chunk` · `normalizeStream` · `dedupe` · `aggregate` · `memoizeGlobal`
- `3-lib/payload-lib.py` → `chunk` · `dedupe` · `aggregate` · `parse_payload` · `to_output`
- Regra: lib e a fonte da verdade; nos Code embutem copias das funcoes usadas.

## Passo 3 — Demo JS Payload Normalizer (dedupe + normalizacao O(n))

> Para a demo, rodar localmente (`n8n start`) ou em instancia de teste.

```bash
curl -X POST http://localhost:5678/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' \
  -d '{
    "payload": [
      {"id":1,"name":"Lead A","score":88},
      {"id":1,"name":"Lead A","score":88},
      {"id":2,"name":"Lead B","score":45},
      {"id":3,"name":"Lead C","score":72}
    ]
  }'
# → {"success":true,"processedItems":3,"deduped":1,"itemsPerSecond":...}
```

**Ponto-chave:** id duplicado entrou 2x e saiu 1x — dedupe por chave primitiva
(`Set`), em UMA passada (O(n)), sem copiar o objeto inteiro por item.

## Passo 4 — Escalar para payload pesado (prova de streaming)

```bash
# Gerar 100k itens e enviar ao mesmo webhook
node -e '
  const rows = [];
  for (let i = 0; i < 100000; i++) rows.push({id: i, name: "Lead "+i, score: Math.floor(Math.random()*100)});
  console.log(JSON.stringify({payload: rows}));
' > /tmp/payload-100k.json

curl -X POST http://localhost:5678/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' \
  --data @/tmp/payload-100k.json
# → success, processedItems ~100k, durationMs e itemsPerSecond reportados
```

**Ponto-chave:** mesmo processo (chunk 1000) aguenta 100k sem estourar o event loop.

## Passo 5 — Demo Python Payload Enricher (agregacao stdlib)

```bash
curl -X POST http://localhost:5678/webhook/nos/python-enricher \
  -H 'Content-Type: application/json' \
  -d '{
    "payload": [
      {"id":1,"tipo":"B2B","score":88},
      {"id":2,"tipo":"B2C","score":45},
      {"id":3,"tipo":"B2B","score":72}
    ]
  }'
# → {"success":true,"processedItems":3,"byTipo":{"B2B":2,"B2C":1},"somaScore":{"B2B":160,"B2C":45}}
```

**Ponto-chave:** agregacao com `Counter`/`defaultdict` (O(n)) e apenas stdlib.

## Passo 6 — Demo Expressões & Memo Playground

```bash
# Rodar manualmente o workflow no n8n UI (Manual Trigger)
# → FilterHighScore filtra score >= 70 via expressao {{ $json.score }}
# → MemoizeReference cacheia o limiar em $getWorkflowStaticData('global')
# → Rodar de novo: cachedAt nao muda (memoizacao entre execucoes)
```

**Ponto-chave:** valor estavel calculado 1x e reutilizado — demonstra
`$getWorkflowStaticData` na pratica.

## Passo 7 — Retrofit e monitoramento

- Mostrar `4-retrofit/RETROFIT.md` (ADPLAN, PRO ANALISES, CC Collector/Metrics)
- Mostrar `5-monitoring/QUERIES.md` (mt_payload_metrics + alertas de duracao)

## Sucesso

- ✅ 3 workflows validados com n8nac (`Workflow is valid`)
- ✅ Dedupe O(n) em UMA passada (JS) demonstrado com 100k itens
- ✅ Agregacao Python apenas stdlib (Counter/defaultdict)
- ✅ Memoizacao entre execucoes (`$getWorkflowStaticData`)
- ✅ Biblioteca `3-lib/` como fonte unica de transformacao

## Observacao

Nenhum workflow foi publicado no n8n. Publicacao somente apos homologacao,
com confirmacao explicita via `bash 6-automation/deploy-custom-nodes.sh --dry-run`.