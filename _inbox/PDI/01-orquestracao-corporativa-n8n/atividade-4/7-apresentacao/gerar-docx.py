#!/usr/bin/env python3
"""Gera o DOCX desta atividade (observabilidade n8n-CRM) com secoes de autoria."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

HERE = os.path.dirname(os.path.abspath(__file__))
doc = Document()
st = doc.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
for s in doc.sections:
    s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5); s.left_margin = Cm(3); s.right_margin = Cm(3)

def cover():
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(110)
    r = p.add_run('PDI'); r.bold = True; r.font.size = Pt(14); r.font.color.rgb = RGBColor(0x8B,0x45,0x13)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('Observabilidade e Logs de Sincronizacao n8n-CRM'); r.bold = True; r.font.size = Pt(23)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(28)
    r = p.add_run('Documento Tecnico de PDI'); r.font.size = Pt(12); r.font.color.rgb = RGBColor(0x6B,0x7A,0x8A)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(16)
    for line in ["Autor: PDI Marcos Luciano - marcosluciano.rodrigues@v4company.com",
                 "Unidade: FV Marketing / V4 Company, Automacao e Infraestrutura",
                 "Data: Agosto 2026", "Area: Automacao e Infraestrutura",
                 "Status: Entregue (desenvolvido)"]:
        rr = p.add_run(line + '\n'); rr.font.size = Pt(11); rr.font.color.rgb = RGBColor(0x49,0x55,0x60)
    doc.add_page_break()

def h1(t):
    hh = doc.add_heading(t, level=1)
    for r in hh.runs: r.font.color.rgb = RGBColor(0x8B,0x45,0x13)
    return hh

def tbl(headers, rows):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = 'Light Grid Accent 1'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(headers): t.rows[0].cells[i].text = str(c)
    for r in rows:
        cells = t.add_row().cells
        for i, c in enumerate(r): cells[i].text = str(c)

cover()
h1('1. Contexto')
doc.add_paragraph('A FV usa 4 CRMs (Imobiliario, Saude, Varejo, Servicos). Cada time copia o dado a mao e ninguem confia no numero do outro. Quando o dado diverge, a culpa cai no analytics.')
h1('2. Diagnostico')
doc.add_paragraph('Sem sincronizacao, o mesmo lead aparece com 3 e-mails e 2 telefones diferentes. Campanhas disparam 2x, o cliente recebe spam e a marca queima. Custo operacional e reputacional.')
h1('3. Solucao')
doc.add_paragraph('Barramento n8n onde cada evento publica com trace_id. Os outros 3 CRMs assinam e aplicam last-write-wins por trace_id mais timestamp, com log auditavel.')
h1('4. Como funciona (pipeline)')
tbl(['Etapa', 'Responsavel', 'Detalhe'], [
    ['1. Webhook', 'CRM_A.lead.updated', 'Injeta trace_id (UUID) e ts'],
    ['2. Normalizacao', 'map_fields()', 'E-mail minusculo, telefone E.164, sem e-mail descarta'],
    ['3. Publish', 'event_bus.publish(trace_id)', 'Fan-out para 3 assinantes'],
    ['4. Subscribe', 'CRM_B/C/D.apply()', 'Last-write-wins, idempotente'],
    ['5. Log', 'trace_store.save()', 'Rastro completo para auditoria e rollback'],
])
doc.add_paragraph('Falha em 1 CRM: retry 3x com backoff, sem bloquear os demais (isolamento de falha).')
h1('5. Antes vs Depois')
tbl(['Cenario', 'Antes (manual)', 'Depois (barramento)'], [
    ['Conflito de dado', 'Surge e ninguem ve', 'Logado com trace_id'],
    ['Retrabalho', '~50h/sem', '~1h/sem'],
    ['Spam ao cliente', 'Frequente', 'Eliminado (dedupe)'],
    ['Auditoria', 'Inexistente', 'Rastro completo'],
])
h1('6. Entregas')
for x in ['Workflow 01-sync-4crm.json: orquestracao com trace_id e idempotencia.',
          'Script normalize.py: mapeamento de campos entre CRMs.',
          'Doc runbook.md: como investigar um trace_id e fazer rollback.',
          'Dashboard de divergencia (antes/depois) em tempo real.']:
    doc.add_paragraph(x, style='List Bullet')
h1('7. Metricas')
tbl(['Cenario', 'Antes', 'Depois'], [
    ['Deteccao de falha de sync', 'Dias', '< 1 min'],
    ['Visibilidade por CRM', '0%', '100%'],
    ['Retrabalho semanal', '~50h/sem', '~1h/sem'],
])
doc.add_paragraph('Meta: 99% dos leads com fonte unica ate o fim do trimestre, com zero disparo duplicado.')
h1('8. Decisoes e tradeoffs')
for x in [
    'Log estruturado JSON com trace_id mais painel SQL em vez de APM pago (ADR-011): simples e sem custo, com consulta manual como tradeoff. Contador no n8n foi rejeitado e Datadog ficou como evolucao futura.',
    'trace_id com cobertura de 100%: liga trigger, execucao e escrita no CRM. Exige injetar trace_id e timestamp em todo evento e normalizar campos, com descarte quando falta e-mail.',
    'Barramento com fan-out para 3 CRMs e last-write-wins por trace_id mais timestamp: conflito vira log auditavel com rollback via trace_store.',
    'Isolamento de falha com retry de 3x e backoff por CRM: falha em 1 CRM nao bloqueia os outros, com consistencia eventual temporaria.',
    'Alerta acima de 2% em 5 min com piloto em 1 integracao por 1 semana antes de expandir para 12: evita ruido com nivel e amostragem e protege PII com mascara de e-mail e CNPJ.',
]:
    doc.add_paragraph(x, style='List Bullet')
h1('9. Impacto no negocio')
doc.add_paragraph('Hoje 12 integracoes com 4 CRMs so mostram erro quando o cliente reclama, dias depois, com lead duplicado (3 e-mails e 2 telefones), disparo duplo e retrabalho de cerca de 50h por semana em conciliacao manual. Com contrato de log, painel por trace_id e alerta em menos de 1 min, a meta e MTTR abaixo de 15 min, visibilidade de 0% para 100% por CRM e retrabalho de 50h para cerca de 1h por semana, mirando 99% dos leads com fonte unica e zero disparo duplicado. Isso corta custo operacional direto e risco reputacional de spam.')
h1('10. Referencias de estudo')
for x in [
    'Curso: Observabilidade na Pratica, logs, metricas e traces, na Alura.',
    'Video: Distributed Tracing Explained, trace_id e correlacao, no YouTube, canal CNCF.',
    'Doc: n8n Docs, Logging and observability, na plataforma n8n Docs.',
    'Doc: PostgreSQL Docs, Views and JSON functions, na plataforma PostgreSQL Docs.',
]:
    doc.add_paragraph(x, style='List Bullet')
h1('11. Status final')
doc.add_paragraph('NAO publicado: desenvolvido e em homologacao. Aguarda revisao do time de dados antes de ir a producao.')
out = os.path.join(HERE, 'pdi-orquestracao-corporativa-n8n-a4.docx')
doc.save(out)
print('DOCX:', out)
