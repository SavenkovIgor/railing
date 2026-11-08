# Agent Files Best Practices

Checks for `*.agent.md` files. Every check is pass/fail; cite findings by ID.

## Frontmatter

- FM01 The frontmatter has a non-empty `description` and a `tools` list.
  Why: the agent picker and a parent agent choose an agent by `description`, and without
  `tools` the file does not state which tools the agent gets, so nobody can check them.

## Tools

- TL01 The `tools` list matches the role of the agent: it holds the tools the role needs and no
  tool for work outside the role. An agent whose role excludes an action, such as editing files
  or running commands, has no tool for that action.
  Why: the agent can ignore a restriction in the prompt; it cannot use a tool it does not have.

  ✘ A review agent says "Edit no files" and has a tool that edits files
  ✔ A review agent has only the tools it needs to read, search, and report

## Rules

- RL01 The agent attaches each rule from an instruction file or a skill by a link in a
  `## DependsOn` section and does not copy or restate the rule. An agent that depends on no
  such file needs no `## DependsOn`.
  Why: a copied rule drifts from its source.

  ✘ The body repeats the commit message rules of a skill
  ✔ `## DependsOn` links the skill, and the body adds only what the agent does differently
