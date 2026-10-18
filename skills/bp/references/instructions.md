# Instructions Files Audit Checks

For each `*.instructions.md`, check:

| Code | Check                          | Rule                                                                                                                                                                                            |
|------|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FM01 | `applyTo` present              | Scoped instructions MUST have `applyTo` with a valid glob pattern                                                                                                                               |
| FM02 | `name` present                 | Should have explicit `name` for discoverability                                                                                                                                                 |
| FM03 | `description` present          | Should describe the scope and intent of the instructions                                                                                                                                        |
| SC01 | Scope appropriateness          | Glob in `applyTo` should match the content (e.g., Python rules on `**/*.py`, not on `**/*`)                                                                                                     |
| SC02 | Not too broad                  | Instructions applying to `**/*` should be truly universal; language-specific rules must be scoped                                                                                               |
| CT01 | Content is actionable          | Principles must translate to observable behavior; vague aphorisms without examples score lower                                                                                                  |
| CT02 | Examples present               | For non-trivial rules, a bad/good code example strongly improves LLM compliance                                                                                                                 |
| CT03 | No project-specific hardcoding | Paths, repo names, or feature names that change per project must not appear in user-level instructions (`.copilot/`). Repo-level instructions (`.github/`) MAY contain project-specific content |
