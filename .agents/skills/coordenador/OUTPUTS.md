# OUTPUTS — Coordenador V4
## Exemplos de output esperado

---

## Output 1: Checklist semanal completo

**Input:** "Roda o checklist desta semana — temos 2 clientes ativos (Clínica X e E-commerce Moda) e 1 novo (SaaS RH)"

**Output esperado:**
```
CHECKLIST SEMANAL — Semana 14 — 25/04/2025

─── ONBOARDING ───
SaaS RH (cliente novo — semana 2 de 3 de onboarding)

[S] Account Planning completo (SPICED + STEP Frame + oportunidades)?
[N] Planejamento anual com requisitos de sucesso e FCS documentado?
[N] OKRs quebradas e registradas no plano tático?
[S] Sprint inicial documentada no Ekyte conforme padrão?

2/4 itens completos. NÃO transita para Ongoing ainda.

Itens N:
→ Planejamento anual | Responsável: AM | Prazo: até terça
→ OKRs na central tática | Responsável: AM | Prazo: até quarta

─── ONGOING ───

CLÍNICA X:
[S] Replanejamento trimestral em dia?
[S] CSAT/NPS mensal coletado?
[S] OKRs atualizadas no plano tático?
[S] Sprint atual documentada no Ekyte?
[S] Quality Check atualizado?
[N] ROI atualizado no sistema interno?

5/6 — 🟡 Atenção
Item N → ROI | Responsável: GT | Prazo: hoje (sexta)

E-COMMERCE MODA:
[S] Replanejamento trimestral em dia?
[S] CSAT/NPS mensal coletado?
[S] OKRs atualizadas no plano tático?
[S] Sprint atual documentada no Ekyte?
[S] Quality Check atualizado?
[S] ROI atualizado no sistema interno?

6/6 — 🟢 Saudável

─── RITUAIS ───
[S] Comitê P&EG realizado com ata preenchida?
[N] Growths realizados com atas preenchidas? (faltou quarta)
[S] Working Backwards realizado com ata preenchida?

2/3 — Ata do Growth de quarta ausente.
Item N → Growth quarta | Responsável: AM | Ação: preencher retrospectivamente ou registrar que não houve

─── CONSOLIDADO ───

STATUS GERAL: 🟡

PAUTAS PARA COMITÊ DE SEGUNDA:
1. Onboarding SaaS RH — planejamento anual e OKRs pendentes (AM responsável)
2. ROI da Clínica X — GT precisa atualizar (verificar se é bloqueio técnico ou esquecimento)
3. Ata do Growth de quarta — entender o motivo e evitar recorrência
```

---

## Output 2: Diagnóstico sistêmico

**Input:** "Por que as OKRs de 3 clientes diferentes estão desatualizadas na semana 6?"

**Output esperado:**
```
DIAGNÓSTICO SISTÊMICO — OKRs desatualizadas — Semana 6

PADRÃO IDENTIFICADO:
3 de 4 clientes ativos com OKRs não atualizadas na semana 6 consecutiva.
Não é falha individual — é falha de processo ou de clareza de etapa.

CAMADA DA FALHA:
→ Topo (planejamento) — os OKRs existem e foram criados corretamente no onboarding.
→ Meio (processo contínuo) — a atualização semanal não está acontecendo.

Não é falha do topo (planning ok). É falha de operação contínua.

CAUSA RAIZ:
A atualização de OKRs depende dos dados do GT (ROI, KPIs da semana). O GT está 
entregando os dados na sexta. O AM atualiza os OKRs também na sexta — mas já está 
focado no checklist e no Working Backwards. Os OKRs ficam para "depois" e não são 
atualizados.

A causa não é preguiça ou esquecimento — é sequência errada de tarefas e ausência 
de gatilho claro.

PLANO DE CORREÇÃO:
1. [imediato] Definir que o GT envia os KPIs semanais até quinta (não sexta)
   Dono: Coordenador alinha com GT | Prazo: próxima semana

2. [processo] AM atualiza OKRs toda quinta após receber os dados do GT — antes do Working Backwards
   Dono: AM implementa | Prazo: próxima semana

3. [monitoramento] Checklist de sexta agora inclui "GT enviou KPIs até quinta?" como item
   Dono: Coordenador | Prazo: imediato

COMUNICAÇÃO PARA O TIME:
"Identificamos que as OKRs estão ficando desatualizadas porque o GT entrega os dados 
na sexta e o AM já está em outro modo. A partir de agora: GT envia KPIs até quinta, 
AM atualiza OKRs até quinta à tarde. Isso libera a sexta para o checklist e o Working 
Backwards. Mudança entra já na próxima semana."
```

---

## Output 3: Nota de autonomia do time

**Input:** "Estamos na semana 10. Em que pé está a autonomia do time?"

**Output esperado:**
```
AVALIAÇÃO DE AUTONOMIA — Semana 10

NOTA GERAL: 4/5

─── RITUAIS ───
Comitê P&EG: AM facilita com segurança. Pauta estruturada, ata preenchida na hora. ✅
Growth: GT assumiu a facilitação terça e quarta. AM terceira. Ritmo bom. ✅
Working Backwards: alternância AM/GT funcionando. Qualidade das atas melhorou. ✅
Nota rituais: 5/5

─── CHECKLIST ───
Preenchido sem cobrança nas últimas 3 semanas. ✅
2 itens N recorrentes (ROI do GT e atas do Growth) — padrão identificado e 
plano de correção em andamento. 🟡
Nota checklist: 4/5

─── ONBOARDING ───
Último cliente novo (SaaS RH) passou por todos os 4 entregáveis sem intervenção. ✅
Transição para ongoing aconteceu dentro do prazo. ✅
Nota onboarding: 5/5

─── ONGOING ───
2 de 4 clientes consistentemente verdes. ✅
1 cliente em 🟡 há 2 semanas — FCA aberta, plano em execução. 🟡
1 cliente sem replanejamento trimestral (atrasado 1 semana) — AM ciente. 🟡
Nota ongoing: 3/5

─── TESTE DE VALIDAÇÃO ─── 
Checklist verde nas últimas 2 semanas? ✅
Atas preenchidas sem cobrança? ✅ (3 semanas seguidas)

RESULTADO: Autonomia VALIDADA. Time está pronto para operar sem intervenção.

PRÓXIMO PASSO:
Coordenador sai dos rituais a partir da semana 11. Lê atas e checklist assincronamente.
Feedback semanal continua — agora por escrito, máximo 5 minutos de leitura para o time.
Documentar passagem de bastão até o final da semana 12.
```
