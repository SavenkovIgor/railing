---
name: code-overview
description: "You SHOULD use this skill when analyzing code architecture, documenting class relationships, creating code overviews, or explaining data flow between components."
argument-hint: "Classes or files to analyze"
---

# Code Overview

Analyze classes and produce concise architectural documentation about their internal structure, relationships, and interactions.

## When to Use

- Documenting architecture of a group of related classes
- Understanding data flow between components
- Onboarding to an unfamiliar subsystem

## Procedure

### 1. Plan

Create a TODO list with these items:

- Read all provided classes fully, without skipping any parts
- Create empty `code_overview.md` at the project root
- Explain class roles
- Explain internal mechanisms (BE DETAILED — the most important part)
- Explain data flow between classes
- Explain relationships (inheritance, composition, etc.)
- Explain object lifecycle (long-lived? short-lived? creation/destruction ownership?)
- Check framework-specific patterns (if applicable)
- Verify structure and requirements

### 2. Read all source files

Read every provided class from start to end. Do not skip or skim.

### 3. Identify framework-specific patterns

For each class, check where applicable:

- Does it follow a known framework pattern (service, repository, factory, etc.)?
- Does it work across multiple processes or threads?
- Does it use IPC or cross-process communication?
- Does it have observers, listeners, or event subscriptions?
- Are there non-obvious build or dependency constraints?

### 4. Write `code_overview.md`

Create the file at the project root with this structure:

1. Terminology / Definitions
2. Classes, Roles & Goals — what is the global goal and how the classes achieve it together
3. Data Flow — how data flows between classes (DETAILED, human-readable)
4. Relationships — inheritance, composition, dependency
5. Lifecycle / Ownership — who creates, owns, and destroys each object
6. Framework Patterns — findings from step 3 (omit if not applicable)

### 5. Validate output

- Total length ≤ 100 lines
- Valid Markdown
- Links use format: `[ClassOrFunctionName](<path_relative_to_repo_root>#L<line_number>)`
- Every section from step 4 is present
- Data flow explanation is detailed and easy to understand
