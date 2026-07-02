#!/usr/bin/env python3
"""Registra uma memória de agente na base pgvector do Supabase.

Uso:
  python record.py \
    --content "descrição completa" \
    --summary "título resumido" \
    --client cliente --niche nicho \
    --agent-role role --task-type tipo \
    --strategy "estratégia usada" \
    --result "resultado obtido" \
    [--success-score 8] \
    [--tags '["tag1","tag2"]'] \
    [--metadata '{"chave":"valor"}']

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
    parser = argparse.ArgumentParser(description="Registra memória de agente")
    parser.add_argument("--content", required=True, help="Conteúdo completo da memória")
    parser.add_argument("--summary", default="", help="Resumo/título")
    parser.add_argument("--client", default="", help="Cliente")
    parser.add_argument("--niche", default="", help="Nicho")
    parser.add_argument("--agent-role", default="", help="Papel do agente")
    parser.add_argument("--task-type", default="", help="Tipo de tarefa")
    parser.add_argument("--strategy", default="", help="Estratégia usada")
    parser.add_argument("--result", default="", help="Resultado obtido")
    parser.add_argument("--success-score", type=int, default=0, help="Nota de sucesso (1-10)")
    parser.add_argument("--tags", default="[]", help="Tags em JSON array")
    parser.add_argument("--metadata", default="{}", help="Metadados em JSON object")
    args = parser.parse_args()

    supabase_url = get_env("SUPABASE_URL").rstrip("/")
    service_key = get_env("SUPABASE_SERVICE_KEY")

    # Concatena texto relevante para gerar embedding semântico
    texto_embed = f"{args.summary}\n{args.content}\nCliente: {args.client}\nNicho: {args.niche}\nEstratégia: {args.strategy}\nResultado: {args.result}"
    embedding = gerar_embedding(texto_embed)

    record = {
        "embedding": embedding,
        "content": args.content,
        "summary": args.summary or None,
        "client": args.client or None,
        "niche": args.niche or None,
        "agent_role": args.agent_role or None,
        "task_type": args.task_type or None,
        "strategy": args.strategy or None,
        "result": args.result or None,
        "success_score": args.success_score if args.success_score > 0 else None,
        "tags": json.loads(args.tags),
        "metadata": json.loads(args.metadata),
    }

    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

    url = f"{supabase_url}/rest/v1/agent_memories"
    resp = requests.post(url, json=record, headers=headers)

    if resp.status_code not in (200, 201, 204):
        print(f"ERRO Supabase ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)

    print("Memória registrada com sucesso.")


if __name__ == "__main__":
    main()
