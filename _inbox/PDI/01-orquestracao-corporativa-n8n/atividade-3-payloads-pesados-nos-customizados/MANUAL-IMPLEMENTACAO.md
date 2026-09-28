# Manual de Implementação: Nós Customizados e Expressões Avançadas n8n

> **PDI A3 · Área:** Automação & Infraestrutura · **Autor:** Marcos Perettoco
> **Status:** Desenvolvido · Implementar somente **após homologação** da apresentação.

Este manual guia a implantação da atividade 3 na instância n8n da V4 Company, do
zero até o retrofit dos workflows existentes. É o "como fazer" passo a passo de
quem vai executar.

---

## 0. Pré-requisitos

| Item | Detalhe |
|---|---|
| n8n Enterprise acessível | `https://n8n.fvmarketing.com.br` (instância ativa) |
| n8n-as-code configurado | `npx --yes n8nac env status --json` retornando o ambiente `producao` |
| Credencial Supabase | `Command Center Supabase` (`nRJEEi2QwVVKIAHY`): **não** usada nos workflows novos, mas usada no monitoring |
| Permissão de push | Acesso de escrita nos workflows via API n8n (`n8nApi`) |

> A atividade 3 **não depende** de novas tabelas Supabase: os workflows são
> autônomos (só nós `Code`). A tabela `mt_payload_metrics` do `5-monitoring/` é
> opcional e aditiva.

---

## 1. Fase 1: Revisar os padrões (15 min)

Leia e confirme com o time os 3 padrões antes de qualquer código:

1. `1-standards/STANDARD-CODE-JS.md`: regras de nós Code JS (parse 1x, O(n), Set).
2. `1-standards/STANDARD-CODE-PYTHON.md`: regras de nós Code Python (stdlib only).
3. `1-standards/STANDARD-EXPRESSIONS.md`: expressões avançadas + memoização.

**Gate:** se o time não assinar os padrões, nada é publicado.

---

## 2. Fase 2: Carregar a biblioteca 3-lib (10 min)

A biblioteca é a **fonte da verdade** da lógica de transformação.

1. Abra `3-lib/payload-lib.js` e `3-lib/payload-lib.py`.
2. As funções já vêm embutidas nos workflows entregues (cópias).
3. Para usos futuros: copie apenas as funções necessárias para dentro do nó Code.
4. **Regra:** nunca editar a lógica de um nó Code sem atualizar a lib correspondente.

---

## 3. Fase 3: Publicar os workflows (30 min)

Os 3 workflows estão em `2-workflows/` e **já validados** com n8nac
(`Workflow is valid`).

```bash
# 1. Validar mais uma vez (deve acusar ✅ Workflow is valid em todos)
npx --yes n8nac skills validate "2-workflows/[CC] NOS - JS Payload Normalizer.workflow.ts"
npx --yes n8nac skills validate "2-workflows/[CC] NOS - Python Payload Enricher.workflow.ts"
npx --yes n8nac skills validate "2-workflows/[CC] NOS - Expressions & Memo Playground.workflow.ts"

# 2. Publicar (cria/atualiza no n8n)
npx --yes n8nac push "2-workflows/[CC] NOS - JS Payload Normalizer.workflow.ts"
npx --yes n8nac push "2-workflows/[CC] NOS - Python Payload Enricher.workflow.ts"
npx --yes n8nac push "2-workflows/[CC] NOS - Expressions & Memo Playground.workflow.ts"
```

> Alternativa com gate (recomendado na homologação):
> `bash 6-automation/deploy-custom-nodes.sh --dry-run` valida sem publicar.

### 3.1 Ativar webhooks

No n8n UI, ative os nós `Webhook` dos dois workflows de entrada:

- `[CC] NOS - JS Payload Normalizer` → `/nos/js-normalizer`
- `[CC] NOS - Python Payload Enricher` → `/nos/python-enricher`

O `Expressions & Memo Playground` é manual: sem webhook.

---

## 4. Fase 4: Testar com payload simulado (30 min)

### 4.1 Smoke test (10 itens)

