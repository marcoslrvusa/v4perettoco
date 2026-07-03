---
name: new-agent-creation
description: Provides step-by-step templates and guidance for creating new AI agents in Unite-Hub with proper registration, testing, and governance.
---

# New Agent Creation

Step-by-step template for creating new AI agents with proper registration, testing, and governance.

## Quick Start Template

### 1. Create Agent File

Extend BaseAgent with `processTask()` method implementing your agent logic.

### 2. Register in Orchestrator

Add to intent enum and routing logic so the orchestrator knows when to call this agent.

### 3. Add to Registry

Register in `registry.json` with id, name, version, capabilities, queue name, models, governance mode, budget limits.

### 4. Create Tests

Write tests with 100% pass rate before deployment.

## Checklist

- [ ] Create agent file extending BaseAgent
- [ ] Implement processTask() method
- [ ] Add to orchestrator routing
- [ ] Register in registry.json
- [ ] Create tests (100% pass required)
- [ ] Set budget limits
- [ ] Choose governance mode (HUMAN_GOVERNED vs AUTONOMOUS)
- [ ] Document in agent.md

**Standard**: All agents must filter by workspace_id, respect budgets, pass verification.
