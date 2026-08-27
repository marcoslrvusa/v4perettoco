# Standard — Expressões Avançadas no n8n

> **Objetivo:** padrão para expressões `={{ ... }}` em parâmetros de nós n8n —
> referências entre nós, JSONata, condicionais e cache — para payloads pesados.

## Quando usar expressão vs nó Code

| Situação | Use |
|---|---|
| Pegar um campo de outro nó na mesma execução | Expressão `$('Node').item.json.campo` |
| Transformação simples (formatação, concat) | Expressão |
| Dedupe / agregação / normalização em lote | Nó Code (JS/Python) |
| Referenciar dados da execução anterior | `$getWorkflowStaticData()` |
| Consultar por caminho/condição em payload grande | JSONata (`.$filter()`) |

## Referências entre nós

```text
// Último item de outro nó
{{ $('HTTP Request').item.json.leads }}

// Primeiro item
{{ $('HTTP Request').first().json.leads }}

// Todos os itens (cuidado com memória em payload pesado!)
{{ $('HTTP Request').all() }}
```

> **Regra:** `$('Node').all()` materializa o array inteiro. Em payloads pesados,
> prefira processar via nó Code e expor só o que precisa via `item`.

## JSONata para consulta em payload grande

```text
{{ $json.leads.$filter($, function($v) { $v.score >= 70 }).$count() }}
```

Vantagem: consulta e agregação diretas no payload sem nó Code extra.

## Expressões condicionais e coalescência

```text
{{ $json.fallback || $('HTTP Request').item.json.valor }}
{{ $json.tipo == 'B2B' ? 'entrada' : 'pipeline' }}
```

## Cache entre execuções (memoização)

```javascript
// Em nó Code:
const staticData = $getWorkflowStaticData('global');
if (!staticData.taxaCambio) {
  staticData.taxaCambio = 5.4; // busca uma vez, reusa nas próximas execuções
}
return [{ json: { taxa: staticData.taxaCambio } }];
```

## Anti-patterns

| Anti-pattern | Problema |
|---|---|
| `$('Node').all()` dentro de loop | Materializa arrays gigantes repetidamente |
| Expressão complexa com múltiplas chamadas de nó | Re-avalia a cada execução |
| JSONata pesado em payload enorme | Melhor chunking no nó Code |
| Expressão para lógica de negócio reutilizável | Duplicação — vai para `3-lib/` |

## Checagem (antes de publicar)

- [ ] `$('Node').all()` só onde absolutamente necessário
- [ ] Expressões simples o suficiente para leitura rápida
- [ ] Lógica reutilizável movida para `3-lib/` (payload-lib)
- [ ] Valores estáveis cacheados com `$getWorkflowStaticData`