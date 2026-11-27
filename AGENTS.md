# Agent guide for this repository

## Scopes of instructions

Instruction files nest by `applyTo`. Any two scopes either do not overlap, or one contains the other, so the scopes form one tree. One scope can hold several files on different topics. Files in the same scope are siblings.

The list starts at the root. Each scope lists its files, then the scopes inside it:

- `**/*`
  - [global.instructions.md](/com.github.copilot/rules/global.instructions.md) - how the agent works and answers on any task
  - [issues.instructions.md](/com.github.copilot/rules/issues.instructions.md) - scope of one issue in any tracker
  - [system-layout.instructions.md](/com.github.copilot/rules/system-layout.instructions.md) - default places of skills, instructions, and plugins on the user's system
  - `**/*.md`
    - [markdown.instructions.md](/com.github.copilot/rules/markdown.instructions.md) - checks (`MD*`) on the form of any markdown file
    - [prose.instructions.md](/com.github.copilot/rules/prose.instructions.md) - how the text reads
    - `**/{AGENTS.md,SKILL.md,*.instructions.md,*.agent.md}`
      - [context-files.instructions.md](/com.github.copilot/rules/context-files.instructions.md) - how context files link to each other, where a rule lives, and how a requirement reads
    - `notes/**/*.md`
      - [notes.instructions.md](/com.github.copilot/rules/notes.instructions.md) - path, task ID, and language of any note in `notes/`
      - `notes/**/*.overview.md`
        - [reports.instructions.md](/com.github.copilot/rules/reports.instructions.md) - content checks for notes about existing code
        - [reports-overview.instructions.md](/com.github.copilot/rules/reports-overview.instructions.md) - structure of an overview report
      - `notes/**/*.plan.md`
        - [plans.instructions.md](/com.github.copilot/rules/plans.instructions.md) - how a plan changes
  - `**/*.{h,hpp,cc,cpp,cppm,ipp,py,js,ts}`
    - [code.instructions.md](/com.github.copilot/rules/code.instructions.md) - coding principles for any language
    - `**/*.{cpp,hpp,cppm,ipp,h,cc}`
      - [code-cpp.instructions.md](/com.github.copilot/rules/code-cpp.instructions.md) - coding style in C++
    - `**/*.py`
      - [code-python.instructions.md](/com.github.copilot/rules/code-python.instructions.md) - coding style in Python

Nesting is a required property of this tree. A new instruction file joins the scope equal to its own. If no such scope exists, the file opens a new scope inside the narrowest scope that contains its own. A file whose scope partly overlaps another scope breaks the nesting.

A wider scope holds the shared base. A file holds only what differs from the files whose scope contains its own, or what adds to them. It does not restate their rules. An example in the language of the file can show how a rule of a wider scope looks there.

Why: `applyTo` already gives the reader of a file every file whose scope contains its own, so the file needs only the difference.

## Where a duplicated rule stays

When the same rule appears in an instruction file and in a skill, keep it in the instruction. By default, remove it from the skill.

Why: an instruction applies by default through `applyTo`, while a skill applies only when someone invokes it.

## Link paths

Two cases are specific to this plugin:

- A skill that links to another skill or to a plugin file with a leading `/` works only inside this plugin. It is not standalone.
- A path in a manifest or `mcp.json` starts with `./` from the plugin root, as the Agent Plugins specification requires.
  ✔ `./skills/`
  ✘ `skills/`

Why: a leading `/` resolves from the repository root on GitHub and from the workspace root in VS Code. No specification defines how each agent reads it, and nobody has verified it yet.

## Checking links

To check a link, look at the file system inside the repository. The target file must exist at the written path. An anchor must match a heading in that file. Do this by hand, with file listing and reading tools.

- Do not write a script, a tool, or a CI step for it.
- Do not check external URLs. Assume they work.

Why: a link check is a quick look, not a project. A script grows a list of exceptions and costs more to maintain than the broken links it finds.

## Editing skills and this guide

This rule covers every `SKILL.md`, every markdown file inside a skill directory, and this `AGENTS.md`. After you edit such a file, check it against [markdown.instructions.md](/com.github.copilot/rules/markdown.instructions.md) and [prose.instructions.md](/com.github.copilot/rules/prose.instructions.md), each as a whole. Do this before the commit, and fix every failure in the same pull request.

Why: the editor attaches these files by `applyTo`. An agent that edits through a shell or a sub-agent can lack them in its context. A failure found in review costs a round trip.

## Pull request workflow

In every pull request to this repository, the first commit contains only the version bump in [plugin.json](/plugin.json). Make all other changes in later commits.

Why: the bump then does not depend on the rest of the change, and a reviewer sees the new version at once.

## Size of an issue and its pull request

Keep the body of an issue within 50 lines. Plan each issue so that its pull request changes at most 50 lines. Count added plus removed lines in the diff, without the version bump. When a draft issue, a planned pull request, or a pull request in progress goes over the limit, suggest a split to the user. Each part becomes its own issue with its own pull request.

A pull request that only moves or deletes text can go over the limit. If you split a move, the rule stays in two places, or in none, between the two merges.

Ask the user for at most two decisions in one issue, with the recommended option first. When an issue needs more decisions, split it.

Why: the user works in slots of one or two minutes. In one slot, the user makes one or two decisions and then approves the merge. A change in this repository edits rules in prose, not logic, and a reviewer reads each changed line as a rule. A short diff with few decisions fits one slot and lets the reviewer check every rule it changes.

## Closing issues from a pull request

Add a closing line to the pull request description only for a GitHub issue that the user gives in the conversation. Put the line on its own, outside any list or quote:

```text
Closes #123
```

For several issues, write one closing line per issue, each with its own keyword.

Why: GitHub closes an issue on its own only when two conditions hold. The pull request merges into the default branch, and a closing keyword in the description links the two.
