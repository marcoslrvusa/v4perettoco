# Guia de Implantação — Conteúdo + Schema Metal Indianápolis

## O espírito da coisa

SEO técnico é necessário, mas ninguém quer ler site de fundição que parece escrito por robô. O comprador industrial — engenheiro, projetista, dono de oficina — quer sentir que está falando com uma fábrica de verdade, com gente que entende de metal, não com uma página genérica.

Cada texto aqui foi escrito para soar como um profissional da área explicando o assunto para outro profissional. As palavras-chave estão lá, o schema markup está lá, mas a prioridade é **parecer humano**. Se na hora de colar você sentir que precisa adaptar o tom pra ficar mais com a cara da Metal Indianápolis, adapte. Isso é até bem-vindo.

---

## Como aplicar

1. **Edite a página no Elementor**
2. **Clique em cada widget de texto** e cole o conteúdo novo
3. **Adicione um widget HTML** no final da página e cole o schema correspondente
4. **Atualize os H1** onde indicado

Cada página leva uns 7 minutos. Não precisa fazer tudo de uma vez.

---

## 1. HOMEPAGE

### H1 — o título principal da página

Troque o heading que está no hero por este:

> Peças Técnicas em Ferro Fundido Nodular e Cinzento com Usinagem CNC de Precisão

### Parágrafo de abertura

Substitua o texto "Há mais de seis décadas..." por este:

> Há mais de seis décadas, a **Metal Indianápolis** fornece peças técnicas em **ferro fundido nodular e cinzento** para a indústria brasileira, com infraestrutura completa de [fundição própria e usinagem CNC integradas](/solucoes/). São mais de **3.500 toneladas fundidas por ano**, centenas de milhares de anéis de segmento produzidos e **7 segmentos industriais ativos** — automotivo, agrícola, ferroviário, construção civil, máquinas e equipamentos, vidreiro e serviços sob medida. Tudo isso com **certificação ISO 9001** e laboratório metalúrgico próprio equipado com espectrômetro, microscópio metalográfico e durômetro.

> **Por que esse texto funciona:** Ele diz números reais (3.500 toneladas, 7 segmentos), mostra serviço (fundição + usinagem próprias) e fala a língua de quem entende do setor — sem encher de jargão vazio.

### Rótulos dos contadores

Ajuste os textos que aparecem embaixo dos números grandes:

- "de experiência industrial" → **de experiência industrial — atuação contínua desde 1966**
- "fundidas por ano" → **toneladas de ferro fundido processadas anualmente**
- "anéis produzidos por ano" → **anéis de segmento fabricados por ano com usinagem CNC**
- "indústrias ativas" → **segmentos industriais ativos atendidos sob especificação**

### Cards de produtos (5 seções)

**Anéis de Segmento:**

> Os **anéis de segmento** — também conhecidos como anéis de pistão — são componentes circulares e flexíveis fabricados em **ferro fundido nodular (GGG50)** ou **cinzento (GG25)**, instalados nas canaletas do pistão para vedação da câmara de combustão, controle do consumo de óleo e transferência de calor. A Metal Indianápolis produz [anéis de segmento sob especificação](/solucoes/) com usinagem CNC de precisão, assegurando o perfil geométrico correto e a tensão radial adequada para cada aplicação.

**Peças fundidas e usinadas:**

> Componentes em ferro fundido nodular e cinzento produzidos e usinados na própria empresa, da [fundição ao acabamento CNC](/solucoes/). Incluem buchas, flanges, carcaças, suportes e polias — prontos para montagem, com rastreabilidade completa e ISO 9001.

**Usinagem de precisão:**

> Acabamento técnico de precisão em **centros de usinagem CNC com 3 e 4 eixos** e tornos de comando numérico, executando torneamento, fresamento, furação, roscamento e mandrilamento dentro de tolerâncias dimensionais apertadas com controle por MMC.

**Componentes industriais:**

