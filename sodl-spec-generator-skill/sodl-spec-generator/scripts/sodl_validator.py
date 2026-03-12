#!/usr/bin/env python3
"""
SODL Specification Validator and Generator Helper

This script provides utilities for validating and generating SODL specifications.
It integrates with the SODL compiler for syntax validation and provides
templates for common specification patterns.

Usage:
    python sodl_validator.py validate <spec.sodl>
    python sodl_validator.py generate <pattern> [output.sodl]
    python sodl_validator.py check-production <spec.sodl>
"""

import sys
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    from sodlcompiler import SODLCompiler, compile_source
    SODL_AVAILABLE = True
except ImportError:
    SODL_AVAILABLE = False
    print("Warning: sodlcompiler not available. Install with: pip install -e .")


def validate_spec(source_file: str) -> bool:
    """
    Validate a SODL specification file.
    
    Args:
        source_file: Path to the .sodl file
        
    Returns:
        True if valid, False otherwise
    """
    if not SODL_AVAILABLE:
        print("Error: sodlcompiler not available")
        return False
    
    source_path = Path(source_file)
    if not source_path.exists():
        print(f"Error: File not found: {source_file}")
        return False
    
    print(f"Validating: {source_file}")
    print("-" * 60)
    
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        compiler = compile_source(source_code, source_file)
        
        if compiler.has_errors():
            print("❌ Validation FAILED")
            print("\nErrors:")
            compiler.print_diagnostics()
            return False
        else:
            print("✓ Syntax validation PASSED")
            
            # Get AST for additional checks
            ast = compiler.get_ast()
            print(f"✓ AST generated with {len(ast.statements)} statements")
            
            # Check for required constructs
            check_required_constructs(ast)
            
            print("\n✓ Validation complete")
            return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def check_required_constructs(ast) -> None:
    """Check that specification has required constructs."""
    
    has_system = False
    has_intent = False
    has_modules = False
    module_count = 0
    
    for stmt in ast.statements:
        if hasattr(stmt, 'type'):
            if stmt.type == 'system':
                has_system = True
                if hasattr(stmt, 'intent') and stmt.intent:
                    has_intent = True
                if hasattr(stmt, 'modules') and stmt.modules:
                    has_modules = True
                    module_count = len(stmt.modules)
    
    print("\nConstruct Check:")
    print(f"  {'✓' if has_system else '❌'} System definition")
    print(f"  {'✓' if has_intent else '❌'} Intent section")
    print(f"  {'✓' if has_modules else '❌'} Module definitions ({module_count} modules)")


def check_production_readiness(source_file: str) -> bool:
    """
    Check if a SODL specification is production-ready.
    
    Checks for:
    - Error handling configuration
    - Observability configuration
    - Testing strategy
    - Security patterns
    - Complete module definitions
    
    Args:
        source_file: Path to the .sodl file
        
    Returns:
        True if production-ready, False otherwise
    """
    if not SODL_AVAILABLE:
        print("Error: sodlcompiler not available")
        return False
    
    source_path = Path(source_file)
    if not source_path.exists():
        print(f"Error: File not found: {source_file}")
        return False
    
    print(f"Checking production readiness: {source_file}")
    print("-" * 60)
    
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse source to check for production constructs
        checks = {
            'error_handling': 'error_handling:' in source_code,
            'observability': 'observability:' in source_code,
            'testing_strategy': 'testing_strategy:' in source_code,
            'security_patterns': 'security_patterns:' in source_code,
            'architecture': 'architecture:' in source_code,
            'design_patterns': 'design_patterns:' in source_code,
            'dependency_injection': 'dependency_injection:' in source_code,
            'pipeline': 'pipeline' in source_code,
        }
        
        print("\nProduction Readiness Checklist:")
        all_passed = True
        for check, passed in checks.items():
            status = '✓' if passed else '❌'
            print(f"  {status} {check.replace('_', ' ').title()}")
            if not passed:
                all_passed = False
        
        # Validate syntax
        compiler = compile_source(source_code, source_file)
        if compiler.has_errors():
            print("\n❌ Syntax errors found")
            compiler.print_diagnostics()
            return False
        
        print(f"\n{'✓' if all_passed else '⚠'} Production readiness: {'PASSED' if all_passed else 'INCOMPLETE'}")
        return all_passed
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def generate_template(pattern: str, output_file: Optional[str] = None) -> bool:
    """
    Generate a SODL template for a common pattern.
    
    Args:
        pattern: Pattern name (crud, microservice, event-driven, rest-api)
        output_file: Optional output file path
        
    Returns:
        True if successful
    """
    templates = {
        'crud': get_crud_template(),
        'microservice': get_microservice_template(),
        'event-driven': get_event_driven_template(),
        'rest-api': get_rest_api_template(),
        'fullstack': get_fullstack_template(),
    }
    
    if pattern not in templates:
        print(f"Error: Unknown pattern '{pattern}'")
        print(f"Available patterns: {', '.join(templates.keys())}")
        return False
    
    template = templates[pattern]
    
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(template)
            print(f"✓ Generated template: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error writing file: {str(e)}")
            return False
    else:
        print(template)
        return True


