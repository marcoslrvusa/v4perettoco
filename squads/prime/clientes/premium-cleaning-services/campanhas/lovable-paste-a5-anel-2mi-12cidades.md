# COLAR NO LOVABLE — OP. ANEL DE FERRO (A5) — 12 páginas locais

Do NOT publish this header. This is a build prompt, not page copy.
Site: premiumcleaningnj.com (React SPA on Lovable). Copy language: US English.
Source of truth for proof/cases/reviews: `src/data/proof.ts` and `src/data/site.ts`. Never invent proof, ratings, prices, certifications, or addresses.

---

## CREDIT RULES (binding — paste at the top of every prompt)

```
CREDIT RULES (binding): 1) First reply with a 5-bullet build plan and WAIT for my OK — do not generate code yet. 2) When fixing, edit ONLY files I name; never regenerate unaffected files. 3) Never reprint pasted copy; confirm with file paths + per-page checklist. 4) Same error twice → STOP, report file:line, and ask. 5) No new libraries, no redesign, US English, no emojis in UI.
```

---

## WHAT THIS BUILDS

10 new city pages + 2 expansions (Newark and Jersey City) + county hub patches + a reusable Iron Ring link block.

| # | City | URL | County | Primary keyword |
|---:|---|---|---|---|
| 1 | Harrison | `/commercial-cleaning-harrison-nj/` | Hudson | commercial cleaning harrison nj |
| 2 | Kearny | `/commercial-cleaning-kearny-nj/` | Hudson | commercial cleaning kearny nj |
| 3 | East Newark | `/commercial-cleaning-east-newark-nj/` | Hudson | commercial cleaning east newark nj |
| 4 | Belleville | `/commercial-cleaning-belleville-nj/` | Essex | commercial cleaning belleville nj |
| 5 | Irvington | `/commercial-cleaning-irvington-nj/` | Essex | commercial cleaning irvington nj |
| 6 | Hillside | `/commercial-cleaning-hillside-nj/` | Union | commercial cleaning hillside nj |
| 7 | East Orange | `/commercial-cleaning-east-orange-nj/` | Essex | commercial cleaning east orange nj |
| 8 | Nutley | `/commercial-cleaning-nutley-nj/` | Essex | commercial cleaning nutley nj |
| 9 | Bloomfield | `/commercial-cleaning-bloomfield-nj/` | Essex | commercial cleaning bloomfield nj |
| 10 | Secaucus | `/commercial-cleaning-secaucus-nj/` | Hudson | commercial cleaning secaucus nj |
| 11 | Newark (expand) | `/office-cleaning-newark-nj/` | Essex | office cleaning newark nj |
| 12 | Jersey City (expand) | `/office-cleaning-jersey-city-nj/` | Hudson | office cleaning jersey city nj |

Operating logic: each page is a local proof asset, not a doorway. It must answer a real local query, show real building/access context, compare the actual providers that appear in the 2026 scans, and link into the ring. No page may reuse another page's local paragraphs.

---

## STEP 0 — RECON (report only, wait for OK)

```
CREDIT RULES (binding): [PASTE THE CREDIT BLOCK]

In the existing Premium Cleaning NJ project, do NOT change code yet. Inspect and REPORT ONLY:
1) The file that renders /office-cleaning-newark-nj/: path + how route, meta title/description, H1, schema JSON-LD, and layout are implemented.
2) The router file path and the exact route definition pattern for location pages (paste 2 examples).
3) The head/SEO component: does it accept a `jsonLd` prop or inject static <script type="application/ld+json">? Paste the signature.
4) Component paths and props for QuoteCTA, ProofBand, FaqAccordion, PricingTable, RatingBadge.
5) Where city/location data lives today (if any): path + shape.
Reply with the 5-item report only. No code, no plan beyond recon.
```

Do not proceed until the report shows the real file paths. Then paste Step 1.

---

## STEP 1 — DATA + COMPONENT + 3 PILOT PAGES

### 1.1 Create `src/data/ironRing.ts`

Create this file EXACTLY. Do not "improve" the copy. Do not add cities or claims.

