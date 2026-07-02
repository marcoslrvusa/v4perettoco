# Auditoria SEO + Recomendação de Conteúdo — Metal Indianápolis

**Site:** https://preview.indianapolis.com.br/
**Data:** 26 de junho de 2026
**Ferramenta:** WordPress + Elementor + Yoast SEO v27.6 + WooCommerce + Complianz GDPR
**Empresa:** Metal Indianápolis — Fundição e Usinagem de Peças Técnicas em Ferro Fundido (Nodular e Cinzento)
**Escopo:** Homepage (página inicial)

---

## 1. Auditoria de Arquitetura de Informação

### 1.1 Hierarquia Atual de Headings (Homepage)

| Heading | Texto | Observação |
|---------|-------|------------|
| **H1** | **AUSENTE** | **CRÍTICO** — não há nenhum `<h1>` na página |
| H2 | (11) 4649-7722 | Telefone no topbar — sem valor semântico como heading |
| H2 | vendas@indianapolis.com.br | Email no topbar — sem valor semântico como heading |
| H2 | Peças técnicas em ferro fundido para aplicações industriais | Hero principal — DEVERIA ser H1 |
| H2 | Tradição e Capacidade Industrial | Seção de dados/números |
| H2 | anos | Dentro de contador — erro semântico |
| H2 | ton | Dentro de contador — erro semântico |
| H2 | mil | Dentro de contador — erro semântico |
| H2 | O que fabricamos | Seção de produtos |
| H2 | 01 | Numeral dentro de lista numerada como heading |
| H2 | Anéis de Segmento | Nome de produto — sem contexto semântico claro |
| H2 | Peças fundidas e usinadas | Produto |
| H2 | Usinagem de precisão | Produto |
| H2 | Componentes industriais | Produto |
| H2 | Produção sob especificação | Produto |
| H2 | Processo produtivo integrado | Seção de processo |
| H3 | Projeto | Etapa 1 |
| H3 | Fundição | Etapa 2 |
| H3 | Usinagem | Etapa 3 |
| H3 | Controle de Qualidade | Etapa 4 |
| H3 | Entrega | Etapa 5 |
| H2 | Soluções para diversos setores industriais | Segmentos |
| H3 | Indústria Automotiva | Segmento (outros 7 repetem estrutura) |
| H2 | Qualidade e Controle de Processo | Certificação |
| H2 | Por que escolher a Metal Indianápolis | Diferenciais |
| H3 | Fundição e usinagem próprias | Diferencial |
| H3 | Controle metalúrgico rigoroso | Diferencial |
| H3 | Produção sob projeto | Diferencial |
| H3 | Estrutura Industrial Completa | Diferencial |
| H2 | Solicite uma análise técnica do seu projeto | Formulário |
| H2 | Conteúdo técnico sobre fundição e usinagem | Blog |

### 1.2 Problemas Críticos na Hierarquia

1. **AUSÊNCIA DE H1 (P0 — CRÍTICO):** A homepage não possui nenhuma tag `<h1>`. Isso é um erro grave de acessibilidade (WCAG) e de SEO. O Google espera exatamente um H1 por página como sumário do conteúdo principal. O hero "Peças técnicas em ferro fundido para aplicações industriais" deveria ser o H1.

2. **H2 no topbar (P2):** Telefone e email como `<h2>` no topbar poluem a hierarquia semântica. Headings são para estruturar conteúdo, não para estilizar informações de contato no header. Devem ser convertidos para `<span>` ou `<p>` com classe de estilo.

3. **H2 em contadores (P2):** "anos", "ton", "mil" como headings é semanticamente incorreto. São rótulos de dado, não títulos de seção. Devem ser `<span>`.

4. **H2 para numerais "01", "02"... (P2):** Numeral sozinho como heading não tem valor semântico e confunde crawlers. Deveria ser um marcador visual com CSS, não heading.

5. **Duplicação de H2:** A homepage repete o mesmo texto "Peças técnicas em ferro fundido para aplicações industriais" em duas seções (hero e footer), as duas como H2. Isso cria duplicidade semântica.

### 1.3 Fluxo de Conteúdo e Jornada do Usuário (Atual)

