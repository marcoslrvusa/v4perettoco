#!/usr/bin/env python3
"""
gerar_relatorio_semanal.py — Relatório semanal OKR + Google Ads.
Skill: trafego-relatorio-semanal-okr | Builders Hub V4

Uso: python gerar_relatorio_semanal.py [--clientes c1,c2] [--days 7] [--out arquivo.html]
"""
import sys, json, argparse
from pathlib import Path
from datetime import datetime, timedelta

# Importa helper da skill google-ads-dados
GADS_SCRIPTS = Path(__file__).parents[3] / "google-ads-dados" / "scripts"
sys.path.insert(0, str(GADS_SCRIPTS))

try:
    import google_ads_query as gaq
except ImportError:
    print("ERRO: skill google-ads-dados não encontrada. Verifique o duplo-write.", file=sys.stderr)
    sys.exit(1)


# ── Descoberta de clientes ────────────────────────────────────────────────────

def find_clients_base():
    for p in [Path("clientes"), Path("../clientes")]:
        if p.exists():
            return p
    return None


def list_configured_clients(base):
    result = []
    for folder in sorted(base.iterdir()):
        if folder.name.startswith("_") or not folder.is_dir():
            continue
        env = gaq.load_env(folder / ".env")
        if env.get("GOOGLE_ADS_CUSTOMER_ID"):
            result.append(folder.name)
    return result


def load_okrs(client_folder):
    f = client_folder / "okrs.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return {}


def load_client_name(client_folder):
    claude_md = client_folder / "CLAUDE.md"
    if claude_md.exists():
        for line in claude_md.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return client_folder.name.replace("-", " ").title()


# ── Pull de dados ─────────────────────────────────────────────────────────────

def pull_data(client_name, base, days):
    folder = base / client_name
    env_path = folder / ".env"
    env = gaq.load_env(env_path)

    missing = [k for k in gaq.REQUIRED if not env.get(k)]
    if missing:
        return {"error": f"Credenciais faltando: {', '.join(missing)}"}

    try:
        client, cid = gaq.build_client(env)
        period = gaq.period_clause(days=days)

        acct = gaq.run_query(client, cid, gaq.PRESETS["account"].format(p=period))
        camps = gaq.run_query(client, cid, gaq.PRESETS["campaigns"].format(p=period))

        return {"account": acct[0] if acct else {}, "campaigns": camps}
    except Exception as e:
        return {"error": str(e)}


# ── Métricas ──────────────────────────────────────────────────────────────────

def safe_float(v, default=0.0):
    try: return float(v or 0)
    except: return default

def safe_int(v, default=0):
    try: return int(v or 0)
    except: return default

def pct(actual, target):
    if not target: return None
    return round(actual / target * 100, 1)

def status(val, target, higher_is_better=True, warn_margin=0.2):
    if not target: return "neutral"
    ratio = val / target
    if higher_is_better:
        if ratio >= (1 - warn_margin): return "ok"
        if ratio >= (1 - warn_margin * 2): return "warn"
        return "bad"
    else:
        if ratio <= (1 + warn_margin): return "ok"
        if ratio <= (1 + warn_margin * 2): return "warn"
        return "bad"


# ── HTML ──────────────────────────────────────────────────────────────────────

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
       background: #0f0f0f; color: #f0f0f0; padding: 2rem; max-width: 1200px; margin: 0 auto; }
