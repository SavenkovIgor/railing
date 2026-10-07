# Railing

Engineering guardrails that keep AI coding agents on track.

## Contents

```text
├── plugin.json
├── rules/
└── skills/
```

### Plugin manifest

[`plugin.json`](./plugin.json) defines the plugin name, version, description,
and Agent Plugins schema.

For native Cursor plugin discovery, the same manifest is also available at
[`.cursor-plugin/plugin.json`](./.cursor-plugin/plugin.json). Cursor requires
this exact `.cursor-plugin/plugin.json` path for its native plugin format.
When it properly support `plugin.json` at root, this file will be removed

### Rules

- [`global.instructions.md`](./rules/global.instructions.md) - general agent
  behavior and workflow guidance.
- [`global-code.instructions.md`](./rules/global-code.instructions.md) - shared
  coding principles for C++, Python, JavaScript, and TypeScript.
- [`api-cpp.instructions.md`](./rules/api-cpp.instructions.md) - C++ API
  development guidance.
- [`api-python.instructions.md`](./rules/api-python.instructions.md) - Python
  API development guidance.
- [`reports.instructions.md`](./rules/reports.instructions.md) - universal
  requirements for agent-written reports in `reports/`.
- [`reports-overview.instructions.md`](./rules/reports-overview.instructions.md) -
  structure and checks for `*.overview.md` reports.

### Skills

- [`ai-artifacts-review`](./skills/ai-artifacts-review) - audit AI
  configuration artifacts.
- [`bp`](./skills/bp) - validate files against best-practice references.
- [`code-overview`](./skills/code-overview) - document code architecture and
  data flow.
- [`debug-context-artifacts`](./skills/debug-context-artifacts) - inspect the
  initial AI context state.
- [`design-system`](./skills/design-system) - create or audit design systems.
- [`migration-skill-factory`](./skills/migration-skill-factory) - create
  skills for codebase migrations.
- [`reflect`](./skills/reflect) - propose context improvements after a task.
- [`report-review`](./skills/report-review) - clean up a report and verify it
  against the code.
- [`report-write`](./skills/report-write) - write a technical report about
  existing code into `reports/`.
- [`tech-writing`](./skills/tech-writing) - write and review developer
  documentation.
- [`to-issues`](./skills/to-issues) - convert plans and discussions into
  tracker issues.