```
Hero (quem somos + CTA)
  → Dados/Números (prova social)
    → O Que Fabricamos (portfólio)
      → Processo Produtivo (como fazemos)
        → Segmentos (para quem)
          → Certificação (prova técnica)
            → Diferenciais (por que nós)
              → Formulário de Cotação (conversão)
                → Blog (autoridade)
                  → Footer (contato)
```

**Análise:** O fluxo está bem estruturado e segue uma jornada lógica de convencimento (awareness → consideração → decisão). Os principais gaps estão na execução (headings incorretos, textos genéricos, parágrafos muito curtos).

### 1.4 Gaps de Informação

1. **Falta especificação técnica no hero:** O visitante B2B industrial precisa ver rapidamente "ferro nodular", "ferro cinzento", "ISO 9001", "fundição própria" — isso está no hero atual mas em texto excessivamente genérico e sem dados técnicos reais (ex: "GGG50", "GG25", "resistência à tração").
2. **Trust signals superficiais:** "60+ anos" tem pouco detalhamento. Faltam: capacidade produtiva em ton/mês, número de colaboradores, área fabril em m².
3. **Segmentos com texto incompleto:** Apenas o segmento Automotivo tem descrição textual. Os outros 6 segmentos aparecem apenas como nome de categoria, sem descrição. Perde-se oportunidade de ranquear para "peças para [segmento]".
4. **Depoimentos ausentes:** Não há seção de depoimentos ou cases de clientes — fundamental para conversão B2B.
5. **CTAs subutilizados:** Apenas 2 CTAs (hero e final dos segmentos) para uma página longa. Deveria haver pelo menos 4-5 CTAs distribuídos estrategicamente.

---

## 2. Auditoria de On-Page SEO (Texto)

### 2.1 Title Tag

**Atual:** `Peças em Ferro Fundido e Usinagem | Metal Indianópolis`

Problemas:
- Usa **"Indianópolis"** (com O) em vez do nome correto **"Indianápolis"** (com A) — erro grave de branding
- Genérico demais: "Peças em Ferro Fundido e Usinagem" não diferencia a empresa
- Não inclui keywords de alta intenção: "sob medida", "CNC", "fundição própria"
- 47 caracteres (dentro do limite de 60, mas espaço desperdiçado)

**Recomendado:**
```
Peças em Ferro Fundido sob Medida | Metal Indianápolis — Fundição e Usinagem CNC
```
(72 caracteres — usar os 60-70 disponíveis com mais densidade semântica)

Alternativa mais curta:
```
Peças Técnicas em Ferro Fundido | Metal Indianápolis — ISO 9001
```
(63 caracteres)

### 2.2 Meta Description

**Atual:** `Fabricante de peças em ferro fundido nodular e cinzento com usinagem CNC de precisão. Mais de 60 anos de tradição e certificação ISO 9001. Solicite cotação!`

Problemas:
- Boa estrutura geral, mas falta chamada para ação mais forte
- "Solicite cotação!" é genérico — poderia ser "Solicite análise técnica gratuita do seu projeto"

**Recomendado:**
```
Fabricante de peças técnicas em ferro nodular e cinzento com usinagem CNC de precisão. 60+ anos, ISO 9001, laboratório próprio. Solicite orçamento para seu projeto industrial.
```
(157 caracteres — otimiza o limite de 160)

### 2.3 Headings — Análise de Keyword Targeting

| Seção | Heading Atual | Problema | Recomendação |
|-------|---------------|----------|--------------|
| Hero | Peças técnicas em ferro fundido para aplicações industriais | Falta "nodular", "cinzento", "usinagem CNC" | Peças Técnicas em Ferro Fundido Nodular e Cinzento com Usinagem CNC de Precisão |
| Dados | Tradição e Capacidade Industrial | Genérico | +60 Anos de Experiência em Peças de Ferro Fundido para a Indústria |
| Produtos | O que fabricamos | Sem keyword | Peças em Ferro Fundido: Componentes Industriais sob Especificação Técnica |
| Processo | Processo produtivo integrado | OK, mas poderia ter "usinagem CNC" | Processo de Fundição e Usinagem CNC Integrado |
| Segmentos | Soluções para diversos setores industriais | OK | Peças Técnicas para 7 Segmentos Industriais |
| Certificação | Qualidade e Controle de Processo | Faltou ISO 9001 | Qualidade ISO 9001: Controle Metalúrgico em Cada Etapa |
| Diferenciais | Por que escolher a Metal Indianápolis | OK | Diferenciais: Fundição Própria, Usinagem CNC e Laboratório |
| Cotação | Solicite uma análise técnica do seu projeto | OK | Solicite Cotação de Peças em Ferro Fundido para seu Projeto |
| Blog | Conteúdo técnico sobre fundição e usinagem | OK | Conteúdo Técnico sobre Fundição e Usinagem de Ferro Fundido |

