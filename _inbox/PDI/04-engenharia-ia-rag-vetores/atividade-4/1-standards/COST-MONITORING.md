# STANDARD: Monitoramento de Custo LLM

Padrão de telemetria de inferência: o que é emitido por execução, onde é gravado, com qual
cardinalidade, o que dispara alerta e como se audita a conta. É a camada que transforma o cálculo
de `LLM-COST.md` em dado confiável e o teto de `BUDGET.md` em controle automático.

## 1. Escopo e não-escopo

**Escopo:** captura de tokens por execução, cálculo de custo com a tabela de preço vigente,
persistência no ledger, agregação diária, alertas e reconciliação entre chamadas e linhas.

**Não-escopo:** definição de teto (é `BUDGET.md`), escolha de modelo (é `LLM-COST.md`), rastreio de
latência de ponta a ponta (pertence à observabilidade de aplicação) e auditoria de conteúdo de
prompt (pertence à governança).

## 2. Regra de captura

- **Capture:** log de `prompt_tokens`, `completion_tokens`, `model`, `agent` por Run.
- **Custo:** tabela de preço por 1k tokens (atualizar mensal).
- **Alerta:** orçamento diário por agente; 80% → warn, 100% → bloqueio.
- **Otimização:** cache de prompt, modelo menor para tarefas simples.

Campos mínimos por linha do ledger:

| Campo | Tipo | Origem | Observação |
| --- | --- | --- | --- |
| `id` | bigserial | banco | chave da linha |
| `agent` | text | aplicação | identifica o fluxo que gastou |
| `model` | text | resposta da API | modelo efetivamente chamado |
| `prompt_tokens` | int | resposta da API | entrada |
| `completion_tokens` | int | resposta da API | saída |
| `cost_usd` | numeric(10,4) | cálculo | nunca nulo, nunca negativo |
| `created_at` | timestamptz | banco | padrão `now()`, fuso explícito |

Esquema de referência (`3-supabase/usage_schema.sql`):

```sql
create table llm_usage (
  id bigserial primary key,
  agent text,
  model text,
  prompt_tokens int,
  completion_tokens int,
  cost_usd numeric(10,4),
  created_at timestamptz default now()
);
create index on llm_usage (agent, created_at);
```

O índice composto `(agent, created_at)` existe por causa das duas consultas mais rodadas: consumo
por fluxo na janela corrente e digest diário por `agent`. Consultas por `model` ou por razão de
cache são agregações mensais e não justificam índice próprio até prova em contrário.

## 3. Fórmula de custo no ponto de captura

```
custo_usd = (prompt_tokens * preco_in + completion_tokens * preco_out) / 1.000.000
```

com o par de preços escolhido pelo `model` retornado pela API. Se o modelo não existir na tabela
de preço, grava-se com o preço de fallback, incrementa-se `llm_unknown_price_total` e abre-se
alerta: preço ausente é bug de configuração, não desconto.

**Exemplo numérico (parâmetros declarados: `prompt_tokens = 500`, `completion_tokens = 200`, modelo `mini`, preço `$in = 0.15/1M` e `$out = 0.60/1M`):**

```
custo_usd = (500 * 0.15 + 200 * 0.60) / 1.000.000
          = (75 + 120) / 1.000.000
          = 0.000195 USD  ->  gravado como 0.0002 em numeric(10,4)
```

Atenção à precisão: `numeric(10,4)` arredonda para a quarta casa. Sozinho isso perderia a
resolução de execuções baratas. A regra é arredondar só na apresentação e guardar o custo com
mais casas, ou acumular em centavos por `agent` antes de gravar. Enquanto a granularidade for
diária e por fluxo, a perda é aceitável; se a precisão por execução importar, mude a coluna para
`numeric(18,8)` e registre a migração no ADR correspondente.

## 4. Agregação e consultas de operação

Consumo por agente em 1 dia (rotina de checagem diária):

```sql
select agent,
       model,
       count(*)                as execucoes,
       sum(prompt_tokens)      as tokens_in,
       sum(completion_tokens)  as tokens_out,
       sum(cost_usd)           as custo_usd
from llm_usage
where created_at > now() - interval '1 day'
group by agent, model
order by custo_usd desc;
```

Razão de cache por fluxo (meta: maior ou igual a 30%):

