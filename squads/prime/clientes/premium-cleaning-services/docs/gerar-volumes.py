# -*- coding: utf-8 -*-
"""Gera os volumes de entrega do Programa Editorial (DOCX) a partir de artigos/lote-1/*.md."""
import os, re, io, json, glob, importlib.util, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
LOTE = os.path.join(BASE, "artigos", "lote-1")
OUT = os.path.join(BASE, "artigos", "volumes")
os.makedirs(OUT, exist_ok=True)

spec = importlib.util.spec_from_file_location("gad", os.path.join(HERE, "gerar-artigos-docx.py"))
gad = importlib.util.module_from_spec(spec); spec.loader.exec_module(gad)

from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

INK = RGBColor(0x14, 0x14, 0x14)
GOLD = RGBColor(0x8A, 0x6D, 0x3B)
GRAY = RGBColor(0x6B, 0x6B, 0x6B)
LGRAY = RGBColor(0x8A, 0x8A, 0x8A)

BLOCKS = {
    "A": ("Hotel & Hospitality", "vol-A-hotel-hospitality", "Hotel e hospitalidade: padrões de produtividade, cronogramas e inspeção."),
    "B": ("Commercial & Office", "vol-B-commercial-office", "Limpeza comercial e corporativa: contratos, SLAs e verificação de fornecedor."),
    "C": ("Carpet & Floor Care", "vol-C-carpet-floor", "Carpetes e pisos: custo, métodos, secagem, garantia e segurança."),
    "D": ("Restaurant & Kitchen", "vol-D-restaurant-kitchen", "Cozinhas e restaurantes: conformidade, gordura, exaustão e saúde."),
    "E": ("Cost & Procurement", "vol-E-cost-procurement", "Custo real, benchmark, orçamento e processo de compra."),
}
ORDER = "ABCDE"

PENDING = {
    "B5": "Insurance, Bonding and Background Checks: What to Verify Before Hiring a Cleaner",
    "B6": "OSHA Compliance for Commercial Cleaning: Chemicals, PPE and Training",
    "B7": "ATP Testing in Restrooms: How to Prove a Restroom Is Actually Clean",
    "B8": "The Vendor Scorecard: 12 Metrics to Review in a Quarterly Business Review",
    "C5": "Interim vs Restorative Carpet Cleaning in High-Traffic Areas",
    "C6": "Coefficient of Friction: Floor Safety Standards for Commercial Spaces",
    "C7": "Stone and Terrazzo Floor Care: Honing, Polishing and Sealing Schedules",
    "C8": "Grout Sealing vs Grout Restoration: When Cleaning Is No Longer Enough",
    "E1": "The True Cost of a Dirty Office",
    "E2": "Cleaning Cost Benchmarks: New Jersey vs New York City",
    "E3": "How to Build an Annual Cleaning Budget",
    "E4": "The 15-Point Vendor Vetting Checklist",
    "E5": "Contract Terms That Protect the Client",
    "E6": "Change Orders: How to Price Work Outside Scope",
    "E7": "Calculating ROI on Commercial Cleaning",
    "E8": "Vendor Consolidation: One Provider vs Many",
}

PT_TOKENS = set("""não são você vocês também já até isso isto esse essa este esta aquele aquela
para pela pelo pelos pelas uma umas dos das numa num ao aos à às mais como entre
quando onde porque porém então sobre serviço serviços limpeza empresa empresas cliente clientes
orçamento contrato trabalho nosso nossa seus suas fazer feito pode podem deve devem
muito pouco sempre nunca aqui depois antes durante cada qual quais seja ser está estão
foi eram tem têm havia será seria""".split())


def prose_words(body):
    b = re.sub(r"```.*?```", "", body, flags=re.S)
    return len(b.split())


