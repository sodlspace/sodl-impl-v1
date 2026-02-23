---
title: Best Practices
description: Patterns, principles, and common mistakes for writing effective SODL specs.
---

## Writing workflow

Follow this order when writing a new spec — each step builds on the previous:

```
1. Write template (optional)
   └─ Common stack, policies, conventions

2. Define system
   └─ Name, version, extends template

3. Add stack & intent
   └─ Technology choices, primary goal, outcomes, out_of_scope

4. Define interfaces
   └─ Contracts for inter-module communication

5. Create modules
   └─ owns, requires, implements, exports, api, artifacts

6. Define policies
   └─ Security, performance, quality rules with severity

7. Build pipeline
   └─ Steps with output types and gates

8. Validate
   └─ sodl validate spec.sodl

9. Compile
   └─ sodl compile spec.sodl
```

---

## Module design

### Single-responsibility

One module should own one coherent domain. If `owns` has more than five items, consider splitting:

```sodl
# ✅ Focused module
module PlayerModule:
  owns = ["Player entity", "Movement", "Shooting"]
  artifacts = ["src/player.rs"]

# ❌ Too broad
module GameModule:
  owns = ["Everything"]
```

### Declare responsibilities with `owns`

Even if a module has no `implements`, use `owns` to make its purpose explicit. This is what the AI reads to understand what the module is responsible for — and, crucially, what it is _not_ responsible for.

### Keep `requires` minimal

Every entry in `requires` is a coupling point. Prefer interface contracts over direct module-to-module dependencies:

```sodl
# ✅ Depends on interface — swappable
module OrderAPI:
  requires = [OrderRepository]

# ❌ Depends on concrete module — brittle
module OrderAPI:
  requires = [PostgresOrderRepository]
```

---

## Templates and inheritance

### Create a base template for each stack

Encode stack-level conventions (auth, error handling, logging policies) in a `template` so every system that extends it inherits them automatically:

```sodl
template "PythonAPIBase":
  stack:
    language = "Python 3.12"
    web      = "FastAPI"
  policy Security:
    rule "Validate all input with Pydantic"  severity=critical
    rule "No hardcoded secrets in code"       severity=critical
  policy CodeQuality:
    rule "All public functions have docstrings" severity=medium

system "UserAPI" extends "PythonAPIBase":
  # Inherits Security and CodeQuality policies automatically
  stack:
    database = "PostgreSQL"
    auth     = "JWT"
```

### Use inheritance operations for targeted changes

Instead of copying a base spec and editing it, use `override`, `append`, and `remove` to make surgical changes:

```sodl
system "AdminAPI" extends "PythonAPIBase":
  # Change a single stack value
  override stack.auth = "OAuth2"

  # Add a new policy rule without rewriting the policy
  append policy.Security.rules += "Admin endpoints require 2FA"

  # Remove a rule that doesn't apply here
  remove policy.CodeQuality.rules -= "All public functions have docstrings"
```

---

## Policies

### At least one `critical` policy per project

Every non-trivial system should have at least one `critical`-severity rule. These are the hard constraints the AI must never violate. Common candidates:

- No SQL injection
- Passwords must be hashed
- Auth required on all write endpoints
- No hardcoded secrets

### Write verifiable rules — not adjectives

Rules are only useful if they can be checked. Avoid adjectives (`fast`, `secure`, `clean`). Use thresholds, patterns, and observable behaviors:

```sodl
# ✅ Verifiable
policy Performance:
  rule "Response time < 200ms at p95"                    severity=high
  rule "Memory usage stays under 500MB"                  severity=high
  rule "Particle count limited to 500 maximum"           severity=medium

# ❌ Not verifiable
policy Performance:
  rule "Make it fast"         severity=high
  rule "Use less memory"      severity=medium
```

### Use `rationale` fields to explain decisions

When a rule needs context, document the "why" so the AI (and future developers) understand the intent:

```sodl
policy Security:
  rule "Passwords hashed with bcrypt (cost factor 12)" severity=critical
```

### Severity guide

| Level | Use when | AI behavior |
|---|---|---|
| `critical` | Data loss, security breach, core invariant | Must not violate |
| `high` | Required by the system design | Must follow |
| `medium` | Industry best practice | Should follow |
| `low` | Nice-to-have optimization | May follow |

---

## Interfaces

### Define interfaces before modules

Design contracts first, implement second. This forces you to think about the boundary before the internals:

```sodl
# ✅ Contract first
interface OrderRepository:
  method create(order: OrderCreate) -> Order
  method get_by_id(id: UUID) -> Optional[Order]
  method update_status(id: UUID, status: OrderStatus) -> Order

# Then implement
module PostgresOrderRepository:
  implements = [OrderRepository]
  exports    = [OrderRepository]
```

