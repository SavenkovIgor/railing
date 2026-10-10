---
name: report-write
description: >-
  You should use this skill when:
  asked to write a technical report about existing code into `reports/`,
  asked for an architecture overview of classes, modules, or a subsystem,
  asked to explain data flow, ownership, or lifecycle before working on a feature
---

# Report write

## Pick the profile

| Kind | Request | Profile |
|---|---|---|
| `overview` | Understand classes, a subsystem, or a flow | [overview](/com.github.copilot/rules/reports-overview.instructions.md) |

If no profile matches the request, stop and ask. Do not invent a structure.

## Procedure

1. Read the profile
2. Collect the inputs the profile lists and read them fully
3. Create the report in `reports/`, named as the core requirements say, with the
   profile's sections as headings
4. Fill each section as the core requirements say: link every statement about
   code and mark inferences
5. Check the formatting rules of the core requirements and fix violations
6. Reply with the report path and offer `report-review`

Do not verify your own claims beyond the links. `report-review` checks them in
a clean context, so they are not confirmed by the same assumptions that produced them.
