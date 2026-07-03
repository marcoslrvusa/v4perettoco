---
name: create-opencode-plugin
description: Create OpenCode plugins using the @opencode-ai/plugin SDK. Use for building custom tools, event hooks, auth providers, or tool execution interception.
---

# Creating OpenCode Plugins

Create OpenCode plugins using the `@opencode-ai/plugin` SDK.

## Plugin Structure

```
.opencode/plugin/<name>/
├── index.ts          # Entry point, exports Plugin
├── types.ts          # TypeScript types/interfaces
├── utils.ts          # Shared utilities
├── hooks/            # Hook implementations
└── tools/            # Custom tool definitions
```

### Basic Plugin

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({ project, client, $ }) => {
  return {
    // Hook implementations
  }
}
```

### Plugin Locations
- **Project**: `.opencode/plugin/<name>/index.ts` (team-shared)
- **Global**: `~/.config/opencode/plugin/<name>/index.ts` (personal)

## What's Feasible

- Intercepting/blocking tool calls
- Reacting to events (file edits, session completion)
- Adding custom tools for the LLM
- Modifying LLM parameters
- Custom auth flows for providers
- Displaying status messages

## What's NOT Feasible

- Modifying TUI rendering or layout
- Adding new built-in tools (requires OC source)
- Changing core agent behavior/prompts
- Intercepting assistant responses mid-stream
- Adding new keybinds or commands
