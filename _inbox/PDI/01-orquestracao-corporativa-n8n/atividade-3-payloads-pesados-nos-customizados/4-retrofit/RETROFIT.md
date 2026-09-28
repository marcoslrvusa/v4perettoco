# Retrofit: Nós Code e Expressões Existentes

Plano para adaptar os nós `Code` e expressões já existentes nos workflows SDR IA
e Command Center ao padrão de payload pesado da atividade 3.

## Objetivo

Trocar os nós Code "genéricos" (que carregam tudo, copiam objeto por objeto,
re-parseiam JSON) pelas funções otimizadas da biblioteca `3-lib/`, seguindo os
padrões `1-standards/`.

## Inventário de alvos (sintomas observados na atividade 1)

| Workflow                 | Sintoma                                 | Correção                                            |
| ------------------------ | --------------------------------------- | --------------------------------------------------- |
| ADPLAN                   | JS timeout 25min (event loop bloqueado) | Streaming + chunking (`normalizeStream`), sair cedo |
| PRO ANÁLISES             | `toDateTime` undefined                  | Parse 1x na entrada + validação de campo            |
| Collector / Metrics (CC) | Payloads grandes re-processados         | Dedupe por chave + agregação O(n)                   |
| Diversos                 | Código copiado entre nós                | Extrair para `3-lib/` e referenciar                 |

## Passo a passo (por workflow)

### Fase 1: Mapear nós Code

1. Listar todos os nós `Code` (JS e Python) do workflow.
2. Marcar quais processam listas grandes (`$input.all()`, `map`/`filter` em arrays).
3. Marcar onde há `JSON.parse`/`JSON.stringify` dentro de loops.

### Fase 2: Aplicar padrão

1. **Parse 1x:** mover `JSON.parse` do payload para a primeira etapa.
2. **Dedupe O(n):** trocar `filter`+`find`/`indexOf` por `Set` de chave primitiva.
3. **Cópias mínimas:** reduzir spreads `{...item}` para os campos necessários.
4. **Sair cedo:** filtros baratos antes de transformações caras.
5. **Python:** garantir apenas stdlib; `Counter`/`defaultdict` para agregação.

### Fase 3: Teste com payload simulado

```bash
curl -X POST https://n8n.fvmarketing.com.br/webhook/nos/js-normalizer \
  -H 'Content-Type: application/json' \
  -d '{"payload": [{"id":1,"name":"Lead A","score":88}, {"id":1,"name":"Lead A","score":88}]}'
```

- Checar `processedItems`, `deduped`, `durationMs` e `itemsPerSecond`.
- Repetir com 10k e 100k itens; registrar pico de memória.

### Fase 4: Comparação antes e depois

O retrofit só é considerado concluído quando existe número medido dos dois lados.
O procedimento é o mesmo para qualquer workflow alvo:

1. **Baseline:** rode o payload de teste na versão atual e anote `durationMs`,
   `processedItems` e se houve erro.
2. **Mude uma coisa só:** aplique o padrão (parse 1x, `Set`, cópia mínima, sair cedo),
   nada mais. Retrofit com múltiplas mudanças no mesmo commit não permite atribuir
   a causa do ganho.
3. **Reexecute o mesmo payload:** mesma geração de dados, mesma máquina, mesma hora
   do dia quando possível.
4. **Compare:** registre os dois valores na tabela de esforço, com a razão entre eles.

**Exemplo numérico de registro:** payload de 100.000 itens no ADPLAN, baseline de
48.000 ms, após retrofit 650 ms, razão de 74 vezes. Valores ilustrativos: o número
real entra na linha do workflow apenas após a medição na instância.

Critério de aceite por workflow: nenhum item do checklist do `STANDARD-CODE-JS.md`
aberto, ganho medido registrado e `n8nac skills validate` verde antes do push.

## Estimativa de esforço

| Atividade | Esforço | Detalhe |
|---|---|---|
| JS Normalizer (novo) |: | Entregue nesta PDI |
| Python Enricher (novo) |: | Entregue nesta PDI |
| Retrofit ADPLAN | 30 min | Streaming + dedupe |
| Retrofit PRO ANÁLISES | 10 min | Parse 1x + validação |
| Retrofit CC Collector | 20 min | Dedupe + agregação O(n) |
| Extrair lib `3-lib/` | 20 min | Mover funções para payload-lib |

O somatório dos três retrofits é de 1 h. Some a isso a medição antes e depois
(Fase 4), a revisão de código pelo par e o validate: o total realista por workflow
está entre 40 e 60 min. O retrofit do CC Metrics (20 min, mesmo padrão do Collector)
entra na mesma sessão do Collector, porque a correção é idêntica.

**Ordem de execução recomendada:** começar pelo PRO ANÁLISES (10 min, correção
mais simples), seguir para o CC Collector e o CC Metrics, e deixar o ADPLAN por
último, que é o de maior volume e maior risco. Ganho de confiança primeiro,
workflow crítico depois.

## Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Alterar comportamento de produção | Testar em payload simulado antes do push |
| Python sem stdlib assumido | Checklist do `STANDARD-CODE-PYTHON.md` |
| Duplicação voltar | Regra: lib é fonte da verdade (`3-lib/README.md`) |
| Retrofit sem medição antes/depois | Fase 4 obrigatória: baseline anotada antes de editar |
| Mudança de contrato do nó quebrar o downstream | Conferir consumidores do nó antes de publicar |
| Rollback parcial deixar pipeline inconsistente | Rollback sempre por arquivo, workflow por workflow |
| Métrica nova ausente no workflow retrofittado | Incluir `durationMs` e `itemsPerSecond` na mesma alteração |
| Payload de teste diferente entre as medições | Gerar o arquivo de payload uma vez e reutilizar o mesmo |

## Critério de conclusão do retrofit

O retrofit de um workflow termina quando **todas** as condições abaixo são
verdadeiras para aquele workflow:

1. Nenhum `JSON.parse` permanece fora da etapa de entrada.
2. Nenhuma busca por item (`.find`, `.indexOf`, `includes`) opera sobre lista grande.
3. O dedupe usa `Set` ou `Map` com chave primitiva.
4. As cópias de objeto estão limitadas aos campos consumidos a jusante.
5. O nó emite `durationMs` e `itemsPerSecond`.
6. O payload de 100k foi executado sem OOM e sem erro.
7. A comparação antes e depois está registrada.
8. `npx --yes n8nac skills validate` acusa `Workflow is valid`.
9. A cópia das funções confere com `3-lib/`.
10. O rollback por aquele arquivo foi ensaiado ao menos uma vez.