def analyze(md_path):
    raw = io.open(md_path, encoding="utf-8").read()
    meta, body = gad.parse_front(raw)
    aid = os.path.basename(md_path).split("-")[0]
    h2 = re.findall(r"^## ", body, re.M)
    tables = len(re.findall(r"^\|.*\|\s*$\n\|[\s:|-]+\|", body, re.M))
    faq = len(re.findall(r"^\*\*[^*]+\?\*\*\s*$", body, re.M))
    links = set(re.findall(r"\]\((/[^)]+)\)", body))
    jsonld_ok = True
    for blk in re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", body, re.S):
        try:
            json.loads(blk)
        except Exception:
            jsonld_ok = False
    clean = re.sub(r"```.*?```", " ", body, flags=re.S)
    clean = re.sub(r"https?://\S+|[\w.-]+\.(?:com|org|net|nj|io)\b", " ", clean)
    low = re.findall(r"[A-Za-zÀ-ÿ]+", clean.lower())
    pt = sorted({w for w in low if w in PT_TOKENS})
    words = prose_words(body)
    fails = []
    if words < 5000: fails.append(f"palavras {words}")
    if len(h2) < 12: fails.append(f"H2 {len(h2)}")
    if tables < 3: fails.append(f"tabelas {tables}")
    if faq < 8: fails.append(f"FAQ {faq}")
    if not (5 <= len(links) <= 9): fails.append(f"links {len(links)}")
    if pt: fails.append("PT: " + ",".join(pt[:6]))
    if not jsonld_ok: fails.append("JSON-LD")
    meta = {k: v.strip().strip('"').strip("'") for k, v in meta.items()}
    return dict(aid=aid, path=md_path, meta=meta, body=body, words=words,
                h2=len(h2), tables=tables, faq=faq, links=len(links), fails=fails)


def fixed_table(t, widths):
    t.autofit = False
    tblPr = t._tbl.tblPr
    for old in tblPr.findall(qn("w:tblLayout")):
        tblPr.remove(old)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    grid = t._tbl.find(qn("w:tblGrid"))
    if grid is not None:
        for i, gc in enumerate(grid.findall(qn("w:gridCol"))):
            if i < len(widths):
                gc.set(qn("w:w"), str(int(Cm(widths[i]).twips)))
    for i, w in enumerate(widths):
        try: t.columns[i].width = Cm(w)
        except IndexError: pass
    for row in t.rows:
        for i, w in enumerate(widths):
            if i < len(row.cells):
                row.cells[i].width = Cm(w)


def field_footer(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("PREMIUM CLEANING SERVICES  ·  PROGRAMA EDITORIAL NOVEMBRO 2026  ·  ")
    r.font.size = Pt(7.5); r.font.color.rgb = LGRAY
    r2 = p.add_run(); r2.font.size = Pt(7.5); r2.font.color.rgb = LGRAY
    for instr in ("PAGE",):
        f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
        it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = f" {instr} "
        f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
        r2._r.append(f1); r2._r.append(it); r2._r.append(f2)


def rule(doc, color="DED7C8", size=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(10)
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr"); bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "1"); bottom.set(qn("w:color"), color)
    pbdr.append(bottom); pPr.append(pbdr)


def label(doc, text, size=8.5, color=GOLD, before=0, after=4, bold=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text); r.bold = bold; r.font.size = Pt(size); r.font.color.rgb = color
    return p


def render(doc, body):
    """Markdown -> DOCX com numeracao manual reiniciando a cada lista."""
    lines = body.split("\n"); i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1; continue
        if line.startswith("```"):
            i += 1; buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            for cl in buf:
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(0); p.paragraph_format.left_indent = Cm(0.4)
                r = p.add_run(cl); r.font.name = "Courier New"; r.font.size = Pt(7.5)
                r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            doc.add_paragraph(); continue
        if line.lstrip().startswith("|"):
            tl = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                tl.append(lines[i].strip()); i += 1
            rows = [[c.strip() for c in l.strip("|").split("|")] for l in tl]
            rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c or "") for c in r)]
            if rows: gad._table(doc, rows)
            continue
        if line.startswith("### "):
            doc.add_heading(line[4:], level=3); i += 1; continue
        if line.startswith("## "):
            doc.add_heading(line[3:], level=2); i += 1; continue
        if line.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.5)
            p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(10)
            gad.add_runs(p, line[2:])
            for r in p.runs:
                r.italic = True; r.font.color.rgb = RGBColor(0x43, 0x43, 0x43)
            i += 1; continue
        if line.lstrip().startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            gad.add_runs(p, line.lstrip()[2:])
            p.paragraph_format.space_after = Pt(4); i += 1; continue
        if re.match(r"^\d+\.\s", line.lstrip()):
            n = 1
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].lstrip()):
                txt = re.sub(r"^\d+\.\s", "", lines[i].lstrip())
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(0.7)
                p.paragraph_format.first_line_indent = Cm(-0.7)
                p.paragraph_format.space_after = Pt(4)
                rn = p.add_run(f"{n}.  "); rn.bold = True; rn.font.color.rgb = GOLD
                gad.add_runs(p, txt)
                n += 1; i += 1
            continue
        p = doc.add_paragraph()
        gad.add_runs(p, line.strip())
        i += 1


