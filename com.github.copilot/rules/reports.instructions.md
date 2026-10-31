---
name: Report Requirements
applyTo: 'notes/**/*.overview.md'
---

# Report requirements

Universal rules for agent-written technical reports about existing code.
Each report kind adds its own structure in `reports-<kind>.instructions.md`.
Every rule is a pass/fail check; reviews cite rules by ID.

## Content

- R1 Every statement about specific code links to it:
  `[Symbol](path/from/repo/root#L42)`
- R2 State only what you read in the code. Prefix anything inferred with `Assumption:`
- R3 Explain intent, contracts, and non-obvious behavior; do not retell code line by line
- R4 A code block has at most 15 lines and only the lines the text discusses;
  for anything longer, link to the code
- R5 Define domain terms in the `Terminology` section
- R6 No recommendations or design critique unless the profile asks for them
