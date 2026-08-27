# Retrofit — Nós Code e Expressões Existentes

Plano para adaptar os nós `Code` e expressões já existentes nos workflows SDR IA
e Command Center ao padrão de payload pesado da atividade 3.

## Objetivo

Trocar os nós Code "genéricos" (que carregam tudo, copiam objeto por objeto,
re-parseiam JSON) pelas funções otimizadas da biblioteca `3-lib/`, seguindo os
padrões `1-standards/`.

## Inventário de alvos (sintomas observados na atividade 1)

| Workflow                 | Sintoma                                 | Correção                                            |
| ------------------------ | --------------------------------------- | --------------------------------------------------- |
| ADPLAN                   | JS timeout 25min (event loop bloqueado) | Streaming + chunking (`normalizeStream`), sair cedo |
| PRO ANALISES             | `toDateTime` undefined                  | Parse 1x na entrada + validação de campo            |
| Collector / Metrics (CC) | Payloads grandes re-processados         | Dedupe por chave + agregação O(n)                   |
| Diversos                 | Código copiado entre nós                | Extrair para `3-lib/` e referenciar                 |

## Passo a passo (por workflow)

### Fase 1 — Mapear nós Code

1. Listar todos os nós `Code` (JS e Python) do workflow.
2. Marcar quais processam listas grandes (`$input.all()`, `map`/`filter` em arrays).
3. Marcar onde há `JSON.parse`/`JSON.stringify` dentro de loops.

### Fase 2 — Aplicar padrão

1. **Parse 1x:** mover `JSON.parse` do payload para a primeira etapa.
2. **Dedupe O(n):** trocar `filter`+`find`/`indexOf` por `Set` de chave primitiva.
3. **Copias minimas:** reduzir spreads `{...item}` para os campos necessarios.
4. **Sair cedo:** filtros baratos antes de transformacoes caras.
5. **Python:** garantir apenas stdlib; `Counter`/`defaultdict` para agregacao.

### Fase 3 — Teste com payload simulado

```bash
curl -X POST https://n8n.fvmarketing.com.br/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' \
  -d '{"payload": [{"id":1,"name":"Lead A","score":88}, {"id":1,"name":"Lead A","score":88}]}'
```

- Checar `processedItems`, `deduped`, `durationMs` e `itemsPerSecond`.
- Repetir com 10k e 100k itens; registrar pico de memoria.

## Estimativa de esforço

| Atividade | Esforço | Detalhe |
|---|---|---|
| JS Normalizer (novo) | — | Entregue nesta PDI |
| Python Enricher (novo) | — | Entregue nesta PDI |
| Retrofit ADPLAN | 30 min | Streaming + dedupe |
| Retrofit PRO ANALISES | 10 min | Parse 1x + validacao |
| Retrofit CC Collector | 20 min | Dedupe + agregacao O(n) |
| Extrair lib `3-lib/` | 20 min | Mover funcoes para payload-lib |

## Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Alterar comportamento de produção | Testar em payload simulado antes do push |
| Python sem stdlib assumido | Checklist do `STANDARD-CODE-PYTHON.md` |
| Duplicação voltar | Regra: lib é fonte da verdade (`3-lib/README.md`)