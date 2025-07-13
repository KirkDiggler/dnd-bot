# Internal Packages

This directory contains the private application code for dnd-bot. Code here is not intended to be imported by other projects.

## Package Structure

### services/
Business logic orchestration layer. Services coordinate between the game engine (rpg-toolkit), storage, and API layer.

### grpc/
gRPC service implementations. These are thin wrappers that translate gRPC calls to service calls.

### storage/
Persistence layer with interfaces and implementations for PostgreSQL and Redis.

### engine/
Integration layer for rpg-toolkit. Adapts the game engine to our specific needs.

## Design Principles

1. **Clear Boundaries**: Each package has a single, well-defined responsibility
2. **Interface Dependencies**: Packages depend on interfaces, not concrete types
3. **No Circular Dependencies**: Strict layering is enforced
4. **Testability**: All packages designed for easy testing with mocks