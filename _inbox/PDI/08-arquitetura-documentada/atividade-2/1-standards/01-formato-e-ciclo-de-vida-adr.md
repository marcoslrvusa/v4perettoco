# Formato e Ciclo de Vida do ADR

## 1. O que merece ADR

So decisao arquiteturalmente relevante: troca cara de reverter (banco, fila, orquestrador, provedor), escolha entre alternativas reais e decisao que futuros devs vao questionar. Bugfix, estilo de codigo e configuracao trivial nao ganham ADR.

## 2. Formato oficial (5 secoes, 1 pagina)

1. **Titulo e numero**: `ADR-003: Fila de erros no Supabase em vez de planilha`.
2. **Status**: Proposta, Em avaliacao, Aceita, Implementada, Rejeitada ou Superada (com link do sucessor).
3. **Contexto**: situacao e forcas em jogo, com numeros quando houver (volume, custo, prazo).
4. **Decisao e alternativas**: o que foi escolhido e o que foi descartado, com motivo de uma linha por alternativa.
5. **Consequencias**: o que ganhamos, o que perdemos e o que vamos monitorar.

## 3. Ciclo de vida

| Status | Significado | Quem move |
|--------|-------------|-----------|
| Proposta | Rascunho aberto para comentario, prazo de 1 semana | Autor |
| Em avaliacao | Time discutindo, alternativas na mesa | Tech lead |
| Aceita | Decisao tomada, falta implementar | Tech lead |
| Implementada | Codigo e docs refletem a decisao | Autor |
| Rejeitada | Descartada com motivo registrado | Tech lead |
| Superada | Trocada por ADR novo (link obrigatorio) | Autor do novo ADR |

## 4. Regras duras

- Arquivo: `docs/adr/NNNN-titulo-curto.md`, numero nunca reutilizado.
- Imutavel apos Aceita: correcao so por adendo datado ou ADR sucessor.
- Uma decisao por ADR. Dois assuntos, dois arquivos.
- Consequencias sempre trazem o que monitorar (metrica ou alerta), nunca so texto.