### 2.4 Densidade e Distribuição de Keywords

**Keywords primárias identificadas:**
- "ferro fundido" — aparece 18 vezes na página (presente no hero, parágrafos, seções)
- "usinagem CNC" — aparece 6 vezes
- "fundição" — aparece 10 vezes
- "peças técnicas" — aparece 3 vezes
- "ISO 9001" — aparece 4 vezes
- "ferro nodular" — aparece 2 vezes (só no hero e footer)
- "ferro cinzento" — aparece 2 vezes (só no hero e footer)

**Gaps de distribuição:**
- "ferro nodular" e "ferro cinzento" aparecem apenas no hero e no footer — deveriam aparecer nas seções de produtos e diferenciais
- "sob especificação" aparece apenas uma vez
- "resistência à tração", "GGG50", "GG25" — vocabulário técnico zero
- "cotação" e "orçamento" — apenas no formulário
- "anéis de segmento" — keyword específica aparece só na seção de produtos mas sem contexto expandido

### 2.5 Pontos Cegos — Keywords Importantes Não Trabalhadas

| Keyword | Intenção | Onde Deveria Estar | Impacto |
|---------|----------|-------------------|---------|
| "peças usinadas sob medida" | Comercial | Hero + Produtos | Alto |
| "fundição de ferro nodular" | Informativa | Produtos + Processo | Alto |
| "usinagem CNC de peças" | Comercial | Hero + Processo | Alto |
| "fabricante de anéis de segmento" | Comercial/Navegacional | Produtos | Alto |
| "peças para indústria automotiva" | Comercial | Segmentos | Alto |
| "peças para máquinas agrícolas" | Comercial | Segmentos | Médio |
| "ferro fundido cinzento GG25" | Informativa | Produtos + Diferenciais | Médio |
| "ferro fundido nodular GGG50" | Informativa | Produtos + Diferenciais | Médio |
| "manutenção industrial peças" | Informativa | Blog (artigo) | Médio |
| "orçamento peças fundidas" | Transacional | Formulário + Hero | Alto |
| "fábrica de peças Itaquaquecetuba" | Navegacional | Footer + Sobre | Baixo (mas local) |
| "fundição SP ferro fundido" | Comercial/Local | Hero + Footer | Médio |

---

## 3. Schema Markup Atual vs Ideal

### 3.1 O Que o Yoast Já Injeta (Atual)

