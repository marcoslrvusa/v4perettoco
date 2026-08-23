# PROMPT A3 — DATA & AGENTS (Cole no ORCA aberto em ../orca-data-agents)

Você é o agente A3 do projeto HUB TÁTICO OPERACIONAL V4. Sua branch é `ws3/data-agents`. Leia primeiro: `Harness Engineering/PLANO-MESTRE-HUB-TATICO-V4.md`, `Harness Engineering/ESTADO-ATUAL-E-OBJETIVOS-V4.md` e `../orca-contracts/pace-schema.sql`.

## Regras inegociáveis
1. **NUNCA commite na main** — só na sua branch. Commit a cada bloco.
2. **Sync da Matriz é MANUAL** (planilha muda mensal; SEM cron no MVP). Destino é o **PRODUTO**, não o DADOS: `PRODUTO.matriz_operacional`.
3. **O .xlsx real NUNCA vai para o git** — caminho via env `MATRIZ_XLSX_PATH`. No repo: só script + `matriz-column-map.json` + fixture anonimizada (`tests/fixtures/matriz-sample.xlsx` com dados fictícios).
4. **Agentes Hub NUNCA calculam números** — recebem L1-L4 já calculados e só interpretam.
5. Modelos dos agentes: `primary` via LiteLLM (ox-alpha-free → failover Gemini free). Credenciais via env; pergunte se faltar.

## ENTREGA 1 — migrations/produto_okr_pace.sql
SQL completo para rodar no Supabase PRODUTO (SQL Editor), idempotente (IF NOT EXISTS / OR REPLACE):

1. `okr_pace_snapshots` conforme Plano Mestre §3 (todas as colunas L1-L4, overall_semaforo CHECK, recommended_actions JSONB, raw_data JSONB, created_at)
2. View `v_okr_pace_latest` usando **created_at** no ORDER BY (NÃO existe snapshot_time)
3. `matriz_operacional` conforme Plano Mestre §8 (cliente PK, squad, okr_type CHECK, ekyte_workspace_id, status, account_email, raw JSONB, synced_at)
4. `okr_pace_monthly_agg` (client, mes, avg_semaforo, avg_prob_hit)
5. Extensões `agent_queue`: `ADD COLUMN IF NOT EXISTS csm_comment TEXT, coordinator_decision JSONB, ekyte_project_id UUID, commented_by TEXT, idempotency_key TEXT UNIQUE`
6. **RLS dia 1**: ENABLE ROW LEVEL SECURITY + policy SELECT para authenticated nas tabelas novas (escrita só service_role)
7. Índices: idx_pace_client_date, idx_pace_semaforo, idx_matriz_status

Inclua comentário no topo: "Executar no SQL Editor do PRODUTO (bkenzsvexfayjcrqnmpx)".

## ENTREGA 2 — scripts/sync_matriz_operacional.py
Python 3.11, deps apenas openpyxl + requests (ou supabase-py):
- Lê `MATRIZ_XLSX_PATH` (env; erro claro se ausente)
- Aba `DB_Matriz_Operacional_Ago26`; introspeciona header row detectando colunas por heurística (cliente/nome, squad/equipe, okr_type|tipo_okr|modelo_okr, workspace/ekyte, status, account/responsavel) → merge com overrides de `matriz-column-map.json`
- Upsert idempotente em `PRODUTO.matriz_operacional` (ON CONFLICT cliente) preservando linha original em raw JSONB
- Output final: `{inseridos, atualizados, sem_okr_type: [clientes], workspace_fallback_warning: [clientes sem workspace → 16032]}`
- Normaliza status ("Ativo"/"ativo"/"ATIVO" → 'Ativo')

## ENTREGA 3 — scripts/sync_pessoas.py + map_ekyte_workspace.py
- pessoas: aba `DB_Pessoas_Atualizado` → upsert `PRODUTO.DB_Pessoas_Atualizado` (emailv4company como chave natural)
- map_ekyte: lê `matriz_operacional` → gera `ekyte-workspace-map.json` {squad→workspace_id} + warning list do fallback 16032

## ENTREGA 4 — scripts/ingest_qdrant.py
Deps: qdrant-client + sentence-transformers OU chamada de embedding via API (prefira OpenAI text-embedding-3-small se OPENAI_API_KEY existir; senão local MiniLM 384d — ajuste vector_size conforme escolha e documente).
Cria/popula collections de `../orca-contracts/qdrant-collections.json`:
- `skills`: varre `.agents/skills/**/SKILL.md` e `.opencode/skills/**/SKILL.md` do repo principal (caminho configurável env `REPO_ROOT`)
- `runs`: últimos 90d de `PRODUTO.routine_runs` (id, modo, resumo, output_summary truncado)
- `clients`: de `matriz_operacional` + mission_controls se disponível
- Batch 100 pontos/upsert; payload com source path/tabela p/ citação no dashboard
- Ao final: snapshot diário = dump das collections para volume `/data/qdrant-snapshots` (função chamável + instrução cron comentada)

## ENTREGA 5 — agents/ (OpenCode)
Crie os 2 agentes E copie para `.opencode/agents/` do repo principal:

**agents/okr-pace-analyzer.md** — frontmatter: name okr-pace-analyzer, model primary. Corpo: recebe {client_id, pace_snapshot com L1..L4 numéricos, client_kb}; PROIBIDO inventar/calcular números; aplica FPA + TOC + Médico vs Garçom sobre os números recebidos; retorna APENAS JSON {causa_raiz, pilares_deficientes[], recommended_actions[{funcao(GT|COPY|DESIGNER|CSM|ACCOUNT), acao, prazo YYYY-MM-DD, dono, evidencia}]}. PT-BR.

**agents/action-planner.md** — mesma base; input {semaforo, gaps, client_context}; retorna {actions[...]} priorizado por impacto x esforço; ações específicas e executáveis (não genéricas).

Instrua no corpo de ambos: "Se faltar dado no input, sinalize no campo gaps_detectados — nunca preencha com suposição."

## ENTREGA 6 — testes rápidos
- Rode sync contra a fixture anonimizada apontando um Supabase LOCAL de teste ou dry-run mode (--dry-run imprime SQL sem executar)
- Valide migration num Postgres docker efêmero (postgres:16-alpine) antes de entregar

## Critério de pronto
- [ ] Migration roda limpa 2x seguidas (idempotente) no postgres efêmero
- [ ] Sync --dry-run na fixture → output correto
- [ ] Agentes registrados em .opencode/agents/ e respondem JSON no formato especificado
- [ ] Commits atômicos na ws3/data-agents
Ao terminar: resuma entregas + passo-a-passo para o usuário rodar o sync manual real (env MATRIZ_XLSX_PATH + python3 scripts/sync_matriz_operacional.py).