```ts
export type Competitor = {
  name: string;
  base: string;
  rating: number;
  reviews: number;
  model: string;
  fit: string;
};

export type CityFAQ = { q: string; a: string };
export type County = "Essex" | "Hudson" | "Union";
export type PricingRow = { scope: string; range: string; note: string };

export type IronRingCity = {
  slug: string;
  city: string;
  county: County;
  countySlug: string;
  zips: string[];
  primaryKeyword: string;
  secondaryKeywords: string[];
  metaTitle: string;
  metaDescription: string;
  h1: string;
  directAnswer: string;
  intro: string;
  localTitle: string;
  localBody: string[];
  buildings: string[];
  logistics: string[];
  competitors: Competitor[];
  faqs: CityFAQ[];
  neighbors: string[];
  proofCaseIds: string[];
  imageAlt: string;
};

export const INCLUDED = [
  "Nightly or scheduled office cleaning",
  "Restroom sanitizing and consumable restocking",
  "Trash, recycling, and common-area reset",
  "Hard-floor mopping, carpet spot-cleaning, and interior glass",
  "Breakroom and kitchen cleaning",
  "High-touch surface disinfection",
  "Day porter coverage (optional)",
  "Post-construction or move-in cleans (project-based)",
];

export const PRICING: Record<County, PricingRow[]> = {
  Essex: [
    { scope: "Suite <1,500 sq ft, 2x/week", range: "$350-$700/mo", note: "Professional and medical suites" },
    { scope: "1,500-4,000 sq ft, 3x/week", range: "$700-$1,500/mo", note: "Restrooms, kitchen, floors, trash" },
    { scope: "Floor 5,000+ sq ft, 5x/week", range: "$1,800-$4,200/mo", note: "Multi-zone nightly scope" },
    { scope: "Medical/restroom-heavy", range: "+15-35%", note: "Added frequency and compliance" },
  ],
  Hudson: [
    { scope: "Suite <1,500 sq ft, 2x/week", range: "$400-$750/mo", note: "Office and professional suites" },
    { scope: "1,500-4,000 sq ft, 3x/week", range: "$750-$1,600/mo", note: "Restrooms, kitchen, floors, trash" },
    { scope: "Floor 5,000+ sq ft, 5x/week", range: "$2,000-$4,800/mo", note: "Multi-zone nightly scope" },
    { scope: "High-rise nightly", range: "+10-25%", note: "Access, freight, and COI constraints" },
  ],
  Union: [
    { scope: "Suite <1,500 sq ft, 2x/week", range: "$350-$700/mo", note: "Office and professional suites" },
    { scope: "1,500-4,000 sq ft, 3x/week", range: "$700-$1,500/mo", note: "Restrooms, kitchen, floors, trash" },
    { scope: "3,000-7,000 sq ft, 3x/week", range: "$900-$2,000/mo", note: "Warehouse-office and multi-zone" },
    { scope: "Floor 5,000+ sq ft, 5x/week", range: "$1,800-$4,200/mo", note: "Nightly scope" },
  ],
] as const;

export const IRON_RING_CITIES: Record<string, IronRingCity> = {
  harrison: {
    slug: "commercial-cleaning-harrison-nj",
    city: "Harrison",
    county: "Hudson",
    countySlug: "commercial-cleaning-hudson-county-nj",
    zips: ["07029"],
    primaryKeyword: "commercial cleaning harrison nj",
    secondaryKeywords: ["office cleaning harrison nj", "commercial cleaners harrison nj", "janitorial services harrison nj"],
    metaTitle: "Commercial Cleaning Harrison NJ | 07029",
    metaDescription:
      "Commercial cleaning in Harrison, NJ 07029 — offices, industrial suites and retail along the Passaic River. Nightly crews. Call (973) 204-2310.",
    h1: "Commercial Cleaning in Harrison, NJ",
    directAnswer:
      "For offices, industrial suites, and retail along the Passaic River, Premium Cleaning Services provides nightly and 3x/week commercial cleaning in Harrison, NJ 07029. Crews are dispatched from Newark, supervised, insured, and scheduled around Red Bull Arena event traffic and PATH commuter hours.",
    intro:
      "Harrison is no longer just an industrial river town. The Passaic River waterfront, the PATH station, and the Red Bull Arena district have added offices, restaurants, and residential buildings beside freight and light-industrial suites. That mix creates a specific cleaning problem: a riverfront lobby, a warehouse office, and a game-day restaurant all need different scopes, different access windows, and one accountable vendor. We built a fixed Harrison route around those three building types.",
    localTitle: "Commercial cleaning for Harrison's riverfront, PATH, and industrial corridor",
    localBody: [
      "Our Harrison route covers the blocks around Frank E. Rodgers Boulevard, Harrison Avenue, and the Passaic River waterfront. For riverfront office and residential buildings, we coordinate lobby and amenity cleaning, restroom reset, trash room, and glass. For warehouse and light-industrial offices, the scope shifts to breakrooms, locker areas, floors, and dust control. For restaurants and retail near Red Bull Arena, we work before service or after close so game-day crowds never see a wet floor or an unattended trash can.",
      "Because Harrison shares a border with Newark's Ironbound and Kearny, the same supervisor can cover a Harrison lobby and a Kearny warehouse office on the same night. That is the operational advantage of a two-mile ring: no subcontracted crew, no third-party dispatch, no surprise invoice.",
    ],
    buildings: [
      "Riverfront office and residential buildings along the Passaic River",
      "Warehouse and light-industrial offices near Frank E. Rodgers Boulevard",
      "Restaurants, retail, and service businesses around Red Bull Arena",
      "Professional and medical suites along Harrison Avenue",
      "Small industrial and contractor offices near the PATH station",
    ],
    logistics: [
      "Red Bull Arena event days can close streets and compress loading windows; we confirm the building's event plan before the first visit.",
      "PATH commuter traffic peaks before 9 am and after 5 pm; most office work starts after 6 pm or before 7 am.",
      "Street parking and loading zones are limited on Frank E. Rodgers Boulevard; crews use the building's designated vendor area.",
      "Riverfront buildings often require a COI and vendor registration; we complete both before the first clean.",
      "Harrison, East Newark, and Kearny share one nightly route, so multi-site clients keep one supervisor and one invoice.",
    ],
    competitors: [
      { name: "Totally Cleaning Services", base: "224 John St, Harrison, NJ 07029", rating: 5.0, reviews: 133, model: "Owner-operated local", fit: "Harrison-based; high review volume" },
      { name: "Jersey Cleaning Solution, LLC", base: "223 John St, Harrison, NJ 07029", rating: 5.0, reviews: 6, model: "Owner-operated local", fit: "Small commercial and residential" },
      { name: "One Concept Facility Solutions", base: "109 Belgrove Dr, Kearny, NJ 07032", rating: 4.8, reviews: 21, model: "Supervisor-led facility services", fit: "Kearny and office routes" },
      { name: "Skyline Cleaning Services LLC", base: "143 Rome St, Newark, NJ 07105", rating: 4.2, reviews: 49, model: "Regional commercial cleaner", fit: "Newark and Essex coverage" },
    ],
    faqs: [
      { q: "Do you clean offices near Red Bull Arena on event days?", a: "Yes. We schedule around event-day road closures and pedestrian traffic. For buildings near the arena, crews work before the event window or after the crowd clears; we confirm the building's access plan before the first visit." },
      { q: "Can you clean a warehouse office on Frank E. Rodgers Boulevard?", a: "Yes. Warehouse and light-industrial offices are a core part of our Harrison route. Scope includes the front office, dispatch, breakroom, restrooms, locker areas, and floors, with dust control matched to the building's operation." },
      { q: "Do you serve East Newark and Kearny from the same route?", a: "Yes. Harrison, East Newark, and Kearny are on the same nightly route. A client with buildings in two or three of these towns keeps one supervisor, one checklist system, and one invoice." },
      { q: "What time do crews start in Harrison?", a: "Most Harrison office and retail work starts after 6 pm or before 7 am. Game-day and restaurant accounts are scheduled around service windows. We confirm the exact window in the written scope." },
      { q: "Are you insured for riverfront and building-management requirements?", a: "Yes. We carry general liability and workers' compensation and issue a certificate of insurance before start. For buildings that require vendor registration, we complete the building's onboarding before the first clean." },
      { q: "How fast can you quote a Harrison office?", a: "Send the address, square footage, restroom count, and preferred frequency. We can usually return a written range within one business day and schedule a walkthrough within 48 hours." },
    ],
    neighbors: ["commercial-cleaning-kearny-nj", "commercial-cleaning-east-newark-nj", "office-cleaning-newark-nj"],
    proofCaseIds: ["briard-office", "promenade"],
    imageAlt: "Commercial cleaning in Harrison, NJ — riverfront office and industrial suites",
  },

  kearny: {
    slug: "commercial-cleaning-kearny-nj",
    city: "Kearny",
    county: "Hudson",
    countySlug: "commercial-cleaning-hudson-county-nj",
    zips: ["07032"],
    primaryKeyword: "commercial cleaning kearny nj",
    secondaryKeywords: ["office cleaning kearny nj", "commercial cleaners kearny nj", "janitorial services kearny nj"],
    metaTitle: "Commercial Cleaning Kearny NJ | 07032",
    metaDescription:
      "Commercial cleaning in Kearny, NJ 07032 — warehouse offices, Kearny Point flex space and Route 7 retail. Nightly crews. Call (973) 204-2310.",
    h1: "Commercial Cleaning in Kearny, NJ",
    directAnswer:
      "Premium Cleaning Services provides commercial cleaning in Kearny, NJ 07032 for warehouse offices, Kearny Point flex spaces, and Route 7 retail. Nightly, 3x/week, and day porter coverage is dispatched from our Newark base, with a written scope and a named supervisor.",
    intro:
      "Kearny's commercial stock is a mix of warehouse offices, flex and industrial space at Kearny Point, Route 7 retail, and professional suites in the Arlington section. The town sits at the junction of the NJ Turnpike (Exit 15E) and Route 7, so access and shift timing matter as much as the cleaning itself.",
    localTitle: "Commercial cleaning for Kearny Point, Route 7, and Arlington",
    localBody: [
      "At Kearny Point and the surrounding industrial parks, we clean office pods, breakrooms, locker rooms, dispatch offices, and customer-facing showrooms. Crews work around dock schedules and shift changes; we do not block a live loading bay during an inbound window. For Route 7 retail and restaurants, the work happens before opening or after closing, with trash and restroom resets timed to foot traffic.",
      "Arlington's professional offices and medical suites need a quieter, detail-oriented scope: waiting areas, restrooms, floors, and high-touch surfaces. The same supervisor covers Harrison and East Newark, so a Kearny client with a second site across the river gets one point of contact and one invoice.",
    ],
    buildings: [
      "Warehouse and distribution offices near NJ Turnpike Exit 15E",
      "Flex, industrial, and creative-office space at Kearny Point",
      "Route 7 retail, restaurants, and service businesses",
      "Professional and medical suites in the Arlington section",
      "Municipal-adjacent and contractor offices along Kearny Avenue",
    ],
    logistics: [
      "NJ Turnpike Exit 15E and Route 7 carry heavy truck traffic; we confirm dock access and shift changes before the first visit.",
      "Kearny Point and managed industrial parks require vendor registration and a COI; we complete both before start.",
      "Warehouse crews do not block live loading bays; the schedule is built around inbound and outbound windows.",
      "Arlington offices are cleaned after hours or before opening to avoid patient and staff traffic.",
      "Kearny, Harrison, and East Newark share one nightly route, which keeps multi-site coverage economical.",
    ],
    competitors: [
      { name: "One Concept Facility Solutions", base: "109 Belgrove Dr, Kearny, NJ 07032", rating: 4.8, reviews: 21, model: "Supervisor-led facility services", fit: "Kearny and office routes" },
      { name: "City Wide Facility Solutions - Liberty Harbor", base: "78 John Miller Way, Kearny, NJ 07032", rating: 5.0, reviews: 35, model: "Franchise/system", fit: "Multi-service facility management" },
      { name: "Totally Cleaning Services", base: "224 John St, Harrison, NJ 07029", rating: 5.0, reviews: 133, model: "Owner-operated local", fit: "Harrison-based; high review volume" },
      { name: "Skyline Cleaning Services LLC", base: "143 Rome St, Newark, NJ 07105", rating: 4.2, reviews: 49, model: "Regional commercial cleaner", fit: "Newark and Essex coverage" },
    ],
    faqs: [
      { q: "Do you clean Kearny Point flex and industrial spaces?", a: "Yes. We clean office pods, breakrooms, dispatch areas, locker rooms, and customer-facing showrooms at Kearny Point and nearby industrial parks. Crews work around dock schedules and shift changes." },
      { q: "Can you cover a Route 7 retail or restaurant space?", a: "Yes. Route 7 retail and restaurant work is scheduled before opening or after closing, with glass, floors, restrooms, and trash handled without blocking deliveries or customer flow." },
      { q: "Do you clean medical or professional suites in Arlington?", a: "Yes. Arlington professional and medical suites get common-area cleaning: waiting rooms, reception, restrooms, breakrooms, corridors, and floors. We do not handle exam rooms, procedure rooms, or regulated medical waste." },
      { q: "How do you handle warehouse dock and shift schedules?", a: "We confirm inbound and outbound windows, dock access, and shift changes before the first visit. Crews do not block a live loading bay; the schedule is built around the operation, not a generic after-hours slot." },
      { q: "Are you insured for industrial landlords?", a: "Yes. We carry general liability and workers' compensation and provide a COI before start. For Kearny Point and other managed properties, we complete the landlord's vendor requirements first." },
      { q: "How fast can you start in Kearny?", a: "Most Kearny starts are 3-5 business days after a walkthrough and approved scope. If the building requires COI review or security onboarding, add 1-2 days." },
    ],
    neighbors: ["commercial-cleaning-harrison-nj", "commercial-cleaning-east-newark-nj", "commercial-cleaning-belleville-nj"],
    proofCaseIds: ["briard-office", "promenade"],
    imageAlt: "Commercial cleaning in Kearny, NJ — warehouse office and Kearny Point flex space",
  },

  eastNewark: {
    slug: "commercial-cleaning-east-newark-nj",
    city: "East Newark",
    county: "Hudson",
    countySlug: "commercial-cleaning-hudson-county-nj",
    zips: ["07029"],
    primaryKeyword: "commercial cleaning east newark nj",
    secondaryKeywords: ["office cleaning east newark nj", "commercial cleaners east newark nj", "janitorial services east newark nj"],
    metaTitle: "Commercial Cleaning East Newark NJ | 07029",
    metaDescription:
      "Commercial cleaning in East Newark, NJ 07029 — small industrial offices and contractor suites on the Harrison/Kearny route. Call (973) 204-2310.",
    h1: "Commercial Cleaning in East Newark, NJ",
    directAnswer:
      "East Newark's small industrial and office buildings get the same fixed-route service we run in Harrison and Kearny. Premium Cleaning Services covers East Newark, NJ 07029 with nightly or weekly commercial cleaning, insured crews, and a written checklist for restrooms, floors, and common areas.",
    intro:
      "East Newark is the second-smallest municipality in New Jersey, a compact borough across the Passaic River from Newark. Its commercial base is small industrial buildings, contractor suites, food-production support offices, and neighborhood retail. Because it sits inside the Harrison and Kearny route, it gets the same crew and supervisor without a separate trip charge.",
    localTitle: "Commercial cleaning for East Newark's compact industrial and office stock",
    localBody: [
      "Most East Newark buildings are small-footprint: a single office floor, a contractor shop with a front office, a food-production support space, or a retail unit. That means the scope has to be precise. We build a zone checklist for the front office, restroom, breakroom, production-adjacent areas, and trash, then set frequency based on headcount and shift patterns.",
      "Access is the constraint. Grant Avenue and Passaic Avenue carry truck traffic, and some buildings have limited loading or street parking. We schedule around deliveries and confirm keys, alarm codes, and COI requirements before the first visit. Because Harrison and Kearny are on the same route, a small East Newark office can be served on a 2x/week schedule without a minimum-route surcharge.",
    ],
    buildings: [
      "Small industrial offices and contractor suites",
      "Food-production support offices (non-production areas)",
      "Neighborhood retail and service businesses",
      "Warehouse-adjacent front offices",
      "Mixed-use buildings along Grant Avenue and Passaic Avenue",
    ],
    logistics: [
      "East Newark shares the 07029 ZIP with Harrison; include the street address when requesting a quote.",
      "Grant Avenue and Passaic Avenue carry truck traffic; crews avoid blocking active loading areas.",
      "Some buildings have limited street parking; crews use the designated vendor space or arrive in a compact vehicle.",
      "The borough runs on the Harrison/Kearny route, so service windows are the same as those towns.",
      "COI and vendor registration are completed before the first clean for managed buildings.",
    ],
    competitors: [
      { name: "Blue Home Cleaning Services", base: "440 N 2nd St, East Newark, NJ 07029", rating: 5.0, reviews: 18, model: "Local owner-operated", fit: "East Newark small business" },
      { name: "One Concept Facility Solutions", base: "109 Belgrove Dr, Kearny, NJ 07032", rating: 4.8, reviews: 21, model: "Supervisor-led facility services", fit: "Kearny and office routes" },
      { name: "Jersey Cleaning Solution, LLC", base: "223 John St, Harrison, NJ 07029", rating: 5.0, reviews: 6, model: "Owner-operated local", fit: "Small commercial and residential" },
      { name: "Totally Cleaning Services", base: "224 John St, Harrison, NJ 07029", rating: 5.0, reviews: 133, model: "Owner-operated local", fit: "Harrison-based; high review volume" },
    ],
    faqs: [
      { q: "Do you serve East Newark separately from Harrison?", a: "Yes, but it runs on the same route. East Newark is a short hop from Harrison and Kearny, so a small office or industrial suite gets fixed-route service without a separate trip charge." },
      { q: "Can you clean a small industrial office with a shop floor?", a: "Yes. We define the boundary between office and production areas in the scope. The crew cleans the front office, restrooms, breakroom, and office floors; production equipment and regulated areas stay with your team unless explicitly added." },
      { q: "What ZIP code do you use for East Newark?", a: "East Newark shares the 07029 ZIP with Harrison. Use 07029 for quotes and service-area checks, and include the street address so we can confirm building access and routing." },
      { q: "How do you handle limited parking and truck traffic?", a: "We confirm loading and parking before the first visit. Crews arrive in a compact vehicle, use the building's designated vendor area, and avoid blocking Grant Avenue or Passaic Avenue truck routes." },
      { q: "Are you insured for small commercial buildings?", a: "Yes. We carry general liability and workers' compensation and provide a COI before start. Small buildings get the same insurance and supervisor coverage as larger accounts." },
      { q: "How fast can you quote East Newark?", a: "Send the address, square footage, restroom count, and frequency. We can usually return a written range within one business day and schedule a walkthrough within 48 hours." },
    ],
    neighbors: ["commercial-cleaning-harrison-nj", "commercial-cleaning-kearny-nj", "office-cleaning-newark-nj"],
    proofCaseIds: ["briard-office"],
    imageAlt: "Commercial cleaning in East Newark, NJ — small industrial office",
  },

  belleville: {
    slug: "commercial-cleaning-belleville-nj",
    city: "Belleville",
    county: "Essex",
    countySlug: "commercial-cleaning-essex-county-nj",
    zips: ["07109"],
    primaryKeyword: "commercial cleaning belleville nj",
    secondaryKeywords: ["office cleaning belleville nj", "commercial cleaners belleville nj", "janitorial services belleville nj"],
    metaTitle: "Commercial Cleaning Belleville NJ | 07109",
    metaDescription:
      "Commercial cleaning in Belleville, NJ 07109 — medical suites, professional offices and Main Street retail. Evening crews. Call (973) 204-2310.",
    h1: "Commercial Cleaning in Belleville, NJ",
    directAnswer:
      "Premium Cleaning Services provides commercial cleaning in Belleville, NJ 07109 for medical suites, professional offices, and Main Street retail. Nightly and 2-3x/week crews handle restrooms, waiting rooms, floors, and trash, with scheduling built around patient hours and Route 21 traffic.",
    intro:
      "Belleville's commercial demand runs along Washington Avenue, Main Street, and the Route 21 corridor, with a strong medical and professional-office base around Clara Maass Medical Center. The township also has restaurants, retail, and small industrial pockets. We schedule around patient hours, school traffic, and the evening rush on Route 21.",
    localTitle: "Commercial cleaning for Belleville's medical, professional, and Main Street buildings",
    localBody: [
      "Medical office common areas are not clinical spaces. We clean waiting rooms, reception, restrooms, staff breakrooms, and corridors — not exam rooms, procedure rooms, or regulated medical waste. That distinction matters for compliance and for the scope you sign. For professional suites and law or accounting offices, the work is after hours: desks, conference rooms, kitchen, restrooms, and floors.",
      "Main Street retail and restaurants need a different rhythm: before opening or after close, with glass, floors, restrooms, and trash handled without blocking deliveries or customer flow. We confirm dumpster access, grease-adjacent areas (no hood cleaning), and any building-specific recycling rules before start.",
    ],
    buildings: [
      "Medical office buildings and professional suites near Clara Maass",
      "Law, accounting, and insurance offices along Washington Avenue",
      "Main Street retail, restaurants, and service businesses",
      "Small industrial and contractor offices",
      "Mixed-use buildings along the Route 21 corridor",
    ],
    logistics: [
      "Clara Maass-area medical suites are cleaned before opening or after the last patient; patient hours are confirmed before start.",
      "Route 21 traffic peaks in the evening; crews schedule around the rush rather than sitting in it.",
      "Washington Avenue and Main Street have limited street parking; crews use designated vendor spaces.",
      "Restaurants require before-open or after-close access; hood and exhaust cleaning are not part of the scope.",
      "Belleville shares the Essex route with Bloomfield, Nutley, and Newark, which keeps multi-site coverage efficient.",
    ],
    competitors: [
      { name: "Skyline Cleaning Services LLC", base: "143 Rome St, Newark, NJ 07105", rating: 4.2, reviews: 49, model: "Regional commercial cleaner", fit: "Newark and Essex coverage" },
      { name: "Newark Cleaning Services LLC", base: "191 Bloomfield Ave, Newark, NJ 07104", rating: 4.6, reviews: 29, model: "Local commercial cleaner", fit: "Newark and Essex offices" },
      { name: "Liz Cleaning", base: "855 Clinton Ave, Newark, NJ 07108", rating: 5.0, reviews: 7, model: "Local owner-operated", fit: "Newark-area offices" },
      { name: "N&R Divine Cleaning Services LLC", base: "211 Warren St, Newark, NJ 07103", rating: 5.0, reviews: 6, model: "Local owner-operated", fit: "Small offices" },
    ],
    faqs: [
      { q: "Do you clean medical offices near Clara Maass?", a: "Yes, common areas only. We clean waiting rooms, reception, restrooms, breakrooms, corridors, and floors. We do not clean exam rooms, procedure rooms, or regulated medical waste; those require a clinical protocol." },
      { q: "Can you work around patient hours?", a: "Yes. Most Belleville medical and professional suites are cleaned before opening or after the last patient. We confirm the building's patient schedule and access rules before the first visit." },
      { q: "Do you serve Main Street retail and restaurants?", a: "Yes. Retail and restaurant work is scheduled before opening or after closing, with glass, floors, restrooms, and trash handled without blocking deliveries or customer flow. Hood and exhaust cleaning is a separate specialty." },
      { q: "What does a Belleville office cost?", a: "Reference bands: a suite under 1,500 sq ft at 2x/week typically runs $350-$700/mo; 1,500-4,000 sq ft at 3x/week runs $700-$1,500/mo. Medical or restroom-heavy space can add 15-35%. Final quote after walkthrough." },
      { q: "Are you insured for landlords and medical tenants?", a: "Yes. We carry general liability and workers' compensation and provide a COI before start. For medical tenants, the scope explicitly excludes clinical waste and exam or procedure areas." },
      { q: "How fast can you start in Belleville?", a: "Most starts are 3-5 business days after a walkthrough and approved scope. If the building requires COI review or after-hours registration, add 1-2 days." },
    ],
    neighbors: ["commercial-cleaning-kearny-nj", "commercial-cleaning-bloomfield-nj", "office-cleaning-newark-nj"],
    proofCaseIds: ["briard-office"],
    imageAlt: "Commercial cleaning in Belleville, NJ — medical office and professional suite",
  },

  irvington: {
    slug: "commercial-cleaning-irvington-nj",
    city: "Irvington",
    county: "Essex",
    countySlug: "commercial-cleaning-essex-county-nj",
    zips: ["07111"],
    primaryKeyword: "commercial cleaning irvington nj",
    secondaryKeywords: ["office cleaning irvington nj", "commercial cleaners irvington nj", "janitorial services irvington nj"],
    metaTitle: "Commercial Cleaning Irvington NJ | 07111",
    metaDescription:
      "Commercial cleaning in Irvington, NJ 07111 — offices, clinics and retail along Clinton and Springfield Avenues. Call (973) 204-2310.",
    h1: "Commercial Cleaning in Irvington, NJ",
    directAnswer:
      "For offices, clinics, and retail along Clinton and Springfield Avenues, Premium Cleaning Services provides commercial cleaning in Irvington, NJ 07111. Crews work evenings and weekends, use written zone checklists, and are supervised from our Newark base with insured, background-checked staff.",
    intro:
      "Irvington's commercial corridors run along Clinton Avenue and Springfield Avenue, with a mix of retail, clinics, professional suites, and light industrial. The township is dense, parking is tight, and many buildings have separate front and back entrances. We build evening routes around those constraints.",
    localTitle: "Commercial cleaning for Irvington's Clinton and Springfield Avenue corridors",
    localBody: [
      "Retail and clinic spaces on Clinton Avenue need daily or 3x/week attention: restrooms, floors, glass, trash, and high-touch surfaces. Professional suites and small offices often run well on 2x/week. Light-industrial and contractor spaces need breakroom, locker, and floor care with dust control.",
      "Access is the deciding factor. Some buildings have rear parking, some only street parking, and some share a common entrance with residential units. We confirm the entry, alarm, and trash route before the first visit, then lock the schedule so the same crew handles the same building.",
    ],
    buildings: [
      "Retail and clinic spaces along Clinton Avenue",
      "Professional suites and small offices on Springfield Avenue",
      "Light-industrial and contractor offices",
      "Houses of worship and nonprofit common areas",
      "Mixed-use buildings with shared entrances",
    ],
    logistics: [
      "Street parking is tight on Clinton and Springfield Avenues; crews use the building's designated vendor area.",
      "Irvington Bus Terminal traffic affects evening access; schedules avoid peak boarding windows.",
      "Some buildings have separate front and back entrances; the scope names the entrance used by the crew.",
      "Light-industrial spaces need dust control matched to the operation.",
      "Irvington is on the Newark/East Orange route, so multi-site clients keep one supervisor.",
    ],
    competitors: [
      { name: "DSY Commercial Cleaning Service", base: "340 Myrtle Ave Apt 23, Irvington, NJ 07111", rating: 5.0, reviews: 2, model: "Local owner-operated", fit: "Irvington-area commercial" },
      { name: "Dawn Cleaning Service", base: "2 Berkeley Terrace Apt 10b, Irvington, NJ 07111", rating: 3.0, reviews: 2, model: "Local owner-operated", fit: "Small commercial" },
      { name: "Newark Cleaning Services LLC", base: "191 Bloomfield Ave, Newark, NJ 07104", rating: 4.6, reviews: 29, model: "Local commercial cleaner", fit: "Newark and Essex offices" },
      { name: "Skyline Cleaning Services LLC", base: "143 Rome St, Newark, NJ 07105", rating: 4.2, reviews: 49, model: "Regional commercial cleaner", fit: "Newark and Essex coverage" },
    ],
    faqs: [
      { q: "Do you clean retail on Clinton Avenue?", a: "Yes. Clinton Avenue retail and clinic spaces get before-open or after-close service: glass, floors, restrooms, trash, and high-touch surfaces. We confirm the building's opening time and trash route before the first visit." },
      { q: "Can you cover a professional suite on Springfield Avenue?", a: "Yes. Professional suites typically run 2x/week: desks, conference rooms, kitchen, breakroom, restrooms, and floors. We build a zone checklist so the same crew handles the same rooms each visit." },
      { q: "Do you clean clinics or medical offices in Irvington?", a: "We clean medical office common areas: waiting rooms, reception, restrooms, breakrooms, corridors, and floors. We do not handle exam rooms, procedure rooms, or regulated medical waste." },
      { q: "How do you handle tight street parking?", a: "Crews use compact vehicles and the building's designated vendor area. We confirm parking and loading before the first visit and avoid blocking driveways, bus stops, or fire hydrants." },
      { q: "Are you insured for Irvington commercial buildings?", a: "Yes. We carry general liability and workers' compensation and provide a COI before start. We also complete building-specific security or vendor onboarding when required." },
      { q: "How fast can you quote an Irvington office?", a: "Send the address, square footage, restroom count, and frequency. We can usually return a written range within one business day and schedule a walkthrough within 48 hours." },
    ],
    neighbors: ["office-cleaning-newark-nj", "commercial-cleaning-east-orange-nj", "commercial-cleaning-hillside-nj"],
    proofCaseIds: ["promenade"],
    imageAlt: "Commercial cleaning in Irvington, NJ — retail and professional office",
  },

  hillside: {
    slug: "commercial-cleaning-hillside-nj",
    city: "Hillside",
    county: "Union",
    countySlug: "commercial-cleaning-union-county-nj",
    zips: ["07205"],
    primaryKeyword: "commercial cleaning hillside nj",
    secondaryKeywords: ["office cleaning hillside nj", "commercial cleaners hillside nj", "janitorial services hillside nj"],
    metaTitle: "Commercial Cleaning Hillside NJ | 07205",
    metaDescription:
      "Commercial cleaning in Hillside, NJ 07205 — warehouse offices, Route 22 retail and suites near Kean University. Call (973) 204-2310.",
    h1: "Commercial Cleaning in Hillside, NJ",
    directAnswer:
      "Premium Cleaning Services provides commercial cleaning in Hillside, NJ 07205 for warehouse offices, Route 22 retail, and professional suites near Kean University. Nightly, weekly, and project cleans are available with insured, background-checked crews and a named supervisor.",
    intro:
      "Hillside sits between Route 22, Vaux Hall Road, and the Kean University area, with a commercial base built on warehouse and distribution offices, retail, and professional suites. Shift schedules and dock traffic shape the cleaning window.",
    localTitle: "Commercial cleaning for Hillside's Route 22, warehouse, and Kean-area buildings",
    localBody: [
      "Warehouse and distribution offices need clean breakrooms, restrooms, dispatch desks, and customer-facing front offices without disrupting inbound and outbound shifts. We schedule around dock windows, not the other way around. Route 22 retail and restaurants get before-open or after-close service with glass, floors, restrooms, and trash.",
      "Professional suites near Kean University and the township's medical offices need a quieter scope: waiting areas, restrooms, floors, and high-touch surfaces. Because Hillside is on the Union County edge of our ring, we combine it with Irvington and Newark routes to keep frequency economical.",
    ],
    buildings: [
      "Warehouse and distribution offices near Route 22",
      "Retail and restaurants along Route 22 and Hillside Avenue",
      "Professional suites near Kean University",
      "Light-manufacturing and contractor offices",
      "Medical office common areas",
    ],
    logistics: [
      "Route 22 traffic and warehouse docks shape the service window; we confirm inbound and outbound schedules.",
      "Vaux Hall Road carries commuter traffic; crews avoid peak windows when possible.",
      "Managed industrial parks require vendor registration and a COI before start.",
      "Professional suites are cleaned after hours or before opening.",
      "Hillside is combined with Irvington and Newark routes to keep pricing stable.",
    ],
    competitors: [
      { name: "Jacklin Cleaning Service", base: "257 Hollywood Ave, Hillside, NJ 07205", rating: 4.9, reviews: 20, model: "Local commercial cleaner", fit: "Hillside and Union County" },
      { name: "Olmos Cleaning Services", base: "220 Conklin Ave, Hillside, NJ 07205", rating: 5.0, reviews: 9, model: "Local owner-operated", fit: "Hillside-area offices" },
      { name: "Totally Cleaning Services", base: "224 John St, Harrison, NJ 07029", rating: 5.0, reviews: 133, model: "Owner-operated local", fit: "Harrison-based; high review volume" },
      { name: "Jersey Cleaning Solution, LLC", base: "223 John St, Harrison, NJ 07029", rating: 5.0, reviews: 6, model: "Owner-operated local", fit: "Small commercial and residential" },
    ],
    faqs: [
      { q: "Do you clean warehouse offices near Route 22?", a: "Yes. Warehouse and distribution offices are a core Hillside scope: front office, dispatch, breakrooms, restrooms, locker areas, and floors. We schedule around dock windows and shift changes." },
      { q: "Can you cover Route 22 retail?", a: "Yes. Retail work is scheduled before opening or after closing, with glass, floors, restrooms, and trash handled without blocking deliveries or customer flow." },
      { q: "Do you serve professional suites near Kean University?", a: "Yes. Professional and medical suites get common-area cleaning: waiting rooms, reception, restrooms, breakrooms, corridors, and floors. We do not handle exam rooms, procedure rooms, or regulated medical waste." },
      { q: "What does a Hillside office cost?", a: "Reference bands: a suite under 1,500 sq ft at 2x/week typically runs $350-$700/mo; 1,500-4,000 sq ft at 3x/week runs $700-$1,500/mo. Warehouse-office scope is quoted after a walkthrough." },
      { q: "Are you insured for industrial landlords?", a: "Yes. We carry general liability and workers' compensation and provide a COI before start. For managed industrial parks, we complete the landlord's vendor requirements first." },
      { q: "How fast can you start in Hillside?", a: "Most Hillside starts are 3-5 business days after a walkthrough and approved scope. If the building requires COI review or security onboarding, add 1-2 days." },
    ],
    neighbors: ["commercial-cleaning-irvington-nj", "office-cleaning-newark-nj", "office-cleaning-jersey-city-nj"],
    proofCaseIds: ["promenade"],
    imageAlt: "Commercial cleaning in Hillside, NJ — warehouse office and Route 22 retail",
  },

  eastOrange: {
    slug: "commercial-cleaning-east-orange-nj",
    city: "East Orange",
    county: "Essex",
    countySlug: "commercial-cleaning-essex-county-nj",
    zips: ["07017", "07018", "07019"],
    primaryKeyword: "commercial cleaning east orange nj",
    secondaryKeywords: ["office cleaning east orange nj", "commercial cleaners east orange nj", "janitorial services east orange nj"],
    metaTitle: "Commercial Cleaning East Orange NJ | 07017",
    metaDescription:
      "Commercial cleaning in East Orange, NJ 07017-07019 — professional suites, medical offices and transit-oriented retail. Call (973) 204-2310.",
    h1: "Commercial Cleaning in East Orange, NJ",
    directAnswer:
      "Premium Cleaning Services provides commercial cleaning in East Orange, NJ 07017-07019 for professional suites, medical offices, and transit-oriented retail. Evening and nightly crews cover restrooms, floors, trash, and common areas with a named supervisor and written scope.",
    intro:
      "East Orange's commercial stock clusters around Main Street, Brick Church, and the City Hall corridor, with professional suites, medical offices, nonprofit and admin space, and transit-oriented retail. Many buildings are older, with narrow stairs, shared entrances, and limited parking.",
    localTitle: "Commercial cleaning for East Orange's Main Street and Brick Church corridors",
    localBody: [
      "Older buildings need a crew that reads the building, not just the checklist. We confirm trash chutes, freight and stairs, restroom counts, and after-hours access before the first visit. Professional suites get desk, conference, kitchen, and restroom care; medical offices get common-area cleaning only, with no clinical waste handling.",
      "Brick Church station traffic and street parking shape the evening window. We schedule after the commuter peak and before late-building lockout, then keep the same crew on the same nights so tenants see a familiar, accountable team.",
    ],
    buildings: [
      "Professional and admin suites around Main Street",
      "Medical office common areas near Brick Church",
      "Transit-oriented retail and service businesses",
      "Nonprofit and community organization offices",
      "Older mixed-use buildings with shared entrances",
    ],
    logistics: [
      "Brick Church station traffic peaks before 9 am and after 5 pm; office work starts after the evening peak.",
      "Street parking is limited; crews use the building's vendor space and compact vehicles.",
      "Older buildings may lack freight elevators; equipment size is confirmed before the first visit.",
      "Shared entrances and residential units require a clear access plan.",
      "East Orange is on the Newark/Irvington route, so multi-site clients keep one supervisor.",
    ],
    competitors: [
      { name: "Zhannas Cleaning", base: "62-68 Halsted St Ste 220, East Orange, NJ 07018", rating: 5.0, reviews: 14, model: "Local commercial cleaner", fit: "East Orange and Essex" },
      { name: "Jacklin Cleaning Service", base: "257 Hollywood Ave, Hillside, NJ 07205", rating: 4.9, reviews: 20, model: "Local commercial cleaner", fit: "Hillside and Union County" },
      { name: "Stephany Cleaning Services", base: "132 Telford St, Newark, NJ 07106", rating: 4.9, reviews: 32, model: "Local commercial cleaner", fit: "Newark and East Orange" },
      { name: "Newark Cleaning Services LLC", base: "191 Bloomfield Ave, Newark, NJ 07104", rating: 4.6, reviews: 29, model: "Local commercial cleaner", fit: "Newark and Essex offices" },
    ],
    faqs: [
      { q: "Do you clean offices near Brick Church station?", a: "Yes. Offices and professional suites around Brick Church and Main Street are cleaned after the commuter peak or before opening. We confirm building access, parking, and security before the first visit." },
      { q: "Can you handle older buildings with narrow stairs?", a: "Yes. We confirm stair access, restroom counts, trash routes, and equipment size before the first clean. Compact equipment is used where freight elevators are unavailable." },
      { q: "Do you clean medical offices in East Orange?", a: "We clean medical office common areas: waiting rooms, reception, restrooms, breakrooms, corridors, and floors. We do not handle exam rooms, procedure rooms, or regulated medical waste." },
      { q: "How do you schedule around street parking?", a: "Crews use compact vehicles and the building's designated vendor area. We confirm parking and loading before the first visit and avoid blocking driveways, bus stops, or fire hydrants." },
      { q: "Are you insured for East Orange landlords?", a: "Yes. We carry general liability and workers' compensation and provide a COI before start. We also complete building-specific security or vendor onboarding when required." },
      { q: "How fast can you quote an East Orange office?", a: "Send the address, square footage, restroom count, and frequency. We can usually return a written range within one business day and schedule a walkthrough within 48 hours." },
    ],
    neighbors: ["office-cleaning-newark-nj", "commercial-cleaning-irvington-nj", "commercial-cleaning-bloomfield-nj"],
    proofCaseIds: ["briard-office"],
    imageAlt: "Commercial cleaning in East Orange, NJ — professional office suite",
  },

  nutley: {
    slug: "commercial-cleaning-nutley-nj",
    city: "Nutley",
    county: "Essex",
    countySlug: "commercial-cleaning-essex-county-nj",
    zips: ["07110"],
    primaryKeyword: "commercial cleaning nutley nj",
    secondaryKeywords: ["office cleaning nutley nj", "commercial cleaners nutley nj", "janitorial services nutley nj"],
    metaTitle: "Commercial Cleaning Nutley NJ | 07110",
    metaDescription:
      "Commercial cleaning in Nutley, NJ 07110 — ON3 offices, Franklin Avenue suites and local retail. Nightly and 2-3x/week service. Call (973) 204-2310.",
    h1: "Commercial Cleaning in Nutley, NJ",
    directAnswer:
      "Premium Cleaning Services provides commercial cleaning in Nutley, NJ 07110 for offices at ON3, Franklin Avenue professional suites, and local retail. Nightly and 2-3x/week service includes written zone checklists, insured crews, and supervisor walkthroughs.",
    intro:
      "Nutley's commercial base includes the ON3 campus (the former Hoffmann-La Roche site), Franklin Avenue professional suites, Kingsland Avenue retail, and local restaurants. Campus security and COI requirements are stricter here than in a typical Main Street building.",
    localTitle: "Commercial cleaning for ON3, Franklin Avenue, and Nutley Center",
    localBody: [
      "At ON3 and other campus-style properties, we coordinate security clearance, COI, loading dock access, and after-hours badging before the first clean. The scope typically covers office floors, conference rooms, restrooms, breakrooms, lobbies, and common areas. For Franklin Avenue medical and professional suites, the work is after hours with a focus on waiting rooms, restrooms, and high-touch surfaces.",
      "Nutley Center retail and restaurants need before-open or after-close service. We confirm grease-adjacent boundaries (no hood cleaning), dumpster access, and sidewalk and entrance expectations so the first customer sees a clean frontage.",
    ],
    buildings: [
      "Corporate and campus offices at ON3",
      "Medical and professional suites along Franklin Avenue",
      "Retail and restaurants in Nutley Center",
      "Kingsland Avenue service businesses",
      "Small industrial and contractor offices",
    ],
    logistics: [
      "ON3 and campus properties require security clearance, COI, and after-hours badging before start.",
      "Franklin Avenue parking is limited; crews use designated vendor spaces.",
      "Campus loading docks require scheduled access; we confirm windows before the first clean.",
      "Professional and medical suites are cleaned after hours or before opening.",
      "Nutley is on the Bloomfield/Belleville route, which keeps multi-site coverage efficient.",
    ],
    competitors: [
      { name: "Jersey Pro Cleaners", base: "28 Valley Rd Ste 149-06, Montclair, NJ 07042", rating: 4.9, reviews: 48, model: "Local commercial cleaner", fit: "Montclair and Nutley area" },
      { name: "One Concept Facility Solutions", base: "109 Belgrove Dr, Kearny, NJ 07032", rating: 4.8, reviews: 21, model: "Supervisor-led facility services", fit: "Kearny and office routes" },
      { name: "Skyline Cleaning Services LLC", base: "143 Rome St, Newark, NJ 07105", rating: 4.2, reviews: 49, model: "Regional commercial cleaner", fit: "Newark and Essex coverage" },
      { name: "united cleaning service LLC", base: "380 Mt Prospect Ave, Newark, NJ 07104", rating: 5.0, reviews: 10, model: "Local commercial cleaner", fit: "Newark and Essex offices" },
    ],
    faqs: [
      { q: "Do you clean offices at ON3?", a: "Yes. ON3 and other campus-style properties require security clearance, COI, loading dock access, and after-hours badging. We complete those requirements before the first clean and schedule around campus rules." },
      { q: "Can you cover Franklin Avenue medical or professional suites?", a: "Yes. Common-area cleaning includes waiting rooms, reception, restrooms, breakrooms, corridors, and floors. We do not handle exam rooms, procedure rooms, or regulated medical waste." },
      { q: "Do you clean Nutley Center retail and restaurants?", a: "Yes. Retail and restaurant work is scheduled before opening or after closing, with glass, floors, restrooms, and trash handled without blocking deliveries or customer flow. Hood and exhaust cleaning is a separate specialty." },
      { q: "What does a Nutley office cost?", a: "Reference bands: a suite under 1,500 sq ft at 2x/week typically runs $350-$700/mo; 1,500-4,000 sq ft at 3x/week runs $700-$1,500/mo. Campus security or medical scope can change the quote." },
      { q: "Are you insured for campus and medical landlords?", a: "Yes. We carry general liability and workers' compensation and provide a COI before start. For ON3 and medical buildings, we complete the landlord's vendor and security requirements first." },
      { q: "How fast can you start in Nutley?", a: "Most Nutley starts are 3-5 business days after a walkthrough and approved scope. Campus or medical onboarding can add 1-3 days." },
    ],
    neighbors: ["commercial-cleaning-bloomfield-nj", "commercial-cleaning-belleville-nj", "office-cleaning-newark-nj"],
    proofCaseIds: ["briard-office"],
    imageAlt: "Commercial cleaning in Nutley, NJ — ON3 corporate office",
  },

  bloomfield: {
    slug: "commercial-cleaning-bloomfield-nj",
    city: "Bloomfield",
    county: "Essex",
    countySlug: "commercial-cleaning-essex-county-nj",
    zips: ["07003"],
    primaryKeyword: "commercial cleaning bloomfield nj",
    secondaryKeywords: ["office cleaning bloomfield nj", "commercial cleaners bloomfield nj", "janitorial services bloomfield nj"],
    metaTitle: "Commercial Cleaning Bloomfield NJ | 07003",
    metaDescription:
      "Commercial cleaning in Bloomfield, NJ 07003 — Bloomfield Center retail, medical offices and Bloomfield Avenue suites. Call (973) 204-2310.",
    h1: "Commercial Cleaning in Bloomfield, NJ",
    directAnswer:
      "Premium Cleaning Services provides commercial cleaning in Bloomfield, NJ 07003 for Bloomfield Center retail, medical offices, and professional suites along Bloomfield Avenue. Evening crews, written scope, and a named supervisor keep historic downtown buildings consistent.",
    intro:
      "Bloomfield Center and Bloomfield Avenue carry the township's retail, restaurant, medical, and professional-office demand. The historic building stock adds narrow staircases, shared entrances, and limited after-hours parking — details that decide whether a nightly route actually works.",
    localTitle: "Commercial cleaning for Bloomfield Center and Bloomfield Avenue",
    localBody: [
      "Downtown retail and restaurants need before-open or after-close service: glass, floors, restrooms, trash, and entrance care. Medical and professional suites need a quieter scope: waiting rooms, restrooms, kitchen and breakroom, and high-touch surfaces. Historic buildings often lack a freight elevator, so we confirm equipment size and stair access before the first visit.",
      "Bloomfield is on the same Essex route as Nutley, Belleville, and East Orange. That lets a Bloomfield client with a second site in Nutley or Belleville keep one supervisor and one invoice without paying a separate trip charge.",
    ],
    buildings: [
      "Bloomfield Center retail and restaurants",
      "Medical and professional suites along Bloomfield Avenue",
      "Historic downtown office buildings",
      "Service businesses near Grove Street station",
      "Small industrial and contractor offices",
    ],
    logistics: [
      "Historic buildings may lack freight elevators; equipment size and stair access are confirmed before start.",
      "Bloomfield Center parking is limited; crews use designated vendor spaces.",
      "Grove Street station traffic peaks before 9 am and after 5 pm.",
      "Restaurants require before-open or after-close access; hood cleaning is not in scope.",
      "Bloomfield is on the Nutley/Belleville/East Orange route, so multi-site clients keep one supervisor.",
    ],
    competitors: [
      { name: "The Royal Group - Royal Cleaning LLC", base: "295 Franklin St, Bloomfield, NJ 07003", rating: 4.7, reviews: 26, model: "Local owner-operated", fit: "Bloomfield-area offices" },
      { name: "Commercial & House Cleaning Glen Ridge", base: "Glen Ridge, NJ", rating: 5.0, reviews: 5, model: "Local owner-operated", fit: "Small commercial" },
      { name: "Skyline Cleaning Services LLC", base: "143 Rome St, Newark, NJ 07105", rating: 4.2, reviews: 49, model: "Regional commercial cleaner", fit: "Newark and Essex coverage" },
      { name: "united cleaning service LLC", base: "380 Mt Prospect Ave, Newark, NJ 07104", rating: 5.0, reviews: 10, model: "Local commercial cleaner", fit: "Newark and Essex offices" },
    ],
    faqs: [
      { q: "Do you clean Bloomfield Center retail?", a: "Yes. Bloomfield Center retail and restaurant work is scheduled before opening or after closing, with glass, floors, restrooms, and trash handled without blocking deliveries or customer flow." },
      { q: "Can you handle historic buildings with narrow staircases?", a: "Yes. We confirm stair access, restroom counts, trash routes, and equipment size before the first clean. Compact equipment is used where freight elevators are unavailable." },
      { q: "Do you clean medical offices on Bloomfield Avenue?", a: "We clean medical office common areas: waiting rooms, reception, restrooms, breakrooms, corridors, and floors. We do not handle exam rooms, procedure rooms, or regulated medical waste." },
      { q: "What does a Bloomfield office cost?", a: "Reference bands: a suite under 1,500 sq ft at 2x/week typically runs $350-$700/mo; 1,500-4,000 sq ft at 3x/week runs $700-$1,500/mo. Historic-building access can affect the quote." },
      { q: "Are you insured for downtown landlords?", a: "Yes. We carry general liability and workers' compensation and provide a COI before start. We also complete building-specific security or vendor onboarding when required." },
      { q: "How fast can you start in Bloomfield?", a: "Most Bloomfield starts are 3-5 business days after a walkthrough and approved scope. If the building requires COI review or after-hours registration, add 1-2 days." },
    ],
    neighbors: ["commercial-cleaning-nutley-nj", "commercial-cleaning-belleville-nj", "commercial-cleaning-east-orange-nj"],
    proofCaseIds: ["promenade", "briard-office"],
    imageAlt: "Commercial cleaning in Bloomfield, NJ — Bloomfield Center retail and office",
  },

  secaucus: {
    slug: "commercial-cleaning-secaucus-nj",
    city: "Secaucus",
    county: "Hudson",
    countySlug: "commercial-cleaning-hudson-county-nj",
    zips: ["07094"],
    primaryKeyword: "commercial cleaning secaucus nj",
    secondaryKeywords: ["office cleaning secaucus nj", "commercial cleaners secaucus nj", "janitorial services secaucus nj"],
    metaTitle: "Commercial Cleaning Secaucus NJ | 07094",
    metaDescription:
      "Commercial cleaning in Secaucus, NJ 07094 — Harmon Meadow offices, Mill Creek retail and Meadowlands hospitality. Call (973) 204-2310.",
    h1: "Commercial Cleaning in Secaucus, NJ",
    directAnswer:
      "Premium Cleaning Services provides commercial cleaning in Secaucus, NJ 07094 for Harmon Meadow corporate offices, Mill Creek retail, and Meadowlands hospitality spaces. Nightly and 3x/week crews handle restrooms, floors, glass, and trash with COI support.",
    intro:
      "Secaucus combines Harmon Meadow corporate offices, Mill Creek retail, Meadowlands hospitality, and logistics space around Secaucus Junction. Building management here expects COIs, dock scheduling, and hotel-grade discretion.",
    localTitle: "Commercial cleaning for Harmon Meadow, Mill Creek, and Meadowlands buildings",
    localBody: [
      "Corporate offices in Harmon Meadow need nightly or 3x/week restroom, kitchen, conference, and common-area care. Retail at Mill Creek needs before-open glass, floors, restrooms, and trash. Hotels and hospitality spaces need back-of-house and public-area support timed around check-in, check-out, and events.",
      "Secaucus Junction traffic and Meadowlands event days can compress the access window. We confirm loading dock reservations, freight elevator availability, and COI requirements before start, then lock the crew to the building's actual window rather than a generic after-hours slot.",
    ],
    buildings: [
      "Corporate offices in Harmon Meadow",
      "Retail and restaurants at Mill Creek",
      "Hotels and hospitality spaces in the Meadowlands",
      "Logistics and distribution offices near Secaucus Junction",
      "Showrooms and service businesses along Route 3",
    ],
    logistics: [
      "Harmon Meadow and Mill Creek require vendor registration and a COI before start.",
      "Secaucus Junction traffic and Meadowlands events compress evening access; windows are confirmed in advance.",
      "Hotels require back-of-house discretion and scheduling around check-in and check-out.",
      "Loading docks and freight elevators require reservations; crews do not block active docks.",
      "Secaucus is on the Jersey City/Harrison route, so multi-site clients keep one supervisor.",
    ],
    competitors: [
      { name: "Green Apple Commercial Cleaning", base: "101 Plaza Center #350, Secaucus, NJ 07094", rating: 5.0, reviews: 10, model: "Local commercial cleaner", fit: "Secaucus and Meadowlands" },
      { name: "Shiny Cleaning Agency", base: "35 Journal Square Plaza Ste 103, Jersey City, NJ 07306", rating: 4.9, reviews: 30, model: "Local commercial cleaner", fit: "Jersey City and Journal Square" },
      { name: "City Wide Facility Solutions - Liberty Harbor", base: "78 John Miller Way, Kearny, NJ 07032", rating: 5.0, reviews: 35, model: "Franchise/system", fit: "Multi-service facility management" },
      { name: "Skyline Cleaning Services LLC", base: "143 Rome St, Newark, NJ 07105", rating: 4.2, reviews: 49, model: "Regional commercial cleaner", fit: "Newark and Essex coverage" },
    ],
    faqs: [
      { q: "Do you clean Harmon Meadow corporate offices?", a: "Yes. Harmon Meadow offices get nightly or 3x/week restroom, kitchen, conference, and common-area care. We confirm building security, loading, and COI requirements before the first visit." },
      { q: "Can you cover Mill Creek retail?", a: "Yes. Retail work is scheduled before opening or after closing, with glass, floors, restrooms, and trash handled without blocking deliveries or customer flow." },
      { q: "Do you clean hotels and hospitality spaces?", a: "Yes. We support back-of-house and public-area cleaning timed around check-in, check-out, and events. Our hotel experience includes Marriott-brand housekeeping and public-area standards." },
      { q: "How do you handle Secaucus Junction and event-day traffic?", a: "We confirm loading dock reservations, freight elevator availability, and event schedules before start. Crews are locked to the building's actual access window, not a generic after-hours slot." },
      { q: "Are you insured for hotel and corporate landlords?", a: "Yes. We carry general liability and workers' compensation and provide a COI before start. For hotels and managed office buildings, we complete the property's vendor requirements first." },
      { q: "How fast can you quote a Secaucus office?", a: "Send the address, square footage, restroom count, and frequency. We can usually return a written range within one business day and schedule a walkthrough within 48 hours." },
    ],
    neighbors: ["office-cleaning-jersey-city-nj", "commercial-cleaning-kearny-nj", "commercial-cleaning-harrison-nj"],
    proofCaseIds: ["briard-office", "promenade"],
    imageAlt: "Commercial cleaning in Secaucus, NJ — Harmon Meadow corporate office",
  },
};
```

