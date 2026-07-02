#!/usr/bin/env python3
"""Generate 100% original blog JSON files - zero agency text.
Output: raw-files-v2/retrabalho/ (01-23) and raw-files-v2/novos/ (24-58)"""

import json
import os
import uuid
from datetime import datetime

DIR = os.path.dirname(os.path.abspath(__file__))
RETRABALHO_DIR = os.path.join(DIR, "retrabalho")
NOVOS_DIR = os.path.join(DIR, "novos")

HERO_IMG = "https://preview.indianapolis.com.br/wp-content/uploads/2026/05/fundicao-metal-indianapolis-hero.webp"
CONTATO_URL = "https://preview.indianapolis.com.br/contato/"
SITE_URL = "https://preview.indianapolis.com.br"
AUTHOR = "Vanderlei Rampasso"
PUBLISHER = "Metal Indianápolis"

# Slug and title for all 58 articles
ARTICLES = [
    (1, "ferro-fundido-cinzento", "Ferro fundido cinzento: guia técnico completo de propriedades e aplicações industriais"),
    (2, "preco-ferro-fundido-kg", "Preço do ferro fundido por kg: tabela atualizada e fatores que influenciam o valor"),
    (3, "fabrica-roldanas", "Fábrica de roldanas: como escolher o fornecedor ideal de peças em ferro fundido"),
    (4, "camisa-compressor", "Camisa de compressor: função, materiais e como identificar desgaste"),
    (5, "cabecote-compressor", "Cabeçote de compressor: guia técnico de especificação e manutenção"),
    (6, "anel-segmento-motor", "Anel de segmento de motor: tudo sobre função, tipos e especificações técnicas"),
    (7, "anel-segmento-preco", "Preço de anel de segmento: tabela comparativa e fatores de custo"),
    (8, "preco-ferro-fundido", "Preço do ferro fundido: cotações, tipos de liga e tendências do mercado"),
    (9, "pecas-tratores", "Peças para tratores agrícolas: guia de especificação em ferro fundido"),
    (10, "fundicao-ferros", "Fundição de ferros: processo industrial, tipos de liga e aplicações"),
    (11, "anel-segmento", "Anel de segmento: o que é, como funciona e onde comprar"),
    (12, "fabricante-automotivo", "Fabricante automotivo de peças em ferro fundido: como selecionar o parceiro ideal"),
    (13, "fabricante-de-pecas-para-bombeamento-de-concreto", "Fabricante de peças para bombeamento de concreto: critérios técnicos de avaliação"),
    (14, "fabricante-de-pecas-para-maquinas-e-equipamentos", "Fabricante de peças para máquinas e equipamentos industriais em ferro fundido"),
    (15, "fornecedor-aneis-de-segmento", "Fornecedor de anéis de segmento: como avaliar qualidade e capacidade técnica"),
    (16, "fundicao-de-auto-pecas", "Fundição de autopeças: processo produtivo e vantagens do ferro fundido"),
    (17, "fundicao-de-autopecas", "Fundição de autopeças: especificações técnicas e controle de qualidade"),
    (18, "fundicao-de-ferro-cinzento-e-nodular", "Fundição de ferro cinzento e nodular: diferenças, aplicações e normas técnicas"),
    (19, "fundicao-de-ferro-em-itaquaquecetuba", "Fundição de ferro em Itaquaquecetuba: estrutura industrial e capacidade produtiva"),
    (20, "fundicao-de-ferro-em-pep-set", "Fundição de ferro em pep set: processo, vantagens e aplicações industriais"),
    (21, "fundicao-de-ferro-fundido-2", "Fundição de ferro fundido: processo completo da matéria-prima à peça acabada"),
    (22, "fundicao-de-ferro-fundido", "Fundição de ferro fundido cinzento e nodular: guia técnico completo"),
    (23, "fundicao-de-pecas-em-ferro-fundido", "Fundição de peças em ferro fundido: especificações, prazos e certificações"),
    (24, "fundicao-e-usinagem", "Fundição e usinagem integradas: vantagens da verticalização industrial"),
    (25, "fundicao-e-usinagem-em-ferro-fundido-empresa", "Empresa de fundição e usinagem em ferro fundido: o que considerar na escolha"),
    (26, "fundicao-e-usinagem-proprias", "Fundição e usinagem próprias: diferencial competitivo na indústria metalúrgica"),
    (27, "fundicao-em-sao-paulo", "Fundição em São Paulo: panorama industrial e fornecedores de referência"),
    (28, "fundicao-ferro-fundido-cinzento", "Fundição de ferro fundido cinzento: classes GG20, GG25 e aplicações técnicas"),
    (29, "industria-metalurgica-de-pecas-automotivas", "Indústria metalúrgica de peças automotivas: processos e certificações"),
    (30, "pecas-de-ferro-fundido", "Peças de ferro fundido sob encomenda: guia de especificação técnica"),
    (31, "pecas-para-bomba-de-concreto", "Peças para bomba de concreto em ferro fundido: resistência e durabilidade"),
    (32, "pecas-para-bombeamento-de-concreto", "Peças para bombeamento de concreto: especificações e vida útil"),
    (33, "pecas-para-sistema-de-bombeamento-de-concreto", "Peças para sistema de bombeamento de concreto: manutenção e reposição"),
    (34, "pecas-para-tratores-agricolas", "Peças para tratores agrícolas em ferro fundido: durabilidade no campo"),
    (35, "rolos-de-apoio-para-betoneiras", "Rolos de apoio para betoneiras: especificação em ferro fundido"),
    (36, "servico-de-fundicao-em-sao-paulo", "Serviço de fundição em São Paulo: capacidade técnica e prazos"),
    (37, "abracadeira-para-concreto", "Abraçadeira para concreto: tipos, materiais e aplicações na construção civil"),
    (38, "abracadeira-para-tubo-de-concreto", "Abraçadeira para tubo de concreto: especificações técnicas e instalação"),
    (39, "aneis-de-segmento-de-ferro", "Anéis de segmento de ferro: tipos, materiais e aplicações"),
    (40, "aneis-de-segmento-do-pistao", "Anéis de segmento do pistão: função, desgaste e especificação"),
    (41, "aneis-de-segmento-em-bronze", "Anéis de segmento em bronze: aplicações especiais em compressores"),
    (42, "aneis-de-segmento-para-amortecedores-em-bronze", "Anéis de segmento para amortecedores em bronze: especificação técnica"),
    (43, "aneis-de-segmento-pistao", "Anéis de segmento de pistão para compressores: guia de seleção"),
    (44, "aneis-de-segmento-sob-medida", "Anéis de segmento sob medida: fabricação por desenho técnico"),
    (45, "aneis-para-bombas-a-vacuo", "Anéis para bombas a vácuo: especificação em ferro fundido e bronze"),
    (46, "aneis-para-compressor-de-alta-pressao", "Anéis para compressor de alta pressão: materiais e desempenho"),
    (47, "anel-de-segmento-em-ferro-fundido", "Anel de segmento em ferro fundido: vantagens e aplicações"),
    (48, "anel-de-segmento-para-compressor", "Anel de segmento para compressor: guia de especificação técnica"),
    (49, "cabecote-compressor-de-ar", "Cabeçote de compressor de ar: materiais, dimensões e fornecedores"),
    (50, "cilindro-compressor-de-ar", "Cilindro de compressor de ar em ferro fundido: especificação"),
    (51, "cubos-e-mancais-para-maquinas", "Cubos e mancais para máquinas: fabricação em ferro fundido"),
    (52, "empresa-de-ferro-fundido", "Empresa de ferro fundido: como avaliar um fornecedor industrial"),
    (53, "empresa-de-fundicao-de-ferro-fundido", "Empresa de fundição de ferro fundido: certificações e capacidade"),
    (54, "empresas-fabricantes-de-pecas-automotivas", "Empresas fabricantes de peças automotivas em ferro fundido"),
    (55, "fabrica-de-pecas-automotiva", "Fábrica de peças automotivas: processo de fundição e usinagem"),
    (56, "fabricacao-de-pecas-em-ferro-fundido", "Fabricação de peças em ferro fundido: do projeto à peça pronta"),
    (57, "fabricante-aneis-de-segmento", "Fabricante de anéis de segmento: capacidade técnica e qualidade"),
    (58, "fabricante-abracadeiras-bombeamento-concreto", "Fabricante de abraçadeiras para bombeamento de concreto"),
]


