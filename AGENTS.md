# Agent guide for this repository

## Where markdown rules live

Broadest scope first; each file adds to the ones above it and links instead of restating. Files must not form circular links: if A links to B, B must not link back to A, directly or through a chain of other files. Linking only to files above in this list guarantees it.

- [markdown.instructions.md](./rules/markdown.instructions.md) - checks (`MD*`) on the form of any `*.md`
- [tech-writing](./skills/tech-writing/SKILL.md) - how the text reads
- [docs-bp.md](./skills/bp/references/docs-bp.md) - what a documentation set must cover; requires the two files above as a whole
- [reports.instructions.md](./rules/reports.instructions.md) - extra checks for `reports/` only; drop a `F*` check once `MD*` covers it
- [ai-artifacts-review](./skills/ai-artifacts-review/SKILL.md) - audit of AI artifacts

## How rule files refer to each other

The files above form a hierarchy. A file that depends on another one applies it as a whole.

- A file links to each file it depends on once, in its first paragraph after the title: "This file also requires every check in [file]".
- A file never copies, summarizes, or cites single rules of another file, neither by text nor by ID, and never links to it later in the document.
- A file links only to files above it in the list, as the rule against circular links requires.

Why: a copied or cited rule drifts from its source, and a reader who follows a link to one rule skips the rest of that file.

## Pull request workflow

In every pull request to this repository, the first commit contains only the version bump in both plugin files: [plugin.json](./plugin.json) and [.cursor-plugin/plugin.json](./.cursor-plugin/plugin.json). Both files must carry the same new version. Make all other changes in later commits.

Why: the bump then does not depend on the rest of the change, and a reviewer sees the new version at once.
