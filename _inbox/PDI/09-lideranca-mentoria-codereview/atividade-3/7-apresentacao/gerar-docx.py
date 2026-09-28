#!/usr/bin/env python3
"""Gera o DOCX da Atividade 3 da Trilha 09 (conteúdo inline, paleta PDI)."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = "Delegação e Feedback: Matriz de Delegação e Feedback SBI"
SLUG = "lideranca-mentoria-codereview-a3"

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
for s in doc.sections:
    s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5); s.left_margin = Cm(3); s.right_margin = Cm(3)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(110)
r = p.add_run("PDI"); r.bold = True; r.font.size = Pt(14); r.font.color.rgb = RGBColor(0x8B, 0x45, 0x13)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(TITLE); r.bold = True; r.font.size = Pt(23)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(28)
r = p.add_run("Documento Técnico de PDI"); r.font.size = Pt(12); r.font.color.rgb = RGBColor(0x6B, 0x7A, 0x8A)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(16)
for line in ["Autor: PDI Marcos Luciano - marcosluciano.rodrigues@v4company.com",
             "Unidade: FV Marketing / V4 Company - Automação & Infraestrutura",
             "Data: Setembro 2026", "Área: Automação & Infraestrutura",
             "Status: Entregue (desenvolvido)"]:
    rr = p.add_run(line + "\n"); rr.font.size = Pt(11); rr.font.color.rgb = RGBColor(0x49, 0x55, 0x60)
doc.add_page_break()

def section(title, blocks):
    hh = doc.add_heading(title, level=2)
    for r in hh.runs: r.font.color.rgb = RGBColor(0x8B, 0x1E, 0x1E)
    for kind, *rest in blocks:
        if kind == "p":
            doc.add_paragraph(rest[0])
        elif kind in ("ul", "ol"):
            for x in rest[0]:
                doc.add_paragraph(x, style="List Bullet" if kind == "ul" else "List Number")
        elif kind == "table":
            h, rows = rest
            t = doc.add_table(rows=1, cols=len(h)); t.style = "Light Grid Accent 1"
            for i, c in enumerate(h): t.rows[0].cells[i].text = str(c)
            for row in rows:
                cells = t.add_row().cells
                for i, c in enumerate(row): cells[i].text = str(c)

section("1. Contexto", [("p", "O líder centraliza por medo: delega a tarefa, segura a autoridade e refaz no final. O liderado ou espera ordem para tudo ou decide além da conta."),
    ("p", "Feedback some por meses e explode genérico, sem exemplo e sem pedido. Sem fato e sem saída, gera defesa, não mudança.")])
section("2. Diagnóstico", [("p", "Só 15% das tarefas delegadas tem critério escrito, 2 SBIs por mês no time, 40% de retrabalho do líder e 25h semanais do líder em execução. Causa raiz: delegação binária sem nível e feedback sem método."),
    ("table", ["Sintoma", "Atual"], [["Delegadas com critério", "15%"], ["SBIs por mês", "2"], ["Retrabalho do líder", "40%"], ["Horas operacionais do líder", "25h/sem"]])])
section("3. Solução", [("p", "Matriz de 5 níveis, checklist de pacote delegável, regra do indelegável e roteiro SBI com exemplos prontos e controle mensal de proporção reforco/correcao."),
    ("ul", ["STD-01: níveis, progressão, indelegável, erros clássicos", "STD-02: modelo SBI e exemplos prontos", "TPL matriz por liderado", "TPL roteiro SBI com controle mensal"])])
section("4. Como funciona", [("ol", ["Classificar o pacote na matriz de 1 a 5", "Escrever resultado, restrições, nível, checkpoint e pronto", "Executar sem interferência até o checkpoint", "Feedback SBI em até 48h, 1 reforco para cada correção", "Revisar o nível a cada ciclo"])])
section("5. Entregas", [("table", ["Arquivo", "Conteúdo"], [["STD-01-matriz-delegacao.md", "Níveis e progressão"], ["STD-02-feedback-sbi.md", "Modelo e exemplos"], ["TPL-matriz-delegacao.md", "Mapa por liderado"], ["TPL-roteiro-feedback-sbi.md", "Preparo e controle"]])])
section("6. Métricas de sucesso", [("table", ["Métrica", "Atual", "Meta"], [["Delegadas com critério", "15%", "80% (meta)"], ["SBIs por mês", "2", "12 (meta)"], ["Retrabalho do líder", "40%", "10% (meta)"], ["Horas operacionais", "25h", "10h (meta)"]]),
    ("p", "Metas marcadas como (meta) por serem projetadas, não medidas. Revisão de níveis ao fim do mês.")])

out = os.path.join(HERE, "pdi-" + SLUG + ".docx")
doc.save(out)
print("DOCX:", out)
