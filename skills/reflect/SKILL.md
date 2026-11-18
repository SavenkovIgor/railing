---
name: reflect
description: >-
  You should use this skill when:
  a task is completed,
  a session is long: its context was compacted, it made dozens of tool calls,
  the agent started repeating earlier steps,
  or more than half of the context window is used when a token counter is visible,
  or when a scheduled or manual review of recent agent sessions is requested,
  to reflect on the sessions, propose the 3 most important improvements
  to AI context files that would improve speed or quality next time,
  and record the run in a journal of reviewed sessions and decisions
---

# Reflect

Review agent sessions and propose the 3 most important small fixes for the
harness: AI context files such as instructions (`AGENTS.md`, `*.instructions.md`),
skills via `SKILL.md`, agents via `*.agent.md`, MCP config like `mcp.json`,
ignored-files rules like `.gitignore`/`.cursorignore`, feature-specific
instruction hooks in settings, and the railing plugin itself.
A fix should help reach the same result a little faster or with better quality.
Focus only on improving AI context files and guidance quality.
If a lack of information is relevant only to one specific case,
do not add it to shared context files.

Also analyze whether the sessions included redundant context that did not help,
or context that is too narrow and over-specific for reusable project-level guidance.
If found, propose how to trim or generalize that context.

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
Read and write it with the file tools; create the file if it is missing.

- Append one JSON line per run, after the user has decided on every proposal:
  `date`, `sessions` (each with `id` and `failed`, the list of failed criteria),
  `failures` (the number of sessions that failed each criterion),
  `coverage` (the share of reviewed sessions where at least one skill was invoked), and `proposals`
  (each with `file`, `text`, and `decision`: `applied`, `skipped`, or `undecided`).
- Do not propose again a fix that an earlier entry marks `skipped`,
  unless a new session gives new evidence for it; then cite that session.

## Scope of the review

- By default, review every session of the last 48 hours that no journal entry lists,
  not only the current one.
  Find them through the session history tools, narrowing by date first,
  and read only the turns needed to understand a problem.
- List sessions with `list_sessions` (`createdAfter` set to 48 hours ago), read each with
  `get_session_context` at `detail: summary`, and open `digest` with a small
  `transcriptLimit` only for turns that show a problem. Report sessions whose
  transcript comes back empty as unreadable instead of skipping them silently.
- `digest` lists only tool names; to judge console calls, open `full` with
  `transcriptLimit` of 2 or less only for turns whose digest shows `powershell`
  or `run_in_terminal`.
- Review only the current conversation when the user explicitly asks for it.
- Review at most 20 sessions per run, oldest first, so that older sessions are reviewed
  before they leave the 48-hour window. The rest wait for the next run.
- If no unreviewed session is left, tell the user so and stop.
- Skip sessions of this skill itself, so a review does not analyze earlier reviews.
- A proposal cites the evidence, such as the session and the step, but not secrets,
  credentials, or personal data from the sessions.

## Session assessment

Check each session against 4 criteria. A session fails when it fails at least one;
give the reason in 1-3 sentences that name the failed criteria and the step.

- Efficiency: the agent reached the result without extra steps, repeats, or unique console calls.
- Instruction compliance: the agent followed the instructions and skills in its context.
- Result quality: the user accepted the result without asking to redo it.
- Verbosity: the answers and tool output were no longer than the task needed.

## Cases to look for

Pay most attention to cases where an agent did not do what was expected
or did it inefficiently: ignored an instruction, took extra steps, repeated itself,
or asked the user for something it could find out itself.

### Unique console calls

The user must approve manually every console call that auto-approve does not cover,
so keep approvals few and treat every unique console call with suspicion.

- A generic call such as `git status` is not a problem: it is easy to auto-approve.
- A unique call is a problem: a custom script written for one narrow task,
  a long pipe chain, or an inline `python`/`node` one-liner. It almost certainly
  needed a manual approval.
- For each unique call, check it against the tooling priority: which narrower tool
  could have done the job, and why was it not used? Also flag a general tool used
  where a dedicated one exists, such as `curl` instead of web fetch.
  Find out why the unique approach was needed and what would make it unnecessary.
- If the project has `.vscode/tasks.json` and the agent typed the same command
  in the console, or never searched for the task-running tool, flag it as a missed task.
- Propose the cheapest fix: a clearer instruction, a new task, a missing tool,
  or an auto-approve entry for a call that is generic but missing from the list.

### Skills that did not fire

When an installed skill covered the task of a failed session but the agent did not invoke it,
the cause is usually its `description`. Compare the description with the user's request
and propose a description change that would have matched it.

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

## Proposals

- Propose exactly 3, ranked by importance. Base each one on a failed session;
  the proposal for this skill itself may rely on the current review run instead.
- Each proposal names one concrete file and gives the exact new text.
  Keep it small: 1-3 sentences. A proposal can also move an instruction to
  another file or delete it.
- A proposal can also create a new skill when no installed skill covers a task
  that failed sessions repeat: give its `name` and `description`.
- Before the proposals, print one summary line: the number of reviewed sessions,
  the number of failed sessions with the count per criterion, and the skill coverage.
- Show the proposals in the chat.
- Then ask the user about each proposal through the dialog tool (`ask_user`)
  with options such as apply, edit, skip, or discuss. Apply only what the user accepts.
- If the dialog tool is unavailable, print the proposals and stop without editing
  any file except the journal; mark every proposal `undecided`.
- At least one of the proposals improves this skill itself: a missing check,
  an unclear step, or a wasted step that the review run showed.
  Count it among the 3; if nothing real turns up, name the closest weak spot
  of the skill instead of skipping it.
