#!/usr/bin/env python3
"""
Test script to compile the example spec.sodl file
"""
from sodlcompiler.compiler import SODLCompiler
import os

def main():
    # Path to the example spec file
    spec_file_path = os.path.join(os.path.dirname(__file__), "sodl", "spec.sodl")

    # Read the example spec file
    with open(spec_file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    print("Compiling example spec.sodl...")
    print("="*50)

    # Create compiler instance
    compiler = SODLCompiler()

    # Compile the source
    success = compiler.compile(source_code, "spec.sodl")
    
    # Print diagnostics
    compiler.print_diagnostics()
    
    if success:
        print("\n[SUCCESS] Compilation successful!")
        print(f"Parsed AST with {len(compiler.get_ast().statements if compiler.get_ast() else [])} top-level statements")
    else:
        print("\n[FAILURE] Compilation failed!")
    
    return success

if __name__ == "__main__":
    main()