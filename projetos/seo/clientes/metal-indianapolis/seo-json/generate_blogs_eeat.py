#!/usr/bin/env python3
"""Generate EEAT-compliant Elementor JSON files for blog articles 13 to 58."""

import json
import os
import re
import uuid
from datetime import datetime

DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(DIR, "Blog")
POSTS_FILE = "/tmp/all_posts.json"

HERO_IMG = "https://preview.indianapolis.com.br/wp-content/uploads/2026/05/fundicao-metal-indianapolis-hero.webp"
CONTATO_URL = "https://preview.indianapolis.com.br/contato/"
SITE_URL = "https://preview.indianapolis.com.br"
AUTHOR_NAME = "Vanderlei Rampasso"
AUTHOR_JOB = "Especialista em Fundição e Usinagem"
PUBLISHER = "Metal Indianápolis"
FOUNDING_YEAR = 1966


def make_id():
    return uuid.uuid4().hex[:10]


def make_widget(widget_type, settings):
    return {
        "id": make_id(),
        "settings": settings,
        "elements": [],
        "isInner": False,
        "widgetType": widget_type,
        "elType": "widget"
    }


def make_inner_container(widgets):
    return {
        "id": make_id(),
        "settings": {"content_width": "full"},
        "elements": widgets,
        "elType": "container",
        "isInner": True
    }


def make_outer_container(settings, inner_widgets):
    return {
        "id": make_id(),
        "settings": settings,
        "elements": [make_inner_container(inner_widgets)],
        "elType": "container",
        "isInner": False
    }


def get_hero_settings():
    return {
        "flex_direction": "column",
        "background_background": "classic",
        "background_image": {"url": HERO_IMG, "id": 356, "alt": "", "source": "library"},
        "background_overlay_background": "classic",
        "background_overlay_color": "rgba(0,0,0,0.6)",
        "background_position": "center center",
        "background_size": "cover",
        "background_repeat": "no-repeat",
        "min_height": {"unit": "px", "size": 480},
        "padding": {"unit": "px", "top": "200", "right": "50", "bottom": "60", "left": "50", "isLinked": False}
    }


def get_body_settings(use_bg=False):
    s = {
        "flex_direction": "column",
        "padding": {"unit": "px", "top": "40", "right": "50", "bottom": "40", "left": "50", "isLinked": False}
    }
    if use_bg:
        s["background_background"] = "classic"
        s["background_color"] = "#F5F5F5"
    return s


def get_cta_settings():
    return {
        "flex_direction": "column",
        "background_background": "classic",
        "background_color": "#1B1B1B",
        "padding": {"unit": "px", "top": "60", "right": "50", "bottom": "60", "left": "50", "isLinked": False}
    }


def heading(text, level="h2", size=28, color="#1B1B1B", align="left"):
    return make_widget("heading", {
        "title": text,
        "header_size": level,
        "typography_typography": "custom",
        "typography_font_family": "Sora",
        "typography_font_size": {"unit": "px", "size": size},
        "typography_font_weight": "700",
        "title_color": color,
        "align": align
    })


def text_editor(html, color="#444444", size=16):
    return make_widget("text-editor", {
        "editor": html,
        "typography_typography": "custom",
        "typography_font_family": "Sora",
        "typography_font_size": {"unit": "px", "size": size},
        "typography_font_weight": "300",
        "text_color": color
    })


def make_hero_section(title, intro_text):
    return make_outer_container(get_hero_settings(), [
        heading(title, "h1", 42, "#FFFFFF", "left"),
        text_editor(f"<p>{intro_text}</p>", "#FFFFFF")
    ])


def make_body_from_parts(parts, use_bg=False):
    return make_outer_container(get_body_settings(use_bg), parts)


def make_cta_section():
    return make_outer_container(get_cta_settings(), [
        heading("Solicite sua cotação em até 48 horas úteis", "h2", 36, "#FFFFFF", "center"),
        text_editor("<p style=\"text-align: center;\">Envie seu desenho técnico (DWG, PDF, STEP, IGES) ou amostra física para análise gratuita. Nossa engenharia avalia o projeto e retorna com orçamento em até 48 horas úteis.</p>", "#FFFFFF"),
        make_widget("button", {
            "text": "Solicitar Cotação →",
            "link": {"url": CONTATO_URL, "is_external": "", "nofollow": "", "custom_attributes": ""},
            "button_background_color": "#C62828",
            "button_text_color": "#FFFFFF",
            "typography_typography": "custom",
            "typography_font_family": "Sora",
            "typography_font_size": {"unit": "px", "size": 16},
            "typography_font_weight": "600",
            "border_radius": {"unit": "px", "top": "6", "right": "6", "bottom": "6", "left": "6", "isLinked": True},
            "padding": {"unit": "px", "top": "16", "right": "32", "bottom": "16", "left": "32", "isLinked": False},
            "align": "center"
        })
    ])


