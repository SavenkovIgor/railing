---
name: Notes Requirements
applyTo: 'notes/**/*.md'
---

# Notes requirements

Universal rules for agent-written notes in `notes/`: reports, plans, and other working records of a task.
A kind with a profile adds its own structure in a separate instruction file.
Every rule is a pass/fail check; reviews cite rules by ID.

## File naming

- N1 Path is `notes/<task_id>/YYYY-MM-DD-<slug>.<kind>.md`
- N2 `<task_id>` is the task identifier in the format of the project, such as the
  ticket ID as written in the tracker. Take it from the request or the branch
  name; if neither gives one, ask
- N3 `<slug>` is lowercase kebab-case, 2-5 words naming the content of the file
- N4 `<kind>` is `overview`, which has its own profile, or `plan`, which is
  reserved and has no profile yet

## Language

- L1 Write in the language of the request (Russian or English).
  Keep code identifiers and established English technical terms as is
