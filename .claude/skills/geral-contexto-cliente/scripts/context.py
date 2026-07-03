#!/usr/bin/env python3
"""Contexto de Cliente — puxa, registra e sincroniza fatos do cliente no Supabase.

Uso:
  python context.py pull --client nome           # Puxa contexto completo
  python context.py pull --client nome --field tom_de_voz  # Puxa campo específico
  python context.py push --client nome [opções]   # Registra/atualiza manualmente
  python context.py sync --client nome --path pasta  # Sincroniza da KB local
  python context.py sync --all                   # Sincroniza TODOS os clientes da KB local
  python context.py search --query "texto"       # Busca semântica em todos os clientes
  python context.py list                         # Lista todos os clientes com contexto
  python context.py delete --client nome         # Remove contexto de um cliente

Requer env vars:
  SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY
"""

import argparse
import glob as glob_mod
import json
import os
import re
import subprocess
import sys
from datetime import datetime

import openai
import requests


def get_env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        print(f"ERRO: variável {name} não definida", file=sys.stderr)
        sys.exit(1)
    return val


def gerar_embedding(texto: str) -> list[float]:
    client = openai.OpenAI(api_key=get_env("OPENAI_API_KEY"))
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=texto,
        dimensions=1536,
    )
    return resp.data[0].embedding


def supabase_headers():
    key = get_env("SUPABASE_SERVICE_KEY")
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


def supabase_url() -> str:
    return get_env("SUPABASE_URL").rstrip("/")


def detect_root() -> str | None:
    """Tenta detectar a raiz do Builders Hub (onde estão squads/, projetos/)."""
    candidates = [
        os.getcwd(),
        os.path.expanduser("~/Desktop/AI/v4perettoco-main"),
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    ]
    for path in candidates:
        if os.path.isdir(os.path.join(path, "squads")):
            return path
    return None


def extrair_tom_de_voz(claude_path: str) -> str | None:
    """Extrai informações de tom de voz do CLAUDE.md."""
    if not os.path.exists(claude_path):
        return None
    with open(claude_path) as f:
        content = f.read()

    secoes = []
    padroes = [
        r"(?i)##\s*(Tom de voz|Tom|Voz|Brand Voice|Personalidade)",
        r"(?i)##\s*(Diferenciais|Proposta de Valor|Posicionamento)",
    ]
    for padrao in padroes:
        match = re.search(padrao, content)
        if match:
            start = match.start()
            # Pega o bloco até a próxima seção ou 30 linhas
            linhas = content[start:].split("\n")
            bloco = []
            for linha in linhas[1:]:
                if linha.startswith("##"):
                    break
                bloco.append(linha)
            secoes.append("\n".join(bloco).strip())

    return "\n\n".join(secoes) if secoes else None


def extrair_historico(claude_path: str, mission_control_path: str | None) -> str | None:
    """Extrai histórico do CLAUDE.md e mission-control/historico-checkins.md."""
    partes = []

    if os.path.exists(claude_path):
        with open(claude_path) as f:
            content = f.read()

        padroes = [
            r"(?i)##\s*(Histórico|Histórico Comercial|Histórico de Projetos)",
            r"(?i)##\s*(Relacionamento|Combinados|Pendências)",
            r"(?i)##\s*(Estratégia|Objetivos|Teses atuais)",
        ]
        for padrao in padroes:
            match = re.search(padrao, content)
            if match:
                start = match.start()
                linhas = content[start:].split("\n")
                bloco = []
                for linha in linhas[1:]:
                    if linha.startswith("##"):
                        break
                    bloco.append(linha)
                partes.append("\n".join(bloco).strip())

    historico_path = None
    if mission_control_path and os.path.isdir(mission_control_path):
        candidatos = [
            os.path.join(mission_control_path, "historico-checkins.md"),
            os.path.join(mission_control_path, "combinados.md"),
        ]
        for p in candidatos:
            if os.path.exists(p):
                with open(p) as f:
                    content = f.read().strip()
                    if content:
                        partes.append(f"[{os.path.basename(p).replace('.md','')}]\n{content}")

    return "\n\n".join(partes) if partes else None


def extrair_oferta(claude_path: str) -> str | None:
    """Extrai informações de oferta do CLAUDE.md."""
    if not os.path.exists(claude_path):
        return None
    with open(claude_path) as f:
        content = f.read()

    secoes = []
    padroes = [
        r"(?i)##\s*(Oferta|Produto|Serviço|Produto/Serviço)",
        r"(?i)##\s*(Negócio|Segmento|Público-alvo)",
    ]
    for padrao in padroes:
        match = re.search(padrao, content)
        if match:
            start = match.start()
            linhas = content[start:].split("\n")
            bloco = []
            for linha in linhas[1:]:
                if linha.startswith("##"):
                    break
                bloco.append(linha)
            secoes.append("\n".join(bloco).strip())

    return "\n\n".join(secoes) if secoes else None