### Use `invariants` in interfaces to document guarantees

Interface invariants are constraints that _every_ implementation must satisfy — they belong in the interface, not scattered across module implementations:

```sodl
interface EnemyRepository:
  method spawn(type: str) -> Enemy
  method get_all() -> List[Enemy]
  invariants:
    invariant "Enemy IDs are unique"
    invariant "Spawned enemies are immediately queryable"
```

### Resolve circular dependencies through interfaces

If two modules need to call each other, introduce a shared interface to break the cycle:

```sodl
# ❌ Circular (compiler will reject)
module A:
  requires = [B]
module B:
  requires = [A]

# ✅ Resolved with interface
interface AInterface:
  method do_a() -> Result

module A:
  implements = [AInterface]
  requires   = [BInterface]

module B:
  implements = [BInterface]
  requires   = [AInterface]
```

---

## Acceptance tests

### Every module needs measurable acceptance criteria

Acceptance tests in the `acceptance` block define the Definition of Done. They are evaluated when the pipeline step's `gate` is checked:

```sodl
module AuthAPI:
  acceptance:
    test "registers new user and returns 201"
    test "rejects duplicate email with 409"
    test "returns JWT on valid login"
    test "returns 401 for invalid credentials"
    test "rate limits to 5 requests per minute per IP"
```

### Good test criteria

- **Observable behavior**, not implementation detail: "returns 401" not "checks the token variable"
- **Both positive and negative cases**: success paths and error paths
- **Measurable thresholds** where applicable: "in < 30 seconds", "at 100 concurrent users"
- **Present tense, active voice**: "registers new user" not "new user should be registered"

### Anti-pattern: vague acceptance criteria

```sodl
# ❌ Not testable
acceptance:
  test "authentication works correctly"
  test "handles errors"

# ✅ Testable
acceptance:
  test "returns JWT with 1-hour expiry on valid login"
  test "returns 401 with error message on invalid password"
  test "returns 429 after 5 failed attempts in 60 seconds"
```

---

## Pipelines

### Keep steps atomic

Each step should have one `output` type and one verifiable `gate`. If you find yourself listing many unrelated things in one step, split it:

```sodl
# ✅ Atomic steps
pipeline "Development":
  step Design:
    output = design
    require = "Define architecture and data models"
  step ImplementCore:
    modules = ["AuthModule", "UserModule"]
    output  = code
    gate    = "Unit tests pass"
  step ImplementFeatures:
    modules = ["ProductModule", "OrderModule"]
    output  = code
    gate    = "Feature tests pass"
  step Test:
    output = tests
    gate   = "Coverage >= 85%"

# ❌ Monolithic
pipeline "Development":
  step DoEverything:
    output = code
```

### Gates are pass/fail contracts

Write `gate` values as clear pass/fail criteria, not process descriptions:

```sodl
# ✅ Pass/fail criteria
gate = "All unit tests pass"
gate = "Lighthouse score > 90"
gate = "Process 10k events/sec without lag"

# ❌ Process description (not a gate)
gate = "Run the tests"
```

### Match `artifacts` to real directory structure

Artifact paths should reflect where the generated files will actually live. Inconsistencies cause the AI to create files in unexpected locations:

```sodl
module AuthModule:
  artifacts = ["app/api/auth.py", "tests/test_auth.py"]

module UserModule:
  artifacts = ["app/api/users.py", "tests/test_users.py"]
```

---

## Pre-compile checklist

Before running `sodl compile`, verify:

```
□ Syntax: colons after declarations, double quotes around names
□ All interfaces defined before they appear in requires/implements
□ Every requires resolves to an exports or implements
□ No circular dependencies between modules
□ Pipeline steps in logical order
□ Severity levels: critical/high/medium/low (no other values)
□ Acceptance tests are measurable and observable
□ Artifact paths are relative to project root
□ out_of_scope clearly defined to prevent AI scope creep
□ Policies are specific and testable (no vague adjectives)
□ All interface methods will be implemented by a module
□ Module names are unique within the system
```

---

## Common errors

| Error | Problem | Fix |
|---|---|---|
| `system "App"` (no colon) | Missing block opener | `system "App":` |
| `system MyApp:` | Unquoted name | `system "MyApp":` |
| `method get(id: string)` | Wrong type name | Use `str`, not `string` |
| `severity=urgent` | Invalid severity | Use `critical`, `high`, `medium`, `low` |
| `requires = [Unknown]` | Undefined interface | Define interface before use |
| `step Build:` (no output) | Missing output type | Add `output = code` |
| Mixed tabs/spaces | Parser error | Use 2 spaces throughout |
| Duplicate module names | Name collision | Use unique names |
