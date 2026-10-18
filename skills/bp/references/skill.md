# SKILL.md Best Practices

First read the best practice docs:
[BP](https://agentskills.io/skill-creation/best-practices)

## General Principles

- Line width - 100 characters
- Avoid long paragraphs; use lists, tables, and formatting to break up content
- The skill should only include content that truly requires model reasoning or understanding.
- Use paths from the skill root without `./` (`scripts/foo.sh`) for all skill resources
- Move supporting material to `references/` or `assets/` if needed
- Move a template longer than 10 lines to `assets/` and link it from `SKILL.md`
- `SKILL.md` under 50 lines is great; more than 250 lines is unmanageable and MUST be
  compressed, cut down, or split by moving content to `references/` or `assets/`
- Move the rules of one use case to its own file in `references/` only when all of these hold:
  - `SKILL.md` exceeds 250 lines
  - the use case is separate, so most runs do not need its rules
  - the rules of that use case take more than 30% of `SKILL.md`
- Rules of a use case that take a few paragraphs stay in `SKILL.md`: a separate file adds
  indirection and saves nothing
- State next to each link to a file in `references/` when to read it
- Do NOT put periods at the end of bullet list items (items starting with `-`)

## Scripts

- Move a step to `scripts/` only when the environment that runs it is known; this is rare,
  since a skill cannot assume a runtime or tools
- A script replaces its step in `SKILL.md` and does not duplicate it
- Default script format: Python with inline script metadata (PEP 723), a `# /// script` comment
  block that declares `requires-python` and `dependencies`, run by `uv run`; this is a default,
  not the best choice for every project

## Frontmatter

- `name` must match the folder name exactly (case-sensitive, lowercase-alphanumeric + hyphens)
- `description` must be present, and brief

`argument-hint` is allowed when the skill accepts arguments; at most 7 words.

Add no other fields (such as `user-invocable`): vendors support them unevenly and they add little.

## Body Structure

**NEVER include a `## When to Use` section (or equivalent).**

This is the strictest rule in this reference. Rationale:

- The decision to load a skill is made solely from `description` (gradual context disclosure)
- By the time the body is loaded into context, the skill has already been selected - trigger conditions are irrelevant
- Any content that belongs in `## When to Use` already belongs in `description`
- Including it wastes context tokens and creates maintenance drift between the two

If trigger conditions are not fully expressed in `description`, fix `description` - do not add a body section.

## Description

Anti-patterns:

- "A helpful skill for..." - too vague, won't trigger on real queries
- No trigger phrases - model cannot infer when to load
- Longer than 1024 characters - will be truncated

Patterns to follow:

- Keep it short and actionable: it is shown in skill lists and used for matching,
  not for documentation
- description should start with phrase `You should use this skill when...` followed by specific trigger conditions
- Prefer this frontmatter formatting for description:

```markdown
description: >-
    You should use this skill when:
    [trigger condition 1],
    [trigger condition 2],
```

It should be formatted with `>-\n` to preserve newlines and keep 100 column width
