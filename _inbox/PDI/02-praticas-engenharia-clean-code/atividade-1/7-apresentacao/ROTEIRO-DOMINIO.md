# Roteiro de domínio: Refatoração de Módulo Legado com SOLID e Clean Architecture

Estudo para defesa presencial da atividade: 5 perguntas de coordenador com respostas curtas.

## 1. Por que Clean Architecture foi escolhida e as outras opções rejeitadas?

Porque ela desacopla regra de negócio de DB, e-mail e CRM via ports, permite teste sem infra e o ADR-021 registra hexagonal puro como overhead e manter acoplado como frágil.

## 2. Como o novo serviço elimina o SQL injection do legado?

Troca SQL concatenado por acesso via LeadRepository com consulta parametrizada, então o id da campanha nunca e interpolado na string.

## 3. O que o shadow de 1 sprint com corte em 0,1 por cento garante?

Garante que o módulo novo rode em paralelo ao legado de 600 linhas por 1 sprint com reconciliação diária, e só assume o tráfego se a divergência ficar abaixo de 0,1 por cento, com rollback por flag.

## 4. Como a meta de 85 por cento de cobertura e verificada?

Com testes de porta que usam mocks de Notifier e Repository, cobrindo o serviço sem subir banco nem SMTP, partindo de 0 por cento no legado.

## 5. O que muda de 4 responsabilidades para 1 por classe na prática?

Cada classe passa a ter menos de 45 linhas e um motivo de mudança, então alterar regra de campanha não toca em DB, e-mail ou CRM.
