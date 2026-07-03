---
name: flow-next-opencode-interview
description: Interview user in-depth about an epic, task, or spec file to extract complete implementation details. Use when user wants to flesh out a spec, refine requirements, or clarify a feature before building.
---

# Flow interview

Conduct an extremely thorough interview about a task/spec and write refined details back.

## Input Types
- **Flow epic ID** `fn-N`: Fetch with `flowctl show`, write back with `flowctl epic set-plan`
- **Flow task ID** `fn-N.M`: Fetch, write back with `flowctl task set-spec`
- **File path**: Read, interview, rewrite
- **New idea**: Create epic stub, refine requirements

## Interview Process

Ask questions in plain text, grouped 5-8 per message. 40+ questions typical.

## Question Categories

- Problem & scope
- Users & personas
- Technical constraints
- Edge cases
- Performance requirements
- Security considerations
- Dependencies
- Acceptance criteria
