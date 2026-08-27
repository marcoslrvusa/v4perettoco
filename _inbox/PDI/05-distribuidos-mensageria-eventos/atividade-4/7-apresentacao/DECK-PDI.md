# PDI — Apresentação: Conformidade LGPD no Tráfego Distribuído (criptografia em trânsito e repouso)

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: CONFORMIDADE LGPD NO TRÁFEGO DISTRIBUÍDO (CRIPTOGRAFIA EM TRÂNSITO E REPOUSO)

Marcos Perettoco — V4 Company
25/08/2026 | Sistemas Distribuídos
```

---

## Slide 2: O Problema

**Dados pessoais trafegam entre serviços sem controle de conformidade.**

## Diagnóstico

- Sem criptografia em trânsito entre serviços
- PII em claro no banco
- Sem trilha de consentimento


---

## Slide 3: Arquitetura da Solução

## Abordagem

- TLS 1.2+ e mTLS entre serviços internos
- AES-256 em colunas PII no banco
- Consent_id no cabeçalho das mensagens
- Log imutável de acesso a PII


---

## Slide 4: Entregas

## Artefatos

- LGPD-COMPLIANCE.md (framework + checklist)
- encrypt_pii.py (criptografia)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Trânsito criptografado | Não | TLS/mTLS |
| Repouso (PII) | Claro | AES-256 |
---

## Slide 6: Próximos Passos

- Aplicar mTLS no barramento (Módulo 05-A1)
- Mascarar PII em logs
