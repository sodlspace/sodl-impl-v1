---
title: Language Reference
description: Complete reference for the SODL language constructs.
---

SODL has five top-level constructs: `template`, `system`, `interface`, `module`, and `pipeline`.

All constructs support nested blocks for configuration, constraints, and documentation.

## Quick reference

| Construct | Purpose |
|---|---|
| `template` | Reusable base with shared stack and policies |
| `system` | Main system definition; extends a template |
| `interface` | Data contracts and component contracts |
| `module` | Groups related functionality with ownership |
| `pipeline` | Ordered steps for code generation or deployment |

## File structure

A SODL file typically follows this order:

```sodl
# 1. Templates (reusable bases)
template "Base":
  stack: ...
  policy ...: ...

# 2. Interfaces (contracts)
interface MyInterface:
  method render() -> str

# 3. System definition
system "MySystem" extends "Base":
  version = "1.0.0"
  stack: ...
  intent: ...

  # 4. Nested interfaces (scoped to system)
  interface InnerInterface extends MyInterface:
    ...

  # 5. Modules (within system)
  module MyModule:
    ...

  # 6. Pipelines
  pipeline "Production":
    step Build: ...
```

See the detailed pages for each construct:

- [Syntax reference](/language/syntax/)
- [Constructs in depth](/language/constructs/)
