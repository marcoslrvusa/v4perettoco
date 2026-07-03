---
name: station
description: Use Station CLI (`stn`) for AI agent orchestration - creating agents, running tasks, managing environments, and deploying agent teams. Prefer CLI for file operations and exploration; use MCP tools for programmatic agent execution and detailed queries.
---

# Station CLI

Station is a self-hosted AI agent orchestration platform. You interact with it via the `stn` CLI or MCP tools.

## CLI vs MCP Tools

| Task | Use CLI | Use MCP Tool |
|------|---------|--------------|
| Create/edit agent files | `stn agent create` | - |
| Run an agent | `stn agent run <name> "<task>"` | `call_agent` |
| List agents/environments | `stn agent list` | `list_agents` |
| Add MCP servers | `stn mcp add <name>` | `add_mcp_server_to_environment` |
| Sync configurations | `stn sync <env>` | - |
| Deploy | `stn deploy <env>` | - |

## Agent File Format (dotprompt)

```yaml
---
metadata:
  name: "my-agent"
  description: "What this agent does"
model: gpt-4o-mini
max_steps: 8
tools:
  - "__tool_name"
---
{{role "system"}}
You are a helpful agent that [purpose].

{{role "user"}}
{{userInput}}
```

## Multi-Agent Hierarchy (Coordinator Pattern)

```yaml
---
metadata:
  name: "coordinator"
  description: "Orchestrates specialist agents"
model: gpt-4o-mini
max_steps: 20
agents:
  - "specialist-a"
  - "specialist-b"
---
{{role "system"}}
You coordinate specialists.
Delegate using __agent_<name> tools, then synthesize results.
{{role "user"}}
{{userInput}}
```

## MCP Server Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@package/mcp-server"],
      "env": { "API_KEY": "{{.API_KEY}}" }
    }
  }
}
```

## Common Workflows

1. **Create New Agent**: Write .prompt file → `stn sync` → `stn agent run`
2. **Add External Tools**: `stn mcp add` → `stn sync` → tools available to agents
3. **Create Agent Team**: Specialist agents + coordinator with `agents:` field
4. **Install Bundles**: `stn bundle install` for pre-built agent teams
5. **Deploy**: `stn deploy <env> --target fly|k8s|ansible`
