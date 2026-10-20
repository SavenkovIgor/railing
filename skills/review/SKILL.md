---
name: review
description: >-
    You should use this skill when:
    asked to review a file, uncommitted changes, or the current branch,
    asked whether a change is safe to merge,
    asked to check that a change does what its description says
argument-hint: "File path, uncommitted, or branch"
---

# Review

Review a file or a change against its intent, then run the local review skills of the user and
the project on the same target. Report only; do not edit files.

## DependsOn

- [bp](/skills/bp/SKILL.md)

## Procedure

1. Pick the mode from what the user said
   - A file the user names: review that file as a whole, with no diff
   - Uncommitted changes: review `git diff HEAD` plus untracked files from `git status`
   - The branch: find the default branch with `git remote show origin | grep HEAD`
     (the line reads `HEAD branch: <name>`), then review `git diff origin/<name>...HEAD`
   - If the request fits none of these, ask which one. Do not pick a mode yourself
2. Find the intent of a change: PR description, linked issue, commit messages, or the user's words
   - For a file, the intent is the user's request
   - If none exists, ask one question. Do not guess the intent
3. Read the changed code with its surroundings: callers, tests, and types it touches
4. Check the change against these criteria
   - Correctness: the change does what the intent says, including empty input, errors, and limits
   - Scope (uncommitted and branch modes): every changed line traces to the intent; flag
     unrelated edits, unrequested abstractions, and unrequested options
   - Tests: a behavior change comes with a test that fails before it and passes after it
   - Safety: public behavior changes, data loss, unvalidated input at trust boundaries, security
5. Run the local review skills after your own pass, so one report covers general and
   project-specific rules
   - Find them in the skills list of the current context and in the skill directories of the
     project and the user: `.claude/skills`, `.github/skills`, `.agents/skills` and their `~/`
     counterparts
   - Take a skill when its name or description says it reviews code or changes and its scope
     covers the target
   - Skip `review` itself, and skip any skill that invokes `review`: it would loop
   - Invoke each one with the same target and intent, and tell it to report only
   - Merge its findings into yours: drop a duplicate and keep the higher severity. Prefix each
     finding from a local skill with its name
   - If a skill fails or cannot be loaded, list it under `Not checked`. Do not retry it
6. Run `bp` on the changed files only when the user asks for a standards check, and append its
   report as a separate section

## Findings

- Write the scenario for each finding: the input or state, and the wrong result it produces
- Drop a finding when you cannot write its scenario
- Skip what a formatter or linter owns, and skip problems in unchanged lines the change does not
  make reachable
- Do not list what is correct

## Output Format

```text
Verdict: merge | fix first | block
Intent: <one line>
Local reviews: <skill names that ran> | none found

Findings:
1. [blocking | important | minor] [<local skill, if any>] <path>:<line> - <problem>
   Scenario: <input or state> -> <wrong result>
   Fix: <proposed change>

Not checked: <what you did not read or run>
```

Apply findings only after the user picks them (for example, "fix 1, 3").
