# Roteiro de Demo: Conformidade LGPD em Eventos e Dados (anonimização, consentimento, esquecimento)

Abra o deck (index.html) e percorra os slides na ordem.

1. Slide de Resumo: abra com o problema de negócio e o blast radius.
2. Slide do ADR: defenda a opção escolhida vs as rejeitadas (trade-offs).
3. Slide de Validação/Rollout: mostre como provamos em produção.
4. Slide de Riscos: apresente o plano de mitigação.

A partir do passo 5, a demonstração técnica (terminal + navegador). Pré-requisitos: Python 3.10+
com `cryptography` instalado, acesso de leitura ao banco de homologação, `subject_id` de teste
`00000000-0000-4000-8000-00000000a4de` (seed deste roteiro, não é dado real de titular) e
permissão de escrita apenas na base de homologação. Jamais rode o passo 13 em produção sem o
ticket do titular aberto.

5. **Confirme o ambiente.** Comando: `pwd && git rev-parse --short HEAD`. Saída esperada: a raiz
   do repositório e o SHA curto. Critério de falha: qualquer outro diretório. Se falhar, não
   siga: você estaria demonstrando em outra cópia do código.

6. **Varredura de log (C1).** Comando:
   `python3 2-code/anon.py` adaptado para receber o arquivo, por exemplo
   `python3 -c "from anon import log_safe; import sys; print(log_safe(open('/var/log/app.log').read(), 's4lt'))"`.
   Saída esperada: nenhuma linha com `@` seguido de domínio; só `anon:` + 12 caracteres
   hexadecimais. Critério de falha: qualquer `@` sobrando. Se falhar, mostre a linha crua ao
   público (é o "antes") e diga que o logger precisa trocar de `logger.info(payload)` para
   `logger.info("lead salvo subject=%s", subject_id)`.

7. **Correlação sem PII.** Comando:
   `python3 -c "from anon import anon; print(anon('joao@empresa.com e 12.345.678/0001-90', 's4lt'))"`.
   Saída esperada: dois tokens `anon:...` determinísticos e o resto do texto intacto. Critério
   de falha: valor original preservado. Se falhar, verifique se o `salt` está sendo passado: sem
   salt, o hash é reversível por dicionário.

8. **Demonstre a irreversibilidade do hash.** Comando: rode duas vezes com salts diferentes.
   Saída esperada: tokens diferentes para o mesmo e-mail. Critério de falha: tokens iguais
   (significa que o salt está fixo no código). Se falhar, mostre por que isso é grave: mesmo
   sendo rápido de calcular, sem salt o ataque de dicionário resolve em minutos.

9. **Cifra em repouso (C3).** Comando:
   `python3 -c "from encrypt_pii import encrypt, decrypt; t = encrypt('123.456.789-00'); print(t); print(decrypt(t))"`.
   Saída esperada: um token longo com prefixo do Fernet e, em seguida, o valor original de volta.
   Critério de falha: valor em claro no token. Se falhar, confira se `cryptography` está
   instalado e se o token não foi cortado ao ser copiado.

10. **Mostre o bug documentado da chave.** Comando: rode o passo 9 duas vezes em processos
    separados (`python3 -c ... ; python3 -c ...`). Saída esperada: o token gerado no primeiro
    processo **não** decifra no segundo. Critério esperado: é esse o comportamento, e ele
    ilustra por que `Fernet.generate_key()` em tempo de import não pode ir para produção. Se
    alguém perguntar "então funciona?", a resposta: em homologação de um processo só, sim; em
    produção com reinício, a chave some e o dado vira ruído.

11. **Leia a cascata antes de rodar.** Arquivo: `3-supabase/retention_policy.sql`. Clique nas
    quatro linhas de `DELETE` e conte os destinos. Saída esperada: `leads`, `activities`,
    `traces` e `subject`, nesta ordem, cadastro por último (a ordem importa pelas chaves
    estrangeiras). Critério de falha: um destino faltando. Se faltar, o `mapa-dados.md` está
    incompleto: pare a demo e registre a tabela órfã.

12. **Confirme o antes.** Comando: `SELECT count(*) FROM leads WHERE subject_id = '00000000-0000-4000-8000-00000000a4de';`
    (repetindo para as outras três tabelas). Saída esperada: contagens maiores que zero em
    pelo menos duas tabelas. Critério de falha: tudo zerado, a seed não existe. Se falhar,
    rode a seed do exercício de novo antes de continuar; demonstrar exclusão sobre dado vazio
    não prova nada.

