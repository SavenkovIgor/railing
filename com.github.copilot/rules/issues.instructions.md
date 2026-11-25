---
name: Issue Requirements
applyTo: '**/*'
---

# Issue requirements

Rules for an issue that an agent drafts or edits, in any tracker.

## One reason, one action

Give each issue one problem and one kind of action: add, fix, rewrite, move, or delete. When a draft holds a second problem or a second kind of action, split it into one issue per problem and action.

Check every "and" and every conditional clause such as "fix it only if...": a second action often hides there. A clause that joins two problems or two kinds of action means a split. A clause that joins parts of one change, such as code and its test, stays.

✘ One issue: `Delete examples that restate code.instructions.md, and the buggy ones; fix a buggy one in place if the rule has no other example`
✔ Two issues: `Delete examples that restate code.instructions.md` and `Fix the buggy examples in code-cpp.instructions.md`

Why: an issue with two reasons grows in scope during the work, and its pull request mixes changes that a reviewer judges by different criteria.

## Size of the body

Keep the body of an issue no longer than the diff it plans. The minimum is three lines: the problem, the place, and the expected fix. Agents tend to add background, alternatives, risks, and acceptance criteria to a small fix. Add these parts only when the change needs a decision from the user.

✘ A 15-line issue with background and acceptance criteria for a 2-line fix
✔ Three lines: `Problem: the link to prose.instructions.md is broken`, `Place: AGENTS.md, line 12`, `Fix: add the leading /`

Why: the user reads the issue and then reviews the diff. An issue longer than its diff costs more time to read than the fix costs to review.