def extrair_facts(claude_path: str) -> dict:
    """Extrai fatos estruturados adicionais do CLAUDE.md."""
    facts = {}
    if not os.path.exists(claude_path):
        return facts

    with open(claude_path) as f:
        content = f.read()

    padroes = {
        "segmento": r"(?i)-\s*\*{0,2}Segmento\*{0,2}:?\s*(.+)",
        "publico_alvo": r"(?i)-\s*\*{0,2}Público.alvo\*{0,2}:?\s*(.+)",
        "diferenciais": r"(?i)-\s*\*{0,2}Diferenciais\*{0,2}:?\s*(.+)",
        "canais_ativos": r"(?i)-\s*\*{0,2}Canais ativos\*{0,2}:?\s*(.+)",
        "investimento": r"(?i)-\s*\*{0,2}Investimento\*{0,2}:?\s*(.+)",
        "metricas": r"(?i)-\s*\*{0,2}Métricas atuais\*{0,2}:?\s*(.+)",
    }

    for key, padrao in padroes.items():
        match = re.search(padrao, content)
        if match:
            facts[key] = match.group(1).strip().strip("[]").strip('"')

    return facts


def cmd_pull(args):
    """Puxa contexto do cliente do Supabase."""
    supabase = supabase_url()
    headers = supabase_headers()

    # Puxa por cliente exato
    url = f"{supabase}/rest/v1/client_context?client=eq.{args.client}&limit=1"
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print(f"ERRO Supabase ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)

    results = resp.json()
    if not results:
        print(f"Nenhum contexto encontrado para o cliente '{args.client}'.")
        print("Dica: use 'context.py sync --client {args.client}' para sincronizar da KB local.")
        sys.exit(1)

    data = results[0]

    if args.field:
        field = args.field.replace("-", "_")
        if field in data and data[field]:
            val = data[field]
            if isinstance(val, str):
                print(val)
            else:
                print(json.dumps(val, ensure_ascii=False, indent=2))
        else:
            print(f"Campo '{args.field}' não encontrado ou vazio.")
            sys.exit(1)
    else:
        # Output formatado
        print(f"╔══ Cliente: {data['client']} {'(' + data.get('squad', '') + ')' if data.get('squad') else ''}")
        if data.get("tom_de_voz"):
            print(f"║\n║  TOM DE VOZ\n║  {'─' * 50}")
            for linha in data["tom_de_voz"].split("\n"):
                print(f"║  {linha}")
        if data.get("oferta"):
            print(f"║\n║  OFERTA\n║  {'─' * 50}")
            for linha in data["oferta"].split("\n"):
                print(f"║  {linha}")
        if data.get("historico"):
            print(f"║\n║  HISTÓRICO\n║  {'─' * 50}")
            for linha in data["historico"].split("\n"):
                print(f"║  {linha}")
        if data.get("facts") and data["facts"] != {}:
            print(f"║\n║  FATOS EXTRAS\n║  {'─' * 50}")
            for k, v in data["facts"].items():
                print(f"║  {k.replace('_', ' ').title()}: {v}")
        print(f"║\n║  Fonte: {data.get('source', 'N/A')}  |  Atualizado: {data.get('updated_at', 'N/A')[:10]}")
        print(f"╚══")


def cmd_push(args):
    """Registra ou atualiza contexto do cliente manualmente."""
    supabase = supabase_url()
    headers = supabase_headers()

    facts = {}
    if args.facts:
        try:
            facts = json.loads(args.facts)
        except json.JSONDecodeError:
            print("ERRO: facts deve ser um JSON válido", file=sys.stderr)
            sys.exit(1)

    # Gera embedding do conteúdo total para busca semântica
    texto_embed = f"{args.tom_de_voz or ''} {args.historico or ''} {args.oferta or ''} {json.dumps(facts, ensure_ascii=False)}"
    embedding = gerar_embedding(texto_embed) if texto_embed.strip() else None

    record = {
        "client": args.client,
        "squad": args.squad,
        "tom_de_voz": args.tom_de_voz,
        "historico": args.historico,
        "oferta": args.oferta,
        "facts": facts,
        "embedding": embedding,
        "source": args.source or "manual",
    }

    # Tenta upsert via RPC
    payload = {
        "p_client": record["client"],
        "p_squad": record["squad"],
        "p_tom_de_voz": record["tom_de_voz"],
        "p_historico": record["historico"],
        "p_oferta": record["oferta"],
        "p_facts": json.dumps(record["facts"]),
        "p_embedding": record["embedding"],
        "p_source": record["source"],
    }

    url = f"{supabase}/rest/v1/rpc/upsert_client_context"
    resp = requests.post(url, json=payload, headers=headers)

    if resp.status_code == 200:
        print(f"Contexto de '{args.client}' registrado/atualizado com sucesso.")
    else:
        # Fallback: INSERT direto
        del record["embedding"]
        if embedding:
            record["embedding"] = embedding

        url2 = f"{supabase}/rest/v1/client_context"
        headers2 = {**headers, "Prefer": "resolution=merge-duplicates"}
        resp2 = requests.post(url2, json=record, headers=headers2)

        if resp2.status_code in (200, 201, 204):
            print(f"Contexto de '{args.client}' registrado/atualizado com sucesso (fallback).")
        else:
            print(f"ERRO Supabase ({resp2.status_code}): {resp2.text}", file=sys.stderr)
            sys.exit(1)


def cmd_sync(args):
    """Sincroniza contexto da KB local para o Supabase."""
    root = detect_root()
    if not root:
        print("ERRO: não foi possível detectar a raiz do Builders Hub", file=sys.stderr)
        print("Execute de dentro do repositório ou use --path", file=sys.stderr)
        sys.exit(1)

    clientes = []

    if args.all:
        # Descobre todos os clientes
        pattern = os.path.join(root, "squads", "*", "clientes", "*")
        for pasta in glob_mod.glob(pattern):
            nome = os.path.basename(pasta)
            squad = os.path.basename(os.path.dirname(os.path.dirname(pasta)))
            clientes.append((nome, squad, pasta))
    elif args.client:
        if args.path:
            pasta = args.path
        else:
            # Procura o cliente
            pattern = os.path.join(root, "squads", "*", "clientes", args.client)
            matches = glob_mod.glob(pattern)
            if not matches:
                print(f"Cliente '{args.client}' não encontrado em squads/*/clientes/", file=sys.stderr)
                sys.exit(1)
            pasta = matches[0]

        nome = os.path.basename(pasta)
        squad = os.path.basename(os.path.dirname(os.path.dirname(pasta)))
        clientes.append((nome, squad, pasta))
    else:
        print("Use --client NOME ou --all", file=sys.stderr)
        sys.exit(1)

    for nome, squad, pasta in clientes:
        print(f"↻ Sincronizando '{nome}' ({squad})...")

        claude_path = os.path.join(pasta, "CLAUDE.md")
        mission_path = os.path.join(pasta, "mission-control")

        tom_de_voz = extrair_tom_de_voz(claude_path) or args.tom_de_voz
        historico = extrair_historico(claude_path, mission_path) or args.historico
        oferta = extrair_oferta(claude_path) or args.oferta
        facts = extrair_facts(claude_path)

        if args.facts:
            try:
                facts.update(json.loads(args.facts))
            except json.JSONDecodeError:
                print(f"  AVISO: facts inválido, ignorado", file=sys.stderr)

        if not any([tom_de_voz, historico, oferta, facts]):
            print(f"  AVISO: nenhum dado extraído para '{nome}', pulando", file=sys.stderr)
            continue

        # Simula push
        class PushArgs:
            pass
        p = PushArgs()
        p.client = nome
        p.squad = squad
        p.tom_de_voz = tom_de_voz
        p.historico = historico
        p.oferta = oferta
        p.facts = json.dumps(facts)
        p.source = "kb-sync"

        cmd_push(p)
        print(f"  ✓ {nome} sincronizado.\n")


def cmd_search(args):
    """Busca semântica em todos os contextos de cliente."""
    supabase = supabase_url()
    headers = supabase_headers()

    embedding = gerar_embedding(args.query)

    payload = {
        "query_embedding": embedding,
        "match_threshold": args.threshold,
        "match_count": args.limit,
    }
    if args.client:
        payload["filter_client"] = args.client
    if args.squad:
        payload["filter_squad"] = args.squad

    url = f"{supabase}/rest/v1/rpc/match_client_context"
    resp = requests.post(url, json=payload, headers=headers)

    if resp.status_code != 200:
        print(f"ERRO Supabase ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)

    results = resp.json()
    if not results:
        print("Nenhum resultado encontrado.")
        return

    print(f"Resultados para: '{args.query}'")
    print(f"{'─' * 60}")
    for r in results:
        print(f"\n  {r['client']} (similariade: {r['similarity']:.2f})")
        print(f"  Squad: {r.get('squad', 'N/A')}")
        if r.get("tom_de_voz") and len(r["tom_de_voz"]) > 120:
            print(f"  Tom de Voz: {r['tom_de_voz'][:120]}...")
        elif r.get("tom_de_voz"):
            print(f"  Tom de Voz: {r['tom_de_voz']}")
        if r.get("oferta") and len(r["oferta"]) > 120:
            print(f"  Oferta: {r['oferta'][:120]}...")
        elif r.get("oferta"):
            print(f"  Oferta: {r['oferta']}")


def cmd_list(args):
    """Lista todos os clientes com contexto registrado."""
    supabase = supabase_url()
    headers = supabase_headers()

    url = f"{supabase}/rest/v1/client_context?select=client,squad,source,updated_at&order=client.asc"
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print(f"ERRO Supabase ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)

    results = resp.json()
    if not results:
        print("Nenhum cliente com contexto registrado.")
        return

    print(f"Clientes com contexto ({len(results)}):")
    print(f"{'─' * 60}")
    for r in results:
        print(f"  • {r['client']:25s} | Squad: {r.get('squad', '-'):15s} | {r.get('source', 'N/A'):8s} | {r.get('updated_at', '')[:10]}")


def cmd_delete(args):
    """Remove contexto de um cliente."""
    supabase = supabase_url()
    headers = supabase_headers()

    url = f"{supabase}/rest/v1/client_context?client=eq.{args.client}"
    resp = requests.delete(url, headers=headers)

    if resp.status_code in (200, 204):
        print(f"Contexto de '{args.client}' removido.")
    else:
        print(f"ERRO Supabase ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Contexto de Cliente — fatos exatos do cliente no Supabase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Comandos:
  pull    Puxa contexto de um cliente
  push    Registra/atualiza contexto manualmente
  sync    Sincroniza da KB local para o Supabase
  search  Busca semântica em contextos de clientes
  list    Lista clientes com contexto
  delete  Remove contexto de um cliente

Exemplos:
  python context.py pull --client fips-nautica
  python context.py pull --client fips-nautica --field tom_de_voz
  python context.py push --client x --tom_de_voz "tom formal" --oferta "serviço de SEO"
  python context.py sync --client fips-nautica
  python context.py sync --all
  python context.py search --query "cliente de moda masculina com tom jovem"
  python context.py list
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="Comando")

    # pull
    p_pull = subparsers.add_parser("pull", help="Puxa contexto de um cliente")
    p_pull.add_argument("--client", required=True, help="Nome do cliente")
    p_pull.add_argument("--field", help="Campo específico (tom_de_voz, historico, oferta)")

    # push
    p_push = subparsers.add_parser("push", help="Registra/atualiza contexto")
    p_push.add_argument("--client", required=True, help="Nome do cliente")
    p_push.add_argument("--squad", default="", help="Squad do cliente")
    p_push.add_argument("--tom-de-voz", dest="tom_de_voz", default=None, help="Tom de voz")
    p_push.add_argument("--historico", default=None, help="Histórico")
    p_push.add_argument("--oferta", default=None, help="Oferta")
    p_push.add_argument("--facts", default=None, help="Fatos extras em JSON")
    p_push.add_argument("--source", default="manual", help="Fonte (manual, kb-sync, agent-record)")

    # sync
    p_sync = subparsers.add_parser("sync", help="Sincroniza da KB local")
    p_sync.add_argument("--client", default=None, help="Nome do cliente")
    p_sync.add_argument("--path", default=None, help="Caminho da pasta do cliente")
    p_sync.add_argument("--all", action="store_true", help="Sincronizar todos os clientes")
    p_sync.add_argument("--tom-de-voz", dest="tom_de_voz", default=None, help="Tom de voz (override)")
    p_sync.add_argument("--historico", default=None, help="Histórico (override)")
    p_sync.add_argument("--oferta", default=None, help="Oferta (override)")
    p_sync.add_argument("--facts", default=None, help="Fatos extras em JSON")

    # search
    p_search = subparsers.add_parser("search", help="Busca semântica")
    p_search.add_argument("--query", required=True, help="Texto da busca")
    p_search.add_argument("--client", default=None, help="Filtrar por cliente")
    p_search.add_argument("--squad", default=None, help="Filtrar por squad")
    p_search.add_argument("--threshold", type=float, default=0.7, help="Limiar de similaridade")
    p_search.add_argument("--limit", type=int, default=5, help="Máx. resultados")

    # list
    subparsers.add_parser("list", help="Lista clientes")

    # delete
    p_delete = subparsers.add_parser("delete", help="Remove contexto")
    p_delete.add_argument("--client", required=True, help="Nome do cliente")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "pull": cmd_pull,
        "push": cmd_push,
        "sync": cmd_sync,
        "search": cmd_search,
        "list": cmd_list,
        "delete": cmd_delete,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
