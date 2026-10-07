# Published Standards Reference

Analyzes the code in context and produces a prioritized report of applicable published standards and widely-adopted practices.

## Output

- Technology inventory: languages, frameworks, protocols, patterns detected in the code.
- Standards map: for each detected technology, the published standards that apply.
- Compliance gap list: what the code already satisfies and what it violates or omits.
- Prioritized checklist: actionable items with standard reference, rationale, and verification steps.

## Standard Catalog

### Coding Style & Language Standards

| Standard                        | Trigger                              |
|---                              |---                                   |
| PEP 8 – Style Guide for Python  | Python files present                 |
| PEP 257 – Docstring Conventions | Python files with functions/classes  |
| PEP 484 – Type Hints            | Python files, esp. public APIs       |
| Google C++ Style Guide          | C/C++ files present                  |
| MISRA C:2012                    | Embedded / safety-critical C code    |
| CERT C Coding Standard          | C/C++ code with manual memory or I/O |
| ISO/IEC 9899:2018 (C18)         | Any C code                           |
| ISO/IEC 14882:2020 (C++20)      | Any C++ code                         |
| ESLint Airbnb Style Guide       | JavaScript / TypeScript files        |
| Google TypeScript Style Guide   | TypeScript files                     |

### API & Protocol Standards

| Standard                                 | Trigger                                |
|---                                       |---                                     |
| RFC 9110 – HTTP Semantics                | HTTP servers, clients, or middleware   |
| RFC 9112 – HTTP/1.1                      | HTTP/1.1 wire format                   |
| RFC 9113 – HTTP/2                        | HTTP/2 usage                           |
| RFC 7807 – Problem Details for HTTP APIs | REST APIs returning errors             |
| RFC 8259 – JSON                          | Any JSON serialization                 |
| OpenAPI Specification 3.x                | REST API definitions                   |
| RFC 6749 – OAuth 2.0                     | Authorization flows                    |
| RFC 7519 – JWT                           | Token-based auth                       |
| RFC 7517 – JWK                           | Key management in auth                 |
| RFC 3986 – URI                           | URL construction or parsing            |
| RFC 4122 – UUID                          | ID generation                          |
| ISO 8601 – Date and Time                 | Date/time serialization                |
| gRPC / Protocol Buffers                  | gRPC services or .proto files          |
| GraphQL Specification                    | GraphQL schemas or resolvers           |
| WebSocket RFC 6455                       | WebSocket connections                  |
| AMQP 1.0 – ISO/IEC 19464                 | Message queue usage                    |
| OpenTelemetry Specification              | Tracing, metrics, logs instrumentation |
| Semantic Versioning 2.0.0                | Package/API versioning                 |
| Keep a Changelog                         | Changelog files                        |

### Security Standards

| Standard                       | Trigger                                      |
|--------------------------------|--------------------------------------        |
| OWASP Top 10                   | Any web application code                     |
| OWASP API Security Top 10      | REST/GraphQL/gRPC APIs                       |
| OWASP ASVS 4.0                 | Applications requiring formal security level |
| OWASP Cheat Sheet Series       | Specific attack surface patterns detected    |
| CERT Secure Coding (Java)      | Java code                                    |
| NIST SP 800-53 Rev 5           | Federal/regulated systems                    |
| NIST SP 800-190                | Container / Docker usage                     |
| CWE Top 25                     | General vulnerability patterns               |
| RFC 8446 – TLS 1.3             | TLS configuration                            |
| RFC 7525 – TLS Recommendations | TLS cipher/cert setup                        |
| NIST SP 800-63B                | Authentication / password handling           |

### Systems & Architecture Standards

| Standard                               | Trigger                                                    |
|--------------------------------------- |--------------------------------------                      |
| 12-Factor App                          | Any server-side application                                |
| POSIX.1-2017 (IEEE Std 1003.1-2017)    | POSIX system calls, shell scripts                          |
| ISO/IEC 25010 – Software Quality Model | Architecture / quality attribute decisions                 |
| IEEE 830 – SRS / Requirements          | Requirements or spec documents in repo                     |
| C4 Model (Simon Brown)                 | Architecture diagrams or docs                              |
| Richardson Maturity Model              | REST API design level assessment                           |
| CAP Theorem                            | Distributed system with consistency/availability tradeoffs |
| The Reactive Manifesto                 | Async / reactive architecture                              |

### Data & Persistence Standards

| Standard                           | Trigger                             |
|---------------------------------   |-------------------------------------|
| SQL:2016 – ISO/IEC 9075            | SQL queries or schema definitions   |
| RFC 5321 – SMTP                    | Email sending logic                 |
| RFC 5322 – Internet Message Format | Email header/body construction      |
| RFC 4180 – CSV                     | CSV file parsing or generation      |
| RFC 8785 – JSON Canonicalization   | Deterministic JSON for signing      |
| OpenID Connect 1.0                 | SSO / identity layer over OAuth 2.0 |

## Procedure

1. Inventory the code.
   - Read the files in context.
   - Detect: languages, frameworks, libraries, configuration formats, protocols, communication patterns, auth mechanisms, data formats.
   - List every detected technology as a candidate for standard mapping.

2. Map technologies to standards.
   - For each detected technology, consult the catalog above.
   - Select standards whose applicability trigger matches.
   - For each selected standard record:
     - `standard_id`: short name and reference
     - `trigger_match`: which technology or pattern triggered inclusion
     - `scope`: which files or code sections are in scope
     - `priority`: blocking | important | informational

3. Assess compliance for each standard.
   - Read the code against the standard's key requirements.
   - Classify each requirement as:
     - `compliant`: code satisfies the requirement
     - `violation`: code clearly contradicts the requirement
     - `gap`: requirement is missing or unverifiable from current context
     - `not-applicable`: requirement does not apply to this code's scope
   - Record evidence: file, line or pattern that supports the classification.

4. Prioritize findings.
   - `blocking`: standard violation that introduces security risk, data loss risk, or protocol incompatibility with external systems.
   - `important`: deviation from the standard that reduces interoperability, maintainability, or correctness.
   - `informational`: style or convention gap; low risk but worth tracking.

5. Build the checklist.
   - For each `violation` or `gap` with priority `blocking` or `important`:
     - Item title (one line)
     - Standard reference (name + URL)
     - What the standard requires
     - What the code does instead (with file/line if available)
     - How to verify compliance after the fix (command, test, or manual check)

6. Report what is already compliant.
   - List standards that were checked and satisfied - gives confidence baseline.

## Branching Logic

- If the code uses a technology not in the catalog:
  - Search for the primary published specification for that technology.
  - Add it to the ad-hoc section of the report with source link.
  - Apply the same assessment procedure.

- If the code is in a safety-critical domain (embedded, medical, aviation, automotive):
  - Escalate to MISRA, DO-178C, IEC 62443, or ISO 26262 as appropriate.
  - Flag for human review - do not make compliance claims for these without expert sign-off.

- If context is limited (only a snippet, no imports visible):
  - Narrow to standards that can be evaluated from visible code only.
  - Mark all technology-detection-dependent standards as `not-verifiable` and explain why.

- If a focus area argument was provided (e.g., `security`, `API`):
  - Prioritize the matching catalog domains.
  - Still report other domains briefly if high-severity issues are found.
