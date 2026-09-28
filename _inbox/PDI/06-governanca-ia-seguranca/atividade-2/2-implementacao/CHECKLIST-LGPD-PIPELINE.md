# CHECKLIST-LGPD-PIPELINE | Conformidade por pipeline

Marcar por pipeline antes de ir a producao. Dono: dono do pipeline com o encarregado.

- [ ] Catalogo de campos preenchido (categoria, finalidade, base legal art. 7, retencao, destino)
- [ ] Base legal valida por campo; legitimo interesse com teste escrito e canal de oposicao
- [ ] Minimizacao aplicada na entrada (sem campo reserva, sem CPF sem justificativa)
- [ ] Etapa de anonimizacao/pseudonimizacao antes de agregar (`anonimizacao.py`, k minimo 5)
- [ ] Salt e chaves de pseudonimo sob controle separado (ver atividade 3)
- [ ] Rotina de DSAR com responsavel e prazo de ate 15 dias (art. 18)
- [ ] Tabela de retencao publicada com rotina de descarte (art. 15 e 16)
- [ ] Registro das operacoes mantido (art. 37); RIPD avaliado quando houver risco (art. 38)
