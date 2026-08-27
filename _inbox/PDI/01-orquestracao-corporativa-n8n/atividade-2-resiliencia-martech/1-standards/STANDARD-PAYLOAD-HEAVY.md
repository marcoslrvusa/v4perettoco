# Padrao de Processamento de Payloads Pesados — n8n Enterprise V4

> **Versao:** 1.0 | **Status:** Pronto para homologacao | **Ultima revisao:** 2026-08-05

## 1. Problema

Payloads de integracao MarTech (lista de contatos, exportacao de pedidos,
sincronizacao de catalogo) frequentemente excedem 1 MB e chegam a dezenas de MB.
Quando o n8n processa o JSON inteiro de uma vez:

- ocorre estouro de memoria / OOM;
- o event loop trava (JS timeout classico dos SDR IA);
- o n8n serializa o payload inteiro a cada no (overhead de rede/CPU);
- a operacao da instancia degrada para TODOS os outros workflows.

## 2. Principios

1. **Nunca carregue o payload inteiro em memoria** — processe em lotes (chunk).
2. **Separe dados de referencia do trabalho** — payload leve na fila; os dados
   pesados ficam no Supabase (tabela ou storage) e sao lidos por streaming.
3. **Prefira operacoes O(n) ou O(n log n)** — evite aninhar no Code node.
4. **Stateless kernels** — o codigo de transformacao nao guarda estado global;
   recebe um chunk e devolve um chunk.
5. **Log do que foi feito** — cada chunk tem checkpoint para retomar (idempotencia).

## 3. Tabela de Decisao

| Situacao | Estrategia |
|----------|-----------|
| Payload < 64 KB | Processa direto no Code node (normal) |
| 64 KB – 1 MB | Chunking em memoria (SplitInBatches do n8n) |
| 1 MB – 50 MB | Chunking + armazenamento parcial no Supabase |
| > 50 MB | Streaming em arquivo (temporary) + chunks |

## 4. Chunking no n8n

Nao criar loops manualmente no Code node. Usar o node **Split in Batches** do n8n:

```
HTTP Request (JSON pesado)
  → Code: Normalize + extrai array
  → Split In Batches (batchSize: 500)
  → Code: Processa chunk (kernel stateless)
  → Code: Checkpoint (grava progresso no Supabase)
  → Merge / progress-bar
```

- O n8n serializa cada batch individualmente — mantem a memoria sob controle.
- Cada batch roda como item proprio; erros viram retry batch com continueErrorOutput.

### 4.1 Kernel JavaScript (Code node)

Regras do kernel:
- Funcoes puras: `(input) => output`, sem mutable state fora do loop.
- Evitar `JSON.stringify` de payload grande desnecessario — so no checkpoint.
- Usar `for...of` classico; evitar spread gigante (`...arr`).
- Cortar campos desnecessarios no normalize (schema de saida enxuto).

Exemplo minimo de normalize + chunk:

```js
// Normalize: recebe payload bruto e devolve so o essencial
const items = $input.all();
const LIGHT = (x) => ({
  id: x.id,
  name: x.name || '',
  email: x.email || '',
  phone: x.phone || null,
  tags: Array.isArray(x.tags) ? x.tags.slice(0, 20) : [],
});

return items.map((i) => ({ json: LIGHT(i.json) }));
```

### 4.2 Alternativa Python (n8n Python node)

Nos cenarios de processamento numerico/pandas/string-heavy, usar Code node Python
(opcional em instancias com o runtime Python habilitado):

```python
import json

items = [json.loads(item) for item in items]

def light(x):
    return {
        'id': x.get('id'),
        'name': x.get('name', ''),
        'email': x.get('email', ''),
    }

return [{'json': light(x)} for x in items]
```

## 5. Checkpoint / Retomabilidade

Tabela `mt_job_progress` registra, por job_id, o `chunk_index` processado. Em caso de
falha, o worker retoma de onde parou (nao reprocessa tudo):

```
job_id, chunk_index, total_chunks, status, updated_at
```

- Inicio do batch: `UPDATE mt_job_progress SET status='running'`.
- Fim do batch: `status='done'`, `chunk_index=total`.
- Falha mid-batch: `status='paused'` + `error_message`; retry continua no
  `chunk_index` salvo.

## 6. Limites e Seguranca

| Recurso | Limite |
|---------|--------|
| Tamanho maximo em memoria por chunk | 5 MB |
| Itens por batch | 500 |
| Jobs pesados em paralelo | 2 por fila |
| Timeout de chunk | 30 s |
| Payload total max para streaming | 200 MB |

## 7. Anti-Patterns de Payload Pesado

| Anti-pattern | Problema |
|--------------|----------|
| `JSON.parse` de 20 MB no webhook de entrada | OOM no request |
| Modelagem de payload no Code node com 3 loops | Timeout JS |
| `...spread` de dezenas de MB | Consome memoria 2x |
| Reprocessar tudo quando 1 chunk falha | Backlog gigante; usa checkpoint |
| Payload completo duplicado em cada node | Serializacao cara |
| Guardar payload inteiro na linha do job | Fila gigante no Supabase |
| Sem release de referencia apos chunk | Memory leak em execucoes longas |