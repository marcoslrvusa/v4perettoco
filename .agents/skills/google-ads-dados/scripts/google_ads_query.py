#!/usr/bin/env python3
"""
google_ads_query.py — Consulta Google Ads via API oficial.
Skill: google-ads-dados | Builders Hub V4
"""
import os, sys, json, csv, io, argparse
from pathlib import Path
from datetime import datetime, timedelta

try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
except ImportError:
    print("ERRO: pip install google-ads", file=sys.stderr); sys.exit(1)


# ── Env ──────────────────────────────────────────────────────────────────────

def find_env(cliente=None):
    candidates = []
    if cliente:
        candidates += [Path(f"clientes/{cliente}/.env"), Path(f"../{cliente}/.env")]
    candidates += [Path(".env")]
    for p in candidates:
        if p.exists():
            return p
    if cliente:
        return Path(f"clientes/{cliente}/.env")
    return Path(".env")


def load_env(path):
    env = {}
    if not path or not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


REQUIRED = ["GOOGLE_ADS_DEVELOPER_TOKEN","GOOGLE_ADS_CLIENT_ID",
            "GOOGLE_ADS_CLIENT_SECRET","GOOGLE_ADS_REFRESH_TOKEN","GOOGLE_ADS_CUSTOMER_ID"]


def resolve_creds(env, env_path):
    missing = [k for k in REQUIRED if not env.get(k)]
    if not missing:
        return env
    if not sys.stdin.isatty():
        print(f"ERRO: Credenciais faltando: {', '.join(missing)}\n  Arquivo: {env_path}", file=sys.stderr)
        sys.exit(2)
    print(f"\nFaltam credenciais do Google Ads em {env_path}")
    print("Como obter: veja SKILL.md da skill google-ads-dados\n")
    vals = {}
    for k in missing:
        vals[k] = input(f"  {k}: ").strip()
    with open(env_path, "a", encoding="utf-8") as f:
        f.write("\n# ─── Google Ads ──────────────────────────────────────\n")
        for k, v in vals.items():
            f.write(f"{k}={v}\n")
    print(f"Salvo em {env_path}\n")
    env.update(vals)
    return env