def get_crud_template() -> str:
    """Return CRUD application template."""
    return '''# CRUD Application Template
# Generated by sodl_validator.py

system "CrudApplication":
  version = "1.0.0"
  
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    database = "PostgreSQL"
    orm = "SQLAlchemy"
    testing = ["pytest", "pytest-cov", "pytest-asyncio"]
  
  intent:
    primary = "CRUD application for entity management"
    outcomes = [
      "Create, read, update, delete operations",
      "RESTful API with proper status codes",
      "Input validation and error handling",
      "Database persistence with transactions"
    ]
    out_of_scope = [
      "User authentication",
      "Real-time updates",
      "File uploads"
    ]
  
  architecture:
    style = "Clean Architecture"
    layers = ["Domain", "Application", "Infrastructure", "Interface"]
  
  design_patterns:
    - name = "Repository"
      scope = "global"
    - name = "Dependency Injection"
      scope = "global"
  
  dependency_injection:
    container = "AutoWire"
    injection_style = "Constructor Injection"
    lifetime_rules:
      - service = "DatabaseConnection"
        scope = "Singleton"
      - service = "EntityService"
        scope = "Transient"
  
  error_handling:
    strategy = "Result Pattern"
    error_codes:
      - code = "NOT_FOUND"
        http_status = 404
        user_message = "Resource not found"
      - code = "VALIDATION_ERROR"
        http_status = 400
        user_message = "Invalid input data"
      - code = "CONFLICT"
        http_status = 409
        user_message = "Resource conflict"
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
      framework = "pytest-asyncio"
    e2e_tests:
      framework = "httpx"
  
  security_patterns:
    authentication = "JWT"
    authorization = "RBAC"
    data_protection:
      encryption_at_rest = "AES-256"
      encryption_in_transit = "TLS 1.3"
  
  interface EntityRepository:
    doc = "Repository for entity CRUD operations"
    method create(entity: EntityInput) -> Entity
    method get_by_id(id: str) -> Optional[Entity]
    method get_all(page: int, limit: int) -> List[Entity]
    method update(id: str, updates: EntityUpdate) -> Entity
    method delete(id: str) -> bool
    invariants:
      invariant "All operations are transactional"
      invariant "Timestamps stored in UTC"
  
  module DataLayer:
    implements = [EntityRepository]
    exports = [EntityRepository]
    owns = ["ORM models", "Database operations", "Repository implementation"]
    invariants:
      invariant "All timestamps stored in UTC"
      invariant "Use database transactions"
    artifacts = [
      "app/models/entity.py",
      "app/repositories/entity_repository.py"
    ]
  
  module ServiceLayer:
    requires = [EntityRepository]
    owns = ["Business logic", "Validation", "Entity management"]
    invariants:
      invariant "All business rules enforced"
      invariant "Input validated before processing"
    artifacts = [
      "app/services/entity_service.py"
    ]
  
  module APILayer:
    requires = [EntityService]
    owns = ["REST endpoints", "Request/Response mapping"]
    api:
      model EntityInput:
        field name: str (min_length=1, max_length=200)
        field description: str (max_length=2000)
      
      model EntityResponse:
        field id: str
        field name: str
        field created_at: datetime
      
      endpoint "GET /api/entities" -> List[EntityResponse]
      endpoint "POST /api/entities" -> EntityResponse (201)
      endpoint "GET /api/entities/{id}" -> EntityResponse
      endpoint "PUT /api/entities/{id}" -> EntityResponse
      endpoint "DELETE /api/entities/{id}" -> Empty (204)
    
    invariants:
      invariant "All endpoints require authentication"
      invariant "Request bodies validated against schemas"
    acceptance:
      test "creates entity with valid data"
      test "returns 400 for invalid input"
      test "returns 404 for non-existent entity"
    artifacts = [
      "app/routes/entity_routes.py",
      "app/schemas/entity.py"
    ]
  
  pipeline "Development":
    step ImplementModels:
      modules = ["DataLayer"]
      output = code
      gate = "Models pass unit tests"
    
    step ImplementRepository:
      modules = ["DataLayer"]
      output = code
      gate = "Repository tests pass"
    
    step ImplementService:
      modules = ["ServiceLayer"]
      output = code
      gate = "Service tests pass"
    
    step ImplementAPI:
      modules = ["APILayer"]
      output = code
      gate = "API integration tests pass"
    
    step GenerateTests:
      output = tests
      gate = "Test coverage >= 80%"
'''


