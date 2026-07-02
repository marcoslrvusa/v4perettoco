#!/usr/bin/env python3
"""Insert inline image widgets into EEAT-generated blog JSON files (13-58)."""

import json
import os
import uuid

DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(DIR, "Blog")

IMAGES = {
    "foundry1": "https://cdn.pixabay.com/photo/2019/09/05/01/31/iron-4452869_1280.jpg",
    "foundry2": "https://cdn.pixabay.com/photo/2017/03/01/17/51/crucible-2109202_640.jpg",
    "factory1": "https://cdn.pixabay.com/photo/2015/08/03/20/07/factory-873839_640.jpg",
    "factory2": "https://cdn.pixabay.com/photo/2015/08/03/20/06/factory-873837_640.jpg",
    "milling1": "https://cdn.pixabay.com/photo/2016/01/20/11/10/milling-1151344_1280.jpg",
    "milling2": "https://cdn.pixabay.com/photo/2018/10/11/04/57/milling-cutters-3738903__340.jpg",
    "cnc1": "https://cdn.pixabay.com/photo/2020/07/28/20/13/machine-5446222_1280.jpg",
    "lathe1": "https://cdn.pixabay.com/photo/2021/05/17/11/24/lathe-6260379__340.jpg",
    "engine1": "https://images.unsplash.com/photo-1739488754789-5a2e85ee6a79?auto=format&fit=crop&w=1200",
    "engine2": "https://images.unsplash.com/photo-1742729096825-ebbcc50dea65?auto=format&fit=crop&w=1200",
    "tractor1": "https://images.unsplash.com/photo-1748119920170-36357c35066d?auto=format&fit=crop&w=1200",
    "tractor2": "https://images.unsplash.com/photo-1774291635198-fba0031e630a?auto=format&fit=crop&w=1200",
    "tractor3": "https://images.unsplash.com/photo-1779287340324-f42e09de2f2d?auto=format&fit=crop&w=1200",
    "automotive1": "https://images.unsplash.com/photo-1533473359331-0135ef1b58d6?auto=format&fit=crop&w=1200",
    "metal1": "https://cdn.pixabay.com/photo/2016/01/20/10/55/milling-1151323__340.jpg",
    "construction1": "https://cdn.pixabay.com/photo/2019/08/05/11/28/concrete-4385987_1280.jpg",
    "construction2": "https://cdn.pixabay.com/photo/2018/05/02/21/03/construction-site-3370731_1280.jpg",
    "industry1": "https://cdn.pixabay.com/photo/2019/12/15/16/46/industry-4697562_1280.jpg",
    "engineering1": "https://cdn.pixabay.com/photo/2020/04/13/15/55/measurement-5040461_1280.jpg",
}

