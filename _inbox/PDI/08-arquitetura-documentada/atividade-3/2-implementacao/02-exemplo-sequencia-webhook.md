# Exemplo Real 2: Sequencia do Webhook n8n para Worker

Mostra o contrato real: o que o n8n manda, o que o worker devolve e onde cada erro cai.

```mermaid
sequenceDiagram
  participant N as n8n
  participant W as Worker Python
  participant M as Meta Ads API
  participant S as Supabase
  N->>W: POST /coletar conta_id e janela
  W->>M: GET metricas da conta
  alt Sucesso
    M-->>W: 200 metricas
    W->>S: INSERT em coletas
    W-->>N: 200 ok
  else Rate limit
    M-->>W: 429 retry-after
    W->>W: Backoff exponencial
  else Falha definitiva
    W->>S: INSERT em erros
    W-->>N: 500 falha com conta_id
  end
```

Contrato: `conta_id` e `janela` obrigatorios na entrada; saida sempre `200 ok` ou `500 falha com conta_id`, nunca timeout silencioso.
