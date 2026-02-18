# SODL Advanced Reference

This document contains advanced SODL features, detailed examples, and complex use cases not covered in the main skill instructions.

## Advanced SODL Concepts

### Complex Type Definitions

#### Union Types
```sodl
union Shape = Circle | Rectangle | Triangle

object Circle {
    radius: Float
    center: Point
}

object Rectangle {
    width: Float
    height: Float
    topLeft: Point
}

object Triangle {
    pointA: Point
    pointB: Point
    pointC: Point
}

object Point {
    x: Float
    y: Float
}
```

#### Nested Objects
```sodl
object Company {
    name: String
    address: Address
    departments: List<Department>
    employees: Map<String, Employee>
}

object Department {
    name: String
    manager: Employee
    members: List<Employee>
}

object Employee {
    id: String
    name: String
    position: String
    contact: ContactInfo
}

object ContactInfo {
    email: String
    phone: String
    emergencyContact: EmergencyContact?
}

object EmergencyContact {
    name: String
    relationship: String
    phone: String
}
```

### Advanced Enum Features
```sodl
enum HttpStatus {
    Continue = 100
    OK = 200
    Created = 201
    Accepted = 202
    BadRequest = 400
    Unauthorized = 401
    Forbidden = 403
    NotFound = 404
    InternalServerError = 500
}

// Enum with associated values
enum Result<T> {
    Success(value: T)
    Error(message: String, code: Int)
}
```

### Template and Macro Systems
```sodl
// Template definitions
template Entity<T> {
    id: String
    createdAt: DateTime
    updatedAt: DateTime
    data: T
}

// Using templates
object UserEntity = Entity<User>

object User {
    name: String
    email: String
    role: UserRole
}

enum UserRole {
    Admin
    Editor
    Viewer
}
```

## SODL Transformation Examples

### Converting SODL to JSON Schema
```python
def sodl_to_json_schema(sodl_ast):
    """Convert SODL AST to JSON Schema"""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
        "required": []
    }
    
    for obj_def in sodl_ast.get('objects', []):
        obj_name = obj_def['name']
        obj_props = {}
        required = []
        
        for prop in obj_def.get('properties', []):
            prop_name = prop['name']
            prop_type = prop['type']
            
            # Convert SODL type to JSON Schema type
            json_type = sodl_type_to_json(prop_type)
            obj_props[prop_name] = json_type
            
            # Required if not optional
            if not prop.get('optional', False):
                required.append(prop_name)
        
        schema['properties'][obj_name] = {
            "type": "object",
            "properties": obj_props,
            "required": required
        }
    
    return schema

def sodl_type_to_json(sodl_type):
    """Convert SODL type to JSON Schema type"""
    type_mapping = {
        'String': {'type': 'string'},
        'Int': {'type': 'integer'},
        'Float': {'type': 'number'},
        'Bool': {'type': 'boolean'},
        'DateTime': {'type': 'string', 'format': 'date-time'}
    }
    
    # Handle optional types
    if sodl_type.endswith('?'):
        base_type = sodl_type[:-1]
        return type_mapping.get(base_type, {'type': 'object'})
    
    return type_mapping.get(sodl_type, {'type': 'object'})
```

### Converting SODL to TypeScript Interfaces
```python
def sodl_to_typescript(sodl_ast):
    """Convert SODL AST to TypeScript interfaces"""
    ts_code = []
    
    # Generate enums
    for enum_def in sodl_ast.get('enums', []):
        ts_code.append(f"export enum {enum_def['name']} {{")
        for i, value in enumerate(enum_def['values']):
            if isinstance(value, dict):  # Named value with assignment
                ts_code.append(f"  {value['name']} = {value['value']}{',' if i < len(enum_def['values']) - 1 else ''}")
            else:  # Simple value
                ts_code.append(f"  {value} = '{value}'{',' if i < len(enum_def['values']) - 1 else ''}")
        ts_code.append("}\n")
    
    # Generate interfaces
    for obj_def in sodl_ast.get('objects', []):
        ts_code.append(f"export interface {obj_def['name']} {{")
        for prop in obj_def.get('properties', []):
            prop_name = prop['name']
            prop_type = sodl_type_to_ts(prop['type'])
            optional = '?' if prop.get('optional', False) else ''
            ts_code.append(f"  {prop_name}{optional}: {prop_type};")
        ts_code.append("}\n")
    
    return "\n".join(ts_code)

def sodl_type_to_ts(sodl_type):
    """Convert SODL type to TypeScript type"""
    type_mapping = {
        'String': 'string',
        'Int': 'number',
        'Float': 'number',
        'Bool': 'boolean',
        'DateTime': 'Date'
    }
    
    # Handle optional types
    if sodl_type.endswith('?'):
        base_type = sodl_type[:-1]
        ts_type = type_mapping.get(base_type, base_type)
        return ts_type
    
    # Handle collections
    if sodl_type.startswith('List<'):
        inner_type = sodl_type[5:-1]  # Remove 'List<>' wrapper
        return f'{sodl_type_to_ts(inner_type)}[]'
    elif sodl_type.startswith('Map<'):
        # Simplify Map to Record for TypeScript
        return 'Record<string, any>'
    
    return type_mapping.get(sodl_type, sodl_type)
```

