version: '3.8'

# ============================================================
# V4 Agents Hub — Stack completa para Dokploy
# ============================================================
# Domínios:
#   auth.fvmarketing.com.br         → Authelia (tela de login)
#   opencode.fvmarketing.com.br     → opencode-login → roteia pro user
#
# FASE 1: Só subir authelia-redis + authelia + opencode-login
#         (opencode-web containers sobem depois)
# ============================================================

services:
  # ─── Redis (Sessões do Authelia) ───
  authelia-redis:
    image: redis:7-alpine
    container_name: authelia-redis
    networks:
      - dokploy-network
    volumes:
      - authelia_redis_data:/data
    command: ["redis-server", "--appendonly", "yes"]
    restart: unless-stopped

  # ─── Authelia (Tela de Login) ───
  authelia:
    image: authelia/authelia:latest
    container_name: authelia
    depends_on:
      - authelia-redis
    networks:
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=dokploy-network"
      - "traefik.http.routers.authelia.rule=Host(`auth.fvmarketing.com.br`)"
      - "traefik.http.services.authelia.loadbalancer.server.port=9091"
      - "traefik.http.routers.authelia.tls=true"
      - "traefik.http.routers.authelia.tls.certresolver=letsencrypt"
    volumes:
      - ./projetos/infraestrutura/authelia/config:/config:ro
    restart: unless-stopped

  # ─── Login App (Proxy + Roteador) ───
  opencode-login:
    build:
      context: ./projetos/infraestrutura/opencode-login
      dockerfile: Dockerfile
    container_name: opencode-login
    environment:
      - PORT=3000
      - SESSION_SECRET=${SESSION_SECRET}
      - USERS_PATH=/app/users.json
      - NODE_ENV=production
    networks:
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=dokploy-network"
      - "traefik.http.routers.opencode.rule=Host(`opencode.fvmarketing.com.br`)"
      - "traefik.http.services.opencode.loadbalancer.server.port=3000"
      - "traefik.http.routers.opencode.tls=true"
      - "traefik.http.routers.opencode.tls.certresolver=letsencrypt"
      - "traefik.http.routers.opencode.middlewares=opencode-auth"
      - "traefik.http.middlewares.opencode-auth.forwardAuth.address=http://authelia:9091/api/verify?auth=forwarded"
      - "traefik.http.middlewares.opencode-auth.forwardAuth.trustForwardHeader=true"
      - "traefik.http.middlewares.opencode-auth.forwardAuth.authResponseHeaders=Remote-User,Remote-Groups,Remote-Email"
    volumes:
      - ./projetos/infraestrutura/opencode-login/users.json:/app/users.json:ro
    depends_on:
      - authelia
    restart: unless-stopped

  # ─── OpenCode Web — marcos.luciano ───
  opencode-web-marcos-luciano:
    image: node:22-bookworm
    container_name: opencode-web-marcos-luciano
    command: >
      bash -c "apt-get update && apt-get install -y git curl sudo && 
      npm install -g opencode-ai && 
      opencode web --hostname 0.0.0.0 --port 4096"
    networks:
      - dokploy-network
    volumes:
      - opencode_workspace_marcos_luciano:/workspace
      - opencode_config_marcos_luciano:/root/.config/opencode
    working_dir: /workspace
    restart: unless-stopped

  # ─── OpenCode Web — fhelipe.aranha ───
  opencode-web-fhelipe-aranha:
    image: node:22-bookworm
    container_name: opencode-web-fhelipe-aranha
    command: >
      bash -c "apt-get update && apt-get install -y git curl sudo && 
      npm install -g opencode-ai && 
      opencode web --hostname 0.0.0.0 --port 4096"
    networks:
      - dokploy-network
    volumes:
      - opencode_workspace_fhelipe_aranha:/workspace
      - opencode_config_fhelipe_aranha:/root/.config/opencode
    working_dir: /workspace
    restart: unless-stopped

  # ─── OpenCode Web — csm.2 ───
  opencode-web-csm-2:
    image: node:22-bookworm
    container_name: opencode-web-csm-2
    command: >
      bash -c "apt-get update && apt-get install -y git curl sudo && 
      npm install -g opencode-ai && 
      opencode web --hostname 0.0.0.0 --port 4096"
    networks:
      - dokploy-network
    volumes:
      - opencode_workspace_csm_2:/workspace
      - opencode_config_csm_2:/root/.config/opencode
    working_dir: /workspace
    restart: unless-stopped

  # ─── OpenCode Web — csm.3 ───
  opencode-web-csm-3:
    image: node:22-bookworm
    container_name: opencode-web-csm-3
    command: >
      bash -c "apt-get update && apt-get install -y git curl sudo && 
      npm install -g opencode-ai && 
      opencode web --hostname 0.0.0.0 --port 4096"
    networks:
      - dokploy-network
    volumes:
      - opencode_workspace_csm_3:/workspace
      - opencode_config_csm_3:/root/.config/opencode
    working_dir: /workspace
    restart: unless-stopped

  # ─── LiteLLM (Gateway de Modelos) ───
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    container_name: litellm
    networks:
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=dokploy-network"
      - "traefik.http.routers.litellm.rule=Host(`litellm.fvmarketing.com.br`)"
      - "traefik.http.services.litellm.loadbalancer.server.port=4000"
      - "traefik.http.routers.litellm.tls=true"
      - "traefik.http.routers.litellm.tls.certresolver=letsencrypt"
    volumes:
      - ./litellm-config.yaml:/app/config.yaml:ro
    environment:
      - LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY}
      - LITELLM_SALT_KEY=${LITELLM_SALT_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    command: ["--config=/app/config.yaml", "--port=4000"]
    restart: unless-stopped

volumes:
  authelia_redis_data:
  opencode_workspace_marcos_luciano:
  opencode_workspace_fhelipe_aranha:
  opencode_workspace_csm_2:
  opencode_workspace_csm_3:
  opencode_config_marcos_luciano:
  opencode_config_fhelipe_aranha:
  opencode_config_csm_2:
  opencode_config_csm_3:

networks:
  dokploy-network:
    external: true
