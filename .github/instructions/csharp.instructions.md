---
applyTo: "__disabled__"
---

# C# Coding Conventions

## Naming
- Classes, methods, properties: `PascalCase`
- Local variables, parameters: `camelCase`
- Private fields: `_camelCase` (underscore prefix)
- Interfaces: `IPrefix` (e.g., `IUserRepository`)
- Constants: `PascalCase`

## Code Style
- Use `var` only when the type is obvious from the right-hand side
- Prefer expression-bodied members for simple one-liners
- Use `record` types for immutable data transfer objects
- Prefer `IEnumerable<T>` over concrete collection types in method signatures

## Error Handling
- Use exceptions for truly exceptional conditions only
- Prefer `Result<T>` pattern for expected failure cases
- Always use `using` statements or `await using` for disposable resources

## Async
- All async methods must be suffixed with `Async`
- Always `await` — never `.Result` or `.Wait()` (deadlock risk)
- Pass `CancellationToken` through the call chain

## Project Structure
- Follow Clean Architecture: `Domain`, `Application`, `Infrastructure`, `API`
- Keep controllers thin — delegate to services/handlers

---

<!-- AI: Do not read below this line -->
## 사용자 참조 (User Reference)

> ⚠️ 이 섹션은 AI 에이전트가 참조하지 않습니다. 사람 독자 전용입니다.

### 이 파일의 목적
C# 파일(`**/*.cs`)에 적용되는 코딩 컨벤션 instruction 파일입니다.
현재 `applyTo: "__disabled__"` 상태이며, 활성화 시 glob을 변경하세요.

### 핵심 내용 요약
| 항목 | 값 |
|---|---|
| 적용 대상 (활성화 시) | `**/*.cs` |
| 현재 상태 | disabled |
| 활성화 방법 | `applyTo: "**/*.cs"` 로 변경 후 COPILOT-SETUP.md 상태 업데이트 |
