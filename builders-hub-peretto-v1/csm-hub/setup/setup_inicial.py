"""
setup_inicial.py — Configuração inicial do CSM Hub.

Uso:
  python setup/setup_inicial.py              # valida ambiente
  python setup/setup_inicial.py --instalar-crons  # instala crons
"""
import sys
import subprocess
import argparse
from pathlib import Path

BASE = Path(__file__).parent.parent.resolve()
V4_PATH = BASE.parent / "v4-automations"
PYTHON = sys.executable


def validar_ambiente():
    print("Validando ambiente CSM Hub...")
    print()

    erros = []

    # Verifica v4-automations
    if not V4_PATH.exists():
        erros.append(f"v4-automations não encontrado em {V4_PATH}")
    else:
        print(f"✅ v4-automations encontrado em {V4_PATH}")

    # Verifica .env
    env_file = V4_PATH / "config" / ".env"
    if not env_file.exists():
        erros.append("config/.env não encontrado no v4-automations")
    else:
        conteudo = env_file.read_text()
        campos = ["ANTHROPIC_API_KEY", "GMAIL_SENDER", "EMAIL_COORDENADOR"]
        for campo in campos:
            if campo in conteudo and f"{campo}=..." not in conteudo:
                print(f"✅ {campo} configurado")
            else:
                erros.append(f"{campo} não configurado em .env")

        if "EMAIL_CSM" not in conteudo:
            print("⚠️  EMAIL_CSM não configurado — usando EMAIL_AM como fallback")

    # Verifica clientes.json
    clientes_file = V4_PATH / "config" / "clientes.json"
    if not clientes_file.exists():
        erros.append("config/clientes.json não encontrado")
    else:
        print("✅ clientes.json encontrado")

    # Verifica módulos
    modulos = ["csm-principal", "flag-roi", "flag-churn", "flag-okr", "flag-operacao"]
    for mod in modulos:
        skill = BASE / "modulos" / mod / "SKILL.md"
        if skill.exists():
            print(f"✅ Módulo {mod} completo")
        else:
            erros.append(f"Módulo {mod} incompleto — SKILL.md não encontrado")

    print()
    if erros:
        print(f"❌ {len(erros)} problema(s) encontrado(s):")
        for e in erros:
            print(f"   • {e}")
        print()
        print("Corrija os problemas acima antes de continuar.")
        return False
    else:
        print("✅ Ambiente válido. CSM Hub pronto para ativar.")
        return True


def instalar_crons():
    print("Instalando crons do CSM Hub...")

    crons = [
        f"0 7 * * 4 {PYTHON} {BASE}/automacoes/detector_flags.py >> {BASE}/logs/csm.log 2>&1",
        f"0 20 * * 0 {PYTHON} {BASE}/automacoes/detector_flags.py >> {BASE}/logs/csm.log 2>&1",
    ]

    # Cria pasta de logs
    (BASE / "logs").mkdir(exist_ok=True)

    # Lê crontab atual
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    existing = result.stdout if result.returncode == 0 else ""

    # Remove entradas antigas do CSM Hub
    lines = [l for l in existing.splitlines() if str(BASE) not in l]

    lines.append("")
    lines.append("# V4 CSM Hub — Detector de flags")
    lines.extend(crons)
    lines.append("")

    proc = subprocess.run(
        ["crontab", "-"],
        input="\n".join(lines),
        text=True,
        capture_output=True
    )

    if proc.returncode == 0:
        print("✅ Crons instalados:")
        print("   Quinta 7h  → detector_flags.py")
        print("   Domingo 20h → detector_flags.py")
        print(f"   Logs em: {BASE}/logs/csm.log")
    else:
        print(f"❌ Erro ao instalar crons: {proc.stderr}")


def main():
    parser = argparse.ArgumentParser(description="Setup inicial do CSM Hub")
    parser.add_argument("--instalar-crons", action="store_true")
    args = parser.parse_args()

    ok = validar_ambiente()

    if args.instalar_crons:
        if ok:
            instalar_crons()
        else:
            print("Corrija os erros antes de instalar os crons.")


if __name__ == "__main__":
    main()
