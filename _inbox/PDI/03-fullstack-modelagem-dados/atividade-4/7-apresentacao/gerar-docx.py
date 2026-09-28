#!/usr/bin/env python3
"""Gera pdi-fullstack-modelagem-dados-a4.docx (conteúdo real da atividade)."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE = os.path.dirname(os.path.abspath(__file__))
ACCENT = RGBColor(0x8B, 0x45, 0x13)
GRAY = RGBColor(0x6B, 0x7A, 0x8A)

TITLE = "Otimização de Core Web Vitals (LCP/INP/CLS) com Diagnóstico Real"

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
for s in doc.sections:
    s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5); s.left_margin = Cm(3); s.right_margin = Cm(3)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(110)
r = p.add_run("PDI"); r.bold = True; r.font.size = Pt(14); r.font.color.rgb = ACCENT
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(TITLE); r.bold = True; r.font.size = Pt(23)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(28)
r = p.add_run("Documento Técnico de PDI"); r.font.size = Pt(12); r.font.color.rgb = GRAY
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(16)
for line in ["Autor: Marcos Luciano (marcosluciano.rodrigues@v4company.com)",
             "Unidade: FV Marketing / V4 Company",
             "Área: Automação & Infraestrutura",
             "Data: Agosto 2026", "Status: Entregue (desenvolvido)"]:
    rr = p.add_run(line + "\n"); rr.font.size = Pt(11); rr.font.color.rgb = RGBColor(0x49, 0x55, 0x60)
doc.add_page_break()


def h2(t):
    hh = doc.add_heading(t, level=2)
    for r in hh.runs:
        r.font.color.rgb = ACCENT


def tbl(headers, rows):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = "Light Grid Accent 1"
    for i, c in enumerate(headers):
        t.rows[0].cells[i].text = str(c)
    for row in rows:
        cells = t.add_row().cells
        for i, c in enumerate(row):
            cells[i].text = str(c)


h2("1. Contexto")
doc.add_paragraph("Portais com LCP próximo de 4s, INP ruim ao clicar em ações e CLS ao carregar cards. CWV e sinal de ranqueamento e de retenção.")
h2("2. Diagnóstico")
tbl(["Métrica", "Campo", "Alvo"], [["LCP", "4.1 s", "<= 2.5 s"], ["INP", "410 ms", "<= 200 ms"], ["CLS", "0.22", "<= 0.1"]])
doc.add_paragraph("LCP: hero sem fetchpriority nem preconnect. INP: handler síncrono bloqueia. CLS: cards sem aspect-ratio.")
h2("3. Solução (ADR-034)")
doc.add_paragraph("Ordem de otimização LCP, INP e depois CLS, pelo maior ROI. Medir no CrUX antes de cada mudança.")
doc.add_paragraph("Entregas: 1-standards/CWV-DIAGNOSTICO.md e CORE-WEB-VITALS.md, 2-code/cwv_fixes.html e 3-supabase/field_cwv.py (baseline de campo via CrUX).")
h2("4. Como funciona")
for x in ["field_cwv.py coleta o baseline de campo (p75, janela de 28 dias).",
          "LCP: preconnect + fetchpriority=high no hero + AVIF.",
          "INP: chunks com dynamic import + debounce nas ações.",
          "CLS: aspect-ratio e min-height nos cards; nada inserido acima do fold via JS tardio.",
          "Re-medir em 28 dias e confirmar LCP<=2.5, INP<=200, CLS<=0.1."]:
    doc.add_paragraph(x, style="List Bullet")
h2("5. Validação")
for x in ["Baseline de campo via field_cwv.py.",
          "Aplicar correções; re-medir em 28 dias.",
          "Confirmar LCP<=2.5, INP<=200, CLS<=0.1."]:
    doc.add_paragraph(x, style="List Bullet")
h2("6. Métricas e SLO")
tbl(["SLO", "Alvo"], [["LCP p75", "<= 2.5 s"], ["INP p75", "<= 200 ms"], ["CLS p75", "<= 0.1"]])
h2("7. Decisões e tradeoffs")
for x in ["Ordem LCP, INP e depois CLS: CLS visível continua um ciclo; LCP de 4,1s afasta mais usuário.",
          "CrUX antes de cada mudança: ciclo de confirmação de 28 dias; Lighthouse guia o dia a dia.",
          "priority só no hero: priority na imagem errada atrasa o resto.",
          "Dynamic import por rota: primeiro uso de chat ou mapa pode atrasar um chunk.",
          "Reserva fixa de layout: espaço vazio breve em conteúdo variável, melhor que o salto."]:
    doc.add_paragraph(x, style="List Bullet")
h2("8. Impacto no negócio")
doc.add_paragraph("Meta de 75% das sessões no 'bom' (LCP até 2,5s, INP até 200ms, CLS até 0,1), o que reduz abandono no portal de agentes e protege tráfego orgânico sem reescrever o front.")
h2("9. Referências de estudo")
for x in ["Curso: Learn Performance (web.dev, Google)",
          "Vídeo: Core Web Vitals (Google Chrome Developers, YouTube)",
          "Doc oficial: Web Vitals, https://web.dev/vitals/ (verificada em 2026-09-28)",
          "Doc oficial: PageSpeed Insights, https://developers.google.com/speed/docs/insights/v5/about (verificada em 2026-09-28)"]:
    doc.add_paragraph(x, style="List Bullet")
h2("10. Status final")
doc.add_paragraph("Desenvolvido e em homologação. Próximos passos: Lighthouse CI no pipeline e RUM de INP por rota.")

out = os.path.join(HERE, "pdi-fullstack-modelagem-dados-a4.docx")
doc.save(out)
print("DOCX:", out)
