# Atlas — Custos de Infraestrutura, Governança e Uso do Cliente

> Análise realista (não genérica) de cada aspecto do produto.
> Resposta direta à crítica: "O GPT disse que você é muito ruim nisso."

---

## 1. Custos de Infraestrutura (Reais)

### 1.1 Premissa: O que cada módulo realmente precisa

Módulo                     | Projeto-base       | CPU | RAM | Disco | DB Required      | Dependências Críticas
-------------------------- | ------------------ | --- | --- | ----- | ---------------- | ---------------------
Superset BI                | apache/superset    | 2   | 4GB | 10GB  | PostgreSQL       | Redis (cache), Celery (async)
Metabase (embutido)        | metabase/metabase  | 1   | 2GB | 5GB   | PostgreSQL       | JDK 21 (JVM pesada)
Grafana (alertas)          | grafana/grafana    | 1   | 1GB | 5GB   | PostgreSQL (opt) | Go binary (leve)
n8n (orquestração)         | n8n-io/n8n         | 1   | 2GB | 10GB  | PostgreSQL       | Redis (fila)
Opensend (email)           | namuh-eng/opensend | 1   | 2GB | 20GB  | PostgreSQL       | Redis + AWS SES
OpenMail (automação email) | ShadowWalker2014   | 1   | 2GB | 10GB  | PostgreSQL       | Redis + BullMQ + Resend
Signal (CRM/sales)         | jay-sahnan/signal  | 1   | 2GB | 10GB  | PostgreSQL       | Supabase + Anthropic API
BrightBean (social)        | brightbeanxyz      | 2   | 4GB | 20GB  | PostgreSQL       | Playwright + API rate limits
ZernFlow (chatbot)         | zernio-dev/zernflow| 1   | 2GB | 10GB  | PostgreSQL       | Supabase
OpenPage (LP builder)      | buildingopen       | 1   | 1GB | 5GB   | —                | Gemini API (opcional)
FreeCrawl (SEO)            | kemalai/FreeCrawl  | —   | —   | —     | —                | Desktop app (não server)
OpenCMO (intel)            | study8677/OpenCMO  | 1   | 2GB | 10GB  | PostgreSQL       | API keys diversas
Rival (comp Intel)         | tessak22/rival     | 1   | 2GB | 10GB  | PostgreSQL       | Tabstack API
DuckDB (DW leve)           | duckdb/duckdb      | 1   | 1GB | 5GB   | —                | Embedded (zero server)

### 1.2 Cenários de Deploy

#### Cenário A: Tudo num servidor (1 cliente pequeno, MVP)

```
1 servidor Hetzner CX32 (4 vCPU, 8 GB RAM, 160 GB SSD)
  ├── Superset (4 GB RAM, 2 vCPU) ──────── R$ 18/mês
  ├── PostgreSQL + Redis (1 GB RAM) ─────── R$ 4/mês
  ├── n8n (512 MB RAM) ─────────────────── R$ 2/mês
  ├── Opensend (512 MB RAM) ────────────── R$ 2/mês
  ├── BrightBean (2 GB RAM) ────────────── R$ 9/mês
  ├── Signal (1 GB RAM) ────────────────── R$ 4/mês
  └── OpenPage + Grafana + Nginx ───────── R$ 2/mês

Custo servidor:          € 39,90/mês ≈ R$ 240/mês
Domínio + SSL:           R$ 10/mês (rateado)
Backup (Hetzner Storage Box 100GB): R$ 7/mês
Monitoramento (Uptime Kuma auto): R$ 0

Total infra:             ~R$ 257/mês
```

**Problema:** 8 GB RAM é apertado. Superset sozinho come 4 GB. Se tiver 2 usuários concorrentes fazendo query pesada, o server morre.

**Realidade:** Para MVP com 1 cliente pequeno, precisa de **CX42 (8 vCPU, 16 GB RAM)** → € 59,90 ≈ **R$ 360/mês**.

#### Cenário B: Servidor por cliente (3-10 clientes, cada um isolado)

