#!/usr/bin/env python3
"""
gerar_oauth_token.py — Gera refresh_token OAuth2 para Google Ads API.
Execute UMA VEZ por conta Google e salve o token em .env.

Pré-requisitos:
  pip install google-auth-oauthlib

Como obter client_id + client_secret:
  1. console.cloud.google.com → APIs & Services → Credentials
  2. Create OAuth 2.0 Client ID → Desktop App
  3. Baixe o JSON ou copie ID e Secret
"""
import sys, json
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("Execute: pip install google-auth-oauthlib")
    sys.exit(1)

SCOPE = ["https://www.googleapis.com/auth/adwords"]

def main():
    print("=== Gerador de Refresh Token — Google Ads ===\n")
    client_id     = input("Client ID (OAuth): ").strip()
    client_secret = input("Client Secret: ").strip()
    developer_token = input("Developer Token (Google Ads API Center): ").strip()

    config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    tmp = Path("/tmp/gads_oauth_tmp.json")
    tmp.write_text(json.dumps(config))

    flow = InstalledAppFlow.from_client_secrets_file(str(tmp), scopes=SCOPE)
    creds = flow.run_local_server(port=0)
    tmp.unlink()

    print("\n✅ Autenticação concluída!\n")
    print("Adicione em clientes/<cliente>/.env:\n")
    print(f"GOOGLE_ADS_DEVELOPER_TOKEN={developer_token}")
    print(f"GOOGLE_ADS_CLIENT_ID={client_id}")
    print(f"GOOGLE_ADS_CLIENT_SECRET={client_secret}")
    print(f"GOOGLE_ADS_REFRESH_TOKEN={creds.refresh_token}")
    print(f"GOOGLE_ADS_CUSTOMER_ID=<ID-10-digitos-sem-hifens>")
    print(f"# GOOGLE_ADS_LOGIN_CUSTOMER_ID=<MCC-ID-se-usar-conta-gerenciadora>")

if __name__ == "__main__":
    main()