def make_schema_section(schema_html):
    return make_outer_container(
        {"flex_direction": "column", "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}},
        [make_widget("html", {"editor": schema_html})]
    )


def p(text):
    return f"<p>{text}</p>"


def h3(text):
    return f"<h3>{text}</h3>"


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def strong(text):
    return f"<strong>{text}</strong>"


def get_slug_url(slug):
    return f"{SITE_URL}/{slug}/"


def classify_category(slug, title):
    t = (slug + " " + title).lower()
    if any(w in t for w in ["anel", "aneis", "segmento", "pistao", "bronze", "bomba-vacuo"]):
        return "aneis"
    if any(w in t for w in ["fundicao-de-ferro", "fundicao ferro", "fundicao e usinagem"]):
        return "fundicao-geral"
    if any(w in t for w in ["fundicao-de-auto", "fundicao-de-autopecas", "fundicao autopecas"]):
        return "fundicao-autopecas"
    if any(w in t for w in ["fundicao-de-ferro-cinzento", "fundicao ferro-fundido-cinzento"]):
        return "fundicao-cinzento"
    if any(w in t for w in ["fundicao-de-ferro-em-itaquaquecetuba", "fundicao-de-ferro-fundido", "fundicao-de-pecas", "fundicao-em-sao-paulo", "fundicao-ferro-fundido", "servico-de-fundicao"]):
        return "fundicao-servicos"
    if any(w in t for w in ["fundicao-de-ferro-em-pep"]):
        return "fundicao-pep-set"
    if "abracadeira" in t:
        return "abracadeiras"
    if any(w in t for w in ["pecas-para-bomba", "pecas-para-bombeamento", "pecas-para-sistema-de-bombeamento"]):
        return "bombeamento"
    if any(w in t for w in ["pecas-para-tratores"]):
        return "tratores"
    if any(w in t for w in ["pecas-de-ferro", "fabricacao-de-pecas"]):
        return "pecas-ferro"
    if any(w in t for w in ["compressor", "cabecote-compr", "cilindro-compr"]):
        return "compressores"
    if any(w in t for w in ["cubos", "mancais"]):
        return "cubos-mancais"
    if any(w in t for w in ["empresa-de", "empresas-fabricantes"]):
        return "empresa"
    if any(w in t for w in ["fabrica-de-pecas-automotiva", "fabricante-de-pecas-automotivas"]):
        return "auto-pecas"
    if any(w in t for w in ["fabricante-aneis", "fornecedor-aneis"]):
        return "fornecedor-aneis"
    if any(w in t for w in ["fabricante-de-pecas-para-bombeamento", "fabricante-de-pecas-para-maquinas", "fabricante-abracadeiras"]):
        return "fabricante-industrial"
    if "rolos" in t:
        return "rolos"
    if "industria-metalurgica" in t:
        return "industria-metalurgica"
    return "geral"


def generate_schema_article(slug, title, content_preview, category):
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": f"{SITE_URL}/{slug}/#article",
                "headline": title,
                "description": content_preview[:160] if content_preview else title,
                "author": {
                    "@type": "Person",
                    "name": AUTHOR_NAME,
                    "jobTitle": AUTHOR_JOB,
                    "affiliation": {"@type": "Organization", "name": PUBLISHER}
                },
                "publisher": {
                    "@type": "Organization",
                    "name": PUBLISHER,
                    "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/wp-content/uploads/2026/05/LOGOTIPO-HORIZONTAL-1-1-scaled.webp"}
                },
                "datePublished": "2026-05-20",
                "dateModified": "2026-06-29",
                "image": HERO_IMG,
                "mainEntityOfPage": f"{SITE_URL}/{slug}/",
                "about": {"@type": "Thing", "name": title.split(":")[0] if ":" in title else title},
                "keywords": slug.replace("-", ", ")
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{SITE_URL}/{slug}/#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE_URL}/blog/"},
                    {"@type": "ListItem", "position": 3, "name": title[:60], "item": f"{SITE_URL}/{slug}/"}
                ]
            }
        ]
    }

    # Add FAQ schema if category has questions
    faq_pairs = get_faq_pairs(category, slug)
    if faq_pairs:
        faq_schema = {
            "@type": "FAQPage",
            "@id": f"{SITE_URL}/{slug}/#faq",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faq_pairs
            ]
        }
        schema["@graph"].append(faq_schema)

    return schema