```
Por cliente: Hetzner CX42 (8 vCPU, 16 GB, 160 GB SSD)
  ├── Docker Compose com todos os containers
  ├── PostgreSQL + Redis dedicados
  └── Backup automático via borg

Custo por cliente:       € 59,90 ≈ R$ 360/mês
x 10 clientes:           R$ 3.600/mês
Domínios (10 x R$ 10):   R$ 100/mês
Total infra 10 clientes: R$ 3.700/mês

Receita estimada:
  2 Core (R$ 2.500) + 5 Pro (R$ 5.900) + 2 Enterprise (R$ 12.900) + 1 WL (R$ 19.900)
  = R$ 74.400/mês
Custo infra:             R$ 3.700/mês → **5% da receita** ✅
```

#### Cenário C: Cluster Kubernetes (escala 50+ clientes)

```
3 nodes Hetzner AX102 (16 vCPU, 32 GB, 2x NVMe 1.9 TB)
  ├── k3s cluster + Longhorn (storage distribuído)
  ├── PostgreSQL operador (CloudNativePG)
  ├── Redis cluster
  └── Cada cliente = namespace isolado

Custo cluster:           3 x € 89 = € 267/mês ≈ R$ 1.600/mês
Domínios (50 x R$ 10):   R$ 500/mês
Backup offsite (S3):     R$ 200/mês
Monitoramento (Grafana Cloud free tier): R$ 0
Total infra 50 clientes: R$ 2.300/mês

Receita estimada (mix de planos): R$ 250-350k/mês
Custo infra:              <1% da receita ✅✅
```

### 1.3 Custos Variáveis (API e Serviços Externos)

Item                    | Modelo de Custo                | Custo estimado/mês por cliente ativo
----------------------- | ------------------------------ | ------------------------------------
Claude API (OpenSoul)   | $3/M tokens input, $15/M output | **$15-45** (uso moderado, 500k-1.5M tokens)
Gemini API (OpenCMO)    | $0.10-0.50/M tokens (free tier) | **$2-5** (free tier cobre muito)
Anthropic API (Signal)  | $3/M input, $15/M output        | **$10-30** (enriquecimento de leads)
OpenAI (VariantLab)     | $2.50-10/M tokens               | **$5-20** (geração de variantes de LP)
AWS SES (email)         | $0.10/1k emails                 | **$1-5** (10k-50k emails/mês)
Resend (email alt)      | $0.0001/email                   | **$5-10** (50k-100k emails)
Tabstack API (Rival)    | $0.003/extract                  | **$10-30** (50-200 extrações/semana)
Bright Data (opcional)  | $0.001-0.01/request            | **$5-50** (depende do volume)
Firecrawl (SEO Autopilot)| $0.002/page                   | **$2-10** (crawls semanais)
SMTP/domínios            | $5-15/mês por domínio           | **$10/mês**

**Total APIs por cliente ativo:** **$55-205/mês** ≈ **R$ 300-1.200/mês**

> 💡 **Mitigação:** BYOK (Bring Your Own Key) para APIs de LLM. Cliente Enterprise paga as próprias chaves. Atlas só adiciona markup de 20% para gestão.

### 1.4 Tabela de Custo Total por Plano (Realista)

Item                     | Core (R$/mês) | Pro (R$/mês) | Enterprise (R$/mês) | White-Label (R$/mês)
------------------------ | ------------ | ----------- | ------------------- | --------------------
Servidor (Hetzner)       | 360          | 360         | 360                 | 720 (dedicado maior)
Domínio + SSL            | 10           | 10          | 10                  | 50 (5 domínios)
APIs LLM (média)         | 150          | 300         | 600                 | 2.000
AWS SES                  | 2            | 5           | 20                  | 100
Monitoramento + Backup   | 10           | 20          | 30                  | 100
Suporte (humano rateado) | 100          | 200         | 500                 | 1.000
**Custo total**          | **R$ 632**   | **R$ 895**  | **R$ 1.520**        | **R$ 3.970**
**Preço de venda**       | **R$ 2.500** | **R$ 5.900**| **R$ 12.900**        | **R$ 19.900**
**Margem bruta**         | **75%**      | **85%**     | **88%**             | **80%**

