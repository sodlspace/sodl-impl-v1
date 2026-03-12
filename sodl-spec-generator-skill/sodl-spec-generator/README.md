# SODL Specification Generator Skill

Expert skill for generating production-ready SODL (Specification-Oriented Development Language) specifications.

## What This Skill Provides

This skill transforms Claude into an expert SODL architect capable of generating comprehensive, production-ready specifications for:

- **Full-stack applications** - Backend, frontend, API, and UI binding
- **Microservices** - CQRS, event-driven, hexagonal architecture
- **REST APIs** - Authentication, authorization, CRUD operations
- **E-commerce platforms** - Product catalog, shopping cart, order management
- **Enterprise systems** - Clean architecture, dependency injection, observability

## Installation

### Option 1: Copy to Skills Directory

Copy the `sodl-spec-generator-skill` directory to your Qwen skills directory:

**Windows:**
```bash
xcopy /E /I sodl-spec-generator-skill %USERPROFILE%\.qwen\skills\sodl-spec-generator
```

**macOS/Linux:**
```bash
cp -r sodl-spec-generator-skill ~/.qwen/skills/sodl-spec-generator
```

### Option 2: Package as .skill File

```bash
# Package the skill
python scripts/package_skill.py sodl-spec-generator-skill

# This creates sodl-spec-generator.skill file
```

## Usage

Once installed, the skill will automatically trigger when you ask about:

- Creating SODL specifications
- Generating system architecture in SODL
- Defining APIs, modules, or interfaces in SODL
- Creating production-ready specifications with error handling, observability, testing
- Converting requirements to SODL format

### Example Prompts

```
Create a SODL specification for a task management API with JWT authentication
```

```
Generate a production-ready SODL file for an e-commerce microservice with CQRS
```

```
Convert this requirements document into a SODL specification
```

```
Create a SODL template for a CRUD application with Clean Architecture
```

## Skill Structure

```
sodl-spec-generator/
├── SKILL.md                          # Main skill instructions
├── references/
│   └── sodl-quick-reference.md       # SODL syntax quick reference
├── scripts/
│   └── sodl_validator.py             # Validation and generation utilities
└── assets/
    ├── examples/
    │   └── ecommerce-platform.sodl   # Example SODL specification
    └── templates/                     # SODL templates (generated on demand)
```

## Features

### 1. Production-Ready Specifications

Every generated SODL includes:

- ✅ **Architecture patterns** - Clean Architecture, Hexagonal, CQRS, Event-Driven
- ✅ **Dependency injection** - Container configuration and lifetime rules
- ✅ **Error handling** - Result pattern, retry policies, circuit breakers
- ✅ **Observability** - Logging, tracing, metrics configuration
- ✅ **Testing strategy** - Unit, integration, E2E, load testing
- ✅ **Security patterns** - Authentication, authorization, data protection

### 2. Template Generation

Generate templates for common patterns:

```bash
python scripts/sodl_validator.py generate crud output.sodl
python scripts/sodl_validator.py generate microservice output.sodl
python scripts/sodl_validator.py generate rest-api output.sodl
python scripts/sodl_validator.py generate event-driven output.sodl
python scripts/sodl_validator.py generate fullstack output.sodl
```

### 3. Validation

Validate SODL specifications:

```bash
# Syntax validation
python scripts/sodl_validator.py validate spec.sodl

# Production readiness check
python scripts/sodl_validator.py check-production spec.sodl
```

### 4. Quality Criteria

Generated specifications follow strict quality criteria:

**Completeness:**
- System version, stack, and intent defined
- Architecture style and layers specified
- All modules have requires, owns, and artifacts
- Interfaces define all necessary methods
- API endpoints fully specified
- Pipeline with generation steps and gates

**Architecture Quality:**
- Appropriate architecture style selected
- Layers properly separated
- Design patterns appropriately applied
- Dependencies are acyclic
- DI enables testability

**Production Readiness:**
- Error handling strategy defined
- Observability configured
- Testing strategy comprehensive
- Security patterns addressed
- Retry policies specified

## SODL Compiler Integration

For validation, install the SODL compiler:

```bash
# From the sodl-impl-v1 directory
pip install -e .

# Or using uv
uv sync
```

Then use the compiler to validate generated specifications:

```bash
sodlcompiler generated-spec.sodl
```

## Example Output

A generated SODL specification includes:

```sodl
system "MyApplication":
  version = "1.0.0"
  
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    database = "PostgreSQL"
  
  architecture:
    style = "Clean Architecture"
    layers = ["Domain", "Application", "Infrastructure", "Interface"]
  
  design_patterns:
    - name = "Repository"
      scope = "global"
  
  error_handling:
    strategy = "Result Pattern"
    retry_policy:
      max_attempts = 3
  
  observability:
    logging:
      format = "JSON"
      level = "INFO"
    tracing:
      enabled = true
  
  module MyModule:
    requires = [Interface1]
    owns = ["Responsibility"]
    artifacts = ["app/module.py"]
  
  pipeline "Development":
    step Implement:
      modules = ["MyModule"]
      output = code
      gate = "Tests pass"
```

## Best Practices

When using this skill:

1. **Provide clear requirements** - The more context, the better the specification
2. **Specify technology preferences** - Mention preferred frameworks, databases
3. **Define quality attributes** - Performance, security, scalability needs
4. **Ask for specific patterns** - Request CQRS, Event Sourcing, etc. if needed
5. **Validate iteratively** - Use the SODL compiler during development

## Troubleshooting

### Skill Not Triggering

Ensure your prompt mentions:
- "SODL specification"
- "Generate SODL"
- "Create SODL file"
- "Specification-driven development"

### Validation Errors

If the SODL compiler reports errors:
1. Check indentation (2 or 4 spaces consistently)
2. Verify all lists use proper syntax
3. Ensure module references exist
4. Check field constraint syntax

### Missing Constructs

If generated spec is missing sections:
1. Explicitly request them (e.g., "include error handling")
2. Ask for "production-ready" specification
3. Specify required quality attributes

## Contributing

To extend this skill:

1. Add new templates to `assets/templates/`
2. Add example specifications to `assets/examples/`
3. Update `references/sodl-quick-reference.md` with new constructs
4. Enhance `scripts/sodl_validator.py` with new utilities

## License

This skill is part of the SODL project and is licensed under the Business Source License 1.1 (BSL 1.1).

## Support

For issues or questions:
- Check the SODL documentation in `.sodl/SODL_spec_05.md`
- Review examples in `examples/` directory
- Use the SODL compiler for validation

---

**SODL Specification Generator** - Expert SODL architecture for AI-driven code generation.
