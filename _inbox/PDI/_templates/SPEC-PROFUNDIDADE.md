# SPEC-PROFUNDIDADE: elevação técnica do PDI 2026

Spec obrigatória para toda revisão de conteúdo em `_inbox/PDI/`. Objetivo triplo:

1. **Nível técnico extremo**: invariantes, matemática, modos de falha, SLO, custo, segurança, operação.
2. **Volumetria maior**: dobrar o total de prosa (base atual: 104.145 palavras em `.md`; meta: 250.000+).
3. **Didático para sênior**: quem já trabalha com o tema deve aprender algo novo em cada seção, mesmo assim
   um coordenador de PDI consegue acompanhar. Modelo mental antes de código, exemplo numérico antes de abstração.

---

## 1. Idioma: português do Brasil (obrigatório)

1. **Acentuação correta em toda prosa.** Formas acentuadas sempre que existirem no dicionário:
   decisão, métrica, latência, padrão, referências, negócio, implementação, automação, solução,
   conexão, janela, usuário, código, função, segurança, operação, observabilidade, publicação,
   evolução, gestão, saúde, liderança, análise, informação, produção, configuração, validação,
   injeção, avaliação, previsão, execução, expressão, transação, indexação, partição, replicação,
   consistência, disponibilidade, particionamento, serialização, concorrência, assinatura,
   até, não, após, também, você, será, além, orçamento, nível, técnica, técnicos, técnico,
   médico, físico, único, médio, início, fim, página, vídeo, áudio, ênfase, caráter, caráteres,
   atrás, prá (se usado), crase correta (à API, à fila, à equipe), números por extenso em prosa
   curta (três, cinco, quinze).
2. **PROIBIDO o travessão comum de LLM (U+2014) e o entity HTML correspondente (nome `mdash`) em qualquer arquivo**
   (`.md`, `.html`, `.json`, `.py`, `.ts`, `.sql`, `.sh`, `.js`, `.yml`). Substitua por:
   - dois-pontos para introduzir explicação ou lista: "Consequência: perda de ordem";
   - vírgula para aposto: "o orquestrador, que é stateless, escala horizontalmente";
   - ponto final e nova frase para pausa forte;
   - barra vertical `|` ou ponto para separar título e subtítulo: "Resiliência | Filas e retry".
   Também proibido o travessão duplo. Meia-risca simples só em compostos (`server-side`,
   `feature-flag`) e intervalos numéricos (`10-20`, `15-22`, `R$ 500-1.500`) sem espaços nas pontas.
3. **Ortografia**: gênero e número corretos, crase obrigatória, vírgula antes do "e" final de
   lista com duas frases, aspas HTML escapadas (`&quot;`), nenhum anglicismo cru sem tradução.
   Na primeira ocorrência use o termo em inglês entre aspas e depois a forma em português:
   primeiro "`circuit breaker`", depois disjuntor de circuito.
4. Termos técnicos que não têm tradução consagrada (webhook, idempotência, backlog, runbook,
   SLO, p95, Docker, Supabase) ficam como estão, sem inventar tradução.

## 2. Verdade e números

1. **Nunca placeholder** (`{{...}}`, "lorem", "texto aqui", seção genérica vazia).
2. **Link clicável só se verificado** com WebFetch (status 200) nesta sessão ou se a URL já
   existia no arquivo. Sem link, cite título + plataforma: "Artigo: How to count, PostgreSQL Wiki".
   Nunca invente DOI, autor, data ou número de página.
3. **Número projetado leva `(meta)`**. Número real existente no arquivo (ou no repositório)
   é reaproveitado sem alterar. Nenhum dado novo inventado fora de exemplo rotulado.
4. **Exemplo numérico rotulado**: toda conta nova usada para ensinar deve abrir com
   "**Exemplo numérico:**" e os parâmetros declarados, para ninguém confundir com medição real.
5. Fórmulas em Markdown com `$...$` inline ou bloco de código, sempre com a unidade
   (ms, req/s, R$, tokens, linhas) e uma conta fechada em números redondos.

## 3. Metas de volumetria (verificáveis com `wc -l`)

