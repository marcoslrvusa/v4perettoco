# 🏗️ BRIEFING V0 — PREMIUM CONTRACTORS LLC

## 📋 DADOS DO NEGÓCIO

| Campo                   | Valor                                                                                                                                                                                                                |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Empresa**             | Premium Contractors LLC                                                                                                                                                                                              |
| **Desde**               | 1988 — **37+ anos de estrada**                                                                                                                                                                                       |
| **Fundador/Presidente** | Diniz Teixeira                                                                                                                                                                                                       |
| **Sede**                | 107 Vesey St, Newark, NJ 07105                                                                                                                                                                                       |
| **Telefone**            | 973-558-5226 / 973-204-2310                                                                                                                                                                                          |
| **Email**               | office@premiumcontractorllc.com                                                                                                                                                                                      |
| **Área de atuação**     | New Jersey + New York                                                                                                                                                                                                |
| **Especialidade**       | Construção comercial — hotéis, restaurantes, multifamily, aeroportos                                                                                                                                                 |
| **Clientes âncora**     | Marriott, Hilton, Wendy's, The Briad Group                                                                                                                                                                           |
| **Serviços**            | Metal framing, wood framing, drywall, painting, wallcovering, acoustical ceiling, insulation, finish trimming, doors, kitchen cabinets, ceramic/LVT/carpet tile, metal ceiling, asphalt repairs, stripping, cleaning |
| **Equipe**              | Diniz Teixeira (President), Emerson Rodrigues (Finance), Brenda Souza (Office), Robert Firme (PM), Italo Bacelar (Project Assistant)                                                                                 |

## 🎯 OBJETIVO

Reconstruir o site do zero saindo do Wix (lento, sem SEO, sem personalidade) para um site **Next.js 14+ (App Router) + Tailwind CSS + Framer Motion** que transmita:

- **Autoridade absoluta** — "somos os caras da construção comercial em NJ/NY desde 1988"
- **Solidez** — construção pesada, concreto, aço, pegada industrial premium
- **Confiança** — portfolios reais, clientes reais, projetos reais
- **Movimento** — o site precisa sentir que "constrói", não que "parou no tempo"

Site atual que queremos refazer: https://www.premiumcontractorllc.com/
Pegue o logo daqui: https://static.wixstatic.com/media/9c2b39_3c9a0628131c4a93806993a9afa33c37~mv2.png/v1/fill/w_154,h_180,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/predio%20colorido.png

## 🎨 DIREÇÃO DE DESIGN (UI/UX)

### Paleta de Cores

```
--primary: #1a1a2e        (azul-marinho profundo, quase preto)
--primary-light: #16213e   (variação escura)
--accent: #e94560          (vermelho fogo / laranja queimado — CTA, energia)
--accent-hover: #d63850
--surface: #0f3460         (azul médio, cartões)
--text: #f5f5f5            (quase branco)
--text-secondary: #a0a0b0
--bg-dark: #0a0a0f         (fundo hero)
--bg-card: #111122         (fundo cartões)
```

### Tipografia

- **Headings:** Inter Tight (pesos 700, 800, 900) — impacto, condensado, construção
- **Body:** Inter (pesos 300, 400, 500) — legibilidade máxima
- **Monospace (stats/números):** JetBrains Mono — pra dar peso de dado/engenharia

### Sensação Visual

- **Background:** Fundos escuros com textura sutil de concreto/aço (noise texture overlay)
- **Gradientes:** Mesh gradients escuros com tons de azul profundo → azul petróleo
- **Iluminação:** Efeitos de "glow" sutil nos cantos, como luz de canteiro de obras
- **Linhas/Grid:** Linhas de construção (grid patterns) como elemento decorativo
- **Ícones:** Line icons grossos, estilo engenharia (não icons genéricos)
- **Fotos:** SEMPRE reais do portfólio. Sem stock photo. Tratamento com leve contraste/quente

