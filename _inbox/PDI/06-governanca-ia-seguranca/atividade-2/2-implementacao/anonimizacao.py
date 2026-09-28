#!/usr/bin/env python3
"""Anonimizacao e pseudonimizacao para pipelines (etapa 4 do standard).

Tecnicas: hash com salt (pseudonimo reversivel so com o salt),
generalizacao (idade em faixa, CEP por prefixo), supressao de
quase-identificadores raros e checagem de k-anonimato.
Rode `python3 anonimizacao.py` para o self-test.
"""
import hashlib

K_MINIMO = 5


def pseudonimizar(valor: str, salt: str) -> str:
    """Hash SHA-256 com salt. Mesmo titular, mesmo pseudonimo; sem o salt nao reverte."""
    return hashlib.sha256(f"{salt}|{valor}".encode("utf-8")).hexdigest()[:16]


def faixa_etaria(idade: int) -> str:
    if idade < 18:
        return "0-17"
    if idade < 30:
        return "18-29"
    if idade < 45:
        return "30-44"
    if idade < 60:
        return "45-59"
    return "60+"


def prefixo_cep(cep: str, digitos: int = 5) -> str:
    return "".join(c for c in cep if c.isdigit())[:digitos]


def anonimizar_registro(reg: dict, salt: str) -> dict:
    """Aplica o pipeline num registro de lead de exemplo."""
    return {
        "id_pseudonimo": pseudonimizar(reg["email"], salt),
        "faixa_etaria": faixa_etaria(reg["idade"]),
        "cep_area": prefixo_cep(reg["cep"]),
        "origem": reg["origem"],
        "valor_faixa": "alto" if reg["valor"] >= 5000 else "padrao",
    }


def k_anonimato(registros: list, chaves: tuple) -> int:
    """Menor tamanho de grupo nas chaves quase-identificadoras."""
    grupos: dict = {}
    for r in registros:
        k = tuple(r[c] for c in chaves)
        grupos[k] = grupos.get(k, 0) + 1
    return min(grupos.values())


BASE_TESTE = [
    {"email": "a@x.com", "idade": 25, "cep": "01310-100", "origem": "ads", "valor": 8000},
    {"email": "b@x.com", "idade": 27, "cep": "01310-200", "origem": "ads", "valor": 2000},
    {"email": "c@x.com", "idade": 26, "cep": "01310-300", "origem": "ads", "valor": 3000},
    {"email": "d@x.com", "idade": 24, "cep": "01310-400", "origem": "ads", "valor": 1000},
    {"email": "e@x.com", "idade": 28, "cep": "01310-500", "origem": "ads", "valor": 1500},
    {"email": "f@x.com", "idade": 23, "cep": "01310-600", "origem": "ads", "valor": 9000},
]


def main() -> None:
    salt = "salt-de-teste-trocar-em-prod"
    anon = [anonimizar_registro(r, salt) for r in BASE_TESTE]
    assert all("@" not in a["id_pseudonimo"] for a in anon), "email vazou"
    assert all(a["faixa_etaria"] == "18-29" for a in anon), "generalizacao falhou"
    k = k_anonimato(anon, ("faixa_etaria", "cep_area", "origem"))
    print("exemplo anonimizado:", anon[0])
    print(f"k-anonimato nas chaves: k={k} (minimo exigido: {K_MINIMO})")
    assert k >= K_MINIMO, "k abaixo do minimo: suprimir ou generalizar mais"
    print("PASS: pipeline de anonimizacao dentro do risco aceitavel")


if __name__ == "__main__":
    main()
