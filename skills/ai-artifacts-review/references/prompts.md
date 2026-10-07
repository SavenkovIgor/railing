# Prompt Files Audit Checks

For each `*.prompt.md`, check:

| Code | Check                           | Rule                                                                                                                                                                                  |
|------|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FM01 | `name` present                  | Optional but strongly recommended; without it the prompt is invoked only by filename                                                                                                  |
| FM02 | `description` present           | Required for the prompt to appear in Copilot's command palette with a useful description                                                                                              |
| FM03 | `argument-hint` present         | Required when the prompt accepts user input; explains what to pass                                                                                                                    |
| FM04 | `tools` declared                | Should list tools the prompt needs; prevents silent tool-unavailability failures                                                                                                      |
| FM05 | `agent` mode declared           | `ask`, `agent`, or `plan` - must match the prompt's complexity (plan-level tasks need `agent: "Plan"`)                                                                                |
| CT01 | No hardcoded ephemeral context  | Build branch numbers, temporary file paths, or sprint-specific names must not be embedded in reusable prompts                                                                         |
| CT02 | Output file extensions correct  | If the prompt creates files, the extension must match the file type (`.instructions.md` is reserved for instruction files auto-loaded by Copilot; specs must use `.md` or `.spec.md`) |
| CT03 | Scope matches abstraction level | A prompt named generically (e.g., `arch-overview`) must not contain Chromium-specific checklist items unless scoped to Chromium projects                                              |
| CT04 | Prompts vs skills boundary      | If the prompt has conditional logic, branching, quality gates, or multi-step procedures with loops - it should be a skill, not a prompt                                               |