def get_faq_pairs(category, slug):
    cat = category
    t = slug.replace("-", " ")

    general_qs = [
        ("Quais as certificações que uma fundição deve ter?", "Uma fundição de qualidade deve possuir ISO 9001:2015 (sistema de gestão da qualidade), laboratório próprio com espectrômetro para análise química, e controle metalúrgico rigoroso. A Metal Indianápolis possui ISO 9001 e laboratório próprio desde 1966."),
        ("Qual o prazo de entrega de peças sob encomenda?", "O prazo varia conforme a complexidade da peça e volume do lote. Em média, a Metal Indianápolis entrega lotes de 50 a 10.000 peças em 15 a 45 dias úteis, incluindo fundição, usinagem e controle de qualidade."),
        ("Vocês aceitam desenho técnico para orçamento?", "Sim. Aceitamos desenhos em DWG, PDF, STEP e IGES, além de amostras físicas para engenharia reversa. Nossa equipe técnica analisa e retorna com proposta em até 48 horas úteis."),
    ]

    specific_qs = {
        "aneis": [
            ("Qual a função do anel de segmento no compressor?", "O anel de segmento tem três funções críticas: vedar a câmara de compressão para evitar vazamento de ar, controlar a distribuição de óleo lubrificante nas paredes do cilindro, e transferir calor do pistão para o cilindro. Anéis de baixa qualidade causam perda de eficiência e aumento do consumo de energia."),
            ("Como saber se o anel de segmento precisa ser trocado?", "Sinais típicos de desgaste incluem: redução da pressão de operação do compressor, aumento no consumo de óleo lubrificante, ruídos anormais durante o funcionamento, e presença de óleo no ar comprimido. A recomendação técnica é inspecionar os anéis a cada 2.000 horas de operação."),
            ("Qual a diferença entre anel de segmento de ferro fundido e bronze?", "Anéis de ferro fundido (GG25 ou GGG50) oferecem maior resistência ao desgaste e são adequados para aplicações de alta pressão e temperatura. Anéis de bronze têm melhor condutividade térmica e são usados em aplicações com lubrificação crítica ou meios corrosivos."),
            ("O que causa falha prematura em anéis de segmento?", "As causas mais comuns incluem: desalinhamento do pistão no cilindro, lubrificação inadequada, partículas abrasivas no sistema, temperatura excessiva de operação, e escolha incorreta do material para a aplicação específica."),
            ("Quanto tempo dura um anel de segmento de compressor?", "A vida útil varia conforme a severidade da aplicação. Em condições normais de operação com manutenção adequada, anéis de segmento de qualidade duram entre 4.000 e 8.000 horas. A Metal Indianápolis produz anéis com ligas especiais que prolongam a vida útil em até 30% comparado a anéis convencionais."),
        ],
        "fundicao-geral": [
            ("Qual a diferença entre ferro fundido cinzento e nodular?", "A diferença fundamental está na forma da grafita: no ferro cinzento a grafita é lamelar (em forma de flocos), o que confere alta capacidade de amortecimento de vibrações mas menor resistência à tração. No ferro nodular a grafita é esferoidal (em forma de nódulos), proporcionando maior resistência mecânica e ductilidade."),
            ("Quais as classes de ferro fundido mais comuns?", "As classes mais comuns são GG20 (200 MPa de resistência à tração) e GG25 (250 MPa) para ferro cinzento, e GGG40 (400 MPa) e GGG50 (500 MPa) para ferro nodular. Cada classe atende a normas ABNT NBR, DIN, ISO e ASTM com especificações equivalentes."),
            ("O que significa GG20 e GG25 na classificação do ferro fundido?", "GG vem do alemão 'Grauguss' (ferro fundido cinzento). O número indica a resistência à tração mínima em MPa. GG20 = 200 MPa, GG25 = 250 MPa. Na norma ABNT NBR 6589, estas classes equivalem a FC200 e FC250 respectivamente."),
            ("Qual o processo de fundição mais utilizado no Brasil?", "O processo de moldagem em areia verde responde por cerca de 70% da produção brasileira de fundidos. Outros processos incluem cold box (caixa fria) para maior precisão dimensional, pep set para peças de médio porte, e microfusão (cera perdida) para geometrias complexas."),
            ("Quanto tempo leva o processo de fundição?", "O ciclo completo — da aprovação do desenho à peça pronta — leva de 15 a 45 dias úteis, dependendo da complexidade. Isso inclui: preparação do molde, fusão em forno de indução, vazamento, resfriamento, rebarbação, tratamento térmico e usinagem final."),
        ],
        "fundicao-autopecas": [
            ("Por que o ferro fundido é usado em autopeças?", "O ferro fundido oferece a melhor relação custo-benefício para componentes automotivos que exigem alta resistência ao desgaste, capacidade de amortecimento de vibrações e estabilidade dimensional. Além disso, a excelente usinabilidade do material reduz custos de fabricação."),
            ("Quais autopeças são fabricadas em ferro fundido?", "As principais incluem: blocos de motor, cabeçotes, discos de freio, tambores de freio, anéis de segmento, bielas, virabrequins, carcaças de transmissão, polias, cubos de roda e suportes diversos."),
            ("Qual a diferença entre peças fundidas e forjadas?", "Peças fundidas são produzidas pelo vazamento de metal líquido em moldes, permitindo geometrias complexas e maior liberdade de design. Peças forjadas são conformadas mecanicamente, oferecendo maior resistência mas com menor complexidade geométrica e maior custo."),
        ],
        "bombeamento": [
            ("Quais peças de bombeamento de concreto sofrem mais desgaste?", "As peças com maior desgaste são: a válvula S (ou válvula basculante), os anéis de desgaste, os cilindros de concreto, as abraçadeiras de tubulação, e os cotovelos de aço. Todas essas peças estão sujeitas a abrasão intensa pelo concreto em alta pressão."),
            ("Como evitar desgaste prematuro em peças de bombeamento?", "Utilizar peças de ferro fundido de alta qualidade com tratamento térmico adequado, manter a lubricidade correta do concreto, fazer inspeções regulares a cada 500 m³ bombeados, e substituir peças nos intervalos recomendados pelo fabricante."),
            ("Qual a função da abraçadeira no bombeamento de concreto?", "A abraçadeira tem a função crítica de vedar as conexões entre tubulações de bombeamento, suportando pressões de até 85 bar. Uma abraçadeira de má qualidade pode causar vazamentos, perda de pressão e interrupção da obra."),
        ],
        "compressores": [
            ("Quais as principais peças de um compressor de ar?", "As peças críticas incluem: cilindro, cabeçote, pistão, anéis de segmento, camisa do cilindro, válvulas de admissão e descarga, e biela. Cada componente deve ser fabricado com materiais específicos — ferro fundido cinzento GG25 para cilindros e cabeçotes, e ferro nodular GGG50 para anéis de segmento."),
            ("Como escolher o cabeçote de compressor ideal?", "A escolha depende do tipo de compressor (alternativo, parafuso ou centrífugo), da pressão de trabalho (baixa: até 7 bar, média: 7-15 bar, alta: acima de 15 bar), da vazão necessária (m³/min), e do fluido (ar, gases ou refrigerantes). Consulte sempre a engenharia do fabricante."),
        ],
        "abracadeiras": [
            ("Quais os tipos de abraçadeira para concreto?", "Os principais tipos são: abraçadeira tipo U (para conexões simples), abraçadeira dupla (para maior segurança em altas pressões), abraçadeira de pressão (com vedação reforçada), e abraçadeira articulada (para facilidade de montagem e desmontagem)."),
            ("Qual material é ideal para abraçadeiras de concreto?", "O ferro fundido nodular GGG50 é o material ideal por oferecer alta resistência mecânica, tenacidade e resistência à corrosão. Abraçadeiras de aço carbono têm menor durabilidade, enquanto as de ferro fundido cinzento podem ser frágeis para aplicações de alta pressão."),
        ],
        "tratores": [
            ("Quais peças agrícolas são fabricadas em ferro fundido?", "As principais peças agrícolas em ferro fundido incluem: cubos de roda para carretas, mancais, polias, engrenagens, carcaças de transmissão, tambores de freio, suportes estruturais, e componentes de sistemas hidráulicos e de suspensão."),
            ("Qual a vantagem do ferro nodular em peças agrícolas?", "O ferro nodular GGG50 oferece resistência mecânica comparável ao aço (500 MPa de tração) com melhor resistência à corrosão e menor custo de fabricação. Para peças agrícolas sujeitas a impactos e cargas variáveis, o ferro nodular é a escolha mais custo-efetiva."),
        ],
        "empresa": [
            ("Como escolher uma empresa de fundição confiável?", "Os critérios essenciais são: certificação ISO 9001, laboratório próprio com espectrômetro, capacidade de fundição e usinagem integradas, tempo de mercado, referências de clientes, capacidade produtiva, e suporte técnico especializado."),
            ("Por que a verticalização (fundição + usinagem) é importante?", "Empresas com fundição e usinagem próprias eliminam a terceirização, reduzindo lead time, garantindo controle total da qualidade, eliminando retrabalhos de interface, e oferecendo peça pronta com única responsabilidade contratual."),
        ],
        "cubos-mancais": [
            ("Qual a diferença entre cubo e mancal?", "O cubo é um componente que conecta um eixo a uma roda ou polia, transmitindo torque e movimento. O mancal é um suporte que sustenta eixos rotativos, reduzindo atrito através de rolamentos ou buchas. Ambos são fabricados em ferro fundido por sua resistência e estabilidade."),
        ],
    }

    qs = specific_qs.get(cat, [])
    return qs + general_qs


