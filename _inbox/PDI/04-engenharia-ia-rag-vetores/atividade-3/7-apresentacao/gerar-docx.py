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

BASE_SECTIONS = [('1. Contexto', [['p', 'Orquestracao multi-agente com supervisor mais especialistas, handoff explicito, isolamento de contexto, timeouts e fallbacks, contra agente unico com prompt de 8k tokens.']]), ('2. Diagnostico', [['p', 'Sem SRP entre agentes, com contexto compartilhado ha vazamento de PII, sem handoff formal e sem timeout um worker travado para o fluxo.']]), ('3. Solucao', [['p', 'Supervisor com route(intent), workers researcher, coder e reviewer isolados, handoff com contexto minimo, memoria de curto e longo prazo, max hops e modelo leve no supervisor.']]), ('4. Entregas', [['ul', ['MULTI-AGENT.md e MULTIAGENT-PROTOCOL.md', 'orchestrator.py, supervisor.py, memory.py e workers isolados', 'handoff_schema.py e handoff.md']]]), ('5. Metricas', [['ul', ['Timeout por agente menor ou igual a 15 s', 'Handoff com fallback 100 por cento', 'Vazamento 0', 'Sucesso de cerca de 49 por cento para cerca de 97 por cento', 'Meta maior ou igual a 95 por cento em tarefas de 3 etapas']]]), ('6. Status final', [['p', 'Desenvolvido e em homologacao. Aguarda revisao antes de producao.']])]

EXTRA_SECTIONS = [('9. Decisoes e tradeoffs', [['ul', ['Supervisor com handoff tipado em vez de agente unico com prompt de 8k tokens: aceitei mais nos para ganhar foco, teste por papel e fronteira clara entre triagem, consulta e proposta.', 'Contexto proprio por agente com passagem de resumo minimo: escolhi isolamento para zerar vazamento, com meta de 0 ocorrencias, mesmo com custo de serializar o handoff.', 'Timeout menor ou igual a 15 s por agente com fallback em 100 por cento dos handoffs: preferi degradar com re-rota a travar o fluxo quando um worker trava.', 'Max hops contra loop e supervisor com modelo leve: contive custo e recursao em vez de deixar o supervisor reiterar sem limite.', 'Memoria de curto e longo prazo com estado preservado: troquei reexecucao do zero por retomada a partir do ultimo handoff valido.']]]), ('10. Impacto no negocio', [['p', 'A orquestracao com timeout menor ou igual a 15 s, fallback em 100 por cento e vazamento 0 eleva o sucesso de cerca de 49 por cento para cerca de 97 por cento, com meta maior ou igual a 95 por cento em tarefas de 3 etapas, o que reduz retrabalho por contaminacao e da previsibilidade de custo por papel.']]), ('11. Referencias de estudo', [['ul', ['Curso: Multi-AI Agent Systems with LangGraph, plataforma DeepLearning.AI.', 'Video: Padroes de orquestracao com supervisor e handoff, plataforma YouTube, canal LangChain.', 'Doc oficial: Documentacao do LangGraph para grafos de agentes, documentacao oficial LangChain.', 'Doc oficial: Guia de function calling e structured outputs, documentacao oficial OpenAI.']]])]

cover()
for title, blocks in (BASE_SECTIONS + EXTRA_SECTIONS):
    add_section(title, blocks)
out = os.path.join(HERE, "pdi-" + D['slug'] + ".docx")
doc.save(out)
print("DOCX:", out)
