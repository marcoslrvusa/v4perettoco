# Script de Demonstração — Conformidade LGPD no Tráfego Distribuído (criptografia em trânsito e repouso)

## Setup
```bash
# Estrutura da entrega
tree 05-distribuidos-mensageria-eventos/atividade-4/
```

## Passo 1: Contexto
Explique o problema:
> Dados pessoais trafegam entre serviços sem controle de conformidade.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- TLS 1.2+ e mTLS entre serviços internos
- AES-256 em colunas PII no banco
- Consent_id no cabeçalho das mensagens
- Log imutável de acesso a PII

## Passo 3: Entregas
Mostre os artefatos gerados:
- LGPD-COMPLIANCE.md (framework + checklist)
- encrypt_pii.py (criptografia)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Trânsito criptografado | Não | TLS/mTLS |
| Repouso (PII) | Claro | AES-256 |
