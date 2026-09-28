#!/usr/bin/env python3
"""Gera pdi-fullstack-modelagem-dados-a1.docx (conteudo real da atividade)."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE = os.path.dirname(os.path.abspath(__file__))
ACCENT = RGBColor(0x8B, 0x45, 0x13)
GRAY = RGBColor(0x6B, 0x7A, 0x8A)

TITLE = "Queries Complexas e Indexacao no Supabase (PostgreSQL)"

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
for s in doc.sections:
    s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5); s.left_margin = Cm(3); s.right_margin = Cm(3)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(110)
r = p.add_run("PDI"); r.bold = True; r.font.size = Pt(14); r.font.color.rgb = ACCENT
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(TITLE); r.bold = True; r.font.size = Pt(23)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(28)
r = p.add_run("Documento Tecnico de PDI"); r.font.size = Pt(12); r.font.color.rgb = GRAY
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(16)
for line in ["Autor: Marcos Luciano (marcosluciano.rodrigues@v4company.com)",
             "Unidade: FV Marketing / V4 Company",
             "Area: Automacao & Infraestrutura",
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
doc.add_paragraph("O Supabase que sustenta a operacao SDR IA e a fila mt_jobs sofria com queries sem plano de execucao: JOINs pesados sem indice, leituras sequenciais em tabelas de milhoes de linhas, funcoes com RLS no caminho quente e autovacuum desconfigurado. Resultado: timeouts de webhook, dashboards de 8s ou mais e fila com backlog invisivel.")
h2("2. Diagnostico")
tbl(["Caso", "Sintoma", "Causa-raiz"],
    [["Fila mt_jobs", "pick de 1,8s com Seq Scan", "filtro sem indice composto + LEFT JOIN desnecessario"],
     ["Sync CRM", "JOIN de auditoria em 4,2s", "FK sem indice + filtro em coluna sem indice"],
     ["Dashboard", "agregacao em 8,4s sobre 12M linhas", "count(DISTINCT) + janela sem materializacao"]])
h2("3. Solucao")
doc.add_paragraph("Metodo EXPLAIN ANALYZE como diagnostico, indices certos por padrao de acesso (B-tree composto, GIN, BRIN), particionamento por range com TTL, autovacuum calibrado e RLS com policies simples. Padrao em 1-standards/PERFORMANCE-SUPABASE.md; PoCs adversariais em 2-sql; casos reais em 3-casos.")
h2("4. Como funciona")
for x in ["Rodar EXPLAIN (ANALYZE, BUFFERS) e procurar Seq Scan, Nested Loop com re-scan, Sort explicito e spill em temp file.",
          "Criar indice composto na ordem igualdade, range e depois ORDER BY.",
          "GIN para arrays/jsonb, BRIN para series temporais ordenadas por tempo.",
          "Particionar append-only por range com job de TTL; calibrar autovacuum e monitorar bloat.",
          "Aplicar em producao com CREATE INDEX CONCURRENTLY fora de pico."]:
    doc.add_paragraph(x, style="List Bullet")
h2("5. Entregas")
tbl(["Pasta", "Conteudo"],
    [["1-standards", "PERFORMANCE-SUPABASE.md (planos, indices, particionamento, autovacuum, RLS)"],
     ["2-sql", "5 PoCs adversariais antes/depois + 06-planos-antes-depois.md"],
     ["3-casos", "3 gargalos reais (fila mt_jobs, sync CRM, dashboard)"],
     ["7-apresentacao", "deck, demo, relatorio HTML/DOCX/PDF"]])
h2("6. Metricas de sucesso")
tbl(["Metrica", "Atual", "Meta"],
    [["Worker da fila mt_jobs (pick job)", "1.8s (Seq Scan)", "< 10ms"],
     ["JOIN de sync CRM (auditoria 30d)", "4.2s", "< 250ms"],
     ["Dashboard de performance (janela 7d)", "8.4s", "< 1.5s"],
     ["Bloat em tabelas de log", "nao monitorado", "< 20%"],
     ["Timeout de webhook por query lenta", "~3/dia", "0"]])
h2("7. Decisoes e tradeoffs")
for x in ["Nenhuma query sem EXPLAIN (ANALYZE, BUFFERS): exige disciplina de revisao e staging com volumetria representativa.",
          "Indice composto igualdade, range e depois ORDER BY: escrita paga um pouco mais por indice; aceito pela leitura do worker a cada 15s.",
          "BRIN 10x menor que B-tree em created_at: so vale se a ordem fisica acompanha o tempo.",
          "Particionamento com TTL: exige job de manutencao; sem ele a tabela cresce sem limite.",
          "CREATE INDEX CONCURRENTLY fora de pico: criacao mais lenta e fora de transacao; janela de deploy precisa prever."]:
    doc.add_paragraph(x, style="List Bullet")
h2("8. Impacto no negocio")
doc.add_paragraph("Com os indices e o metodo EXPLAIN, o pick fica abaixo de 10ms, o sync abaixo de 250ms e o dashboard abaixo de 1,5s, zerando timeouts e devolvendo visibilidade da fila sem trocar de banco.")
h2("9. Referencias de estudo")
for x in ["Curso: SQL Performance Explained, de Markus Winand (use-the-index-luke.com)",
          "Video: Postgres Performance (Supabase, YouTube)",
          "Doc oficial: Using EXPLAIN (PostgreSQL), https://www.postgresql.org/docs/current/using-explain.html (verificada em 2026-09-28)",
          "Doc oficial: Query Optimization (Supabase), https://supabase.com/docs/guides/database/query-optimization (verificada em 2026-09-28)"]:
    doc.add_paragraph(x, style="List Bullet")
h2("10. Status final")
doc.add_paragraph("Desenvolvido e em homologacao. Nenhum indice foi aplicado em producao nesta etapa, apenas documentado e provado. Proximos passos: rodar 06-planos-antes-depois.md no staging, aplicar indices com CONCURRENTLY, configurar job de particionamento e validar RLS.")

out = os.path.join(HERE, "pdi-fullstack-modelagem-dados-a1.docx")
doc.save(out)
print("DOCX:", out)
