---
name: geral-contexto-cliente
description: "Puxa, registra e sincroniza fatos exatos do cliente (tom de voz, histórico, oferta) no Supabase pra alimentar o trabalho do agente. Use SEMPRE que for trabalhar em qualquer tarefa para um cliente — o agente DEVE puxar o contexto automaticamente antes de começar. Também use quando o usuário mencionar 'contexto do cliente', 'fatos do cliente', 'tom de voz', 'quem é o cliente', 'histórico com o cliente', 'antes de começar puxa o contexto', 'cliente X', ou quiser consultar/atualizar dados do cliente."
area: geral
version: 1.0.0
---
# Contexto de Cliente (geral-contexto-cliente)

## O que é

Armazena no Supabase os **fatos exatos e estruturados** de cada cliente — tom de voz, histórico comercial, oferta, e fatos extras — pra que QUALQUER agente possa puxar esse contexto automaticamente antes de trabalhar.

Diferente da `geral-memoria-agentes` (que guarda o que OS AGENTES fizeram e funcionou), esta skill guarda os FATOS DO CLIENTE: quem ele é, como fala, o que comprou, o que vendemos pra ele.

## Comportamento automático (CRÍTICO)

**ANTES** de começar QUALQUER trabalho envolvendo um cliente identificável:

1. **Detecte o nome do cliente** no prompt do usuário ou no diretório atual
2. **Puxe o contexto automaticamente**:
   ```bash
   python .agents/skills/geral-contexto-cliente/scripts/context.py pull --client NOME_DO_CLIENTE
   ```
3. **Use os dados puxados** pra informar TUDO que você produzir — tom de voz, oferta e histórico devem influenciar cada decisão
4. **Se não encontrar contexto**, avise: "Cliente sem contexto no Supabase. Quer rodar `context.py sync --client NOME` pra puxar da KB local?"

**DEPOIS** de concluir o trabalho (se descobriu fatos novos ou atualizações):

```bash
python .agents/skills/geral-contexto-cliente/scripts/context.py push --client NOME \
  --tom-de-voz "..." --historico "..." --oferta "..."
```

Ou registre automaticamente via `sync --client NOME` se a KB local foi atualizada.

## Setup inicial (uma vez)

### 1. Schema no Supabase

```bash
export SUPABASE_URL="https://gswzuzetverulcgzhynb.supabase.co"
export SUPABASE_SERVICE_KEY="<service_role_key>"
export OPENAI_API_KEY="<sua_chave_openai>"
```

