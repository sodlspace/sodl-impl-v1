# SODL Syntax Reference

Quick reference guide for SODL v0.3 syntax patterns.

## Basic Structure

### System Declaration

```sodl
system "SystemName":
  version = "1.0.0"
  # System content
```

### Template Declaration

```sodl
template "TemplateName":
  # Template content
```

### Inheritance

```sodl
system "ChildSystem" extends "ParentTemplate":
  # System content
```

## Stack Definition

```sodl
stack:
  language = "Python 3.12"
  web = "FastAPI"
  database = "PostgreSQL"
  key = "value"
```

## Intent Definition

```sodl
intent:
  primary = "Main goal description"
  outcomes = [
    "Outcome 1",
    "Outcome 2"
  ]
  out_of_scope = [
    "Not included feature 1",
    "Not included feature 2"
  ]
```

## Interface Syntax

### Basic Interface

```sodl
interface InterfaceName:
  doc = "Interface description"
  method method_name(param: Type) -> ReturnType
  invariants:
    invariant "Constraint description"
```

### Interface with Multiple Methods

```sodl
interface StorageInterface:
  doc = "Storage operations"
  method create(data: Input) -> Output
  method read(id: UUID) -> Optional[Output]
  method update(id: UUID, data: Update) -> Output
  method delete(id: UUID) -> bool
  invariants:
    invariant "IDs are unique"
    invariant "Operations are atomic"
```

### Interface Inheritance

```sodl
interface ChildInterface extends ParentInterface:
  override method parent_method(param: Type) -> NewReturnType
  method new_method(param: Type) -> ReturnType
```

## Module Syntax

### Full Module Structure

```sodl
module ModuleName:
  owns = ["Responsibility 1", "Responsibility 2"]
  requires = [Interface1, Interface2]
  implements = [Interface3]
  exports = [Interface3]
  api:
    # API definitions
  invariants:
    invariant "Constraint 1"
    invariant "Constraint 2"
  acceptance:
    test "Test description 1"
    test "Test description 2"
  artifacts = ["file1.py", "file2.py"]
  config:
    key = value
```

### Module with Endpoints

```sodl
module APIModule:
  api:
    endpoint "GET /path" -> ResponseType
    endpoint "POST /path" -> ResponseType (201 CREATED)
    endpoint "PUT /path/{id}" -> ResponseType
    endpoint "DELETE /path/{id}" -> Empty (204 NO CONTENT)
```

### Module with Models

```sodl
module ModelsModule:
  api:
    model ModelName:
      field field1: Type
      field field2: Optional[Type]
      field field3: Type (constraint)
```

## Policy Syntax

```sodl
policy PolicyName:
  rule "Rule description" severity=critical
  rule "Rule description" severity=high
  rule "Rule description" severity=medium
  rule "Rule description" severity=low
```

### Multiple Policies

```sodl
policy Security:
  rule "Security rule 1" severity=critical
  rule "Security rule 2" severity=high

policy Performance:
  rule "Performance rule 1" severity=medium
```

## Pipeline Syntax

### Basic Pipeline

```sodl
pipeline "PipelineName":
  step StepName:
    output = output_type
    require = "Requirement description"
```

### Full Pipeline with Gates

```sodl
pipeline "Development":
  step Design:
    output = design
    require = "Create architecture"
    
  step Implement:
    modules = ["Module1", "Module2"]
    output = code
    require = "Follow guidelines"
    gate = "Tests pass"
    
  step Review:
    output = diff
    require = "Review checklist"
    gate = "Approval received"
```

## Override Operations

### Replace Value

```sodl
override path.to.value = "new value"
```

### Append to List

```sodl
append path.to.list += "new item"
```

### Remove from List

```sodl
remove path.to.list -= "item to remove"
```

### Replace Block

```sodl
replace block BlockName:
  # New block content
```

## Data Types

### Primitive Types

- `str`: String
- `int`: Integer
- `float`: Floating point
- `bool`: Boolean
- `bytes`: Byte array

### Generic Types

- `List[Type]`: List of Type
- `Optional[Type]`: Type or None
- `Dict[KeyType, ValueType]`: Dictionary
- `UUID`: Universally Unique Identifier
- `datetime`: Date and time

### Type Constraints

```sodl
field priority: int (1-3)
field priority: int (ge=1, le=3)
field email: str (format="email")
```

## Common Patterns

### CRUD Interface

```sodl
interface CRUDRepository:
  method create(input: Input) -> Entity
  method read(id: UUID) -> Optional[Entity]
  method update(id: UUID, updates: Update) -> Entity
  method delete(id: UUID) -> bool
  method list(filters: Filters) -> List[Entity]
```

### REST API Module

```sodl
module RESTAPIModule:
  requires = [Repository]
  api:
    endpoint "GET /api/resources" -> List[Response]
    endpoint "GET /api/resources/{id}" -> Response
    endpoint "POST /api/resources" -> Response (201 CREATED)
    endpoint "PUT /api/resources/{id}" -> Response
    endpoint "DELETE /api/resources/{id}" -> Empty (204 NO CONTENT)
  invariants:
    invariant "RESTful conventions followed"
    invariant "JSON schema validated"
```

### Storage Module

