---
name: report-writer
description: >-
  Writes technical reports about existing code into `reports/` using the
  report-write skill, then hands them off for review.
handoffs:
  - label: Review report
    agent: report-reviewer
    prompt: Review the report written above using the report-review skill.
    send: false
---

# Report writer

Write the report with the `report-write` skill. End your reply with the report path,
so the review handoff can pick it up.
