# -*- coding: utf-8 -*-
"""Gera a biblioteca HTML (index + 24 paginas) a partir de artigos/lote-1/*.md."""
import os, re, io, glob, json, shutil, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
LOTE = os.path.join(BASE, "artigos", "lote-1")
DEST = "/home/marcos/Desktop/v4perettoco-main/premium-artigos-novembro"
ART = os.path.join(DEST, "artigos")
SRC_LOGO = "/home/marcos/Desktop/v4perettoco-main/assets/images"

BLOCKS = {
    "A": ("Hotel & Hospitality", "Hotel e hospitalidade: produtividade, cronogramas e inspeção."),
    "B": ("Commercial & Office", "Limpeza comercial: contratos, SLA e verificação de fornecedor."),
    "C": ("Carpet & Floor Care", "Carpetes e pisos: custo, métodos, secagem e garantia."),
    "D": ("Restaurant & Kitchen", "Cozinhas: conformidade, gordura, exaustão e inspeção."),
    "E": ("Cost & Procurement", "Custo real, benchmark, orçamento e processo de compra."),
}
PENDING = {
    "B5": "Insurance, Bonding and Background Checks", "B6": "OSHA Compliance for Commercial Cleaning",
    "B7": "ATP Testing in Restrooms", "B8": "The Vendor Scorecard: 12 Metrics",
    "C5": "Interim vs Restorative Carpet Cleaning", "C6": "Coefficient of Friction: Floor Safety",
    "C7": "Stone and Terrazzo Floor Care", "C8": "Grout Sealing vs Grout Restoration",
    "E1": "The True Cost of a Dirty Office", "E2": "Cleaning Cost Benchmarks: NJ vs NYC",
    "E3": "How to Build an Annual Cleaning Budget", "E4": "The 15-Point Vendor Vetting Checklist",
    "E5": "Contract Terms That Protect the Client", "E6": "Change Orders: Outside Scope",
    "E7": "Calculating ROI on Commercial Cleaning", "E8": "Vendor Consolidation: One vs Many",
}
VOLLINK = {"A": "vol-A-hotel-hospitality", "B": "vol-B-commercial-office",
           "C": "vol-C-carpet-floor", "D": "vol-D-restaurant-kitchen", "E": "vol-E-cost-procurement"}


def parse_front(text):
    meta, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
            body = text[end + 4:]
    return meta, body.lstrip("\n")


def inline(t):
    t = H.escape(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\*\w])\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)

    def lnk(m):
        label, url = m.group(1), m.group(2)
        if url.startswith("http"):
            return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'
        return f'<span class="planned" title="URL de destino planejada no site">{label} <em>{url}</em></span>'
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lnk, t)


def render(body):
    lines = body.split("\n")
    out, i, jsonld = [], 0, []
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1; continue
        if ln.startswith("```"):
            lang = ln[3:].strip(); buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            code = "\n".join(buf)
            if lang == "json":
                try:
                    json.loads(code); jsonld.append(code)
                except Exception:
                    pass
            out.append(f'<pre class="code">{H.escape(code)}</pre>')
            continue
        if ln.lstrip().startswith("|"):
            tl = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                tl.append(lines[i].strip()); i += 1
            rows = [[c.strip() for c in l.strip("|").split("|")] for l in tl]
            rows = [r for r in rows if not all(re.fullmatch(r":?:?-{2,}:?:?", c or "") for c in r)]
            if rows:
                th = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
                tb = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
                out.append(f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
            continue
        if ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:])}</h3>"); i += 1; continue
        if ln.startswith("## "):
            out.append(f"<h2>{inline(ln[3:])}</h2>"); i += 1; continue
        if ln.startswith("# "):
            out.append(f"<h1>{inline(ln[2:])}</h1>"); i += 1; continue
        if re.match(r"^-{3,}$", ln.strip()):
            out.append("<hr>"); i += 1; continue
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ").strip()); i += 1
            out.append(f'<blockquote><p>{inline(" ".join(x for x in buf if x))}</p></blockquote>')
            continue
        if ln.lstrip().startswith("- "):
            items = []
            while i < len(lines) and lines[i].lstrip().startswith("- "):
                items.append(lines[i].lstrip()[2:]); i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s", ln.lstrip()):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].lstrip()):
                items.append(re.sub(r"^\d+\.\s", "", lines[i].lstrip())); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        m = re.fullmatch(r"\*\*([^*]+)\*\*", ln.strip())
        if m and m.group(1).rstrip().endswith("?"):
            out.append(f'<h4 class="faq-q">{inline(m.group(1))}</h4>'); i += 1; continue
        out.append(f"<p>{inline(ln.strip())}</p>"); i += 1
    return "\n".join(out), jsonld