```sql
select agent,
       count(*) filter (where from_cache) as hits,
       count(*)                           as total,
       count(*) filter (where from_cache)::numeric / count(*) as hit_rate
from llm_usage
group by agent;
```

> Observação de implementação: a coluna `from_cache` é o campo que permite auditar a meta de
> hit rate. Se o esquema atual não a tiver, acrescente como `boolean not null default false`
> antes de publicar o dashboard, e faça a migração em janela de manutenção.

Reconciliação diária (invariante: toda execução vira exatamente uma linha):

```sql
select d.dia,
       d.execucoes,
       d.ledger_linhas,
       d.execucoes - d.ledger_linhas as divergencia
from (
  select date_trunc('day', created_at) as dia,
         count(*) as ledger_linhas,
         sum(case when cost_usd is null or cost_usd < 0 then 1 else 0 end) as invalidas
  from llm_usage group by 1
) d;
```

## 5. Alertas

| Alerta | Condição | Destinatário | Ação esperada |
| --- | --- | --- | --- |
| Warn de orçamento | razão diária >= 80% | account no Slack | revisar consumo por `agent` |
| Bloqueio | razão diária >= 100% | automático + engenharia | pausar agentes não-críticos |
| Hit rate baixo | abaixo de 30% em 7 dias | engenharia de IA | revisar limiar e normalização |
| Preço desconhecido | qualquer ocorrência | engenharia de IA | atualizar tabela no mesmo dia |
| Ledger divergente | execuções x linhas != 0 | engenharia de IA | reprocessar fila pendente |
| Volume anômalo | pico acima do histórico sem campanha | engenharia + account | investigar loop ou retry |

Cardinalidade: os alertas usam apenas `agent`, `model` e `cliente` como rótulo. Sem `user_id`,
sem `session_id`, sem hash de prompt. Detalhe fino é consulta no ledger, não métrica.

## 6. Anti-padrões

1. Medir custo só na plataforma do fornecedor: você não consegue cruzar com o seu `agent`.
2. Enviar token de prompt como rótulo: estoura cardinalidade e derruba a coleta.
3. Calcular custo em memória sem gravar linha: perde tudo no restart e não audita.
4. Contar hit rate sem rótulo de fluxo: média global esconde o fluxo que não usa cache.
5. Alertar por valor absoluto: o teto é por cliente, o absoluto global não diz nada.
6. Atualizar preço "depois": a tabela de preço é configuração versionada, com data de vigência.
7. Confiar em `created_at` sem fuso: gravar sempre com `timestamptz`.

## 7. Plano de teste

| Caso | Critério de aceite |
| --- | --- |
| Execução normal | 1 linha, `cost_usd > 0`, `model` = retornado pela API |
| Resposta de cache | 1 linha, `from_cache = true`, `cost_usd = 0` |
| Modelo novo sem preço | fallback aplicado e contador de preço desconhecido incrementado |
| Falha da API no meio da execução | nenhuma linha de sucesso, fila de retry não duplica custo |
| Reprocessamento de fila | linha idempotente por `id` de execução, sem duplicidade |
| Consulta diária | retorna em tempo aceitável com 1 mês de dados e índice `(agent, created_at)` |
| Reinhício do coletor | contagem do ledger não zera, sem perda de linha |

## 8. Checklist de adesão

1. `prompt_tokens` e `completion_tokens` vêm da resposta da API, não de contagem local.
2. `model` é o efetivamente chamado.
3. `cost_usd` nunca é nulo nem negativo.
4. Tabela de preço tem dono, data de revisão e processo mensal.
5. Existe índice para as duas consultas mais rodadas.
6. Hit rate é calculável por `agent` em uma consulta.
7. Alerta de 80% entregue a pessoa que pode agir.
8. Bloqueio de 100% não derruba agentes críticos.
9. Reconciliação execuções x linhas roda todo dia.
10. Cardinalidade limitada a `agent`, `model` e `cliente`.
11. Fuso de `created_at` é explícito em todas as consultas.
12. Dashboard mostra o mesmo número do ledger (nenhum cálculo paralelo).

## 9. Referências

- Doc oficial: Guia de preços e tokens da API, documentação oficial OpenAI.
- Doc oficial: Guia de prompt caching, documentação oficial Anthropic.
- Curso: FinOps for AI and LLM Cost Optimization, plataforma Udemy.
