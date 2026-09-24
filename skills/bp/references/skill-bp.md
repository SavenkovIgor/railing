# SKILL.md Best Practices

First read the best practice docs:
[BP](https://agentskills.io/skill-creation/best-practices)

## General Principles

- Line width - 100 characters
- Avoid long paragraphs; use lists, tables, and formatting to break up content
- `SKILL.md` under 50 lines is great; more than 300 is unmanageable and SHOULD be compressed/split/cut down
- The skill should only include content that truly requires model reasoning or understanding.
- Use relative paths (`./scripts/foo.sh`) for all skill resources
- Move supporting material to `references/` or `assets/` if needed
- If something could be done with script, prefer the script and place it in `scripts/`
- Do NOT put periods at the end of bullet list items (items starting with `-`)

## Frontmatter

- `name` must match the folder name exactly (case-sensitive, lowercase-alphanumeric + hyphens)
- `description` must be present, and brief

Ideally skill should not have any more frontmatter fields due to compatibility with various loaders and marketplaces.

## Body Structure

**NEVER include a `## When to Use` section (or equivalent).**

This is the strictest rule in this reference. Rationale:

- The decision to load a skill is made solely from `description` (gradual context disclosure)
- By the time the body is loaded into context, the skill has already been selected — trigger conditions are irrelevant
- Any content that belongs in `## When to Use` already belongs in `description`
- Including it wastes context tokens and creates maintenance drift between the two

If trigger conditions are not fully expressed in `description`, fix `description` — do not add a body section.

## Description

Anti-patterns:

- "A helpful skill for..." — too vague, won't trigger on real queries
- No trigger phrases — model cannot infer when to load
- Longer than 1024 characters — will be truncated

Patterns to follow:

- description should start with phrase `You should use this skill when...` followed by specific trigger conditions
- Prefer this frontmatter formatting for description:

```markdown
description: >-
    You should use this skill when:
    [trigger condition 1],
    [trigger condition 2],
```

It should be formatted with `>-\n` to preserve newlines and keep 100 column width
