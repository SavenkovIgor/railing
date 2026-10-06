---
name: report-review
description: >-
  You should use this skill when:
  asked to clean up, review, or check a report in `reports/`,
  asked to verify that a technical markdown document matches the code
---

# Report review

Input: a report path. Take the kind from the `.<kind>.md` suffix and read the
[core requirements](../../rules/reports.instructions.md) and the matching
`../../rules/reports-<kind>.instructions.md`. If the kind is unknown, apply the core
only and say so.

## 1. Clean up: edit in place

- Fix every `F*`, `L*`, and R6 (filler) violation directly in the file
- Do not change facts, link targets, or code. If a fix needs a fact change,
  report it as a finding instead

## 2. Verify against code: report only

Run this step in a subagent. Pass it only the report path and the instructions
below, not this conversation, so it does not inherit the author's assumptions.
If no subagent tool is available, do it yourself and re-read the code for every claim.

Subagent instructions:

- Check every code link: the file exists, the line is inside the named symbol
- Pick the key claims: ownership, lifecycle, threading, call order, data flow,
  error handling. Verify each one by reading the code
- Return each claim as: report location, claim, verdict
  (`confirmed`, `wrong`, `unverifiable`), evidence link

## 3. Profile checks: report only

Run the profile's checks. Also check R1-R5 and R7.

## Reply format

```text
Cleanup: <N> edits (<rule IDs>)

Findings:
1. [wrong | missing | unverifiable | <rule ID>] <section> — <problem>
   Evidence: <path#Lline>
   Fix: <proposed change>
```

List only `wrong` and `unverifiable` claims, not confirmed ones. Do not apply
findings until the user picks them (for example, "fix 1, 3").
