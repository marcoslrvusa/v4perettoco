"""
detector_flags.py — Roda QUINTA 7h e DOMINGO 20h (cron automático).

Coleta dados de todas as fontes, detecta flags por cliente,
prioriza por impacto, aciona o agente CSM correto para cada flag
e envia briefing consolidado ao CSM + Coordenador.

Depende de: v4-automations/scripts/connectors.py
"""
import sys
import os
from pathlib import Path
from datetime import date, timedelta
from dotenv import load_dotenv

# Importa connectors do v4-automations
V4_PATH = Path(__file__).parent.parent.parent / "v4-automations"
sys.path.insert(0, str(V4_PATH))

from scripts.connectors import (
    GoogleAdsConnector, MetaConnector,
    GmailConnector, claude, load_clientes
)
from scripts.ekyte.connector import EkyteClient

load_dotenv(V4_PATH / "config" / ".env")

# ── THRESHOLDS PADRÃO ────────────────────────────────────────────────────────
# Personalize em config/clientes.json por cliente (campo "csm_thresholds")

DEFAULTS = {
    "roi": {"roas_meta": 2.5, "semanas": 2},
    "churn": {"nps_min": 50, "csat_min": 3.5},
    "okr": {"progresso_min_pct": 60},
    "operacao": {"dias_atraso": 3, "semanas_timesheet": 1},
}

SYSTEM_CSM = """
Você é o Agente CSM da V4 Company — orquestrador de Customer Success.

Recebe dados de flags detectadas automaticamente e gera o briefing
consolidado para o CSM humano tomar decisões.

Para cada flag:
- Classifique a urgência (Crítica / Alta / Média)
- Identifique o tipo de problema
- Recomende a ação imediata
- Indique qual área acionar

Seja direto. O CSM precisa de decisão, não de análise longa.
"""


