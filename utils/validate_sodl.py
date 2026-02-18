#!/usr/bin/env python3
"""
Direct SODL validation script using sodlcompiler
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def validate_sodl_file(filepath):
    """Validate a SODL file using the compiler directly."""
    try:
        from sodlcompiler.compiler import SODLCompiler
        
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        compiler = SODLCompiler()
        success = compiler.compile(code, filepath)
        
        if success:
            print(f"[OK] SODL syntax is valid ({len(code.splitlines())} lines)")
            
            # Show AST summary if available
            if compiler.ast:
                from sodlcompiler.ast import SystemBlock, InterfaceBlock, ModuleBlock, PipelineBlock
                
                ast = compiler.ast
                systems = [s for s in ast.statements if isinstance(s, SystemBlock)]
                interfaces = [s for s in ast.statements if isinstance(s, InterfaceBlock)]
                modules = [s for s in ast.statements if isinstance(s, ModuleBlock)]
                pipelines = [s for s in ast.statements if isinstance(s, PipelineBlock)]
                
                print(f"  - Found {len(systems)} systems")
                print(f"  - Found {len(interfaces)} interfaces")
                print(f"  - Found {len(modules)} modules")
                print(f"  - Found {len(pipelines)} pipelines")
        else:
            print("[ERROR] SODL compilation failed!")
            error_reporter = compiler.get_error_reporter()
            for error in error_reporter.get_errors():
                print(f"  - Line {error.line}: {error.message}")
                
    except ImportError as e:
        print(f"[ERROR] Could not import SODL compiler: {e}")
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
    except Exception as e:
        print(f"[ERROR] Error validating SODL file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_sodl.py <sodl_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    validate_sodl_file(filepath)