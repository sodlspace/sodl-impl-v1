---
title: Use Cases
description: Where SODL delivers the most value — and why.
---

SODL is useful wherever you use an AI coding agent. It becomes _especially_ effective in the situations below, where free-form prompts tend to break down.

---

## Web application scaffolding

**The problem:** AI agents guess framework conventions, file structure, and component boundaries when prompted with "build me a blog." Each follow-up prompt resets context.

**Why SODL helps:** The `module` construct enforces hard boundaries between UI, service, and data layers. The `interface` declarations tell the AI exactly what contracts each layer must satisfy before generating a single file. The AI never has to guess the structure.

```sodl
system "BlogPlatform":
  stack:
    language = "Python 3.12"
    web      = "Flask"
    database = "SQLite"

  interface PostRepository:
    method get_by_id(id: UUID) -> Optional[Post]
    method get_all(page: int, limit: int) -> List[Post]

  module BlogUI:
    requires = [PostRepository]
    api:
      endpoint "GET /"          -> HTML
      endpoint "GET /post/{id}" -> HTML
    invariants:
      invariant "Markdown is sanitized before rendering"
    artifacts = ["app/views.py", "templates/*.html"]

  module PostService:
    implements = [PostRepository]
    exports    = [PostRepository]
    artifacts  = ["app/services/posts.py"]
```

**Best for:** Full-stack apps, multi-page sites, any project with clear frontend/backend/data separation.

---

## REST API development

**The problem:** Auth strategy, error format, validation library, and HTTP status codes are decided inconsistently across prompts. The AI changes conventions between sessions.

**Why SODL helps:** `policy Security` rules lock in auth requirements before any endpoint is generated. Endpoint declarations with explicit response types (`TokenResponse`, `Empty (204)`) give the AI the exact contract for every route. `acceptance` tests in each module define what "done" means.

```sodl
system "TaskAPI":
  stack:
    language = "TypeScript"
    web      = "Hono"
    database = "PostgreSQL"
    auth     = "JWT"

  policy Security:
    rule "All endpoints require JWT validation"    severity=critical
    rule "No direct SQL string interpolation"      severity=critical
    rule "Rate limit auth endpoints to 5/min/IP"  severity=high

  module TaskAPI:
    api:
      endpoint "POST /api/tasks"       -> TaskResponse (201)
      endpoint "GET /api/tasks/{id}"   -> TaskResponse
      endpoint "DELETE /api/tasks/{id}" -> Empty (204)
    acceptance:
      test "returns 201 with task ID on creation"
      test "returns 404 for unknown task"
      test "returns 401 without valid JWT"
```

**Best for:** Any REST API where auth, validation, and error handling conventions need to be enforced project-wide.

---

## Microservices

**The problem:** With multiple services, AI agents don't know how services communicate, which events they emit, or what contracts they must fulfill. Each service gets generated in isolation.

**Why SODL helps:** `interface` declarations act as service contracts. One system spec can define the `EventPublisher` interface that the Order service must implement and the Fulfillment service requires — making the dependency explicit before either service is generated.

```sodl
system "OrderService":
  stack:
    language  = "Python 3.12"
    web       = "FastAPI"
    messaging = "RabbitMQ"

  policy Reliability:
    rule "All events published with acknowledgment"          severity=critical
    rule "Use database transactions for state changes"       severity=critical
    rule "Retry failed messages with exponential backoff"    severity=high

  interface EventPublisher:
    method publish(event: OrderEvent) -> bool

  module OrderAPI:
    requires = [EventPublisher]
    invariants:
      invariant "Emit OrderCreated event on order creation"
      invariant "Use optimistic locking for concurrent updates"

  module RabbitMQPublisher:
    implements = [EventPublisher]
    exports    = [EventPublisher]
```

**Best for:** Systems with more than two services, event-driven architectures, anything using a message bus.

---

## Data pipelines (ETL)

**The problem:** AI generates ETL code without knowing the schema validation strategy, deduplication rules, or retry behavior — leading to pipelines that break on bad data in production.

**Why SODL helps:** Pipeline `step` blocks map directly to ETL stages. `policy DataQuality` rules enforce validation and deduplication before any code is written. The `gate` field in each step means the AI cannot proceed to loading without the extraction and transformation steps being proven correct.

