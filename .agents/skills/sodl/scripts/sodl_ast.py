#!/usr/bin/env python3
"""
SODL AST Generation Script
Generates detailed AST representation of SODL code
"""

import sys
import json
from pathlib import Path

# Add project root to path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent.parent.parent  # Go up 4 levels to reach project root
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