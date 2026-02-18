"""
SODL MCP Server

PROPRIETARY SOFTWARE LICENSE

Copyright (c) 2026 SODL Project. All Rights Reserved.

NOTICE: All information contained herein is, and remains the property of
SODL Project and its suppliers, if any. The intellectual and technical
concepts contained herein are proprietary to SODL Project and its suppliers
and may be covered by patents, patents in process, and are protected by trade
secret or copyright law.

Dissemination of this information or reproduction of this material is strictly
forbidden unless prior written permission is obtained from SODL Project.

Provides:
- Resources: Access to SODL documentation files
- Tools: Compile and validate SODL code with detailed feedback
"""

import sys
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

# Add parent directory to path to import sodlcompiler
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sodlcompiler.compiler import SODLCompiler

# Initialize FastMCP server
mcp = FastMCP("SODL Server", json_response=True)

# Path to documentation files
DOCS_PATH = project_root / ".sodl"


@mcp.resource("sodl://docs/main")
def get_main_documentation() -> str:
    """Get the main SODL documentation (comprehensive guide)"""
    doc_file = DOCS_PATH / "SODL_DOCUMENTATION.md"
    if doc_file.exists():
        return doc_file.read_text(encoding="utf-8")
    return "Documentation file not found"


@mcp.resource("sodl://docs/syntax")
def get_syntax_reference() -> str:
    """Get the SODL syntax reference (quick lookup)"""
    doc_file = DOCS_PATH / "SYNTAX_REFERENCE.md"
    if doc_file.exists():
        return doc_file.read_text(encoding="utf-8")
    return "Syntax reference file not found"


@mcp.resource("sodl://docs/examples")
def get_examples_collection() -> str:
    """Get the SODL examples collection (17+ real-world examples)"""
    doc_file = DOCS_PATH / "EXAMPLES_COLLECTION.md"
    if doc_file.exists():
        return doc_file.read_text(encoding="utf-8")
    return "Examples collection file not found"


@mcp.resource("sodl://docs/api")
def get_api_reference() -> str:
    """Get the SODL API reference (complete construct specifications)"""
    doc_file = DOCS_PATH / "API_REFERENCE.md"
    if doc_file.exists():
        return doc_file.read_text(encoding="utf-8")
    return "API reference file not found"


@mcp.resource("sodl://docs/index")
def get_documentation_index() -> str:
    """Get the documentation index (navigation guide)"""
    doc_file = DOCS_PATH / "DOCUMENTATION_INDEX.md"
    if doc_file.exists():
        return doc_file.read_text(encoding="utf-8")
    return "Documentation index file not found"


@mcp.resource("sodl://docs/readme")
def get_readme() -> str:
    """Get the SODL README (overview and quick start)"""
    doc_file = DOCS_PATH / "README.md"
    if doc_file.exists():
        return doc_file.read_text(encoding="utf-8")
    return "README file not found"


@mcp.resource("sodl://examples/spec_sample")
def get_spec_sample() -> str:
    """Get the sample SODL file (working example)"""
    spec_file = DOCS_PATH / "spec_sample.sodl"
    if spec_file.exists():
        return spec_file.read_text(encoding="utf-8")
    return "Sample spec file not found"


@mcp.resource("sodl://examples/library_example")
def get_library_example() -> str:
    """Get the library example SODL file"""
    spec_file = DOCS_PATH / "library_example.sodl"
    if spec_file.exists():
        return spec_file.read_text(encoding="utf-8")
    return "Library example file not found"


@mcp.tool()
def compile_sodl(code: str, filename: str = "<input>") -> dict[str, Any]:
    """
    Compile and validate SODL code.

    Args:
        code: The SODL source code to compile
        filename: Optional filename for error reporting

    Returns:
        Dictionary containing:
        - success: Boolean indicating if compilation succeeded
        - errors: List of error messages (if any)
        - warnings: List of warning messages (if any)
        - ast_summary: High-level AST summary (if successful)
    """
    compiler = SODLCompiler()
    success = compiler.compile(code, filename)
    
    error_reporter = compiler.get_error_reporter()
    
    result = {
        "success": success,
        "errors": [
            {
                "message": error.message,
                "line": error.line,
                "column": error.column,
                "severity": "error"
            }
            for error in error_reporter.get_errors()
        ],
        "warnings": [
            {
                "message": warning.message,
                "line": warning.line,
                "column": warning.column,
                "severity": "warning"
            }
            for warning in error_reporter.get_warnings()
        ],
    }
    
    # Add AST summary if compilation succeeded
    if success and compiler.ast:
        from sodlcompiler.ast import SystemBlock, InterfaceBlock, ModuleBlock, PipelineBlock
        
        ast = compiler.ast
        systems = [s for s in ast.statements if isinstance(s, SystemBlock)]
        interfaces = [s for s in ast.statements if isinstance(s, InterfaceBlock)]
        modules = [s for s in ast.statements if isinstance(s, ModuleBlock)]
        pipelines = [s for s in ast.statements if isinstance(s, PipelineBlock)]
        
        result["ast_summary"] = {
            "systems": len(systems),
            "interfaces": len(interfaces),
            "modules": len(modules),
            "pipelines": len(pipelines),
        }
    
    return result


