# SODL

**Version 0.5** - DSL for specification-driven development with AI coding agents.

## Overview

SODL is a Domain-Specific Language (DSL) that enables controlled AI-driven code generation through explicit specifications. This repository contains the complete SODL v0.5 implementation including language documentation, compiler, and MCP server for AI agent integration.

SODL v0.5 introduces enhanced features including architecture patterns, dependency injection, error handling, observability, testing strategies, and security patterns.

## What is SODL?

SODL is indentation-based DSL for controlled AI-driven code generation. It allows developers to describe:

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

### 1. SODL Language Documentation

- **examples/** - Example SODL specifications including ModernTodoApp, PresentationGenerator, and more
- **releases/** - Release artifacts and documentation
- **.sodl/SODL_spec_05.md** - Language specification markdown

### 2. SODL Compiler (`sodlcompiler/`)

A Python-based compiler for SODL files with:

- Lexical analysis (tokenization)
- Syntax parsing (AST generation)
- Semantic analysis (validation)
- Detailed error reporting with line numbers
- AST inspection capabilities

### 3. SODL MCP Server (`sodl_mcp/`)

Model Context Protocol server providing AI agents with:

- Access to all documentation as MCP resources
- Real-time compilation and validation tools
- AST analysis capabilities
- Syntax validation
- Prompt templates for common tasks

## Quick Start

### Prerequisites

- Python 3.12 or higher
- uv package manager (recommended) or pip

### Installation

```bash
# Install compiler dependencies
uv sync

# Or using pip
pip install -e .
```

### Using the Compiler

```bash
# Compile a SODL file
sodlcompiler examples/ModernTodoApp.sodl

# Show AST
sodlcompiler examples/ModernTodoApp.sodl --show-ast

# Validate syntax only
python -m sodlcompiler.compiler --validate examples/ModernTodoApp.sodl
```

### Programmatic Usage

```python
from sodlcompiler import SODLCompiler, compile_source

# Compile source code
compiler = SODLCompiler()
success = compiler.compile(source_code, "app.sodl")

if success:
    ast = compiler.get_ast()
    # Traverse and analyze AST
else:
    compiler.print_diagnostics()

# See sodlcompiler/API_USAGE.md for complete API documentation
```

### Setting Up the MCP Server

```bash
# Install MCP server
cd sodl_mcp
uv sync

# Run the server
sodl-mcp
```

See `sodl_mcp/README.md` for detailed MCP server setup and configuration, including client API examples and custom prompt template extension.

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
│   └── constraints_example.sodl   # Field-level constraints example [NEW]
│
├── sodlcompiler/                   # Compiler implementation
│   ├── __main__.py                 # CLI entry point
│   ├── lexer.py                    # Tokenization
│   ├── parser.py                   # AST parsing
│   ├── semantic_analyzer.py        # Validation
│   ├── ast.py                      # AST node definitions
│   ├── compiler.py                 # Main compiler
│   ├── errors.py                   # Error handling
│   └── API_USAGE.md                # Python API documentation [NEW]
│
├── sodl_mcp/                       # MCP Server
│   ├── sodl_mcp/
│   │   ├── server.py               # MCP server implementation
│   │   └── __init__.py
│   ├── tests/                      # Test suite
│   ├── pyproject.toml              # MCP package config
│   ├── README.md                   # MCP server docs (with client API examples)
│   └── SETUP.md                    # Setup instructions
│
├── sodl-vscode-extension/          # VSCode extension for SODL
├── website/                        # Documentation website
├── tests/                          # Test suite
├── utils/                          # Utility scripts
├── releases/                       # Release artifacts
├── .github/                        # GitHub workflows and templates
├── .agents/                        # AI agent configurations
│
├── pyproject.toml                  # Project configuration
├── uv.lock                         # Lock file
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
- ✅ **architecture** - Architectural style and layer definitions **[NEW v0.5]**
- ✅ **design_patterns** - Design patterns (Repository, CQRS, Saga, Factory) **[NEW v0.5]**
- ✅ **dependency_injection** - DI container configuration **[NEW v0.5]**
- ✅ **error_handling** - Error strategies and retry policies **[NEW v0.5]**
- ✅ **observability** - Logging, tracing, and metrics **[NEW v0.5]**
- ✅ **testing_strategy** - Comprehensive testing definitions **[NEW v0.5]**
- ✅ **security_patterns** - Authentication, authorization, data protection **[NEW v0.5]**
- ✅ **ui_theme** - Reusable UI component libraries and UX rules **[ENHANCED v0.5]**
- ✅ **bindings** - Automatic API-UI binding **[NEW v0.5]**

## Development

### Running Compiler Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest test_compiler.py
```

### Testing the Compiler

```bash
# Test compilation
python test_compiler.py

# Test on examples
python test_example.py

# Debug lexer
python debug_lexer.py

# Debug tokens
python debug_tokens.py
```

### Working on the MCP Server

```bash
cd sodl_mcp

# Install dependencies
uv sync

# Run tests
pytest

# Run server
sodl-mcp
```

## Use Cases

SODL enables:

- 📝 **Writing Specifications** - Clear, structured specifications for AI code generation
- 🤖 **AI-Driven Development** - Controlled code generation with explicit constraints
- 🔍 **Semantic Search** - Build searchable knowledge bases over specifications
- 🛠️ **Tool Development** - Create compilers, linters, and IDE integrations
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
- Improve the compiler implementation
- Add new documentation examples
- Enhance the MCP server capabilities
- Create IDE integrations
- Write tutorials and guides

## Learn More

- Read the [SODL Language Specification PDF](releases/)
- Explore [example specifications](examples/)
- Read the [Compiler Python API Documentation](sodlcompiler/API_USAGE.md)
- Check out the [MCP Server with Client API Examples](sodl_mcp/README.md)
- View the [VSCode extension](sodl-vscode-extension/)
- See [Field-Level Constraints Example](examples/constraints_example.sodl)

## Acknowledgments

SODL demonstrates specification-driven development, where clear intent and constraints guide AI-assisted code generation toward predictable, maintainable results.

---

**SODL v0.5** - Explicit. Structured. AI-Ready.

*"Architecture before code. Constraints before suggestions. Developer-controlled AI."*
