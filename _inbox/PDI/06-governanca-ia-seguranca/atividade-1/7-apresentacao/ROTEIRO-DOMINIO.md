# Roteiro de Dominio | A1 Guardrails e anti-prompt-injection

## P1: Qual a diferenca entre injecao direta e indireta?
Direta vem do usuario no prompt; indireta vem de fonte que o modelo consome (documento, pagina, e-mail) com instrucao embutida. A indireta e mais perigosa porque dispensa o atacante de falar com o bot. Defesa igual para as duas: delimitar dado, detectar padrao e validar saida.

## P2: Por que nao confiar so em prompt bem escrito?
Porque o modelo nao separa com seguranca instrucao de dado: texto dentro da janela vira candidato a comando. Barreira estrutural (delimitador, detector, contrato de saida, HITL) funciona mesmo quando o prompt falha.

## P3: O que o proxy faz e o que ele nao faz?
Faz sanitizacao, deteccao por regras e validacao de contrato sem dependencia externa. Nao substitui Moderation API nos casos duvidosos nem dispensa HITL em acao irreversivel; ele e a primeira muralha, nao o castelo.

## P4: Como medir se funciona?
Bateria de 60 casos (20 diretas, 20 indiretas, 10 extracoes, 10 fora de contrato) com placar e piso de 95% para sair de staging, mais latencia p95 e cobertura de HITL no alto risco.

## P5: Qual o custo de operar?
Regras custam milissegundos; o custo real e mapear o contrato de saida por automacao e operar o HITL. Em troca, cada novo fluxo com LLM nasce com teto de dano conhecido.