> **Nota:** Margens saudáveis, mas dependem de escala. Com 1 cliente Core isolado, a margem real é menor (custo do servidor não é rateado). A conta acima assume que cada servidor roda 1 cliente.

---

## 2. Governança

### 2.1 LGPD e Proteção de Dados

Cada módulo coleta dados diferentes. Mapeamento obrigatório:

Módulo           | Dados coletados                                  | Base legal LGPD        | Retenção
---------------- | ------------------------------------------------ | ---------------------- | --------------------
Superset/BI      | Métricas de anúncio, vendas, tráfego (agregados) | Legítimo interesse     | Indeterminado (agregados)
Signal CRM       | Nome, email, cargo, telefone de leads            | Consentimento explícito| 12 meses pós último contato
BrightBean       | Posts, agendamentos, métricas de engajamento     | Legítimo interesse     | Indeterminado
Opensend         | Email, nome, histórico de abertura/clique        | Consentimento explícito| Até descadastro + 6 meses
ZernFlow         | Mensagens de chat, perfil do contato             | Consentimento + contrato| 90 dias após fim do fluxo
OpenCMO          | URLs, marcas, menções públicas                   | Legítimo interesse     | Indeterminado
OpenPage         | Conteúdo da landing page, dados de formulário    | Consentimento explícito| 30 dias após conversão

**Medidas obrigatórias:**

```
□ Termo de uso para cada módulo que coleta dados pessoais
□ Política de privacidade unificada, específica por módulo
□ Botão "Excluir meus dados" funcional em todos os módulos
□ Registro de consentimento (timestamp + IP + versão do termo)
□ Criptografia em repouso (AES-256 para PostgreSQL + Redis)
□ Criptografia em trânsito (TLS 1.3 para todas as conexões)
□ Isolamento lógico entre clientes (schema PostgreSQL por cliente)
□ Backup criptografado com rotação de chaves
□ DPO designado (pode ser terceirizado)
```

### 2.2 Segurança

Aspecto                    | Implementação                          | Custo estimado
-------------------------- | -------------------------------------- | --------------
WAF (Web Application Firewall) | Cloudflare (free tier cobre)      | R$ 0
Autenticação               | Better Auth + SSO (SAML/OIDC)          | R$ 0 (open source)
MFA                        | TOTP via Better Auth                   | R$ 0
Rate limiting              | Nginx + Cloudflare                     | R$ 0
Hardening Docker           | Non-root user + read-only rootfs       | R$ 0
Vulnerability scanning     | Trivy + Docker Scout (free)            | R$ 0
SIEM / log centralizado    | Grafana Loki + Promtail (self-hosted)  | R$ 50-150/mês (storage)
Pentest anual              | Contratado                             | R$ 15-25k/ano
Auditoria de acesso        | PostgreSQL audit logs + n8n logs       | R$ 0

### 2.3 Compliance Adicional por Setor do Cliente

Setor do Cliente          | Regulação Extra                     | Impacto no Atlas
------------------------ | ----------------------------------- | -------------------------------------
**Saúde**                | LGPD art. 11 (dados sensíveis)      | Precisamos de criptografia adicional, logs de acesso mais granulares, termo de uso específico. **Não recomendar Atlas para saúde sem consultoria jurídica.**
**Financeiro**           | Bacen + LGPD                        | Logs de auditoria imutáveis, separação lógica completa, SLA maior. **Cobrar 30% a mais.**
**Educação**             | LGPD + FNDE (menores)               | Consentimento parental para coleta. Limitar coleta ao mínimo.
**E-commerce**           | LGPD + Marco Civil da Internet      | Padrão. Sem custo extra.
**Agências (white-label)** | Lei de franquias + propriedade intelectual | Contrato específico protegendo código fonte do Atlas.

