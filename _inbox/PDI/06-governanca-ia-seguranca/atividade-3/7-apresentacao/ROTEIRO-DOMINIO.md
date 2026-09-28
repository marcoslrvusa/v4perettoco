# Roteiro de Dominio | A3 Segredos e rotacao

## P1: Onde o segredo deve morar?
No cofre (Vault ou gerenciado do provider) em producao, em secrets do Actions no CI, em `.env` fora do git so no local. Codigo so referencia nome de variavel, nunca valor.

## P2: Com que frequencia girar?
Critica 30 dias, alta 90, padrao 180. Onde der, dynamic secret com TTL curto substitui a agenda: a credencial nasce, usa e morre.

## P3: OIDC ou chave estatica no CI?
OIDC sempre que o provider suporta: o workflow assume papel sem guardar segredo longo. Chave estatica so como excecao documentada e com rotacao curta.

## P4: Vazou, e agora?
Revoga no provider, gira e redistribui, audita o uso no periodo exposto, avalia comunicar (cliente e ANPD se houver pessoal), fecha com post-mortem. Critica em ate 4 h.

## P5: O scan no CI nao vai travar o time?
No primeiro mes trava um pouco, e e proposital: limpa historico, ajusta padroes e ensina o fluxo. Depois vira guarda silencioso que so fala quando ha risco real.
