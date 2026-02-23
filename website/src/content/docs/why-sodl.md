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

## Where SODL delivers the most value

Some workflows benefit more than others. SODL is especially effective when:

- **Building a REST API** — `policy Security` rules enforce auth, validation, and error handling before any endpoint is generated. See [REST API use case](/use-cases/#rest-api-development).
- **Scaffolding a microservice** — `interface` contracts define exactly what each service must implement, preventing implicit coupling. See [microservices use case](/use-cases/#microservices).
- **Running a data pipeline** — pipeline `step` blocks map to ETL stages, and `gate` criteria ensure each stage is proven before the next runs. See [data pipeline use case](/use-cases/#data-pipelines-etl).
- **Working on an existing codebase** — `out_of_scope` keeps the AI from refactoring things you didn't ask it to touch. See [brownfield use case](/use-cases/#brownfield--incremental-refactoring).

For the full breakdown of where SODL excels, see [Use Cases](/use-cases/).

## Who benefits most

- **Teams using Cursor** who want consistent AI outputs across developers and sessions
- **Developers building with Claude or GPT** who want reproducible, constraint-aware results
- **Architects** who want to encode design decisions once and enforce them everywhere
- **Anyone who has re-explained their tech stack to an AI more than twice**
