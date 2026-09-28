# ROTEIRO-DOMINIO: 5 Perguntas que Podem Cair

## 1. ADR não vira burocracia que ninguém preenche?
Resposta: só se o formato for longo. O nosso tem 5 seções e 1 página, preenchido em minutos. E o filtro ajuda: só decisão cara de reverter ganha ADR, o resto continua em PR normal.

## 2. Por que imutável? E se tiver erro de digitação?
Resposta: imutável no conteúdo decidido, não na ortografia. Correção posterior entra como adendo datado. Se a decisão mudou de verdade, um ADR novo supera o antigo com link. O histórico honesto vale mais que o texto perfeito.

## 3. Quem pode propor e quem aprova?
Resposta: qualquer pessoa propõe, o tech lead move de em avaliação para aceita após 1 semana de comentários. Sem dono e sem prazo o ADR apodrece em proposta eterna.

## 4. Qual a diferença para documentar no C4?
Resposta: C4 mostra o que existe, ADR mostra por que existe. O diagrama diz que usamos Supabase; o ADR-002 diz por que descartamos SQLite e planilha. Um sem o outro conta metade da história.

## 5. Como saber se o ADR está funcionando?
Resposta: duas métricas: decisões refeitas por falta de registro (meta zero no trimestre) e tempo para achar um motivo (meta minutos). Se alguém ainda pergunta "por que" no chat, falta ADR.
