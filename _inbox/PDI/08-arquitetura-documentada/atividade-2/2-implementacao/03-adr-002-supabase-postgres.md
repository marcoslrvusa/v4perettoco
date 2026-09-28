# ADR-002: Supabase Postgres como Estado do Orquestrador

- **Status:** Implementada
- **Data:** 2026-04-02
- **Autor:** Marcos Luciano
- **Decisores:** Marcos Luciano, lideranca FV Marketing

## Contexto

O estado das coletas morava em abas de planilha editadas a mao: sobrescrita entre operadores, sem historico e sem como saber qual conta falhou e quando. Com 3 contas novas por mes, a planilha ja travava a conciliacao semanal de verba.

## Decisao

Usar Supabase Postgres como fonte de estado, com tabelas `contas`, `coletas` e `erros`, acessado por workers e painel via mesma URL de projeto.

## Alternativas consideradas

- SQLite local no worker: simples e sem custo, mas sem acesso concorrente do painel e do n8n.
- Manter planilha: zero obra, mas sem integridade, sem historico e com edicao manual.

## Consequencias

- Ganhamos: historico auditavel, acesso concorrente e fila de erros consultavel pelo painel.
- Perdemos: dependencia de provedor externo e necessidade de politicas de acesso por tabela.
- Vamos monitorar: linhas na fila de erros por dia e tempo medio de resolucao.
