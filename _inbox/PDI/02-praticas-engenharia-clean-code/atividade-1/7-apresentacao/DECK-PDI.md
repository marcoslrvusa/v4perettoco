# Deck PDI — Refatoracao de Modulo Legado com SOLID e Clean Architecture

Area: Engenharia de Software

## Slide 1: Resumo Executivo
Refatoracao do modulo de orquestracao de campanhas (antigo CampaignService, 600+ linhas, acoplado) para Clean Architecture com ports/adapters e os 5 principios SOLID. Entrego o antes/depois, o ADR e um teste que prova a nova testabilidade.
O ponto nao e 'estilo': e eliminar classes de risco (SQL injection, transacoes ausentes, falha silenciosa de CRM) e tornar o modulo coberto por teste sem subir infra.
## Slide 2: Contexto de Producao
O modulo dispara 3-5 campanhas/dia para listas de 5k-80k leads.
Falha silenciosa de gravacao no CRM ja causou duplo contato (reclamacao real).
Qualquer alteracao hoje exige deploy manual e testes manuais.
## Slide 3: O Problema e o Blast Radius
O CampaignService original misturava regra de negocio, acesso direto a banco, envio de e-mail e chamada de CRM no mesmo metodo.
| Violacao | Manifestacao |
| --- | --- |
| SRP | 1 classe cuida de regra+DB+email+CRM |
| OCP | novo canal = editar metodo central |
| DIP | aplicacao depende de psycopg2/smtp direto |
| Sem transacao | estado parcial em falha |
## Slide 4: Diagnostico e Causa Raiz
SQL concatenado (f"SELECT ... {camp.id}") — vetor de injection.
Sem transacao: lead marcado enviado mas e-mail falha -> estado inconsistente.
Impossivel testar: 600 linhas, 4 dependencias de I/O acopladas, 0% cobertura.
## Slide 5: Decisao Arquitetural (ADR)
ADR-021 — Camadas e Ports/Adapters
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| Clean Architecture | testavel, desacoplado | mais arquivos | ESCOLHIDA |
| Hexagonal puro | simetrico | overhead | rejeitada |
| Manter acoplado + E2E | zero refactor | fragil | rejeitada |
> Nota: Dependencia de I/O vira interface (Protocol): LeadRepository, Notifier, Logger. O servico depende de abstracoes; implementacoes sao injetadas no bootstrap.
## Slide 6: Entregas desta Atividade
SOLID-BEFORE-AFTER.md — mapeamento violacao->solucao.
before_campaign_service.py — modulo legado.
after_campaign_service.py — Clean Architecture + 1 teste.
## Slide 7: Plano de Validacao e Rollout
Cobrir o servico com testes de porta (mock de Notifier/Repository) — alvo 85%.
Feature flag: novo modulo em paralelo por 1 sprint (shadow).
Se divergencia < 0,1%, migrar trafego e remover legado.
Rollback: flag desliga o novo sem deploy.
## Slide 8: Metricas e SLO
| Metrica | Antes | Depois |
| --- | --- | --- |
| Acoplamento (resp/classe) | 4 | 1 |
| Cobertura | 0% | >= 85% |
| Linhas por classe | 600+ | < 45 |
| SQL injection | sim | eliminado |
## Slide 9: Riscos e Mitigacoes
| Risco | Mitigacao |
| --- | --- |
| Shadow com divergencia | reconciliacao diaria |
| Time nao adota | PR template + lint de arquitetura |
## Slide 10: Proximos Passos
Aplicar o molde aos demais modulos legados.
Mutation testing (mutmut) no servico.