# Engenharia de Custos de LLM

Padrão canônico de precificação de execução de LLM: fórmula, tabela de preço, roteamento por
complexidade e regra de cache. Todo código que chama modelo pago deve seguir este arquivo.

## 1. Escopo e não-escopo

**Escopo:**

- Cálculo de custo de uma execução (tokens de entrada, tokens de saída, modelo, cache).
- Roteamento de intenção para modelo leve ou modelo forte.
- Regra de quando a resposta pode ser servida de cache sem custo.
- Integração com o ledger `llm_usage` e com o teto descrito em `BUDGET.md`.

**Não-escopo:**

- Definição de preço comercial cobrado do cliente (é consequência deste padrão, não é este padrão).
- Qualidade da resposta: é tratada pelo conjunto-ouro de avaliação, que apenas veta troca de modelo.
- Custos de infraestrutura fora de inferência (armazenamento, rede, observabilidade).
- Custo de embedding de RAG: entra no mesmo ledger, mas com `agent` próprio, para não contaminar a conta de geração.

## 2. Termos

| Termo | Definição operacional |
| --- | --- |
| Token | Unidade de cobrança da API; entrada e saída têm preços diferentes |
| Custo por tarefa | Valor em USD gasto por uma execução completa do agente |
| Baseline | Custo por tarefa antes da otimização, com tudo no modelo forte e sem cache |
| Roteamento | Escolha do modelo a partir da intenção da tarefa, antes da chamada |
| Cache de prompt | Reutilização de resposta já computada para pergunta similar |
| Hit rate | Fração de execuções servidas de cache em uma janela de tempo |
| Ledger | Registro por execução com modelo, tokens e custo em reais/dólares |
| Budget | Teto de gasto por cliente em uma janela, com alerta e bloqueio |
| Intenção | Rótulo da tarefa (`triagem`, `proposta`, `analise_complexa`) usado pelo roteador |

## 3. Regra canônica

```
custo_tarefa = (in * $in + out * $out) * (1 - cache_hit)
```

Onde:

- `in` e `out`: tokens de entrada e de saída da execução, em tokens.
- `$in` e `$out`: preço do modelo escolhido, em USD por 1.000.000 de tokens.
- `cache_hit`: `1` se a resposta veio do cache, `0` se a chamada foi executada.

Tabela de preços vigente no padrão (revisada mensalmente, dono: engenharia de IA):

| Modelo | $in por 1M | $out por 1M | Cenário de uso |
| --- | --- | --- | --- |
| mini | 0.15 | 0.60 | triagem, classificação, extração, resposta curta padrão |
| maxi | 3.00 | 15.00 | proposta, análise complexa, raciocínio longo, revisão contratual |

Implementação mínima aceitável (`2-code/cost_calc.py`):

```python
PRICING = {
    "mini": {"in": 0.15/1e6, "out": 0.60/1e6},
    "maxi": {"in": 3.00/1e6, "out": 15.00/1e6},
}

def route_model(intent):
    """Escolhe o modelo a partir da intenção. Padrão: forte só quando declarado."""
    return "maxi" if intent in ("proposta", "analise_complexa") else "mini"

def cost(task, cache_hit=False):
    """Custo em USD de uma tarefa. Cache hit zera o valor da execução."""
    m = PRICING[route_model(task["intent"])]
    return (task["in"] * m["in"] + task["out"] * m["out"]) * (0.0 if cache_hit else 1.0)
```

Regras de implementação:

1. O preço **nunca** é chumbado em vários arquivos: existe uma única fonte (`PRICING`).
2. Preço desconhecido **nunca** vira zero: cai em fallback caro e gera alerta.
3. O custo é calculado **depois** da chamada, com o modelo efetivamente usado.
4. `cache_hit` é informado pelo cache, nunca inferido por similaridade de texto fora da camada de cache.

## 4. Tabela de decisão

| Se (intenção) | E (contexto) | Então (modelo) | E (cache) |
| --- | --- | --- | --- |
| triagem | qualquer | mini | permitido |
| extração | formato estruturado curto | mini | permitido |
| classificação | rótulo fechado | mini | permitido |
| proposta | texto comercial | maxi | proibido se houver PII |
| analise_complexa | múltiplos documentos | maxi | proibido |
| revisão | contrato ou cláusula | maxi | proibido |
| intenção desconhecida | qualquer | maxi (degradação cara) | permitido com cuidado |
| qualquer | entrada contém PII | definido pela intenção | **nunca** |

Decisões derivadas:

- **Se** a intenção é trivial **e** a resposta é determinística, **então** mini com cache liberado.
- **Se** a intenção é complexa **e** a resposta exige raciocínio longo, **então** maxi e cache desligado para aquele fluxo.
- **Se** a pergunta já existe no cache com similaridade acima do limiar, **então** resposta salva e custo zero.
- **Se** o cliente atingiu 80% do teto, **então** alerta; **se** atingiu 100%, **então** agentes não-críticos pausados.
- **Se** o modelo não tem preço cadastrado, **então** custo com preço de fallback e alerta imediato de tabela desatualizada.

## 5. Exemplo numérico