def make_id():
    return uuid.uuid4().hex[:10]


def make_widget(wt, settings):
    return {"id": make_id(), "settings": settings, "elements": [], "isInner": False, "widgetType": wt, "elType": "widget"}


def make_inner(widgets):
    return {"id": make_id(), "settings": {"content_width": "full"}, "elements": widgets, "elType": "container", "isInner": True}


def make_outer(settings, widgets):
    return {"id": make_id(), "settings": settings, "elements": [make_inner(widgets)], "elType": "container", "isInner": False}


def hero_section(title):
    return make_outer({
        "flex_direction": "column",
        "background_background": "classic",
        "background_image": {"url": HERO_IMG, "id": 356, "alt": "", "source": "library"},
        "background_overlay_background": "classic",
        "background_overlay_color": "rgba(0,0,0,0.6)",
        "background_position": "center center",
        "background_size": "cover",
        "min_height": {"unit": "px", "size": 480},
        "padding": {"unit": "px", "top": "200", "right": "50", "bottom": "60", "left": "50", "isLinked": False}
    }, [
        make_widget("heading", {"title": title, "header_size": "h1", "typography_typography": "custom",
            "typography_font_family": "Sora", "typography_font_size": {"unit": "px", "size": 42},
            "typography_font_weight": "700", "title_color": "#FFFFFF", "align": "left"}),
        make_widget("text-editor", {"editor": f"<p>Guia técnico completo sobre {title.lower()} para profissionais da indústria metalúrgica. Informações atualizadas com especificações, normas e aplicações.</p>",
            "typography_typography": "custom", "typography_font_family": "Sora",
            "typography_font_size": {"unit": "px", "size": 16}, "typography_font_weight": "300", "text_color": "#FFFFFF"})
    ])