> Peças técnicas em ferro fundido para máquinas e equipamentos industriais: polias, engrenagens, mancais, roletes, suportes estruturais e componentes para prensas, britadores e sistemas de movimentação, com especificação de ferro nodular ou cinzento conforme a aplicação.

**Produção sob especificação:**

> [Fabricação sob demanda](/contato/) a partir de desenho técnico (DWG, PDF, STEP, IGES) ou amostra física, com engenharia reversa e assessoria técnica na seleção do material ideal. Lotes de 50 a 10.000 peças com prazo de 15 a 45 dias úteis.

### Seção "Processo produtivo"

> 	Da análise técnica do desenho ou amostra à entrega final, cada etapa do **processo de fundição e usinagem CNC** é monitorada com controle metalúrgico rigoroso — da composição química no forno de indução à inspeção dimensional em MMC — garantindo precisão, rastreabilidade e qualidade ISO 9001 em cada peça.

### Seção "Qualidade"

> A **Metal Indianápolis** opera com **Sistema de Gestão da Qualidade certificado ISO 9001** e realiza controle rigoroso em todas as etapas. O laboratório metalúrgico próprio é equipado com espectrômetro para análise da composição química, microscópio metalográfico para avaliação microestrutural e durômetro para medição de dureza — assegurando a conformidade de cada peça, desde a [fundição de ferros nodular e cinzento](/solucoes/) até o acabamento CNC final.

### Seção "Solicite análise técnica"

> Envie seu desenho técnico (DWG, PDF, STEP ou IGES) e receba em até **48 horas úteis** uma **análise técnica gratuita** com proposta personalizada para produção de peças em ferro fundido. Nossa engenharia avalia a viabilidade metalúrgica, indica a liga ideal (GGG40, GGG50, GG20 ou GG25) e define o processo de usinagem mais adequado. [Solicite sua cotação agora](/contato/) — sem compromisso.

