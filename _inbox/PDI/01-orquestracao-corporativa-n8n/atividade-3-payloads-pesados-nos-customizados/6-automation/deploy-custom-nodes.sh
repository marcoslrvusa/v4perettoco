#!/usr/bin/env bash
# ============================================================
# deploy-custom-nodes.sh — Deploy dos workflows da atividade 3
# PDI A3: Nós customizados / expressões avançadas
#
# USO: bash deploy-custom-nodes.sh [--dry-run]
# ⚠️ NÃO executar antes da homologação da apresentação.
# ============================================================
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKFLOWS_DIR="$BASE_DIR/2-workflows"
DRY_RUN=0

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

if [[ "$DRY_RUN" == "0" ]]; then
  echo "❌ Deploy REAL bloqueado — aguardando homologação."
  echo "   Rode com --dry-run para validar sem publicar."
  exit 1
fi

echo "🔍 DRY-RUN — validando workflows com n8nac..."
for f in "$WORKFLOWS_DIR"/*.workflow.ts; do
  echo "   → $(basename "$f")"
  npx --yes n8nac skills validate "$f"
done

echo
echo "✅ Todos os workflows válidos. Para publicar (após homologação):"
echo "   npx --yes n8nac push \"2-workflows/[CC] NOS - JS Payload Normalizer.workflow.ts\""
echo "   npx --yes n8nac push \"2-workflows/[CC] NOS - Python Payload Enricher.workflow.ts\""
echo "   npx --yes n8nac push \"2-workflows/[CC] NOS - Expressions & Memo Playground.workflow.ts\""
echo
echo "Lembrete: nenhum workflow deve ser publicado antes da homologação."