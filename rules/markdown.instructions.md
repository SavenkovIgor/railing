---
name: Markdown Requirements
applyTo: '**/*.md'
---

# Markdown requirements

Rules for all Markdown files. Every rule is a pass/fail check; reviews cite rules by ID.

## Code

- MD1 Every code fence has a language tag; use `text` for plain output

## Language

- MD2 Write in the language of the document.
- MD3 For English, use American spelling and grammar.

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
