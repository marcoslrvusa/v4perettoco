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

**Saída esperada:** três mensagens de validação verde, uma por arquivo.
**Critério de falha:** qualquer `Workflow is invalid` ou erro de sintaxe do transformer.
**Se der errado:** não siga para o push. Abra o arquivo apontado pelo erro, corrija a
decoração `@node`/`@workflow` apontada, rode o validate de novo e só continue quando
os três passarem. Nunca publique workflow que não validou.

## Passo 2: Mostrar a biblioteca reutilizável (3-lib)

- `3-lib/payload-lib.js` → `chunk` · `normalizeStream` · `dedupe` · `aggregate` · `memoizeGlobal`
- `3-lib/payload-lib.py` → `chunk` · `dedupe` · `aggregate` · `parse_payload` · `to_output`
- Regra: lib e a fonte da verdade; nos Code embutem cópias das funções usadas.

**Como mostrar:** abra `payload-lib.js` e destaque o gerador `chunk` (usa `yield`,
não materializa a lista toda) e `normalizeStream` (filtra, dedupe e transforma no
mesmo laço). Depois abra `payload-lib.py` e destaque `chunk` com `itertools.islice`.

**Critério de falha:** se a lib estiver vazia ou divergente do que está embutido nos
workflows, pare a demo: isso é I5 violado (a lib deixou de ser a fonte da verdade).
**Se der errado:** mostre o diff entre a função da lib e a cópia do nó, escolha a
versão nova e registre para sincronizar antes do push.

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

**Saída esperada:** `processedItems: 3`, `deduped: 1`, `success: true`.
**Critério de falha:** `processedItems` diferente de 3, ou `deduped` diferente de 1.
**Se der errado:** confira se o campo de dedupe é `id` e se o filtro barato não está
descartando item válido. Abra a execução no n8n UI e veja o JSON de saída do nó
`Normalize in One Pass` para localizar em qual nó o dado foi perdido.

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

**Saída esperada:** `processedItems` próximo de 100.000, `durationMs` registrado,
`itemsPerSecond` coerente, worker do n8n sem reinício.
**Critério de falha:** execução em `error`, worker reiniciando, ou `durationMs`
acima de 60.000 ms (meta: segundos).
**Se der errado:** (1) valide o JSON gerado com `node -e "JSON.parse(require('fs').readFileSync('/tmp/payload-100k.json','utf8')); console.log('ok')"`;
(2) reduza `chunk_size` para 500 no nó `Parse and Chunk`; (3) confirme que nenhum
`JSON.parse` entrou depois da etapa de entrada.

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

**Saída esperada:** `byTipo` com as contagens corretas e `somaScore` com a soma por
categoria: B2B = 88 + 72 = 160, B2C = 45.
**Critério de falha:** `ModuleNotFoundError`, soma errada, ou retorno que não seja
lista de `{'json': ...}`.
**Se der errado:** abra o nó `Enrich Python` e procure qualquer `import` fora da
stdlib. Se o import for legítimo mas indisponível, refaça a lógica com
`collections` antes de considerar dependência externa.

## Passo 6: Demo Expressões & Memo Playground

```bash
# Rodar manualmente o workflow no n8n UI (Manual Trigger)
# → FilterHighScore filtra score >= 70 via expressao {{ $json.score }}
# → MemoizeReference cacheia o limiar em $getWorkflowStaticData('global')
# → Rodar de novo: cachedAt não muda (memoização entre execuções)
```

**Ponto-chave:** valor estável calculado 1x e reutilizado: demonstra
`$getWorkflowStaticData` na prática.

**Saída esperada:** na 1ª execução `cachedAt` novo; na 2ª execução o mesmo valor.
**Critério de falha:** `cachedAt` diferente entre execuções seguidas, ou limiar
diferente do configurado.
**Se der errado:** confira se a chave do static data está versionada (`limiar:v2`)
e se alguém limpou o workflow static data no UI entre as execuções.

## Passo 7: Retrofit e monitoramento

- Mostrar `4-retrofit/RETROFIT.md` (ADPLAN, PRO ANÁLISES, CC Collector/Metrics)
- Mostrar `5-monitoring/QUERIES.md` (mt_payload_metrics + alertas de duração)

**Como mostrar:** abra a tabela de alvos do RETROFIT e aponte o sintoma de cada
linha (timeout de 25 min, `toDateTime` undefined, payload re-processado). Em
seguida rode a consulta §3 do QUERIES.md e explique a leitura da tendência horária.

**Critério de falha:** query que falha por tabela inexistente é esperado antes da
criação opcional; query que falha por erro de sintaxe não é.
**Se der errado:** comente a criação da tabela `mt_payload_metrics` (§6) e mostre
apenas a DDL, sem executar: a criação acontece após a homologação.

## Passo 8: Gate de deploy em modo dry-run

```bash
bash 6-automation/deploy-custom-nodes.sh --dry-run
```

**Saída esperada:** lista dos três workflows com `Workflow is valid` e a mensagem
de que o deploy real está bloqueado.
**Critério de falha:** qualquer workflow inválido, ou saída diferente de
"DRY-RUN: validando workflows".
**Se der errado:** não tente rodar sem `--dry-run`: o script bloqueia de propósito e
essa trava é parte da evidência de controle de mudança.

