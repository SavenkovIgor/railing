---
name: bp
description: >-
  You should use this skill when checking or validating files against best-practice
  references, including code, documentation, configuration, and skill files.
argument-hint: "File path(s) to validate"
user-invocable: true
---

# Best Practices Validation

Validate given file(s) against best practice references using parallel sub-agents.

## Response Format

All sub-agents must return their findings in this structure:

```plaintext
## [Reference Name] Validation

### Summary
One or two sentences: overall verdict for this file against this reference.

### Findings
For each issue found:
- **[severity: blocking | important | style]** - [Rule or principle violated]
  - Location: [file:line, or "n/a"]
  - Found: [the problematic fragment or pattern]
  - Fix: [the corrected version or recommended action]

### Compliant
Bulleted list of checks from the reference that the file satisfies. Omit this section if nothing passes.

### Priority Actions
Numbered list of the 2–3 most important changes, in order of impact.
```

## Procedure

### 1. Inspect the target file

Read each file passed as argument. Identify its type, purpose, and content domain - enough to know which references apply. Do **not** read the reference files.

### 2. Select relevant references

Choose only the references that match the file under review:

| Reference                                       | When it applies                                                                  |
|---                                              |---                                                                               |
| [chromium](references/chromium-bp.md)           | Chromium-style C++ files: `*.{cc,cpp,h,hpp}`                                                |
| [cicd](references/cicd-bp.md)                   | `.github/workflows/`, `.gitlab-ci.yml`, pipeline configs                         |
| [cmake](references/cmake-bp.md)                 | `CMakeLists.txt`, `*.cmake` files; build configuration and dependency management |
| [cpp-file-naming](references/cpp-file-naming-bp.md) | C++ file and directory names and extensions: `*.{cpp,hpp,cppm,ipp,h,cc,C,H,c++,h++}` |
| [devops](references/devops-bp.md)               | `*.tf`, `ansible*.yml`, provisioning and configuration management files          |
| [docker](references/docker-bp.md)               | `Dockerfile*`, `*.dockerfile`, `docker-compose*.yml`, `compose*.yml`             |
| [docs](references/docs-bp.md)                   | Documentation `*.md` files (README, guides, wikis), except `reports/**/*.md`    |
| [markdown](/com.github.copilot/rules/markdown.instructions.md) | Any `*.md` file, except `reports/**/*.md`                                        |
| [python](references/python-bp.md)               | Any `*.py` file                                                                  |
| [builds](references/reproducible-builds.md)     | Build scripts, lock files, CI configs                                            |
| [skill](references/skill-bp.md)                 | `SKILL.md` files                                                                 |
| [standards](references/standards-bp.md)         | Code files; or when explicit standards/RFC/OWASP/ISO check requested             |
| [system-design](references/system-design-bp.md) | Design specs and proposals describing a system to be built or changed           |
| [report-review](/skills/report-review/SKILL.md)       | Report files matching `reports/**/*.md`                                          |

A single file may match multiple references.

### 3. Spawn one sub-agent per reference

For each selected reference, launch a sub-agent and pass it exactly three things:

1. The target file - full path and content
2. The reference file - full path of the matching `*-bp.md`
3. The response format - the exact template defined in the "Response Format" section above

Instruct each sub-agent to: read the target file and the reference file, validate the file against every criterion in the reference, and return findings using the provided format. Sub-agents work in parallel.

### 4. Aggregate and report

Collect all sub-agent responses. Present them in order of severity (blocking findings first). If multiple sub-agents flag the same issue, merge into one entry and note both references.
