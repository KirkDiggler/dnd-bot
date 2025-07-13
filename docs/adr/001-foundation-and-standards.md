# ADR-001: Foundation and Standards

## Status
Accepted

## Context
We are building `dnd-bot`, an API gateway and game orchestration service that enables tabletop RPG experiences across multiple interfaces (Discord, web, mobile). This service acts as the bridge between game engines (starting with rpg-toolkit) and user interfaces, providing real-time multiplayer gameplay.

After experiencing architectural debt in dnd-bot-discord (issue #316), we recognize the critical importance of establishing clear boundaries, patterns, and standards from the beginning. This ADR establishes the foundational decisions that will guide all future development.

## Decision

### 1. Mission Statement
> **dnd-bot provides a real-time API gateway for tabletop RPG sessions, enabling consistent game experiences across any interface while leveraging rpg-toolkit as the core game engine.**

Key principles:
- **Interface Agnostic**: Discord, web, mobile, CLI - all equal citizens
- **Real-time First**: Built for live, multiplayer gameplay
- **Engine Powered**: rpg-toolkit handles game mechanics; we handle orchestration
- **Ruleset Flexible**: D&D 5e today, other systems tomorrow

### 2. Architectural Standards

#### Separation of Concerns
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   UI Clients    │────▶│    dnd-bot      │────▶│   rpg-toolkit   │
│ (Discord, Web)  │ API │  (Orchestrator) │uses │  (Game Engine)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

- **dnd-bot**: Session management, real-time streaming, persistence, API gateway
- **rpg-toolkit**: Game mechanics, rules engine, dice, conditions, effects
- **UI Clients**: Presentation and user interaction only

#### API-First Design
- All functionality exposed through gRPC APIs
- Protocol buffers define the contract
- gRPC streaming for real-time updates
- No client has special access - Discord uses same APIs as web

#### Package Boundaries
Each package must have:
1. Clear, single responsibility documented in README.md
2. Well-defined interfaces (no concrete type dependencies)
3. Its own test suite with coverage goals
4. No circular dependencies

### 3. Development Standards

#### Documentation Requirements
- **ADRs**: Record architectural decisions with status, context, decision, consequences
- **Journey Docs**: Capture exploration, questions, "dragons" encountered
- **Package READMEs**: Purpose, usage, examples, boundaries
- **API Documentation**: Generated from protobuf definitions

#### Code Standards
- **100% test coverage** for core packages (services, engine integration)
- **80% test coverage** for API handlers
- **Pre-commit hooks**: fmt, mod tidy, lint, test
- **No magic strings**: All constants defined and typed
- **Error handling**: Wrapped errors with context
- **Logging**: Structured logging with correlation IDs

#### Testing Philosophy
- **Integration over unit tests** where possible
- **Real dependencies** when safe (Redis, Postgres in tests)
- **Mock external services** (Discord API, third-party APIs)
- **Table-driven tests** for comprehensive coverage
- **Testify suite** for test organization

### 4. Technology Choices

#### Core Stack
- **Language**: Go (consistency with rpg-toolkit)
- **API**: gRPC with protobuf
- **Real-time**: gRPC streaming + Redis pub/sub
- **Storage**: PostgreSQL (game state) + Redis (cache/real-time)
- **Web Framework**: None - gRPC-gateway handles HTTP

#### Dependencies
- **rpg-toolkit**: Core game engine (our own)
- **grpc-go**: Google's gRPC implementation
- **testify**: Test framework
- **mockery**: Mock generation
- **golang-migrate**: Database migrations

### 5. Project Organization

```
dnd-bot/
├── api/proto/          # API contracts
├── internal/           # Private application code
│   ├── services/       # Business logic orchestration
│   ├── grpc/          # gRPC implementations
│   ├── storage/       # Persistence layer
│   └── engine/        # rpg-toolkit integration
├── pkg/               # Public packages (if any)
├── web/               # React companion app
├── cmd/               # Application entrypoints
└── docs/              # ADRs, journey docs
```

### 6. Operational Standards

#### Observability
- Structured logging with correlation IDs
- Metrics for all gRPC endpoints
- Distributed tracing for request flow
- Health checks for all dependencies

#### Deployment
- Single binary deployment
- Configuration through environment variables
- Graceful shutdown handling
- Rolling updates without dropping connections

## Consequences

### Positive
- Clear boundaries prevent scope creep and architectural drift
- API-first enables multiple UIs without duplication
- rpg-toolkit integration provides proven game mechanics
- Documentation standards ensure knowledge preservation
- Test standards ensure reliability and refactoring confidence

### Negative
- More upfront design work than a monolithic approach
- API versioning complexity as system evolves
- Integration testing requires more setup
- Documentation requirements add development overhead

### Risks and Mitigations
- **Risk**: Over-engineering for current needs
  - **Mitigation**: Start with minimal viable API, expand based on real usage
- **Risk**: rpg-toolkit changes breaking our integration
  - **Mitigation**: Pin versions, comprehensive integration tests
- **Risk**: Real-time complexity for web clients
  - **Mitigation**: Provide both streaming and polling options

## References
- rpg-toolkit architecture: Event-driven game engine design
- dnd-bot-discord issue #316: Lessons learned from architectural debt
- gRPC best practices: https://grpc.io/docs/guides/
- Go project layout: https://github.com/golang-standards/project-layout