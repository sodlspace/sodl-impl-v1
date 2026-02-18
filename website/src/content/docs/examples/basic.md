---
title: Basic Documentation Site
description: A minimal SODL spec for an Astro + Starlight documentation website.
---

This example shows a minimal SODL spec for a documentation website built with Astro and Starlight.

## The spec

```sodl
# Reusable base for Astro/Starlight docs sites
template "DocsBase":
  stack:
    language        = "TypeScript"
    styling         = "Tailwind CSS 4"
    hosting         = "Vercel"
    package_manager = "npm"
  policy Accessibility:
    rule "All interactive elements have aria attributes" severity=high
    rule "Components use semantic HTML" severity=medium

# Documentation website system
system "MyDocs" extends "DocsBase":
  version = "0.1.0"
  stack:
    framework     = "Astro 5"
    documentation = "Starlight 0.32"

  intent:
    primary = "Documentation site for the MyLib library"
    outcomes = [
      "Getting started guide",
      "Full API reference",
      "Code examples with syntax highlighting"
    ]
    out_of_scope = [
      "User authentication",
      "Comments or community features",
      "Versioned docs"
    ]

  module AstroConfig:
    owns      = ["Site-wide Astro and Starlight configuration"]
    artifacts = ["astro.config.mjs"]
    config:
      site  = "https://mylib.dev"
      title = "MyLib"

  module DocumentationContent:
    owns = ["All Markdown documentation pages"]
    invariants:
      invariant "Content in src/content/docs/"
      invariant "Pages use Starlight frontmatter: title, description"
    artifacts = ["src/content/docs/"]

  module StaticAssets:
    owns = ["Global CSS and public assets"]
    invariants:
      invariant "Global CSS at src/styles/global.css"
      invariant "Tailwind CSS configured via @tailwindcss/vite plugin"
    artifacts = ["src/styles/", "public/"]

  pipeline "Development":
    step Install:
      require = "npm install"
      gate    = "All dependencies installed"
    step Dev:
      modules = ["DocumentationContent", "AstroConfig"]
      require = "astro dev"
      gate    = "Dev server running with HMR"

  pipeline "Production":
    step Build:
      modules = ["DocumentationContent", "AstroConfig", "StaticAssets"]
      require = "astro build"
      gate    = "Static site built to dist/"
    step Deploy:
      require = "Push to main triggers Vercel deployment"
      gate    = "Site live at https://mylib.dev"
```

## How to use this

1. Save the spec as `spec.sodl` in your project root
2. Open Cursor and reference it: `@spec.sodl`
3. Ask Cursor to implement each module:

```
@spec.sodl implement the DocumentationContent module with getting-started, api-reference, and examples pages
```

The AI will respect your stack choices, content structure, and all invariants.
