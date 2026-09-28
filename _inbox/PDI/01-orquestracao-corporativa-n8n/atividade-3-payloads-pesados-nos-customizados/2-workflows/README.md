# Workflows: PDI-NOS-CUSTOMIZADOS (payloads pesados)

Workflows n8n desenvolvidos para a terceira atividade do PDI. **Não publicar em
produção ainda**: aguardando homologação da apresentação.

## Componentes

| # | Workflow | Tipo | Propósito |
|---|----------|------|-----------|
| 1 | `[CC] NOS - JS Payload Normalizer` | Webhook (`/nos/js-normalizer`) | Parse 1x, chunking streaming, dedupe O(n) e normalização em UMA passada (JS) |
| 2 | `[CC] NOS - Python Payload Enricher` | Webhook (`/nos/python-enricher`) | Enriquecimento/agregacao em Python com stdlib (dedupe set + Counter/defaultdict) |
| 3 | `[CC] NOS - Expressions & Memo Playground` | Manual | Demonstra expressões avançadas (IF, referência) + memoização com `$getWorkflowStaticData` |

## Arquitetura

```
[1] JS Payload Normalizer
  Webhook ──▶ ParseAndChunk (streaming) ──▶ NormalizeInOnePass (O(n)) ──▶ Metrics
[2] Python Payload Enricher
  Webhook ──▶ ParsePayload (decode 1x) ──▶ EnrichPython (set/Counter) ──▶ Summary
[3] Expressions & Memo Playground
  Manual ──▶ GenerateSampleData ──▶ FilterHighScore (IF) ──▶ MemoizeReference ──▶ Output
```

## Dependências

- Nenhuma credencial externa: apenas nos `Code` (JS/Python).
- Lógica reutilizável: `../3-lib/payload-lib.js` e `payload-lib.py`
  (fonte da verdade; os workflows embutem cópias das funções usadas).

## Como usar (quando autorizado a publicar)

1. `npx --yes n8nac push "2-workflows/[CC] NOS - JS Payload Normalizer.workflow.ts"`
   (e demais).
2. Ativar os webhooks desejados.
3. Testar:

```bash
curl -X POST https://n8n.fvmarketing.com.br/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' \
  -d '{"payload": [{"id":1,"name":"Lead A","score":88}, {"id":1,"name":"Lead A","score":88}, {"id":2,"name":"Lead B","score":45}]}'
```

Esperado no JS Normalizer: `processedItems: 2`, `deduped: 1`.

> **Status: NÃO publicado.** Workflows validados com n8nac (`Workflow is valid`).
> Publicar somente após homologação da apresentação.

## Configuração

| Parâmetro | Valor default | Onde |
|-----------|--------------|------|
| Chunk size (JS Normalizer) | 1000 itens | Node `Parse and Chunk` |
| Limiar de score (Playground) | 70 | Node `Filter High Score` |
| Paths de webhook | `/nos/*` | Nodes Webhook |

## Contratos de entrada e saída

Cada workflow define um contrato simples, que é o que permite testar sem subir
nenhuma dependência externa.

**JS Payload Normalizer**

| Campo | Tipo | Observação |
|---|---|---|
| `payload` | string JSON ou array | Aceita os dois formatos; a string é decodificada 1x |
| `chunk_size` | inteiro, opcional | Default 1000; valores baixos reduzem pico de heap |
| Saída `totalItems` | inteiro | Volume bruto recebido |
| Saída `processedItems` | inteiro | Volume depois do filtro e do dedupe |
| Saída `deduped` | inteiro | `totalItems - processedItems` |
| Saída `durationMs` | inteiro | Medido a partir de `startedAt` do nó de entrada |
| Saída `itemsPerSecond` | inteiro | `processedItems / (durationMs / 1000)`, arredondado |

**Python Payload Enricher**

| Campo | Tipo | Observação |
|---|---|---|
| `payload` | array de objetos com `tipo` e `score` | Processado em passada única |
| Saída `byTipo` | objeto | Contagem por categoria (`Counter`) |
| Saída `somaScore` | objeto | Soma de `score` por categoria (`defaultdict`) |
| Saída `processed` | inteiro | Itens válidos entregues |

**Expressions & Memo Playground**

| Campo | Tipo | Observação |
|---|---|---|
| Entrada | nenhuma | Manual Trigger gera 500 leads de amostra |
| Limiar | número, fixo em 70 | Aplicado pela expressão no nó `Filter High Score` |
| Saída `cachedAt` | ISO 8601 ou marcador da 1ª execução | Evidência de memoização |

## Por que esta ordem de nós

A cadeia `Webhook → Parse and Chunk → Normalize in One Pass → Return Metrics`
não é estética, cada fronteira carrega uma decisão:

1. **Webhook primeiro e barato.** Ele só aceita e reconhece; `responseMode: 'onReceived'`
   evita segurar a conexão HTTP do chamador pelo tempo total de processamento.
2. **Parse na segunda posição.** Assim nenhum nó a jusante precisa de `JSON.parse`,
   e qualquer re-parse posterior é violação de contrato detectável por leitura.
3. **Normalização em nó separado do parse.** Manter as duas responsabilidades
   distintas permite trocar a regra de normalização sem tocar na validação de
   entrada, e vice-versa.
4. **Métrica em nó final próprio.** O cálculo de `durationMs` usa `startedAt`
   transmitido no mesmo objeto de contexto, o que elimina clock skew entre nós e
   garante que a duração cubra o pipeline inteiro, não só a última etapa.

```mermaid
flowchart LR
    W[Webhook] --> P[Parse and Chunk]
    P --> N[Normalize in One Pass]
    N --> R[Return Metrics]
    R --> OUT[resposta JSON ao chamador]
```

## Como diagnosticar quando algo falhar

| Sintoma | Provável causa | Onde olhar |
|---|---|---|
| `processedItems: 0` com payload preenchido | JSON malformado virou `[]`, ou filtro barato agressivo demais | Nó `Parse and Chunk`, flag de parse |
| `deduped` muito alto | Produtor enviando duplicado | Consulta §4 de `5-monitoring/QUERIES.md` |
| `durationMs` acima de 60.000 | Regressão de complexidade ou payload maior que o normal | Execução no n8n UI, diff do nó |
| Execução em `error` | Item inválido passou do filtro e chegou na transformação | Mensagem do nó, invariante I9 |
| Webhook 404 | Workflow desativado ou path diferente de `/nos/*` | Nó `Webhook` do workflow |

## Limites conhecidos

- O webhook ainda aceita 100k itens num único POST. O particionamento no produtor
  é a solução definitiva e ficou para a camada de ingestão.
- O fatiamento em `chunks` preserva a fronteira de lote no dado, mas o processamento
  atual executa os lotes na mesma passada. A retomada automática entre lotes depende
  do checkpoint `mt_job_progress` da atividade 2.
- Não há autenticação própria nos webhooks `/nos/*`: se a instância expuser a rota
  publicamente, o controle de acesso precisa vir de proxy ou de credencial do n8n.
