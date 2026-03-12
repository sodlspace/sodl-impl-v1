# SODL v0.5 Quick Reference

Complete syntax reference for SODL (Specification-Oriented Development Language) v0.5.

## Table of Contents

1. [Syntax Fundamentals](#syntax-fundamentals)
2. [Top-Level Constructs](#top-level-constructs)
3. [System Definition](#system-definition)
4. [Templates](#templates)
5. [Interfaces](#interfaces)
6. [Modules](#modules)
7. [APIs and Models](#apis-and-models)
8. [Policies](#policies)
9. [Pipelines](#pipelines)
10. [Architecture Patterns](#architecture-patterns)
11. [Field Constraints](#field-constraints)
12. [Common Patterns](#common-patterns)

---

## Syntax Fundamentals

### Indentation

SODL uses indentation (2 or 4 spaces) to define block structure:

```sodl
system "MySystem":
    version = "1.0.0"
    stack:
        language = "Python 3.12"
        web = "FastAPI"
```

### Strings

Double quotes for strings:

```sodl
intent:
    primary = "Build a REST API"
```

### Lists

Square brackets with comma-separated values:

```sodl
outcomes = [
    "Create todos",
    "Delete todos",
    "Update todos"
]
```

### Comments

Hash symbol for comments:

```sodl
# This is a comment
stack:
    language = "Python 3.12"  # Inline comment
```

---

## Top-Level Constructs

| Construct | Purpose | Example |
|-----------|---------|---------|
| `system` | Concrete system definition | `system "MyApp":` |
| `template` | Reusable base specification | `template "BaseWebApp":` |
| `interface` | Functionality contract | `interface Repository:` |
| `policy` | Global rules with severity | `policy Security:` |
| `ui_theme` | UI component library | `ui_theme "Material":` |
| `module` | Unit of generation | `module UserAPI:` |
| `pipeline` | Generation process | `pipeline "Development":` |

---

## System Definition

### Basic Structure

```sodl
system "SystemName":
    version = "1.0.0"
    
    stack:
        language = "Python 3.12"
        web = "FastAPI"
        database = "PostgreSQL"
        orm = "SQLAlchemy"
        testing = ["pytest", "pytest-cov"]
    
    intent:
        primary = "System purpose"
        outcomes = ["Deliverable 1", "Deliverable 2"]
        out_of_scope = ["Excluded feature"]
    
    architecture:
        style = "Clean Architecture"
        layers = ["Domain", "Application", "Infrastructure", "Interface"]
    
    design_patterns:
        - name = "Repository"
          scope = "global"
        - name = "CQRS"
          scope = "modules: [Order, Inventory]"
    
    dependency_injection:
        container = "AutoWire"
        injection_style = "Constructor Injection"
        lifetime_rules:
            - service = "DatabaseConnection"
              scope = "Singleton"
            - service = "UserService"
              scope = "Transient"
    
    error_handling:
        strategy = "Result Pattern"
        error_codes:
            - code = "NOT_FOUND"
              http_status = 404
              user_message = "Resource not found"
        retry_policy:
            max_attempts = 3
            backoff = "exponential"
    
    observability:
        logging:
            format = "JSON"
            level = "INFO"
        tracing:
            enabled = true
            provider = "OpenTelemetry"
        metrics:
            enabled = true
            provider = "Prometheus"
    
    testing_strategy:
        unit_tests:
            framework = "pytest"
            coverage_target = 80%
        integration_tests:
            framework = "pytest-bdd"
        e2e_tests:
            framework = "playwright"
    
    security_patterns:
        authentication = "JWT"
        authorization = "RBAC"
        data_protection:
            encryption_at_rest = "AES-256"
            encryption_in_transit = "TLS 1.3"
```

### Extending Templates

```sodl
system "MyApp" extends "BaseWebApp":
    override stack.language = "Python 3.13"
    append stack.testing += "pytest-asyncio"
    remove stack.testing -= "pytest-cov"
    
    intent:
        primary = "My specific application"
```

---

## Templates

### Template Definition

```sodl
template "BasePythonWebApp":
    stack:
        language = "Python 3.12"
        testing = ["pytest"]
    
    architecture:
        style = "Clean Architecture"
        layers = ["Domain", "Application", "Infrastructure", "Interface"]
    
    design_patterns:
        - name = "Repository"
          scope = "global"
    
    policy Security:
        rule = "Validate all inputs"
        severity = "high"
```

### Template Chaining

```sodl
template "BaseWebApp":
    stack:
        language = "Python 3.12"

template "CRUDWebApp" extends "BaseWebApp":
    ui:
        components:
            - name = "StandardForm"
            - name = "DataTable"

system "ProductCatalog" extends "CRUDWebApp":
    intent:
        primary = "Product catalog system"
```

---

## Interfaces

### Basic Interface

```sodl
interface TodoRepository:
    doc = "Repository for todo CRUD operations"
    
    method create(todo: TodoInput) -> Todo
    method get_by_id(id: int) -> Optional[Todo]
    method get_all(filters: TodoFilters) -> List[Todo]
    method update(id: int, updates: TodoUpdate) -> Todo
    method delete(id: int) -> bool
    
    invariants:
        invariant "All todos have unique IDs"
        invariant "Timestamps stored in UTC"
```

### Interface Extension

```sodl
interface BaseRepository:
    doc = "Base repository contract"
    method find_by_id(id: str) -> Optional[Entity]
    method find_all() -> List[Entity]

interface TodoRepository extends BaseRepository:
    doc = "Todo-specific repository"
    method create(todo: TodoInput) -> Todo
    method get_by_priority(priority: str) -> List[Todo]
```

---

## Modules

### Complete Module Structure

```sodl
module TodoAPI:
    requires = [TodoRepository, UserService]
    implements = [ITodoAPI]
    exports = [ITodoAPI]
    
    owns = [
        "REST API for todos",
        "Request validation",
        "Response mapping"
    ]
    
    api:
        model TodoRequest:
            field title: str (min_length=1, max_length=200)
            field description: str (max_length=2000)
            field priority: str (enum=["low", "medium", "high"])
            field due_date: Optional[datetime]
        
        model TodoResponse:
            field id: int
            field title: str
            field completed: bool
            field created_at: datetime
        
        endpoint "GET /api/todos" -> List[TodoResponse]
        endpoint "POST /api/todos" -> TodoResponse (201)
        endpoint "GET /api/todos/{id}" -> TodoResponse
        endpoint "PUT /api/todos/{id}" -> TodoResponse
        endpoint "DELETE /api/todos/{id}" -> Empty (204)
    
    invariants:
        invariant "All endpoints require authentication"
        invariant "Request bodies validated against schemas"
        invariant "Rate limiting applied to all endpoints"
    
    acceptance:
        test "creates todo with valid data"
        test "returns 400 for invalid input"
        test "returns 404 for non-existent todo"
        test "returns 401 for unauthenticated requests"
    
    artifacts = [
        "app/routes/todo_routes.py",
        "app/schemas/todo.py",
        "app/validators/todo.py"
    ]
    
    config:
        rate_limit:
            requests_per_minute = 60
            burst_size = 10
```

### Module Design Patterns

```sodl
module OrderProcessing:
    requires = [OrderRepository, PaymentGateway, InventoryService]
    
    design_patterns:
        - name = "Saga"
          type = "Choreography"
          compensating_transactions = true
        - name = "CQRS"
          read_side = "OrderQueries"
          write_side = "OrderCommands"
    
    owns = ["Order lifecycle management"]
```

---

## APIs and Models

### Model with Field Constraints

```sodl
model UserInput:
    field email: str (
        pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
        max_length=255
    )
    field password: str (
        min_length=8,
        max_length=128,
        requires_uppercase=true,
        requires_lowercase=true,
        requires_digit=true
    )
    field name: str (min_length=1, max_length=100)
    field role: str (enum=["user", "moderator", "admin"], default="user")
```

### Constraint Types

```sodl
model Example:
    # String constraints
    field email: str (pattern="regex", min_length=1, max_length=255)
    
    # Numeric constraints
    field age: int (min=0, max=150)
    field price: decimal (min=0.01, max=999999.99, precision=2)
    
    # Collection constraints
    field tags: List[str] (max_items=10, unique=true)
    field items: List[OrderItem] (min_items=1, max_items=100)
    
    # Enum constraints
    field status: str (enum=["pending", "active", "completed"])
    
    # Boolean with default
    field active: bool (default=true)
```

### Endpoint Definitions

```sodl
api:
    # Query endpoint
    endpoint "GET /api/users" -> List[UserResponse]
    
    # Create endpoint
    endpoint "POST /api/users" -> UserResponse (201)
    
    # Get by ID
    endpoint "GET /api/users/{id}" -> UserResponse
    
    # Update endpoint
    endpoint "PUT /api/users/{id}" -> UserResponse
    
    # Delete endpoint
    endpoint "DELETE /api/users/{id}" -> Empty (204)
    
    # Custom operation
    endpoint "POST /api/users/{id}/activate" -> UserResponse
```

---

## Policies

### Security Policy

```sodl
policy SecurityPolicy:
    rules:
        "All passwords must be hashed using bcrypt with cost factor >= 10" severity = "critical"
        "JWT tokens must use RS256 algorithm with 2048-bit keys" severity = "critical"
        "All API responses must include security headers" severity = "high"
        "Failed login attempts must be logged with IP and timestamp" severity = "high"
        "Password reset tokens must expire within 1 hour" severity = "high"
        "Database connections must use TLS 1.3" severity = "critical"
        "PII data must be encrypted at rest using AES-256" severity = "critical"
```

### Performance Policy

```sodl
policy PerformancePolicy:
    rules:
        "API response time must be under 200ms for 95th percentile" severity = "high"
        "Database queries must complete within 100ms" severity = "high"
        "Cache hit ratio must be above 80%" severity = "medium"
        "Memory usage must not exceed 512MB per instance" severity = "medium"
```

---

## Pipelines

### Development Pipeline

```sodl
pipeline "Development":
    step ImplementModels:
        modules = ["DataLayer"]
        output = code
        require = "Define ORM models with relationships and constraints"
        gate = "Models pass unit tests"
    
    step ImplementServices:
        modules = ["ServiceLayer"]
        output = code
        require = "Implement business logic with error handling"
        gate = "Service tests pass"
    
    step ImplementAPI:
        modules = ["APILayer"]
        output = code
        require = "Create REST endpoints with validation"
        gate = "API integration tests pass"
    
    step ImplementUI:
        modules = ["WebUI"]
        output = code
        require = "Build responsive UI components"
        gate = "UI tests pass"
    
    step GenerateTests:
        output = tests
        require = "Generate test scaffolding"
        gate = "Test coverage >= 80%"
    
    step SecurityReview:
        output = security_report
        require = "Run security analysis"
        gate = "No critical or high severity issues"
```

---

## Architecture Patterns

### Clean Architecture

```sodl
architecture:
    style = "Clean Architecture"
    layers = ["Domain", "Application", "Infrastructure", "Interface"]
    
    layer_rules:
        - "Domain layer must not depend on any other layer"
        - "Application layer depends only on Domain"
        - "Infrastructure implements interfaces from Application"
        - "Interface adapts Application for external consumers"
```

### Hexagonal Architecture

```sodl
architecture:
    style = "Hexagonal (Ports and Adapters)"
    layers = ["Domain", "Application"]
    
    ports:
        - name = "Input Ports"
          type = "Use Cases"
        - name = "Output Ports"
          type = "Repository Interfaces"
    
    adapters:
        - name = "Input Adapters"
          implements = ["REST API", "GraphQL API", "CLI"]
        - name = "Output Adapters"
          implements = ["Database", "Message Queue", "External Services"]
```

### Layered Architecture

```sodl
architecture:
    style = "Layered Architecture"
    layers = ["Presentation", "Business", "Persistence", "Database"]
    
    layer_rules:
        - "Each layer can only depend on adjacent lower layer"
        - "Business layer contains all business logic"
        - "Persistence layer handles data access"
```

### Event-Driven Architecture

```sodl
architecture:
    style = "Event-Driven"
    
    event_bus:
        type = "Message Broker"
        implementation = "RabbitMQ"
    
    event_types:
        - name = "Domain Events"
          scope = "Within bounded context"
        - name = "Integration Events"
          scope = "Across bounded contexts"
    
    design_patterns:
        - name = "Event Sourcing"
          scope = "global"
        - name = "CQRS"
          scope = "global"
```

---

## Common Patterns

### CRUD Application

```sodl
system "CrudApp":
    architecture:
        style = "Clean Architecture"
        layers = ["Domain", "Application", "Infrastructure", "Interface"]
    
    module DataLayer:
        implements = [Repository]
        owns = ["ORM models", "Database operations"]
        artifacts = ["app/models/", "app/repositories/"]
    
    module ServiceLayer:
        requires = [Repository]
        owns = ["Business logic", "Validation"]
        artifacts = ["app/services/"]
    
    module APILayer:
        requires = [Service]
        owns = ["REST endpoints", "Request/Response mapping"]
        artifacts = ["app/routes/", "app/schemas/"]
    
    module WebUI:
        requires = [APILayer]
        owns = ["HTML templates", "Frontend logic"]
        artifacts = ["app/templates/", "app/static/"]
```

### Microservice

```sodl
system "OrderService":
    architecture:
        style = "Hexagonal"
        layers = ["Domain", "Application"]
    
    design_patterns:
        - name = "CQRS"
          scope = "global"
        - name = "Saga"
          scope = "modules: [OrderProcessing]"
    
    error_handling:
        strategy = "Result Pattern"
        retry_policy:
            max_attempts = 3
            backoff = "exponential"
    
    observability:
        logging:
            format = "JSON"
            level = "INFO"
        tracing:
            enabled = true
            provider = "OpenTelemetry"
    
    module OrderCommands:
        owns = ["Create order", "Update order", "Cancel order"]
    
    module OrderQueries:
        owns = ["Get order", "List orders", "Search orders"]
```

### REST API with JWT Auth

```sodl
system "AuthenticatedAPI":
    security_patterns:
        authentication = "JWT"
        authorization = "RBAC"
        token_expiry_minutes = 30
        refresh_token_expiry_days = 7
    
    module Authentication:
        owns = ["User registration", "Login", "Token refresh"]
        api:
            endpoint "POST /api/auth/register" -> AuthResponse
            endpoint "POST /api/auth/login" -> AuthResponse
            endpoint "POST /api/auth/refresh" -> AuthResponse
        
        invariants:
            invariant "Passwords hashed with bcrypt"
            invariant "Tokens signed with RS256"
    
    module ProtectedAPI:
        requires = [Authentication]
        owns = ["Protected resources"]
        
        invariants:
            invariant "All endpoints require valid JWT"
            invariant "RBAC checks on all operations"
```

---

## Validation Commands

```bash
# Compile and validate
sodlcompiler specification.sodl

# Show AST
sodlcompiler specification.sodl --show-ast

# Validate syntax only
sodlcompiler specification.sodl --validate

# Programmatic usage
python -c "from sodlcompiler import compile_source; compiler = compile_source(open('spec.sodl').read(), 'spec.sodl')"
```