**Exemplo numérico (parâmetros declarados: `in = 500` tokens, `out = 200` tokens, intenção `triagem`):**

```
rota escolhida: mini
custo_miss = 500 * 0.15/1e6 + 200 * 0.60/1e6
           = 0.000075 + 0.000120
           = 0.000195 USD
custo_hit  = 0.000195 * (1 - 1) = 0 USD
```

**Exemplo numérico (mesmos parâmetros, sem roteamento, tudo no maxi):**

```
custo_maxi = 500 * 3.00/1e6 + 200 * 15.00/1e6
           = 0.001500 + 0.003000
           = 0.004500 USD
razao      = 0.004500 / 0.000195 = 23.1x
```

**Exemplo numérico (janela mensal, parâmetros declarados: 100.000 execuções, 90% triagem em mini, 30% de hit de cache):**

```
sem otimizacao = 100.000 * 0.004500 = 450.00 USD
com roteamento = 100.000 * (0.90*0.000195 + 0.10*0.004500)
               = 100.000 * 0.0006255 = 62.55 USD
com cache 30%  = 62.55 * (1 - 0.30) sobre o que sobrou = 43.79 USD   (meta)
reducao        = 1 - 43.79/450.00 = 90.3%                            (meta)
```

Todas as contas acima são projetação de comportamento (**meta**), não medição de produção.

## 6. Anti-padrões

O que o sênior reprovaria na revisão:

1. **Preço chumbado em cada módulo.** Duas fontes de preço significam duas verdades; na divergência, o ledger mente.
2. **`cost = 0` para modelo desconhecido.** Some silenciosamente a receita e esconde mudança de catálogo do fornecedor.
3. **Cache key só com o texto da pergunta.** Resposta de um cliente pode ser servida a outro; a chave precisa de `tenant_id`.
4. **Cache gravando antes do guardrail de PII.** É o vazamento mais caro do sistema, em termos de risco, não de tokens.
5. **Roteador por chamada de LLM.** Paga um modelo para decidir qual modelo pagar, adiciona latência e falha em cascata.
6. **Contar custo com o modelo pretendido e não com o chamado.** Fallback para o modelo forte fica invisível na conta.
7. **Métrica de custo sem cardinalidade de `agent`.** Gera gráfico global que ninguém consegue agir.
8. **Alerta de budget só no fim do mês.** Chega tarde demais para qualquer mitigação.
9. **Assumir que cache hit mantém qualidade igual sem medir.** Pergunta parecida com contexto diferente é resposta errada.
10. **Otimizar antes de medir baseline.** Sem número de partida, a redução de 85% é opinião.

## 7. Telemetria

| Métrica | Tipo | Cardinalidade | Alerta |
| --- | --- | --- | --- |
| `llm_cost_usd_total` | contador | `agent`, `model`, `fluxo` | somatório diário acima da parcela do budget |
| `llm_tokens_prompt_total` | contador | `model` | crescimento sem mudança de volume |
| `llm_tokens_completion_total` | contador | `model` | razão `out/in` fora da faixa histórica |
| `llm_cache_hit_rate` | gauge | `fluxo` | abaixo de 30% em janela de 7 dias |
| `llm_route_ratio` | gauge | `model` | modelo forte acima do mix esperado |
| `llm_budget_usage_ratio` | gauge | `cliente` | 80% warn, 100% bloqueio |
| `llm_unknown_price_total` | contador | `model` | qualquer ocorrência (zero tolerância) |

Regras de cardinalidade: nunca usar `user_id`, `prompt` ou `session_id` como rótulo de métrica. O detalhe fino vive no ledger `llm_usage` (consulta por SQL), e a métrica agregada fica barata. Se o volume de INSERT incomodar, agregue em janelas de 1 minuto e faça flush, sem perder a linha por execução no ledger.

## 8. Plano de teste

| Caso | Entrada esperada | Critério de aceite |
| --- | --- | --- |
| Tarefa trivial, cache miss | rota `mini`, custo `0.000195` USD | igual à conta da seção 5 |
| Tarefa trivial, cache hit | custo `0` | `cost(..., cache_hit=True) == 0` |
| Intenção `proposta` | rota `maxi` | valor igual à conta de referência |
| Intenção desconhecida | rota `maxi` com alerta | degradação cara, nunca barata por engano |
| Entrada com PII | cache não gravado | nenhuma linha nova no armazenamento de cache |
| Modelo sem preço | fallback + alerta | `llm_unknown_price_total` incrementa |
| Teto em 80% | alerta disparado | notificação entregue à account |
| Teto em 100% | agentes não-críticos pausados | agentes críticos continuam rodando |
| Migração de tabela de preço | ledger usa preço novo | soma diária muda no mesmo dia da publicação |
| Resposta em lote dentro do SLA | custo com desconto e prazo cumprido | p95 dentro da janela declarada |

Executar também teste de propriedade: para toda intenção da lista de triviais, `route_model(intent) == "mini"`. O teste falha sozinho quando alguém acrescentar intenção nova sem classificar.

## 9. Checklist de adesão

