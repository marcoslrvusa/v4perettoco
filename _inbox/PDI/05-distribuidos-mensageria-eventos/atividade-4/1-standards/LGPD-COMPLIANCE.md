# STANDARD — Conformidade LGPD (Dados Distribuídos)

## Princípios aplicados
- **Trânsito:** TLS 1.2+ obrigatório; mTLS entre serviços internos.
- **Repouso:** AES-256 em campos sensíveis (CPF, e-mail) no banco.
- **Minimização:** só transmite o necessário no evento.
- **Consentimento:** `consent_id` carregado no cabeçalho da mensagem.
- **Auditoria:** log imutável de acesso a PII.

## Checklist
- [ ] TLS em todos os tópicos/filas
- [ ] Criptografia de colunas PII
- [ ] Máscara em logs
- [ ] Retenção e direito ao esquecimento documentados
