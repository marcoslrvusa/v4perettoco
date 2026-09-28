# PDI: Nós Customizados e Expressões Avançadas n8n Enterprise

> **Área:** Automação & Infraestrutura
> **Unidade:** FV Marketing / V4 Company
> **Autor:** Marcos Perettoco
> **Data:** Agosto 2026
> **Status:** **Entregue (desenvolvido) · NÃO publicado: aguardando homologação**
>
> ✅ Entregas concluídas: 1-standards (3 padrões) · 2-workflows (3 workflows validados
> com n8nac) · 3-lib (biblioteca JS/Python reutilizável) · 4-retrofit ·
> 5-monitoring · 6-automation · 7-apresentacao (deck + demo + relatório HTML/DOCX/PDF)

---

## Entregas desta PDI

```
PDI-NOS-CUSTOMIZADOS/
├── 1-standards/          → Padrões de nós Code (JS/Python) e expressões avançadas
├── 2-workflows/          → Workflows n8n prontos para deploy (.workflow.ts)
├── 3-lib/                → Biblioteca reutilizável (payload-lib.js / payload-lib.py)
├── 4-retrofit/           → Plano de retrofit para nós Code e expressões existentes
├── 5-monitoring/         → Queries de performance e diagnóstico de payload
├── 6-automation/         → Scripts de deploy e validação
└── 7-apresentacao/       → Deck e script de demonstração
```

## Problema Resolvido

Nós `Code` em workflows n8n são escritos com frequência como "um nó que faz tudo":
carregam o payload inteiro na memória, percorrem listas com complexidade O(n²),
re-parseiam JSON a cada etapa, repetem a mesma lógica em dezenas de workflows e
usam expressões inline difíceis de manter. Quando o payload é pesado (10k+, 100k+
de itens), isso vira OOM, event loop bloqueado e timeout: exatamente o sintoma da
atividade 1 (ADPLAN: JS timeout 25min) e da atividade 2 (payload pesado sem
checkpoint).

Esta atividade entrega a **camada de transformação**: nós customizados (JS e Python)
e expressões avançadas que processam payloads pesados de forma **streaming,
incremental e reutilizável**: o motor que roda DENTRO de cada etapa dos pipelines
entregues nas atividades 1 e 2.

## Arquitetura Resumida

```
Payload pesado (10k+ itens)
  → [Nó Code JS] Stream + Chunk + Memoização      (normalização incremental)
    → [Nó Code JS] Mapeamento com reduzida cópia   (evita O(n²))
      → [Nó Code Python] Batch enriquecimento      (stdlib: collections/itertools)
        → [Expressões avançadas] $('node') + JSONata + batched references
          → Saída: itens processados + métricas de performance
```

## Frentes de trabalho

1. **Nós Code JS avançados**: streaming com geradores, chunking lazy, memoização,
   redução de cópias de objeto e corte de complexidade O(n²) → O(n).
2. **Nós Code Python no n8n**: enriquecimento e agregação pesados com a biblioteca
   padrão (collections, itertools, functools), sem dependências externas.
3. **Expressões avançadas**: referências entre nós (`$('node').item`), JSONata,
   expressões condicionais e reutilização via `$getWorkflowStaticData`.

## Próximos Passos (homologação)

1. Revisar `1-standards/` (3 padrões): já escritos
2. Ler `3-lib/` (payload-lib.js / payload-lib.py): biblioteca compartilhada
3. Publicar workflows (`bash 6-automation/deploy-custom-nodes.sh`) e ajustar IDs
4. Executar retrofit nos nós Code existentes (`4-retrofit/`)
5. Configurar queries de performance (`5-monitoring/`) e validar com payload simulado

> ⚠️ NENHUM workflow foi enviado ao n8n nesta etapa: publicação apenas após homologação.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Payload 100k itens processado | OOM / timeout | Streaming, < 2 GB pico |
| Complexidade de normalização | O(n²) em vários casos | O(n) padrão |
| Re-parse de JSON por pipeline | Múltiplos por etapa | 1x na entrada |
| Código duplicado entre workflows | Alto (copiar/colar) | Biblioteca única `3-lib/` |
| Expressões de manutenção difícil | Inline, não testáveis | Padronizadas + JSONata |

## Decisoes e tradeoffs

1. Parse 1x na entrada com chunk default de 1000 em vez de JSON.parse por etapa: elimina re-parse dentro de loop. O tradeoff e exigir padronizar a entrada como string ou array no Webhook /nos/js-normalizer.
2. Normalizacao em uma passada O(n) com Set por chave primitiva em vez de .find e indexOf em loop O(n²): payload de 100k itens sai de bilhoes de operacoes para centenas de milhares. O tradeoff e exigir disciplina de copia minima de campos em vez de spread completo por item.
3. Python so com stdlib (collections, itertools, Counter e defaultdict) sem pandas e sem pip: roda no Code node sem dependencia externa. O tradeoff e ter menos sintaxe pronta para dataframe em troca de deploy simples e sem quebra por versao de pacote.
4. Biblioteca unica 3-lib (payload-lib.js e payload-lib.py) como fonte da verdade em vez de copiar e colar entre workflows: funcoes chunk, dedupe, aggregate, normalizeStream, memoizeGlobal e toOutput vivem num lugar so. O tradeoff e que os workflows embutem copias e exigem sincronizar com a lib a cada mudanca.
5. Memoizacao com $getWorkflowStaticData global para valores estaveis em vez de recalcular por execucao: limiar e config calculados 1x e reutilizados. O tradeoff e que o dado cacheado pode ficar defasado e exige invalidacao consciente.

## Impacto no negocio

O sintoma ja visto na atividade 1 com JS timeout de 25 min no ADPLAN e na atividade 2 com payload sem processamento incremental travava importacoes e sincronizacoes ao escalar de 10k para 100k itens. Com streaming, dedupe O(n) e pico abaixo de 2 GB, o mesmo fluxo processa 10 ou 100k itens sem trocar de maquina, com parse unico e codigo unico na 3-lib em vez de copia entre dezenas de workflows. Isso corta tempo de execucao, elimina OOM e event loop bloqueado e reduz custo de manutencao de expressoes inline nao testaveis para padrao com JSONata.

## Referencias de estudo

- Curso: JavaScript Performance, estruturas de dados e complexidade, na Alura.
- Video: JavaScript Event Loop and Memory Explained, no YouTube, canal Fireship.
- Doc: n8n Docs, Code node JavaScript and Python, na plataforma n8n Docs.
- Doc: MDN Docs, Map, Set and Array iteration, na plataforma MDN Web Docs.
