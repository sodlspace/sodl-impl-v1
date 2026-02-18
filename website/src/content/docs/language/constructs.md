---
title: Constructs in Depth
description: Detailed reference for each SODL construct — template, system, interface, module, pipeline.
---

## template

A `template` is a reusable base that captures shared stack choices and policies.

```sodl
template "AstroSiteBase":
  stack:
    language       = "TypeScript"
    styling        = "Tailwind CSS 4"
    hosting        = "Vercel"
    package_manager = "npm"
  policy Accessibility:
    rule "All interactive elements have aria attributes" severity=high
    rule "Components use semantic HTML" severity=medium
```

Templates are referenced by `system` via `extends`. All stack and policy declarations are inherited.

---

## system

A `system` is the main construct that defines a software system.

```sodl
system "MySite" extends "AstroSiteBase":
  version = "1.0.0"
  stack:
    framework = "Astro 5"

  intent:
    primary      = "Marketing website"
    outcomes     = ["Hero section", "Blog"]
    out_of_scope = ["User auth"]
```

### system.stack

Extends the inherited stack with system-specific additions.

### system.intent

Captures the _why_ of the system:

- `primary` — one-line purpose statement
- `outcomes` — list of key features or deliverables
- `out_of_scope` — explicit exclusions

### system.version

Semantic version string for the spec.

---

## interface

An `interface` defines a contract — methods, invariants, and documentation.

```sodl
interface HeroComponent extends AstroComponent:
  doc = "Landing page hero section"
  override method render(tagline: str, subtitle: str) -> str
  invariants:
    invariant "tagline is the main H1 heading"
    invariant "Accessible: section has aria-labelledby"
```

- `doc` — human-readable description
- `override method` — method that overrides a parent interface method
- `invariants` — list of assertions that must hold

Interfaces can be declared at the top level or nested inside a `system`.

---

## module

A `module` groups related functionality and declares ownership of artifacts.

```sodl
module UIComponents:
  implements = [HeroComponent, FeatureGridComponent]
  exports    = [HeroComponent, FeatureGridComponent]
  requires   = [ThemeConfig]
  artifacts  = ["src/components/"]
  config:
    theme = "dark"
  invariants:
    invariant "All components are single-file .astro format"
```

| Key | Purpose |
|---|---|
| `implements` | Interfaces this module fulfills |
| `exports` | Interfaces available to other modules |
| `requires` | Modules or interfaces this module depends on |
| `owns` | List of string descriptions of what this module owns |
| `artifacts` | File system paths this module writes to |
| `config` | Module-level configuration key-value pairs |

---

## pipeline

A `pipeline` defines an ordered sequence of steps for code generation or deployment.

```sodl
pipeline "Production":
  step Install:
    output  = "node_modules"
    require = "npm install with pinned versions"
    gate    = "Clean dependency tree installed"
  step Build:
    modules = ["UIComponents", "DocumentationContent"]
    output  = "dist/"
    require = "astro build"
    gate    = "Static site built to dist/"
  step Deploy:
    output  = "deployment"
    require = "Push to main triggers Vercel deployment"
    gate    = "Site live at https://sodl.space"
```

### step

Each step has:

| Key | Purpose |
|---|---|
| `output` | What this step produces |
| `require` | Command or condition to execute |
| `gate` | Acceptance criterion — must pass before next step |
| `modules` | Which modules are involved in this step |
