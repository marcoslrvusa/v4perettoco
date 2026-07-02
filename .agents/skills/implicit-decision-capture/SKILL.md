---
name: implicit-decision-capture
description: Automatically capture implicit technical decisions and uncertainties encountered by AI agents during coding work. This skill logs decision points where the agent chose an approach without explicit user guidance, enabling later review and context enrichment.
---

# Implicit Decision Capture

Automatically capture implicit technical decisions and uncertainties encountered by AI agents during coding work.

## When to Use

Use proactively during any coding task to track "what choices I made and why."

- When the agent chooses between alternatives without explicit guidance
- When trade-offs are encountered (performance vs readability, etc.)
- When assumptions are made about the codebase
- When uncertainty exists about the best approach

## Decision Log Format

```markdown
## Decision: [title]
- **Context**: What was being done
- **Options considered**: [alternative A, alternative B]
- **Chosen approach**: [what was selected]
- **Rationale**: [why this option won]
- **Uncertainty**: [what's still unknown]
- **Date**: [ISO-8601]
```

## Patterns

- **Architecture decisions**: Framework choice, pattern selection
- **Implementation decisions**: Algorithm choice, library selection
- **Trade-off decisions**: Speed vs quality, scope decisions
- **Assumption decisions**: What was assumed about the domain
