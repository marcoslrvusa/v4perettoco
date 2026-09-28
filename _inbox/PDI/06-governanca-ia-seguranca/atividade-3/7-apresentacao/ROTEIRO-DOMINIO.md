# Roteiro de Domínio | A3 Segredos e rotação

## P1: Onde o segredo deve morar?
No cofre (Vault ou gerenciado do provider) em produção, em secrets do Actions no CI, em `.env` fora do git só no local. Código só referencia nome de variável, nunca valor.

## P2: Com que frequência girar?
Crítica 30 dias, alta 90, padrão 180. Onde der, dynamic secret com TTL curto substitui a agenda: a credencial nasce, usa e morre.

## P3: OIDC ou chave estática no CI?
OIDC sempre que o provider suporta: o workflow assume papel sem guardar segredo longo. Chave estática só como exceção documentada e com rotação curta.

## P4: Vazou, e agora?
Revoga no provider, gira e redistribui, audita o uso no período exposto, avalia comunicar (cliente e ANPD se houver pessoal), fecha com post-mortem. Crítica em até 4 h.

## P5: O scan no CI não vai travar o time?
No primeiro mês trava um pouco, e e proposital: limpa histórico, ajusta padrões e ensina o fluxo. Depois vira guarda silencioso que só fala quando há risco real.
