# Deck PDI: Atividade 1, Code Review Efetivo

## Slide 1: Resumo executivo
Review hoje é loteria: PR gigante passa sem leitura e PR pequeno trava em gosto pessoal. Entrega: política escrita do que barra vs sugere, checklist objetivo, SLA de resposta e template de PR. Efeito esperado: primeira resposta em 8h úteis e retrabalho pós merge de 17% para 6% (meta).

## Slide 2: O problema em números
Tempo mediano de primeira resposta 26h. 38% dos PRs acima de 400 linhas. 17% geram retrabalho em 7 dias. Comentários acionáveis por PR: 1,8. Diagnóstico: sem regra escrita, cada revisor inventa o próprio critério.

## Slide 3: O que barra o merge
7 barreiras: lógica errada, falta de teste, falha de segurança básica, quebra de contrato, CI vermelho, vazamento de dados, PR gigante sem justificativa. Todo o resto é sugestão. Barreira curta funciona porque é memorizável.

## Slide 4: O que é só sugestão
Estilo, nome "melhor", refatoração opcional, micro performance sem evidência. Prefixos `nit:` e `sugestão:` sinalizam que não bloqueia. Sugestão sem motivo pode ser ignorada sem culpa.

## Slide 5: SLA de resposta
Padrão 8h úteis, urgente 2h com label. Quem não atende reatribui no dia. Autor responde tudo em 1 dia útil. SLA é de resposta, não de merge, porque cada um só pode ser cobrado pelo que controla.

## Slide 6: Tamanho de PR
Teto de 400 linhas como norma com justificativa, não trava técnica. Fatiar por refatoração antes de comportamento. PR pequeno revisa em 20 min; PR de 900 linhas ninguém lê de verdade.

## Slide 7: Checklist objetivo
6 blocos: corretude, testes, segurança e dados, contrato, legibilidade e veredito em 3 vias. Checklist no PR elimina "esqueci de olhar" e padroniza o rigor entre revisores.

## Slide 8: Etiqueta de comentário
Formato gravidade + fato + motivo + sugestão. Exemplos de ruim vs bom para SQL injection, dúvida de retry e nit de nome. Thread com 3+ trocas vira call de 15 min; sem acordo decide o dono da área em 1 dia.

## Slide 9: Papéis e CODEOWNERS
Autor descreve e responde tudo. Revisor lê de verdade e dá veredito claro. Áreas críticas (pagamento, dados, auth, infra) exigem dono da área e 2 approvals; resto, 1 approval.

## Slide 10: Métricas de sucesso
Resposta 26h para 8h (meta). PRs grandes 38% para 10% (meta). Retrabalho 17% para 6% (meta). Comentários acionáveis 1,8 para 3,0 (meta). Revisão semanal pelo líder nos primeiros 2 meses.

## Slide 11: Tradeoffs assumidos
Barreira curta vs exaustiva. Sugestão não bloqueia. Teto como norma, não trava. SLA de resposta, não de merge. 2 revisores só onde o blast radius justifica.

## Slide 12: Rollout em 3 passos
Semana 1: template de PR e checklist nos 3 repos de maior movimento. Semana 2: CODEOWNERS + proteção de branch. Semanas 3 a 6: medir e ajustar SLA com o time.

## Slide 13: Próximos passos e pedido
Pedir ao time: adotar o checklist já no próximo PR e reatribuir quando não der para cumprir o SLA. Pedir à gestão: bancar 1 approval obrigatório e 2 em área crítica. Fechamento: review previsível destrava entrega e forma gente sênior em código real.
