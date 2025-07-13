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

#### Layered Architecture
We are a **data-powered API**, the API version of rpg-toolkit. Our architecture enforces strict layering:

```
┌─────────────────────────────────────────────────────┐
│                   gRPC Layer                        │
│  - Proto definitions (external contract)            │
│  - Proto ↔ Domain conversion                        │
│  - gRPC error mapping                               │
├─────────────────────────────────────────────────────┤
│                 Service Layer                       │
│  - Business logic orchestration                     │
│  - Transaction boundaries                           │
│  - Domain model operations                          │
├─────────────────────────────────────────────────────┤
│                Repository Layer                     │
│  - Storage interfaces                               │
│  - Domain ↔ Data model conversion                   │
│  - Query logic                                      │
├─────────────────────────────────────────────────────┤
│              Storage Adapters                       │
│  - Redis, DynamoDB, PostgreSQL, etc.               │
│  - User's choice of implementation                  │
└─────────────────────────────────────────────────────┘
```

**Layer Principles:**
1. **Protos are External**: Proto definitions can evolve independently of internal models
2. **Domain Models are Internal**: Service layer uses rich domain models, not protos
3. **No Context Mixing**: Each layer only knows about the layer directly below it
4. **Interface Boundaries**: Every layer interaction happens through interfaces
5. **Mockable by Design**: Each layer generates its own mocks for testing

**Example Layer Separation:**
```go
// Proto (external contract)
message CreateSessionRequest {
    string name = 1;
    string dm_id = 2;
}

// Domain (internal model)
type Session struct {
    ID        string
    Name      string
    DM        *Player
    Players   []*Player
    State     SessionState
    CreatedAt time.Time
}

// Service (orchestration)
type SessionService interface {
    CreateSession(ctx context.Context, input CreateSessionInput) (*Session, error)
}

// Repository (storage)
type SessionRepository interface {
    Save(ctx context.Context, session *Session) error
    FindByID(ctx context.Context, id string) (*Session, error)
}
```

**Conversion Pattern:**
- gRPC handlers convert proto → domain
- Services operate on domain models
- Repositories convert domain → storage models
- Each conversion is explicit and testable

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

#### Conversion Patterns
**Proto to Domain:**
```go
// in grpc handler
func (s *grpcServer) CreateSession(ctx context.Context, req *pb.CreateSessionRequest) (*pb.Session, error) {
    // Convert proto to domain input
    input := CreateSessionInput{
        Name: req.Name,
        DMID: req.DmId,
    }
    
    // Call service with domain types
    session, err := s.service.CreateSession(ctx, input)
    if err != nil {
        return nil, toGRPCError(err)
    }
    
    // Convert domain to proto response
    return &pb.Session{
        Id:        session.ID,
        Name:      session.Name,
        DmId:      session.DM.ID,
        State:     pb.SessionState(session.State),
        CreatedAt: timestamppb.New(session.CreatedAt),
    }, nil
}
```

**Domain to Storage:**
```go
// in repository implementation
func (r *redisSessionRepository) Save(ctx context.Context, session *Session) error {
    // Convert domain to storage model
    data := sessionData{
        ID:        session.ID,
        Name:      session.Name,
        DMID:      session.DM.ID,
        PlayerIDs: extractPlayerIDs(session.Players),
        State:     string(session.State),
        CreatedAt: session.CreatedAt.Unix(),
    }
    
    // Store using adapter-specific logic
    return r.client.Set(ctx, "session:"+session.ID, data, 0).Err()
}
```

**Benefits of This Pattern:**
- API can evolve without breaking internal models
- Storage can change without affecting business logic
- Each layer is independently testable
- Clear separation of concerns

#### Testing Philosophy
- **Integration over unit tests** where possible
- **Real dependencies** when safe (Redis in tests)
- **Mock external services** (Discord API, third-party APIs)
- **Table-driven tests** for comprehensive coverage
- **Testify suite** for test organization

### 4. Technology Choices

#### Core Stack
- **Language**: Go (consistency with rpg-toolkit)
- **API**: gRPC with protobuf
- **Real-time**: gRPC streaming + Redis pub/sub
- **Storage**: Repository pattern with adapters (Redis for initial implementation)
- **Web Framework**: None - gRPC-gateway handles HTTP

#### Dependencies
- **rpg-toolkit**: Core game engine (our own)
- **grpc-go**: Google's gRPC implementation
- **testify**: Test framework
- **mockery**: Mock generation
- **Storage adapters**: Pluggable based on deployment needs

### 5. Project Organization

```
dnd-bot/
├── api/proto/v1/       # API contracts (external, versioned)
│   ├── session.proto   # Session management
│   ├── dice.proto      # Dice rolling service
│   └── common.proto    # Shared types
├── internal/           # Private application code
│   ├── domain/         # Domain models and interfaces
│   │   ├── session/    # Session aggregate
│   │   └── player/     # Player aggregate
│   ├── services/       # Business logic orchestration
│   │   ├── session/    # Session service
│   │   └── game/       # Game orchestration
│   ├── grpc/           # gRPC layer
│   │   ├── handlers/   # gRPC service implementations
│   │   └── converters/ # Proto ↔ Domain converters
│   ├── repositories/   # Repository implementations
│   │   ├── redis/      # Redis adapters
│   │   └── memory/     # In-memory for testing
│   ├── storage/        # Storage interfaces
│   └── engine/         # rpg-toolkit integration
├── pkg/                # Public packages (if any)
├── web/                # React companion app
├── cmd/server/         # Application entrypoint
└── docs/               # ADRs, journey docs
```

**Package Responsibilities:**
- `api/proto`: External API contract, can evolve independently
- `internal/domain`: Core business entities, pure Go structs
- `internal/services`: Business logic, uses domain models
- `internal/grpc`: API layer, converts between proto and domain
- `internal/repositories`: Storage implementations, pluggable
- `internal/engine`: Integrates rpg-toolkit for game mechanics

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
- Layered architecture enables independent evolution of API, business logic, and storage
- Repository pattern allows users to choose their preferred storage backend
- Interface-driven design makes the system highly testable and modular
- Proto/domain separation protects internal models from external API changes

### Negative
- More upfront design work than a monolithic approach
- API versioning complexity as system evolves
- Integration testing requires more setup
- Documentation requirements add development overhead
- Conversion code between layers adds boilerplate
- Multiple models (proto, domain, storage) for same concept
- Learning curve for developers new to layered architecture

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