---
applyTo: "__disabled__"
---

# TypeScript Coding Conventions

## Naming
- Variables and functions: `camelCase`
- Types, interfaces, classes, enums: `PascalCase`
- Constants: `SCREAMING_SNAKE_CASE`
- Files: `kebab-case.ts`

## Types
- Prefer `interface` over `type` for object shapes
- Avoid `any` — use `unknown` when the type is truly unknown
- Use strict null checks — never suppress with `!`
- Export types explicitly: `export type { UserDto }`

## Code Style
- Prefer `const` over `let`; never use `var`
- Use `async/await` over raw Promises
- Avoid barrel re-exports (`index.ts`) in large modules — they cause circular dependency issues
- Keep functions pure where possible; isolate side effects

## React (if applicable)
- Functional components only — no class components
- Props interface named `{ComponentName}Props`
- Co-locate component, styles, and tests in the same directory

---

<!-- AI: Do not read below this line -->
## 사용자 참조 (User Reference)

> ⚠️ 이 섹션은 AI 에이전트가 참조하지 않습니다. 사람 독자 전용입니다.

### 이 파일의 목적
TypeScript 파일(`**/*.ts`, `**/*.tsx`)에 적용되는 코딩 컨벤션 instruction 파일입니다.
현재 `applyTo: "__disabled__"` 상태이며, 활성화 시 glob을 변경하세요.

### 핵심 내용 요약
| 항목 | 값 |
|---|---|
| 적용 대상 (활성화 시) | `**/*.ts, **/*.tsx` |
| 현재 상태 | disabled |
| 활성화 방법 | `applyTo: "**/*.ts"` 로 변경 후 COPILOT-SETUP.md 상태 업데이트 |