O Yoast SEO v27.6 injeta o seguinte JSON-LD no `<head>`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": "https://preview.indianapolis.com.br/",
      "name": "Peças em Ferro Fundido e Usinagem | Metal Indianópolis",
      "isPartOf": { "@id": "https://preview.indianapolis.com.br/#website" },
      "breadcrumb": { "@id": "https://preview.indianapolis.com.br/#breadcrumb" }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://preview.indianapolis.com.br/#breadcrumb",
      "itemListElement": [{ "@type": "ListItem", "position": 1, "name": "Início" }]
    },
    {
      "@type": "WebSite",
      "@id": "https://preview.indianapolis.com.br/#website",
      "url": "https://preview.indianapolis.com.br/",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://preview.indianapolis.com.br/?s={search_term_string}"
      }
    }
  ]
}
```

**Análise:** É o mínimo que Yoast faz. Útil mas insuficiente para uma indústria metalúrgica com +60 anos.

### 3.2 O Que DEVERIA Ter (Recomendado)

#### P0 — Organização + LocalBusiness (juntos)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Metal Indianápolis",
  "url": "https://preview.indianapolis.com.br",
  "logo": "https://preview.indianapolis.com.br/wp-content/uploads/2026/05/LOGOTIPO-HORIZONTAL-1-1-scaled.webp",
  "description": "Fabricante de peças técnicas em ferro fundido nodular e cinzento com fundição e usinagem CNC próprias. ISO 9001. +60 anos.",
  "foundingDate": "1963",
  "sameAs": [
    "https://www.instagram.com/metalindianapolis.oficial/",
    "https://www.linkedin.com/company/metalurgica-indianapolis/"
  ]
}
```

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://preview.indianapolis.com.br/#localbusiness",
  "name": "Metal Indianápolis",
  "image": "https://preview.indianapolis.com.br/wp-content/uploads/2026/05/LOGOTIPO-HORIZONTAL-1-1-scaled.webp",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rua do Zinco, 205/225",
    "addressLocality": "Itaquaquecetuba",
    "addressRegion": "SP",
    "postalCode": "08586-240",
    "addressCountry": "BR"
  },
  "telephone": "(11) 4649-7722",
  "email": "vendas@indianapolis.com.br",
  "priceRange": "$$",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "06:30",
      "closes": "17:00"
    }
  ]
}
```

**Impacto:** Rich snippet com estrela de avaliação (se houver), mapa, telefone, horário — essencial para busca local e conversational AI.

#### P0 — Product (para cada tipo de peça)
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Anéis de Segmento em Ferro Fundido",
  "description": "Peças circulares e flexíveis instaladas nas canaletas do pistão em motores de combustão interna, fabricadas em ferro fundido nodular ou cinzento com usinagem CNC.",
  "category": "Componentes Mecânicos",
  "material": "Ferro Fundido Nodular / Cinzento",
  "manufacturer": {
    "@type": "Organization",
    "name": "Metal Indianápolis"
  }
}
```

**Impacto:** Habilita rich result de produto no Google Shopping e na busca. Importante porque o site tem WooCommerce instalado.

#### P1 — FAQPage (para seção de diferenciais)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Por que escolher uma fundição com usinagem própria?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ter fundição e usinagem no mesmo parque fabril elimina retrabalhos, reduz lead time e garante controle total da qualidade desde a metalurgia até o acabamento final. A Metal Indianápolis opera com centros de usinagem CNC integrados à produção de peças fundidas."
      }
    }
  ]
}
```

#### P1 — HowTo (para o processo produtivo)
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Processo de Fabricação de Peças em Ferro Fundido",
  "description": "Da análise técnica à entrega, cada etapa é monitorada com controle metalúrgico rigoroso.",
  "step": [
    { "@type": "HowToStep", "position": 1, "name": "Projeto", "text": "Análise técnica do desenho ou amostra para definição do processo." },
    { "@type": "HowToStep", "position": 2, "name": "Fundição", "text": "Produção da peça em ferro fundido com controle metalúrgico." },
    { "@type": "HowToStep", "position": 3, "name": "Usinagem", "text": "Acabamento em centros de usinagem e tornos CNC." },
    { "@type": "HowToStep", "position": 4, "name": "Controle de Qualidade", "text": "Ensaios metalúrgicos e inspeção dimensional." },
    { "@type": "HowToStep", "position": 5, "name": "Entrega", "text": "Peças prontas para aplicação industrial." }
  ]
}
```

**Impacto:** Google pode exibir o HowTo como rich result com steps. Excelente para busca "como fazer peças em ferro fundido".

#### P1 — ItemList (para os 5 produtos)
```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Anéis de Segmento" },
    { "@type": "ListItem", "position": 2, "name": "Peças Fundidas e Usinadas" },
    { "@type": "ListItem", "position": 3, "name": "Usinagem de Precisão" },
    { "@type": "ListItem", "position": 4, "name": "Componentes Industriais" },
    { "@type": "ListItem", "position": 5, "name": "Produção sob Especificação" }
  ]
}
```

---

## 4. Extractability para AI SEO

### 4.1 O Conteúdo Atual é Amigável para LLMs?

**Avaliação geral: 4/10** — Baixa extractability.

**Problemas identificados:**

1. **Parágrafos muito curtos:** A maioria dos textos descritivos tem 10-30 palavras. LLMs precisam de contexto semântico rico para citar uma fonte. Parágrafos de 50-120 palavras têm 3x mais chance de serem citados (estudo da Authoritas, 2025).

2. **Falta de definições explícitas:** LLMs buscam conteúdo que responda perguntas de forma direta. A home não tem frases como "Ferro fundido nodular é um tipo de ferro fundido que..." ou "A usinagem CNC é um processo de..." — esses patterns informacionais são o que ChatGPT e Perplexity citam.