@mcp.tool()
def validate_sodl_syntax(code: str) -> dict[str, Any]:
    """
    Quick syntax validation for SODL code.

    Args:
        code: The SODL source code to validate

    Returns:
        Dictionary containing:
        - valid: Boolean indicating if syntax is valid
        - errors: List of syntax errors (if any)
        - line_count: Number of lines in the code
    """
    compiler = SODLCompiler()
    success = compiler.compile(code, "<validation>")
    
    error_reporter = compiler.get_error_reporter()
    
    return {
        "valid": success,
        "errors": [
            {
                "message": error.message,
                "line": error.line,
                "column": error.column,
            }
            for error in error_reporter.get_errors()
        ],
        "line_count": len(code.split("\n")),
    }


@mcp.tool()
def get_sodl_ast(code: str, filename: str = "<input>") -> dict[str, Any]:
    """
    Compile SODL code and return detailed AST representation.

    Args:
        code: The SODL source code to compile
        filename: Optional filename for error reporting

    Returns:
        Dictionary containing:
        - success: Boolean indicating if compilation succeeded
        - ast: Detailed AST representation (if successful)
        - errors: List of error messages (if any)
    """
    compiler = SODLCompiler()
    success = compiler.compile(code, filename)
    
    result = {
        "success": success,
        "errors": [
            {
                "message": error.message,
                "line": error.line,
                "column": error.column,
            }
            for error in compiler.get_error_reporter().get_errors()
        ],
    }
    
    if success and compiler.ast:
        from sodlcompiler.ast import SystemBlock, InterfaceBlock, ModuleBlock, PipelineBlock
        
        ast = compiler.ast
        systems = [s for s in ast.statements if isinstance(s, SystemBlock)]
        interfaces = [s for s in ast.statements if isinstance(s, InterfaceBlock)]
        modules = [s for s in ast.statements if isinstance(s, ModuleBlock)]
        pipelines = [s for s in ast.statements if isinstance(s, PipelineBlock)]
        
        result["ast"] = {
            "systems": [
                {
                    "name": system.name.value if hasattr(system.name, 'value') else str(system.name),
                    "line": system.line,
                    "has_stack": system.stack_block is not None,
                    "has_intent": system.intent_block is not None,
                }
                for system in systems
            ],
            "interfaces": [
                {
                    "name": interface.name.name if hasattr(interface.name, 'name') else str(interface.name),
                    "line": interface.line,
                    "methods": [
                        {
                            "name": method.name.name if hasattr(method.name, 'name') else str(method.name),
                            "return_type": method.return_type.base_type if hasattr(method.return_type, 'base_type') else str(method.return_type),
                        }
                        for method in (interface.methods or [])
                    ],
                }
                for interface in interfaces
            ],
            "modules": [
                {
                    "name": module.name.name if hasattr(module.name, 'name') else str(module.name),
                    "line": module.line,
                    "has_api": module.api_block is not None,
                    "requires": len(module.requires or []),
                }
                for module in modules
            ],
            "pipelines": [
                {
                    "name": pipeline.name.value if hasattr(pipeline.name, 'value') else str(pipeline.name),
                    "line": pipeline.line,
                    "steps": len(pipeline.steps),
                }
                for pipeline in pipelines
            ],
        }
    
    return result


@mcp.prompt()
def sodl_helper(task: str, context: str = "") -> str:
    """
    Generate helpful prompts for working with SODL.

    Args:
        task: The type of help needed (e.g., "write_system", "debug_error", "learn_syntax")
        context: Optional context or code snippet
    """
    prompts = {
        "write_system": """I need to write a SODL system definition. Please help me:
1. Define the system structure with appropriate sections (stack, intent, etc.)
2. Create interfaces for data contracts
3. Define modules with their functionality
4. Set up a pipeline for code generation

Reference the SODL documentation for syntax and best practices.""",

        "debug_error": f"""I'm getting an error in my SODL code. Please help me:
1. Identify the issue in the code
2. Explain what's wrong
3. Suggest how to fix it

Context:
{context}

Use the SODL syntax reference to validate the fix.""",

        "learn_syntax": """I want to learn SODL syntax. Please:
1. Show me a simple example of a complete system
2. Explain the key constructs (system, interface, module, pipeline)
3. Provide best practices for writing SODL

Use examples from the SODL examples collection.""",

        "optimize_spec": f"""Help me optimize this SODL code:
{context}

1. Review the structure and organization
2. Suggest improvements for clarity
3. Ensure best practices are followed
4. Check for missing or redundant sections

Reference the SODL API reference for complete specifications.""",
    }

    return prompts.get(task, f"""Please help with: {task}

Context:
{context}

Use the SODL documentation resources to provide accurate guidance.""")


def main():
    """Run the MCP server"""
    # Run with stdio transport for MCP communication
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
