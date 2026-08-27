#!/bin/bash
# ============================================================
# Deploy MarTech — Resiliencia n8n Enterprise V4 (PDI-MARTECH)
# ============================================================
# Uso: bash deploy-martech.sh
#
# ⚠️  NAO RODAR EM PRODUCAO AINDA (aguardando homologacao).
#     Este script valida e publica os workflows.
#     Para homologacao: rodar com --verify apenas.
# ============================================================

set -euo pipefail

DRY_RUN="${1:-}"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORKFLOWS_DIR="$ROOT_DIR/2-workflows"

WORKFLOWS=(
    "[CC] MT Queue Gateway.workflow.ts"
    "[CC] MT - Heavy Payload Processor.workflow.ts"
    "[CC] MT - Queue Worker.workflow.ts"
    "[CC] MT - CRM Sync Observabilidade.workflow.ts"
)

echo "============================================"
echo " Deploy MarTech Resilient - RODE SOMENTE POS-HOMOLOGACAO"
echo "============================================"
echo ""

if [ "$DRY_RUN" = "--validate-only" ]; then
    echo "🔍 Modo validacao (sem push)."
fi

# Step 1: Validate
for wf in "${WORKFLOWS[@]}"; do
    echo "[check] $wf"
    if npx n8nac skills validate "$WORKFLOWS_DIR/$wf" 2>&1 | grep -q "Workflow is valid"; then
        echo "  ✅ $wf: valido"
    else
        echo "  ❌ $wf: FALHA NA VALIDACAO — corrija antes de publicar."
        exit 1
    fi
done

# Step 2: Push (only quando autorizado)
if [ "$DRY_RUN" = "--validate-only" ]; then
    echo ""
    echo "🔍 Validacao concluida. Nada foi publicado."
    exit 0
fi

echo ""
echo "⚠️  PUBLICACAO EM PRODUCAO."
read -p "Confirmar publicacao dos 4 workflows? (somente pos-homologacao) [s/N] " -r
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Cancelado. Nada foi publicado."
    exit 0
fi

for wf in "${WORKFLOWS[@]}"; do
    echo "→ Push $wf..."
    npx n8nac push "$WORKFLOWS_DIR/$wf" --verify && echo "  ✅ Push OK" || echo "  ⚠️  Push falhou (continue manualmente)"
done

# Step 3: Instructions
echo ""
echo "🔧 CONFIGURACAO MANUAL NECESSARIA"
echo "============================================"
echo ""
echo "1. Copy do ID do '[CC] MT - Heavy Payload Processor' (criado acima):"
echo "   → colar em 'ExecuteHeavyPayloadProcessor' do '[CC] MT - Queue Worker'"
echo ""
echo "2. Credenciais (ja devem existir):"
echo "   - Command Center Supabase (nRJEEi2QwVVKIAHY) — usado nos nodes Supabase"
echo ""
echo "3. Schema v3.0 aplicado:"
echo "   → bash run-migration.sh  (ou SQL Editor do Supabase)"
echo ""
echo "4. Publicar (Shift+P) e ativar: Gateway, Worker, Heavy Payload, Observabilidade"
echo ""
echo "5. Teste:"
echo "   curl -X POST https://n8n.fvmarketing.com.br/webhook/mt/gateway \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"queue\":\"crm-sync\",\"object\":\"order\",\"id\":\"test-1\",\"client\":\"demo\"}'"
echo ""
echo "============================================"
echo " Deploy concluido."
echo "============================================"