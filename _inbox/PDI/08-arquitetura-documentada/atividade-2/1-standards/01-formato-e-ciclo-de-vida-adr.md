# Formato e Ciclo de Vida do ADR

## 1. O que merece ADR

Só decisão arquiteturalmente relevante: troca cara de reverter (banco, fila, orquestrador, provedor), escolha entre alternativas reais e decisão que futuros devs vão questionar. Bugfix, estilo de código e configuração trivial não ganham ADR.

## 2. Formato oficial (5 seções, 1 página)

1. **Título e número**: `ADR-003: Fila de erros no Supabase em vez de planilha`.
2. **Status**: Proposta, Em avaliação, Aceita, Implementada, Rejeitada ou Superada (com link do sucessor).
3. **Contexto**: situação e forças em jogo, com números quando houver (volume, custo, prazo).
4. **Decisão e alternativas**: o que foi escolhido e o que foi descartado, com motivo de uma linha por alternativa.
5. **Consequências**: o que ganhamos, o que perdemos e o que vamos monitorar.

## 3. Ciclo de vida

| Status | Significado | Quem move |
|--------|-------------|-----------|
| Proposta | Rascunho aberto para comentário, prazo de 1 semana | Autor |
| Em avaliação | Time discutindo, alternativas na mesa | Tech lead |
| Aceita | Decisão tomada, falta implementar | Tech lead |
| Implementada | Código e docs refletem a decisão | Autor |
| Rejeitada | Descartada com motivo registrado | Tech lead |
| Superada | Trocada por ADR novo (link obrigatório) | Autor do novo ADR |

## 4. Regras duras

- Arquivo: `docs/adr/NNNN-titulo-curto.md`, número nunca reutilizado.
- Imutável após Aceita: correção só por adendo datado ou ADR sucessor.
- Uma decisão por ADR. Dois assuntos, dois arquivos.
- Consequências sempre trazem o que monitorar (métrica ou alerta), nunca só texto.
