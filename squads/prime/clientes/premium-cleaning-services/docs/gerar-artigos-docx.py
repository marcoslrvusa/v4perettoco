# -*- coding: utf-8 -*-
"""Converte artigos em Markdown (convencao propria) para DOCX no padrao Premium."""
import sys, os, re, io, importlib.util
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def split_bold(text):
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    out = []
    for p in parts:
        if p.startswith('**') and p.endswith('**') and len(p) > 4:
            out.append((p[2:-2], True))
        elif p:
            out.append((p, False))
    return out

def add_runs(par, text, size=None, color=None):
    for chunk, bold in split_bold(text):
        r = par.add_run(chunk)
        r.bold = bold
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = color

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:fill'), hexcolor)
    tcPr.append(shd)


def _tbl_borders(table, color='DED7C8', sz='4'):
    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(old)
    b = OxmlElement('w:tblBorders')
    for edge in ('top','left','bottom','right','insideH','insideV'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'),'single'); el.set(qn('w:sz'), sz)
        el.set(qn('w:space'),'0'); el.set(qn('w:color'), color)
        b.append(el)
    tblPr.append(b)

def style_table(table, banded=False, border='DED7C8'):
    """Estilo sem azul: bordas quentes, cabecalho tratado pelo chamador."""
    table.style = 'Table Grid'
    _tbl_borders(table, border)
    if banded:
        for idx, row in enumerate(table.rows):
            if idx == 0: continue
            if idx % 2 == 0:
                for c in row.cells:
                    shade(c, 'FBF8F1')

def set_heading_colors(doc):
    for name, size in (('Heading 1', 20), ('Heading 2', 13.5), ('Heading 3', 11.5)):
        try:
            st = doc.styles[name]
        except KeyError:
            continue
        st.font.name = 'Calibri'; st.font.size = Pt(size); st.font.bold = True
        st.font.color.rgb = RGBColor(0x1A,0x1A,0x1A)
        st.paragraph_format.space_before = Pt(14); st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.keep_with_next = True


def _is_blue(hexv):
    h = hexv.strip('#').upper()
    if len(h) != 6: return False
    try:
        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    except ValueError:
        return False
    return b > r + 25 and b > g + 15

def purge_blue(docx_path):
    """Remove qualquer tom azul de styles/theme/settings do pacote docx."""
    import zipfile, shutil, re as _re
    tmp = docx_path + '.tmp'
    zin = zipfile.ZipFile(docx_path)
    zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.endswith('.xml') or item.filename.endswith('.rels'):
            try: txt = data.decode('utf-8')
            except UnicodeDecodeError:
                zout.writestr(item, data); continue
            def repl_color(m):
                return m.group(1) + ('1A1A1A' if _is_blue(m.group(2)) else m.group(2)) + '"'
            txt = _re.sub(r'(w:color w:val=")([0-9A-Fa-f]{6})"', repl_color, txt)
            def repl_fill(m):
                return m.group(1) + ('F5F0E6' if _is_blue(m.group(2)) else m.group(2)) + '"'
            txt = _re.sub(r'(w:fill=")([0-9A-Fa-f]{6})"', repl_fill, txt)
            txt = _re.sub(r'(<w:shd[^>]*w:val="clear"[^>]*w:color="auto"[^>]*w:fill=")([0-9A-Fa-f]{6})"',
                          lambda m: m.group(1) + ('F5F0E6' if _is_blue(m.group(2)) else m.group(2)) + '"', txt)
            txt = _re.sub(r'(<a:srgbClr val=")([0-9A-Fa-f]{6})"',
                          lambda m: m.group(1) + ('1A1A1A' if _is_blue(m.group(2)) else m.group(2)) + '"', txt)
            txt = _re.sub(r'(<a:srgbClr val=")([0-9A-Fa-f]{6})"',
                          lambda m: m.group(1) + ('F5F0E6' if _is_blue(m.group(2)) else m.group(2)) + '"', txt)
            data = txt.encode('utf-8')
        zout.writestr(item, data)
    zout.close(); zin.close()
    shutil.move(tmp, docx_path)
    return docx_path

def base_doc():
    doc = Document()
    st = doc.styles['Normal']
    st.font.name = 'Calibri'; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')
    st.paragraph_format.space_after = Pt(8)
    st.paragraph_format.line_spacing = 1.15
    for name in ('Heading 1','Heading 2','Heading 3'):
        doc.styles[name].font.name = 'Calibri'
    s = doc.sections[0]
    s.top_margin = Cm(2.2); s.bottom_margin = Cm(2.0)
    s.left_margin = Cm(2.4); s.right_margin = Cm(2.4)
    return doc

def parse_front(text):
    meta, body = {}, text
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            for line in text[3:end].strip().splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip()
            body = text[end+4:]
    return meta, body.lstrip('\n')

def _table(doc, rowsraw):
    ncols = max(len(r) for r in rowsraw)
    tb = doc.add_table(rows=0, cols=ncols)
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, r in enumerate(rowsraw):
        cells = tb.add_row().cells
        for ci in range(ncols):
            txt = r[ci] if ci < len(r) else ''
            cells[ci].text = ''
            par = cells[ci].paragraphs[0]
            par.paragraph_format.space_after = Pt(0)
            add_runs(par, txt, size=9.5)
            if ri == 0:
                for run in par.runs: run.bold = True
        if ri == 0:
            for c in cells: shade(c, '1A1A1A')
            for c in cells:
                for run in c.paragraphs[0].runs: run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
    style_table(tb)
    doc.add_paragraph()

def render_body(doc, body):
    blocks = body.split('\n')
    i = 0
    while i < len(blocks):
        line = blocks[i].rstrip()
        if not line.strip():
            i += 1; continue
        if line.startswith('```'):
            i += 1; buf = []
            while i < len(blocks) and not blocks[i].startswith('```'):
                buf.append(blocks[i]); i += 1
            i += 1
            for cl in buf:
                par = doc.add_paragraph()
                par.paragraph_format.space_after = Pt(0)
                par.paragraph_format.left_indent = Cm(0.4)
                r = par.add_run(cl)
                r.font.name = 'Courier New'; r.font.size = Pt(8)
                r.font.color.rgb = RGBColor(0x33,0x33,0x33)
            doc.add_paragraph(); continue
        if line.lstrip().startswith('|'):
            tlines = []
            while i < len(blocks) and blocks[i].lstrip().startswith('|'):
                tlines.append(blocks[i].strip()); i += 1
            rowsraw = [[c.strip() for c in l.strip('|').split('|')] for l in tlines]
            rowsraw = [r for r in rowsraw if not all(re.fullmatch(r':?-{2,}:?', c or '') for c in r)]
            if rowsraw: _table(doc, rowsraw)
            continue
        if line.startswith('### '):
            doc.add_heading(line[4:], level=3); i += 1; continue
        if line.startswith('## '):
            doc.add_heading(line[3:], level=2); i += 1; continue
        if line.startswith('# '):
            doc.add_page_break(); doc.add_heading(line[2:], level=1); i += 1; continue
        if line.startswith('> '):
            par = doc.add_paragraph()
            par.paragraph_format.left_indent = Cm(0.5)
            par.paragraph_format.space_before = Pt(6); par.paragraph_format.space_after = Pt(10)
            add_runs(par, line[2:])
            for run in par.runs:
                run.italic = True; run.font.color.rgb = RGBColor(0x43,0x43,0x43)
            i += 1; continue
        if line.lstrip().startswith('- '):
            par = doc.add_paragraph(style='List Bullet')
            add_runs(par, line.lstrip()[2:])
            par.paragraph_format.space_after = Pt(4); i += 1; continue
        if re.match(r'^\d+\.\s', line.lstrip()):
            par = doc.add_paragraph(style='List Number')
            add_runs(par, re.sub(r'^\d+\.\s', '', line.lstrip()))
            par.paragraph_format.space_after = Pt(4); i += 1; continue
        par = doc.add_paragraph()
        add_runs(par, line.strip())
        i += 1

def count_words(doc):
    txt = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells: txt.append(c.text)
    return len(' '.join(txt).split())

def build(md_path):
    raw = io.open(md_path, encoding='utf-8').read()
    meta, body = parse_front(raw)
    doc = base_doc()
    set_heading_colors(doc)
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(70); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(meta.get('eyebrow', 'PROGRAMA EDITORIAL · PREMIUM CLEANING SERVICES')); r.bold = True; r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0x8a,0x6d,0x3b)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(meta.get('title','')); r.bold = True; r.font.size = Pt(24)
    if meta.get('subtitle'):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(meta['subtitle']); r.font.size = Pt(13); r.font.color.rgb = RGBColor(0x55,0x55,0x55)
    doc.add_paragraph()
    rows = [('Slug', meta.get('slug','')), ('URL de destino', meta.get('dest','')),
            ('Meta title', meta.get('meta_title','')), ('Meta description', meta.get('meta_desc','')),
            ('Query-alvo', meta.get('query','')), ('Volume estimado', meta.get('volume','')),
            ('Palavras', meta.get('words','')), ('Autor', meta.get('author','Premium Cleaning Services Editorial Team')),
            ('Publicado / atualizado', meta.get('date',''))]
    t = doc.add_table(rows=0, cols=2)
    for k, v in rows:
        if not v: continue
        c = t.add_row().cells
        c[0].text = k; c[1].text = v
        shade(c[0], 'F5F0E6')
        c[0].paragraphs[0].runs[0].bold = True
        c[0].width = Cm(4.2); c[1].width = Cm(12.5)
    style_table(t)
    doc.add_page_break()
    render_body(doc, body)
    out = os.path.splitext(md_path)[0] + '.docx'
    doc.save(out)
    purge_blue(out)
    print(f"OK {out} · {count_words(doc)} palavras · {os.path.getsize(out)} bytes")
    return out

if __name__ == '__main__':
    for a in sys.argv[1:]:
        build(a)
