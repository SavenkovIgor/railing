---
name: migration-skill-factory
description: "You SHOULD use this skill if API/language versions changed and you need skills to migrate old usage across a codebase."
argument-hint: "What changed (old -> new), version range, and target repo scope"
user-invocable: true
---

# Migration Skill Factory

## What This Produces

This meta-skill creates a set of migration skills from a version or API update.

Output:
- A normalized change list between old and new behavior.
- A migration plan with priorities and risk tags.
- One concrete migration skill per change type.
- Compatibility classification for each generated skill.
- Verification checklist for each generated migration skill. #changes

## When to Use

Use this skill when at least one is true:
- A language, framework, SDK, or product version was upgraded.
- API signatures, semantics, defaults, deprecations, or behavior changed.
- You need repeatable codebase-wide refactoring instructions.
- You want migration work split into focused skills instead of one large prompt.

## Required Inputs

- Subject of migration: language/API/product and target versions.
- Source of truth links or files:
  - Preferred: official release notes, migration guides, changelogs.
  - Fallback: old/new source code and docs snapshots.
- Target codebase scope: full repo or selected folders.
- Risk tolerance: strict safe mode or aggressive replacement mode.
- Runtime versions:
  - current version in production/dev
  - target version after migration

## Procedure

1. Build migration context.
   - Confirm old state and new state.
   - Identify compatibility surface: syntax, signatures, runtime behavior, tooling.
   - Define scope boundaries and exclusions.

2. Collect authoritative changes.
   - Parse release notes first.
   - If notes are incomplete, inspect source/API diff to fill gaps.
   - Normalize every change into one record:
     - change_id
     - category (syntax, API, behavior, config, tooling, deprecation, removal)
     - old_pattern
     - new_pattern
     - caveats
     - confidence (high/medium/low)
     - compatibility_mode (pre-migration-compatible | target-version-only)
     - evidence link

3. Classify compatibility and safety.
   - For each change, decide if it can be applied safely before switching runtime/API version.
   - Set compatibility_mode:
     - pre-migration-compatible: safe to apply on current version and stays valid on target version.
     - target-version-only: should be applied only after runtime/API switch.
   - Set safety_label:
     - high-safe: deterministic, backwards-compatible, no behavior drift expected.
     - medium-safe: mostly mechanical but requires local verification.
     - review-required: semantics may differ or tooling evidence is weak.
   - Add explicit user notice to every generated skill:
     - when it can be run
     - when it must not be run
     - why

4. Prioritize changes.
   - Score each change by impact and migration complexity.
   - Mark blocking changes first (compile/runtime breakage).
   - Group related records into migration units.

5. Generate one migration skill per migration unit.
   - Ask the user where to place the new skill (e.g., `.copilot/skills/` or `.github/skills/`) before creating any files.
   - Create folder `<chosen-path>/<unit-name>/`.
   - Start from [migration skill template](assets/migration-skill-template.md).
   - Create SKILL.md with:
     - precise trigger description (keywords from old API and new API)
     - compatibility and applicability section
     - exact detection strategy for old usage
     - replacement strategy with safety checks
     - validation steps and rollback criteria
   - Keep each generated skill narrowly scoped to one migration unit.

6. Define detection strategy for each generated skill.
   - Search patterns:
     - symbol names
     - call signatures
     - config keys
     - imports/modules
   - Add false-positive guards.
   - Note context-dependent cases requiring manual review.

7. Define replacement strategy for each generated skill.
   - Prefer mechanical, deterministic replacements.
   - If behavior changed, include transformation logic and guardrails.
   - Preserve semantics before style.
   - For risky edits, require preview and staged rollout.

8. Define validation for each generated skill.
   - Static checks: lint/type/build.
   - Behavior checks: tests, snapshots, selected runtime checks.
   - Migration acceptance criteria:
     - zero known old-pattern matches in scoped paths
     - no new build or test regressions attributable to migration

9. Package delivery.
   - Produce migration matrix table:
     - change_id
     - generated skill name
     - compatibility_mode
     - safety_label
     - detection done
     - replacement done
     - validation status
   - Flag unresolved low-confidence items for manual triage.

## Branching Logic

- If release notes and source diff disagree:
  - Trust official migration guide first, then changelog, then code inspection.
  - Mark conflicting items as manual-review-required.

- If old usage has multiple valid replacements:
  - Split into separate generated skills by scenario.
  - Add explicit applicability rules for each scenario.

- If replacement is not semantics-preserving:
  - Do not auto-replace blindly.
  - Generate a review-first skill with decision checkpoints.

- If change is pre-migration-compatible:
  - Mark generated skill as high-safe by default unless evidence suggests otherwise.
  - Explicitly inform user it can be applied now on current version.

- If change is target-version-only:
  - Block automatic edit mode until target runtime/API is active.
  - Explicitly warn user the skill is post-upgrade-only.

- If confidence is low:
  - Restrict to detection/report mode only.
  - Require human approval before edits.

## Quality Gates

Generated migration skills are complete only if all are true:
- Description is specific and keyword-rich.
- Old/new patterns are concrete and testable.
- Compatibility mode is explicitly declared.
- Preconditions and forbidden-conditions are explicit.
- Detection and replacement steps are reproducible.
- Validation commands and expected outcomes are explicit.
- Safety limits and manual-review cases are documented.

## Output Contract

When invoked, return:
1. Change inventory (normalized).
2. Proposed generated-skill list with rationale.
3. For each generated skill:
   - name
   - trigger description
  - compatibility_mode and applicability statement
  - safety_label and justification
   - detection plan
   - replacement plan
   - validation plan
   - risk level
4. Migration matrix and open questions.

## Example Invocation Ideas

- "Create migration skills for Python 3.12 -> 3.13 breaking and deprecated changes used in this repo."
- "Analyze API v1 -> v2 changes and generate one migration skill per endpoint/signature family."
- "From framework release notes 4.x -> 5.x, produce migration skills in safe mode for this codebase."

## Asset Reference

- Child skill template: [migration skill template](assets/migration-skill-template.md)