.page-header { border-left: 4px solid #e50914; padding-left: 1rem; margin-bottom: 2.5rem; }
.page-header h1 { font-size: 1.8rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.05em; }
.page-header .sub { color: #666; font-size: 0.85rem; margin-top: 0.3rem; }
.card { background: #161616; border: 1px solid #252525; border-radius: 10px;
        padding: 1.5rem; margin-bottom: 1.5rem; }
.card.err { border-color: #e50914; }
.card-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.25rem; }
.card-header h2 { font-size: 1.15rem; font-weight: 700; }
.badge { background: #e50914; color: #fff; font-size: 0.7rem; font-weight: 700;
         padding: 0.2rem 0.55rem; border-radius: 4px; text-transform: uppercase; }
.badge.quarter { background: #333; }
.meta { color: #777; font-size: 0.8rem; margin-bottom: 1rem; }
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 0.75rem; margin-bottom: 1.25rem; }
.kpi { background: #1f1f1f; border-radius: 7px; padding: 0.9rem; border-top: 3px solid #333; }
.kpi.ok  { border-top-color: #22c55e; }
.kpi.warn { border-top-color: #f59e0b; }
.kpi.bad { border-top-color: #e50914; }
.kpi.neutral { border-top-color: #555; }
.kpi-lbl { font-size: 0.68rem; color: #777; text-transform: uppercase;
           letter-spacing: 0.06em; margin-bottom: 0.4rem; }
.kpi-val { font-size: 1.6rem; font-weight: 900; line-height: 1; }
.kpi-sub { font-size: 0.7rem; color: #888; margin-top: 0.3rem; }
table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
th { background: #111; color: #666; padding: 0.45rem 0.6rem;
     text-align: left; font-weight: 600; border-bottom: 1px solid #252525; }
td { padding: 0.45rem 0.6rem; border-bottom: 1px solid #1e1e1e; }
tr:last-child td { border-bottom: none; }
.err-msg { color: #e50914; font-size: 0.9rem; }
.footer { text-align: center; color: #333; font-size: 0.72rem; margin-top: 3rem; }
.no-google { color: #555; font-size: 0.85rem; padding: 0.5rem 0; }
"""

def build_card(display_name, okrs, data):
    if "error" in data:
        return f"""<div class="card err">
  <div class="card-header"><h2>{display_name}</h2><span class="badge">Erro</span></div>
  <p class="err-msg">{data['error']}</p>
</div>"""

    acct  = data.get("account", {})
    camps = data.get("campaigns", [])

    cost        = safe_float(acct.get("metrics.cost"))        or sum(safe_float(c.get("metrics.cost")) for c in camps)
    conversions = safe_float(acct.get("metrics.conversions")) or sum(safe_float(c.get("metrics.conversions")) for c in camps)
    clicks      = safe_int(acct.get("metrics.clicks"))        or sum(safe_int(c.get("metrics.clicks")) for c in camps)
    impressions = safe_int(acct.get("metrics.impressions"))   or sum(safe_int(c.get("metrics.impressions")) for c in camps)

    ctr = (clicks / impressions * 100) if impressions else 0
    cac = (cost / conversions)         if conversions else 0

    targets  = okrs.get("targets", {})
    t_invest = targets.get("investimento_semana", 0)
    t_leads  = targets.get("leads_semana", 0)
    t_cac    = targets.get("cac_max", 0)
    quarter  = okrs.get("quarter", "Q2 2026")
    meta_str = okrs.get("meta_anual", "")

    s_invest = status(cost, t_invest, higher_is_better=False) if t_invest else "neutral"
    s_leads  = status(conversions, t_leads)                   if t_leads  else "neutral"
    s_cac    = status(cac, t_cac, higher_is_better=False)     if t_cac    else "neutral"

    def sub_invest():
        if t_invest: return f"{pct(cost, t_invest)}% da meta ${t_invest:,.0f}"
        return "sem meta definida"
    def sub_leads():
        if t_leads: return f"{pct(conversions, t_leads)}% da meta {t_leads}"
        return "sem meta definida"
    def sub_cac():
        if t_cac: return f"Max ${t_cac:,.0f}"
        return "sem meta definida"

    top = sorted(camps, key=lambda x: safe_float(x.get("metrics.cost")), reverse=True)[:5]
    rows = "".join(f"""<tr>
      <td>{c.get('campaign.name','')[:45]}</td>
      <td>${safe_float(c.get('metrics.cost')):,.0f}</td>
      <td>{safe_float(c.get('metrics.conversions')):.0f}</td>
      <td>${safe_float(c.get('metrics.cost_per_conversion')):,.0f}</td>
      <td>{safe_float(c.get('metrics.ctr',0))*100:.1f}%</td>
    </tr>""" for c in top)

    table = f"""<table>
  <thead><tr><th>Campanha</th><th>Spend</th><th>Conv.</th><th>CAC</th><th>CTR</th></tr></thead>
  <tbody>{rows}</tbody>
</table>""" if top else ""

    return f"""<div class="card">
  <div class="card-header">
    <h2>{display_name}</h2>
    <span class="badge quarter">{quarter}</span>
  </div>
  {f'<p class="meta">Meta anual: {meta_str}</p>' if meta_str else ''}
  <div class="kpis">
    <div class="kpi {s_invest}">
      <div class="kpi-lbl">Investimento</div>
      <div class="kpi-val">${cost:,.0f}</div>
      <div class="kpi-sub">{sub_invest()}</div>
    </div>
    <div class="kpi {s_leads}">
      <div class="kpi-lbl">Conversões</div>
      <div class="kpi-val">{conversions:.0f}</div>
      <div class="kpi-sub">{sub_leads()}</div>
    </div>
    <div class="kpi {s_cac}">
      <div class="kpi-lbl">CAC</div>
      <div class="kpi-val">${cac:,.0f}</div>
      <div class="kpi-sub">{sub_cac()}</div>
    </div>
    <div class="kpi neutral">
      <div class="kpi-lbl">CTR</div>
      <div class="kpi-val">{ctr:.1f}%</div>
      <div class="kpi-sub">{clicks:,} cliques / {impressions:,} imp.</div>
    </div>
  </div>
  {table}
</div>"""


def build_html(cards, week_start, week_end):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Relatório Semanal OKR — {week_start} a {week_end}</title>
<style>{CSS}</style>
</head>
<body>
<div class="page-header">
  <h1>Relatório Semanal — OKR + Google Ads</h1>
  <div class="sub">{week_start} → {week_end} &nbsp;·&nbsp; Gerado em {now}</div>
</div>
{''.join(cards)}
<div class="footer">trafego-relatorio-semanal-okr · Builders Hub V4 · marcoslrvusa</div>
</body>
</html>"""


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clientes", help="Lista separada por vírgula")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--out")
    ap.add_argument("--base")
    args = ap.parse_args()

    base = Path(args.base) if args.base else find_clients_base()
    if not base:
        print("ERRO: pasta clientes/ não encontrada", file=sys.stderr); sys.exit(1)

    names = [n.strip() for n in args.clientes.split(",")] if args.clientes else list_configured_clients(base)
    if not names:
        print("Nenhum cliente com GOOGLE_ADS_CUSTOMER_ID configurado.")
        print("Configure em clientes/<cliente>/.env e em clientes/<cliente>/okrs.json")
        sys.exit(0)

    end   = datetime.today() - timedelta(days=1)
    start = end - timedelta(days=args.days - 1)
    w_start = start.strftime("%d/%m/%Y")
    w_end   = end.strftime("%d/%m/%Y")

    print(f"Gerando relatório: {w_start} → {w_end} | {len(names)} cliente(s)\n")

    cards = []
    for name in names:
        folder = base / name
        display = load_client_name(folder)
        okrs    = load_okrs(folder)
        print(f"  {display}...", end=" ", flush=True)
        data = pull_data(name, base, args.days)
        if "error" in data:
            print(f"ERRO: {data['error']}")
        else:
            n_camps = len(data.get("campaigns", []))
            print(f"OK ({n_camps} campanhas)")
        cards.append(build_card(display, okrs, data))

    html = build_html(cards, w_start, w_end)

    if args.out:
        out = Path(args.out)
    else:
        week_tag = start.strftime("%Y-W%V")
        out = Path(f"relatorios/okr-semanal-{week_tag}.html")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"\nRelatório salvo: {out}")
    return str(out)


if __name__ == "__main__":
    main()
