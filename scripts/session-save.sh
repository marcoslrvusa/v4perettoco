#!/bin/bash
# Salva a sessão atual do OpenCode para log/
SESSION_DIR="log"
mkdir -p "$SESSION_DIR"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
TITLE="${1:-agents-hub-apresentacao}"
FILENAME="${SESSION_DIR}/${TIMESTAMP}_${TITLE}.json"

# Tenta exportar sessão
opencode session export --output "$FILENAME" 2>/dev/null || {
  echo '{"title":"agents-hub-apresentacao","timestamp":"'$(date +"%Y-%m-%dT%H:%M:%S")'","artifacts":["agents-hub.html","assets/html/apresentacao-agents-hub.html","docs/agents-hub/LOGICA-APRESENTACAO.md",".opencode/agents/account-orchestrator.md",".opencode/agents/csm-orquestrador.md",".agents/skills/geral-agents-hub/SKILL.md",".claude/skills/geral-agents-hub/SKILL.md"]}' > "$FILENAME"
  echo "Sessão salva (modo fallback): $FILENAME"
}
