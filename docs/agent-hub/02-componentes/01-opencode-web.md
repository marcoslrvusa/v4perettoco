# OpenCode Web

**Propósito:** Interface web multi-squad dos agentes de IA — onde cada membro do time acessa os agentes, compartilha sessões e gerencia skills.

---

## 1. Arquitetura de Acesso

```
                    ┌─────────────────────────────────┐
                    │        Hostinger VPS             │
                    │    (4 vCPU, 16GB RAM)            │
                    │                                  │
                    │  ┌──────────────────────────┐    │
                    │  │     OpenCode Web          │    │
                    │  │  ┌────────────────────┐   │    │
                    │  │  │ Squad Account      │   │    │
                    │  │  │ Squad Copy         │   │    │
                    │  │  │ Squad GT           │   │    │
                    │  │  │ Squad CSM/Coord    │   │    │
                    │  │  └────────────────────┘   │    │
                    │  └──────────────────────────┘    │
                    │                                  │
                    │  ┌─────────┐  ┌──────────────┐  │
                    │  │ LiteLLM │  │   n8n        │  │
                    │  │ gateway │  │  headless     │  │
                    │  └─────────┘  └──────────────┘  │
                    └─────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
   │  Account A   │    │   Copy A     │    │    GT A      │
   │  (browser)   │    │  (browser)   │    │  (browser)   │
   └──────────────┘    └──────────────┘    └──────────────┘
```

## 2. Configuração `opencode.json`

Cada squad acessa o mesmo OpenCode Web com sua própria chave LiteLLM. A configuração principal:

```json
{
  "mcp": {
    "ekyte": {
      "type": "remote",
      "url": "https://api.ekyte.com/mcp?token={env:EKYTE_MCP_TOKEN}",
      "enabled": true
    },
    "google-drive": {
      "type": "remote",
      "url": "https://google-drive-mcp.example.com/mcp",
      "oauth-client-id": "{env:GOOGLE_OAUTH_CLIENT_ID}",
      "oauth-client-secret": "{env:GOOGLE_OAUTH_CLIENT_SECRET}",
      "enabled": true
    },
    "google-people": {
      "type": "remote",
      "url": "https://people.googleapis.com/v1",
      "oauth-client-id": "{env:GOOGLE_OAUTH_CLIENT_ID}",
      "oauth-client-secret": "{env:GOOGLE_OAUTH_CLIENT_SECRET}",
      "enabled": true
    },
    "google-calendar": {
      "type": "remote",
      "url": "https://www.googleapis.com/calendar/v3",
      "oauth-client-id": "{env:GOOGLE_OAUTH_CLIENT_ID}",
      "oauth-client-secret": "{env:GOOGLE_OAUTH_CLIENT_SECRET}",
      "enabled": true
    }
  },
  "modelProvider": "litellm",
  "model": "gpt-4o-mini"
}
```

## 3. Como Cada Squad Usa

| Squad | Agentes Principais | Uso Típico |
|---|---|---|
| **Account** | account-orchestrator, vendas-account, checkin-review, checkin-roleplay | Pré/pós check-in, handoff, pesquisa de cliente |
| **Copy** | content-studio, copy-content, pipeline-conteudo | Produção de conteúdo editorial, LPs, emails |
| **GT** | media-buyer, relatorios-trafego, cro-otimizacao, midia-paga | Análise de tráfego, otimização de campanhas |
| **Design** | criacao-design, gerar-html, gerar-pdf, gerar-ppt | Interfaces, PDFs, apresentações |
| **CSM** | csm-orquestrador, flag-churn | QBR, diagnóstico de risco, NPS |
| **Coord** | executor-comite, cmoorch, growth-team, launch-pad, revenue-ops | Comitê, planejamento, estratégia |
| **Geral** | analista-dados, pesquisador, revisor, sdr-tech, seo-visibilidade | Serviços transversais |

## 4. Session Sharing

O OpenCode Web permite compartilhar sessões entre usuários do mesmo squad:

```
Usuário A (Account) inicia sessão com @account-checkin-review
Usuário B (Account) vê a mesma sessão ao acessar o workspace
```

Regras:
- Compartilhamento apenas dentro do mesmo squad
- Cada usuário mantém seu próprio token Ekyte 
- Modelo é definido pelo LiteLLM por chave virtual

## 5. Modo Híbrido (Web + n8n)

| Operação | Onde Roda | Motivo |
|---|---|---|
| Interação com agente | OpenCode Web | Resposta em tempo real, contexto visual |
| Relatório semanal | n8n | Headless, cron, sem necessidade de UI |
| Briefing do comitê | n8n puxa → agente gera | Workflow noturno, resultado salvo no Drive |
| Flag automática | n8n → ticket no Ekyte | Gatilho de dados, sem interação humana |
| Geração de conteúdo em lote | OpenCode Web (agente) | Requer validação visual do copywriter |

---

**Documentos relacionados:**
- [02-componentes/02-litellm.md](02-litellm.md) — Gateway de modelos
- [01-fundacional/01-ekyte-coracao.md](../01-fundacional/01-ekyte-coracao.md) — Ekyte como centro
