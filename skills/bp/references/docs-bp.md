# Documentation Validation

Evaluate documentation files for quality and effectiveness.
Verify that the documentation is up to date and accurately reflects the current state of the code.

## Evaluation Framework

### Key Documentation Principles

1. Clarity
   - CL1 Use plain language that the target audience can understand.
   - CL2 Define or explain each project-specific or domain-specific technical
     term and acronym on first use.
   - CL3 Use language, terminology, and detail appropriate for the target audience.
   - CL4 Use grammatically correct language.

2. Conciseness
   - CN1 Omit details that do not affect the reader's decision or next action.
   - CN2 Cover one specific topic or task in each document.
   - CN3 Handle edge cases without letting them dominate the main content.

3. Structure
   - ST1 Pass every check in
     [markdown.instructions.md](../../../rules/markdown.instructions.md).
   - ST2 Put important information at the beginning.
   - ST3 Use headings to organize content and enable scanning.
   - ST4 Use text highlighting with purpose and do not scatter it across the page;
     follow the formatting rules in the [tech-writing skill](../../tech-writing/SKILL.md).
   - ST5 Use consistent styling throughout the document and related documents.
   - ST6 Use working Markdown links for all file references.
   - ST7 Follow the code font rule under "Format technical content" in the
     [tech-writing skill](../../tech-writing/SKILL.md).
   - ST8 Use terminology consistently throughout the document.

### Prose Style

Prose style rules live in one place: the
[tech-writing skill](../../tech-writing/SKILL.md). Read it and check the
documentation's prose against it. Do not restate its rules here.

### Documentation Categories (Diátaxis Framework)

Assess whether the documentation provides adequate coverage across these categories:

1. Tutorials - Help developers learn and get started.
   - TU1 Provide step-by-step instructions for new contributors.
   - TU2 Explain the context and why, as well as how.

2. How-to Guides - Address specific tasks and goals.
   - HT1 Provide clear instructions for common development tasks.
   - HT2 Focus on practical outcomes.

3. Explanation - Provide understanding of concepts and architecture.
   - EX1 Explain the project's structure and design decisions.
   - EX2 Explain relationships between components.

4. Reference - Provide technical specifications.
   - RF1 Make API documentation clear and complete.
   - RF2 Document configuration options.
