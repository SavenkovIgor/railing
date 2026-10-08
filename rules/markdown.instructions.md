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

### MD4 Link text must not duplicate the URL or path

The text in `[...]` exists to give the reader meaningful context - it should never be a raw copy of the path in `(...)`.
Use a descriptive label or, at minimum, just the filename.

✘ `[references/doc-validation.md](references/doc-validation.md)`
✔ `[doc-validation.md](references/doc-validation.md)`
✔ `[Documentation Validation](references/doc-validation.md)`

## Emphasis

### MD5 Avoid bolding everything in a row

Overusing bold text is an anti-pattern.
Fix it by removing most bold formatting and keeping only truly important words or short phrases.

Reasoning: if everything is bold, then nothing is truly bold, and it stops guiding attention effectively.

## Symbols

- MD6 Emoji and some other symbols are not monospaced and can break alignment, so avoid them in documents (files).
  In chat responses, emoji are fine.

  In documents, always replace:
  - `✅` with `✔`
  - `❌` with `✘`
  - `…` with `...`

  Do not apply these replacements to chat output formats that a document defines,
  such as severity markers in a review report.

## Horizontal Dividers

- MD7 Avoid using `---` as a visual divider in almost all cases. Keep it only when
  required by a format, such as the delimiters around YAML frontmatter.
