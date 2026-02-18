# SODL Code Examples Collection

Comprehensive collection of SODL code examples for various application patterns.

## Table of Contents

1. [Web Applications](#web-applications)
2. [REST APIs](#rest-apis)
3. [Microservices](#microservices)
4. [Data Processing](#data-processing)
5. [CLI Applications](#cli-applications)
6. [Real-time Applications](#real-time-applications)
7. [Integration Patterns](#integration-patterns)
8. [Testing Patterns](#testing-patterns)

## Web Applications

### Simple Blog Platform

```sodl
system "SimpleBlog":
  version = "1.0.0"
  stack:
    language = "Python 3.12"
    web = "Flask"
    database = "SQLite"
    templating = "Jinja2"
  
  intent:
    primary = "Personal blogging platform with posts and comments"
    outcomes = [
      "Create and publish blog posts",
      "View posts with markdown rendering",
      "Comment on posts",
      "Tag-based categorization"
    ]
    out_of_scope = ["User authentication", "Admin panel"]

  interface PostRepository:
    method create(post: PostInput) -> Post
    method get_by_id(id: UUID) -> Optional[Post]
    method get_all(page: int, limit: int) -> List[Post]
    method get_by_tag(tag: str) -> List[Post]
    method update(id: UUID, updates: PostUpdate) -> Post
    method delete(id: UUID) -> bool

  interface CommentRepository:
    method create(comment: CommentInput) -> Comment
    method get_by_post(post_id: UUID) -> List[Comment]
    method delete(id: UUID) -> bool

  module BlogUI:
    requires = [PostRepository, CommentRepository]
    api:
      endpoint "GET /" -> HTML
      endpoint "GET /post/{id}" -> HTML
      endpoint "POST /post/create" -> Redirect
      endpoint "POST /post/{id}/comment" -> Redirect
    invariants:
      invariant "Markdown is sanitized before rendering"
      invariant "All forms include CSRF protection"
    artifacts = ["app/views.py", "templates/*.html"]

  module PostService:
    implements = [PostRepository]
    exports = [PostRepository]
    invariants:
      invariant "Posts have unique slugs"
      invariant "Timestamps are in UTC"
    artifacts = ["app/services/posts.py"]

  module CommentService:
    implements = [CommentRepository]
    exports = [CommentRepository]
    invariants:
      invariant "Comments reference valid posts"
    artifacts = ["app/services/comments.py"]

  pipeline "Development":
    step Implement:
      modules = ["PostService", "CommentService", "BlogUI"]
      output = code
      gate = "Integration tests pass"
```

### E-Commerce Product Page

```sodl
system "ProductShowcase":
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    frontend = "HTMX + Alpine.js"
    database = "PostgreSQL"
  
  intent:
    primary = "Dynamic product display with filtering and search"
    outcomes = [
      "Browse products with images",
      "Filter by category, price, rating",
      "Real-time search without page reload",
      "Product detail views with reviews"
    ]

  interface ProductCatalog:
    method search(query: str, filters: ProductFilters) -> List[Product]
    method get_product(id: UUID) -> ProductDetail
    method get_categories() -> List[Category]

  interface ReviewService:
    method get_reviews(product_id: UUID) -> List[Review]
    method get_average_rating(product_id: UUID) -> float

  module ProductAPI:
    requires = [ProductCatalog, ReviewService]
    api:
      endpoint "GET /api/products" -> List[ProductCard]
      endpoint "GET /api/products/{id}" -> ProductDetail
      endpoint "GET /api/search" -> List[ProductCard]
      endpoint "GET /api/categories" -> List[Category]
    invariants:
      invariant "Responses are cached for 5 minutes"
      invariant "Images are served via CDN"

  module ProductPages:
    requires = [ProductCatalog, ReviewService]
    api:
      endpoint "GET /products" -> HTML
      endpoint "GET /products/{id}" -> HTML
    invariants:
      invariant "HTMX handles dynamic content updates"
      invariant "Images have lazy loading"
    artifacts = ["app/pages.py", "templates/products/*.html"]

  pipeline "Production":
    step Implement:
      modules = ["ProductAPI", "ProductPages"]
      output = code
      require = "Optimize for Core Web Vitals"
      gate = "Lighthouse score > 90"
```

## REST APIs

### User Management API

```sodl
system "UserManagementAPI":
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    database = "PostgreSQL"
    auth = "JWT"
  
  intent:
    primary = "RESTful API for user account management"
    outcomes = [
      "User registration and profile management",
      "JWT-based authentication",
      "Role-based access control",
      "Email verification workflow"
    ]

  policy Security:
    rule "Passwords hashed with bcrypt" severity=critical
    rule "JWT tokens expire in 1 hour" severity=high
    rule "Rate limit authentication endpoints" severity=high
    rule "Validate all input with Pydantic" severity=critical

  interface UserRepository:
    method create(user: UserCreate) -> User
    method get_by_id(id: UUID) -> Optional[User]
    method get_by_email(email: str) -> Optional[User]
    method update(id: UUID, updates: UserUpdate) -> User
    method delete(id: UUID) -> bool
    method verify_email(token: str) -> bool

  interface AuthService:
    method register(credentials: RegisterRequest) -> User
    method login(credentials: LoginRequest) -> TokenResponse
    method verify_token(token: str) -> Optional[User]
    method refresh_token(refresh_token: str) -> TokenResponse

  module AuthAPI:
    requires = [AuthService]
    api:
      endpoint "POST /api/auth/register" -> UserResponse (201)
      endpoint "POST /api/auth/login" -> TokenResponse
      endpoint "POST /api/auth/refresh" -> TokenResponse
      endpoint "POST /api/auth/verify-email" -> Empty (204)
    invariants:
      invariant "Rate limit 5 requests per minute per IP"
      invariant "Return 401 for invalid credentials"
      invariant "Log all authentication attempts"
    acceptance:
      test "registers new user successfully"
      test "rejects duplicate email"
      test "returns JWT on valid login"
      test "rejects invalid credentials"
    artifacts = ["app/api/auth.py"]

  module UserAPI:
    requires = [UserRepository, AuthService]
    api:
      endpoint "GET /api/users/me" -> UserResponse
      endpoint "PUT /api/users/me" -> UserResponse
      endpoint "DELETE /api/users/me" -> Empty (204)
      endpoint "GET /api/users/{id}" -> PublicUserResponse
    invariants:
      invariant "Require valid JWT for all endpoints"
      invariant "Users can only modify their own data"
      invariant "Sensitive fields hidden in public responses"
    artifacts = ["app/api/users.py"]

  pipeline "Production":
    step ImplementAuth:
      modules = ["AuthAPI"]
      output = code
      gate = "Security tests pass"
    
    step ImplementUsers:
      modules = ["UserAPI"]
      output = code
      gate = "Integration tests pass"
```

### Task Queue API

```sodl
system "TaskQueueAPI":
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    queue = "Celery + Redis"
    database = "PostgreSQL"
  
  intent:
    primary = "API for submitting and monitoring async tasks"
    outcomes = [
      "Submit tasks to background queue",
      "Check task status and results",
      "Cancel running tasks",
      "Retry failed tasks"
    ]

  interface TaskQueue:
    method submit(task: TaskSubmission) -> TaskID
    method get_status(task_id: TaskID) -> TaskStatus
    method get_result(task_id: TaskID) -> TaskResult
    method cancel(task_id: TaskID) -> bool
    method retry(task_id: TaskID) -> TaskID

  module TaskAPI:
    requires = [TaskQueue]
    api:
      endpoint "POST /api/tasks" -> TaskSubmitResponse (202)
      endpoint "GET /api/tasks/{id}" -> TaskStatusResponse
      endpoint "GET /api/tasks/{id}/result" -> TaskResultResponse
      endpoint "POST /api/tasks/{id}/cancel" -> Empty (204)
      endpoint "POST /api/tasks/{id}/retry" -> TaskSubmitResponse
    invariants:
      invariant "Return 202 Accepted for async submissions"
      invariant "Include task ID in response headers"
      invariant "Provide polling URL in response"
    artifacts = ["app/api/tasks.py"]

  module CeleryWorker:
    implements = [TaskQueue]
    exports = [TaskQueue]
    config:
      broker = "redis://localhost:6379/0"
      result_backend = "redis://localhost:6379/1"
      max_retries = 3
    invariants:
      invariant "Tasks are idempotent"
      invariant "Failed tasks are logged"
    artifacts = ["app/workers/celery_app.py"]

  pipeline "Deploy":
    step Implement:
      modules = ["TaskAPI", "CeleryWorker"]
      output = code
      gate = "Load tests pass at 100 tasks/sec"
```

## Microservices

### Order Processing Service

```sodl
system "OrderService":
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    database = "PostgreSQL"
    messaging = "RabbitMQ"
    cache = "Redis"
  
  intent:
    primary = "Microservice for order processing and fulfillment"
    outcomes = [
      "Create and manage orders",
      "Publish order events to message bus",
      "Track order status transitions",
      "Handle payment confirmations"
    ]

  policy Reliability:
    rule "All events published with acknowledgment" severity=critical
    rule "Implement circuit breaker for external calls" severity=high
    rule "Use database transactions for state changes" severity=critical
    rule "Retry failed messages with exponential backoff" severity=high

  interface OrderRepository:
    method create(order: OrderCreate) -> Order
    method get_by_id(id: UUID) -> Optional[Order]
    method update_status(id: UUID, status: OrderStatus) -> Order
    method get_by_customer(customer_id: UUID) -> List[Order]

  interface EventPublisher:
    method publish(event: OrderEvent) -> bool
    method publish_batch(events: List[OrderEvent]) -> int

  interface PaymentClient:
    method verify_payment(payment_id: str) -> PaymentStatus
    method refund(payment_id: str, amount: Decimal) -> bool

  module OrderAPI:
    requires = [OrderRepository, EventPublisher]
    api:
      endpoint "POST /api/orders" -> OrderResponse (201)
      endpoint "GET /api/orders/{id}" -> OrderResponse
      endpoint "PUT /api/orders/{id}/status" -> OrderResponse
      endpoint "GET /api/customers/{id}/orders" -> List[OrderResponse]
    invariants:
      invariant "Emit OrderCreated event on order creation"
      invariant "Emit OrderStatusChanged on status update"
      invariant "Use optimistic locking for concurrent updates"
    artifacts = ["app/api/orders.py"]

  module EventHandler:
    requires = [OrderRepository, PaymentClient]
    owns = ["Payment confirmation handler", "Order timeout handler"]
    invariants:
      invariant "Handle PaymentConfirmed event idempotently"
      invariant "Update order status transactionally"
    artifacts = ["app/handlers/events.py"]

  module RabbitMQPublisher:
    implements = [EventPublisher]
    exports = [EventPublisher]
    config:
      exchange = "orders"
      routing_key_prefix = "order"
    artifacts = ["app/messaging/publisher.py"]

  pipeline "Production":
    step ImplementCore:
      modules = ["OrderAPI", "RabbitMQPublisher"]
      output = code
      gate = "Unit tests pass"
    
    step ImplementHandlers:
      modules = ["EventHandler"]
      output = code
      gate = "Integration tests pass"
```

### API Gateway

```sodl
system "APIGateway":
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    cache = "Redis"
    monitoring = "Prometheus"
  
  intent:
    primary = "Central API gateway with routing and rate limiting"
    outcomes = [
      "Route requests to backend services",
      "Implement rate limiting per client",
      "Cache responses when appropriate",
      "Collect metrics for all requests"
    ]

  policy Performance:
    rule "Cache GET responses for 60 seconds" severity=medium
    rule "Timeout backend requests after 30 seconds" severity=high
    rule "Implement circuit breaker for each service" severity=critical

  policy Security:
    rule "Validate JWT tokens before routing" severity=critical
    rule "Rate limit 100 requests per minute per client" severity=high
    rule "Strip sensitive headers from responses" severity=high

  interface ServiceRouter:
    method route(request: Request) -> Response
    method get_service_url(service_name: str, path: str) -> str

  interface RateLimiter:
    method check_limit(client_id: str, endpoint: str) -> bool
    method record_request(client_id: str, endpoint: str) -> None

  module GatewayAPI:
    requires = [ServiceRouter, RateLimiter]
    api:
      endpoint "ANY /*" -> ProxiedResponse
    invariants:
      invariant "Check rate limit before routing"
      invariant "Add correlation ID to all requests"
      invariant "Log all requests with timing"
    artifacts = ["app/gateway.py"]

  module RedisRateLimiter:
    implements = [RateLimiter]
    exports = [RateLimiter]
    config:
      window_seconds = 60
      max_requests = 100
    artifacts = ["app/rate_limiter.py"]

  pipeline "Deploy":
    step Implement:
      modules = ["GatewayAPI", "RedisRateLimiter"]
      output = code
      gate = "Load tests pass at 1000 req/sec"
```

## Data Processing

### ETL Pipeline

```sodl
system "DataETLPipeline":
  stack:
    language = "Python 3.12"
    database = "PostgreSQL"
    warehouse = "BigQuery"
    orchestration = "Airflow"
  
  intent:
    primary = "Extract, transform, and load data from multiple sources"
    outcomes = [
      "Extract data from REST APIs and databases",
      "Transform and clean data",
      "Load into data warehouse",
      "Schedule daily runs with retry logic"
    ]

  policy DataQuality:
    rule "Validate schema before loading" severity=critical
    rule "Log data quality metrics" severity=high
    rule "Quarantine invalid records" severity=high
    rule "Deduplicate records by unique key" severity=critical

  interface DataExtractor:
    method extract_from_api(api_config: APIConfig) -> DataFrame
    method extract_from_db(query: str) -> DataFrame
    method extract_from_file(path: str, format: str) -> DataFrame

  interface DataTransformer:
    method clean(df: DataFrame, rules: CleanRules) -> DataFrame
    method validate(df: DataFrame, schema: Schema) -> ValidationResult
    method enrich(df: DataFrame, enrichments: List[Enrichment]) -> DataFrame

  interface DataLoader:
    method load(df: DataFrame, table: str, mode: LoadMode) -> LoadResult
    method create_table(schema: Schema, table: str) -> bool

  module ExtractorModule:
    implements = [DataExtractor]
    exports = [DataExtractor]
    invariants:
      invariant "Implement exponential backoff for API calls"
      invariant "Stream large datasets to avoid memory issues"
    artifacts = ["app/extract.py"]

  module TransformerModule:
    implements = [DataTransformer]
    exports = [DataTransformer]
    invariants:
      invariant "All transformations are deterministic"
      invariant "Invalid records logged with reason"
    artifacts = ["app/transform.py"]

  module LoaderModule:
    implements = [DataLoader]
    exports = [DataLoader]
    config:
      batch_size = 10000
      max_retries = 3
    artifacts = ["app/load.py"]

  module PipelineOrchestrator:
    requires = [DataExtractor, DataTransformer, DataLoader]
    owns = ["Pipeline DAG definition", "Error handling"]
    artifacts = ["dags/etl_pipeline.py"]

  pipeline "Production":
    step ImplementComponents:
      modules = ["ExtractorModule", "TransformerModule", "LoaderModule"]
      output = code
      gate = "Component tests pass"
    
    step ImplementOrchestration:
      modules = ["PipelineOrchestrator"]
      output = code
      gate = "End-to-end test completes"
```

### Real-time Stream Processor

```sodl
system "StreamProcessor":
  stack:
    language = "Python 3.12"
    streaming = "Kafka"
    processing = "Faust"
    storage = "Redis"
  
  intent:
    primary = "Process streaming events in real-time"
    outcomes = [
      "Consume events from Kafka topics",
      "Apply transformations and aggregations",
      "Detect anomalies in real-time",
      "Output to downstream topics"
    ]

  interface EventConsumer:
    method consume(topic: str) -> Stream[Event]
    method commit_offset(topic: str, partition: int, offset: int) -> None

  interface EventProcessor:
    method transform(event: Event) -> ProcessedEvent
    method aggregate(window: TimeWindow, events: List[Event]) -> Aggregate
    method detect_anomaly(event: Event, baseline: Stats) -> Optional[Anomaly]

  interface EventProducer:
    method produce(topic: str, event: Event) -> None
    method produce_batch(topic: str, events: List[Event]) -> None

  module FaustApp:
    requires = [EventProcessor]
    owns = ["Faust agents", "Stream definitions"]
    config:
      broker = "kafka://localhost:9092"
      processing_guarantee = "at-least-once"
    invariants:
      invariant "Process events in order per partition"
      invariant "Handle deserialization errors gracefully"
    artifacts = ["app/faust_app.py"]

  module AnomalyDetector:
    implements = [EventProcessor]
    exports = [EventProcessor]
    config:
      threshold_std_dev = 3.0
      window_size = "5 minutes"
    artifacts = ["app/anomaly.py"]

  pipeline "Deploy":
    step Implement:
      modules = ["FaustApp", "AnomalyDetector"]
      output = code
      gate = "Process 10k events/sec without lag"
```

## CLI Applications

### Database Migration Tool

```sodl
system "DBMigrationCLI":
  stack:
    language = "Python 3.12"
    cli = "Click"
    database = "PostgreSQL"
  
  intent:
    primary = "CLI tool for managing database migrations"
    outcomes = [
      "Generate migration files from models",
      "Apply migrations in order",
      "Rollback migrations",
      "Show migration status"
    ]

  interface MigrationRepository:
    method get_all() -> List[Migration]
    method get_applied() -> List[Migration]
    method get_pending() -> List[Migration]
    method mark_applied(migration: Migration) -> None
    method mark_reverted(migration: Migration) -> None

  interface MigrationExecutor:
    method apply(migration: Migration) -> ExecutionResult
    method revert(migration: Migration) -> ExecutionResult
    method validate(migration: Migration) -> ValidationResult

  module CLICommands:
    requires = [MigrationRepository, MigrationExecutor]
    api:
      command "init" -> None
      command "generate <name>" -> None
      command "migrate" -> None
      command "rollback [steps]" -> None
      command "status" -> None
    invariants:
      invariant "Commands idempotent where possible"
      invariant "Show progress for long operations"
      invariant "Confirm destructive operations"
    artifacts = ["cli/commands.py"]

  module PostgresExecutor:
    implements = [MigrationExecutor]
    exports = [MigrationExecutor]
    config:
      transaction_per_migration = true
    invariants:
      invariant "Wrap each migration in transaction"
      invariant "Rollback on first error"
    artifacts = ["cli/executor.py"]

  pipeline "Release":
    step Implement:
      modules = ["CLICommands", "PostgresExecutor"]
      output = code
      gate = "CLI integration tests pass"
```

### Log Analyzer

```sodl
system "LogAnalyzer":
  stack:
    language = "Python 3.12"
    cli = "Typer"
    parsing = "regex + pyparsing"
  
  intent:
    primary = "Analyze and extract insights from log files"
    outcomes = [
      "Parse various log formats",
      "Filter logs by criteria",
      "Generate statistics and summaries",
      "Export results to JSON/CSV"
    ]

  interface LogParser:
    method parse_file(path: str, format: LogFormat) -> List[LogEntry]
    method parse_line(line: str, format: LogFormat) -> Optional[LogEntry]
    method detect_format(path: str) -> Optional[LogFormat]

  interface LogAnalyzer:
    method filter(entries: List[LogEntry], criteria: FilterCriteria) -> List[LogEntry]
    method summarize(entries: List[LogEntry]) -> Summary
    method group_by(entries: List[LogEntry], field: str) -> Dict[str, List[LogEntry]]
    method top_errors(entries: List[LogEntry], n: int) -> List[ErrorSummary]

  module CLIInterface:
    requires = [LogParser, LogAnalyzer]
    api:
      command "analyze <file> [options]" -> None
      command "filter <file> [criteria]" -> None
      command "stats <file>" -> None
      command "export <file> --format=<format>" -> None
    artifacts = ["cli/main.py"]

  pipeline "Build":
    step Implement:
      modules = ["CLIInterface"]
      output = code
      gate = "Process 1GB log file in < 30 seconds"
```

## Real-time Applications

### Chat Application

```sodl
system "RealtimeChat":
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    websocket = "WebSockets"
    database = "PostgreSQL"
    cache = "Redis"
  
  intent:
    primary = "Real-time chat with multiple rooms"
    outcomes = [
      "Join and leave chat rooms",
      "Send and receive messages in real-time",
      "See typing indicators",
      "Store message history"
    ]

  interface MessageBroker:
    method publish(room_id: str, message: Message) -> None
    method subscribe(room_id: str) -> AsyncIterator[Message]
    method broadcast_to_room(room_id: str, event: Event) -> None

  interface MessageStore:
    method save(message: Message) -> None
    method get_history(room_id: str, limit: int) -> List[Message]

  module WebSocketHandler:
    requires = [MessageBroker, MessageStore]
    api:
      websocket "/ws/room/{room_id}" -> None
    invariants:
      invariant "Authenticate connection before accepting"
      invariant "Send ping/pong for keepalive"
      invariant "Handle disconnects gracefully"
    artifacts = ["app/websocket.py"]

  module RedisBroker:
    implements = [MessageBroker]
    exports = [MessageBroker]
    config:
      pubsub_channels = "room:*"
    artifacts = ["app/broker.py"]

  pipeline "Deploy":
    step Implement:
      modules = ["WebSocketHandler", "RedisBroker"]
      output = code
      gate = "Support 1000 concurrent connections"
```

### Live Dashboard

```sodl
system "LiveDashboard":
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    frontend = "HTMX + Server-Sent Events"
    database = "TimescaleDB"
  
  intent:
    primary = "Real-time monitoring dashboard with live updates"
    outcomes = [
      "Display metrics updating every second",
      "Show alerts and anomalies",
      "Historical data charts",
      "No client-side JavaScript framework needed"
    ]

  interface MetricsCollector:
    method collect_latest() -> MetricsSnapshot
    method get_timeseries(metric: str, duration: Duration) -> List[DataPoint]

  interface AlertDetector:
    method check_thresholds(metrics: MetricsSnapshot) -> List[Alert]
    method get_active_alerts() -> List[Alert]

  module SSEEndpoint:
    requires = [MetricsCollector, AlertDetector]
    api:
      endpoint "GET /stream/metrics" -> SSE
      endpoint "GET /api/metrics/history" -> TimeseriesData
    invariants:
      invariant "Send heartbeat every 15 seconds"
      invariant "Reconnect on connection drop"
    artifacts = ["app/sse.py"]

  module DashboardUI:
    requires = [MetricsCollector]
    api:
      endpoint "GET /dashboard" -> HTML
    invariants:
      invariant "HTMX handles live updates"
      invariant "Fallback to polling if SSE unavailable"
    artifacts = ["app/dashboard.py", "templates/dashboard.html"]

  pipeline "Deploy":
    step Implement:
      modules = ["SSEEndpoint", "DashboardUI"]
      output = code
      gate = "Updates visible within 1 second"
```

## Integration Patterns

### Third-Party API Client

```sodl
system "PaymentAPIClient":
  stack:
    language = "Python 3.12"
    http = "httpx"
    retry = "tenacity"
  
  intent:
    primary = "Robust client for payment gateway API"
    outcomes = [
      "Process payments with retry logic",
      "Handle webhooks for payment status",
      "Implement circuit breaker pattern",
      "Support idempotent operations"
    ]

  policy Reliability:
    rule "Retry failed requests with exponential backoff" severity=critical
    rule "Open circuit breaker after 5 consecutive failures" severity=high
    rule "Use idempotency keys for all requests" severity=critical
    rule "Timeout requests after 30 seconds" severity=high

  interface PaymentGateway:
    method charge(amount: Decimal, payment_method: str) -> PaymentResult
    method refund(payment_id: str, amount: Decimal) -> RefundResult
    method get_status(payment_id: str) -> PaymentStatus
    method verify_webhook(signature: str, payload: str) -> bool

  module PaymentClient:
    implements = [PaymentGateway]
    exports = [PaymentGateway]
    config:
      base_url = "https://api.payment-gateway.com"
      timeout_seconds = 30
      max_retries = 3
    invariants:
      invariant "Include API key in all requests"
      invariant "Generate idempotency key per request"
      invariant "Log all API interactions"
    artifacts = ["app/clients/payment.py"]

  module WebhookHandler:
    requires = [PaymentGateway]
    api:
      endpoint "POST /webhooks/payment" -> Empty (200)
    invariants:
      invariant "Verify webhook signature"
      invariant "Process webhooks idempotently"
    artifacts = ["app/webhooks.py"]

  pipeline "Production":
    step Implement:
      modules = ["PaymentClient", "WebhookHandler"]
      output = code
      gate = "Handle gateway downtime gracefully"
```

## Testing Patterns

### Complete Test Suite Example

```sodl
system "TestableApp":
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    testing = ["pytest", "pytest-asyncio", "pytest-cov"]
    mocking = "pytest-mock"
  
  intent:
    primary = "Application with comprehensive test coverage"
    outcomes = [
      "Unit tests for all modules",
      "Integration tests for APIs",
      "E2E tests for critical flows",
      "Achieve 90% code coverage"
    ]

  policy Testing:
    rule "All modules have unit tests" severity=high
    rule "All endpoints have integration tests" severity=high
    rule "Critical paths have E2E tests" severity=critical
    rule "Maintain test coverage above 85%" severity=high

  module APIModule:
    requires = [DataService]
    api:
      endpoint "POST /api/data" -> Response
      endpoint "GET /api/data/{id}" -> Response
    acceptance:
      test "creates resource successfully"
      test "returns 404 for missing resource"
      test "validates input schema"
      test "handles database errors"
    artifacts = ["app/api.py", "tests/test_api.py"]

  module DataService:
    implements = [DataService]
    exports = [DataService]
    acceptance:
      test "stores data correctly"
      test "retrieves data by ID"
      test "handles concurrent access"
      test "maintains referential integrity"
    artifacts = ["app/service.py", "tests/test_service.py"]

  module IntegrationTests:
    owns = ["API integration tests", "Database integration tests"]
    acceptance:
      test "full CRUD workflow completes"
      test "error responses have correct format"
      test "authentication flow works"
    artifacts = ["tests/integration/test_api_integration.py"]

  module E2ETests:
    owns = ["End-to-end tests"]
    acceptance:
      test "complete user journey succeeds"
      test "handles error scenarios gracefully"
    artifacts = ["tests/e2e/test_flows.py"]

  pipeline "CI":
    step RunUnitTests:
      output = tests
      gate = "All unit tests pass"
    
    step RunIntegrationTests:
      output = tests
      gate = "All integration tests pass"
    
    step RunE2ETests:
      output = tests
      gate = "All E2E tests pass"
    
    step CheckCoverage:
      gate = "Coverage >= 85%"
```

---

## Usage Patterns

### Pattern: Repository + Service + API

This pattern separates data access, business logic, and API layers.

```sodl
interface Repository:
  method create(entity: Entity) -> Entity
  method read(id: UUID) -> Optional[Entity]
  method update(id: UUID, updates: dict) -> Entity
  method delete(id: UUID) -> bool

interface Service:
  method process(input: Input) -> Output
  method validate(input: Input) -> ValidationResult

module RepositoryImpl:
  implements = [Repository]
  exports = [Repository]

module ServiceImpl:
  implements = [Service]
  exports = [Service]
  requires = [Repository]

module API:
  requires = [Service]
  api:
    endpoint "POST /resource" -> Response
```

### Pattern: Event-Driven Architecture

```sodl
interface EventBus:
  method publish(event: Event) -> None
  method subscribe(event_type: str, handler: Callable) -> None

module Producer:
  requires = [EventBus]
  invariants:
    invariant "Publish events after transaction commits"

module Consumer:
  requires = [EventBus]
  invariants:
    invariant "Process events idempotently"
```

### Pattern: CQRS (Command Query Responsibility Segregation)

```sodl
interface CommandHandler:
  method handle(command: Command) -> CommandResult

interface QueryHandler:
  method handle(query: Query) -> QueryResult

module WriteAPI:
  requires = [CommandHandler]
  api:
    endpoint "POST /resource" -> CommandResponse

module ReadAPI:
  requires = [QueryHandler]
  api:
    endpoint "GET /resource" -> QueryResponse
```

---

For more detailed explanations, see `SODL_DOCUMENTATION.md`.
For quick syntax lookup, see `SYNTAX_REFERENCE.md`.
