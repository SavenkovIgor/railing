# Agent guide for this repository

## Scopes of instructions

Instruction files nest by `applyTo`. Any two scopes either do not overlap, or one contains the other, so the scopes form one tree. One scope can hold several files on different topics; files in the same scope are siblings.

Scopes from the root down; each scope lists its files, then the scopes inside it:

- `**/*`
  - [global.instructions.md](/com.github.copilot/rules/global.instructions.md) - how the agent works and answers on any task
  - [issues.instructions.md](/com.github.copilot/rules/issues.instructions.md) - scope of one issue in any tracker
  - `**/*.md`
    - [markdown.instructions.md](/com.github.copilot/rules/markdown.instructions.md) - checks (`MD*`) on the form of any markdown file
    - [prose.instructions.md](/com.github.copilot/rules/prose.instructions.md) - how the text reads
    - `notes/**/*.md`
      - [notes.instructions.md](/com.github.copilot/rules/notes.instructions.md) - path, task ID, and language of any note in `notes/`
      - `notes/**/*.overview.md`
        - [reports.instructions.md](/com.github.copilot/rules/reports.instructions.md) - content checks for notes about existing code
        - [reports-overview.instructions.md](/com.github.copilot/rules/reports-overview.instructions.md) - structure of an overview report
  - `**/*.{h,hpp,cc,cpp,cppm,ipp,py,js,ts}`
    - [code.instructions.md](/com.github.copilot/rules/code.instructions.md) - coding principles for any language
    - `**/*.{cpp,hpp,cppm,ipp,h,cc}`
      - [code-cpp.instructions.md](/com.github.copilot/rules/code-cpp.instructions.md) - coding style in C++
    - `**/*.py`
      - [code-python.instructions.md](/com.github.copilot/rules/code-python.instructions.md) - coding style in Python

Nesting is a required property of this tree. A new instruction file joins the scope equal to its own, or opens a new scope inside the narrowest scope that contains its own. A file whose scope partly overlaps another scope breaks the nesting.

A wider scope holds the shared base. A file holds only what differs from the files whose scope contains its own or adds to them, and does not restate their rules. An example in the language of the file may show how a rule of a wider scope looks there.

Why: `applyTo` already gives the reader of a file every file whose scope contains its own, so the file needs only the difference.

## How rule files refer to each other

There are three kinds of dependencies. Each has its own place:

- Inside a skill, between its own files: described by the skill standard, not by this guide.
- Between instruction files: given by the nesting of `applyTo`, with no links.
- Between different skills, or from a skill to an instruction file: listed in the `## DependsOn` section. Only this kind goes there.

Rules for links:

- An instruction file never links to another instruction file or to a skill. `applyTo` nesting already applies every file whose scope contains its own, and the editor does this on its own; rely on that behavior.
- A skill links to every instruction file and skill it depends on, once, in a `## DependsOn` section directly after the goal paragraph. A skill applies each linked file as a whole.
- A link in a routing table, where a skill picks one target by the input, is not a dependency and stays where it is.
- Files must not form circular links: if A links to B, B must not link back to A, directly or through a chain of other files.
- A file never copies, summarizes, or cites single rules of another file, neither by text nor by ID, and never links to it later in the document.

Why: a copied or cited rule drifts from its source, and a reader who follows a link to one rule skips the rest of that file. An instruction attaches by `applyTo` on its own, while a skill runs only when invoked, so an instruction that depends on a skill depends on something that may not be loaded. A skill can run before the file it works on is in the context, so `applyTo` has not attached anything yet; a link is the lesser evil there.

## Where a duplicated rule stays

When the same rule appears in an instruction file and in a skill, remove it from the skill by default and keep it in the instruction.

Why: an instruction applies by default through `applyTo`, while a skill applies only when someone invokes it.

## Link paths

Two cases are specific to this plugin:

- A skill that links to another skill or to a plugin file with a leading `/` works only inside this plugin; it is not standalone.
- A path in a manifest or `mcp.json` starts with `./` from the plugin root, as the Agent Plugins specification requires.
  ✔ `./skills/`
  ✘ `skills/`

Why: a leading `/` resolves from the repository root on GitHub and from the workspace root in VS Code; how each agent reads it is not specified and not yet verified.

## Checking links

Check that a link works by looking at the file system inside the repository: the target file exists at the written path, and an anchor matches a heading in that file. Do this by hand, with file listing and reading tools.

- Do not write a script, a tool, or a CI step for it.
- Do not check external URLs; assume they work.

Why: a link check is a quick look, not a project. A script grows a list of exceptions and costs more to maintain than the broken links it finds.

## Editing skills and this guide

An edit to any `SKILL.md`, to a markdown file inside a skill directory, or to this `AGENTS.md` requires a check of the edited file against [markdown.instructions.md](/com.github.copilot/rules/markdown.instructions.md) and [prose.instructions.md](/com.github.copilot/rules/prose.instructions.md), each as a whole. Do this before the commit, and fix every failure in the same pull request.

Why: the editor attaches these files by `applyTo`, but an agent that edits through a shell or a sub-agent may not have them in context, and a failure found in review costs a round trip.

## Phrasing of requirements

State each requirement positively: say what to do. Add a prohibition ("not here, not there") only when LLMs make that mistake in practice, and name the mistake.

Why: a prohibition for an error that never happens costs tokens and clutters the context of both the model and the human reader. Break the rule when a mistake is costly and likely enough to justify the extra line.

## Pull request workflow

In every pull request to this repository, the first commit contains only the version bump in [plugin.json](/plugin.json). Make all other changes in later commits.

Why: the bump then does not depend on the rest of the change, and a reviewer sees the new version at once.

## Size of an issue and its pull request

Keep the body of an issue within 50 lines. Plan each issue so that its pull request changes at most 50 lines: added plus removed lines in the diff, without the version bump. When a draft issue, a planned pull request, or a pull request in progress goes over the limit, suggest that the user split the issue into several issues, each with its own pull request.

A pull request that only moves or deletes text may go over the limit. Splitting a move leaves the rule in two places, or in none, between the two merges.

Ask the user for at most two decisions in one issue, with the recommended option first. When an issue needs more decisions, split it.

Why: the user works in slots of one or two minutes: take a couple of decisions, then approve the merge. A change in this repository edits rules in prose, not logic, and a reviewer reads each changed line as a rule. A short diff with few decisions fits one slot and lets the reviewer check every rule it changes.

## Closing issues from a pull request

Only when the user gives a GitHub issue in the conversation, the pull request description names that issue in a closing line. Put the line on its own, outside any list or quote:

```text
Closes #123
```

For several issues, write one closing line per issue, each with its own keyword.

Why: GitHub closes an issue on its own only when the pull request merges into the default branch and a closing keyword in the description links the two.
