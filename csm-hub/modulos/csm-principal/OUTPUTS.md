# OUTPUTS — CSM Principal V1

## Output 1: Triagem de flag

**Input:** "Flag de churn no cliente Clínica X — NPS 42, CSAT 3.2"

```
FLAG RECEBIDA — Risco de Churn — Clínica X — 26/04/2025

1. IMPACTO NO CLIENTE
   Um NPS de 42 indica que o cliente está insatisfeito e provável detrator.
   Combinado com CSAT 3.2, sinaliza problema de percepção de valor — não
   necessariamente de resultado. O cliente pode estar obtendo resultado
   mas não enxergando. Risco real de não renovação ao fim do contrato.

2. URGÊNCIA
   Piora sozinho — insatisfação não resolvida gera narrativa negativa.
   Acionar agora.

3. ÁREA RESPONSÁVEL
   Squad operacional (AM + GT) para diagnóstico de resultado.
   CSM conduz conversa de percepção diretamente com o cliente.

4. DECISÃO
   [X] Acionar squad operacional para diagnóstico de resultado (hoje)
   [X] Agendar conversa CSM + cliente em até 48h
   [X] Comunicar Coordenador agora

5. COMUNICAÇÃO AO COORDENADOR
   [Coordenador], flag de churn na Clínica X. NPS 42 + CSAT 3.2.
   Decisão: diagnóstico com o squad hoje + conversa com cliente em 48h.
   Te atualizo após a conversa.
```

## Output 2: Acionamento de área

**Input:** "Acione o squad operacional para a Clínica X"

```
ACIONAMENTO CSM — Squad Operacional — 26/04/2025

Para: GT [nome] + AM [nome]
Cópia: Coordenador [nome]

Contexto:
A Clínica X está com NPS 42 e CSAT 3.2 no mês de abril.
O resultado de mídia está dentro da meta (CPL R$78 vs meta R$80),
mas a percepção do cliente não reflete isso.

Impacto se não resolvido:
Cliente com LT de 8 meses em risco de não renovar contrato
que vence em 60 dias.

O que preciso de vocês:
Análise do que foi entregue vs o que foi comunicado ao cliente
nas últimas 4 semanas. Hipótese: gap de report, não de resultado.
Prazo: até amanhã 12h.

Critério de resolução:
Entender se é problema de entrega ou de percepção.
Se percepção: CSM ajusta comunicação com o cliente.
Se entrega: squad abre FCA e corrige.

Próximo contato: amanhã 14h com diagnóstico.
```

## Output 3: Plano de sucesso

**Input:** "Monte o plano de sucesso da Clínica X"

```
PLANO DE SUCESSO — Clínica X

Objetivo de negócio:
Aumentar o volume de pacientes para implante dentário em 30%
até o fim do ano. O dono quer abrir uma segunda unidade em 2026.

Definição de sucesso:
60 leads qualificados/mês com CPL ≤ R$80 e taxa de
agendamento ≥ 35% até o Q3.

Principais riscos antecipados:
1. Fadiga de criativo — alta probabilidade / impacto médio
   (mitigar: rotação mensal obrigatória de criativos)
2. Sazonalidade de julho — média probabilidade / impacto alto
   (mitigar: aumentar verba em junho, reduzir em julho)

Marco de 90 dias:
Ao final do Q2, o cliente deve ter:
- CPL estabilizado abaixo de R$80
- Pipeline de 180+ leads no trimestre
- NPS acima de 65

Frequência de QBR: trimestral (próximo: julho/2025)
```
