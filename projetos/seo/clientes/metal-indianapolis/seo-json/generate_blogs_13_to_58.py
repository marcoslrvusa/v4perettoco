#!/usr/bin/env python3
"""Generate Elementor JSON files for blog articles 13 to 58."""

import json
import os
import re
import uuid

DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(DIR, "Blog")
POSTS_FILE = "/tmp/all_posts.json"

HERO_IMG = "https://preview.indianapolis.com.br/wp-content/uploads/2026/05/fundicao-metal-indianapolis-hero.webp"
CONTATO_URL = "https://preview.indianapolis.com.br/contato/"

IMAGES = [
    ("https://cdn.pixabay.com/photo/2019/09/05/01/31/iron-4452869_1280.jpg", "Fundição de ferro fundido na Metal Indianápolis - vazamento de metal"),
    ("https://cdn.pixabay.com/photo/2017/03/01/17/51/crucible-2109202_640.jpg", "Cadinho com metal fundido na indústria metalúrgica"),
    ("https://cdn.pixabay.com/photo/2015/08/03/20/07/factory-873839_640.jpg", "Fábrica de fundição industrial - estrutura metalúrgica"),
    ("https://cdn.pixabay.com/photo/2015/08/03/20/06/factory-873837_640.jpg", "Indústria metalúrgica de fundição e usinagem"),
    ("https://cdn.pixabay.com/photo/2016/01/20/11/10/milling-1151344_1280.jpg", "Usinagem CNC de peças em ferro fundido"),
    ("https://cdn.pixabay.com/photo/2018/10/11/04/57/milling-cutters-3738903__340.jpg", "Ferramentas de fresagem para usinagem de precisão"),
    ("https://cdn.pixabay.com/photo/2020/07/28/20/13/machine-5446222_1280.jpg", "Máquina CNC na fabricação de peças industriais"),
    ("https://cdn.pixabay.com/photo/2021/05/17/11/24/lathe-6260379__340.jpg", "Torno mecânico para usinagem de precisão"),
    ("https://images.unsplash.com/photo-1533473359331-0135ef1b58d6?auto=format&fit=crop&w=1200", "Indústria automotiva - linha de produção e componentes"),
    ("https://cdn.pixabay.com/photo/2016/01/20/10/55/milling-1151323__340.jpg", "Fresagem de precisão em componentes de ferro fundido"),
]


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


def make_hero_section(title, intro_text):
    heading = make_widget("heading", {
        "title": title,
        "header_size": "h1",
        "typography_typography": "custom",
        "typography_font_family": "Sora",
        "typography_font_size": {"unit": "px", "size": 42},
        "typography_font_weight": "700",
        "title_color": "#FFFFFF",
        "align": "left"
    })
    text = make_widget("text-editor", {
        "editor": f"<p>{intro_text}</p>",
        "typography_typography": "custom",
        "typography_font_family": "Sora",
        "typography_font_size": {"unit": "px", "size": 16},
        "typography_font_weight": "300",
        "text_color": "#FFFFFF"
    })
    return make_outer_container(get_hero_settings(), [heading, text])


def make_body_section(html_content, use_bg=False):
    text = make_widget("text-editor", {
        "editor": html_content,
        "typography_typography": "custom",
        "typography_font_family": "Sora",
        "typography_font_size": {"unit": "px", "size": 16},
        "typography_font_weight": "300",
        "text_color": "#444444"
    })
    return make_outer_container(get_body_settings(use_bg), [text])


