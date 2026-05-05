---
name: gestao-novo-cliente-peretto
description: Cria um novo cliente seguindo o padrão da unidade Peretto & Co. Use quando o usuário quiser adicionar um cliente da franquia, configurar Google Ads ou escalar a operação local.
area: gestao
author: marcoslrvusa
version: 1.0.0
---

# Novo Cliente Peretto & Co

Esta skill automatiza a criação de novos clientes para a unidade **Peretto & Co**, garantindo que a estrutura de pastas e as configurações de Google Ads sigam o padrão de escala da franquia.

## Quando usar
- Quando chegar um cliente novo na unidade.
- Quando precisar organizar um cliente antigo no padrão de escala Peretto.
- Quando o usuário disser "criar cliente peretto", "novo cliente pra minha unidade" ou similar.

## Processo de Execução

1. **Coleta de Informações**:
   - Pergunte o **Nome do Cliente** (slug em kebab-case).
   - Pergunte o **Google Ads Customer ID** (ID da conta no Google Ads).
   - Pergunte a **URL do NotebookLM** (se houver).

2. **Criação da Estrutura**:
   - Crie a pasta em `bases/peretto-co/clientes/{cliente-slug}`.
   - Copie todo o conteúdo de `bases/peretto-co/clientes/_template-peretto/` para a nova pasta.

3. **Configuração do Ambiente**:
   - Crie o arquivo `.env` baseado no `.env.example`.
   - Preencha o `GOOGLE_ADS_CUSTOMER_ID` no `.env`.
   - Preencha o `NOTEBOOKLM_URL` no `.env`.

4. **Personalização**:
   - Atualize o `README.md` substituindo `[Nome do Cliente]` pelo nome real.
   - Gere o `CLAUDE.md` inicial do cliente usando a lógica de contexto da V4.

5. **Finalização**:
   - Informe ao usuário que o cliente foi criado com sucesso.
   - Sugira rodar `/contexto` dentro da pasta para inicializar a IA com os dados reais que ele colocar lá.

## Exemplo de Uso
**Usuário**: "Quero criar um cliente novo chamado 'Academia Fit' para a Peretto."
**IA**: "Perfeito! Qual o Google Ads Customer ID da Academia Fit? (Se não tiver agora, pode pular)."
**Usuário**: "É 123-456-7890."
**IA**: [Executa criação] -> "Pronto! A Academia Fit foi configurada em `bases/peretto-co/clientes/academia-fit/`."
