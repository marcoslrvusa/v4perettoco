# STANDARD-AUDIT-LOG | Trilhas de auditoria em workflows

Versao 1.0, Setembro 2026. Escopo: workflows criticos de automacao (disparo de campanha, sync de leads/CRM, rotinas de verba, jobs de dados).

## 1. Evento minimo (6 campos obrigatorios)

Todo evento registra: `ts` (UTC ISO 8601), `ator` (quem: usuario, service account ou job), `acao` (o que, vocabulario controlado), `alvo` (onde: workflow, campanha, registro por id), `resultado` (ok, erro, bloqueado) e `hash_prev` (encadeamento). Contexto extra vai em `detalhe` sem segredo e sem PII bruta (usar id ou hash).

## 2. Propriedades da trilha

Append-only (nunca edita nem apaga dentro do prazo), hash encadeado SHA-256 verificavel, relogio unico em UTC, armazenamento separado do sistema auditado, acesso de leitura restrito e toda leitura sensivel tambem logada.

## 3. Retencao em camadas

Quente (busca rapida, 90 dias, espelha o event history do CloudTrail) e fria imutavel (ate 5 anos, espelha o CloudTrail Lake com retencao longa). Apagar antes do prazo exige excecao formal com motivo e aprovacao. Backup testado: restauracao ensaiada 1 vez por semestre.

## 4. Mapeamento NIST CSF 2.0

| Funcao | Uso da trilha |
|--------|---------------|
| Govern (GV) | Politica de registro, papeis e revisao periodica |
| Identify (ID) | Inventario de workflows cobertos e lacunas |
| Protect (PR) | Integridade (hash), controle de acesso, sem segredo no evento |
| Detect (DE) | Alertas sobre bloqueado/erro em sequencia |
| Respond (RS) | Reconstrucao de incidente em ate 30 min (meta) |
| Recover (RC) | Lista de acoes para refazer a partir do log |

## 5. Rotina operacional

Revisao semanal dos eventos `bloqueado` e `erro`; revisao mensal com o dono de cada workflow; relatorio trimestral de compliance (cobertura, integridade verificada, incidentes reconstruidos). Achado de guardrail (atividade 1), dado pessoal (atividade 2, LGPD art. 37) ou segredo (atividade 3) gera acao com dono e prazo.