### Animações (Framer Motion)

- `scroll-triggered fade-up` em cada section
- `stagger children` em grids de portfólio
- `parallax sutil` em imagens hero
- `counter animation` em números (anos, projetos, clientes)
- `reveal text` com caractere por caractere em taglines
- `hover scale + shadow` em cards de projeto
- Presença o tempo todo, mas SEMPRE performática (respeitando `prefers-reduced-motion`)

## 📐 ARQUITETURA DE INFORMAÇÃO

```
/                          → Home (hero + stats + featured projects + clients + CTA)
/about                     → História, valores, equipe, visão
/services                  → Overview de serviços
/services/metal-framing    → Página individual por serviço (SEO)
/services/drywall
/services/painting
/services/wood-framing
... (cada serviço)
/projects                  → Portfolio grid filtrável
/projects/the-edge-multifamily
/projects/signature-flight-support
/projects/...              → Página de case study individual
/industries/hospitality    → Hotéis, restaurantes
/industries/multifamily    → Residencial multifamily
/industries/commercial     → Escritórios, comerciais
/team                      → Conheça o time
/contact                   → Contato + form + mapa
/safety                    → Cultura de segurança, EMR, OSHA
/careers                   → Trabalhe conosco
/blog                      → Conteúdo SEO
/faq                       → FAQ com schema
/llms.txt                  → IA SEO (novo!)
```

## 🔥 PÁGINA HOME — ESPECIFICAÇÃO DETALHADA

### Section 1 — Hero (acima da dobra)

```
[Navbar transparente → sólida no scroll]
  Logo SVG (alta qualidade) | Serviços | Projetos | Sobre | Contato | [GET A QUOTE]

[Hero full-viewport com background parallax]
  Badge: "EST. 1988" ou "NEWARK, NJ"
  H1: "Commercial Construction. Built Different." (ou "Precision. Power. Premium.")
  Subtítulo: "Serving New Jersey & New York since 1988. Specializing in hotel, restaurant, and commercial construction."

  CTA primário: "Request a Quote →" (accent color)
  CTA secundário: "View Our Portfolio"

  [Stats bar flutuando ou abaixo]
    +250 Projects Completed | 37+ Years | 50+ Client Partners | NJ + NY
```

### Section 2 — Trust Bar (clientes)

Clientes reais em grid de logos: Marriott, Hilton, Wendy's, The Briad Group, mais 10+.

### Section 3 — Featured Projects (com caso)

3 projetos em destaque com foto grande + escopo + link "View Case Study →"

### Section 4 — Services Overview

Grid 3x2 ou 4x2 com icons + nomes + short description + link

### Section 5 — Depoimento em destaque

```
"Premium Contractors is an incredible business partner... Their attention to customer service, detail, and understanding project timelines is of highest importance."
— Jason Honigfeld, COO/CFO, The Briad Group
```

(Full-width, tipografia grande, fundo escuro)

### Section 6 — CTA Final

"Ready to discuss your next project?" + form curto (4 campos)

### Footer

Endereço, telefones, email, LinkedIn, links rápidos, direitos.

## 📱 CRO (CONVERSION RATE OPTIMIZATION)

1. **Sticky CTA bar mobile** — "Call Now" e "Get Quote" SEMPRE visíveis
2. **Form de 4 campos:** Nome, Telefone, Email, Tipo de Projeto (dropdown) + Submit
3. **CTAs em cada service page** com contexto ("Get a Quote for Your Metal Framing Project")
4. **Trust signals** em cada página: selo "Since 1988", logos de cliente, depoimentos
5. **Prova social acima do form** — 1 depoimento curto + aggregate rating stars
6. **WhatsApp/live chat** flutuante (se aplicável)
7. **Page speed <2s LCP** — essencial em construção civil (lentidão = desconfiança)
8. **Click-to-call** no header em mobile
9. **Lead magnet** "Commercial Construction Capability Statement" (PDF download) em troca de email
10. **Micro-conversões** em cada scroll: badges contadores animados

