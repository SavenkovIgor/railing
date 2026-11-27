---
name: System Layout
applyTo: '**/*'
---

# System layout

Default places of agent files for the Copilot harness, on the system of any user of this plugin.
`~` is the home directory: `%USERPROFILE%` on Windows, `$HOME` on Linux and macOS.
A path without `~` starts at the workspace root.

## Skills

- Personal skills: `~/.copilot/skills/`
- Workspace skills: `.github/skills/`

## Instructions

- Personal instructions: `~/.copilot/copilot-instructions.md` and `~/.copilot/instructions/**/*.instructions.md`
- Workspace instructions: `.github/instructions/**/*.instructions.md`

## Plugins

- Copilot CLI plugins: `~/.copilot/installed-plugins/<marketplace>/<plugin>/`

Why: an agent that knows these paths opens the file at once. Otherwise it asks the user or guesses.