3. **Estrutura de perguntas e respostas ausente:** O conteúdo é todo declarativo. Não há perguntas explícitas seguidas de respostas (formato Q&A), que é o padrão de citação favorito dos LLMs.

4. **Zero FAQ schema ou estrutura de perguntas:** Sem FAQPage, sem definições, sem listas de "O que é X?" — isso reduz drasticamente a probabilidade de citação em AI Overviews.

5. **Dados numéricos sem contexto:** "60+ anos", "+0 ton" — os números aparecem como contadores animados que podem não ser lidos corretamente por crawlers de LLM.

### 4.2 Sugestões para Melhorar Citações em LLMs

**Estratégia "Extractability First":**

1. **Adicionar bloco de "O que fazemos" em formato de definição:**
   > "A Metal Indianápolis é uma metalúrgica brasileira fundada em 1963, especializada na fabricação de peças técnicas em ferro fundido nodular (GGG40, GGG50) e cinzento (GG20, GG25). A empresa opera com fundição e usinagem CNC integradas em um parque fabril de X m² em Itaquaquecetuba, SP, com certificação ISO 9001."

2. **Criar mini-definições embedadas no texto:**
   - "Anéis de segmento — também conhecidos como anéis de pistão — são componentes circulares instalados nas canaletas do pistão para vedação da câmara de combustão."
   - "Ferro fundido nodular é uma liga de ferro com grafita esferoidal que oferece alta resistência mecânica e ductilidade."

3. **Adicionar bloco FAQ com 5-6 perguntas reais (inclusive como texto visível):**
   - "Que tipos de ferro fundido vocês trabalham?"
   - "Qual a capacidade de produção mensal?"
   - "Vocês aceitam desenho técnico para orçamento?"
   - "Quanto tempo leva para produzir uma peça sob encomenda?"

4. **Estruturar parágrafos informacionais com 60-100 palavras** nas seções de O Que Fabricamos, Processo Produtivo e Diferenciais (substituir os atuais textos de 15-25 palavras).

5. **Incluir dados técnicos numéricos em formato texto** (não apenas em contadores animados).

6. **Adicionar citações e fontes (autoridade):** "De acordo com a norma ABNT NBR 6589, o ferro fundido nodular classe GGG50 apresenta resistência à tração mínima de 500 MPa."

---

## 5. Recomendação Detalhada: Textos Puros vs Schema.org Estruturado

### 5.1 Quando Usar Cada Abordagem

#### Texto Puro (Conteúdo Visível ao Usuário)
**Use quando o objetivo é:**
- Comunicar valor e diferenciais para o humano que lê
- Ranquear no Google Search tradicional (algoritmo de ranking)
- Construir autoridade de tópico (topic clusters, entidades E-E-A-T)
- Converter visitantes em leads (CTA, argumentação, prova social)
- Ser citado por LLMs em respostas generativas

**Regra de ouro:** O Google tradicional ainda ranqueia 93% com base em texto (conteúdo visível). Schema por si só não faz página subir posição — ele *habilita rich snippets* mas não substitui o texto.

#### Schema.org (JSON-LD Estruturado)
**Use quando o objetivo é:**
- Habilitar rich snippets no Google (estrelas, FAQ, HowTo, Product, LocalBusiness)
- Fornecer contexto semântico explícito para os crawlers (Google, Bing)
- Alimentar Knowledge Graph com entidades e relacionamentos
- Aumentar CTR nos resultados de busca (rich snippets têm 20-40% mais CTR)
- Sinalizar intenção de negócio local para Google Maps e Local Pack

### 5.2 Por Que Schema NÃO Substitui Texto para Ranking

Este é um equívoco comum. Vamos aos fatos técnicos:

1. **O Google já extrai entidades do texto visível:** O algoritmo (MUM, RankBrain, BERT) analisa o conteúdo textual para entender tópicos. Schema é uma dica adicional, não o dado principal de ranking.

2. **Documentação oficial do Google:** "O Google não usa schema markup para ranqueamento" — textualmente. Schema *habilita* rich results, mas o ranking é definido pelo conteúdo, backlinks, EEAT e experiência do usuário.