## 🚀 SEO + SCHEMA MARKUP AVANÇADO

### Schema Estratégico (JSON-LD em todas as páginas)

**Home:**

```json
{
  "@context": "https://schema.org",
  "@type": "GeneralContractor",
  "name": "Premium Contractors LLC",
  "description": "Commercial construction company serving New Jersey and New York since 1988. Specializing in hotel, restaurant, and commercial construction.",
  "url": "https://www.premiumcontractorllc.com",
  "telephone": "+1-973-558-5226",
  "email": "office@premiumcontractorllc.com",
  "foundingDate": "1988",
  "founder": {
    "@type": "Person",
    "name": "Diniz Teixeira"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "107 Vesey St",
    "addressLocality": "Newark",
    "addressRegion": "NJ",
    "postalCode": "07105",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.7271,
    "longitude": -74.1706
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "07:00",
      "closes": "17:00"
    }
  ],
  "areaServed": [
    {"@type": "State", "name": "New Jersey"},
    {"@type": "State", "name": "New York"}
  ],
  "priceRange": "$$$",
  "image": "https://www.premiumcontractorllc.com/og-image.jpg",
  "sameAs": [
    "https://www.linkedin.com/company/premium-contractorsllc"
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Construction Services",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Metal Framing"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Drywall Installation"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Commercial Painting"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Acoustical Ceilings"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Ceramic Tile Installation"}}
    ]
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "50"
  }
}
```

**Service Pages (exemplo: /services/metal-framing):**

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Metal Framing",
  "provider": {
    "@type": "GeneralContractor",
    "name": "Premium Contractors LLC",
    "url": "https://www.premiumcontractorllc.com"
  },
  "areaServed": [
    {"@type": "State", "name": "New Jersey"},
    {"@type": "State", "name": "New York"}
  ],
  "description": "Professional metal framing services for commercial construction projects including hotels, restaurants, and multifamily buildings.",
  "offers": {
    "@type": "Offer",
    "priceSpecification": {
      "@type": "PriceSpecification",
      "priceCurrency": "USD"
    }
  }
}
```

**Review Schema (depoimentos):**

```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "GeneralContractor",
    "name": "Premium Contractors LLC"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "5"
  },
  "author": {
    "@type": "Person",
    "name": "Jason Honigfeld"
  },
  "publisher": {
    "@type": "Organization",
    "name": "The Briad Group"
  },
  "reviewBody": "Premium Contractors is an incredible business partner... Highly recommend."
}
```

**FAQ Schema (/faq):**

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What areas does Premium Contractors serve?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We serve commercial clients throughout New Jersey and New York from our headquarters in Newark, NJ."
      }
    },
    {
      "@type": "Question",
      "name": "What types of commercial projects do you handle?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We specialize in hotel construction, restaurant build-outs, multifamily residential, and general commercial spaces."
      }
    },
    {
      "@type": "Question",
      "name": "How long has Premium Contractors been in business?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We've been delivering quality construction since 1988 — over 37 years of experience."
      }
    },
    {
      "@type": "Question",
      "name": "Do you work with major hotel brands?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. We are trusted partners of Marriott, Hilton, and other premier hospitality brands."
      }
    }
  ]
}
```

