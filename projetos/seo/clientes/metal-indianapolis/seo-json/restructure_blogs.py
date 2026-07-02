#!/usr/bin/env python3
"""Restructure blogs 11-16: one container per section, matching blog 05 pattern."""

import json
import copy
import uuid
import os
from glob import glob

DIR = os.path.dirname(os.path.abspath(__file__))


def make_container(settings, elements):
    return {
        "id": uuid.uuid4().hex[:10],
        "settings": settings,
        "elements": elements,
        "elType": "container",
        "isInner": False
    }


def make_inner(elements):
    return {
        "id": uuid.uuid4().hex[:10],
        "settings": {"content_width": "full"},
        "elements": elements,
        "elType": "container",
        "isInner": True
    }


def rebuild_blog(data):
    content = data.get("content", [])
    if not content:
        return data

    all_widgets = []
    for container in content:
        for el in container.get("elements", []):
            for w in el.get("elements", []):
                all_widgets.append(copy.deepcopy(w))

    images = [w for w in all_widgets if w.get("widgetType") == "image"]
    htmls = [w for w in all_widgets if w.get("widgetType") == "html"]
    buttons = [w for w in all_widgets if w.get("widgetType") == "button"]
    rest = [w for w in all_widgets if w.get("widgetType") not in ("image", "html", "button")]

    # Group into sections: heading + following text-editors
    sections = []
    i = 0
    while i < len(rest):
        w = rest[i]
        if w.get("widgetType") == "heading":
            sec = [w]
            i += 1
            while i < len(rest) and rest[i].get("widgetType") == "text-editor":
                sec.append(rest[i])
                i += 1
            sections.append(sec)
        else:
            i += 1

    if not sections:
        return data

    # Classify each section
    hero = sections[0]
    body = []
    faq = None
    cta = None

    for sec in sections[1:]:
        title = sec[0].get("settings", {}).get("title", "").lower()
        if "perguntas frequentes" in title or "faq" in title:
            faq = sec
        elif "como solicitar" in title or "solicite" in title or "orçamento" in title:
            cta = sec
        else:
            body.append(sec)

    new_content = []

    # [0] Hero
    hero_settings = {
        "flex_direction": "column",
        "background_background": "classic",
        "background_image": {"url": "https://preview.indianapolis.com.br/wp-content/uploads/2026/05/fundicao-metal-indianapolis-hero.webp", "id": 356, "alt": "", "source": "library"},
        "background_overlay_background": "classic",
        "background_overlay_color": "rgba(0,0,0,0.6)",
        "background_position": "center center",
        "background_size": "cover",
        "background_repeat": "no-repeat",
        "min_height": {"unit": "px", "size": 480},
        "padding": {"unit": "px", "top": "200", "right": "50", "bottom": "60", "left": "50", "isLinked": False}
    }
    new_content.append(make_container(hero_settings, [make_inner(hero)]))

    # [1] First image
    if images:
        img_settings = {
            "flex_direction": "column",
            "padding": {"unit": "px", "top": "30", "right": "50", "bottom": "30", "left": "50", "isLinked": False}
        }
        new_content.append(make_container(img_settings, [make_inner([images[0]])]))

    # [2..n] Body sections (no bg, bg, no bg, bg...)
    for idx, sec in enumerate(body):
        use_bg = idx % 2 == 1  # odd sections get bg (first body section has no bg)
        sec_settings = {
            "flex_direction": "column",
            "padding": {"unit": "px", "top": "30", "right": "50", "bottom": "30", "left": "50", "isLinked": False}
        }
        if use_bg:
            sec_settings["background_background"] = "classic"
            sec_settings["background_color"] = "#F9F9F9"
        new_content.append(make_container(sec_settings, [make_inner(sec)]))

    # FAQ
    if faq:
        faq_settings = {
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "#F9F9F9",
            "padding": {"unit": "px", "top": "40", "right": "50", "bottom": "40", "left": "50", "isLinked": False}
        }
        new_content.append(make_container(faq_settings, [make_inner(faq)]))

    # CTA
    cta_all = (cta or []) + buttons
    if cta_all:
        cta_settings = {
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "#F9F9F9",
            "padding": {"unit": "px", "top": "60", "right": "50", "bottom": "60", "left": "50", "isLinked": False}
        }
        new_content.append(make_container(cta_settings, [make_inner(cta_all)]))

    # Schema
    if htmls:
        schema_settings = {
            "flex_direction": "column",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
        }
        new_content.append(make_container(schema_settings, [make_inner(htmls)]))

    # Second image
    if len(images) > 1:
        img2_settings = {
            "flex_direction": "column",
            "padding": {"unit": "px", "top": "30", "right": "50", "bottom": "30", "left": "50", "isLinked": False}
        }
        new_content.append(make_container(img2_settings, [make_inner([images[1]])]))

    data["content"] = new_content
    return data


def main():
    files = sorted(glob(f"{DIR}/[0-9][0-9]-blog-*.json"))
    target = [f for f in files if any(f"/{n}-blog-" in f for n in range(11, 17))]

    print(f"Reestruturando {len(target)} blogs...\n")
    for fpath in target:
        name = os.path.basename(fpath)
        with open(fpath) as f:
            data = json.load(f)
        old_n = len(data.get("content", []))
        data = rebuild_blog(data)
        new_n = len(data.get("content", []))
        with open(fpath, "w") as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"  {name}: {old_n} containers -> {new_n} containers")
    print("\nConcluido!")


if __name__ == "__main__":
    main()
