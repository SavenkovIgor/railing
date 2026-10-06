---
name: Report Requirements
applyTo: 'reports/**/*.md'
---

# Report requirements

Universal rules for agent-written technical reports in `reports/`.
Each report kind adds its own structure in `reports-<kind>.instructions.md`.
Every rule is a pass/fail check; reviews cite rules by ID.

## File naming

- N1 Path is `reports/YYYY-MM-DD-<slug>.<kind>.md`
- N2 `<slug>` is lowercase kebab-case, 2-5 words naming the subject
- N3 `<kind>` is one of the profiles listed in the `report-write` skill

## Content

- R1 Every statement about specific code links to it:
  `[Symbol](path/from/repo/root#L42)`
- R2 State only what you read in the code. Prefix anything inferred with `Assumption:`
- R3 Explain intent, contracts, and non-obvious behavior; do not retell code line by line
- R4 A code block has at most 15 lines and only the lines the text discusses;
  for anything longer, link to the code
- R5 One term per concept. Define domain terms in the `Terminology` section
- R6 No filler: no intro that restates the title, no closing summary that repeats
  sections, no "it is important to note", no unsupported adjectives
  (robust, seamless, powerful, efficient)
- R7 No recommendations or design critique unless the profile asks for them

## Formatting

- F1 Exactly one `#` heading, on the first line
- F2 Heading levels do not skip (`##` then `####` fails)
- F3 Every code fence has a language tag; use `text` for plain output
- F4 No `---` horizontal rules
- F5 No emoji. Use `✔` and `✘` for status marks, `...` instead of `…`
- F6 Link text is not a copy of the URL or path
- F7 At most one bold fragment per paragraph or list item; no bold in headings
- F8 Code identifiers, file names, flags, and config keys are in inline code

## Language

- L1 Write in the language of the request (Russian or English).
  Keep code identifiers and established English technical terms as is
- L2 English: American spelling
- L3 Russian: name the actor and use a verb, not a nominalization:
  `сервис обрабатывает запрос`, not `производится обработка запроса`

For prose style beyond these checks, follow
[tech-writing](../skills/tech-writing/SKILL.md).
