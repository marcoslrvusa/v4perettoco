# Emergência — Procedimentos para Queda de Componentes

**Propósito:** Procedimentos claros para quando algo no Agent Hub falha — desde queda de VPS até falha de MCP.

---

## 1. Matriz de Gravidade

| Nível | Descrição | Exemplos | SLA |
|---|---|---|---|
| **P0** | Toda operação parada | VPS fora do ar, LiteLLM morto, Ekyte offline | 1h |
| **P1** | Um squad parado | Agente de squad não funciona, MCP específico caiu | 4h |
| **P2** | Funcionalidade degradada | Modelo lento, OAuth expirou, token expirado | 24h |
| **P3** | Incômodo | Latência alta, relatório atrasou, cron falhou | 48h |

## 2. Procedimentos por Componente

### 2.1 VPS Fora do Ar (P0)

```
Sintomas:
  - OpenCode Web não abre
  - n8n não responde
  - LiteLLM não acessível

Procedimento:
1. Verificar status no painel Hostinger (https://hpanel.hostinger.com)
2. Tentar SSH: ssh admin@IP_DO_VPS
3. Se SSH não funciona:
   a. Acessar console no painel Hostinger
   b. Verificar logs: journalctl -xe
   c. Se reboot resolve: sudo reboot
   d. Se não resolve: restore do último snapshot
4. Se restore do snapshot:
   a. Verificar Docker: docker ps
   b. Subir containers: docker-compose up -d
   c. Verificar health: curl localhost:4000/health (LiteLLM)
   d. Verificar n8n: curl localhost:5678/health
5. Notificar squads no Slack: "#agenthub-status: VPS restaurado"

Rollback:
  - Snapshot diário automático (configurar no Hostinger)
  - Docker volumes persistentes em /opt/agent-hub/data/
```

### 2.2 LiteLLM Offline (P0)

```
Sintomas:
  - Agentes retornam "model not found" ou "connection refused"
  - curl localhost:4000/health falha

Procedimento:
1. Verificar container: docker ps | grep litellm
2. Se container parou: docker restart litellm
3. Se não sobe:
   a. Verificar logs: docker logs litellm --tail 100
   b. Verificar config: docker exec litellm cat /app/config.yaml
   c. Verificar variáveis de ambiente no .env
4. Se config corrompida:
   a. Restaurar config.yaml do backup
   b. docker-compose restart litellm
5. Testar: curl http://localhost:4000/health

Rollback:
  - Config versionada no git (docs/server-setup/)
  - Backup diário do litellm-config.yaml
```

### 2.3 Ekyte MCP Fora (P2)

```
Sintomas:
  - Agentes retornam "Ekyte MCP error" ou "token inválido"
  - create_task / list_tasks falha

Procedimento:
1. Verificar status do Ekyte: https://status.ekyte.com (ou suporte)
2. Se Ekyte está online mas MCP não funciona:
   a. Verificar token: "Seu token MCP expirou? Gere um novo em Configurações > Usuário"
   b. Verificar .env no VPS: grep EKYTE_MCP_TOKEN .env
   c. Testar manualmente: curl -H "Authorization: Bearer $TOKEN" https://api.ekyte.com/mcp
3. Se token expirou:
   a. Usuário regenera no Ekyte
   b. Atualiza .env no VPS
   c. Restarta OpenCode Web (ou recarrega sessão)

Mitigação temporária:
  - Usuário cria tasks manualmente no Ekyte (UI web) até MCP voltar
  - n8n ainda funciona se tem API key separada do MCP
  - Drive MCP continua funcionando (independente de Ekyte)
```

### 2.4 Google Drive MCP Offline (P2)

```
Sintomas:
  - "Drive MCP não autorizado"
  - "OAuth token expired"

Procedimento:
1. Se OAuth expirou:
   a. Usuário roda qualquer tool do Drive MCP
   b. Navegador abre tela de autorização
   c. Usuário autoriza novamente
   d. Token refresh automático (se escopo correto)
2. Se erro de API:
   a. Verificar https://status.cloud.google.com
   b. Se Google estável: verificar credenciais OAuth no Google Cloud Console
   c. Verificar se OAuth client ID/secret estão corretos no .env

Mitigação temporária:
  - Acessar Drive diretamente pelo navegador
  - Colar conteúdo manualmente para o agente
```

### 2.5 n8n Offline (P1)

```
Sintomas:
  - Relatórios automáticos não chegam
  - Briefing do comitê não foi gerado
  - Flags não disparam

Procedimento:
1. Verificar container: docker ps | grep n8n
2. Logs: docker logs n8n --tail 100
3. Se erro de credencial:
   a. Verificar encryption key
   b. Verificar service account do Google
4. Se workflow específico falhou:
   a. Acessar UI do n8n (localhost:5678)
   b. Verificar execution log do workflow
   c. "Run once" para testar
5. Se cron não disparou:
   a. Verificar timezone do container
   b. Verificar se container está com horário correto

Mitigação temporária:
  - Workflows críticos (comitê): rodar manualmente na UI do n8n
```

## 3. Contatos de Emergência

| Papel | Responsável | Contato |
|---|---|---|
| Admin VPS | Infra V4 | Slack: @infra |
| Token Ekyte | Cada usuário | Slack direto com admin |
| OAuth Google | Admin Google Workspace | Slack: @admin |
| LiteLLM | Desenvolvedor | Slack: @dev |

## 4. Plano de Continuidade

| Situação | Plano A | Plano B | Plano C |
|---|---|---|---|
| VPS cai | Restore snapshot | Subir em VPS reserva | Cada squad usa OpenCode local |
| LiteLLM cai | Restart container | Fallback para API direta (sem proxy) | Modelos gratuitos direto |
| Ekyte cai | Aguardar Ekyte voltar | UI web do Ekyte | Tasks no Drive (temporário) |
| Drive cai | Aguardar Google voltar | Conteúdo colado manualmente | Documentos locais |
| n8n cai | Restart container | Rodar workflows manualmente | Pular automações não críticas |

---

**Documentos relacionados:**
- [02-seguranca.md](02-seguranca.md) — Tokens, chaves e políticas
- [02-componentes/01-opencode-web.md](../02-componentes/01-opencode-web.md) — Acesso ao OpenCode
- [02-componentes/05-n8n.md](../02-componentes/05-n8n.md) — Automações
