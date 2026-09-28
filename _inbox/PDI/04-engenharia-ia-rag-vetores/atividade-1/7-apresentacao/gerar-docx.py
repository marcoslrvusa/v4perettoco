#!/usr/bin/env python3
"""Gera o DOCX desta atividade a partir de report.json (padrão PDI sênior) + 3 seções de autoria."""
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
    r = p.add_run('Documento Técnico de PDI'); r.font.size = Pt(12); r.font.color.rgb = RGBColor(0x6B,0x7A,0x8A)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(16)
    for line in [f"Autor: {D['autor']}", f"Unidade: FV Marketing / V4 Company", f"Data: Agosto 2026",
                 f"Área: 04 Engenharia de IA, RAG e Vetores", "Status: Entregue (desenvolvido)"]:
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
            p = doc.add_paragraph(); p.add_run("Atenção: ").bold = True; p.add_run(rest[0])
        elif kind == "code":
            p = doc.add_paragraph(rest[1]); p.style = doc.styles['No Spacing']
            for r in p.runs: r.font.name = 'Consolas'; r.font.size = Pt(9)

BASE_SECTIONS = [('1. Contexto', [['p', 'Baseline RAG a partir do curso Building RAG Agents with LLMs (NVIDIA DLI), com chunk 512 e overlap 64, top-k 20 com rerank para top-5, e avaliação de faithfulness em 10 perguntas.']]), ('2. Diagnóstico', [['p', 'Chunk grande gera ruído e chunk pequeno perde contexto. Similaridade pura devolve contexto irrelevante e não há métrica de qualidade sem normalização de embeddings.']]), ('3. Solução', [['p', 'Módulo com tokenizacao, embeddings text-embedding-3-small de 1536 dim, similaridade por cosseno com threshold 0.82, guardrails de PII e golden set com 50 pares.']]), ('4. Entregas', [['ul', ['DLI-NOTES.md', 'rag_baseline.py (embed.py, count_tokens, cosine, check_safety, eval_report)', 'CONCLUSAO.md e guardrails.md']]]), ('5. Métricas', [['ul', ['Faithfulness maior ou igual a 0.8', 'Chunk 512 com overlap 64', 'Score médio maior ou igual a 0.90 no golden set', '100 por cento de bloqueio em guardrails']]]), ('6. Status final', [['p', 'Desenvolvido e em homologação. Aguarda revisão antes de produção.']])]

EXTRA_SECTIONS = [('9. Decisões e tradeoffs', [['ul', ['Chunk 512 com overlap 64: escolhi coesão contra custo de tokens, porque chunk grande gera ruído e chunk pequeno perde contexto, conforme ADR-041.', 'Top-k 20 com rerank para top-5: aceitei latência extra do rerank para filtrar o ruído da similaridade pura.', 'Normalizar embeddings de 1536 dim com cosseno e threshold 0.82: padronizei a medida para o score ser comparável entre textos de tamanhos distintos.', 'Golden set com 50 pares e faithfulness maior ou igual a 0.8 em 10 perguntas: troquei avaliação no olhômetro por gate reproduzível no CI.', 'Guardrail fail-closed com 100 por cento de bloqueio antes da produção: preferi falso positivo seguro a resposta tóxica, fora de domínio ou com PII.']]]), ('10. Impacto no negócio', [['p', 'O baseline com faithfulness maior ou igual a 0.8 e score médio maior ou igual a 0.90 no golden set de 50 pares reduz risco de hallucination em produção e elimina a surpresa de fatura com contagem previa de tokens, o que encurta homologação e sustenta as atividades seguintes de RAG híbrido e custos.']]), ('11. Referências de estudo', [['ul', ['Curso: Building RAG Agents with LLMs, plataforma NVIDIA Deep Learning Institute (DLI).', 'Vídeo: RAG from Scratch com chunking, embeddings e avaliação, plataforma YouTube, canal LangChain.', 'Doc oficial: Guia de embeddings text-embedding-3-small, documentação oficial OpenAI.', 'Doc oficial: Documentação do pgvector com índice HNSW, documentação oficial pgvector.']]])]

cover()
for title, blocks in (BASE_SECTIONS + EXTRA_SECTIONS):
    add_section(title, blocks)
out = os.path.join(HERE, "pdi-" + D['slug'] + ".docx")
doc.save(out)
print("DOCX:", out)
