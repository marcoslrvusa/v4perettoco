#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT_DIR/log"
SESSION_ID="${1:-}"

if [ -z "$SESSION_ID" ]; then
  SESSION_ID=$(opencode session list --format json 2>/dev/null | python3 -c "
import sys, json
sessions = json.load(sys.stdin)
if sessions:
    print(sessions[0]['id'])
" 2>/dev/null || true)
fi

if [ -z "$SESSION_ID" ]; then
  echo "Nenhuma sessão encontrada."
  exit 1
fi

TITLE=$(opencode session list --format json 2>/dev/null | python3 -c "
import sys, json
sessions = json.load(sys.stdin)
for s in sessions:
    if s['id'] == '$SESSION_ID':
        title = s.get('title', 'untitled').replace('/', '_').replace(' ', '_')
        from datetime import datetime
        ts = s.get('created', 0) / 1000
        print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S') + '_' + title)
        break
" 2>/dev/null || echo "unknown")

FILENAME="$LOG_DIR/$TITLE.json"

opencode export "$SESSION_ID" --sanitize 2>/dev/null > "$FILENAME"

echo "Sessão salva: $FILENAME"
echo "ID: $SESSION_ID"
wc -c "$FILENAME" | awk '{print "Tamanho: " $1 " bytes"}'
