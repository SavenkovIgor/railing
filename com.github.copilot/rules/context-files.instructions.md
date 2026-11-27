---
name: Context Files
applyTo: '**/{AGENTS.md,SKILL.md,*.instructions.md,*.agent.md}'
---

# Context files

Rules for AI context files: instructions, skills, and agents.

## How rule files refer to each other

There are three kinds of dependencies. Each has its own place:

- Inside a skill, between its own files: described by the skill standard, not by this file.
- Between instruction files: given by the nesting of `applyTo`, with no links.
- Between different skills, or from a skill to an instruction file: listed in the `## DependsOn` section. Only this kind goes there.

Rules for links:

- An instruction file never links to another instruction file or to a skill. `applyTo` nesting already applies every file whose scope contains its own, and the editor does this on its own. Rely on that behavior.
- A skill links once to every instruction file and skill it depends on. The links go in a `## DependsOn` section directly after the goal paragraph. A skill applies each linked file as a whole.
- In a routing table, a skill picks one target by the input. A link in such a table is not a dependency and stays where it is.
- Files must not form circular links. If A links to B, B must not link back to A, directly or through a chain of other files.
- A file never copies, summarizes, or cites single rules of another file, by text or by ID. It also never links to that file later in the document.

Why: a copied or cited rule drifts from its source. A reader who follows a link to one rule skips the rest of that file. An instruction attaches by `applyTo` on its own, while a skill runs only when someone invokes it. So an instruction that depends on a skill depends on something that is not always loaded. A skill can run before the file it works on is in the context, and then `applyTo` has not attached anything yet. There, a link costs less than a missing rule.

## Where a duplicated rule stays

When the same rule appears in an instruction file and in a skill, keep it in the instruction. By default, remove it from the skill.

Why: an instruction applies by default through `applyTo`, while a skill applies only when someone invokes it.

## Where a new rule lives

Put a rule in the narrowest place that always loads it. A rule that applies to files by glob goes in an instruction file. A procedure that runs on demand goes in a skill. A rule that needs its own context or tool limits goes in an agent. When a program can check the rule, write the check (a task, a linter, a hook) instead of prose.

Why: a rule in a wider place than it needs costs context on every task. A rule in a skill loads only when someone invokes it.

## Phrasing of requirements

State each requirement positively: say what to do. Add a prohibition ("not here, not there") only when LLMs make that mistake in practice. Name the mistake.

When an edit replaces one option with another, write only the new option. Agents tend to keep the old option as a contrast. The reader of the new text never saw the old option. An old version of the text does not show a mistake in practice.

✘ `Find longer lines with the IDE text search tool, not with awk in the console`
✔ `Find longer lines with the IDE text search tool`

Why: a prohibition for an error that never happens costs tokens and clutters the context of both the model and the human reader. Break the rule when a mistake is costly and likely enough to justify the extra line.
