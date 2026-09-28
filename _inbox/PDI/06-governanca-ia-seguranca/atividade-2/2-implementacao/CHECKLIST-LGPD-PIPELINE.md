# CHECKLIST-LGPD-PIPELINE | Conformidade por pipeline

Marcar por pipeline antes de ir a produção. Dono: dono do pipeline com o encarregado.

- [ ] Catálogo de campos preenchido (categoria, finalidade, base legal art. 7, retenção, destino)
- [ ] Base legal valida por campo; legítimo interesse com teste escrito e canal de oposição
- [ ] Minimização aplicada na entrada (sem campo reserva, sem CPF sem justificativa)
- [ ] Etapa de anonimizacao/pseudonimizacao antes de agregar (`anonimizacao.py`, k mínimo 5)
- [ ] Salt e chaves de pseudônimo sob controle separado (ver atividade 3)
- [ ] Rotina de DSAR com responsável e prazo de até 15 dias (art. 18)
- [ ] Tabela de retenção publicada com rotina de descarte (art. 15 e 16)
- [ ] Registro das operações mantido (art. 37); RIPD avaliado quando houver risco (art. 38)
