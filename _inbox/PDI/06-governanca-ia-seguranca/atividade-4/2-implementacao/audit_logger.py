#!/usr/bin/env python3
"""Logger de auditoria append-only com hash encadeado (etapas 1 e 2 do standard).

Cada evento em JSON Lines carrega ts, ator, acao, alvo, resultado,
detalhe (sem segredo, sem PII bruta) e hash_prev. `verify()` detecta
qualquer edicao ou remocao. Rode `python3 audit_logger.py` para o self-test.
"""
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone

CAMPOS = ("ts", "ator", "acao", "alvo", "resultado")


def _hash(evento: dict) -> str:
    base = json.dumps(evento, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


def registrar(caminho: str, ator: str, acao: str, alvo: str,
              resultado: str, detalhe: dict | None = None) -> dict:
    prev = "GENESIS"
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as f:
            linhas = [ln for ln in f if ln.strip()]
            if linhas:
                prev = json.loads(linhas[-1])["hash"]
    evento = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ator": ator,
        "acao": acao,
        "alvo": alvo,
        "resultado": resultado,
        "detalhe": detalhe or {},
        "hash_prev": prev,
    }
    evento["hash"] = _hash({k: v for k, v in evento.items() if k != "hash"})
    with open(caminho, "a", encoding="utf-8") as f:
        f.write(json.dumps(evento, ensure_ascii=False) + "\n")
    return evento


def verify(caminho: str) -> dict:
    prev = "GENESIS"
    total = 0
    with open(caminho, encoding="utf-8") as f:
        for n, linha in enumerate(f, 1):
            if not linha.strip():
                continue
            ev = json.loads(linha)
            if ev["hash_prev"] != prev:
                return {"ok": False, "linha": n, "motivo": "quebra de encadeamento"}
            if ev["hash"] != _hash({k: v for k, v in ev.items() if k != "hash"}):
                return {"ok": False, "linha": n, "motivo": "conteudo adulterado"}
            prev = ev["hash"]
            total += 1
    return {"ok": True, "eventos": total, "motivo": "cadeia integra"}


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        log = os.path.join(tmp, "audit.jsonl")
        registrar(log, "job:sync-crm", "lead.atualizado", "lead:4821", "ok",
                  {"campos": ["telefone"]})
        registrar(log, "user:marcos", "campanha.pausada", "camp:77", "ok",
                  {"motivo": "orcamento"})
        registrar(log, "guardrail", "saida.bloqueada", "flow:resumo", "bloqueado",
                  {"regra": "injecao-direta"})
        r = verify(log)
        assert r["ok"] and r["eventos"] == 3, r
        print("PASS: cadeia integra com 3 eventos")
        with open(log, "a", encoding="utf-8") as f:
            f.write('{"ts": "x", "hash_prev": "FALSO", "hash": "y"}\n')
        r2 = verify(log)
        assert r2["ok"] is False, r2
        print("PASS: adulteracao detectada na linha", r2["linha"])


if __name__ == "__main__":
    main()
