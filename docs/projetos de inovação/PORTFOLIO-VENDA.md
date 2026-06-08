# Portfólio de Produtos para Venda — Peretto e Co

> Foco: produtos que a equipe (8-10 pessoas, 2 seniors) consegue operar.
> Setup pelos seniors, operação diária por plenos/juniores.

---

## 0. Premissa: Como ler este documento

Cada produto tem 3 classificações:

```
🔧 Setup senior:  ⬛⬛⬛⬛⬛  (quantas barra, mais complexo)
👶 Operação junior: ⭐⭐⭐⭐⭐  (quantas estrelas, mais fácil)
💰 Ticket mensal:   R$ X.XXX  (preço sugerido)
⏱ Tempo até vender: X semanas (setup + treinamento)
```

Se um produto tem **operação junior baixa**, ele não entra — o time não consegue sustentar.

---

## 1. Produto Estrela: Peretto Monitor (GEO + Concorrência)

**O que vende:** "Sua marca aparece no ChatGPT? E nos concorrentes? A Peretto monitora tudo e entrega um relatório semanal."

**Projetos-base:** OpenCMO + GEO SEO Claude + Drift

```
🔧 Setup senior:  ⬛⬛ (2-3 dias de um senior)
👶 Operação junior: ⭐⭐⭐⭐⭐ (5/5)
💰 Ticket: R$ 1.500-2.500/mês
⏱ Tempo até vender: 2 semanas
```

**Por que funciona com esse time:**
- Senior instala uma vez (Docker + API keys)
- Rotina semanal: segunda de manhã o relatório já está pronto (automático)
- Junior só: abre o PDF → revisa → envia pro cliente por email
- Zero manutenção contínua
- Se quebrar, o Drift manda alerta e o senior resolve em 30min

**O que o cliente recebe:**
```
Relatório Semanal Peretto Monitor
├── GEO Score (0-100): Como a marca aparece em ChatGPT, Gemini, Perplexity, Claude
├── Variação vs semana anterior: ▲ 5 pts
├── Concorrentes: Quem subiu/desceu
├── Recomendações: 3 ações para melhorar (ex: "criar artigo sobre [tema]")
└── Formato: PDF white-label com logo do cliente
```

**Como vender:**
- Diagnóstico gratuito: "Deixa eu ver como sua marca aparece nas IAs"
- Mostra o relatório de 1 semana grátis
- Cliente vê que a concorrência aparece e ele não → venda na hora

**Custo operacional:** ~R$ 100/mês de APIs + 30min/semana do junior
**Margem:** 95%

---

## 2. Peretto Social — Gestão de Redes Sociais com IA

**O que vende:** "Troque Buffer/SocialPilot por uma plataforma white-label com IA integrada que gera posts, agenda e analisa."

**Projetos-base:** BrightBean Studio + SocialFlow

```
🔧 Setup senior:  ⬛⬛⬛ (3-4 dias)
👶 Operação junior: ⭐⭐⭐⭐ (4/5)
💰 Ticket: R$ 2.000-4.000/mês
⏱ Tempo até vender: 3-4 semanas
```

**Por que funciona com esse time:**
- Equipe de social media JÁ SABE fazer agendamento de posts
- BrightBean substitui o Buffer que já usam (mesma lógica, interface similar)
- IA gera o conteúdo (SocialFlow), o junior só revisa e aprova
- Senior só configura os canais de cada cliente uma vez

**O que o junior faz no dia a dia:**
```
1. Abre o BrightBean → vê a fila de posts sugeridos pela IA
2. Revisa o tom de voz (2-3 min por post)
3. Aprova ou ajusta
4. Agenda ou publica
5. No fim do mês: exporta relatório de engajamento
```

**Custo operacional:** ~R$ 360/mês servidor + R$ 100 APIs
**Margem:** 80-85%

**Risco:** BrightBean é AGPL. Como é SaaS (não distribui), ok. Mas se precisar modificar, envolve senior.

---

## 3. Peretto LPs — Landing Pages com IA

**O que vende:** "Landing page pronta em 24h, com copy otimizada por IA e testes A/B — sem pagar agência de criação."

**Projetos-base:** Landing Page Factory + Shippage + VariantLab

```
🔧 Setup senior:  ⬛⬛⬛ (3 dias)
👶 Operação junior: ⭐⭐⭐ (3/5)
💰 Ticket: R$ 1.500-3.000/mês (ou R$ 2.000-5.000 por projeto avulso)
⏱ Tempo até vender: 2 semanas
```

**Por que funciona com esse time:**
- Pipeline: brief → estratégia → copy → visual → construir → revisar → publicar
- Senior cria o template do pipeline no n8n
- Junior roda o pipeline para cada cliente: cola o briefing → IA gera → junior revisa
- Designer da equipe ajusta o visual (se necessário)
- Copywriter não precisa começar do zero

**O que o junior faz:**
```
1. Pega o briefing do cliente (ou usa o que já tem do check-in)
2. Roda o pipeline: "landing page para [cliente] — campanha de [mês]"
3. Recebe a LP gerada (HTML + copy)
4. Revisa: tom de voz, informações, CTA
5. Passa pro designer ajustar cor/logo (30 min)
6. Publica
```