### 1.2 Create `src/components/IronRingCityPage.tsx`

Use the same `Layout`, `Seo`, `QuoteCTA`, `ProofBand`, `FaqAccordion`, `PricingTable`, `RatingBadge` already in the project. Do not redesign. Render in this exact order:

1. `<h1>{city.h1}</h1>`
2. `<p className="direct-answer">{city.directAnswer}</p>`
3. `<QuoteCTA />`
4. `<p>{city.intro}</p>`
5. `<h2>{city.localTitle}</h2>` + `city.localBody` paragraphs
6. `<h2>Buildings we clean in {city.city}</h2>` + `city.buildings` list
7. `<h2>What's included in every {city.city} scope</h2>` + `INCLUDED` list
8. `<h2>Access, scheduling, and local logistics</h2>` + `city.logistics` list
9. `<h2>What commercial cleaning costs in {city.city}</h2>` + `<PricingTable rows={PRICING[city.county]} footnote="Reference bands; final quote after walkthrough." />`
10. `<h2>{city.city} cleaning providers compared</h2>` + semantic competitor table + footnote `"Public Google Maps data, October 2026. Not an endorsement; verify current ratings before signing."`
11. `<ProofBand caseIds={city.proofCaseIds} />`
12. `<h2>Frequently asked questions</h2>` + `<FaqAccordion faqs={city.faqs} />` — each item must render `id={`faq-${i + 1}`}`.
13. NAP block: name, 107 Vesey St, Newark, NJ 07105, `tel:+19732042310`, `office@premiumccs.com`, "Serving {city.city} and the Iron Ring."
14. `<IronRingLinks current={city.slug} neighbors={city.neighbors} countySlug={city.countySlug} />`
15. `<QuoteCTA />`

