#!/usr/bin/env python3
"""Gera o DOCX da atividade 1 (padrão PDI sênior, paleta #8b4513/#1a1f24/#6b7a8a)."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

D = {
  "title": "Modelo C4 na Prática Aplicado ao Orquestrador de Automação V4",
  "slug": "arquitetura-documentada-a1",
  "autor": "Marcos Luciano",
  "unidade": "FV Marketing / V4 Company",
  "data": "Setembro 2026",
  "área": "Automação & Infraestrutura",
  "sections": [
    ("1. Contexto", [
      ("p", "O Orquestrador de Automação V4 executa coleta de métricas, disparo de emails e sincronização da operação FV Marketing com n8n (:5678), workers Python (:8000), Supabase Postgres e painel Next.js (:3000), falando com Meta Ads API e Gmail API."),
      ("p", "Cada pessoa desenhava o sistema de um jeito. Onboarding de 3 dias e incidentes de coleta sem mapa de diagnóstico."),
    ]),
    ("2. Diagnóstico", [
      ("table", ["Sintoma", "Causa"], [
        ["Onboarding de 3 dias", "Sem diagrama de contexto oficial"],
        ["Incidente vira adivinhação", "Sem containers com portas e dependências"],
        ["Mudança no n8n quebra coleta", "Componentes do n8n não mapeados"],
      ]),
    ]),
    ("3. Solução", [
      ("p", "Aplicar os 4 níveis do C4 sobre o sistema real: contexto, containers, componentes do n8n e a função executar_com_retry. Structurizr DSL como fonte única e Mermaid como espelho no repo."),
      ("note", "PR que muda container exige DSL e Mermaid atualizados juntos."),
    ]),
    ("4. Como funciona (coleta Meta Ads)", [
      ("ol", ["Trigger agenda coleta-meta-ads a cada 30 min no n8n.", "Subworkflow chama workers via webhook com conta e janela.", "executar_com_retry com backoff 30s, 60s e 120s.", "Worker grava métricas no Supabase; falha vira fila de erros.", "Painel Next.js exibe verba ao gestor."]),
    ]),
    ("5. Entregas", [
      ("ul", ["1-standards/01-guia-c4-aplicado.md: guia dos 4 níveis.", "1-standards/02-diagramas-sistema-automacao.md: diagramas reais.", "2-implementacao/01-workspace-c4.dsl: fonte Structurizr.", "2-implementacao/02-exemplo-mermaid-c4.md: espelho Mermaid.", "2-implementacao/03-checklist-revisao-c4.md: checklist de PR."]),
    ]),
    ("6. Métricas e próximos passos", [
      ("table", ["Métrica", "Atual", "Meta"], [
        ["Sistemas com contexto", "1", "3"],
        ["Containers documentados", "4 de 4", "4 de 4"],
        ["Diagramas desatualizados +30d", "0", "0"],
        ["Onboarding de operador", "3 dias", "1 dia"],
      ]),
      ("p", "Próximos passos: publicar Structurizr Lite com link interno, incluir contexto no onboarding, revisar a cada mudança de container."),
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