**Vantagem:** Pode vender como serviço recorrente ("LP nova todo mês") avulso ("preciso de uma LP urgente").

**Custo operacional:** ~R$ 50/mês APIs + 2h do junior por LP
**Margem:** 85-90%

---

## 4. Peretto Chat — Atendimento Automático com IA

**O que vende:** "Chatbot para WhatsApp/Instagram que responde seus clientes com IA, treinado no conteúdo da sua marca."

**Projetos-base:** ZernFlow + BrightBean (inbox unificado)

```
🔧 Setup senior:  ⬛⬛ (2 dias)
👶 Operação junior: ⭐⭐⭐⭐ (4/5)
💰 Ticket: R$ 800-2.000/mês
⏱ Tempo até vender: 2 semanas
```

**Por que funciona com esse time:**
- ZernFlow é visual flow builder (drag-and-drop, igual ManyChat)
- Junior monta o fluxo de conversa sem escrever código
- Senior só configura a integração com WhatsApp/Instagram API
- Depois de configurado, junior mantém: ajusta respostas, adiciona novos fluxos

**O que o junior faz:**
```
1. Abre o ZernFlow → arrasta blocos no canvas visual
2. Cria fluxo: "Boas-vindas" → "Capturar lead" → "Direcionar para humano"
3. Alimenta a AI com FAQ do cliente
4. Testa: manda mensagem no WhatsApp, vê se responde certo
5. Ajusta o que precisar
```

**Custo operacional:** ~R$ 100/mês (servidor compartilhado + Supabase)
**Margem:** 90-95%

---

## 5. Peretto Analytics — Dashboard de Marketing com Perguntas em Português

**O que vende:** "Conecte Meta Ads, Google Ads e GA4 num dashboard que você pergunta em português e ele responde."

**Projetos-base:** Full-Funnel AI Analytics + Superset

```
🔧 Setup senior:  ⬛⬛⬛⬛ (4-5 dias)
👶 Operação junior: ⭐⭐⭐ (3/5)
💰 Ticket: R$ 2.000-4.000/mês
⏱ Tempo até vender: 3-4 semanas
```

**Por que funciona com esse time:**
- Senior configura as conexões (Meta Ads, Google Ads, GA4) usando n8n + DuckDB
- Depois de configurado, o junior:
  - Abre o dashboard no Superset (já pronto)
  - Faz perguntas em português: "qual campanha teve melhor ROAS esse mês?"
  - Exporta o relatório em PDF
- Diferencial: não precisa de analista de dados para extrair insight

**Dificuldade:** Superset é complexo. Se o dashboard quebrar, senior precisa arrumar.
**Mitigação:** Fazer templates de dashboard que não mudam. Junior não mexe na configuração, só consome.

**Custo operacional:** ~R$ 360/mês servidor + R$ 50 APIs
**Margem:** 80-85%

---

## 6. Peretto Content — Produção de Conteúdo Acelerada por IA

**O que vende:** "Produção de conteúdo 5x mais rápida com IA — blog, email, redes, tudo num pipeline aprovado."

**Projetos-base:** Marketing Engine + MiCA

```
🔧 Setup senior:  ⬛⬛⬛ (3 dias)
👶 Operação junior: ⭐⭐⭐⭐ (4/5)
💰 Ticket: R$ 2.000-5.000/mês (inclui operação humana)
⏱ Tempo até vender: 3 semanas
```

**Por que funciona com esse time:**
- Pipeline no n8n: cola o briefing → IA gera conteúdo → passa por compliance → aprova
- Junior opera o pipeline, senior revisa outputs no começo
- MiCA gera campanhas multicanal (email + WhatsApp + Instagram) em 5 minutos
- Ideal para clientes menores que precisam de volume mas não têm budget para equipe grande

**O que o junior faz:**
```
1. Cola o briefing do cliente no pipeline do Marketing Engine
2. Roda: gera 5 opções de post para Instagram
3. Escolhe a melhor, ajusta o tom
4. Agenda no Peretto Social (BrightBean)
5. Pronto
```

**Custo operacional:** ~R$ 100-200 APIs + 1h do junior por entrega
**Margem:** 85-90%

---

## 7. Matriz de Decisão para o Time

Produto | Setup senior | Operação junior | Ticket | Esforço comercial | Risco técnico | Prioridade
--------|-------------|----------------|-------|------------------|--------------|-----------
**1. GEO Monitor** | ⬛⬛ (2-3 dias) | ⭐⭐⭐⭐⭐ | R$ 2k | Baixo (diagnóstico grátis vende) | Mínimo | **🥇**
**3. Peretto Chat** | ⬛⬛ (2 dias) | ⭐⭐⭐⭐ | R$ 1,5k | Médio (precisa mostrar valor) | Baixo | **🥇**
**2. Peretto Social** | ⬛⬛⬛ (3-4 dias) | ⭐⭐⭐⭐ | R$ 3k | Baixo (já fazem, só troca ferramenta) | Médio | **🥈**
**6. Peretto Content** | ⬛⬛⬛ (3 dias) | ⭐⭐⭐⭐ | R$ 3,5k | Médio | Baixo | **🥈**
**4. Peretto LPs** | ⬛⬛⬛ (3 dias) | ⭐⭐⭐ | R$ 2k | Baixo (toda empresa precisa) | Baixo | **🥉**
**5. Peretto Analytics** | ⬛⬛⬛⬛ (4-5 dias) | ⭐⭐⭐ | R$ 3k | Alto (precisa explicar) | Médio-Alto | **4º**

