# -*- coding: utf-8 -*-
import os, io, importlib.util
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = "/home/marcos/orca/workspaces/v4perettoco-main/SEO-Premium/squads/prime/clientes/premium-cleaning-services"
spec = importlib.util.spec_from_file_location("gen", os.path.join(BASE, "docs/gerar-artigos-docx.py"))
gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)

OUT = os.path.join(BASE, "artigos/Premium-Cleaning-Programa-Editorial-Noviembre-2026.docx")
INK='141414'; GOLD='C9A96E'; GOLD_L='F7F3EA'; GRAY='6B6B6B'; LINE='E4E4E4'

BLOCKS = [
 ("A","Hotel & Hospitality","165.000 buscas/mês","/hotel-housekeeping-services",[
  ("A1","Hotel Housekeeping Productivity Standards: Rooms per Attendant Hour by Property Tier","hotel housekeeping productivity standards","165k","/hotel-housekeeping-services","PRONTO",
   ["Quantos créditos por hora cada faixa de hotel entrega","Como transformar status de quarto em crédito","Como construir o padrão da própria propriedade"],
   ["O que um padrão mede de fato","Créditos por hora por tier","Tabela de créditos por status","Fórmula com exemplo resolvido","Seis variáveis que quebram o benchmark","Inspeção e retrabalho","KPIs semanais","Plano de 30 dias"],
   "É a espinha dorsal do bloco: define a unidade que todos os outros artigos de hotel usam."),
  ("A2","Marriott, Hilton and Hyatt Brand Standards: What a Third-Party Cleaning Vendor Must Prove","hotel brand cleaning standards","—","/hotel-housekeeping-services","EM PRODUÇÃO",
   ["O que cada bandeira exige de apresentação e frequência","Quais documentos a auditoria de marca pede","Como um fornecedor prova conformidade"],
   ["Padrão de marca como piso, não teto","Diferenças por tier dentro da mesma bandeira","Documentação obrigatória","Erros que reprovam auditoria","O que exigir no contrato","Checklist de evidências"],
   "Converte o discurso de qualidade em conformidade verificável — argumento direto para redes e bandeiras."),
  ("A3","Cost per Occupied Room (CPOR): How to Audit Your Housekeeping Vendor Invoice","hotel housekeeping cost per room","—","/hotel-housekeeping-cost-pricing-guide-2026","EM PRODUÇÃO",
   ["Como calcular custo real por quarto ocupado","Onde a fatura esconde horas não produtivas","Como comparar propostas com bases diferentes"],
   ["Definição de CPOR","Horas produtivas vs pagas","Componentes da fatura","Erros de rateio","Modelo de auditoria mensal","Quando renegociar"],
   "Transforma a conversa de preço em auditoria — o cliente passa a comparar metodologia, não apenas tarifa."),
  ("A4","In-House Laundry vs Outsourced Hotel Laundry: Cost, Linen Life and Turnaround","hotel laundry outsourcing","—","/hotel-housekeeping-services","EM PRODUÇÃO",
   ["Custo real de lavanderia interna","Impacto na vida útil do enxoval","Prazos e risco operacional"],
   ["Custos invisíveis da lavanderia interna","Terceirização: o que entra no contrato","Vida útil e reposição","Giro e prazo","Riscos de continuidade","Modelo de decisão"],
   "Abre a porta de um serviço adjacente de alto ticket, sem sair do cluster hotel."),
  ("A5","Public Area Cleaning Standards for Hotels: Lobby, Elevators, Restrooms and F&B Outlets","hotel public area cleaning","—","/hospitality-cleaning-services-nj","EM PRODUÇÃO",
   ["Frequência por tipo de área pública","Como medir qualidade em área de fluxo","Padrão para lobby, elevador, banheiro e A&B"],
   ["Por que área pública define a percepção","Frequências por zona","Banheiros: o teste de 15 minutos","Elevadores e pisos","A&B e áreas de apoio","Painel de inspeção"],
   "Cobre a lacuna entre limpeza de quarto e limpeza comercial, hoje um vazio na malha do site."),
  ("A6","Hotel Deep Clean Calendar: Quarterly, Seasonal and Annual Tasks with Checklist","hotel deep cleaning schedule","—","/hotel-cleaning-services-new-jersey","EM PRODUÇÃO",
   ["O que entra em cada ciclo de limpeza profunda","Como precificar sem parar o andar","Calendário anual pronto"],
   ["O que é limpeza profunda","Ciclo trimestral","Ciclo sazonal","Ciclo anual","Janelas de execução","Checklist e registro"],
   "Vende projeto recorrente de alta margem e sustenta a página de limpeza em NJ."),
  ("A7","Housekeeping Staffing 7 Days a Week Without Overtime: Shift Models That Work","hotel housekeeping staffing","—","/hotel-turnover-cleaning-checklist","EM PRODUÇÃO",
   ["Modelos de escala para cobertura 7 dias","Como evitar hora extra estrutural","Dimensionamento por pico de chegada"],
   ["O problema do pico de chegada","Três modelos de escala","Dimensionamento por dia da semana","Rotação e ausência","Custo de cobertura","Indicadores de fadiga"],
   "Ataca a dor número um de quem opera andares e prepara o terreno para o serviço terceirizado."),
  ("A8","The 40-Point Hotel Room Inspection Checklist (and How to Score It)","hotel room inspection checklist","—","/hotel-cleaning-services-new-jersey","EM PRODUÇÃO",
   ["Quais 40 pontos realmente importam","Como pontuar e classificar","Como usar o score para treinar"],
   ["Por que checklist padronizado","Banheiro (12 pontos)","Cama e enxoval (8)","Superfícies e piso (9)","Amenidades e tecnologia (6)","Apresentação e odores (5)","Sistema de pontuação"],
   "É o material que o cliente baixa e compartilha internamente — maior potencial de link e citação em IA."),
 ]),
 ("B","Office & Janitorial","22.200 buscas/mês","/office-cleaning-new-jersey",[
  ("B1","Commercial Cleaning RFP: 12 Clauses Every NJ/NY Facility Manager Should Require","commercial cleaning RFP","—","/janitorial-contracts-daily-office-cleaning","EM PRODUÇÃO",
   ["Quais cláusulas protegem o contratante","Como comparar propostas de forma justa","O que nunca pode ficar fora do RFP"],
   ["Escopo mensurável","SLA e penalidades","Seguro e bonding","Pessoal e treinamento","Produtos e equipamentos","Reajuste e rescisão"],"Documento de referência que gera download e contato de facility manager."),
  ("B2","Cleaning SLA and KPIs: How to Measure a Janitorial Vendor Beyond “Looks Clean”","cleaning contract SLA KPIs","880","/janitorial-services-nj","EM PRODUÇÃO",
   ["Quais KPIs realmente medem limpeza","Como definir metas contratuais","Como reportar semanalmente"],
   ["Por que 'parece limpo' não é KPI","Cinco KPIs essenciais","Metodologia de inspeção","Painel semanal","Consequências contratuais","Exemplo de SLA"],"Liga diretamente ao nosso serviço de supervisão e relatório."),
  ("B3","Office Cleaning Frequency by Foot Traffic: Daily, 3x Week or Weekly?","how often should an office be cleaned","—","/office-cleaning-new-jersey","EM PRODUÇÃO",
   ["Como calcular frequência por uso real","Custo de cada frequência","Sinais de que a frequência está errada"],
   ["Metragem, não cabeças","Cálculo por foot traffic","Custo por frequência","Sintomas de subfrequência","Sintomas de sobrefrequência","Modelo de decisão"],"Ajuda o cliente a comprar a frequência certa — reduz churn por insatisfação."),
  ("B4","How to Switch Commercial Cleaning Vendors in 30 Days Without Service Gaps","how to change cleaning company","—","/office-cleaning-small-business","EM PRODUÇÃO",
   ["Cronograma de transição sem interrupção","O que transferir e o que recomeçar","Como proteger a operação no dia 1"],
   ["Por que transições falham","Cronograma de 30 dias","Transferência de equipe","Inventário e equipamentos","Comunicação interna","Checklist do dia 1"],"Converte quem já está insatisfeito — intenção de compra altíssima."),
  ("B5","Insurance, Bonding and Background Checks: What to Verify Before Hiring a Cleaner","cleaning company insurance bonding","—","/office-cleaning-new-jersey","EM PRODUÇÃO",
   ["Quais coberturas exigir e em que limites","Diferença entre bonding e seguro","Como verificar de verdade"],
   ["Riscos cobertos e não cobertos","Bonding explicado","Background check: o que checar","Certificados e validade","Perguntas ao fornecedor","Red flags"],"Constrói autoridade e reduz objeção de preço na comparação com concorrente barato."),
  ("B6","OSHA Compliance for Commercial Cleaning: Chemicals, PPE and Training","commercial cleaning OSHA requirements","—","/janitorial-services-nj","EM PRODUÇÃO",
   ["Obrigações de segurança do fornecedor","Como ler SDS e treinar equipe","O que auditar em inspeção"],
   ["Riscos químicos","SDS e rotulagem","EPI por tarefa","Treinamento e registro","Ergonomia e turnos","O que pedir ao fornecedor"],"Blindagem jurídica: tema que o cliente pesquisa quando já teve problema."),
  ("B7","ATP Testing in Restrooms: How to Prove a Restroom Is Actually Clean","ATP testing restroom cleaning","—","/office-cleaning-new-jersey","EM PRODUÇÃO",
   ["O que é ATP e o que ele mede","Como usar sem virar teatro","Limiares e protocolo"],
   ["O que ATP mede","Limiares de referência","Pontos de coleta","Protocolo de leitura","Como reportar","Limitações do teste"],"Diferencial técnico raro no mercado — ótimo para citação em IA."),
  ("B8","The Vendor Scorecard: 12 Metrics to Review in a Quarterly Business Review","cleaning vendor scorecard","—","/janitorial-contracts-daily-office-cleaning","EM PRODUÇÃO",
   ["O que levar para a QBR","Como pontuar o fornecedor","Como transformar score em decisão"],
   ["Por que QBR sem dado é reunião social","12 métricas","Pesos e pontuação","Preparação da reunião","Plano de ação","Renovação ou troca"],"Cria ritual de retenção: cliente que mede é cliente que fica."),
 ]),
 ("C","Carpet & Floor Care","18.100 buscas/mês","/commercial-carpet-cleaning",[
  ("C1","Commercial Carpet Cleaning Cost per Square Foot in NJ and NYC: 2026 Ranges","commercial carpet cleaning cost per square foot","18,1k","/commercial-carpet-cleaning","EM PRODUÇÃO",
   ["Faixas de preço por m² em NJ e NYC","O que muda o preço","Como comparar orçamentos"],
   ["Faixas 2026","Variáveis de preço","Métodos e custo","Mínimos e deslocamento","Contrato vs avulso","Como pedir orçamento"],"Maior volume do bloco e intenção comercial imediata."),
  ("C2","Encapsulation vs Hot Water Extraction: Which Method for Which Carpet","encapsulation vs extraction carpet","—","/commercial-carpet-cleaning","EM PRODUÇÃO",
   ["Diferença técnica entre métodos","Qual usar por tipo de fibra e sujeira","Impacto em tempo de secagem"],
   ["Como cada método funciona","Quando encapsular","Quando extrair","Fibras e sensibilidade","Tempo de secagem","Erros comuns"],"Responde à dúvida que precede a compra e qualifica o lead."),
  ("C3","Carpet Drying Time: How to Clean Overnight and Reopen in the Morning","carpet cleaning drying time","—","/commercial-carpet-cleaning","EM PRODUÇÃO",
   ["Quanto tempo cada método leva para secar","Como limpar à noite e abrir de manhã","Riscos de umidade residual"],
   ["Por que secagem importa","Tempos por método","Ventilação e ar-condicionado","Controle de umidade","Janela noturna","Checklist de liberação"],"Argumento operacional decisivo para escritórios e varejo."),
  ("C4","Carpet Cleaning and Warranty: What Manufacturers Require to Keep Coverage","carpet warranty cleaning requirements","—","/commercial-carpet-cleaning","EM PRODUÇÃO",
   ["O que a garantia exige de manutenção","Como documentar limpezas","O que anula a cobertura"],
   ["Como funciona a garantia","Requisitos de manutenção","Documentação aceita","Produtos proibidos","Intervalo mínimo","Checklist de conformidade"],"Tema de alto valor percebido e baixa concorrência."),
  ("C5","Interim vs Restorative Carpet Cleaning in High-Traffic Areas","interim carpet cleaning high traffic","—","/commercial-carpet-cleaning-high-traffic","EM PRODUÇÃO",
   ["Quando fazer limpeza intermediária","Como alternar com restauração","Custo por m² ao longo do ano"],
   ["Ciclo de sujeira em área de fluxo","Limpeza intermediária","Restauração","Calendário combinado","Custo anual","Indicadores de degradação"],"Vende contrato recorrente em vez de serviço avulso."),
  ("C6","Coefficient of Friction: Floor Safety Standards for Commercial Spaces","floor coefficient of friction standards","—","/tile-grout-deep-cleaning-commercial","EM PRODUÇÃO",
   ["O que é coeficiente de atrito","Limites aceitos e normas","Como a limpeza altera o COF"],
   ["COF explicado","Normas aplicáveis","Piso molhado vs seco","Produtos que reduzem atrito","Teste e medição","Documentação de segurança"],"Abre conversa com facilities e seguradoras — ângulo raro."),
  ("C7","Stone and Terrazzo Floor Care: Honing, Polishing and Sealing Schedules","terrazzo floor care maintenance","—","/tile-grout-cleaning","EM PRODUÇÃO",
   ["Diferença entre lustrar, polir e selar","Frequência por tipo de pedra","Erros que danificam o piso"],
   ["Tipos de pedra","Abrasivos e etapas","Cronograma por fluxo","Selagem e proteção","Manchas e correções","Custo de reposição"],"Protege ativo caro e justifica contrato especializado."),
  ("C8","Grout Sealing vs Grout Restoration: When Cleaning Is No Longer Enough","grout sealing vs restoration","190","/floor-grout-restoration-pricing-guide","EM PRODUÇÃO",
   ["Quando selar e quando restaurar","Faixas de preço","Como avaliar resultado"],
   ["O que degrada o rejunte","Selagem: indicação","Restauração: indicação","Processo passo a passo","Preço e expectativa","Antes e depois"],"Fecha o bloco com serviço de ticket alto e prova visual."),
 ]),
 ("D","Restaurant & Kitchen","1.000+ buscas/mês","/restaurant-commercial-cleaning",[
  ("D1","NFPA 96 Explained: Hood Cleaning Frequencies and Documentation","NFPA 96 hood cleaning requirements","1k","/restaurant-hood-exhaust-cleaning-nj","EM PRODUÇÃO",
   ["Frequência exigida por tipo de cozinha","Documentação obrigatória","O que a inspeção verifica"],
   ["O que a NFPA 96 cobre","Frequências por volume de cozimento","Certificado e registro","Sinalização e acesso","Erros que reprovam","Checklist do restaurante"],"Requisito legal: maior intenção de compra do bloco."),
  ("D2","New Jersey Grease Trap Rules: Sizing, Pumping and Recordkeeping","grease trap cleaning regulations NJ","—","/restaurant-grease-trap-cleaning-nj","EM PRODUÇÃO",
   ["Dimensionamento exigido","Frequência de bombeamento","Registros que a fiscalização pede"],
   ["Por que a caixa de gordura importa","Dimensionamento","Frequência prática","Manifesto e registros","Sinais de saturação","Multas e riscos"],"Combina conformidade e urgência — telefone toca."),
  ("D3","The 20 Most Common Health Inspection Violations in Commercial Kitchens","health inspection violations restaurant","390","/restaurant-cleaning-checklist-health-inspection","EM PRODUÇÃO",
   ["As 20 violações mais frequentes","Como cada uma é prevenida","Como passar na reinspeção"],
   ["As 20 violações","Categorias de risco","Prevenção por área","Registro diário","Reinspeção","Plano de correção"],"Conteúdo que o gerente salva e imprime — alto potencial de citação."),
  ("D4","Kitchen Deep Cleaning: A Nightly, Weekly and Monthly Protocol","commercial kitchen deep cleaning","—","/commercial-kitchen-cleaning-nj","EM PRODUÇÃO",
   ["O que é feito por turno, semana e mês","Tempo e equipamento necessários","Como documentar"],
   ["Diferença entre limpeza e higienização","Protocolo noturno","Protocolo semanal","Protocolo mensal","Equipamentos e químicos","Registro e auditoria"],"Vende recorrência e organiza a operação do cliente."),
  ("D5","Bar and Nightclub Cleaning: Glassware, Drains, Sticky Floors and Odor","bar cleaning service NJ","—","/overnight-restaurant-cleaning","EM PRODUÇÃO",
   ["Os pontos críticos de bar","Como eliminar odor de verdade","Rotina noturna"],
   ["Por que bar é diferente","Bancada e superfícies","Ralos e odor","Pisos pegajosos","Banheiros","Rotina de fechamento"],"Segmento com alta rotatividade de fornecedor e pouca oferta especializada."),
  ("D6","Quarry Tile Floor Care in Commercial Kitchens: Degreasing Without Damage","quarry tile kitchen floor cleaning","—","/restaurant-commercial-cleaning","EM PRODUÇÃO",
   ["Como desengordurar sem atacar o rejunte","Frequência e método","Segurança e escorregamento"],
   ["Quarry tile e gordura","Produtos adequados","Método por camada","Rejunte e vedação","Segurança de piso","Cronograma"],"Resolve dor crônica de cozinha industrial com método técnico."),
  ("D7","Post-Event Restaurant Turnaround: Cleaning Between Services and Private Events","restaurant event cleaning turnaround","—","/restaurant-commercial-cleaning","EM PRODUÇÃO",
   ["Como virar o salão entre serviços","Tempo mínimo realista","Equipe e equipamento"],
   ["O que é turnaround","Janela entre serviços","Checklist por zona","Equipe mínima","Sincronização com cozinha","Riscos de atraso"],"Serviço de urgência com margem alta e decisão rápida."),
  ("D8","Grease Fire Risk and Insurance: What Cleaners Must Document","grease fire prevention restaurant","—","/restaurant-hood-exhaust-cleaning-nj","EM PRODUÇÃO",
   ["Como a gordura vira incêndio","O que a seguradora exige","Documentos que protegem o restaurante"],
   ["Cadeia do incêndio de gordura","Pontos de acúmulo","Exigências de seguradora","Documentação do serviço","Treinamento da equipe","Plano de resposta"],"Fecha o bloco unindo risco financeiro e obrigação contratual."),
 ]),
 ("E","Custo & Procurement","18.100 buscas/mês","/commercial-cleaning-services-nj",[
  ("E1","The True Cost of a Dirty Office: Absenteeism, Turnover and Client Perception","cost of a dirty office","—","/insights/hidden-costs-inconsistent-commercial-cleaning-nj-ny","EM PRODUÇÃO",
   ["Como quantificar o custo da sujeira","Impacto em absenteísmo e rotatividade","Efeito na percepção do cliente"],
   ["Custo visível vs invisível","Absenteísmo","Rotatividade","Percepção de clientes","Modelo de cálculo","Quando o barato sai caro"],"Cria urgência econômica em quem só olha preço."),
  ("E2","Commercial Cleaning Benchmarks: NJ vs NYC Rates in 2026","commercial cleaning rates NJ NYC","18,1k","/commercial-cleaning-services-nj","EM PRODUÇÃO",
   ["Faixas de preço por região e serviço","Por que NY custa mais","Como usar benchmark na negociação"],
   ["Metodologia do benchmark","Faixas NJ","Faixas NYC","Diferenças de custo","Erros de comparação","Como negociar com dado"],"Conteúdo de referência com forte potencial de backlink."),
  ("E3","How to Build an Annual Commercial Cleaning Budget","commercial cleaning budget","—","/insights/commercial-cleaning-cost-nj-pricing-guide-2026","EM PRODUÇÃO",
   ["Como montar o orçamento anual","O que costuma ser esquecido","Como prever reajuste"],
   ["Estrutura do orçamento","Custo por área e frequência","Serviços extras","Reserva para emergência","Reajuste anual","Modelo em planilha"],"Fala com o decisor financeiro, não só com o operacional."),
  ("E4","15-Point Vendor Vetting Checklist for Facility Managers","commercial cleaning vendor vetting","—","/best-commercial-cleaning-companies-nj-2026","EM PRODUÇÃO",
   ["Os 15 pontos de verificação","Como checar cada um","Sinais de fornecedor frágil"],
   ["Por que due diligence falha","15 pontos","Verificação documental","Referências reais","Visita técnica","Red flags"],"Alimenta a página de 'melhores empresas' com critério verificável."),
  ("E5","Cleaning Contract Terms That Cost You Money: Auto-Renewal, Escalators and Change Orders","commercial cleaning contract terms","880","/janitorial-contracts-daily-office-cleaning","EM PRODUÇÃO",
   ["As cláusulas que encarecem o contrato","Como negociar cada uma","O que exigir na renovação"],
   ["Renovação automática","Reajuste e escalonamento","Change orders","Penalidades","Rescisão","Checklist de negociação"],"Alto valor prático: o cliente usa na mesa de negociação."),
  ("E6","Change Orders and Add-On Fees: The Hidden Line Items in Cleaning Invoices","cleaning invoice add-on fees","—","/insights/hidden-costs-inconsistent-commercial-cleaning-nj-ny","EM PRODUÇÃO",
   ["Quais adicionais aparecem na fatura","O que é legítimo e o que é abuso","Como auditar a fatura"],
   ["Anatomia da fatura","Adicionais legítimos","Adicionais abusivos","Auditoria mensal","Como renegociar","Modelo de conferência"],"Gera conversa imediata com quem já é cliente de outro fornecedor."),
  ("E7","The ROI of Professional Cleaning: Productivity, Retention and Client Perception","ROI of professional office cleaning","—","/commercial-cleaning-services-nj","EM PRODUÇÃO",
   ["Como calcular retorno de limpeza","Variáveis de produtividade","Como apresentar para a diretoria"],
   ["Por que ROI de limpeza é difícil","Variáveis mensuráveis","Produtividade","Retenção de talento","Percepção de clientes","Modelo de apresentação"],"Dá ao cliente o argumento que ele leva para o board."),
  ("E8","Vendor Consolidation: When One Cleaning Partner Beats Five Specialists","cleaning vendor consolidation","—","/commercial-cleaning-services-nj","EM PRODUÇÃO",
   ["Quando consolidar fornecedores","Riscos da consolidação","Como migrar sem perder qualidade"],
   ["Custo da fragmentação","Ganhos de consolidação","Riscos","Modelo híbrido","Plano de migração","Como medir"],"Argumento de expansão de conta — vende o pacote completo."),
 ]),
]


