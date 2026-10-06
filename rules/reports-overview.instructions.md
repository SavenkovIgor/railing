---
name: Overview Report Profile
applyTo: 'reports/**/*.overview.md'
---

# Overview report profile

Describes how a group of existing classes or modules works, to onboard onto it
before changing it. Describe the code as it is; do not critique the design (R7).

## Input

- The classes, files, or modules named in the request
- Read each of them fully; do not skim

## Structure

Use these `##` sections in this order:

1. `Terminology`: domain terms used in the report
2. `Roles and goals`: the shared goal and the role of each class in it
3. `Data flow`: numbered steps of how data moves between classes,
   each step with a code link
4. `Relationships`: inheritance, composition, dependencies
5. `Lifecycle and ownership`: who creates, owns, and destroys each object
6. `Framework patterns`: services, factories, observers, IPC, threads.
   Omit the section if none apply

## Checks

- O1 Every input class or module appears in `Roles and goals`
- O2 Every `Data flow` step names the source, the target, and what is passed
- O3 Every long-lived object has a creator and an owner in `Lifecycle and ownership`
- O4 Threads, processes, or IPC are stated explicitly when present
- O5 The report is at most 100 lines, excluding code blocks
