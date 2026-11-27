---
name: reflect
description: >-
  Use this skill after a task is completed, after a long session,
  or when a scheduled or manual review of recent agent sessions is requested.
  A session is long when its context was compacted or the agent made dozens of tool calls.
  A session is also long when the agent repeated earlier steps
  or a visible token counter shows that more than half of the context window is used.
  The skill proposes the 4 most important improvements to AI context files
  and records the run in a journal of reviewed sessions and decisions.
---

# Reflect

Review agent sessions and propose the 4 most important small fixes for the harness.
The harness consists of AI context files: instructions (`AGENTS.md`, `*.instructions.md`),
skills (`SKILL.md`), agents (`*.agent.md`), MCP config (`mcp.json`),
ignore rules (`.gitignore`, `.cursorignore`), instruction hooks in settings,
and the railing plugin itself.
A fix helps the agent reach the same result faster or with better quality.
Improve only AI context files and guidance quality.
If only one specific case needs the missing information,
do not add it to shared context files.

Also check whether the sessions included redundant context that did not help,
or context that is too narrow for reusable project-level guidance.
If you find such context, propose how to trim or generalize it.

## DependsOn

- [global.instructions.md](/com.github.copilot/rules/global.instructions.md)

The IDE usually attaches these files through `applyTo`.
Open a link only when its file is missing from the context.

## Steps