def set_col_widths(table, widths_cm):
    table.autofit = False
    tblPr = table._tbl.tblPr
    layout = OxmlElement('w:tblLayout'); layout.set(qn('w:type'), 'fixed'); tblPr.append(layout)
    grid = table._tbl.find(qn('w:tblGrid'))
    if grid is not None:
        for gc, w in zip(grid.findall(qn('w:gridCol')), widths_cm):
            gc.set(qn('w:w'), str(int(w * 567)))
    for row in table.rows:
        for cell, w in zip(row.cells, widths_cm):
            cell.width = Cm(w)

def compact(table, pad=60):
    tblPr = table._tbl.tblPr
    mar = OxmlElement('w:tblCellMar')
    for side, val in (('top', pad), ('bottom', pad), ('left', 90), ('right', 90)):
        el = OxmlElement(f'w:{side}'); el.set(qn('w:w'), str(val)); el.set(qn('w:type'), 'dxa'); mar.append(el)
    tblPr.append(mar)

def repeat_header(table):
    tr = table.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    el = OxmlElement('w:tblHeader'); el.set(qn('w:val'), 'true'); trPr.append(el)
    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        cs = OxmlElement('w:cantSplit'); cs.set(qn('w:val'), 'true'); trPr.append(cs)

def set_cell_bg(cell, hexv):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:fill'),hexv)
    tcPr.append(shd)