Acesse [Supabase Dashboard → SQL Editor](https://supabase.com/dashboard/project/gswzuzetverulcgzhynb/sql/new) e execute o conteúdo de `scripts/setup/supabase-schema.sql`.

### 2. Variáveis de ambiente

Já devem estar configuradas se você já usa `geral-memoria-agentes`. Verifique:

```bash
echo $SUPABASE_URL
echo $SUPABASE_SERVICE_KEY
echo $OPENAI_API_KEY
```

Se faltar alguma, configure no `~/.bashrc` ou no OpenCode.

## Como usar

### Puxar contexto de um cliente (mais comum)

```bash
python .agents/skills/geral-contexto-cliente/scripts/context.py pull --client fips-nautica
```

Puxa campo específico:

```bash
python .agents/skills/geral-contexto-cliente/scripts/context.py pull --client fips-nautica --field tom_de_voz
```

### Registrar/atualizar contexto manualmente

```bash
python .agents/skills/geral-contexto-cliente/scripts/context.py push \
  --client fips-nautica \
  --squad "squad-exemplo" \
  --tom-de-voz "Tom jovem e descontraído, usa gírias náuticas, primeira pessoa do singular" \
  --historico "Cliente desde jan/2025. Já fizemos: auditoria SEO (fev), campanha Meta (mar-mai)" \
  --oferta "Serviço completo de SEO + Mídia Paga, pacote mensal de R$ X.XXX" \
  --facts '{"segmento":"moda masculina","publico_alvo":"homens 25-45 anos A/B","diferenciais":"roupas com tecnologia de secagem rápida"}'
```

### Sincronizar da KB local (automático)

Puxa os dados do `CLAUDE.md` e `mission-control/` do cliente e sobe pro Supabase:

```bash
# Cliente específico
python .agents/skills/geral-contexto-cliente/scripts/context.py sync --client fips-nautica

# TODOS os clientes de uma vez
python .agents/skills/geral-contexto-cliente/scripts/context.py sync --all
```

O script detecta automaticamente a raiz do Builders Hub, encontra o cliente em `squads/*/clientes/{cliente}/` e extrai:
- **Tom de voz** → seção "Tom de Voz" ou "Posicionamento" do CLAUDE.md
- **Histórico** → seção "Histórico" + `mission-control/historico-checkins.md` + `combinados.md`
- **Oferta** → seção "Oferta/Produto" + "Negócio" do CLAUDE.md
- **Fatos extras** → segmento, público, canais, investimento, métricas do CLAUDE.md

### Buscar contextos por similaridade semântica

```bash
python .agents/skills/geral-contexto-cliente/scripts/context.py search \
  --query "cliente de moda masculina com tom jovem e descontraído"
```

### Listar todos os clientes com contexto

```bash
python .agents/skills/geral-contexto-cliente/scripts/context.py list
```

### Remover contexto

```bash
python .agents/skills/geral-contexto-cliente/scripts/context.py delete --client fips-nautica
```

## Gatilhos de ativação automática

Sempre que:

- ✅ Você começar uma tarefa e conseguir identificar o cliente (pelo prompt, diretório, ou KB)
- ✅ O usuário mencionar "contexto", "fatos do cliente", "tom de voz", "quem é o cliente"
- ✅ O usuário disser "antes de começar, puxa o contexto do cliente"
- ✅ O usuário mencionar o nome de um cliente que você sabe que existe no Supabase
- ✅ Você for escrever qualquer coisa pro cliente (email, copy, relatório, análise)
- ✅ Você for fazer uma auditoria ou diagnóstico para um cliente

Não use quando:

- ❌ A tarefa não tem cliente associado (genérica, interna, infraestrutura)
- ❌ O contexto já foi puxado na mesma sessão (não repita sem necessidade)
- ❌ O setup do Supabase ainda não foi feito

## Exemplo de fluxo completo

```
1. Usuário: "Preciso escrever um email pro cliente Fips Náutica sobre a nova campanha"
2. AGENTE DETECTA: cliente = "fips-nautica"
3. AGENTE PUXA:
   python context.py pull --client fips-nautica
   → Retorna: tom de voz (jovem, náutico, primeira pessoa), histórico (cliente desde jan/2025),
     oferta (SEO + mídia paga), fatos extras (moda masculina, público 25-45 anos A/B)
4. AGENTE USA esses fatos pra escrever o email no tom certo, mencionando
   o histórico e alinhado com a oferta
5. Se descobrir algo novo durante a conversa:
   python context.py push --client fips-nautica --facts '{"nova_info":"descoberta na call"}'
6. FIM
```

## Estrutura dos dados no Supabase

Tabela `client_context` no mesmo projeto Supabase da `agent_memories`:

| Campo | Tipo | Descrição |
|---|---|---|
| `client` | TEXT (UNIQUE) | Nome do cliente (slug) |
| `squad` | TEXT | Squad ao qual pertence |
| `tom_de_voz` | TEXT | Guia de tom de voz, personalidade, linguagem |
| `historico` | TEXT | Histórico de interações, projetos, combinados |
| `oferta` | TEXT | Produtos/serviços contratados, proposta de valor |
| `facts` | JSONB | Fatos extras (segmento, público, diferenciais, canais, métricas) |
| `embedding` | VECTOR(1536) | Embedding semântico para busca por similaridade |
| `source` | TEXT | kb-sync, manual, ou agent-record |
| `created_at` | TIMESTAMPTZ | Quando foi criado |
| `updated_at` | TIMESTAMPTZ | Última atualização |

## Dependências

- Python 3.8+ com pacotes: `openai`, `requests`
- Supabase com extensão pgvector habilitada
- Chave de API OpenAI (para embeddings)
- Service Role Key do Supabase
