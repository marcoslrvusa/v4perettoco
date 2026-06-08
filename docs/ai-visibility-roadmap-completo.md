# Roadmap Completo — AI Visibility

> Da decisão de comprar ao primeiro resultado mensurável: **~60 dias**.
> O menor tempo possível sem ser irresponsável — cada fase tem duração justa, não acelerada.

---

## Fase 1 — Kickoff + Diagnóstico (Semana 1)

**Duração:** 5-7 dias · **Account + Agentes** · **R$ 4.900** (one-time)

### Atividades

| Atividade | Quem | Duração | Entregável |
|---|---|---|---|
| Kickoff meeting | Account + Cliente | 60min | Ata de kickoff alinhada |
| Coleta de 20 queries-alvo | Cliente (formulário) | Na call | Top 20 queries |
| Acesso ao SEMRush | Cliente (ou via V4) | 1 dia | Conta conectada |
| Acesso ao GA4 | Cliente | 1 dia | View configurada |
| Acesso ao robots.txt / site | Cliente | Imediato | Credenciais |

### Formulário de Queries-Alvo

| Tipo | Quantidade |
|---|---|
| "What is [category]?" | 5 |
| "Best [category] for [use case]" | 5 |
| "[Brand] vs [competitor]" | 5 |
| "How to [problem they solve]" | 5 |
| "[Category] pricing" | 5 |
| Dúvidas comuns do cliente | 5 |

### O que acontece

1. Account coleta as 20 queries-alvo, valida acessos (SEMRush, GA4, site) e alinha expectativas
2. **Agentes disparam coleta 100% automática:**
   - SEMRush API → AI Overviews, site audit, benchmark
   - Citation Checker → 100 buscas em 5 plataformas (ChatGPT, Perplexity, Gemini, Claude, Copilot)
   - GA4/GSC Connector → dados de tráfego referido por IAs
3. **@analista-dados processa tudo em 3 minutos:**
   - Auditoria técnica com checklist de 15 pontos
   - Benchmark competitivo com SAIV score
   - Gap analysis priorizado por criticidade
   - Roadmap de implantação em 3 sprints
4. **@revisor valida** cruzando outputs Claude + Gemini
5. **Agentes de entrega geram em paralelo (~10min):**
   - @gerar-pdf → Relatório completo (10 seções, capa + anexos)
   - @gerar-html → Dashboard interativo com gráficos dinâmicos
   - @gerar-ppt → Deck de 15-20 slides para apresentação

### Entregável

Relatório PDF + Dashboard HTML + Deck de apresentação com:
- Status atual: onde o cliente está hoje (provavelmente zero citações)
- Benchmark: onde os concorrentes estão
- Gap analysis: o que precisa mudar
- Roadmap: sprints 1-3 com prazos
- Recomendação: "comece pela implantação"

### Investimento

| Item | Detalhe |
|---|---|
| **Preço** | R$ 4.900 (one-time) |
| **Horas humanas** | ~6h (Account 2h · Analista 3h · Revisor 1h) |
| **Horas agente** | ~45min (coleta + análise + geração) |
| **Automação** | 85% do trabalho (coleta → análise → validação → entrega) |
| **Cliente precisa** | Participar do kickoff, fornecer acessos |

---

## Fase 2 — Sprint 1: Foundation (Semanas 2-3)

**Duração:** 2 semanas · **GT + Copy** · **Incluso na Implantação (R$ 14.900)**

**Objetivo:** Remover todas as barreiras técnicas para que os AI crawlers possam ler, entender e citar o conteúdo.

### Checklist

| # | Tarefa | Responsável | Prazo |
|---|---|---|---|
| 1 | Auditar robots.txt e liberar AI crawlers (GPTBot, PerplexityBot, ClaudeBot, Google-Extended) | GT/Técnico | Dia 8 |
| 2 | Implementar Organization schema | GT/Técnico | Dia 10 |
| 3 | Implementar Article/BlogPosting schema | GT/Técnico | Dia 12 |
| 4 | Implementar FAQPage schema (páginas FAQ) | GT/Técnico | Dia 14 |
| 5 | Implementar HowTo schema (se aplicável) | GT/Técnico | Dia 14 |
| 6 | Implementar Product schema (se aplicável) | GT/Técnico | Dia 14 |
| 7 | Criar `/pricing.md` (pricing legível por agentes de IA) | Copy + GT | Dia 16 |
| 8 | Criar `/llms.txt` (contexto para IAs) | Copy | Dia 16 |
| 9 | Adicionar "last updated" visível em todas as páginas | GT/Técnico | Dia 18 |
| 10 | Adicionar author attribution com credentials | Copy + GT | Dia 20 |
| 11 | Validar tudo com SEMRush Site Audit | @revisor | Dia 22 |

