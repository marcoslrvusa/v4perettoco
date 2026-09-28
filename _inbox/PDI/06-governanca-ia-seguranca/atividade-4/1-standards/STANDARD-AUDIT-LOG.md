# STANDARD-AUDIT-LOG | Trilhas de auditoria em workflows

Versão 1.0, Setembro 2026. Escopo: workflows críticos de automação (disparo de campanha, sync de leads/CRM, rotinas de verba, jobs de dados).

## 1. Evento mínimo (6 campos obrigatórios)

Todo evento registra: `ts` (UTC ISO 8601), `ator` (quem: usuário, service account ou job), `acao` (o que, vocabulário controlado), `alvo` (onde: workflow, campanha, registro por id), `resultado` (ok, erro, bloqueado) e `hash_prev` (encadeamento). Contexto extra vai em `detalhe` sem segredo e sem PII bruta (usar id ou hash).

## 2. Propriedades da trilha

Append-only (nunca edita nem apaga dentro do prazo), hash encadeado SHA-256 verificável, relógio único em UTC, armazenamento separado do sistema auditado, acesso de leitura restrito e toda leitura sensível também logada.

## 3. Retenção em camadas

Quente (busca rápida, 90 dias, espelha o event history do CloudTrail) e fria imutável (até 5 anos, espelha o CloudTrail Lake com retenção longa). Apagar antes do prazo exige exceção formal com motivo e aprovação. Backup testado: restauração ensaiada 1 vez por semestre.

## 4. Mapeamento NIST CSF 2.0

| Função | Uso da trilha |
|--------|---------------|
| Govern (GV) | Política de registro, papéis e revisão periódica |
| Identify (ID) | Inventário de workflows cobertos e lacunas |
| Protect (PR) | Integridade (hash), controle de acesso, sem segredo no evento |
| Detect (DE) | Alertas sobre bloqueado/erro em sequência |
| Respond (RS) | Reconstrução de incidente em até 30 min (meta) |
| Recover (RC) | Lista de ações para refazer a partir do log |

## 5. Rotina operacional

Revisão semanal dos eventos `bloqueado` e `erro`; revisão mensal com o dono de cada workflow; relatório trimestral de compliance (cobertura, integridade verificada, incidentes reconstruidos). Achado de guardrail (atividade 1), dado pessoal (atividade 2, LGPD art. 37) ou segredo (atividade 3) gera ação com dono e prazo.
