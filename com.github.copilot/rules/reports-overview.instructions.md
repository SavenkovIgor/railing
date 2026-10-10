---
name: Overview Report Profile
applyTo: 'reports/**/*.overview.md'
---

# Overview report profile

Describes how a group of existing classes or modules works, to onboard onto it
before changing it. Describe the code as it is; do not critique the design.

## Input

- The classes, files, or modules named in the request
- Read each of them fully; do not skim

## Structure

Use these `##` sections in this order:

1. `Terminology`: domain terms used in the report
2. `Roles and goals`: the shared goal and the role of each class in it
3. `Internal mechanisms`: how each class does its job, with the non-obvious
   logic, state, and contracts. This is the most detailed section
4. `Data flow`: numbered steps of how data moves between classes,
   each step with a code link
5. `Relationships`: inheritance, composition, dependencies
6. `Lifecycle and ownership`: which objects are long-lived and which are
   short-lived, and who creates, owns, and destroys each
7. `Framework patterns`: for each class, check whether it follows a known
   pattern (service, repository, factory), works across threads or processes,
   uses IPC, has observers, listeners, or event subscriptions, or has
   non-obvious build or dependency constraints. Omit the section if none apply

## Checks

- O1 Every input class or module appears in `Roles and goals`
- O2 Every `Data flow` step names the source, the target, and what is passed
- O3 Every class in `Roles and goals` has a subsection or paragraph in `Internal mechanisms`
- O4 Every long-lived object has a creator and an owner in `Lifecycle and ownership`
- O5 Threads, processes, or IPC are stated explicitly when present
- O6 The report is at most 250 lines, excluding code blocks
