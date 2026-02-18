import sys
from pathlib import Path

# Add project root to path
project_root = Path().resolve()
sys.path.insert(0, str(project_root))

from sodlcompiler.compiler import SODLCompiler
from sodlcompiler.ast import SystemBlock, InterfaceBlock, ModuleBlock, PipelineBlock

def analyze_sodl_file(filepath):
    """Analyze a SODL file and provide detailed information."""
    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    # Create compiler and compile
    compiler = SODLCompiler()
    success = compiler.compile(code, filepath)

    if not success:
        print('[ERROR] Compilation failed!')
        error_reporter = compiler.get_error_reporter()
        for error in error_reporter.get_errors():
            print(f'  - Line {error.line}: {error.message}')
        return

    if not compiler.ast:
        print('[WARNING] Compiled successfully but no AST generated')
        return

    ast = compiler.ast
    systems = [s for s in ast.statements if isinstance(s, SystemBlock)]
    interfaces = [s for s in ast.statements if isinstance(s, InterfaceBlock)]
    modules = [s for s in ast.statements if isinstance(s, ModuleBlock)]
    pipelines = [s for s in ast.statements if isinstance(s, PipelineBlock)]
    
    print('[OK] AST Structure Analysis:')
    print(f'  Total statements: {len(ast.statements)}')
    print(f'  Systems: {len(systems)}')
    print(f'  Interfaces: {len(interfaces)}')
    print(f'  Modules: {len(modules)}')
    print(f'  Pipelines: {len(pipelines)}')
    
    # Print details about each system
    for system in systems:
        print(f'\nSystem: {system.name.value if hasattr(system.name, "value") else str(system.name)}')
        print(f'  Line: {system.line}')
        print(f'  Has Stack: {system.stack_block is not None}')
        print(f'  Has Intent: {system.intent_block is not None}')
        
    # Print details about each interface
    for interface in interfaces:
        print(f'\nInterface: {interface.name.name if hasattr(interface.name, "name") else str(interface.name)}')
        print(f'  Line: {interface.line}')
        if hasattr(interface, 'methods') and interface.methods:
            print(f'  Methods: {len(interface.methods)}')
            for method in interface.methods:
                method_name = method.name.name if hasattr(method.name, 'name') else str(method.name)
                return_type = method.return_type.base_type if hasattr(method.return_type, 'base_type') else str(method.return_type)
                print(f'    - {method_name}: {return_type}')
        
    # Print details about each module
    for module in modules:
        print(f'\nModule: {module.name.name if hasattr(module.name, "name") else str(module.name)}')
        print(f'  Line: {module.line}')
        print(f'  Has API: {module.api_block is not None}')
        if hasattr(module, 'requires') and module.requires:
            print(f'  Requires: {len(module.requires)} modules')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_sodl.py <sodl_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    analyze_sodl_file(filepath)