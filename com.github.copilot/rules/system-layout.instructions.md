---
name: System Layout
applyTo: '**/*'
---

# System layout

Default places of agent files on the system of any user of this plugin.
`~` is the home directory: `%USERPROFILE%` on Windows, `$HOME` on Linux and macOS.
A path without `~` starts at the workspace root.

## Skills

- Personal skills: `~/.copilot/skills/`, `~/.claude/skills/`, and `~/.agents/skills/`
- Workspace skills: `.github/skills/`, `.claude/skills/`, and `.agents/skills/`

## Plugins

- Copilot CLI plugins: `~/.copilot/installed-plugins/<marketplace>/<plugin>/`.
  A plugin installed from a Git URL is under `~/.copilot/installed-plugins/_direct/`.
- Plugins that the workspace turns on or off: `enabledPlugins` in `.github/copilot/settings.json`

## State

- Journal of the reflect skill: `~/.local/state/railing/reflect/journal.jsonl`

Why: an agent that knows these paths opens the file at once. Otherwise it asks the user or guesses.