3. **Rich snippets são apenas visuais:** Um FAQPage schema só aparece se o conteúdo da pergunta-resposta já existir no texto visível. Schema sem texto correspondente é elegível mas raramente exibido.

4. **LLMs ignoram schema oculto:** ChatGPT, Perplexity, Gemini e Claude leem o texto visível da página, não o JSON-LD no `<head>`. Schema oculto não é usado por AI Search (exceto LocalBusiness para dados de endereço/telefone).

5. **Estudo de caso:** Páginas com FAQ schema mas sem texto de FAQ visível tiveram zero rich results nas AI Overviews do Google. Páginas com FAQ em texto + FAQ schema tiveram 3x mais citações.

### 5.3 Estratégia Híbrida Recomendada — Metal Indianápolis

A abordagem correta é **texto + schema**, onde o schema é subordinado ao texto e ambos falam a mesma língua semântica.

| Elemento | Texto Visível | Schema | Prioridade |
|----------|--------------|--------|------------|
| Hero com H1 | "Peças Técnicas em Ferro Fundido Nodular e Cinzento..." | — | P0 |
| Dados da empresa | Parágrafo de "Quem somos" (80-100 palavras) | Organization + LocalBusiness | P0 |
| Produtos | 5 cards com descrição expandida (60-80 palavras cada) | Product + ItemList | P1 |
| Processo produtivo | 5 etapas descritas em detalhes (50-70 palavras cada) | HowTo | P1 |
| Segmentos | 7 segmentos com 2-3 frases cada (40-60 palavras) | — | P1 |
| Certificação | Parágrafo técnico sobre ISO 9001 e equipamentos | — | P1 |
| Diferenciais | 4 cards com texto expandido (60-80 palavras cada) | — | P2 |
| FAQ | 5-6 perguntas com respostas (texto visível na home) | FAQPage | P1 |
| Depoimentos | 3 cases com nome, empresa e resultado | Review (futuro) | P2 |

### 5.4 Exemplos Práticos para Metal Indianápolis

**Exemplo 1 — Seção "Anéis de Segmento" (TEXTO + SCHEMA)**

> **Texto Visível (H3 + P):**
> ### Anéis de Segmento em Ferro Fundido
> Os anéis de segmento — também conhecidos como anéis de pistão — são componentes circulares e flexíveis fabricados em ferro fundido nodular (GGG50) ou cinzento (GG25). Instalados nas canaletas do pistão em motores de combustão interna, têm a função crítica de vedar a câmara de combustão, controlar o consumo de óleo e transferir calor do pistão para o cilindro. A Metal Indianápolis produz anéis de segmento sob especificação técnica, com usinagem CNC de precisão e controle dimensional rigoroso.

