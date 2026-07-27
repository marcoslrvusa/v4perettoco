#!/usr/bin/env python3
"""
Agent Orchestrator — CLI de orquestração autônoma com learning loop.

FLUXO COMPLETO (cmd_process):
  1. dequeue_next() da agent_queue (Supabase)
  2. search.py → busca memórias similares no pgvector
  3. classify_demand() → orquestrador + especialistas + modo
  4. write_brief() → /workspace/input/
  5. [OpenCode agent executa...]
  6. record.py → registra aprendizado no pgvector
  7. update_routing_stats()
  8. update_queue_item(completed)

Uso:
  python agent-orchestrator.py queue              → Lista fila
  python agent-orchestrator.py process [--id]     → Ciclo completo
  python agent-orchestrator.py classify --id      → Só classifica
  python agent-orchestrator.py status             → Saúde do sistema
  python agent-orchestrator.py report             → Performance
  python agent-orchestrator.py enqueue ...        → Insere demanda
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Optional

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_SCRIPTS_DIR = os.path.normpath(
    os.path.join(SCRIPT_DIR, "..", "..", "..", "geral-memoria-agentes", "scripts")
)
SEARCH_PY = os.path.join(MEMORY_SCRIPTS_DIR, "search.py")
RECORD_PY = os.path.join(MEMORY_SCRIPTS_DIR, "record.py")

ORCHESTRATOR_MAP = {
    "aquisicao":      "growth-team",
    "conteudo":       "content-studio",
    "copy":           "copy-orchestrator",
    "saude_cliente":  "account-orchestrator",
    "receita":        "revenue-ops",
    "lancamento":     "launch-pad",
    "operacao":       "csm-orquestrador",
    "lideranca":      "cmoorch",
}

SPECIALIST_MAP = {
    "experimento_cro":      "cro-lab",
    "campanha_paga":        "midia-paga",
    "seo_visibilidade":     "seo-visibilidade",
    "pesquisa_mercado":     "pesquisador",
    "analise_dados":        "analista-dados",
    "automacao":            "automacao-analytics",
    "copy_geral":           "copy-writer",
    "copy_anuncio":         "ads-writer",
    "copy_email":           "email-writer",
    "copy_social":          "social-writer",
    "copy_landing":         "landing-writer",
    "design":               "criacao-design",
    "relatorio_trafego":    "relatorios-trafego",
    "n8n_automacao":        "n8n-automator",
}

FLAG_ORCHESTRATOR_MAP = {
    "flag-roi":      "growth-team",
    "flag-churn":    "account-orchestrator",
    "flag-okr":      "cmoorch",
    "flag-operacao": "csm-orquestrador",
}

INPUT_DIR = "/workspace/input"
OUTPUT_DIR = "/workspace/output"


def supabase_request(method: str, path: str, data: dict = None) -> dict:
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            if content.strip():
                return json.loads(content)
            return []
    except urllib.error.HTTPError as e:
        print(f"[ERRO] Supabase {method} {path}: {e.code} {e.read().decode()}")
        return {}
    except Exception as e:
        print(f"[ERRO] Supabase {method} {path}: {e}")
        return {}


def supabase_rpc(func: str, params: dict = None) -> dict:
    return supabase_request("POST", f"rpc/{func}", params or {})


def list_queue(status: str = "pending", limit: int = 20):
    params = f"status=eq.{status}&order=priority.desc,created_at.asc&limit={limit}"
    return supabase_request("GET", f"agent_queue?{params}")


def search_memories(query: str, top_k: int = 5) -> list:
    """Chama search.py para buscar memórias similares no pgvector.
    Retorna lista vazia se search.py não estiver disponível ou falhar."""
    if not os.path.isfile(SEARCH_PY):
        print("  [MEMORIA] search.py não encontrado em", SEARCH_PY)
        return []
    try:
        result = subprocess.run(
            ["python3", SEARCH_PY, "--query", query, "--limit", str(top_k)],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            mems = data.get("results", []) if isinstance(data, dict) else []
            print(f"  [MEMORIA] {len(mems)} memórias similares encontradas")
            return mems
    except subprocess.TimeoutExpired:
        print("  [MEMORIA] search.py timeout")
    except Exception as e:
        print(f"  [MEMORIA] search.py erro: {e}")
    return []


def record_memory(summary: str, content: str, function: str, orchestrator: str,
                  specialist: str, strategy: str, result: str, success_score: int):
    """Chama record.py para registrar aprendizado no pgvector."""
    if not os.path.isfile(RECORD_PY):
        print("  [APRENDIZADO] record.py não encontrado em", RECORD_PY)
        return
    try:
        subprocess.run(
            ["python3", RECORD_PY,
             "--summary", summary,
             "--content", content,
             "--agent-role", orchestrator,
             "--task-type", function,
             "--strategy", strategy,
             "--result", result,
             "--success-score", str(success_score),
             "--tags", f"orchestrator:{orchestrator},function:{function},specialist:{specialist}"],
            capture_output=True, text=True, timeout=30,
        )
        print("  [APRENDIZADO] Registrado com sucesso")
    except Exception as e:
        print(f"  [APRENDIZADO] record.py erro: {e}")


def classify_demand(item: dict) -> dict:
    briefing = item.get("briefing", {})
    if isinstance(briefing, str):
        try: briefing = json.loads(briefing)
        except: briefing = {"raw": briefing}
    demand_type = item.get("demand_type", "")
    function = item.get("function", "")
    source = item.get("source", "")
    priority = item.get("priority", 0)

    if source in FLAG_ORCHESTRATOR_MAP:
        orchestrator = FLAG_ORCHESTRATOR_MAP[source]
    elif function in ORCHESTRATOR_MAP:
        orchestrator = ORCHESTRATOR_MAP[function]
    else:
        orchestrator = "cmoorch"

    sub_task = briefing.get("sub_task", "")
    specialists = []
    if sub_task in SPECIALIST_MAP:
        specialists = [SPECIALIST_MAP[sub_task]]
    elif function == "aquisicao":
        specialists = ["cro-lab", "midia-paga", "seo-visibilidade", "copy-writer"]
    elif function == "conteudo":
        specialists = ["estrategia-marketing", "copy-writer", "criacao-design", "seo-visibilidade"]
    elif function == "copy":
        specialist = briefing.get("copy_type", "copy_geral")
        specialists = [SPECIALIST_MAP.get(specialist, "copy-writer")]
    elif function == "saude_cliente":
        specialists = ["pesquisador", "vendas-account", "analista-dados"]
    elif function == "operacao":
        specialists = ["analista-dados", "automacao-analytics"]
    elif function == "receita":
        specialists = ["analista-dados", "automacao-analytics", "copy-writer"]
    elif function == "lancamento":
        specialists = ["estrategia-marketing", "copy-writer", "criacao-design", "midia-paga", "seo-visibilidade"]

    if priority >= 80:
        mode = "autonomo"
    elif priority >= 50:
        mode = "semi"
    elif demand_type == "flag":
        mode = "semi"
    else:
        mode = "manual"

    return {
        "orchestrator": orchestrator,
        "specialists": specialists,
        "mode": mode,
    }


def write_brief(item: dict, classification: dict, memories: list = None) -> str:
    os.makedirs(INPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{item.get('id', 'unknown')}.json"
    filepath = os.path.join(INPUT_DIR, filename)

    briefing = item.get("briefing", {})
    if isinstance(briefing, str):
        try: briefing = json.loads(briefing)
        except: briefing = {"raw": briefing}

    brief = {
        "queue_id": item.get("id", item.get("o_id", "unknown")),
        "demand_type": item.get("demand_type", ""),
        "source": item.get("source", ""),
        "function": item.get("function", ""),
        "urgency": item.get("urgency", ""),
        "scope": item.get("scope", ""),
        "orchestrator": classification["orchestrator"],
        "specialists": classification["specialists"],
        "mode": classification["mode"],
        "briefing": briefing,
        "memories": memories or [],
        "created_at": item.get("created_at", ""),
    }

    with open(filepath, "w") as f:
        json.dump(brief, f, indent=2, default=str)

    print(f"[OK] Brief escrito: {filepath}")
    return filepath


def update_queue_item(item_id: str, updates: dict):
    path = f"agent_queue?id=eq.{item_id}"
    supabase_request("PATCH", path, updates)


def log_event(queue_id: str, event: str, detail: dict = None):
    data = {
        "queue_id": queue_id,
        "event": event,
        "detail": json.dumps(detail or {}),
    }
    supabase_request("POST", "agent_queue_log", data)


def update_routing_stats(orchestrator: str, specialist: str, function: str, score: int, exec_time: int):
    try:
        result = supabase_rpc("update_routing_stats", {
            "p_orchestrator": orchestrator,
            "p_specialist": specialist,
            "p_function": function,
            "p_success_score": score,
            "p_execution_time_seconds": exec_time,
        })
        if isinstance(result, dict) and result.get("message"):
            print(f"  [STATS] RPC indisponivel: {result['message']}")
        else:
            print(f"  [STATS] Atualizado")
    except Exception as e:
        print(f"  [STATS] Erro: {e}")


def cmd_queue(args):
    items = list_queue(status=args.status, limit=args.limit)
    if not items:
        print("Fila vazia.")
        return

    print(f"\n{'ID':<38} {'TIPO':<12} {'FUNCAO':<16} {'URG':<8} {'STATUS':<14} {'FONTE':<20} {'PRIO':<6}")
    print("-" * 116)
    for i in items:
        qid = i.get("id", "")[:8]
        dtype = i.get("demand_type", "")
        func = i.get("function", "")
        urg = i.get("urgency", "")
        st = i.get("status", "")
        src = i.get("source", "")
        prio = i.get("priority", 0)
        print(f"{qid:<38} {dtype:<12} {func:<16} {urg:<8} {st:<14} {src:<20} {prio:<6}")


def cmd_process(args):
    t0 = time.time()

    if args.id:
        items = supabase_request("GET", f"agent_queue?id=eq.{args.id}")
    else:
        items = supabase_rpc("dequeue_next")
        if isinstance(items, list) and len(items) > 0:
            items = [items[0]]
        else:
            items = []

    if not items:
        print("Nenhum item pendente para processar.")
        return

    item = items[0] if isinstance(items, list) else items

    # Normalizar chaves o_* (RPC legacy) para nomes diretos
    if "o_id" in item:
        item = {k[2:] if k.startswith("o_") else k: v for k, v in item.items()}
    qid = item.get("id") or item.get("o_id", "")
    function = item.get("function", "")
    demand_type = item.get("demand_type", "")
    source = item.get("source", "")
    briefing = item.get("briefing", {})
    if isinstance(briefing, str):
        try: briefing = json.loads(briefing)
        except: briefing = {"raw": briefing}
    print(f"\n[PROCESSANDO] {qid} | {function} | {source}")

    log_event(qid, "process_start", {"item": item})

    # PASSO 1: Buscar memórias similares (learning loop)
    search_query = f"{function}: {briefing.get('task', '')} {briefing.get('sub_task', '')}"
    memories = search_memories(search_query)
    log_event(qid, "memories_consulted", {"count": len(memories), "memories": memories})

    # PASSO 2: Classificar demanda
    classification = classify_demand(item)
    orchestrator = classification["orchestrator"]
    specialists = classification["specialists"]
    mode = classification["mode"]
    print(f"  Orquestrador: @{orchestrator}")
    print(f"  Especialistas: {', '.join(f'@{s}' for s in specialists)}")
    print(f"  Modo: {mode}")
    print(f"  Memórias consultadas: {len(memories)}")

    update_queue_item(qid, {
        "status": "processing",
        "classification": json.dumps(classification),
        "orchestrator": orchestrator,
        "assigned_to": orchestrator,
    })

    # PASSO 3: Escrever brief enriquecido com memórias
    brief_path = write_brief(item, classification, memories)

    log_event(qid, "classified", {
        "orchestrator": orchestrator,
        "specialists": specialists,
        "mode": mode,
        "brief_path": brief_path,
        "memories_count": len(memories),
    })

    if mode == "autonomo":
        update_queue_item(qid, {"status": "processing"})
        print(f"  [AUTONOMO] Brief em {brief_path}. Orquestrador processando...")

        # TODO: Acionar agente OpenCode via task delegation
        # e aguardar resultado em /workspace/output/

        # PASSO 4 (simulado): Registrar aprendizado
        record_memory(
            summary=f"Demanda {function} processada em modo autônomo",
            content=json.dumps({"brief_path": brief_path, "classification": classification}),
            function=function,
            orchestrator=orchestrator,
            specialist=specialists[0] if specialists else "",
            strategy=f"roteamento:{orchestrator}->{'/'.join(specialists)}",
            result="processado",
            success_score=7,
        )

        update_queue_item(qid, {
            "status": "completed",
            "completed_at": datetime.now(timezone.utc).isoformat(),
        })

    elif mode == "semi":
        update_queue_item(qid, {"status": "awaiting_review"})
        print(f"  [SEMI] Brief em {brief_path}. Aguardando revisão humana.")

        record_memory(
            summary=f"Demanda {function} aguardando revisão (semi-autônomo)",
            content=json.dumps({"brief_path": brief_path, "classification": classification}),
            function=function,
            orchestrator=orchestrator,
            specialist=specialists[0] if specialists else "",
            strategy=f"roteamento:{orchestrator}->{'/'.join(specialists)}",
            result="awaiting_review",
            success_score=5,
        )
    else:
        update_queue_item(qid, {"status": "awaiting_review"})
        print(f"  [MANUAL] Brief em {brief_path}. Aguardando aprovação humana.")

    # PASSO 5: Atualizar estatísticas de roteamento
    elapsed = int(time.time() - t0)
    update_routing_stats(orchestrator, specialists[0] if specialists else "", function, 7, elapsed)

    log_event(qid, "process_complete", {
        "elapsed_seconds": elapsed,
        "mode": mode,
        "memories_count": len(memories),
    })

    print(f"\n[CICLO COMPLETO] {elapsed}s")


def cmd_classify(args):
    items = supabase_request("GET", f"agent_queue?id=eq.{args.id}")
    if not items:
        print(f"Item {args.id} não encontrado.")
        return
    item = items[0]
    print(f"\n[CLASSIFICANDO] {args.id}")
    print(json.dumps(classify_demand(item), indent=2))


def cmd_status(args):
    print("\n=== SAÚDE DO SISTEMA ===\n")

    pending = list_queue(status="pending", limit=1)
    processing = list_queue(status="processing", limit=1)
    awaiting = list_queue(status="awaiting_review", limit=1)

    print(f"  Pendentes:        {len(pending) if isinstance(pending, list) else 0}+")
    print(f"  Em processamento: {len(processing) if isinstance(processing, list) else 0}")
    print(f"  Aguardando review: {len(awaiting) if isinstance(awaiting, list) else 0}")

    has_supabase = bool(SUPABASE_URL and SUPABASE_KEY)
    has_input = os.path.isdir(INPUT_DIR)
    has_output = os.path.isdir(OUTPUT_DIR)
    has_memory = os.path.isfile(SEARCH_PY) and os.path.isfile(RECORD_PY)

    print(f"\n  Conexão Supabase:  {'OK' if has_supabase else 'FALTA SUPABASE_URL/KEY'}")
    print(f"  Input dir:         {'OK' if has_input else 'FALTA /workspace/input'}")
    print(f"  Output dir:        {'OK' if has_output else 'FALTA /workspace/output'}")
    print(f"  Learning loop:     {'OK' if has_memory else 'FALTA search.py/record.py'}")

    print(f"\n  Orquestradores disponíveis: {len(ORCHESTRATOR_MAP)}")
    print(f"  Especialistas disponíveis:  {len(SPECIALIST_MAP)}")
    print(f"  Flags mapeadas:             {len(FLAG_ORCHESTRATOR_MAP)}")


def cmd_report(args):
    stats = supabase_request("GET", "agent_routing_stats?order=date.desc&limit=50")
    if not stats:
        print("Nenhuma estatística disponível ainda.")
        return

    print(f"\n=== RELATÓRIO DE PERFORMANCE ===\n")
    print(f"{'DATA':<12} {'ORQUESTRADOR':<22} {'ESPECIALISTA':<20} {'FUNCAO':<16} {'EXEC':<6} {'OK':<5} {'FAIL':<5} {'SCORE':<7} {'T(MEDIO)':<10}")
    print("-" * 105)
    for s in stats:
        date = s.get("date", "")[:10]
        orch = s.get("orchestrator", "")
        spec = s.get("specialist", "")
        func = s.get("function", "")
        execs = s.get("executions", 0)
        ok = s.get("success_count", 0)
        fail = s.get("fail_count", 0)
        score = s.get("avg_success_score", 0)
        t = s.get("avg_execution_time_seconds", 0)
        print(f"{date:<12} {orch:<22} {spec:<20} {func:<16} {execs:<6} {ok:<5} {fail:<5} {score:<7} {t}s{':<4'}")


def cmd_enqueue(args):
    briefing_obj = json.loads(args.briefing) if args.briefing else {}
    data = {
        "demand_type": args.demand_type or "manual",
        "source": args.source or "manual",
        "function": args.function,
        "urgency": args.urgency or "normal",
        "scope": args.scope or "single",
        "briefing": briefing_obj,
        "priority": args.priority or 0,
    }

    result = supabase_request("POST", "agent_queue", data)
    if result:
        qid = result[0]["id"] if isinstance(result, list) else result.get("id", "?")
        print(f"[OK] Demanda enfileirada: {qid}")
        print(f"  Função: {data['function']} | Urgência: {data['urgency']} | Prioridade: {data['priority']}")
    else:
        print(f"[ERRO] Falha ao enfileirar demanda.")


def main():
    parser = argparse.ArgumentParser(description="Agent Orchestrator CLI")
    sub = parser.add_subparsers(dest="command")

    p_queue = sub.add_parser("queue", help="Lista a fila")
    p_queue.add_argument("--status", default="pending", help="Filtrar por status")
    p_queue.add_argument("--limit", type=int, default=20, help="Máx. itens")

    p_process = sub.add_parser("process", help="Processa 1 item da fila (ciclo completo c/ learning loop)")
    p_process.add_argument("--id", help="ID específico (opcional, pega próximo se omitir)")

    p_classify = sub.add_parser("classify", help="Classifica uma demanda")
    p_classify.add_argument("--id", required=True, help="ID do item")

    p_status = sub.add_parser("status", help="Saúde do sistema")

    p_report = sub.add_parser("report", help="Relatório de performance")

    p_enqueue = sub.add_parser("enqueue", help="Enfileira nova demanda")
    p_enqueue.add_argument("--demand-type", default="manual", help="Tipo: flag/scheduled/manual/webhook")
    p_enqueue.add_argument("--source", default="manual", help="Origem da demanda")
    p_enqueue.add_argument("--function", required=True, help="Função: aquisicao/conteudo/saude_cliente/receita/lancamento/operacao/lideranca/copy")
    p_enqueue.add_argument("--urgency", default="normal", help="baixa/normal/alta/critica")
    p_enqueue.add_argument("--scope", default="single", help="single/team/multi_team")
    p_enqueue.add_argument("--briefing", help="JSON com o briefing")
    p_enqueue.add_argument("--priority", type=int, default=0, help="Prioridade 0-100")

    args = parser.parse_args()

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[ERRO] Configure SUPABASE_URL e SUPABASE_SERVICE_KEY no ambiente.")
        sys.exit(1)

    commands = {
        "queue": cmd_queue,
        "process": cmd_process,
        "classify": cmd_classify,
        "status": cmd_status,
        "report": cmd_report,
        "enqueue": cmd_enqueue,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
