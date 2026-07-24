# Lições Aprendidas — Hub de Agentes

## 23/07/2026 — HOME=/workspace + entrypoint corrompeu workspace em produção

### O que aconteceu

5 commits foram empurrados direto pra `main` do `hub-agentes-ia`:
`43080fd` (HOME=/workspace), `44ec346` (cópia scripts), `9be1fe1`/`92f66ec`/`2a8db27` (consulta-banco).

O commit `43080fd` mudou `HOME=/workspace` em todos os 6 serviços OpenCode no docker-compose. Isso fez o OpenCode runtime escrever arquivos de estado/config dentro de `/workspace/`. No restart, o entrypoint tentava `git pull --ff-only`, detectava sujeira no repositório, e eventualmente o workspace era destruído e clonado do zero — levando junto estado, histórico de sessão e dados de usuário.

### Causa raiz

1. **Mudança de `HOME` sem entender o efeito cascata**: `HOME=/workspace` faz OpenCode buscar config/state dentro do repositório clonado. Os volumes Docker montam em `/home/node/`, não em `/workspace/`. Qualquer escrita do OpenCode no workspace polui o git e quebra pull.
2. **Trabalho feito no clone errado**: havia dois clones locais do mesmo repositório (`hub-agentes-ia/` e `hub-agentes-infra-unify/`), em estados diferentes. O trabalho foi feito no `hub-agentes-infra-unify` (que estava à frente) e empurrado, enquanto o `hub-agentes-ia` ficou para trás.
3. **Push direto na `main` sem branch intermediária**: toda alteração que afeta entrypoint, Dockerfile ou docker-compose DEVE ir para uma branch de teste primeiro.

### Guardrails (regras para TODAS as sessões futuras)

1. **NUNCA mude `HOME` em variáveis de ambiente de container** sem validar que OpenCode e entrypoint usam paths absolutos (`/home/node/...`), não relativos a `$HOME`.
2. **NUNCA empurre direto pra `main`** alterações em `infra/entrypoint.sh`, `infra/Dockerfile.opencode`, `docker-compose.agentes.yml` ou `infra/auth/`. Use uma branch (`fix/...` ou `feat/...`), teste em staging, só depois mergeie.
3. **SEMPRE verifique qual clone local está sendo usado** (`git remote -v` + `git log -1`). Os dois clones (`hub-agentes-ia` e `hub-agentes-infra-unify`) apontam pro mesmo remote — manter sincronizados ou eliminar a duplicidade.
4. **SEMPRE leia o entrypoint.sh completo** antes de fazer qualquer alteração que afete paths de arquivo. O entrypoint tem lógica destrutiva (`rm -rf /workspace/*`) se detectar inconsistência.
5. **Workspace NÃO é lugar para state**: OpenCode state (state.json, projects.json) vive em volume Docker (`/home/node/.local/share/opencode`), NÃO em `/workspace/`. Qualquer escrita no workspace é perdida no próximo `git pull` / restart.
6. **Antes de commitar qualquer alteração que afete a produção, execute:** `git log --oneline -5` + `git diff --stat` e descreva em voz alta o que cada arquivo alterado faz.

### Diagnóstico rápido se workspace quebrar de novo

```
# Dentro do container:
ls -la /workspace/.git              # .git existe?
ls /workspace/.config/opencode/     # Tem config fantasma aqui?
echo $HOME                           # HOME ainda é /workspace?
git -C /workspace status --short    # Untracked files poluindo?
```
