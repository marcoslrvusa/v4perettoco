# DECK PDI: ADRs com Ciclo de Vida (Atividade 2)

## Slide 1: Capa
ADRs: decisões de arquitetura registradas, com ciclo de vida e exemplos reais. Marcos Luciano, FV Marketing / V4 Company, Setembro 2026.

## Slide 2: O problema
"Por que n8n?" Ninguém lembrava. Decisão refeita do zero a cada questionamento, 3 vezes no trimestre.

## Slide 3: O que é um ADR em 1 minuto
Uma decisão por arquivo, 5 seções, 1 página, imutável. O log de ADRs e a memória da arquitetura.

## Slide 4: O que merece ADR
Só o caro de reverter: banco, fila, orquestrador, provedor. Critério: trocar depois custa mais de 1 semana.

## Slide 5: Formato oficial
Título e número, status, contexto com números, decisão, alternativas com motivo de 1 linha, consequências com métrica.

## Slide 6: Ciclo de vida
Proposta, em avaliação, aceita, implementada. Saídas laterais: rejeitada e superada com link do sucessor.

## Slide 7: Exemplo real 1
ADR-001: n8n self-hosted. Descartados fila própria (3 semanas sem UI) e Apps Script (sem log nem retry). Monitor: falha de coleta acima de 5 por cento em 24h.

## Slide 8: Exemplo real 2
ADR-002: Supabase Postgres com `contas`, `coletas` e `erros`. Descartados SQLite (sem concorrência) e planilha (sem integridade). Monitor: fila de erros por dia.

## Slide 9: Regras duras
Número nunca reutilizado, imutável após aceita, uma decisão por arquivo, consequência sempre com métrica.

## Slide 10: Demo ao vivo
Abrir o template, depois ADR-001 e ADR-002. Mostrar como achar o motivo em minutos por busca no repo.

## Slide 11: Métricas
2 ADRs registrados rumo a 6, decisões refeitas de 3 para 0 no trimestre, tempo de resposta de dias para minutos.

## Slide 12: Próximos passos
Criar `docs/adr/` no repo, exigir ADR para decisão cara, revisão anual com dono definido.

## Slide 13: Fechamento
Arquitetura com memória: ninguém recapitula motivo, ninguém refaz decisão. Perguntas.
