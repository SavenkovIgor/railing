---
name: Plan Profile
applyTo: 'notes/**/*.plan.md'
---

# Plan profile

A plan is a working document that the reader executes as written.
It holds only the current decision for each step.
Every rule is a pass/fail check. Reviews cite rules by ID.

## Editing

- P1 To change a decision, rewrite the place in the plan that holds it, and
  delete the old option. Agents tend to append the new decision at the end,
  so the plan says one thing in step 2 and the opposite ten lines later.

  ✘ Step 2: `Store the cache in Redis`. At the end: `Update: use SQLite instead`
  ✔ Step 2: `Store the cache in SQLite`

- P2 No two statements in the plan contradict each other. After an edit,
  find the steps that depend on the changed decision and rewrite them too
- P3 The plan holds no history: no `Update:`, `previously`, `we first decided`,
  strikethrough, or changelog section. If the reason against the old option
  still matters for execution, state it as a current constraint:
  `Use SQLite. The CI runners have no Redis`

Why: the reader executes the plan without its history. Two versions of one
decision force the reader to guess which one is current. The history of
decisions belongs in git or in an ADR.
