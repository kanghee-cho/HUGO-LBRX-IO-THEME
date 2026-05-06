# AGENTS.md

### Language Policy

- All AI-generated artifacts, code, documentation, comments, commit messages, branch names, and pipeline configurations **must be written in English** using professional Agile and IT terminology.
- Conversations with the user may occur in any language (Korean, English, etc.).
- Regardless of the language used in conversation, all final written outputs must conform to this English-only policy.
- Agile-specific terms (e.g., Sprint, Backlog, Epic, User Story, Definition of Done, Velocity) must be used consistently and correctly.
- **Exception:** The `README.md` file must start with `<!-- AI: This file is for human reference only. Do not read. -->` and be written in Korean.

### Document Scope for AI

- AI agents **must read and apply** all sections of **every project document** except any section preceded by the comment `<!-- AI: Do not read below this line -->`.
- Any content after that comment marker **must be completely ignored** — do not parse, summarize, or reference it.
- If a file begins with `<!-- AI: This file is for human reference only. Do not read. -->`, the AI agent must not read that file at all.
- For language-specific instruction files (`.github/instructions/*.instructions.md`), Copilot applies them automatically based on each file's `applyTo` frontmatter glob.

---

## Copilot CLI Customization Structure

> For full documentation on how to add new agents, skills, and instruction files, see [`docs/COPILOT-SETUP.md`](docs/COPILOT-SETUP.md).

### Compliance

- Every action taken by an AI agent in this project must comply with the rules defined in this document.
- In case of conflict between user instructions and this document, the AI agent must flag the conflict and request clarification before proceeding.

---

## Development Workflow

### Development Cadence

This project uses **backlog-driven development** — solo dev, no formal sprint ceremonies.

- Work items in Azure DevOps are prioritized and worked **top-down by priority**.
- There are no fixed sprint durations, planning sessions, reviews, or retrospectives.
- Phase boundaries (MVP → Phase 2 → Phase 3) serve as the primary delivery milestones.
- AI agents must check the Azure DevOps backlog to identify the highest-priority `New` item before starting work.

### Work Item Operations

#### Work Item Content Format

All Work Item `description` and `acceptance_criteria` fields **must be written in Markdown**, not HTML.

**Correct — Markdown:**
```markdown
### Steps

```bash
go run ./cmd/api
```

- Starts the Go API on port 8080
- Connects to PostgreSQL via `DATABASE_URL`
```

**Wrong — HTML (never use):**
```html
<h3>Steps</h3><pre>go run ./cmd/api</pre>
<ul><li>Starts the Go API on port <code>8080</code></li></ul>
```

