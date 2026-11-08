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
