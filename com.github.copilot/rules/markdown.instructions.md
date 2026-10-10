---
name: Markdown Requirements
applyTo: '**/*.md'
---

# Markdown requirements

Rules for all Markdown files. Every rule is a pass/fail check; reviews cite rules by ID.

## Code

- MD1 Every code fence has a language tag; use `text` for plain output

## Links

- MD4 Link text must not duplicate the URL or path.
  Why: the text in `[...]` gives the reader meaningful context, so it should
  never be a raw copy of the path in `(...)`. Use a descriptive label or, at
  minimum, just the filename.

  ✘ `[references/doc-validation.md](references/doc-validation.md)`
  ✔ `[doc-validation.md](references/doc-validation.md)`
  ✔ `[Documentation Validation](references/doc-validation.md)`

- MD5 Every link uses the syntax `[text](url)`; no bare URLs outside code spans and code fences.
  Why: a bare URL gives the reader no context and renders inconsistently.

  ✘ `See https://example.com/docs`
  ✔ `See [the docs](https://example.com/docs)`

- MD10 Prefer a link path written from the root of the repository, with a leading `/`, over a path with `..` segments. A `..` path is allowed; this is a preference, not a hard rule.
  Why: a root-based path survives a file move and needs no level counting.

  ✘ `[markdown.instructions.md](../../com.github.copilot/rules/markdown.instructions.md)`
  ✔ `[markdown.instructions.md](/com.github.copilot/rules/markdown.instructions.md)`

## Emphasis

- MD6 At most 3 bold fragments per document, with no exceptions.
  Why: if everything is bold, nothing stands out, and bold stops guiding
  attention. Fix a failure by removing bold from all but the fragments the
  reader must not miss.

## Symbols

- MD7 A document contains no emoji, no `✅`, `❌`, or `…`. Use `✔`, `✘`, and `...`.
  The only emoji allowed are the markers of a chat output format that the same
  document defines, such as severity markers in a review report.
  Why: emoji are not monospaced and break alignment. Chat responses are not
  documents, so emoji are fine there.

## Horizontal Dividers

- MD8 `---` appears on its own line only as the delimiter of YAML frontmatter.
  Why: a divider adds no meaning, and headings already split the document.
  Fix a failure by deleting every other `---` line; do not replace it with another divider.

## Globs

- MD9 A run of two or more file extensions is written as one brace glob in one code span; separate `*.ext` spans in a row fail.
  Write each extension once, in its own case: `{c,C}` for two different extensions, never a case-folded form.
  Start the glob with `**/` only where it is matched against paths, such as an `applyTo` value; a plain list of extensions that names file kinds starts with `*.`.
  Why: one glob is shorter, shows the whole set at a glance, and can be compared with an `applyTo` value without reordering or retyping.

  ✘ `*.cpp`, `*.hpp`, `*.cc`
  ✔ `*.{cpp,hpp,cc}`
  ✔ `**/*.{cpp,hpp,cc}` in an `applyTo` value