Competitor table columns: `Provider | Base | Google rating | Reviews | Model | Best fit`. Use `<table>`, `<caption>`, `<thead>`, `<th scope="col">`. Wrap in a horizontally scrollable container on mobile.

JSON-LD (static, in served HTML — same injection pattern as existing pages):
- `Service` with `name`, `serviceType: "Commercial cleaning"`, `areaServed` city, `provider: { "@id": "https://premiumcleaningnj.com/#business" }`, `url`.
- `FAQPage` with every Q&A verbatim.
- `BreadcrumbList`: Home > Commercial Cleaning NJ > {County} County > {City}.
- `WebPage` with `speakable: { "@type": "SpeakableSpecification", cssSelector: [".direct-answer", "#faq-1", "#faq-2"] }`.

### 1.3 Add routes

Add these 10 routes using the existing router pattern (same trailing slash behavior as `/office-cleaning-newark-nj/`). Do not create a second router.

```
/commercial-cleaning-harrison-nj/
/commercial-cleaning-kearny-nj/
/commercial-cleaning-east-newark-nj/
/commercial-cleaning-belleville-nj/
/commercial-cleaning-irvington-nj/
/commercial-cleaning-hillside-nj/
/commercial-cleaning-east-orange-nj/
/commercial-cleaning-nutley-nj/
/commercial-cleaning-bloomfield-nj/
/commercial-cleaning-secaucus-nj/
```

