# Railing

Engineering guardrails that keep AI coding agents on track.

## Contents

```text
├── plugin.json
├── com.github.copilot/
│   ├── agents/
│   └── rules/
└── skills/
```

### Plugin manifest

[`plugin.json`](/plugin.json) defines the plugin name, version, description,
and Agent Plugins schema.

VS Code reads rules and agents only from the `com.github.copilot/` directory,
so they live there.

### Rules

- [`global.instructions.md`](/com.github.copilot/rules/global.instructions.md) - general agent
  behavior and workflow guidance.
- [`global-code.instructions.md`](/com.github.copilot/rules/global-code.instructions.md) - shared
  coding principles for C++, Python, JavaScript, and TypeScript.
- [`api-cpp.instructions.md`](/com.github.copilot/rules/api-cpp.instructions.md) - C++ API
  development guidance.
- [`api-python.instructions.md`](/com.github.copilot/rules/api-python.instructions.md) - Python
  API development guidance.
- [`markdown.instructions.md`](/com.github.copilot/rules/markdown.instructions.md) - formatting
  checks for all `*.md` files.
- [`reports.instructions.md`](/com.github.copilot/rules/reports.instructions.md) - universal
  requirements for agent-written reports in `reports/`.
- [`reports-overview.instructions.md`](/com.github.copilot/rules/reports-overview.instructions.md) -
  structure and checks for `*.overview.md` reports.

### Agents

- [`engineering-maturity`](/com.github.copilot/agents/engineering-maturity.agent.md) -
  engineering maturity advisor.
- [`gilfoyle`](/com.github.copilot/agents/gilfoyle.agent.md) - blunt code
  review and analysis.
- [`report-reviewer`](/com.github.copilot/agents/report-reviewer.agent.md) -
  review reports against the code.
- [`report-writer`](/com.github.copilot/agents/report-writer.agent.md) - write
  technical reports about existing code.

### Skills

- [`ai-artifacts-review`](/skills/ai-artifacts-review) - audit AI
  configuration artifacts.
- [`bp`](/skills/bp) - validate files against best-practice references.
- [`debug-context-artifacts`](/skills/debug-context-artifacts) - inspect the
  initial AI context state.
- [`design-system`](/skills/design-system) - create or audit design systems.
- [`migration-skill-factory`](/skills/migration-skill-factory) - create
  skills for codebase migrations.
- [`reflect`](/skills/reflect) - propose context improvements after a task.
- [`report-review`](/skills/report-review) - clean up a report and verify it
  against the code.
- [`report-write`](/skills/report-write) - write a technical report about
  existing code into `reports/`, including architecture and data-flow
  overviews (kind `overview`).
- [`tech-writing`](/skills/tech-writing) - write and review developer
  documentation.
- [`to-issues`](/skills/to-issues) - convert plans and discussions into
  tracker issues.