def get_microservice_template() -> str:
    """Return microservice template."""
    return '''# Microservice Template
# Generated by sodl_validator.py

system "Microservice":
  version = "1.0.0"
  
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    database = "PostgreSQL"
    message_queue = "RabbitMQ"
    cache = "Redis"
    testing = ["pytest", "pytest-asyncio", "pytest-mock"]
  
  intent:
    primary = "Autonomous microservice with CQRS and event-driven architecture"
    outcomes = [
      "Independent deployment and scaling",
      "Event-driven communication",
      "CQRS for read/write separation",
      "Resilient error handling"
    ]
    out_of_scope = [
      "User interface",
      "Direct database access from other services"
    ]
  
  architecture:
    style = "Hexagonal"
    layers = ["Domain", "Application"]
    
    ports:
      - name = "Input Ports"
        type = "Use Cases"
      - name = "Output Ports"
        type = "Repository Interfaces"
    
    adapters:
      - name = "Input Adapters"
        implements = ["REST API", "Message Consumer"]
      - name = "Output Adapters"
        implements = ["Database", "Message Queue"]
  
  design_patterns:
    - name = "CQRS"
      scope = "global"
      read_side = "Query Handlers"
      write_side = "Command Handlers"
    - name = "Saga"
      type = "Orchestration"
      compensating_transactions = true
    - name = "Repository"
      scope = "global"
  
  dependency_injection:
    container = "AutoWire"
    injection_style = "Constructor Injection"
    lifetime_rules:
      - service = "DatabaseConnection"
        scope = "Singleton"
      - service = "MessageBus"
        scope = "Singleton"
      - service = "CommandHandler"
        scope = "Transient"
  
  error_handling:
    strategy = "Result Pattern"
    error_codes:
      - code = "NOT_FOUND"
        http_status = 404
      - code = "VALIDATION_ERROR"
        http_status = 400
      - code = "CONFLICT"
        http_status = 409
      - code = "SERVICE_UNAVAILABLE"
        http_status = 503
    retry_policy:
      max_attempts = 3
      backoff = "exponential"
      timeout_ms = 5000
    circuit_breaker:
      enabled = true
      failure_threshold = 5
      recovery_timeout_ms = 30000
  
  observability:
    logging:
      format = "JSON"
      level = "INFO"
      correlation_id = true
    tracing:
      enabled = true
      provider = "OpenTelemetry"
      sampling_rate = 0.1
    metrics:
      enabled = true
      provider = "Prometheus"
      histogram_buckets = [5, 10, 25, 50, 100, 250, 500, 1000]
    health_checks:
      - name = "database"
        endpoint = "/health/db"
      - name = "message_queue"
        endpoint = "/health/mq"
  
  testing_strategy:
    unit_tests:
      framework = "pytest"
      coverage_target = 85%
    integration_tests:
      framework = "pytest-asyncio"
      testcontainers = true
    contract_tests:
      framework = "pact"
    load_tests:
      framework = "locust"
      target_rps = 1000
  
  security_patterns:
    authentication = "JWT"
    authorization = "RBAC"
    service_to_service = "mTLS"
    data_protection:
      encryption_at_rest = "AES-256"
      encryption_in_transit = "TLS 1.3"
    api_security:
      rate_limiting = true
      input_sanitization = true
      output_encoding = true
  
  # Command side
  module CommandHandlers:
    owns = ["Create entity", "Update entity", "Delete entity"]
    design_patterns:
      - name = "Command"
        scope = "local"
    invariants:
      invariant "All commands are idempotent"
      invariant "Commands validated before execution"
    artifacts = [
      "app/commands/",
      "app/command_handlers/"
    ]
  
  # Query side
  module QueryHandlers:
    owns = ["Get entity", "List entities", "Search entities"]
    design_patterns:
      - name = "Query"
        scope = "local"
    invariants:
      invariant "Queries are side-effect free"
      invariant "Query results cached when appropriate"
    artifacts = [
      "app/queries/",
      "app/query_handlers/"
    ]
  
  # Event publishing
  module EventPublisher:
    owns = ["Domain event publication", "Event routing"]
    requires = ["MessageBus"]
    invariants:
      invariant "Events published atomically with state changes"
      invariant "Event schema versioned"
    artifacts = [
      "app/events/",
      "app/event_publishers/"
    ]
  
  # API layer
  module APIAdapter:
    requires = ["CommandHandlers", "QueryHandlers"]
    owns = ["REST endpoints", "Request/Response mapping"]
    api:
      endpoint "GET /api/entities" -> List[EntityResponse]
      endpoint "POST /api/entities" -> EntityResponse (201)
      endpoint "GET /api/entities/{id}" -> EntityResponse
      endpoint "PUT /api/entities/{id}" -> EntityResponse
      endpoint "DELETE /api/entities/{id}" -> Empty (204)
    
    invariants:
      invariant "All endpoints require authentication"
      invariant "Rate limiting applied"
    artifacts = [
      "app/routes/",
      "app/schemas/"
    ]
  
  # Infrastructure
  module Infrastructure:
    implements = ["EntityRepository", "MessageBus"]
    owns = ["Database operations", "Message queue operations"]
    invariants:
      invariant "Database transactions used"
      invariant "Messages published reliably"
    artifacts = [
      "app/infrastructure/"
    ]
  
  pipeline "Development":
    step ImplementDomain:
      modules = ["CommandHandlers", "QueryHandlers"]
      output = code
      gate = "Domain tests pass"
    
    step ImplementInfrastructure:
      modules = ["Infrastructure", "EventPublisher"]
      output = code
      gate = "Infrastructure tests pass"
    
    step ImplementAPI:
      modules = ["APIAdapter"]
      output = code
      gate = "API tests pass"
    
    step IntegrationTests:
      output = test_results
      gate = "All integration tests pass"
    
    step LoadTests:
      output = load_report
      gate = "Performance targets met"
'''