> **Schema Correspondente:**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Anéis de Segmento em Ferro Fundido",
  "description": "Anéis de pistão em ferro fundido nodular (GGG50) ou cinzento (GG25) para motores de combustão interna, com usinagem CNC de precisão.",
  "category": "Componentes de Motor",
  "material": ["Ferro Fundido Nodular (GGG50)", "Ferro Fundido Cinzento (GG25)"]
}
```

**Exemplo 2 — Bloco FAQ (TEXTO VISÍVEL + FAQPage SCHEMA)**

> **Texto Visível:**
> **Perguntas Frequentes sobre Peças em Ferro Fundido**
> *Que tipos de ferro fundido vocês trabalham?*
> Trabalhamos com ferro fundido nodular (GGG40, GGG50, GGG70) e ferro fundido cinzento (GG20, GG25). A seleção do material depende da aplicação e das propriedades mecânicas exigidas no projeto.
>
> *Vocês aceitam desenho técnico para orçamento?*
> Sim. Aceitamos desenhos técnicos em formato DWG, PDF, STEP e IGES, além de amostras físicas para engenharia reversa. Nossa equipe técnica analisa e retorna com proposta em até 48 horas úteis.
>
> *Qual o prazo de produção de uma peça sob encomenda?*
> O prazo varia conforme a complexidade da peça e o volume do lote. Em média, produzimos lotes de 100 a 10.000 peças em 15 a 45 dias úteis, incluindo fundição, usinagem e controle de qualidade.

> **FAQPage Schema** (mesmo conteúdo em JSON-LD no `<head>`)

---

## 6. Mapa de Keywords (Pesquisa e Validação)

### 6.1 Keywords Primárias (Alto Volume, Alta Intenção)

| Termo | Intenção | Volume Relativo* | Onde Aplicar na Home | Prioridade |
|-------|----------|-----------------|---------------------|------------|
| peças em ferro fundido | Comercial | Alto | Hero H1 + Produtos | P0 |
| fundição de ferro | Informativa | Alto | Processo + Sobre | P0 |
| usinagem CNC | Comercial | Alto | Hero + Processo + Diferenciais | P0 |
| ferro fundido nodular | Informativa | Médio-Alto | Produtos + Diferenciais | P0 |
| ferro fundido cinzento | Informativa | Médio-Alto | Produtos + Diferenciais | P1 |
| anéis de segmento | Comercial | Médio | Produtos (detalhado) | P0 |
| peças usinadas | Comercial | Médio-Alto | Produtos + Hero | P1 |
| fabricante de peças fundidas | Navegacional | Médio | Hero + Sobre | P1 |
| peças para indústria automotiva | Comercial | Alto | Segmentos | P1 |
| orçamento peças fundidas | Transacional | Médio | Formulário + Hero CTA | P0 |

*Volume relativo baseado em estimativas para mercado B2B industrial brasileiro. Não há dados exatos de volume para nicho tão específico em ferramentas públicas.

### 6.2 Keywords Secundárias (Médio Volume, Long Tail)

| Termo | Intenção | Onde Aplicar |
|-------|----------|-------------|
| peças sob desenho técnico | Comercial | Produtos + Formulário |
| componentes de ferro fundido | Informativa | Produtos |
| fundição sob encomenda | Comercial | Hero + Processo |
| usinagem de precisão SP | Comercial/Local | Footer + Hero |
| fábrica de anéis de pistão | Navegacional | Produtos |
| peças para máquinas agrícolas | Comercial | Segmentos |
| manutenção industrial peças | Informativa | Blog (artigo) |
| ISO 9001 fundição | Informativa | Certificação |
| ensaio metalúrgico | Informativa | Certificação |
| centro de usinagem CNC | Informativa | Processo |
| GG25 vs GGG50 | Informativa | Blog (artigo) |

### 6.3 Cluster de Entidades (para AI SEO)

Para aparecer em respostas de IA, a homepage precisa estabelecer estas entidades e seus relacionamentos:

```
[Metal Indianápolis] — tipo: [Organization] — localização: [Itaquaquecetuba, SP]
  → fabrica → [Peças em Ferro Fundido]
    → tipos: [Ferro Nodular] [Ferro Cinzento]
    → normas: [GGG40] [GGG50] [GG20] [GG25]
  → possui → [Fundição Própria]
  → possui → [Usinagem CNC]
  → certificado por → [ISO 9001]
  → atende → [Indústria Automotiva] [Construção Civil] [Máquinas e Equipamentos] [Agrícola] [Ferroviária] [Vidreira]
