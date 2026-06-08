# Sessão: APE Keyword Process README

**Data:** 2026-05-25
**Contexto:** Criar versão APE do keyword process da planilha PAL da Atlas Copco

## O que foi feito
1. Lido `PAL - README.csv` (14 linhas) — README da planilha PAL que documenta o fluxo de keyword selection
2. Analisado escopo dos produtos com base no input do usuário:
   - **PAL** = Generators (sheets 3-4) + Energy Storage ZBP/ZBC (sheets 5-6) + Charging & Hybrid filtrado (sheet 9)
   - **APE** = Light Towers (sheets 1-2) + Mobile Solar Plants (sheets 7-8) + Charging & Hybrid (sheet 9, hybrid only)
   - EV Charger keywords removidos (fora de escopo)
3. Criado `APE - README.csv` seguindo a mesma estrutura do PAL

## Arquivos criados
- `APE - README.csv` — README da planilha APE com fluxo e mapeamento de produtos

## Próximos passos sugeridos
- Criar as sheets individuais na planilha APE: LightTowers_VOLUME.csv, LightTowers_ESTRATEGIA.csv, etc.
- Migrar os dados de keywords das sheets 1, 2, 7, 8 do PAL para APE
- Filtrar sheet 9 removendo EV Charger keywords, manter só hybrid generator
