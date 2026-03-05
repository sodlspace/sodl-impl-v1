# SODL Language Documentation v0.5 (Enhanced)
## Specification-Oriented Development Language
### Complete Specification with Backend, Frontend, API-UI Binding, and Architecture Patterns Support

**Version:** 0.5 (Enhanced Draft)  
**Status:** Stable + Extensions  
**Last Updated:** 2026  

---

## Table of Contents

1. [Overview](#1-overview)
2. [Key Characteristics](#2-key-characteristics)
3. [Core Pipeline](#3-core-pipeline)
4. [Language Constructs](#4-language-constructs)
5. [System Definition](#5-system-definition)
6. [Templates and Inheritance](#6-templates-and-inheritance)
7. [UI/UX Extension](#7-uiux-extension)
8. [Interfaces](#8-interfaces)
9. [Policies](#9-policies)
10. [Modules](#10-modules)
11. [Pipelines and Steps](#11-pipelines-and-steps)
12. [Architecture & Design Patterns](#12-architecture--design-patterns) **[NEW]**
13. [Dependency Injection](#13-dependency-injection) **[NEW]**
14. [Error Handling & Observability](#14-error-handling--observability) **[NEW]**
15. [Testing Strategy](#15-testing-strategy) **[NEW]**
16. [Security & Data](#16-security--data) **[NEW]**
17. [Complete Examples](#17-complete-examples)
18. [Design Principles](#18-design-principles)
19. [Best Practices](#19-best-practices)
20. [Compiler Output](#20-compiler-output)
21. [Non-Goals](#21-non-goals)
22. [Language Reference](#22-language-reference)
23. [Version History](#23-version-history)
24. [Appendix A: Quick Reference](#appendix-a-quick-reference)
25. [Appendix B: Migration Guide v0.4 to v0.5](#appendix-b-migration-guide-v04-to-v05)

---

## 1. Overview

SODL (Specification-Oriented Development Language) is a Python-like, indentation-based Domain-Specific Language (DSL) for controlled AI-driven code generation. It allows developers to describe intent, architecture, constraints, UI/UX behavior, API definitions, automatic API-UI binding, **architectural patterns**, **dependency injection**, **error handling**, **observability**, and **testing strategies** in a concise, structured, and reproducible way.

SODL transforms prompt engineering into specification engineering, enabling reproducible, reviewable, and maintainable AI-driven development for both backend and frontend components.

### 1.1 Purpose

SODL serves as a bridge between human intent and AI-generated code. Instead of writing vague prompts, developers write precise specifications that:

- Define what must be built and why
- Constrain how generation proceeds
- Ensure quality through explicit rules
- Enable automatic UI generation from API definitions
- Support full-stack development in a single language
- **Enforce architectural patterns and design principles** **[NEW]**
- **Standardize error handling and observability** **[NEW]**
- **Define comprehensive testing strategies** **[NEW]**

### 1.2 Target Audience

- **Software Architects:** Define system structure, constraints, and architectural patterns
- **Developers:** Specify modules, interfaces, APIs, and implementation details
- **AI Coding Agents:** Consume specifications to generate code
- **Project Managers:** Track generation progress through pipelines
- **QA Engineers:** Define testing strategies and quality gates

### 1.3 Philosophy

SODL is built on the principle that specifications should be explicit, verifiable, and reusable. Rather than relying on AI to infer requirements, SODL makes all assumptions explicit and enforceable.

---

## 2. Key Characteristics

| Characteristic | Description | Benefit |
|----------------|-------------|---------|
| Python-like syntax | Familiar to software engineers | Low learning curve |
| Indentation-based blocks | Uses `:` and indentation for structure | Clean, readable code |
| Declarative | Describes what, not how | Focus on intent, not implementation |
| Explicit constraints | Over implicit assumptions | Reduces ambiguity |
| Human-writable, machine-compilable | Easy to write and deterministic to parse | Consistent output |
| AI-agent targeted | Generates instructions for AI coding agents, not application code | Controlled generation |
| Full-stack aware | Supports backend, frontend, and automatic API-UI binding | Unified specification |
| Template inheritance | Reuse specifications through extends mechanism | DRY principle |
| Policy enforcement | Severity-based rules with enforcement levels | Quality assurance |
| **Architecture patterns** | **Explicit architectural style and design patterns** | **Consistent code structure** **[NEW]** |
| **Dependency injection** | **Standardized DI configuration** | **Testability and modularity** **[NEW]** |
| **Error handling** | **Unified error handling strategy** | **Reliability and debugging** **[NEW]** |
| **Observability** | **Logging, tracing, metrics configuration** | **Production readiness** **[NEW]** |
| **Testing strategy** | **Comprehensive testing definitions** | **Quality assurance** **[NEW]** |

### 2.1 Syntax Fundamentals

#### 2.1.1 Indentation

SODL uses indentation (2 or 4 spaces) to define block structure, similar to Python.

```sodl
system "MySystem":
    version = "1.0.0"
    stack:
        language = "Python 3.12"
        web = "Flask"
```

#### 2.1.2 Strings

Strings can be defined with double quotes:

```sodl
intent:
    primary = "Build a todo list application"
```

#### 2.1.3 Lists

Lists use square brackets with comma-separated values:

```sodl
outcomes = [
    "Users can create todos",
    "Users can delete todos"
]
```

#### 2.1.4 Comments

Comments start with `#`:

```sodl
# This is a comment
stack:
    language = "Python 3.12"  # Inline comment
```

---

## 3. Core Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Intent    │ →  │    Plan     │ →  │ Prompt Chunks│ →  │Coding Agent │
└─────────────┘    └─────────────┘    └──────────────┘    └─────────────┘
```

### 3.1 Pipeline Stages

| Stage | Purpose | Output |
|-------|---------|--------|
| Intent | Defines what must be built and why | Intent specification |
| Plan | Defines how generation is staged and constrained | Generation plan |
| Prompt Chunks | Deterministic instructions consumed by an AI coding agent | Markdown files |
| Code Generation | Backend code via `output = code` | Application code |
| UI Generation | Frontend code via `output = ui` | UI components |
| Binding Generation | API-UI connections via `bindings` | Integration code |
| **Architecture Validation** | **Verify architectural patterns** | **Architecture report** **[NEW]** |
| **Test Generation** | **Generate tests per strategy** | **Test suites** **[NEW]** |

### 3.2 Flow Description

1. **Intent Phase:** Developer writes SODL specification defining system goals
2. **Plan Phase:** Compiler analyzes specification and creates generation plan
3. **Prompt Chunks Phase:** Compiler generates deterministic instructions for AI agents
4. **Coding Agent Phase:** AI agents (Cursor, Claude, GPT) consume instructions and generate code
5. **Verification Phase:** Generated code is validated against acceptance criteria
6. **Architecture Review:** **Verify architectural patterns are followed** **[NEW]**
7. **Test Execution:** **Run generated tests against quality gates** **[NEW]**

### 3.3 Compiler Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        SODL Compiler                            │
├─────────────────────────────────────────────────────────────────┤
│  1. Parse SODL specification                                    │
│  2. Validate syntax and semantics                               │
│  3. Resolve templates and inheritance                           │
│  4. Generate module-specific instructions                       │
│  5. Generate UI binding instructions                            │
│  6. Generate architecture pattern instructions                  │ **[NEW]**
│  7. Generate dependency injection configuration                 │ **[NEW]**
│  8. Generate error handling scaffolding                         │ **[NEW]**
│  9. Generate observability configuration                        │ **[NEW]**
│  10. Generate test scaffolding per strategy                     │ **[NEW]**
│  11. Output structured prompt chunks                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     .sodl/ Output Directory                     │
├─────────────────────────────────────────────────────────────────┤
│  global.md          # System-level context                      │
│  ui/                # UI-specific instructions                  │
│  modules/           # Module-specific instructions              │
│  steps/             # Step-by-step generation instructions      │
│  architecture/      # Architecture pattern instructions         │ **[NEW]**
│  testing/           # Test generation instructions              │ **[NEW]**
│  manifest.json      # Metadata and structure                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Language Constructs

### 4.1 Top-Level Constructs

| Construct | Purpose | Scope | Example |
|-----------|---------|-------|---------|
| `template` | Reusable base specification (including UI patterns) | Global | `template "BaseWebApp":` |
| `system` | Concrete system to be generated | Global | `system "MyApp":` |
| `interface` | Required functionality contract | Global | `interface TodoStore:` |
| `policy` | Global rules and constraints (Security, Performance) | Global | `policy Security:` |
| `ui_theme` | Global UI/UX rules and component library definitions | Global | `ui_theme "MaterialWeb":` |
| `module` | Unit of responsibility and generation | System | `module UserAPI:` |
| `pipeline` | Controlled generation process | System | `pipeline "Development":` |
| `step` | Atomic generation phase | Pipeline | `step Implement:` |
| **`architecture`** | **System architecture style and layers** | **System** | **`architecture:`** **[NEW]** |
| **`design_patterns`** | **Design patterns for modules** | **System/Module** | **`design_patterns:`** **[NEW]** |
| **`dependency_injection`** | **DI container configuration** | **System** | **`dependency_injection:`** **[NEW]** |
| **`error_handling`** | **Error handling strategy** | **System** | **`error_handling:`** **[NEW]** |
| **`observability`** | **Logging, tracing, metrics** | **System** | **`observability:`** **[NEW]** |
| **`testing_strategy`** | **Testing approach and coverage** | **System** | **`testing_strategy:`** **[NEW]** |
| **`security_patterns`** | **Security architecture patterns** | **System** | **`security_patterns:`** **[NEW]** |

### 4.2 Construct Relationships

```
┌──────────────────────────────────────────────────────────────┐
│                         system                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   stack     │  │   intent    │  │        ui           │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  modules    │  │  pipeline   │  │      policies       │  │
│  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────────────┐  │  │
│  │  │ api   │  │  │  │ step  │  │  │  │   Security    │  │  │
│  │  │ owns  │  │  │  └───────┘  │  │  │   Performance │  │  │
│  │  │ ui    │  │  │             │  │  └───────────────┘  │  │
│  │  └───────┘  │  │             │  │                     │  │
│  └─────────────┘  │             │  │                     │  │
│                   │             │  │                     │  │
│  ┌─────────────┐  │             │  │                     │  │
│  │ architecture│  │             │  │                     │  │
│  │ patterns    │  │             │  │                     │  │
│  │ di          │  │             │  │                     │  │
│  │ error       │  │             │  │                     │  │
│  │ observability│ │             │  │                     │  │
│  │ testing     │  │             │  │                     │  │
│  └─────────────┘  │             │  │                     │  │
└───────────────────┴─────────────┴──────────────────────────┘
         ↑                                    ↑
    extends template                    references ui_theme
```

### 4.3 Valid Construct Combinations

| Parent | Valid Children |
|--------|----------------|
| `system` | `stack`, `intent`, `ui`, `module`, `pipeline`, `policy`, `api`, `interface`, **`architecture`**, **`design_patterns`**, **`dependency_injection`**, **`error_handling`**, **`observability`**, **`testing_strategy`**, **`security_patterns`** |
| `template` | `stack`, `ui`, `policy`, `interface`, **`architecture`**, **`design_patterns`** |
| `module` | `owns`, `requires`, `implements`, `exports`, `api`, `ui`, `invariants`, `acceptance`, `artifacts`, `config`, **`design_patterns`** |
| `pipeline` | `step` |
| `ui` | `theme`, `rules`, `components`, `bindings`, `pages` |
| `interface` | `doc`, `method`, `invariants`, `extends` |
| `policy` | `rule`, `severity`, `rules` |

---

## 5. System Definition

A `system` is the root executable specification that defines a complete application or component.

### 5.1 Basic System Syntax

```sodl
system "MySystem":
    version = "1.0.0"
    stack:
        language = "Python 3.12"
        web = "Flask"
    intent:
        primary = "Main application goal"
    ui:
        theme = "Material"
        bindings:
            - method: "GET"
              control: "DataTable"
    architecture:
        style = "Clean Architecture"
        layers = ["Domain", "Application", "Infrastructure", "Interface"]
```

### 5.2 System Components

#### 5.2.1 version

Defines the specification version (not application version).

```sodl
system "MyApp":
    version = "1.0.0"
```

#### 5.2.2 stack

Defines technological context and dependencies.

```sodl
stack:
    language = "Python 3.12"
    web = "FastAPI"
    templating = "Jinja2"
    ui_framework = "Material Components Web"
    database = "PostgreSQL"
    orm = "SQLAlchemy"
    cache = "Redis"
    testing = ["pytest", "pytest-cov"]
    linting = ["flake8", "black"]
```

**Stack Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `language` | string | Yes | Programming language |
| `web` | string | No | Web framework |
| `templating` | string | No | Template engine |
| `ui_framework` | string | No | UI component library |
| `database` | string | No | Database system |
| `orm` | string | No | Object-relational mapper |
| `cache` | string | No | Caching system |
| `testing` | list | No | Testing frameworks |
| `linting` | list | No | Code quality tools |

#### 5.2.3 intent

Defines goals, outcomes, and scope boundaries.

```sodl
intent:
    primary = "Build a todo list application"
    outcomes = [
        "Users can create, read, update, delete todos",
        "Todos have categories and due dates",
        "RESTful API with JSON responses"
    ]
    out_of_scope = [
        "User authentication",
        "Real-time sync",
        "Mobile app"
    ]
```

**Intent Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `primary` | string | Yes | Main goal description |
| `outcomes` | list | No | Expected deliverables |
| `out_of_scope` | list | No | Explicitly excluded features |

#### 5.2.4 api (System Level)

Defines system-wide API endpoints.

```sodl
api:
    - endpoint: "/api/users"
      method: "GET"
      description: "Get list of users"
      response:
          type: "array"
          items:
              type: "object"
    - endpoint: "/api/users"
      method: "POST"
      description: "Create a user"
      request:
          type: "object"
```

---

## 6. Templates and Inheritance

Templates are reusable base specifications that can be extended by systems.

### 6.1 Template Definition

```sodl
template "BasePythonWebApp":
    stack:
        language = "Python 3.12"
        testing = ["pytest"]
    ui:
        theme = "BaseTheme"
        rules:
            - name: "ShowLoadingOnAsync"
              actions: ["showLoadingDuring(action.name)"]
    policy Security:
        rule = "No secrets in repository"
        severity = "critical"
        rule = "Validate all inputs"
        severity = "high"
    architecture:
        style = "Clean Architecture"
        layers = ["Domain", "Application", "Infrastructure", "Interface"]
    design_patterns:
        - name = "Repository"
          scope = "global"
        - name = "Dependency Injection"
          scope = "global"
```

### 6.2 Inheritance with extends

Systems can extend templates to inherit their configuration (including UI rules, architecture, and patterns).

```sodl
system "MyApp" extends "BasePythonWebApp":
    intent:
        primary = "My specific application"
    stack:
        web = "Flask"
    ui:
        # Inherits rules from BasePythonWebApp
        bindings:
            - endpoint_method: "GET"
              control_type: "DataTable"
    architecture:
        # Inherits style from template
        layers += ["Presentation"]  # Append additional layer
```

### 6.3 Inheritance Rules

| Rule | Description |
|------|-------------|
| Single inheritance only | A system can extend only one template (MVP) |
| Merge order: parent → child | Parent values are applied first, then child values |
| Child values override parent values | Child specifications take precedence |
| UI Rules are merged | Child rules can override parent behaviors |
| UI Components are merged | Child components can override parent templates |
| Policies are merged | Child policies add to or override parent policies |
| **Architecture is merged** | **Child can add/override layers** **[NEW]** |
| **Design patterns are merged** | **Child can add module-specific patterns** **[NEW]** |

### 6.4 Override Operations

| Operation | Syntax | Meaning | Example |
|-----------|--------|---------|---------|
| Replace | `override path = value` | Replace scalar or block | `override stack.language = "Python 3.13"` |
| Append | `append path += value` | Append to list | `append stack.testing += "pytest-asyncio"` |
| Remove | `remove path -= value` | Remove from list | `remove stack.testing -= "pytest-cov"` |
| Replace block | `replace block Name:` | Replace entire named block | `replace block ui:` |

### 6.5 Override Examples

```sodl
system "CustomApp" extends "BasePythonWebApp":
    override stack.language = "Python 3.13"
    append stack.testing += "pytest-asyncio"
    remove stack.testing -= "pytest-cov"
    override ui.theme = "DarkMode"
    append ui.rules += "CustomValidationRule"
    append architecture.layers += ["Presentation"]
    append design_patterns += 
        - name = "CQRS"
          scope = "modules: [Order, Inventory]"
    
    replace block ui:
        theme = "CustomTheme"
        rules:
            - name: "CustomRule"
              actions: ["customAction()"]
```

### 6.6 Template Chaining

Templates can extend other templates:

```sodl
template "BaseWebApp":
    stack:
        language = "Python 3.12"
    policy Security:
        rule = "Validate all inputs"
        severity = "high"
    architecture:
        style = "Layered Architecture"

template "CRUDWebApp" extends "BaseWebApp":
    ui:
        components:
            - name: "StandardForm"
            - name: "DataTable"
        bindings:
            - endpoint_method: "GET"
              control_type: "DataTable"
    design_patterns:
        - name = "Repository"
          scope = "global"
        - name = "Factory"
          scope = "modules: [Payment]"

system "ProductCatalog" extends "CRUDWebApp":
    intent:
        primary = "Product catalog system"
    stack:
        database = "PostgreSQL"
    architecture:
        style = "Clean Architecture"  # Override parent style
```

### 6.7 Template Best Practices

- **Keep templates focused:** Each template should address a specific concern
- **Document template requirements:** Specify what child systems must provide
- **Use meaningful names:** Template names should indicate their purpose
- **Test templates independently:** Verify templates work before extending
- **Version templates:** Track template changes for compatibility
- **Limit inheritance depth:** Max 3 levels to avoid complexity

---

## 7. UI/UX Extension

### 7.1 ui_theme (Top-Level Construct)

`ui_theme` defines reusable UI component libraries and global UX rules that can be referenced by systems.

```sodl
ui_theme "MaterialWeb":
    components:
        - name: "StandardForm"
          description: "Standard form with auto-fill and validation"
        - name: "DataTable"
          description: "Table for displaying entity lists"
        - name: "ConfirmationModal"
          description: "Confirmation modal dialog"
        - name: "NavigationMenu"
          description: "Primary navigation component"
        - name: "SearchBar"
          description: "Search input with autocomplete"
    rules:
        - name: "UserFriendlyErrors"
          severity = "high"
          description: "Display errors in a user-friendly format"
        - name: "AutoFillKnownFields"
          severity = "medium"
          description: "Auto-fill fields if data is available"
        - name: "ValidateOnBlur"
          severity = "high"
          description: "Validate field on blur"
        - name: "ShowLoadingOnAsync"
          severity = "medium"
          description: "Show spinner during async operations"
    bindings:
        - endpoint_method: "GET"
          control_type: "DataTable"
        - endpoint_method: "POST"
          control_type: "StandardForm"
        - endpoint_method: "PUT"
          control_type: "StandardForm"
        - endpoint_method: "DELETE"
          control_type: "ConfirmationModal"
```

**Usage in system:**

```sodl
system "MyApp":
    ui:
        theme = "MaterialWeb"  # References ui_theme definition
```

### 7.2 ui Section (System, Template, Module)

Defines UI structure, UX rules, component bindings, and pages.

```sodl
ui:
    theme = "StandardWeb"
    
    rules:
        - name: "AutoFillKnownFields"
          description: "Auto-fill fields if data is available"
          conditions:
            - "field.type == 'text' && field.name in ['email', 'name']"
          actions:
            - "prefillFromUserProfile(field.name)"
        
        - name: "ValidateOnBlur"
          description: "Validate field on blur"
          conditions:
            - "field.validation != null"
          actions:
            - "validateField(field.name, field.validation)"
        
        - name: "EnableButtonOnDependencies"
          description: "Button enabled only when dependent fields are filled"
          conditions:
            - "component.type == 'button' && component.dependencies != null"
          actions:
            - "enableIfFieldsFilled(component.dependencies.fields)"
        
        - name: "ShowLoadingOnAsync"
          description: "Show spinner during async operations"
          conditions:
            - "action.type == 'async'"
          actions:
            - "showLoadingDuring(action.name)"
        
        - name: "UserFriendlyErrors"
          description: "Display errors in a user-friendly format"
          conditions:
            - "action.result == 'error'"
          actions:
            - "showError(action.error, 'user_friendly')"
        
        - name: "ResponsiveLayout"
          description: "Adapt layout to screen size"
          conditions:
            - "viewport.width < 768"
          actions:
            - "switchToMobileLayout()"
        
        - name: "AccessibilityCompliance"
          description: "Ensure WCAG 2.1 AA compliance"
          conditions:
            - "component.rendered == true"
          actions:
            - "addAriaLabels(component)"
            - "ensureKeyboardNavigation(component)"
    
    components:
        - name: "StandardForm"
          description: "Standard form with auto-fill and validation"
          template:
              component: "form"
              fields: "{{fields}}"
              buttons:
                  - name: "submit"
                    label: "{{submitLabel | default('Save')}}"
                    type: "button"
                    dependencies: "{{fields}}"
                  - name: "cancel"
                    label: "Cancel"
                    type: "button"
                    onClick: "closeForm"
          ux_rules:
            - "AutoFillKnownFields"
            - "ValidateOnBlur"
            - "EnableButtonOnDependencies"
        
        - name: "DataTable"
          description: "Table for displaying entity lists"
          template:
              component: "table"
              columns: "{{columns}}"
              data_source: "{{endpoint}}"
              actions: "{{actions}}"
              pagination:
                  enabled: true
                  page_size: 25
              sorting:
                  enabled: true
                  default_column: "id"
                  default_order: "asc"
              filtering:
                  enabled: true
                  search_columns: ["name", "email"]
          ux_rules:
            - "ShowLoadingOnAsync"
            - "UserFriendlyErrors"
        
        - name: "ConfirmationModal"
          description: "Confirmation modal dialog"
          template:
              component: "modal"
              title: "{{title}}"
              content: "{{content}}"
              buttons:
                  - name: "confirm"
                    label: "{{confirmLabel | default('Confirm')}}"
                    onClick: "{{confirmAction}}"
                  - name: "cancel"
                    label: "{{cancelLabel | default('Cancel')}}"
                    onClick: "closeModal"
          ux_rules:
            - "ShowLoadingOnAsync"
            - "UserFriendlyErrors"
        
        - name: "NavigationMenu"
          description: "Primary navigation component"
          template:
              component: "nav"
              items: "{{menuItems}}"
              responsive: true
              mobile_breakpoint: 768
          ux_rules:
            - "ResponsiveLayout"
            - "AccessibilityCompliance"
        
        - name: "SearchBar"
          description: "Search input with autocomplete"
          template:
              component: "input"
              type: "search"
              placeholder: "{{placeholder | default('Search...')}}"
              autocomplete: "{{endpoint}}"
              debounce: 300
          ux_rules:
            - "ShowLoadingOnAsync"
    
    bindings:
        - endpoint_method: "GET"
          control_type: "DataTable"
          default_params:
              columns: ["id", "name", "email"]
              actions:
                  - name: "edit"
                    endpoint: "{{endpoint}}/{id}"
                    icon: "edit"
                  - name: "delete"
                    endpoint: "{{endpoint}}/{id}"
                    icon: "delete"
              pagination:
                  enabled: true
                  page_size: 25
              sorting:
                  enabled: true
              filtering:
                   enabled: true
        
        - endpoint_method: "POST"
          control_type: "StandardForm"
          default_params:
              fields:
                  - name: "name"
                    type: "text"
                    validation: "required"
                    label: "Name"
                  - name: "email"
                    type: "email"
                    validation: "email"
                    label: "Email"
              submitLabel: "Create"
              cancelEnabled: true
        
        - endpoint_method: "PUT"
          control_type: "StandardForm"
          default_params:
              fields:
                  - name: "name"
                    type: "text"
                    validation: "required"
                    label: "Name"
                  - name: "email"
                    type: "email"
                    validation: "email"
                    label: "Email"
              submitLabel: "Save"
              cancelEnabled: true
              loadExistingData: true
        
        - endpoint_method: "DELETE"
          control_type: "ConfirmationModal"
          default_params:
              title: "Confirm Deletion"
              content: "Are you sure you want to delete this item?"
              confirmLabel: "Delete"
              cancelLabel: "Cancel"
              confirmAction: "deleteItem"
    
    pages:
        - name: "UsersPage"
          description: "User management page"
          layout: "default"
          components:
              - type: "NavigationMenu"
                params:
                  menuItems: ["Users", "Settings", "Logout"]
              - type: "DataTable"
                params:
                  endpoint: "/api/users"
                  columns: ["id", "name", "email", "created_at"]
              - type: "StandardForm"
                params:
                  endpoint: "/api/users"
                  mode: "create"
                  title: "Create User"
              - type: "StandardForm"
                params:
                  endpoint: "/api/users/{id}"
                  mode: "edit"
                  title: "Edit User"
              - type: "ConfirmationModal"
                params:
                  endpoint: "/api/users/{id}"
                  title: "Delete User"
        
        - name: "DashboardPage"
          description: "Main dashboard"
          layout: "dashboard"
          components:
              - type: "NavigationMenu"
                params:
                  menuItems: ["Dashboard", "Users", "Reports"]
              - type: "DataTable"
                params:
                  endpoint: "/api/recent-activity"
                  columns: ["timestamp", "action", "user"]
```

### 7.3 Automatic API-UI Binding

The `bindings` section enables automatic mapping of API endpoints to UI controls:

| Endpoint Method | Control Type | Default Behavior | Parameters |
|-----------------|--------------|------------------|------------|
| GET | DataTable | Display list with edit/delete actions | columns, actions, pagination, sorting |
| POST | StandardForm | Create form with validation | fields, submitLabel, cancelEnabled |
| PUT | StandardForm | Edit form with pre-filled data | fields, submitLabel, loadExistingData |
| DELETE | ConfirmationModal | Confirmation dialog before deletion | title, content, confirmLabel |
| GET/{id} | StandardForm | View/Edit single item | fields, mode, title |

### 7.4 UX Rules System

| Rule Name | Trigger | Action | Severity |
|-----------|---------|--------|----------|
| AutoFillKnownFields | Text fields with known names | Pre-fill from user profile | medium |
| ValidateOnBlur | Field with validation rules | Validate on blur event | high |
| EnableButtonOnDependencies | Button with dependencies | Enable when fields filled | medium |
| ShowLoadingOnAsync | Async action | Show loading spinner | medium |
| UserFriendlyErrors | Error result | Display user-friendly message | high |
| ResponsiveLayout | Viewport width < 768px | Switch to mobile layout | medium |
| AccessibilityCompliance | Component rendered | Add ARIA labels, keyboard nav | high |

### 7.5 UI Component Templates

#### 7.5.1 StandardForm

```sodl
components:
    - name: "StandardForm"
      template:
          component: "form"
          fields: "{{fields}}"
          buttons:
              - name: "submit"
                label: "{{submitLabel | default('Save')}}"
                type: "button"
                dependencies: "{{fields}}"
          ux_rules:
              - "AutoFillKnownFields"
              - "ValidateOnBlur"
              - "EnableButtonOnDependencies"
```

#### 7.5.2 DataTable

```sodl
components:
    - name: "DataTable"
      template:
          component: "table"
          columns: "{{columns}}"
          data_source: "{{endpoint}}"
          actions: "{{actions}}"
          pagination:
              enabled: true
              page_size: 25
          sorting:
              enabled: true
          filtering:
              enabled: true
```

#### 7.5.3 ConfirmationModal

```sodl
components:
    - name: "ConfirmationModal"
      template:
          component: "modal"
          title: "{{title}}"
          content: "{{content}}"
          buttons:
              - name: "confirm"
                label: "{{confirmLabel | default('Confirm')}}"
                onClick: "{{confirmAction}}"
              - name: "cancel"
                label: "{{cancelLabel | default('Cancel')}}"
                onClick: "closeModal"
```

### 7.6 UI Binding Examples

```sodl
# Example: Automatic binding for CRUD operations
ui:
    bindings:
        - endpoint_method: "GET"
          control_type: "DataTable"
          default_params:
              columns: ["id", "name", "email", "created_at"]
              actions:
                  - name: "edit"
                    endpoint: "{{endpoint}}/{id}"
                  - name: "delete"
                    endpoint: "{{endpoint}}/{id}"
        
        - endpoint_method: "POST"
          control_type: "StandardForm"
          default_params:
              fields:
                  - name: "name"
                    type: "text"
                    validation: "required"
                  - name: "email"
                    type: "email"
                    validation: "email"
              submitLabel: "Create"
        
        - endpoint_method: "PUT"
          control_type: "StandardForm"
          default_params:
              fields:
                  - name: "name"
                    type: "text"
                    validation: "required"
                  - name: "email"
                    type: "email"
                    validation: "email"
              submitLabel: "Save"
              loadExistingData: true
        
        - endpoint_method: "DELETE"
          control_type: "ConfirmationModal"
          default_params:
              title: "Confirm Deletion"
              content: "Are you sure?"
```

---

## 8. Interfaces

Interfaces describe required functionality contracts without implementation details.

### 8.1 Interface Declaration

```sodl
interface ImageStore:
    doc = "Stores PNG images and returns public URLs"
    method save_png(pngBytes: bytes) -> SavedImage
    method get_url(filename: str) -> str
    invariants:
        invariant = "Filename is generated server-side"
        invariant = "URLs are publicly accessible"
```

### 8.2 Interface Methods

Method syntax: `method name(param: type) -> return_type`

```sodl
interface TodoStore:
    doc = "Persistent storage for todo items"
    method create(todo: TodoInput) -> TodoItem
    method get_all() -> List[TodoItem]
    method get_by_id(id: UUID) -> Optional[TodoItem]
    method update(id: UUID, updates: TodoUpdate) -> TodoItem
    method delete(id: UUID) -> bool
```

### 8.3 Interface Inheritance

```sodl
interface Storage:
    method save( bytes) -> str
    method retrieve(key: str) -> bytes

interface ImageStorage extends Storage:
    override method save( bytes) -> SavedImage
    method get_thumbnail(key: str, size: tuple) -> bytes
```

### 8.4 Interface Usage in Modules

```sodl
module ImageAPI:
    requires = [ImageStore]  # Depends on interface

module StorageLocal:
    implements = [ImageStore]  # Must implement all methods
    exports = [ImageStore]  # Provides interface to others
```

**Semantics:**

| Keyword | Meaning | Enforcement |
|---------|---------|-------------|
| `requires` | Module depends only on interface contract | Must be provided by another module |
| `implements` | Module must implement all interface methods | All methods must be defined |
| `exports` | Module provides interface to other modules | Interface becomes available system-wide |

### 8.5 Interface Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `doc` | string | No | Interface documentation |
| `method` | method def | Yes | Method signatures |
| `invariants` | list | No | Constraints that must hold |
| `extends` | interface name | No | Parent interface |

### 8.6 Complete Interface Example

```sodl
interface UserRepository:
    doc = "User data access layer"
    
    method create(user: UserInput) -> User
    method get_by_id(id: UUID) -> Optional[User]
    method get_by_email(email: str) -> Optional[User]
    method get_all(page: int, page_size: int) -> PagedUsers
    method update(id: UUID, updates: UserUpdate) -> User
    method delete(id: UUID) -> bool
    
    invariants:
        invariant = "Email addresses are unique"
        invariant = "User IDs are UUIDs"
        invariant = "Passwords are never returned in responses"
        invariant = "All timestamps use UTC"
```

---

## 9. Policies

Policies define global rules and constraints with severity levels.

### 9.1 Policy Syntax

```sodl
policy Security:
    rule = "No secrets in repository"
    severity = "critical"
    rule = "Validate all user input"
    severity = "high"
    rule = "Use HTTPS for external APIs"
    severity = "high"
    rule = "Log security events"
    severity = "medium"
```

### 9.2 Severity Levels

| Severity | Meaning | Enforcement | Example |
|----------|---------|-------------|---------|
| `critical` | MUST NOT violate | Hard constraint, blocks generation | No secrets in code |
| `high` | MUST follow | Required constraint | Input validation |
| `medium` | SHOULD follow | Strong recommendation | Caching strategy |
| `low` | MAY follow | Suggestion | Code comments |

### 9.3 Multiple Policies

```sodl
system "SecureApp":
    policy Security:
        rule = "Encrypt sensitive data at rest"
        severity = "critical"
        rule = "Use parameterized queries"
        severity = "critical"
        rule = "Implement rate limiting"
        severity = "high"
    
    policy Performance:
        rule = "Cache frequently accessed data"
        severity = "medium"
        rule = "Use database indexes"
        severity = "high"
        rule = "Lazy load large resources"
        severity = "medium"
    
    policy CodeQuality:
        rule = "Test coverage above 80%"
        severity = "high"
        rule = "No code duplication"
        severity = "medium"
        rule = "Document public APIs"
        severity = "medium"
```

### 9.4 API Security Policies

```sodl
policy SecureAPIAccess:
    rule = "All API calls must be authenticated"
    severity = "critical"
    rules:
        - if: "api_call.method != 'GET'"
          then: "require_authentication"
        - if: "api_call.endpoint contains '/admin'"
          then: "require_admin_role"

policy InputValidation:
    rule = "All input data must be validated"
    severity = "high"
    rules:
        - if: "request.body != null"
          then: "validate_input(request.body)"
        - if: "request.params != null"
          then: "validate_params(request.params)"
        - if: "request.headers != null"
          then: "validate_headers(request.headers)"
```

### 9.5 UI Policies

```sodl
policy UIAccessibility:
    rule = "All UI components must be accessible"
    severity = "high"
    rules:
        - if: "component.type == 'button'"
          then: "add_aria_label(component)"
        - if: "component.type == 'image'"
          then: "add_alt_text(component)"
        - if: "component.type == 'form'"
          then: "add_keyboard_navigation(component)"

policy UIPerformance:
    rule = "UI must load within 3 seconds"
    severity = "high"
    rules:
        - if: "page.initial_load"
          then: "lazy_load_non_critical_resources()"
        - if: "image.size > 100KB"
          then: "compress_and_optimize(image)"
```

### 9.6 Policy Inheritance

Policies from templates are inherited by systems:

```sodl
template "BaseWebApp":
    policy Security:
        rule = "Validate all inputs"
        severity = "high"

system "MyApp" extends "BaseWebApp":
    policy Security:
        rule = "Encrypt sensitive data"
        severity = "critical"
    # Inherits "Validate all inputs" from BaseWebApp
```

---

## 10. Modules

Modules are the primary unit of generation and responsibility.

### 10.1 Module Structure

```sodl
module ImageAPI:
    owns = ["Image upload endpoint", "Image retrieval logic"]
    requires = [ImageStore]
    api:
        endpoint "POST/api/images" -> JsonSavedImage
        endpoint "GET/api/images/{id}" -> JsonImage
    ui:
        pages:
            - name: "UploadPage"
              components:
                  - type: "StandardForm"
                    params:
                        endpoint: "/api/images"
    invariants:
        invariant = "Accept only PNG and JPEG formats"
        invariant = "Validate file size < 10MB"
    acceptance:
        test = "valid image uploads successfully"
        test = "oversized image returns 413"
        test = "invalid format returns 400"
    artifacts = ["app/api.py", "app/routes/images.py"]
    design_patterns:
        - name = "Factory"
          purpose = "Create different image processors"
```

### 10.2 Module Sections

| Section | Purpose | Example | Required |
|---------|---------|---------|----------|
| `owns` | Domain ownership and responsibilities | `owns=["User authentication"]` | No |
| `requires` | Required interfaces (dependencies) | `requires=[TodoStore, Logger]` | No |
| `implements` | Implemented interfaces | `implements=[TodoStore]` | No |
| `exports` | Provided interfaces to others | `exports=[TodoStore]` | No |
| `api` | External API definition | `endpoint "GET/api/todos"` | No |
| `ui` | UI pages and components owned by module | `pages: [UsersPage]` | No |
| `invariants` | Must-hold constraints | `invariant "IDs are unique"` | No |
| `acceptance` | Definition of Done (tests) | `test "creates todo successfully"` | No |
| `artifacts` | Allowed file scope | `artifacts=["app.py"]` | No |
| `config` | Module configuration | `config: timeout = 30` | No |
| **`design_patterns`** | **Design patterns for this module** | **`design_patterns: [...]`** | **No** **[NEW]** |

### 10.3 API Endpoints

```sodl
module TodoAPI:
    api:
        endpoint "GET/api/todos" -> List[TodoResponse]
        endpoint "POST/api/todos" -> TodoResponse (201 CREATED)
        endpoint "PUT/api/todos/{id}" -> TodoResponse
        endpoint "DELETE/api/todos/{id}" -> Empty (204 NO CONTENT)
        endpoint "GET/api/todos/{id}" -> TodoResponse
```

### 10.4 API Models

```sodl
module StorageModels:
    owns = ["Data models for todo items"]
    api:
        model TodoItem:
            field id: UUID
            field title: str
            field description: Optional[str]
            field category: Optional[str]
            field due_date: Optional[datetime]
            field priority: int (1-3)
            field completed: bool
        
        model TodoInput:
            field title: str
            field description: Optional[str]
            field category: Optional[str]
            field due_date: Optional[str]
            field priority: int (1-3)
        
        model TodoUpdate:
            field title: Optional[str]
            field description: Optional[str]
            field category: Optional[str]
            field due_date: Optional[str]
            field priority: Optional[int]
            field completed: Optional[bool]
        
        model TodoResponse:
            field id: UUID
            field title: str
            field description: Optional[str]
            field category: Optional[str]
            field due_date: Optional[datetime]
            field priority: int
            field completed: bool
            field created_at: datetime
            field updated_at: datetime
```

### 10.5 Invariants

```sodl
module UserService:
    invariants:
        invariant = "Email addresses are unique"
        invariant = "Passwords are hashed with bcrypt"
        invariant = "User IDs are UUIDs"
        invariant = "All timestamps use UTC"
        invariant = "Password minimum length is 8 characters"
        invariant = "Email format is validated"
```

### 10.6 Acceptance Tests

```sodl
module WebUI:
    acceptance:
        test = "renders empty state when no todos exist"
        test = "submits valid todo and displays it"
        test = "shows error on invalid due date"
        test = "toggles completion status correctly"
        test = "deletes todo and updates UI"
        test = "validates required fields before submission"
        test = "displays loading state during async operations"
        test = "shows user-friendly error messages"
```

### 10.7 Complete Module Example

```sodl
module InMemoryTodoStore:
    implements = [TodoStore]
    exports = [TodoStore]
    config:
        persistence = "in-memory (ephemeral)"
        max_items = 1000
        thread_safe = true
    invariants:
        invariant = "Thread-safe access to todo list"
        invariant = "All operations maintain data consistency"
        invariant = "UUIDs are unique across all todos"
        invariant = "Max items limit is enforced"
    acceptance:
        test = "persists todo across GET calls within same runtime"
        test = "correctly creates new todos with unique IDs"
        test = "properly updates existing todos"
        test = "successfully deletes todos"
        test = "handles concurrent access safely"
        test = "returns 404 for non-existent todo ID"
        test = "enforces max items limit"
    artifacts = ["app/storage.py"]
    design_patterns:
        - name = "Repository"
          purpose = "Abstract data access"
```

### 10.8 Module Dependencies

```sodl
module ProductAPI:
    requires = [ProductRepository, CacheService]
    # This module depends on ProductRepository and CacheService interfaces
    # Implementation must be provided by other modules

module PostgresProductRepository:
    implements = [ProductRepository]
    exports = [ProductRepository]
    # This module provides ProductRepository implementation

module RedisCache:
    implements = [CacheService]
    exports = [CacheService]
    # This module provides CacheService implementation
```

---

## 11. Pipelines and Steps

Pipelines define the controlled generation process.

### 11.1 Pipeline Syntax

```sodl
pipeline "Development":
    step Design:
        output = design
        require = "Produce architecture diagram and data model"
    step Implement:
        modules = ["StorageModels", "TodoStore", "TodoAPI"]
        output = code
        gate = "All acceptance tests pass"
    step GenerateUI:
        modules = ["UserUI"]
        output = ui
        gate = "UI components render correctly"
    step Review:
        output = diff
        require = "Code review checklist completed"
```

### 11.2 Step Definition

Steps are atomic generation phases with specific outputs and constraints.

```sodl
step Implement "Backend":
    modules = ["ImageAPI", "StorageLocal"]
    output = code
    require = "Generate code incrementally"
    gate = "pytest passes with 80% coverage"
```

### 11.3 Step Components

| Component | Purpose | Example | Required |
|-----------|---------|---------|----------|
| `modules` | Which modules to generate | `modules=["TodoAPI"]` | No |
| `output` | Type of output to produce | `output = code` | Yes |
| `require` | Additional requirements | `require = "Follow style guide"` | No |
| `gate` | Exit criteria | `gate = "All tests pass"` | No |
| `depends_on` | Step dependencies | `depends_on = ["Design"]` | No |

### 11.4 Allowed Output Types

| Type | Description | Use Case |
|------|-------------|----------|
| `design` | Architecture diagrams, data models | Planning phase |
| `code` | Application code (backend/frontend) | Implementation phase |
| `ui` | User Interface code (HTML, CSS, JS components) | UI generation phase |
| `tests` | Test code | Testing phase |
| `diff` | Code changes/review | Review phase |
| `docs` | Documentation | Documentation phase |
| **`architecture`** | **Architecture validation report** | **Architecture review** **[NEW]** |

### 11.5 Complete Pipeline Example

```sodl
pipeline "Cursor":
    step Design:
        output = design
        require = "Create data model and API specification"
        gate = "Architecture approved"
    
    step ImplementModels:
        modules = ["StorageModels", "APISchemas"]
        output = code
        require = "Use Pydantic for validation"
        gate = "Models compile without errors"
        depends_on = ["Design"]
    
    step ImplementStorage:
        modules = ["InMemoryTodoStore"]
        output = code
        require = "Thread-safe implementation"
        gate = "Storage tests pass"
        depends_on = ["ImplementModels"]
    
    step ImplementAPI:
        modules = ["TodoAPI"]
        output = code
        require = "RESTful conventions"
        gate = "API tests pass"
        depends_on = ["ImplementStorage"]
    
    step ImplementUI:
        modules = ["WebUI"]
        output = ui
        require = "Material Design components"
        gate = "UI tests pass"
        depends_on = ["ImplementAPI"]
    
    step ValidateArchitecture:
        output = architecture
        require = "Verify Clean Architecture patterns"
        gate = "Architecture validation passed"
        depends_on = ["ImplementAPI"]
    
    step GenerateTests:
        output = tests
        require = "Generate tests per testing_strategy"
        gate = "Test scaffolding complete"
        depends_on = ["ImplementAPI"]
    
    step FinalReview:
        output = diff
        require = "All acceptance criteria met"
        gate = "Full integration test suite passes"
        depends_on = ["ImplementUI", "ValidateArchitecture", "GenerateTests"]
```

### 11.6 Pipeline Best Practices

- **Order steps by logical dependency:** Later steps should depend on earlier steps
- **Use gates to enforce quality:** Each step should have clear exit criteria
- **Make steps atomic:** Each step should accomplish one clear goal
- **Specify clear output types:** Define what each step produces
- **Document dependencies:** Use `depends_on` to clarify step order
- **Include review steps:** Add review gates before deployment
- **Include architecture validation:** Verify patterns before final review **[NEW]**
- **Include test generation:** Generate tests as separate step **[NEW]**

---

## 12. Architecture & Design Patterns **[NEW]**

### 12.1 architecture Construct

Defines the overall architectural style and layer structure of the system.

```sodl
architecture:
    style = "Clean Architecture"  # or "Hexagonal", "MVC", "Microservices", "Layered"
    dependency_rule = "Dependencies point inward"
    layers = ["Domain", "Application", "Infrastructure", "Interface"]
    layer_descriptions:
        - layer = "Domain"
          description = "Business logic and entities"
          dependencies = []
        - layer = "Application"
          description = "Use cases and orchestration"
          dependencies = ["Domain"]
        - layer = "Infrastructure"
          description = "External services and data access"
          dependencies = ["Domain", "Application"]
        - layer = "Interface"
          description = "API, UI, and external interfaces"
          dependencies = ["Application"]
```

**Architecture Styles:**

| Style | Description | Best For |
|-------|-------------|----------|
| `Clean Architecture` | Layers with inward dependencies | Enterprise applications |
| `Hexagonal` | Ports and adapters | Systems with multiple interfaces |
| `MVC` | Model-View-Controller | Web applications |
| `Microservices` | Distributed services | Scalable systems |
| `Layered` | Traditional n-tier | Simple applications |
| `Event-Driven` | Event-based communication | Real-time systems |

### 12.2 design_patterns Construct (System Level)

Defines design patterns to be used across the system.

```sodl
design_patterns:
    - name = "Repository"
      purpose = "Abstract database access"
      scope = "global"
      when_to_use = "All data access operations"
      template = "Generic repository pattern with unit of work"
    
    - name = "CQRS"
      purpose = "Separate read and write models"
      scope = "modules: [Order, Inventory]"
      when_to_use = "High read/write ratio, complex queries"
      template = "Commands go to WriteModel, Queries to ReadModel"
    
    - name = "Saga"
      purpose = "Distributed transaction management"
      scope = "modules: [Payment, Order]"
      when_to_use = "Multi-service operations requiring rollback"
      template = "Orchestration-based saga with compensating transactions"
    
    - name = "Factory"
      purpose = "Object creation abstraction"
      scope = "modules: [Payment]"
      when_to_use = "Multiple implementations of same interface"
      template = "Abstract factory with concrete implementations"
    
    - name = "Observer"
      purpose = "Event notification system"
      scope = "global"
      when_to_use = "Decoupled event handling"
      template = "EventBus with subscriber pattern"
    
    - name = "Strategy"
      purpose = "Interchangeable algorithms"
      scope = "modules: [Payment, Notification]"
      when_to_use = "Multiple algorithms for same operation"
      template = "Strategy interface with concrete implementations"
```

### 12.3 design_patterns Construct (Module Level)

Modules can specify their own design patterns:

```sodl
module "PaymentModule":
    owns = ["Payment processing logic"]
    requires = ["PaymentGateway", "OrderService"]
    design_patterns:
        - name = "Strategy"
          purpose = "Support multiple payment providers"
          context = "PaymentProcessor interface with Stripe/PayPal implementations"
        
        - name = "Observer"
          purpose = "Notify services on payment events"
          context = "EventBus for OrderCreated, PaymentFailed events"
        
        - name = "Repository"
          purpose = "Abstract database access"
          context = "Generic repository for all entities"
```

### 12.4 pattern_library Construct (Top-Level)

Reusable pattern definitions that can be referenced by systems.

```sodl
pattern_library "StandardPatterns":
    pattern "CQRS":
        description = "Separate read and write models"
        when_to_use = "High read/write ratio, complex queries"
        template = "Commands go to WriteModel, Queries to ReadModel"
        implementation_notes = "Use separate databases for read/write if needed"
    
    pattern "Saga":
        description = "Distributed transaction management"
        when_to_use = "Multi-service operations requiring rollback"
        template = "Orchestration-based saga with compensating transactions"
        implementation_notes = "Store saga state for recovery"
    
    pattern "Repository":
        description = "Abstract data access layer"
        when_to_use = "All database operations"
        template = "Generic repository with unit of work"
        implementation_notes = "Use generics for common operations"
```

**Usage in system:**

```sodl
system "MyApp":
    design_patterns:
        - ref = "StandardPatterns.CQRS"
          scope = "modules: [Order, Inventory]"
        - ref = "StandardPatterns.Repository"
          scope = "global"
```

### 12.5 Architecture Validation

Architecture patterns are validated during the pipeline:

```sodl
pipeline "Production":
    step ValidateArchitecture:
        output = architecture
        require = "Verify all modules follow Clean Architecture"
        gate = "No dependency violations detected"
        depends_on = ["ImplementAPI"]
```

**Validation Rules:**

- Dependencies must follow layer rules
- Patterns must be implemented as specified
- No circular dependencies between modules
- Interface contracts must be respected

---

## 13. Dependency Injection **[NEW]**

### 13.1 dependency_injection Construct

Defines the dependency injection container configuration and lifetime rules.

```sodl
dependency_injection:
    container = "AutoWire"  # or "Manual", "Unity", "Ninject", "Spring"
    injection_style = "Constructor Injection"  # or "Property Injection", "Method Injection"
    
    lifetime_rules:
        - service = "DatabaseConnection"
          scope = "Singleton"
          description = "Single connection pool for application lifetime"
        
        - service = "UserSession"
          scope = "Request"
          description = "New session per HTTP request"
        
        - service = "EmailService"
          scope = "Transient"
          description = "New instance per injection"
        
        - service = "CacheService"
          scope = "Singleton"
          description = "Shared cache across application"
        
        - service = "Logger"
          scope = "Singleton"
          description = "Centralized logging instance"
    
    registration_conventions:
        - pattern = "*Repository"
          scope = "Singleton"
        - pattern = "*Service"
          scope = "Transient"
        - pattern = "*Controller"
          scope = "Transient"
    
    modules_to_scan:
        - "app/services"
        - "app/repositories"
        - "app/controllers"
```

### 13.2 Lifetime Scopes

| Scope | Description | Use Case |
|-------|-------------|----------|
| `Singleton` | Single instance for application lifetime | Database connections, cache, logger |
| `Request` | Single instance per HTTP request | User session, request context |
| `Transient` | New instance per injection | Statelessservices, validators |
| `Scoped` | Single instance per scope (custom) | Unit of work, transaction |

### 13.3 Module-Level DI Configuration

Modules can override or add DI registrations:

```sodl
module "PaymentModule":
    config:
        dependency_injection:
            - service = "PaymentProcessor"
              scope = "Singleton"
              interface = "IPaymentProcessor"
            - service = "StripePaymentProcessor"
              scope = "Singleton"
              implements = "IPaymentProcessor"
```

### 13.4 DI Best Practices

- **Prefer constructor injection** for explicit dependencies
- **Use interfaces** for service abstractions
- **Avoid service locator** pattern
- **Register services in composition root**
- **Keep services stateless** when possible
- **Use appropriate lifetime scopes** to avoid memory leaks

---

## 14. Error Handling & Observability **[NEW]**

### 14.1 error_handling Construct

Defines the error handling strategy for the system.

```sodl
error_handling:
    strategy = "Result Pattern"  # or "Exceptions", "Either Monad", "HTTP Status Codes"
    
    error_codes:
        - code = "USER_NOT_FOUND"
          http_status = 404
          user_message = "User does not exist"
          log_level = "warning"
          retry = false
        
        - code = "VALIDATION_ERROR"
          http_status = 422
          user_message = "Invalid input data"
          log_level = "info"
          retry = false
        
        - code = "DATABASE_ERROR"
          http_status = 500
          user_message = "Internal server error"
          log_level = "error"
          retry = true
        
        - code = "RATE_LIMIT_EXCEEDED"
          http_status = 429
          user_message = "Too many requests"
          log_level = "warning"
          retry = true
    
    retry_policy:
        max_attempts = 3
        backoff = "exponential"
        initial_delay = "1s"
        max_delay = "30s"
        timeout = "30s"
        retryable_errors = ["DATABASE_ERROR", "NETWORK_ERROR", "TIMEOUT"]
    
    global_handler = "MiddlewareErrorHandler"
    
    error_response_format:
        include_stack_trace = false  # Never in production
        include_error_code = true
        include_timestamp = true
        include_request_id = true
```

### 14.2 observability Construct

Defines logging, tracing, and metrics configuration.

```sodl
observability:
    logging:
        format = "JSON"  # or "Text", "Structured"
        level = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        correlation_id = "required"
        include_timestamp = true
        include_source = true
        output = ["console", "file", "elasticsearch"]
        retention_days = 30
        sensitive_fields = ["password", "token", "credit_card"]
    
    tracing:
        enabled = true
        provider = "OpenTelemetry"  # or "Jaeger", "Zipkin", "AWS X-Ray"
        sampling_rate = 0.1  # 10% of requests
        propagation = ["traceparent", "baggage"]
        export_to = ["jaeger", "prometheus"]
        include_db_queries = true
        include_http_requests = true
    
    metrics:
        enabled = true
        provider = "Prometheus"  # or "CloudWatch", "Datadog"
        default_buckets = [0.1, 0.5, 1.0, 5.0, 10.0]
        default_labels = ["service", "version", "environment"]
        custom_metrics:
            - name = "business_transactions_total"
              type = "counter"
              labels = ["transaction_type", "status"]
            - name = "request_duration_seconds"
              type = "histogram"
              labels = ["endpoint", "method", "status_code"]
    
    health_checks:
        enabled = true
        endpoint = "/health"
        checks = ["database", "cache", "external_apis"]
        interval = "30s"
    
    alerts:
        - name = "HighErrorRate"
          condition = "error_rate > 5%"
          window = "5m"
          severity = "critical"
          notify = ["slack", "pagerduty"]
        
        - name = "HighLatency"
          condition = "p99_latency > 2s"
          window = "10m"
          severity = "warning"
          notify = ["slack"]
```

### 14.3 Module-Level Error Handling

Modules can define specific error handling:

```sodl
module "PaymentModule":
    config:
        error_handling:
            strategy = "Result Pattern"
            custom_errors:
                - code = "PAYMENT_FAILED"
                  http_status = 402
                  user_message = "Payment could not be processed"
                  log_level = "error"
                  retry = true
            retry_policy:
                max_attempts = 5  # Override global
                backoff = "exponential"
```

### 14.4 Observability Best Practices

- **Use structured logging** for better parsing
- **Include correlation IDs** for request tracing
- **Sample traces** in high-traffic systems
- **Define SLOs** for critical metrics
- **Redact sensitive data** in logs
- **Set up alerts** for critical conditions

---

## 15. Testing Strategy **[NEW]**

### 15.1 testing_strategy Construct

Defines the comprehensive testing approach for the system.

```sodl
testing_strategy:
    unit_tests:
        framework = "pytest"  # or "unittest", "Jest", "JUnit"
        pattern = "AAA"  # Arrange-Act-Assert
        coverage_target = 80%
        parallel = true
        timeout = "30s"
        directories = ["tests/unit"]
        naming_convention = "test_*.py"
    
    integration_tests:
        pattern = "Given-When-Then"  # BDD style
        framework = "pytest-bdd"
        database = "TestContainer"
        directories = ["tests/integration"]
        cleanup = "after_each"
        parallel = false
    
    e2e_tests:
        framework = "Playwright"  # or "Selenium", "Cypress"
        browsers = ["chromium", "firefox", "webkit"]
        headless = true
        screenshot_on_failure = true
        video_on_failure = true
        directories = ["tests/e2e"]
    
    api_tests:
        framework = "pytest"
        base_url = "http://localhost:8000"
        directories = ["tests/api"]
        validate_schemas = true
    
    load_tests:
        framework = "locust"
        scenarios:
            - name = "NormalLoad"
              users = 100
              spawn_rate = 10
              duration = "5m"
            - name = "StressTest"
              users = 1000
              spawn_rate = 50
              duration = "10m"
    
    mocking:
        strategy = "Interface-based"
        library = "unittest.mock"  # or "Mockito", "Moq"
        auto_mock = ["external_apis", "database", "cache"]
    
    test_
        strategy = "Factories"
        library = "factory_boy"
        seed = 42
        cleanup = "transaction_rollback"
    
    ci_cd:
        run_on_commit = ["unit", "api"]
        run_on_merge = ["unit", "integration", "api", "e2e"]
        run_nightly = ["load", "security"]
        coverage_gate = 80%
        fail_on_flaky = true
```

### 15.2 Test Types

| Type | Purpose | When to Run |
|------|---------|-------------|
| `unit` | Test individual components | On every commit |
| `integration` | Test component interactions | On merge to main |
| `e2e` | Test complete user flows | On merge, nightly |
| `api` | Test API contracts | On every commit |
| `load` | Test performance under load | Nightly, before release |
| `security` | Test security vulnerabilities | Nightly, before release |

### 15.3 Module-Level Testing

Modules can define specific test requirements:

```sodl
module "PaymentModule":
    acceptance:
        test = "Processes valid payment successfully"
        test = "Handles payment failure gracefully"
        test = "Refunds payment correctly"
        test = "Validates payment data"
    
    config:
        testing:
            unit_coverage_target = 90%  # Higher than global
            integration_required = true
            security_scan = true
```

### 15.4 Testing Best Practices

- **Define acceptance criteria** for every module
- **Include positive and negative test cases**
- **Test interface boundaries**
- **Verify invariants through tests**
- **Aim for 80%+ code coverage**
- **Include integration tests**
- **Automate test execution in CI/CD**
- **Fail fast on flaky tests**

---

## 16. Security & Data **[NEW]**

### 16.1 security_patterns Construct

Defines security architecture and data protection patterns.

```sodl
security_patterns:
    authentication:
        method = "JWT"  # or "OAuth2", "SAML", "API Key", "Session"
        token_expiry = "1h"
        refresh_token = true
        refresh_token_expiry = "7d"
        multi_factor = false
        password_policy:
            min_length = 8
            require_uppercase = true
            require_lowercase = true
            require_numbers = true
            require_special = true
            max_age_days = 90
    
    authorization:
        model = "RBAC"  # or "ABAC", "PBAC", "ReBAC"
        roles = ["Admin", "User", "Guest", "Moderator"]
        permissions:
            - role = "Admin"
              permissions = ["*"]
            - role = "User"
              permissions = ["read:own", "write:own", "delete:own"]
            - role = "Guest"
              permissions = ["read:public"]
    
    data_protection:
        encryption_at_rest = "AES-256"
        encryption_in_transit = "TLS 1.3"
        key_management = "AWS KMS"  # or "Azure Key Vault", "HashiCorp Vault"
        pii_fields = ["email", "phone", "ssn", "credit_card"]
        pii_encryption = true
        data_retention_days = 365
        backup_encryption = true
    
    api_security:
        rate_limiting = true
        rate_limit_requests = 100
        rate_limit_window = "1m"
        cors_enabled = true
        cors_origins = ["https://trusted-domain.com"]
        csrf_protection = true
        input_validation = "strict"
        output_encoding = true
    
    audit:
        enabled = true
        log_authentication = true
        log_authorization = true
        log_data_access = true
        log_data_modification = true
        retention_days = 365
        immutable = true
```

### 16.2 data_migrations Construct

Defines database migration strategy.

```sodl
data_migrations:
    strategy = "Code-based"  # or "SQL-based", "ORM-based"
    tool = "Alembic"  # or "Flyway", "Liquibase", "Django Migrations"
    rollback_supported = true
    zero_downtime = true
    
    conventions:
        naming = "YYYYMMDD_HHMMSS_description"
        directory = "migrations"
        auto_generate = true
        review_required = true
    
    deployment:
        run_on_deploy = true
        backup_before_migrate = true
        test_on_staging = true
        rollback_plan_required = true
    
    data_seeding:
        enabled = true
        environments = ["development", "staging"]
        seed_data_directory = "seeds"
```

### 16.3 Module-Level Security

Modules can define specific security requirements:

```sodl
module "UserModule":
    config:
        security:
            authentication_required = true
            authorization_checks = ["role:Admin", "permission:write:users"]
            audit_log = true
            pii_handling = true
            rate_limiting:
                enabled = true
                requests = 10
                window = "1m"
```

### 16.4 Security Best Practices

- **Never store secrets in code**
- **Use parameterized queries** to prevent SQL injection
- **Validate all inputs** server-side
- **Encrypt sensitive data** at rest and in transit
- **Implement rate limiting** to prevent abuse
- **Log security events** for audit
- **Regular security scans** in CI/CD
- **Follow principle of least privilege**

---

## 17. Complete Examples

### 17.1 Example 1: Enterprise Application with Full Architecture

```sodl
system "EnterpriseApp":
    version = "1.0.0"
    
    stack:
        language = "Python 3.12"
        web = "FastAPI"
        database = "PostgreSQL"
        orm = "SQLAlchemy"
        cache = "Redis"
        ui_framework = "Material Components Web"
        testing = ["pytest", "pytest-cov", "pytest-bdd"]
        linting = ["flake8", "black", "mypy"]
    
    intent:
        primary = "Enterprise resource planning system"
        outcomes = [
            "User management with RBAC",
            "Product catalog with search",
            "Order processing with payment",
            "Reporting and analytics",
            "Responsive web interface"
        ]
        out_of_scope = [
            "Mobile applications",
            "Third-party integrations",
            "Legacy data migration"
        ]
    
    architecture:
        style = "Clean Architecture"
        dependency_rule = "Dependencies point inward"
        layers = ["Domain", "Application", "Infrastructure", "Interface"]
        layer_descriptions:
            - layer = "Domain"
              description = "Business logic and entities"
              dependencies = []
            - layer = "Application"
              description = "Use cases and orchestration"
              dependencies = ["Domain"]
            - layer = "Infrastructure"
              description = "External services and data access"
              dependencies = ["Domain", "Application"]
            - layer = "Interface"
              description = "API, UI, and external interfaces"
              dependencies = ["Application"]
    
    design_patterns:
        - name = "Repository"
          purpose = "Abstract database access"
          scope = "global"
        - name = "CQRS"
          purpose = "Separate read and write models"
          scope = "modules: [Order, Inventory]"
        - name = "Saga"
          purpose = "Distributed transaction management"
          scope = "modules: [Payment, Order]"
        - name = "Factory"
          purpose = "Object creation abstraction"
          scope = "modules: [Payment]"
        - name = "Observer"
          purpose = "Event notification system"
          scope = "global"
    
    dependency_injection:
        container = "AutoWire"
        injection_style = "Constructor Injection"
        lifetime_rules:
            - service = "DatabaseConnection"
              scope = "Singleton"
            - service = "UserSession"
              scope = "Request"
            - service = "EmailService"
              scope = "Transient"
            - service = "CacheService"
              scope = "Singleton"
            - service = "Logger"
              scope = "Singleton"
    
    error_handling:
        strategy = "Result Pattern"
        error_codes:
            - code = "USER_NOT_FOUND"
              http_status = 404
              user_message = "User does not exist"
              log_level = "warning"
            - code = "VALIDATION_ERROR"
              http_status = 422
              user_message = "Invalid input data"
              log_level = "info"
            - code = "DATABASE_ERROR"
              http_status = 500
              user_message = "Internal server error"
              log_level = "error"
        retry_policy:
            max_attempts = 3
            backoff = "exponential"
            initial_delay = "1s"
            max_delay = "30s"
            timeout = "30s"
        global_handler = "MiddlewareErrorHandler"
    
    observability:
        logging:
            format = "JSON"
            level = "INFO"
            correlation_id = "required"
            include_timestamp = true
            include_source = true
            output = ["console", "file", "elasticsearch"]
            retention_days = 30
        tracing:
            enabled = true
            provider = "OpenTelemetry"
            sampling_rate = 0.1
            propagation = ["traceparent", "baggage"]
            export_to = ["jaeger", "prometheus"]
        metrics:
            enabled = true
            provider = "Prometheus"
            default_buckets = [0.1, 0.5, 1.0, 5.0, 10.0]
        health_checks:
            enabled = true
            endpoint = "/health"
            checks = ["database", "cache", "external_apis"]
    
    testing_strategy:
        unit_tests:
            framework = "pytest"
            pattern = "AAA"
            coverage_target = 80%
            parallel = true
            timeout = "30s"
        integration_tests:
            pattern = "Given-When-Then"
            framework = "pytest-bdd"
            database = "TestContainer"
        e2e_tests:
            framework = "Playwright"
            browsers = ["chromium", "firefox"]
            headless = true
        ci_cd:
            run_on_commit = ["unit", "api"]
            run_on_merge = ["unit", "integration", "api", "e2e"]
            coverage_gate = 80%
    
    security_patterns:
        authentication:
            method = "JWT"
            token_expiry = "1h"
            refresh_token = true
            password_policy:
                min_length = 8
                require_uppercase = true
                require_lowercase = true
                require_numbers = true
                require_special = true
        authorization:
            model = "RBAC"
            roles = ["Admin", "User", "Guest", "Moderator"]
        data_protection:
            encryption_at_rest = "AES-256"
            encryption_in_transit = "TLS 1.3"
            pii_fields = ["email", "phone", "ssn", "credit_card"]
        api_security:
            rate_limiting = true
            rate_limit_requests = 100
            rate_limit_window = "1m"
            cors_enabled = true
            csrf_protection = true
    
    data_migrations:
        strategy = "Code-based"
        tool = "Alembic"
        rollback_supported = true
        zero_downtime = true
    
    ui:
        theme = "MaterialWeb"
        rules:
            - name: "AutoFillKnownFields"
              conditions: ["field.type == 'text' && field.name in ['email', 'name']"]
              actions: ["prefillFromUserProfile(field.name)"]
            - name: "ValidateOnBlur"
              conditions: ["field.validation != null"]
              actions: ["validateField(field.name, field.validation)"]
            - name: "ShowLoadingOnAsync"
              conditions: ["action.type == 'async'"]
              actions: ["showLoadingDuring(action.name)"]
            - name: "AccessibilityCompliance"
              conditions: ["component.rendered == true"]
              actions: ["addAriaLabels(component)", "ensureKeyboardNavigation(component)"]
        components:
            - name: "StandardForm"
              template:
                  component: "form"
                  fields: "{{fields}}"
            - name: "DataTable"
              template:
                  component: "table"
                  columns: "{{columns}}"
            - name: "ConfirmationModal"
              template:
                  component: "modal"
                  title: "{{title}}"
                  content: "{{content}}"
        bindings:
            - endpoint_method: "GET"
              control_type: "DataTable"
            - endpoint_method: "POST"
              control_type: "StandardForm"
            - endpoint_method: "PUT"
              control_type: "StandardForm"
            - endpoint_method: "DELETE"
              control_type: "ConfirmationModal"
        pages:
            - name: "UsersPage"
              components:
                  - type: "DataTable"
                    params:
                        endpoint: "/api/users"
                  - type: "StandardForm"
                    params:
                        endpoint: "/api/users"
                        mode: "create"
    
    policy Security:
        rule = "No secrets in repository"
        severity = "critical"
        rule = "Validate all user input"
        severity = "high"
        rule = "Use parameterized queries"
        severity = "critical"
    
    policy Performance:
        rule = "Cache frequently accessed data"
        severity = "medium"
        rule = "Use database indexes"
        severity = "high"
    
    policy CodeQuality:
        rule = "Test coverage above 80%"
        severity = "high"
        rule = "No code duplication"
        severity = "medium"
    
    interface UserRepository:
        doc = "User data access layer"
        method create(user: UserInput) -> User
        method get_by_id(id: UUID) -> Optional[User]
        method get_by_email(email: str) -> Optional[User]
        method get_all(page: int, page_size: int) -> PagedUsers
        method update(id: UUID, updates: UserUpdate) -> User
        method delete(id: UUID) -> bool
        invariants:
            invariant = "Email addresses are unique"
            invariant = "User IDs are UUIDs"
            invariant = "Passwords are never returned in responses"
    
    interface ProductRepository:
        doc = "Product data access layer"
        method find_all(filters: ProductFilters, page: int) -> PagedProducts
        method find_by_id(id: UUID) -> Optional[Product]
        method search(query: str, page: int) -> PagedProducts
        method create(product: ProductInput) -> Product
        method update(id: UUID, updates: ProductUpdate) -> Product
        invariants:
            invariant = "SKUs are unique across all products"
            invariant = "Prices are positive decimals"
    
    module UserAPI:
        owns = ["User CRUD API"]
        requires = [UserRepository]
        api:
            endpoint "GET/api/users" -> List[User]
            endpoint "POST/api/users" -> User
            endpoint "PUT/api/users/{id}" -> User
            endpoint "DELETE/api/users/{id}" -> Empty
        ui:
            pages:
                - name: "UsersPage"
        invariants:
            invariant = "Email addresses are unique"
            invariant = "User IDs are UUIDs"
            invariant = "Passwords are hashed with bcrypt"
        acceptance:
            test = "creates user via POST with valid payload"
            test = "returns 404 for non-existent user ID"
            test = "updates user via PUT"
            test = "deletes user via DELETE"
            test = "validates email format"
            test = "hashes passwords before storage"
        artifacts = ["app/api/users.py"]
        design_patterns:
            - name = "Repository"
              purpose = "Abstract data access"
    
    module UserUI:
        owns = ["User Management Interface"]
        requires = ["UserAPI"]
        ui:
            pages:
                - name: "UsersPage"
        invariants:
            invariant = "Forms validate client and server-side"
            invariant = "Material Design components properly initialized"
            invariant = "Accessibility standards met"
        acceptance:
            test = "renders user list correctly"
            test = "creates user via form submission"
            test = "edits user via form submission"
            test = "deletes user with confirmation"
            test = "shows loading state during operations"
            test = "displays user-friendly error messages"
            test = "keyboard navigation works"
        artifacts = ["app/ui/users.py", "app/templates/users.html"]
    
    module ProductAPI:
        owns = ["Product CRUD API"]
        requires = [ProductRepository]
        api:
            endpoint "GET/api/products" -> PagedProducts
            endpoint "POST/api/products" -> Product
            endpoint "PUT/api/products/{id}" -> Product
            endpoint "DELETE/api/products/{id}" -> Empty
            endpoint "GET/api/products/search" -> PagedProducts
        invariants:
            invariant = "SKUs are unique"
            invariant = "Prices are validated"
            invariant = "Cache results for 5 minutes"
        acceptance:
            test = "lists products with pagination"
            test = "searches products by query"
            test = "creates product with valid SKU"
            test = "returns 404 for non-existent product"
        artifacts = ["app/api/products.py"]
        design_patterns:
            - name = "CQRS"
              purpose = "Separate read/write models"
    
    module PostgresUserRepository:
        implements = [UserRepository]
        exports = [UserRepository]
        config:
            connection_pool_size = 20
        invariants:
            invariant = "Use prepared statements"
            invariant = "Encrypt PII fields"
        artifacts = ["app/repositories/users.py"]
        design_patterns:
            - name = "Repository"
              purpose = "Abstract data access"
    
    module PostgresProductRepository:
        implements = [ProductRepository]
        exports = [ProductRepository]
        config:
            connection_pool_size = 20
            search_index = "gin"
        invariants:
            invariant = "Use prepared statements"
            invariant = "Implement full-text search"
        artifacts = ["app/repositories/products.py"]
    
    pipeline "Production":
        step Design:
            output = design
            require = "Architecture diagram and data model"
            gate = "Architecture approved"
        
        step ImplementModels:
            modules = ["StorageModels", "APISchemas"]
            output = code
            require = "Use Pydantic for validation"
            gate = "Models compile without errors"
            depends_on = ["Design"]
        
        step ImplementRepositories:
            modules = ["PostgresUserRepository", "PostgresProductRepository"]
            output = code
            require = "Follow repository pattern"
            gate = "Repository tests pass"
            depends_on = ["ImplementModels"]
        
        step ImplementAPI:
            modules = ["UserAPI", "ProductAPI"]
            output = code
            require = "RESTful conventions"
            gate = "API tests pass"
            depends_on = ["ImplementRepositories"]
        
        step ImplementUI:
            modules = ["UserUI"]
            output = ui
            require = "Material Design components"
            gate = "UI tests pass"
            depends_on = ["ImplementAPI"]
        
        step ValidateArchitecture:
            output = architecture
            require = "Verify Clean Architecture patterns"
            gate = "No dependency violations"
            depends_on = ["ImplementAPI"]
        
        step GenerateTests:
            output = tests
            require = "Generate tests per testing_strategy"
            gate = "Test scaffolding complete"
            depends_on = ["ImplementAPI"]
        
        step FinalReview:
            output = diff
            require = "All acceptance criteria met"
            gate = "Full integration test suite passes"
            depends_on = ["ImplementUI", "ValidateArchitecture", "GenerateTests"]
```

### 17.2 Example 2: Microservices with Event-Driven Architecture

```sodl
system "MicroservicesApp":
    version = "1.0.0"
    
    stack:
        language = "Python 3.12"
        web = "FastAPI"
        database = "PostgreSQL"
        message_broker = "RabbitMQ"
        cache = "Redis"
    
    architecture:
        style = "Microservices"
        communication = "Event-Driven"
        services = ["UserService", "OrderService", "PaymentService", "NotificationService"]
        service_discovery = "Consul"
        api_gateway = "Kong"
    
    design_patterns:
        - name = "Saga"
          purpose = "Distributed transaction management"
          scope = "global"
        - name = "Event Sourcing"
          purpose = "Event-based state management"
          scope = "modules: [Order, Payment]"
        - name = "CQRS"
          purpose = "Separate read and write models"
          scope = "modules: [Order, Inventory]"
        - name = "Circuit Breaker"
          purpose = "Fault tolerance"
          scope = "global"
    
    dependency_injection:
        container = "AutoWire"
        injection_style = "Constructor Injection"
        lifetime_rules:
            - service = "MessageBus"
              scope = "Singleton"
            - service = "DatabaseConnection"
              scope = "Singleton"
    
    error_handling:
        strategy = "Result Pattern"
        retry_policy:
            max_attempts = 3
            backoff = "exponential"
        circuit_breaker:
            enabled = true
            failure_threshold = 5
            recovery_timeout = "30s"
    
    observability:
        logging:
            format = "JSON"
            correlation_id = "required"
        tracing:
            enabled = true
            provider = "OpenTelemetry"
            sampling_rate = 0.1
        metrics:
            enabled = true
            provider = "Prometheus"
    
    testing_strategy:
        unit_tests:
            framework = "pytest"
            coverage_target = 85%
        integration_tests:
            pattern = "Given-When-Then"
            database = "TestContainer"
        contract_tests:
            framework = "Pact"
            enabled = true
        ci_cd:
            run_on_commit = ["unit", "contract"]
            run_on_merge = ["unit", "integration", "contract", "e2e"]
    
    security_patterns:
        authentication:
            method = "JWT"
            token_expiry = "1h"
        authorization:
            model = "RBAC"
        data_protection:
            encryption_at_rest = "AES-256"
            encryption_in_transit = "TLS 1.3"
    
    module OrderService:
        owns = ["Order processing"]
        design_patterns:
            - name = "Saga"
              purpose = "Coordinate order fulfillment"
            - name = "Event Sourcing"
              purpose = "Track order state changes"
        api:
            endpoint "POST/api/orders" -> Order
            endpoint "GET/api/orders/{id}" -> Order
        invariants:
            invariant = "Orders are idempotent"
            invariant = "State changes are logged as events"
    
    module PaymentService:
        owns = ["Payment processing"]
        requires = ["OrderService"]
        design_patterns:
            - name = "Saga"
              purpose = "Coordinate with order service"
            - name = "Circuit Breaker"
              purpose = "Handle payment gateway failures"
        api:
            endpoint "POST/api/payments" -> Payment
            endpoint "GET/api/payments/{id}" -> Payment
        invariants:
            invariant = "Payments are idempotent"
            invariant = "Failed payments trigger compensation"
    
    pipeline "Microservices":
        step Design:
            output = design
            require = "Service boundaries and event contracts"
        
        step ImplementServices:
            modules = ["OrderService", "PaymentService"]
            output = code
            gate = "Service tests pass"
        
        step ImplementEvents:
            output = code
            require = "Event schemas and handlers"
            gate = "Event tests pass"
            depends_on = ["ImplementServices"]
        
        step ContractTests:
            output = tests
            require = "Pact contract tests"
            gate = "Contracts verified"
            depends_on = ["ImplementServices"]
        
        step Deploy:
            output = diff
            require = "All tests pass"
            depends_on = ["ImplementEvents", "ContractTests"]
```

---

## 18. Design Principles

### 18.1 Core Principles

| Principle | Description | Application |
|-----------|-------------|-------------|
| Explicit over implicit | State everything clearly, avoid assumptions | Document all requirements |
| Constraints over suggestions | Use enforceable rules, not soft guidelines | Use policies with severity |
| Architecture before code | Define structure before implementation | Design modules and interfaces first |
| Deterministic prompts | Same spec always produces same instructions | Avoid ambiguous language |
| Developer-controlled AI | Human maintains control over generation process | Use gates and reviews |
| UI/API Symmetry | UI components should directly reflect API contracts | Use automatic bindings |
| Full-stack integration | Backend and frontend specifications in one language | Single SODL file |
| **Pattern-driven development** | **Use explicit architectural patterns** | **Define architecture and patterns** **[NEW]** |
| **Quality by design** | **Build quality into specification** | **Define testing and observability** **[NEW]** |

### 18.2 Specification Quality

- **Completeness:** All requirements are documented
- **Consistency:** No conflicting specifications
- **Clarity:** Unambiguous language throughout
- **Verifiability:** All claims can be tested
- **Maintainability:** Easy to update and extend
- **Reusability:** Templates and patterns are reusable

### 18.3 AI Agent Guidelines

When generating instructions for AI coding agents:

- **Be specific:** Provide exact requirements
- **Provide context:** Include relevant background information
- **Set constraints:** Define what is not allowed
- **Define success:** Specify acceptance criteria
- **Include examples:** Show expected patterns
- **Reference patterns:** Point to architectural patterns
- **Define quality gates:** Specify testing requirements

---

## 19. Best Practices

### 19.1 Module Organization

- Keep modules focused on single responsibility
- Use interfaces to define contracts between modules
- Clearly specify dependencies with `requires`
- Document ownership boundaries with `owns`
- Limit module size (max 500 lines of generated code)
- Group related functionality together
- **Specify design patterns** for each module **[NEW]**

### 19.2 Interface Design

- Design interfaces before implementing modules
- Keep interfaces stable; change implementations instead
- Use semantic type annotations
- Document invariants for interface contracts
- Minimize interface surface area
- Version interfaces when breaking changes are needed

### 19.3 UI/UX Design

- Define `ui_theme` for consistent look and feel across systems
- Use `bindings` to automate CRUD UI generation
- Keep UI logic separate from business logic in modules
- Define `ux_rules` for consistent interaction patterns (validation, loading states)
- Test UI on multiple screen sizes
- Ensure accessibility compliance (WCAG 2.1 AA)
- Document component usage patterns

### 19.4 Pipeline Structure

- Order steps by logical dependency
- Use gates to enforce quality at each step
- Make steps atomic and independently verifiable
- Specify clear output types for each step (`code`, `ui`, `tests`)
- Include review steps before deployment
- Document step dependencies explicitly
- **Include architecture validation step** **[NEW]**
- **Include test generation step** **[NEW]**

### 19.5 Policy Definition

- Use appropriate severity levels
- Make policies specific and measurable
- Group related rules into named policies
- Prioritize critical security and data integrity rules
- Review policies regularly
- Document policy rationale

### 19.6 Testing Strategy

- Define acceptance criteria for every module
- Include positive and negative test cases
- Test interface boundaries
- Verify invariants through tests
- Verify UI bindings match API contracts
- Aim for 80%+ code coverage
- Include integration tests
- **Automate test execution in CI/CD** **[NEW]**
- **Include contract tests for microservices** **[NEW]**

### 19.7 API-UI Binding

- Always define bindings for CRUD operations
- Use consistent control types for similar endpoints
- Document default parameters for each binding
- Test binding correctness in acceptance criteria
- Handle error states gracefully
- Provide loading feedback for async operations

### 19.8 Template Usage

- Create templates for common patterns
- Document template requirements
- Test templates independently
- Version templates for compatibility
- Use template inheritance wisely
- Avoid deep inheritance chains (max 3 levels)
- **Include architecture patterns in templates** **[NEW]**

### 19.9 Architecture & Patterns

- **Define architecture style explicitly** **[NEW]**
- **Document layer dependencies** **[NEW]**
- **Use design patterns consistently** **[NEW]**
- **Validate architecture in pipeline** **[NEW]**
- **Reference pattern libraries** **[NEW]**

### 19.10 Dependency Injection

- **Use constructor injection** **[NEW]**
- **Define lifetime scopes clearly** **[NEW]**
- **Register services in composition root** **[NEW]**
- **Keep services stateless when possible** **[NEW]**

### 19.11 Error Handling & Observability

- **Use structured logging** **[NEW]**
- **Include correlation IDs** **[NEW]**
- **Define retry policies** **[NEW]**
- **Set up alerts for critical conditions** **[NEW]**
- **Redact sensitive data in logs** **[NEW]**

### 19.12 Security

- **Never store secrets in code** **[NEW]**
- **Use parameterized queries** **[NEW]**
- **Validate all inputs server-side** **[NEW]**
- **Encrypt sensitive data** **[NEW]**
- **Implement rate limiting** **[NEW]**
- **Log security events** **[NEW]**

---

## 20. Compiler Output

A SODL compiler produces structured output for AI agents:

```
.sodl/
├── global.md              # System-level context
├── ui/                    # UI-specific instructions
│   ├── theme.md
│   ├── components.md
│   ├── bindings.md
│   └── pages.md
├── modules/               # Module-specific instructions
│   ├── ImageAPI.md
│   ├── StorageLocal.md
│   └── ...
├── steps/                 # Step-by-step generation instructions
│   ├── Design.md
│   ├── ImplementModels.md
│   ├── ImplementAPI.md
│   └── ...
├── architecture/          # Architecture pattern instructions **[NEW]**
│   ├── layers.md
│   ├── patterns.md
│   └── validation.md
├── testing/               # Test generation instructions **[NEW]**
│   ├── unit.md
│   ├── integration.md
│   └── e2e.md
├── observability/         # Observability configuration **[NEW]**
│   ├── logging.md
│   ├── tracing.md
│   └── metrics.md
└── manifest.json          # Metadata and structure
```

These files are consumed by AI coding agents (Cursor, Claude, GPT) to generate application code.

---

## 21. Non-Goals

SODL is **not**:

| Non-Goal | Explanation |
|----------|-------------|
| A programming language | SODL does not execute; it generates instructions for AI agents |
| A UML replacement | SODL is text-based, not visual modeling |
| A test framework | SODL defines tests but does not run them |
| A code generator | SODL generates instructions, not application code directly |
| A runtime system | SODL specifications are not executed at runtime |
| A visual UI designer | SODL defines structure, not pixel-perfect layout |
| A database schema tool | SODL describes data models but doesn't create databases |
| A deployment tool | SODL can specify deployment but doesn't execute it |
| **A pattern enforcer** | **SODL defines patterns but AI implements them** **[NEW]** |
| **A security scanner** | **SODL defines security rules but doesn't scan code** **[NEW]** |

---

## 22. Language Reference

### 22.1 Keywords

| Keyword | Purpose | Scope | Example |
|---------|---------|-------|---------|
| `system` | Define a concrete system | Top-level | `system "MyApp":` |
| `template` | Define a reusable template | Top-level | `template "BaseWeb":` |
| `ui_theme` | Define a reusable UI component library | Top-level | `ui_theme "Material":` |
| **`pattern_library`** | **Define reusable pattern definitions** | **Top-level** | **`pattern_library "Standard":`** **[NEW]** |
| `extends` | Inherit from template | System | `system "App" extends "Base":` |
| `interface` | Define functionality contract | Top-level | `interface Store:` |
| `implements` | Implement an interface | Module | `implements=[Store]` |
| `exports` | Provide interface to others | Module | `exports=[Store]` |
| `requires` | Depend on interface | Module | `requires=[Store]` |
| `module` | Define generation unit | System | `module API:` |
| `policy` | Define rules and constraints | System/Template | `policy Security:` |
| `pipeline` | Define generation process | System | `pipeline "Dev":` |
| `step` | Define generation phase | Pipeline | `step Implement:` |
| `override` | Replace value | System | `override stack.language = "3.13"` |
| `append` | Add to list | System | `append stack.testing += "pytest"` |
| `remove` | Remove from list | System | `remove stack.testing -= "unittest"` |
| `replace` | Replace block | System | `replace block ui:` |
| **`architecture`** | **Define architecture style** | **System** | **`architecture:`** **[NEW]** |
| **`design_patterns`** | **Define design patterns** | **System/Module** | **`design_patterns:`** **[NEW]** |
| **`dependency_injection`** | **Configure DI container** | **System** | **`dependency_injection:`** **[NEW]** |
| **`error_handling`** | **Define error strategy** | **System** | **`error_handling:`** **[NEW]** |
| **`observability`** | **Configure logging/tracing** | **System** | **`observability:`** **[NEW]** |
| **`testing_strategy`** | **Define testing approach** | **System** | **`testing_strategy:`** **[NEW]** |
| **`security_patterns`** | **Define security architecture** | **System** | **`security_patterns:`** **[NEW]** |
| **`data_migrations`** | **Define migration strategy** | **System** | **`data_migrations:`** **[NEW]** |

### 22.2 Sections

| Section | Purpose | Parent | Example |
|---------|---------|--------|---------|
| `stack` | Technology stack definition | System/Template | `stack: language = "Python"` |
| `intent` | Goals and scope | System | `intent: primary = "Build app"` |
| `api` | API definition (endpoints, models) | System/Module | `endpoint "GET/api/todos"` |
| `ui` | UI definition (rules, components, bindings, pages) | System/Template/Module | `ui: theme = "Material"` |
| `owns` | Ownership declaration | Module | `owns = ["Auth"]` |
| `invariants` | Constraints that must hold | Interface/Module | `invariant = "IDs unique"` |
| `acceptance` | Definition of done | Module | `test = "creates todo"` |
| `artifacts` | File scope | Module | `artifacts = ["app.py"]` |
| `config` | Configuration values | Module | `config: timeout = 30` |
| `rules` | UX rules | UI | `rules: - name: "Validate"` |
| `components` | UI component definitions | UI/UI Theme | `components: - name: "Form"` |
| `bindings` | API-UI mappings | UI/UI Theme | `bindings: - method: "GET"` |
| `pages` | UI page definitions | UI | `pages: - name: "Home"` |
| **`layers`** | **Architecture layer definitions** | **Architecture** | **`layers = ["Domain", ...]`** **[NEW]** |
| **`lifetime_rules`** | **DI lifetime scopes** | **Dependency Injection** | **`lifetime_rules:`** **[NEW]** |
| **`error_codes`** | **Error code definitions** | **Error Handling** | **`error_codes:`** **[NEW]** |
| **`logging`** | **Logging configuration** | **Observability** | **`logging:`** **[NEW]** |
| **`unit_tests`** | **Unit test configuration** | **Testing Strategy** | **`unit_tests:`** **[NEW]** |

### 22.3 Severity Levels

| Severity | Meaning | Enforcement | Color Code |
|----------|---------|-------------|------------|
| `critical` | Must not violate | Hard constraint, blocks generation | 🔴 Red |
| `high` | Must follow | Required constraint | 🟠 Orange |
| `medium` | Should follow | Strong recommendation | 🟡 Yellow |
| `low` | May follow | Suggestion | 🟢 Green |

### 22.4 Output Types

| Type | Description | Use Case |
|------|-------------|----------|
| `design` | Architecture and planning | Initial design phase |
| `code` | Application code | Implementation phase |
| `ui` | User Interface code | UI generation phase |
| `tests` | Test code | Testing phase |
| `diff` | Code changes | Review phase |
| `docs` | Documentation | Documentation phase |
| **`architecture`** | **Architecture validation** | **Architecture review** **[NEW]** |

### 22.5 UI Component Types

| Component | Purpose | Default Binding | Template Variables |
|-----------|---------|-----------------|-------------------|
| `StandardForm` | Data entry forms | POST, PUT | `{{fields}}`, `{{submitLabel}}` |
| `DataTable` | List/display data | GET | `{{columns}}`, `{{endpoint}}` |
| `ConfirmationModal` | Confirm actions | DELETE | `{{title}}`, `{{content}}` |
| `NavigationMenu` | Primary navigation | N/A | `{{menuItems}}` |
| `SearchBar` | Search input | GET (search) | `{{placeholder}}`, `{{endpoint}}` |

### 22.6 UX Rules

| Rule | Trigger | Action | Default Severity |
|------|---------|--------|------------------|
| `AutoFillKnownFields` | Known field names | Pre-fill from profile | medium |
| `ValidateOnBlur` | Field validation | Validate on blur | high |
| `EnableButtonOnDependencies` | Button dependencies | Enable when filled | medium |
| `ShowLoadingOnAsync` | Async operations | Show spinner | medium |
| `UserFriendlyErrors` | Error results | Friendly messages | high |
| `ResponsiveLayout` | Viewport < 768px | Mobile layout | medium |
| `AccessibilityCompliance` | Component rendered | ARIA labels, keyboard nav | high |

### 22.7 Data Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text value | `"Hello World"` |
| `int` | Integer value | `42` |
| `bool` | Boolean value | `true`, `false` |
| `list` | Array of values | `["a", "b", "c"]` |
| `UUID` | Universally unique identifier | `550e8400-e29b-41d4-a716-446655440000` |
| `datetime` | Date and time | `2024-01-15T10:30:00Z` |
| `Optional[T]` | Nullable type | `Optional[str]` |
| `List[T]` | List of type T | `List[User]` |

---

## 23. Version History

### v0.5 (Enhanced Draft) - Current
- **Added `architecture` construct** for explicit architecture definition
- **Added `design_patterns` construct** for pattern-driven development
- **Added `pattern_library` construct** for reusable patterns
- **Added `dependency_injection` construct** for DI configuration
- **Added `error_handling` construct** for error strategy
- **Added `observability` construct** for logging, tracing, metrics
- **Added `testing_strategy` construct** for comprehensive testing
- **Added `security_patterns` construct** for security architecture
- **Added `data_migrations` construct** for migration strategy
- **Enhanced pipeline** with architecture validation and test generation steps
- **Enhanced compiler output** with architecture, testing, observability directories
- **Updated best practices** with new sections for patterns, DI, error handling, security

### v0.4 - Previous Stable
- Full-stack support with UI/UX extension
- Automatic API-UI binding
- UI theme and component definitions
- Enhanced templates with UI inheritance
- UI policies for accessibility and performance

### v0.3 - Legacy
- Stable syntax for production use
- Complete interface system
- Pipeline and step definitions
- Template inheritance
- Policy severity levels

---

## 24. Appendix A: Quick Reference

### A.1 Syntax Cheat Sheet

```sodl
# System Definition
system "Name":
    version = "1.0.0"
    stack:
        language = "Python 3.12"
    intent:
        primary = "Goal"
    architecture:
        style = "Clean Architecture"
        layers = ["Domain", "Application", "Infrastructure"]
    design_patterns:
        - name = "Repository"
          scope = "global"
    dependency_injection:
        container = "AutoWire"
        injection_style = "Constructor Injection"
    error_handling:
        strategy = "Result Pattern"
    observability:
        logging:
            format = "JSON"
            level = "INFO"
    testing_strategy:
        unit_tests:
            framework = "pytest"
            coverage_target = 80%

# Template with Inheritance
template "Base":
    stack:
        language = "Python 3.12"
    architecture:
        style = "Clean Architecture"

system "App" extends "Base":
    override stack.language = "Python 3.13"

# Interface
interface Store:
    method create(Input) -> Output
    invariants:
        invariant = "Constraint"

# Module
module API:
    requires = [Store]
    api:
        endpoint "GET/api/items" -> List[Item]
    acceptance:
        test = "works correctly"
    design_patterns:
        - name = "Repository"
          purpose = "Abstract data access"

# UI Section
ui:
    theme = "MaterialWeb"
    rules:
        - name: "ValidateOnBlur"
          actions: ["validate()"]
    components:
        - name: "StandardForm"
          template:
              component: "form"
    bindings:
        - endpoint_method: "GET"
          control_type: "DataTable"
    pages:
        - name: "HomePage"
          components:
              - type: "DataTable"

# Pipeline
pipeline "Dev":
    step Implement:
        output = code
        gate = "Tests pass"
    step ValidateArchitecture:
        output = architecture
        gate = "Patterns verified"
    step GenerateTests:
        output = tests
        gate = "Tests generated"
```

### A.2 Common Patterns

#### CRUD Module Pattern

```sodl
module EntityAPI:
    api:
        endpoint "GET/api/entities" -> List[Entity]
        endpoint "POST/api/entities" -> Entity
        endpoint "PUT/api/entities/{id}" -> Entity
        endpoint "DELETE/api/entities/{id}" -> Empty
    ui:
        pages:
            - name: "EntitiesPage"
    design_patterns:
        - name = "Repository"
          purpose = "Abstract data access"
```

#### Repository Pattern

```sodl
interface EntityRepository:
    method find_all() -> List[Entity]
    method find_by_id(id: UUID) -> Optional[Entity]
    method create(entity: EntityInput) -> Entity
    method update(id: UUID, updates: EntityUpdate) -> Entity
    method delete(id: UUID) -> bool

module PostgresEntityRepository:
    implements = [EntityRepository]
    exports = [EntityRepository]
    design_patterns:
        - name = "Repository"
          purpose = "Abstract data access"
```

#### UI Binding Pattern

```sodl
ui:
    bindings:
        - endpoint_method: "GET"
          control_type: "DataTable"
        - endpoint_method: "POST"
          control_type: "StandardForm"
        - endpoint_method: "PUT"
          control_type: "StandardForm"
        - endpoint_method: "DELETE"
          control_type: "ConfirmationModal"
```

#### Architecture Pattern

```sodl
architecture:
    style = "Clean Architecture"
    dependency_rule = "Dependencies point inward"
    layers = ["Domain", "Application", "Infrastructure", "Interface"]
    layer_descriptions:
        - layer = "Domain"
          description = "Business logic and entities"
          dependencies = []
        - layer = "Application"
          description = "Use cases and orchestration"
          dependencies = ["Domain"]
```

#### Dependency Injection Pattern

```sodl
dependency_injection:
    container = "AutoWire"
    injection_style = "Constructor Injection"
    lifetime_rules:
        - service = "DatabaseConnection"
          scope = "Singleton"
        - service = "UserSession"
          scope = "Request"
        - service = "EmailService"
          scope = "Transient"
```

#### Testing Strategy Pattern

```sodl
testing_strategy:
    unit_tests:
        framework = "pytest"
        pattern = "AAA"
        coverage_target = 80%
    integration_tests:
        pattern = "Given-When-Then"
        framework = "pytest-bdd"
    e2e_tests:
        framework = "Playwright"
        browsers = ["chromium", "firefox"]
    ci_cd:
        run_on_commit = ["unit", "api"]
        run_on_merge = ["unit", "integration", "api", "e2e"]
        coverage_gate = 80%
```

### A.3 Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid indentation | Mixed tabs and spaces | Use consistent indentation |
| Unknown keyword | Typo in keyword | Check keyword spelling |
| Circular dependency | Module A requires B, B requires A | Refactor module structure |
| Missing interface | Module requires undefined interface | Define or import interface |
| Invalid binding | Endpoint method not supported | Use GET, POST, PUT, or DELETE |
| Template not found | Extends references undefined template | Define template first |
| **Invalid architecture style** | **Unknown architecture style** | **Use Clean, Hexagonal, MVC, etc.** **[NEW]** |
| **Invalid pattern** | **Unknown design pattern** | **Use Repository, CQRS, Saga, etc.** **[NEW]** |
| **Invalid DI scope** | **Unknown lifetime scope** | **Use Singleton, Request, Transient** **[NEW]** |

---


**SODL: Turning prompt engineering into specification engineering.**  
**SODL v0.5: Full-stack AI-driven development with architecture patterns, quality assurance, and production readiness.**

---

*End of Document*