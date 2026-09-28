# Docs como Codigo: Fundamentos Praticados Aqui

## 1. Principio

Documentacao e codigo do mesmo repo: mesmo git, mesmo PR, mesmo revisor. Diagrama fora do git nao existe oficialmente.

## 2. Regras adotadas

- Todo diagrama e texto (Mermaid) dentro de `.md`, nunca imagem solta sem fonte.
- Diagrama mora perto do que descreve: fluxo de coleta ao lado do worker, nao em wiki distante.
- PR que muda comportamento atualiza o diagrama no mesmo PR, cobrado no checklist.
- Arquivo de desenho editavel (draw.io, figma export) so vale como rascunho; o oficial e o Mermaid no repo.

## 3. O que versionar e o que nao versionar

| Versiona no repo | Nao versiona |
|------------------|--------------|
| Mermaid de fluxos criticos | Prints de dashboard |
| C4 em DSL + espelho Mermaid | Rascunho de whiteboard |
| ADRs | Ata de reuniao solta |
| Matriz de ownership (atividade 4) | Planilha de desenho sem fonte |

## 4. Validacao no CI

Quebrar o build em bloco Mermaid com sintaxe invalida. Ferramenta sugerida: `mermaid-cli` (`mmdc`) rodando nos arquivos `.md` alterados no PR. Semantica (o desenho esta certo) continua com o revisor humano e o checklist de docs vivos.