def detectar_flags_cliente(cliente: dict) -> list:
    """
    Detecta todas as flags ativas de um cliente.
    Retorna lista de flags com tipo, dados e urgência.
    """
    flags = []
    thresholds = {**DEFAULTS, **cliente.get("csm_thresholds", {})}
    hoje = date.today()

    # ── FLAG ROI ──────────────────────────────────────────────────────────────
    try:
        gads = GoogleAdsConnector()
        meta = MetaConnector()

        g = gads.get_performance(cliente["google_ads_customer_id"], days=14)
        m = meta.get_performance(cliente["meta_ad_account_id"], days=14)

        roas_google = g.get("roas", 0)
        roas_meta = m.get("roas", 0)
        roas_medio = max(roas_google, roas_meta)
        meta_roas = thresholds["roi"]["roas_meta"]

        if roas_medio > 0 and roas_medio < meta_roas:
            desvio_pct = ((roas_medio - meta_roas) / meta_roas) * 100
            flags.append({
                "tipo": "roi",
                "urgencia": "Crítica" if roas_medio < 1 else "Alta",
                "dado": f"ROAS {roas_medio:.1f} vs meta {meta_roas}",
                "desvio_pct": round(desvio_pct, 1),
                "dados_brutos": {"google": g, "meta": m},
            })
    except Exception as e:
        print(f"  ROI check erro: {e}")

    # ── FLAG CHURN (verifica via dados disponíveis) ───────────────────────────
    # NPS/CSAT vem de dados históricos — verificar no vault ou Ekyte
    # Por ora, placeholder para integração com pesquisa NPS
    nps = cliente.get("ultimo_nps")
    csat = cliente.get("ultimo_csat")
    if nps and csat:
        if nps < thresholds["churn"]["nps_min"] and csat < thresholds["churn"]["csat_min"]:
            flags.append({
                "tipo": "churn",
                "urgencia": "Crítica",
                "dado": f"NPS {nps} + CSAT {csat}",
                "dados_brutos": {"nps": nps, "csat": csat},
            })

    # ── FLAG OKR ──────────────────────────────────────────────────────────────
    okrs = cliente.get("okrs", {})
    krs = okrs.get("krs", [])
    for kr in krs:
        meta_kr = kr.get("meta", 0)
        atual_kr = kr.get("atual", 0)
        if meta_kr > 0 and atual_kr > 0:
            progresso = (atual_kr / meta_kr) * 100
            # Estima progresso esperado baseado na semana do quarter
            semana_quarter = ((hoje.month - 1) % 3) * 4 + min(hoje.day // 7, 4)
            esperado_pct = (semana_quarter / 12) * 100
            if esperado_pct > 0 and (progresso / esperado_pct * 100) < thresholds["okr"]["progresso_min_pct"]:
                flags.append({
                    "tipo": "okr",
                    "urgencia": "Alta",
                    "dado": f"KR '{kr['descricao']}': {progresso:.0f}% vs {esperado_pct:.0f}% esperado",
                    "dados_brutos": kr,
                })

    # ── FLAG OPERAÇÃO ─────────────────────────────────────────────────────────
    try:
        ekyte = EkyteClient()
        workspace_id = cliente.get("ekyte_workspace_id")
        squad_id = cliente.get("ekyte_squad_id")

        atrasadas = ekyte.get_tarefas_atrasadas(workspace_id=workspace_id, squad_id=squad_id)
        fcas_abertas = ekyte.get_fcas_abertas(workspace_id=workspace_id, squad_id=squad_id)
        ts = ekyte.get_timesheet_semana(squad_id=squad_id)

        if len(atrasadas) > 0 and len(fcas_abertas) == 0:
            flags.append({
                "tipo": "operacao",
                "urgencia": "Média",
                "dado": f"{len(atrasadas)} tarefa(s) atrasada(s) sem FCA aberta",
                "dados_brutos": {"atrasadas": len(atrasadas), "fcas": len(fcas_abertas)},
            })

        if not ts.get("atualizado"):
            flags.append({
                "tipo": "operacao",
                "urgencia": "Média",
                "dado": "Timesheet GT zerado esta semana",
                "dados_brutos": ts,
            })
    except Exception as e:
        print(f"  Operação check erro: {e}")

    return flags


def gerar_briefing_csm(cliente: dict, flags: list) -> str:
    """Usa Claude para gerar o briefing de decisão para o CSM."""
    if not flags:
        return f"## {cliente['nome']} — 🟢 Saudável\nNenhuma flag detectada. Monitorando."

    user_prompt = f"""
Gere o briefing de decisão para o CSM sobre o cliente {cliente['nome']}.

Flags detectadas ({len(flags)}):
{flags}

OKR do cliente: {cliente.get('okrs', {}).get('objetivo', 'não definido')}
LT do cliente: {cliente.get('lt_meses', '?')} meses
Contrato vence em: {cliente.get('contrato_vence_dias', '?')} dias

Gere no formato:

## {cliente['nome']} — [CRÍTICO/ATENÇÃO/MONITORAR]

**Flags ativas:** [lista resumida]

**Prioridade 1:** [a flag mais urgente]
→ Tipo: [roi/churn/okr/operacao]
→ Dado: [o número]
→ Ação recomendada: [o que o CSM deve fazer agora]
→ Área a acionar: [quem]

[se houver mais flags, lista as demais]

**Decisão do CSM:** [campo para o CSM preencher após leitura]
"""
    return claude(SYSTEM_CSM, user_prompt, max_tokens=600)


def montar_email_csm(briefings: list[tuple]) -> str:
    """Monta HTML do email de briefing para o CSM."""
    semana = date.today().isocalendar()[1]
    conteudo = ""

    for nome, briefing, num_flags in briefings:
        cor = "#dc3545" if num_flags >= 2 else "#ffc107" if num_flags == 1 else "#28a745"
        conteudo += f"""
<div style="border-left: 4px solid {cor}; padding: 16px; margin: 12px 0;
            background: #fafafa; border-radius: 0 8px 8px 0;">
<pre style="white-space: pre-wrap; font-family: Arial, sans-serif;
            font-size: 13px; margin: 0; line-height: 1.6;">{briefing}</pre>
</div>
"""

    total_flags = sum(n for _, _, n in briefings)
    clientes_criticos = sum(1 for _, _, n in briefings if n >= 2)

    return f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto; color: #333; padding: 20px;">
<h2 style="border-bottom: 2px solid #e0e0e0; padding-bottom: 8px;">
  Briefing CSM — Semana {semana} — {date.today().strftime('%d/%m/%Y')}
</h2>
<div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin: 12px 0;
            display: flex; gap: 24px; font-size: 13px;">
  <span>Flags totais: <strong>{total_flags}</strong></span>
  <span>Clientes críticos: <strong>{clientes_criticos}</strong></span>
  <span>Clientes monitorados: <strong>{len(briefings)}</strong></span>
</div>
{conteudo}
<hr style="margin: 24px 0; border: none; border-top: 1px solid #e0e0e0;">
<p style="color: #999; font-size: 12px;">
  V4 CSM Hub — Detector de flags automático.
  Quinta 7h + Domingo 20h.
</p>
</body>
</html>
"""


def main():
    print(f"[Detector de Flags CSM] Iniciando — {date.today()}")

    clientes = load_clientes()
    briefings = []

    for cliente in clientes:
        print(f"  Verificando: {cliente['nome']}...")
        flags = detectar_flags_cliente(cliente)
        briefing = gerar_briefing_csm(cliente, flags)
        briefings.append((cliente["nome"], briefing, len(flags)))
        print(f"  Flags detectadas: {len(flags)}")

    html = montar_email_csm(briefings)

    gmail = GmailConnector()
    gmail.send(
        to=[os.getenv("EMAIL_COORDENADOR"), os.getenv("EMAIL_CSM", os.getenv("EMAIL_AM"))],
        subject=f"Briefing CSM — Semana {date.today().isocalendar()[1]} — {sum(n for _,_,n in briefings)} flags",
        body_html=html,
    )

    print(f"[Detector de Flags CSM] Concluído.")


if __name__ == "__main__":
    main()
