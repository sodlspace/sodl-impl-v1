# SODL

**Version 0.5** - DSL for specification-driven development with AI coding agents.

## Overview

SODL is a Domain-Specific Language (DSL) that enables controlled AI-driven code generation through explicit specifications. This repository contains the SODL v0.5 specification, example specifications, documentation website, and the SODL Specification Generator skill for AI agents.

## What is SODL?

SODL is an indentation-based DSL for controlled AI-driven code generation. It allows developers to describe:

- **Intent**: What must be built and why
- **Architecture**: System structure, modules, and interfaces
- **Constraints**: Rules, invariants, and acceptance criteria
- **Pipeline**: Controlled generation process
- **Architecture Patterns**: Clean Architecture, Hexagonal, MVC, and more
- **Dependency Injection**: Container configuration and lifetime rules
- **Error Handling**: Unified error strategies with retry policies
- **Observability**: Logging, tracing, and metrics configuration
- **Testing Strategy**: Unit, integration, E2E, and load testing
- **Security Patterns**: Authentication, authorization, and data protection

The compiler transforms SODL files into structured prompts for AI coding agents, enabling deterministic, reviewable, and reproducible code generation.

## Project Components

### 1. SODL Language Specification

- **examples/** - Example SODL specifications including ModernTodoApp, PresentationGenerator, and more
- **.sodl/SODL_spec_05.md** - Language specification markdown
- **releases/** - Release artifacts and documentation (coming soon)

### 2. SODL Specification Generator Skill (`sodl-spec-generator-skill/`)

AI agent skill for generating production-ready SODL specifications with:
- Architecture patterns (Clean Architecture, Hexagonal, CQRS)
- Dependency injection configuration
- Error handling strategies
- Observability setup
- Testing strategies
- Security patterns
- Template generation utilities
- Validation scripts

### 3. Documentation Website (`website/`)

Astro-based documentation website showcasing SODL specifications.

## Quick Start

### Using the Specification Generator Skill

```bash
# Copy skill to your AI agent's skills directory
cp -r sodl-spec-generator-skill ~/.qwen/skills/sodl-spec-generator

# Or on Windows
xcopy /E /I sodl-spec-generator-skill %USERPROFILE%\.qwen\skills\sodl-spec-generator
```

### Generate a SODL Specification

Once the skill is installed, ask your AI agent:

```
Create a SODL specification for a task management API with JWT authentication
```

```
Generate a production-ready SODL file for an e-commerce microservice with CQRS
```

### Using the Validation Script

```bash
# Validate a SODL specification
python sodl-spec-generator-skill/sodl-spec-generator/scripts/sodl_validator.py validate spec.sodl

# Generate a template
python sodl-spec-generator-skill/sodl-spec-generator/scripts/sodl_validator.py generate crud output.sodl
```

## Project Structure

```
sodl-impl-v1/
├── .sodl/                          # Specification files
│   └── SODL_spec_05.md            # Language specification v0.5
│
├── examples/                       # Example SODL specifications
│   ├── ModernTodoApp.sodl         # Todo app example
│   ├── PresentationGenerator.sodl # Presentation generator example
│   ├── jd_matching.sodl           # JD matching example
│   ├── react-demo.sodl            # React demo example
│   ├── sodlcompiler.sodl          # SODL compiler specification
│   ├── vst_host_plugin.sodl       # VST host plugin example
│   ├── web_ui.sodl                # Web UI example
│   └── constraints_example.sodl   # Field-level constraints example
│
├── sodl-spec-generator-skill/     # AI agent skill for SODL generation
│   └── sodl-spec-generator/
│       ├── SKILL.md               # Main skill instructions
│       ├── README.md              # Skill documentation
│       ├── references/
│       │   └── sodl-quick-reference.md
│       ├── scripts/
│       │   └── sodl_validator.py  # Validation utilities
│       └── assets/
│           └── examples/
│               └── ecommerce-platform.sodl
│
├── website/                        # Documentation website (Astro)
├── releases/                       # Release artifacts
├── .github/                        # GitHub workflows and templates
│
├── context7.json                   # Context7 configuration
├── LICENSE                         # License file
└── README.md                       # This file
```

## Example SODL

Here's a simple SODL example:

```sodl
system "TodoApp":
  version = "1.0.0"
  stack:
    language = "Python 3.12"
    web = "FastAPI"

  intent:
    primary = "Task management application"
    outcomes = ["Create and manage todos", "RESTful API"]

  architecture:
    style = "Clean Architecture"
    layers = ["Domain", "Application", "Infrastructure", "Interface"]

  design_patterns:
    - name = "Repository"
      scope = "global"
    - name = "Factory"
      scope = "modules: [Notification]"

  dependency_injection:
    container = "AutoWire"
    injection_style = "Constructor Injection"
    lifetime_rules:
      - service = "DatabaseConnection"
        scope = "Singleton"
      - service = "TodoService"
        scope = "Transient"

  error_handling:
    strategy = "Result Pattern"
    error_codes:
      - code = "TODO_NOT_FOUND"
        http_status = 404
        user_message = "Todo not found"
    retry_policy:
      max_attempts = 3
      backoff = "exponential"

  observability:
    logging:
      format = "JSON"
      level = "INFO"
    tracing:
      enabled = true
      provider = "OpenTelemetry"

  testing_strategy:
    unit_tests:
      framework = "pytest"
      coverage_target = 80%
    integration_tests:
      framework = "pytest-bdd"

  interface TodoStore:
    method create(todo: TodoInput) -> Todo
    method get_all() -> List[Todo]

  module TodoAPI:
    requires = [TodoStore]
    api:
      endpoint "GET /api/todos" -> List[TodoResponse]
      endpoint "POST /api/todos" -> TodoResponse

  pipeline "Build":
    step Implement:
      modules = ["TodoAPI"]
      output = code
      gate = "Tests pass"
    step ValidateArchitecture:
      output = architecture
      gate = "No dependency violations"
    step GenerateTests:
      output = tests
      gate = "Test scaffolding complete"
```

## SODL Language Features

This project showcases the following SODL language constructs:

- ✅ **system** - Concrete system declarations with stack and intent
- ✅ **template** - Reusable specification templates
- ✅ **interface** - Functionality contracts
- ✅ **module** - Units of generation with dependencies
- ✅ **policy** - Rules and constraints with severity levels
- ✅ **api** - Endpoint and model specifications
- ✅ **invariants** - System constraints
- ✅ **acceptance** - Testing criteria
- ✅ **pipeline** - Controlled generation process with steps
- ✅ **architecture** - Architectural style and layer definitions **[v0.5]**
- ✅ **design_patterns** - Design patterns (Repository, CQRS, Saga, Factory) **[v0.5]**
- ✅ **dependency_injection** - DI container configuration **[v0.5]**
- ✅ **error_handling** - Error strategies and retry policies **[v0.5]**
- ✅ **observability** - Logging, tracing, and metrics **[v0.5]**
- ✅ **testing_strategy** - Comprehensive testing definitions **[v0.5]**
- ✅ **security_patterns** - Authentication, authorization, data protection **[v0.5]**
- ✅ **ui_theme** - Reusable UI component libraries and UX rules **[v0.5]**
- ✅ **bindings** - Automatic API-UI binding **[v0.5]**

## Using the Specification Generator Skill

### Installation

```bash
# Copy to AI agent skills directory
cp -r sodl-spec-generator-skill ~/.qwen/skills/sodl-spec-generator
```

### Features

The skill provides:

1. **Production-Ready Specification Generation**
   - Architecture patterns selection
   - Dependency injection setup
   - Error handling strategies
   - Observability configuration
   - Testing strategy definitions
   - Security pattern implementation

2. **Template Generation**
   ```bash
   python scripts/sodl_validator.py generate crud output.sodl
   python scripts/sodl_validator.py generate microservice output.sodl
   python scripts/sodl_validator.py generate rest-api output.sodl
   python scripts/sodl_validator.py generate fullstack output.sodl
   ```

3. **Validation**
   ```bash
   python scripts/sodl_validator.py validate spec.sodl
   python scripts/sodl_validator.py check-production spec.sodl
   ```

### Example Prompts

```
Create a SODL specification for a task management API with JWT authentication
Generate a production-ready SODL file for an e-commerce microservice with CQRS
Convert this requirements document into a SODL specification
Create a SODL template for a CRUD application with Clean Architecture
```

## Use Cases

SODL enables:

- 📝 **Writing Specifications** - Clear, structured specifications for AI code generation
- 🤖 **AI-Driven Development** - Controlled code generation with explicit constraints
- 🔍 **Semantic Search** - Build searchable knowledge bases over specifications
- 🛠️ **Tool Development** - Create linters and IDE integrations
- 📚 **Documentation** - Self-documenting system architectures
- 🎓 **Teaching** - Structured approach to system design

## Technology Context

**SODL targets:**
- Python-based applications
- Web frameworks (FastAPI, Flask, Django)
- RESTful APIs
- Microservices
- Data processing pipelines
- CLI applications
- Real-time systems
- Full-stack applications (backend + frontend)

**SODL v0.5 supports:**
- Automatic API-UI binding
- UI theme definitions with component libraries
- Multiple architecture patterns (Clean Architecture, Hexagonal, MVC)
- Comprehensive testing strategies
- Observability configuration (logging, tracing, metrics)
- Security patterns (authentication, authorization, encryption)

**Compatible with:**
- Cursor AI editor
- Claude coding agent
- GPT-based code generators
- Any AI coding assistant

## Core Philosophy

> **"Turning prompt engineering into specification engineering"**

SODL formalizes the pipeline:

```
Intent → Architecture → Constraints → Generation → Validation
```

- **Intent**: What must be built and why
- **Architecture**: How components are structured (layers, patterns, DI)
- **Constraints**: Rules that must be enforced (policies, security)
- **Generation**: Deterministic, reviewable code creation
- **Validation**: Architecture validation and test generation

## License

This project is licensed under the **Business Source License 1.1 (BSL 1.1)**.

**Key terms:**
- ✅ Free for internal use, consulting, and embedding in larger systems
- ✅ Commercial use allowed (except competitive offerings)
- ✅ Can modify and create derivative works
- ❌ Cannot offer SODL as a competitive hosted/managed service
- 📅 Changes to Apache License 2.0 on: **2030-02-16**

See the [LICENSE](LICENSE) file for complete terms.

For commercial licensing (competitive offerings), contact: sodl.space@gmail.com

## Contributing

Contributions are welcome! You can:

- Extend the SODL language specification
- Improve the specification generator skill
- Add new documentation examples
- Enhance the validation utilities
- Create IDE integrations
- Write tutorials and guides

## Learn More

- Read the [SODL Language Specification](.sodl/SODL_spec_05.md)
- Explore [example specifications](examples/)
- Check out the [SODL Specification Generator Skill](sodl-spec-generator-skill/)
- View the [Documentation Website](website/)
- See [Field-Level Constraints Example](examples/constraints_example.sodl)

## Acknowledgments

SODL demonstrates specification-driven development, where clear intent and constraints guide AI-assisted code generation toward predictable, maintainable results.

---

**SODL v0.5** - Explicit. Structured. AI-Ready.

*"Architecture before code. Constraints before suggestions. Developer-controlled AI."*
