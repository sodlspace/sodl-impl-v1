# SODL

**Version 0.3** - DSL for specification-driven development with AI coding agents.

## Overview

SODL is a Domain-Specific Language (DSL) that enables controlled AI-driven code generation through explicit specifications. This repository contains the complete SODL implementation including language documentation, compiler, and MCP server for AI agent integration.

## What is SODL?

SODL is indentation-based DSL for controlled AI-driven code generation. It allows developers to describe:

- **Intent**: What must be built and why
- **Architecture**: System structure, modules, and interfaces
- **Constraints**: Rules, invariants, and acceptance criteria
- **Pipeline**: Controlled generation process

The compiler transforms SODL files into structured prompts for AI coding agents, enabling deterministic, reviewable, and reproducible code generation.

## Project Components

### 1. SODL Language Documentation (`sodl/`)

Comprehensive documentation suite optimized for both humans and AI agents:

- **SODL_DOCUMENTATION.md** - Complete language guide (~1000 lines)
- **SYNTAX_REFERENCE.md** - Quick syntax lookup (~600 lines)
- **EXAMPLES_COLLECTION.md** - 17+ real-world examples (~900 lines)
- **API_REFERENCE.md** - Complete API reference (~800 lines)
- **spec_sample.sodl** - Working example specification
- **library_example.sodl** - Library example specification
- **ModernTodoApp.sodl** - Todo app example specification
- **SODL Language Specification_v0.3.pdf** - Official specification

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
sodlcompiler sodl/spec_sample.sodl

# Show AST
sodlcompiler sodl/spec_sample.sodl --show-ast

# Validate syntax only
python -m sodlcompiler.compiler --validate sodl/spec_sample.sodl
```

### Setting Up the MCP Server

```bash
# Install MCP server
cd sodl_mcp
uv sync

# Run the server
sodl-mcp
```

See `sodl_mcp/README.md` for detailed MCP server setup and configuration.

## Project Structure

```
sodl-impl-v1/
├── sodl/                           # Language documentation
│   ├── SODL_DOCUMENTATION.md           # Complete guide
│   ├── SYNTAX_REFERENCE.md             # Quick syntax reference
│   ├── EXAMPLES_COLLECTION.md          # 17+ examples
│   ├── API_REFERENCE.md                # Complete API reference
│   ├── DOCUMENTATION_INDEX.md          # Navigation guide
│   ├── spec_sample.sodl                # Working example
│   ├── library_example.sodl            # Library example
│   ├── ModernTodoApp.sodl              # Todo app example
│   └── SODL Language Specification_v0.3.pdf
│
├── sodlcompiler/                       # Compiler implementation
│   ├── __main__.py                     # CLI entry point
│   ├── lexer.py                        # Tokenization
│   ├── parser.py                       # AST parsing
│   ├── semantic_analyzer.py            # Validation
│   ├── ast.py                          # AST node definitions
│   ├── compiler.py                     # Main compiler
│   └── errors.py                       # Error handling
│
├── sodl_mcp/                       # MCP Server
│   ├── sodl_mcp/
│   │   ├── server.py                   # MCP server implementation
│   │   └── __init__.py
│   ├── tests/                          # Test suite
│   │   ├── test_resources.py
│   │   ├── test_tools.py
│   │   └── test_integration.py
│   ├── pyproject.toml                  # MCP package config
│   ├── README.md                       # MCP server docs
│   └── SETUP.md                        # Setup instructions
│
├── pyproject.toml                      # Project configuration
├── uv.lock                             # Lock file
├── test_compiler.py                    # Compiler tests
├── test_example.py                     # Example tests
└── README.md                           # This file
```

## Example SODL

Here's a simple SODL example:

```sodl
system "TodoApp":
  stack:
    language = "Python 3.12"
    web = "FastAPI"

  intent:
    primary = "Task management application"
    outcomes = ["Create and manage todos", "RESTful API"]

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

**Compatible with:**
- Cursor AI editor
- Claude coding agent
- GPT-based code generators
- Any AI coding assistant

## Core Philosophy

> **"Turning prompt engineering into specification engineering"**

SODL formalizes the pipeline:

```
Intent → Architecture → Constraints → Generation
```

- **Intent**: What must be built and why
- **Architecture**: How components are structured
- **Constraints**: Rules that must be enforced
- **Generation**: Deterministic, reviewable code creation

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

- Read the [SODL Language Specification PDF](sodl/SODL%20Language%20Specification_v0.3.pdf)
- Browse the [documentation collection](sodl/README.md)
- Explore [example specifications](sodl/spec_sample.sodl)
- Check out the [MCP server](sodl_mcp/README.md)

## Acknowledgments

SODL demonstrates specification-driven development, where clear intent and constraints guide AI-assisted code generation toward predictable, maintainable results.

---

**SODL v0.3** - Explicit. Structured. AI-Ready.

*"Architecture before code. Constraints before suggestions. Developer-controlled AI."*