**BreadcrumbList Schema (todas as páginas internas):**

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.premiumcontractorllc.com"},
    {"@type": "ListItem", "position": 2, "name": "Services", "item": "https://www.premiumcontractorllc.com/services"},
    {"@type": "ListItem", "position": 3, "name": "Metal Framing", "item": "https://www.premiumcontractorllc.com/services/metal-framing"}
  ]
}
```

**LocalBusiness + Organization + WebSite**: Todas combinadas em uma página.

**SiteNavigationElement schema**: Para navegação principal.

**Person schema**: Para cada membro da equipe na /team.

### Otimizações Técnicas SEO

- Meta titles: `Metal Framing Services in NJ | Premium Contractors LLC` (formato: `{Serviço} in {Área} | {Empresa}`)
- Meta descriptions com CTA embutido
- Open Graph / Twitter Cards com imagens 1200x630
- Canonical tags em todas as páginas
- XML Sitemap dinâmico
- Robots.txt otimizado
- Core Web Vitals (LCP < 2.5s, FID < 100ms, CLS < 0.1)
- Imagens em WebP/AVIF com lazy loading + blur placeholder
- Structured data testing no Google Rich Results Test
- Hreflang se aplicável

## 🤖 LLMs.txt (AI SEO — NOVO)

Criar `/llms.txt` e `/llms-full.txt` para ser encontrado por LLMs.

```
# Premium Contractors LLC

> Commercial construction company serving New Jersey and New York since 1988.

## Company
- Name: Premium Contractors LLC
- Founded: 1988
- Headquarters: 107 Vesey St, Newark, NJ 07105
- Phone: 973-558-5226
- Email: office@premiumcontractorllc.com
- Service Area: New Jersey, New York
- President: Diniz Teixeira

## Services
- Metal Framing: Light gauge steel framing for commercial buildings
- Drywall & Finishing: Taping, spackling, and smooth finishes
- Commercial Painting: Interior and exterior painting
- Acoustical Ceilings: Suspended ceiling systems
- Wood Framing: Structural wood framing
- Insulation: Thermal and acoustic insulation
- Wallcovering: Commercial wallpaper installation
- Ceramic/LVT/Carpet Tile: Flooring installation
- Kitchen Cabinets: Commercial cabinetry installation
- Doors: Commercial door installation
- Finish Trimming: Baseboards, crown molding, casing
- Metal Ceilings: Architectural metal ceiling systems
- Asphalt Repairs: Parking lot and pavement repair
- Stripping Services: Paint and wallcovering removal
- Cleaning: Post-construction cleaning

## Key Clients
- Marriott Hotels
- Hilton Hotels
- Wendy's
- The Briad Group

## Notable Projects
- The Edge Multi-Family Residential (Elizabeth, NJ) — 50 rooms, metal framing
- Signature Flight Support (Atlantic City Airport, NJ) — painting, acoustical ceiling, framing

