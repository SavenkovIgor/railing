---
name: review
description: >-
    You should use this skill when:
    asked to review a diff, a branch, a commit range, or a pull request,
    asked whether a change is safe to merge,
    asked to check that a change does what its description says
argument-hint: "Optional: file path, commit range, or PR number. Default: uncommitted changes."
user-invocable: true
---

# Review

## DependsOn

- [bp](/skills/bp/SKILL.md)

Review a change against its intent. Report only; do not edit files.

## Procedure

1. Pick the target
   - With no argument, take uncommitted changes (`git diff HEAD`)
   - If there are none, take the branch against its base (`git diff <base>...HEAD`)
   - Otherwise take the path, commit range, or PR the user names
2. Find the intent: PR description, linked issue, commit messages, or the user's own words
   - If none exists, ask one question. Do not guess the intent
3. Read the changed code with its surroundings: callers, tests, and types it touches
4. Check the change against these criteria
   - Correctness: the change does what the intent says, including empty input, errors, and limits
   - Scope: every changed line traces to the intent; flag unrelated edits, unrequested
     abstractions, and unrequested options
   - Tests: a behavior change comes with a test that fails before it and passes after it
   - Safety: public behavior changes, data loss, unvalidated input at trust boundaries, security
5. Run `bp` on the changed files only when the user asks for a standards check, and append its
   report as a separate section

## Findings

- Write the scenario for each finding: the input or state, and the wrong result it produces
- Drop a finding when you cannot write its scenario
- Skip what a formatter or linter owns, and skip problems in unchanged lines the change does not
  make reachable
- Do not list what is correct

## Reply format

```text
Verdict: merge | fix first | block
Intent: <one line>

Findings:
1. [blocking | important | minor] <path>:<line> - <problem>
   Scenario: <input or state> -> <wrong result>
   Fix: <proposed change>

Not checked: <what you did not read or run>
```

Apply findings only after the user picks them (for example, "fix 1, 3").
