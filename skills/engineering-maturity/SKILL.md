---
name: engineering-maturity
description: >-
    You SHOULD use this skill when a team asks which engineering practices are missing and in
    what order to adopt them (maturity assessment, practice gap analysis, "what should we
    improve first?"). Do not use it for bug fixes, code review, or architecture decisions.
---

# Engineering maturity

## Goal

Help a team spend limited improvement effort where it matters most. Engineering teams have dozens of practices they *could* adopt - the goal is to surface only the ones that have a measurable effect on maturity for *this* team's size, ranked by the fastest return on that effort.

Do not give generic advice like "improve CI/CD". Name specific practices that fit the team and
the project.

Phase 1 - Repo reconnaissance (automated, no questions needed):
Inspect the repository for specific artifacts. Each artifact is direct evidence that a practice exists or is absent.

Phase 2 - Targeted questions (only for gaps recon couldn't resolve):
Short, closed questions. Not "how is your process?" but "does artifact X exist, yes or no?"

Output - Ranked gap list:
Missing practices sorted by ROI for the team's stratum. Each entry includes: Δ-effect from research, effort estimate, ROI, affected maturity dimensions, and a one-line implementation hint.

## Step 0: Establish Team Size Stratum

**Do this before anything else. Without stratum, all recommendations are unreliable.**

Ask: "How many engineers are on this team (including QA, DevOps, and embedded SRE)?"

Classify as:

- Small: ≤10
- Medium: 11–50
- Large: 51–150
- >150: Note that the source research excluded these teams (sample too small). Recommendations will be extrapolated - state this explicitly.

## Phase 1: Repo reconnaissance

Search the repository for each artifact. Record each as ✔ present / ✘ absent / ? unclear.
Do not assume. If a file is not found, mark ✘.

Read [recon-checklist.md](references/recon-checklist.md) for the artifacts to search for.

## Phase 2: Targeted questions

Ask **only** for items that recon marked ✘ or ? and that have Δ ≥ 2.0 for the team's stratum.
Keep questions binary or single-choice. Do not ask open-ended questions.

Always ask (cannot be inferred from repo):

1. How many engineers are on the team? *(if not yet established)*
2. Does each release have a single named owner (DRI) who is responsible end-to-end?
3. Are secrets stored in a centralized secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager) - not in `.env` files or config repos?
4. When a test fails in CI, does it block the merge, or can developers override and merge anyway?
5. Are your CI/CD pipelines based on a shared template, or does each service maintain its own independently?

Ask only if no onboarding guide was found in recon:
6. Does a written onboarding guide exist outside the repo (Confluence, Notion, internal wiki)?

Ask only if no ADR directory was found:
7. Are significant technical decisions documented anywhere (ADRs, RFCs, decision logs - even informal)?

Ask only if no SLO/SLI files were found:
8. Are SLIs and SLOs defined for any key user-facing flows (availability, latency)?

Ask only if no rollback docs were found:
9. Have you ever deliberately rehearsed a rollback (rolled back a real release to verify the procedure works)?

## Practice data

Read [practice-database.md](references/practice-database.md) before building the gap table.
It holds the glossary, the research source and its limitations, the practice list, Δ and ROI
values, and baseline scores per stratum.

## Output Format

Produce exactly this structure after recon + questions. No generic preambles.

### 1. Team Profile

- Size stratum: Small / Medium / Large / >150-extrapolated
- Evidence sources: repo recon / answers to questions / both
- Confidence: high / partial - explicitly list what could not be determined

### 2. Recon Summary

List every checked artifact as ✔ / ✘ / ? grouped by category. Do not omit ✘ items - they are the input for the gap table.

### 3. Practice Gap Table

Only include practices that are absent (✘ from recon or "no" from questions) and have Δ ≥ 1.5 for this stratum. Sort by ROI descending.

| Priority | Practice | How absence was detected | Δ | Effort (h)                             | ROI | Dimensions affected |
|---                                             |---|---                                     |---  |---                  |
| 1                                              | … | [artifact not found / answer was "no"] | …   | …                   |

### 4. Implementation Order

Weeks 1–2 (ROI > 0.3 - do these first):

- `<practice name>: <one-line implementation hint>`

Weeks 3–5 (ROI 0.1–0.3):

- ...

Weeks 6–8+ (ROI < 0.1 - infrastructure investment):

- …

### 5. Caveats

- List assumptions made due to ? items
- Flag any dimension already at ≥ 7.0 (diminishing returns apply)
- Note if team size > 150 (data extrapolated)
- Note role perception gap if relevant: in the research, developers consistently rate quality 0.6–0.9 points lower than team leads and CTOs on alerting, review, and engagement metrics. If the assessment came from a single role, actual gaps may differ.

## Quality Criteria

A response from this skill is acceptable only if:

- Team size stratum was established before any recommendation was made
- Every recommendation names a specific practice (e.g. "add PR template with rollback field"), not a direction ("improve review quality")
- Every recommendation includes Δ and ROI from [practice-database.md](references/practice-database.md)
- Recon artifacts are listed explicitly as ✔/✘ - not assumed from context
- Observations from recon are separated from assumptions

A response is not acceptable if:

- It recommends "improve CI/CD" without specifying which practice is missing and why
- It gives the same priority list regardless of team size stratum
- It makes recommendations without first checking whether the practice already exists
- It omits Δ and ROI numbers
