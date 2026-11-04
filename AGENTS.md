# Agent guide for this repository

## Scopes of instructions

Instruction files nest by `applyTo`: the scope of each file equals or lies inside the scope of its parent. The files do not depend on each other. Both trees below have one root:

- [global.instructions.md](/com.github.copilot/rules/global.instructions.md) - `**/*`; how the agent works and answers on any task

Markdown tree, broadest scope first; the parent of each file is the file above it, and the parent of the first file is the root:

- [markdown.instructions.md](/com.github.copilot/rules/markdown.instructions.md) - `**/*.md`; checks (`MD*`) on the form of any markdown file
- [prose.instructions.md](/com.github.copilot/rules/prose.instructions.md) - `**/*.md`; how the text reads
- [notes.instructions.md](/com.github.copilot/rules/notes.instructions.md) - `notes/**/*.md`; path, task ID, and language of any note in `notes/`
- [reports.instructions.md](/com.github.copilot/rules/reports.instructions.md) - `notes/**/*.overview.md`; content checks for notes about existing code
- `reports-<kind>.instructions.md` (in the same directory) - `notes/**/*.<kind>.md`; structure of one report kind

Code tree; the parent of a nested item is the item that contains it, and the parent of the top item is the root:

- [global-code.instructions.md](/com.github.copilot/rules/global-code.instructions.md) - `**/*.{h,hpp,cc,cpp,cppm,ipp,py,js,ts}`; coding principles for any language
  - [api-cpp.instructions.md](/com.github.copilot/rules/api-cpp.instructions.md) - `**/*.{cpp,hpp,cppm,ipp,h,cc}`; API design and naming in C++
  - [api-python.instructions.md](/com.github.copilot/rules/api-python.instructions.md) - `**/*.py`; API design and naming in Python

Nesting is a required property of both trees. A new instruction file goes below the narrowest file whose scope contains its own. A file whose scope is not inside the scope of its parent breaks the nesting.

A parent holds the shared base. A nested file holds only what differs from the files whose scope contains its own or adds to them, and does not restate their rules. An example in the language of the nested file may show how a parent rule looks there.

Why: `applyTo` already gives the reader of a nested file every file whose scope contains its own, so the nested file needs only the difference.

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

## Closing issues from a pull request

Only when the user gives a GitHub issue in the conversation, the pull request description names that issue in a closing line. Put the line on its own, outside any list or quote:

```text
Closes #123
```

For several issues, write one closing line per issue, each with its own keyword.

Why: GitHub closes an issue on its own only when the pull request merges into the default branch and a closing keyword in the description links the two.
