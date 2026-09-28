#!/usr/bin/env python3
"""Gera o DOCX desta atividade a partir de report.json (padrao PDI senior) + 3 secoes de autoria."""
import json, os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "report.json"), encoding="utf-8") as f:
    D = json.load(f)

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
    for line in [f"Autor: {D['autor']}", f"Unidade: FV Marketing / V4 Company", f"Data: Agosto 2026",
                 f"Area: 04 Engenharia de IA, RAG e Vetores", "Status: Entregue (desenvolvido)"]:
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
        elif kind == "h":
            doc.add_heading(rest[0], level=3)
        elif kind == "note":
            p = doc.add_paragraph(); p.add_run("Nota: ").bold = True; p.add_run(rest[0])
        elif kind == "warn":
            p = doc.add_paragraph(); p.add_run("Atencao: ").bold = True; p.add_run(rest[0])
        elif kind == "code":
            p = doc.add_paragraph(rest[1]); p.style = doc.styles['No Spacing']
            for r in p.runs: r.font.name = 'Consolas'; r.font.size = Pt(9)

BASE_SECTIONS = [('1. Contexto', [['p', 'Framework de custo de LLM com custo por tarefa, cache de prompt, roteamento por complexidade e budget, contra uso de modelo maxi para tudo com custo 10x.']]), ('2. Diagnostico', [['p', 'Modelo unico sem roteamento, sem cache a mesma pergunta paga 2x, e custo invisivel impede precificar ao cliente.']]), ('3. Solucao', [['p', 'Regra trivial para leve, complexo para forte e repetido para cache, com ledger por fluxo, budget por cliente e batch assincrono dentro do SLA.']]), ('4. Entregas', [['ul', ['LLM-COST.md e COST-MONITORING.md', 'cost_calc.py e track_cost.py com ledger.save', 'BUDGET.md e usage_schema.sql']]]), ('5. Metricas', [['ul', ['Custo por tarefa menor ou igual a baseline vezes 0.4', 'Cache hit maior ou igual a 30 por cento', 'Budget com alerta em 80 por cento', 'Reducao maior ou igual a 85 por cento com score maior ou igual a 0.90']]]), ('6. Status final', [['p', 'Desenvolvido e em homologacao. Aguarda revisao antes de producao.']])]

EXTRA_SECTIONS = [('9. Decisoes e tradeoffs', [['ul', ['Roteamento por complexidade em vez de modelo maxi para tudo: troquei simplicidade por governanca, porque o maxi custa 10x e a regra trivial vai para leve e complexo vai para forte.', 'Cache semantico com meta de hit maior ou igual a 30 por cento e regra de nunca cachear PII: aceitei gestao de invalidacao para nao pagar 2x a mesma pergunta, sem expor dado sensivel.', 'Custo por tarefa com meta menor ou igual a baseline vezes 0.4 e ledger por fluxo: escolhi contabilidade visivel para permitir precificar ao cliente.', 'Budget por cliente com alerta em 80 por cento: preferi travar crescimento de gasto cedo a descobrir estouro na fatura.', 'Batch assincrono respeitando SLA: empacotei chamadas para buscar desconto preservando score maior ou igual a 0.90 e reducao maior ou igual a 85 por cento.']]]), ('10. Impacto no negocio', [['p', 'O framework com custo por tarefa menor ou igual a baseline vezes 0.4, hit de cache maior ou igual a 30 por cento e alerta em 80 por cento do budget torna o agente precificavel e reduz o custo mensal em meta maior ou igual a 85 por cento, o que destrava margem e evita subsidio invisivel de inferencia.']]), ('11. Referencias de estudo', [['ul', ['Curso: FinOps for AI and LLM Cost Optimization, plataforma Udemy.', 'Video: Reducao de custo de LLM com cache e roteamento, plataforma YouTube, canal Y Combinator.', 'Doc oficial: Guia de precos e tokens da API, documentacao oficial OpenAI.', 'Doc oficial: Guia de prompt caching, documentacao oficial Anthropic.']]])]

cover()
for title, blocks in (BASE_SECTIONS + EXTRA_SECTIONS):
    add_section(title, blocks)
out = os.path.join(HERE, "pdi-" + D['slug'] + ".docx")
doc.save(out)
print("DOCX:", out)