### Entregáveis

- `robots.txt` otimizado (AI crawlers liberados)
- Schema markup implementado nas páginas identificadas
- `pricing.md` no root do domínio
- `llms.txt` no root do domínio
- Relatório de validação técnica

### Investimento

| Item | Detalhe |
|---|---|
| **Horas humanas** | ~30h (GT 20h · Copy 6h · Account 4h) |
| **Cliente já vê** | Site tecnicamente pronto para ser extraído por IAs |
| **Cliente precisa** | Aprovar implementações, liberar acesso ao CMS |

---

## Fase 2 — Sprint 2: Content (Semanas 4-6)

**Duração:** 3 semanas · **Copy + GT** · **Incluso na Implantação (R$ 14.900)**

**Objetivo:** Tornar o conteúdo extraível e citável por IA.

### Priorização de Páginas

Selecionar 10 páginas com base em:
1. Relevância para as queries-alvo
2. Potencial de citação (conteúdo que pode ser definition block, comparison, etc.)
3. Tráfego orgânico atual (dados SEMRush)
4. Gap competitivo (concorrente tem, cliente não tem)

### Content Blocks por Tipo de Query

| Query Pattern | Bloco | Exemplo de Implementação |
|---|---|---|
| "What is X?" | **Definition Block** | Primeiro parágrafo: definição clara de 40-60 palavras. "X é um [categoria] que [funcionalidade principal], diferente de [alternativa] porque [diferencial]." |
| "How to X?" | **Step-by-Step Block** | Lista numerada com 4-7 passos. Cada passo: verbo + resultado esperado. + HowTo schema. |
| "X vs Y" | **Comparison Table** | Tabela com 5-8 critérios lado a lado. Linhas: preço, features, suporte, integrações, etc. |
| "Best X for Y" | **Pros/Cons + Use Case** | Para cada opção: 3 pros + 3 cons + "best for [specific use case]". |
| "X pricing" | **Pricing Block** | Tabela de tiers com: preço, limites, features. + Product schema. |
| "X review" | **Review Block** | Nota geral + breakdown por critério + AggregateRating schema. |
| Perguntas comuns | **FAQ Block** | 5-8 perguntas reais (do suporte, vendas, reviews) + FAQPage schema. |

### Regras de Ouro

1. **Lead com a resposta** — primeira frase de cada seção já responde a pergunta
2. **Blocos autossuficientes** — cada section funciona standalone (IA pode extrair só aquele trecho)
3. **40-60 palavras** para trechos-chave (tamanho ideal de snippet extraction)
4. **Dados originais com fonte** — toda estatística tem link para a fonte original
5. **Datas em tudo** — "Last updated: [data]" em toda página otimizada
6. **Autor com credencial** — nome, cargo, link para LinkedIn/bio
7. **Tom autoritativo** — "De acordo com [fonte]" em vez de afirmações sem apoio
8. **Sem keyword stuffing** — Princeton GEO mostra que keyword stuffing reduz visibilidade em IA em -10%

### Entregáveis

- 10 páginas otimizadas com blocks adequados
- Relatório de validação com extractability score (target: 80%+)
- **Primeiras citações em IA começam a aparecer entre os dias 30-45**

### Investimento

| Item | Detalhe |
|---|---|
| **Horas humanas** | ~60h (Copy 40h · GT 12h · Account 8h) |
| **Cliente precisa** | Revisar e aprovar conteúdo |

---

## Fase 2 — Sprint 3: Presence (Semanas 7-8)

**Duração:** 2 semanas · **Copy + Account** · **Incluso na Implantação (R$ 14.900)**

**Objetivo:** Estabelecer presença do cliente nos locais onde as IAs buscam fontes.

### Third-Party Presence Strategy

| Canal | Ação | Prioridade |
|---|---|---|
| **Wikipedia** | Verificar se página existe. Se existir: atualizar com dados precisos. Se não: avaliar viabilidade (notoriedade exigida). | Alta |
| **Reddit** | Participação autêntica em 3 subreddits do setor (sem spam). Respostas com profundidade técnica. | Alta |
| **G2 / Capterra / TrustRadius** | Perfil atualizado com reviews reais. Responder reviews negativos. | Alta |
| **YouTube** | Criar/vincular conteúdo para "how to" queries (Google AI Overviews cita YouTube frequentemente). | Média |
| **Quora** | Responder perguntas do nicho com profundidade. | Média |
| **Industry publications** | Guest posts em veículos relevantes do setor. | Média |
| **LinkedIn Articles** | Publicação de thought leadership do time do cliente. | Baixa |

