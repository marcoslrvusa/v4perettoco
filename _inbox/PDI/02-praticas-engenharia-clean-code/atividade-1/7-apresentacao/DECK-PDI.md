# Deck PDI: Refatoração de Módulo Legado com SOLID e Clean Architecture

Área: Engenharia de Software

## Slide 1: Resumo Executivo
Refatoração do módulo de orquestração de campanhas (antigo CampaignService, 600+ linhas, acoplado) para Clean Architecture com ports/adapters e os 5 princípios SOLID. Entrego o antes/depois, o ADR e um teste que prova a nova testabilidade.
O ponto não é 'estilo': é eliminar classes de risco (SQL injection, transações ausentes, falha silenciosa de CRM) e tornar o módulo coberto por teste sem subir infra.
## Slide 2: Contexto de Produção
O módulo dispara 3-5 campanhas/dia para listas de 5k-80k leads.
Falha silenciosa de gravação no CRM já causou duplo contato (reclamação real).
Qualquer alteração hoje exige deploy manual e testes manuais.
## Slide 3: O Problema e o Blast Radius
O CampaignService original misturava regra de negócio, acesso direto a banco, envio de e-mail e chamada de CRM no mesmo método.
| Violação | Manifestação |
| --- | --- |
| SRP | 1 classe cuida de regra+DB+email+CRM |
| OCP | novo canal = editar método central |
| DIP | aplicação depende de psycopg2/smtp direto |
| Sem transação | estado parcial em falha |
## Slide 4: Diagnóstico e Causa Raiz
SQL concatenado (f"SELECT ... {camp.id}"): vetor de injection.
Sem transação: lead marcado enviado mas e-mail falha -> estado inconsistente.
Impossível testar: 600 linhas, 4 dependências de I/O acopladas, 0% cobertura.
## Slide 5: Decisão Arquitetural (ADR)
ADR-021: Camadas e Ports/Adapters
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| Clean Architecture | testável, desacoplado | mais arquivos | ESCOLHIDA |
| Hexagonal puro | simétrico | overhead | rejeitada |
| Manter acoplado + E2E | zero refactor | frágil | rejeitada |
> Nota: Dependência de I/O vira interface (Protocol): LeadRepository, Notifier, Logger. O serviço depende de abstrações; implementações são injetadas no bootstrap.
## Slide 6: Entregas desta Atividade
SOLID-BEFORE-AFTER.md: mapeamento violacao->solução.
before_campaign_service.py: módulo legado.
after_campaign_service.py: Clean Architecture + 1 teste.
## Slide 7: Plano de Validação e Rollout
Cobrir o serviço com testes de porta (mock de Notifier/Repository): alvo 85%.
Feature flag: novo módulo em paralelo por 1 sprint (shadow).
Se divergência < 0,1%, migrar tráfego e remover legado.
Rollback: flag desliga o novo sem deploy.
## Slide 8: Métricas e SLO
| Métrica | Antes | Depois |
| --- | --- | --- |
| Acoplamento (resp/classe) | 4 | 1 |
| Cobertura | 0% | >= 85% |
| Linhas por classe | 600+ | < 45 |
| SQL injection | sim | eliminado |
## Slide 9: Riscos e Mitigações
| Risco | Mitigação |
| --- | --- |
| Shadow com divergência | reconciliação diária |
| Time não adota | PR template + lint de arquitetura |
## Slide 10: Próximos Passos
Aplicar o molde aos demais módulos legados.
Mutation testing (mutmut) no serviço.