def cover(doc, kicker, title, subtitle, meta_line, badge):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(90)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(kicker); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = GOLD
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    r = p.add_run(title); r.bold = True; r.font.size = Pt(30); r.font.color.rgb = INK
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(subtitle); r.font.size = Pt(12); r.font.color.rgb = GRAY
    rule(doc)
    if badge:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(badge); r.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = GOLD
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(40)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(meta_line); r.font.size = Pt(9); r.font.color.rgb = LGRAY
    doc.add_page_break()


def article_head(doc, a):
    m = a["meta"]
    label(doc, m.get("eyebrow", "PROGRAMA EDITORIAL"), before=6, after=8)
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2)
    r = p.add_run(m.get("title", a["aid"])); r.bold = True; r.font.size = Pt(19); r.font.color.rgb = INK
    if m.get("subtitle"):
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(8)
        r = p.add_run(m["subtitle"]); r.font.size = Pt(10.5); r.font.color.rgb = GRAY
    rule(doc)
    strip = f"QUERY-ALVO  {m.get('query','')}   ·   DESTINO  {m.get('dest','')}   ·   {a['words']:,} PALAVRAS".replace(",", ".")
    label(doc, strip, size=7.5, color=LGRAY, after=14, bold=False)


def approval_page(doc, block_letter, block_name, arts, pending_ids):
    doc.add_page_break()
    label(doc, "FOLHA DE APROVAÇÃO", before=10, after=6)
    p = doc.add_paragraph()
    r = p.add_run(f"Bloco {block_letter} — {block_name}"); r.bold = True; r.font.size = Pt(17); r.font.color.rgb = INK
    rule(doc)
    p = doc.add_paragraph()
    gad.add_runs(p, "Confira cada artigo e marque a decisão. As observações podem ser feitas por número de artigo, "
                    "no campo abaixo da tabela. Nenhum conteúdo será publicado antes desta aprovação.")
    doc.add_paragraph()
    t = doc.add_table(rows=0, cols=5)
    hdr = ["#", "Artigo", "Query-alvo", "Palav.", "Aprovar"]
    c = t.add_row().cells
    for i, h in enumerate(hdr):
        c[i].text = ""; par = c[i].paragraphs[0]; par.paragraph_format.space_after = Pt(0)
        r = par.add_run(h); r.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        gad.shade(c[i], "1A1A1A")
    for a in arts:
        c = t.add_row().cells
        vals = [a["aid"], a["meta"].get("title", ""), a["meta"].get("query", ""), f"{a['words']:,}".replace(",", "."), "☐ sim   ☐ não"]
        for i, v in enumerate(vals):
            c[i].text = ""; par = c[i].paragraphs[0]; par.paragraph_format.space_after = Pt(0)
            gad.add_runs(par, v, size=7.5)
    gad.style_table(t)
    fixed_table(t, [0.9, 6.9, 3.8, 1.6, 3.0])
    doc.add_paragraph()
    label(doc, "OBSERVAÇÕES", size=8, color=GOLD, before=8, after=6)
    for _ in range(3):
        p = doc.add_paragraph()
        pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement("w:pBdr"); bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "4"); bottom.set(qn("w:space"), "1")
        bottom.set(qn("w:color"), "DED7C8"); pbdr.append(bottom); pPr.append(pbdr)
        p.paragraph_format.space_after = Pt(9)
    gad.add_runs(p, "Aprovado por: ______________________________________     Data: ____ / ____ / 2026", size=10)
    if pending_ids:
        doc.add_paragraph()
        label(doc, "EM PRODUÇÃO — ENTREGA NA PRÓXIMA REMESSA", size=8, color=GOLD, before=10, after=4)
        for pid in pending_ids:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.4); p.paragraph_format.space_after = Pt(2)
            r = p.add_run(f"{pid}  ·  {PENDING.get(pid,'')}"); r.font.size = Pt(8.5); r.font.color.rgb = GRAY


