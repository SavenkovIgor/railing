# Agent guide for this repository

## Scopes of markdown instructions

Instruction files for markdown nest by `applyTo`: the scope of each file equals or lies inside the scope of the file above it. The files do not depend on each other. Broadest scope first:

- [markdown.instructions.md](/com.github.copilot/rules/markdown.instructions.md) - `**/*.md`; checks (`MD*`) on the form of any markdown file
- [prose.instructions.md](/com.github.copilot/rules/prose.instructions.md) - `**/*.md`; how the text reads
- [reports.instructions.md](/com.github.copilot/rules/reports.instructions.md) - `reports/**/*.md`; extra checks for `reports/` only; drop a `F*` check once `MD*` covers it
- `reports-<kind>.instructions.md` (in the same directory) - `reports/**/*.<kind>.md`; structure of one report kind

Nesting is a required property of this list. A new instruction file for markdown goes below the narrowest file whose scope contains its own. A file whose scope is not inside the scope of the file above it breaks the nesting.

Files do not restate rules of files whose scope contains theirs.

## How rule files refer to each other

There are three kinds of dependencies. Each has its own place:

- Inside a skill, between its own files: described by the skill standard, not by this guide.
- Between instruction files: given by the nesting of `applyTo`, with no links.
- Between different skills, or from a skill to an instruction file: listed in the `## DependsOn` section. Only this kind goes there.

Rules for links:

- An instruction file never links to another instruction file or to a skill. `applyTo` nesting already applies the files above it, and the editor does this on its own; rely on that behavior.
- A skill links to every instruction file and skill it depends on, once, in a `## DependsOn` section directly after the title. A skill applies each linked file as a whole.
- A link in a routing table, where a skill picks one target by the input, is not a dependency and stays where it is.
- Files must not form circular links: if A links to B, B must not link back to A, directly or through a chain of other files.
- A file never copies, summarizes, or cites single rules of another file, neither by text nor by ID, and never links to it later in the document.

Why: a copied or cited rule drifts from its source, and a reader who follows a link to one rule skips the rest of that file. An instruction attaches by `applyTo` on its own, while a skill runs only when invoked, so an instruction that depends on a skill depends on something that may not be loaded. A skill can run before the file it works on is in the context, so `applyTo` has not attached anything yet; a link is the lesser evil there.

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
  ✔ `[report-review](/skills/report-review/SKILL.md)`
  ✘ `[report-review](../../report-review/SKILL.md)`
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
