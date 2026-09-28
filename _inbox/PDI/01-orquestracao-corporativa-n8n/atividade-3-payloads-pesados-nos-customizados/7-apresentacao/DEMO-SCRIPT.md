# Script de Demonstração: Nós Customizados e Expressões Avançadas n8n (PDI-NOS-CUSTOMIZADOS)

> Homologação simulada. NENHUM passo publica em produção.

## Setup

```bash
npx n8nac env status --json

tree _inbox/PDI/01-orquestracao-corporativa-n8n/atividade-3-payloads-pesados-nos-customizados/
```

## Passo 1: Validar Workflows (n8nac, sem push)

```bash
npx -y n8nac skills validate "2-workflows/[CC] NOS - JS Payload Normalizer.workflow.ts"
npx -y n8nac skills validate "2-workflows/[CC] NOS - Python Payload Enricher.workflow.ts"
npx -y n8nac skills validate "2-workflows/[CC] NOS - Expressions & Memo Playground.workflow.ts"
# Todos devem acusar: ✅ Workflow is valid
```

## Passo 2: Mostrar a biblioteca reutilizável (3-lib)

- `3-lib/payload-lib.js` → `chunk` · `normalizeStream` · `dedupe` · `aggregate` · `memoizeGlobal`
- `3-lib/payload-lib.py` → `chunk` · `dedupe` · `aggregate` · `parse_payload` · `to_output`
- Regra: lib e a fonte da verdade; nos Code embutem cópias das funções usadas.

## Passo 3: Demo JS Payload Normalizer (dedupe + normalização O(n))

> Para a demo, rodar localmente (`n8n start`) ou em instância de teste.

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

**Ponto-chave:** id duplicado entrou 2x e saiu 1x: dedupe por chave primitiva
(`Set`), em UMA passada (O(n)), sem copiar o objeto inteiro por item.

## Passo 4: Escalar para payload pesado (prova de streaming)

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

## Passo 5: Demo Python Payload Enricher (agregação stdlib)

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

**Ponto-chave:** agregação com `Counter`/`defaultdict` (O(n)) e apenas stdlib.

## Passo 6: Demo Expressões & Memo Playground

```bash
# Rodar manualmente o workflow no n8n UI (Manual Trigger)
# → FilterHighScore filtra score >= 70 via expressao {{ $json.score }}
# → MemoizeReference cacheia o limiar em $getWorkflowStaticData('global')
# → Rodar de novo: cachedAt não muda (memoização entre execuções)
```

**Ponto-chave:** valor estável calculado 1x e reutilizado: demonstra
`$getWorkflowStaticData` na prática.

## Passo 7: Retrofit e monitoramento

- Mostrar `4-retrofit/RETROFIT.md` (ADPLAN, PRO ANÁLISES, CC Collector/Metrics)
- Mostrar `5-monitoring/QUERIES.md` (mt_payload_metrics + alertas de duração)

## Sucesso

- ✅ 3 workflows validados com n8nac (`Workflow is valid`)
- ✅ Dedupe O(n) em UMA passada (JS) demonstrado com 100k itens
- ✅ Agregação Python apenas stdlib (Counter/defaultdict)
- ✅ Memoização entre execuções (`$getWorkflowStaticData`)
- ✅ Biblioteca `3-lib/` como fonte única de transformação

## Observação

Nenhum workflow foi publicado no n8n. Publicação somente após homologação,
com confirmação explícita via `bash 6-automation/deploy-custom-nodes.sh --dry-run`.