## Passo 9: Teste de borda com payload malformado

```bash
curl -X POST http://localhost:5678/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' \
  -d '{"payload": "{isto nao e json valido}"}'
```

**Saída esperada:** resposta estruturada com flag de erro de parse (não uma lista
vazia silenciosa) e a execução encerrando sem derrubar o workflow.
**Critério de falha:** retorno `processedItems: 0` sem nenhuma indicação de erro.
**Se der errado:** ajuste o nó `Parse and Chunk` para expor `parseError` e
reexecute: zero silencioso é pior que erro explícito, porque máscara falha do
produtor.

## Passo 10: Teste de borda com itens inválidos

```bash
curl -X POST http://localhost:5678/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' \
  -d '{"payload": [{"id":4,"name":"Valido","score":90},{"name":"Sem id"},null,{"id":5,"name":"Tambem valido","score":10}]}'
```

**Saída esperada:** `processedItems: 2`; os itens sem `id` e o `null` são
descartados sem exceção.
**Critério de falha:** a execução inteira vai para `error` por causa de um item.
**Se der errado:** o filtro barato está ausente ou depois da transformação; inverta
a ordem no nó `Normalize in One Pass`.

## Passo 11: Contagem de operações antes e depois (prova de O(n))

```bash
# Conta as construções proibidas em todos os workflows
grep -c "JSON.parse" 2-workflows/*.workflow.ts
grep -c "\.find(\|\.indexOf(\|includes(" 2-workflows/*.workflow.ts
```

**Saída esperada:** `JSON.parse` aparece apenas no nó de entrada de cada workflow;
zero ocorrências de busca por item dentro de laço.
**Critério de falha:** qualquer `.find(` ou `.indexOf(` num nó que percorra lista
grande.
**Se der errado:** identifique o nó, troque por `Set`/`Map` e valide de novo antes
de qualquer push.

## Passo 12: Conferência da lib contra as cópias

```bash
grep -n "function\* chunk\|normalizeStream\|memoizeGlobal" 3-lib/payload-lib.js
grep -n "def chunk\|def dedupe\|def aggregate" 3-lib/payload-lib.py
```

**Saída esperada:** as seis funções JS e as cinco Python presentes e com assinatura
igual à das cópias embutidas nos workflows.
**Critério de falha:** função existente na lib e ausente nos nós (ou o contrário,
com assinatura divergente).
**Se der errado:** sincronize para o lado da lib, pois ela é a fonte da verdade,
e registre a mudança em `3-lib/README.md`.

## Passo 13: Simulação do alerta de regressão

```sql
SELECT workflow_name, duration_ms, items_per_second, executed_at
FROM mt_payload_metrics
WHERE duration_ms > 60000
ORDER BY duration_ms DESC;
```

**Saída esperada:** consulta aceita (mesmo que retorne zero linhas antes da criação
da tabela).
**Critério de falha:** erro de sintaxe, ou alerta configurado apontando para coluna
inexistente.
**Se der errado:** confira o DDL do §6 de `5-monitoring/QUERIES.md` e crie a tabela
somente após a homologação.

## Passo 14: Rollback ensaiado em um workflow

```bash
git status --short "2-workflows/"
git diff --stat "2-workflows/"
# Exercício: reverta um único arquivo e valide novamente
npx -y n8nac skills validate "2-workflows/[CC] NOS - Expressions & Memo Playground.workflow.ts"
```

**Saída esperada:** diff limpo (nada alterado durante a demo) e validate verde.
**Critério de falha:** mais de um workflow alterado ao mesmo tempo.
**Se der errado:** rollback sempre é por arquivo: um workflow revertido não pode
arrastar os outros dois junto.

## Passo 15: Checklist de homologação em voz alta

- [ ] 3 padrões revisados e assinados pelo time
- [ ] 3 workflows validados (`Workflow is valid`)
- [ ] Smoke test de 10 itens OK
- [ ] Carga de 100k itens OK, sem OOM
- [ ] Payload malformado sinalizado, não silenciado
- [ ] Itens inválidos descartados sem derrubar o lote
- [ ] Python apenas stdlib
- [ ] Memoização estável entre duas execuções
- [ ] Lib conferida contra as cópias
- [ ] Dry-run do deploy OK
- [ ] Consultas de monitoring aceitas
- [ ] Rollback por arquivo demonstrado

**Critério de falha:** qualquer item desmarcado bloqueia a publicação.
**Se der errado:** retome o passo correspondente desta lista; nenhum item pode ser
pulado por pressa.

## Sucesso

- ✅ 3 workflows validados com n8nac (`Workflow is valid`)
- ✅ Dedupe O(n) em UMA passada (JS) demonstrado com 100k itens
- ✅ Agregação Python apenas stdlib (Counter/defaultdict)
- ✅ Memoização entre execuções (`$getWorkflowStaticData`)
- ✅ Biblioteca `3-lib/` como fonte única de transformação

## Observação

Nenhum workflow foi publicado no n8n. Publicação somente após homologação,
com confirmação explícita via `bash 6-automation/deploy-custom-nodes.sh --dry-run`.