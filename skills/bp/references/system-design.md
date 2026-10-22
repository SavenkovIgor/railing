# System Design Validation

Evaluate system architecture and design decisions against fundamental engineering principles.
Surface any violations and explain the trade-offs.

## Principles

### Idempotency

Running the same operation multiple times must produce the same result as running it once.

Check for:

- Operations that mutate state without idempotency guards
- Side effects that compound on repeated execution
- Missing deduplication or at-least-once delivery handling

### Distributed Systems

Design distributed systems to be observable:

- Logs: levelled and timestamped, with component context in standard/widespread format (consider JSON)
- Metrics: numeric measurements over time, with dimensions for filtering and aggregation
- Traces: end-to-end request flows across services, including timing and metadata

Generate a trace ID at the request edge and propagate it through downstream services.

### Durability class

The design must state, or let the reader infer, whether the system is disposable or durable.
Rate four factors:

- Consequences: the harm if the system fails.
- Replacement cost: the time to rebuild the system from scratch.
- Dependencies: the people and other systems that rely on it.
- Maintenance cost: the effort to keep it running over time.

A system is disposable only when all four factors are low. Otherwise it is durable.
When the factors are unclear, treat the system as durable.

Check for:

- No stated or inferable durability class (important)
- A durable system whose design omits the checks under Operational Requirements (important)
- A disposable system whose design adds rollback, SLOs, or multi-environment release machinery (style)
- Isolation claimed as the reason a system is disposable (no customer data, no inbound calls from production systems) without a mechanism that enforces it (important)

### Operational Requirements

For durable systems, check:

- Release model: How changes reach users, how to roll them back, and whether versions remain compatible during deployment.
- Availability and recovery: Availability targets, critical failure points, and RTO/RPO where relevant.
- Failure behavior: How the system handles unavailable dependencies, timeouts, and overload.
- Observability: Whether available signals reveal issues and help locate their cause.