### 1.4 Pilot publish (3 pages)

Build only Harrison, Kearny, and East Newark first. Publish. Then report:
- file paths created/edited
- route paths
- `curl` proof that each page returns 200 and contains `FAQPage` + `Service` without JS
- word count per page (must be >= 1,100)
- screenshot/description of the mobile competitor table

Wait for OK before Step 2.

---

## STEP 2 — NEXT 4 PAGES

Reuse the same component and data. Add routes for Belleville, Irvington, Hillside, East Orange. Do not touch the 3 pilot pages. Report the same 5-item proof. Wait for OK.

---

## STEP 3 — LAST 3 PAGES

Add routes for Nutley, Bloomfield, Secaucus. Report the same 5-item proof. Wait for OK.

---

## STEP 4 — PATCH NEWARK + JERSEY CITY (existing pages only)

Edit only the files that render these two URLs. Do not regenerate the pages.

### 4.1 Newark — `/office-cleaning-newark-nj/`

Add after the existing "Premium vs Other NJ Bidders in Newark/Essex" section:

**H2: Newark cleaning providers compared**

Intro: "Newark has no shortage of commercial cleaners. The table below compares the providers that appear most often in our 2026 local scans, with their public Google review counts and base locations. It is a starting point for your own diligence, not an endorsement."

