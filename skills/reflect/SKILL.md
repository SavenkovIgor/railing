---
name: reflect
description: >-
  You should use this skill when:
  a task is completed,
  a session is long: its context was compacted, it made dozens of tool calls,
  the agent started repeating earlier steps,
  or more than half of the context window is used when a token counter is visible,
  to reflect on the conversation and propose 2-3 improvements to AI context files
  that would improve speed or quality next time
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
- Whether the run showed one of the context failure modes below

## Context management

A larger context window does not make an agent more reliable. The more tokens the window holds,
the less reliably the model uses any of them, because attention is a finite budget. Treat the
context as a resource to spend, and check the conversation for the four failure modes below.
Each fix works by removing information, so propose it as a rule that keeps the window lean.

| Failure mode | Symptom in the conversation | Fix | Candidate artifact change |
|--------------|-----------------------------|-----|---------------------------|
| Poisoning | A wrong conclusion was saved, then treated as fact | Validate | Require a real check, such as a test or a command, before a conclusion goes into notes or memory |
| Distraction | A long history made the agent repeat old actions | Compact | Move long-lived state into files and pull it in on demand; summarize old steps |
| Confusion | Too many tools or docs made the agent choose wrongly | Curate | Give each skill or agent only the tools its job needs; load the rest on request |
| Clash | The window holds two versions of the same fact | Prune | Delete the superseded version, or restart the window from the corrected state |

Notes for the proposals:

- Compaction is lossy, and a summary of a summary drifts; prefer files over repeated summaries
- Prefer a fresh window with a restated current state over patching a poisoned one
- Tool definitions cost context even when unused, so also check the MCP and tool configuration
- Large tool results, such as file dumps, test output, and schema dumps, usually fill the window;
  propose narrower reads, filters, or output limits


And yes, you can propose new items in this prompt itself if you think it is necessary
Maybe I missed something important that could improve the results and
simplify the process for you
