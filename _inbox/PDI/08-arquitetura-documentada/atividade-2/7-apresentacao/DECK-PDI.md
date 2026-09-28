# DECK PDI: ADRs com Ciclo de Vida (Atividade 2)

## Slide 1: Capa
ADRs: decisoes de arquitetura registradas, com ciclo de vida e exemplos reais. Marcos Luciano, FV Marketing / V4 Company, Setembro 2026.

## Slide 2: O problema
"Por que n8n?" Ninguem lembrava. Decisao refeita do zero a cada questionamento, 3 vezes no trimestre.

## Slide 3: O que e um ADR em 1 minuto
Uma decisao por arquivo, 5 secoes, 1 pagina, imutavel. O log de ADRs e a memoria da arquitetura.

## Slide 4: O que merece ADR
So o caro de reverter: banco, fila, orquestrador, provedor. Criterio: trocar depois custa mais de 1 semana.

## Slide 5: Formato oficial
Titulo e numero, status, contexto com numeros, decisao, alternativas com motivo de 1 linha, consequencias com metrica.

## Slide 6: Ciclo de vida
Proposta, em avaliacao, aceita, implementada. Saidas laterais: rejeitada e superada com link do sucessor.

## Slide 7: Exemplo real 1
ADR-001: n8n self-hosted. Descartados fila propria (3 semanas sem UI) e Apps Script (sem log nem retry). Monitor: falha de coleta acima de 5 por cento em 24h.

## Slide 8: Exemplo real 2
ADR-002: Supabase Postgres com `contas`, `coletas` e `erros`. Descartados SQLite (sem concorrencia) e planilha (sem integridade). Monitor: fila de erros por dia.

## Slide 9: Regras duras
Numero nunca reutilizado, imutavel apos aceita, uma decisao por arquivo, consequencia sempre com metrica.

## Slide 10: Demo ao vivo
Abrir o template, depois ADR-001 e ADR-002. Mostrar como achar o motivo em minutos por busca no repo.

## Slide 11: Metricas
2 ADRs registrados rumo a 6, decisoes refeitas de 3 para 0 no trimestre, tempo de resposta de dias para minutos.

## Slide 12: Proximos passos
Criar `docs/adr/` no repo, exigir ADR para decisao cara, revisao anual com dono definido.

## Slide 13: Fechamento
Arquitetura com memoria: ninguem recapitula motivo, ninguem refaz decisao. Perguntas.