def get_intro_from_original(html_content):
    """Extract first meaningful paragraph from original content."""
    match = re.search(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL)
    if match:
        text = re.sub(r'<[^>]+>', '', match.group(1))
        text = re.sub(r'&nbsp;', ' ', text).strip()
        if len(text) > 350:
            text = text[:347] + '...'
        return text
    return ""


def get_kw_h2(topic, slug):
    """Generate H2 section headings with keywords."""
    t = topic.lower()
    if "anel" in t:
        return [
            "O que são anéis de segmento e como funcionam",
            "Tipos de anéis de segmento para aplicações industriais",
            "Materiais utilizados na fabricação de anéis de segmento",
            "Aplicações dos anéis de segmento na indústria",
            "Vantagens dos anéis de segmento em ferro fundido",
            "Como escolher o anel de segmento ideal para seu equipamento",
        ]
    if "fundicao" in t and "cinzento" in t:
        return [
            "O que é ferro fundido cinzento e suas características",
            "Propriedades mecânicas do ferro fundido cinzento GG20 e GG25",
            "Processo de fundição do ferro cinzento",
            "Aplicações industriais do ferro fundido cinzento",
            "Vantagens do ferro fundido cinzento na indústria",
            "Como escolher a classe ideal de ferro cinzento",
        ]
    if "nodular" in t:
        return [
            "O que é ferro fundido nodular e suas propriedades",
            "Diferenças entre ferro nodular e ferro cinzento",
            "Classes de ferro nodular GGG40, GGG50 e aplicações",
            "Processo de fabricação do ferro fundido nodular",
        ]
    if "abracadeira" in t:
        return [
            "O que são abraçadeiras para concreto",
            "Tipos de abraçadeiras para tubulação de concreto",
            "Materiais e especificações técnicas",
            "Aplicações na construção civil",
            "Vantagens das abraçadeiras de ferro fundido",
            "Como escolher a abraçadeira ideal para sua obra",
        ]
    if "bombeamento" in t or "bomba de concreto" in t:
        return [
            "Peças essenciais para bombeamento de concreto",
            "Critérios de qualidade em peças para bomba de concreto",
            "Materiais utilizados em peças de bombeamento",
            "Como aumentar a vida útil das peças de bombeamento",
            "Vantagens de peças em ferro fundido para concreto",
        ]
    if "compressor" in t:
        return [
            "Componentes essenciais de compressores de ar",
            "Materiais ideais para peças de compressor",
            "Como escolher peças de reposição para compressor",
            "Manutenção preventiva de compressores industriais",
            "Vantagens das peças em ferro fundido para compressores",
        ]
    if "trator" in t:
        return [
            "Peças agrícolas em ferro fundido: essenciais para o campo",
            "Tipos de peças para tratores agrícolas",
            "Vantagens do ferro fundido em componentes agrícolas",
            "Como escolher o fornecedor de peças para tratores",
            "Manutenção de peças agrícolas fundidas",
        ]
    if "cubos" in t or "mancais" in t:
        return [
            "O que são cubos e mancais industriais",
            "Materiais utilizados em cubos e mancais",
            "Aplicações na indústria e no setor agrícola",
            "Vantagens dos cubos e mancais em ferro fundido",
            "Como especificar cubos e mancais para seu projeto",
        ]
    if "empresa" in t and ("fundicao" in t or "ferro" in t):
        return [
            "O que considerar ao escolher uma empresa de fundição",
            "Certificações e qualidade em fundição",
            "Capacidade produtiva e verticalização",
            "Diferenciais de uma fundição com ISO 9001",
            "Como avaliar fornecedores de peças fundidas",
        ]
    if "automotiv" in t:
        return [
            "A importância das peças automotivas em ferro fundido",
            "Principais peças automotivas fabricadas em ferro fundido",
            "Vantagens do ferro fundido na indústria automotiva",
            "Como escolher um fabricante de peças automotivas",
            "Controle de qualidade na fabricação de autopeças",
        ]
    if "fabricante" in t and "aneis" in t:
        return [
            "Como escolher um fabricante de anéis de segmento",
            "Critérios de qualidade em anéis de segmento",
            "Processo produtivo de anéis de segmento",
            "Vantagens de anéis de segmento em ferro fundido",
        ]
    if "usinagem" in t:
        return [
            "O que é fundição e usinagem integradas",
            "Vantagens da verticalização fundição + usinagem",
            "Processo de usinagem CNC de precisão",
            "Controle de qualidade em peças usinadas",
            "Como escolher um parceiro de fundição e usinagem",
        ]
    return [
        "O que é e como funciona",
        "Principais tipos e variações",
        "Aplicações na indústria",
        "Vantagens e benefícios",
        "Como escolher o fornecedor ideal",
        "Perguntas frequentes",
    ]


