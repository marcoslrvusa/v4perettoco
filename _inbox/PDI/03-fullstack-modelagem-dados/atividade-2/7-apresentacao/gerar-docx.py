#!/usr/bin/env python3
"""Gera pdi-fullstack-modelagem-dados-a2.docx (conteúdo real da atividade)."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE = os.path.dirname(os.path.abspath(__file__))
ACCENT = RGBColor(0x8B, 0x45, 0x13)
DARK = RGBColor(0x1A, 0x1F, 0x24)
GRAY = RGBColor(0x6B, 0x7A, 0x8A)

TITLE = "APIs Modulares de Missão Crítica (FastAPI) com Paginação, Cache e Rate Limiting"

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
doc.add_paragraph("Endpoints internos servem 3 a 5 sistemas. Listas de 5k a 80k sem paginação estouravam memória. Sem rate limit, 2k req/min derrubavam o Postgres.")
h2("2. Diagnóstico")
doc.add_paragraph("Offset em tabelas grandes equivale a full scan. Conexões não pooladas levam a esgotamento. Sem distinção entre 4xx e 5xx o cliente não sabe quando retentar.")
tbl(["Sintoma", "Hoje", "Alvo"], [["Paginação", "offset", "cursor-based"], ["Cache", "nenhum", "Redis + invalidação"],
     ["Rate limit", "ausente", "por api_key"], ["Erro 5xx", "stack cru", "envelope"]])
h2("3. Solução (ADR-032)")
doc.add_paragraph("FastAPI + Redis + slowapi: stack async e madura. Cursor-based para estabilidade e cache por chave com invalidação no write.")
doc.add_paragraph("Padrão entregue em 1-standards/API-STANDARD.md e implementação real em 2-code/main_api.py (paginação cursor, cache Redis com TTL 30s, rate limit 100 req/min, envelope de erro com trace_id).")
h2("4. Como funciona")
for x in ["Cliente chama GET /v1/leads?after=<cursor>&limit=50.",
          "Rate limit por chave: estourou 100 req/min, responde 429 + Retry-After.",
          "Cache: segundo hit da mesma chave vem do Redis; write invalida a chave.",
          "Fallback: Redis fora, o caminho direto no banco responde.",
          "Erros 4xx não retentam; 5xx pedem retry com backoff."]:
    doc.add_paragraph(x, style="List Bullet")
h2("5. Validação")
for x in ["Carga com k6: 200 req/s por 5 min.", "Estouro de quota responde 429.", "Segundo hit vem do Redis."]:
    doc.add_paragraph(x, style="List Bullet")
h2("6. Métricas e SLO")
tbl(["SLO", "Alvo"], [["p95 (lista)", "< 200 ms cache hit"], ["Rate limit", "100/min/key"], ["Disponibilidade", ">= 99.5%"]])
h2("7. Decisões e tradeoffs")
for x in ["Cursor-based em vez de offset: custo estável por página; perde salto para página N, aceito porque o consumo e sequencial.",
          "Cache Redis TTL 30s + stale-while-revalidate 60s com invalidação no write: janela de segundos com dado defasado, aceita para listagem de leads.",
          "Rate limit 100 req/min por chave: cliente em pico recebe 429 e implementa backoff; um cliente não derruba os demais.",
          "Fallback para o banco sem cache: disponibilidade acima de p95 nesse cenário.",
          "Envelope com trace_id e 4xx vs 5xx: exige log com trace_id para depurar sem stack cru."]:
    doc.add_paragraph(x, style="List Bullet")
h2("8. Impacto no negócio")
doc.add_paragraph("Com cursor, cache e rate limit, o p95 da lista fica abaixo de 200ms no hit e a disponibilidade atinge 99,5%, o que protege a operação de SDR e CRM em pico de campanha sem aumentar custo de banco.")
h2("9. Referências de estudo")
for x in ["Curso: FastAPI Beyond CRUD (TalkPython Training)",
          "Vídeo: Curso completo de FastAPI (freeCodeCamp, YouTube)",
          "Doc oficial: Documentação do FastAPI, https://fastapi.tiangolo.com/ (verificada em 2026-09-28)",
          "Doc oficial: Redis, https://redis.io/ (verificado em 2026-09-28)"]:
    doc.add_paragraph(x, style="List Bullet")
h2("10. Status final")
doc.add_paragraph("Desenvolvido e em homologação. Próximos passos: gateway com OAuth2 e tracing OTel.")

out = os.path.join(HERE, "pdi-fullstack-modelagem-dados-a2.docx")
doc.save(out)
print("DOCX:", out)
