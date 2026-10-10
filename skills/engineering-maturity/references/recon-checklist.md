# Recon checklist

## Testing

- [ ] Test files exist (any `*test*`, `*spec*` file patterns)
- [ ] Managed test data - check **either**: separate directory (`fixtures/`, `__snapshots__/`, `testdata/`, `test/data/`) **or** inline patterns (`toMatchInlineSnapshot(`, `syrupy` imports, `conftest.py` with fixture functions). Both count; absence of the directory alone is not sufficient evidence of ✘.
- [ ] Test coverage config (`.coveragerc`, `jest.config.*`, `pytest.ini`, `[tool.coverage]` in `pyproject.toml`)
- [ ] E2E test directory (`e2e/`, `cypress/`, `playwright/`, `tests/e2e/`)
- [ ] Flaky test handling config (pytest-rerunfailures, jest `--retries`, quarantine list)

## CI/CD

- [ ] Pipeline definition exists (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `Taskfile.yml`, `Makefile` with CI targets)
- [ ] Evidence of pipeline standardization (shared/reusable workflow files, not per-service copy-paste)
- [ ] PR check gates visible (status checks or required reviewers in branch config)

## PR Hygiene

- [ ] PR/MR template with structured fields (`.github/pull_request_template.md` or `.gitlab/merge_request_templates/`)
- [ ] `CODEOWNERS` file
- [ ] PR size constraints config (danger.js, reviewdog, size-label-bot, `max-pr-lines` settings)

## Security

- [ ] No raw secrets in tracked files (spot-check `.env`, `config/`, `*.yaml` for patterns like `password=`, `secret=`, `token=`)
- [ ] `.env.example` or `*.example` present (signals secrets are externalized)
- [ ] Secret scanning config (`.gitleaks.toml`, `.secretlintrc`, `truffleHog` config, GitHub secret scanning enabled)
- [ ] Dependency update bot (`dependabot.yml`, `renovate.json`)

## Documentation

- [ ] README present and non-trivial (>20 lines, covers local setup)
- [ ] `docs/` or `doc/` directory exists
- [ ] ADR directory (`docs/decisions/`, `docs/adr/`, `adr/`, `rfcs/`)
- [ ] Onboarding guide (`CONTRIBUTING.md`, `docs/onboarding*`, `docs/getting-started*`)
- [ ] CHANGELOG or release notes file

## Release Management

- [ ] Release workflow defined (release pipeline, tagging workflow, `release.yml`)
- [ ] Feature flag references in code (`featureFlag`, `feature_flag`, LaunchDarkly/Flagsmith/Unleash SDK imports)
- [ ] Rollback procedure documented (runbook, release docs with "rollback" section)

## Monitoring & Incidents

- [ ] SLO/SLI definitions (`slo.yml`, `slo/`, docs with "SLO" or "SLI" headings)
- [ ] Alert rule files (`alerts/`, `*.alerts.yaml`, Prometheus recording/alerting rules)
- [ ] Runbooks or playbooks (`runbooks/`, `playbooks/`, `docs/incidents/`)