CATEGORY_IMAGES = {
    "aneis": [
        ("engine1", "Anéis de segmento em ferro fundido para compressores e motores industriais"),
        ("engine2", "Componentes automotivos com anéis de segmento em ferro fundido"),
        ("milling1", "Usinagem de precisão de anéis de segmento em ferro fundido"),
    ],
    "bombeamento": [
        ("construction1", "Peças para bombeamento de concreto em ferro fundido"),
        ("construction2", "Sistema de bombeamento de concreto com componentes fundidos"),
        ("foundry1", "Fundição de peças para bombeamento de concreto"),
    ],
    "abracadeiras": [
        ("construction1", "Abraçadeiras para tubulação de concreto em ferro fundido"),
        ("construction2", "Conexões e abraçadeiras para sistema de bombeamento"),
        ("metal1", "Fabricação de abraçadeiras em ferro fundido nodular"),
    ],
    "compressores": [
        ("cnc1", "Peças para compressor de ar em ferro fundido usinadas CNC"),
        ("lathe1", "Usinagem de cabeçotes e cilindros para compressor"),
        ("milling1", "Componentes de compressor em ferro fundido cinzento"),
    ],
    "tratores": [
        ("tractor1", "Peças agrícolas em ferro fundido para tratores"),
        ("tractor2", "Componentes fundidos para tratores agrícolas"),
        ("tractor3", "Peças de reposição para tratores em ferro fundido"),
    ],
    "fundicao-geral": [
        ("foundry1", "Fundição de ferro fundido - vazamento de metal na indústria"),
        ("factory1", "Indústria de fundição de ferro - estrutura metalúrgica"),
        ("milling1", "Usinagem de peças em ferro fundido"),
    ],
    "fundicao-autopecas": [
        ("automotive1", "Autopeças em ferro fundido para indústria automotiva"),
        ("engine1", "Componentes automotivos fundidos em ferro"),
        ("foundry1", "Fundição de autopeças em ferro fundido"),
    ],
    "fundicao-cinzento": [
        ("foundry1", "Ferro fundido cinzento - processo de vazamento industrial"),
        ("factory1", "Indústria de fundição de ferro cinzento GG20 e GG25"),
        ("milling1", "Usinagem de peças em ferro fundido cinzento"),
    ],
    "fundicao-servicos": [
        ("foundry1", "Serviço de fundição de ferro fundido industrial"),
        ("factory2", "Empresa de fundição de ferro - parque fabril"),
        ("cnc1", "Usinagem CNC como serviço agregado à fundição"),
    ],
    "fundicao-pep-set": [
        ("factory1", "Fundição em pep set - processo de moldagem industrial"),
        ("foundry2", "Processo de fundição em pep set para peças de médio porte"),
    ],
    "empresa": [
        ("factory1", "Empresa de fundição de ferro fundido com ISO 9001"),
        ("factory2", "Indústria metalúrgica de fundição - estrutura industrial"),
        ("cnc1", "Fundição com usinagem própria - verticalização industrial"),
    ],
    "auto-pecas": [
        ("automotive1", "Fábrica de peças automotivas em ferro fundido"),
        ("engine1", "Componentes automotivos fundidos - blocos e cabeçotes"),
        ("engine2", "Peças para indústria automotiva em ferro fundido"),
    ],
    "fabricante-industrial": [
        ("industry1", "Fabricante de peças industriais em ferro fundido"),
        ("foundry1", "Fundição de peças industriais - processo produtivo"),
        ("cnc1", "Fabricação de peças para máquinas e equipamentos"),
    ],
    "pecas-ferro": [
        ("foundry1", "Fabricação de peças em ferro fundido sob encomenda"),
        ("milling1", "Usinagem de peças de ferro fundido para indústria"),
        ("factory1", "Produção de peças em ferro fundido cinzento e nodular"),
    ],
    "cubos-mancais": [
        ("milling2", "Cubos e mancais em ferro fundido para máquinas"),
        ("lathe1", "Usinagem de cubos e mancais industriais"),
        ("metal1", "Componentes de cubos e mancais em ferro fundido"),
    ],
    "rolos": [
        ("milling1", "Rolos de apoio para betoneiras em ferro fundido"),
        ("foundry1", "Fundição de rolos e cilindros para equipamentos"),
        ("factory1", "Fabricação de rolos de apoio industriais"),
    ],
    "industria-metalurgica": [
        ("industry1", "Indústria metalúrgica de peças automotivas"),
        ("foundry1", "Metalurgia de ferro fundido para autopeças"),
        ("factory1", "Indústria metalúrgica - fundição e usinagem"),
    ],
    "fornecedor-aneis": [
        ("engine1", "Fornecedor de anéis de segmento em ferro fundido"),
        ("engine2", "Anéis de segmento para compressores - fornecimento industrial"),
        ("milling1", "Fabricação de anéis de segmento sob medida"),
    ],

    "geral": [
        ("foundry1", "Fundição de ferro fundido - processo industrial"),
        ("factory1", "Indústria de fundição de ferro fundido"),
        ("milling1", "Usinagem de precisão em ferro fundido"),
    ],
}


def make_id():
    return uuid.uuid4().hex[:10]


def make_image_widget(img_url, alt_text):
    return {
        "id": make_id(),
        "settings": {
            "image": {"url": img_url, "id": "", "alt": alt_text, "source": "external"},
            "width": {"unit": "%", "size": 100},
            "align": "center",
            "image_size": "full",
            "caption_source": "none",
            "hover_animation": "grow",
            "_animation": "fadeInUp",
            "link_to": "none",
            "open_lightbox": "yes"
        },
        "elements": [],
        "isInner": False,
        "widgetType": "image",
        "elType": "widget"
    }


def make_image_container(img_url, alt_text):
    outer_id = make_id()
    inner_id = make_id()
    return {
        "id": outer_id,
        "settings": {
            "flex_direction": "column",
            "padding": {"unit": "px", "top": "30", "right": "50", "bottom": "30", "left": "50", "isLinked": False}
        },
        "elements": [
            {
                "id": inner_id,
                "settings": {"content_width": "full"},
                "elements": [make_image_widget(img_url, alt_text)],
                "elType": "container",
                "isInner": True
            }
        ],
        "elType": "container",
        "isInner": False
    }


def has_image_widget(container):
    for el in container.get("elements", []):
        for w in el.get("elements", []):
            if w.get("widgetType") == "image":
                return True
    return False