def build_client(env):
    cfg = {
        "developer_token": env["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "client_id": env["GOOGLE_ADS_CLIENT_ID"],
        "client_secret": env["GOOGLE_ADS_CLIENT_SECRET"],
        "refresh_token": env["GOOGLE_ADS_REFRESH_TOKEN"],
        "use_proto_plus": True,
    }
    mcc = env.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID","").replace("-","")
    if mcc:
        cfg["login_customer_id"] = mcc
    cid = env["GOOGLE_ADS_CUSTOMER_ID"].replace("-","")
    return GoogleAdsClient.load_from_dict(cfg), cid


# ── GAQL Presets ─────────────────────────────────────────────────────────────

def period_clause(days=None, since=None, until=None):
    if since and until:
        return f"BETWEEN '{since}' AND '{until}'"
    if days:
        end = datetime.today() - timedelta(days=1)
        start = end - timedelta(days=days-1)
        return f"BETWEEN '{start:%Y-%m-%d}' AND '{end:%Y-%m-%d}'"
    return "DURING LAST_7_DAYS"


PRESETS = {
    "account": """
        SELECT customer.descriptive_name, customer.currency_code,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.all_conversions, metrics.ctr,
               metrics.average_cpc, metrics.cost_per_conversion
        FROM customer WHERE segments.date {p}""",

    "campaigns": """
        SELECT campaign.name, campaign.status, campaign.advertising_channel_type,
               campaign_budget.amount_micros,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.ctr, metrics.average_cpc,
               metrics.cost_per_conversion, metrics.search_impression_share
        FROM campaign
        WHERE segments.date {p} AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC""",

    "adgroups": """
        SELECT campaign.name, ad_group.name, ad_group.status,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.ctr, metrics.average_cpc
        FROM ad_group
        WHERE segments.date {p} AND ad_group.status != 'REMOVED'
          AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC""",

    "keywords": """
        SELECT campaign.name, ad_group.name,
               ad_group_criterion.keyword.text,
               ad_group_criterion.keyword.match_type,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.ctr, metrics.average_cpc,
               metrics.quality_score
        FROM keyword_view
        WHERE segments.date {p} AND ad_group_criterion.status != 'REMOVED'
          AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC""",

    "search_terms": """
        SELECT campaign.name, ad_group.name,
               search_term_view.search_term, search_term_view.status,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.ctr
        FROM search_term_view
        WHERE segments.date {p}
        ORDER BY metrics.cost_micros DESC""",

    "conversions": """
        SELECT conversion_action.name, conversion_action.category,
               metrics.conversions, metrics.all_conversions, metrics.conversions_value
        FROM conversion_action
        WHERE segments.date {p} AND conversion_action.status = 'ENABLED'
        ORDER BY metrics.conversions DESC""",
}


# ── Query ─────────────────────────────────────────────────────────────────────

def row_to_dict(row):
    raw = json.loads(type(row).to_json(row))
    flat = {}
    def _flatten(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                _flatten(v, f"{prefix}{k}.")
        elif isinstance(obj, list):
            flat[prefix.rstrip(".")] = obj
        else:
            flat[prefix.rstrip(".")] = obj
    _flatten(raw)
    # micros → dollars
    for k in list(flat.keys()):
        if ("cost_micros" in k or "amount_micros" in k or "average_cpc" in k) and isinstance(flat[k], (int,float)) and flat[k]:
            flat[k.replace("_micros","")] = round(flat[k] / 1_000_000, 2)
    return flat


def run_query(client, customer_id, gaql):
    svc = client.get_service("GoogleAdsService")
    try:
        stream = svc.search_stream(customer_id=customer_id, query=gaql)
        return [row_to_dict(row) for batch in stream for row in batch.results]
    except GoogleAdsException as ex:
        for err in ex.failure.errors:
            print(f"ERRO API: {err.message}", file=sys.stderr)
        sys.exit(1)


# ── Output ────────────────────────────────────────────────────────────────────

def fmt_table(rows, fields=None):
    if not rows: return "(sem resultados)"
    keys = fields or list(rows[0].keys())
    widths = {k: min(max(len(k), max(len(str(r.get(k,""))) for r in rows)), 45) for k in keys}
    hdr = "  ".join(k.ljust(widths[k]) for k in keys)
    sep = "  ".join("-"*widths[k] for k in keys)
    body = "\n".join("  ".join(str(r.get(k,""))[:widths[k]].ljust(widths[k]) for k in keys) for r in rows)
    return f"{hdr}\n{sep}\n{body}"


def fmt_csv(rows, fields=None):
    if not rows: return ""
    keys = fields or list(rows[0].keys())
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=keys, extrasaction="ignore")
    w.writeheader(); w.writerows(rows)
    return buf.getvalue()


def format_output(rows, fmt, fields):
    if fields: rows = [{k: r.get(k) for k in fields} for r in rows]
    if fmt == "json": return json.dumps(rows, ensure_ascii=False, indent=2)
    if fmt == "csv":  return fmt_csv(rows, fields)
    return fmt_table(rows, fields)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Consulta Google Ads")
    p.add_argument("query", help=f"Preset: {', '.join(PRESETS)} — ou GAQL completo")
    p.add_argument("--cliente")
    p.add_argument("--days", type=int)
    p.add_argument("--since"); p.add_argument("--until")
    p.add_argument("--fields")
    p.add_argument("--format", choices=["table","json","csv"], default="table")
    p.add_argument("--out")
    p.add_argument("--max", type=int)
    p.add_argument("--customer-id")
    args = p.parse_args()

    env_path = find_env(args.cliente)
    env = load_env(env_path)
    env = resolve_creds(env, env_path)
    client, cid = build_client(env)
    if args.customer_id:
        cid = args.customer_id.replace("-","")

    period = period_clause(args.days, args.since, args.until)
    key = args.query.lower()
    gaql = PRESETS[key].format(p=period) if key in PRESETS else args.query

    rows = run_query(client, cid, gaql)
    if args.max: rows = rows[:args.max]

    fields = [f.strip() for f in args.fields.split(",")] if args.fields else None
    output = format_output(rows, args.format, fields)

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Salvo: {args.out} ({len(rows)} linhas)")
    else:
        print(output)
        if args.format == "table":
            print(f"\n{len(rows)} linha(s)")


if __name__ == "__main__":
    main()