### Princípios

1. **Autenticidade > Quantidade** — Uma resposta de qualidade no Reddit vale mais que 10 posts genéricos
2. **Links de volta** — Sempre que possível, referenciar o conteúdo do cliente como fonte
3. **Consistência** — Presença contínua, não campanha única
4. **Monitoramento** — Rastrear menções e citações resultantes (SEMRush Brand Monitoring)

### Entregáveis

- Perfis verificados e atualizados nas plataformas-alvo
- Calendário de presença em terceiros (próximos 3 meses)
- Relatório de citações capturadas pós-implementação

### Investimento

| Item | Detalhe |
|---|---|
| **Horas humanas** | ~30h (Copy 14h · Account 12h · GT 4h) |
| **Cliente precisa** | Aprovar presença em terceiros |

---

## Handoff para Gestão Contínua (Dias 56-60)

| Atividade | Duração | Entregável |
|---|---|---|
| Treinamento do time do cliente | 60min | Time capacitado a manter conteúdo otimizado |
| Entrega de documentação | — | Manual de boas práticas AI SEO (customizado) |
| Transição de métricas | — | Dashboard configurado + baseline estabelecido |
| Alinhamento de expectativas | 30min | O que muda: de projeto para gestão contínua |
| Definição de comunicação | — | Canais: e-mail mensal, call trimestral, emergência WhatsApp |

---

## Fase 3 — Gestão Contínua (Mês 3+)

**Duração:** Mensal recorrente · **Time completo** · **R$ 7.900/mês**

### Ciclo Mensal

```
Semana 1: MONITORAR
  → Puxar dados de citações (manual + SEMRush)
  → Verificar novas queries com AI Overviews
  → Rodar SEMRush Site Audit
  → Alimentar dashboard

Semana 2: RELATAR
  → @analista-dados gera análise do mês
  → @revisor valida
  → @gerar-html gera dashboard interativo
  → Enviar relatório ao cliente (+ call de 15min se necessário)

Semana 3: OTIMIZAR
  → 4 páginas do mês (selecionadas por prioridade)
  → Aplicar content blocks onde faltam
  → Atualizar dados e freshness

Semana 4: EXPANDIR
  → Nova query discovery (SEMRush)
  → Ajustes em third-party presence
  → Preparar recomendações para o próximo mês
```

### Ciclo Trimestral (QBR)

```
Pré-QBR (1 semana antes):
  → @analista-dados puxa dados do trimestre completo
  → Comparativo mês a mês vs trimestre anterior
  → Atualização do benchmark competitivo
  → Draft do deck de QBR

QBR Call (60min):
  → Resultados do trimestre (métricas vs baseline)
  → Novas queries descobertas + cobertura
  → Novos concorrentes entrando no radar
  → Recomendações estratégicas
  → Oportunidades de expansão (add-ons, upsells)

Pós-QBR:
  → @gerar-ppt gera deck final
  → SOW atualizado (se houver mudança de escopo)
  → Próximos passos registrados
```

### O que está incluso

- Monitoramento SEMRush semanal + mensal
- Relatório mensal com dashboard interativo
- Otimização contínua de conteúdo (4 páginas/mês)
- Novas queries + plataformas (mercado muda)
- QBR trimestral com recomendações estratégicas

### Investimento

| Item | Detalhe |
|---|---|
| **Preço** | R$ 7.900/mês (contrato 12 meses · mínimo 6 meses) |
| **Horas humanas** | ~28h/mês (Account 6h · GT 4h · Copy 10h · Analista 6h · Revisor 2h) |
| **Automação** | ~60% da gestão contínua |
| **Resultado esperado** | +40% citações em 6 meses |

---

## Add-ons e Upsells

| Add-on | Preço | Descrição |
|---|---|---|
| **Domínio adicional** | +R$ 2.900/mês | Monitoramento e otimização de um domínio extra do mesmo cliente |
| **Pacote de conteúdo** | +R$ 3.900/mês | +10 páginas/mês de otimização |
| **Competitor Intelligence** | +R$ 1.900/mês | Monitoramento aprofundado de 5 concorrentes específicos |
| **Content Production** | +R$ 2.900/mês | Criação de conteúdo novo otimizado para IA (4 posts/mês) |
| **Technical Deep Dive** | +R$ 4.900 (one-time) | Auditoria técnica completa + implementação de schema avançado |
| **Agente de IA personalizado** | Sob consulta | Treinar um agente customizado no conteúdo do cliente |

