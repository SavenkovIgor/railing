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

### Operational Requirements

For relevant designs, check:

- Release model: How changes reach users, how to roll them back, and whether versions remain compatible during deployment.
- Availability and recovery: Availability targets, critical failure points, and RTO/RPO where relevant.
- Failure behavior: How the system handles unavailable dependencies, timeouts, and overload.
- Observability: Whether available signals reveal issues and help locate their cause.
