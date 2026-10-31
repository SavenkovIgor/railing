---
name: report-write
description: >-
  You should use this skill when:
  asked to write a technical report about existing code into `notes/<task_id>/`,
  asked for an architecture overview of classes, modules, or a subsystem,
  asked to explain data flow, ownership, or lifecycle before working on a feature
---

# Report write

Write a technical report about existing code into `notes/<task_id>/`, following the profile for its kind.

## Pick the profile

| Kind | Request | Profile |
|---|---|---|
| `overview` | Understand classes, a subsystem, or a flow | [overview](/com.github.copilot/rules/reports-overview.instructions.md) |

If no profile matches the request, stop and ask. Do not invent a structure.

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

Do not verify your own claims beyond the links. `report-review` checks them in
a clean context, so they are not confirmed by the same assumptions that produced them.
