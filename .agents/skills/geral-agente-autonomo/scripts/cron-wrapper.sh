#!/bin/bash
# ==============================================================
# Agent Orchestra — Cron Wrapper
# ==============================================================
# Instalação (como root):
#   cp cron-wrapper.sh /usr/local/bin/agent-orchestra-cron
#   chmod +x /usr/local/bin/agent-orchestra-cron
#
#   cat > /etc/cron.d/agent-orchestra << 'EOF'
#   # Agent Orchestra - processa fila a cada 15 minutos
#   */15 * * * * root /usr/local/bin/agent-orchestra-cron >> /var/log/agent-orchestra.log 2>&1
#   EOF
#
#   systemctl restart cron
# ==============================================================

set -euo pipefail

# Configuração
ORCHESTRATOR_DIR="/workspace"
ORCHESTRATOR_SCRIPT="$ORCHESTRATOR_DIR/agent-orchestrator.py"
LOG_FILE="/var/log/agent-orchestra.log"
MAX_EXECUTIONS=5          # Máx itens por ciclo
LOCK_FILE="/tmp/agent-orchestra.lock"

# Carrega env vars do sistema
if [ -f /etc/environment ]; then
    set -a; source /etc/environment; set +a
fi
if [ -f "$ORCHESTRATOR_DIR/.env" ]; then
    set -a; source "$ORCHESTRATOR_DIR/.env"; set +a
fi

# Verifica pré-requisitos
if [ ! -f "$ORCHESTRATOR_SCRIPT" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERRO: $ORCHESTRATOR_SCRIPT não encontrado"
    exit 1
fi

if [ -z "${SUPABASE_URL:-}" ] || [ -z "${SUPABASE_SERVICE_KEY:-}" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERRO: SUPABASE_URL e SUPABASE_SERVICE_KEY obrigatórios"
    exit 1
fi

# Lock para evitar execução concorrente
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] AVISO: Outra execução em andamento. Pulando."
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Agent Orchestra Cron — Iniciando"

# Processa até MAX_EXECUTIONS itens
for i in $(seq 1 $MAX_EXECUTIONS); do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Ciclo $i de $MAX_EXECUTIONS..."

    # Verifica se há pendentes antes de chamar o script
    PENDING=$($ORCHESTRATOR_SCRIPT queue 2>/dev/null | wc -l)
    if [ "$PENDING" -le 2 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fila vazia. Finalizando."
        break
    fi

    cd "$ORCHESTRATOR_DIR"
    python3 "$ORCHESTRATOR_SCRIPT" process
    EXIT_CODE=$?

    if [ $EXIT_CODE -ne 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERRO: process exit code $EXIT_CODE"
        break
    fi
done

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Agent Orchestra Cron — Concluído"
flock -u 9
