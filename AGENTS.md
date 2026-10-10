# Agent guide for this repository

## Where markdown rules live

Broadest scope first; each file adds to the ones above it and links instead of restating. Files must not form circular links: if A links to B, B must not link back to A, directly or through a chain of other files. Linking only to files above in this list guarantees it.

- [markdown.instructions.md](/com.github.copilot/rules/markdown.instructions.md) - checks (`MD*`) on the form of any `*.md`
- [tech-writing](/skills/tech-writing/SKILL.md) - how the text reads
- [docs-bp.md](/skills/bp/references/docs-bp.md) - what a documentation set must cover; requires the two files above as a whole
- [reports.instructions.md](/com.github.copilot/rules/reports.instructions.md) - extra checks for `reports/` only; drop a `F*` check once `MD*` covers it
- `reports-<kind>.instructions.md` (in the same directory) - structure of one report kind; requires the file above as a whole
- [ai-artifacts-review](/skills/ai-artifacts-review/SKILL.md) - audit of AI artifacts

## How rule files refer to each other

The files above form a hierarchy. A file that depends on another one applies it as a whole.

- A file links to each file it depends on once, in its first paragraph after the title: "This file also requires every check in [file]".
- A file never copies, summarizes, or cites single rules of another file, neither by text nor by ID, and never links to it later in the document.
- A file links only to files above it in the list, as the rule against circular links requires.
- An instruction file (`com.github.copilot/rules/`) links only to other instruction files, never to a skill. A skill may link to skills and to instruction files.

Why: a copied or cited rule drifts from its source, and a reader who follows a link to one rule skips the rest of that file. An instruction attaches by `applyTo` on its own, while a skill runs only when invoked, so an instruction that depends on a skill depends on something that may not be loaded.

## Where a duplicated rule stays

When the same rule appears in an instruction file and in a skill, remove it from the skill by default and keep it in the instruction.

Why: an instruction applies by default through `applyTo`, while a skill applies only when someone invokes it.

## Link paths

A link path never contains a `..` segment. Write it by context:

- A link inside a skill to a file of the same skill starts at the skill root, with no `./`.
  ✔ `[docs-bp.md](references/docs-bp.md)`
  ✘ `[docs-bp.md](./references/docs-bp.md)`
- A link from a skill to another skill or to a plugin file starts at the plugin root, with a leading `/`.
  Such a skill works only inside this plugin; it is not standalone.
  ✔ `[tech-writing](/skills/tech-writing/SKILL.md)`
  ✘ `[tech-writing](../../tech-writing/SKILL.md)`
- A link in a plugin-level file (`AGENTS.md`, `README.md`, `com.github.copilot/`) starts at the plugin root, with a leading `/`.
  ✔ `[plugin.json](/plugin.json)`
  ✘ `[plugin.json](./plugin.json)`
- A path in a manifest or `mcp.json` starts with `./` from the plugin root, as the Agent Plugins specification requires.
  ✔ `./skills/`
  ✘ `skills/`

Why: a root-based path survives a file move and needs no level counting. A leading `/` resolves from the repository root on GitHub and from the workspace root in VS Code; how each agent reads it is not specified and not yet verified.

## Pull request workflow

In every pull request to this repository, the first commit contains only the version bump in [plugin.json](/plugin.json). Make all other changes in later commits.

Why: the bump then does not depend on the rest of the change, and a reviewer sees the new version at once.
