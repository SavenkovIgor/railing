---
name: reflect
description: "You SHOULD use this skill after completing a task to reflect on the conversation and propose 2–3 improvements to AI context files that would improve speed or quality next time."
user-invocable: true
---

# Reflect

Check all the previous conversation and propose 2-3 fixes for AI context files
(for example: instructions like `AGENTS.md` and `*.instructions.md`,
commands like `*.prompt.md`, skills via `SKILL.md`, agents via `*.agent.md`,
MCP config like `mcp.json`, ignored-files rules like `.gitignore`/
`.cursorignore`, and feature-specific instruction hooks in settings)
that could help you achieve the same result but
a little bit faster or with better quality. Focus only on improving AI context
files and guidance quality. If there was some lack of information that is
relevant only to this specific case, it is not necessary to add it to shared
context files.

Also analyze whether the task included redundant context that did not help solve it,
or context that is too narrow and over-specific for reusable project-level guidance.
If found, propose how to trim or generalize that context.

## Possible points to focus

- It could be lack of documentation in some class and therefore you should
  seek for external docs
- It could be the prompt that lack some information and user should provide more details
  that are really match to the prompt on abstraction level
- It could be the missed info in feature documentation or missing feature completely
- It could be too long search of necessary code in the codebase and the search
  recommendations could be slightly improved
- It could be excessive context in the task that adds noise but does not improve
  the quality of the solution
- It could be context that is too detailed for one tiny part of the system and
  unlikely to be broadly useful across similar tasks
- What context instructions could instead be expressed as a validation code or with project validation tool to replace
  context pollution with strict algorithmic checks


And yes, you can propose new items in this prompt itself if you think it is necessary
Maybe I missed something important that could improve the results and
simplify the process for you