def body_section(html, use_bg=False):
    s = {"flex_direction": "column", "padding": {"unit": "px", "top": "40", "right": "50", "bottom": "40", "left": "50", "isLinked": False}}
    if use_bg:
        s["background_background"] = "classic"
        s["background_color"] = "#F5F5F5"
    return make_outer(s, [make_widget("text-editor", {"editor": html,
        "typography_typography": "custom", "typography_font_family": "Sora",
        "typography_font_size": {"unit": "px", "size": 16}, "typography_font_weight": "300", "text_color": "#444444"})])


def cta_section():
    return make_outer({
        "flex_direction": "column", "background_background": "classic", "background_color": "#1B1B1B",
        "padding": {"unit": "px", "top": "60", "right": "50", "bottom": "60", "left": "50", "isLinked": False}
    }, [
        make_widget("heading", {"title": "Solicite sua cotação em até 48 horas úteis", "header_size": "h2",
            "typography_typography": "custom", "typography_font_family": "Sora",
            "typography_font_size": {"unit": "px", "size": 36}, "typography_font_weight": "700",
            "title_color": "#FFFFFF", "align": "center"}),
        make_widget("text-editor", {"editor": "<p style=\"text-align: center;\">Envie seu desenho técnico (DWG, PDF, STEP, IGES) ou amostra física para análise gratuita. Nossa engenharia avalia o projeto e retorna com orçamento em até 48 horas úteis.</p>",
            "typography_typography": "custom", "typography_font_family": "Sora",
            "typography_font_size": {"unit": "px", "size": 16}, "typography_font_weight": "300", "text_color": "#FFFFFF"}),
        make_widget("button", {"text": "Solicitar Cotação →", "link": {"url": CONTATO_URL, "is_external": "", "nofollow": "", "custom_attributes": ""},
            "button_background_color": "#C62828", "button_text_color": "#FFFFFF",
            "typography_typography": "custom", "typography_font_family": "Sora",
            "typography_font_size": {"unit": "px", "size": 16}, "typography_font_weight": "600",
            "border_radius": {"unit": "px", "top": "6", "right": "6", "bottom": "6", "left": "6", "isLinked": True},
            "padding": {"unit": "px", "top": "16", "right": "32", "bottom": "16", "left": "32", "isLinked": False}, "align": "center"})
    ])


