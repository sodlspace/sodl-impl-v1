# SODL MCP Server - Quick Start

Get the SODL MCP Server running in 5 minutes!

## Prerequisites

✓ Python 3.10 or higher  
✓ uv package manager installed  
✓ SODL project with documentation

## Installation

```bash
# Navigate to the project
cd sodl_mcp

# Install dependencies
uv sync

# Verify installation
uv run pytest
```

Expected output: **22 passed in ~1s** ✓

## Configuration

### For Cursor IDE

Create or edit your MCP configuration file:

**Windows:** `.cursor/mcp.json` in your project

```json
{
  "mcpServers": {
    "SODL": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "D:/Work/RnD/ml/GenAI/SODL-demo/sodl_mcp",
        "SODL-mcp"
      ]
    }
  }
}
```

**Linux/Mac:** `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "SODL": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/SODL-demo/sodl_mcp",
        "SODL-mcp"
      ]
    }
  }
}
```

**Important:** Replace the path with your actual project location!

## Usage Examples

### 1. Access Documentation

Ask your AI agent:

```
"Show me the SODL syntax reference"
```

The agent will use: `SODL://docs/syntax`

### 2. Validate Code

Ask your AI agent:

```
"Validate this SODL code:

system "MyApp":
  stack:
    language = "Python 3.12"
"
```

The agent will use: `compile_SODL(code)`

### 3. Get Examples

Ask your AI agent:

```
"Show me examples of SODL systems"
```

The agent will use: `SODL://docs/examples`

### 4. Debug Errors

Ask your AI agent:

```
"Why is this SODL code failing? [paste code]"
```

The agent will compile and provide detailed error feedback.

## Testing the Server

### Method 1: Run Tests

```bash
cd sodl_mcp
uv run pytest -v
```

You should see all 22 tests pass.

### Method 2: Import Check

```bash
uv run python -c "from sodl_mcp.server import mcp; print('Server ready!')"
```

### Method 3: Use in Cursor

1. Restart Cursor after adding MCP config
2. Start a new chat
3. Ask: "Can you access SODL documentation?"
4. Agent should confirm access to resources

## Available Resources

| Resource | Description |
|----------|-------------|
| `SODL://docs/main` | Complete documentation (~1000 lines) |
| `SODL://docs/syntax` | Syntax reference (~600 lines) |
| `SODL://docs/examples` | 17+ real-world examples (~900 lines) |
| `SODL://docs/api` | API reference (~800 lines) |
| `SODL://docs/index` | Documentation navigation |
| `SODL://docs/readme` | Quick overview |
| `SODL://examples/spec_sample` | Working example |
| `SODL://examples/library_example` | Library example |

## Available Tools

| Tool | Purpose |
|------|---------|
| `compile_SODL()` | Full compilation with feedback |
| `validate_SODL_syntax()` | Quick syntax check |
| `get_SODL_ast()` | Detailed AST inspection |

## Available Prompts

| Prompt | Purpose |
|--------|---------|
| `SODL_helper()` | Context-aware help |

## Troubleshooting

### Server Won't Start

**Check Python version:**
```bash
python --version  # Should be 3.10+
```

**Reinstall:**
```bash
cd sodl_mcp
uv sync --reinstall
```

### Documentation Not Found

**Check directory structure:**
```bash
ls ../sodl/SODL_DOCUMENTATION.md
```

The `sodl/` folder should be at the same level as `sodl_mcp/`.

### Tests Fail

**Run with verbose output:**
```bash
uv run pytest -v -s
```

**Check imports:**
```bash
uv run python -c "from sodl_mcp import server"
```

## Next Steps

1. ✅ **Verify installation** - Run tests
2. ✅ **Configure Cursor** - Add MCP config  
3. ✅ **Test with agent** - Ask about SODL
4. ✅ **Read README.md** - Learn all features
5. ✅ **Explore examples** - Try the tools

## Common Tasks

**Run server manually:**
```bash
cd sodl_mcp
uv run SODL-mcp
```

**Run tests:**
```bash
uv run pytest
```

**Format code:**
```bash
uv run black .
```

**Lint code:**
```bash
uv run ruff check .
```

## Support

**Documentation:**
- See [README.md](README.md) for complete documentation
- See [SETUP.md](SETUP.md) for detailed setup instructions
- See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for project overview

**Issues:**
- Check test output for diagnostics
- Review SETUP.md troubleshooting section
- Verify directory structure

---

**That's it!** You're now ready to use the SODL MCP Server. 🚀

For more details, see [README.md](README.md).
