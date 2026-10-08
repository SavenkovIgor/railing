# Documentation Validation

Evaluate documentation files for quality and effectiveness.
Verify that the documentation is up to date and accurately reflects the current state of the code.

## Evaluation Framework

### Key Documentation Principles

1. Clarity
   - CL1 Does the documentation use plain language that's easy to understand?
   - CL2 Are technical terms and acronyms properly defined or explained when first introduced?
   - CL3 Is the documentation accessible to the target audience?
   - CL4 Is the documentation grammatically correct?

2. Conciseness
   - CN1 Does the documentation focus on necessary information without overwhelming details?
   - CN2 Is each document focused on a specific topic or task?
   - CN3 Are edge cases appropriately handled without dominating the main content?

3. Structure
   - ST1 Is the documentation in proper, valid markdown format?
   - ST2 Is important information prioritized at the beginning?
   - ST3 Are headings used effectively to organize content and enable scanning?
   - ST4 Is text highlighting used with purpose and not scattered across the page (see the formatting rules in the [tech-writing skill](../../tech-writing/SKILL.md))?
   - ST5 Is styling consistent throughout the document and across related documents?
   - ST6 Do all file references use working markdown links?
   - ST7 Is all code naming formatted with inline `code` markdown?
   - ST8 Is terminology consistent throughout the document?

### Prose Style

Prose style rules live in one place: the
[tech-writing skill](../../tech-writing/SKILL.md). Read it and check the
documentation's prose against it. Do not restate its rules here.

### Documentation Categories (Diátaxis Framework)

Assess whether the documentation provides adequate coverage across these categories:

1. Tutorials - Does it help developers learn and get started?
   - TU1 Are there step-by-step instructions for new contributors?
   - TU2 Do tutorials provide context and explain the "why" along with the "how"?

2. How-to Guides - Does it address specific tasks and goals?
   - HT1 Are there clear instructions for common development tasks?
   - HT2 Are the guides focused on practical outcomes?

3. Explanation - Does it provide understanding of concepts and architecture?
   - EX1 Is there documentation explaining the project's structure and design decisions?
   - EX2 Are relationships between components clearly explained?

4. Reference - Does it provide technical specifications?
   - RF1 Is API documentation clear and complete?
   - RF2 Are configuration options documented?
