# Roteiro de Domínio | A1 Guardrails e anti-prompt-injection

## P1: Qual a diferença entre injeção direta e indireta?
Direta vem do usuário no prompt; indireta vem de fonte que o modelo consome (documento, página, e-mail) com instrução embutida. A indireta é mais perigosa porque dispensa o atacante de falar com o bot. Defesa igual para as duas: delimitar dado, detectar padrão e validar saída.

## P2: Por que não confiar só em prompt bem escrito?
Porque o modelo não separa com segurança instrução de dado: texto dentro da janela vira candidato a comando. Barreira estrutural (delimitador, detector, contrato de saída, HITL) funciona mesmo quando o prompt falha.

## P3: O que o proxy faz e o que ele não faz?
Faz sanitização, detecção por regras e validação de contrato sem dependência externa. Não substitui Moderation API nos casos duvidosos nem dispensa HITL em ação irreversível; ele e a primeira muralha, não o castelo.

## P4: Como medir se funciona?
Bateria de 60 casos (20 diretas, 20 indiretas, 10 extrações, 10 fora de contrato) com placar e piso de 95% para sair de staging, mais latência p95 e cobertura de HITL no alto risco.

## P5: Qual o custo de operar?
Regras custam milissegundos; o custo real e mapear o contrato de saída por automação e operar o HITL. Em troca, cada novo fluxo com LLM nasce com teto de dano conhecido.
