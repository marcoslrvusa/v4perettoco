# ROTEIRO-DOMINIO: 5 Perguntas que Podem Cair

## 1. ADR nao vira burocracia que ninguem preenche?
Resposta: so se o formato for longo. O nosso tem 5 secoes e 1 pagina, preenchido em minutos. E o filtro ajuda: so decisao cara de reverter ganha ADR, o resto continua em PR normal.

## 2. Por que imutavel? E se tiver erro de digitacao?
Resposta: imutavel no conteudo decidido, nao na ortografia. Correcao posterior entra como adendo datado. Se a decisao mudou de verdade, um ADR novo supera o antigo com link. O historico honesto vale mais que o texto perfeito.

## 3. Quem pode propor e quem aprova?
Resposta: qualquer pessoa propoe, o tech lead move de em avaliacao para aceita apos 1 semana de comentarios. Sem dono e sem prazo o ADR apodrece em proposta eterna.

## 4. Qual a diferenca para documentar no C4?
Resposta: C4 mostra o que existe, ADR mostra por que existe. O diagrama diz que usamos Supabase; o ADR-002 diz por que descartamos SQLite e planilha. Um sem o outro conta metade da historia.

## 5. Como saber se o ADR esta funcionando?
Resposta: duas metricas: decisoes refeitas por falta de registro (meta zero no trimestre) e tempo para achar um motivo (meta minutos). Se alguem ainda pergunta "por que" no chat, falta ADR.
