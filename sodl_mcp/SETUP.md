# SODL MCP Server - Setup Guide

Complete setup instructions for the SODL MCP Server.

## Prerequisites

### Required

- **Python 3.10 or higher**
- **uv** package manager (recommended) or pip
- **SODL project** (parent directory with `sodl/` and `sodlcompiler/`)

### Verify Prerequisites

```bash
# Check Python version
python --version  # Should show 3.10.x or higher

# Check uv installation (if using uv)
uv --version

# Verify project structure
ls -la ../sodl/      # Should show documentation files
ls -la ../sodlcompiler/   # Should show compiler files
```

## Installation Methods

### Method 1: Using uv (Recommended)

**Why uv?**
- Faster dependency resolution
- Better dependency management
- Integrated virtual environment handling
- Consistent with user preferences

**Steps:**

```bash
# Navigate to project directory
cd sodl_mcp

# Sync dependencies
uv sync

# Verify installation
uv run sodl-mcp --help
```

### Method 2: Using pip

```bash
# Navigate to project directory
cd sodl_mcp

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install in editable mode
pip install -e .

# Verify installation
sodl-mcp --help
```

### Method 3: Development Mode

For active development with additional tools:

```bash
cd sodl_mcp

# Install with dev dependencies
uv sync --extra dev

# Or with pip:
pip install -e ".[dev]"
```

## Configuration

### For Cursor IDE

#### Option 1: Project-Specific Configuration

Create or edit `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "sodl": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "D:/Work/RnD/ml/GenAI/sodl-demo/sodl_mcp",
        "sodl-mcp"
      ]
    }
  }
}
```

**Note:** Replace the path with your actual project path.

#### Option 2: User-Level Configuration

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "sodl": {
      "command": "python",
      "args": [
        "-m",
        "sodl_mcp.server"
      ],
      "cwd": "D:/Work/RnD/ml/GenAI/sodl-demo/sodl_mcp",
      "env": {
        "PYTHONPATH": "D:/Work/RnD/ml/GenAI/sodl-demo"
      }
    }
  }
}
```

#### Option 3: Using Absolute Python Path

```json
{
  "mcpServers": {
    "sodl": {
      "command": "D:/Work/RnD/ml/GenAI/sodl-demo/sodl_mcp/.venv/Scripts/python.exe",
      "args": [
        "-m",
        "sodl_mcp.server"
      ],
      "cwd": "D:/Work/RnD/ml/GenAI/sodl-demo/sodl_mcp"
    }
  }
}
```

### For Other MCP Clients

The server uses stdio transport by default. Configure your MCP client to run:

```bash
sodl-mcp
```

Or:

```bash
python -m sodl_mcp.server
```

## Verification

### Test Server Manually

```bash
# Run the server (will wait for stdio input)
cd sodl_mcp
uv run sodl-mcp

# Or with Python
python -m sodl_mcp.server
```

The server should start and wait for MCP protocol messages on stdin.

### Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_tools.py

# Run with coverage
pytest --cov=sodl_mcp
```

### Test from Cursor

1. Restart Cursor after configuring MCP
2. Open the MCP inspector (if available)
3. Check that "sodl" server is listed
4. Try accessing a resource: `sodl://docs/syntax`

## Directory Structure

The server expects this directory structure:

```
project_root/
├── sodl/                          # Documentation (required)
│   ├── SODL_DOCUMENTATION.md
│   ├── SYNTAX_REFERENCE.md
│   ├── EXAMPLES_COLLECTION.md
│   ├── API_REFERENCE.md
│   ├── DOCUMENTATION_INDEX.md
│   ├── README.md
│   ├── spec_sample.sodl
│   └── library_example.sodl
│
├── sodlcompiler/                       # Compiler (required)
│   ├── __init__.py
│   ├── compiler.py
│   ├── lexer.py
│   ├── parser.py
│   ├── semantic_analyzer.py
│   ├── ast.py
│   └── errors.py
│
└── sodl_mcp/                       # MCP Server
    ├── sodl_mcp/
    │   ├── __init__.py
    │   └── server.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_resources.py
    │   ├── test_tools.py
    │   └── test_integration.py
    ├── pyproject.toml
    ├── README.md
    └── SETUP.md (this file)
```

## Troubleshooting

### Issue: "Module not found: sodlcompiler"

**Cause:** The `sodlcompiler` module is not in the Python path.

**Solution 1:** Ensure directory structure is correct (see above)

