import type { Plugin } from "@opencode-ai/plugin"

const FREE_MODELS = [
  { id: "deepseek-v4-flash-free",    name: "DeepSeek V4 Flash Free",  tags: ["Código", "Tool calling", "Coding geral"],                             vision: false, default: true },
  { id: "nemotron-3-ultra-free",     name: "Nemotron 3 Ultra Free",   tags: ["📷 Visão", "Imagens", "NVIDIA", "Reasoning"],                         vision: true,  default: false },
  { id: "minimax-m2.5-free",         name: "MiniMax M2.5 Free",       tags: ["Leve", "Rápido", "Contexto curto", "Small model"],                   vision: false, default: false },
  { id: "mimo-v2.5-free",            name: "MiMo V2.5 Free",          tags: ["Leve", "Respostas rápidas"],                                          vision: false, default: false },
  { id: "laguna-s-2.1-free",         name: "Laguna S 2.1 Free",      tags: ["Uso geral", "Equilíbrio"],                                            vision: false, default: false },
  { id: "ling-3.0-flash-free",       name: "Ling 3.0 Flash Free",    tags: ["Flash rápido", "Resp. curtas"],                                       vision: false, default: false },
  { id: "north-mini-code-free",      name: "North Mini Code Free",   tags: ["Código leve", "Snippets"],                                            vision: false, default: false },
  { id: "big-pickle-free",           name: "Big Pickle Free",        tags: ["Stealth", "Experimental"],                                            vision: false, default: false },
]

export const Plugin: Plugin = async () => {
  return {
    tools: [
      {
        name: "list-zen-models",
        description: "Lista os modelos free do OpenCode Zen com especialidades. Use quando o usuario perguntar sobre modelos disponiveis, qual modelo usar, ou o que cada modelo faz de melhor.",
        parameters: {
          type: "object",
          properties: {
            filterVision: {
              type: "boolean",
              description: "Se true, retorna apenas modelos com suporte a visao (leitura de imagens)"
            },
            filterCode: {
              type: "boolean",
              description: "Se true, retorna apenas modelos especializados em codigo"
            }
          }
        },
        handler: async ({ filterVision, filterCode }) => {
          let models = [...FREE_MODELS]

          if (filterVision) models = models.filter(m => m.vision)
          if (filterCode) models = models.filter(m => m.tags.some(t => t.toLowerCase().includes("código")))

          return models.map(m => {
            const tagStr = m.tags.map(t => `[${t}]`).join(" ")
            const visionStr = m.vision ? " ✅ Le imagens" : ""
            const defaultStr = m.default ? " ← Padrão atual" : ""
            return `ID: opencode/${m.id}\n   ${m.name} ${tagStr}${visionStr}${defaultStr}`
          }).join("\n\n")
        }
      },
      {
        name: "current-zen-model",
        description: "Mostra qual modelo do OpenCode Zen esta ativo no momento e sugere trocas se necessario. Use quando o usuario perguntar qual modelo esta rodando.",
        parameters: { type: "object", properties: {} },
        handler: async () => {
          return `Modelo atual: opencode/deepseek-v4-flash-free (padrao)\n  DeepSeek V4 Flash Free [Código] [Tool calling] [Coding geral]\n\nPara ler imagens, troque para:\n  opencode/nemotron-3-ultra-free [📷 Visão] [Imagens] [NVIDIA]\n\nUse /models no chat para selecionar outro modelo interativamente.`
        }
      }
    ]
  }
}
