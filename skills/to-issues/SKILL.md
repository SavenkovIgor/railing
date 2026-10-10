---
name: to-issues
description: >-
    You should use this skill when: breaking down a plan into tasks,
    converting a discussion into actionable issues, splitting a proposal
    into tickets, creating issues from meeting notes or design decisions.
    Works with any issue tracker - infers GitHub Issues, Jira, Linear,
    GitLab, etc. from project context.
---

# To issues

Decompose the preceding plan, discussion, or proposal into discrete, actionable
issues and file them in the project's issue tracker.

## Procedure

### 1. Identify the Tracker

Inspect project context to determine where issues go:

| Signal | Tracker |
|--------|---------|
| `.github/` folder, `gh` CLI available | GitHub Issues |
| `JIRA_URL` env var, `jira` in config | Jira |
| `linear` in deps or `.linear/` config | Linear |
| `.gitlab-ci.yml`, `gitlab` remote | GitLab Issues |
| No clear signal | Ask the user before proceeding |

Use available tools (GitHub MCP, `gh` CLI, REST API, Linear SDK, etc.) to
create issues. Fall back to asking the user which tool to use if none is detected.

### 2. Extract Issues from Context

For each distinct unit of work extract: **Title** (one action sentence),
**Body** (context, acceptance criteria, links), **Labels** (bug/feat/chore),
**Size** (flag if large enough for sub-tasks). Each issue must be independently
completable; one concern per issue; preserve nuance from the discussion.

### 3. Confirm Before Filing

Present the full list and wait for explicit approval before creating anything.
See [output formats](references/output-formats.md) for the expected layout.
If the user asks to edit, adjust and confirm again.

### 4. Create the Issues

File each issue using the appropriate tool. Prefer batch APIs when available.
See [output formats](references/output-formats.md) for the `gh` command and
summary table format.

### 5. Optional - Link Issues

If the tracker supports epics, milestones, or parent issues and a natural
grouping exists, offer to link the created issues. Ask the user first; don't
create structure they didn't ask for.
