#!/usr/bin/env python3
"""
flag-hook.py — Conecta flags detectadas à agent_queue.

Uso direto (standalone):
  python3 flag-hook.py --flag roi --client "Cliente X" --urgencia Alta --dado "ROAS 1.2 vs meta 2.5"

Uso como módulo (importado pelo detector_flags.py):
  from flag_hook import enqueue_flag
  enqueue_flag(tipo="roi", urgencia="Crítica", dado="ROAS 1.2", cliente="Cliente X", dados_brutos={...})
"""

import json
import os
import sys
import urllib.request
import urllib.error

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

FLAG_FUNCTION_MAP = {
    "roi":      "aquisicao",
    "churn":    "saude_cliente",
    "okr":      "lideranca",
    "operacao": "operacao",
}

FLAG_PRIORITY_MAP = {
    "Crítica": 90,
    "Alta":    70,
    "Média":   50,
    "Baixa":   20,
}


def enqueue_flag(tipo: str, urgencia: str, dado: str, cliente: str = "",
                 dados_brutos: dict = None, source: str = ""):
    """Enfileira uma flag detectada na agent_queue."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print(f"[FLAG-HOOK] AVISO: SUPABASE não configurado. Flag {tipo} não enfileirada.")
        return None

    function = FLAG_FUNCTION_MAP.get(tipo, "operacao")
    priority = FLAG_PRIORITY_MAP.get(urgencia, 50)
    flag_source = source or f"flag-{tipo}"

    briefing = {
        "flag_type": tipo,
        "urgency": urgencia,
        "data": dado,
        "raw_data": dados_brutos or {},
        "cliente": cliente,
    }

    payload = json.dumps({
        "demand_type": "flag",
        "source": flag_source,
        "function": function,
        "urgency": "alta" if urgencia in ("Crítica", "Alta") else "normal",
        "scope": "single",
        "priority": priority,
        "briefing": json.dumps(briefing),
        "status": "pending",
    }).encode()

    url = f"{SUPABASE_URL}/rest/v1/agent_queue"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            qid = result[0]["id"] if isinstance(result, list) else "?"
            print(f"[FLAG-HOOK] Flag {tipo} enfileirada: {qid} (prioridade {priority}, função {function})")
            return qid
    except urllib.error.HTTPError as e:
        print(f"[FLAG-HOOK] ERRO HTTP {e.code}: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"[FLAG-HOOK] ERRO: {e}")
        return None


def main():
    import argparse
    p = argparse.ArgumentParser(description="Flag Hook — enfileira flags na agent_queue")
    p.add_argument("--flag", required=True, help="Tipo: roi/churn/okr/operacao")
    p.add_argument("--urgencia", default="Média", help="Crítica/Alta/Média/Baixa")
    p.add_argument("--dado", default="", help="Descrição do dado detectado")
    p.add_argument("--cliente", default="", help="Nome do cliente")
    p.add_argument("--source", default="", help="Fonte da flag (opcional)")
    p.add_argument("--dados-brutos", default="{}", help="JSON com dados brutos")
    args = p.parse_args()

    qid = enqueue_flag(
        tipo=args.flag,
        urgencia=args.urgencia,
        dado=args.dado,
        cliente=args.cliente,
        source=args.source,
        dados_brutos=json.loads(args.dados_brutos),
    )
    if qid:
        print(f"OK: {qid}")
    else:
        print("FALHA: não foi possível enfileirar")
        sys.exit(1)


if __name__ == "__main__":
    main()