def get_event_driven_template() -> str:
    """Return event-driven architecture template."""
    return '''# Event-Driven Architecture Template
# Generated by sodl_validator.py

system "EventDrivenSystem":
  version = "1.0.0"
  
  stack:
    language = "Python 3.12"
    message_broker = "Apache Kafka"
    event_store = "EventStoreDB"
    testing = ["pytest", "pytest-asyncio"]
  
  intent:
    primary = "Event sourcing with CQRS for audit-able, scalable system"
    outcomes = [
      "Complete audit trail via event sourcing",
      "Scalable read models via CQRS",
      "Event-driven integrations",
      "Temporal queries supported"
    ]
  
  architecture:
    style = "Event-Driven"
    
    event_bus:
      type = "Event Stream"
      implementation = "Apache Kafka"
      partitions = 8
      replication_factor = 3
    
    event_store:
      type = "EventStoreDB"
      projections_enabled = true
  
  design_patterns:
    - name = "Event Sourcing"
      scope = "global"
      snapshot_strategy = "Every 100 events"
    - name = "CQRS"
      scope = "global"
      read_side = "Projections"
      write_side = "Aggregates"
    - name = "Saga"
      type = "Choreography"
  
  event_types:
    - name = "Domain Events"
      scope = "Within bounded context"
      retention_days = 365
    - name = "Integration Events"
      scope = "Across bounded contexts"
      retention_days = 7
  
  error_handling:
    strategy = "Event Compensation"
    dead_letter_queue:
      enabled = true
      max_retries = 3
    poison_pill_handling:
      enabled = true
      alert_on_threshold = 10
  
  observability:
    event_tracing:
      enabled = true
      correlation_id = true
      causation_id = true
    projection_monitoring:
      lag_alert_threshold_ms = 5000
  
  module EventStore:
    owns = ["Event persistence", "Stream management", "Snapshots"]
    invariants:
      invariant "Events are immutable"
      invariant "Events appended atomically"
      invariant "Optimistic concurrency enforced"
    artifacts = [
      "app/event_store/"
    ]
  
  module Aggregates:
    owns = ["Business logic", "State reconstruction", "Event generation"]
    invariants:
      invariant "Aggregates are consistency boundaries"
      invariant "All state changes produce events"
    artifacts = [
      "app/aggregates/"
    ]
  
  module Projections:
    owns = ["Read model updates", "Query handling"]
    invariants:
      invariant "Projections are eventually consistent"
      invariant "Projections are idempotent"
    artifacts = [
      "app/projections/"
    ]
  
  module EventHandlers:
    owns = ["Event processing", "Side effects", "Integration triggers"]
    invariants:
      invariant "Event handlers are idempotent"
      invariant "Failures logged and retried"
    artifacts = [
      "app/event_handlers/"
    ]
  
  pipeline "Development":
    step ImplementEventStore:
      modules = ["EventStore"]
      output = code
      gate = "Event store tests pass"
    
    step ImplementAggregates:
      modules = ["Aggregates"]
      output = code
      gate = "Aggregate tests pass"
    
    step ImplementProjections:
      modules = ["Projections"]
      output = code
      gate = "Projection tests pass"
    
    step ImplementEventHandlers:
      modules = ["EventHandlers"]
      output = code
      gate = "Handler tests pass"
'''


