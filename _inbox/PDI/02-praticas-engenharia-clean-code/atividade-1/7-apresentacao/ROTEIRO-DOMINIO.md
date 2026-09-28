# Roteiro de domínio: Refatoração de Módulo Legado com SOLID e Clean Architecture

Estudo para defesa presencial da atividade: perguntas de coordenador com respostas curtas.

## 1. Por que Clean Architecture foi escolhida e as outras opções rejeitadas?

Porque ela desacopla regra de negócio de DB, e-mail e CRM via ports, permite teste sem infra e o ADR-021 registra hexagonal puro como overhead e manter acoplado como frágil. A escolha não é ideológica: o caso tem quatro dependências de I/O e zero cobertura, então a porta é o menor desenho que resolve os dois problemas ao mesmo tempo. Hexagonal puro pediria simetria de portas que este módulo não usa; manter acoplado transferiria o custo para teste E2E, que é lento e frágil.

## 2. Como o novo serviço elimina o SQL injection do legado?

Troca SQL concatenado por acesso via LeadRepository com consulta parametrizada, então o id da campanha nunca e interpolado na string. No adaptador concreto, o valor vira parâmetro vinculado (`$1`) e o banco trata a fronteira entre dado e sintaxe. O teste de sanidade cobre entrada hostil (apóstrofo, unicode, ponto e vírgula) e falharia se alguém reintroduzisse f-string na consulta.

## 3. O que o shadow de 1 sprint com corte em 0,1 por cento garante?

Garante que o módulo novo rode em paralelo ao legado de 600 linhas por 1 sprint com reconciliação diária, e só assume o tráfego se a divergência ficar abaixo de 0,1 por cento, com rollback por flag. Como 0,1 por cento em base grande ainda gera volume, o corte combina percentual com teto absoluto: no máximo 5 divergências por dia (meta). Exemplo numérico: 40 campanhas de 20.000 leads são 800.000 eventos comparados, e 0,1 por cento seriam 800 divergências, volume suficiente para inviabilizar a migração se depender de triagem manual.

## 4. Como a meta de 85 por cento de cobertura e verificada?

Com testes de porta que usam mocks de Notifier e Repository, cobrindo o serviço sem subir banco nem SMTP, partindo de 0 por cento no legado. A cobertura é gate no CI: pull request abaixo de 85 por cento não faz merge. Como cobertura infla com teste de getter, o segundo sinal é mutação com mutmut: se asserções de regra não morrem quando o operador muda, o teste não vale.

## 5. O que muda de 4 responsabilidades para 1 por classe na prática?

Cada classe passa a ter menos de 45 linhas e um motivo de mudança, então alterar regra de campanha não toca em DB, e-mail ou CRM. Exemplo numérico: antes, a mudança era exposta a 4 de 4 alvos do módulo; depois, a 1 de 14, ou seja, de 100 por cento para 7 por cento do módulo. O custo de mais arquivos é real, mas é pago em revisão, não em incidente.

## 6. E se a refatoração quebrar o envio em produção?

A quebra é detectada antes do envio real, porque o sombra não dispara para o lead. O novo módulo roda em modo de leitura, grava o que faria em tabela de comparação e o legado continua sendo o único que envia. Se a divergência estourar o corte, a flag volta para o legado em minutos, sem deploy, porque o caminho antigo permanece compilado até 2 sprints sem divergência.

## 7. Qual o SLO e o que acontece quando ele estoura?

SLI principal: proporção de campanhas cuja reconciliação diária fecha com zero divergência, meta de 99,9 por cento (meta) em 30 dias, com alerta em até 24 h (meta). SLI complementar: cobertura maior ou igual a 85 por cento como gate. Ao estourar, congela a migração, desliga a flag, abre incidente de severidade 2 e faz postmortem sem culpa em até 5 dias úteis, com obrigação de atualizar o invariante e o teste correspondente.

## 8. Quanto custa e quem decide se vale a pena?

Esforço de 56 h (meta) distribuídas em diagnóstico, refatoração, testes, documentação e sombra. Custo direto: R$ 8.400 (meta) a R$ 150/h (meta). Quem decide é a coordenação técnica com o dono do módulo, porque a decisão muda o custo de manutenção, não só o código. Ponto de equilíbrio (meta): menos de 8 meses, considerando 12 h/mês de remendo (Exemplo numérico) e o custo de um incidente de base grande.

## 9. E se o time não adotar o padrão depois da sua entrega?

Adoção não se sustenta em boletim, se sustenta em ferramenta que reprova. O teste de adesão arquitetural roda no CI e falha o pull request que importar infraestrutura dentro do domínio; o PR template cobre a parte de revisão humana. Enquanto o gate não existir, a meta de adesão é uma promessa; quando o gate existe, a métrica é o percentual de pull requests reprovados na primeira rodada, que é o que mostra se o time está aprendendo.

## 10. Por que não usar biblioteca de injeção de dependência?

Porque o bootstrap tem três linhas de fiação. Um container resolveria um problema que não existe e adicionaria dependência nova num módulo cujo objetivo é reduzir dependência. A regra prática: injeção por construtor enquanto a montagem couber em um arquivo; quando a montagem crescer, aí sim vale container, e a decisão vira um ADR novo.

## 11. Qual a alternativa mais barata que você deixou de fora?

Manter o legado e apenas parametrizar o SQL, com cerca de 4 h de trabalho. Resolve o vetor de injection, que é o risco de segurança mais grave, mas deixa intactos: ausência de transação, falha silenciosa de CRM, 0 por cento de cobertura e blast radius de 4 responsabilidades. A recomendação é registrar essa opção como estabilização de emergência, não como plano, porque ela não muda a probabilidade do próximo incidente.

## 12. O que você deixaria para trás conscientemente?

Refatoração dos adaptadores para padrão de retry idempotente com backoff e jitter, e a reconciliação horária no lugar da diária. Também ficam de fora os testes de contrato automatizados para o adaptador de CRM externo, que dependem de ambiente fornecido pela outra empresa. Tudo isso é backlog consciente com prioridade, não esquecimento, e aparece nos próximos passos do README.

## 13. Pergunta de negócio: qual o impacto em R$ e horas se isso não for feito?

Exemplo numérico: 4 campanhas por dia × 20 dias úteis = 80 campanhas por mês sobem pelo módulo. Se 1 em 80 falhar de forma silenciosa, o módulo gera 1 incidente por mês, cada um com reclamação, remendo manual e reenvio. Com 3 h de remendo (meta) × 2 ocorrências (meta) × 2 pessoas afetadas (meta) = 12 h/mês, ou 1,5 dia útil por mês só de remendo, somadas ao custo de reputação em base de até 80 mil leads. Contra R$ 8.400 (meta) de esforço único, a conta fecha em menos de 8 meses (meta).