def page_number(par):
    run = par.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'),'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'),'preserve'); it.text = 'PAGE'
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'),'end')
    run._r.append(f1); run._r.append(it); run._r.append(f2)
    run.font.size = Pt(8.5); run.font.color.rgb = RGBColor(0x8A,0x8A,0x8A)

def band(doc, title, subtitle, height=None):
    t = doc.add_table(rows=1, cols=1)
    c = t.rows[0].cells[0]
    set_cell_bg(c, INK)
    c.text = ''
    p = c.paragraphs[0]; p.paragraph_format.space_before = Pt(22); p.paragraph_format.space_after = Pt(4)
    r = p.add_run(title); r.bold = True; r.font.size = Pt(26); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
    if subtitle:
        p2 = c.add_paragraph(); p2.paragraph_format.space_after = Pt(22)
        r2 = p2.add_run(subtitle); r2.font.size = Pt(12); r2.font.color.rgb = RGBColor(0xC9,0xA9,0x6E)
    doc.add_paragraph()

def label(doc, text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text.upper()); r.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(0x8A,0x6D,0x3B)

def article_page(doc, aid, title, query, vol, dest, status, responde, estrutura, why, current_arts=None):
    current_arts = current_arts or []
    label(doc, f"Artigo {aid}  ·  {status}")
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(10)
    r = p.add_run(title); r.bold = True; r.font.size = Pt(17)
    t = doc.add_table(rows=0, cols=2)
    for k, v in (("Query-alvo", query), ("Volume", (vol + "/mês") if vol!="—" else "cauda longa"), ("Página que alimenta", dest), ("Extensão prevista", "~5.000 palavras")):
        c = t.add_row().cells
        c[0].text = k; c[1].text = v
        set_cell_bg(c[0], GOLD_L)
        c[0].paragraphs[0].runs[0].bold = True
        for cell in (c[0], c[1]):
            for run in cell.paragraphs[0].runs: run.font.size = Pt(9.5)
    set_col_widths(t, [4.2, 12.3]); compact(t, 50); gen.style_table(t)
    label(doc, "O que o artigo responde")
    for item in responde:
        par = doc.add_paragraph(style='List Bullet'); gen.add_runs(par, item)
        par.paragraph_format.space_after = Pt(3)
    label(doc, "Estrutura planejada")
    for n, item in enumerate(estrutura, 1):
        par = doc.add_paragraph()
        par.paragraph_format.left_indent = Cm(0.7)
        par.paragraph_format.first_line_indent = Cm(-0.7)
        par.paragraph_format.space_after = Pt(3)
        rr = par.add_run(f"{n}.  "); rr.bold = True; rr.font.color.rgb = RGBColor(0x8A,0x6D,0x3B)
        gen.add_runs(par, item)
    par = doc.add_paragraph(); par.paragraph_format.space_before = Pt(8)
    r = par.add_run("Por que está no programa: "); r.bold = True; r.font.size = Pt(10)
    r2 = par.add_run(why); r2.font.size = Pt(10); r2.font.color.rgb = RGBColor(0x43,0x43,0x43)

    label(doc, "Entregáveis")
    for item in ("Answer box de 40–60 palavras", "12 a 15 subtítulos em formato de pergunta",
                 "3 a 5 tabelas de dados", "FAQ com 8 a 10 perguntas e schema",
                 "5 a 8 links internos com âncora exata", "Bloco de prova e JSON-LD no apêndice"):
        par = doc.add_paragraph(style='List Bullet')
        run = par.add_run(item); run.font.size = Pt(10)
        par.paragraph_format.space_after = Pt(2)

    label(doc, "Links internos previstos")
    par = doc.add_paragraph()
    dests = [dest] + [x[4] for x in current_arts if x[4] != dest]
    seen = []
    for d in dests:
        if d not in seen: seen.append(d)
    run = par.add_run("  ·  ".join(seen[:4])); run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x43,0x43,0x43)
    doc.add_page_break()

