# ADR-002: Supabase Postgres como Estado do Orquestrador

- **Status:** Implementada
- **Data:** 2026-04-02
- **Autor:** Marcos Luciano
- **Decisores:** Marcos Luciano, liderança FV Marketing

## Contexto

O estado das coletas morava em abas de planilha editadas a mão: sobrescrita entre operadores, sem histórico e sem como saber qual conta falhou e quando. Com 3 contas novas por mês, a planilha já travava a conciliação semanal de verba.

## Decisão

Usar Supabase Postgres como fonte de estado, com tabelas `contas`, `coletas` e `erros`, acessado por workers e painel via mesma URL de projeto.

## Alternativas consideradas

- SQLite local no worker: simples e sem custo, mas sem acesso concorrente do painel e do n8n.
- Manter planilha: zero obra, mas sem integridade, sem histórico e com edição manual.

## Consequências

- Ganhamos: histórico auditável, acesso concorrente e fila de erros consultável pelo painel.
- Perdemos: dependência de provedor externo e necessidade de políticas de acesso por tabela.
- Vamos monitorar: linhas na fila de erros por dia e tempo médio de resolução.
