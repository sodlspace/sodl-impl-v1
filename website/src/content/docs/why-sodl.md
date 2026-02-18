---
title: Why SODL
description: The problem with free-form AI prompts and how structured specifications fix it.
---

## The problem with free-form prompts

When you ask an AI to "build a REST API for a task management app", the AI makes dozens of implicit decisions:

- Which framework? Express, Fastify, Hono?
- SQL or NoSQL?
- JWT or session-based auth?
- What error handling strategy?
- What file structure?

The AI doesn't know what _you_ want. It guesses. And each follow-up prompt resets context, leading to inconsistency, drift, and rework.

## Structured context changes everything

SODL gives AI agents a structured specification that answers these questions upfront:

```sodl
system "TaskAPI":
  stack:
    language  = "TypeScript"
    framework = "Hono"
    database  = "PostgreSQL"
    auth      = "JWT"

  intent:
    primary  = "REST API for task management"
    out_of_scope = ["Real-time", "File uploads"]

  policy Security:
    rule "All endpoints require JWT validation" severity=high
    rule "No direct SQL string interpolation" severity=high
```

Now every AI generation call — whether it's the first or the fiftieth — has the same ground truth.

## What SODL provides

### Intent clarity

The `intent` block captures _what_ and _why_. The AI understands the purpose of the system before it writes any code.

### Architectural constraints

The `stack` block locks in technology choices. The `policy` blocks enforce rules that must never be violated.

### Module boundaries

The `module` construct defines ownership and artifact paths, preventing the AI from scattering code across the project.

### Generation pipelines

The `pipeline` construct orchestrates multi-step generation with explicit gates — ensuring each step passes before the next begins.

## SODL vs alternatives

| Approach | Consistency | Reusability | AI-native |
|---|---|---|---|
| Free-form prompts | ❌ | ❌ | ✅ |
| README docs | ⚠️ | ⚠️ | ❌ |
| OpenAPI / schemas | ✅ | ✅ | ⚠️ |
| **SODL** | ✅ | ✅ | ✅ |

SODL is designed specifically for AI code generation — not for humans to read, not for machines to execute, but for AI agents to understand and act on.

## Who benefits most

- **Teams using Cursor** who want consistent AI outputs across developers
- **Developers building with Claude or GPT** who want reproducible results
- **Architects** who want to encode decisions once and enforce them everywhere