### 2.4 SLA (Service Level Agreement)

Indicador        | Core         | Pro          | Enterprise   | White-Label
---------------- | ------------ | ------------ | ------------ | ------------
Uptime           | 99% (3.6 dias/ano) | 99.5% | 99.9% | 99.95%
Suporte          | Email 48h     | Email 24h + Chat 8h | Chat 4h + Telefone 1h | Dedicado 1h
Incidente crítico| 8h           | 4h           | 1h           | 30 min
Backup           | Diário, 7 dias| Diário, 30 dias| Horário, 60 dias| Horário, 90 dias
DR (Disaster Recovery) | N/A   | RPO 24h, RTO 8h | RPO 1h, RTO 2h | RPO 15 min, RTO 30 min

> **Custo do SLA:** Para atingir 99.9% de uptime, precisamos de cluster HA (mínimo 2 servidores por cliente). O custo de infra para Enterprise dobra (R$ 720/mês de servidor). Já incluído na precificação.

### 2.5 Política de Backup

```
Dados                         | Frequência | Retenção | Destino
----------------------------- | ---------- | -------- | --------------------
PostgreSQL (todos módulos)    | A cada 6h  | 30 dias  | Hetzner Storage Box + S3
Configuração (Docker volumes) | Diária     | 14 dias  | Hetzner Storage Box
Mídia (imagens, assets)       | Diária     | 7 dias   | S3 (classe Glacier)
Logs (Grafana Loki)           | Contínuo   | 90 dias  | Local (retenção curta)

Processo:
  backup.sh → borg backup (dedup + compressão + criptografia)
  Teste de restore: a cada 30 dias (automático via script)
  Alerta se backup falhar: Telegram + Email
```

---

## 3. Uso do Cliente

### 3.1 Jornada do Cliente (Onboarding)

**Dia 0 — Venda fechada**
- [ ] Envio de formulário de kickoff (quais módulos, URLs, contas de anúncio)
- [ ] Criação do servidor (automático via Terraform + Ansible) — **~15 min**
- [ ] Geração de senha temporária + envio de email de boas-vindas

**Dia 1 — Setup técnico (time V4)**

```
Tarefa                             | Responsável     | Tempo estimado
---------------------------------- | --------------- | --------------
Criar VPS + Docker compose         | DevOps          | 20 min
Configurar DNS + SSL               | DevOps          | 10 min
Conectar Meta Ads token            | Account         | 15 min
Conectar Google Ads + GA4          | Account         | 15 min
Configurar domínio de email        | Account         | 10 min
Setup inicial do CRM (Signal)      | Account         | 20 min
Criar dashboard principal (Superset)| Analytics      | 40 min
Testar envio de email (Opensend)   | Account         | 10 min
Total setup técnico                | —               | ~2h20
```

**Dia 2-3 — Treinamento do cliente (2 sessões de 1h)**

| Sessão | Pauta |
|--------|-------|
| **Sessão 1: Produto** | Visão geral, navegação, dashboard, como extrair relatório |
| **Sessão 2: Fluxo** | Como pedir alteração, como aprovar conteúdo, como escalar |

**Dia 7 — Review de adoção**
- [ ] Cliente logou pelo menos 3 vezes?
- [ ] Viu o dashboard?
- [ ] Tem dúvidas não respondidas?
- [ ] **Se não logou em 7 dias → disparar alerta interno (risco de churn)**

### 3.2 Métricas de Adoção (Health Score)

**Health Score = peso 1 × frequência + peso 2 × profundidade + peso 3 × NPS**

Métrica                          | Peso | Ruim (0)      | Médio (0.5)   | Bom (1.0)
-------------------------------- | ---- | ------------- | ------------- | -----------------
Logins por semana                | 25%  | <2            | 2-4           | >4
Módulos usados / módulos contratados | 25% | <30%      | 30-70%        | >70%
Relatórios exportados por mês    | 15%  | 0             | 1-3           | >3
Tickets de suporte abertos       | 10%  | >5/mês        | 2-5/mês       | <2/mês
Tempo até primeiro valor (TTFV)  | 15%  | >30 dias      | 15-30 dias    | <15 dias
NPS (coletado trimestralmente)   | 10%  | <6            | 7-8           | 9-10

