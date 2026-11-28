---
name: to-issues
description: >-
    You should use this skill when: breaking down a plan into tasks,
    converting a discussion into actionable issues, splitting a proposal
    into tickets, creating issues from meeting notes or design decisions.
    Works with any issue tracker.
---

# To issues

Decompose the preceding plan, discussion, or proposal into discrete, actionable
issues and file them in the project's issue tracker.

## DependsOn

- [issues.instructions.md](/com.github.copilot/rules/issues.instructions.md)

## Procedure

### 1. Identify the Tracker

Find the issue tracker of the project from the context, and a tool that files issues in it.
If either is unclear, ask the user before proceeding.

### 2. Extract Issues from Context

For each distinct unit of work, extract a title (one action sentence), a body
(context, acceptance criteria, links), labels (bug, feat, chore), and a size.
Flag an issue that is large enough for sub-tasks. Each issue must be
independently completable. Keep the nuance of the discussion.

### 3. Confirm Before Filing

Present the full list and wait for explicit approval before creating anything.
See [output formats](references/output-formats.md) for the expected layout.
If the user asks to edit, adjust and confirm again.

### 4. Create the Issues

File each issue using the appropriate tool. Prefer batch APIs when available.
See [output formats](references/output-formats.md) for the summary table format.

### 5. Optional - Link Issues

If the tracker supports epics, milestones, or parent issues, and the created
issues form a natural group, offer to link them. Link them only after the user agrees.