```sodl
module StorageModule:
  implements = [StorageInterface]
  exports = [StorageInterface]
  config:
    storage_path = "./data"
    max_size = 1000
  invariants:
    invariant "Thread-safe operations"
    invariant "Data consistency maintained"
```

### UI Module

```sodl
module UIModule:
  requires = [DataService]
  api:
    endpoint "GET /page" -> HTML
    endpoint "POST /action" -> Redirect
  invariants:
    invariant "Client and server validation"
    invariant "Responsive design"
  artifacts = ["templates/*.html", "static/css/*.css", "static/js/*.js"]
```

## Severity Levels

| Level | Usage | Enforcement |
|-------|-------|-------------|
| `critical` | Must not violate | Hard constraint |
| `high` | Must follow | Required |
| `medium` | Should follow | Recommended |
| `low` | May follow | Suggested |

## Output Types

| Type | Purpose |
|------|---------|
| `design` | Architecture, diagrams, data models |
| `code` | Application source code |
| `tests` | Test code and test suites |
| `diff` | Code changes for review |
| `docs` | Documentation files |

## Complete Minimal Example

```sodl
system "MinimalApp":
  stack:
    language = "Python 3.12"
    web = "Flask"
  intent:
    primary = "Simple web application"
  
  interface DataStore:
    method save(data: str) -> str
    method load(id: str) -> str
  
  module API:
    requires = [DataStore]
    api:
      endpoint "POST /save" -> str
      endpoint "GET /load/{id}" -> str
  
  module Storage:
    implements = [DataStore]
    exports = [DataStore]
  
  pipeline "Build":
    step Implement:
      modules = ["Storage", "API"]
      output = code
      gate = "Tests pass"
```

## Comments

SODL uses `#` for comments:

```sodl
# This is a comment
system "App":  # Inline comment
  # Block comment
  stack:
    language = "Python"  # Language choice
```

## Indentation Rules

- Use 2 or 4 spaces for indentation (be consistent)
- Use colon (`:`) to start indented blocks
- Do not mix tabs and spaces
- Nested blocks increase indentation level

```sodl
system "App":
  intent:
    primary = "Example"
    outcomes = [
      "Outcome 1"
    ]
```

## String Values

### Single-line Strings

```sodl
value = "String content"
```

### Multi-line Strings (in lists)

```sodl
outcomes = [
  "First line",
  "Second line"
]
```

## Lists

```sodl
list_field = ["item1", "item2", "item3"]

# Multi-line list
list_field = [
  "item1",
  "item2",
  "item3"
]
```

## Field Assignment

```sodl
scalar_field = "value"
number_field = 42
boolean_field = true
```

## Naming Conventions

- **Systems**: PascalCase - `"MySystem"`
- **Templates**: PascalCase - `"BaseTemplate"`
- **Interfaces**: PascalCase - `InterfaceName`
- **Modules**: PascalCase - `ModuleName`
- **Policies**: PascalCase - `PolicyName`
- **Pipelines**: String - `"PipelineName"`
- **Steps**: PascalCase - `StepName`
- **Methods**: snake_case - `method_name`
- **Fields**: snake_case - `field_name`
- **Endpoints**: HTTP path - `"GET /api/path"`

## Reserved Keywords

- `system`
- `template`
- `extends`
- `interface`
- `module`
- `policy`
- `pipeline`
- `step`
- `stack`
- `intent`
- `api`
- `method`
- `model`
- `field`
- `endpoint`
- `owns`
- `requires`
- `implements`
- `exports`
- `invariants`
- `invariant`
- `acceptance`
- `test`
- `artifacts`
- `config`
- `rule`
- `severity`
- `output`
- `require`
- `gate`
- `override`
- `append`
- `remove`
- `replace`
- `doc`
- `primary`
- `outcomes`
- `out_of_scope`
- `version`

## Error Patterns to Avoid

### ❌ Missing Colon

```sodl
system "App"  # Missing colon
  intent:
```

### ✅ Correct

```sodl
system "App":
  intent:
```

### ❌ Inconsistent Indentation

```sodl
system "App":
  intent:
      primary = "Goal"  # Too much indentation
```

### ✅ Correct

```sodl
system "App":
  intent:
    primary = "Goal"
```

### ❌ Missing Quotes

```sodl
system MyApp:  # Missing quotes around system name
```

### ✅ Correct

```sodl
system "MyApp":
```

### ❌ Invalid Type Syntax

```sodl
method get(id: string) -> object  # Use str, not string
```

### ✅ Correct

```sodl
method get(id: str) -> dict
```

## Quick Lookup

### Need to define a system?
```sodl
system "Name":
  stack:
    language = "Python 3.12"
  intent:
    primary = "Description"
```

### Need to define an interface?
```sodl
interface Name:
  method operation(param: Type) -> ReturnType
```

### Need to define a module?
```sodl
module Name:
  requires = [Interface]
  api:
    endpoint "GET /path" -> ResponseType
```

### Need to define a pipeline?
```sodl
pipeline "Name":
  step StepName:
    modules = ["Module"]
    output = code
    gate = "Tests pass"
```

### Need to add a policy?
```sodl
policy Name:
  rule "Description" severity=level
```

---

For complete examples and detailed explanations, see `SODL_DOCUMENTATION.md`.
