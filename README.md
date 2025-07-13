# dnd-bot

> **Real-time API gateway for tabletop RPG sessions, enabling consistent game experiences across any interface while leveraging rpg-toolkit as the core game engine.**

## Vision

dnd-bot serves as the orchestration layer between game engines and user interfaces, making tabletop RPGs accessible anywhere - Discord, web browser, mobile app, or even CLI. By separating game mechanics (via rpg-toolkit) from presentation, we enable rich, real-time multiplayer experiences without duplicating logic across platforms.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   UI Clients    │────▶│    dnd-bot      │────▶│   rpg-toolkit   │
│ (Discord, Web)  │ API │  (Orchestrator) │uses │  (Game Engine)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Core Responsibilities

- **Session Management**: Create and manage multiplayer game sessions
- **Real-time Updates**: Stream game state changes to all connected clients
- **API Gateway**: Provide consistent gRPC API for all client types
- **State Persistence**: Save and restore game sessions
- **Rule Orchestration**: Coordinate between UI actions and game engine

### What This Is NOT

- **Not a game engine**: rpg-toolkit handles mechanics, rules, dice
- **Not a UI**: Clients handle presentation and user interaction
- **Not ruleset-specific**: Built to support any tabletop RPG system

## Getting Started

### Prerequisites

- Go 1.21+
- PostgreSQL 15+
- Redis 7+
- protoc 3.x with Go plugins

### Development Setup

```bash
# Clone the repository
git clone https://github.com/KirkDiggler/dnd-bot.git
cd dnd-bot

# Install dependencies
go mod download

# Run tests
make test

# Run the server
make run
```

### Pre-commit Workflow

**Always** run before committing:
```bash
make pre-commit
```

This ensures:
- Code is formatted (`go fmt`)
- Dependencies are tidy (`go mod tidy`)
- Linting passes
- Tests pass

## Project Structure

```
dnd-bot/
├── api/proto/          # gRPC API definitions
├── internal/           # Private application code
│   ├── services/       # Business logic orchestration
│   ├── grpc/          # gRPC service implementations
│   ├── storage/       # Persistence layer
│   └── engine/        # rpg-toolkit integration
├── cmd/               # Application entrypoints
├── web/               # React companion app
└── docs/              # Architecture decisions and journey logs
```

Each package includes a README explaining its purpose and boundaries.

## Documentation

- **[Architecture Decision Records](docs/adr/)**: Understand why we built it this way
- **[Journey Documents](docs/journey/)**: Learn from our exploration and challenges
- **[API Documentation](docs/api/)**: Generated from protobuf definitions

## Milestones

### Phase 1: Foundation ✅
- [x] Core architecture decisions (ADR-001)
- [ ] Basic gRPC server setup
- [ ] rpg-toolkit integration
- [ ] Session management

### Phase 2: Real-time Combat
- [ ] Combat state management
- [ ] Turn order and initiative
- [ ] Action processing
- [ ] Real-time updates via streaming

### Phase 3: Hex Grid Maps
- [ ] Hex grid domain model
- [ ] Token movement and positioning
- [ ] Fog of war
- [ ] Line of sight calculations

### Phase 4: Multi-client Support
- [ ] Discord bot integration
- [ ] React web app
- [ ] State synchronization
- [ ] Conflict resolution

## Design Principles

1. **API-First**: Every feature starts with API design
2. **Real-time Default**: Built for live, multiplayer gameplay  
3. **Interface Agnostic**: No client gets special treatment
4. **Test Everything**: 100% coverage for core packages
5. **Document the Journey**: ADRs, journey docs, and clear READMEs

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

Key points:
- Follow established patterns (see [ADR-001](docs/adr/001-foundation-and-standards.md))
- Write tests for everything
- Document your decisions
- Keep packages focused and bounded

## Related Projects

- [rpg-toolkit](https://github.com/yourusername/rpg-toolkit): Core game engine
- [dnd-bot-discord](https://github.com/KirkDiggler/dnd-bot-discord): Discord-specific renderer

## License

MIT License - see [LICENSE](LICENSE) file for details