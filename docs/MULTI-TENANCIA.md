# Multi-tenancy: Isolamento de Dados por Usuário

## Problema

Usuários de um squad podem ver dados de clientes que não são seus. Em um ambiente multi-usuário com OpenCode + eKyte + Supabase, precisamos garantir que:

- Usuário do Squad A **não vê** clientes do Squad B
- Dentro do squad, cada usuário vê **só os clientes atribuídos a ele**

## Arquitetura Atual

| Camada | Onde os dados vivem | Isolamento |
|---|---|---|
| eKyte (tarefas, boards, projetos) | API eKyte com token | **Já resolve** — token é scoped por empresa. Workspaces isolam squads. |
| Local files (KBs de cliente) | `squads/{squad}/clientes/{cliente}/` | **Container resolve** — cada usuário tem seu container com acesso só às pastas dele |
| Supabase (memórias, flags, agent_queue) | Tabelas compartilhadas | **Não resolve** — RLS precisa ser implementado |
| n8n (workflows) | Workspaces do n8n | **Depende** — cada squad/cliente pode ter workspace separado |

## Solução Proposta

### 1. eKyte (já funciona)

Cada usuário recebe um token eKyte scoped para a empresa dele. O MCP tool do eKyte já valida:

```json
{
  "mcp": {
    "ekyte-marcos": {
      "type": "remote",
      "url": "https://api.ekyte.com/mcp?token=TOKEN_DO_MARCOS",
      "enabled": true
    },
    "ekyte-joao": {
      "type": "remote",
      "url": "https://api.ekyte.com/mcp?token=TOKEN_DO_JOÃO",
      "enabled": true
    }
  }
}
```

Cada token só vê a empresa do dono. Workspaces do eKyte podem representar squads.

### 2. Containers Multi-usuário (já funciona)

Cada usuário tem:
- Próprio container Docker com OpenCode
- Própria KB (squads/, clientes/, projetos/)
- Próprio `opencode.json` com seus tokens
- Próprio `.env` com suas chaves de API

O sistema de arquivos do container é o isolamento — João não acessa o filesystem do Marcos.

**Setup de novo usuário:**
```bash
# 1. Criar container
docker run -d --name opencode-joao \
  -v /data/usuarios/joao:/workspace \
  opencode-multiuser

# 2. Copiar config base com token eKyte dele
scp opencode.json root@server:/data/usuarios/joao/
scp .env root@server:/data/usuarios/joao/
```

### 3. Supabase — RLS (precisa implementar)

Tabelas que precisam de RLS por `user_id` ou `company_id`:

```sql
-- agent_memories
CREATE POLICY "usuarios veem só suas proprias memorias"
ON agent_memories FOR ALL
USING (user_id = current_setting('app.current_user_id')::uuid);

-- agent_queue  
CREATE POLICY "usuarios veem só sua fila"
ON agent_queue FOR ALL
USING (user_id = current_setting('app.current_user_id')::uuid);

-- flags
ALTER TABLE flags ADD COLUMN IF NOT EXISTS company_id UUID;
CREATE POLICY "flags por empresa"
ON flags FOR ALL
USING (company_id = current_setting('app.company_id')::uuid);
```

**Modelo de dados para correlação usuário ↔ clientes:**

```sql
CREATE TABLE user_client_access (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  squad TEXT NOT NULL,
  client_id TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'viewer', -- admin, editor, viewer
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(user_id, client_id)
);
```

### 4. Fluxo de Login e Autenticação

```
Usuário faz login → OpenCode Multi-User
  → Container Docker dedicado
  → opencode.json específico (com tokens dele)
  → .env com credenciais dele
  → Filesystem com só as KBs dele
  → Supabase RLS filtra pelo user_id dele
```

## Matriz de Decisão

| Abordagem | Complexidade | Isolamento | Manutenção |
|---|---|---|---|
| Container por usuário + RLS | Média | Alto | Baixa |
| Schema separado por cliente | Alta | Máximo | Alta |
| Tudo na mesma tabela com RLS | Baixa | Médio | Média |
| Snowflake/ClickHouse externo | Muito alta | Máximo | Muito alta |

**Recomendação:** Container por usuário + RLS no Supabase. É o melhor custo-benefício.

## Próximos Passos (se aprovado)

1. Criar script de setup de novo usuário (container + config + tokens)
2. Implementar RLS no Supabase nas tabelas existentes
3. Criar tabela `user_client_access` com correlação usuário ↔ cliente
4. Adicionar endpoint no agent-orchestrator que valida acesso antes de processar fila
5. Documentar onboarding de novo usuário (skill [[onboarding-multiuser]])