| Artefato | Mínimo | Meta |
|---|---|---|
| `README.md` da atividade | 200 linhas | 240-300 |
| `README.md` do módulo (card) | 50 linhas | 70-90 |
| Standard principal em `1-standards/` (maior da atividade) | 240 linhas | 300-400 |
| Demais `.md` em `1-standards/` | 100 linhas | 140-200 |
| `7-apresentacao/DECK-PDI.md` | 55 blocos/slide | 70-90 |
| `7-apresentacao/DEMO-SCRIPT.md` | 15 passos | 18-25 |
| `7-apresentacao/ROTEIRO-DOMINIO.md` | 8 perguntas | 10-12 |
| `7-apresentacao/pdi-*.html` | 9 seções numeradas | 10-12 |
| `report.json` | espelho fiel do HTML | idem |

Por atividade, a prosa somada (README + standards + deck + demo + roteiro) deve chegar a
**7.000 palavras no mínimo**. Prioridade quando o tempo apertar: README e standard principal
depois HTML/report.json, depois roteiro, deck e demo.

## 4. Estrutura obrigatória do README da atividade

Manter o padrão SPEC-ENTREGA (metadados, árvore de entregas, problema, arquitetura,
métricas, próximos passos) e acrescentar estas seções, nesta ordem:

1. `## Problema Resolvido` (existente, ampliar com números de partida).
2. `## Modelo mental` (como o sistema realmente se comporta por dentro, 8-15 linhas, sem jargão solto).
3. `## Arquitetura` (diagrama ` ```mermaid ` obrigatório + legenda das decisões de borda).
4. `## Matemática da solução` (fórmulas, capacidade, concorrência, custo; sempre com exemplo numérico rotulado).
5. `## Invariantes` (lista do que nunca pode ser falso, com a violação correspondente).
6. `## Modos de falha` (tabela: sintome | causa raiz | como detecta | como mitiga | tempo de recuperação).
7. `## SLO e orçamento de erro` (SLI, meta, janela de medição, o que fazer quando estoura).
8. `## Operação` (runbook resumido: checagens, mitigação, rollback, quem aciona).
9. `## Decisões e tradeoffs` (existente; ampliar com alternativas descartadas e por quê).
10. `## Impacto no negócio` (existente; manter).
11. `## Esforço e custo` (horas, R$ ou tokens com parâmetros declarados, projeção com `(meta)`).
12. `## Referências` (existente; ampliar, só com link verificado).
13. `## Checklist de domínio` (10-15 itens de verificação que o sênior faria antes de dizer pronto).

## 5. Checklist de senioridade por artefato

**Standard (`1-standards/*.md`)**: escopo e não-escopo; termos; regra canônica com fórmula;
tabela de decisão (se X e Y então Z); exemplo numérico; anti-padrões (o que o sênior reprovaria);
telemetria (quais métricas, cardinalidade, alerta); plano de teste (casos e critério de aceite);
checklist de adesão (10+ itens); referências verificadas.

**DECK-PDI.md**: narrativa slide a slide (título, fala, evidência); >= 3 diagramas `mermaid`;
ao menos 1 slide de matemática com conta fechada; ao menos 1 slide de tradeoff (matriz);
ao menos 1 slide de falha e recuperação; fecho com métricas e próximos passos.

**DEMO-SCRIPT.md**: passos numerados com comando ou clique exato, saída esperada,
critério de falha e o que fazer se der errar (pré-requisito, seed, rollback).

**ROTEIRO-DOMINIO.md**: perguntas adversariais de coordenador (por que não X, quanto custa,
quem decide, e se cair no meio da noite, qual o SLO, como prova que funciona, o que você
deixaria para trás, qual a alternativa mais barata) e uma de negócio (impacto em R$ ou horas).

**HTML do relatório**: seções 1 a 6 do template mais `7. Matemática e capacidade`,
`8. Modos de falha e runbook`, `9. Decisões e alternativas descartadas`,
`10. Segurança e observabilidade` (ou equivalente da trilha, com outro título honesto);
tabelas densas, `div.callout` no fecho, `div.pipeline` no "Como funciona", CSS do template
preservado, caminho de assets `../../../../../` inalterado.

**Código (`2-*`, `3-*`, ...)**: docstrings em português acentuado, tratamento de erro,
modo `--self-test` ou `test_*.py` executável, caso de borda (vazio, nulo, unicode, limite),
medição de tempo ou contagem quando fizer sentido. Identificadores e palavras-chave de
linguagem nunca ganham acento.

## 6. Repertório técnico sugerido por trilha

- **01 Orquestração n8n**: Little's Law ($L = \lambda W$), filas e concorrência, backoff com
  jitter, idempotência por chave, poison pill e DLQ, circuit breaker, pagamento at-least-once
  versus exactly-once, virtual threads versus workers, custo por execução em R$.
- **02 Clean code**: acoplamento e coesão medidos, camadas por dependência, cobertura como
  gate, Código de 600 linhas versus classes < 45 linhas, mocks versus fakes, dívida técnica
  em horas, refatoração em sombra (shadow) e reconciliação.
- **03 Modelagem de dados**: cardinalidade, normalização e quando violar, índices B-tree/BRIN/GIN
  com custo de escrita, `EXPLAIN (ANALYZE, BUFFERS)`, particionamento por tempo, RLS, janelas
  temporais, N+1, paginção por cursor versus offset, transação e isolamento.
- **04 IA/RAG**: chunking com overlap e contagem de tokens, latência p95 por etapa, recall@k,
  reranking, custo por consulta, embeddings de dimensão fixa, avaliação com conjunto-ouro,
  prompt injection em RAG, gravação e despejo de contexto, alucinação e citação obrigatória.
- **05 Distribuídos**: at-least-once e idempotência, outbox, ordenação por partição, poison
  pill, backpressure, sagas versus transação distribuída, repetição e deduplicação, modo de
  falha parcial, RPO e RTO, head of line blocking.
- **06 Governança e segurança**: OWASP Top 10 para LLM, modelo de ameaça, defesa em profundidade,
  PII e anonimização, rotação de segredos, trilha de auditoria imutável, rate limit e custo,
  human in the loop em ação irreversível, prompt injection direta e indireta.
- **07 Gestão técnica**: WIP limitado e filas de espera, Monte Carlo para previsão de entrega,
  escopo versus capacidade, métricas de fluxo (lead time, throughput), postmortem sem culpa,
  RACI, matriz de risco com probabilidade vezes impacto, comunicação a stakeholder.
- **08 Arquitetura documentada**: C4 em 4 níveis, ADR com contexto e consequências,
  diagrama como código (Mermaid e Structurizr), contrato de API e versionamento, catálogo de
  dados e ownership, docs vivos com verificação automática, dívida de documentação.
- **09 Liderança e mentoria**: 1:1 com pauta, feedback estruturado no formato SBI (situação, comportamento, impacto),
  delegação por matriz de maturidade, code review com SLA e checklist, retro com ação rastreável,
  feedback difícil, plano de evolução com metas verificáveis, dívida de conhecimento.
- **10 Saúde e autogestão**: WIP pessoal, ciclos ultradianos, proteção de agenda, custo de
  troca de contexto (reativação em minutos), ergonomia e pausas, ritmo sustentável de estudo,
  energia versus horas, limites negociados com a liderança, sinais de sobrecarga.

## 7. Imutabilidade do repositório

1. **Não apagar nem renomear** arquivo existente (quebra links do portal). Só adicionar.
2. Slugs de HTML/DOCX/PDF e nomes de script permanecem idênticos.
3. Depois de mexer no HTML: atualizar `report.json` (mesmos títulos de seção, mesmos números)
   e os blocos fixos do `gerar-docx.py` (também corrigir capa: `area`, `data`, `status` vindos
   do JSON, sem texto fixo de outra trilha) e regenerar o DOCX com `python3 gerar-docx.py`.
4. PDF não é regenerado pelo autor de conteúdo (a coordenação regenera em lote ao final).
5. Nada fora de `_inbox/PDI/` e do portal pode ser alterado.

## 8. Autoverificação ao final do trabalho

```bash
T=/home/marcos/Desktop/v4perettoco-main/_inbox/PDI/<sua-trilha>
grep -rn $'\u2014' "$T" && echo "TRAVESSAO ENCONTRADO" || echo "ok sem travessao"
grep -rn "mdash" "$T" && echo "ENTITY PROIBIDO" || echo "ok sem entity"
grep -rn "{{" "$T" && echo "PLACEHOLDER" || echo "ok sem placeholder"
find "$T" -name README.md -path "*atividade*" -exec sh -c 'echo "$(wc -l < "$1") $1"' _ {} \;
find "$T" -path "*1-standards/*.md" -exec sh -c 'echo "$(wc -l < "$1") $1"' _ {} \;
find "$T" -name "*.md" -exec cat {} + | wc -w   # palavras da trilha
```

Reporte na resposta final: palavras da trilha antes e depois, linhas de cada artefato
atingido, arquivos novos criados e resultado das três verificações acima.