---

## Gatilhos de Expansão

| Sinal | Ação | Add-on Sugerido |
|---|---|---|
| Cliente atingiu 70%+ de query coverage | Expandir para mais 20 queries | Pacote de conteúdo + |
| Marca citada 15+ vezes/mês por 3 meses consecutivos | Introduzir competitive intelligence | Competitor Intelligence |
| Cliente tem 2+ marcas/domínios | Expandir para o segundo domínio | Domínio adicional |
| NRR estável há 6+ meses | Propor programa de conteúdo novo | Content Production |
| QBR mostra gap técnico identificado | Oferecer Technical Deep Dive | Technical Deep Dive |

---

## Timeline Resumida

```
W1        W2-3       W4-6         W7-8       M3+
Diagnóstico → Foundation → Content → Presence → Gestão Contínua
  R$4.900  │──────── R$14.900 ────────│       R$7.900/mês
  (6h)     │──────── ~120h ───────────│       ~28h/mês
```

Do kickoff ao primeiro resultado mensurável: **~60 dias**.

---

## Resultados Esperados por Fase

| Métrica | Diagnóstico | Implantação | Gestão (12m) |
|---|---|---|---|
| **Citações em IA** | 0 → diagnóstico | 3-8 citações | 15-40 citações |
| **SAIV Score** | 0% (baseline) | 10-25% | 30-60% |
| **Query Coverage** | 0% (baseline) | 3-5 queries | 12-18 queries |
| **AI Referral Traffic** | — | Primeiros sinais | 5-15% do tráfego orgânico |
| **Extractability Score** | Medido (baseline) | 80%+ | 85-95% |

---

## Curva de NRR por Cliente

```
Mês 0:  Diagnóstico (one-time)            → R$ 4.900
Mês 1:  Implantação (parcela 1/2)         → R$ 7.450
Mês 2:  Implantação (parcela 2/2)         → R$ 7.450
Mês 3+: Gestão Contínua                    → R$ 7.900/mês
Mês 6+: Gestão + Add-on (ex: domínio extra) → R$ 10.800/mês
Mês 12: Reajuste anual                     → R$ 11.340/mês (+5%)
```

**Expansão total:** do diagnóstico (R$ 4.900 one-time) para gestão + add-on (R$ 10.800/mês) = cliente que começa pagando R$ 4.900 vira **R$ 129.600/ano**.

### Metas de NRR

| Indicador | Ano 1 | Ano 2 |
|---|---|---|
| **NRR alvo** | 85% (ano de construção) | 120%+ (operação madura) |
| **Churn rate mensal** | < 5% (target: 3%) | < 3% (target: 2%) |
| **Expansion rate** | 15% com add-on no mês 6 | 40% com add-on |
| **Conversão Diagnóstico → Implantação** | 50% | 60% |
| **Conversão Implantação → Gestão** | 70% | 80% |
| **Vida média do cliente (LTV)** | 14 meses | 24 meses |

---

## Nem tudo é automático

Os agentes automatizam **85% do diagnóstico** e **~60% da gestão contínua**.

O que **NÃO** é automatizado:
- Estratégia de recomendação
- Relacionamento com o cliente
- Decisões de posicionamento
- Conteúdo criativo original

> Onde o ser humano é insubstituível, a gente coloca ser humano. Onde a máquina é mais rápida, a gente coloca máquina. Essa honestidade é o que faz o produto funcionar de verdade.

---

## Modelo de Contrato (Gestão Contínua)

- Mínimo: 6 meses
- Ideal: 12 meses
- Faturamento: Mensal, com reajuste anual pelo IPCA + 5%
- Garantia: Se após 3 meses não houver nenhuma citação em IA, o cliente pode cancelar sem multa

### Renovação Antecipada

| Prazo | Preço Mensal | Economia |
|---|---|---|
| Mensal (sem fidelidade) | R$ 9.900 (preço cheio) | — |
| 6 meses | R$ 7.900/mês | 20% |
| 12 meses | R$ 6.900/mês | 30% |

---

*Documento gerado a partir de `ai-visibility-agent-architecture.html` e `docs/ai-seo-operations-manual.md` — maio 2026.*
