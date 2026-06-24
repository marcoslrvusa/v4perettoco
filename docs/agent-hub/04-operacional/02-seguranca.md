# Segurança — Políticas de Acesso, Dados e Chaves

**Propósito:** Estabelecer regras claras de segurança para o Agent Hub — acesso a modelos, dados de clientes, tokens e MCPs.

---

## 1. Matriz de Acesso

| Recurso | Quem Acessa | Como | Onde Fica |
|---|---|---|---|
| **OpenCode Web** | Todos os membros | Navegador + SSO | VPS (Hostinger) |
| **LiteLLM** | Agentes (via SDK) | API localhost:4000 | VPS (Docker) |
| **Ekyte MCP** | Agentes + cada membro | Token por usuário | api.ekyte.com |
| **Drive MCP** | Agentes + cada membro | OAuth individual | googleapis.com |
| **n8n UI** | Admin + coordenação | Navegador + senha | VPS (Docker) |
| **VPS (SSH)** | Apenas admin | Chave SSH | Hostinger |
| **Builders Hub** | Todos (git) | gh CLI + token | GitHub |

## 2. Políticas de Token e Chave

### 2.1 Ekyte MCP Token

- Cada usuário gera o **próprio token** em Configurações > Usuário
- Token é registrado no .env do VPS como `EKYTE_MCP_TOKEN_{USER_ID}`
- Ações no Ekyte são registradas como executadas pelo dono do token
- **Nunca compartilhar** tokens entre usuários
- Revogar imediatamente quando membro sai do time

### 2.2 Google Drive MCP OAuth

- OAuth vinculado à conta Google Workspace do membro
- Escopos mínimos: `drive.readonly` + `drive.file` (não `drive` full)
- `drive.file` limita acesso apenas a arquivos criados ou abertos pelo app
- Revogar acesso em https://myaccount.google.com/permissions

### 2.3 LiteLLM Virtual Keys

- Uma chave virtual **por squad** (não por usuário)
- Budget mensal configurado para evitar surpresas
- Rate limit por chave para evitar abuso
- Modelos liberados controlados por squad

### 2.4 n8n

- Encryption key obrigatória para credenciais das nodes
- Webhooks do Ekyte com HMAC validation
- Service account do Google (não OAuth de usuário)
- Acesso à UI protegido por senha + 2FA

## 3. Segurança de Dados de Clientes

| Tipo de Dado | Onde Trafega | Onde Fica | Criptografia |
|---|---|---|---|
| Briefings | Drive MCP (HTTPS) | Google Drive | Em trânsito (TLS) |
| Transcripts de call | Drive MCP (HTTPS) | Google Drive | Em trânsito (TLS) |
| Tasks/projetos | Ekyte MCP (HTTPS) | api.ekyte.com | Em trânsito (TLS) |
| Tokens de plataforma | .env no VPS (nunca no git) | VPS + LiteLLM | Em repouso (Docker volume) |
| Dados de anúncios | V4mos API (HTTPS) | API externa | Em trânsito (TLS) |

**Regras:**
- **Nunca** colocar tokens, senhas ou chaves em arquivos versionados
- **Nunca** manter dados de cliente em estações locais — apenas no Drive/Ekyte
- Logs de sessão do OpenCode ficam em `log/` (gitignored) — Limpar periodicamente
- Relatórios com dados sensíveis: salvar sempre no Drive (não local)

## 4. Boas Práticas

```bash
# .env template (NUNCA commitar)
# =============================
# Ekyte
EKYTE_MCP_TOKEN_ACCOUNT=sk-xxx
EKYTE_MCP_TOKEN_COPY=sk-yyy

# LiteLLM
LITELLM_MASTER_KEY=sk-litellm-master
LITELLM_VIRTUAL_KEY_ACCOUNT=sk-account-xxx

# OAuth
GOOGLE_OAUTH_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=GOCSPX-xxx
```

## 5. Procedimentos de Emergência

| Evento | Ação | Responsável |
|---|---|---|
| Token Ekyte vazado | Revogar em Configurações > Usuário + gerar novo | Admin |
| Chave LiteLLM vazada | Revogar virtual key + criar nova | Admin |
| VPS comprometido | Rebuild desde o backup + rodar onboarding | Admin |
| Membro sai do time | Revogar token Ekyte + OAuth Drive + remover do squad | Admin |
| Bug em agente que expõe dados | Parar agente, revisar código, atualizar skill | Desenvolvedor |

---

**Documentos relacionados:**
- [01-onboarding.md](01-onboarding.md) — Checklist de novo membro
- [04-emergencia.md](04-emergencia.md) — Procedimentos de contingência
- [01-fundacional/01-ekyte-coracao.md](../01-fundacional/01-ekyte-coracao.md) — Ekyte como centro
