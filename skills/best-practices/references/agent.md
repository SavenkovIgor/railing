# Agent Files Best Practices

Checks for `*.agent.md` files. Every check is pass/fail; cite findings by ID.

- FM01 The frontmatter has a non-empty `description` and a `tools` list.
  Why: the agent picker chooses an agent by `description`; without `tools`, nobody can check
  what the agent may do.
- TL01 `tools` holds only the tools the role of the agent needs. An agent that must not edit
  files or run commands has no tool for it.
  Why: the agent can ignore a ban in the prompt, but it cannot use a tool it does not have.
- RL01 The agent links rules from instruction files and skills in `## DependsOn` instead of
  copying them. An agent without such rules needs no `## DependsOn`.
  Why: a copied rule drifts from its source.
