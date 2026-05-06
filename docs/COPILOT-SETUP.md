# Copilot CLI Setup Guide

> This file documents the official Copilot CLI customization structure for the KHCHO-LBRX-IO project.
> It is a **developer reference** for adding new agents, skills, and instruction files.
> AI agents must reference this file when creating or managing customization files. It is not required for routine coding tasks.

---

## Official Directory Map

```
.github/
  copilot-instructions.md          # Repo-wide custom instructions (always loaded)
  instructions/
    *.instructions.md              # Path-specific instructions (loaded by applyTo glob)
  agents/
    *.agent.md                     # Custom agent profiles (persona + tools + auto-delegation)
  skills/
    {skill-name}/
      SKILL.md                     # Skill definition (just-in-time, on-demand)
      [optional scripts/resources]

AGENTS.md                          # AI agent behavior rules (always loaded — git root)
```

---

## When to Use Each Feature

| Feature | Location | Format | When to Use |
|---|---|---|---|
| **Repo-wide instructions** | `.github/copilot-instructions.md` | Markdown | Standards that apply to every task (coding conventions, project-wide rules) |
| **Path instructions** | `.github/instructions/*.instructions.md` | `applyTo` frontmatter + Markdown | Rules for specific file types or directories (language patterns, domain rules) |
| **Custom agents** | `.github/agents/*.agent.md` | YAML frontmatter + Markdown | Specialist persona with specific tools and expertise; supports auto-delegation |
| **Skills** | `.github/skills/{name}/SKILL.md` | `name`/`description` frontmatter + Markdown | Just-in-time repeatable workflows; loaded only when Copilot deems relevant or manually invoked |

---

## File Format Requirements

### Custom Agent (`.github/agents/*.agent.md`)

```markdown
---
description: What this agent does and when to use it
tools:
  - view
  - edit
  - create
infer: true   # true = Copilot auto-delegates when relevant
---
Agent instructions body...
```

### Skill (`.github/skills/{name}/SKILL.md`)

```markdown
---
name: skill-name            # Must match the directory name, lowercase with hyphens
description: What it does and when Copilot should use it
allowed-tools: shell        # Optional: pre-approve specific tools
---
Skill instructions body...
```

### Path Instruction (`.github/instructions/*.instructions.md`)

```markdown
---
applyTo: "path/glob/**/*.ext"   # Files this instruction applies to
---
Instruction body...
```

---

## Rules for Adding New Customizations

- **Never place agent definitions in `.github/instructions/`** — agents belong in `.github/agents/`.
- **Never place skill files directly in `.github/instructions/`** — skills belong in `.github/skills/{name}/SKILL.md`.
- **Skill file must be named `SKILL.md`** — other names are not recognized by Copilot CLI.
- **Agent file must use `.agent.md` extension** — other extensions are not recognized.
- When adding a new specialist workflow, create both a **skill** (implementation) and an **agent** (persona + delegation) if the workflow warrants auto-delegation.
- Use the `applyTo` glob to enable or disable an instruction file — set it to `__disabled__` to deactivate.
- The **Status** column below is the single source of truth for what is currently active.

---

## Currently Active Customizations

| Type | File | Applied To | Status |
|---|---|---|---|
| Instruction | `go.instructions.md` | `**/*.go` | disabled |
| Instruction | `typescript.instructions.md` | `**/*.ts, **/*.tsx` | disabled |
| Instruction | `csharp.instructions.md` | `**/*.cs` | disabled |
| Instruction | `powershell.instructions.md` | `**/*.ps1` | disabled |
| Instruction | `shellscript.instructions.md` | `**/*.sh` | disabled |
| Instruction | `python.instructions.md` | `**/*.py` | disabled |
| Instruction | `clojure.instructions.md` | `**/*.clj, **/*.cljs, **/*.cljc` | disabled |
| Agent | `questionnaire-designer.agent.md` | On-demand | disabled |
| Skill | `questionnaire-designer/SKILL.md` | On-demand | disabled |

