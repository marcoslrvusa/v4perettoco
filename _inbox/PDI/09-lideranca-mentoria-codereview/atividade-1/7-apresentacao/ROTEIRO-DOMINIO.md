# Roteiro de Domínio: Atividade 1, Code Review Efetivo

## Q1: Por que só 7 barreiras? E se passar um defeito fora da lista?
Resposta: lista curta é memorizável e cobre os defeitos caros (lógica, teste, segurança, contrato, CI, dados, tamanho). Defeito raro fora da lista é pego pelo CI, pelo segundo revisor em área crítica ou vira item novo da lista na revisão mensal. Lista exaustiva ninguém lê, e regra ignorada é pior que regra curta.

## Q2: `nit:` não vai acumular dívida cosmética para sempre?
Resposta: em parte, sim, e é tradeoff consciente. A saída é mover estilo para linter e formatter automatizados, não para debate humano. O review cuida do que máquina não pega. Se `nit:` se repete, vira regra de lint em vez de comentário.

## Q3: Teto de 400 linhas não incentiva fracionamento artificial?
Resposta: por isso é norma com justificativa, não trava. Migração e rename legítimos passam com explicação em 2 linhas. O alvo é o PR de feature inchado por preguiça de fatiar, que é a maioria dos casos acima do teto.

## Q4: E quando autor e revisor não entram em acordo?
Resposta: thread com 3+ trocas vira call de 15 min. Sem acordo, o dono da área decide em 1 dia útil e registra contexto, decisão e motivo no PR. O registro impede o mesmo debate no próximo PR.

## Q5: Como evitar que 1 approval vire carimbo?
Resposta: três frentes. CODEOWNERS garante que área crítica tem dono de verdade. Métrica de comentários acionáveis por PR expõe approval vazio sem apontar dedo. E cultura: "LGTM" em PR gigante é tratado como ausência, com conversa direta do líder, não como punição pública.
