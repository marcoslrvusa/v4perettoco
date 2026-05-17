<img src="../../../v4-logo.png" alt="V4 Logo" width="120"/>

# [Nome do Cliente]

Copie esta pasta e renomeie com o nome do cliente.

## Estrutura

- `calls/` — Transcricoes de reunioes, audios transcritos, anotacoes de call
- `checkins/` — Pautas, ensaios, reviews e materiais finais de check-in
- `docs/` — Documentos do cliente: briefing, propostas, contratos, apresentacoes
- `campanhas/` — Dados de campanhas: CSVs, relatorios, prints de dashboards
- `mission-control/` — Estado vivo da conta criado por `/contexto` ou `/account-handoff`

## Como usar

1. Jogue seus arquivos nas pastas correspondentes
2. Rode `/contexto` para a IA ler tudo, gerar CLAUDE.md/AGENTS.md e montar o Mission Control
3. Comece a trabalhar — a IA ja vai conhecer o cliente

## Dicas

- Quanto mais dados voce colocar, melhor a IA trabalha
- Transcricoes de calls sao ouro — a IA entende contexto, tom e prioridades do cliente
- Atualize os dados periodicamente e rode `/contexto` de novo
