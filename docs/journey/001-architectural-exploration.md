# Journey: Architectural Exploration

## The Beginning

This project emerged from a late-night realization while working on [dnd-bot-discord issue #316](https://github.com/KirkDiggler/dnd-bot-discord/issues/316). We had accumulated significant architectural debt - business logic scattered across packages, tight coupling between domain and ruleset-specific code, and two different state tracking systems coexisting uncomfortably.

The question arose: What if we separated the Discord bot (renderer) from the game logic entirely? What if we could play D&D through Discord, web, mobile, or even CLI - all using the same backend?

## The Vision

We imagined a world where:
- A DM runs a session from their laptop's web interface with a beautiful hex grid
- Players join from Discord on their phones during commute
- Someone switches to the web app when they get home for better visuals
- All seamlessly synchronized, all the same game

This led to recognizing that we needed:
1. A clean API gateway (dnd-bot) 
2. A solid game engine (rpg-toolkit)
3. Various renderers (Discord bot, React app, etc.)

## Dragons Encountered

### Dragon 1: Event-Driven Everything?
**Initial thought**: Make the entire system event-driven like rpg-toolkit.

**Reality check**: The Discord bot doesn't need internal events - it responds to Discord interactions. Over-engineering alert!

**Resolution**: Only the game engine (rpg-toolkit) is event-driven. The API layer (dnd-bot) uses traditional service patterns.

### Dragon 2: Where Does the Game Engine Live?
**Options considered**:
1. Embed game logic in dnd-bot
2. Expand rpg-toolkit to include game flow
3. Create separate game-engine repo

**Decision**: rpg-toolkit IS our game engine. dnd-bot orchestrates it.

**Why**: rpg-toolkit already has the event-driven architecture, dice rolling, conditions, effects - everything needed for game mechanics. Don't reinvent the wheel.

### Dragon 3: Real-time Synchronization
**Challenge**: How do we sync game state across Discord and web clients in real-time?

**Exploration**:
- WebSockets? Complex client management
- Server-Sent Events? One-way only
- gRPC streaming? Elegant but requires gRPC-Web

**Decision**: gRPC streaming with Redis pub/sub for internal distribution.

**Trade-offs**: More complex than REST, but enables rich real-time features.

## Lessons from the Past

From dnd-bot-discord's architectural debt:
1. **Scatter business logic → pain**: When character creation logic lived in 5 different packages, every change was a nightmare
2. **Tight coupling → inflexibility**: Mixing D&D 5e rules with domain logic made other rulesets impossible
3. **Multiple state systems → bugs**: Legacy bit flags + new FlowState = confusion and errors

## Architectural Epiphanies

### Separation of Concerns is Everything
```
UI (Discord/Web) → API (dnd-bot) → Engine (rpg-toolkit)
```
Each layer has ONE job. UI presents. API orchestrates. Engine computes.

### Interfaces Enable Evolution
By depending on interfaces, not implementations, we can:
- Swap PostgreSQL for DynamoDB
- Replace Redis with RabbitMQ  
- Add new rulesets without touching core code

### Documentation is a Feature
Not overhead - a feature. ADRs capture "why". Journey docs capture "how we got here". READMEs maintain focus.

## Open Questions

1. **Session Persistence**: How much state do we persist vs recompute?
2. **Conflict Resolution**: When Discord and web clients conflict, who wins?
3. **Performance**: Can we handle 100 concurrent games? 1000?
4. **Versioning**: How do we evolve APIs without breaking clients?

## Next Dragons to Slay

1. **Dragon: Hex Grid State Management**
   - Efficient storage and streaming of large maps
   - Fog of war calculations
   - Line of sight algorithms

2. **Dragon: Rule System Abstraction**
   - How to support D&D 5e today but Pathfinder tomorrow?
   - Where's the boundary between engine and ruleset?

3. **Dragon: Testing Strategy**
   - How to test real-time features?
   - Integration tests with multiple clients?
   - Load testing game sessions?

## Reflections

Building this separation between dnd-bot and dnd-bot-discord feels like finally paying down technical debt properly. Instead of refactoring in place (always dangerous), we're extracting the right abstractions.

The beauty is that rpg-toolkit remains pure - just game mechanics. dnd-bot adds the multiplayer, persistence, and API layers. And renderers like dnd-bot-discord can focus solely on user experience.

This could grow beyond our D&D games. This architecture could power any tabletop RPG system. That's exciting and terrifying.

---

*Last updated: Initial exploration and decision to separate concerns*