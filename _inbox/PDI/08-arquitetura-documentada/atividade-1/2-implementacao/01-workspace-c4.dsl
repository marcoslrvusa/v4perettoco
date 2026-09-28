workspace "Orquestrador de Automacao V4" "C4 do sistema real de automacao FV Marketing" {

  !identifiers hierarchical

  model {
    operador = person "Operador de Automacao" "Cria e monitora fluxos"
    gestor = person "Gestor de Trafego" "Consome relatorios e alertas"

    orq = softwareSystem "Orquestrador de Automacao V4" "Executa fluxos n8n e workers" {
      n8n = container "n8n" "Fluxos, triggers e webhooks" "n8n, porta 5678"
      workers = container "Workers Python" "Coleta e tarefas pesadas" "Python 3.12, porta 8000"
      db = container "Supabase Postgres" "Estado, filas e logs" "Postgres" {
        tags "Database"
      }
      painel = container "Painel Next.js" "Visao e disparo manual" "Next.js, porta 3000"
    }

    meta = softwareSystem "Meta Ads API" "Metricas de campanhas" {
      tags "External"
    }
    gmail = softwareSystem "Gmail API" "Disparo de emails" {
      tags "External"
    }

    operador -> orq.painel "Opera via"
    orq -> gestor "Envia alertas e relatorios"
    orq.painel -> orq.db "Le e grava"
    orq.n8n -> orq.workers "Chama via webhook"
    orq.workers -> orq.db "Le e grava"
    orq.workers -> meta "Coleta metricas"
    orq.n8n -> gmail "Dispara via"
  }

  views {
    systemContext orq "Contexto" {
      include *
      autoLayout
    }
    container orq "Containers" {
      include *
      autoLayout
    }
    styles {
      element "External" {
        background #6b7a8a
      }
      element "Database" {
        shape Cylinder
      }
    }
  }
}
