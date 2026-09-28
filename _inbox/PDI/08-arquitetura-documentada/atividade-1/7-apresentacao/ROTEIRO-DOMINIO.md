# ROTEIRO-DOMINIO: 5 Perguntas que Podem Cair

## 1. Por que C4 e nao UML tradicional?
Resposta: UML tem 14 diagramas e ninguem concorda qual usar; C4 tem 4 niveis com publico definido e regra de zoom unico, o que cabe no ritmo de automacao onde quem desenha e quem opera sao as mesmas pessoas.

## 2. Manter DSL e Mermaid duplicados nao apodrece?
Resposta: apodrece se nao houver regra. A regra aqui: PR que muda container exige os dois atualizados, e o checklist de revisao cobra isso. DSL e fonte, Mermaid e espelho.

## 3. Por que nivel 4 so em uma funcao?
Resposta: codigo muda todo dia e doc de codigo vira lixo em uma semana. Documentamos so onde bug custa dinheiro: o retry da coleta que decide verba de trafego nos relatorios.

## 4. Onde fica o deploy (VPS, Docker)?
Resposta: fora desta atividade de proposito. Infra hoje e VPS unica, entao o diagrama de deploy seria trivial e falso. Entra quando houver segundo ambiente.

## 5. Como isso reduz incidente na pratica?
Resposta: em falha de coleta, o operador abre o container, ve que workers chamam Meta via webhook e gravam no Supabase, e checa fila de erros em vez de perguntar no chat. Caminho de diagnostico de minutos, nao de horas.
