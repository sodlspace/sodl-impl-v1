---
title: Constructs in Depth
description: Detailed reference for each SODL construct — template, system, interface, module, policy, pipeline.
---

## template

A `template` is a reusable base that captures shared stack choices and policies. Multiple systems can extend the same template.

```sodl
template "AstroSiteBase":
  stack:
    language        = "TypeScript"
    styling         = "Tailwind CSS 4"
    hosting         = "Vercel"
    package_manager = "npm"
  policy Accessibility:
    rule "All interactive elements have aria attributes" severity=high
    rule "Components use semantic HTML" severity=medium
```

Templates are referenced by `system` via `extends`. All stack and policy declarations are inherited.

### Template inheritance operations

When a `system` (or another template) extends a base, it can modify inherited content with three operations:

| Operation | Syntax | Effect |
|---|---|---|
| `override` | `override path.to.value = "new"` | Replaces a single inherited value |
| `append` | `append path.to.list += "item"` | Adds an item to an inherited list |
| `remove` | `remove path.to.list -= "item"` | Removes an item from an inherited list |

```sodl
system "MySite" extends "AstroSiteBase":
  # Override a stack value
  override stack.hosting = "Netlify"

  # Add a new outcome to an inherited list
  append intent.outcomes += "Dark mode toggle"

  # Remove an inherited policy rule
  remove policy.Accessibility.rules -= "Components use semantic HTML"
```

---

## system

A `system` is the main construct that defines a software system. It is the root of a SODL spec.

```sodl
system "MySite" extends "AstroSiteBase":
  version = "1.0.0"
  stack:
    framework = "Astro 5"

  intent:
    primary      = "Marketing website"
    outcomes     = ["Hero section", "Blog", "Pricing page"]
    out_of_scope = ["User auth", "Payment processing"]
```

### system.stack

Declares or extends the technology stack. Keys are free-form (`language`, `framework`, `database`, `auth`, etc.):

```sodl
stack:
  language  = "TypeScript"
  framework = "Next.js 15"
  database  = "PostgreSQL"
  auth      = "JWT"
```

### system.intent

Captures the _why_ of the system:

- `primary` — one-line purpose statement
- `outcomes` — list of key features or deliverables
- `out_of_scope` — explicit exclusions that prevent scope drift

### system.version

Semantic version string for the spec (e.g. `"1.0.0"`).

---

## interface

An `interface` defines a contract — methods, invariants, and documentation. It can be declared at the top level or nested inside a `system`.

```sodl
interface UserRepository:
  doc = "Persistent storage contract for user records"
  method create(user: UserCreate) -> User
  method get_by_id(id: UUID) -> Optional[User]
  method get_by_email(email: str) -> Optional[User]
  method update(id: UUID, updates: UserUpdate) -> User
  method delete(id: UUID) -> bool
  invariants:
    invariant "User emails are unique across the system"
    invariant "Deleted users cannot be retrieved"
```

### Interface inheritance

Interfaces can extend other interfaces using `extends`. The child interface inherits all methods and can override them:

```sodl
interface AdminRepository extends UserRepository:
  override method delete(id: UUID) -> AuditedDeletion
  method ban(id: UUID, reason: str) -> bool
```

- `doc` — human-readable description
- `override method` — replaces an inherited method's signature
- `invariants` — assertions that any implementation must satisfy

---

## module

A `module` groups related functionality and declares ownership of artifacts.

```sodl
module AuthAPI:
  requires = [AuthService]
  api:
    endpoint "POST /api/auth/register" -> UserResponse (201)
    endpoint "POST /api/auth/login"    -> TokenResponse
    endpoint "POST /api/auth/refresh"  -> TokenResponse
    endpoint "POST /api/auth/verify"   -> Empty (204)
  invariants:
    invariant "Rate limit 5 requests per minute per IP"
    invariant "Return 401 for invalid credentials"
    invariant "Log all authentication attempts"
  acceptance:
    test "registers new user successfully"
    test "rejects duplicate email with 409"
    test "returns JWT on valid login"
    test "rejects invalid credentials with 401"
  artifacts = ["app/api/auth.py"]
```