1. Read the journal as [Journal](#journal) describes.
2. Select the sessions as [Scope of the review](#scope-of-the-review) describes.
3. Assess each session as [Session assessment](#session-assessment) describes.
4. Look for problems in the failed sessions only: [Cases to look for](#cases-to-look-for),
   [Possible points to focus](#possible-points-to-focus), and
   [Context management](#context-management).
5. Propose fixes as [Proposals](#proposals) describes.
6. Append the entry of this run to the journal.

## Journal

The journal keeps the results of earlier runs in
`~/.local/state/railing/reflect/journal.jsonl` on every platform.
Read and write it with the file tools. If the file is missing, create it.

- After the user decides on every proposal, append one JSON line per run with these fields:
  - `date`
  - `sessions`: each with `id` and `failed`, the list of failed criteria
  - `failures`: the number of sessions that failed each criterion
  - `coverage`: the share of reviewed sessions that invoked at least one skill
  - `proposals`: each with `file`, `text`, and `decision` (`applied`, `skipped`, or `undecided`)
- Do not propose a fix again when an earlier entry marks it `skipped`.
  If a new session gives new evidence, propose it and cite that session.

## Scope of the review

- By default, review every session of the last 48 hours that no journal entry lists,
  not only the current one.
  Find them with the session history tools, filter by date first,
  and read only the turns that explain a problem.
- List sessions with `list_sessions` and set `createdAfter` to 48 hours ago.
  Read each session with `get_session_context` at `detail: summary`.
  Open `digest` with a small `transcriptLimit` only for turns that show a problem.
  Report a session with an empty transcript as unreadable.
- `digest` lists only tool names. To judge console calls, open `full`
  with `transcriptLimit` of 2 or less.
  Do this only for turns whose digest shows `powershell` or `run_in_terminal`.
- If the user asks for it, review only the current conversation.
- Review at most 20 sessions per run, oldest first,
  so that no session leaves the 48-hour window unreviewed. The next run reviews the rest.
- If no unreviewed session is left, tell the user so and stop.
- Skip sessions of this skill itself, so a review does not analyze earlier reviews.
- In a proposal, cite the evidence, such as the session and the step.
  Do not include secrets, credentials, or personal data from the sessions.

## Session assessment

Check each session against 4 criteria. A session fails when it fails at least one.
Give the reason in 1-3 sentences that name the failed criteria and the step.

- Efficiency: the agent reached the result without extra steps, repeats, or unique console calls.
- Instruction compliance: the agent followed the instructions and skills in its context.
- Result quality: the user accepted the result without asking to redo it.
- Verbosity: the answers and tool output were no longer than the task needed.

## Cases to look for

Pay most attention to cases where the agent did not do what you expected
or worked inefficiently: it ignored an instruction, took extra steps, repeated itself,
or asked the user for something it could find itself.

### Unique console calls

The user must approve every console call that auto-approve does not cover.
Keep approvals few and treat every unique console call with suspicion.

- A generic call such as `git status` is not a problem. You can auto-approve it easily.
- A unique call is a problem: a custom script for one narrow task,
  a long pipe chain, or an inline `python`/`node` one-liner.
  It almost certainly needed a manual approval.
- Check each unique call against the tooling priority.
  Which narrower tool could do the job, and why did the agent not use it?
  Also flag a general tool used where a dedicated one exists, such as `curl` instead of web fetch.
  Find why the agent needed the unique approach and what would make it unnecessary.
- If the project has `.vscode/tasks.json` and the agent typed the same command
  in the console, or never searched for the task-running tool, flag a missed task.
- Propose the cheapest fix: a clearer instruction, a new task, a missing tool,
  or an auto-approve entry for a generic call that the list lacks.

### Skills that did not fire

If an installed skill covered the task of a failed session and the agent did not invoke it,
the cause is usually the skill `description`.
Compare the description with the user's request
and propose a change that would match the request.

## Possible points to focus

- A class lacks documentation, so the agent must read external docs.
- The prompt lacks details. The user should give details at the abstraction level of the prompt.
- The feature documentation lacks information, or the feature is missing.
- The agent searched too long for the code. Improve the search recommendations.
- The task contains excessive context that adds noise and does not improve the solution.
- The context is too detailed for one small part of the system
  and unlikely to help in similar tasks.
- An instruction can become validation code or a project validation tool.
  Replace context pollution with strict algorithmic checks.
- The run showed one of the context failure modes below.

## Context management

A larger context window does not make an agent more reliable.
The more tokens the window holds, the less reliably the model uses any of them,
because attention is a finite budget.
Treat the context as a resource to spend, and check the conversation for the four failure modes below.
Each fix removes information, so propose it as a rule that keeps the window lean.

| Failure mode | Symptom in the conversation | Fix | Candidate artifact change |
|--------------|-----------------------------|-----|---------------------------|
| Poisoning | A wrong conclusion was saved, then treated as fact | Validate | Require a real check, such as a test or a command, before a conclusion goes into notes or memory |
| Distraction | A long history made the agent repeat old actions | Compact | Move long-lived state into files and load it on demand. Summarize old steps |
| Confusion | Too many tools or docs made the agent choose wrongly | Curate | Give each skill or agent only the tools its job needs. Load the rest on request |
| Clash | The window holds two versions of the same fact | Prune | Delete the superseded version, or restart the window from the corrected state |

Notes for the proposals:

- Compaction is lossy, and a summary of a summary drifts. Prefer files over repeated summaries.
- Prefer a fresh window with a restated current state over patching a poisoned one.
- Tool definitions cost context even when unused, so also check the MCP and tool configuration.
- Large tool results, such as file dumps, test output, and schema dumps, usually fill the window.
  Propose narrower reads, filters, or output limits.

## Proposals

- Propose 4 fixes, ranked by importance. Base each one on a failed session.
- At least one proposal changes a skill (`SKILL.md`),
  and at least one changes an instruction file (`*.instructions.md`, `AGENTS.md`).
- When the failed sessions give no evidence for one of these two kinds,
  propose fewer fixes and say which kind had no evidence.
- Each proposal names one concrete file and gives the exact new text.
  Keep it small: 1-3 sentences. A proposal can also move an instruction to
  another file or delete it.
- If no installed skill covers a task that failed sessions repeat,
  a proposal can create a new skill. Give its `name` and `description`.
- Before the proposals, print one summary line: the number of reviewed sessions,
  the number of failed sessions with the count per criterion, and the skill coverage.
- Show the proposals in the chat.
- Then ask the user about each proposal through the dialog tool (`ask_user`)
  with options such as apply, edit, skip, or discuss. Apply only what the user accepts.
- If the dialog tool is unavailable, print the proposals and edit no file except the journal.
  Mark every proposal `undecided`.
