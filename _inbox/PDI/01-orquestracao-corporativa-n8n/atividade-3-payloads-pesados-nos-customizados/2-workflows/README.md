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