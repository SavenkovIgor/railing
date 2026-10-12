# VS Code tasks.json best practices

Target outcomes: discoverability, portability, maintainability.
Discoverability achieved with icons, details, default groups, and hidden helper tasks.
Portability achieved with platform blocks, path variables, and repository-only dependencies.
Maintainability achieved with thin tasks, shared defaults, and a fixed key order.

Sources, read them before validating:

- [Tasks guide](https://code.visualstudio.com/docs/debugtest/tasks)
- [Tasks appendix](https://code.visualstudio.com/docs/reference/tasks-appendix)
- [Variables reference](https://code.visualstudio.com/docs/reference/variables-reference)

## Rule 1: Give every task a matching icon and a consistent color

Problem: Tasks without icons are hard to tell apart; random colors carry no meaning.
Solution: Set `icon.id` (codicon) by purpose and `icon.color` by task kind, one scheme
for the whole file. `icon.color` accepts only the eight `terminal.ansi*` names.
A compound task takes the icon and color of its main kind.
Reasoning: The icon is the fastest cue in the Run Task list and terminal tabs.
Example:

| Kind           | `icon.id`        | `icon.color`           |
|---             |---               |---                     |
| build          | `tools`          | `terminal.ansiBlue`    |
| test           | `beaker`         | `terminal.ansiGreen`   |
| run, watch     | `play`, `eye`    | `terminal.ansiCyan`    |
| lint, format   | `checklist`      | `terminal.ansiYellow`  |
| clean          | `trash`          | `terminal.ansiRed`     |
| install, setup | `cloud-download` | `terminal.ansiMagenta` |

## Rule 2: Mark exactly one default task per group

Problem: Without a default, `Run Build Task` and `Run Test Task` show a picker; several
defaults bring the picker back.
Solution: If the file has build tasks, one has `"group": { "kind": "build", "isDefault": true }`.
Do the same with `kind: "test"` if it has test tasks.
Avoid: `inputs` in a default task. It runs often, and a prompt on each run is friction.

## Rule 3: Use `label` and `detail` consistently

Problem: Labels mix `Build App`, `build-app`, and `buildApp`; some tasks have a `detail`
and some do not.
Solution:

- `label`: pick one naming style (CamelCase, kebab-case, Title Case) for every label
- `detail`: either every task has one or none does; the text is free plain text

Reasoning: Uniform names are predictable to type and to reference from `dependsOn`
and `preLaunchTask`.

## Rule 4: Fold near-duplicate tasks into inputs

Problem: Tasks that differ by one argument (configuration, target, test filter) multiply.
Solution: Replace the copies with one task and `${input:id}` (`promptString`, `pickString`,
`command`; nesting is not supported). Every input has `description`.
A `pickString` option is a string or an object with `label` and `value`; the dropdown
shows `label: value`. Set `default` to one of the option values, not a label.
Example:

```json
{
    "id": "configuration",
    "type": "pickString",
    "description": "Build configuration",
    "options": [
        { "label": "Debug", "value": "debug" },
        { "label": "Release", "value": "release" }
    ],
    "default": "debug"
}
```

## Rule 5: Keep one key order in every task

Problem: Random key order makes diffs noisy and tasks hard to scan.
Solution: Order keys as follows and omit the unused ones: `label`, `detail`, `hide`, `icon`,
`group`, `type`, `command`, `args`, `dependsOn`, `dependsOrder`, `isBackground`, platform
blocks (`windows`, `linux`, `osx`), `options` (with `shell`), `presentation`,
`problemMatcher`, `runOptions`.
Reasoning: Identity and visibility come first, then what runs, then how it looks.

## Rule 6: Hoist repeated fields to the top level

Problem: The same `presentation`, `problemMatcher`, `options`, or `type` repeated in every
task drifts apart.
Solution: Set these once at the top level after `version`; a task overrides a property by
defining it with a different value. Tasks that never print problems set
`"problemMatcher": []`.
Avoid: A global `problemMatcher` that most tasks do not need.

## Rule 7: Hide helper tasks and compose them with `dependsOn`

Problem: Helper tasks clutter the Run Task list; "build, then test" in one shell line
duplicates both tasks.
Solution: Set `hide: true` on every task that is only a dependency or a prelaunch task.
Keep build and test as separate hidden tasks and add a compound task with `dependsOn`.
Set `dependsOrder: "sequence"` when order matters; the default is parallel and the order
is not recursive.
Avoid: Hiding a default task.

## Rule 8: Set `presentation` on purpose

Problem: Default presentation treats every task the same.
Solution: Choose the properties by task kind:

| Kind              | `presentation`                                          |
|---                |---                                                      |
| build             | `reveal: "silent"`, `revealProblems: "onProblem"`       |
| test, run         | `reveal: "always"`, `panel: "dedicated"`, `clear: true` |
| watch, background | `reveal: "never"`, `panel: "dedicated"`                 |
| short helper      | `reveal: "never"`, `close: true`                        |

Reasoning: `silent` brings the panel up only if the output is not scanned for problems;
`revealProblems` opens the Problems panel only when there is something to show.

## Rule 9: Write paths from the workspace root with `${/}`

Problem: Absolute paths, `~`, and hard-coded `/` or `\` fail on other machines.
Solution: Start every path with `${workspaceFolder}` (not the deprecated
`${workspaceRoot}`) and separate with `${/}`, the shorthand for `${pathSeparator}`.
Example: `"${workspaceFolder}${/}scripts${/}build.sh"`
Avoid: `${/}` where the Windows shell is bash. It expands to `\`, which bash reads as an
escape; use `/` there.

## Rule 10: Override commands and variables per platform

Problem: A `command` or variable that exists on one OS breaks the file for the rest.
Solution: One `command` if it works everywhere; otherwise a base `command` with an
override in `windows`, `linux`, or `osx`. In a cross-platform file, keep variables that
exist on one OS (`${env:USERPROFILE}`, `${env:HOME}`) inside that OS block.
Prefer `type: "process"` with `args` when no shell feature (pipe, `&&`, glob) is needed:
no shell differs and no quoting can go wrong.
Reasoning: Platform properties override task and global ones for that platform only.
`options.env` values reach the started process only; they are not substituted into
`command` or `args`.

## Rule 11: Fix the shell per platform in the file

Problem: The shell comes from the user's terminal profile, so the same task behaves
differently on each machine.
Solution: Set `options.shell` in `tasks.json` (top level, overridden in platform blocks),
not in user settings or `terminal.integrated.automationProfile.*`. Use one shell per
platform in every task.
Avoid: `bash` as the Windows shell unless the README lists Git Bash as a prerequisite;
plain `bash` can resolve to WSL. Tasks run in a non-login, non-interactive shell, so they
must not rely on `.bashrc` or `nvm` setup.
Example:

```json
"options": { "shell": { "executable": "bash", "args": ["-c"] } },
"windows": {
    "options": {
        "shell": { "executable": "powershell.exe", "args": ["-NoProfile", "-Command"] }
    }
}
```

## Rule 12: Keep tasks thin and repository-only

Problem: Long command lines in JSON are untestable and hard to escape; a task that needs
files or tools outside the repo works on one machine.
Solution: A task runs one existing script or tool with arguments. Logic lives in scripts
that also run outside VS Code. Reference only files under `${workspaceFolder}` and tools
the README lists as prerequisites.
Reasoning: `tasks.json` is a launcher, not a build system, and everyone who opens it must
be able to run it.

## Rule 13: Give problem-producing tasks a working matcher and keep the file clean

Problem: Build output without a matcher fills no Problems panel; a wrong pattern fills it
with false entries; editor warnings mean VS Code ignores a property.
Solution: Use a built-in matcher (`$gcc`, `$tsc`, `$eslint-stylish`) or a custom `pattern`
tested against real output, with `fileLocation` resolving against `${workspaceFolder}`.
A background task needs `isBackground: true` and a `background` block with
`beginsPattern` and `endsPattern`; without it the task never reports that it finished.
The file has no IDE problems and no deprecated properties (`isShellCommand`,
`showOutput`, `echoCommand`, `suppressTaskName`, `isBuildCommand`, `isTestCommand`).

## Rule 14: Do not start tasks automatically

Problem: `runOptions.runOn: "folderOpen"` runs a command as soon as the folder opens.
Solution: Avoid it. If a task needs it, document it and keep it free of side effects.
Reasoning: The task runs repository code before the contributor reads it.

## Cross-platform strategies

Problem: Tasks run on the contributor's OS, shell, and tools. One command line rarely
works on Windows, Linux, and macOS alike.
Solution: Pick one strategy for the repository, list its prerequisites in the README,
and apply it to every task. Mixing strategies needs the prerequisites of all of them.

| Strategy                 | Prerequisites             | Use when                             |
|---                       |---                        |---                                   |
| Dev container            | Docker, Dev Containers    | the project builds on Linux only     |
| Git Bash and Python (uv) | Git for Windows, uv       | tasks need real logic on every OS    |
| Command per platform     | the toolchain only        | tasks are one-line calls to a tool   |
| Cross-platform tool      | that tool                 | one tool (npm, cargo, cmake) does it |

- Dev container: define `.devcontainer/devcontainer.json`; tasks run in a Linux container,
  so there are no `windows` or `osx` blocks. Costs: Docker everywhere, slower bind mounts
  on Windows and macOS, no native tools.
- Git Bash and Python (uv): bash comes from Git for Windows on Windows and from the OS
  elsewhere; logic lives in Python scripts started with `uv run script.py`, not in
  `.sh` and `.cmd` pairs. Set the shell per Rule 11 and write paths with `/` (Rule 9).
  Costs: two tools on Windows; point to the Git binary so `bash` does not resolve to WSL.
- Command per platform: Rule 10, usually `scripts/test.sh` next to `scripts/test.cmd`.
  Costs: every script exists twice and drifts; keep each a thin call to the same tool.
- Cross-platform tool: `type: "process"` with `args`, such as `npm run build`; no shell and
  no per-OS blocks. Costs: the tool must behave the same everywhere.
