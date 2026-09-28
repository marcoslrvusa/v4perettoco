#!/usr/bin/env python3
"""Gera o DOCX da atividade 4 (padrão PDI sênior, paleta #8b4513/#1a1f24/#6b7a8a)."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

D = {
  "title": "Catálogo de Serviços e Ownership com Matriz de Responsabilidade",
  "slug": "arquitetura-documentada-a4",
  "autor": "Marcos Luciano",
  "unidade": "FV Marketing / V4 Company",
  "data": "Setembro 2026",
  "área": "Automação & Infraestrutura",
  "sections": [
    ("1. Contexto", [
      ("p", "Worker quebrava de madrugada e ninguém sabia quem acordar: sistema sem dono, cada peça com um talvez o fulano saiba. Matriz declara dono, suplente e escala para as 6 peças do orquestrador."),
    ]),
    ("2. Diagnóstico", [
      ("table", ["Sintoma", "Causa"], [
        ["Ninguém sabe quem acordar", "Peça sem dono declarado"],
        ["Férias viram incidente", "Peça sem suplente testado"],
        ["Saída apaga história", "Ownership só na memória"],
      ]),
    ]),
    ("3. Solução", [
      ("p", "Catálogo em catalog-info.yaml padrão Backstage, matriz de responsabilidade das 6 peças e roda de ownership semanal com escala em 15 minutos. Dono e pessoa com nome, nunca o time."),
      ("note", "Formato Backstage mesmo sem portal rodando: migração zero no futuro."),
    ]),
    ("4. Matriz resumida", [
      ("table", ["Peça", "Dono", "Suplente"], [
        ["n8n", "Marcos Luciano", "A definir"],
        ["Workers Python", "Marcos Luciano", "A definir"],
        ["Supabase Postgres", "Marcos Luciano", "A definir"],
        ["Painel Next.js", "A definir", "Marcos Luciano"],
        ["Meta Ads API", "Gestor de tráfego", "Marcos Luciano"],
        ["Gmail API", "Marcos Luciano", "A definir"],
      ]),
    ]),
    ("5. Entregas", [
      ("ul", ["01-catalogo-e-ownership-fundamentos.md: regras e criticidade.", "02-matriz-responsabilidade-orquestrador.md: matriz real.", "01-catalog-info-exemplo.yaml: YAML do worker.", "02-template-catalog-info.yaml: template.", "03-roda-ownership.md: revezamento semanal."]),
    ]),
    ("6. Métricas e próximos passos", [
      ("table", ["Métrica", "Atual", "Meta"], [
        ["Sistemas com dono", "4 de 4", "6 de 6"],
        ["Peças sem suplente", "2", "0"],
        ["Dono achado em 15 min", "1 de 3", "3 de 3"],
      ]),
      ("p", "Próximos passos: subir YAML por sistema, definir dono e suplente na reunião do squad, revisão trimestral."),
    ]),
  ],
}

HERE = os.path.dirname(os.path.abspath(__file__))
doc = Document()
st = doc.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
for s in doc.sections:
    s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5); s.left_margin = Cm(3); s.right_margin = Cm(3)

def cover():
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(110)
    r = p.add_run('PDI'); r.bold = True; r.font.size = Pt(14); r.font.color.rgb = RGBColor(0x8B,0x45,0x13)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(D['title']); r.bold = True; r.font.size = Pt(23)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(28)
    r = p.add_run('Documento Técnico de PDI'); r.font.size = Pt(12); r.font.color.rgb = RGBColor(0x6B,0x7A,0x8A)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(16)
    for line in [f"Autor: {D['autor']}", f"Unidade: {D['unidade']}", f"Data: {D['data']}",
                 f"Área: {D['área']}", "Status: Entregue (desenvolvido)"]:
        rr = p.add_run(line + '\n'); rr.font.size = Pt(11); rr.font.color.rgb = RGBColor(0x49,0x55,0x60)
    doc.add_page_break()

def add_section(title, blocks):
    hh = doc.add_heading(title, level=2)
    for r in hh.runs: r.font.color.rgb = RGBColor(0x8B,0x1E,0x1E)
    for kind, *rest in blocks:
        if kind == "p":
            doc.add_paragraph(rest[0])
        elif kind in ("ul", "ol"):
            for x in rest[0]:
                doc.add_paragraph(x, style='List Bullet' if kind == "ul" else 'List Number')
        elif kind == "table":
            h, rows = rest
            t = doc.add_table(rows=1, cols=len(h)); t.style = 'Light Grid Accent 1'
            for i, c in enumerate(h): t.rows[0].cells[i].text = str(c)
            for r in rows:
                cells = t.add_row().cells
                for i, c in enumerate(r): cells[i].text = str(c)
        elif kind == "note":
            p = doc.add_paragraph(); p.add_run("Nota: ").bold = True; p.add_run(rest[0])

cover()
for title, blocks in D['sections']:
    add_section(title, blocks)
out = os.path.join(HERE, "pdi-" + D['slug'] + ".docx")
doc.save(out)
print("DOCX:", out)
