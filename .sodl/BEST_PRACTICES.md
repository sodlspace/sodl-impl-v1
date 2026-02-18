# SODL Best Practices Guide

**Version 0.3** | Writing & Compilation Guidelines

This document consolidates best practices for writing, validating, and compiling SODL specifications.

---

## Table of Contents

1. [Writing Best Practices](#writing-best-practices)
2. [Compilation Best Practices](#compilation-best-practices)
3. [Common Errors to Avoid](#common-errors-to-avoid)
4. [Pre-Compile Checklist](#pre-compile-checklist)
5. [Recommended Workflow](#recommended-workflow)

---

## Writing Best Practices

### 1. Start with Templates for Reusability

Create reusable base templates that can be extended by multiple systems:

```sodl
# ✅ Create reusable base templates
template "BasePythonGame":
  stack:
    language = "Rust 2021"
    testing = ["cargo test"]
  policy Performance:
    rule "Maintain 60 FPS" severity=high

# Then extend for specific projects
system "MyGame" extends "BasePythonGame":
  intent:
    primary = "Specific game description"
```

**Benefits:**
- Reduces duplication across projects
- Enforces consistent standards
- Easy to update multiple systems by changing template

---

### 2. Keep Modules Single-Responsibility

Each module should own one coherent domain:

```sodl
# ✅ Focused module
module PlayerModule:
  owns = ["Player entity", "Movement", "Shooting"]
  artifacts = ["src/player.rs"]

# ❌ Too broad
module GameModule:
  owns = ["Everything"]  # Don't do this
```

**Guidelines:**
- One module = one source file (typically)
- If `owns` has more than 5 items, consider splitting
- Related functionality stays together

---

### 3. Define Interfaces Before Implementation

Design contracts first, then implement:

```sodl
# ✅ Contract first
interface EnemyFactory:
  method spawn(type: str) -> Enemy
  method spawn_boss() -> Boss

# Then implement
module EnemySpawner:
  implements = [EnemyFactory]
  exports = [EnemyFactory]
```

**Benefits:**
- Decouples modules from concrete implementations
- Enables swapping implementations without changing dependents
- Clarifies module boundaries early

---

### 4. Use Explicit Dependencies

Declare all module dependencies with `requires`:

```sodl
# ✅ Clear dependency graph
module MainModule:
  requires = [PlayerModule, EnemyModule, ProjectileModule]

# ❌ Implicit coupling (avoid)
module MainModule:
  # No requires declared but uses other modules
```

**Why it matters:**
- Enables dependency validation at compile time
- Makes architecture visible and auditable
- Prevents hidden coupling

---

### 5. Write Measurable Policies

Policies should be specific and testable:

```sodl
# ✅ Specific and testable
policy Performance:
  rule "Maintain 60 FPS with 100+ enemies" severity=high
  rule "Particle count limited to 500 max" severity=medium

# ❌ Vague (avoid)
policy Performance:
  rule "Make it fast" severity=high  # Too ambiguous
```

**Policy quality checklist:**
- [ ] Can this be verified programmatically or manually?
- [ ] Is the threshold clear (numbers, not adjectives)?
- [ ] Is severity level appropriate?

---

### 6. Define Clear Acceptance Tests

Acceptance criteria must be actionable:

```sodl
# ✅ Actionable test criteria
module PlayerModule:
  acceptance:
    test "player moves with WASD input"
    test "player shoots toward mouse cursor"
    test "dash ability has cooldown"

# ❌ Vague tests (avoid)
module PlayerModule:
  acceptance:
    test "player works correctly"  # Not measurable
```

**Good test characteristics:**
- Describes observable behavior
- Includes both positive and negative cases
- Uses present tense, active voice

---

### 7. Use Severity Levels Appropriately

| Severity | When to Use | Enforcement |
|----------|-------------|-------------|
| `critical` | Security, data loss, core invariants | Hard constraint, blocks generation |
| `high` | Required functionality, performance targets | Required constraint |
| `medium` | Best practices, code quality | Strong recommendation |
| `low` | Nice-to-have optimizations | Suggestion |

**Examples:**

```sodl
policy Security:
  rule "No SQL injection vulnerabilities" severity=critical
  rule "All user input validated" severity=high

policy CodeQuality:
  rule "Functions documented with docstrings" severity=medium
  rule "Variable names are descriptive" severity=low
```

---

### 8. Define Scope Boundaries Explicitly

Use `out_of_scope` to prevent feature creep:

```sodl
intent:
  primary = "Top-down shooter with progression"
  outcomes = [
    "Player moves with WASD and aims with mouse",
    "Enemies spawn in waves"
  ]
  out_of_scope = ["Multiplayer", "Save system", "Main menu"]
```

**Why it matters:**
- Sets clear expectations
- Prevents scope drift during development
- Helps AI agents understand boundaries

---

### 9. Pipeline Steps Should Be Atomic

Each step should have a single, verifiable output:

```sodl
# ✅ Sequential, verifiable steps
pipeline "Development":
  step Design:
    output = design
  step Implement:
    modules = ["PlayerModule", "EnemyModule"]
    output = code
    gate = "Game compiles without errors"
  step Test:
    output = tests
    gate = "All acceptance tests pass"
  step Polish:
    output = diff
    gate = "Performance targets met"

# ❌ Monolithic step (avoid)
pipeline "Development":
  step DoEverything:  # Don't do this
    output = code
```

**Step design principles:**
- One output type per step
- Gates are pass/fail criteria
- Steps ordered by dependency

---

### 10. Artifact Paths Should Match Project Structure

Keep artifact declarations consistent with actual file organization:

```sodl
# ✅ Consistent with actual file structure
module PlayerModule:
  artifacts = ["src/player.rs"]

module EnemyModule:
  artifacts = ["src/enemy.rs"]

module WaveModule:
  artifacts = ["src/wave.rs"]
```

**Conventions:**
- Use relative paths from project root
- Group related modules in same directory
- Match module name to file name when possible

---

## Compilation Best Practices

### 1. Validate Syntax Before Full Compile

Run quick syntax validation first to catch errors early:

```bash
# Fast syntax check
sodl validate game_spec.sodl

# Then full compile if valid
sodl compile game_spec.sodl
```

**Benefits:**
- Faster feedback loop
- Catches typos and formatting errors
- Saves time on deep compilation errors

---

### 2. Check Module Dependencies

Ensure all `requires` have matching `exports` or `implements`:

```sodl
# ✅ Valid dependency chain
module A:
  exports = [ServiceInterface]

module B:
  requires = [ServiceInterface]  # Can resolve

# ❌ Unresolved dependency
module C:
  requires = [UnknownInterface]  # Compilation error
```

**Validation checklist:**
- [ ] Every `requires` has a matching `exports` or `implements`
- [ ] No circular dependencies
- [ ] Interface methods fully implemented

---

### 3. Verify Interface Contracts

All interface methods must be implemented by modules that `implements` them:

```sodl
interface Store:
  method create(data: Input) -> Output
  method read(id: str) -> Output

module StoreImpl:
  implements = [Store]
  # Must implement BOTH create and read methods
```

**Compiler checks:**
- Method signature matches interface
- All methods present
- Return types compatible

---

### 4. Watch for Circular Dependencies

Avoid modules that depend on each other:

```sodl
# ❌ Circular (avoid)
module A:
  requires = [B]

module B:
  requires = [A]  # Creates cycle

# ✅ Resolve with interface
module A:
  requires = [BInterface]

module B:
  implements = [BInterface]
  requires = [AInterface]

module A:
  implements = [AInterface]
```

**Detection:**
- Compiler will report dependency cycles
- Refactor using interfaces to break cycles
- Consider merging tightly-coupled modules

---

### 5. Use Consistent Indentation

SODL is indentation-sensitive (like Python):

```sodl
# ✅ 2 spaces (be consistent)
system "App":
  stack:
    language = "Rust"

# ❌ Mixed (avoid)
system "App":
  stack:
      language = "Rust"  # Inconsistent indentation
```

**Rules:**
- Use 2 or 4 spaces (choose one, be consistent)
- Never mix tabs and spaces
- Colon (`:`) starts indented block

---

## Common Errors to Avoid

| Error | Problem | Fix |
|-------|---------|-----|
| Missing colon | `system "App"` | `system "App":` |
| Unquoted names | `system MyApp` | `system "MyApp":` |
| Wrong type syntax | `method get(id: string)` | `method get(id: str)` |
| Inconsistent indent | Mixed tabs/spaces | Use 2 spaces throughout |
| Missing artifacts | Module with no files | Add `artifacts = [...]` |
| Undefined interface | `requires = [Unknown]` | Define interface first |
| Missing method | Interface method not implemented | Implement all interface methods |
| Invalid severity | `severity=urgent` | Use: `critical`, `high`, `medium`, `low` |
| Pipeline without output | `step Build:` (no output) | Add `output = code` |
| Duplicate module names | Two modules with same name | Use unique names |

---

## Pre-Compile Checklist

Before running `sodl compile`, verify:

```
□ Syntax valid (colons, quotes, indentation)
□ All interfaces defined before use
□ Module dependencies resolvable (requires → exports/implements)
□ Pipeline steps in logical order
□ Severity levels appropriate (critical/high/medium/low)
□ Acceptance tests measurable and actionable
□ Artifact paths exist or will exist after generation
□ No circular dependencies between modules
□ out_of_scope clearly defined
□ Policies are testable and specific
□ All interface methods implemented
□ Module names are unique
□ Version string is valid (if specified)
```

**Quick validation command:**
```bash
sodl validate game_spec.sodl && echo "Syntax OK"
```

---

## Recommended Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                     SODL Development Flow                    │
└─────────────────────────────────────────────────────────────┘

1. Write Template (optional)
   └─→ Define common stack, policies, conventions

2. Define System
   └─→ Add system name, version, extends (if using template)

3. Add Stack & Intent
   └─→ Technology choices, primary goal, outcomes, scope

4. Define Interfaces
   └─→ Contracts for inter-module communication

5. Create Modules
   └─→ owns, requires, implements, exports, api, artifacts

6. Define Policies
   └─→ Security, performance, quality rules with severity

7. Build Pipeline
   └─→ Steps with output types and gates

8. Syntax Validate
   └─→ sodl validate game_spec.sodl

9. Compile
   └─→ sodl compile game_spec.sodl

10. Review Generated Instructions
    └─→ Check global.md, modules/*.md, steps/*.md
```

---

## Module Organization Patterns

### Layered Architecture

```sodl
# Presentation layer
module WebUIModule:
  requires = [GameService]
  artifacts = ["src/ui.rs"]

# Service layer
module GameServiceModule:
  requires = [PlayerRepository, EnemyRepository]
  artifacts = ["src/service.rs"]

# Data layer
module PlayerRepositoryModule:
  implements = [PlayerRepository]
  exports = [PlayerRepository]
  artifacts = ["src/repository.rs"]
```

### Feature-Based Organization

```sodl
# Player feature
module PlayerModule:
  owns = ["Player entity", "Movement", "Shooting"]
  artifacts = ["src/player.rs"]

# Enemy feature
module EnemyModule:
  owns = ["Enemy AI", "Spawning", "Boss fights"]
  artifacts = ["src/enemy.rs"]

# Combat feature
module CombatModule:
  owns = ["Collision", "Damage calculation"]
  artifacts = ["src/combat.rs"]
```

---

## Interface Design Patterns

### Repository Pattern

```sodl
interface EnemyRepository:
  doc = "Persistent storage for enemy entities"
  method spawn(enemy_type: str, position: Vec2) -> Enemy
  method get_all() -> List[Enemy]
  method remove(enemy_id: UUID) -> bool
  method get_by_id(enemy_id: UUID) -> Optional[Enemy]
  invariants:
    invariant "Enemy IDs are unique"
    invariant "Spawned enemies are immediately queryable"
```

### Factory Pattern

```sodl
interface EnemyFactory:
  doc = "Creates enemies based on wave configuration"
  method create_basic(position: Vec2) -> Enemy
  method create_elite(position: Vec2, elite_type: str) -> Enemy
  method create_boss(position: Vec2, wave_number: int) -> Boss
  invariants:
    invariant "Boss only created on boss waves (5, 10, 15...)"
    invariant "Elite enemies have valid elite_type"
```

### Service Pattern

```sodl
interface WaveService:
  doc = "Manages wave progression and enemy spawning"
  method start_wave(wave_number: int) -> WaveInfo
  method get_current_wave() -> WaveInfo
  method is_wave_complete() -> bool
  method spawn_next_wave() -> WaveInfo
  invariants:
    invariant "Wave numbers are sequential"
    invariant "Boss wave every 5 waves"
```

---

## Policy Examples by Category

### Security Policies

```sodl
policy Security:
  rule "No hardcoded secrets in source code" severity=critical
  rule "All user input validated and sanitized" severity=critical
  rule "Use parameterized queries for database access" severity=critical
  rule "Implement rate limiting on public APIs" severity=high
  rule "Log all authentication attempts" severity=high
  rule "Use HTTPS for all external API calls" severity=high
```

### Performance Policies

```sodl
policy Performance:
  rule "Maintain 60 FPS with 100+ enemies on screen" severity=high
  rule "Memory usage stays under 500MB" severity=high
  rule "Particle count limited to 500 maximum" severity=medium
  rule "Use object pooling for frequently created entities" severity=medium
  rule "Batch draw calls where possible" severity=low
```

### Code Quality Policies

```sodl
policy CodeQuality:
  rule "All public functions have doc comments" severity=medium
  rule "No functions longer than 50 lines" severity=low
  rule "Test coverage above 80% for core modules" severity=high
  rule "No unused dependencies in Cargo.toml" severity=low
  rule "Clippy warnings resolved" severity=medium
```

---

## Acceptance Test Patterns

### CRUD Module Tests

```sodl
module PlayerModule:
  acceptance:
    # Create
    test "player spawns at starting position"
    test "player has correct initial health (100)"
    test "player has correct initial speed (200.0)"

    # Read
    test "player position accessible via getter"
    test "player health accessible via getter"

    # Update
    test "player health decreases on damage"
    test "player speed increases with speed powerup"

    # Delete
    test "player entity removed on death"

    # Edge cases
    test "player cannot go below 0 health"
    test "player movement clamped to screen bounds"
```

### API Module Tests

```sodl
module EnemyAPIModule:
  acceptance:
    # Success cases
    test "GET /enemies returns list of all enemies"
    test "GET /enemies/{id} returns enemy details"
    test "POST /enemies/spawn creates new enemy"

    # Error cases
    test "GET /enemies/{id} returns 404 for unknown ID"
    test "POST /enemies/spawn returns 400 for invalid type"

    # Integration
    test "spawned enemy appears in GET /enemies list"
    test "deleted enemy removed from GET /enemies list"
```

---

## Pipeline Patterns

### Standard Development Pipeline

```sodl
pipeline "Development":
  step Design:
    output = design
    require = "Define architecture and data models"

  step ImplementCore:
    modules = ["CoreModule", "UtilsModule"]
    output = code
    gate = "Core module tests pass"

  step ImplementFeatures:
    modules = ["PlayerModule", "EnemyModule", "CombatModule"]
    output = code
    gate = "Feature tests pass"

  step Integrate:
    modules = ["MainModule"]
    output = code
    gate = "Full integration tests pass"

  step Polish:
    output = diff
    require = "Add visual effects, optimize performance"
    gate = "Performance targets met"
```

### CI/CD Pipeline

```sodl
pipeline "CI":
  step Lint:
    output = tests
    require = "Run clippy, rustfmt"
    gate = "No linting errors"

  step Test:
    output = tests
    require = "Run full test suite"
    gate = "All tests pass with 80% coverage"

  step Build:
    output = code
    require = "Build release binary"
    gate = "Build succeeds without warnings"

  step Deploy:
    output = diff
    require = "Deploy to staging environment"
    gate = "Smoke tests pass"
```

---

## Quick Reference

### Syntax Reminders

```sodl
# System declaration (quotes required)
system "MySystem":

# Module with all sections
module MyModule:
  owns = ["Responsibility"]
  requires = [Interface]
  implements = [Interface]
  exports = [Interface]
  api:
    endpoint "GET /path" -> Response
    model ModelName:
      field name: Type
  invariants:
    invariant "Constraint"
  acceptance:
    test "Test description"
  artifacts = ["src/file.rs"]
  config:
    key = value

# Interface
interface MyInterface:
  doc = "Description"
  method name(param: Type) -> ReturnType
  invariants:
    invariant "Constraint"

# Policy
policy PolicyName:
  rule "Rule description" severity=level

# Pipeline
pipeline "Name":
  step StepName:
    modules = ["Module"]
    output = code
    require = "Requirement"
    gate = "Exit criteria"
```

### Reserved Keywords

```
system, template, extends, interface, module, policy, pipeline, step
stack, intent, api, method, model, field, endpoint
owns, requires, implements, exports, invariants, invariant
acceptance, test, artifacts, config, rule, severity
output, require, gate, override, append, remove, replace
doc, primary, outcomes, out_of_scope, version
```

### Valid Severity Levels

- `critical` - Must not violate
- `high` - Must follow
- `medium` - Should follow
- `low` - May follow

### Valid Output Types

- `design` - Architecture, diagrams, data models
- `code` - Application source code
- `tests` - Test code and test suites
- `diff` - Code changes for review
- `docs` - Documentation files

---

## Additional Resources

- **[SYNTAX_REFERENCE.md](SYNTAX_REFERENCE.md)** - Quick syntax lookup
- **[SODL_DOCUMENTATION.md](SODL_DOCUMENTATION.md)** - Comprehensive language guide
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API specification
- **[EXAMPLES_COLLECTION.md](EXAMPLES_COLLECTION.md)** - 17+ complete examples
- **[SODL Language Specification_v0.3.pdf](SODL%20Language%20Specification_v0.3.pdf)** - Official spec

---

**SODL v0.3** - Explicit. Structured. AI-Ready.

*"Architecture before code. Constraints before suggestions. Developer-controlled AI."*
