# Google Drive MCP — Knowledge Base Viva

**Propósito:** Google Drive como repositório de documentos, briefings, relatórios e artefatos — acessado pelos agentes em tempo de query via MCP.

---

## 1. Arquitetura

```
  Agente OpenCode
       │
       │ Drive MCP (8 tools)
       ▼
  ┌─────────────────────────────────────────────┐
  │              Google Drive                    │
  │                                              │
  │  ┌──────────┐ ┌──────────┐ ┌─────────────┐  │
  │  │Clientes  │ │ Projetos │ │ Comitê/OKRs │  │
  │  │  /       │ │  /       │ │  /          │  │
  │  │briefings │ │campanhas │ │relatorios   │  │
  │  │transcripts│ │artefatos │ │briefings    │  │
  │  │checkins  │ │          │ │             │  │
  │  └──────────┘ └──────────┘ └─────────────┘  │
  └─────────────────────────────────────────────┘
       │
       │ OAuth 2.0 por usuário
       ▼
  Cada membro autentica seu próprio Drive
```

## 2. Conexão (OAuth 2.0)

```json
{
  "mcp": {
    "google-drive": {
      "type": "remote",
      "url": "https://api.google.com/mcp/drive/v3",
      "oauth-client-id": "{env:GOOGLE_OAUTH_CLIENT_ID}",
      "oauth-client-secret": "{env:GOOGLE_OAUTH_CLIENT_SECRET}",
      "scopes": [
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/drive.file"
      ],
      "enabled": true
    }
  }
}
```

**Importante:** Não sincronizamos o Drive inteiro para o VPS. O MCP acessa arquivos sob demanda. Cada usuário faz OAuth na primeira tool call — o navegador abre para autorizar.

## 3. As 8 Ferramentas do Drive MCP

### Pesquisa e Leitura
| Tool | O Que Faz | Quando Usar |
|---|---|---|
| `search_files(query)` | Busca arquivos por nome/conteúdo | Antes de qualquer leitura |
| `read_file_content(fileId)` | Lê conteúdo como texto/markdown | Para acessar briefings, pautas, relatórios |
| `get_file_metadata(fileId)` | Metadados: nome, tipo, data, dono | Verificar versão, autor, data |
| `list_folder_contents(folderId)` | Lista arquivos dentro de uma pasta | Navegar na estrutura do cliente |

### Criação e Escrita
| Tool | O Que Faz | Quando Usar |
|---|---|---|
| `create_file(name, content, parentId)` | Cria arquivo markdown/texto | Salvar resultado de análise, relatório |
| `create_folder(name, parentId)` | Cria pasta | Organizar novo cliente/projeto no Drive |
| `copy_file(fileId, newName, parentId)` | Duplica arquivo | Templates de briefing, pautas |
| `download_file(fileId, format)` | Baixa como PDF/docx | Exportar para compartilhar |

### Permissões (avançado)
| Tool | O Que Faz | Quando Usar |
|---|---|---|
| `get_permissions(fileId)` | Lista quem tem acesso | Auditoria de segurança |
| `update_permissions(fileId, ...)` | Altera permissões | Compartilhar com cliente |

## 4. Estrutura de Pastas Recomendada

```
Drive V4 Company/
├── Clientes/
│   └── {cliente}/
│       ├── Briefings/
│       ├── Transcripts/
│       ├── Check-ins/
│       ├── Relatorios/
│       └── Artefatos/
├── Projetos/
│   └── {projeto}/
│       ├── Briefing/
│       ├── Execucao/
│       └── Entregues/
├── Comite/
│   ├── Dados-consolidados/
│   ├── Briefings-semanais/
│   └── OKRs/
├── Templates/
│   ├── briefing-checkin.md
│   ├── pauta-reuniao.md
│   └── relatorio-semanal.md
└── Skills/
    └── (skills compartilhadas do Builders Hub)
```

## 5. Como os Agentes Usam

| Agente | Lê do Drive | Escreve no Drive |
|---|---|---|
| **@account-checkin-roleplay** | Pautas, mission-control, histórico | — |
| **@account-checkin-review** | Transcript da call | Resumo do check-in |
| **@copy-content** | Briefing de campanha, links | Rascunho da LP, versões |
| **@executor-comite** | Dados consolidados (do n8n) | Briefing formatado + HTML |
| **@analista-dados** | OKRs, relatórios anteriores | Análise atualizada |
| **@pesquisador** | Briefing de cliente | Pesquisa profunda |

## 6. Pontes com Ekyte

Drive e Ekyte **não se conectam diretamente**. A ponte é feita pelo agente ou pelo n8n:

```
Agente lê briefing no Drive
  → Ekyte MCP cria tarefa baseada no briefing
  → Comentário na tarefa com link do Drive

n8n ouve webhook do Ekyte (tarefa concluída)
  → n8n cria PDF no Drive com resultado
  → n8n comenta na tarefa com link do Drive
```

---

**Documentos relacionados:**
- [01-fundacional/02-mcp-ecossistema.md](../01-fundacional/02-mcp-ecossistema.md) — Como MCPs se combinam
- [04-ekyte-mcp.md](04-ekyte-mcp.md) — Tools do Ekyte