def get_rest_api_template() -> str:
    """Return REST API with authentication template."""
    return '''# REST API with JWT Authentication Template
# Generated by sodl_validator.py

system "AuthenticatedRESTAPI":
  version = "1.0.0"
  
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    database = "PostgreSQL"
    orm = "SQLAlchemy"
    authentication = "PyJWT"
    password_hashing = "bcrypt"
  
  intent:
    primary = "Secure REST API with JWT authentication and RBAC"
    outcomes = [
      "User registration and authentication",
      "JWT-based authorization",
      "Role-based access control",
      "Secure password management"
    ]
  
  security_patterns:
    authentication = "JWT"
    authorization = "RBAC"
    roles = ["user", "admin", "superadmin"]
    
    token_settings:
      access_token_expiry_minutes = 30
      refresh_token_expiry_days = 7
      algorithm = "RS256"
      key_size = 2048
    
    password_policy:
      min_length = 8
      max_length = 128
      require_uppercase = true
      require_lowercase = true
      require_digit = true
      require_special = false
      history_count = 5
    
    data_protection:
      encryption_at_rest = "AES-256"
      encryption_in_transit = "TLS 1.3"
  
  interface IUserRepository:
    doc = "User data access"
    method create(user: UserInput) -> User
    method get_by_id(id: str) -> Optional[User]
    method get_by_email(email: str) -> Optional[User]
    method update(id: str, updates: UserUpdate) -> User
    invariants:
      invariant "Emails are unique"
      invariant "Passwords never returned"
  
  interface ITokenService:
    doc = "JWT token management"
    method create_access_token(user_id: str, roles: List[str]) -> str
    method create_refresh_token(user_id: str) -> str
    method validate_token(token: str) -> TokenPayload
    method refresh_access_token(refresh_token: str) -> str
    invariants:
      invariant "Tokens signed with RS256"
      invariant "Expired tokens rejected"
  
  module AuthenticationModule:
    implements = [ITokenService]
    requires = [IUserRepository]
    owns = ["User registration", "Login", "Token refresh", "Password reset"]
    
    api:
      endpoint "POST /api/auth/register" -> AuthResponse
      endpoint "POST /api/auth/login" -> AuthResponse
      endpoint "POST /api/auth/refresh" -> AuthResponse
      endpoint "POST /api/auth/logout" -> Empty
      endpoint "POST /api/auth/forgot-password" -> Empty
      endpoint "POST /api/auth/reset-password" -> Empty
    
    invariants:
      invariant "Passwords hashed with bcrypt (cost >= 10)"
      invariant "Failed logins logged with IP"
      invariant "Rate limiting on auth endpoints"
    
    acceptance:
      test "registers user with valid data"
      test "rejects weak passwords"
      test "rejects duplicate emails"
      test "returns JWT on successful login"
      test "rejects invalid credentials"
      test "refreshes access token"
    
    artifacts = [
      "app/routes/auth_routes.py",
      "app/services/auth_service.py",
      "app/services/token_service.py"
    ]
  
  module ProtectedResources:
    requires = [AuthenticationModule]
    owns = ["Protected API endpoints"]
    
    api:
      endpoint "GET /api/users/me" -> UserProfileResponse
      endpoint "PUT /api/users/me" -> UserProfileResponse
      endpoint "GET /api/users" -> List[UserProfileResponse] (admin)
      endpoint "DELETE /api/users/{id}" -> Empty (admin)
    
    invariants:
      invariant "All endpoints require valid JWT"
      invariant "RBAC checks on admin endpoints"
      invariant "Users can only access own data"
    
    artifacts = [
      "app/routes/user_routes.py",
      "app/middleware/auth_middleware.py"
    ]
  
  policy SecurityPolicy:
    rules:
      "All passwords must be hashed using bcrypt with cost factor >= 10" severity = "critical"
      "JWT tokens must use RS256 algorithm with 2048-bit keys" severity = "critical"
      "All API responses must include security headers" severity = "high"
      "Failed login attempts must be logged with IP and timestamp" severity = "high"
      "Password reset tokens must expire within 1 hour" severity = "high"
      "Rate limiting must be applied to all auth endpoints" severity = "high"
  
  pipeline "Development":
    step ImplementUserModel:
      modules = ["AuthenticationModule"]
      output = code
      gate = "User model tests pass"
    
    step ImplementAuthService:
      modules = ["AuthenticationModule"]
      output = code
      gate = "Auth service tests pass"
    
    step ImplementAuthRoutes:
      modules = ["AuthenticationModule"]
      output = code
      gate = "Auth endpoint tests pass"
    
    step ImplementProtectedRoutes:
      modules = ["ProtectedResources"]
      output = code
      gate = "Protected endpoint tests pass"
    
    step SecurityReview:
      output = security_report
      gate = "No critical or high severity issues"
'''