---

## 8. Plano de Ação (Primeiros 60 Dias)

### Semana 1-2: Produto 1 (GEO Monitor) + Produto 3 (Chat)

```
Senior 1: Setup do OpenCMO + GEO SEO Claude + Drift (2 dias)
Senior 2: Setup do ZernFlow + integração WhatsApp (2 dias)

Time comercial: Oferecer diagnóstico gratuito de GEO para 5 clientes atuais
  → "Vou ver como sua marca aparece no ChatGPT essa semana e te mando o relatório"
  → Na semana seguinte, entrega o relatório + proposta

Junior 1: Opera o GEO Monitor (relatório semanal)
Junior 2: Monta fluxo de chatbot para o primeiro cliente
```

**Meta:** 2 clientes de GEO Monitor + 1 cliente de Chat até o fim do mês 1.
**Receita esperada:** R$ 4.000-6.500/mês (2 x R$ 2k + 1 x R$ 1,5k)

### Semana 3-4: Produto 2 (Social) + Produto 6 (Content)

```
Senior 1: Setup do BrightBean Studio (3 dias)
Senior 2: Setup do Marketing Engine + MiCA (3 dias)

Time: Onboarding do time de social media no BrightBean
  → "A partir de agora todo conteúdo é criado e aprovado aqui"
  → Clientes atuais já migram → economia de ferramenta (Buffer) já justifica

Junior 1 (social): Opera BrightBean no dia a dia
Junior 2 (conteúdo): Opera Marketing Engine para gerar conteúdo
```

**Meta:** Migrar 3 clientes atuais para BrightBean (reduz custo de ferramenta). 1 novo cliente de Content.
**Receita esperada:** R$ 9.500-18.000/mês (acumulado com mês 1)

### Semana 5-8: Produto 4 (LPs) + Produto 5 (Analytics)

```
Senior 1: Setup da Landing Page Factory + Shippage (3 dias)
Senior 2: Setup do Full-Funnel AI Analytics + Superset (5 dias)

Time: Pipeline de LP testado com 1 cliente existente
  → Landing page que levava 1 semana, agora sai em 24h

Time: Dashboard conectado para os clientes que já pediam "quero ver meus dados"
```

**Meta:** 1 cliente de LP + 1 cliente de Analytics.
**Receita esperada:** R$ 14.000-27.000/mês (acumulado)

---

## 9. Custos e Receita Projetada (Mês 3)

```
Receita:
  GEO Monitor (3 clientes x R$ 2.000)           = R$ 6.000
  Peretto Social (3 clientes x R$ 2.500)        = R$ 7.500
  Peretto Chat (2 clientes x R$ 1.500)          = R$ 3.000
  Peretto Content (2 clientes x R$ 3.000)       = R$ 6.000
  Peretto LPs (1 cliente x R$ 2.500)            = R$ 2.500
  Peretto Analytics (1 cliente x R$ 3.000)      = R$ 3.000
  Total receita recorrente                       = R$ 28.000/mês

Custos:
  Servidores (3 x Hetzner CX42 + 1 compartilhado) = R$ 1.080/mês
  APIs (Gemini + Anthropic + SES)                  = R$ 600/mês
  Domínios (8 x R$ 10)                             = R$ 80/mês
  Total custo                                      = R$ 1.760/mês

Margem bruta:                                       = 93,7%
Margem líquida (considerando 30% do time envolvido)= ~R$ 18.000/mês de lucro incremental
```

---

## 10. Regras de Ouro para Esse Time

1. **Senior constrói, junior opera.** Nenhum produto depende de senior para funcionar no dia a dia. Se precisar, o produto é complexo demais.

2. **Setup documentado em checklist.** Senior cria um passo-a-passo escrito para cada operação. Junior segue o checklist.

3. **Templates antes de customização.** Não customizar para cada cliente antes de validar o template pelo menos 3 vezes.

4. **Produto 1 e 2 são os mais fáceis de vender.** GEO Monitor porque é novidade (aparecer em IA). Social porque substitui custo que o cliente já tem (Buffer/SocialPilot).

5. **Não virar empresa de suporte.** Se um cliente gera mais tickets do que receita, não vale a pena. Produto tem que ser auto-suficiente.

---

> **Documento criado em:** 26/05/2026
> **Considerações:** Time de 8-10 pessoas, 2 seniors, resto pleno/junior.
> **Foco:** Produtos que geram receita E são operáveis pelo time atual.
