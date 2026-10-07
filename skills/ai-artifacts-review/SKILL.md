---
name: ai-artifacts-review
description: >-
  You SHOULD use this skill when asked to audit, review, or improve AI configuration files (instructions, prompts, skills, or agents) — covers frontmatter completeness, scope correctness, structure, and cross-artifact consistency.
user-invocable: true
argument-hint: "Optional: one or more file paths or names to review. If omitted, all AI artifacts in the repo are reviewed."
---

# AI Artifacts Review

## What This Produces

A structured audit of AI context files against official GitHub Copilot and
agent-skill best practices.

Output:

- Per-artifact findings table (file, issue, severity, fix).
- Cross-artifact consistency issues.
- Prioritized fix list ordered by severity.
- A summary of what is already correct.

## Check-ID Prefix Legend

- `FM` — Frontmatter: YAML metadata fields at the top of the file
- `SC` — Scope: whether `applyTo` globs match the content
- `CT` — Content: quality and correctness of the body text
- `PA` — Path: file paths and references within artifacts
- `ST` — Structure: overall organization, length, and modularity
- `PN` — Persona: agent identity and behavioral consistency
- `XA` — Cross-Artifact: consistency between multiple artifacts

**Check execution order:** Apply checks in this sequence to reduce conflicts:
1. `FM` → `SC` → `PA` (structural metadata first)
2. `CT` → `ST` → `PN` (per-artifact content)
3. `XA` (cross-artifact, only when full context is available)

## Procedure

### 0. Read required references first (mandatory)

You SHOULD read the references below before starting the review:

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills Best Practices](https://agentskills.io/skill-creation/best-practices)

Do not begin the audit unless all references listed are fully reviewed and accessible.

### 1. Enumerate artifacts to review

**Scenario A — Specific files passed as arguments:**

1. Restrict the review to exactly those files.
2. Skip the full-repo scan entirely.
3. Skip cross-artifact checks (XA*) unless explicitly requested, since they require full context.
4. Read each specified file fully, including its frontmatter block.

**Scenario B — No files passed:**

1. Collect all files matching:
   - `.copilot/instructions/**/*.instructions.md`
   - `.copilot/prompts/**/*.prompt.md`
   - `.copilot/skills/**/SKILL.md`
   - `.copilot/agents/**/*.agent.md`
   - `.github/copilot-instructions.md`
   - `.github/instructions/**/*.instructions.md`
   - `.github/prompts/**/*.prompt.md`
   - `.github/skills/**/SKILL.md`
   - `.github/agents/**/*.agent.md`
2. Read each file fully, including its frontmatter block.
3. Proceed with both per-artifact and cross-artifact checks.

### 2. Audit artifacts by type

Read **only** the reference files that match the artifact types under review.
Do not read reference files for artifact types that are not in scope.

- **Instructions** (`*.instructions.md`): read [references/instructions.md](references/instructions.md)
- **Prompts** (`*.prompt.md`): read [references/prompts.md](references/prompts.md)
- **Skills** (`SKILL.md`): read [references/skills.md](references/skills.md)
- **Agents** (`*.agent.md`): read [references/agents.md](references/agents.md)

#### 2a. Content checks (all artifact types)

Apply these CT checks to every artifact, regardless of type:

- `CT01` **Rationale section** — If the artifact contains non-obvious design decisions, constraints that differ from common defaults, or rules whose purpose is unclear from context, it SHOULD include a `## Rationale` (or `### Why`) section explaining those choices. Flag absence as `informational`.

### 3. Check cross-artifact consistency

- `XA01` **Path convention alignment** — Skills that generate new artifacts must output to paths consistent with the repo's own artifact layout.
- `XA02` **Instruction overlap** — Two instruction files must not define conflicting rules for the same file type and scope.
- `XA03` **Skill/prompt duplication** — A skill and a prompt covering the same task must be consolidated; prefer the skill if the task is multi-step.
- `XA04` **Extension correctness** — `.instructions.md` suffix is reserved for Copilot auto-loaded instruction files — no other file type should use it.
- `XA05` **Markdown link formatting** — Links in artifact documents should use Markdown link syntax `[description](url)` instead of bare URLs.
- `XA06` **Markdown table alignment** — All Markdown tables must be properly aligned (header, separator, and row cell counts are consistent) across all rows and columns.
- `XA07` **Bold overuse** — If a document uses bold (`**`) on more than 5 distinct words/phrases, suggest replacing some with inline code (`` ` ``) for technical terms, keeping bold only for critical warnings or key concepts.

### 4. IDE validation via `get_errors`

Run `get_errors` on every reviewed file and include the results as-is in the report.
Any error-level finding is **blocking**. Any warning-level finding is **important**.

## Severity Scale

Every finding in the chat report MUST include its emoji marker.
Apply consistently in per-artifact findings, cross-artifact table,
IDE validation results, and the prioritized fix list.

- ❌ `blocking` — The artifact will not work correctly or will cause AI behavior errors
- ⚠️ `important` — The artifact works but is undiscoverable, inconsistent, misleading or wasting token budget
- ℹ️ `informational` — Style, convention, or minor quality improvement

## Output Format

Return sections in this order:

### 1. Artifact Inventory

List every found artifact with its type and path.

### 2. Per-Artifact Findings

For each artifact with at least one issue:

```text
**[filename]** (type)
  [emoji] [severity] [check-id] — description of issue
  Fix: concrete action to take
```

### 3. Cross-Artifact Issues

Table: Issue | Affected Files | Severity | Fix

### 4. IDE Validation Results

For each file where `get_errors` returns findings: list the file and error messages.

### 5. Prioritized Fix List

Ordered: blocking → important → informational.
Each item: priority, file, check-id, one-line description, concrete fix.

### 6. Already Correct

List artifacts and checks that pass without issues. Gives a confidence baseline.

## Completion Criteria

The review is done when ALL of the following are true:

- Every enumerated artifact has been audited against its applicable checks
- `get_errors` has been run on every reviewed file
- The output contains all 6 required sections (Inventory, Findings, Cross-Artifact, IDE Validation, Fix List, Already Correct)
- Every finding has a severity emoji, check-ID, and a concrete fix proposal

## Example Invocations

- "Review all AI context files in this repo."
- "Run the ai-artifacts-review skill — focus on skills only."
- "Check my prompts for best practice violations."
- "Audit the AI artifacts before I add a new skill."
