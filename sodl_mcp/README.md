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

### Access Documentation Resources

AI agents can retrieve documentation using the MCP resource protocol:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async with stdio_client(server_parameters) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize the session
        await session.initialize()
        
        # List available resources
        resources = await session.list_resources()
        for resource in resources.resources:
            print(f"Resource: {resource.uri}")
        
        # Read specific documentation
        docs = await session.read_resource("sodl://docs/main")
        syntax = await session.read_resource("sodl://docs/syntax")
        examples = await session.read_resource("sodl://docs/examples")
```

### Using Tools: Compile and Validate

```python
# Compile and validate SODL code
result = await session.call_tool(
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

# Parse the result
if result["success"]:
    print(f"✓ Compilation successful!")
    print(f"AST Summary: {result['ast_summary']}")
else:
    print("Compilation errors:")
    for error in result["errors"]:
        print(f"  Line {error['line']}, Column {error['column']}: {error['message']}")
```

### Get Detailed AST Analysis

```python
# Get detailed AST representation
ast_result = await session.call_tool(
    "get_sodl_ast",
    {"code": sodl_code, "filename": "app.sodl"}
)

if ast_result["success"]:
    ast = ast_result["ast"]
    
    # Iterate through systems
    for system in ast["systems"]:
        print(f"System: {system['name']} (line {system['line']})")
        if system['has_stack']:
            print("  Has stack configuration")
        if system['has_intent']:
            print("  Has intent definition")
    
    # Iterate through interfaces
    for interface in ast["interfaces"]:
        print(f"Interface: {interface['name']}")
        for method in interface['methods']:
            print(f"  Method: {method['name']}() -> {method['return_type']}")
    
    # Iterate through modules
    for module in ast["modules"]:
        print(f"Module: {module['name']}")
        if module['has_api']:
            print("  Has API definitions")
        if module['requires'] > 0:
            print(f"  Requires {module['requires']} dependencies")
```

### Quick Syntax Validation

```python
# Quick syntax check without full compilation
validation = await session.call_tool(
    "validate_sodl_syntax",
    {"code": sodl_code}
)

if validation["valid"]:
    print(f"✓ Syntax valid ({validation['line_count']} lines)")
else:
    print("Syntax errors:")
    for error in validation["errors"]:
        print(f"  Line {error['line']}: {error['message']}")
```

### Using Prompt Templates

```python
# Get help prompt for writing a system
prompt = await session.get_prompt(
    "sodl_helper",
    {"task": "write_system"}
)
print(prompt.messages)

# Get help with debugging
debug_prompt = await session.get_prompt(
    "sodl_helper",
    {
        "task": "debug_error",
        "context": my_sodl_code_with_error
    }
)

# Get optimization suggestions
optimize_prompt = await session.get_prompt(
    "sodl_helper",
    {
        "task": "optimize_spec",
        "context": my_existing_spec
    }
)
```

### Complete AI Agent Integration Example

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def sodl_agent_workflow():
    """Example AI agent workflow using SODL MCP Server"""
    
    # Server parameters - adjust path to your setup
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "sodl_mcp.server"],
        cwd="/path/to/sodl_mcp"
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Step 1: Learn syntax from documentation
            docs = await session.read_resource("sodl://docs/syntax")
            
            # Step 2: Generate SODL code based on requirements
            sodl_code = '''
system "UserManagement":
  stack:
    language = "Python 3.12"
    web = "FastAPI"
  
  intent:
    primary = "User authentication and management"
    outcomes = ["User registration", "Login/logout", "Profile management"]

interface IUserService:
  method create_user(email: str, password: str) -> User
  method get_user(id: str) -> Optional[User]
  method delete_user(id: str) -> Result[void, Error]

module UserAPI:
  requires = [IUserService]
  implements = [IUserService]
  
  api:
    endpoint "POST /api/users" -> UserResponse
    endpoint "GET /api/users/{id}" -> UserResponse
    endpoint "DELETE /api/users/{id}" -> void
'''
            
            # Step 3: Validate the code
            result = await session.call_tool(
                "compile_sodl",
                {"code": sodl_code, "filename": "user_mgmt.sodl"}
            )
            
            if result["success"]:
                print("✓ SODL specification is valid!")
                
                # Step 4: Get AST for further processing
                ast = await session.call_tool(
                    "get_sodl_ast",
                    {"code": sodl_code}
                )
                
                # Step 5: Use AST to generate code generation plan
                print(f"Found {ast['ast']['systems'][0]['name']}")
                print(f"  Interfaces: {len(ast['ast']['interfaces'])}")
                print(f"  Modules: {len(ast['ast']['modules'])}")
            else:
                print("✗ Validation failed:")
                for error in result["errors"]:
                    print(f"  {error['line']}: {error['message']}")

# Run the workflow
asyncio.run(sodl_agent_workflow())
```

### Error Handling and Diagnostics

```python
async def compile_with_detailed_errors(session, sodl_code: str):
    """Compile SODL code with comprehensive error reporting"""
    
    result = await session.call_tool(
        "compile_sodl",
        {"code": sodl_code, "filename": "app.sodl"}
    )
    
    # Structured error report
    report = {
        "success": result["success"],
        "file": "app.sodl",
        "errors": [],
        "warnings": []
    }
    
    # Process errors
    for error in result.get("errors", []):
        report["errors"].append({
            "location": f"{error['line']}:{error['column']}",
            "message": error["message"],
            "severity": error["severity"]
        })
    
    # Process warnings
    for warning in result.get("warnings", []):
        report["warnings"].append({
            "location": f"{warning['line']}:{warning['column']}",
            "message": warning["message"],
            "severity": warning["severity"]
        })
    
    return report

# Usage
report = await compile_with_detailed_errors(session, my_sodl_code)
if not report["success"]:
    for error in report["errors"]:
        print(f"[ERROR] {error['location']}: {error['message']}")
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

### Prompt Templates

The built-in `sodl_helper` prompt provides predefined templates for common tasks. The server uses a dictionary-based approach to map task names to prompt templates.

### Integration with AI Agents

AI coding agents can:

1. **Learn SODL** by reading documentation resources
2. **Validate code** before presenting to users
3. **Debug errors** with detailed compiler feedback
4. **Explore AST** to understand code structure
5. **Get guidance** through prompt templates

---

## Extending Prompt Templates

### Understanding the Prompt Mechanism

The MCP server's `sodl_helper` prompt uses a dictionary-based template system:

```python
@mcp.prompt()
def sodl_helper(task: str, context: str = "") -> str:
    prompts = {
        "write_system": """...template...""",
        "debug_error": """...template...""",
        "learn_syntax": """...template...""",
        "optimize_spec": """...template...""",
    }
    return prompts.get(task, default_prompt)
```

### Adding Custom Prompt Templates

To add custom prompt templates for specialized AI generation tasks:

#### Option 1: Extend the Server (Recommended)

Add new prompt templates directly to `server.py`:

```python
@mcp.prompt()
def sodl_custom_helper(
    task: str, 
    domain: str = "", 
    complexity: str = "medium",
    context: str = ""
) -> str:
    """
    Custom prompt generator for specialized AI tasks.
    
    Args:
        task: The task type (e.g., "generate_microservice", "create_test_suite")
        domain: Application domain (e.g., "fintech", "healthcare", "ecommerce")
        complexity: Complexity level ("simple", "medium", "enterprise")
        context: Additional context or existing SODL code
    """
    templates = {
        "generate_microservice": f"""
You are generating a microservice specification in SODL.

Domain: {domain}
Complexity: {complexity}

Requirements:
1. Define system with appropriate stack
2. Create interfaces for all service contracts
3. Define modules with API endpoints
4. Set up CI/CD pipeline
5. Include security policies

Context:
{context}

Generate a complete SODL specification following Clean Architecture principles.
""",
        
        "create_test_suite": f"""
You are creating a comprehensive test strategy in SODL.

Domain: {domain}
Complexity: {complexity}

Define:
1. Unit test requirements for all modules
2. Integration test scenarios
3. E2E test flows
4. Performance testing criteria
5. Security testing requirements

Context:
{context}

Generate SODL acceptance criteria with measurable gates.
""",
        
        "security_review": f"""
You are performing a security review of a SODL specification.

Domain: {domain}
Complexity: {complexity}

Review for:
1. Authentication mechanisms
2. Authorization patterns
3. Data encryption requirements
4. Input validation rules
5. Audit logging requirements

Context:
{context}

Identify security gaps and suggest policy additions.
"""
    }
    
    return templates.get(task, f"Unknown task: {task}")
```

#### Option 2: External Template Configuration

For dynamic template loading, create a template configuration file:

**`prompt_templates.json`:**
```json
{
  "templates": {
    "generate_microservice": {
      "description": "Generate a microservice SODL specification",
      "parameters": ["domain", "complexity", "context"],
      "template": "You are generating a microservice...\nDomain: {domain}\n..."
    },
    "create_test_suite": {
      "description": "Create comprehensive test strategy",
      "parameters": ["domain", "context"],
      "template": "You are creating test strategy...\nDomain: {domain}\n..."
    }
  }
}
```

**Load templates dynamically in server.py:**
```python
import json
from pathlib import Path

TEMPLATES_FILE = Path(__file__).parent / "prompt_templates.json"

def load_custom_templates():
    """Load custom prompt templates from configuration file"""
    if TEMPLATES_FILE.exists():
        with open(TEMPLATES_FILE) as f:
            return json.load(f)["templates"]
    return {}

@mcp.prompt()
def sodl_dynamic_prompt(template_name: str, **kwargs) -> str:
    """
    Dynamic prompt generator using external templates.
    
    Args:
        template_name: Name of the template to use
        **kwargs: Template parameters
    """
    templates = load_custom_templates()
    
    if template_name not in templates:
        return f"Template '{template_name}' not found. Available: {list(templates.keys())}"
    
    template = templates[template_name]["template"]
    return template.format(**kwargs)
```

### Custom Prompt Generation Logic

For highly specialized AI generation tasks that require custom logic beyond simple templates:

#### Example: Architecture-Aware Prompt Generation

```python
from sodlcompiler.ast import SystemBlock, ModuleBlock, InterfaceBlock

@mcp.prompt()
def architecture_aware_prompt(
    sodl_code: str,
    generation_goal: str,
    architectural_constraints: list[str] = None
) -> str:
    """
    Generate context-aware prompts based on SODL AST analysis.
    
    Args:
        sodl_code: The SODL source code to analyze
        generation_goal: What the AI should generate
        architectural_constraints: List of architectural rules to enforce
    """
    # Compile and analyze the SODL code
    compiler = SODLCompiler()
    compiler.compile(sodl_code, "<analysis>")
    
    if not compiler.ast:
        return "Error: Could not parse SODL code"
    
    ast = compiler.ast
    
    # Extract architectural information
    systems = [s for s in ast.statements if isinstance(s, SystemBlock)]
    modules = [s for s in ast.statements if isinstance(s, ModuleBlock)]
    interfaces = [s for s in ast.statements if isinstance(s, InterfaceBlock)]
    
    # Build architectural context
    arch_context = []
    
    for system in systems:
        if system.stack_block:
            stack = system.stack_block.properties
            arch_context.append(f"Technology Stack: {stack}")
        
        if system.intent_block:
            intent = system.intent_block.primary.value if system.intent_block.primary else "Unknown"
            arch_context.append(f"System Intent: {intent}")
    
    arch_context.append(f"Modules: {len(modules)}")
    arch_context.append(f"Interfaces: {len(interfaces)}")
    
    # Add constraint enforcement
    constraint_rules = ""
    if architectural_constraints:
        constraint_rules = "\n\nArchitectural Constraints:\n"
        for i, constraint in enumerate(architectural_constraints, 1):
            constraint_rules += f"{i}. {constraint}\n"
    
    # Generate the prompt
    prompt = f"""
You are generating code based on a SODL specification.

## Architectural Context
{chr(10).join(arch_context)}

## Generation Goal
{generation_goal}
{constraint_rules}

## Instructions
1. Analyze the SODL specification structure
2. Follow the defined architecture patterns
3. Respect all module dependencies and interfaces
4. Generate code that satisfies the stated intent
5. Include appropriate error handling and validation

## Output Format
- Organize code by module boundaries
- Include type annotations
- Add documentation strings
- Follow the technology stack conventions
"""
    
    return prompt
```

#### Example: Domain-Specific Prompt Generation

```python
@mcp.prompt()
def domain_specific_prompt(
    sodl_code: str,
    domain: str,
    compliance_requirements: list[str] = None
) -> str:
    """
    Generate domain-specific prompts with compliance requirements.
    
    Args:
        sodl_code: The SODL source code
        domain: Application domain (e.g., "healthcare", "finance", "aviation")
        compliance_requirements: List of compliance standards to meet
    """
    domain_rules = {
        "healthcare": {
            "standards": ["HIPAA", "HL7 FHIR"],
            "requirements": [
                "All PHI must be encrypted at rest and in transit",
                "Audit logging for all data access",
                "Role-based access control",
                "Data retention policies"
            ]
        },
        "finance": {
            "standards": ["PCI DSS", "SOX", "GDPR"],
            "requirements": [
                "Payment data encryption",
                "Transaction audit trail",
                "Segregation of duties",
                "Data privacy controls"
            ]
        },
        "aviation": {
            "standards": ["DO-178C", "ARP4754"],
            "requirements": [
                "Safety-critical code certification",
                "Requirements traceability",
                "Formal verification where applicable",
                "Comprehensive testing coverage"
            ]
        }
    }
    
    domain_info = domain_rules.get(domain.lower(), {})
    
    compliance_section = ""
    if compliance_requirements:
        compliance_section = "\n## Compliance Requirements\n"
        for req in compliance_requirements:
            compliance_section += f"- {req}\n"
    
    if domain_info:
        compliance_section += f"\n## Domain Standards\n"
        for standard in domain_info.get("standards", []):
            compliance_section += f"- Comply with {standard}\n"
        compliance_section += f"\n## Domain Requirements\n"
        for req in domain_info.get("requirements", []):
            compliance_section += f"- {req}\n"
    
    prompt = f"""
You are generating a {domain} application from SODL specifications.
{compliance_section}

## Generation Guidelines

1. **Security First**: All data must be protected according to {domain} standards
2. **Audit Trail**: Log all significant operations
3. **Validation**: Validate all inputs against defined constraints
4. **Error Handling**: Implement comprehensive error handling
5. **Testing**: Generate tests that verify compliance requirements

Review the SODL specification carefully and generate code that:
- Meets all stated functional requirements
- Complies with {domain} industry standards
- Implements all specified security controls
- Provides complete audit trails
"""
    
    return prompt
```

### Testing Custom Prompts

```python
async def test_custom_prompts(session):
    """Test custom prompt generation"""
    
    # Test architecture-aware prompt
    arch_prompt = await session.get_prompt(
        "architecture_aware_prompt",
        {
            "sodl_code": my_sodl_code,
            "generation_goal": "Generate FastAPI implementation",
            "architectural_constraints": [
                "Use dependency injection",
                "Follow repository pattern",
                "Implement CQRS for writes"
            ]
        }
    )
    print(arch_prompt.messages)
    
    # Test domain-specific prompt
    domain_prompt = await session.get_prompt(
        "domain_specific_prompt",
        {
            "sodl_code": my_sodl_code,
            "domain": "healthcare",
            "compliance_requirements": [
                "HIPAA compliance required",
                "All access must be logged"
            ]
        }
    )
    print(domain_prompt.messages)
```

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
