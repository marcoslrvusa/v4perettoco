# LGPD — Padrao de Dados e Eventos

1. **Minimizacao**: so o necessario para a finalidade.
2. **Consentimento por finalidade**: campanha != score.
3. **Anonimizacao em log/trace**: e-mail/CNPJ viram hash.
4. **Retencao definida**: PII tem TTL.
5. **Esquecimento**: delete em cascata por subject_id.

## Regra de ouro
Nunca PII em log, trace ou cache. Use hash(subject) para correlacao.
