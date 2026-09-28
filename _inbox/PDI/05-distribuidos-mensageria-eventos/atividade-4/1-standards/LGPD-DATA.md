# LGPD: Padrão de Dados e Eventos

1. **Minimização**: só o necessário para a finalidade.
2. **Consentimento por finalidade**: campanha != score.
3. **Anonimização em log/trace**: e-mail/CNPJ viram hash.
4. **Retenção definida**: PII tem TTL.
5. **Esquecimento**: delete em cascata por subject_id.

## Regra de ouro
Nunca PII em log, trace ou cache. Use hash(subject) para correlação.
