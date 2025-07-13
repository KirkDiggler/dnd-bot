# Claude AI Development Guidelines

## Code Patterns & Style

### Type Safety Guidelines
- **Use typed structs over maps**: Instead of `map[string]int` for ability scores, use a strongly typed struct
- **Use typed constants**: Define constants for string values (e.g., ability names, damage types)
- **Use `any` over `interface{}`**: With Go 1.18+, prefer `any` for better readability
- **Avoid magic strings**: All string literals should be defined as constants

```go
// ❌ BAD: Magic strings and untyped maps
abilities := map[string]int{"strength": 10, "dexterity": 14}

// ✅ GOOD: Typed struct and constants
type AbilityScores struct {
    Strength     int
    Dexterity    int
    Constitution int
    Intelligence int
    Wisdom       int
    Charisma     int
}

// ✅ GOOD: Typed constants for string values
const (
    AbilityStrength     = "strength"
    AbilityDexterity    = "dexterity"
    AbilityConstitution = "constitution"
    AbilityIntelligence = "intelligence"
    AbilityWisdom       = "wisdom"
    AbilityCharisma     = "charisma"
)
```

### Constructor Pattern
Always use config structs with validation:
```go
type ServiceConfig struct {
    Repository Repository
    Client     ExternalClient
    Logger     Logger
}

func (c *ServiceConfig) Validate() error {
    if c.Repository == nil {
        return errors.New("repository is required")
    }
    // ... more validation
    return nil
}

func NewService(cfg *ServiceConfig) (*Service, error) {
    if err := cfg.Validate(); err != nil {
        return nil, err
    }
    return &Service{
        repo:   cfg.Repository,
        client: cfg.Client,
        logger: cfg.Logger,
    }, nil
}
```

### Repository Pattern
- **Storage Agnostic**: Repositories define interfaces, not implementations
- **Pluggable Adapters**: Redis today, DynamoDB tomorrow, user's choice
- **One Repository Per Domain Model**: SessionRepository for Session, CharacterRepository for Character
- **Data Models for Persistence**: Separate structs for storage representation

```go
// Domain model - business logic
type Session struct {
    ID      string
    Name    string
    Players []Player
}

// Repository interface - storage agnostic
type SessionRepository interface {
    Get(ctx context.Context, id string) (*Session, error)
    Save(ctx context.Context, session *Session) error
    List(ctx context.Context, opts ListOptions) ([]*Session, error)
}

// Redis implementation (one of many possible)
type redisSessionRepository struct {
    client *redis.Client
}

// Could also have: dynamoSessionRepository, mongoSessionRepository, etc.
```

### Service Layer
- **Business Logic Lives Here**: Services contain ALL business logic
- **Orchestration**: Services coordinate between repositories, external APIs, and domain models
- **Keep It Simple Elsewhere**: Handlers and repositories should be dumb
- **Single Source of Truth**: If business logic is scattered, you're doing it wrong

Example of proper separation:
```go
// ✅ GOOD: Handler just delegates
func (h *Handler) CreateSession(req Request) {
    session, err := h.service.CreateSession(req.ToInput())
    if err != nil {
        return h.handleError(err)
    }
    return h.respond(session)
}

// ✅ GOOD: All logic in service
func (s *Service) CreateSession(input CreateSessionInput) (*Session, error) {
    // Validation
    if err := s.validateSessionInput(input); err != nil {
        return nil, err
    }
    
    // Business logic
    session := &Session{
        ID:   generateID(),
        Name: input.Name,
    }
    
    // Orchestration
    if err := s.repo.Save(ctx, session); err != nil {
        return nil, err
    }
    
    // Publish events
    s.publisher.Publish(SessionCreatedEvent{SessionID: session.ID})
    
    return session, nil
}
```

### gRPC Handler Pattern
- **Thin Wrappers**: gRPC handlers are thin wrappers around services
- **Proto to Domain**: Convert protobuf types to domain types
- **Error Mapping**: Convert domain errors to gRPC status codes

```go
func (s *grpcServer) CreateSession(ctx context.Context, req *pb.CreateSessionRequest) (*pb.Session, error) {
    // Convert proto to domain
    input := protoToDomain(req)
    
    // Call service
    session, err := s.service.CreateSession(ctx, input)
    if err != nil {
        return nil, toGRPCError(err)
    }
    
    // Convert domain to proto
    return domainToProto(session), nil
}
```

### Error Handling
```go
// Define errors at package level
var (
    ErrSessionNotFound = errors.New("session not found")
    ErrPlayerNotInSession = errors.New("player not in session")
)

// Wrap with context
return fmt.Errorf("failed to get session %s: %w", id, ErrSessionNotFound)
```

### Testing Approach
- **Testify Suite**: Use `suite.Suite` for test organization
- **Real Redis When Possible**: Test with real Redis using testcontainers or miniredis
- **Mock External APIs**: Mock only external dependencies
- **Table-driven Tests**: For comprehensive test coverage

### Package Organization
```
/cmd/server/                # Main entry point
/internal/
  /domain/                  # Domain models and interfaces
    /session/               # Session aggregate
      - session.go          # Domain model
      - repository.go       # Repository interface
  /repositories/            # Repository implementations
    /redis/                 # Redis adapters
      - session.go
    /dynamodb/              # DynamoDB adapters (future)
      - session.go
  /services/                # Service layer
    /session/               # Session service
      - service.go
      - service_test.go
  /grpc/                    # gRPC layer
    /server/                # gRPC server setup
    /handlers/              # gRPC service implementations
      - session.go
  /engine/                  # rpg-toolkit integration
    - adapter.go            # Adapts rpg-toolkit to our needs
/api/proto/                 # Protobuf definitions
  /v1/
    - session.proto
    - common.proto
```

### Development Workflow
**ALWAYS** work in branches:
```bash
# Create feature branch
git checkout -b feat/session-management

# Create fix branch  
git checkout -b fix/storage-flexibility

# Create docs branch
git checkout -b docs/api-documentation
```

### Pre-commit Workflow
**ALWAYS** run before committing:
```bash
make pre-commit
```
This runs:
1. `go fmt` - Format code
2. `go mod tidy` - Clean dependencies  
3. Linter - Catch common issues
4. Unit tests - Ensure nothing broken

### Storage Philosophy
- **No Database Preferences**: Users choose their storage
- **Repository Pattern**: Enables storage flexibility
- **Start with Redis**: Simple, fast, good enough for MVP
- **Add Adapters as Needed**: PostgreSQL, DynamoDB, MongoDB - user's choice

### gRPC Best Practices
- **Streaming for Real-time**: Use server streaming for live updates
- **Versioned APIs**: Put protos in versioned directories (v1, v2)
- **Clear Service Boundaries**: One service per domain concept
- **Status Codes**: Map domain errors to appropriate gRPC codes

### Documentation Standards
- **ADRs for Decisions**: Document the "why" behind architectural choices
- **Journey Docs for Learning**: Capture exploration and dragons encountered
- **Package READMEs**: Each package explains its purpose and boundaries
- **Proto Comments**: Document all RPC methods and messages

## Remember
- Keep it simple - don't over-engineer
- Storage flexibility is key - no database lock-in
- When in doubt, follow existing patterns
- All code changes go through branches and PRs
- Test with real dependencies when safe (Redis)
- Document the journey, not just the destination