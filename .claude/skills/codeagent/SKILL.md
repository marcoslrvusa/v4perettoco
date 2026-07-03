---
name: codeagent
description: Execute codeagent-wrapper for multi-backend AI code tasks. Supports Codex, Claude, Gemini, and OpenCode backends with agent presets, skill injection, file references (@syntax), worktree isolation, parallel execution, and structured output.
---

# Codeagent Wrapper

Multi-backend AI code task executor with agent presets, skill injection, and parallel orchestration.

## Backends

| Backend | Best For |
|---------|----------|
| Codex | Deep code analysis, complex logic, large refactoring |
| Claude | Documentation, prompt engineering, clear-requirement features |
| Gemini | UI/UX prototyping, design system implementation |
| OpenCode | Lightweight tasks |

## Agent Presets

Bundle backend, model, prompt, and tool control into a reusable name.

| Agent | Purpose | Read-Only |
|-------|---------|-----------|
| code-explorer | Trace code, map architecture | Yes |
| code-architect | Design approaches, build sequences | Yes |
| code-reviewer | Review for bugs, conventions | Yes |
| develop | Implement code, run tests | No |

## Skill Injection

Auto-detected from working directory (package.json → frontend-design, go.mod → golang-best-practices, etc.) or manually specified.

## Parallel Execution

Topologically sorted tasks with dependency resolution. Independent tasks run concurrently.

## Worktree Isolation

Execute in isolated git worktree to keep changes separate.
