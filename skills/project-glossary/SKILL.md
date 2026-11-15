---
name: project-glossary
description: >-
    You should use this skill when:
    asked to build or update a glossary, dictionary, or ubiquitous language of a project,
    asked to collect the terms a team uses from its issue tracker, docs, and code,
    asked which word the team uses for a domain concept
argument-hint: Optional area or bounded context
---

# Project glossary

Collect the domain terms of a project from its issue tracker, docs, and code, and merge them into
one `GLOSSARY.md` with one canonical word per concept. The file follows the glossary format of
Matt Pocock's
[domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling)
skill, so that skill can maintain it afterward.

## Inputs

- An optional area or bounded context; without it, cover the whole project
- An existing `GLOSSARY.md` or `GLOSSARY-MAP.md`: update it and keep its decisions unless a
  source contradicts them
- Access to the issue tracker through a Model Context Protocol (MCP) tool, a CLI, or an export
  from the user

## Source priority

1. Issue tracker: issue titles, descriptions, and comments, pull request descriptions, and
   review comments. Here the team writes to each other, so these are the words people use
2. Docs: README, `docs/`, wiki, architecture decision records (ADRs), onboarding notes
3. Code: names of modules, types, functions, enum values, config keys, and API routes. Code
   shows what exists, but its names lag behind renames and carry implementation words

The canonical term for a concept comes from the highest source that names it. Within one source,
take the word used more often in the last year. Put the other words under `_Avoid_`, and the code
identifier under `_Code_` when it differs from the term.

## Procedure

1. Find the tracker from the git remote, config files, and available tools. If no tool reaches
   it, ask the user for access or an export, and run without it only if the user agrees
2. Read the last 200 issues and pull requests, open and closed, with comments. Favor items with
   long discussions. Delegate the reading to subagents when it does not fit in one context
3. Note each candidate term: a domain noun, verb, or state that an outsider would not understand,
   or that the team uses in a narrower sense than usual. Keep the words used for it and one link
4. Read the docs, then the code, and match their names to the candidates; add concepts that
   appear only there
5. Drop general programming terms such as timeout, retry, or DTO, and words seen only once
6. Group the words into concepts and pick each canonical term by the source priority
7. Collect the open cases: a tie between words, one word for two concepts, a doc or code meaning
   that contradicts the tracker. Ask the user about them in one batch, recommended option first
8. Write the file from [GLOSSARY.md.template](assets/GLOSSARY.md.template). For an area with
   its own words, write `GLOSSARY.md` inside the area and list it in a root `GLOSSARY-MAP.md`

## Glossary rules

- Define what the concept is, in one or two sentences, without implementation details
- Write terms in the language the team uses in the tracker, spelled as the team spells them
- Group terms under `###` headings when clusters emerge; a flat list is fine otherwise
- Put cases the user left open under `## Flagged ambiguities`
- Change no code; report code identifiers that differ from their term as rename candidates

## Output Format

Report in chat:

1. Paths of the written files
2. A table of the added and changed terms: term, words under `_Avoid_`, and the sources that use
   it (tracker, docs, code)
3. Rename candidates: code identifiers that differ from their canonical term
4. Sources not read: tracker ranges, docs, and directories skipped
