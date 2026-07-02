#!/usr/bin/env python3
"""Inject expanded HTML content into article JSONs.

Reads expansions from a JSON file mapping slug -> [section_html, ...]
and replaces the body of each text-editor widget in the matching article.
"""
import os, sys, json, re

DIR = "/home/marcos/Desktop/AI/v4perettoco-main/projetos/seo/clientes/metal-indianapolis/seo-json/raw-files-v3"

def find_article(slug):
    for subdir in ("retrabalho", "novos"):
        for f in os.listdir(os.path.join(DIR, subdir)):
            if slug in f and f.endswith('.json'):
                return os.path.join(DIR, subdir, f)
    return None

def inject(path, sections_html):
    with open(path) as f:
        data = json.load(f)
    sec_idx = 0
    for c in data.get("content", []):
        for el in c.get("elements", []):
            for w in el.get("elements", []):
                ed = w.get("settings", {}).get("editor", "")
                if isinstance(ed, str) and '<h2>' in ed and sec_idx < len(sections_html):
                    w["settings"]["editor"] = sections_html[sec_idx]
                    sec_idx += 1
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    return sec_idx

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: inject_expansions.py <expansions.json>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        expansions = json.load(f)
    for slug, sections_html in expansions.items():
        path = find_article(slug)
        if not path:
            print(f"NOT FOUND: {slug}")
            continue
        n = inject(path, sections_html)
        print(f"OK {slug}: {n} sections updated")