### Schema (adicione um widget HTML no final da página e cole tudo)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Metal Indianápolis",
  "url": "https://preview.indianapolis.com.br",
  "logo": "https://preview.indianapolis.com.br/wp-content/uploads/2026/05/LOGOTIPO-HORIZONTAL-1-1-scaled.webp",
  "description": "Fabricante de peças técnicas em ferro fundido nodular e cinzento com fundição e usinagem CNC próprias. ISO 9001. Mais de 60 anos.",
  "foundingDate": "1966",
  "sameAs": ["https://www.instagram.com/metalindianapolis.oficial/", "https://www.linkedin.com/company/metalurgica-indianapolis/"]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Metal Indianápolis",
  "address": {"@type":"PostalAddress","streetAddress":"Rua do Zinco, 205/225","addressLocality":"Itaquaquecetuba","addressRegion":"SP","postalCode":"08586-240","addressCountry":"BR"},
  "telephone": "(11) 4649-7722",
  "email": "vendas@indianapolis.com.br",
  "priceRange": "$$",
  "openingHoursSpecification": [{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"06:30","closes":"17:00"}]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Produtos em Ferro Fundido",
  "itemListElement": [
    {"@type":"ListItem","position":1,"name":"Anéis de Segmento"},
    {"@type":"ListItem","position":2,"name":"Peças Fundidas e Usinadas"},
    {"@type":"ListItem","position":3,"name":"Usinagem de Precisão CNC"},
    {"@type":"ListItem","position":4,"name":"Componentes Industriais"},
    {"@type":"ListItem","position":5,"name":"Produção sob Especificação"}
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Processo de Fabricação de Peças em Ferro Fundido",
  "step": [
    {"@type":"HowToStep","position":1,"name":"Projeto e Análise Técnica","text":"Análise do desenho técnico ou amostra para definição do tipo de ferro fundido e tolerâncias."},
    {"@type":"HowToStep","position":2,"name":"Fundição com Controle Metalúrgico","text":"Preparação do ferro em forno de indução com composição química controlada por espectrômetro."},
    {"@type":"HowToStep","position":3,"name":"Usinagem CNC de Precisão","text":"Acabamento em centros de usinagem CNC com 3 e 4 eixos."},
    {"@type":"HowToStep","position":4,"name":"Controle de Qualidade","text":"Inspeção dimensional e ensaios metalúrgicos com registros ISO 9001."},
    {"@type":"HowToStep","position":5,"name":"Entrega","text":"Peças prontas com certificados de qualidade e rastreabilidade."}
  ]
}
</script>
```

---

## 2. EMPRESA

### H1

Troque o heading do hero por este:

> Conheça a Metal Indianápolis — Fundição e Usinagem CNC desde 1966

### Parágrafo do hero

> A **Metal Indianápolis** é referência brasileira na fabricação de peças técnicas em **ferro fundido nodular e cinzento**, com **mais de 60 anos de experiência** em fundição e usinagem CNC. Localizada em Itaquaquecetuba (SP), atende indústrias dos segmentos automotivo, agrícola, ferroviário, construção civil e bens de capital, transformando [desenhos técnicos e amostras em componentes prontos](/solucoes/) sob especificação, com **certificação ISO 9001** e controle metalúrgico em laboratório próprio equipado com espectrômetro, microscópio metalográfico e durômetro.

### Nossa História

> Fundada em **1966**, a Metal Indianápolis acumula mais de sessenta anos de experiência na fabricação de componentes técnicos em ferro fundido para a indústria brasileira. A empresa desenvolveu ao longo das décadas uma infraestrutura industrial verticalizada: o processo começa na [fundição própria com fornos de indução e controle metalúrgico por espectrômetro](/solucoes/), passa pelo tratamento térmico quando necessário e chega ao acabamento em centros de usinagem CNC com 3 e 4 eixos. Esse modelo integrado elimina intermediários, reduz lead times e garante que cada peça entregue — seja um anel de segmento, um componente automotivo ou uma peça para máquinas agrícolas — saia do mesmo chão de fábrica com a qualidade que a **ISO 9001** exige e com rastreabilidade completa de lote.

### Qualidade e Controle

> A Metal Indianápolis opera com **Sistema de Gestão da Qualidade certificado ISO 9001**, com controle rigoroso em todas as etapas. O **laboratório metalúrgico próprio** é equipado com **espectrômetro** para análise da composição química das ligas, **microscópio metalográfico** para avaliação da microestrutura do ferro fundido e **durômetro** para medição de dureza superficial e profunda. A esses ensaios soma-se o controle dimensional rigoroso — incluindo **máquina de medição por coordenadas (MMC)** para peças com tolerâncias apertadas. Cada lote produzido é integralmente rastreado, da matéria-prima ao produto final.

### Certificados

> A Metal Indianápolis mantém seu Sistema de Gestão da Qualidade certificado pela **ISO 9001**, com políticas e procedimentos documentados que garantem a conformidade de cada peça produzida — desde a [fundição e usinagem CNC](/solucoes/) até a entrega final. Clique nos certificados abaixo para visualizar os documentos oficiais.

### Schema (widget HTML no final da página)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Metal Indianápolis",
  "url": "https://preview.indianapolis.com.br",
  "logo": "https://preview.indianapolis.com.br/wp-content/uploads/2026/05/LOGOTIPO-HORIZONTAL-1-1-scaled.webp",
  "description": "Fabricante de peças técnicas em ferro fundido nodular e cinzento com fundição e usinagem CNC próprias. ISO 9001. Mais de 60 anos.",
  "foundingDate": "1966",
  "sameAs": ["https://www.instagram.com/metalindianapolis.oficial/", "https://www.linkedin.com/company/metalurgica-indianapolis/"]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Metal Indianápolis",
  "address": {"@type":"PostalAddress","streetAddress":"Rua do Zinco, 205/225","addressLocality":"Itaquaquecetuba","addressRegion":"SP","postalCode":"08586-240","addressCountry":"BR"},
  "telephone": "(11) 4649-7722",
  "email": "vendas@indianapolis.com.br",
  "priceRange": "$$",
  "openingHoursSpecification": [{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"06:30","closes":"17:00"}]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type":"Question","name":"Há quantos anos a Metal Indianápolis atua no mercado?","acceptedAnswer":{"@type":"Answer","text":"A Metal Indianápolis foi fundada em 1966 e acumula mais de 60 anos de experiência na fabricação de peças técnicas em ferro fundido nodular e cinzento para a indústria brasileira."}},
    {"@type":"Question","name":"A Metal Indianápolis possui certificação ISO 9001?","acceptedAnswer":{"@type":"Answer","text":"Sim. A Metal Indianápolis opera com Sistema de Gestão da Qualidade certificado ISO 9001, com laboratório metalúrgico próprio equipado com espectrômetro, microscópio metalográfico e durômetro."}},
    {"@type":"Question","name":"Que tipos de peças em ferro fundido a Metal Indianápolis fabrica?","acceptedAnswer":{"@type":"Answer","text":"A Metal Indianápolis fabrica peças técnicas em ferro fundido nodular e cinzento, incluindo anéis de segmento, componentes automotivos, peças para máquinas agrícolas, componentes ferroviários e peças industriais sob especificação com usinagem CNC de precisão."}}
  ]
}
</script>
```

