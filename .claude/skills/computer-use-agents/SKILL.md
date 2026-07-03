---
name: computer-use-agents
description: Build AI agents that interact with computers like humans do - viewing screens, moving cursors, clicking buttons, and typing text. Covers Anthropic's Computer Use, OpenAI's Operator/CUA, and open-source alternatives. Critical focus on sandboxing, security, and handling the unique challenges of vision-based control.
---

# Computer Use Agents

Build AI agents that interact with computers like humans do - viewing screens, moving cursors, clicking buttons, and typing text.

## Perception-Reasoning-Action Loop

The fundamental architecture: observe screen, reason about next action, execute action, repeat.

1. PERCEPTION: Screenshot captures current screen state
2. REASONING: Vision-language model analyzes and plans
3. ACTION: Execute mouse/keyboard operations
4. FEEDBACK: Observe result, continue or correct

## Key Patterns

- **Sandboxed Environment**: Must run in isolated Docker containers with virtual desktops. Network restrictions, read-only filesystem, no host credentials.
- **Browser-Use (Playwright)**: For browser-only automation, structured DOM access is more efficient than pixel-based. Faster, cheaper, more precise.
- **User Confirmation**: Gate sensitive actions (purchases, auth, file ops) through human confirmation.
- **Action Logging**: All actions logged for debugging, security auditing, and reproducibility.
- **Humanized Interaction**: Add variance to click coordinates, delays, and mouse movements to avoid anti-bot detection.

## Sharp Edges

- **Web content can hijack agents**: Prompt injection via page content. Defense: sandboxing, classifier-based detection, user confirmation for sensitive actions.
- **Vision agents click exact centers**: Detectable as non-human. Add Gaussian variance to coordinates.
- **Dropdowns, scrollbars, drags are unreliable**: Use keyboard alternatives when possible.

## Anti-Patterns

- Running without step limits (infinite loops)
- No sandbox (running on host system directly)
- Full resolution screenshots (token explosion)
- Auto-approving all actions
- Not logging rejected actions
