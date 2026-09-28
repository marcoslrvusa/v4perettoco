# Roteiro de domínio: Estudo de Design Patterns aplicados ao ecossistema

Estudo para defesa presencial da atividade: 5 perguntas de coordenador com respostas curtas.

O roteiro traz 12 perguntas no total: as cinco originais mais as adversariais de praxe, por que
não usar a alternativa mais barata, quanto custa, quem decide, o que acontece se cair no meio da
noite, qual é o SLO, como se prova que funciona, o que ficaria para trás e qual o impacto em
horas e em reais.

As respostas abaixo são deliberadamente curtas. Em defesa, a resposta curta é entregue primeiro e
só depois vem a evidência (arquivo, seção ou número), para não depender de material aberto na
hora.

## 1. Onde cada padrão entra na operação?

Adapter no CRM e LLM externos, Strategy no roteamento de modelo e Observer nos eventos de domínio como e-mail e estoque.

Evidência: `1-standards/DESIGN-PATTERNS-NOTES.md`, seção 3, e o diagrama de arquitetura no
README da atividade.

## 2. Por que Singleton para clients foi rejeitado?

Porque cria estado global oculto e dificulta teste, então a decisão ADR-024 troca por injeção de dependência com fakes nos testes.

Evidência: linha do Singleton na tabela do ADR-024 e o anti-padrão correspondente na seção 7 do
standard.

## 3. Como plugar um fornecedor novo sem mexer no core?

Criando um adapter que implementa o port existente, como PayPalAdapter ou StripeAdapter, e registrando na factory sem recompilar regra de negócio.

Evidência: sequência de comandos no `DEMO-SCRIPT.md`, passos 5 a 9.

## 4. Como a entrega é validada?

Rodando patterns_demo.py, abrindo PR com Adapter em 1 CRM piloto e aplicando o checklist de padrões no template de PR.

Evidência: critério de aceite por item na seção de Validação do README.

## 5. Como evitar over-engineering com padrões?

Aplicando padrão só onde há variação real e com code review que cobra valor entregue, não quantidade de padrões.

Evidência: não-escopo na seção 1 do standard, item de reprovação no checklist de adesão.

## 6. Por que não usar uma biblioteca de integração pronta?

Porque ela resolve o formato externo e não resolve o nosso modelo interno: a dependência entraria no caminho crítico, ganharíamos mais uma API para aprender e continuaríamos sem contrato próprio para teste. A indireção que interessa é a nossa port, porque é o que permite fake em pull request. Quando a biblioteca cobrir um padrão que já estamos reinventando com contrato estável, aí sim ela vira candidata, documentada em ADR próprio.

## 7. Quanto custa e quem decide?

**Exemplo numérico:** o plano soma 8 horas de leitura da trilha, 4 de padronização do checklist, 12 do piloto de Adapter em 1 handler de CRM, 6 de Strategy, 5 de deck, demo e roteiro e 3 de revisão com a coordenação, totalizando 38 horas. Com valor hora de R$ 60 (parâmetro declarado apenas para ensinar a conta), o custo é 38 x 60 = R$ 2.280. Quem decide: o dev propõe, o revisor de arquitetura aprova o ADR, a coordenação do PDI aprova a alocação das horas. Nenhuma hora extra entra sem essa aprovação.

## 8. E se cair no meio da noite, o que se faz?

Runbook da seção de Operação: checar taxa de erro e p95 por adapter, localizar o fornecedor degradado e desligá-lo por feature flag, mantendo o restante do fluxo de pé. O rollback do piloto é a flag, não deploy reverso. Depois, postmortem sem culpa em até 2 dias úteis com ação rastreável. Ponto que não se negocia: falha de um observador não derruba o emissor, então um erro de e-mail nunca cancela a confirmação de um pedido.

## 9. Qual é o SLO desta solução?

Três SLI com meta e janela: disponibilidade do caminho crítico atrás de adapter >= 99,5 por cento em base mensal (meta), latência p95 do handler com adapter <= 800 ms em base diária (meta), e taxa de erro do núcleo causada por terceiro <= 1 por cento em base semanal (meta). Orçamento de erro: 0,5 por cento de indisponibilidade em 30 dias dá 3,6 horas, das quais 1 hora por mês fica alocada ao risco de terceiro (meta). Se o risco estourar a fatia, desliga-se o fornecedor e negocia-se SLA com o parceiro, não se aumenta o orçamento em silêncio.

## 10. Como você prova que funciona?

Quatro provas, em ordem de força: o script `patterns_demo.py` roda sem rede e termina com código de saída zero; o teste de tabela cobre cada entrada documentada da factory; o teste de arquitetura falha se aparecer import de SDK no núcleo; e o primeiro onboarding real pós-piloto é medido de ponta a ponta, com dias entre kickoff e primeiro evento em produção. Até existir a quarta prova, tudo o que é número na apresentação é (meta), e eu digo isso em voz alta antes que alguém pergunte.

## 11. Qual a alternativa mais barata?

Escrever if e else conforme o caso aparecer. Ela é mais barata no mês zero e mais cara depois: cada fornecedor nova $C$ ramificações, a chance de erro por mudança cresce com $1-(1-p)^{k}$ e a revisão precisa inspecionar mais pontos. A conta está na seção de matemática: 24 pontos de toque contra 10, uma redução de 58,3 por cento (Exemplo numérico). A alternativa barata de verdade é não aplicar padrão onde não há variação: é o que o não-escopo do standard garante.

## 12. O que você deixaria para trás?

Deixaria para depois o broker de mensagens: o piloto usa bus in-memory e síncrono de propósito, porque precisa provar desacoplamento de código antes de desacoplamento de infraestrutura. Deixaria também os padrões criacionais além da factory simples, e a refatoração dos demais módulos de integração até fechar o piloto de CRM. Se o bus in-memory virar gargalo ou a ordem entre eventos virar requisito de negócio, aí o broker sobe para a frente da fila, com ADR próprio.

## 13. Qual o impacto no negócio, em horas e em reais?

O onboarding de fornecedor sai da ordem de semanas para até 2 dias atrás de adapter testado (meta). **Exemplo numérico:** com 4 fornecedores por ano, 10 dias economizados por fornecedor e R$ 350 por dia-dev (parâmetros declarados apenas para ensinar a conta), o ganho é $4 \times 10 \times 350 = \text{R\$ } 14.000$ por ano de esforço devolvido ao roadmap, contra R$ 2.280 de custo do plano de 38 horas, com payback no primeiro fornecedor do ano. Além do dinheiro: menos ponto de falha duplicado significa menos incidente fora do horário comercial, e revisão com vocabulário comum encurta o ciclo de pull request. Se a pergunta vier complementada por "e quem responde se o padrão não for seguido", a resposta é: o autor do pull request pela variação que ele introduziu, o revisor de arquitetura pela adesão ao ADR-024, e a coordenação pela prioridade quando a adesão colidir com prazo de produto. O checklist no template de PR é o instrumento que transforma essa resposta em obrigação registrada, e não em conversa de revisão.
