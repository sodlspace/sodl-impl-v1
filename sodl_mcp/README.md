# SODL MCP Server

**Version 0.1.0** - Model Context Protocol server for SODL DSL

## Overview

The SODL MCP Server provides AI coding agents with direct access to SODL documentation and real-time compilation/validation tools. This enables agents to write, validate, and debug SODL specifications with expert-level accuracy.

## Features

### 📚 Documentation Resources

Access comprehensive SODL documentation through MCP resources:

- **`sodl://docs/main`** - Complete SODL documentation (~1000 lines)
- **`sodl://docs/syntax`** - Quick syntax reference (~600 lines)
- **`sodl://docs/examples`** - 17+ real-world examples (~900 lines)
- **`sodl://docs/api`** - Complete API reference (~800 lines)
- **`sodl://docs/index`** - Documentation navigation guide
- **`sodl://docs/readme`** - Quick start and overview
- **`sodl://examples/spec_sample`** - Working example specification
- **`sodl://examples/library_example`** - Library example specification

### 🔧 Compilation Tools

Validate and compile SODL code with detailed feedback:

#### `compile_sodl(code: str, filename: str = "<input>")`

Compile SODL code and get comprehensive feedback.

**Returns:**
```json
{
  "success": true,
  "errors": [],
  "warnings": [],
  "ast_summary": {
    "systems": 1,
    "templates": 0,
    "interfaces": 2,
    "modules": 3,
    "policies": 1,
    "pipelines": 1
  }
}
```

#### `validate_sodl_syntax(code: str)`

Quick syntax validation without full semantic analysis.

**Returns:**
```json
{
  "valid": true,
  "errors": [],
  "line_count": 150
}
```

#### `get_sodl_ast(code: str, filename: str = "<input>")`

Get detailed AST representation of compiled SODL code.

**Returns:**
```json
{
  "success": true,
  "ast": {
    "systems": [...],
    "interfaces": [...],
    "modules": [...],
    "pipelines": [...]
  },
  "errors": []
}
```

### 💡 Prompt Templates

Helper prompts for common SODL tasks:

- **`sodl_helper("write_system")`** - Help writing a new system
- **`sodl_helper("debug_error", context="...")`** - Debug errors
- **`sodl_helper("learn_syntax")`** - Learn SODL syntax
- **`sodl_helper("optimize_spec", context="...")`** - Optimize specifications

## Installation

### Using uv (recommended)

```bash
cd sodl_mcp
uv sync
```

### Using pip

```bash
cd sodl_mcp
pip install -e .
```

## Usage

### Running the Server

The server uses stdio transport for MCP communication:

```bash
sodl-mcp
```

Or directly with Python:

```bash
python -m sodl_mcp.server
```

### Configuring in Cursor

Add to your MCP configuration (`~/.cursor/mcp.json` or project-specific):

```json
{
  "mcpServers": {
    "sodl": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/sodl_mcp",
        "sodl-mcp"
      ]
    }
  }
}
```

Or with absolute path to Python:

```json
{
  "mcpServers": {
    "sodl": {
      "command": "python",
      "args": [
        "-m",
        "sodl_mcp.server"
      ],
      "cwd": "/path/to/sodl_mcp"
    }
  }
}
```

## Example Usage

### Access Documentation

```python
# In your MCP client
docs = await client.read_resource("sodl://docs/main")
syntax = await client.read_resource("sodl://docs/syntax")
examples = await client.read_resource("sodl://docs/examples")
```

### Validate SODL Code

```python
# Compile and validate
result = await client.call_tool(
    "compile_sodl",
    {
        "code": """
system "TodoApp":
  stack:
    language = "Python 3.12"
    web = "FastAPI"

  intent:
    primary = "Task management"
""",
        "filename": "todo.sodl"
    }
)

if result["success"]:
    print(f"✓ Compilation successful!")
    print(f"AST Summary: {result['ast_summary']}")
else:
    for error in result["errors"]:
        print(f"✗ Line {error['line']}: {error['message']}")
```

### Get AST Analysis

```python
# Get detailed AST
ast_result = await client.call_tool(
    "get_sodl_ast",
    {"code": sodl_code}
)

for system in ast_result["ast"]["systems"]:
    print(f"System: {system['name']}")
    print(f"  Sections: {', '.join(system['sections'])}")
```

## Architecture