def build_volume(letter, arts, pending_ids):
    name, slug, desc = BLOCKS[letter]
    doc = gad.base_doc(); gad.set_heading_colors(doc)
    field_footer(doc.sections[0])
    total = len(arts) + len(pending_ids)
    if pending_ids:
        badge = f"PARTE 1  ·  {len(arts)} DE {total} ARTIGOS  ·  {len(pending_ids)} EM PRODUÇÃO"
    else:
        badge = f"COMPLETO  ·  {len(arts)} DE {total} ARTIGOS"
    cover(doc, "PROGRAMA EDITORIAL  ·  NOVEMBRO 2026", f"Bloco {letter} — {name}",
          desc, f"Premium Cleaning Services  ·  {sum(a['words'] for a in arts):,} palavras".replace(",", "."), badge)

    label(doc, "SUMÁRIO", before=0, after=8)
    t = doc.add_table(rows=0, cols=3)
    for a in arts:
        c = t.add_row().cells
        for i, v in enumerate([a["aid"], a["meta"].get("title", ""), f"{a['words']:,}".replace(",", ".")]):
            c[i].text = ""; par = c[i].paragraphs[0]; par.paragraph_format.space_after = Pt(2)
            gad.add_runs(par, v, size=8.5)
    gad.style_table(t)
    fixed_table(t, [1.2, 12.8, 2.2])
    if pending_ids:
        doc.add_paragraph()
        label(doc, "EM PRODUÇÃO", size=8, color=GOLD, after=4)
        for pid in pending_ids:
            p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2)
            r = p.add_run(f"{pid}  ·  {PENDING.get(pid,'')}"); r.font.size = Pt(8.5); r.font.color.rgb = GRAY

    for idx, a in enumerate(arts):
        doc.add_page_break()
        article_head(doc, a)
        render(doc, a["body"])

    approval_page(doc, letter, name, arts, pending_ids)
    out = os.path.join(OUT, f"{slug}.docx")
    doc.save(out); gad.purge_blue(out)
    return out