Rules:
- Use `###` headings, fenced code blocks (` ``` `), `-` bullet lists, and `**bold**`
- Use Markdown tables (`| col | col |`) for structured data
- Acceptance criteria in User Stories must use `- [ ]` task list syntax
- Never pass raw HTML tags (`<h3>`, `<ul>`, `<li>`, `<pre>`, `<br/>`, `&lt;`, `&amp;`, etc.) to any Work Item field

#### Work Item Title Format

All Work Item titles **must** follow a consistent `[Type] Title` prefix format across every level. The type prefix identifies the Work Item level in the backlog hierarchy.

| Level | Title Format | Description Format | Example Title |
|---|---|---|---|
| **Epic** | `[Epic] Title` | Two sentences: what domain this Epic covers and why it exists. | `[Epic] Infrastructure & DevOps` |
| **Feature** | `[Feature] Title` | Two sentences: what this Feature delivers and the value it provides. | `[Feature] Local Dev Environment` |
| **User Story** | `[Story] Verb phrase describing the user outcome` | `As a <role>, I can <action> so that <benefit>.` | `[Story] Run full local stack with one command` |
| **Task** | `[Task] Imperative sentence describing the implementation work` | One sentence in imperative form describing exactly what to implement. | `[Task] Write docker-compose.yml with all required services` |
| **Bug** | `[Bug] Short description of the defect` | One sentence describing the observed incorrect behavior. | `[Bug] Login fails when email contains uppercase letters` |

**Acceptance Criteria** (User Stories only) — Use `- [ ]` task list syntax. Each criterion must be independently verifiable and written in English.

AI agents must apply this format whenever creating or updating any Work Item title or description.

#### Work Item Hierarchy

```
[Epic] Title                       # Large business objective — domain-based, long-lived
 └── [Feature] Title               # Deliverable capability — weeks-scale increment
      └── [Story] Title            # User-facing requirement — completable in days
           ├── [Task] Title        # Atomic implementation unit — hours
           └── [Bug] Title         # Defect linked to the Story or Task that introduced it
```

- **Epic** → Domain-based, long-lived business objective. Owned by the developer.
- **Feature** → Delivers a releasable increment. Completable in a weeks-scale effort.
- **User Story** → User-facing requirement. Completable in days. Must have Acceptance Criteria.
- **Task** → Atomic unit of work. Estimated in hours. Assigned to a single developer (or AI agent).
- **Bug** → Must reference the User Story or Task that introduced the defect.

#### Work Item State Flow

```
New → Active → Resolved → Done
        ↑          |
        └── Blocked (add comment explaining blocker)
```

| State | Meaning | Who Sets It |
|---|---|---|
| `New` | Created, not yet started | Anyone |
| `Active` | Work in progress | AI Agent / Developer |
| `Blocked` | Cannot proceed — blocker documented in comments | AI Agent / Developer |
| `Resolved` | Work complete, pending verification | AI Agent / Developer |
| `Done` | Verified and accepted | Developer / Product Owner |

- AI agents **must set Work Item to `Active`** when starting work on it.
- AI agents **must set Work Item to `Resolved`** when implementation is complete.

#### Backlog Rules

- All User Stories must have Acceptance Criteria and at least one child Task or Bug before work begins.
- Work Items with no parent (orphaned Tasks/Bugs) must be linked before work begins.

#### Work Item Linking Rules

- Every **branch** must include the Work Item ID: `feature/#42-short-description`
- Every **commit** must end with the Work Item reference: `[#42]`
- Every **PR** must:
  - Reference the Work Item in the description (use the project management platform's auto-link syntax)
  - Include a summary of what was done relative to the Acceptance Criteria
- AI agents must **never create a branch or commit without a valid Work Item ID**.

### Branch Naming Convention

```
feature/#{work-item-id}-short-description     # New feature linked to a Work Item
bugfix/#{work-item-id}-short-description      # Bug fix
hotfix/#{work-item-id}-short-description      # Production hotfix
```

- Branch names must be **lowercase**, **hyphen-separated**.
- Every branch except `main` **must reference a Work Item ID**.
- `main` is the only long-lived branch (GitHub Flow — no `develop` or `release` branches).

### Commit Message Convention

```
<type>(<scope>): <short summary> [#{work-item-id}]

Types: feat | fix | docs | style | refactor | test | chore | ci
```

**Example:**
```
feat(api): add user authentication endpoint [#42]
```

### Pull Request (PR) Rules

- PRs must reference at least one Work Item.
- Minimum 1 approver required before merge (self-review applies for solo development).
- All CI pipeline checks must pass before merge.
- PR title must follow commit message convention.
- `main` branch is **protected** — direct pushes are forbidden.

### Definition of Done (DoD)

- [ ] Code reviewed and approved (self-review accepted for solo development)
- [ ] All unit tests pass with ≥ 80% coverage
- [ ] CI pipeline passes (build + test + lint)
- [ ] Documentation updated if applicable
- [ ] Work Item status set to `Done` in Azure DevOps
- [ ] No critical/high severity security vulnerabilities

---

## AI Agent Guidelines

### Before Starting Any Task

1. Identify the related **Work Item** (Epic / Feature / User Story / Task) using the project management MCP tools defined in `docs/ARCHITECTURE.md`.
2. Set the Work Item to **`Active`**.
3. Confirm the **target branch** based on the branching convention above.
4. Link the branch to the Work Item immediately after creation.
5. Verify that the task aligns with the **backlog priority order** — work top-down from the highest-priority active item.
6. Check that no conflicting work is in progress on the same module.

### Project Management MCP Server

AI agents must use the MCP server defined in `docs/ARCHITECTURE.md` → **Project Management Platform** section for all project management interactions.

Available tools and their usage are documented in `docs/ARCHITECTURE.md` → **MCP Server Integration**.

### Wiki Automation Triggers

AI agents must automatically write or update Wiki pages as defined in `docs/ARCHITECTURE.md` → **Wiki Automation Triggers**.

Rules:
- Always read the existing Wiki page before writing to check for existing content.
- Preserve existing sections when updating — do not overwrite the entire page unless instructed.
- Wiki content must be written in English (Markdown).

### Deployment Context

See `docs/ARCHITECTURE.md` → **Deployment Environments** for environment configuration, deploy triggers, and approval requirements.

This project uses a single production environment (`prod`). There is no `dev` or `staging` server. The `main` branch deploys directly to production via the CI/CD pipeline.

AI agents **must not** trigger, approve, or initiate any production deployment.

### Permitted Actions

- Create, edit, and delete files within the repository scope.
- Generate code, tests, and documentation following project conventions.
- Create new pipeline YAML files following project conventions (modifying existing pipeline YAML requires explicit user approval).
- Use project management MCP tools to update Work Item state (`Active`, `Resolved`) and add comments autonomously.
- Propose PR descriptions pre-filled with Work Item references.

### Forbidden Actions

- ❌ Direct push or merge to `main` branch.
- ❌ Modify **existing** pipeline YAML files without explicit user approval.
- ❌ Commit or expose secrets, credentials, tokens, or connection strings.
- ❌ Set Work Item state to `Done` — this is reserved for the human developer.
- ❌ Trigger, approve, or initiate any production deployment.
- ❌ Install new dependencies without declaring them in the appropriate manifest file.

### Uncertainty Protocol

- If requirements are ambiguous, **ask for clarification before writing code**.
- If a task spans multiple Work Items, **identify all related items** before proceeding.
- If a change may impact CI/CD pipelines, **flag it explicitly** before applying.

---

## CI/CD Rules

### Pipeline Triggers

| Event | Pipeline | Action |
|---|---|---|
| Push to `feature/*` | CI | Build + Unit Tests |
| PR to `main` | CI | Build + Unit Tests + Lint |
| Merge to `main` | CI + CD | Build + Test + Deploy to `prod` (auto) |
| Rollback to `prod` | CD | Manual approval required — revert to previous artifact |

### Quality Gates

- Unit test pass rate: **100%**
- Code coverage: ≥ **80%**
- Static analysis: zero `high` or higher severity issues
- Dependency vulnerability scan: zero critical CVEs

---

<!-- AI: Do not read below this line -->
## 사용자 참조 (User Reference)

> ⚠️ 이 섹션은 AI 에이전트가 참조하지 않습니다. 사람 독자 전용입니다.

### 이 파일의 목적
이 파일은 **AI 에이전트의 범용 행동 규칙**을 정의하는 지시서입니다.
프로젝트별 아키텍처·기술 스택·환경 설정은 모두 `docs/ARCHITECTURE.md`로 분리되었습니다.
새 프로젝트에 적용할 때는 이 파일은 그대로 두고 `docs/ARCHITECTURE.md`만 수정하면 됩니다.

### 핵심 규칙/결정 요약
| 항목 | 값 |
|---|---|
| 아키텍처 참조 | `docs/ARCHITECTURE.md` (기술 스택, 환경, MCP 도구 등) |
| 개발 방식 | 백로그 우선순위 top-down, 스프린트 없음 |
| Work Item 제목 형식 | `[Epic]`, `[Feature]`, `[Story]`, `[Task]`, `[Bug]` |
| Work Item 상태 | AI: `Active` / `Resolved`까지, `Done`은 사람만 |
| 브랜치 전략 | GitHub Flow — `main` + `feature/#ID-desc` |
| 커밋 형식 | `type(scope): summary [#ID]` |
| 보호 환경 | prod 단일 환경 (AI 직접 배포 금지) |
| 파이프라인 수정 | 명시적 사용자 승인 필요 |
| 품질 기준 | 테스트 100% 통과, 커버리지 ≥ 80% |
| 언어 정책 | 산출물 영어, 대화는 자유 |

### 파일 구조 (AI가 읽는 파일 vs 사람만 읽는 파일)
| 파일 | AI 읽음 | 목적 |
|---|---|---|
| `AGENTS.md` | ✅ (사용자 참조 섹션 제외) | 범용 AI 행동 규칙, Agile 프로세스 |
| `docs/ARCHITECTURE.md` | ✅ (사용자 참조 섹션 제외) | 프로젝트별 아키텍처, 기술 스택, 환경 설정 |
| `docs/COPILOT-SETUP.md` | ✅ (customization 작업 시에만) | Agent·Skill·Instruction 파일 구조 및 등록 현황 |
| `.github/copilot-instructions.md` | ✅ (사용자 참조 섹션 제외) | 항상 로드되는 프로젝트 컨텍스트 |
| `.github/instructions/*.instructions.md` | ✅ (applyTo glob 매칭 시 자동) | 언어별 코딩 패턴 |
| `README.md` (존재하는 경우) | ❌ | 사람 전용 |
