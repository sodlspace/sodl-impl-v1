# SODL Compiler Python API

Complete guide to programmatically using the SODL Compiler in Python applications.

## Table of Contents

- [Quick Start](#quick-start)
- [Compiler API](#compiler-api)
- [AST Node Types](#ast-node-types)
- [AST Traversal Patterns](#ast-traversal-patterns)
- [Error Handling](#error-handling)
- [Examples](#examples)

---

## Quick Start

```python
from sodlcompiler import SODLCompiler, compile_source

# Create a compiler instance
compiler = SODLCompiler()

# Compile SODL source code
source_code = '''
system "MyApp":
  stack:
    language = "Python 3.12"
  intent:
    primary = "My application"
'''

success = compiler.compile(source_code, "myapp.sodl")

if success:
    print("Compilation successful!")
    ast = compiler.get_ast()
else:
    compiler.print_diagnostics()
```

---

## Compiler API

### SODLCompiler Class

The main compiler class providing full compilation pipeline.

#### Constructor

```python
compiler = SODLCompiler()
```

#### Methods

##### `compile(source_code: str, filename: str = "<input>") -> bool`

Compiles SODL source code through all phases (lexing, parsing, semantic analysis).

**Parameters:**
- `source_code` (str): The SODL source code to compile
- `filename` (str): Optional filename for error reporting

**Returns:**
- `bool`: `True` if compilation succeeds, `False` otherwise

**Example:**
```python
compiler = SODLCompiler()
success = compiler.compile(source_code, "app.sodl")
```

##### `get_ast() -> Optional[Program]`

Returns the parsed Abstract Syntax Tree.

**Returns:**
- `Program`: The root AST node, or `None` if parsing failed

**Example:**
```python
ast = compiler.get_ast()
if ast:
    for stmt in ast.statements:
        print(type(stmt).__name__)
```

##### `get_error_reporter() -> ErrorReporter`

Returns the error reporter for detailed diagnostics.

**Example:**
```python
reporter = compiler.get_error_reporter()
for error in reporter.get_errors():
    print(f"Error at {error.line}:{error.column}: {error.message}")
```

##### `has_errors() -> bool`

Check if compilation produced any errors.

**Example:**
```python
if compiler.has_errors():
    print("Compilation failed")
```

##### `has_warnings() -> bool`

Check if compilation produced any warnings.

**Example:**
```python
if compiler.has_warnings():
    for warning in compiler.get_error_reporter().get_warnings():
        print(f"Warning: {warning.message}")
```

##### `print_diagnostics()`

Print all diagnostics to stdout.

**Example:**
```python
compiler.print_diagnostics()
```

---

### Convenience Function

#### `compile_source(source_code: str, filename: str = "<input>") -> SODLCompiler`

Compiles source code and returns the compiler instance for further inspection.

**Example:**
```python
from sodlcompiler import compile_source

compiler = compile_source(source_code, "app.sodl")
if compiler.has_errors():
    compiler.print_diagnostics()
else:
    ast = compiler.get_ast()
```

---

## AST Node Types

### Root Node

#### `Program`

The root node of every SODL AST.

**Properties:**
- `statements`: List of top-level declarations (System, Interface, Module, Pipeline, Policy, Template)
- `line`, `column`: Source position (always 0 for root)

**Example:**
```python
from sodlcompiler.ast import Program

ast = compiler.get_ast()
if isinstance(ast, Program):
    print(f"Found {len(ast.statements)} top-level declarations")
```

---

### Declaration Nodes

#### `SystemBlock`

Represents a `system` declaration.

**Properties:**
- `name` (StringLiteral): System name
- `version` (StringLiteral, optional): Version string
- `stack_block` (StackBlock, optional): Technology stack
- `intent_block` (IntentBlock, optional): System intent
- `policies` (List[PolicyBlock]): Applied policies
- `extends` (str, optional): Extended template name
- `override_ops`: Override/append/remove operations

**Example:**
```python
for stmt in ast.statements:
    if isinstance(stmt, SystemBlock):
        print(f"System: {stmt.name.value}")
        if stmt.version:
            print(f"  Version: {stmt.version.value}")
```

#### `TemplateBlock`

Represents a reusable `template` declaration.

**Properties:**
- `name` (StringLiteral): Template name
- `version` (StringLiteral, optional): Version string
- `stack_block` (StackBlock, optional): Default technology stack
- `intent_block` (IntentBlock, optional): Default intent
- `policies` (List[PolicyBlock]): Default policies
- `extends` (str, optional): Parent template name

#### `InterfaceBlock`

Represents an `interface` contract declaration.

**Properties:**
- `name` (Identifier): Interface name
- `doc` (StringLiteral, optional): Documentation string
- `fields` (List[FieldDefinition]): Interface fields
- `models` (List[ModelDefinition]): Data models
- `methods` (List[MethodDefinition]): Method signatures
- `invariants` (List[InvariantDefinition]): Interface invariants
- `extends` (str, optional): Extended interface name

**Example:**
```python
for stmt in ast.statements:
    if isinstance(stmt, InterfaceBlock):
        print(f"Interface: {stmt.name.name}")
        for method in stmt.methods:
            print(f"  Method: {method.name.name}() -> {method.return_type.base_type}")
```

#### `ModuleBlock`

Represents a `module` implementation unit.

**Properties:**
- `name` (Identifier): Module name
- `doc` (StringLiteral, optional): Documentation string
- `owns` (List[StringLiteral]): Owned resources
- `requires` (List[Identifier]): Required interfaces
- `implements` (List[Identifier]): Implemented interfaces
- `exports` (List[Identifier]): Exported interfaces
- `api_block` (APIBlock, optional): API definitions
- `invariants` (List[InvariantDefinition]): Module invariants
- `acceptance` (List[TestDefinition]): Acceptance criteria
- `artifacts` (List[StringLiteral]): Generated artifacts
- `config_block` (ConfigBlock, optional): Configuration

**Example:**
```python
for stmt in ast.statements:
    if isinstance(stmt, ModuleBlock):
        print(f"Module: {stmt.name.name}")
        if stmt.requires:
            print(f"  Requires: {[r.name for r in stmt.requires]}")
        if stmt.api_block and stmt.api_block.endpoints:
            for ep in stmt.api_block.endpoints:
                print(f"  Endpoint: {ep.method} {ep.path}")
```

#### `PolicyBlock`

Represents a `policy` with rules.

**Properties:**
- `name` (Identifier): Policy name
- `rules` (List[RuleDefinition]): Policy rules

#### `PipelineBlock`

Represents a generation `pipeline`.

**Properties:**
- `name` (StringLiteral): Pipeline name
- `steps` (List[StepBlock]): Pipeline steps

---

### Nested Block Nodes

#### `StackBlock`

Technology stack configuration.

**Properties:**
- `properties` (dict): Stack properties (language, web, database, etc.)

**Example:**
```python
if system.stack_block:
    for key, value in system.stack_block.properties.items():
        print(f"  {key}: {value}")
```

#### `IntentBlock`

System intent declaration.

**Properties:**
- `primary` (StringLiteral, optional): Primary purpose
- `outcomes` (List[StringLiteral]): Expected outcomes
- `out_of_scope` (List[StringLiteral]): Explicitly out-of-scope items

#### `APIBlock`

API definitions within a module.

**Properties:**
- `endpoints` (List[EndpointDefinition]): API endpoints
- `models` (List[ModelDefinition]): API-specific models

#### `ConfigBlock`

Module configuration.

**Properties:**
- `properties` (dict): Configuration key-value pairs

---

### Definition Nodes

#### `FieldDefinition`

Field within a model or interface.

**Properties:**
- `name` (Identifier): Field name
- `type_annotation` (TypeAnnotation): Field type
- `constraints` (str, optional): Inline constraints (e.g., `(min_length=3)`)

#### `ModelDefinition`

Data model definition.

**Properties:**
- `name` (Identifier): Model name
- `fields` (List[FieldDefinition]): Model fields

#### `MethodDefinition`

Method signature in an interface.

**Properties:**
- `name` (Identifier): Method name
- `params` (List[tuple[Identifier, TypeAnnotation]]): Parameters
- `return_type` (TypeAnnotation): Return type
- `is_override` (bool): Whether method overrides parent

#### `EndpointDefinition`

API endpoint definition.

**Properties:**
- `method` (str): HTTP method (GET, POST, etc.)
- `path` (str): Endpoint path
- `return_type` (str): Response type description

#### `RuleDefinition`

Policy rule definition.

**Properties:**
- `description` (StringLiteral): Rule description
- `severity` (StringLiteral): Severity level (critical, high, medium, low)

#### `InvariantDefinition`

System/module invariant.

**Properties:**
- `description` (StringLiteral): Invariant description

#### `TestDefinition`

Acceptance test definition.

**Properties:**
- `description` (StringLiteral): Test description

---

### Step and Operator Nodes

#### `StepBlock`

Pipeline step definition.

**Properties:**
- `name` (Identifier): Step name
- `output` (StringLiteral, optional): Output artifact type
- `require` (StringLiteral, optional): Requirement description
- `modules` (List[Identifier]): Modules involved
- `gate` (StringLiteral, optional): Gate condition

#### `OverrideStatement`

Override operator: `override block.field = value`

**Properties:**
- `path` (List[str]): Path to overridden field
- `value` (StringLiteral): New value

#### `AppendStatement`

Append operator: `append block.field += value`

**Properties:**
- `path` (List[str]): Path to appended field
- `value` (StringLiteral): Value to append

#### `RemoveStatement`

Remove operator: `remove block.field -= value`

**Properties:**
- `path` (List[str]): Path to field
- `value` (StringLiteral): Value to remove

---

### Type System Nodes

#### `TypeAnnotation`

Type annotation for fields and parameters.

**Properties:**
- `base_type` (str): Base type name (str, int, bool, etc.)
- `is_optional` (bool): Whether type is `Optional[T]`
- `is_list` (bool): Whether type is `List[T]`
- `generic_arg` (TypeAnnotation, optional): Single generic argument
- `generic_args` (List[TypeAnnotation]): Multiple generic arguments (e.g., `Result<T, E>`)

**Examples:**
```python
# str
TypeAnnotation(base_type="str")

# Optional[str]
TypeAnnotation(base_type="str", is_optional=True)

# List[int]
TypeAnnotation(base_type="int", is_list=True)

# Result<User, Error>
TypeAnnotation(
    base_type="Result",
    generic_args=[
        TypeAnnotation(base_type="User"),
        TypeAnnotation(base_type="Error")
    ]
)
```

---

### Literal and Identifier Nodes

#### `Identifier`

Identifier reference.

**Properties:**
- `name` (str): Identifier name

#### `StringLiteral`

String literal value.

**Properties:**
- `value` (str): String content (without quotes)

#### `NumberLiteral`

Number literal value.

**Properties:**
- `value` (int): Numeric value

---

## AST Traversal Patterns

### Finding All Systems

```python
from sodlcompiler.ast import SystemBlock

def find_all_systems(ast: Program) -> list[SystemBlock]:
    return [stmt for stmt in ast.statements if isinstance(stmt, SystemBlock)]

# Usage
systems = find_all_systems(compiler.get_ast())
for system in systems:
    print(f"System: {system.name.value}")
```

### Finding All Modules

```python
from sodlcompiler.ast import ModuleBlock

def find_all_modules(ast: Program) -> list[ModuleBlock]:
    return [stmt for stmt in ast.statements if isinstance(stmt, ModuleBlock)]

# Usage
modules = find_all_modules(compiler.get_ast())
for module in modules:
    print(f"Module: {module.name.name}")
```

### Finding All Endpoints

```python
from sodlcompiler.ast import ModuleBlock, EndpointDefinition

def find_all_endpoints(ast: Program) -> list[tuple[str, EndpointDefinition]]:
    """Returns list of (module_name, endpoint) tuples"""
    endpoints = []
    for stmt in ast.statements:
        if isinstance(stmt, ModuleBlock) and stmt.api_block:
            for ep in stmt.api_block.endpoints:
                endpoints.append((stmt.name.name, ep))
    return endpoints

# Usage
for module_name, endpoint in find_all_endpoints(compiler.get_ast()):
    print(f"{module_name}: {endpoint.method} {endpoint.path}")
```

### Finding All Interfaces

```python
from sodlcompiler.ast import InterfaceBlock

def find_all_interfaces(ast: Program) -> list[InterfaceBlock]:
    return [stmt for stmt in ast.statements if isinstance(stmt, InterfaceBlock)]

# Usage
interfaces = find_all_interfaces(compiler.get_ast())
for iface in interfaces:
    print(f"Interface: {iface.name.name}")
    for method in iface.methods:
        print(f"  - {method.name.name}()")
```

### Finding Resources by Name

```python
from sodlcompiler.ast import SystemBlock, ModuleBlock, InterfaceBlock

def find_by_name(ast: Program, name: str):
    """Find any declaration by name"""
    for stmt in ast.statements:
        if isinstance(stmt, (SystemBlock, ModuleBlock, InterfaceBlock)):
            stmt_name = stmt.name.value if hasattr(stmt.name, 'value') else stmt.name.name
            if stmt_name == name:
                return stmt
    return None

# Usage
system = find_by_name(compiler.get_ast(), "MyApp")
if system:
    print(f"Found system: {system.name.value}")
```

### Recursive AST Traversal

For deep traversal of nested structures:

```python
from sodlcompiler.ast import ASTNode, ModuleBlock, APIBlock, EndpointDefinition

def traverse_ast(node: ASTNode, visitor):
    """Recursively traverse AST and call visitor on each node"""
    visitor(node)
    
    # Get all child attributes
    for attr_name in dir(node):
        if attr_name.startswith('_'):
            continue
        try:
            attr = getattr(node, attr_name)
            if isinstance(attr, ASTNode):
                traverse_ast(attr, visitor)
            elif isinstance(attr, list):
                for item in attr:
                    if isinstance(item, ASTNode):
                        traverse_ast(item, visitor)
        except Exception:
            pass

# Usage: Find all endpoints recursively
endpoints = []
def collect_endpoints(node):
    if isinstance(node, EndpointDefinition):
        endpoints.append(node)

traverse_ast(compiler.get_ast(), collect_endpoints)
```

### Extracting Specific Information

```python
from sodlcompiler.ast import SystemBlock, ModuleBlock

def extract_system_info(ast: Program) -> dict:
    """Extract comprehensive system information"""
    result = {
        'systems': [],
        'modules': [],
        'interfaces': [],
        'pipelines': []
    }
    
    for stmt in ast.statements:
        if isinstance(stmt, SystemBlock):
            system_info = {
                'name': stmt.name.value,
                'version': stmt.version.value if stmt.version else None,
                'stack': {},
                'intent': None,
                'outcomes': []
            }
            
            if stmt.stack_block:
                system_info['stack'] = stmt.stack_block.properties
            
            if stmt.intent_block:
                system_info['intent'] = stmt.intent_block.primary.value if stmt.intent_block.primary else None
                system_info['outcomes'] = [o.value for o in stmt.intent_block.outcomes]
            
            result['systems'].append(system_info)
            
        elif isinstance(stmt, ModuleBlock):
            module_info = {
                'name': stmt.name.name,
                'requires': [r.name for r in stmt.requires] if stmt.requires else [],
                'implements': [i.name for i in stmt.implements] if stmt.implements else [],
                'endpoints': []
            }
            
            if stmt.api_block and stmt.api_block.endpoints:
                module_info['endpoints'] = [
                    {'method': ep.method, 'path': ep.path}
                    for ep in stmt.api_block.endpoints
                ]
            
            result['modules'].append(module_info)
    
    return result

# Usage
info = extract_system_info(compiler.get_ast())
print(f"Systems: {[s['name'] for s in info['systems']]}")
print(f"Modules: {[m['name'] for m in info['modules']]}")
```

---

## Error Handling

### Error Reporter API

The `ErrorReporter` class provides detailed diagnostic information.

```python
from sodlcompiler.errors import ErrorReporter, ErrorLevel, Diagnostic

reporter = compiler.get_error_reporter()

# Check for errors
if reporter.has_errors():
    print("Compilation failed!")

# Get all errors
errors = reporter.get_errors()
for error in errors:
    print(f"[ERROR] {error.filename}:{error.line}:{error.column}: {error.message}")

# Get all warnings
warnings = reporter.get_warnings()
for warning in warnings:
    print(f"[WARNING] {warning.line}:{warning.column}: {warning.message}")

# Get all diagnostics
for diag in reporter.diagnostics:
    print(diag)  # Formatted output
```

### Diagnostic Object

Each `Diagnostic` contains:

**Properties:**
- `level` (ErrorLevel): ERROR, WARNING, or INFO
- `message` (str): Diagnostic message
- `line` (int): Line number (1-based)
- `column` (int): Column number (1-based)
- `filename` (str, optional): Source filename

**Methods:**
- `__str__()`: Formatted string representation

### Error Output Format

When compilation fails, errors are formatted as:

```
[ERROR] app.sodl:5:3: Unexpected token 'interface' at line 5, column 3
[ERROR] app.sodl:12:1: Expected indentation after 'module' statement
[WARNING] app.sodl:20:5: Unused interface 'IUserService'
```

### Capturing Errors Programmatically

```python
from sodlcompiler import SODLCompiler

def compile_and_report(source_code: str, filename: str) -> dict:
    """Compile and return structured error report"""
    compiler = SODLCompiler()
    success = compiler.compile(source_code, filename)
    
    reporter = compiler.get_error_reporter()
    
    return {
        'success': success,
        'errors': [
            {
                'line': e.line,
                'column': e.column,
                'message': e.message,
                'level': e.level.value
            }
            for e in reporter.get_errors()
        ],
        'warnings': [
            {
                'line': w.line,
                'column': w.column,
                'message': w.message,
                'level': w.level.value
            }
            for w in reporter.get_warnings()
        ]
    }

# Usage
result = compile_and_report(source_code, "app.sodl")
if not result['success']:
    for error in result['errors']:
        print(f"Line {error['line']}: {error['message']}")
```

### Intentional Error Testing

To test error handling, introduce syntax errors intentionally:

```python
# Valid SODL
valid_code = '''
system "TestApp":
  stack:
    language = "Python 3.12"
'''

# Introduce syntax error
invalid_code = '''
system "TestApp"
  stack:  # Missing colon after system name
    language = "Python 3.12"
'''

compiler = SODLCompiler()
if not compiler.compile(invalid_code, "test.sodl"):
    errors = compiler.get_error_reporter().get_errors()
    print(f"Found {len(errors)} error(s):")
    for error in errors:
        print(f"  Line {error.line}: {error.message}")
```

### Common Error Types

| Error Pattern | Example Message |
|--------------|-----------------|
| Missing colon | `Expected ':' after system name` |
| Wrong indentation | `Expected indentation of 2 spaces` |
| Unknown keyword | `Unexpected token 'func' - did you mean 'function'?` |
| Missing required block | `System must have at least one of: stack, intent` |
| Duplicate name | `Duplicate system name 'MyApp'` |
| Invalid type | `Invalid type annotation 'UnknownType'` |

---

## Examples

### Complete Compilation Example

```python
from sodlcompiler import SODLCompiler

source = '''
system "TodoApp":
  version = "1.0.0"
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    database = "PostgreSQL"

  intent:
    primary = "Task management application"
    outcomes = ["Create todos", "Update todos", "Delete todos"]

interface ITodoStore:
  method create(todo: TodoInput) -> Todo
  method get_all() -> List[Todo]
  method delete(id: str) -> Result[void, Error]

module TodoAPI:
  requires = [ITodoStore]
  implements = [ITodoStore]
  
  api:
    endpoint "GET /api/todos" -> List[TodoResponse]
    endpoint "POST /api/todos" -> TodoResponse
    endpoint "DELETE /api/todos/{id}" -> void

pipeline "Build":
  step Implement:
    modules = ["TodoAPI"]
    output = code
    gate = "Tests pass"
'''

compiler = SODLCompiler()
success = compiler.compile(source, "todo.sodl")

if success:
    ast = compiler.get_ast()
    print(f"✓ Compilation successful!")
    print(f"  Systems: {len([s for s in ast.statements if hasattr(s, 'stack_block')])}")
    print(f"  Interfaces: {len([i for i in ast.statements if hasattr(i, 'methods')])}")
    print(f"  Modules: {len([m for m in ast.statements if hasattr(m, 'api_block')])}")
else:
    print("✗ Compilation failed:")
    compiler.print_diagnostics()
```

### AST Analysis Tool

```python
from sodlcompiler import compile_source
from sodlcompiler.ast import *

def analyze_sodl(source_code: str) -> dict:
    """Analyze SODL source and return comprehensive report"""
    compiler = compile_source(source_code)
    
    if compiler.has_errors():
        return {'error': 'Compilation failed', 'diagnostics': compiler.get_error_reporter().diagnostics}
    
    ast = compiler.get_ast()
    
    analysis = {
        'systems': [],
        'interfaces': [],
        'modules': [],
        'pipelines': [],
        'policies': [],
        'templates': []
    }
    
    for stmt in ast.statements:
        if isinstance(stmt, SystemBlock):
            analysis['systems'].append({
                'name': stmt.name.value,
                'version': stmt.version.value if stmt.version else None,
                'has_stack': stmt.stack_block is not None,
                'has_intent': stmt.intent_block is not None
            })
        elif isinstance(stmt, InterfaceBlock):
            analysis['interfaces'].append({
                'name': stmt.name.name,
                'methods': len(stmt.methods) if stmt.methods else 0,
                'fields': len(stmt.fields) if stmt.fields else 0
            })
        elif isinstance(stmt, ModuleBlock):
            endpoint_count = 0
            if stmt.api_block and stmt.api_block.endpoints:
                endpoint_count = len(stmt.api_block.endpoints)
            
            analysis['modules'].append({
                'name': stmt.name.name,
                'requires': len(stmt.requires) if stmt.requires else 0,
                'implements': len(stmt.implements) if stmt.implements else 0,
                'endpoints': endpoint_count
            })
        elif isinstance(stmt, PipelineBlock):
            analysis['pipelines'].append({
                'name': stmt.name.value,
                'steps': len(stmt.steps)
            })
        elif isinstance(stmt, PolicyBlock):
            analysis['policies'].append({
                'name': stmt.name.name,
                'rules': len(stmt.rules)
            })
        elif isinstance(stmt, TemplateBlock):
            analysis['templates'].append({
                'name': stmt.name.value,
                'version': stmt.version.value if stmt.version else None
            })
    
    return analysis

# Usage
report = analyze_sodl(source_code)
for category, items in report.items():
    if items:
        print(f"{category.capitalize()}: {len(items)}")
        for item in items:
            print(f"  - {item.get('name', 'Unknown')}")
```

### Batch Compilation

```python
from pathlib import Path
from sodlcompiler import SODLCompiler

def compile_directory(dir_path: str) -> dict:
    """Compile all .sodl files in a directory"""
    compiler = SODLCompiler()
    results = {
        'success': [],
        'failed': []
    }
    
    sodl_files = list(Path(dir_path).glob('**/*.sodl'))
    
    for file_path in sodl_files:
        source = file_path.read_text()
        
        # Create new compiler instance for each file
        file_compiler = SODLCompiler()
        success = file_compiler.compile(source, str(file_path))
        
        if success:
            results['success'].append(str(file_path))
        else:
            results['failed'].append({
                'file': str(file_path),
                'errors': [
                    {'line': e.line, 'message': e.message}
                    for e in file_compiler.get_error_reporter().get_errors()
                ]
            })
    
    return results

# Usage
results = compile_directory('./examples')
print(f"Compiled {len(results['success'])} files successfully")
print(f"Failed {len(results['failed'])} files")
```

---

## Best Practices

1. **Always check for errors** before accessing the AST
2. **Use separate compiler instances** for independent compilations
3. **Cache compiled ASTs** when processing the same source multiple times
4. **Handle exceptions** around compilation for unexpected errors
5. **Use meaningful filenames** in error reporting for better diagnostics

```python
# Good practice example
def safe_compile(source_code: str, filename: str) -> Optional[Program]:
    try:
        compiler = SODLCompiler()
        if not compiler.compile(source_code, filename):
            print(f"Compilation errors in {filename}:")
            compiler.print_diagnostics()
            return None
        return compiler.get_ast()
    except Exception as e:
        print(f"Unexpected error compiling {filename}: {e}")
        return None
```
