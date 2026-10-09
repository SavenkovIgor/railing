# Agent guide for this repository

## Where markdown rules live

Broadest scope first; each file adds to the ones above it and links instead of restating. Files must not form circular links: if A links to B, B must not link back to A, directly or through a chain of other files. Linking only to files above in this list guarantees it.

- [markdown.instructions.md](./rules/markdown.instructions.md) - checks (`MD*`) on the form of any `*.md`: syntax, fences, headings, links, emphasis, symbols
- [tech-writing](./skills/tech-writing/SKILL.md) - how the text reads: wording, sentence and paragraph style, genre structure
- [docs-bp.md](./skills/bp/references/docs-bp.md) - what a documentation set must cover; cites `MD*` and `tech-writing`, restates neither
- [reports.instructions.md](./rules/reports.instructions.md) - extra checks for `reports/` only; drop a `F*` check once `MD*` covers it
- [ai-artifacts-review](./skills/ai-artifacts-review/SKILL.md) - audit of AI artifacts; its markdown-form checks (`XA05` to `XA07`) move to `MD*`
