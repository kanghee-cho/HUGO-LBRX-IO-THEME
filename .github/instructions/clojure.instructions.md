---
applyTo: "__disabled__"
---

# Clojure Coding Conventions

## Naming
- Functions and variables: `kebab-case`
- Predicates: suffix with `?` (e.g., `valid?`, `empty?`)
- Mutating functions: suffix with `!` (e.g., `reset!`, `swap!`)
- Namespaces: `kebab-case`, mirroring the file path (`my-app.core`)
- Constants: `*earmuffs*` for dynamic vars; plain `kebab-case` for true constants

## Code Style
- Prefer pure functions — isolate side effects at the edges
- Use `let` bindings to name intermediate values for readability
- Prefer `->` and `->>` threading macros over deeply nested calls
- Keep namespaces focused — one primary responsibility per namespace
- Destructure maps and sequences in function parameters where it aids clarity

## Data
- Prefer plain maps and vectors over custom types
- Use `spec` or `malli` for data validation at system boundaries
- Avoid mutable state — use `atom` only when truly necessary

## Error Handling
- Use `ex-info` for structured exceptions: `(throw (ex-info "msg" {:context data}))`
- Catch with `ex-data` to extract structured context

## Project Structure
- Use `deps.edn` (tools.deps) for dependency management
- Source: `src/`, Tests: `test/`, Resources: `resources/`

---

<!-- AI: Do not read below this line -->
## 사용자 참조 (User Reference)

> ⚠️ 이 섹션은 AI 에이전트가 참조하지 않습니다. 사람 독자 전용입니다.

### 이 파일의 목적
Clojure 파일(`**/*.clj`, `**/*.cljs`, `**/*.cljc`)에 적용되는 코딩 컨벤션 instruction 파일입니다.
현재 `applyTo: "__disabled__"` 상태이며, 활성화 시 glob을 변경하세요.

### 핵심 내용 요약
| 항목 | 값 |
|---|---|
| 적용 대상 (활성화 시) | `**/*.clj, **/*.cljs, **/*.cljc` |
| 현재 상태 | disabled |
| 활성화 방법 | `applyTo: "**/*.clj"` 로 변경 후 COPILOT-SETUP.md 상태 업데이트 |
