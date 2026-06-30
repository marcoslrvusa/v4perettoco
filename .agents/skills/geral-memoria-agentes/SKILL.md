---
name: geral-memoria-agentes
description: >
  Memória semântica para agentes OpenCode. Busca o que já funcionou parecido
  com o contexto atual (cliente, nicho, tipo de tarefa) usando pgvector no
  Supabase, em vez de começar do zero. Use para consultar "o que já funcionou
  parecido com isso". ATIVE AUTOMATICAMENTE: sempre que for iniciar QUALQUER
  trabalho para um cliente/nicho, SEMPRE busque memórias similares primeiro.
  Também registre automaticamente ao final de cada tarefa concluída. Setup
  inicial requer pgvector habilitado no Supabase.
area: geral
author: Marcos Luciano Rodrigues Vieira
version: 1.0.0
---

# Memória Semântica de Agentes (geral-memoria-agentes)

## O que é

Uma base vetorial (pgvector no Supabase) que armazena o que os agentes já fizeram e deu certo. Em vez de começar do zero, o agente consulta automaticamente as memórias mais similares ao contexto atual — cliente, nicho, tipo de tarefa, estratégias usadas e resultados obtidos.

## Comportamento automático (critical)

**SEMPRE** que você for trabalhar em qualquer tarefa:

1. **ANTES de planejar** → busque memórias similares com `search.py`
2. **DEPOIS de concluir** → registre o que foi feito com `record.py`

Isso vale para TODO trabalho: SEO, copy, tráfego, check-in de account, análise de dados, configuração de infra, etc. **Não pule este passo.** A qualidade do seu output depende do contexto que as memórias fornecem.

## Setup inicial (uma vez)

Antes de usar, habilite pgvector e crie as tabelas no Supabase:

**Automático** (se tiver SUPABASE_PAT):
```bash
export SUPABASE_URL="https://gswzuzetverulcgzhynb.supabase.co"
export SUPABASE_SERVICE_KEY="<service_role_key>"
export SUPABASE_PAT="<personal_access_token>"
python .agents/skills/geral-memoria-agentes/scripts/setup.py
```