def get_fullstack_template() -> str:
    """Return full-stack web application template."""
    return '''# Full-Stack Web Application Template
# Generated by sodl_validator.py

system "FullStackWebApp":
  version = "1.0.0"
  
  stack:
    language = "Python 3.12"
    backend = "FastAPI"
    frontend = "React 18"
    database = "PostgreSQL"
    orm = "SQLAlchemy"
    ui_framework = "Material-UI"
    state_management = "Redux Toolkit"
    testing = ["pytest", "jest", "playwright"]
  
  intent:
    primary = "Full-stack web application with React frontend and FastAPI backend"
    outcomes = [
      "RESTful API backend",
      "Responsive React frontend",
      "Real-time updates via WebSocket",
      "Authentication and authorization"
    ]
  
  architecture:
    style = "Layered Architecture"
    layers = ["Presentation", "Application", "Domain", "Infrastructure"]
  
  design_patterns:
    - name = "Repository"
      scope = "backend"
    - name = "Container Pattern"
      scope = "frontend"
    - name = "Custom Hooks"
      scope = "frontend"
  
  # Backend modules
  module BackendAPI:
    owns = ["REST API", "Business logic", "Data access"]
    
    api:
      endpoint "GET /api/items" -> List[ItemResponse]
      endpoint "POST /api/items" -> ItemResponse
      endpoint "GET /api/items/{id}" -> ItemResponse
      endpoint "PUT /api/items/{id}" -> ItemResponse
      endpoint "DELETE /api/items/{id}" -> Empty
    
    artifacts = [
      "backend/app/main.py",
      "backend/app/routes/",
      "backend/app/services/",
      "backend/app/models/"
    ]
  
  # Frontend modules
  module FrontendApp:
    owns = ["React components", "State management", "API integration"]
    
    ui:
      theme = "Material"
      components:
        - name = "ItemList"
        - name = "ItemForm"
        - name = "ItemDetail"
    
    artifacts = [
      "frontend/src/App.tsx",
      "frontend/src/components/",
      "frontend/src/hooks/",
      "frontend/src/store/"
    ]
  
  # WebSocket for real-time
  module RealTimeModule:
    owns = ["WebSocket connections", "Real-time updates"]
    
    invariants:
      invariant "WebSocket connections authenticated"
      invariant "Messages validated before broadcast"
    
    artifacts = [
      "backend/app/websocket/",
      "frontend/src/hooks/useWebSocket.ts"
    ]
  
  pipeline "FullStack":
    step ImplementBackend:
      modules = ["BackendAPI"]
      output = code
      gate = "Backend tests pass"
    
    step ImplementFrontend:
      modules = ["FrontendApp"]
      output = code
      gate = "Frontend tests pass"
    
    step ImplementRealTime:
      modules = ["RealTimeModule"]
      output = code
      gate = "WebSocket tests pass"
    
    step IntegrationTests:
      output = test_results
      gate = "E2E tests pass"
'''


