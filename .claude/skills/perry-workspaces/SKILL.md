---
name: perry-workspaces
description: Create and manage isolated Docker workspaces on your tailnet with Claude Code and OpenCode pre-installed.
---

# Perry Workspaces

Create and manage isolated Docker workspaces with Claude Code and OpenCode pre-installed.

## Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/gricha/perry/main/install.sh | bash

# Run agent
perry agent run

# Create workspace
perry start my-proj --clone git@github.com:user/repo.git

# Shell into it
perry shell my-proj
```

## OpenCode Workflow

```bash
opencode attach http://my-proj:4096
```

OpenCode is reachable at `http://<workspace>:4096` from any device on the tailnet.

## SSH Access

```bash
ssh workspace@my-proj
```

Username is always `workspace`. Workspaces registered on tailnet by name.