**Manual** (recomendado na primeira vez):
1. Acesse [Supabase Dashboard → SQL Editor](https://supabase.com/dashboard/project/gswzuzetverulcgzhynb/sql/new)
2. Copie e cole o conteúdo de `scripts/setup/supabase-schema.sql`
3. Execute

### Variáveis de ambiente (configurar no OpenCode)

Configure no seu ambiente ou no `~/.bashrc`:
```bash
export SUPABASE_URL="https://gswzuzetverulcgzhynb.supabase.co"
export SUPABASE_SERVICE_KEY="<service_role_key>"
export OPENAI_API_KEY="<sua_chave_openai>"
```

## Como buscar memórias (search)

Antes de começar qualquer trabalho, gere o embedding do contexto atual e busque:

```bash
python .agents/skills/geral-memoria-agentes/scripts/search.py \
  --query "fazer auditoria SEO para e-commerce de moda masculina, foco em páginas de produto" \
  --client "fips-nautica" \
  --niche "moda" \
  --role "seo-visibilidade" \
  --task-type "seo-audit" \
  --threshold 0.7 \
  --limit 5
```

Parâmetros:
| Flag | Descrição |
|---|---|
| `--query` | Descrição completa do que você vai fazer (obrigatório) |
| `--client` | Filtrar por cliente (opcional — SEMPRE passe se souber) |
| `--niche` | Filtrar por nicho (opcional) |
| `--role` | Filtrar por papel de agente (opcional) |
| `--task-type` | Filtrar por tipo de tarefa (opcional) |
| `--threshold` | Similaridade mínima 0-1 (default 0.7; 0.5 é mais abrangente) |
| `--limit` | Máx. resultados (default 5) |

**Saída**: JSON com memórias ordenadas por similaridade. Use o campo `strategy` e `result` de cada resultado para informar sua abordagem.

**Dica**: Se os filtros restringirem demais, rode sem eles primeiro (só `--query`) e depois refine. Se vierem poucos resultados, baixe o `--threshold` para 0.5.

## Como registrar memórias (record)

Após concluir qualquer trabalho, registre o que foi feito e o resultado:

```bash
python .agents/skills/geral-memoria-agentes/scripts/record.py \
  --content "Auditoria SEO completa para fips-nautica. Analisei 47 páginas de produto e identifiquei: meta descriptions duplicadas, falta de schema.org/Product, imagens sem alt text, URLs não canônicas. Recomendei rewrites de meta descriptions, implementação de Product structured data, otimização de imagens e canonical tags." \
  --summary "SEO audit — e-commerce moda masculina" \
  --client "fips-nautica" \
  --niche "moda" \
  --agent-role "seo-visibilidade" \
  --task-type "seo-audit" \
  --strategy "Auditoria técnica + on-page: crawler com Screaming Frog, análise de structured data com Google Rich Results Test, revisão manual de meta tags e conteúdo" \
  --result "47 páginas auditadas, 12 críticos encontrados, recomendações entregues em relatório HTML" \
  --success-score 8 \
  --tags '["seo","audit","ecommerce","structured-data"]' \
  --metadata '{"paginas_analisadas": 47, "criticos": 12}'
```

Parâmetros:
| Flag | Descrição |
|---|---|
| `--content` | Descrição completa do trabalho (obrigatório — usado para embedding) |
| `--summary` | Título resumido (obrigatório) |
| `--client` | Cliente (obrigatório se souber) |
| `--niche` | Nicho (obrigatório se souber) |
| `--agent-role` | Seu papel de agente |
| `--task-type` | Tipo de tarefa |
| `--strategy` | Abordagem/estratégia usada (MUITO importante — é o que vai ser reusado) |
| `--result` | Resultado obtido |
| `--success-score` | Nota 1-10 do quão bem funcionou |
| `--tags` | Array JSON de tags |
| `--metadata` | Objeto JSON com dados extras |

**IMPORTANTE**: Quanto mais rico o `--strategy` e `--result`, mais útil a memória será no futuro. O embedding é gerado a partir da concatenação de summary + content + client + niche + strategy + result.

## Gatilhos automáticos de ativação

Use esta skill SEMPRE que:

- ✅ For iniciar um trabalho novo para QUALQUER cliente ou nicho
- ✅ For planejar uma estratégia (SEO, copy, tráfego, etc.)
- ✅ For fazer uma auditoria, diagnóstico ou análise
- ✅ For criar conteúdo, campanha ou relatório
- ✅ For configurar infraestrutura para um projeto
- ✅ For fazer check-in, reunião ou call com cliente
- ✅ For escrever código para um projeto específico
- ✅ Finalizar qualquer tarefa (para registrar o aprendizado)

Não use quando:
- ❌ Tarefas genéricas sem contexto de cliente/nicho
- ❌ Perguntas factuais simples ("o que é SEO?")
- ❌ O setup do Supabase ainda não foi feito

## Exemplo de uso completo (fluxo do agente)

```
1. Recebe: "Faz uma análise de concorrência para o cliente XYZ"
2. ANTES: python search.py --query "análise de concorrência" --client "XYZ" --limit 3
   → Retorna: 2 memórias de análises anteriores com estratégias e resultados
3. USA os insights das memórias para planejar a abordagem
4. FAZ o trabalho usando o contexto das memórias
5. DEPOIS: python record.py \
     --summary "Análise de concorrência — nicho saúde" \
     --client "XYZ" \
     --strategy "Analisei top 5 concorrentes via SimilarWeb + SEMrush" \
     --result "14 oportunidades identificadas, entregue em deck" \
     --success-score 9
```

## Dependências

- Python 3.8+ com pacotes: `openai`, `requests` (já instalados no sistema)
- Supabase com extensão pgvector habilitada
- Chave de API OpenAI (para geração de embeddings)
- Service Role Key do Supabase
