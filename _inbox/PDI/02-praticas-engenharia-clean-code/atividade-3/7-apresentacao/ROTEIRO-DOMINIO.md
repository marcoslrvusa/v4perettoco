# Roteiro de domínio: Mapeamento de Domínios com Domain-Driven Design (DDD)

Estudo para defesa presencial da atividade: perguntas de coordenador com respostas curtas, mais as perguntas adversariais e a de negócio que sempre aparecem na banca. Objetivo: responder cada uma em até 40 segundos, com número na mão e sem adjetivo.

## 1. Por que DDD explícito em vez de schema único?

Porque schema único e simples no início mas acopla os 4 squads, enquanto DDD da consistência e linguagem comum com governança explícita. O custo do DDD é previsível: 1 ADR curto e 1 entrada de glossário por contexto novo. O custo do schema único é imprevisível: cada mudança de regra toca 5 pontos (Exemplo numérico), e ninguém consegue prever o efeito cascata antes de quebrar.

## 2. O que muda com bounded contexts e eventos de domínio?

Cada contexto tem seu modelo e os contextos se comunicam por eventos versionados, nunca por tabela compartilhada ou SQL cruzado. Na prática, Campaign deixa de ler a tabela do CRM e passa a reagir a `LeadCreated`. A mudança deixa de ser "atualiza as 5 tabelas" e vira "publica 1 evento", o que derruba a ampliação de mudança de 5 para 1.

## 3. Como o agregado garante consistência?

Só a raiz e referenciada de fora e os filhos não tem identidade pública, então a regra transacional fica num ponto único em vez de espalhada. Comando externo entra pela raiz, a raiz valida a invariante e grava tudo numa transação. Exemplo do código: `Lead.contact()` recusa lead não qualificado lançando `DomainError`, e nenhum caminho do sistema cria `Contact` sem passar por ali.

## 4. Como o mapa e validado antes de virar código?

Em workshop de linguagem ubíqua com Product e 2 squads, validando os agregados contra 3 user stories e só depois gerando os schemas aprovados. Critério de aceite: se a user story só passar com tradução improvisada no código, o glossário está errado. O gate final é a verificação de dependência entre contextos em CI, que bloqueia merge em caso de leitura cruzada.

## 5. Quais são as metas numéricas da atividade?

4 domínios mapeados, 0 modelos duplicados e ao menos 6 eventos de domínio definidos. Além disso, a meta de processo é que 90% das mudanças de regra toquem apenas 1 contexto (meta), medida trimestralmente pelo histórico de revisões.

## 6. Por que não microsserviços agora, se o problema é acoplamento?

Porque o problema é fronteira de modelo, não de deploy. Microsserviço resolve isolamento de processo e custa rede, contrato operacional e observabilidade extra. Se dividirmos os processos antes de dividir o modelo, replicamos o mesmo emaranhado em 4 rede, só que com latência de rede no meio. A ordem é: primeiro fronteira de modelo (nesta atividade), depois, se houver necessidade real de escala independente, a separação de deploy.

## 7. Quem decide quando dois contextos disputam o mesmo conceito?

O dono do contexto onde a regra de negócio vive. Se o conceito tem invariante de transação, ele pertence ao contexto dono daquela regra, e os demais consomem evento. A decisão é registrada no ADR-023 com as alternativas, para não virar discussão eterna. Em empate real, quem sente o custo da mudança paga pela decisão, e o outro contexto apenas assina o contrato.

## 8. E se o barramento cair no meio da noite?

O barramento tem meta de disponibilidade de 99,5% (meta) e as publicações são retidas: o produtor grava o evento e o consumidor reprocessa quando a fila volta. O que não pode acontecer é perder ordem por partição ou duplicar efeito, por isso todo consumidor deduplica por `event_id`. O runbook manda pausar o tópico, corrigir o consumidor e drenar a fila; o acionamento é do dono do barramento, com o dono do contexto consumidor informado.

## 9. Como você prova que o mapa funciona e não virou teoria?

Com três provas executáveis. Primeira: o gate de dependência entre contextos verde em CI, mostrando zero leitura cruzada. Segunda: a razão entre efeitos aplicados e eventos publicados igual a 1,02 no máximo, o que prova deduplicação. Terceira: a métrica de ampliação de mudança caindo de 5 para 1 no histórico de revisões. Se alguma prova não existe, o mapa é slide, não é arquitetura.

## 10. Qual a alternativa mais barata que você descartou e por quê?

Documentar o big ball of mud sem mexer no código. Custa quase nada agora, mas mantém o pagamento contínuo de 96 h por trimestre de retrabalho (Exemplo numérico: 12 mudanças x 4 toques evitados x 2 h). A segunda mais barata seria espelhar colunas para o vizinho, que resolve a leitura hoje e recria o acoplamento amanhã quando a coluna mudar de nome.

## 11. O que você deixaria para trás nesta entrega?

Três coisas. A modelagem de contextos que não têm regra de consistência hoje, porque seria over-engineering. A separação de deploy em microsserviços, que não é problema atual. E a automação de reconciliação de sombra para leituras espelhadas, que fica para a atividade de barramento. Deixo também o versionamento de contrato dos 6 eventos como pendência explícita se o gate de CI não entrar no mesmo sprint.

## 12. Quanto custa e o que muda no bolso do negócio?

40 horas de esforço (meta) distribuídas em workshop de 4 h, modelagem de 12 h, testes de 10 h, contratos de 8 h e gate de CI de 6 h. Sem licença nova. O retorno é a eliminação de 96 h de retrabalho por trimestre (Exemplo numérico), mais redução do risco de incidente por mudança de coluna não comunicada. Traduzindo: em um trimestre o esforço se paga, e a partir do segundo trimestre o squad entrega feature em vez de remendar efeito cascata.