---

## 3. PRODUTOS

### H1

Troque o heading "Produtos" por este H1:

> Catálogo de Peças em Ferro Fundido — Componentes Industriais

### Parágrafo do hero

> Catálogo completo de peças técnicas em **ferro fundido nodular e cinzento** fabricadas sob especificação para aplicações industriais nos segmentos automotivo, construção civil, máquinas e equipamentos. Cada componente é produzido em nosso parque fabril integrado — da [fundição à usinagem CNC](/solucoes/) — com controle metalúrgico em laboratório próprio (espectrômetro, microscópio, durômetro) e **certificação ISO 9001**. Não comercializamos produtos padronizados: toda a produção é [sob demanda e sob medida](/contato/) para a necessidade do seu projeto.

### Parágrafo do catálogo

> Conheça abaixo as categorias de peças técnicas em ferro fundido que produzimos para diferentes segmentos industriais. Todas as peças são fabricadas conforme desenho técnico ou amostra fornecida pelo cliente, em ligas de **ferro nodular (GGG40, GGG50)** ou **cinzento (GG20, GG25)**, com possibilidade de usinagem CNC de precisão e controle dimensional rigoroso. Trabalhamos sob demanda — cada peça é única e fabricada sob medida para a aplicação do seu projeto.

### Schema (widget HTML no final da página)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Catálogo de Peças em Ferro Fundido — Componentes Industriais | Metal Indianápolis",
  "description": "Catálogo completo de peças técnicas em ferro fundido nodular e cinzento para aplicações industriais."
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Categorias de Peças em Ferro Fundido",
  "itemListElement": [
    {"@type":"ListItem","position":1,"name":"Construção Civil"},
    {"@type":"ListItem","position":2,"name":"Anéis de Segmento"},
    {"@type":"ListItem","position":3,"name":"Automotivo"},
    {"@type":"ListItem","position":4,"name":"Máquinas e Equipamentos"}
  ]
}
</script>
```

---

## 4. CONTATO

### H1

Troque "Contato" por este H1:

> Cotação de Peças Técnicas em Ferro Fundido — Contato

### Parágrafo do hero

> Solicite um **orçamento sem compromisso** para sua próxima produção de peças em **ferro fundido nodular ou cinzento**. Na **Metal Indianápolis**, cada projeto passa por análise técnica detalhada — garantimos que a peça especificada atenda exatamente às suas necessidades mecânicas e dimensionais. Com mais de **60 anos de experiência**, fundição e usinagem verticalizadas em parque fabril próprio e **certificação ISO 9001** com laboratório metalúrgico equipado com espectrômetro e durômetro, entregamos peças sob desenho técnico para os segmentos automotivo, agrícola, ferroviário, construção civil e bens de capital. [Fale conosco pelo WhatsApp](https://wa.me/5511972048044) ou preencha o formulário abaixo.

### Parágrafo do formulário

> Envie seu desenho técnico em formato **DWG, PDF, STEP ou IGES** e receba em **até 48 horas úteis** uma análise técnica gratuita com proposta detalhada. Nossa engenharia avalia a viabilidade metalúrgica — indicando o tipo ideal de **ferro fundido (nodular GGG40/GGG50 ou cinzento GG20/GG25)** — e define o processo de [usinagem CNC](/solucoes/) mais adequado à sua peça. Do recebimento do desenho à entrega final, você acompanha um processo ágil e transparente, respaldado por **60 anos de experiência em fundição de precisão**.

### Informações de contato

Formate cada uma com o HTML abaixo:

**Telefone:** `<strong>(11) 4649-7722</strong> — Linha direta com o setor comercial (6h30 às 17h)`

**WhatsApp:** `<strong>(11) 97204-8044</strong> — <a href="https://wa.me/5511972048044">Atendimento rápido via WhatsApp</a> para envio de desenhos e propostas`

**E-mail:** `<strong>vendas@indianapolis.com.br</strong> — Envie sua especificação técnica para cotação`

**Endereço:** `<strong>Rua do Zinco, 205/225, Itaquaquecetuba - SP, CEP 08586-240</strong><br>Fácil acesso pelas rodovias Ayrton Senna, Dutra e Rodoanel`

### Schema (widget HTML no final da página)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Manufacturing",
  "name": "Metal Indianápolis",
  "description": "Fundição e usinagem de peças técnicas em ferro fundido sob especificação. ISO 9001, laboratório próprio.",
  "url": "https://preview.indianapolis.com.br",
  "telephone": "+551146497722",
  "email": "vendas@indianapolis.com.br",
  "address": {"@type":"PostalAddress","streetAddress":"Rua do Zinco, 205/225","addressLocality":"Itaquaquecetuba","addressRegion":"SP","postalCode":"08586-240","addressCountry":"BR"},
  "sameAs": ["https://wa.me/5511972048044", "https://www.linkedin.com/company/metalurgica-indianapolis/"]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ContactPoint",
  "telephone": "+551146497722",
  "contactType": "sales",
  "email": "vendas@indianapolis.com.br"
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Contato | Metal Indianápolis — Cotação de Peças em Ferro Fundido",
  "potentialAction": {
    "@type": "ContactAction",
    "target": {"@type":"EntryPoint","urlTemplate":"https://wa.me/5511972048044"}
  }
}
</script>
```

