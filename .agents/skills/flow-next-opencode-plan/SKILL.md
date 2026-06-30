---
name: flow-next-opencode-plan
description: Create structured build plans from feature requests or Flow IDs. Use when planning features or designing implementation.
---

# Flow plan

Turn a rough idea into an epic with tasks in `.flow/`. This skill does not write code.

**The Golden Rule: No Implementation Code.** Plans are specs, not implementations.

## Input Types
- Feature/bug description in natural language
- Flow epic ID `fn-N` to refine existing epic
- Flow task ID `fn-N.M` to refine specific task

## Depth Options
- **Short**: problem, acceptance, key context only
- **Standard**: + approach, risks, test notes (default)
- **Deep**: + phases, alternatives, rollout plan

## Workflow
1. Parse options (depth, research, review)
2. Run research subagents in parallel
3. Create epic with tasks via `flowctl`
4. Run plan review if configured
