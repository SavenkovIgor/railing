---
name: bp
description: >-
  You should use this skill when checking or validating files against best-practice
  references, including code, documentation, configuration, and skill files.
argument-hint: "File path(s) to validate"
user-invocable: true
---

# Best Practices Validation

## DependsOn

- [markdown.instructions.md](/com.github.copilot/rules/markdown.instructions.md) (docs.md)
- [prose.instructions.md](/com.github.copilot/rules/prose.instructions.md) (docs.md)

Validate given file(s) against best practice references using parallel sub-agents.

## Response Format

All sub-agents must return their findings in this structure:

```text
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

| Reference                                                    | When it applies                                                                         |
|---                                                           |---                                                                                      |
| [chromium](references/chromium.md)                           | Chromium-style C++ files: `*.{cc,cpp,h,hpp}`                                            |
| [cicd](references/cicd.md)                                   | `.github/workflows/`, `.gitlab-ci.yml`, pipeline configs, build scripts, lock files     |
| [cmake](references/cmake.md)                                 | `CMakeLists.txt`, `*.cmake` files; build configuration and dependency management        |
| [cpp-file-naming](references/cpp-file-naming.md)             | C++ file and directory names and extensions: `*.{cpp,hpp,cppm,ipp,h,cc,C,H,c++,h++}`    |
| [devops](references/devops.md)                               | `*.tf`, `ansible*.yml`, provisioning and configuration management files                 |
| [docker](references/docker.md)                               | `Dockerfile*`, `*.dockerfile`, `docker-compose*.yml`, `compose*.yml`                    |
| [docs](references/docs.md)                                   | Documentation `*.md` files (README, guides, wikis), except `reports/**/*.md`            |
| [engineering-standards](references/engineering-standards.md) | Only when published standards (RFC, OWASP, ISO, style guides) are relevant or requested |
| [python](references/python.md)                               | Any `*.py` file                                                                         |
| [skill](references/skill.md)                                 | `SKILL.md` files                                                                        |
| [system-design](references/system-design.md)                 | Design specs and proposals describing a system to be built or changed                   |
| [vscode-tasks](references/vscode-tasks.md)                   | `.vscode/tasks.json`, `*.code-workspace` files with a `tasks` section                   |
| [report-review](/skills/report-review/SKILL.md)              | Report files matching `reports/**/*.md`                                                 |

A single file may match multiple references.

### 3. Spawn one sub-agent per reference

For each selected reference, launch a sub-agent and pass it exactly four things:

1. The target file - full path and content
2. The reference file - full path of the file linked in the table above
3. The response format - the exact template defined in the "Response Format" section above
4. The dependency files - full paths of the files in "DependsOn" whose parenthetical names this reference; none if no entry names it

Instruct each sub-agent to: read the target file, the reference file, and the dependency files, validate the file against every criterion in the reference and in the dependency files as a whole, and return findings using the provided format. Sub-agents work in parallel.

### 4. Aggregate and report

Collect all sub-agent responses. The final report keeps the structure of the "Response Format" section (`Summary`, `Findings`, `Compliant`, `Priority Actions`), with one block per target file. Instead of a reference name, the block heading names the target file.

- Findings: list in order of severity (blocking first). If multiple sub-agents flag the same issue, merge it into one entry with the highest severity among them. Replace the single reference name with a `References:` line that names every reference that reported the issue.
- Summary: one or two sentences covering all references applied to the file.
- Compliant: checks that every applicable reference reports as satisfied.
- Priority Actions: the 2-3 most important changes across all references.

The run is done when every selected reference has a returned response and every finding from those responses is either listed or merged into a listed entry. If a sub-agent returned no response, re-run it before reporting.
