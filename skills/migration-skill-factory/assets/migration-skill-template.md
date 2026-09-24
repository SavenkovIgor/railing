# [Migration Unit Title]

## Goal

Migrate one specific legacy usage pattern to the new version-compatible pattern.

## Compatibility and Applicability

- current_version: [e.g. Python 3.12 / API v1]
- target_version: [e.g. Python 3.13 / API v2]
- compatibility_mode: [pre-migration-compatible | target-version-only]
- safety_label: [high-safe | medium-safe | review-required]

Applicability statement:

- Allowed now: [yes/no and why]
- Allowed only after upgrade: [yes/no and why]
- Forbidden conditions: [conditions where this skill must not edit]

## Source Evidence

- Release notes: [url or file]
- Migration guide: [url or file]
- API/code diff reference: [url or file]

## Detection

- Search targets:
  - imports/modules
  - symbol names
  - signatures
  - config keys
- False-positive guards:
  - [guard 1]
  - [guard 2]
- Detect-only command plan:
  - [command or procedure]

## Replacement Strategy

- old_pattern: [concrete pattern]
- new_pattern: [concrete replacement]
- mechanical steps:
  1. [step]
  2. [step]
  3. [step]
- non-mechanical decisions:
  - [decision rule]

## Safety Rules

- Preserve runtime behavior unless explicitly documented.
- If behavior might change, switch to review-required mode.
- If confidence is low, run detect-only and request approval.

## Validation

- Static checks:
  - [lint/type/build command]
- Behavioral checks:
  - [tests/smoke checks]
- Acceptance criteria:
  - No remaining supported old_pattern matches in scope.
  - No migration-introduced regressions.

## Rollback

- Revert strategy for this migration unit:
  - [how to revert safely]
- Stop conditions:
  - [conditions that require abort and manual triage]

## Output Format

Return:

1. Findings summary.
2. Planned edits summary.
3. Applied edits summary (or detect-only report).
4. Validation result.
5. Open risks and manual follow-ups.
