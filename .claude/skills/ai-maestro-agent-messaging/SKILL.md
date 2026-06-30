---
name: ai-maestro-agent-messaging
description: Send and receive messages between AI agents using AI Maestro's messaging system. Use when the user asks to "send a message", "check inbox", "read messages", "notify [agent]", "tell [agent]", or any inter-agent communication.
---

# AI Maestro Agent Messaging

Send and receive messages between AI agents using AI Maestro's messaging system.

## When to Use

- Sending messages between agents
- Checking inbox for agent communications
- Reading messages from other agents
- Notifying agents of events or state changes
- Coordinating multi-agent workflows

## Architecture

Agents communicate through a message bus:
1. **Producer agent** sends a message with type, payload, and target
2. **Message bus** routes the message to the correct queue
3. **Consumer agent** picks up and processes the message
4. **Response** can be synchronous or asynchronous

## Message Format

```json
{
  "from": "agent-name",
  "to": "target-agent",
  "type": "task|notification|query|response",
  "payload": {},
  "correlation_id": "uuid",
  "timestamp": "ISO-8601"
}
```

## Patterns

- **Request/Response**: Agent A sends task, Agent B processes and responds
- **Broadcast**: Agent notifies all other agents of state change
- **Pipeline**: Sequential processing through multiple agents
- **Supervisor**: Orchestrator dispatches and collects results
