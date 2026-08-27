#!/bin/bash
# ============================================================
# Run Migration - Schema v2.x → v3.0 (MarTech) Supabase
# ============================================================
# Uso: bash run-migration.sh
#
# Executa o schema v3.0 (mt_*) no Supabase via psql.
# Necessario: SUPABASE_URL + SUPABASE_SERVICE_KEY configurados
# em variaveis de ambiente ou .env.
#
# ⚠️ ADITIVO: nao altera tabelas/views do schema v2.x (error_*).
# ============================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCHEMA_FILE="$ROOT_DIR/3-supabase/supabase-schema-v3.sql"

ENV_FILE="$ROOT_DIR/../projetos/infraestrutura/n8n/.env"
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
fi

SUPABASE_URL="${SUPABASE_URL:-}"
SUPABASE_SERVICE_KEY="${SUPABASE_SERVICE_KEY:-}"

echo "============================================"
echo " Migracao Supabase — Schema v3.0 (MarTech)"
echo "============================================"
echo ""

if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_SERVICE_KEY" ]; then
    echo "❌ SUPABASE_URL ou SUPABASE_SERVICE_KEY nao configurados."
    echo ""
    echo "Configure no .env ou exporte as variaveis:"
    echo "  export SUPABASE_URL=https://seuprojeto.supabase.co"
    echo "  export SUPABASE_SERVICE_KEY=sua_service_role_key"
    echo ""
    echo "Ou rode manualmente no SQL Editor do Supabase:"
    echo "  https://supabase.com/dashboard/project/gswzuzetverulcgzhynb"
    echo "  → SQL Editor → colar conteudo de $SCHEMA_FILE"
    exit 1
fi

echo "Executando schema v3.0 (aditivo)..."
echo "URL: $SUPABASE_URL"
echo ""

PGHOST=$(echo "$SUPABASE_URL" | sed 's|https://||' | sed 's|\.supabase\.co.*||').supabase.co

PGPASSWORD="$SUPABASE_SERVICE_KEY" psql \
    -h "$PGHOST" \
    -p 5432 \
    -d postgres \
    -U postgres \
    -f "$SCHEMA_FILE" 2>&1

echo ""
echo "✅ Migracao concluida."
echo ""
echo "Verificar tabelas criadas:"
echo "  SELECT table_name FROM information_schema.tables"
echo "  WHERE table_schema = 'public'"
echo "    AND table_name LIKE 'mt_%';"
echo ""
echo "Verificar views criadas:"
echo "  SELECT relname FROM pg_class"
echo "  WHERE relkind = 'v' AND relname LIKE 'vw_mt_%';"