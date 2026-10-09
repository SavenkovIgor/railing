# Documentation Validation

Evaluate documentation files for quality and effectiveness.
Verify that the documentation is up to date and accurately reflects the current state of the code.
Every rule is a pass/fail check; reviews cite rules by ID.

## Evaluation Framework

### Key Documentation Principles

1. Clarity
   - CL1 No sentence is longer than 30 words, and none uses an idiom or slang.
     Why: long sentences and figurative speech are where readers, and
     especially non-native ones, lose the meaning. The limit is a proxy for
     plain language, so split a long sentence rather than trim words.
   - CL2 Define or explain each project-specific or domain-specific technical
     term and acronym on first use.
   - CL3 The first screen names the audience and its prerequisites
     (for example, "for contributors who know Git"), and every tool, concept,
     or command beyond them is explained or linked where it first appears.
     Why: the reader can only judge fit when the document states who it is for.
   - CL4 Use grammatically correct language.

2. Conciseness
   - CN1 Removing any paragraph would leave a step, decision, or definition
     missing for the task of the document (see CN2).
     Why: every extra paragraph costs reading time and hides the ones that matter.
     Fix a failure by deleting the paragraph, not by shortening it.
   - CN2 Cover one specific topic or task in each document.
   - CN3 Edge cases and exceptions come after the main path or in their own
     section, and take at most a quarter of the document.
     Why: the reader needs the common case first, and a rare case in the
     middle of the steps breaks the flow.

3. Structure
   - ST1 Use valid Markdown.
   - ST2 The first section after the title states what the document is for
     and gives the main answer or action, and background comes after it.
     Why: readers scan the top and leave when it does not answer their question.
   - ST3 Use headings to organize content and enable scanning.
   - ST4 Use text highlighting with purpose and do not scatter it across the page;
     follow the formatting rules in the [tech-writing skill](../../tech-writing/SKILL.md).
   - ST5 Each element type has one form in the document and in the other
     documents of the same directory: one list marker, one heading case, one
     date format, one way to mark a note or warning.
     Why: a changed form reads as a changed meaning.
   - ST6 Use working Markdown links for all file references.
   - ST7 Format all code names with inline `code` Markdown.
   - ST8 No concept is named by two different terms in the document.
     Why: a second term makes the reader look for a second thing.

### Prose Style

Prose style rules live in one place: the
[tech-writing skill](../../tech-writing/SKILL.md). Read it and check the
documentation's prose against it. Do not restate its rules here.

### Documentation Categories (Diátaxis Framework)

Assess whether the documentation provides adequate coverage across these categories:

1. Tutorials - Help developers learn and get started.
   - TU1 Provide step-by-step instructions for new contributors.
   - TU2 Every step, or group of steps, states why it is done or what the
     reader has after it.
     Why: a learner who knows the reason can recover when a step fails.

2. How-to Guides - Address specific tasks and goals.
   - HT1 Provide clear instructions for common development tasks.
   - HT2 Each guide states an outcome the reader can verify, such as a command
     output, a file, or a visible state.
     Why: without a check, the reader cannot tell whether the task is done.

3. Explanation - Provide understanding of concepts and architecture.
   - EX1 Every top-level component or directory is listed with its purpose,
     and every design decision states its reason or the rejected alternative.
     Why: the reasons are what code reading cannot give the newcomer.
   - EX2 Every named component is linked to at least one other component by
     a stated direction (who calls or reads whom) and what passes between them.
     Why: the relationships show how a change in one place reaches the rest.

4. Reference - Provide technical specifications.
   - RF1 Every public symbol in the code (function, class, endpoint, CLI
     command, flag) has its purpose, parameters, return value or output,
     errors, and one example documented.
     Why: the reference is the only place to look up what the code does not
     say. Take the list of public symbols from the code, not from the document.
   - RF2 Document configuration options.