# Fallback image mappings for categories not explicitly listed
CATEGORY_IMAGES["fornecedor-aneis"] = CATEGORY_IMAGES["aneis"]
CATEGORY_IMAGES["fundicao-pep-set"] = CATEGORY_IMAGES["fundicao-servicos"]


def detect_category(filename):
    t = filename.lower()
    if any(w in t for w in ["anel", "aneis", "segmento", "pistao", "bronze", "bomba-vacuo", "fornecedor-aneis", "fabricante-aneis"]):
        return "aneis" if "fornecedor" not in t and "fabricante-aneis" not in t else "fornecedor-aneis"
    if "abracadeira" in t:
        return "abracadeiras"
    if any(w in t for w in ["fundicao-de-auto", "fundicao-de-autopecas", "fundicao autopecas"]):
        return "fundicao-autopecas"
    if any(w in t for w in ["fundicao-de-ferro-cinzento", "fundicao ferro-fundido-cinzento"]):
        return "fundicao-cinzento"
    if any(w in t for w in ["fundicao-de-ferro-em-itaquaquecetuba", "fundicao-de-ferro-fundido", "fundicao-de-pecas", "fundicao-em-sao-paulo", "fundicao-ferro-fundido", "servico-de-fundicao"]):
        return "fundicao-servicos"
    if "fundicao-de-ferro-em-pep" in t:
        return "fundicao-pep-set"
    if any(w in t for w in ["pecas-para-bomba", "pecas-para-bombeamento", "pecas-para-sistema-de-bombeamento"]):
        return "bombeamento"
    if "pecas-para-tratores" in t:
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
    if any(w in t for w in ["fabricante-de-pecas-para-bombeamento", "fabricante-de-pecas-para-maquinas", "fabricante-abracadeiras"]):
        return "fabricante-industrial"
    if "rolos" in t:
        return "rolos"
    if "industria-metalurgica" in t:
        return "industria-metalurgica"
    if any(w in t for w in ["fundicao-de-ferro", "fundicao-ferro", "fundicao-geral"]):
        return "fundicao-geral"
    return "geral"


def process_blog(filepath, category):
    with open(filepath) as f:
        data = json.load(f)

    content = data.get("content", [])

    # Remove any existing image-widget containers
    content = [c for c in content if not has_image_widget(c)]

    # Get images for category
    img_list = CATEGORY_IMAGES.get(category, CATEGORY_IMAGES["geral"])

    # Insert images at strategic positions:
    # After hero (index 0), and interspersed in body sections
    # Positions: after hero (1), after first body block, etc.
    insert_positions = []
    # Skip hero [0], then find body containers (not CTA, not schema)
    body_indices = []
    for i, c in enumerate(content):
        is_cta = any(
            w.get("widgetType") == "button"
            for el in c.get("elements", [])
            for w in el.get("elements", [])
        )
        is_schema = any(
            "ld+json" in w.get("settings", {}).get("editor", "")
            for el in c.get("elements", [])
            for w in el.get("elements", [])
            if w.get("widgetType") == "html"
        )
        if i > 0 and not is_cta and not is_schema:
            body_indices.append(i)

    # Insert images after hero and in-between body sections
    if len(img_list) >= 1 and body_indices:
        insert_positions.append(body_indices[0])  # after first body
    if len(img_list) >= 2 and len(body_indices) >= 3:
        insert_positions.append(body_indices[2])  # after third body
    if len(img_list) >= 3 and len(body_indices) >= 5:
        insert_positions.append(body_indices[4])  # after fifth body

    # Insert in reverse order to preserve indices
    for i, pos in enumerate(reversed(insert_positions)):
        idx = min(i, len(img_list) - 1)
        img_key, alt_text = img_list[idx]
        img_url = IMAGES[img_key]
        container = make_image_container(img_url, alt_text)
        insert_at = min(pos, len(content))
        content.insert(insert_at, container)

    data["content"] = content

    with open(filepath, "w") as f:
        json.dump(data, f, ensure_ascii=False)

    return len(insert_positions)


def main():
    files = sorted(os.listdir(BLOG_DIR))
    total_imgs = 0
    processed = 0

    for f in files:
        if not f.endswith(".json"):
            continue
        num = int(f[:2])
        if num < 13 or num > 58:
            continue

        filepath = os.path.join(BLOG_DIR, f)
        category = detect_category(f)
        count = process_blog(filepath, category)
        total_imgs += count
        processed += 1
        print(f"  {f[:55]:55s} | cat={category:<20s} | +{count} imagens")

    print(f"\nProcessed {processed} articles, added {total_imgs} images total.")


if __name__ == "__main__":
    main()
