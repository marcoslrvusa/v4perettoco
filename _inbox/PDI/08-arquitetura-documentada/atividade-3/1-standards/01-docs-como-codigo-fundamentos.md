# Docs como Código: Fundamentos Praticados Aqui

## 1. Princípio

Documentação e código do mesmo repo: mesmo git, mesmo PR, mesmo revisor. Diagrama fora do git não existe oficialmente.

## 2. Regras adotadas

- Todo diagrama e texto (Mermaid) dentro de `.md`, nunca imagem solta sem fonte.
- Diagrama mora perto do que descreve: fluxo de coleta ao lado do worker, não em wiki distante.
- PR que muda comportamento atualiza o diagrama no mesmo PR, cobrado no checklist.
- Arquivo de desenho editável (draw.io, figma export) só vale como rascunho; o oficial e o Mermaid no repo.

## 3. O que versionar e o que não versionar

| Versiona no repo | Não versiona |
|------------------|--------------|
| Mermaid de fluxos críticos | Prints de dashboard |
| C4 em DSL + espelho Mermaid | Rascunho de whiteboard |
| ADRs | Ata de reunião solta |
| Matriz de ownership (atividade 4) | Planilha de desenho sem fonte |

## 4. Validação no CI

Quebrar o build em bloco Mermaid com sintaxe inválida. Ferramenta sugerida: `mermaid-cli` (`mmdc`) rodando nos arquivos `.md` alterados no PR. Semântica (o desenho está certo) continua com o revisor humano e o checklist de docs vivos.
