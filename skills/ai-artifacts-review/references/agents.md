# Agent Files Audit Checks

For each `*.agent.md`, check:

| Code | Check                           | Rule                                                                                                                                                    |
|------|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| FM01 | `name` present                  | Required for UI display                                                                                                                                 |
| FM02 | `description` present           | Should state persona, domain, and specialization in 50–150 characters                                                                                   |
| FM03 | `tools` declared                | List the tools the agent is allowed to use; avoid granting all tools to narrow-purpose agents                                                           |
| PN01 | Persona is consistent           | Language patterns, sample responses, and behavioral rules must be internally consistent                                                                 |
| PN02 | Forbidden actions are justified | Restrictions ("no code editing") must have a clear rationale and must not make the agent unhelpful for its primary use case                             |
| PN03 | Agent vs skill boundary         | An agent defines a role and toolset. If it contains a multi-step procedure or quality gates, extract those into a skill and reference it from the agent |
