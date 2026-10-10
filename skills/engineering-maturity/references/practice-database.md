# Practice database


> Data source: All Δ-effect sizes, ROI estimates, and baseline scores embedded in this file come from:
> [Алексей Обыскалов, «Инженерная зрелость. Исследование практик и триггеров», Habr, Nov 2025](https://habr.com/ru/articles/963202/)
> 106 teams surveyed (developers, team leads, tech leads, CTOs). Groups: ≤10 / 11–50 / 51–150 engineers.
> **Limitations:** Self-assessed data; Russian-speaking team sample; correlation only - causality not established.

## Glossary

Science-adjacent terms used throughout this skill:

| Term | What it means in plain language |
|---|---|
| Δ (delta) | The average difference in maturity score (scale 1–10) between teams that have a practice and teams that don't. Δ=3.0 means teams with the practice score 3 points higher on that metric. |
| ΔR² | How much a block of practices contributes to the model's explanatory power. Testing block ΔR²≈0.43 means testing practices alone account for 43% of what separates mature from immature teams. |
| ROI (here) | Δ effect ÷ estimated implementation effort in person-hours. ROI=1.5 means: 1.5 maturity points gained per hour invested. Higher = faster payoff. |
| Stratum | Team size bracket used in the research: Small (≤10), Medium (11–50), Large (51–150) |
| DRI | Directly Responsible Individual - one named person who owns a release end-to-end |
| SLO | Service Level Objective: the target threshold for a metric (e.g. p95 < 200 ms) |
| SLI | Service Level Indicator: a measured metric (e.g. p95 latency) |

## Recommended practices

The skill recommends specific engineering practices that make delivery more predictable, observable, and repeatable. It focuses on operationally concrete changes rather than generic advice like "improve quality" or "fix CI/CD."

- PR/MR passport: Every change includes three required fields: goal, what was tested, and rollback plan. This improves review quality and makes incident response easier when a change goes wrong.
- Protected branches and PR size-guards: Merges are gated and oversized changes are discouraged. This keeps review cycles manageable and reduces release risk from large, hard-to-audit diffs.
- Managed test data: Test fixtures and snapshots are version-controlled and deterministic - not generated ad-hoc or dependent on live data. Tests use fixtures or snapshots instead of ad-hoc data setup. That raises trust in tests and makes failures easier to reproduce during incidents.
- Automated tests across levels: The skill treats unit, integration, and E2E coverage as a maturity signal, not just raw test count. The point is confidence in changes, not test volume for its own sake.
- Standardized CI/CD pipelines: Delivery pipelines should be based on shared patterns rather than hand-maintained snowflakes per service. Standardization improves pipeline stability, documentation quality, and release predictability.
- Release DRI: Each release has one explicitly responsible owner end-to-end. This reduces coordination ambiguity and makes monitoring, rollback, and follow-up decisions clearer.
- Centralized secrets management: Secrets belong in Vault or a cloud secret manager, not in `.env` files or tracked config. The research links this to stronger security posture and better outcomes in adjacent areas like releases and incidents.
- SLI / SLOs and burn-rate alerts: Key user flows should have explicit reliability targets and alerts tied to error-budget consumption. This improves alert quality by detecting harmful degradation earlier than generic threshold alarms.
- Feature flags and rollback drills: Teams should be able to reduce blast radius and rehearse rollback as a normal operational motion. This makes releases more predictable and lowers the chance that recovery depends on improvisation.
- Onboarding or offboarding guide: A written guide captures setup steps, access expectations, and basic team operating rules. This strengthens documentation and reduces hidden process knowledge.
- Engineering Handbook and ADRs: Teams keep a living guide for recurring practices and a lightweight log of significant technical decisions. These artifacts help scale context-sharing and reduce repeated debate over already-made decisions.

## Embedded practice database

All Δ values passed Welch's t-test + BH-FDR (α=0.05). Practical significance threshold: **Δ ≥ 1.5**.
Effort estimates are for an average team with no prior infrastructure; actual effort will vary.

### Master ROI Table (all strata combined, sorted by ROI descending)

| #  | Practice                                             | Avg Δ | Effort (h) | ROI           | Affected dimensions                                           | Reaches 5+ dims? |
|----|------------------------------------------------------|-------|------------|---------------|---------------------------------------------------------------|------------------|
| 1  | PR/MR "passport" (goal + test notes + rollback plan) | +3.9  | 2–3        | 1.3–1.9   | Incident mgmt, review quality                                 | -                |
| 2  | Protected branches + PR size-guard                   | +3.5  | 3–4        | 0.9–1.2   | Review quality, release stability                             | -                |
| 3  | DRI mechanism for releases                           | +1.5  | 8–10       | 0.15–0.19 | Release predictability, incident mgmt                         | -                |
| 4  | Onboarding / offboarding guide                       | +2.3  | 16–20      | 0.11–0.14 | Docs, alerting, incident mgmt, engagement                     | ✔ 4 dims        |
| 5  | Centralized secrets (Vault / Secret Manager)         | +2.5  | 20–25      | 0.10–0.12 | Alerting, incidents, test trust, docs, release predictability | ✔ 5 dims        |
| 6  | Managed test data (fixtures / snapshots)             | +2.0  | 24–30      | 0.07–0.08 | Test trust, incident mgmt, pipeline stability, review         | ✔ 4 dims        |
| 7  | Living Engineering Handbook + ADR                    | +1.9  | 24         | 0.08      | Documentation, engagement                                     | -                |
| 8  | Burn-rate alerts + SLO thresholds                    | +2.8  | 40         | 0.07      | Alerting quality, system resilience                           | -                |
| 9  | Feature flags + rollback drills                      | +1.8  | 24–28      | 0.06–0.07 | Release predictability, change failure rate                   | -                |
| 10 | Automated tests (unit + integration + E2E)           | +2.2  | varies     | varies        | Review, docs, incidents, alerting                             | ✔ 4 dims        |
| 11 | Standardized CI/CD pipelines                         | +1.6  | 30         | 0.05      | Alerting, docs, CI stability, release predictability          | ✔ 4 dims        |

ROI thresholds: > 1.0 = instant payoff · > 0.3 = high priority · > 0.1 = medium · < 0.1 = long-term investment

### Stratum-Specific Top Effects

Small teams (≤10) - practices with the largest single measured effect:

| Practice                          | Target metric              | Δ        | Notes                                       |
|-----------------------------------|----------------------------|----------|---------------------------------------------|
| PR/MR passport                    | Incident management        | 3.96 | Highest single effect in the entire dataset |
| Dedicated Security / Infosec role | Incident management        | 3.74 |                                             |
| PR/MR size-guard                  | Review quality             | 3.52 |                                             |
| SLI/SLO defined for key flows     | Alerting quality           | 3.35 |                                             |
| Living Engineering Handbook       | Documentation satisfaction | 3.0  |                                             |
| ADR/RFC for significant decisions | Engagement in improvements | 2.96 |                                             |

Medium teams (11–50) - statistically significant effects:

| Practice                               | Target metric       | Δ        | Notes |
|----------------------------------------|---------------------|----------|-------|
| Managed test data (fixtures/snapshots) | Incident management | 2.99 |       |
| Burn-rate alerts + SLO thresholds      | Alerting quality    | 2.19 |       |

> Why so few significant effects at 11–50? This is a statistical artifact, not a content finding. Score variance is lower in this stratum (teams have stabilized), so the difference between "has practice" and "doesn't" becomes harder to detect with this sample size. The practices still matter - the signal is just below the detection threshold.

Large teams (51–150): The research found only 1 significant correlation and 3 significant practices. Large teams have converged on similar practices; variance is minimal. Focus here shifts from *introducing* practices to *deepening* them: standards, mentoring, engineering culture.

### Baseline Maturity Scores by Stratum (from research)

Use these to identify if a dimension is already in the diminishing-returns zone (≥ 7.0):

| Dimension                 | Small (≤10) | Medium (11–50) | Large (51–150)                         |
|---------------------------|-------------|----------------|----------------------------------------|
| Security & Compliance     | 5.50        | -              | **8.33** ← already saturated for large |
| CI/CD Stability           | 5.67        | 7.86       | 7.68                                   |
| Testing & Reliability     | 5.30        | 7.10           | 6.92                                   |
| Monitoring & Incidents    | 6.40    | 5.95           | 5.97                                   |
| Code Review Quality       | 5.17        | 5.79           | 5.51                                   |
| Release Management        | 3.54        | 4.32           | 5.12                                   |
| Documentation & Processes | 3.65        | -              | 5.24                                   |

> After ~7.0 on any dimension: recommend deepening existing practices (standards, mentoring, culture), not adding new ones.