def schema_section(slug, title):
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "@id": f"{SITE_URL}/{slug}/#article", "headline": title,
             "description": f"Guia técnico completo sobre {title.lower()} para profissionais da indústria.",
             "author": {"@type": "Person", "name": AUTHOR, "affiliation": {"@type": "Organization", "name": PUBLISHER}},
             "publisher": {"@type": "Organization", "name": PUBLISHER,
                 "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/wp-content/uploads/2026/05/LOGOTIPO-HORIZONTAL-1-1-scaled.webp"}},
             "datePublished": "2026-05-20", "dateModified": "2026-06-29",
             "image": HERO_IMG, "mainEntityOfPage": f"{SITE_URL}/{slug}/"},
            {"@type": "BreadcrumbList", "@id": f"{SITE_URL}/{slug}/#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL},
                 {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE_URL}/blog/"},
                 {"@type": "ListItem", "position": 3, "name": title[:60], "item": f"{SITE_URL}/{slug}/"}
             ]}
        ]
    }
    html = f"<script type=\"application/ld+json\">{json.dumps(schema, ensure_ascii=False, indent=2)}</script>"
    return make_outer({"flex_direction": "column", "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}},
                      [make_widget("html", {"editor": html})])


def p(text):
    return f"<p>{text}</p>"


def h2(text):
    return f"<h2>{text}</h2>"


def h3(text):
    return f"<h3>{text}</h3>"


def generate_faq(slug, title):
    t = (slug + " " + title).lower()
    if any(w in t for w in ["anel", "aneis", "segmento", "pistao", "bronze"]):
        return [
            ("Qual a diferença entre anel de segmento de ferro fundido e bronze?",
             "Anéis de ferro fundido GG25 ou GGG50 oferecem maior resistência ao desgaste para aplicações de alta pressão. Anéis de bronze têm melhor condutividade térmica, ideais para lubrificação crítica ou meios corrosivos."),
            ("Como identificar desgaste em anéis de segmento?",
             "Sinais incluem perda de pressão no compressor, aumento no consumo de óleo, ruídos anormais e presença de óleo no ar comprimido. A inspeção deve ocorrer a cada 2.000 horas de operação."),
            ("Qual a vida útil de um anel de segmento?",
             "Em condições normais, anéis de qualidade duram entre 4.000 e 8.000 horas. A Metal Indianápolis produz ligas especiais que prolongam a vida útil em até 30%."),
        ]
    if any(w in t for w in ["fundicao", "ferro", "usinagem"]):
        return [
            ("Qual a diferença entre ferro fundido cinzento e nodular?",
             "No ferro cinzento a grafita é lamelar, proporcionando alto amortecimento de vibrações. No nodular a grafita é esferoidal, com maior resistência mecânica e ductilidade."),
            ("O que significam GG20 e GG25?",
             "GG20 e GG25 são classes de ferro fundido cinzento conforme norma DIN. O número indica a resistência à tração mínima: 200 MPa e 250 MPa respectivamente."),
            ("Qual o prazo de entrega de peças sob encomenda?",
             "O prazo varia de 15 a 45 dias úteis conforme complexidade, incluindo fundição, usinagem e controle de qualidade."),
        ]
    if any(w in t for w in ["bombeamento", "concreto", "bomba", "abracadeira"]):
        return [
            ("Quais peças de bombeamento de concreto sofrem mais desgaste?",
             "Válvula S, anéis de desgaste, cilindros de concreto, abraçadeiras e cotovelos. Todas sujeitas a abrasão intensa pelo concreto em alta pressão."),
            ("Como aumentar a vida útil das peças de bombeamento?",
             "Utilizar peças de ferro fundido com tratamento térmico adequado, manter a lubricidade correta do concreto e inspecionar a cada 500 m³ bombeados."),
            ("Qual a função da abraçadeira no bombeamento?",
             "Vedar as conexões entre tubulações, suportando pressões de até 85 bar. Uma peça de má qualidade causa vazamentos e interrupção da obra."),
        ]
    if any(w in t for w in ["trator", "agricola"]):
        return [
            ("Quais peças agrícolas são fabricadas em ferro fundido?",
             "Cubos de roda, mancais, polias, engrenagens, carcaças de transmissão e tambores de freio são os principais componentes."),
            ("Qual a vantagem do ferro nodular em peças agrícolas?",
             "Oferece 500 MPa de tração com resistência à corrosão superior e menor custo que aço, ideal para impactos e cargas variáveis."),
        ]
    if any(w in t for w in ["compressor", "cabecote", "cilindro"]):
        return [
            ("Quais as principais peças de um compressor de ar?",
             "Cilindro, cabeçote, pistão, anéis de segmento, camisa, válvulas de admissão e biela — cada uma com material específico conforme a aplicação."),
            ("Como escolher o cabeçote de compressor ideal?",
             "Depende do tipo de compressor, pressão de trabalho (7-15 bar para média), vazão e fluido. Consulte sempre a engenharia do fabricante."),
        ]
    if any(w in t for w in ["automotiv", "auto-pecas", "autopecas"]):
        return [
            ("Por que o ferro fundido é usado em autopeças?",
             "Oferece a melhor relação custo-benefício com alta resistência ao desgaste, amortecimento de vibrações e excelente usinabilidade."),
            ("Quais autopeças usam ferro fundido?",
             "Blocos de motor, cabeçotes, discos de freio, anéis de segmento, bielas, virabrequins, carcaças e cubos de roda."),
        ]
    return [
        ("Como escolher um fornecedor de peças em ferro fundido?",
         "Critérios essenciais: ISO 9001, laboratório próprio, capacidade integrada de fundição e usinagem, tempo de mercado e suporte técnico."),
        ("Qual a importância da verticalização?",
         "Empresas com fundição e usinagem próprias eliminam terceirização, reduzem lead time e garantem controle total da qualidade."),
    ]


def generate_content(num, slug, title):
    t = (slug + " " + title).lower()
    cat = "geral"
    if any(w in t for w in ["anel", "aneis", "segmento", "pistao", "bronze"]):
        cat = "aneis"
    elif "fundicao" in t and "usinagem" not in t:
        cat = "fundicao"
    elif any(w in t for w in ["bombeamento", "concreto", "bomba", "abracadeira"]):
        cat = "bombeamento"
    elif any(w in t for w in ["trator", "agricola"]):
        cat = "tratores"
    elif any(w in t for w in ["compressor", "cabecote", "cilindro"]):
        cat = "compressores"
    elif any(w in t for w in ["automotiv", "auto-pecas", "autopecas", "fabrica"]):
        cat = "automotivo"

    h2s = {
        "aneis": [
            ("Especificações técnicas dos anéis de segmento", "Os anéis de segmento são componentes de precisão fabricados em ferro fundido nodular GGG50 ou cinzento GG25, conforme normas ABNT NBR 6916 e DIN 1691. Cada anel passa por controle dimensional em laboratório próprio com espectrômetro para validação da composição química, microscópio metalúrgico para análise microestrutural e durômetro para medição de dureza Brinell. A Metal Indianápolis produz anéis com tolerâncias dimensionais de até 0,01 mm, garantindo vedação perfeita e distribuição uniforme de óleo na câmara de compressão."),
            ("Materiais e classes de resistência", "Os materiais mais utilizados incluem ferro fundido cinzento GG25 (250 MPa) para aplicações de média pressão, ferro nodular GGG50 (500 MPa) para alta pressão e temperatura, e ligas especiais com adição de cromo e molibdênio para resistência ao desgaste acelerado. A escolha do material depende da pressão de operação, temperatura do sistema, tipo de fluido e regime de trabalho do equipamento."),
            ("Aplicações industriais e segmentos atendidos", "Anéis de segmento são essenciais em compressores alternativos industriais, motores de combustão, bombas hidráulicas, sistemas de refrigeração, compressores de ar para mineração, equipamentos de perfuração e sistemas pneumáticos. Cada aplicação exige perfil específico do anéis — retangular, trapezoidal ou chanfrado — além de acabamento superficial controlado."),
            ("Controle de qualidade e certificações", "A Metal Indianápolis opera com ISO 9001:2015, laboratório metalúrgico equipado e equipe técnica com mais de 60 anos de experiência em fundição. Todos os lotes são inspecionados individualmente com relatório de ensaio químico e dimensional, garantindo rastreabilidade completa do processo produtivo."),
            ("Como especificar anéis de segmento para seu projeto", "Para especificar corretamente, informe: diâmetro do cilindro, largura e espessura do anéis, material desejado, pressão de trabalho, temperatura de operação e tipo de lubrificação. A Metal Indianápolis oferece suporte técnico completo para seleção do material e perfil ideal."),
        ],
        "fundicao": [
            ("Processo de fundição: da matéria-prima à peça acabada", "O processo inicia com a seleção das matérias-primas — gusa de alta qualidade, sucata selecionada, ferro-ligas e carbono. A fusão ocorre em fornos de indução com controle preciso de temperatura e composição química. Após o vazamento em moldes de areia verde ou pep set, as peças passam por resfriamento controlado, rebarbação, tratamento térmico e usinagem CNC quando necessário."),
            ("Propriedades mecânicas das classes de ferro fundido", "O ferro fundido cinzento GG20 oferece 200 MPa de resistência à tração, ideal para bases e carcaças. GG25 (250 MPa) é indicado para cilindros e cabeçotes. O nodular GGG40 (400 MPa) e GGG50 (500 MPa) são usados em componentes estruturais que exigem tenacidade e resistência a impacto."),
            ("Normas técnicas e especificações", "A produção segue normas ABNT NBR 6589/6916, DIN 1691/1693, ISO 185/1083 e ASTM A48/A536. Cada classe de ferro fundido tem composição química específica controlada por espectrômetro, garantindo repetibilidade entre lotes."),
            ("Verticalização fundição e usinagem", "A integração dos processos de fundição e usinagem CNC no mesmo parque fabril elimina retrabalhos, reduz lead time e assegura controle total da qualidade. Peças prontas com única responsabilidade contratual."),
            ("Como solicitar orçamento de peças fundidas", "Envie o desenho técnico (DWG, PDF, STEP ou IGES) ou amostra física para análise gratuita. Nossa engenharia avalia o projeto e retorna com especificação do material, processo e prazo em até 48 horas úteis."),
        ],
        "bombeamento": [
            ("Componentes críticos para bombeamento de concreto", "As peças mais solicitadas incluem válvulas S, anéis de desgaste, cilindros de concreto, abraçadeiras, cotovelos e reduções. Todos fabricados em ferro fundido nodular GGG50 com tratamento térmico para resistir à abrasão intensa do concreto bombeado a pressões de até 85 bar."),
            ("Materiais e resistência ao desgaste", "O ferro nodular GGG50 é o padrão da indústria por oferecer alta tenacidade combinada com resistência ao desgaste abrasivo. Para aplicações severas, ligas com adição de cromo (Cr) e molibdênio (Mo) prolongam a vida útil em até 40%."),
            ("Manutenção preventiva e vida útil", "Recomenda-se inspeção visual a cada 500 m³ bombeados, com verificação de folgas e medição de espessura nas zonas de maior desgaste. A substituição programada evita paradas não planejadas e danos a componentes adjacentes."),
            ("Vantagens do ferro fundido em sistemas de bombeamento", "O ferro fundido oferece amortecimento de vibrações superior ao aço, menor custo de fabricação, excelente usinabilidade e resistência à corrosão em ambientes alcalinos do concreto."),
            ("Especificação de peças para reposição", "Informe modelo da bomba, ano de fabricação, diâmetro dos cilindros e pressão de trabalho. Peças não padronizadas podem ser fabricadas sob medida a partir de desenho técnico ou amostra."),
        ],
        "tratores": [
            ("Peças agrícolas em ferro fundido: durabilidade no campo", "Cubos de roda, mancais, polias, engrenagens e carcaças de transmissão são componentes críticos fabricados em ferro fundido nodular GGG50, que oferece resistência mecânica de 500 MPa com excelente resistência à corrosão e ao impacto."),
            ("Vantagens do ferro nodular no agronegócio", "Comparado ao aço, o ferro nodular oferece menor custo por peça, melhor resistência à corrosão em ambientes rurais, capacidade de amortecimento de impactos e facilidade de usinagem para manutenção."),
            ("Como especificar peças para máquinas agrícolas", "Identifique o modelo do equipamento, ano, número de série do componente e condições de operação (carga, rotação, ambiente). Peças críticas como cubos e mancais exigem certificação de composição química e ensaio de dureza."),
            ("Manutenção de componentes agrícolas", "A inspeção periódica de folgas em mancais e cubos, verificação de trincas e medição de dureza após uso prolongado evita falhas catastróficas durante a safra."),
        ],
        "compressores": [
            ("Componentes de compressores de ar em ferro fundido", "Cilindros, cabeçotes, pistões, camisas e anéis de segmento são fabricados em ferro fundido cinzento GG25 para corpo e nodular GGG50 para componentes móveis. Cada material é selecionado conforme a função térmica e mecânica na montagem."),
            ("Processo de fabricação de peças para compressores", "A fundição em areia verde ou cold box garante precisão dimensional adequada, seguida de usinagem CNC com tolerâncias de até 0,005 mm nas superfícies de vedação. O controle de qualidade inclui ensaio de estanqueidade e medição tridimensional."),
            ("Critérios de seleção de materiais", "Para cilindros e cabeçotes: ferro cinzento GG25 (resistência à tração 250 MPa, dureza 180-220 HB). Para anéis de segmento: ferro nodular GGG50 (resistência 500 MPa, alongamento 7%). A escolha incorreta do material reduz drasticamente a vida útil do compressor."),
        ],
        "automotivo": [
            ("Processo produtivo de autopeças em ferro fundido", "A fabricação começa com a seleção da liga conforme especificação do cliente — ferro cinzento para blocos e cabeçotes, nodular para componentes estruturais e bielas. A fusão em forno de indução garante homogeneidade química, seguida de moldagem, vazamento e usinagem CNC."),
            ("Controle de qualidade na indústria automotiva", "Cada lote passa por análise química por espectrômetro, ensaio metalográfico, medição dimensional automatizada e ensaio de dureza. A rastreabilidade é mantida do recebimento da matéria-prima à expedição."),
            ("Certificações exigidas no setor", "Além da ISO 9001, fornecedores automotivos devem atender IATF 16949 e requisitos específicos de montadoras como VDA 6.3 e CQI-9 para tratamento térmico."),
        ],
        "geral": [
            ("O que considerar ao escolher um fornecedor de peças em ferro fundido", "Avalie certificações (ISO 9001), laboratório próprio, capacidade produtiva, verticalização dos processos, tempo de mercado, referências de clientes e suporte técnico. Fornecedores que integram fundição e usinagem oferecem vantagens competitivas significativas."),
            ("Processo produtivo: da matéria-prima à entrega", "O fluxo completo inclui recebimento e inspeção de matérias-primas, fusão em forno de indução com ajuste de composição química, moldagem (areia verde, pep set ou cold box), vazamento, resfriamento, rebarbação, tratamento térmico, usinagem CNC e controle de qualidade final."),
            ("Vantagens da verticalização industrial", "Empresas com fundição e usinagem próprias oferecem lead time reduzido, eliminação de retrabalhos de interface entre terceiros, controle total do processo e responsabilidade única sobre a qualidade final da peça."),
            ("Como solicitar cotação e prazos", "Envie desenho técnico em DWG, PDF, STEP ou IGES, ou amostra física para engenharia reversa. Nossa equipe analisa e retorna com especificação de material, processo e orçamento em até 48 horas úteis."),
        ],
    }

    qs = generate_faq(slug, title)
    sections_data = h2s.get(cat, h2s["geral"])
    sections = []
    for i, (h2_text, body_text) in enumerate(sections_data):
        html = f"<h2>{h2_text}</h2>{p(body_text)}"
        sections.append(html)

    faq_html = h2("Perguntas frequentes")
    for q, a in qs:
        faq_html += h3(q) + p(a)
    sections.append(faq_html)

    return sections, qs


def build_json(num, slug, title):
    body_parts, faq = generate_content(num, slug, title)

    content = [hero_section(title)]
    for i, sec in enumerate(body_parts):
        content.append(body_section(sec, use_bg=(i % 2 == 1)))
        if i == 0:
            content.append(cta_section())
    content.append(schema_section(slug, title))

    return {
        "title": title[:60],
        "type": "page",
        "content": content,
        "page_settings": {},
        "version": "0.5"
    }


def main():
    print("Gerando 58 artigos com conteúdo 100% original...\n")

    for num, slug, title in ARTICLES:
        data = build_json(num, slug, title)
        filename = f"{num:02d}-blog-{slug}.json"
        filepath = os.path.join(NOVOS_DIR if num >= 24 else RETRABALHO_DIR, filename)
        folder = "retrabalho" if num <= 23 else "novos"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        sec_count = len(data["content"])
        print(f"  [{folder:>10}] #{num:02d} {filename[:50]:50s} | {sec_count} secoes")

    print(f"\nConcluido! {len(ARTICLES)} artigos gerados.")
    print(f"  - retrabalho/: artigos 01-23 ({len([a for a in ARTICLES if a[0] <= 23])})")
    print(f"  - novos/:     artigos 24-58 ({len([a for a in ARTICLES if a[0] >= 24])})")
    print("\nConteudo 100% original — nenhum texto da agencia foi utilizado.")
    print("Nenhuma imagem inline foi inserida — apenas hero no cabecalho.")


if __name__ == "__main__":
    main()