def build_index(arts):
    doc = gad.base_doc(); gad.set_heading_colors(doc)
    field_footer(doc.sections[0])
    cover(doc, "PROGRAMA EDITORIAL  ·  NOVEMBRO 2026", "Índice do Programa",
          "40 artigos planejados · 5 blocos · 4 volumes nesta remessa",
          "Premium Cleaning Services  ·  atualizado em 29/10/2026",
          f"{len(arts)} DE 40 ARTIGOS ENTREGUES")
    label(doc, "SITUAÇÃO POR BLOCO", before=0, after=8)
    t = doc.add_table(rows=0, cols=5)
    c = t.add_row().cells
    for i, h in enumerate(["Bloco", "Tema", "Entregues", "Total", "Situação"]):
        c[i].text = ""; par = c[i].paragraphs[0]; par.paragraph_format.space_after = Pt(0)
        r = par.add_run(h); r.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        gad.shade(c[i], "1A1A1A")
    for L in ORDER:
        got = [a for a in arts if a["aid"].startswith(L)]
        tot = 8
        sit = "COMPLETO" if len(got) == tot else ("PARTE 1" if got else "PREVISTO")
        c = t.add_row().cells
        for i, v in enumerate([L, BLOCKS[L][0], str(len(got)), str(tot), sit]):
            c[i].text = ""; par = c[i].paragraphs[0]; par.paragraph_format.space_after = Pt(2)
            gad.add_runs(par, v, size=8.5)
    gad.style_table(t)
    fixed_table(t, [1.4, 6.6, 2.2, 1.4, 4.6])
    doc.add_paragraph()

    label(doc, "ARTIGOS ENTREGUES", size=9, color=GOLD, before=8, after=6)
    t = doc.add_table(rows=0, cols=6)
    c = t.add_row().cells
    for i, h in enumerate(["#", "Bloco", "Título", "Query-alvo", "Palavras", "Situação"]):
        c[i].text = ""; par = c[i].paragraphs[0]; par.paragraph_format.space_after = Pt(0)
        r = par.add_run(h); r.bold = True; r.font.size = Pt(8); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        gad.shade(c[i], "1A1A1A")
    for a in arts:
        c = t.add_row().cells
        vals = [a["aid"], a["aid"][0], a["meta"].get("title", ""), a["meta"].get("query", ""),
                f"{a['words']:,}".replace(",", "."), "ENTREGUE"]
        for i, v in enumerate(vals):
            c[i].text = ""; par = c[i].paragraphs[0]; par.paragraph_format.space_after = Pt(0)
            gad.add_runs(par, v, size=7)
    gad.style_table(t)
    fixed_table(t, [0.9, 1.3, 5.7, 4.4, 1.7, 2.2])

    doc.add_paragraph()
    label(doc, "PRÓXIMA REMESSA", size=9, color=GOLD, before=8, after=6)
    t = doc.add_table(rows=0, cols=3)
    c = t.add_row().cells
    for i, h in enumerate(["#", "Bloco", "Título"]):
        c[i].text = ""; par = c[i].paragraphs[0]; par.paragraph_format.space_after = Pt(0)
        r = par.add_run(h); r.bold = True; r.font.size = Pt(8); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
        gad.shade(c[i], "1A1A1A")
    for pid in sorted(PENDING, key=lambda x: (x[0], int(x[1:]))):
        c = t.add_row().cells
        for i, v in enumerate([pid, pid[0], PENDING[pid]]):
            c[i].text = ""; par = c[i].paragraphs[0]; par.paragraph_format.space_after = Pt(0)
            gad.add_runs(par, v, size=7.5)
    gad.style_table(t)
    fixed_table(t, [1.2, 1.4, 13.6])

    out = os.path.join(OUT, "00-indice-programa-editorial.docx")
    doc.save(out); gad.purge_blue(out)
    return out


def audit_blue(path):
    z = zipfile.ZipFile(path)
    hits = 0
    for it in z.infolist():
        if not (it.filename.endswith(".xml") or it.filename.endswith(".rels")):
            continue
        try: txt = z.read(it.filename).decode("utf-8")
        except UnicodeDecodeError: continue
        for m in re.finditer(r'(?:w:color w:val="|w:fill="|a:srgbClr val=")([0-9A-Fa-f]{6})"', txt):
            if gad._is_blue(m.group(1)): hits += 1
    z.close()
    return hits


def main():
    files = sorted(glob.glob(os.path.join(LOTE, "*.md")))
    arts = [analyze(f) for f in files]
    arts.sort(key=lambda a: (a["aid"][0], int(a["aid"][1:])))
    fails = [a for a in arts if a["fails"]]
    print(f"ARTIGOS: {len(arts)}  ·  APROVADOS: {len(arts)-len(fails)}  ·  REPROVADOS: {len(fails)}")
    for a in fails:
        print(f"  FAIL {a['aid']}: {'; '.join(a['fails'])}")
    out = []
    for L in ORDER:
        got = [a for a in arts if a["aid"].startswith(L)]
        pend = sorted([p for p in PENDING if p.startswith(L)], key=lambda x: int(x[1:]))
        if not got: continue
        out.append(build_volume(L, got, pend))
    out.append(build_index(arts))
    for p in out:
        print(f"DOCX {os.path.basename(p)}  {os.path.getsize(p)}b  azul={audit_blue(p)}")


if __name__ == "__main__":
    main()