doc = gen.base_doc()
gen.set_heading_colors(doc)
sec = doc.sections[0]
sec.different_first_page_header_footer = True
# header / footer
hp = sec.header.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hr = hp.add_run("Premium Cleaning Services  ·  Programa Editorial Novembro 2026")
hr.font.size = Pt(8); hr.font.color.rgb = RGBColor(0x9A,0x9A,0x9A)
fp = sec.footer.paragraphs[0]
fp.paragraph_format.tab_stops.add_tab_stop(Cm(16))
fr = fp.add_run("Confidencial · V4"); fr.font.size = Pt(8.5); fr.font.color.rgb = RGBColor(0x8A,0x8A,0x8A)
fp.add_run("\t")
page_number(fp)

# ---------- CAPA
for _ in range(5): doc.add_paragraph()
band(doc, "Programa Editorial", "40 artigos · Novembro 2026")
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(18)
r = p.add_run("Dossiê de aprovação"); r.bold = True; r.font.size = Pt(20)
p = doc.add_paragraph()
r = p.add_run("Premium Cleaning Services · Nova Jersey & Nova York"); r.font.size = Pt(12); r.font.color.rgb = RGBColor(0x55,0x55,0x55)
for _ in range(10): doc.add_paragraph()
p = doc.add_paragraph()
r = p.add_run("5 blocos  ·  8 artigos por bloco  ·  ~5.000 palavras por artigo  ·  ~200.000 palavras");
r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x6B,0x6B,0x6B)
p = doc.add_paragraph()
r = p.add_run("Premium Cleaning Services Editorial Team  ·  28 de outubro de 2026")
r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(0x9A,0x9A,0x9A)
doc.add_page_break()