---

## 5. BLOG POSTS

Os 12 artigos de blog já estão completos:
- Textos EEAT com 1500–2500 palavras
- Imagens gratuitas (Pixabay / Unsplash) inseridas no layout
- Schema Article + FAQPage embutido no JSON

Para publicar, importe o JSON direto no Elementor (template > import template) ou crie o post manualmente e cole o texto extraído do arquivo.

---

## 6. SOLUÇÕES

O arquivo `02-solucoes-page.json` já existe com 13 containers e 4 imagens. Se quiser adicionar schema markup, é rápido — é só pedir.

---

## Checklist rápido

| Página    | H1     | Textos    | Schema    |
| --------- | ------ | --------- | --------- |
| Homepage  | ✅      | 12 textos | 4 schemas |
| Empresa   | ✅      | 5 textos  | 3 schemas |
| Produtos  | ✅      | 2 textos  | 2 schemas |
| Contato   | ✅      | 8 textos  | 3 schemas |
| Blog (12) | já tem | já tem    | já tem    |

---

## Uma dica antes de publicar

O Google valoriza conteúdo original, mas o que realmente faz diferença é o usuário ler e pensar "essa empresa sabe do que está falando". Os textos foram escritos pensando nisso — engenheiro conversando com engenheiro, não blog genérico de SEO. Se na hora de colar você sentir vontade de trocar uma palavra ou um link, troque. O importante é que soe como a Metal Indianápolis de verdade.
