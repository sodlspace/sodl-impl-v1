---
title: Syntax Reference
description: SODL syntax — keywords, blocks, values, and formatting rules.
---

## Comments

Lines starting with `#` are comments:

```sodl
# This is a comment
system "MySystem":  # inline comment
  version = "1.0.0"
```

## Indentation

SODL uses 2-space indentation. Blocks are introduced with a colon (`:`).

```sodl
system "MySystem":
  stack:
    language = "TypeScript"
```

## String values

All string values are double-quoted:

```sodl
primary = "Marketing website for my product"
```

## Array values

Arrays use bracket syntax with double-quoted items:

```sodl
outcomes = [
  "Hero section with CTA",
  "Feature grid",
  "Contact form"
]
```

## Key-value pairs

Simple assignments use `=`:

```sodl
version  = "1.0.0"
language = "TypeScript"
```

## Block declarations

Blocks use a name followed by colon on the same line:

```sodl
stack:
  language = "TypeScript"
  framework = "Astro"
```

Named blocks (like `policy`, `module`, `pipeline`, `step`) include an identifier:

```sodl
policy Security:
  rule "Validate all inputs" severity=high

module AuthModule:
  owns = ["Authentication logic"]
```

## Policy blocks

A `policy` groups rules under a named concern. Each rule has a `severity`:

```sodl
policy Security:
  rule "All API endpoints require JWT validation" severity=critical
  rule "Rate limit authentication endpoints" severity=high
  rule "Log all authentication attempts" severity=medium

policy CodeQuality:
  rule "All public functions have docstrings" severity=medium
  rule "Variable names are descriptive" severity=low
```

### Severity levels

| Level | Meaning |
|---|---|
| `critical` | Must not be violated — blocks generation |
| `high` | Required constraint |
| `medium` | Strong recommendation |
| `low` | Suggestion |

## Extends and implements

Inheritance uses the `extends` keyword:

```sodl
template "Base":
  stack:
    language = "TypeScript"

system "MySystem" extends "Base":
  ...

interface MyComponent extends AstroComponent:
  ...
```

Module dependencies use `implements`, `requires`, and `exports`:

```sodl
module UIComponents:
  implements = [HeroComponent, FeatureCard]
  exports    = [HeroComponent, FeatureCard]
  requires   = [ThemeConfig]
```

## Method signatures

Interfaces declare methods with typed parameters:

```sodl
interface HeroComponent:
  method render(tagline: str, subtitle: str) -> str
```

### Types

**Primitive types:** `str`, `int`, `float`, `bool`, `bytes`, `UUID`, `datetime`

**Generic types** — both bracket and angle-bracket syntax are accepted:

```sodl
method get_all(page: int) -> List[Post]
method find(id: UUID) -> Optional[User]
method get_stats() -> Result<Success, Error>
```

**API response types** (used in `endpoint` declarations):

```sodl
endpoint "GET /posts" -> List[PostCard]
endpoint "GET /post/{id}" -> HTML
endpoint "POST /action" -> Redirect
endpoint "GET /stream" -> SSE
endpoint "DELETE /item/{id}" -> Empty (204)
```

### Naming conventions

| Element | Convention | Example |
|---|---|---|
| Systems, Templates | PascalCase string | `"MySystem"` |
| Interfaces, Modules, Policies | PascalCase | `UserRepository` |
| Pipelines | string | `"Production"` |
| Steps | PascalCase | `StepName` |
| Methods, fields | snake_case | `get_by_id` |
| Endpoints | HTTP verb + path | `"GET /api/path"` |

## Invariants

Invariants are string assertions that must hold:

```sodl
invariants:
  invariant "Logo links to home /"
  invariant "All images have alt text"
```

## Pipeline output types

The `output` field in a `step` block is an identifier that declares what the step produces. The conventional values are:

| Value | What it produces |
|---|---|
| `design` | Architecture decisions, diagrams, data models |
| `code` | Application source code |
| `tests` | Test files and test suites |
| `diff` | Code changes for review |
| `docs` | Documentation files |

```sodl
pipeline "Development":
  step Design:
    output = design
    require = "Define architecture and data models"
  step Implement:
    modules = ["AuthModule", "UserModule"]
    output = code
    gate = "Unit tests pass"
  step Test:
    output = tests
    gate = "Coverage >= 85%"
```

## Artifacts

The `artifacts` key lists file system paths that a module owns:

```sodl
module UIComponents:
  artifacts = ["src/components/", "src/layouts/"]
```
