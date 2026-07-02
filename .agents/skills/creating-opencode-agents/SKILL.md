---
name: creating-opencode-agents
description: Use when creating OpenCode agents - provides markdown format with YAML frontmatter, mode/tools/permission configuration, and best practices for specialized AI assistants.
---

# Creating OpenCode Agents

Expert guidance for creating OpenCode AI agents with proper configuration, tools, and permissions.

## Quick Reference

### File Location
- **Project**: `.opencode/agent/<name>.md`
- **Global**: `~/.config/opencode/agent/<name>.md`

### Minimal Agent Structure
```markdown
---
description: Brief explanation of the agent's purpose
mode: all
---
System prompt content here...
```

### Required Fields
- **`description`** (string): Brief explanation of the agent's purpose (REQUIRED)

### Optional Fields
| Field | Type | Description |
|-------|------|-------------|
| `mode` | `primary` \| `subagent` \| `all` | How agent can be used (default: `all`) |
| `model` | string | Override model |
| `temperature` | number | Response randomness 0.0-1.0 |
| `maxSteps` | number | Maximum iterations |
| `tools` | object | Enable/disable tools with boolean values |
| `permission` | object | Tool access: `ask`, `allow`, or `deny` |
| `disable` | boolean | Deactivate the agent |

### Agent Modes
- **`primary`**: Main assistant, switchable via Tab
- **`subagent`**: Specialized, invoked by @mentions
- **`all`**: Default; usable in both contexts

## Tools Configuration

| Tool | Description |
|------|-------------|
| `read` | Read file contents |
| `write` | Create new files |
| `edit` | Modify existing files |
| `bash` | Execute shell commands |
| `grep` | Search file contents |
| `glob` | Find files by pattern |
| `webfetch` | Fetch web content |
| `websearch` | Search the web |

## Permission Configuration

```yaml
permission:
  edit: ask
  bash: deny
  webfetch: allow
```

Per-command bash permissions:
```yaml
permission:
  bash:
    "git push": ask
    "git *": allow
    "npm test": allow
    "*": deny
```

## Best Practices

- Use **kebab-case** for agent names
- Grant minimum necessary tools
- Use permissions to restrict dangerous operations
- Disable bash for read-only agents
- Be specific in prompts
