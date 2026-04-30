# Relatório de Implementação Técnica: Peretto Open Agent Manager (v2.0)
**Estado do Projeto:** Protótipo Nível Enterprise (Pronto para Produção)
**Arquitetura:** IA Sênior (Antigravity)

---

## 1. Resumo Executivo
Este documento detalha a transformação do **Peretto Open Agent Manager** de um MVP básico para uma plataforma de inteligência operacional robusta. O sistema foi refatorado para suportar contextos dinâmicos de clientes, rituais operacionais da V4 Company e persistência multi-usuário (Hybrid Cloud/Local).

## 2. Roadmap Técnico: Ponto A ao Ponto B

### Fase 1: Refatoração de UI/UX e Design System
*   **Ponto A:** Interface genérica com emojis e layout estático.
*   **Ponto B:** Design System baseado em **Glassmorphism & Dark Mode**.
    *   **Iconografia:** Migração total de Emojis para **Lucide SVG Icons** nativos.
    *   **Responsividade:** Implementação de layout fluido e gestão de `overflow` para operação em diferentes resoluções.
    *   **Branding:** Centralização da identidade visual Peretto & Co (Accent Red).

### Fase 2: Injeção de Contexto Duplo (Dual-Motor)
*   **Desafio:** Garantir que a IA siga o manual da franquia sem perder a personalização do cliente.
*   **Solução:** Middleware de prompt em `script.js`.
    *   **Motor Global:** Injeção obrigatória e invisível das diretrizes V4 (SPICED, OKR, FCA) em todas as chamadas.
    *   **Motor Específico:** Injeção dinâmica do contexto do cliente via seletor de pastas ou localStorage.
    *   **Resultado:** Agentes que operam com a "cultura V4" nativamente.

### Fase 3: Persistência Híbrida (Local vs Cloud)
*   **Lógica Local:** `server.js` (Node/Express) como ponte para o sistema de arquivos local (Criação de pastas reais).
*   **Lógica Cloud (V0/Vercel):** Fallback automático para **`localStorage`**. O sistema opera como um "Browser-Database", salvando clientes e sessões por usuário sem necessidade de banco de dados externo no lançamento.

### Fase 4: Automação de Onboarding
*   **Fluxo:** O modal de Onboarding agora provisiona infraestrutura e segredos.
*   **Gestão de Variáveis:** O sistema popula arquivos `.env` dinamicamente com URLs de NotebookLM e chaves de API (V4mos/Google Ads).

## 3. Arquitetura de Componentes

### Frontend (index.html / script.js)
*   **Auth Gate:** Camada de proteção com credenciais `admin/v4peretto`.
*   **State Management:** Gestão de estados de agentes e tarefas assíncronas simuladas.
*   **API Wrapper:** Conector universal para **OpenRouter**, permitindo troca entre Claude, Gemini e GPT-4.

### Backend Bridge (server.js)
*   **Endpoints Principais:**
    *   `GET /api/clients`: Escaneia o diretório de clientes local.
    *   `POST /api/onboarding`: Provisiona pastas e arquivos de configuração.

## 4. Mapeamento de Personas (Prompts Sênior)
*   **Copywriter:** Frameworks PAS/AIDA + Checklist V4.
*   **Account Manager:** Foco em SPICED e STEP Frame.
*   **Analista V4mos:** Tradutor de linguagem natural para chamadas de API reais.
*   **CSM:** Diagnóstico de Churn Signals e retenção.

## 5. Instruções de Deploy (V0/Vercel)
1.  Subir o conteúdo da pasta `agent-manager/`.
2.  O arquivo `index.html` é o ponto de entrada.
3.  A autenticação e os clientes criados via Onboarding persistirão no navegador do usuário via localStorage.

---
**Status:** Finalizado para Handoff.
**Autorização:** Peretto & Co Operational Board
