#!/usr/bin/env python3
"""Add free-use image widgets into blog Elementor JSON files."""

import json
import os
import copy
import uuid

DIR = os.path.dirname(os.path.abspath(__file__))

# Free-license image URLs (Pixabay + Unsplash, all CC0/Unsplash license verified)
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
}

# Blog-to-images mapping: filename_suffix -> [image_key, alt_text, image_key2, alt_text2]
BLOG_IMAGES = {
    "05-blog-ferro-fundido-cinzento": {
        "img1": ("foundry1", "Fundição de ferro fundido cinzento na Metal Indianápolis - processo de vazamento de ferro"),
        "img2": ("foundry2", "Cadinho e metal fundido na indústria de fundição de ferros"),
    },
    "06-blog-preco-ferro-fundido-kg": {
        "img1": ("factory1", "Fábrica de fundição de ferro com estrutura metálica industrial"),
        "img2": ("factory2", "Indústria metalúrgica de fundição de ferro e metais"),
    },
    "07-blog-fabrica-roldanas": {
        "img1": ("milling1", "Máquina fresadora CNC na usinagem de peças de ferro fundido"),
        "img2": ("milling2", "Ferramentas de corte e fresagem para usinagem de precisão"),
    },
    "08-blog-camisa-compressor": {
        "img1": ("lathe1", "Torno mecânico para usinagem de camisas de compressor em ferro fundido"),
        "img2": ("milling1", "Usinagem CNC de precisão para componentes de compressor"),
    },
    "09-blog-cabecote-compressor": {
        "img1": ("cnc1", "Máquina CNC perfurada para fabricação de cabeçotes de compressor"),
        "img2": ("metal1", "Fresagem de precisão em componentes industriais de ferro fundido"),
    },
    "10-blog-anel-segmento-motor": {
        "img1": ("engine1", "Anéis de segmento e peças de motor automotivo em ferro fundido"),
        "img2": ("engine2", "Pistões e anéis de segmento visíveis em motor de combustão"),
    },
    "11-blog-anel-segmento-preco": {
        "img1": ("engine2", "Pistões de motor com anéis de segmento em ferro fundido"),
        "img2": ("engine1", "Componentes automotivos em ferro fundido - anéis de segmento"),
    },
    "12-blog-preco-ferro-fundido": {
        "img1": ("foundry1", "Vazamento de ferro fundido na indústria metalúrgica"),
        "img2": ("factory2", "Processo industrial de fundição de ferro e metais ferrosos"),
    },
    "13-blog-pecas-tratores": {
        "img1": ("tractor1", "Trator agrícola e equipamentos no campo - peças em ferro fundido"),
        "img2": ("tractor2", "Trator verde com implementos agrícolas no campo"),
        "img3": ("tractor3", "Trator agrícola em atividade no campo - componentes fundidos"),
    },
    "14-blog-fundicao-ferros": {
        "img1": ("foundry1", "Fundição de ferro - vazamento de metal fundido na indústria"),
        "img2": ("foundry2", "Processo de fundição em cadinho na metalurgia industrial"),
    },
    "15-blog-anel-segmento": {
        "img1": ("engine1", "Anéis de segmento para motor - componentes automotivos de ferro fundido"),
        "img2": ("engine2", "Pistões automotivos com anéis de segmento - aplicação em motores"),
    },
    "16-blog-fabricante-automotivo": {
        "img1": ("automotive1", "Fabricante automotivo - linha de produção industrial"),
        "img2": ("engine1", "Componentes automotivos em ferro fundido para indústria"),
    },
}


def make_image_widget(img_url, alt_text, widget_id=None):
    """Create an Elementor image widget dict."""
    if widget_id is None:
        widget_id = uuid.uuid4().hex[:10]
    return {
        "id": widget_id,
        "settings": {
            "image": {
                "url": img_url,
                "id": "",
                "alt": alt_text,
                "source": "external"
            },
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
    """Create an outer container wrapping an inner container + image widget."""
    inner_id = uuid.uuid4().hex[:10]
    outer_id = uuid.uuid4().hex[:10]
    widget_id = uuid.uuid4().hex[:10]
    return {
        "id": outer_id,
        "settings": {
            "flex_direction": "column",
            "padding": {
                "unit": "px",
                "top": "30",
                "right": "50",
                "bottom": "30",
                "left": "50",
                "isLinked": False
            }
        },
        "elements": [
            {
                "id": inner_id,
                "settings": {"content_width": "full"},
                "elements": [make_image_widget(img_url, alt_text, widget_id)],
                "elType": "container",
                "isInner": True
            }
        ],
        "elType": "container",
        "isInner": False
    }


def has_image_widget(container):
    """Check if a container has an image widget inside."""
    for el in container.get("elements", []):
        for w in el.get("elements", []):
            if w.get("widgetType") == "image":
                return True
    return False


def process_blog(filename, images_cfg):
    filepath = os.path.join(DIR, filename)
    if not os.path.exists(filepath):
        print(f"  SKIP: {filename} not found")
        return

    with open(filepath, "r") as f:
        data = json.load(f)

    content = data.get("content", [])

    # Remove any existing image-widget containers first
    content = [c for c in content if not has_image_widget(c)]

    img_keys = sorted([k for k in images_cfg.keys() if k.startswith("img")])

    # Insert images in reverse order so indices don't shift
    # img1 -> position 1 (after hero), img2+ -> appended to end
    positions = []
    for i in range(len(img_keys)):
        if i == 0:
            positions.append(1)  # after hero
        else:
            positions.append(len(content) + i - 1)  # append to end

    for i, pos in enumerate(reversed(positions)):
        key = img_keys[-(i + 1)]
        img_key, alt_text = images_cfg[key]
        img_url = IMAGES[img_key]
        container = make_image_container(img_url, alt_text)
        content.insert(min(pos, len(content)), container)

    data["content"] = content

    with open(filepath, "w") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"  OK: {filename} ({len(img_keys)} imagens adicionadas)")


def main():
    print("Adicionando imagens nos 12 blog posts...")
    for blog_base, cfg in BLOG_IMAGES.items():
        filename = f"{blog_base}.json"
        process_blog(filename, cfg)
    print("\nConcluído!")


if __name__ == "__main__":
    main()
