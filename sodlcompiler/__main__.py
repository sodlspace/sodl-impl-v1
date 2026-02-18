#!/usr/bin/env python3
"""
SODL Compiler - Command Line Interface

Business Source License 1.1

Copyright (c) 2026 SODL Project License text copyright (c) 2017 MariaDB
Corporation Ab. "Business Source License" is a trademark of MariaDB
Corporation Ab.

Licensor: SODL Project

Licensed Work: SODL v0.3

Change Date: 2030-02-16

Change License: Apache License, Version 2.0

Additional Use Grant

You may use, copy, modify, create derivative works of, publicly perform,
publicly display, and redistribute the Licensed Work for any purpose,
including commercial purposes, provided that you do not use the Licensed
Work in a Competitive Offering.
"""

import sys
import argparse
from pathlib import Path
from sodlcompiler.compiler import SODLCompiler


def main():
    parser = argparse.ArgumentParser(
        prog="sodlcompiler",
        description="Compiler for the SODL DSL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s spec.sodl                       # Compile a spec file
  %(prog)s spec.sodl -o output_dir         # Compile with output directory
  %(prog)s spec.sodl --verbose             # Verbose output
  %(prog)s --version                       # Show version
        """
    )
    
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Input .sodl file to compile"
    )

    parser.add_argument(
        "-o", "--output",
        dest="output_dir",
        help="Output directory for generated artifacts (not yet implemented)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="SODL Compiler v0.1.0"
    )
    
    args = parser.parse_args()
    
    if not args.input_file:
        parser.print_help()
        return 1
    
    input_path = Path(args.input_file)
    
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist.", file=sys.stderr)
        return 1
    
    if not input_path.suffix.lower() == ".sodl":
        print(f"Warning: Input file does not have .sodl extension", file=sys.stderr)

    try:
        # Read the input file
        with input_path.open('r', encoding='utf-8') as f:
            source_code = f.read()

        if args.verbose:
            print(f"Compiling {input_path}...", file=sys.stderr)

        # Create compiler instance
        compiler = SODLCompiler()

        # Compile the source
        success = compiler.compile(source_code, str(input_path))
        
        # Print diagnostics
        compiler.print_diagnostics()
        
        if success:
            if args.verbose:
                print(f"✓ Compilation successful!", file=sys.stderr)
                ast = compiler.get_ast()
                if ast:
                    print(f"  Parsed {len(ast.statements)} top-level statements", file=sys.stderr)
            else:
                print("Compilation successful!")
            return 0
        else:
            if not args.verbose:
                print("Compilation failed!", file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"Error during compilation: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())