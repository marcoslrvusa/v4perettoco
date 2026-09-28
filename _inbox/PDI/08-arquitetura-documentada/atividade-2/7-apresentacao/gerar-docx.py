#!/usr/bin/env python3
"""Gera o DOCX da atividade 2 (padrao PDI senior, paleta #8b4513/#1a1f24/#6b7a8a)."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

D = {
  "title": "ADRs, Architecture Decision Records com Ciclo de Vida e Exemplos Reais",
  "slug": "arquitetura-documentada-a2",
  "autor": "Marcos Luciano",
  "unidade": "FV Marketing / V4 Company",
  "data": "Setembro 2026",
  "area": "Automacao & Infraestrutura",
  "sections": [
    ("1. Contexto", [
      ("p", "Decisoes como por que n8n ou por que Supabase viviam na cabeca de uma pessoa ou no chat. Tres decisoes refeitas no trimestre por falta de registro."),
    ]),
    ("2. Diagnostico", [
      ("table", ["Sintoma", "Causa"], [
        ["Mesma decisao rediscutida", "Motivo e alternativas nao registrados"],
        ["Fornecedor novo zera a conversa", "Sem criterio de comparacao antigo"],
        ["Saida de pessoa apaga historia", "Decisao so na memoria individual"],
      ]),
    ]),
    ("3. Solucao", [
      ("p", "ADRs numerados e imutaveis em docs/adr/NNNN-titulo.md: 5 secoes em 1 pagina, ciclo Proposta, Em avaliacao, Aceita, Implementada, com saidas Rejeitada e Superada."),
      ("note", "Consequencia sem metrica nao entra. Todo ADR diz o que vai monitorar."),
    ]),
    ("4. Exemplos reais", [
      ("p", "ADR-001: n8n self-hosted. Descartados fila propria (3 semanas sem UI) e Apps Script (sem log nem retry). Monitor: falha de coleta acima de 5 por cento em 24h."),
      ("p", "ADR-002: Supabase Postgres com contas, coletas e erros. Descartados SQLite (sem concorrencia) e planilha (sem integridade). Monitor: fila de erros por dia."),
    ]),
    ("5. Entregas", [
      ("ul", ["1-standards/01-formato-e-ciclo-de-vida-adr.md: formato e ciclo.", "1-standards/02-exemplos-reais-adr.md: resumos comentados.", "2-implementacao/01-template-adr.md: template de 1 pagina.", "02-adr-001 e 03-adr-002: ADRs reais integrais."]),
    ]),
    ("6. Metricas e proximos passos", [
      ("table", ["Metrica", "Atual", "Meta"], [
        ["ADRs registrados", "2", "6"],
        ["Decisoes refeitas no trimestre", "3", "0"],
        ["Tempo para achar um motivo", "dias", "minutos"],
      ]),
      ("p", "Proximos passos: criar docs/adr no repo, exigir ADR para decisao cara, revisao anual com dono definido."),
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
    r = p.add_run('Documento Tecnico de PDI'); r.font.size = Pt(12); r.font.color.rgb = RGBColor(0x6B,0x7A,0x8A)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(16)
    for line in [f"Autor: {D['autor']}", f"Unidade: {D['unidade']}", f"Data: {D['data']}",
                 f"Area: {D['area']}", "Status: Entregue (desenvolvido)"]:
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
