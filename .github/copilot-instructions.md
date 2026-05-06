# GitHub Copilot Instructions

> This file provides always-on project context for GitHub Copilot (and other AI coding assistants).
>
> - **Project architecture, API design, tech stack, DB conventions** → [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md)
> - **Agile process, Work Item rules, CI/CD, AI behavior rules** → [`AGENTS.md`](../AGENTS.md)
> - **Language-specific coding patterns** → [`docs/COPILOT-SETUP.md`](../docs/COPILOT-SETUP.md) → Currently Active Customizations

---

## Language-Specific Instruction Files

> Instruction files in `.github/instructions/` are applied automatically by Copilot when
> the file being edited matches the `applyTo` glob in each file's frontmatter.
> To stop a file from applying, change its `applyTo` to a non-matching pattern (e.g. `__disabled__`).