# ---------- COMO LER
p = doc.add_paragraph(); r = p.add_run("Como ler este documento"); r.bold = True; r.font.size = Pt(18)
doc.add_paragraph()
doc.add_paragraph("Este dossiê reúne o programa completo de conteúdo de novembro: os 40 artigos, o bloco a que pertencem, a busca que cada um ataca e a página do site que cada um fortalece. A aprovação aqui é de tema, ângulo e destino — não da redação final, que passa por revisão antes de publicar.")
doc.add_paragraph("Cada artigo tem uma página própria com três informações que bastam para decidir: o que ele responde, como está estruturado e por que está no programa. O artigo A1 aparece na íntegra como amostra do padrão de escrita que será aplicado aos 39 restantes.")
doc.add_paragraph("A lógica do programa é uma só: nenhum artigo compete com uma página que já vende. Cada peça existe para criar a malha de links internos que hoje é o gargalo do site — o benchmark mostrou que os concorrentes que rankeiam têm entre 10 e 20 links internos por artigo de topo, e nós temos em média 1.")
label(doc, "Status")
doc.add_paragraph("PRONTO — artigo escrito e revisado, incluído na íntegra neste documento.")
doc.add_paragraph("EM PRODUÇÃO — tema, ângulo, estrutura e destino aprovados; redação entra no arquivo conforme os lotes avançam (4 artigos por lote).")
label(doc, "Como aprovar")
doc.add_paragraph("Basta marcar os blocos aprovados na página final ou responder apontando os artigos que quer ajustar. Aprovar o Bloco A libera o Lote 1 imediatamente; os demais blocos podem ser aprovados em paralelo.")
doc.add_page_break()

