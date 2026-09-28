# Roteiro de domínio: Pipeline de Testes Automatizados (Unit/Integration/E2E) com 80% de Cobertura

Estudo para defesa presencial da atividade: 5 perguntas de coordenador com respostas curtas, mais 10 perguntas adversárias com resposta desenvolvida. A ordem de estudo sugerida e linear: comece pelas cinco rápidas para fixar a linguagem, depois ataque as adversárias, que pedem número, dono e caminho de recuperação em vez de opinião.

## 1. Por que 3 camadas em vez de só unitários mockados?

Porque unitário sozinho é rápido mas cego a integração, então a estratégia soma unitário para lógica pura, integração com DB efêmero para ports e E2E só no happy path.

## 2. Como o gate de 80 por cento bloqueia o merge na prática?

Com pytest --cov=src --cov-fail-under=80 no CI como required check: cobertura abaixo de 80 por cento falha o pipeline e o PR não mergeia.

## 3. Por que o E2E fica em stage separado com retry?

Porque E2E é lento e mais instável, então roda separado com retry para não travar o merge enquanto unit e integração seguram o gate em menos de 3 min.

## 4. O que significam as metas de 90 por cento, 80 por cento e menos de 1 por cento?

Unitário mira 90 por cento na lógica pura, integração mira 80 por cento nos ports com DB efêmero, e flaky rate fica abaixo de 1 por cento com retry de 1 vez e isolamento.

## 5. Qual comando valida a entrega localmente?

pytest --cov=src --cov-fail-under=80, que reproduz o gate do CI em qualquer máquina antes do push.

## Perguntas adversariais de coordenador

## 6. Por que 80 por cento e não 90 ou 100?

Porque 80 por cento é o ponto em que o gate passa a capturar regressão real sem obrigar a testar código defensivo e morto que não traz redução de defeito na mesma proporção do custo de manutenção. 100 por cento força teste para cada linha de guarda e log, infla a suíte e cria teste que só verifica que a linguagem funciona. 90 por cento fica como meta da camada unitária, onde o teste é barato. A decisão fica registrada no ADR-022, e mudar o teto exige decisão nova, nunca pressa de merge.

## 7. Quanto custa manter essa pipeline?

Custo dividido em dois: implantação única e execução recorrente. A implantação está estimada em 21 h (meta) entre configuração, camada unitária, camada de integração, workflow e documentação. A execução recorrente é o tempo do job no CI, orçado em menos de 3 min por pull request no caminho crítico. **Exemplo numérico (parâmetros declarados):** 2 vCPU por 2 min de execução, 4 vCPU·min por pull request, 50 pull requests por semana, total de 200 vCPU·min semanais. A conta é método, não medição da plataforma.

## 8. Quem decide mudar o teto de cobertura?

A coordenação técnica, por decisão registrada como ADR, nunca o autor de um pull request em particular. Na prática: quem decide é quem responde pela qualidade do repositório; quem implementa é o autor do change; quem valida é o revisor, conferindo que a mudança de teto veio com justificativa. Se o teto virar variável ajustável por branch, o gate deixa de ser regra e vira sugestão.

## 9. E se o gate cair no meio da noite, o que se faz?

O main fica com check vermelho e nenhum merge novo entra até a correção. O runbook manda: (1) confirmar se é defeito de teste ou queda real de cobertura; (2) se for defeito de teste, corrigir o teste ou reverter o último commit com `git revert`; (3) se for queda real de cobertura, o merge que causou a queda é revertido, não o teto. Ninguém baixa o teto às 3 h da manhã. Rollback completo do gate é reverter o commit que alterou `pytest.ini`, uma mudança comum versionada.

## 10. Qual o SLO desta entrega?

Três SLIs com janela declarada: cobertura global maior ou igual a 80 por cento, medida a cada execução; tempo do gate de unit mais integração abaixo de 3 min, medido na mediana semanal; taxa de teste instável abaixo de 1 por cento, calculada sobre as execuções da semana. Ao estourar: cobertura, bloqueia merge; tempo, paraleliza e ajusta fixture; flaky, isola e corrige a causa, sem adicionar retry novo.

## 11. Como você prova que o gate realmente funciona?

Com um teste negativo proposital: comentar um teste, rodar o mesmo comando do CI e observar código de saída diferente de zero com a lista de linhas faltantes. Prova dupla: (a) o caso verde com cobertura atingida retorna 0; (b) o caso com lacuna retorna 1. Se qualquer um dos dois resultados divergir, o gate não é confiável. Essa prova roda localmente e é reproduzida no Passo 9 do roteiro de demo.

## 12. Qual o anti-padrão mais perigoso desta estratégia?

Cobertura alta com teste vazio, o que a literatura chama de contabilidade de cobertura. Um teste sem asserção ou com asserção sobre implementação derruba o número e não protege nada. A defesa é dupla: revisão de código olhando a qualidade do teste, não só o percentual, e mutation testing nos módulos núcleo, medindo se o teste falharia se o código mudasse. **Exemplo numérico:** 200 mutantes gerados, 170 mortos pela suíte, mutation score de 85 por cento, indicando que 15 por cento das mutações passariam despercebidas.

## 13. Qual a alternativa mais barata e o que ela deixa para trás?

A alternativa mais barata é manter só o lint, que já existe, somado à revisão humana. Custo praticamente zero. Deixa para trás exatamente o que a atividade endereça: detecção de regressão de comportamento. O lint não vê que a mudança de parser quebrou a tool, e a revisão humana, por mais cuidadosa, é probabilística e não bloqueia nada por regra. A conta: zero de custo fixo contra horas de validação manual por release e regressão frequente em produção.

## 14. O que você deixaria para trás se tivesse que cortar metade do escopo?

Cortaria o E2E e manteria unitário, integração e o gate. Motivo: o E2E é a camada mais cara e mais instável, e as duas camadas rápidas já capturam a maior parte da regressão nos cerca de 30 módulos. Também deixaria o mutation testing para depois, por ser contínuo e não ser pré-condição do gate. Não cortaria o `branch = true`, porque sem ele a medição mente sobre ramos não testados.

## 15. Como isso se conecta ao negócio?

O projeto tem cerca de 30 módulos Python mais os JS, o CI só roda lint e refactor de prompt ou tool injeta regressão em produção. **Exemplo numérico (parâmetros declarados):** validação manual de 8 h por release, duas releases por semana, quatro semanas, total de 64 h por mês em validação que não deixa ativo. Com o gate, esse tempo vira minutos de leitura de resultado e horas de construção de testes, que continuam protegendo depois de pagas. O impacto direto: regressão de frequente para rara, com flaky abaixo de 1 por cento e feedback em menos de 3 min.
