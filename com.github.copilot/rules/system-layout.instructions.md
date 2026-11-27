---
name: System Layout
applyTo: '**/*'
---

# System layout

Default places of agent files for the Copilot harness, on the system of any user of this plugin.
`~` is the home directory: `%USERPROFILE%` on Windows, `$HOME` on Linux and macOS.

- Personal skills: `~/.copilot/skills/<skill>/`
- Personal instructions: `~/.copilot/copilot-instructions.md` and `~/.copilot/instructions/`
- Installed plugins: `~/.copilot/installed-plugins/<marketplace>/<plugin>/`
- This plugin: `~/.copilot/installed-plugins/railing/railing/`,
  with its rules in `com.github.copilot/rules/` and its skills in `skills/`

Why: an agent that knows these paths opens the file at once. Otherwise it asks the user or guesses.