# ---------- INDICE
p = doc.add_paragraph(); r = p.add_run("Índice"); r.bold = True; r.font.size = Pt(18)
doc.add_paragraph()
t = doc.add_table(rows=1, cols=4)
h = t.rows[0].cells
for i, htxt in enumerate(("ID","Artigo","Busca-alvo","Status")):
    h[i].text = htxt; set_cell_bg(h[i], INK)
    for run in h[i].paragraphs[0].runs: run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF); run.bold = True; run.font.size = Pt(9)
for tag, name, vol, dest, arts in BLOCKS:
    for aid, title, query, v, d, status, resp, est, why in arts:
        c = t.add_row().cells
        c[0].text = aid; c[1].text = title; c[2].text = query; c[3].text = status
        for cell in c:
            for run in cell.paragraphs[0].runs: run.font.size = Pt(8.5)
        c[0].paragraphs[0].runs[0].bold = True
        if status == "PRONTO":
            set_cell_bg(c[3], 'E8F5E9')
        else:
            set_cell_bg(c[3], GOLD_L)
set_col_widths(t, [1.2, 8.8, 3.6, 3.0]); compact(t, 40); repeat_header(t); gen.style_table(t)
doc.add_page_break()

# ---------- BLOCOS
for bi, (tag, name, vol, dest, arts) in enumerate(BLOCKS):
    band(doc, f"Bloco {tag} — {name}", vol)
    p = doc.add_paragraph()
    r = p.add_run("8 artigos · destino principal " + dest); r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x6B,0x6B,0x6B)
    doc.add_page_break()
    for aid, title, query, v, d, status, resp, est, why in arts:
        if aid == "A1":
            raw = io.open(os.path.join(BASE, "artigos/lote-1/A1-hotel-housekeeping-productivity-standards.md"), encoding='utf-8').read()
            meta, body = gen.parse_front(raw)
            label(doc, "Artigo A1  ·  PRONTO  ·  ÍNTEGRA")
            p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(6)
            r = p.add_run(title); r.bold = True; r.font.size = Pt(17)
            p = doc.add_paragraph()
            r = p.add_run(f"{query} · ~5.000 palavras · alimenta {d}"); r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(0x6B,0x6B,0x6B)
            gen.render_body(doc, body)
            doc.add_page_break()
        else:
            article_page(doc, aid, title, query, v, d, status, resp, est, why, arts)