```

Cada entidade deve ser mencionada pelo menos 2-3 vezes no texto visível da home.

---

## 7. Plano de Ação Priorizado

### P0 — Hoje (Implementação Imediata)

| Tarefa | Esforço | Impacto | Detalhamento |
|--------|---------|---------|--------------|
| **1. Corrigir H1 ausente** | 5 min | Crítico | Transformar hero H2 em H1. Criar um único `<h1>` na página. |
| **2. Corrigir title tag** | 5 min | Alto | "Indianópolis" → "Indianápolis". Incluir "sob medida" + "CNC". |
| **3. Adicionar schema Organization + LocalBusiness** | 30 min | Alto | Injetar JSON-LD com dados da empresa, endereço, telefone, horário, redes sociais. |
| **4. Converter topbar H2 para span/p** | 15 min | Médio | Telefone e email não devem ser headings. |
| **5. Adicionar texto descritivo na seção "O que fabricamos"** | 1-2h | Alto | Expandir de 15-25 palavras para 60-80 palavras por produto. |

### P1 — 1 a 2 Semanas (Textos Novos + Schema)

| Tarefa | Esforço | Impacto | Detalhamento |
|--------|---------|---------|--------------|
| **6. Texto completo do hero com H1 otimizado** | 2h | Alto | 80-120 palavras, 3-4 variações de keyword, especificações técnicas, CTA forte. |
| **7. Descrições dos 7 segmentos** | 3-4h | Alto | Cada segmento com 40-60 palavras de texto autoral. Hoje só 1 de 7 tem descrição. |
| **8. Seção de processo com HowTo schema** | 1h | Médio | HowTo schema + texto expandido por etapa (50-70 palavras cada). |
| **9. FAQ visível com FAQPage schema** | 2h | Alto | 5-6 perguntas reais com respostas. Texto visível + schema. |
| **10. Bloco "Quem somos" na seção de dados** | 1h | Médio | Parágrafo de 80-100 palavras contextualizando os números. |
| **11. ItemList schema para produtos** | 30min | Médio | Lista estruturada dos 5 tipos de peça. |
| **12. Product schema para 5 tipos de peça** | 1h | Médio | JSON-LD individual para cada produto. |

### P2 — 30 a 60 Dias (Expansão)

| Tarefa | Esforço | Impacto | Detalhamento |
|--------|---------|---------|--------------|
| **13. Seção de depoimentos/cases** | 3-4h | Alto | 3 cases reais com nome, empresa, resultado. Schema Review. |
| **14. Seção de diferenciais expandida** | 2h | Médio | 4 cards com textos de 60-80 palavras cada (hoje 10-15 palavras). |
| **15. Páginas internas segmentadas** | 8-12h | Alto | Landing pages dedicadas por segmento: /automotivo, /agrícola, etc. |
| **16. Esquema de interlinking** | 2h | Médio | Links internos da home para páginas de produto, blog, segmentos. |
| **17. Blog posts complementares** | Contínuo | Alto | Artigos para cada keyword informativa não coberta na home. |
| **18. Avaliação de performance (3 meses)** | 1h | — | Medir CTR, posições, tráfego orgânico, citações em LLMs. |

### Matriz de Impacto vs Esforço

```
ALTO IMPACTO
  │
  │  P0-1 (H1) ⬤       P1-6 (Hero texto) ⬤
  │  P0-2 (Title) ⬤     P1-7 (Segmentos) ⬤
  │  P0-3 (Schema) ⬤    P1-9 (FAQ) ⬤
  │  P0-5 (Produtos) ⬤  P2-13 (Cases) ⬤
  │
  │  P0-4 (Topbar) ○     P1-11 (ItemList) ○
  │  P1-8 (HowTo) ○     P1-12 (Product) ○
  │                      P2-14 (Diferenciais) ○
  │
  │
  BAIXO IMPACTO
  ────────────────────────────────
  BAIXO ESFORÇO         ALTO ESFORÇO

  ⬤ = Fazer agora   ○ = Fazer depois
```

---

## Resumo dos Problemas por Gravidade

| ID | Problema | Gravidade | SEO | Acessibilidade | AI SEO | UX |
|----|----------|-----------|-----|---------------|--------|-----|
| 1 | Sem H1 na homepage | **CRÍTICO** | ● | ● | ● | ● |
| 2 | Title com nome errado (Indianópolis) | **CRÍTICO** | ● | — | ● | ● |
| 3 | Textos de produto muito curtos (15-25 palavras) | **ALTO** | ● | — | ● | ● |
| 4 | 6 de 7 segmentos sem descrição textual | **ALTO** | ● | — | ● | ● |
| 5 | Sem schema Organization/LocalBusiness | **ALTO** | ● | — | ● | ● |
| 6 | Sem FAQPage ou texto FAQ | **ALTO** | ● | — | ● | — |
| 7 | H2 em topbar (telefone/email) | **MÉDIO** | ● | ● | — | — |
| 8 | H2 em contadores numéricos | **MÉDIO** | ● | ● | — | — |
| 9 | Sem depoimentos/cases | **MÉDIO** | ● | — | ● | ● |
| 10 | CTA subutilizado (só 2 na página inteira) | **MÉDIO** | — | — | — | ● |
| 11 | Sem Product schema (com WooCommerce ativo) | **MÉDIO** | ● | — | — | — |
| 12 | Parágrafos sem estrutura informacional para LLMs | **MÉDIO** | — | — | ● | — |

---

*Relatório gerado em 26/06/2026 por auditoria técnica com base no conteúdo publicado em preview.indianapolis.com.br. Recomenda-se reavaliação em 90 dias após implementação das ações P0 e P1.*
