# VS Code tasks.json best practices

Target outcomes: discoverability, portability, maintainability.
Discoverability achieved with icons, details, default groups, and hidden helper tasks.
Portability achieved with platform blocks, path variables, and repository-only dependencies.
Maintainability achieved with thin tasks, shared defaults, and a fixed key order.

Sources, read them before validating:

- [Tasks guide](https://code.visualstudio.com/docs/debugtest/tasks)
- [Tasks appendix](https://code.visualstudio.com/docs/reference/tasks-appendix)
- [Variables reference](https://code.visualstudio.com/docs/reference/variables-reference)

## Rule 1: Give every task an icon that matches its purpose

Problem: Tasks without icons are hard to tell apart in the Run Task list and the terminal tabs.
Solution: Set `icon.id` to a codicon that names the action, not the tool.
Reasoning: The icon is the fastest visual cue; a mismatched one misleads.
Example:

| Purpose        | `icon.id`        |
|---             |---               |
| build          | `tools`          |
| package        | `package`        |
| test           | `beaker`         |
| run            | `play`           |
| watch          | `eye`            |
| lint, format   | `checklist`      |
| clean          | `trash`          |
| install, setup | `cloud-download` |
| docs           | `book`           |

## Rule 2: Use icon colors by one fixed scheme

Problem: Random colors carry no meaning and differ from task to task.
Solution: Map a color to a task kind once and apply it to every task of that kind.
`icon.color` accepts only the eight `terminal.ansi*` names.
Reasoning: A reader learns the scheme once and reads the whole list at a glance.
Example: build `terminal.ansiBlue`, test `terminal.ansiGreen`, lint and format
`terminal.ansiYellow`, clean `terminal.ansiRed`, run and watch `terminal.ansiCyan`,
setup `terminal.ansiMagenta`. A compound task takes the color of its main kind.

## Rule 3: Mark one default task per group

Problem: Without a default, `Run Build Task` and `Run Test Task` show a picker every time.
Solution: If the file has build tasks, exactly one has `group.isDefault: true` with
`kind: "build"`. If it has test tasks, exactly one has `kind: "test"` with `isDefault: true`.
Reasoning: Default tasks bind to the hotkeys; several defaults bring the picker back.
Avoid: A default task with `inputs`. It runs often, so a prompt on each run is friction.
Example:

```json
"group": { "kind": "build", "isDefault": true }
```

## Rule 4: Use `label` and `detail` consistently

Problem: Labels mix `Build App`, `build-app`, and `buildApp`; some tasks have a `detail`
and some do not. The Run Task list looks random.
Solution:

- `label`: pick one naming style (CamelCase, kebab-case, Title Case) and use it in every
  label
- `detail`: either every task has one or none does; the text is free plain text

Reasoning: Uniform names are predictable to type in the picker and to reference from
`dependsOn` and `preLaunchTask`.

## Rule 5: Fold near-duplicate tasks into inputs

Problem: Tasks that differ by one argument (configuration, target, test filter) multiply.
Solution: Replace the copies with one task and `${input:id}`. Types: `promptString`,
`pickString`, `command`.
Reasoning: One task is one place to fix. Inputs cannot be nested.
Avoid: Inputs in tasks that Rule 3 makes default, and in tasks that other tasks depend on.

## Rule 6: Describe `pickString` options with label and value

Problem: Raw option strings show cryptic values in the dropdown.
Solution: An option is a string or an object with `label` and `value`; the dropdown
shows `label: value`. Every input has `description`. Set `default` and make it one of
the option `value` entries, not a label.
Reasoning: A default keeps the common case to one keypress.
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

## Rule 7: Keep one key order in every task

Problem: Random key order makes diffs noisy and tasks hard to scan.
Solution: Order keys as follows and omit the ones a task does not use:
`label`, `detail`, `hide`, `icon`, `group`, `type`, `command`, `args`, `dependsOn`,
`dependsOrder`, `isBackground`, platform blocks (`windows`, `linux`, `osx`), `options`
(with `shell`), `presentation`, `problemMatcher`, `runOptions`.
Reasoning: Identity and visibility come first, then what runs, then how it looks.

## Rule 8: Hoist repeated fields to the top level

Problem: The same `presentation`, `problemMatcher`, `options`, or `type` repeated in every
task drifts apart.
Solution: Set these once at the top level. A task overrides a property by defining it
with a different value. Keep `version` first.
Reasoning: Task properties override global ones, so only the exceptions stay in tasks.
Avoid: A global `problemMatcher` that most tasks do not need. Tasks that never print
problems set `"problemMatcher": []`.

## Rule 9: Hide tasks that nobody runs directly

Problem: Helper tasks clutter the Run Task list.
Solution: Set `hide: true` on every task that is only a dependency or a prelaunch task.
Reasoning: Hidden tasks stay usable through `dependsOn` and `preLaunchTask`.
Avoid: Hiding a default task.

## Rule 10: Compose with `dependsOn`

Problem: A task that does "build, then test" in one shell line duplicates both tasks.
Solution: Keep build and test as separate hidden tasks. Add a compound task with
`dependsOn` listing both. Set `dependsOrder: "sequence"` when order matters;
the default is parallel, and the order is not recursive.
Reasoning: Each step stays reusable and keeps its own problem matcher.

## Rule 11: Set `presentation` on purpose

Problem: Default presentation reveals and reuses the terminal the same way for all tasks.
Solution: Choose the properties by task kind:

| Kind               | `presentation`                                            |
|---                 |---                                                        |
| build              | `reveal: "silent"`, `revealProblems: "onProblem"`         |
| test, run          | `reveal: "always"`, `panel: "dedicated"`, `clear: true`   |
| watch, background  | `reveal: "never"`, `panel: "dedicated"`                   |
| short helper       | `reveal: "never"`, `close: true`                          |

Reasoning: `silent` brings the panel up only if the output is not scanned for problems,
and `revealProblems` opens the Problems panel only when there is something to show.

## Rule 12: Make cross-platform tasks work on every platform

Problem: A `command` that works on one OS breaks the file for the rest of the team.
Solution: Choose per task:

- Same command everywhere: one `command`
- Different command: a base `command` and an override in `windows`, `linux`, or `osx`
- Different shell setup for a whole platform: a platform block at the top level

Prefer `type: "process"` with `args` when no shell feature (pipe, `&&`, glob) is needed;
there is no shell to differ and no quoting to get wrong.
Reasoning: Platform properties override task and global ones for that platform only.

## Rule 13: Write paths from the workspace root with `${/}`

Problem: Absolute paths, `~`, and hard-coded `/` or `\` fail on other machines.
Solution: Start every path with `${workspaceFolder}`, separate with `${/}`
(shorthand for `${pathSeparator}`). Use `${workspaceFolder}`, not the deprecated
`${workspaceRoot}`.
Example: `"${workspaceFolder}${/}scripts${/}build.sh"`
Avoid: Using `${/}` where the shell on Windows is bash. It expands to `\`, which bash
reads as an escape; use `/` there.

## Rule 14: Use platform variables only in platform blocks

Problem: `${env:USERPROFILE}` on Linux and `${env:HOME}` on Windows resolve to nothing.
Solution: In a cross-platform file, put variables that exist on one OS only inside that
OS block.
Reasoning: `options.env` values are visible to the started process only; they are not
substituted into `command` or `args`. Read an existing variable with `${env:NAME}`.

## Rule 15: Fix the shell per platform in the file

Problem: The shell comes from the user's terminal profile, so the same task behaves
differently on each machine.
Solution: Set `options.shell` in `tasks.json` (top level, overridden in platform
blocks), not in user settings or `terminal.integrated.automationProfile.*`.
Pick one shell per platform and use it in every task.
Reasoning: The file carries its own contract and works without per-user setup.
Avoid: `bash` as the Windows shell unless the repo documents Git Bash as a prerequisite;
plain `bash` on Windows can resolve to WSL. A task also runs in a non-login,
non-interactive shell, so it must not rely on `.bashrc` or `nvm` setup.
Example:

```json
"options": {
    "shell": { "executable": "bash", "args": ["-c"] }
},
"windows": {
    "options": {
        "shell": { "executable": "powershell.exe", "args": ["-NoProfile", "-Command"] }
    }
}
```

## Rule 16: Keep tasks thin

Problem: Long command lines, pipes, and conditionals in JSON are untestable and hard to
escape.
Solution: A task runs one existing script or tool with arguments. Logic lives in
scripts the repo already has and that run outside VS Code too.
Reasoning: `tasks.json` is a launcher, not a build system.

## Rule 17: Depend on the repository only

Problem: A task that calls a script outside the repo, or a tool that is not documented,
works on one machine.
Solution: Reference only files under `${workspaceFolder}` and tools that the README lists
as prerequisites. Use `${userHome}` or absolute paths only for locations
that exist on every machine.
Reasoning: Everyone who opens the file must be able to run the task.

## Rule 18: Give problem-producing tasks a working problem matcher

Problem: Build and lint output without a matcher gives no Problems panel entries; a wrong
pattern gives false ones.
Solution: Use a built-in matcher (`$gcc`, `$tsc`, `$eslint-stylish`) or a custom `pattern`
that is tested against real output. Set `fileLocation` so paths resolve against
`${workspaceFolder}`. A background task needs a `background` block with
`beginsPattern` and `endsPattern` and `isBackground: true`.
Reasoning: A background task without a matcher never reports that it finished.

## Rule 19: Keep the file free of IDE problems

Problem: Warnings from the editor point to ignored or invalid properties.
Solution: Open the file and clear the Problems panel for it. Remove deprecated
properties (`isShellCommand`, `showOutput`, `echoCommand`, `suppressTaskName`,
`isBuildCommand`, `isTestCommand`).
Reasoning: Schema warnings usually mean VS Code silently ignores the property.

## Rule 20: Do not start tasks automatically

Problem: `runOptions.runOn: "folderOpen"` runs a command as soon as the folder opens.
Solution: Avoid it. If the task is a real need, document it and keep it side-effect free.
Reasoning: A task that starts on open runs repository code before the contributor reads it.

## Cross-platform strategies

Problem: Tasks run on the contributor's OS, shell, and installed tools. One command line
rarely works on Windows, Linux, and macOS alike.
Solution: Pick one strategy for the repository, document its prerequisites in the README,
and apply it to every task. Do not mix strategies in one file.
Reasoning: A mixed file needs the prerequisites of every strategy and breaks in
unexpected places.

| Strategy                  | Prerequisites               | Use when                                |
|---                        |---                          |---                                      |
| Dev container             | Docker, Dev Containers      | the project builds on Linux only        |
| Git Bash and Python (uv)  | Git for Windows, uv         | tasks need real logic on every OS       |
| Command per platform      | none beyond the toolchain   | tasks are one-line calls to a tool      |
| Cross-platform tool       | that tool                   | one tool (npm, cargo, cmake) does it    |

### Dev container

- Define the environment in `.devcontainer/devcontainer.json`; the tasks then run inside
  the Linux container, so one shell and one set of paths is enough
- No `windows` or `osx` blocks, no `${/}` workarounds
- Costs: Docker on every machine, slower file access on Windows and macOS bind mounts,
  no native Windows or macOS tools

### Git Bash and Python with uv

- Windows uses the bash from Git for Windows, Linux and macOS use their own bash; tasks
  call bash scripts that stay trivial or call `uv run script.py`
- Logic lives in Python scripts, not in `.sh` and `.cmd` pairs; uv installs the pinned
  Python and dependencies, so scripts need no manual setup
- Set the bash executable per platform in `options.shell` (Rule 15) and write paths
  with `/`, not `${/}` (Rule 13)
- Costs: two tools to install on Windows; plain `bash` may resolve to WSL, so point to
  the Git for Windows binary

### Command per platform

- One `command` plus overrides in `windows`, `linux`, or `osx` (Rule 12), usually
  `scripts/test.sh` next to `scripts/test.cmd`
- Costs: every script exists twice and drifts apart; keep each one a thin call to the
  same tool

### Cross-platform tool

- `type: "process"` with the tool and `args`, such as `npm run build` or
  `cmake --build`; no shell, no per-OS blocks
- Costs: the tool must be installed and behave the same on all platforms
