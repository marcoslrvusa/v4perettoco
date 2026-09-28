#!/usr/bin/env python3
"""Gera o DOCX da atividade 3 (padrão PDI sênior, paleta #8b4513/#1a1f24/#6b7a8a)."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

D = {
  "title": "Documentação como Código, Mermaid e Diagramas Versionados",
  "slug": "arquitetura-documentada-a3",
  "autor": "Marcos Luciano",
  "unidade": "FV Marketing / V4 Company",
  "data": "Setembro 2026",
  "área": "Automação & Infraestrutura",
  "sections": [
    ("1. Contexto", [
      ("p", "Diagramas em arquivos soltos fora do git: sem versão certa, sem revisão em PR, sempre desatualizados. Incidente começava caçando print no chat."),
    ]),
    ("2. Diagnóstico", [
      ("table", ["Sintoma", "Causa"], [
        ["Ninguém acha a versão certa", "Desenho solto fora do git"],
        ["PR não revisa diagrama", "Imagem binária sem diff"],
        ["Doc mente após mudança", "Diagrama longe do código"],
      ]),
    ]),
    ("3. Solução", [
      ("p", "Diagramas como texto Mermaid no repo: flowchart para caminhos e retries, sequenceDiagram para contratos n8n e worker. Dois exemplos reais, guia rápido e validação no CI com mermaid-cli."),
      ("note", "C4 detalhado continua no Structurizr DSL da atividade 1. Cada ferramenta no seu quadrado."),
    ]),
    ("4. Como funciona", [
      ("ol", ["Edita o .md com Mermaid junto do worker.", "PR com diff legível do desenho.", "CI roda mmdc e quebra em sintaxe invalida.", "Revisor aplica checklist de docs vivos.", "GitHub renderiza a versão certa."]),
    ]),
    ("5. Entregas", [
      ("ul", ["1-standards/01-docs-como-codigo-fundamentos.md: regras.", "02-mermaid-guia-rapido.md: sintaxe mínima.", "01-exemplo-fluxo-coleta.md e 02-exemplo-sequencia-webhook.md: reais.", "03-checklist-docs-vivos.md: revisão de PR."]),
    ]),
    ("6. Métricas e próximos passos", [
      ("table", ["Métrica", "Atual", "Meta"], [
        ["Diagramas vivos no repo", "4", "10"],
        ["Diagramas soltos fora do git", "6", "0"],
        ["PRs com diagrama revisado", "0", "5"],
      ]),
      ("p", "Próximos passos: converter os 3 fluxos críticos, ligar o CI, apagar soltos após migração."),
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