1. Existe uma única fonte de preço, com dono e data de revisão.
2. A fórmula implementada bate com a da seção 3, incluindo o fator de cache.
3. O roteador é função pura, sem chamada de rede, com testes.
4. Toda intenção tem entrada na tabela de decisão.
5. Intenção desconhecida degrada para o modelo forte e é contada.
6. A chave de cache inclui o escopo do cliente.
7. O guardrail de PII roda antes de qualquer escrita de cache.
8. O ledger grava o modelo efetivamente chamado.
9. Toda execução tem exatamente uma linha no ledger.
10. O hit rate é calculável por SQL em uma linha.
11. O alerta de 80% foi testado com consumo simulado.
12. O bloqueio de 100% não derruba os agentes críticos.
13. O score de qualidade é medido antes e depois de troca de roteamento.
14. Existe rollback de cache e roteamento sem migração.
15. Os números do relatório vêm do ledger, não de planilha.

## 10. Contagem de tokens em streaming e em lote

Duas situações quebram a ingenuidade do `cost()` se não forem tratadas:

**Streaming.** A resposta chega em pedaços e o objeto de uso (entrada e saída) só fecha no último
chunk. Regras: (1) nenhum `cost_usd` é gravado antes do fim da resposta; (2) se a API não devolver
o uso no fim, mede-se com o tokenizador do modelo e a linha recebe `estimated = true`, para que
nenhum relatório confunda estimativa com medição; (3) conexão interrompida grava a linha com o
status interrompido e os tokens parciais conhecidos, nunca zero.

```python
def finalizar_stream(eventos, model):
    """Fecha a contagem ao fim do stream. Retorna (prompt, completion, estimado)."""
    prompt = completion = 0
    estimado = False
    for ev in eventos:
        if ev.tipo == "uso":
            prompt, completion = ev.prompt_tokens, ev.completion_tokens
        elif ev.tipo == "delta":
            completion += len(ev.texto.split())
    if prompt == 0 and completion == 0:
        prompt, completion, estimado = estimar_por_tokenizador(eventos), 0, True
    return prompt, completion, estimado
```

**Lote (batch).** O desconto de lote muda o preço, não a fórmula. A chave é aplicar o multiplicador
no momento da gravação, com a taxa versionada, e nunca guardar "custo cheio" para corrigir depois:
ledger é o registro do que foi pago, não a projeção do que seria pago.

```python
def custo_lote(custo_cheio, taxa_lote=0.50):
    """Aplica o desconto de lote já no ledger. Taxa versionada no repositório."""
    return round(custo_cheio * taxa_lote, 8)
```

| Situação | Multiplicador | Onde é decidido |
| --- | --- | --- |
| Chamada online | 1.00 | fluxo normal |
| Lote dentro do SLA | 0.50 (meta) | flag por fluxo com janela de tolerância |
| Cache hit | 0.00 | camada de cache |
| Retentativa de erro | igual à original | idempotência por `execution_id` |

## 11. Idempotência do ledger

Retry não pode virar cobrança dupla. A linha do ledger é única por execução:

```sql
create unique index ux_llm_usage_execution
  on llm_usage (execution_id);
```

Com a restrição acima, o reprocessamento da fila usa `on conflict do nothing` e o pior caso vira
linha ausente (recuperável) em vez de linha duplicada (que infla a conta e derruba o custo por
tarefa). A reconciliação diária do `COST-MONITORING.md` detecta os dois casos: contagem menor que
execuções indica fila pendente, contagem maior indica bug de gravação.

Regra operacional: toda chamada de LLM na aplicação recebe um `execution_id` gerado **antes** da
chamada, compartilhado pelo retry, pelo trace e pela linha do ledger. Sem ele, três sistemas falam
de três verdades sobre a mesma execução.

## 12. Versionamento da chave de cache

Cache é função do texto **e** do contrato de resposta. Se o prompt de sistema mudar, a resposta
antiga deixa de ser válida, mesmo com a pergunta idêntica. A chave canônica é:

```
cache_key = hash(tenant_id + prompt_version + normalizar(pergunta))
```

- `tenant_id`: isolamento entre clientes, sem exceção.
- `prompt_version`: incremento obrigatório a cada mudança de prompt de sistema ou de ferramenta.
- `normalizar(pergunta)`: minúsculas, sem acento de ruído, espaços colapsados; o que **não** se
  normaliza é número, sigla e valor monetário, porque trocar "R$ 500" por "500" cria resposta errada.

Invalidação: ao publicar `prompt_version` nova, as entradas antigas não são apagadas de imediato,
elas simplesmente deixam de ser consultadas e expiram por TTL. Apagar em massa durante o horário de
pico é um modo de falha desnecessário; expiração silenciosa faz o mesmo trabalho.

## 13. Referências

- Doc oficial: Guia de preços e tokens da API, documentação oficial OpenAI.
- Doc oficial: Guia de prompt caching, documentação oficial Anthropic.
- Curso: FinOps for AI and LLM Cost Optimization, plataforma Udemy.
- Vídeo: Redução de custo de LLM com cache e roteamento, plataforma YouTube, canal Y Combinator.