def get_kw_text(topic, slug, section_index):
    """Generate keyword-rich body text for each section."""
    t = (topic + " " + slug.replace("-", " ")).lower()

    texts = {
        "aneis_def": f"<p>Os {strong('anéis de segmento')} — também conhecidos como anéis de pistão — são componentes circulares e flexíveis instalados nas canaletas do pistão em {strong('compressores de ar')}, motores de combustão e sistemas hidráulicos. Sua função principal é vedar a câmara de compressão, controlar a distribuição de óleo lubrificante e transferir calor do pistão para o cilindro. Fabricados em {strong('ferro fundido nodular GGG50')} ou {strong('ferro fundido cinzento GG25')}, os anéis de segmento da Metal Indianápolis são produzidos sob rigoroso controle metalúrgico em laboratório próprio com espectrômetro, garantindo composição química precisa e propriedades mecânicas consistentes conforme normas ABNT NBR 6916 e DIN 1691.</p>",
    }

    generic_def = f"<p>Na Metal Indianápolis, com mais de 60 anos de experiência em {strong('fundição e usinagem de ferro fundido')}, entendemos a importância de cada componente industrial. Este artigo apresenta informações técnicas detalhadas para ajudar engenheiros, compradores e profissionais de manutenção a tomar decisões mais assertivas na especificação e aquisição de peças em ferro fundido.</p>"

    return generic_def


