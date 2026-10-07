---
name: debug-context-artifacts
description: >-
  Manual-only debug command. Do NOT trigger this automatically - only invoke
  it when the user explicitly runs it by name. It snapshots the AI context
  init state (instructions, commands, skills, MCP servers, and tools loaded
  into the session before the user typed anything) for debugging purposes.
user-invocable: true
---

# Debug: AI Context Artifacts - Init State Snapshot

**STRICT RULE: Do NOT read files, search the codebase, call tools, or fetch any external data.
Report ONLY what is already present in your current context right now.**

Produce a structured snapshot of every AI artifact visible in your context at this moment.
The goal is to understand the **init state** of this chat session - what was loaded automatically
before the user typed anything.

---

## Output Format

Print the following tables. If a category has no entries, still print the table header with
a single row saying `- none detected -`.

---

### Instructions & Rules

Artifacts that shape behavior globally or for specific file patterns
(system prompts, CLAUDE.md, .cursorrules, custom instructions, etc.).

| # | Name / File | Path | Location | Scope / applyTo | Content in Context? |
|---|-------------|------|----------|-----------------|---------------------|
| 1 | …           | …    | …        | …               | full / reference    |

**Columns:**

- Name / File - display name or filename
- Path - exact path as you know it (repo-relative or absolute); `injected` if embedded in system prompt with no file path
- Location - see *Path Location Taxonomy* in Notes
- Scope / applyTo - glob pattern, directory, or `global`
- Content in Context? - `full` (text is in your context window) · `reference` (only path/name mentioned)

---

### Commands & Prompts

User-invocable prompt templates (`.prompt.md`, slash commands
that are simple prompt expansions without conditional activation logic).

| # | Name / File | Path | Location | Invocation | Content in Context? |
|---|-------------|------|----------|------------|---------------------|

**Columns:**

- Location - see *Path Location Taxonomy* in Notes
- Invocation - slash command name or attachment method
- Content in Context? - `full` (text is in your context window) ·
  `reference` (only path/name mentioned)

---

### Skills

Conditionally activated knowledge bundles - domain-specific behaviors
that can trigger automatically (by file type, import, keyword, context)
or be invoked explicitly. Distinguished from Commands by having
activation logic and/or persistent behavioral modifications.

| # | Skill Name | Path | Location | Activation Trigger | Active Now? | Content in Context? |
|---|------------|------|----------|--------------------|-------------|---------------------|

**Columns:**

- Location - see *Path Location Taxonomy* in Notes

**Activation Trigger** - keyword / model-detected relevance/ file-pattern / manual-only / always-on
**Active Now?** - yes (content loaded and influencing behavior) / no (available but dormant) / n/a (environment has no concept of passive activation) / unknown
**Content in Context?** - full / reference / not loaded

---

### MCP Servers & Extensions

External tool integrations - MCP servers, IDE extensions exposing tools, etc.

| # | Server / Extension Name | Config Path | Location | Tools Exposed | Status |
|---|-------------------------|-------------|----------|---------------|--------|

**Columns:**

- Location - see *Path Location Taxonomy* in Notes
- Tools Exposed - list of tool names visible to you right now (truncate to first 5 + count if many)
- Status - `connected` · `listed-only` · `unknown`

---

### Tools & Capabilities

All tools available in this session - native, deferred, and MCP-provided.

| # | Tool Name | Source | Category | Availability |
|---|-----------|--------|----------|--------------|

**Columns:**

- Source - `built-in` · `deferred` · `mcp:<server-name>` · `extension:<name>`
- Category - `file` · `terminal` · `search` · `web` · `browser` · `planning` · `memory` · `scheduling` · `ide` · `other`
- Availability - `immediate` (callable right now) · `deferred` (requires fetch/activation first) · `unknown`

---

### Persistent State & Memory

File-based memory, conversation history, cached context, or any persistent
state loaded into this session automatically.

| # | Item | Path / Location | Location | Type | Content in Context? |
|---|------|-----------------|----------|------|---------------------|

**Columns:**

- Location - see *Path Location Taxonomy* in Notes
- Type - `memory-index` · `memory-file` · `conversation-cache` · `settings` · `other`
- Content in Context? - `full` · `reference` · `not loaded`

---

### IDE & Workspace Context (if applicable)

Open files, active editor selection, terminal output, problems panel,
git state, environment metadata, etc.
*Skip this table entirely if your environment is not an IDE.*

| # | Context Item | Value / Path | Injected As |
|---|--------------|--------------|-------------|

**Columns:**

- Injected As - `full-content` · `path-reference` · `metadata`

---

### Workspace Task Definitions (if applicable)

Tasks, run configurations, or build targets injected from workspace config
(e.g. `tasks.json`, `launch.json`, `Makefile`).
*Skip this table entirely if no task definitions are detected.*

| # | Task Name | Source File | Type / Group | Content in Context? |
|---|-----------|-------------|--------------|---------------------|

**Columns:**

- Source File - config file path
- Type / Group - `build` · `test` · `run` · `lint` · `deploy` · `other`
- Content in Context? - `full` · `reference`

---

### Environment & Isolation

Runtime environment details: platform, shell, working directory,
isolation model (worktrees, sandboxes, containers), permission mode.

| # | Property          | Value                                                 |
|---|-------------------|-------------------------------------------------------|
| 1 | Platform          | ...                                                   |
| 2 | Shell             | ...                                                   |
| 3 | Working Directory | ...                                                   |
| 4 | Isolation Model   | ... (e.g. `git worktree`, `container`, `none`)        |
| 5 | Permission Mode   | ... (e.g. `auto-allow`, `prompt-per-tool`, `unknown`) |
| 6 | Git Branch        | ...                                                   |
| 7 | Git Status        | ...                                                   |

---

## Notes

- If you cannot determine a field with certainty, write `unknown` - do not guess.
- If a file path was mentioned anywhere in your context (system prompt, prior message,
  tool result), include it. If you know only the name but not the path, write `path unknown`.
- "Content in Context?" answers whether the **text body** of the artifact is in your
  context window right now, versus only its name or path being referenced.
- `IDE & Workspace Context` and `Workspace Task Definitions` are IDE-specific -
  omit them cleanly if not applicable,
  do not force-fill with unrelated data.
- For `Tools & Capabilities`, if there are more than ~30 tools, group MCP tools
  by server and list counts instead of individual rows.

### Path Location Taxonomy

Used in the **Location** column of any table with a file path. Pick the *most specific* matching value:

| Value        | Meaning                                                   | Typical paths                                          |
|--------------|-----------------------------------------------------------|--------------------------------------------------------|
| `repo`       | Inside the current git workspace / project                | `./`, relative paths inside workspace                  |
| `user`       | User home dir - personal config & dotfiles                | `~`, `%USERPROFILE%`, `AppData/Roaming` (user-level)   |
| `ide-ext`    | IDE extension installation directory                      | VS Code `extensions/`, Cursor extensions               |
| `ide-config` | IDE user-level config / settings (non-extension)          | `Code/User/`, `.cursor/`, `.vscode/` outside repo      |
| `agent`      | AI framework's own runtime storage                        | `/memories/`, session cache, Copilot workspace storage |
| `system`     | System-wide / global install paths                        | `/usr/`, `/etc/`, `Program Files/`                     |
| `injected`   | No real file - content embedded directly in system prompt | n/a                                                    |
