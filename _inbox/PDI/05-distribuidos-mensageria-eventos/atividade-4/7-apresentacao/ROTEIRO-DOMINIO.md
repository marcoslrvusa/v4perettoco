# Roteiro de Domínio: Atividade 4 (LGPD em eventos e dados)

5 perguntas que um coordenador faria, com respostas curtas para defesa no presencial.

## 1. Onde o PII aparece e como você o elimina do trânsito?
O `lead.criado` carregava CPF, e-mail e telefone em texto puro; agora vai cifrado com AES e o downstream recebe `subject_id` ou hash.

## 2. Como o consentimento e garantido?
Flag `consent_id` obrigatória no payload; sem base legal ativa o dado pessoal não é publicado; auditoria por finalidade.

## 3. Como funciona o direito ao esquecimento?
Uma varredura apaga por `subject_id` em todas as tabelas; cai de 90 dias para menos de 1 dia, dentro do patamar de até 15 dias.

## 4. O que é minimização neste desenho?
Cada etapa recebe só o dado necessário; o Analytics recebe token sem reversão e nada de PII vai para cache.

## 5. Como você prova a conformidade?
Varredura de logs com 0 e-mail ou CNPJ cru, 100% dos fluxos com consentimento e TTL de 365 dias com purge automático.
