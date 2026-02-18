---
name: sodl
description: Use this skill whenever the user wants to work with SODL (Specification Orchestration Definition Language) files. This includes compiling SODL code, validating syntax, checking for errors, converting SODL to other formats, and running SODL-related tools. If the user mentions SODL files, compilation, validation, or asks to work with SODL syntax, use this skill.
license: BSL 1.1. LICENSE.txt has complete terms
---

# SODL (Specification Orchestration Definition Language) Processing Guide

## Overview

This guide covers essential SODL processing operations using Python libraries and command-line tools. SODL is a language for defining object structures and schemas. This skill provides compilation, validation, and transformation capabilities for SODL files.

## Quick Start

```python
from sodlcompiler import compile_sodl

# Compile SODL code
result = compile_sodl(code="your_sodl_code_here")
if result.success:
    print("Compilation successful!")
    print(result.ast_summary)
else:
    print("Errors:", result.errors)
```

## SODL Compilation and Validation

### Basic Compilation
```python
# Import the SODL compiler
from sodl_mcp import compile_sodl

# Compile SODL code
code = '''
object Person {
    name: String
    age: Int
    email: String?
}
'''

result = compile_sodl(code)
if result['success']:
    print("AST Summary:", result['ast_summary'])
    print("Compiled successfully!")
else:
    print("Compilation failed:")
    for error in result['errors']:
        print(f"- {error}")
```

### Syntax Validation
```python
from sodl_mcp import validate_sodl_syntax

code = "your_sodl_code_here"
validation_result = validate_sodl_syntax(code)

if validation_result['valid']:
    print(f"SODL code is valid ({validation_result['line_count']} lines)")
else:
    print("Syntax errors found:")
    for error in validation_result['errors']:
        print(f"- {error}")
```

### Getting AST Representation
```python
from sodl_mcp import get_sodl_ast

code = '''
object User {
    id: Int
    name: String
    active: Bool
}
'''

ast_result = get_sodl_ast(code)
if ast_result['success']:
    print("AST:", ast_result['ast'])
else:
    print("Error getting AST:")
    for error in ast_result['errors']:
        print(f"- {error}")
```

## Common SODL Patterns

### Object Definitions
```sodl
object Person {
    firstName: String
    lastName: String
    age: Int
    email: String?
    address: Address?
}

object Address {
    street: String
    city: String
    zipCode: String
    country: String = "USA"  // Default value
}
```

### Enum Definitions
```sodl
enum Status {
    Active
    Inactive
    Pending
    Suspended
}

enum Priority {
    Low = 1
    Medium = 2
    High = 3
    Critical = 4
}
```

### Interface Definitions
```sodl
interface Identifiable {
    id: String
}

interface Timestamped {
    createdAt: DateTime
    updatedAt: DateTime
}

object Document implements Identifiable, Timestamped {
    id: String
    title: String
    content: String
    createdAt: DateTime
    updatedAt: DateTime
}
```

### Generic Types
```sodl
object Container<T> {
    value: T
    metadata: Map<String, String>
}

object Result<T, E> {
    success: T?
    error: E?
    isSuccess: Bool
}
```

## SODL MCP Tools

### Available MCP Functions

1. **compile_sodl(code, filename=None)** - Compiles SODL code and returns AST
2. **validate_sodl_syntax(code)** - Validates SODL syntax without full compilation
3. **get_sodl_ast(code, filename=None)** - Gets detailed AST representation

### Using MCP Tools in Scripts

