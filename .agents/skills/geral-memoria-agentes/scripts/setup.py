#!/usr/bin/env python3
"""Setup automático do pgvector + schema para memória semântica de agentes.

Uso:
  python setup.py

Requer env vars:
  SUPABASE_URL       — URL do projeto Supabase (ex: https://ref.supabase.co)
  SUPABASE_SERVICE_KEY — service_role key (admin)
  SUPABASE_PAT       — Personal Access Token da Supabase (para Management API SQL)

O script:
  1. Habilita pgvector extension
  2. Cria a tabela agent_memories
  3. Cria índices
  4. Cria a função match_agent_memories
  5. Configura RLS e grants

Alternativa manual: cole o conteúdo de scripts/setup/supabase-schema.sql
no SQL Editor do Supabase Dashboard.
"""

import os
import sys

import requests


def get_env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        print(f"ERRO: variável {name} não definida", file=sys.stderr)
        sys.exit(1)
    return val


def main():
    supabase_url = get_env("SUPABASE_URL").rstrip("/")
    service_key = get_env("SUPABASE_SERVICE_KEY")
    pat = os.environ.get("SUPABASE_PAT")

    # Extrai o ref do projeto da URL
    # Formato: https://<ref>.supabase.co
    ref = supabase_url.replace("https://", "").split(".")[0]
    print(f"Projeto Supabase: {ref}")

    # Lê o schema SQL
    schema_path = os.path.join(os.path.dirname(__file__), "setup", "supabase-schema.sql")
    if not os.path.exists(schema_path):
        print(f"ERRO: schema SQL não encontrado em {schema_path}", file=sys.stderr)
        sys.exit(1)

    with open(schema_path) as f:
        sql = f.read()

    # Tenta via Management API SQL endpoint
    if pat:
        print("Usando Management API (automático)...")
        headers = {
            "Authorization": f"Bearer {pat}",
            "Content-Type": "application/json",
        }
        payload = {"query": sql}
        url = "https://api.supabase.com/v1/projects/{}/sql".format(ref)
        resp = requests.post(url, json=payload, headers=headers)

        if resp.status_code == 201:
            print("Setup concluído com sucesso!")
            return
        else:
            print(f"Management API falhou ({resp.status_code}): {resp.text}", file=sys.stderr)

    # Fallback: via service_role key + REST SQL (se disponível)
    print("Tentando via REST API com service_role...")
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }

    # O Supabase REST API permite SQL bruto via /rest/v1/rpc/
    # Mas a função precisa existir primeiro. Tentamos criar diretamente.

    # Tentativa 1: criar a extensão via SQL query no endpoint de query custom
    # Nota: isso só funciona se houver uma função RPC que aceite SQL
    # Normalmente a Supabase não expõe SQL bruto via REST por segurança.

    # Se chegou aqui, não foi possível executar automaticamente
    print()
    print("=" * 60)
    print("SETUP AUTOMÁTICO NÃO DISPONÍVEL")
    print("=" * 60)
    print()
    print("Para concluir o setup manualmente:")
    print()
    print(f"1. Abra https://supabase.com/dashboard/project/{ref}/sql/new")
    print("2. Copie o conteúdo do arquivo:")
    print(f"   {schema_path}")
    print("3. Cole no SQL Editor e execute")
    print()
    print("Ou configure SUPABASE_PAT (Personal Access Token) e rode de novo:")
    print("  export SUPABASE_PAT='sbp_seu_token_aqui'")
    print("  python setup.py")
    print()

    sys.exit(1)


if __name__ == "__main__":
    main()