def generate_article_content(slug, title, original_html, category):
    """Generate full EEAT-compliant article content."""
    clean = re.sub(r'<p[^>]*>\s*</p>', '', original_html)
    paragraphs = re.findall(r'(<p[^>]*>.*?</p>)', clean, re.DOTALL)

    # Use original first paragraph as intro
    intro = ""
    if paragraphs:
        intro_text = re.sub(r'<[^>]+>', '', paragraphs[0])
        intro_text = re.sub(r'&nbsp;', ' ', intro_text).strip()
        intro = intro_text[:350]

    # Build FAQ pairs
    faq_pairs = get_faq_pairs(category, slug)

    # Build H2 sections with content
    h2_headers = get_kw_h2(title, slug)
    content_sections = []

    for idx, h2 in enumerate(h2_headers[:5]):
        section_html = f"<h2>{h2}</h2>"

        # Generate section body from original paragraphs
        start_p = 1 + idx * 2
        section_paras = []
        for pi in range(start_p, min(start_p + 3, len(paragraphs))):
            if pi < len(paragraphs):
                section_paras.append(paragraphs[pi])
        if section_paras:
            section_html += "".join(section_paras)
        else:
            section_html += f"<p>Consulte nossos engenheiros técnicos para informações detalhadas sobre {title.lower()}.</p>"

        # Add technical details based on section type
        if idx == 0:
            section_html += f"<p>A {strong('Metal Indianápolis')} possui laboratório próprio equipado com espectrômetro para validação da composição química, microscópio metalúrgico para análise microestrutural e durômetro para medição de dureza Brinell. Todos os processos são certificados ISO 9001:2015.</p>"
        elif idx == 2:
            section_html += f"<p>O processo produtivo da Metal Indianápolis integra {strong('fundição e usinagem CNC próprias')} no mesmo parque fabril em Itaquaquecetuba, SP — um diferencial que elimina retrabalhos, reduz lead time e garante controle total da qualidade desde a metalurgia até o acabamento final.</p>"
        elif idx == 3:
            section_html += f"<p>Solicite uma {strong('análise técnica gratuita')} do seu projeto. Nossa equipe de engenharia avalia o desenho técnico (DWG, PDF, STEP, IGES) ou amostra física e retorna com a especificação ideal do material e processo de fabricação.</p>"

        content_sections.append(section_html)

    # Build FAQ section
    faq_html = "<h2>Perguntas frequentes</h2>"
    for q, a in faq_pairs[:5]:
        faq_html += f"<h3>{q}</h3><p>{a}</p>"

    content_sections.append(faq_html)

    return intro, content_sections