| Provider | Base | Rating | Reviews | Model | Best fit |
|---|---|---:|---:|---|---|
| Skyline Cleaning Services LLC | 143 Rome St, Newark, 07105 | 4.2 | 49 | Regional commercial cleaner | Newark and Essex coverage |
| Alexa's Cleaning | 41 Kossuth St, Newark, 07105 | 5.0 | 271 | Local commercial cleaner | Newark and Ironbound |
| T&S Cleaning Pros LLC | One Gateway Center, Newark, 07102 | 4.8 | 107 | Regional commercial cleaner | Newark corporate offices |
| Newark Cleaning Services LLC | 191 Bloomfield Ave, Newark, 07104 | 4.6 | 29 | Local commercial cleaner | Newark and Essex offices |
| united cleaning service LLC | 380 Mt Prospect Ave, Newark, 07104 | 5.0 | 10 | Local commercial cleaner | Newark and Essex offices |
| Liz Cleaning | 855 Clinton Ave, Newark, 07108 | 5.0 | 7 | Local owner-operated | Newark-area offices |
| N&R Divine Cleaning Services LLC | 211 Warren St, Newark, 07103 | 5.0 | 6 | Local owner-operated | Small offices |

Footnote: "Public Google Maps data, October 2026. Not an endorsement; verify current ratings before signing."

