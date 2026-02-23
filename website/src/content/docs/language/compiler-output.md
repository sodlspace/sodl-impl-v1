---
title: Compiler & Output
description: How the SODL compiler works today and what it will produce.
---

## Current state

The SODL compiler currently acts as a **parser and validator**. Running `sodl compile` against a spec file checks syntax, resolves dependencies, and validates interface contracts — but does not yet write output files.

```bash
# Validate syntax and structure
sodl validate spec.sodl

# Full compile (validation + dependency check)
sodl compile spec.sodl
```

What the compiler validates today:
- Syntax correctness (indentation, colons, quotes)
- All `requires` references resolve to an `exports` or `implements`
- No circular dependencies between modules
- Interface contracts (all declared methods present)
- Module name uniqueness

---

## Planned output (roadmap)

The compiler's output generator is in development. Once complete, `sodl compile` will write a structured set of markdown files that AI coding agents can consume directly:

```
.sodl/
├── global.md          # System-level context for the AI agent
├── modules/
│   ├── AuthAPI.md     # Per-module generation instructions
│   ├── UserAPI.md
│   └── ...
├── steps/
│   ├── Implement__AuthAPI.md   # Step-scoped instructions per module
│   └── ...
└── manifest.json      # Metadata: module graph, pipeline order, version
```

### global.md

Contains the system-level context that applies to every generation call:

- Stack choices (language, framework, database, auth)
- System intent and out-of-scope boundaries
- All active policies with their rules and severities
- Interface contracts that modules must fulfill

### modules/ModuleName.md

Per-module instructions the AI reads when generating that module:

- What this module owns and is responsible for
- Which interfaces it implements (with full method signatures)
- Module-level invariants and constraints
- Acceptance criteria the generated code must satisfy
- Artifact paths to write to

### steps/StepName__ModuleName.md

Combines step-level context with module-level instructions for a specific pipeline step:

- Which output type this step produces (`code`, `tests`, etc.)
- The `require` condition for this step
- The `gate` the output must pass before the next step

### manifest.json

Machine-readable metadata:

```json
{
  "system": "UserManagementAPI",
  "version": "1.0.0",
  "modules": ["AuthAPI", "UserAPI"],
  "pipeline": "Production",
  "steps": ["ImplementAuth", "ImplementUsers"]
}
```

---

## Intended workflow (once generator ships)

```
Write .sodl spec
       │
       ▼
sodl validate spec.sodl
  └─ fix any errors
       │
       ▼
sodl compile spec.sodl
  └─ generates .sodl/ output folder
       │
       ▼
Feed output files to AI agent
  └─ @.sodl/global.md build the AuthAPI module
       │
       ▼
AI generates code guided by structured spec
  └─ constrained by policies, interfaces, invariants
```

The key insight: instead of writing a one-off prompt, you write a spec once and the compiler turns it into structured, reusable AI instructions. Every generation call — first or fiftieth — uses the same ground truth.

---

## Using the compiler today

Until the generator is complete, you can use SODL specs directly as context for your AI coding tool:

```
# Cursor
@spec.sodl build the AuthAPI module

# Claude
Attached: spec.sodl — implement the UserRepository interface
```

The spec file itself is human-readable and gives AI agents the same information the compiled output will contain — it just requires the agent to parse it directly rather than reading pre-compiled markdown.