#### Script: sodl_compile.py
```python
#!/usr/bin/env python3
"""
Compile a SODL file and output results
"""
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def compile_sodl(code, filename="<input>"):
    """
    Compile and validate SODL code.
    """
    try:
        from sodlcompiler.compiler import SODLCompiler
        
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
    except ImportError:
        # Fallback if compiler is not available
        return {
            "success": False,
            "errors": [{"message": "SODL compiler not available", "line": 0, "column": 0, "severity": "error"}],
            "warnings": [],
        }


def main():
    if len(sys.argv) != 2:
        print("Usage: python sodl_compile.py <sodl_file>")
        print("Note: Run from project root directory for proper module resolution")
        sys.exit(1)
        
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
            
        result = compile_sodl(code, filename)
        
        if result['success']:
            print("[OK] Compilation successful!")
            print("\nAST Summary:")
            print(json.dumps(result['ast_summary'], indent=2))
        else:
            print("[ERROR] Compilation failed:")
            for error in result['errors']:
                print(f"  - Line {error['line']}: {error['message']}")
                
    except FileNotFoundError:
        print(f"[ERROR] File {filename} not found")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

#### Script: sodl_validate.py
```python
#!/usr/bin/env python3
"""
Validate SODL syntax without full compilation
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def validate_sodl_syntax(code):
    """
    Quick syntax validation for SODL code.
    """
    try:
        from sodlcompiler.compiler import SODLCompiler
        
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
    except ImportError:
        # Fallback if compiler is not available
        return {
            "valid": False,
            "errors": [{"message": "SODL compiler not available", "line": 0, "column": 0}],
            "line_count": len(code.split("\n")),
        }


def main():
    if len(sys.argv) != 2:
        print("Usage: python sodl_validate.py <sodl_file>")
        print("Note: Run from project root directory for proper module resolution")
        sys.exit(1)
        
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
            
        result = validate_sodl_syntax(code)
        
        if result['valid']:
            print(f"[OK] SODL syntax is valid ({result['line_count']} lines)")
        else:
            print("[ERROR] Syntax errors found:")
            for error in result['errors']:
                print(f"  - Line {error['line']}: {error['message']}")
                
    except FileNotFoundError:
        print(f"[ERROR] File {filename} not found")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

#### Script: sodl_ast.py
```python
#!/usr/bin/env python3
"""
Get detailed AST representation of SODL code
"""
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def get_sodl_ast(code, filename="<input>"):
    """
    Compile SODL code and return detailed AST representation.
    """
    try:
        from sodlcompiler.compiler import SODLCompiler
        
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
    except ImportError:
        # Fallback if compiler is not available
        return {
            "success": False,
            "errors": [{"message": "SODL compiler not available", "line": 0, "column": 0}],
            "ast": {}
        }


def main():
    if len(sys.argv) != 2:
        print("Usage: python sodl_ast.py <sodl_file>")
        print("Note: Run from project root directory for proper module resolution")
        sys.exit(1)
        
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
            
        result = get_sodl_ast(code, filename)
        
        if result['success']:
            print("SODL AST Structure:")
            print(json.dumps(result['ast'], indent=2))
        else:
            print("[ERROR] Error getting AST:")
            for error in result['errors']:
                print(f"  - Line {error['line']}: {error['message']}")
                
    except FileNotFoundError:
        print(f"[ERROR] File {filename} not found")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## SODL Best Practices

### Naming Conventions
- Object names: PascalCase (e.g., `UserProfile`)
- Property names: camelCase (e.g., `firstName`)
- Enum values: PascalCase (e.g., `ActiveStatus`)

### Type Definitions
- Use optional types (`String?`, `Int?`) when values can be null
- Use generic collections: `List<String>`, `Map<String, Int>`
- Define default values for optional properties when appropriate

### Documentation
```sodl
/**
 * Represents a user in the system
 * @author System Administrator
 * @version 1.0
 */
object User {
    /**
     * Unique identifier for the user
     */
    id: String
    
    /** User's display name */
    displayName: String
    
    /** User's email address */
    email: String
}
```

## Error Handling

Common SODL errors and how to address them:

1. **Syntax Errors**: Check brackets, braces, and semicolons
2. **Type Mismatches**: Ensure property types match expected values
3. **Undefined References**: Verify all referenced types exist
4. **Duplicate Names**: Ensure unique names within scope

## Quick Reference

| Task | Command/Code |
|------|--------------|
| Compile SODL | `compile_sodl(code)` |
| Validate Syntax | `validate_sodl_syntax(code)` |
| Get AST | `get_sodl_ast(code)` |
| Object Definition | `object Name { property: Type }` |
| Enum Definition | `enum Name { Value1, Value2 }` |
| Optional Properties | `property: Type?` |
| Default Values | `property: Type = defaultValue` |

## Next Steps

- For advanced SODL features, see REFERENCE.md
- For complex transformations, see the transformation scripts in the scripts directory
- For troubleshooting common issues, see REFERENCE.md