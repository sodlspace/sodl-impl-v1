#!/usr/bin/env python3
"""
SODL Validation Script
Validates SODL syntax without full compilation
"""

import sys
from pathlib import Path

# Add project root to path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent.parent.parent  # Go up 4 levels to reach project root
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