## Advanced MCP Tools

### Extended Compilation Options
```python
# Note: These functions require running from the project root directory
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent  # Adjust path as needed
sys.path.insert(0, str(project_root))

from sodlcompiler.compiler import SODLCompiler

def compile_sodl_with_options(code, filename="<input>", options=None):
    """Compile SODL with extended options"""
    if options is None:
        options = {}
    
    compiler = SODLCompiler()
    success = compiler.compile(code, filename)
    
    result = {
        "success": success,
        "options_used": options
    }
    
    if success:
        # Process AST based on options
        if options.get('include_debug_info'):
            result['debug_info'] = compiler.debug_info if hasattr(compiler, 'debug_info') else {}
        
        if options.get('generate_docs'):
            result['documentation'] = generate_docs(compiler.ast) if compiler.ast else None
    
    return result

# Example usage:
# result = compile_sodl_with_options(
#     code=sodl_code,
#     filename="example.sodl",
#     options={
#         'include_debug_info': True,
#         'generate_docs': True
#     }
# )
```

### Batch Processing
```python
def batch_compile_sodl_files(file_paths):
    """Compile multiple SODL files"""
    results = {}
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            result = compile_sodl(code, file_path)
            results[file_path] = result
        except Exception as e:
            results[file_path] = {
                'success': False,
                'errors': [str(e)]
            }
    
    return results
```

## SODL Validation Rules

### Semantic Validation
```python
def validate_semantics(ast):
    """Perform semantic validation on SODL AST"""
    errors = []
    
    # Check for duplicate names
    names = set()
    for obj in ast.get('objects', []):
        if obj['name'] in names:
            errors.append(f"Duplicate object name: {obj['name']}")
        else:
            names.add(obj['name'])
    
    for enum in ast.get('enums', []):
        if enum['name'] in names:
            errors.append(f"Duplicate enum name: {enum['name']}")
        else:
            names.add(enum['name'])
    
    # Check for undefined types
    defined_types = names.union({'String', 'Int', 'Float', 'Bool', 'DateTime'})
    for obj in ast.get('objects', []):
        for prop in obj.get('properties', []):
            prop_type = prop['type'].rstrip('?')  # Remove optional marker
            if prop_type not in defined_types:
                errors.append(f"Undefined type '{prop_type}' in object '{obj['name']}'")
    
    return errors
```

### Cross-Reference Validation
```python
def validate_cross_references(ast):
    """Validate cross-references between objects"""
    errors = []
    
    # Create a mapping of all defined types
    type_definitions = {}
    
    for obj in ast.get('objects', []):
        type_definitions[obj['name']] = obj
        
    for enum in ast.get('enums', []):
        type_definitions[enum['name']] = enum
    
    # Validate all property types
    for obj in ast.get('objects', []):
        for prop in obj.get('properties', []):
            # Remove optional marker and collection wrappers for validation
            clean_type = prop['type'].rstrip('?')
            if clean_type.startswith('List<'):
                clean_type = clean_type[5:-1]
            elif clean_type.startswith('Map<'):
                clean_type = clean_type.split(',')[0][4:]
            
            if clean_type not in type_definitions and clean_type not in ['String', 'Int', 'Float', 'Bool', 'DateTime']:
                errors.append(f"In object '{obj['name']}': Undefined type '{clean_type}' for property '{prop['name']}'")
    
    return errors
```

## Performance Optimization

### Large SODL File Handling
```python
def stream_parse_sodl(file_path):
    """Stream parse large SODL files to manage memory usage"""
    import mmap
    
    with open(file_path, 'r', encoding='utf-8') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
            # Process the file in chunks
            chunk_size = 8192  # 8KB chunks
            pos = 0
            
            while pos < len(mmapped_file):
                chunk = mmapped_file[pos:pos+chunk_size]
                chunk_str = chunk.decode('utf-8', errors='ignore')
                
                # Process chunk for SODL constructs
                # This is a simplified example - real implementation would be more complex
                yield chunk_str
                pos += chunk_size
```

### Caching Compilation Results
```python
import hashlib
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_compile_sodl(code_hash, code):
    """Cache compilation results based on code hash"""
    return compile_sodl(code)

def compile_sodl_with_cache(code, filename=None):
    """Compile SODL with automatic caching"""
    code_hash = hashlib.sha256(code.encode()).hexdigest()
    return cached_compile_sodl(code_hash, code)
```

## Integration Examples