**Solution 2:** Set PYTHONPATH:
```bash
# Windows
set PYTHONPATH=D:\Work\RnD\ml\GenAI\sodl-demo
python -m sodl_mcp.server

# Linux/Mac
export PYTHONPATH=/path/to/sodl-demo
python -m sodl_mcp.server
```

**Solution 3:** Add to MCP config:
```json
{
  "env": {
    "PYTHONPATH": "/path/to/sodl-demo"
  }
}
```

### Issue: "Documentation file not found"

**Cause:** The `sodl/` directory is not in the expected location.

**Solution:** Verify the directory structure:
```bash
ls ../sodl/sodl_DOCUMENTATION.md
```

If not found, ensure `sodl/` is at the same level as `sodl_mcp/`.

### Issue: "Server not responding"

**Cause:** Server may not be starting correctly.

**Solution 1:** Test manually:
```bash
cd sodl_mcp
uv run sodl-mcp
```

If you see errors, check the Python version and dependencies.

**Solution 2:** Check Cursor logs for MCP errors

**Solution 3:** Try a simpler configuration:
```json
{
  "mcpServers": {
    "sodl": {
      "command": "python",
      "args": ["-m", "sodl_mcp.server"],
      "cwd": "/absolute/path/to/sodl_mcp"
    }
  }
}
```

### Issue: "Permission denied" on Windows

**Cause:** PowerShell execution policy may block scripts.

**Solution:**
```powershell
# Check current policy
Get-ExecutionPolicy

# Set to allow local scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Tests fail with import errors

**Cause:** Test environment not properly configured.

**Solution:**
```bash
# Ensure you're in the right directory
cd sodl_mcp

# Reinstall in editable mode
uv sync
# or
pip install -e .

# Run tests with Python path
PYTHONPATH=.. pytest
```

## Development Setup

### For Contributing

```bash
# Clone/navigate to project
cd sodl_mcp

# Install with dev dependencies
uv sync --extra dev

# Install pre-commit hooks (if using)
pre-commit install

# Run tests
pytest

# Format code
black sodl_mcp/ tests/

# Lint code
ruff check sodl_mcp/ tests/

# Type check (if mypy is added)
mypy sodl_mcp/
```

### For Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sodl_mcp --cov-report=html

# Run specific tests
pytest tests/test_tools.py::test_compile_sodl

# Run with verbose output
pytest -v -s
```

## Performance Tuning

### Resource Caching

The server reads documentation files on each request. For production use, consider:

1. Caching file contents in memory
2. Using a content hash to detect changes
3. Implementing lazy loading

### Compilation Performance

For large SODL files:

1. Use `validate_sodl_syntax` for quick checks
2. Only use `get_sodl_ast` when detailed analysis is needed
3. Consider implementing incremental compilation

## Security Considerations

### Code Execution

The compiler parses and analyzes code but does not execute it. However:

1. Be cautious with untrusted input
2. Consider resource limits for large files
3. Monitor for potential DoS via complex inputs

### File Access

The server only reads from the `sodl/` directory. It does not:

1. Write files
2. Execute system commands
3. Access network resources

## Next Steps

After setup:

1. ✅ **Verify installation** - Run tests
2. ✅ **Configure Cursor** - Add to MCP config
3. ✅ **Test resources** - Access documentation
4. ✅ **Test tools** - Compile sample code
5. ✅ **Read README** - Learn about features
6. ✅ **Explore examples** - Try the prompts

## Support

### Getting Help

1. **Documentation Issues:**
   - Check `README.md` for usage examples
   - Review test files for code examples
   - Read SODL documentation in `../sodl/`

2. **Setup Issues:**
   - Review troubleshooting section above
   - Check directory structure
   - Verify Python version and dependencies

3. **Development Issues:**
   - Review `pyproject.toml` for configuration
   - Check test files for expected behavior
   - Run tests to identify problems

### Useful Commands

```bash
# Quick reference

# Install
uv sync

# Run server
uv run sodl-mcp

# Run tests
pytest

# Format code
black .

# Lint code
ruff check .

# Check structure
tree -L 2
```

## Version Information

- **MCP Server Version:** 0.1.0
- **SODL Language Version:** 0.3
- **Python Requirement:** >=3.10
- **MCP SDK Version:** >=1.0.0

---

**Setup Complete!** You're now ready to use the SODL MCP Server.

For usage examples, see [README.md](README.md).
For API details, see the documentation in `../sodl/`.