| Key | Purpose |
|---|---|
| `implements` | Interfaces this module fulfills |
| `exports` | Interfaces available to other modules |
| `requires` | Modules or interfaces this module depends on |
| `owns` | List of string descriptions of what this module owns |
| `artifacts` | File system paths this module writes to |
| `config` | Module-level configuration key-value pairs |
| `api` | Endpoint, model, and command declarations |
| `invariants` | Constraints that must hold for this module |
| `acceptance` | Definition-of-Done test criteria |

### module.acceptance

The `acceptance` block declares the Definition of Done for a module as a list of `test` criteria. Each criterion is a string describing observable, verifiable behavior:

```sodl
module PaymentModule:
  acceptance:
    test "processes a card payment and returns a receipt"
    test "returns 402 when card is declined"
    test "refunds within 5 minutes of request"
    test "logs all payment attempts"
```

Good acceptance criteria:
- Describe observable behavior, not implementation
- Use present tense, active voice
- Include both success and failure cases
- State measurable thresholds where applicable

### module.api

Declares the public surface of a module — endpoints, WebSocket routes, CLI commands, and data models:

```sodl
module ProductAPI:
  api:
    endpoint "GET /api/products"       -> List[ProductCard]
    endpoint "GET /api/products/{id}"  -> ProductDetail
    endpoint "POST /api/products"      -> ProductDetail (201)
    endpoint "DELETE /api/products/{id}" -> Empty (204)
    websocket "/ws/live-inventory"    -> None
    model ProductCard:
      field id:    UUID
      field name:  str
      field price: float
```

---

## policy

A `policy` groups enforceable rules under a named concern. Every rule has a `severity` that signals how strictly it must be followed.

```sodl
policy Security:
  rule "Passwords hashed with bcrypt" severity=critical
  rule "JWT tokens expire in 1 hour" severity=high
  rule "Rate limit authentication endpoints" severity=high
  rule "Validate all input with Pydantic" severity=critical

policy Performance:
  rule "Cache GET responses for 60 seconds" severity=medium
  rule "Timeout backend requests after 30 seconds" severity=high
  rule "Implement circuit breaker for each service" severity=critical
```

Policies can be declared inside a `template` (inherited by all extending systems) or directly inside a `system`.

### Severity levels

| Level | Meaning | Enforcement |
|---|---|---|
| `critical` | Must not be violated | Hard constraint — blocks generation |
| `high` | Required | Must be followed |
| `medium` | Recommended | Strong suggestion |
| `low` | Optional | Nice-to-have |

### Writing good policy rules

Effective rules are specific and verifiable:

```sodl
# ✅ Specific and testable
policy Performance:
  rule "Response time < 200ms at p95 under 100 concurrent users" severity=high
  rule "Particle count limited to 500 maximum" severity=medium

# ❌ Too vague
policy Performance:
  rule "Make it fast" severity=high
```

---

## pipeline

A `pipeline` defines an ordered sequence of steps for code generation or deployment.

```sodl
pipeline "Production":
  step ImplementAuth:
    modules = ["AuthModule"]
    output  = code
    gate    = "Security tests pass"

  step ImplementAPI:
    modules = ["UserAPI", "ProductAPI"]
    output  = code
    gate    = "Integration tests pass"

  step Deploy:
    output  = diff
    require = "Push to main triggers Vercel deployment"
    gate    = "Site live at https://example.com"
```

### step

Each `step` is an atomic generation phase inside a pipeline:

| Key | Purpose |
|---|---|
| `output` | What this step produces (`design`, `code`, `tests`, `diff`, `docs`) |
| `require` | Condition or command to execute in this step |
| `gate` | Acceptance criterion — must pass before the next step begins |
| `modules` | Which modules are in scope for this step |

Steps execute in declaration order. A `gate` that fails halts the pipeline at that step, requiring human review before continuing.

### Pipeline output types

| Value | What it produces |
|---|---|
| `design` | Architecture decisions, data models |
| `code` | Application source code |
| `tests` | Test files and test suites |
| `diff` | Code changes for human review |
| `docs` | Documentation files |