### SODL with Web APIs
```python
import json
from sodl_mcp import compile_sodl

def api_response_to_sodl_template(api_response):
    """Generate SODL template from API response"""
    def infer_type(value):
        if isinstance(value, str):
            return 'String'
        elif isinstance(value, int):
            return 'Int'
        elif isinstance(value, float):
            return 'Float'
        elif isinstance(value, bool):
            return 'Bool'
        elif isinstance(value, list):
            if value:
                inner_type = infer_type(value[0])
                return f'List<{inner_type}>'
            return 'List<any>'
        elif isinstance(value, dict):
            return 'Object'  # Would need recursive processing
        else:
            return 'any'
    
    # Parse the API response
    if isinstance(api_response, str):
        data = json.loads(api_response)
    else:
        data = api_response
    
    # Generate SODL object
    sodl_lines = ["object ApiResponse {"]
    for key, value in data.items():
        sodl_type = infer_type(value)
        sodl_lines.append(f"  {key}: {sodl_type}")
    sodl_lines.append("}")
    
    sodl_code = "\n".join(sodl_lines)
    
    # Validate the generated SODL
    result = compile_sodl(sodl_code)
    if result['success']:
        return sodl_code
    else:
        raise ValueError(f"Generated invalid SODL: {result['errors']}")
```

### SODL with Database Schemas
```python
def db_schema_to_sodl(schema_info):
    """Convert database schema to SODL objects"""
    sodl_objects = []
    
    for table_name, columns in schema_info.items():
        # Convert table name to PascalCase for SODL object
        object_name = "".join(word.capitalize() for word in table_name.split("_"))
        
        sodl_obj = [f"object {object_name} {{"]
        for col_name, col_info in columns.items():
            # Map DB types to SODL types
            sodl_type = map_db_type_to_sodl(col_info['type'], col_info.get('nullable', False))
            sodl_obj.append(f"  {col_name}: {sodl_type}")
        sodl_obj.append("}")
        
        sodl_objects.append("\n".join(sodl_obj))
    
    return "\n\n".join(sodl_objects)

def map_db_type_to_sodl(db_type, nullable):
    """Map database type to SODL type"""
    type_mapping = {
        'varchar': 'String',
        'text': 'String',
        'int': 'Int',
        'bigint': 'Int',
        'float': 'Float',
        'double': 'Float',
        'decimal': 'Float',
        'bool': 'Bool',
        'timestamp': 'DateTime',
        'datetime': 'DateTime',
        'date': 'DateTime',
    }
    
    sodl_type = type_mapping.get(db_type.lower(), 'String')
    if nullable:
        sodl_type += '?'
    
    return sodl_type
```

## Testing SODL Code

### Unit Testing Framework
```python
def test_sodl_validity():
    """Basic unit tests for SODL validity"""
    test_cases = [
        # Valid SODL
        {
            'name': 'Valid object definition',
            'code': 'object Test { id: Int }',
            'should_pass': True
        },
        {
            'name': 'Valid enum definition',
            'code': 'enum Status { Active, Inactive }',
            'should_pass': True
        },
        # Invalid SODL
        {
            'name': 'Missing closing brace',
            'code': 'object Test { id: Int ',
            'should_pass': False
        }
    ]
    
    for test_case in test_cases:
        result = validate_sodl_syntax(test_case['code'])
        success = result['valid'] == test_case['should_pass']
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_case['name']}")
        
        if not success:
            print(f"  Expected: {'valid' if test_case['should_pass'] else 'invalid'}")
            print(f"  Got: {'valid' if result['valid'] else 'invalid'}")
```

## Troubleshooting Common Issues

### Circular Dependencies
```sodl
// Problem: Circular dependency
object User {
    id: Int
    posts: List<Post>  // References Post
}

object Post {
    id: Int
    author: User       // References User - circular!
}
```

Solution: Use forward declarations or interfaces:
```sodl
// Solution 1: Forward declaration concept (if supported)
object User {
    id: Int
    posts: List<Post>
}

object Post {
    id: Int
    author: User
}
```

### Complex Nested Structures
```sodl
object Company {
    departments: List<Department>
}

object Department {
    employees: List<Employee>
}

object Employee {
    manager: Employee?  // Self-reference
}
```

## Advanced Scripting Examples

### Script: sodl_transform.py
```python
#!/usr/bin/env python3
"""
Transform SODL to various output formats
"""
import sys
import json
from sodl_mcp import compile_sodl

def transform_to_format(sodl_code, target_format):
    """Transform SODL to target format"""
    result = compile_sodl(sodl_code)
    
    if not result['success']:
        return None, result['errors']
    
    ast = result['ast']
    
    if target_format.lower() == 'json':
        return json.dumps(ast, indent=2), None
    elif target_format.lower() == 'typescript':
        from .transformers import sodl_to_typescript
        return sodl_to_typescript(ast), None
    elif target_format.lower() == 'jsonschema':
        from .transformers import sodl_to_json_schema
        return json.dumps(sodl_to_json_schema(ast), indent=2), None
    else:
        return None, [f"Unsupported target format: {target_format}"]

def main():
    if len(sys.argv) != 3:
        print("Usage: python sodl_transform.py <sodl_file> <format>")
        print("Formats: json, typescript, jsonschema")
        sys.exit(1)
        
    filename = sys.argv[1]
    target_format = sys.argv[2]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
            
        output, errors = transform_to_format(code, target_format)
        
        if errors:
            print("❌ Transformation failed:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print(output)
                
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## License Information

- **SODL Compiler**: [Appropriate license]
- **MCP Tools**: [Appropriate license]
- **Transformation Utilities**: [Appropriate license]