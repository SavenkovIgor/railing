---
name: migration-skill-factory
description: >-
  Use this skill after an upgrade of a language, framework, or SDK version,
  or after an API changed or became deprecated.
  Also use it when old usage needs a refactor across a codebase,
  or when migration work needs a split into focused skills.
argument-hint: "What changed, versions, and repo scope"
---

# Migration Skill Factory

Create a set of migration skills from a version or API update, one skill per change type.

## Inputs

- The subject of the migration: the language, API, or product and the target versions.
- Links or files that are the source of truth:
  - Preferred: official release notes, migration guides, and changelogs.
  - Fallback: snapshots of the old and new source code and docs.
- The scope in the target codebase: the full repository or selected folders.
- The risk tolerance: strict safe mode or aggressive replacement mode.
- The runtime versions:
  - the current version in production or development
  - the target version after the migration

## Procedure

1. Build the migration context.
   - Confirm the old state and the new state.
   - Find what the change affects: syntax, signatures, runtime behavior, and tooling.
   - Define the scope boundaries and the exclusions.

2. Collect the authoritative changes.
   - Parse the release notes first.
   - If the notes are incomplete, inspect the source or API diff to fill the gaps.
   - Normalize every change into one record:
     - `change_id`
     - `category` (syntax, API, behavior, config, tooling, deprecation, removal)
     - `old_pattern`
     - `new_pattern`
     - `caveats`
     - `confidence` (high, medium, low)
     - `compatibility_mode` (`pre-migration-compatible` | `target-version-only`)
     - a link to the evidence

3. Classify compatibility and safety.
   - For each change, decide whether you can apply it safely before you switch the runtime or API version.
   - Set `compatibility_mode`:
     - `pre-migration-compatible`: you can apply it safely on the current version, and it stays valid on the target version.
     - `target-version-only`: apply it only after the runtime or API switch.
   - Set `safety_label`:
     - `high-safe`: the change is deterministic and backward-compatible. No behavior change is expected.
     - `medium-safe`: the change is mostly mechanical but needs a local check.
     - `review-required`: the semantics can differ, or the tooling evidence is weak.
   - Add an explicit notice for the user to every generated skill. The notice says:
     - when the user can run the skill
     - when the user must not run the skill
     - why

4. Prioritize the changes.
   - Score each change by its impact and by the complexity of its migration.
   - Put blocking changes first: changes that break the build or the runtime.
   - Group related records into migration units.

5. Generate one migration skill per migration unit.
   - Before you create any files, ask the user where to put the new skill, for example `.copilot/skills/` or `.github/skills/`.
   - Create the folder `<chosen-path>/<unit-name>/`.
   - Start from the [migration skill template](assets/migration-skill-template.md).
   - Create `SKILL.md` with these parts:
     - a precise trigger description with keywords from the old API and the new API
     - a section on compatibility and applicability
     - an exact strategy to detect the old usage
     - a replacement strategy with safety checks
     - validation steps and rollback criteria
   - Limit each generated skill to one migration unit.

6. Define the detection strategy for each generated skill.
   - Search for these patterns:
     - symbol names
     - call signatures
     - config keys
     - imports and modules
   - Add guards against false positives.
   - List the cases that depend on context and need a manual review.

7. Define the replacement strategy for each generated skill.
   - Prefer mechanical, deterministic replacements.
   - If the behavior changed, include the transformation logic and guardrails.
   - Preserve semantics before style.
   - For risky edits, require a preview and a staged rollout.

8. Define the validation for each generated skill.
   - Static checks: lint, type checks, and the build.
   - Behavior checks: tests, snapshots, and selected runtime checks.
   - The migration is accepted when both conditions are true:
     - The scoped paths contain zero known matches of the old pattern.
     - The migration causes no new build or test failures.

9. Deliver the results.
   - Build a migration matrix with these columns:
     - `change_id`
     - the name of the generated skill
     - `compatibility_mode`
     - `safety_label`
     - detection done
     - replacement done
     - validation status
   - Flag the unresolved low-confidence items for manual triage.

## Branching Logic

- If the release notes and the source diff disagree:
  - Trust the official migration guide first, then the changelog, then the code.
  - Mark the conflicting items as `manual-review-required`.

- If the old usage has more than one valid replacement:
  - Split it into separate generated skills, one per scenario.
  - Add explicit applicability rules for each scenario.

- If the replacement changes the semantics:
  - Do not replace the code automatically without a review.
  - Generate a review-first skill with decision checkpoints.

- If the change is `pre-migration-compatible`:
  - Mark the generated skill as `high-safe` by default, unless the evidence shows otherwise.
  - Tell the user that they can apply it now, on the current version.

- If the change is `target-version-only`:
  - Block automatic edits until the target runtime or API is active.
  - Warn the user that the skill can run only after the upgrade.

- If the confidence is low:
  - Allow only detection and reports.
  - Require a human approval before any edit.

## Quality Gates

A generated migration skill is complete only when all of these conditions are true:

- The description is specific and contains the relevant keywords.
- The old and new patterns are concrete and testable.
- The skill declares its compatibility mode explicitly.
- The preconditions and the forbidden conditions are explicit.
- The detection and replacement steps give the same result on every run.
- The validation commands and their expected results are explicit.
- The skill documents its safety limits and the cases for manual review.

## Output Format

When the user invokes this skill, return:

1. The normalized inventory of changes.
2. The list of proposed skills, with the reason for each.
3. For each generated skill:
   - the name
   - the trigger description
   - `compatibility_mode` and the applicability statement
   - `safety_label` and its justification
   - the detection plan
   - the replacement plan
   - the validation plan
   - the risk level
4. The migration matrix and the open questions.

## Example Invocations

- "Create migration skills for Python 3.12 -> 3.13 breaking and deprecated changes used in this repo."
- "Analyze API v1 -> v2 changes and generate one migration skill per endpoint/signature family."
- "From framework release notes 4.x -> 5.x, produce migration skills in safe mode for this codebase."