13. **Execute a exclusão (C3).** Comando: `psql ... -f 3-supabase/retention_policy.sql` com o
    `subject_id` de teste no lugar de `$1`. Saída esperada: as quatro contagens seguidas de
    `DELETE 1` ou mais. Critério de falha: qualquer erro no meio sem o estado retomar. Se
    falhar, reinicie o script: a idempotência permite rodar de novo do zero, e é exatamente o
    que o teste T1 faz com `kill -9`.

14. **Prove a exclusão.** Comando: repita os quatro `SELECT count(*)` do passo 12. Saída
    esperada: `0` nas quatro. Critério de falha: qualquer contagem acima de zero. Se falhar,
    identifique qual destino sobrou e cite o modo de falha correspondente da tabela do README:
    exclusão parcial é o pior estado, porque o titular fica apagado em um lugar e vivo em outro.

15. **Prove a auditoria (sem PII).** Comando: `SELECT * FROM audit_log WHERE subject_id = '00000000-0000-4000-8000-00000000a4de';`
    Saída esperada: linha com `action = 'delete'`, destinos, resultado e data/hora, e **nenhum
    campo de e-mail ou CPF**. Critério de falha: qualquer coluna com dado pessoal. Se falhar,
    explique que a prova da exclusão não pode conter o dado excluído e registre como incidente.

16. **Demonstre a idempotência (T2).** Comando: rode o script do passo 13 mais duas vezes.
    Saída esperada: mesmo resultado final, sem erro de chave duplicada. Critério de falha:
    exceção de chave estrangeira ou de `subject` inexistente. Se falhar, o script precisa do
    `ON CONFLICT DO NOTHING` no `deletion_request`, que é justamente a linha que torna a
    retomada segura.

17. **Teste de falha fechada (T3).** Comando: pare o serviço de consentimento e tente publicar
    um evento de exemplo. Saída esperada: payload **minimizado** (sem e-mail, sem CPF, sem
    telefone), com o evento recusado ou reduzido conforme o modo configurado. Critério de
    falha: payload completo saindo com o gateway fora. Se falhar, a configuração está em modo
    de falha aberta: corrija antes de qualquer outra demonstração.

18. **Teste de ordem (C6).** Comando: publique `lead.criado` e logo em seguida
    `subject.delete` para o mesmo `subject_id`, com rebalanceamento forçado no meio (adicione
    um consumidor ao grupo). Saída esperada: estado final "apagado" em 100% das execuções (repita
    5 vezes). Critério de falha: em alguma execução o dado voltou a existir. Se falhar, a chave
    de partição não é `subject_id`: sem a chave certa, ordem não é garantida e o experimento
    prova o contrário do que você quer mostrar.

19. **Teste de carga do gateway (T9).** Comando: gere `400 eventos/s` por 15 minutos contra
    homologação com cache quente. Saída esperada: `p95 <= 25 ms` (meta) e zero timeout de
    publicação. Critério de falha: p95 acima da meta ou qualquer evento sem `consent_id`. Se
    falhar, olhe o `consent_cache_hit_ratio` antes de mexer em instância: cache frio é a causa
    mais comum.

20. **Mostre o gate de schema (C7).** Comando: adicione ao `lead_event.avsc` um campo de e-mail
    sem `pii:true` e rode a validação da esteira. Saída esperada: build falhando com a mensagem
    apontando o campo. Critério de falha: build passando. Se falhar, reverta o campo na hora e
    explique que a proteção hoje depende de vigilância humana, o que é um risco registrado.

21. **Feche no deck.** Volte ao `index.html`, slides 15 (SLO), 19 (próximos passos) e 20
    (fecho). Saída esperada: os seis compromissos do slide de fecho lidos em voz alta. Critério
    de falha: apresentar meta sem dono. Se faltar tempo, corte os passos 9 e 10 (são ilustração
    didática) e mantenha 13, 14, 15 e 18, que são a prova central.

22. **Rollback da demonstração.** Comando: restaure a seed de teste
    (`INSERT` do exercício) e apague as linhas de `audit_log` geradas pela demo. Saída esperada:
    base de homologação igual ao estado inicial. Critério de falha: dado de teste esquecido na
    base. Se falhar, registre no ticket da atividade para limpeza na próxima janela.

23. **Registro final.** Comando: anexar ao ticket a saída dos passos 6, 14, 15, 18 e 19 com data
    e horário. Saída esperada: cinco evidências numeradas. Critério de falha: alguma evidência
    faltando. Se falhar, o item do checklist "testes executados nesta versão" não pode ser
    marcado, e a atividade não está pronta.

Material de apoio: pdi-distribuidos-mensageria-eventos-a4-report.pdf (dossiê completo).