**H2: Newark ZIPs and neighborhoods we cover**

Copy: "We clean offices, retail, and commercial common areas across Downtown (07102), the Ironbound (07105), North Newark (07104), the West Ward (07106, 07108), the South Ward (07112, 07114), and the Raymond Boulevard/Route 21 corridor. If your building is near Newark Penn Station, the Ironbound, or the waterfront, it is inside our nightly route."

Add 2 FAQs to the existing FAQ accordion:
- "Do you clean offices in the Ironbound?" — "Yes. We clean offices, restaurants, and retail support spaces in the Ironbound (07105), including buildings along Raymond Boulevard, Ferry Street, and Market Street. Restaurant front-of-house and office areas are in scope; hood and exhaust cleaning is a separate specialty."
- "Can you cover a Newark building and a Harrison or Kearny site on the same contract?" — "Yes. Newark, Harrison, Kearny, and East Newark are on the same nightly route. One supervisor, one scope system, one invoice."

Add links to: `/commercial-cleaning-harrison-nj/`, `/commercial-cleaning-kearny-nj/`, `/commercial-cleaning-east-newark-nj/`, `/commercial-cleaning-belleville-nj/`, `/commercial-cleaning-irvington-nj/`.

ProofBand: `caseIds={["briard-office"]}`.

