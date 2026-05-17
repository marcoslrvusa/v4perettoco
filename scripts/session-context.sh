#!/usr/bin/env bash
# Carrega contexto de uma sessão anterior salva em log/
# Uso: ./scripts/session-context.sh <arquivo.json>
# Retorna um resumo formatado para usar como contexto

set -euo pipefail

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Arquivo não encontrado: $FILE"
  exit 1
fi

python3 -c "
import json, sys

with open('$FILE') as f:
    data = json.load(f)

info = data.get('info', {})
msgs = data.get('messages', [])

title = info.get('title', 'Untitled')
created = info.get('created', 0)
model = info.get('model', info.get('provider', 'unknown'))

from datetime import datetime
ts = datetime.utcfromtimestamp(created / 1000) if created > 0 else datetime.utcnow()

print(f'=== Sessão Anterior ===')
print(f'Título: {title}')
print(f'Data:   {ts.strftime(\"%Y-%m-%d %H:%M:%S\")}')
print(f'Modelo: {model}')
print(f'Msgs:   {len(msgs)}')
print()

# Extrair resumo: as mensagens do usuário (role=user ou parts com user)
user_msgs = []
assistant_msgs = []
for m in msgs:
    parts = m.get('parts', [])
    role = m.get('info', {}).get('role', '')
    if not role:
        # Try to infer from parts
        for p in parts:
            if isinstance(p, dict) and p.get('type') == 'text':
                text = p.get('text', '')[:300]
                if m.get('info', {}).get('isUser', False):
                    user_msgs.append(text)
                else:
                    assistant_msgs.append(text)

# Print a conversation summary
if user_msgs:
    print('--- Principais perguntas/tarefas do usuário ---')
    for i, msg in enumerate(user_msgs[-5:], 1):
        print(f'{i}. {msg}')
        print()

if assistant_msgs:
    print('--- Principais respostas/entregas ---')
    for i, msg in enumerate(assistant_msgs[-3:], 1):
        print(f'{i}. {msg}')
        print()
" 2>/dev/null