```
sodl_mcp/
├── sodl_mcp/
│   ├── __init__.py          # Package initialization
│   └── server.py            # Main MCP server implementation
├── tests/
│   ├── __init__.py
│   ├── test_resources.py    # Test documentation resources
│   ├── test_tools.py        # Test compilation tools
│   └── test_integration.py  # Integration tests
├── pyproject.toml           # Project configuration
├── README.md                # This file
└── SETUP.md                 # Setup instructions
```

## How It Works

### Resources

The server exposes SODL documentation files as MCP resources. When an agent requests a resource like `sodl://docs/main`, the server reads the corresponding markdown file from the `../sodl/` directory and returns its contents.

### Tools

The compilation tools use the `sodlcompiler` module (from the parent project) to:

1. **Lex** - Tokenize the SODL source code
2. **Parse** - Build an Abstract Syntax Tree (AST)
3. **Analyze** - Perform semantic analysis and validation
4. **Report** - Generate detailed error and warning messages

### Integration with AI Agents

AI coding agents can:

1. **Learn SODL** by reading documentation resources
2. **Validate code** before presenting to users
3. **Debug errors** with detailed compiler feedback
4. **Explore AST** to understand code structure
5. **Get guidance** through prompt templates

## Development

### Setup Development Environment

```bash
cd sodl_mcp
uv sync --extra dev
```

### Run Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Code Formatting

```bash
black sodl_mcp/ tests/
ruff check sodl_mcp/ tests/
```

## Dependencies

### Runtime

- **mcp** (>=1.0.0) - Model Context Protocol SDK
- **sodlcompiler** - SODL compiler (from parent project)

### Development

- **pytest** (>=8.0.0) - Testing framework
- **pytest-asyncio** (>=0.23.0) - Async test support
- **black** (>=24.0.0) - Code formatter
- **ruff** (>=0.1.0) - Linter

## Project Status

**Current Version:** 0.1.0 (Alpha)

### ✅ Implemented

- [x] Documentation resources (8 resources)
- [x] Compilation tools (3 tools)
- [x] Prompt templates (1 prompt)
- [x] Error reporting with line numbers
- [x] AST analysis and summaries
- [x] Stdio transport support

### 🚧 Planned

- [ ] HTTP transport support
- [ ] Incremental compilation (edit suggestions)
- [ ] Syntax highlighting metadata
- [ ] Code completion suggestions
- [ ] Template generation tools
- [ ] Integration with CI/CD pipelines

## Use Cases

### For AI Coding Agents

- **Learn sodl syntax** from comprehensive documentation
- **Validate specifications** before code generation
- **Debug compilation errors** with precise feedback
- **Understand structure** through AST inspection

### For Developers

- **Quick reference** lookup during development
- **Syntax validation** in editor/IDE
- **Error diagnostics** with detailed messages
- **Code exploration** via AST analysis

### For Teams

- **Centralized documentation** access
- **Consistent validation** across tools
- **Standardized error messages**
- **Automated quality checks**

## Contributing

Contributions are welcome! Please:

1. Follow the existing code style (Black + Ruff)
2. Add tests for new features
3. Update documentation as needed
4. Ensure all tests pass

## Troubleshooting

### Server Won't Start

**Check Python version:**
```bash
python --version  # Should be 3.10+
```

**Verify installation:**
```bash
uv run sodl-mcp --help
```

### Documentation Not Found

The server expects the `sodl/` directory to be in the parent directory of `sodl_mcp/`. Ensure the directory structure is:

```
project_root/
├── sodl/           # Documentation files
│   ├── sodl_DOCUMENTATION.md
│   ├── SYNTAX_REFERENCE.md
│   └── ...
└── sodl_mcp/        # MCP server
    ├── sodl_mcp/
    └── ...
```

### Compilation Errors

Make sure the `sodlcompiler` module is accessible. The server adds the parent directory to `sys.path`, so the project structure should be:

```
project_root/
├── sodlcompiler/        # Compiler module
│   ├── compiler.py
│   ├── lexer.py
│   └── ...
└── sodl_mcp/        # MCP server
```

## License

This project follows the same license as the SODL project.

## Support

For issues, questions, or contributions:

1. Check the documentation in `sodl/`
2. Review test files in `tests/`
3. Examine example usage in this README

---

**SODL MCP Server v0.1.0** - Empowering AI agents with SODL expertise.

*"Turn documentation into capabilities. Turn validation into confidence."*