```bash
curl -X POST https://n8n.fvmarketing.com.br/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' \
  -d '{"payload":[{"id":1,"name":"Lead A","score":88},{"id":1,"name":"Lead A","score":88},{"id":2,"name":"Lead B","score":45}]}'

# Esperado:
# {"success":true,"processedItems":2,"deduped":1,"itemsPerSecond":...}
```

### 4.2 Teste de escala (100k itens)

```bash
node -e '
  const rows = [];
  for (let i = 0; i < 100000; i++) rows.push({id: i, name: "Lead "+i, score: Math.floor(Math.random()*100)});
  console.log(JSON.stringify({payload: rows}));
' > /tmp/payload-100k.json

curl -X POST https://n8n.fvmarketing.com.br/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' \
  --data @/tmp/payload-100k.json
```

**Critérios de aceite:**

| Critério | Valor |
|---|---|
| `success` | `true` |
| `processedItems` | ~100000 |
| `durationMs` | < 60.000 (meta: segundos) |
| `itemsPerSecond` | registrado (base para baseline) |
| Pico de memória da instância | sem OOM, sem trava |

### 4.3 Teste Python

```bash
curl -X POST https://n8n.fvmarketing.com.br/webhook/nos/python-enricher \
  -H 'Content-Type: application/json' \
  -d '{"payload":[{"id":1,"tipo":"B2B","score":88},{"id":2,"tipo":"B2C","score":45}]}'

# Esperado: byTipo {"B2B":1,"B2C":1}, somaScore {"B2B":88,"B2C":45}
```

### 4.4 Teste de borda (obrigatório antes do push)

Os testes de escala mostram que o caminho feliz aguenta carga. Os testes de borda
mostram que o caminho errado não derruba o pipeline. Rode os quatro:

```bash
# a) Lista vazia
curl -X POST http://localhost:5678/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' -d '{"payload": []}'
# Esperado: success true, processedItems 0

# b) Payload nulo
curl -X POST http://localhost:5678/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' -d '{"payload": null}'
# Esperado: success true, processedItems 0, sem erro 500

# c) JSON malformado
curl -X POST http://localhost:5678/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' -d '{"payload": "{quebrado}"}'
# Esperado: flag de erro de parse visivel, nao lista vazia silenciosa

# d) Itens invalidos misturados com validos
curl -X POST http://localhost:5678/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' \
  -d '{"payload": [{"id":1,"name":"Ok","score":10},{"name":"sem id"},null]}'
# Esperado: processedItems 1, execucao nao falha
```

**Critério de bloqueio:** se qualquer um dos quatro retornar erro 500 ou derrubar
a execução, o push fica suspenso até o filtro barato ser colocado antes da
transformação no nó `Normalize in One Pass`.

### 4.5 Registro da baseline

Antes de sair da fase de teste, grave os números. Sem baseline não há como provar
ganho nem detectar regressão futura:

| Arquivo | O que registrar |
|---|---|
| `/tmp/payload-100k.json` | Gerar uma única vez e reutilizar sempre o mesmo |
| `duration_ms` | Valor da execução de 100k |
| `items_per_second` | Valor da execução de 100k |
| `processed_items` / `deduped` | Conferência de integridade |
| Pico de memória | Conferido no host do n8n durante a execução |

Anote tudo em `5-monitoring/` ou no próprio PR de revisão. A comparação do retrofit
(Fase 4 do `4-retrofit/RETROFIT.md`) usa exatamente esse arquivo de payload como
referência.

---

## 5. Fase 5: Retrofit dos workflows existentes (2 dias)

Siga `4-retrofit/RETROFIT.md`. Resumo:

| Workflow | Correção | Esforço |
|---|---|---|
| ADPLAN | Streaming + dedupe (JS) | 30 min |
| PRO ANÁLISES | Parse 1x + validação | 10 min |
| CC Collector | Dedupe + agregação O(n) | 20 min |
| CC Metrics | Dedupe + agregação O(n) | 20 min |

**Fluxo de retrofit por workflow:**