# ---------- APROVACAO
p = doc.add_paragraph(); r = p.add_run("Aprovação"); r.bold = True; r.font.size = Pt(18)
doc.add_paragraph()
doc.add_paragraph("Marque abaixo os blocos aprovados. Aprovar um bloco libera o lote de 4 artigos correspondente; os blocos não aprovados voltam para ajuste de tema antes da produção.")
t = doc.add_table(rows=1, cols=4)
h = t.rows[0].cells
for i, htxt in enumerate(("Bloco","Tema","Artigos","Aprovado")):
    h[i].text = htxt; set_cell_bg(h[i], INK)
    for run in h[i].paragraphs[0].runs: run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF); run.bold = True; run.font.size = Pt(9)
for tag, name, vol, dest, arts in BLOCKS:
    c = t.add_row().cells
    c[0].text = tag; c[1].text = name; c[2].text = "8"; c[3].text = "(  ) sim   (  ) ajustar"
    for cell in c:
        for run in cell.paragraphs[0].runs: run.font.size = Pt(9.5)
set_col_widths(t, [1.6, 7.2, 2.0, 5.7]); compact(t, 70); repeat_header(t); gen.style_table(t)
doc.add_paragraph()
for rotulo in ("Aprovado por", "Data", "Observações"):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(20)
    r = p.add_run(rotulo + ": "); r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x8A,0x8A,0x8A)
    r2 = p.add_run("_" * 46); r2.font.size = Pt(10); r2.font.color.rgb = RGBColor(0xB0,0xB0,0xB0)
doc.add_paragraph()
p = doc.add_paragraph()
r = p.add_run("Documento confidencial V4 · Premium Cleaning Services · 28/10/2026 · 40 artigos · 10 lotes de 4 · entrega estimada em 8 a 10 semanas.")
r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(0x9A,0x9A,0x9A)

doc.save(OUT)
gen.purge_blue(OUT)
print("OK", OUT, os.path.getsize(OUT), "bytes ·", gen.count_words(doc), "palavras")
