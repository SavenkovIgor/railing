---
name: tour
description: >-
    You should use this skill when:
    asked to explain, map, or onboard onto an unfamiliar codebase or repository,
    asked how a project is structured or where to change something in it,
    asked to drill into one area of a codebase after a first overview
argument-hint: Optional area to drill into
---

# Tour

Explain an unfamiliar codebase to an engineer who knows the language and tools but not this
project, and who must soon change or review its code. Two levels: a one-page map of the whole
repository, and a drill into one area of it.

## DependsOn

- [reports.instructions.md](/com.github.copilot/rules/reports.instructions.md)

## Inputs

- An optional area from the request: a module, directory, feature, or flow
- No area: run the map level. With an area: run the drill level
- Answer in the language of the request and keep code identifiers as they are
- Answer in chat; the skill creates and changes no files

## Procedure

Map:

1. Read the signals of intent before the source: README, manifests, build files, CI config,
   agent instructions, the top-level tree
2. Find the entry points (main, CLI, server routes, exported API, plugin manifest) and read
   each one fully
3. Trace the one or two flows the project exists for, from entry point to result, and read
   every file on the path
4. Group files into modules by responsibility. Take dependencies from imports, includes, and
   calls, not from folder names
5. Note the terms that appear in names and would not be clear to an outsider
6. For each common change, find the files to edit and the tests that cover them
7. Write the map. For a repository too large to read in one pass, delegate the searching to
   subagents and read the entry points and the flow files yourself

Drill:

1. Run map steps 1-2 without output if the repository is not yet read
2. Read every file of the area fully, its tests, and the call sites at its boundary
3. Write the drill

## Output Format

The map has these `##` sections in this order, in at most 100 lines excluding diagrams:

1. `Purpose`: what the project does and for whom, in 2-3 sentences
2. `Build and run`: commands for build, test, and run. State a command only when a config file
   or CI step defines it, and run none of them
3. `Structure`: a flowchart of the modules, then a table of module, responsibility, and entry file
4. `Main flow`: a sequence diagram, then numbered steps, each with a code link
5. `Terminology`
6. `Where to change`: a table of the change, the files to edit, and the tests that cover them
7. `Watch out`: non-obvious contracts, conventions, generated or vendored code, and hidden
   coupling that a reviewer needs to know. State facts, not judgments
8. `Not read`: the directories and files you skipped
9. `Drill next`: 3-5 areas worth a drill, one line each saying why

The drill has these `##` sections in this order, in at most 150 lines excluding diagrams:

1. `Role`: where the area sits, who calls it, and what it calls
2. `Structure`: a diagram of the area
3. `How it works`: the mechanisms, contracts, and state, with the non-obvious logic
4. `Flow`: numbered steps, each naming the source, the target, what is passed, and a code link
5. `Lifecycle and ownership`: who creates, owns, and destroys long-lived objects, and which
   threads or processes are involved. Omit the section if none apply
6. `Tests`: what covers the area and what does not
7. `Watch out`: as in the map, scoped to the area

## Diagrams

- Write Mermaid in a `mermaid` fence. A diagram is not a code block for the line limit
- Use `flowchart` for structure, `sequenceDiagram` for flows over time, `stateDiagram-v2` for
  lifecycle, and `classDiagram` only for an area built on inheritance
- Keep a diagram to 10 nodes at most; split it instead of shortening labels
- Make each node a module, class, or file that the text links
- Draw only the edges you read in the code, and label each edge with what passes along it