1. Mapear nós Code que processam listas grandes (`$input.all()`, `map`/`filter`).
2. Aplicar o padrão: parse 1x → Set de dedupe → cópia mínima → sair cedo.
3. Testar com o mesmo payload ANTES e DEPOIS; comparar `durationMs`.
4. Só então publicar o workflow retrofittado.

---

## 6. Fase 6: Monitoramento (30 min)

1. (Opcional) Criar a tabela `mt_payload_metrics` no Supabase
   (`5-monitoring/QUERIES.md` §6) para guardar histórico.
2. Ajustar o nó `Return Metrics` dos workflows para gravar nessa tabela
   (via nó Supabase com a credencial `Command Center Supabase`).
3. Configurar os alertas do `5-monitoring/QUERIES.md` §5:

| Condição | Ação |
|---|---|
| `duration_ms > 60000` | Alertar: payload ou nó regrediu |
| `items_per_second` cai > 50% vs média 24h | Investigar nó Code |
| `dedupe_pct > 50%` | Cliente envia duplicado: orientar filtro |

---

## 7. Rollback

Como cada workflow é independente e **não altera schema existente**, o rollback é
trivial:

```bash
# Desativar os workflows publicados (n8n UI → desativar) ou:
# Republicar a versão anterior via git (git checkout do arquivo anterior + n8nac push)
```

Se o problema for em um workflow retrofittado, reverta **somente aquele workflow**
para a versão anterior no git e re-faça o push: o restante do pipeline permanece.

### 7.1 Sequência exata de rollback por arquivo

```bash
# 1) Identificar o que mudou
git status --short "2-workflows/"

# 2) Reverter APENAS o arquivo culpado
git checkout -- "2-workflows/[CC] NOS - JS Payload Normalizer.workflow.ts"

# 3) Confirmar que o diff sumiu
git diff --stat "2-workflows/"

# 4) Reapublicar somente aquele workflow
npx --yes n8nac push "2-workflows/[CC] NOS - JS Payload Normalizer.workflow.ts"

# 5) Revalidar os demais para garantir que nada foi pego junto
npx --yes n8nac skills validate "2-workflows/[CC] NOS - Python Payload Enricher.workflow.ts"
```

### 7.2 Níveis de rollback

| Nível | Quando | Ação | Tempo típico |
|---|---|---|---|
| Nó | Só um nó regrediu | Reverter o `jsCode` daquele nó e validar | Minutos |
| Workflow | O workflow inteiro está ruim | `git checkout` do arquivo + `push` | Minutos |
| Trilha | Vários workflows quebrados | Desativar os webhooks `/nos/*` no UI e investigar | Imediato |
| Global | Instância instável | Pausar a trilha inteira e acionar coordenação | Conforme impacto |

Regra: o rollback é sempre do menor escopo que resolve. Reverter três workflows
porque um falhou apaga a evidência dos dois que estavam bons e obriga a refazer
validação inteira depois.

### 7.3 Depois do rollback

1. Registrar quando, qual arquivo e qual sintoma motivou a reversão.
2. Repetir a Fase 4 (teste com payload simulado) na versão revertida, para garantir
   que a reversão não deixou o pipeline em estado misto.
3. Só re-tentar a publicação depois de reproduzir o problema localmente
   (`n8n start` em máquina de teste) e aplicar a correção.

---

## 8. Checklist final de homologação

- [ ] 3 padrões revisados e assinados pelo time (`1-standards/`)
- [ ] 3 workflows validados (`n8nac skills validate` → ✅)
- [ ] Smoke test OK (10 itens, dedupe funciona)
- [ ] Escala OK (100k itens, sem OOM, durationMs registrado)
- [ ] Teste Python OK (byTipo/somaScore corretos)
- [ ] Playground: memoização confirmada (cachedAt não muda na 2ª execução)
- [ ] Retrofit de pelo menos 1 workflow existente concluído com ganho medido
- [ ] Alertas de `5-monitoring/` configurados
- [ ] Baseline de `itemsPerSecond` documentado

> ✅ Implementação concluída quando todos os itens acima forem verificados.
> Nenhum item deve ser pulado: cada um protege contra regressão de performance.