---
name: flow-next-opencode-work
description: Execute a Flow epic or task systematically with git setup, task tracking, quality checks, and commit workflow. Use when implementing a plan or working through a spec.
---

# Flow work

Execute a plan systematically. Focus on finishing.

Uses `.flow/` for ALL task tracking via `flowctl` (bundled in `.opencode/bin/flowctl`).

## Workflow

1. Parse options (branch mode, review mode)
2. Read phases from `phases.md`
3. Execute each phase in order
4. Run review if configured
5. Verify gates (tests, quality checks)

## Ralph Mode

When `FLOW_RALPH=1`: use `flowctl done` to verify task status before committing, `git add -A` always.
