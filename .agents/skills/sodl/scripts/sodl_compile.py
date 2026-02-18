#!/usr/bin/env python3
"""
SODL Compilation Script
Compiles a SODL file and displays the results
"""

import sys
import json
from pathlib import Path

# Add project root to path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent.parent.parent  # Go up 4 levels to reach project root
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