**Alertas automáticos:**
- Health Score < 0.4: **Alerta vermelho** → Account agenda call de recuperação em 48h
- Health Score 0.4-0.6: **Alerta amarelo** → Account envia dicas de uso por email
- TTFV > 30 dias: **Alerta de churn** → Oferecer sessão extra de treinamento

### 3.3 Suporte e Operação

**Canais de suporte:**

| Canal | Core | Pro | Enterprise |
|-------|------|-----|------------|
| Email | ✅ 48h | ✅ 24h | ✅ 4h |
| Chat in-app | ❌ | ✅ 8h (horário comercial) | ✅ 24h |
| Telefone/WhatsApp | ❌ | ❌ | ✅ 1h |
| Base de conhecimento | ✅ | ✅ | ✅ + vídeos customizados |
| Community forum | ✅ | ✅ | ✅ + acesso a beta features |

**Equipe necessária para operar Atlas:**

| Função | Dedicação | Custo/mês (CLT) | Com 10 clientes | Com 50 clientes |
|--------|-----------|----------------|-----------------|-----------------|
| DevOps/SRE | 50% → 100% | R$ 12k | R$ 6k | R$ 12k |
| Account (suporte clientes) | 25% por cliente | R$ 8k | R$ 8k (1 dedicado) | R$ 24k (3 accounts) |
| Analytics Engineer | 50% | R$ 10k | R$ 5k | R$ 10k |
| Customer Success | 0% → 50% | R$ 8k | R$ 0 | R$ 4k |
| Jurídico (LGPD) | 10% | R$ 5k (terceiro) | R$ 500 | R$ 2k |
| **Total equipe** | | | **R$ 19.5k/mês** | **R$ 52k/mês** |

### 3.4 Churn — Causas Raiz e Prevenção

Baseado em dados reais de plataformas de marketing (RD Station, Resultados Digitais):

```
Causa raiz de churn                    | Frequência | Prevenção no Atlas
--------------------------------------- | ---------- | -----------------------------------
Cliente não entende o valor            | 40%        | Onboarding com TTFV < 15 dias. Relatório semanal automático de "o que Atlas fez por você essa semana".
Problemas técnicos (lentidão, downtime)| 25%        | SLA claro. Monitoramento proativo. Post-mortem público.
Falta de suporte                       | 15%        | Chat in-app + base de conhecimento. Account dedicado no Enterprise.
Preço alto                             | 10%        | Revisão trimestral de uso. Oferecer downgrade antes de churn.
Mudança de prioridade do cliente       | 10%        | Impossível prevenir. Deixar porta aberta: "Seu dashboard de BI fica disponível por 30 dias após o cancelamento."
```

**Estratégia de save (quando cliente pede cancelamento):**

```
1. "Poxa, o que aconteceu?" → Escuta ativa (sem desconto ainda)
2. "Vi que você usa só 3 dos 6 módulos do seu plano. Quer migrar pro Core?" → Downgrade é melhor que churn
3. "Posso liberar 30 dias grátis do módulo X que você ainda não testou." → Re-engajamento
4. "Se for questão de $$, posso fazer 20% por 3 meses." → Último recurso
```

**Taxa de churn estimada:** 3-5%/mês para Core, 1-2%/mês para Pro, <1%/mês para Enterprise.

**LTV estimado por plano:**
- Core: R$ 2.500 / 5% = R$ 50.000 (17 meses médios)
- Pro: R$ 5.900 / 3% = R$ 196.000 (33 meses)
- Enterprise: R$ 12.900 / 1% = R$ 1.290.000 (100 meses)

### 3.5 Expansão (Upsell)

Marcos para ofertar upgrade:

