---
applyTo: "__disabled__"
---

# Go Coding Conventions

## Naming
- Packages: lowercase, single word (`userservice`, not `user_service`)
- Exported: `PascalCase` — unexported: `camelCase`
- Interfaces: noun or `-er` suffix (`Reader`, `UserStore`)
- Error variables: `ErrNotFound`, `ErrInvalidInput`

## Error Handling
- Always handle errors explicitly — never use `_` for error returns
- Wrap errors with context: `fmt.Errorf("creating user: %w", err)`
- Define sentinel errors as package-level `var Err... = errors.New(...)`

## Code Style
- Keep functions small and focused — one responsibility per function
- Prefer table-driven tests using `t.Run`
- Use `context.Context` as the first parameter for any I/O or long-running operation
- Avoid `init()` unless absolutely necessary

## Project Layout
- Follow standard Go project layout: `cmd/`, `internal/`, `pkg/`
- Place domain types in `internal/domain/`
- Keep `main.go` minimal — wire dependencies, start server

---

<!-- AI: Do not read below this line -->
## 사용자 참조 (User Reference)

> ⚠️ 이 섹션은 AI 에이전트가 참조하지 않습니다. 사람 독자 전용입니다.

### 이 파일의 목적
Go 언어 파일(`**/*.go`)에 적용되는 코딩 컨벤션 instruction 파일입니다.
현재 `applyTo: "__disabled__"` 상태이며, 활성화 시 `**/*.go`로 변경하세요.

### 핵심 내용 요약
| 항목 | 값 |
|---|---|
| 적용 대상 (활성화 시) | `**/*.go` |
| 현재 상태 | disabled |
| 활성화 방법 | `applyTo: "**/*.go"` 로 변경 후 COPILOT-SETUP.md 상태 업데이트 |