```sodl
system "DataETLPipeline":
  stack:
    language      = "Python 3.12"
    warehouse     = "BigQuery"
    orchestration = "Airflow"

  policy DataQuality:
    rule "Validate schema before loading"     severity=critical
    rule "Deduplicate records by unique key"  severity=critical
    rule "Quarantine invalid records"         severity=high

  pipeline "Production":
    step ExtractAndTransform:
      modules = ["ExtractorModule", "TransformerModule"]
      output  = code
      gate    = "Component tests pass with sample data"
    step Load:
      modules = ["LoaderModule"]
      output  = code
      gate    = "End-to-end test loads 1M rows without error"
```

**Best for:** Data engineering projects, batch jobs, any pipeline where data quality invariants must be enforced.

---

## CLI tooling

**The problem:** AI agents implement CLI commands with inconsistent error handling, no idempotency guarantees, and unclear responsibility boundaries.

**Why SODL helps:** CLI commands are declared in the `api` block alongside HTTP endpoints — the AI sees the full public surface of the tool upfront. `owns` declarations make responsibility explicit. Invariants like "commands are idempotent where possible" get enforced across every command, not just the ones you prompt for individually.

```sodl
system "DBMigrationCLI":
  stack:
    language = "Python 3.12"
    cli      = "Click"
    database = "PostgreSQL"

  module CLICommands:
    api:
      command "migrate"           -> None
      command "rollback [steps]"  -> None
      command "status"            -> None
    invariants:
      invariant "Commands idempotent where possible"
      invariant "Confirm destructive operations"
      invariant "Show progress for long operations"
```

**Best for:** Developer tools, build scripts, migration utilities, any CLI with multiple subcommands.

---

## Real-time systems

**The problem:** WebSocket and SSE endpoints have different lifecycle semantics from REST. AI agents often miss authentication at connection time, skip keepalive handling, or generate race conditions under concurrent connections.

**Why SODL helps:** `websocket` and `SSE` endpoint types in the `api` block signal to the AI that connection management, reconnection logic, and keepalive are required. `gate` criteria in pipeline steps enforce concurrency targets before the system is considered done.

```sodl
system "RealtimeChat":
  stack:
    language  = "Python 3.12"
    websocket = "WebSockets"
    cache     = "Redis"

  module WebSocketHandler:
    api:
      websocket "/ws/room/{room_id}" -> None
    invariants:
      invariant "Authenticate connection before accepting"
      invariant "Send ping/pong for keepalive"
      invariant "Handle disconnects gracefully"

  pipeline "Deploy":
    step Implement:
      output = code
      gate   = "Support 1000 concurrent connections"
```

**Best for:** Chat, live dashboards, notification systems, collaborative tools, any system with persistent connections.

---

## Brownfield / incremental refactoring

**The problem:** When changing an existing system, AI agents don't know which parts to leave alone. They refactor beyond the requested scope, break existing conventions, or introduce inconsistencies.

**Why SODL helps:** The `out_of_scope` field explicitly tells the AI what not to touch. `interface` contracts define the boundaries of the change — the AI implements the new interface without touching modules that aren't listed in `requires`. Template inheritance with `override`/`append`/`remove` lets you make targeted changes to a base spec without rewriting everything.

```sodl
system "LegacyAPIRefactor" extends "ExistingAPIBase":
  intent:
    primary      = "Migrate auth layer from sessions to JWT"
    outcomes     = ["Replace SessionAuth module with JWTAuth module"]
    out_of_scope = [
      "User data model changes",
      "Existing business logic modules",
      "Database schema"
    ]

  # Override only the auth implementation
  override stack.auth = "JWT"

  module JWTAuth:
    implements = [AuthService]
    exports    = [AuthService]
    artifacts  = ["app/auth/jwt.py"]
```

**Best for:** Migrating legacy systems, swapping infrastructure (auth, DB, cache), adding features to existing codebases without breaking what works.

---

## Choosing the right constructs per use case

| Use case | Key constructs | Main benefit |
|---|---|---|
| Web app scaffolding | `module`, `interface`, `artifacts` | Enforced layer boundaries |
| REST API | `policy`, `endpoint`, `acceptance` | Consistent auth + error handling |
| Microservices | `interface`, `policy Reliability`, `pipeline` | Explicit service contracts |
| Data pipelines | `pipeline step`, `gate`, `policy DataQuality` | Enforced data quality invariants |
| CLI tooling | `command`, `owns`, `invariants` | Consistent UX across commands |
| Real-time | `websocket`, `SSE`, `gate` | Connection lifecycle handled |
| Brownfield | `out_of_scope`, `override`, `template` | Scoped changes, no collateral damage |
