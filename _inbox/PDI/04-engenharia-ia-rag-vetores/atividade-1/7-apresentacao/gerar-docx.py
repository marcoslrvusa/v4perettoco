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

BASE_SECTIONS = [('1. Contexto', [['p', 'Baseline RAG a partir do curso Building RAG Agents with LLMs (NVIDIA DLI), com chunk 512 e overlap 64, top-k 20 com rerank para top-5, e avaliacao de faithfulness em 10 perguntas.']]), ('2. Diagnostico', [['p', 'Chunk grande gera ruido e chunk pequeno perde contexto. Similaridade pura devolve contexto irrelevante e nao ha metrica de qualidade sem normalizacao de embeddings.']]), ('3. Solucao', [['p', 'Modulo com tokenizacao, embeddings text-embedding-3-small de 1536 dim, similaridade por cosseno com threshold 0.82, guardrails de PII e golden set com 50 pares.']]), ('4. Entregas', [['ul', ['DLI-NOTES.md', 'rag_baseline.py (embed.py, count_tokens, cosine, check_safety, eval_report)', 'CONCLUSAO.md e guardrails.md']]]), ('5. Metricas', [['ul', ['Faithfulness maior ou igual a 0.8', 'Chunk 512 com overlap 64', 'Score medio maior ou igual a 0.90 no golden set', '100 por cento de bloqueio em guardrails']]]), ('6. Status final', [['p', 'Desenvolvido e em homologacao. Aguarda revisao antes de producao.']])]

EXTRA_SECTIONS = [('9. Decisoes e tradeoffs', [['ul', ['Chunk 512 com overlap 64: escolhi coesao contra custo de tokens, porque chunk grande gera ruido e chunk pequeno perde contexto, conforme ADR-041.', 'Top-k 20 com rerank para top-5: aceitei latencia extra do rerank para filtrar o ruido da similaridade pura.', 'Normalizar embeddings de 1536 dim com cosseno e threshold 0.82: padronizei a medida para o score ser comparavel entre textos de tamanhos distintos.', 'Golden set com 50 pares e faithfulness maior ou igual a 0.8 em 10 perguntas: troquei avaliacao no olhometro por gate reproduzivel no CI.', 'Guardrail fail-closed com 100 por cento de bloqueio antes da producao: preferi falso positivo seguro a resposta toxica, fora de dominio ou com PII.']]]), ('10. Impacto no negocio', [['p', 'O baseline com faithfulness maior ou igual a 0.8 e score medio maior ou igual a 0.90 no golden set de 50 pares reduz risco de hallucination em producao e elimina a surpresa de fatura com contagem previa de tokens, o que encurta homologacao e sustenta as atividades seguintes de RAG hibrido e custos.']]), ('11. Referencias de estudo', [['ul', ['Curso: Building RAG Agents with LLMs, plataforma NVIDIA Deep Learning Institute (DLI).', 'Video: RAG from Scratch com chunking, embeddings e avaliacao, plataforma YouTube, canal LangChain.', 'Doc oficial: Guia de embeddings text-embedding-3-small, documentacao oficial OpenAI.', 'Doc oficial: Documentacao do pgvector com indice HNSW, documentacao oficial pgvector.']]])]

cover()
for title, blocks in (BASE_SECTIONS + EXTRA_SECTIONS):
    add_section(title, blocks)
out = os.path.join(HERE, "pdi-" + D['slug'] + ".docx")
doc.save(out)
print("DOCX:", out)