CSS = """
:root{--ink:#151515;--paper:#fffdf8;--cream:#f7f2e7;--line:#e7e0d2;--gold:#b08a3e;--gold-dark:#8b6a2a;--red:#c8102e;--gray:#4a4a4a;--muted:#8a8a8a}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:"Montserrat",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.65}a{color:inherit}
h1,h2,h3,h4{font-family:"Montserrat",sans-serif;letter-spacing:-.6px}
.header{position:sticky;top:0;z-index:20;background:rgba(255,253,248,.94);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.header-inner{max-width:1180px;margin:0 auto;padding:12px 28px;display:flex;align-items:center;justify-content:space-between;gap:20px}
.brand{display:flex;align-items:center;gap:14px;text-decoration:none}
.brand img{height:26px;width:auto;display:block}
.brand-text{display:flex;flex-direction:column;line-height:1.2;border-left:1px solid var(--line);padding-left:14px}
.brand-text strong{font-size:12.5px;letter-spacing:2px;font-weight:700}
.brand-text span{font-size:9.5px;letter-spacing:1.5px;color:var(--muted);text-transform:uppercase}
.links{display:flex;gap:18px;font-size:12px;align-items:center}
.links a{text-decoration:none;color:#555;font-weight:500}.links a:hover{color:var(--ink)}
.cta{background:var(--ink);color:#fff!important;padding:9px 16px;border-radius:4px;font-weight:600}
.hero{background:radial-gradient(900px 420px at 82% -10%,rgba(176,138,62,.28),transparent 62%),linear-gradient(135deg,#121212 0%,#1d1d1d 58%,#27221a 100%);color:#fff;padding:70px 28px 78px}
.hero-inner{max-width:1120px;margin:0 auto}
.eyebrow{font-size:10.5px;font-weight:700;letter-spacing:2.2px;text-transform:uppercase;color:#e4c98a;margin-bottom:18px}
.hero h1{font-size:clamp(34px,5.2vw,58px);line-height:1.07;margin:0 0 20px;max-width:900px;font-weight:700}
.hero p{max-width:720px;color:rgba(255,255,255,.74);font-size:17px;line-height:1.7;margin:0}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin-top:32px}
.stat{border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);border-radius:8px;padding:14px 18px;min-width:140px}
.stat b{display:block;font-size:26px;letter-spacing:-1px}.stat span{font-size:9.5px;letter-spacing:1.4px;text-transform:uppercase;color:rgba(255,255,255,.55)}
.wrap{max-width:1180px;margin:0 auto;padding:50px 28px 90px}
.intro{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;margin-bottom:24px}
.intro h2{font-size:28px;margin:0 0 8px}.intro p{margin:0;color:#555;max-width:640px;font-size:14.5px}
.note{font-size:11.5px;color:#6b5a34;background:#f6efdf;border:1px solid #e7d9ba;padding:10px 14px;border-radius:6px;white-space:nowrap}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 26px}
.filter{font-family:inherit;font-size:12px;font-weight:500;border:1px solid var(--line);background:#fff;color:#444;padding:8px 13px;border-radius:999px;cursor:pointer}
.filter small{color:var(--muted);margin-left:5px}.filter.active{background:var(--ink);color:#fff;border-color:var(--ink)}.filter.active small{color:#d8c9a4}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.art-card{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:10px;padding:20px;text-decoration:none;transition:.18s;min-height:215px}
.art-card:hover{transform:translateY(-3px);box-shadow:0 18px 40px rgba(21,21,21,.08);border-color:#d6c9ad}
.art-top{display:flex;justify-content:space-between;gap:8px;align-items:center;margin-bottom:12px}
.art-cluster{font-size:9.5px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;color:var(--gold-dark)}
.art-type{font-size:10px;background:#f6efdf;color:#7d5f22;border-radius:999px;padding:4px 9px;font-weight:700;letter-spacing:.5px}
.art-card h3{font-size:16.5px;line-height:1.35;margin:0 0 9px;font-weight:700}
.art-card p{font-size:12.5px;line-height:1.55;color:#666;margin:0 0 16px;flex:1}
.art-meta{margin-top:auto;display:flex;gap:10px;font-size:10.5px;color:var(--muted);border-top:1px solid #f0ece2;padding-top:12px}
.art-meta b{color:#333}.art-meta span:last-child{margin-left:auto;color:var(--ink);font-weight:600}
.vols{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:8px}
.vol{background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px;display:flex;flex-direction:column}
.vol.done{border-top:3px solid var(--ink)}.vol.part{border-top:3px solid #d8c9a4}
.vol-top{display:flex;justify-content:space-between;font-size:9.5px;letter-spacing:1.3px;text-transform:uppercase;color:var(--gold-dark);font-weight:700}
.vol h3{font-family:"Montserrat";font-size:19px;margin:12px 0 6px}
.vol p{color:#666;font-size:12.5px;margin:0 0 14px;flex:1}
.vol-meta{font-size:11px;color:var(--muted);margin-bottom:14px}.vol-meta b{color:var(--ink)}
.dl{display:flex;gap:8px}
.dl a{flex:1;text-align:center;border:1px solid var(--line);border-radius:4px;padding:10px;font-size:12px;text-decoration:none;font-weight:700;background:#fff}
.dl a:hover{border-color:var(--gold);background:var(--cream)}
.cta-box{margin-top:44px;background:linear-gradient(135deg,#171717,#2a251d);color:#fff;border-radius:12px;padding:32px;display:flex;justify-content:space-between;gap:24px;align-items:center;flex-wrap:wrap}
.cta-box h3{margin:0 0 8px;font-size:22px}.cta-box p{margin:0;color:rgba(255,255,255,.65);font-size:14px}
.cta-box a{background:#e4c98a;color:#1a1a1a;text-decoration:none;padding:12px 18px;border-radius:5px;font-weight:700;font-size:12.5px;white-space:nowrap}
.pend-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;margin-top:22px}
.pend-col h4{font-size:10.5px;letter-spacing:1.5px;text-transform:uppercase;color:var(--gold-dark);margin:0 0 4px}
ul.pend{list-style:none;padding:0;margin:0}
ul.pend li{font-size:13px;color:#666;border-bottom:1px dotted var(--line);padding:8px 0}
ul.pend li b{color:var(--gold-dark);display:inline-block;min-width:34px;font-size:11.5px;letter-spacing:.5px}
.footer{border-top:1px solid var(--line);padding:22px 28px;font-size:11px;color:#777;display:flex;justify-content:space-between;gap:20px;max-width:1180px;margin:0 auto;flex-wrap:wrap;align-items:center}
.footer img{height:18px;opacity:.85}
.doc{max-width:760px;margin:0 auto;padding:52px 28px 80px}
.doc .crumb{font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);margin-bottom:18px}
.doc .crumb a{color:var(--gold-dark);text-decoration:none;font-weight:600}
.doc .kicker{font-size:10px;letter-spacing:1.8px;text-transform:uppercase;color:var(--gold-dark);font-weight:700}
.doc h1{font-size:clamp(28px,4vw,42px);line-height:1.12;margin:14px 0 12px}
.doc .sub{color:#666;font-size:16px;margin:0 0 20px}
.doc .meta{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:26px}
.doc .meta span{font-size:10.5px;border:1px solid var(--line);border-radius:999px;padding:6px 11px;color:#666;background:#fff}
.doc hr{border:0;border-top:1px solid var(--line);margin:30px 0}
.doc h2{font-size:22px;margin:34px 0 12px}
.doc h3{font-size:17px;margin:26px 0 10px}
.doc .faq-q{font-size:15.5px;margin:22px 0 6px;color:var(--ink)}
.doc p{margin:0 0 15px;font-size:15px;color:#2a2a2a}
.doc blockquote{margin:22px 0;padding:18px 22px;background:var(--cream);border-left:3px solid var(--gold);border-radius:0 6px 6px 0}
.doc blockquote p{margin:0;font-size:15px}
.doc ul,.doc ol{margin:0 0 16px;padding-left:22px}.doc li{margin-bottom:7px;font-size:15px;color:#2a2a2a}
.doc .planned{color:#555;font-weight:600}.doc .planned em{font-style:normal;color:var(--gold-dark);font-weight:500;font-size:.9em}
.tbl{overflow-x:auto;margin:22px 0 26px}
.doc table{width:100%;border-collapse:collapse;font-size:13px}
.doc th{background:var(--ink);color:#fff;text-align:left;padding:10px 12px;font-weight:600;font-size:12px}
.doc td{border-bottom:1px solid var(--line);padding:10px 12px;vertical-align:top}
.doc tr:nth-child(even) td{background:#fbf8f1}
pre.code{background:#f4f1ea;border:1px solid var(--line);border-radius:6px;padding:14px;font-size:10.5px;overflow-x:auto;color:#333}
details{margin:26px 0;border:1px solid var(--line);border-radius:6px;background:#fff}
summary{cursor:pointer;padding:12px 16px;font-size:12.5px;font-weight:600;color:var(--gold-dark)}
details pre{margin:0;border:0;border-top:1px solid var(--line);border-radius:0;max-height:320px}
.docnav{display:flex;justify-content:space-between;gap:16px;margin-top:44px;padding-top:20px;border-top:1px solid var(--line);font-size:12.5px}
.docnav a{text-decoration:none;color:var(--gold-dark);font-weight:600}
.docnav a.dl2{background:var(--ink);color:#fff;padding:9px 14px;border-radius:4px}
@media(max-width:900px){.grid{grid-template-columns:1fr 1fr}.intro{flex-direction:column;align-items:flex-start}.note{white-space:normal}}
@media(max-width:620px){.brand img{height:20px}.brand-text{padding-left:10px}.brand-text span{display:none}.brand-text strong{font-size:10.5px;letter-spacing:1.4px}.header-inner{padding:10px 14px;gap:10px}.links{gap:8px}.links .cta{padding:8px 10px;font-size:11px}.pend-grid{grid-template-columns:1fr}.grid{grid-template-columns:1fr}.hero{padding:52px 20px 60px}.wrap{padding:36px 20px 60px}.links a:not(.cta){display:none}.doc{padding:36px 20px 60px}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">')


def fmt(n):
    return f"{n:,}".replace(",", ".")


def header(prefix="", back=False, label=""):
    links = (f'<a href="{prefix}index.html">{label}</a>' if back else
             '<a href="#volumes">Volumes</a><a href="#proxima">Próxima remessa</a>')
    return f'''<header class="header"><div class="header-inner">
<a class="brand" href="{prefix}index.html"><img src="{prefix}assets/logo-v4-red.png" alt="V4 Company">
<span class="brand-text"><strong>PREMIUM CLEANING</strong><span>Biblioteca editorial</span></span></a>
<div class="links">{links}<a class="cta" href="{prefix}#volumes">Baixar volumes</a></div>
</div></header>'''


def footer(prefix=""):
    return f'''<footer class="footer"><span>Premium Cleaning Services · (973) 204-2310 · 107 Vesey St, Newark, NJ 07105</span>
<span>Programa editorial · novembro de 2026</span><img src="{prefix}assets/logo-v4-red.png" alt="V4 Company"></footer>'''


def article_page(a):
    L = a["aid"][0]
    name = BLOCKS[L][0]
    content, jsonld = render(a["body"])
    scripts = "\n".join(f'<script type="application/ld+json">{j}</script>' for j in jsonld)
    evidence = ""
    if jsonld:
        js = "\n\n".join(jsonld)
        evidence = (f'<details><summary>Dados estruturados (JSON-LD) incluídos no artigo</summary>'
                    f'<pre class="code">{H.escape(js)}</pre></details>')
    mins = max(1, round(a["words"] / 240))
    vol = VOLLINK[L]
    prev = a.get("prev"); nxt = a.get("next")
    nav = ['<div class="docnav">']
    nav.append(f'<a href="{prev["slug"]}.html">← {prev["aid"]} · Anterior</a>' if prev else '<a href="index.html">← Biblioteca</a>')
    nav.append(f'<a href="../volumes/{vol}.pdf" class="dl2">Baixar no volume {L} (PDF)</a>')
    nav.append(f'<a href="{nxt["slug"]}.html">{nxt["aid"]} · Próximo →</a>' if nxt else '<span></span>')
    nav.append("</div>")
    return f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{H.escape(a["meta"].get("meta_title") or a["meta"].get("title",""))} | Premium Cleaning Services</title>
<meta name="description" content="{H.escape(a["meta"].get("meta_desc",""))}">{FONTS}
<style>{CSS}</style>{scripts}</head><body>
{header("../", True, "← Biblioteca editorial")}
<article class="doc">
<div class="kicker">Editorial program · Block {L} · {H.escape(name)}</div>
<h1>{inline(a["meta"].get("title",""))}</h1>
<p class="sub">{inline(a["meta"].get("subtitle",""))}</p>
<div class="meta"><span>{a["aid"]}</span><span>{fmt(a["words"])} palavras</span><span>{mins} min</span><span>Query: {H.escape(a["meta"].get("query",""))}</span><span>Destino: {H.escape(a["meta"].get("dest",""))}</span></div>
<hr>
{content}
{evidence}
{"".join(nav)}
</article>
{footer("../")}</body></html>'''


def build():
    os.makedirs(os.path.join(DEST, "assets"), exist_ok=True)
    os.makedirs(ART, exist_ok=True)
    for f in ("logo-v4-red.png", "logo-v4-white.png"):
        shutil.copy2(os.path.join(SRC_LOGO, f), os.path.join(DEST, "assets", f))

    arts = []
    for path in sorted(glob.glob(os.path.join(LOTE, "*.md"))):
        raw = io.open(path, encoding="utf-8").read()
        meta, body = parse_front(raw)
        aid = os.path.basename(path).split("-")[0]
        words = len(re.sub(r"```.*?```", "", body, flags=re.S).split())
        arts.append(dict(aid=aid, meta=meta, body=body, words=words,
                         slug=meta.get("slug") or os.path.basename(path)[:-3]))
    arts.sort(key=lambda a: (a["aid"][0], int(a["aid"][1:])))
    for i, a in enumerate(arts):
        a["prev"] = arts[i - 1] if i > 0 else None
        a["next"] = arts[i + 1] if i < len(arts) - 1 else None
        io.open(os.path.join(ART, a["slug"] + ".html"), "w", encoding="utf-8").write(article_page(a))

    total = sum(a["words"] for a in arts)
    cards = []
    for a in arts:
        L = a["aid"][0]
        mins = max(1, round(a["words"] / 240))
        desc = a["meta"].get("meta_desc", "")[:200]
        cards.append(f'''<a class="art-card" data-cluster="{L}" href="artigos/{a["slug"]}.html">
<div class="art-top"><span class="art-cluster">{H.escape(BLOCKS[L][0])}</span><span class="art-type">{a["aid"]}</span></div>
<h3>{inline(a["meta"].get("title",""))}</h3><p>{inline(desc)}</p>
<div class="art-meta"><span><b>{fmt(a["words"])}</b> palavras</span><span>{mins} min</span><span>Ler artigo →</span></div></a>''')

    counts = {L: sum(1 for a in arts if a["aid"][0] == L) for L in "ABCDE"}
    filters = f'<button class="filter active" data-f="all">Todos <small>{len(arts)}</small></button>'
    filters += "".join(f'<button class="filter" data-f="{L}">{H.escape(BLOCKS[L][0])} <small>{counts[L]}</small></button>'
                       for L in "ABCDE")

    vol_pages = {"A": 149, "B": 65, "C": 65, "D": 143}
    vols = []
    for L in "ABCD":
        name, desc = BLOCKS[L]
        n = counts[L]
        badge = "COMPLETO" if n == 8 else f"PARTE 1 · {n} de 8"
        cls = "done" if n == 8 else "part"
        slug = VOLLINK[L]
        vols.append(f'''<article class="vol {cls}"><div class="vol-top"><span>Bloco {L}</span><span>{badge}</span></div>
<h3>{H.escape(name)}</h3><p>{H.escape(desc)}</p>
<div class="vol-meta"><b>{fmt(sum(a["words"] for a in arts if a["aid"][0]==L))}</b> palavras · <b>{vol_pages[L]}</b> páginas · folha de aprovação</div>
<div class="dl"><a href="volumes/{slug}.pdf">PDF</a><a href="volumes/{slug}.docx">DOCX</a></div></article>''')

    pend = ""
    for L in "BCE":
        items = "".join(f'<li><b>{k}</b> {v}</li>' for k, v in PENDING.items() if k[0] == L)
        pend += f'<div class="pend-col"><h4>Bloco {L} · {BLOCKS[L][0]}</h4><ul class="pend">{items}</ul></div>'
    pend = f'<div class="pend-grid">{pend}</div>'

    html = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Biblioteca editorial Premium Cleaning | {len(arts)} artigos completos</title>
<meta name="description" content="Biblioteca editorial Premium Cleaning Services: {len(arts)} artigos completos sobre limpeza de hotéis, comercial, carpetes e cozinhas. Programa de 40 artigos, novembro de 2026.">{FONTS}
<style>{CSS}</style></head><body>
{header()}
<section class="hero"><div class="hero-inner"><div class="eyebrow">Programa editorial · novembro de 2026</div>
<h1>{len(arts)} artigos completos em 4 blocos de entrega</h1>
<p>Biblioteca construída sobre as 40 keywords do programa: guias técnicos de 5.000+ palavras para hotelaria, limpeza comercial, carpetes e operação de cozinha em New Jersey e Nova York.</p>
<div class="stats"><div class="stat"><b>{len(arts)}</b><span>Artigos completos</span></div>
<div class="stat"><b>2</b><span>Blocos completos</span></div><div class="stat"><b>4</b><span>Volumes entregues</span></div>
<div class="stat"><b>{fmt(total)}</b><span>Palavras no total</span></div></div></div></section>
<div class="wrap"><div class="intro"><div><h2>Biblioteca por bloco</h2>
<p>Filtre por bloco para ver a cobertura. Cada artigo tem resposta direta, tabelas, perguntas frequentes, links internos planejados e dados estruturados.</p></div>
<div class="note">Drafts editoriais · publicação no site depende de aprovação</div></div>
<div class="filters">{filters}</div>
<div class="grid" id="grid">{"".join(cards)}</div>
<div id="volumes"><div class="intro" style="margin-top:56px"><div><h2>Volumes para aprovação</h2>
<p>Os mesmos artigos em documento. PDF para ler, DOCX para comentar. Cada volume termina com a folha de aprovação do bloco.</p></div>
<div class="note">10 arquivos · DOCX e PDF</div></div>
<div class="vols">{"".join(vols)}
<article class="vol"><div class="vol-top"><span>Índice</span><span>24 de 40</span></div>
<h3>Índice do programa</h3><p>Os 40 artigos planejados com bloco, query-alvo, contagem de palavras e situação. Inclui a lista da próxima remessa.</p>
<div class="vol-meta">3 páginas · visão consolidada</div>
<div class="dl"><a href="volumes/00-indice-programa-editorial.pdf">PDF</a><a href="volumes/00-indice-programa-editorial.docx">DOCX</a></div></article>
</div></div>
<div id="proxima" style="margin-top:52px"><h2 style="font-size:26px;margin:0 0 8px">Próxima remessa · 16 artigos</h2>
<p style="color:#555;margin:0;font-size:14px">Fecham os blocos B e C e abrem o bloco E.</p>
{pend}</div>
<div class="cta-box"><div><h3>Pronto para aprovar os dois blocos completos?</h3>
<p>Hotelaria (A1–A8) e restaurante (D1–D8) estão fechados. B e C seguem em Parte 1.</p></div>
<a href="volumes/00-indice-programa-editorial.pdf">Ver índice completo</a></div></div>
{footer()}
<script>const b=[...document.querySelectorAll('.filter')],c=[...document.querySelectorAll('.art-card')];
b.forEach(x=>x.onclick=()=>{{b.forEach(y=>y.classList.remove('active'));x.classList.add('active');const f=x.dataset.f;
c.forEach(k=>k.style.display=(f==='all'||k.dataset.cluster===f)?'':'none')}});</script>
</body></html>'''
    io.open(os.path.join(DEST, "index.html"), "w", encoding="utf-8").write(html)
    print(f"index {os.path.getsize(os.path.join(DEST,'index.html'))}b · {len(arts)} paginas")


if __name__ == "__main__":
    build()
