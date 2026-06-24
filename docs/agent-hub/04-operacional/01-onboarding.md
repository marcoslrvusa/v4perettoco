# Onboarding — Novo Membro do Time

**Propósito:** Checklist para configurar um novo membro de squad no Agent Hub em ~30 minutos.

---

## 1. Pré-requisitos

- [ ] Membro já tem acesso ao Google Workspace da V4
- [ ] Membro já tem conta no Ekyte (criada pelo admin)

## 2. Checklist

### 2.1 Google Drive MCP — OAuth

```
1. Membro acessa OpenCode Web no navegador
2. Roda qualquer agente que use Drive MCP
3. Navegador abre tela de autorização Google
4. Membro autoriza escopos: drive.readonly + drive.file
5. Token OAuth fica armazenado na sessão do OpenCode Web
```

**Verificar:** `@analista-dados "Busca por 'briefing' no Drive"` — deve retornar resultados.

### 2.2 Ekyte MCP — Token

```
1. Membro acessa Configurações > Usuário no Ekyte
2. Gera token MCP (botão "Gerar Token")
3. Copia token para .env no VPS:
   EKYTE_MCP_TOKEN_{SQUAD}={token_do_membro}
4. Ou adiciona no OpenCode Web via settings UI
```

**Verificar:** `@account-checkin "Lista minhas tasks abertas"` — deve retornar tasks do membro.

### 2.3 LiteLLM — Chave Virtual

```
1. Admin cria chave virtual para o squad (se não existir)
   curl -X POST http://localhost:4000/virtual_keys \
     -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
     -d '{"models": [...], "rpm": 200, "budget": 50}'
2. Chave é configurada no OpenCode Web como LITELLM_VIRTUAL_KEY
```

### 2.4 OpenCode Web — Acesso

```
1. Membro acessa https://opencode.v4company.com.br
2. Faz login (SSO Google Workspace, se configurado)
3. Seleciona o squad
4. Verifica que os agentes do squad aparecem na lista
```

## 3. Primeiros Comandos

Após configurar, o membro deve testar:

```bash
# 1. Testar Ekyte
"Liste as tasks do meu squad em aberto"

# 2. Testar Drive
"Busque no Drive por 'briefing'"

# 3. Testar agente do squad
"@account-checkin-roleplay, me prepara pro check-in de amanhã"

# 4. Testar criação
"Crie uma tarefa no Ekyte: 'Finalizar onboarding' para mim, prazo: amanhã"
```

## 4. Troubleshooting Comum

| Problema | Causa Provável | Solução |
|---|---|---|
| "Token inválido" ao chamar Ekyte | Token expirou ou não foi gerado | Regenerar token no Ekyte |
| "Drive MCP não autorizado" | OAuth não foi concluído | Rodar tool do Drive para disparar OAuth |
| "Modelo não encontrado" | Chave LiteLLM não tem acesso ao modelo | Admin verificar virtual key |
| "Rate limit excedido" | Muitas requisições no mesmo minuto | Aguardar 60s ou aumentar rpm na virtual key |
| Agente não aparece | Squad errado selecionado | Verificar squad no OpenCode Web |

## 5. Saída do Onboarding

Ao final, o membro deve conseguir:
- [ ] Listar tasks do squad no Ekyte
- [ ] Buscar documentos no Drive
- [ ] Rodar o agente principal do squad
- [ ] Criar tarefas no Ekyte via agente
- [ ] Salvar arquivos no Drive via agente

---

**Documentos relacionados:**
- [02-seguranca.md](02-seguranca.md) — Políticas de segurança
- [02-componentes/01-opencode-web.md](../02-componentes/01-opencode-web.md) — Acesso ao OpenCode