### 4.2 Jersey City — `/office-cleaning-jersey-city-nj/`

Add after the existing "Why Local NJ Dispatch Helps Hudson Buildings" section:

**H2: Jersey City cleaning providers compared**

Intro: "Jersey City's commercial cleaning market includes local owner-operators, regional firms, and Brooklyn-based crews that cross the river. The table below compares providers that appear in our 2026 local scans, with public Google review counts and base locations."

| Provider | Base | Rating | Reviews | Model | Best fit |
|---|---|---:|---:|---|---|
| Shiny Cleaning Agency | 35 Journal Square Plaza Ste 103, Jersey City, 07306 | 4.9 | 30 | Local commercial cleaner | Jersey City and Journal Square |
| Hudson Cleaners NJ | 98 Mallory Ave, Jersey City, 07304 | 5.0 | 2 | Local owner-operated | Jersey City |
| Totally Cleaning Services | 224 John St, Harrison, 07029 | 5.0 | 133 | Owner-operated local | Harrison-based; high review volume |
| Park Slope Cleaning | Brooklyn, NY | 4.8 | 43 | Brooklyn-based commercial cleaner | NYC and Jersey City crossover |
| Skyline Cleaning Services LLC | 143 Rome St, Newark, 07105 | 4.2 | 49 | Regional commercial cleaner | Newark and Essex coverage |

Footnote: "Public Google Maps data, October 2026. Not an endorsement; verify current ratings before signing."

**H2: Jersey City ZIPs and neighborhoods we cover**

Copy: "We cover offices and commercial common areas in Downtown and Exchange Place (07302), Journal Square (07306), the Heights (07307), Greenville (07305), the West Side (07304), and the waterfront (07310, 07311). High-rise buildings require COI, freight elevator reservations, and dock scheduling; we handle all three before the first clean."

Add 2 FAQs:
- "Do you handle freight elevator and COI requirements in Jersey City high-rises?" — "Yes. We confirm COI, freight elevator reservations, loading dock windows, and building security before the first clean. Nightly office and retail routes are scheduled around those constraints."
- "Can you clean a Jersey City office and a Harrison or Secaucus site on one contract?" — "Yes. Jersey City, Secaucus, Harrison, and Kearny are on the same Hudson route. One supervisor and one invoice cover multiple sites."

Add links to: `/commercial-cleaning-harrison-nj/`, `/commercial-cleaning-kearny-nj/`, `/commercial-cleaning-secaucus-nj/`.

ProofBand: `caseIds={["briard-office"]}`.

---

## STEP 5 — COUNTY HUBS + RING LINKS

### 5.1 Create `src/components/IronRingLinks.tsx`

A reusable block with:
- H2: "Iron Ring cities we serve"
- One sentence: "These are the 1-5 mile cities around our Newark base, each with its own local page, ZIP coverage, building types, access notes, and current provider comparison."
- Links to all 10 new pages + the 2 existing city pages. Highlight the current page with `aria-current="page"` and no link.

Do not modify the global footer. Render this block on each new city page and on the two expanded pages.

### 5.2 Patch the county hubs

- `/commercial-cleaning-essex-county-nj/`: add H2 "Iron Ring cities we serve in Essex County" + links to Newark, Belleville, Irvington, East Orange, Nutley, Bloomfield.
- `/commercial-cleaning-hudson-county-nj/`: add H2 "Iron Ring cities we serve in Hudson County" + links to Harrison, Kearny, East Newark, Secaucus, Jersey City.
- `/commercial-cleaning-union-county-nj/`: add H2 "Iron Ring cities we serve in Union County" + link to Hillside.
- `/commercial-cleaning-services-nj/`: add a "Local coverage" block with all 12 links.
- `/office-cleaning-new-jersey/`: add a "Local coverage" block with all 12 links.

Each county block gets one sentence: "Each city page includes local ZIPs, building types, access notes, and a current provider comparison based on our October 2026 Google Maps scan."

### 5.3 Add internal links from high-authority pages

Add a small "Local coverage" link block (not a redesign) to:
- `/office-cleaning/`
- `/janitorial-services-nj/`

Links: all 12 city pages.

---

## STEP 6 — QA GATE (report only, no fixes without approval)

Report a table with one row per page:

| Check | Pass/Fail | Evidence |
|---|---|---|
| HTTP 200 | | |
| One H1, exact copy | | |
| Title <= 60 chars | | |
| Meta 120-155 chars | | |
| Word count >= 1,100 | | |
| Direct answer is first paragraph after H1 | | |
| 6 FAQs + FAQPage verbatim | | |
| Service + BreadcrumbList + WebPage/Speakable | | |
| Static JSON-LD visible in `curl` (no JS) | | |
| Competitor table has 4+ rows + footnote | | |
| NAP exact | | |
| 3 neighbor links + county link + core links | | |
| No 404 on internal links | | |
| No duplicate local paragraph across pages | | |
| No "best", "#1", "guaranteed", or invented review | | |
| Mobile table scrolls horizontally | | |
| CTA above and below | | |

Stop after the report. Fix only items I approve, one by one.

---

## OPERATOR CHECKLIST (not for Lovable)

- Publish one page per day, in this order: Harrison, Kearny, East Newark, Belleville, Irvington, Hillside, East Orange, Nutley, Bloomfield, Secaucus.
- After each publish: request indexing in Google Search Console for the exact URL.
- After each publish: create one GBP post linking to the page with `?utm_source=google&utm_medium=gbp&utm_campaign=iron_ring_{city}`.
- Add the page to the GBP Q&A bank with one local question.
- Re-scan 9x9 at 2 miles on day 14 and day 30; compare against `campanhas/baseline-scans-local-seo-a5.md`.
- Review target: +20 in month 1 (43 -> 63+), responses under 24 hours.
- Do not publish a page if the client cannot confirm the ZIPs or building access. Fix the data first.

---

## HARD BANS

- No invented reviews, ratings, clients, certifications, prices, or addresses.
- No "best in {city}" or "#1" claims.
- No competitor disparagement.
- No fake GBP location or doorway page.
- No PBN, link farm, or paid guest post.
- No lorem, placeholder, "coming soon", or empty image alt.
- No emojis in UI.
- No global redesign; reuse existing components.
