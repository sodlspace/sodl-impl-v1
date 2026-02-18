---
title: Getting Started
description: Install SODL and write your first specification in minutes.
---

SODL (Specification Orchestration Definition Language) is a declarative language for expressing software architecture, intent, and constraints — designed specifically for AI-assisted code generation.

## Prerequisites

- Node.js 20 or later
- An AI coding tool: [Cursor](https://cursor.sh), Claude, or GPT-4

## Installation

SODL is used as a specification language — no runtime installation needed. You write `.sodl` files and reference them as context in your AI coding tool.

To get syntax highlighting in your editor, install the SODL VS Code extension:

```bash
code --install-extension sodl-lang.sodl
```

Or clone the SODL language server from GitHub:

```bash
git clone https://github.com/sodlspace/sodl-impl-v1
```

## Your first SODL spec

Create a file called `my-app.sodl` at the root of your project:

```sodl
system "MyApp":
  version = "0.1.0"
  stack:
    language  = "TypeScript"
    framework = "Next.js 15"
    styling   = "Tailwind CSS"

  intent:
    primary  = "Task management SaaS for small teams"
    outcomes = [
      "User can create and manage tasks",
      "Team members can be invited via email",
      "Dashboard with task overview"
    ]
    out_of_scope = ["Real-time collaboration", "Mobile apps"]

  module TaskModule:
    owns = ["Task CRUD operations"]
    artifacts = ["src/modules/tasks/"]

  module AuthModule:
    owns = ["User authentication and sessions"]
    artifacts = ["src/modules/auth/"]
```

## Using the spec with Cursor

Add your `.sodl` file as a Cursor rule or reference it in your prompts:

```
@my-app.sodl implement the TaskModule following all invariants
```

Cursor will use the spec to understand the project context, stack, and constraints before generating any code.

## Using the spec with Claude

Paste your spec at the start of a conversation:

```
Here is my project specification:

[contents of my-app.sodl]

Please implement the TaskModule. Follow all constraints and invariants defined in the spec.
```

## Next steps

- Read [Why SODL](/why-sodl/) to understand the motivation
- Learn the full [Language Reference](/language/)
- See [Examples](/examples/) for real-world specs