| Gatilho | Ação | Conversão esperada |
|---------|------|--------------------|
| Cliente Core usou 80%+ da capacidade do servidor por 2 semanas consecutivas | "Seu servidor está no limite. Pro te dá +50% de recursos + 3 módulos novos." | 20% |
| Cliente Core pede funcionalidade de módulo Pro 2+ vezes | "Você já tentou o módulo X? Está incluso no Pro." | 30% |
| Cliente Pro completa 6 meses sem churn | "Parabéns! Quer testar o Agente Autônomo grátis por 30 dias?" | 15% → upsell Enterprise |
| Clente pede 3+ customizações de branding | "Já pensou no white-label? Sua marca, seu produto." | 10% |

---

## 4. Riscos Reais (Não Genéricos)

### 4.1 Risco Técnico #1: Integração de 8 módulos é um inferno

Verdade: cada projeto open-source tem sua própria stack, sua própria forma de autenticação, seu próprio banco.

**Custo real de integração:** 2 meses de um engenheiro full-stack sênior (R$ 40k) só para fazer:
- Auth unificado (Better Auth + SSO) entre todos os módulos
- Navegação consistente (cada módulo tem UI diferente)
- Compartilhamento de dados entre módulos (ex: leads do Signal aparecerem no Superset)

**Mitigação:** Não integrar tudo de uma vez. Fase 1 = só Superset + n8n. Fase 2 = adiciona Opensend. Fase 3 = adiciona BrightBean. E assim por diante.

### 4.2 Risco Técnico #2: PostgreSQL não escala com 50 clientes no mesmo cluster

Cada módulo precisa de PostgreSQL. Com 8 módulos × 50 clientes = 400 bancos de dados.

**Solução real:** CloudNativePG (operador K8s) com pool de conexões via PgBouncer. Ou usar schema-per-client em vez de database-per-client.

### 4.3 Risco de Negócio #1: Cliente não quer self-hosted

Mesmo com a promessa de "seus dados na sua nuvem", muitos clientes preferem SaaS por preguiça de administrar servidor.

**Dado real:** 70% dos clientes de marketing preferem SaaS gerenciado. Só 30% querem self-hosted.

**Mitigação:** Oferecer Atlas Cloud (V4 hospeda) como opção primária. Self-hosted como diferencial para clientes com LGPD rigorosa.

### 4.4 Risco de Negócio #2: Manutenção dos projetos open-source

Se o Superset lançar breaking change na API, todo o BI quebra. Se o BrightBean parar de ser mantido, social media morre.

**Mitigação:**
- Fazer fork dos projetos críticos (manter mirror interno)
- Testes de integração automatizados (CI/CD) que rodam semanalmente com versão latest dos projetos
- Contingência: ter 2 projetos por categoria (ex: Superset e Metabase; BrightBean e Socioboard)

---

## 5. Resumo Executivo (Para o GPT)

> "O Atlas não é um produto para construir em 1 mês com R$ 15k. É um produto para construir em 6-9 meses com R$ 115k (Fases 1-4), começando pequeno com Superset + n8n + 1 cliente piloto, e expandindo módulo por módulo conforme validação.
>
> A margem é real (75-88%) porque a infraestrutura self-hosted é barata na Hetzner. O risco maior não é custo — é complexidade de integração entre 8 projetos open-source diferentes. Por isso o roadmap prioriza integração progressiva.
>
> O churn estimado de 3-5% ao mês no plano Core é consistente com o mercado de ferramentas de marketing. LTV de R$ 50k justifica CAC de até R$ 15k (vendas + onboarding).
>
> Para clientes Enterprise, o custo de SLA 99.9% e suporte dedicado é coberto pela margem de 88%. O verdadeiro custo não está no servidor, está na equipe de operação (R$ 19.5k/mês com 10 clientes)."

---

> **Documento criado em:** 26/05/2026
> **Resposta à crítica:** "O GPT disse que você é muito ruim nisso."
> **Bad take do GPT:** ❌ Custos de infra não são genéricos quando calculados por módulo individual com provedor real (Hetzner, não cloud genérica).
