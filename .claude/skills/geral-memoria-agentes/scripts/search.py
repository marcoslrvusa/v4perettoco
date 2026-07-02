#!/usr/bin/env python3
"""Busca memórias similares na base pgvector do Supabase.

Uso:
  python search.py --query "texto da busca" \
    [--client cliente] [--niche nicho] [--role role] \
    [--task-type tipo] [--threshold 0.7] [--limit 5]

Requer env vars:
  SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY
"""

import argparse
import json
import os
import sys

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


def main():
    parser = argparse.ArgumentParser(description="Busca memórias similares de agentes")
    parser.add_argument("--query", required=True, help="Texto da consulta")
    parser.add_argument("--client", default=None, help="Filtrar por cliente")
    parser.add_argument("--niche", default=None, help="Filtrar por nicho")
    parser.add_argument("--role", default=None, help="Filtrar por papel do agente")
    parser.add_argument("--task-type", default=None, help="Filtrar por tipo de tarefa")
    parser.add_argument("--threshold", type=float, default=0.7, help="Limiar de similaridade (0-1)")
    parser.add_argument("--limit", type=int, default=5, help="Máx. resultados")
    args = parser.parse_args()

    supabase_url = get_env("SUPABASE_URL").rstrip("/")
    service_key = get_env("SUPABASE_SERVICE_KEY")

    embedding = gerar_embedding(args.query)

    payload = {
        "query_embedding": embedding,
        "match_threshold": args.threshold,
        "match_count": args.limit,
    }
    if args.client:
        payload["filter_client"] = args.client
    if args.niche:
        payload["filter_niche"] = args.niche
    if args.role:
        payload["filter_role"] = args.role
    if args.task_type:
        payload["filter_task"] = args.task_type

    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }

    url = f"{supabase_url}/rest/v1/rpc/match_agent_memories"
    resp = requests.post(url, json=payload, headers=headers)

    if resp.status_code != 200:
        print(f"ERRO Supabase ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)

    results = resp.json()
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
