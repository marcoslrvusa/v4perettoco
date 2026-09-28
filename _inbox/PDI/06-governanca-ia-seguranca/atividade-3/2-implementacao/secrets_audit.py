#!/usr/bin/env python3
"""Varredura local de segredos em repos (etapa 4 do standard).

Procura padroes reais de credencial em texto, confere se `.env` e
chaves estao no `.gitignore` e gera relatorio. Nao envia nada para
fora da maquina. Rode `python3 secrets_audit.py [PASTA]` para auditar,
ou sem argumento para o self-test.
"""
import os
import re
import sys
import tempfile

PADROES = {
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_key": re.compile(r"\bsk-(proj-)?[A-Za-z0-9_-]{20,}\b"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    "senha_em_codigo": re.compile(
        r"(?i)(password|passwd|secret|api[_-]?key)\s*[:=]\s*['\"][^'\"]{4,}['\"]"
    ),
}
EXT_PERMITIDAS = {".py", ".js", ".ts", ".json", ".yml", ".yaml", ".env", ".txt", ".md", ".sh"}
IGNORAR_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def auditar(pasta: str) -> dict:
    achados = []
    for raiz, dirs, arqs in os.walk(pasta):
        dirs[:] = [d for d in dirs if d not in IGNORAR_DIRS]
        for nome in arqs:
            if os.path.splitext(nome)[1].lower() not in EXT_PERMITIDAS:
                continue
            caminho = os.path.join(raiz, nome)
            try:
                with open(caminho, encoding="utf-8", errors="ignore") as f:
                    for i, linha in enumerate(f, 1):
                        for rotulo, rx in PADROES.items():
                            if rx.search(linha):
                                achados.append({"arquivo": caminho, "linha": i, "tipo": rotulo})
            except OSError:
                continue
    gitignore = os.path.join(pasta, ".gitignore")
    protegido = False
    if os.path.exists(gitignore):
        with open(gitignore, encoding="utf-8", errors="ignore") as f:
            txt = f.read()
            protegido = ".env" in txt and "*.pem" in txt
    return {"achados": achados, "gitignore_ok": protegido}


def main() -> None:
    if len(sys.argv) > 1:
        rel = auditar(sys.argv[1])
        print(f"achados: {len(rel['achados'])} | .gitignore ok: {rel['gitignore_ok']}")
        for a in rel["achados"]:
            print(f"  {a['tipo']}: {a['arquivo']}:{a['linha']}")
        raise SystemExit(1 if rel["achados"] or not rel["gitignore_ok"] else 0)
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "app.py"), "w") as f:
            f.write('KEY = "AKIAIOSFODNN7EXAMPLE"\nTOKEN = "ghp_abc123abc123abc123ab"\n')
        with open(os.path.join(tmp, ".gitignore"), "w") as f:
            f.write(".env\n*.pem\n*.key\nsecret.txt\n")
        rel = auditar(tmp)
        tipos = {a["tipo"] for a in rel["achados"]}
        assert tipos == {"aws_access_key", "github_token"}, tipos
        assert rel["gitignore_ok"] is True
        print(f"PASS: detectou {sorted(tipos)} e validou .gitignore")


if __name__ == "__main__":
    main()
