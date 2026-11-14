---
name: Global Agent Instructions
applyTo: '**/*'
---

# Global Agent Instructions

## Challenge & Critique

**Do not default to agreement. Correctness over agreeableness.**

- Before implementing, check whether the requested approach fits the problem well
- Flag over-engineering, premature abstraction, or misdiagnosed problems when there is a concrete reason to do so
- When something seems off in the architecture, naming, or approach, say so clearly instead of silently complying
- When critiquing, explain *why* and suggest a concrete alternative when possible

## Tooling priority

If a skill covers the task, follow it instead of building your own procedure. The skill decides what to do; the tiers below decide how to run each step, including the steps of a skill.

Use the narrowest tool built for the action. Move to a broader tool only when the narrower one lacks a capability the step needs, and name that capability before the call. The tiers below run from narrowest to broadest:

1. Tasks from `.vscode/tasks.json`. Build, test, lint, and run the project through a defined task, not by typing the same command in the terminal. Read `.vscode/tasks.json` for the labels. If the task-running tool is not in your tool list, it is usually deferred: find it with tool search (query: `run VS Code task`) before you fall back to the console.
2. Dedicated tools. Use the tool built for the action: IDE tools for search, file reads, edits, diagnostics, and test runs; a web fetch tool for pages; an MCP tool for GitHub.
3. Console. Use `run_in_terminal` as a last resort.

✘ `curl` to read a page, `sed -i` to edit a file
✔ the web fetch tool, the edit tool

Why: a broader tool costs the user more review. A task is checked in advance, and a dedicated tool call shows its effect at a glance. A console command has to be read and understood before the user can approve it.

### Console calls

Expect the user to stop any console call that is not obvious at a glance. If the user cannot verify a command in a few seconds, they interrupt it rather than review it.

- Before a console call, name the narrower tools you tried and why they did not fit.
- Write one short command per call, with well-known tools and common flags. Agents tend to chain commands with pipes, `&&`, and `;` into one line; split such a line into separate calls.
- If the user interrupts a console call, ask what to do next or go back to a narrower tool. Agents tend to retry the same action as a reworded command; an interrupt means no, not "try another form".

**`run_in_terminal` for read-only filesystem operations is FORBIDDEN.** Use the substitution table below instead:

| Instead of | Use |
|---|---|
| `ls`, `find` | `Explore` subagent or `read_file` on the directory |
| `grep`, `rg` | `Explore` subagent with a targeted query |
| `cat`, `head`, `tail` | `read_file` |
| `wc`, `stat` | `Explore` subagent |

Creating git worktrees from the console is FORBIDDEN. ALWAYS create a worktree with an IDE tool (the IDE's built-in worktree support); `git worktree add` in `run_in_terminal` is not permitted, even as a fallback. If no IDE tool can do it, stop and ask instead of using the console.

## Missing instructions and skills

If a needed instruction file, skill, or agent is not in your context, do not search the disk for it (home, plugin caches, other repositories). Stop, tell the user what is missing, name the likely cause (plugin not enabled, IDE did not attach it), propose a fix (check the plugin, reload the window), and ask whether to continue without it.

## Efficiency

Each request re-reads the whole conversation, so cost scales with steps and context size, not effort - cut steps and bulky tool output, never the depth of the work itself.

- Batch independent lookups (reads, searches, diagnostics) into one round of parallel tool calls. A second round is only for questions the first round's answers raised.
- When manually rechecking a long-running command that has no auto notification on completion (e.g. `get_task_output`, re-running `get_errors` after a build), use exponential backoff - 2s, 4s, 8s, 16s, capped at 32s - instead of tight polling.
