# Especificação Padrão de Entrega — PDI 2026 (Builders Hub)

Cada atividade de PDI deve ser entregue em uma pasta própria seguindo este padrão,
idêntico às atividades 1 e 2 já homologadas (anteriormente `PDI - A1` e `PDI-MARTECH`).

## Estrutura de pastas (por módulo)

```
_inbox/PDI/{NN-modulo}/
├── README.md                                  ← card do módulo (template abaixo)
└── atividade-{N}/
    ├── README.md                              ← resumo da atividade (padrão A1/A2)
    ├── 1-standards/                           ← documentação / padrões / análise
    ├── 2-*/3-*/4-*/5-*/6-*                    ← entregas técnicas da atividade
    │                                            (nomes variam por atividade:
    │                                            standards, codigo, workflows, supabase,
    │                                            sql, scripts, testes, retrofit, etc.)
    └── 7-apresentacao/
        ├── DECK-PDI.md                        ← narrativa do deck
        ├── DEMO-SCRIPT.md                     ← roteiro de demonstração
        ├── pdi-{slug}.html                    ← RELATÓRIO (visual padrão obrigatório)
        ├── pdi-{slug}.docx                    ← gerado via gerar-docx.py
        ├── pdi-{slug}.pdf                     ← gerado via headless chrome
        └── gerar-docx.py                      ← script python-docx da atividade
```

## Visual do relatório (obrigatório)

- **Base:** `_templates/template-relatorio-pdi.html` (cópia pronta para usar).
- **Placeholders a substituir:** `{{TITULO}}`, `{{BADGE}}`, `{{MODULO}}`, `{{DATA}}`,
  `{{SLUG}}`, `{{ASSETS_PATH}}`, `{{CONTEXTO}}`, `{{DIAGNOSTICO}}`, `{{SOLUCAO}}`,
  `{{COMO_FUNCIONA}}`, `{{ENTREGAS}}`, `{{METRICAS}}`, `{{STATUS_FINAL}}`.
- **ASSETS_PATH** (para qualquer atividade dentro de `_inbox/PDI/{modulo}/atividade-{N}/7-apresentacao/`):
  `../../../../../` e em seguida `assets/...`. Ou seja `../../../../../assets/logo-peretto.png`.
- **CAPA:** logo Peretto (`assets/logo-peretto.png`) + foto circular
  (`assets/images/logo-peretto-perfil.jpg`) + badge + título + meta (Autor: Marcos Luciano;
  Unidade: FV Marketing / V4 Company — Automação & Infraestrutura; Status: NÃO publicado).
- **Seção "Como funciona":** usar o box `.pipeline` com animação de pulsos (cópia do
  template/atividade 2). Toda atividade com fluxo de engenharia DEVE ter este box.
- Seções numeradas: 1 Contexto, 2 Diagnóstico, 3 Solução, 4 Como funciona, 5 Entregas,
  6 Métricas de sucesso + callout final de status.
- Tabelas/styling já no template. Todo `Gerar` conteúdo técnico REAL e específico da
  atividade — nunca deixar placeholder preenchido de forma genérica.
- Nome do relatório: `pdi-{slug}.html` onde `{slug}` é a atividade (ex.: `pdi-solidez-clean-code-a1`).

## README da atividade (padrão A1/A2)

Precisa ter: título, quadro de metadados (Área: Automação & Infraestrutura; Unidade;
Autor Marcos Luciano/Perettoco; Data; Status), "Entregas desta PDI" com o diagrama de
árvore (1-standards…7-apresentacao), "Problema Resolvido", "Arquitetura Resumida"
(reprodução esqueemática), "Próximos Passos" e tabela "Métricas de Sucesso" (Atual/Meta).

## README do módulo (card)

```markdown
# PDI — {Título do Módulo}

> **Área:** Automação & Infraestrutura
> **Autor:** Marcos Perettoco
> **Perfil:** Tech Lead Sênior L2 / GPTS
> **Período:** Presencial de {agosto–dezembro} 2025
> **Status:** {Em desenvolvimento / Entregue}

Módulo com {N} atividades. Cada atividade na própria pasta `atividade-{N}/`.

| Atividade | Foco | Pasta |
|-----------|------|-------|
| 1 … | … | `atividade-1/` |
| 2 … | … | `atividade-2/` |
| … | … | … |
```

## DOCX — gerar-docx.py

Copiar e adaptar o `gerar-docx.py` da atividade 2 (python-docx, capa + seções + tabelas,
paleta #8b4513/#1a1f24/#6b7a8a). Executar para gerar `pdi-{slug}.docx` na mesma pasta.

## PDF

Gerar via Chrome headless (disponível em `/usr/bin/google-chrome`):

```bash
google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf="$(pwd)/pdi-{slug}.pdf" \
  "file://$(pwd)/pdi-{slug}.html"
```

> Verificação: `file` deve retornar "PDF document".