# Mermaid Guia Rápido (só o que usamos)

## Fluxo (flowchart)

```mermaid
flowchart TD
  A["Trigger 30 min"] --> B["Chama worker via webhook"]
  B --> C{"Coleta ok?"}
  C -->|"Sim"| D["Grava no Supabase"]
  C -->|"Nao, rate limit"| E["Backoff e retry"]
  E --> C
  C -->|"Nao, falhou 3x"| F["Fila de erros"]
```

## Sequência (sequenceDiagram)

```mermaid
sequenceDiagram
  participant N as n8n
  participant W as Worker Python
  participant M as Meta Ads API
  participant S as Supabase
  N->>W: POST /coletar conta e janela
  W->>M: GET metricas
  M-->>W: metricas ou 429
  W->>S: INSERT coletas ou erros
  W-->>N: 200 ok ou falha
```

## Regras de sintaxe que quebram o CI

- Rótulos com caracteres especiais vão entre aspas: `A["Trigger 30 min"]`.
- Setas de resposta usam `-->>`, não `->>`.
- Condição usa chaves: `C{"Coleta ok?"}`.
- Nomes de participante sem espaço: `participant W as Worker Python`.
- Todo bloco abre com tripla crase + `mermaid` e fecha com tripla crase, sem indentação estranha.
