# ONBOARDING CSM — Guia de Implementação

> Siga este guia na ordem. Cada etapa tem um critério de validação.
> Setup completo: ~2 horas na primeira vez.

---

## Etapa 1 — Configurar o ambiente (15 min)

**Pré-requisito:** v4-automations já instalado e funcionando.

```bash
# 1. Clone o repositório
git clone [url-do-csm-hub] csm-hub

# 2. Adicione as variáveis ao config/.env do v4-automations
echo "EMAIL_CSM=seu-email@v4company.com" >> ../v4-automations/config/.env

# 3. Adicione campos CSM em config/clientes.json para cada cliente:
# "lt_meses": 8,
# "contrato_vence_dias": 60,
# "ultimo_nps": null,
# "ultimo_csat": null,
# "csm_thresholds": {}  ← deixe vazio para usar os defaults
```

**Validação:** `python automacoes/detector_flags.py` deve rodar sem erro.

---

## Etapa 2 — Configurar Claude Projects (30 min)

Crie 5 Projects no claude.ai. Para cada um:

| Project | System prompt |
|---|---|
| CSM Principal | `SKILL.md` + `CONTEXT.md` de `modulos/csm-principal/` |
| Flag ROI | `SKILL.md` + `CONTEXT.md` de `modulos/flag-roi/` |
| Flag Churn | `SKILL.md` + `CONTEXT.md` de `modulos/flag-churn/` |
| Flag OKR | `SKILL.md` + `CONTEXT.md` de `modulos/flag-okr/` |
| Flag Operação | `SKILL.md` + `CONTEXT.md` de `modulos/flag-operacao/` |

**Como configurar:**
1. claude.ai → Projects → New Project
2. Cole o conteúdo dos dois arquivos no campo "System Prompt"
3. Adicione o OUTPUTS.md como knowledge do Project
4. Nomeie o Project com o nome do módulo

**Validação:** Abra o Project CSM Principal e digite:
`"Inicie o setup da unidade [nome da sua unidade]"`
O agente deve guiar o setup.

---

## Etapa 3 — Setup inicial da carteira (45 min)

Abra o Project CSM Principal e conduza:

```
1. "Liste todos os clientes ativos da carteira"
   → Preencha o perfil básico de cada cliente

2. "Monte o plano de sucesso do cliente [X]"
   → Repita para cada cliente

3. "Defina os critérios de flag personalizados para [X]"
   → Se o cliente tiver thresholds diferentes dos defaults
```

**Onde registrar:** Vault Obsidian (pasta `clientes/`) + Ekyte workspace de cada cliente.

**Validação:** Cada cliente tem um `_index.md` no vault com plano de sucesso preenchido.

---

## Etapa 4 — Ativar as automações (10 min)

```bash
# Instala o cron do detector de flags
python setup/setup_inicial.py --instalar-crons
```

Isso adiciona ao crontab:
- Quinta 7h → `detector_flags.py`
- Domingo 20h → `detector_flags.py`

**Validação:** `crontab -l` mostra as duas entradas.

---

## Etapa 5 — Teste de ponta a ponta (20 min)

```bash
# Roda o detector manualmente
python automacoes/detector_flags.py
```

Verifique:
- Email chegou para CSM e Coordenador
- Briefing está formatado corretamente
- Flags (se houver) estão com dados reais

Se tudo ok: **CSM Hub está ativo.**

---

## Critério de validação final

O setup está completo quando:
- [ ] Detector rodou sem erro
- [ ] 5 Projects criados e respondendo
- [ ] Plano de sucesso de todos os clientes preenchido
- [ ] Crons ativos no crontab
- [ ] Primeiro briefing automático recebido

---

## Como replicar para outra unidade

1. Clone o repositório
2. Edite apenas `modulos/*/CONTEXT.md` com os dados da nova unidade
3. Siga este guia do zero
4. O `SKILL.md` de cada módulo não precisa ser tocado

O CONTEXT.md é o único arquivo que muda entre unidades.
