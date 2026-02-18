# SODL API Reference v0.3

Complete reference for all SODL constructs, fields, and types.

## Table of Contents

1. [Top-Level Constructs](#top-level-constructs)
2. [System](#system)
3. [Template](#template)
4. [Interface](#interface)
5. [Module](#module)
6. [Policy](#policy)
7. [Pipeline](#pipeline)
8. [Step](#step)
9. [Data Types](#data-types)
10. [Operations](#operations)

---

## Top-Level Constructs

### system

Defines a concrete system to be generated.

**Syntax:**
```sodl
system "SystemName":
  [system_body]
```

**Fields:**
- `version`: (optional) String version identifier
- `stack`: (required) Technology stack definition
- `intent`: (required) System goals and scope
- `policy`: (optional) Multiple named policies
- `interface`: (optional) Multiple interface definitions
- `module`: (optional) Multiple module definitions
- `pipeline`: (optional) Multiple pipeline definitions

**Example:**
```sodl
system "MyApp":
  version = "1.0.0"
  stack:
    language = "Python 3.12"
  intent:
    primary = "Build application"
```

**Inheritance:**
```sodl
system "ChildApp" extends "ParentTemplate":
  intent:
    primary = "Extended application"
```

---

### template

Defines a reusable base specification.

**Syntax:**
```sodl
template "TemplateName":
  [template_body]
```

**Fields:**
Same as `system` except templates are not directly executable.

**Example:**
```sodl
template "BaseWebApp":
  stack:
    language = "Python 3.12"
    web = "Flask"
  policy Security:
    rule "No secrets in repo" severity=critical
```

---

### interface

Defines a functionality contract without implementation.

**Syntax:**
```sodl
interface InterfaceName:
  [doc = "Description"]
  [method declarations]
  [invariants block]
```

**Fields:**
- `doc`: (optional) String description of interface purpose
- `method`: (one or more) Method declarations
- `invariants`: (optional) Block containing invariant declarations

**Method Syntax:**
```sodl
method method_name(param1: Type1, param2: Type2) -> ReturnType
```

**Invariants Syntax:**
```sodl
invariants:
  invariant "Constraint description"
  invariant "Another constraint"
```

**Interface Inheritance:**
```sodl
interface ChildInterface extends ParentInterface:
  override method parent_method(param: Type) -> NewReturnType
  method new_method(param: Type) -> ReturnType
```

**Example:**
```sodl
interface UserRepository:
  doc = "User data access layer"
  method create(user: UserInput) -> User
  method get_by_id(id: UUID) -> Optional[User]
  method update(id: UUID, updates: dict) -> User
  method delete(id: UUID) -> bool
  invariants:
    invariant "Email addresses are unique"
    invariant "Passwords are hashed"
```

---

### module

Defines a unit of responsibility and generation.

**Syntax:**
```sodl
module ModuleName:
  [module_sections]
```

**Sections:**

#### owns
List of string descriptions of module responsibilities.

```sodl
owns = ["Responsibility 1", "Responsibility 2"]
```

#### requires
List of interface names this module depends on.

```sodl
requires = [Interface1, Interface2]
```

#### implements
List of interface names this module implements.

```sodl
implements = [Interface1]
```

#### exports
List of interface names this module provides to others.

```sodl
exports = [Interface1]
```

#### api
API definition block containing endpoints and/or models.

**Endpoints:**
```sodl
api:
  endpoint "METHOD /path" -> ResponseType
  endpoint "METHOD /path/{param}" -> ResponseType (STATUS CODE)
```

**Models:**
```sodl
api:
  model ModelName:
    field field_name: Type
    field optional_field: Optional[Type]
    field constrained_field: Type (constraint)
```

#### invariants
Constraints that must hold for this module.

```sodl
invariants:
  invariant "Constraint description"
  invariant "Another constraint"
```

#### acceptance
Definition of Done - tests that must pass.

```sodl
acceptance:
  test "Test description"
  test "Another test"
```

#### artifacts
List of file paths this module may modify.

```sodl
artifacts = ["path/to/file.py", "path/to/*.html"]
```

#### config
Configuration key-value pairs.

```sodl
config:
  key = value
  timeout = 30
  enabled = true
```

**Complete Example:**
```sodl
module UserAPI:
  owns = ["User management endpoints"]
  requires = [UserRepository]
  api:
    endpoint "GET /api/users" -> List[UserResponse]
    endpoint "POST /api/users" -> UserResponse (201 CREATED)
    endpoint "GET /api/users/{id}" -> UserResponse
    endpoint "PUT /api/users/{id}" -> UserResponse
    endpoint "DELETE /api/users/{id}" -> Empty (204 NO CONTENT)
  invariants:
    invariant "Validate all inputs"
    invariant "Return consistent error format"
  acceptance:
    test "creates user successfully"
    test "returns 404 for missing user"
    test "validates email format"
  artifacts = ["app/api/users.py"]
  config:
    max_page_size = 100
```

---

### policy

Defines rules and constraints with severity levels.

**Syntax:**
```sodl
policy PolicyName:
  rule "Rule description" severity=level
  [more rules]
```

**Severity Levels:**
- `critical`: MUST NOT violate (hard constraint)
- `high`: MUST follow (required)
- `medium`: SHOULD follow (recommended)
- `low`: MAY follow (suggested)

**Example:**
```sodl
policy Security:
  rule "No secrets in repository" severity=critical
  rule "Validate all user input" severity=high
  rule "Use HTTPS for APIs" severity=high
  rule "Log security events" severity=medium
  rule "Use security headers" severity=low

policy Performance:
  rule "Cache responses for 5 minutes" severity=medium
  rule "Use database indexes" severity=high
  rule "Implement pagination" severity=high
```

---

### pipeline

Defines the controlled generation process.

**Syntax:**
```sodl
pipeline "PipelineName":
  step StepName:
    [step_definition]
  [more steps]
```

**Example:**
```sodl
pipeline "Development":
  step Design:
    output = design
    require = "Create architecture diagram"
    
  step Implement:
    modules = ["Module1", "Module2"]
    output = code
    gate = "All tests pass"
    
  step Review:
    output = diff
    require = "Code review checklist"
```

---

### step

Defines an atomic generation phase within a pipeline.

**Syntax:**
```sodl
step StepName:
  [modules = [list]]
  output = output_type
  [require = "requirement"]
  [gate = "exit criteria"]
```

**Alternative Syntax:**
```sodl
step StepType "StepName":
  [step_fields]
```

**Fields:**

#### modules
List of module names to generate in this step.

```sodl
modules = ["ModuleA", "ModuleB"]
```

#### output
Type of output to produce.

**Allowed values:**
- `design`: Architecture diagrams, data models
- `code`: Application source code
- `tests`: Test code
- `diff`: Code changes/review
- `docs`: Documentation

```sodl
output = code
```

#### require
Additional requirements or instructions for this step.

```sodl
require = "Follow style guide PEP-8"
```

#### gate
Exit criteria that must be met before proceeding.

```sodl
gate = "All unit tests pass with 80% coverage"
```

**Examples:**
```sodl
step Design:
  output = design
  require = "Create entity-relationship diagram"

step Implement "Backend":
  modules = ["DatabaseModule", "APIModule"]
  output = code
  require = "Use async/await for I/O operations"
  gate = "Integration tests pass"

step Review:
  output = diff
  require = "Security checklist completed"
  gate = "Two approvals received"
```

---

## Section Details

### stack

Defines the technology stack.

**Syntax:**
```sodl
stack:
  key = "value"
  another_key = "value"
```

**Common Keys:**
- `language`: Programming language and version
- `web`: Web framework
- `database`: Database system
- `orm`: Object-Relational Mapper
- `cache`: Caching system
- `messaging`: Message queue system
- `testing`: List of testing tools
- `frontend`: Frontend framework
- `templating`: Template engine

**Example:**
```sodl
stack:
  language = "Python 3.12"
  web = "FastAPI"
  database = "PostgreSQL"
  orm = "SQLAlchemy"
  cache = "Redis"
  messaging = "RabbitMQ"
  testing = ["pytest", "pytest-asyncio", "pytest-cov"]
  frontend = "React"
```

---

### intent

Defines system goals and scope.

**Syntax:**
```sodl
intent:
  primary = "Main goal"
  [outcomes = [list]]
  [out_of_scope = [list]]
```

**Fields:**

#### primary
Main goal or purpose of the system (required).

```sodl
primary = "Build a task management application"
```

#### outcomes
List of expected outcomes or features (optional).

```sodl
outcomes = [
  "Users can create tasks",
  "Tasks have due dates",
  "Email notifications for deadlines"
]
```

#### out_of_scope
List of explicitly excluded features (optional).

```sodl
out_of_scope = [
  "User authentication",
  "Mobile app",
  "Real-time collaboration"
]
```

**Example:**
```sodl
intent:
  primary = "E-commerce product catalog"
  outcomes = [
    "Browse products by category",
    "Search products by keyword",
    "Filter by price and rating",
    "View product details with images"
  ]
  out_of_scope = [
    "Shopping cart",
    "Checkout process",
    "Payment processing"
  ]
```

---

## Data Types

### Primitive Types

| Type | Description | Example |
|------|-------------|---------|
| `str` | String | `"Hello"` |
| `int` | Integer | `42` |
| `float` | Floating point | `3.14` |
| `bool` | Boolean | `true`, `false` |
| `bytes` | Byte array | `b"data"` |

### Generic Types

| Type | Description | Example |
|------|-------------|---------|
| `List[T]` | List of type T | `List[str]`, `List[User]` |
| `Optional[T]` | T or None | `Optional[str]` |
| `Dict[K, V]` | Dictionary | `Dict[str, int]` |
| `Tuple[T1, T2]` | Tuple | `Tuple[str, int]` |
| `Set[T]` | Set | `Set[str]` |

### Special Types

| Type | Description |
|------|-------------|
| `UUID` | Universally Unique Identifier |
| `datetime` | Date and time |
| `date` | Date only |
| `time` | Time only |
| `Decimal` | Decimal number for financial calculations |
| `JSON` | JSON data |
| `HTML` | HTML content |
| `URL` | URL string |

### Custom Types

You can reference custom types defined in models:

```sodl
api:
  model User:
    field id: UUID
    field name: str

method get_user(id: UUID) -> User
```

### Type Constraints

Add constraints to types using parentheses:

```sodl
field age: int (ge=0, le=120)
field priority: int (1-3)
field email: str (format="email")
field password: str (min_length=8)
field score: float (ge=0.0, le=100.0)
```

**Common Constraints:**
- `ge`: Greater than or equal
- `le`: Less than or equal
- `gt`: Greater than
- `lt`: Less than
- `min_length`: Minimum string length
- `max_length`: Maximum string length
- `regex`: Regex pattern
- `format`: Format type (email, url, etc.)

---

## Operations

### override

Replace a scalar value or entire block.

**Syntax:**
```sodl
override path.to.field = new_value
```

**Examples:**
```sodl
system "App" extends "BaseTemplate":
  override stack.language = "Python 3.13"
  override stack.web = "Django"
```

---

### append

Append items to a list.

**Syntax:**
```sodl
append path.to.list += value
append path.to.list += "value"
```

**Examples:**
```sodl
system "App" extends "BaseTemplate":
  append stack.testing += "pytest-cov"
  append stack.testing += "pytest-asyncio"
```

---

### remove

Remove items from a list.

**Syntax:**
```sodl
remove path.to.list -= value
remove path.to.list -= "value"
```

**Examples:**
```sodl
system "App" extends "BaseTemplate":
  remove stack.testing -= "pytest-mock"
```

---

### replace

Replace an entire named block.

**Syntax:**
```sodl
replace block BlockName:
  [new_block_content]
```

**Example:**
```sodl
system "App" extends "BaseTemplate":
  replace block Security:
    rule "New security rule" severity=critical
```

---

## Endpoint Syntax

### Basic Endpoint

```sodl
endpoint "METHOD /path" -> ResponseType
```

### Endpoint with Path Parameters

```sodl
endpoint "GET /users/{id}" -> UserResponse
endpoint "DELETE /posts/{post_id}/comments/{comment_id}" -> Empty
```

### Endpoint with Status Code

```sodl
endpoint "POST /users" -> UserResponse (201 CREATED)
endpoint "DELETE /users/{id}" -> Empty (204 NO CONTENT)
```

### HTTP Methods

- `GET`: Retrieve resource(s)
- `POST`: Create new resource
- `PUT`: Update entire resource
- `PATCH`: Partially update resource
- `DELETE`: Delete resource
- `HEAD`: Headers only
- `OPTIONS`: Allowed methods
- `ANY`: Match any method (for proxies/gateways)

### Response Types

#### Standard Response
```sodl
endpoint "GET /users" -> UserResponse
endpoint "POST /users" -> UserResponse
```

#### List Response
```sodl
endpoint "GET /users" -> List[UserResponse]
```

#### Empty Response
```sodl
endpoint "DELETE /users/{id}" -> Empty
endpoint "DELETE /users/{id}" -> Empty (204 NO CONTENT)
```

#### HTML Response
```sodl
endpoint "GET /" -> HTML
endpoint "GET /page" -> HTML (via Jinja2)
```

#### Special Responses
```sodl
endpoint "POST /login" -> Redirect to "/"
endpoint "ANY /*" -> ProxiedResponse
endpoint "GET /stream" -> SSE
```

---

## Model Syntax

### Basic Model

```sodl
model ModelName:
  field field_name: Type
```

### Model with Optional Fields

```sodl
model User:
  field id: UUID
  field name: str
  field email: Optional[str]
  field bio: Optional[str]
```

### Model with Constraints

```sodl
model TodoItem:
  field id: UUID
  field title: str (min_length=1, max_length=200)
  field priority: int (ge=1, le=3)
  field completed: bool
  field due_date: Optional[datetime]
```

### Nested Models

```sodl
model Address:
  field street: str
  field city: str
  field country: str

model User:
  field id: UUID
  field name: str
  field address: Address
```

---

## Invariant Syntax

Invariants are string descriptions of constraints that must hold.

**Syntax:**
```sodl
invariants:
  invariant "Constraint description"
  invariant "Another constraint"
```

**Examples:**
```sodl
invariants:
  invariant "All IDs are UUIDs"
  invariant "Email addresses are unique"
  invariant "Passwords are hashed with bcrypt"
  invariant "Timestamps use UTC"
  invariant "Operations are atomic"
  invariant "Thread-safe access"
```

---

## Acceptance Test Syntax

Acceptance tests define the "Definition of Done" for modules.

**Syntax:**
```sodl
acceptance:
  test "Test description"
  test "Another test description"
```

**Examples:**
```sodl
acceptance:
  test "creates user with valid data"
  test "rejects duplicate email"
  test "returns 404 for missing user"
  test "validates email format"
  test "hashes password before storing"
  test "handles concurrent updates safely"
```

**Best Practices:**
- Write tests as outcome descriptions, not implementation details
- Include both positive and negative test cases
- Cover edge cases and error scenarios
- Ensure tests are independently verifiable

---

## Artifact Syntax

Artifacts define which files a module is allowed to modify.

**Syntax:**
```sodl
artifacts = ["path/to/file.py"]
artifacts = ["path/*.py", "templates/*.html"]
```

**Glob Patterns:**
- `*`: Match any characters in a filename
- `**`: Match any directories recursively
- `?`: Match single character

**Examples:**
```sodl
artifacts = ["app/main.py"]
artifacts = ["app/api.py", "app/models.py"]
artifacts = ["app/routes/*.py"]
artifacts = ["templates/**/*.html"]
artifacts = ["app/**/*.py", "tests/**/*.py"]
```

---

## Config Syntax

Configuration key-value pairs for module settings.

**Syntax:**
```sodl
config:
  key = value
  number = 42
  boolean = true
  string = "value"
```

**Examples:**
```sodl
config:
  persistence = "in-memory (ephemeral)"
  max_connections = 100
  timeout_seconds = 30
  enabled = true
  base_url = "https://api.example.com"
  retry_attempts = 3
  log_level = "INFO"
```

---

## Special Constructs

### WebSocket Endpoint

```sodl
api:
  websocket "/ws/channel" -> None
  websocket "/ws/room/{room_id}" -> None
```

### Server-Sent Events (SSE)

```sodl
api:
  endpoint "GET /stream/events" -> SSE
```

### Command (CLI)

```sodl
api:
  command "init" -> None
  command "migrate [options]" -> None
  command "generate <name>" -> None
```

---

## Comments

Use `#` for single-line comments:

```sodl
# This is a comment
system "App":  # Inline comment
  # Another comment
  stack:
    language = "Python"  # Language choice
```

**Multi-line comments:**
```sodl
# This is a longer comment
# that spans multiple lines
# to explain something complex
```

---

## Reserved Words

The following are reserved keywords and cannot be used as identifiers:

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
- `websocket`
- `command`
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
- `modules`

---

## Compiler Output Structure

The SODL compiler generates the following structure:

```
.sodl/
├── global.md              # System-level context
├── modules/
│   ├── Module1.md        # Module-specific instructions
│   ├── Module2.md
│   └── ...
├── steps/
│   ├── Step1__Module1.md # Step-by-step instructions
│   └── ...
└── manifest.json         # Metadata and compilation info
```

### global.md

Contains:
- System intent and goals
- Technology stack
- Global policies
- Interface definitions
- Overall architecture

### modules/ModuleName.md

Contains:
- Module responsibilities
- Required interfaces
- API definitions
- Invariants and constraints
- Acceptance criteria
- File artifacts

### steps/StepName__ModuleName.md

Contains:
- Step-specific instructions
- Module to generate
- Output type
- Requirements
- Exit criteria (gates)

### manifest.json

Contains:
- Compilation metadata
- File structure
- Module dependencies
- Step order
- Validation results

---

## Validation Rules

### System Level

- ✅ Must have `stack` section
- ✅ Must have `intent` section with `primary` field
- ✅ Must have at least one `pipeline`
- ⚠️ Should have at least one `module`

### Interface Level

- ✅ Must have at least one `method`
- ✅ Method parameters must have types
- ✅ Method must have return type
- ⚠️ Should have `doc` field

### Module Level

- ✅ Must have at least one section (`owns`, `requires`, etc.)
- ✅ `requires` must reference defined interfaces
- ✅ `implements` must reference defined interfaces
- ✅ If `implements` an interface, must define all its methods
- ⚠️ Should have `artifacts` section
- ⚠️ Should have `acceptance` section

### Pipeline Level

- ✅ Must have at least one `step`
- ✅ Each step must have `output` field
- ✅ Step `modules` must reference defined modules

### Policy Level

- ✅ Must have at least one `rule`
- ✅ Each rule must have `severity`
- ✅ Severity must be one of: `critical`, `high`, `medium`, `low`

---

## Error Messages

Common compilation errors:

### Syntax Errors

- `Missing colon after system declaration`
- `Inconsistent indentation at line X`
- `Unexpected token: expected '=' but found ':'`

### Semantic Errors

- `Module 'X' requires undefined interface 'Y'`
- `Interface 'X' not found`
- `Module 'X' claims to implement 'Y' but missing method 'Z'`
- `Circular dependency: A requires B, B requires A`
- `Step references undefined module 'X'`

### Validation Errors

- `System missing required 'intent' section`
- `Interface must have at least one method`
- `Invalid severity level: must be critical, high, medium, or low`

---

## Best Practices

### Naming Conventions

- **Systems**: PascalCase in quotes - `system "MySystem"`
- **Templates**: PascalCase in quotes - `template "BaseTemplate"`
- **Interfaces**: PascalCase - `interface UserRepository`
- **Modules**: PascalCase - `module UserAPI`
- **Policies**: PascalCase - `policy Security`
- **Pipelines**: String in quotes - `pipeline "Development"`
- **Steps**: PascalCase - `step Implement`
- **Methods**: snake_case - `method get_user`
- **Fields**: snake_case - `field user_name`
- **Config keys**: snake_case - `timeout_seconds = 30`

### File Organization

```sodl
# Order sections consistently:
system "Name":
  version = "x.y.z"
  
  stack:
    # ...
  
  intent:
    # ...
  
  policy PolicyName:
    # ...
  
  interface InterfaceName:
    # ...
  
  module ModuleName:
    # ...
  
  pipeline "PipelineName":
    # ...
```

### Documentation

- Always provide `doc` for interfaces
- Use descriptive names for modules
- Write clear invariants and acceptance tests
- Document `out_of_scope` to set clear boundaries

---

For complete examples, see `EXAMPLES_COLLECTION.md`.
For syntax quick reference, see `SYNTAX_REFERENCE.md`.
For comprehensive guide, see `SODL_DOCUMENTATION.md`.