def make_cta_section():
    heading = make_widget("heading", {
        "title": "Solicite sua cotação em até 48 horas úteis",
        "header_size": "h2",
        "typography_typography": "custom",
        "typography_font_family": "Sora",
        "typography_font_size": {"unit": "px", "size": 36},
        "typography_font_weight": "700",
        "title_color": "#FFFFFF",
        "align": "center"
    })
    text = make_widget("text-editor", {
        "editor": "<p style=\"text-align: center;\">Envie seu desenho técnico (DWG, PDF, STEP, IGES) ou amostra física para análise gratuita. Nossa engenharia avalia o projeto e retorna com orçamento em até 48 horas úteis.</p>",
        "typography_typography": "custom",
        "typography_font_family": "Sora",
        "typography_font_size": {"unit": "px", "size": 16},
        "typography_font_weight": "300",
        "text_color": "#FFFFFF"
    })
    button = make_widget("button", {
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
    return make_outer_container(get_cta_settings(), [heading, text, button])


def make_schema_section():
    html = make_widget("html", {"editor": ""})
    return make_outer_container(
        {"flex_direction": "column", "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}},
        [html]
    )


def clean_html(html):
    """Remove empty paragraphs and normalize whitespace."""
    html = re.sub(r'<p[^>]*>\s*</p>', '', html)
    html = re.sub(r'\s+', ' ', html).strip()
    return html


def split_html_into_chunks(html, num_chunks=2):
    """Split HTML content into roughly equal chunks by paragraph count.
    Skips the first paragraph (already used as intro in hero)."""
    paragraphs = re.findall(r'(<p[^>]*>.*?</p>)', html, re.DOTALL)
    if not paragraphs:
        return [html]

    # Skip first paragraph (used as intro)
    body_paras = paragraphs[1:]
    if not body_paras:
        return ['']

    total = len(body_paras)
    chunk_size = max(1, total // num_chunks)
    chunks = [''] * num_chunks

    for i in range(num_chunks):
        start = i * chunk_size
        if i == num_chunks - 1:
            end = total
        else:
            end = start + chunk_size
        chunks[i] = ''.join(body_paras[start:end])

    return [c for c in chunks if c.strip()]


def get_intro_text(html):
    """Extract first meaningful paragraph as intro text."""
    match = re.search(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    if match:
        text = re.sub(r'<[^>]+>', '', match.group(1))
        text = re.sub(r'&nbsp;', ' ', text).strip()
        if len(text) > 300:
            text = text[:297] + '...'
        return text
    return ""


def make_image_section(img_url, alt_text):
    img_widget = make_widget("image", {
        "image": {"url": img_url, "id": "", "alt": alt_text, "source": "external"},
        "width": {"unit": "%", "size": 100},
        "align": "center",
        "image_size": "full",
        "caption_source": "none"
    })
    return make_outer_container(
        {"flex_direction": "column", "padding": {"unit": "px", "top": "30", "right": "50", "bottom": "30", "left": "50", "isLinked": False}},
        [img_widget]
    )


def generate_blog(data, post_index):
    slug = data["slug"]
    title = data["title"]["rendered"]
    html_content = data["content"]["rendered"]
    html_content = clean_html(html_content)

    intro = get_intro_text(html_content)

    sections = []
    sections.append(make_hero_section(title, intro))

    # Split content into chunks and add with alternating background
    chunks = split_html_into_chunks(html_content, 3)
    for i, chunk in enumerate(chunks):
        sections.append(make_body_section(chunk, use_bg=(i % 2 == 1)))

    # Add CTA in the middle (after first chunk, before last)
    # Since we have 3 chunks, insert CTA after chunk 1 (index 2 currently)
    cta_section = make_cta_section()
    insert_pos = min(2, len(sections))
    sections.insert(insert_pos, cta_section)

    sections.append(make_schema_section())

    blog_data = {
        "title": title,
        "type": "page",
        "content": sections,
        "page_settings": {},
        "version": "0.4"
    }

    return blog_data


def main():
    with open(POSTS_FILE) as f:
        all_posts = json.load(f)

    # Skip first 12 posts (already have JSON files for articles 01-12)
    # Remaining posts (index 12+) are articles 13-58
    new_posts = all_posts[12:]

    print(f"Total posts in API: {len(all_posts)}")
    print(f"New posts to generate: {len(new_posts)}")

    for idx, post in enumerate(new_posts):
        blog_data = generate_blog(post, idx)
        slug = post["slug"]
        blog_number = idx + 13
        filename = f"{blog_number:02d}-blog-{slug}.json"
        filepath = os.path.join(BLOG_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(blog_data, f, ensure_ascii=False)

        print(f"  #{blog_number:02d}: {filename} ({len(json.dumps(blog_data))} bytes)")

    print(f"\nGenerated {len(new_posts)} new blog files!")


if __name__ == "__main__":
    main()