def print_help():
    """Print help information."""
    print("""
SODL Specification Validator and Generator

Usage:
    python sodl_validator.py <command> [arguments]

Commands:
    validate <file.sodl>              Validate SODL syntax
    check-production <file.sodl>      Check production readiness
    generate <pattern> [output.sodl]  Generate template
    help                              Show this help

Patterns:
    crud          CRUD application
    microservice  CQRS microservice
    event-driven  Event sourcing system
    rest-api      REST API with JWT auth
    fullstack     Full-stack web app

Examples:
    python sodl_validator.py validate spec.sodl
    python sodl_validator.py check-production spec.sodl
    python sodl_validator.py generate crud output.sodl
    python sodl_validator.py generate microservice
""")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "validate":
        if len(sys.argv) < 3:
            print("Error: Missing file argument")
            print("Usage: python sodl_validator.py validate <file.sodl>")
            sys.exit(1)
        success = validate_spec(sys.argv[2])
        sys.exit(0 if success else 1)
    
    elif command == "check-production":
        if len(sys.argv) < 3:
            print("Error: Missing file argument")
            print("Usage: python sodl_validator.py check-production <file.sodl>")
            sys.exit(1)
        success = check_production_readiness(sys.argv[2])
        sys.exit(0 if success else 1)
    
    elif command == "generate":
        if len(sys.argv) < 3:
            print("Error: Missing pattern argument")
            print("Usage: python sodl_validator.py generate <pattern> [output.sodl]")
            sys.exit(1)
        pattern = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else None
        success = generate_template(pattern, output)
        sys.exit(0 if success else 1)
    
    elif command == "help":
        print_help()
        sys.exit(0)
    
    else:
        print(f"Error: Unknown command '{command}'")
        print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