def build_blog_json(slug, title, original_html, category):
    """Build the complete Elementor JSON for a blog post."""
    intro, body_sections = generate_article_content(slug, title, original_html, category)
    schema = generate_schema_article(slug, title, intro, category)
    schema_html = f"<script type=\"application/ld+json\">{json.dumps(schema, ensure_ascii=False, indent=2)}</script>"

    content = []

    # Hero section
    if not intro:
        intro = f"Guia técnico completo sobre {title.lower()} para profissionais da indústria. Entenda especificações, aplicações e como escolher o fornecedor ideal."
    content.append(make_hero_section(title, intro))

    # Body sections
    for i, sec_html in enumerate(body_sections):
        use_bg = i % 2 == 1
        content.append(make_body_from_parts([text_editor(sec_html)], use_bg))

        # Insert CTA after first body section
        if i == 0:
            content.append(make_cta_section())

    # Schema section
    content.append(make_schema_section(schema_html))

    return {
        "title": title[:60],
        "type": "page",
        "content": content,
        "page_settings": {},
        "version": "0.4"
    }


def main():
    with open(POSTS_FILE) as f:
        all_posts = json.load(f)

    # Skip first 12 posts (already have JSON files)
    new_posts = all_posts[12:]

    print(f"Total posts in API: {len(all_posts)}")
    print(f"New posts to generate (EEAT): {len(new_posts)}")
    print()

    for idx, post in enumerate(new_posts):
        slug = post["slug"]
        title = post["title"]["rendered"]
        original_html = post["content"]["rendered"]
        category = classify_category(slug, title)

        blog_data = build_blog_json(slug, title, original_html, category)
        blog_number = idx + 13

        # Clean up old file if exists (exact filename match, not substring)
        expected_name = f"{blog_number:02d}-blog-{slug}.json"
        old_path = os.path.join(BLOG_DIR, expected_name)
        if os.path.exists(old_path):
            os.remove(old_path)

        filename = f"{blog_number:02d}-blog-{slug}.json"
        filepath = os.path.join(BLOG_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(blog_data, f, ensure_ascii=False)

        # Count sections for reporting
        sections = len(blog_data["content"])
        body_widgets = sum(
            1 for sec in blog_data["content"]
            for inner in sec.get("elements", [])
            for w in inner.get("elements", [])
            if w.get("widgetType") in ("heading", "text-editor")
        )
        has_schema = any(
            "application/ld+json" in w.get("settings", {}).get("editor", "")
            for sec in blog_data["content"]
            for inner in sec.get("elements", [])
            for w in inner.get("elements", [])
            if w.get("widgetType") == "html"
        )
        print(f"  #{blog_number:02d} {filename[:55]:55s} | cat={category:<20s} | sec={sections} | widgets={body_widgets} | schema={'Y' if has_schema else 'N'}")

    print(f"\nGenerated {len(new_posts)} EEAT-compliant blog files!")
    print("Each article includes: Article schema + FAQPage schema + BreadcrumbList + EEAT structure")


if __name__ == "__main__":
    main()
