# Exemplo Real 1: Fluxo de Coleta Meta Ads

Fonte oficial do desenho abaixo. Qualquer mudança no worker de coleta exige atualizar este bloco no mesmo PR.

```mermaid
flowchart TD
  A["Trigger coleta-meta-ads, 30 min"] --> B["Subworkflow monta conta e janela"]
  B --> C["POST worker :8000/coletar"]
  C --> D{"Resposta?"}
  D -->|"200 ok"| E["INSERT coletas no Supabase"]
  D -->|"429 rate limit"| F["Backoff 30s, 60s, 120s"]
  F --> C
  D -->|"Falha 3x"| G["INSERT erros e alerta"]
  E --> H["Painel exibe verba"]
```

Donos: worker em `workers/coleta_meta.py` (exemplo), workflow `coleta-meta-ads` no n8n. Última revisão: Setembro 2026.
