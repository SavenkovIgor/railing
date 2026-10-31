# Agent guide for this repository

## Scopes of markdown instructions

Instruction files for markdown nest by `applyTo`: the scope of each file equals or lies inside the scope of the file above it. The files do not depend on each other. Broadest scope first:

- [markdown.instructions.md](/com.github.copilot/rules/markdown.instructions.md) - `**/*.md`; checks (`MD*`) on the form of any markdown file
- [prose.instructions.md](/com.github.copilot/rules/prose.instructions.md) - `**/*.md`; how the text reads
- [notes.instructions.md](/com.github.copilot/rules/notes.instructions.md) - `notes/**/*.md`; path, task ID, and language of any note in `notes/`
- [reports.instructions.md](/com.github.copilot/rules/reports.instructions.md) - `notes/**/*.overview.md`; content checks for notes about existing code
- `reports-<kind>.instructions.md` (in the same directory) - `notes/**/*.<kind>.md`; structure of one report kind

Nesting is a required property of this list. A new instruction file for markdown goes below the narrowest file whose scope contains its own. A file whose scope is not inside the scope of the file above it breaks the nesting.

Files do not restate rules of files whose scope contains theirs.

## How rule files refer to each other

There are three kinds of dependencies. Each has its own place:

- Inside a skill, between its own files: described by the skill standard, not by this guide.
- Between instruction files: given by the nesting of `applyTo`, with no links.
- Between different skills, or from a skill to an instruction file: listed in the `## DependsOn` section. Only this kind goes there.

Rules for links:

- An instruction file never links to another instruction file or to a skill. `applyTo` nesting already applies the files above it, and the editor does this on its own; rely on that behavior.
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

## Closing issues from a pull request

Only when the user gives a GitHub issue in the conversation, the pull request description names that issue in a closing line. Put the line on its own, outside any list or quote:

```text
Closes #123
```

For several issues, write one closing line per issue, each with its own keyword.

Why: GitHub closes an issue on its own only when the pull request merges into the default branch and a closing keyword in the description links the two.
