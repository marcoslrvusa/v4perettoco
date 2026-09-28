# Retry Matrix: Configuração por Tipo de Node

## Configuração Nativa (node-level)

| Tipo de Node | retryOnFail | maxTries | waitBetweenTries | Observação |
|-------------|-------------|----------|------------------|------------|
| HTTP Request | true | 3 | 5000 | Sempre configurar |
| Supabase API | true | 2 | 3000 | Rede interna, falhas raras |
| Slack | true | 3 | 5000 | 429 frequente em pico |
| Google Sheets | true | 2 | 5000 | Rate limit em batch |
| Redis | true | 2 | 2000 | Conexão local, rápido |
| WhatsApp / API externa | true | 3 | 5000 | Instabilidade comum |
| Postgres | true | 2 | 3000 | Timeout de query |
| n8n node (API interna) | true | 3 | 5000 | Pode rate limitar |
| Code (JavaScript/Python) | false | - | - | Retry não ajuda erro de lógica |
| Set / Edit Fields | false | - | - | Dados já validados |
| IF / Switch | false | - | - | Expressões simples |

## Configuração Customizada (loop com backoff)

Para cenários que exigem controle fino (429, 5xx persistentes):

```typescript
// Parametros do loop customizado
{
  baseDelay: 1000,       // 1s inicial
  maxDelay: 300000,      // 5s maximo
  maxTries: 3,
  multiplier: 2,          // Exponencial: 1s, 2s, 4s
  jitterPercent: 25,      // Mais ou menos 25% aleatorio
}
```

### Código de Backoff

```javascript
// Code node - calcular wait com jitter
const attempt = $input.first().json._attempt || 1;
const baseDelay = 1000;   // 1s
const maxDelay = 300000;  // 5min
const multiplier = 2;

const waitMs = Math.min(
  maxDelay,
  baseDelay * Math.pow(multiplier, attempt - 1)
);
const jitter = waitMs * (0.25 * (Math.random() * 2 - 1));
const finalWait = Math.round(waitMs + jitter);

return [{ json: { _waitMs: finalWait, _attempt: attempt + 1 } }];
```

## Códigos HTTP: Retentar ou Não?

| Status | Retentar? | Ação |
|--------|-----------|------|
| 400 | Não | Payload inválido: revisar manualmente |
| 401 | Não | Credencial expirou: alertar equipe imediatamente |
| 403 | Não | Permissão negada: alertar equipe |
| 404 | Não | Endpoint/URL mudou: revisar |
| 408 | Sim (3x) | Timeout do servidor: backoff |
| 409 | Sim (3x) | Conflito: retentar com backoff |
| 422 | Não | Dado mal formatado: revisar payload |
| 425 | Sim (3x) | Very Early: retentar |
| 429 | Sim (3x) | Rate limit: respeitar Retry-After se presente |
| 500 | Sim (3x) | Erro interno do servidor |
| 502 | Sim (3x) | Upstream com problema |
| 503 | Sim (3x) | Serviço indisponível |
| 504 | Sim (3x) | Timeout do upstream |
