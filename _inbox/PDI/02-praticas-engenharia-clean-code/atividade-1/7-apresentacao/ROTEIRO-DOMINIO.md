# Roteiro de dominio: Refatoracao de Modulo Legado com SOLID e Clean Architecture

Estudo para defesa presencial da atividade: 5 perguntas de coordenador com respostas curtas.

## 1. Por que Clean Architecture foi escolhida e as outras opcoes rejeitadas?

Porque ela desacopla regra de negocio de DB, e-mail e CRM via ports, permite teste sem infra e o ADR-021 registra hexagonal puro como overhead e manter acoplado como fragil.

## 2. Como o novo servico elimina o SQL injection do legado?

Troca SQL concatenado por acesso via LeadRepository com consulta parametrizada, entao o id da campanha nunca e interpolado na string.

## 3. O que o shadow de 1 sprint com corte em 0,1 por cento garante?

Garante que o modulo novo rode em paralelo ao legado de 600 linhas por 1 sprint com reconciliacao diaria, e so assume o trafego se a divergencia ficar abaixo de 0,1 por cento, com rollback por flag.

## 4. Como a meta de 85 por cento de cobertura e verificada?

Com testes de porta que usam mocks de Notifier e Repository, cobrindo o servico sem subir banco nem SMTP, partindo de 0 por cento no legado.

## 5. O que muda de 4 responsabilidades para 1 por classe na pratica?

Cada classe passa a ter menos de 45 linhas e um motivo de mudanca, entao alterar regra de campanha nao toca em DB, e-mail ou CRM.
