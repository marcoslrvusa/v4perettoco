# LiteLLM — Gateway de Modelos

**Propósito:** Proxy unificado entre os agentes OpenCode e os modelos de IA — governa acesso, rate limits e custos por squad.

---

## 1. Arquitetura

```
                  ┌──────────────┐
                  │   Agente     │
                  │  OpenCode    │
                  └──────┬───────┘
                         │ via OpenAI-compatible SDK
                         ▼
                  ┌──────────────┐
                  │   LiteLLM    │
                  │  Docker      │
                  │  :4000       │
                  └──┬───────┬───┘
                     │       │
            ┌────────┼───────┼──────────────┐
            │        │       │              │
            ▼        ▼       ▼              ▼
     ┌─────────┐ ┌──────┐ ┌──────┐   ┌──────────┐
     │ DeepSeek│ │Gemini│ │Claude│   │  GPT-4o  │
     │ V4 Flash│ │2.5   │ │Sonnet│   │          │
     │ (free)  │ │(free)│ │ 4    │   │          │
     └─────────┘ └──────┘ └──────┘   └──────────┘
```

## 2. Configuração Docker

```yaml
# docker-compose.yml (parte do LiteLLM)
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    ports:
      - "4000:4000"
    volumes:
      - ./litellm-config.yaml:/app/config.yaml
      - ./litellm.env:/app/.env
    environment:
      - LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY}
    command: ["--config", "/app/config.yaml"]
```

## 3. Configuração de Modelos (`litellm-config.yaml`)

```yaml
model_list:
  # DeepSeek V4 Flash (gratuito)
  - model_name: deepseek-v4-flash-free
    litellm_params:
      model: openai/deepseek-chat
      api_key: ${DEEPSEEK_API_KEY}
      api_base: https://api.deepseek.com/v1
      rpm: 100
      max_tokens: 128000

  # Gemini 2.5 Flash (gratuito)
  - model_name: gemini-2.5-flash-free
    litellm_params:
      model: gemini/gemini-2.5-flash
      api_key: ${GEMINI_API_KEY}
      rpm: 30
      max_tokens: 1048576

  # Claude Sonnet 4
  - model_name: claude-sonnet-4
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514
      api_key: ${ANTHROPIC_API_KEY}
      rpm: 50
      max_tokens: 8192

  # GPT-4o Mini (econômico)
  - model_name: gpt-4o-mini
    litellm_params:
      model: openai/gpt-4o-mini
      api_key: ${OPENAI_API_KEY}
      rpm: 100
      max_tokens: 16000

  # GPT-4o (full)
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: ${OPENAI_API_KEY}
      rpm: 30
      max_tokens: 16000
```

## 4. Chaves Virtuais por Squad

Cada squad recebe uma chave virtual com limites próprios:

| Squad | Chave Virtual | Modelos Liberados | Rate Limit | Budget Mensal |
|---|---|---|---|---|
| Account | `sk-account-xxx` | deepseek-v4-flash, gemini-2.5-flash, claude-sonnet-4 | 200 rpm | $50 |
| Copy | `sk-copy-xxx` | deepseek-v4-flash, gemini-2.5-flash, gpt-4o-mini | 200 rpm | $30 |
| GT | `sk-gt-xxx` | deepseek-v4-flash, gemini-2.5-flash, gpt-4o-mini | 200 rpm | $30 |
| Design | `sk-design-xxx` | deepseek-v4-flash, claude-sonnet-4, gpt-4o | 100 rpm | $80 |
| CSM | `sk-csm-xxx` | deepseek-v4-flash, gemini-2.5-flash, gpt-4o-mini | 150 rpm | $20 |
| Coord | `sk-coord-xxx` | deepseek-v4-flash, gemini-2.5-flash, claude-sonnet-4, gpt-4o | 200 rpm | $100 |

## 5. Integração com OpenCode

No `opencode.json`, apontamos para o LiteLLM como provider:

```json
{
  "modelProvider": "litellm",
  "model": "gpt-4o-mini",
  "customProviders": {
    "litellm": {
      "type": "openai-compatible",
      "apiKey": "{env:LITELLM_VIRTUAL_KEY}",
      "baseURL": "http://localhost:4000/v1"
    }
  }
}
```

Cada agente específica qual modelo usar:

```yaml
# .opencode/agents/copy-content.md
model: gpt-4o-mini
temperature: 0.7
```

## 6. Comandos Úteis

```bash
# Ver status do LiteLLM
curl http://localhost:4000/health

# Listar chaves virtuais
curl http://localhost:4000/virtual_keys \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"

# Criar nova chave virtual para squad
curl -X POST http://localhost:4000/virtual_keys \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"models": ["deepseek-v4-flash", "gpt-4o-mini"], "rpm": 200}'

# Ver uso e custos
curl http://localhost:4000/spend \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"
```

---

**Documentos relacionados:**
- [01-opencode-web.md](01-opencode-web.md) — Interface dos agentes
- [01-fundacional/01-ekyte-coracao.md](../01-fundacional/01-ekyte-coracao.md) — Ekyte como centro
