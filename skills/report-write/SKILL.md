---
name: report-write
description: >-
  You should use this skill when:
  asked to write a technical report about existing code into `notes/<task_id>/`,
  asked for an architecture overview of classes, modules, or a subsystem,
  asked to explain data flow, ownership, or lifecycle before working on a feature
---

# Report write

Write a technical report about existing code into `notes/<task_id>/`. Follow the profile for the
kind of the report.

## Pick the profile

| Kind | Request | Profile |
|---|---|---|
| `overview` | Understand classes, a subsystem, or a flow | [overview](/com.github.copilot/rules/reports-overview.instructions.md) |

If no profile matches the request, stop and ask the user. Do not invent a structure.

## Procedure

1. Read the profile
2. Collect the inputs the profile lists and read them fully
3. Find the task ID as the notes requirements say
4. Create the report in `notes/<task_id>/`, named as the notes requirements say, with the
   profile's sections as headings
5. Fill each section as the core requirements say: link every statement about
   code and mark inferences
6. Check the formatting rules of the core requirements and fix violations
7. Reply with the report path and offer `report-review`

Limit your own check of the claims to their links. `report-review` checks the claims in a
clean context, free of the assumptions that produced them.