## Links
- Website: https://www.premiumcontractorllc.com
- LinkedIn: https://www.linkedin.com/company/premium-contractorsllc
- Cleaning Services: https://insights.premiumcleaningnj.com/
```

## ⚡ STACK TÉCNICA (V0)

| Requisito | Especificação |
|---|---|
| **Framework** | Next.js 15+ (App Router) — output `export` ou Vercel |
| **Estilo** | Tailwind CSS v4 + class-variance-authority + tailwind-merge |
| **Animações** | Framer Motion (otimizado com `useInView`, `lazy-motion`) |
| **Fonte** | Inter + Inter Tight via next/font/google |
| **Ícones** | Lucide React + Heroicons outline |
| **Form** | React Hook Form + Zod |
| **Imagens** | next/image (WebP, lazy, blur placeholder) |
| **SEO** | next-seo ou metadata API nativa do Next.js App Router |
| **Schema** | JSON-LD inline no layout (script structured data) |
| **Analytics** | Google Analytics 4 + Hotjar ready |
| **Deploy** | Vercel (com otimizações automáticas de imagem) |
| **Performance** | Lighthouse 95+, Core Web Vitals verdes |
| **Acessibilidade** | WCAG AA (contraste, focus, aria, keyboard nav) |
| **Responsivo** | Mobile-first, breakpoints sm/md/lg/xl/2xl |

## 📱 COMPORTAMENTO MOBILE

- Navbar vira hamburger + sheet drawer (Radix ou shadcn)
- CTAs fixos no bottom: "Get Quote" + "Call Now"
- Grids de portfolio viram single column
- Stats counter ainda anima mas em formato compacto
- Form ocupa largura total
- Botões com minimum 44px tap target
- Tabelas viram cards empilhados

## 🧱 COMPONENTES REUTILIZÁVEIS (shadcn/ui style)

```
Button (variant: primary, secondary, ghost, accent, outline)
Card (com hover effect, image overlay)
Badge (anos, certificações)
SectionHeading (com linha decorativa ou glow)
StatsCounter (animado com IntersectionObserver)
TestimonialCard
ProjectCard (imagem + título + escopo + link)
ServiceCard (ícone + nome + descrição curta)
TeamMemberCard (foto + nome + cargo + bio curta)
ClientLogoCarousel (infinite scroll com logos reais)
ContactForm (4 campos + submit)
FAQAccordion
Breadcrumbs
StickyCTA (mobile bottom bar)
MapEmbed (Google Maps)
Footer (multi-coluna)
```

## 🎬 BRIEFING DIRETO PRA V0

> **"Crie um site para a Premium Contractors LLC, uma construtora comercial de Newark/NJ fundada em 1988. Use Next.js 15 App Router + Tailwind CSS v4 + Framer Motion. O visual precisa ser escuro, dramático, industrial-premium: fundo preto-azulado (#0a0a0f), detalhes em vermelho fogo (#e94560), tipografia Inter Tight (headings, bold) e Inter (body). Textura sutil de noise/grid nos fundos. Hero com parallax, stats animados, scroll reveals. O layout deve transmitir autoridade absoluta: 37+ anos de estrada, clientes como Marriott e Hilton, +250 projetos entregues. Paleta 100% dark mode. Formulário curto de 4 campos. Schema JSON-LD de GeneralContractor completo. SEO com breadcrumbs + FAQ schema + Service schema em cada página de serviço. Portfolio com casos reais. Depoimentos em destaque. Gere /llms.txt para AI SEO. Performance LCP <2s. Acessibilidade WCAG AA. Responsivo mobile-first. Use Framer Motion pra animações de entrada, contadores, parallax suave e stagger em grids. Crie páginas: /, /about, /services, /services/[slug], /projects, /projects/[slug], /industries/[slug], /team, /contact, /faq, /safety, /careers, /llms.txt."

## 📦 PÁGINAS QUE A V0 DEVE GERAR

1. **Home** (`/`) — hero, stats, featured projects, clients, services overview, depoimento, CTA
2. **About** (`/about`) — história, valores (Quality/Innovation/Integrity/Collaboration), visão ("To be the LEADING CONSTRUCTION COMPANY in the USA"), equipe
3. **Services Overview** (`/services`) — grid com todos os 15+ serviços
4. **Service Detail** (`/services/[slug]`) — template dinâmico para cada serviço com descrição, casos relacionados, CTA específico
5. **Portfolio** (`/projects`) — grid filtrável com projetos
6. **Case Study** (`/projects/[slug]`) — detalhe do projeto com escopo, fotos, desafios, resultados
7. **Industries** (`/industries/hospitality`) — setores que atendem
8. **Team** (`/team`) — cards do time
9. **Contact** (`/contact`) — form + mapa + informações
10. **Safety** (`/safety`) — cultura de segurança, compliance
11. **FAQ** (`/faq`) — accordion + schema markup
12. **Careers** (`/careers`) — trabalhe conosco
13. **Blog** (`/blog`) — posts de conteúdo SEO
14. **llms.txt** (`/llms.txt`) — AI SEO
15. **llms-full.txt** (`/llms-full.txt`) — versão completa

---

⚠️ **Importante:** O site atual da Premium Contractors está no Wix — lento, sem mobile adequado, sem schema, sem SEO. Tudo que está no briefing acima é **inexistente hoje**. A V0 vai construir do zero algo que seja referência absoluta no setor de construção comercial. O cliente final é uma construtora de verdade com 37+ anos — o site precisa ter a solidez de um edifício.
