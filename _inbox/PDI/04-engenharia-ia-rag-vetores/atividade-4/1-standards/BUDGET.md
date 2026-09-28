# Política de Budget por Cliente

Padrão operacional de teto de gasto: quanto, quando alerta, quando bloqueia, quem decide e o que
se faz quando a conta chega perto do limite. Complementa `LLM-COST.md` (que calcula) e
`COST-MONITORING.md` (que mede).

## 1. Escopo e não-escopo

**Escopo:** teto mensal por cliente, faixas de ação, responsável por faixa, cadência de revisão,
regra de bloqueio e o que é liberado mesmo com teto cheio.

**Não-escopo:** definição de preço comercial; teto por projeto interno (usa o mesmo mecanismo,
com `cliente` igual ao código do projeto); e custos não relacionados a inferência.

## 2. Política

- Teto mensal no onboarding (ex.: R$ 200).
- Alerta em 80% (Slack p/ account).
- Em 100%: pausa agentes não-críticos.
- Revisão mensal.

## 3. Faixas de ação

| Faixa | Razão de consumo | Ação | Responsável | Prazo |
| --- | --- | --- | --- | --- |
| 0 a 60% | consumo normal | nada | automático | sem ação |
| 60 a 80% | aproximação | digest semanal no canal do cliente | automático | semanal |
| 80 a 99% | alerta | aviso no Slack para a account com consumo por `agent` | automático | imediato |
| 100% | bloqueio | pausa de agentes não-críticos | automático | imediato |
| Acima de 100% | estouro | incidente, revisão de escopo com o cliente | account + engenharia | 1 dia útil |
| Teto revisado | mudança de contrato | novo teto publicado e reavaliado | account | na renegociação |

Lista de agentes não-críticos é versionada no repositório, com dono. Agente crítico é aquele
cuja indisponibilidade quebra compromisso contratual; listar menos agentes como críticos é a
postura padrão, porque reduz o dano do bloqueio.

## 4. Modelo de dados e cálculo

O teto é dado de configuração por cliente, e o consumo é a soma do ledger na janela corrente:

```sql
select
  c.cliente,
  c.teto_mensal,
  sum(u.cost_usd) as consumo,
  sum(u.cost_usd) / nullif(c.teto_mensal, 0) as razao
from llm_usage u
join budget_cliente c on c.cliente = u.agent
where u.created_at >= date_trunc('month', now())
group by 1, 2;
```

Regras de cálculo:

1. A janela é calendário (`date_trunc('month')`), não dias móveis; contrato e fatura falam o mesmo período.
2. A razão é calculada sobre o teto **em moeda do ledger**; se o teto for em R$, existe conversão versionada.
3. Consumo em andamento entra: o teto usa `sum` sobre o que já foi gravado, sem previsão.
4. Teto ausente ou zero **nunca** significa consumo ilimitado: significa configuração inválida e alerta.
5. O alerta é idempotente: reenviar o mesmo aviso a cada nova execução é ruído, não controle.

## 5. Exemplo numérico

**Exemplo numérico (parâmetros declarados: teto de R$ 200, dia 12 de 30, consumo acumulado de R$ 148):**

```
razao = 148 / 200 = 0.74  ->  faixa 60-80%, digest semanal
projecao de fim de mes = 148 / 12 * 30 = 370 R$   (meta de extrapolação linear)
projecao acima do teto -> antecipar revisao, nao esperar o dia 30
```

**Exemplo numérico (mesmo cliente, dia 25, consumo de R$ 164):**

```
razao = 164 / 200 = 0.82  ->  alerta imediato no Slack para a account
```

A projeção linear é deliberadamente grosseira e serve só para antecipar conversa; a decisão de
bloqueio é sempre pelo consumo real, nunca pela projeção.

## 6. Anti-padrões

1. Teto global da empresa escondendo um cliente que consome sozinho 70% do total.
2. Alerta em 100%: nesse momento o dinheiro já saiu, o alerta virou confirmação.
3. Zerar o consumo manualmente para "deixar rodar" sem registrar a decisão.
4. Agente crítico demais: se tudo é crítico, o bloqueio não bloqueia nada.
5. Comparar consumo em USD com teto em R$ sem taxa versionada.
6. Revisar teto só quando estoura; a revisão é mensal e preventiva por definição.

## 7. Telemetria

| Métrica | Cardinalidade | Alerta |
| --- | --- | --- |
| `budget_usage_ratio` | `cliente` | 80% warn, 100% bloqueio |
| `budget_blocked_agents_total` | `cliente`, `agent` | qualquer aumento é revisado |
| `budget_config_missing_total` | `cliente` | qualquer ocorrência |
| `budget_fx_stale_total` | par de moedas | taxa de conversão mais antiga que 1 dia |

## 8. Plano de teste

| Caso | Critério de aceite |
| --- | --- |
| Consumo simulado em 79% | nenhum alerta de bloqueio |
| Consumo simulado em 80% | exatamente um alerta entregue à account |
| Consumo simulado em 100% | agentes não-críticos pausados, críticos ativos |
| Teto não configurado | alerta de configuração ausente, nunca consumo livre |
| Reinício do serviço durante a janela | consumo não zera (estado vem do banco) |
| Dois clientes na mesma janela | razões independentes, sem contaminação |

## 9. Checklist de adesão

1. Todo cliente de produção tem teto configurado antes do onboarding.
2. A faixa de 80% foi testada com consumo simulado.
3. A lista de agentes não-críticos está versionada e tem dono.
4. O bloqueio pausa sem derrubar agentes críticos.
5. A razão de consumo é calculada no banco, não em memória.
6. A janela de medição é calendário e bate com a fatura.
7. Teto sem configuração gera alerta, não liberdade.
8. A account recebe o aviso com consumo por `agent`, não só a razão.
9. A revisão mensal tem data marcada e pauta definida.
10. A projeção é rotulada como projeção e não vira decisão sozinha.
11. Moeda do teto e moeda do ledger são compatíveis com taxa versionada.
12. O incidente de estouro tem postmortem com ação rastreável.

## 10. Referências

- Doc oficial: Guia de preços e tokens da API, documentação oficial OpenAI.
- Curso: FinOps for AI and LLM Cost Optimization, plataforma Udemy.
