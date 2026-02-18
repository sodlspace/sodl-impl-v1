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

## Severity modifiers

Rules accept an inline `severity` modifier:

```sodl
rule "All API endpoints require auth" severity=high
rule "Use semantic HTML" severity=medium
rule "Avoid inline styles" severity=low
```

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

Available types: `str`, `int`, `float`, `bool`, `list`, `dict`, `any`.

## Invariants

Invariants are string assertions that must hold:

```sodl
invariants:
  invariant "Logo links to home /"
  invariant "All images have alt text"
```

## Artifacts

The `artifacts` key lists file system paths that a module owns:

```sodl
module UIComponents:
  artifacts = ["src/components/", "src/layouts/"]
```
