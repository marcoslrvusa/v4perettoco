#!/usr/bin/env python3
"""Gera pdi-fullstack-modelagem-dados-a3.docx (conteúdo real da atividade)."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE = os.path.dirname(os.path.abspath(__file__))
ACCENT = RGBColor(0x8B, 0x45, 0x13)
GRAY = RGBColor(0x6B, 0x7A, 0x8A)

TITLE = "Arquitetura Serverless para Processamento Assíncrono (event-driven)"

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
doc.add_paragraph("Clientes enviam planilhas de 1k a 50k linhas. Worker always-on ficava 90% ocioso. Pico de 200 uploads derrubava o worker.")
h2("2. Diagnóstico")
doc.add_paragraph("Processamento síncrono no request gera timeout. Sem idempotência, reprocessar duplicava leads. Sem limite de concorrência, a rajada derruba tudo.")
tbl(["Hoje", "Alvo"], [["worker ocioso", "scale to zero"], ["sem fila", "queue + retry"], ["sem isolamento", "1 falha não derruba"]])
h2("3. Solução (ADR-033)")
doc.add_paragraph("Fila + função + store: upload grava objeto e publica evento; consumo com concorrência limitada e dedup. Rejeitada a via direta Lambda no upload, sem backpressure.")
doc.add_paragraph("Padrão em 1-standards/SERVERLESS-STANDARD.md e SERVERLESS-SECURITY.md; handler real em 2-code/process_upload.py; infra em infra/terraform_serverless.tf.")
h2("4. Como funciona")
for x in ["Upload grava no store e publica file.uploaded com metadados (URL).",
          "Consumer com concorrência limitada (10) processa com dedup hash(arquivo + tenant).",
          "Falha vai para retry; após N tentativas, DLQ com replay manual.",
          "Timeout de até 60s; jobs longos vão para Cloud Tasks ou fila.",
          "Segredos em Secret Manager e DB via pooler com TLS."]:
    doc.add_paragraph(x, style="List Bullet")
h2("5. Validação")
for x in ["Enviar 200 planilhas; medir paralelismo e custo.",
          "Forcar falha parcial; confirmar retry sem duplicata.",
          "1 arquivo ruim não afeta os outros."]:
    doc.add_paragraph(x, style="List Bullet")
h2("6. Métricas e SLO")
tbl(["SLO", "Alvo"], [["Custo/1k planilhas", "< R$ 0,20"], ["P95", "< 60 s"], ["Duplicatas", "0"]])
h2("7. Decisões e tradeoffs")
for x in ["Nunca processar no request: resposta assíncrona exige acompanhar status por evento; elimina o timeout.",
          "Idempotência por dedup: custa uma leitura por evento e um store de chaves em prod.",
          "DLQ após N tentativas: replay manual em vez de fila travada na mensagem veneno.",
          "Payload só com metadados: fila leve; consumer busca o objeto no store.",
          "Não usar com carga constante alta: worker always-on sai mais barato; cold start mitigado com concorrência provisionada."]:
    doc.add_paragraph(x, style="List Bullet")
h2("8. Impacto no negócio")
doc.add_paragraph("Custo abaixo de R$ 0,20 por mil planilhas, escala a zero no vale e p95 abaixo de 60s com zero duplicatas, o que viabiliza campanhas de importação em rajada sem provisionar servidor parado.")
h2("9. Referências de estudo")
for x in ["Curso: AWS Lambda e Serverless na prática (Alura)",
          "Vídeo: Serverless em 100 segundos (Fireship, YouTube)",
          "Doc oficial: Cloud Run functions, https://cloud.google.com/functions/docs (verificada em 2026-09-28)",
          "Doc oficial: Terraform, https://developer.hashicorp.com/terraform/docs (verificada em 2026-09-28)"]:
    doc.add_paragraph(x, style="List Bullet")
h2("10. Status final")
doc.add_paragraph("Desenvolvido e em homologação. Próximos passos: observabilidade por trace_id e workers de agentes no mesmo molde.")

out = os.path.join(HERE, "pdi-fullstack-modelagem-dados-a3.docx")
doc.save(out)
print("DOCX:", out)
