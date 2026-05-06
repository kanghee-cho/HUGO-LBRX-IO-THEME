---
applyTo: "__disabled__"
---

# Shell Script Coding Conventions

## Header
- Always start with a shebang: `#!/usr/bin/env bash`
- Set strict mode at the top of every script:
  ```bash
  set -euo pipefail
  ```

## Naming
- Functions and variables: `snake_case`
- Constants and environment variables: `SCREAMING_SNAKE_CASE`
- Script files: `kebab-case.sh`

## Code Style
- Quote all variable expansions: `"${VAR}"` not `$VAR`
- Use `$(command)` substitution — never backticks
- Prefer `[[ ]]` over `[ ]` for conditionals in Bash
- Keep functions small — one responsibility per function
- Add a usage/help function for any script with parameters

## Error Handling
- Always check exit codes for critical commands
- Use `trap 'cleanup' EXIT` for resource cleanup
- Print errors to stderr: `echo "Error: ..." >&2`

## Security
- Never use `eval` with untrusted input
- Validate all external inputs before use

---

<!-- AI: Do not read below this line -->
## 사용자 참조 (User Reference)

> ⚠️ 이 섹션은 AI 에이전트가 참조하지 않습니다. 사람 독자 전용입니다.

### 이 파일의 목적
Shell 스크립트 파일(`**/*.sh`)에 적용되는 코딩 컨벤션 instruction 파일입니다.
현재 `applyTo: "__disabled__"` 상태이며, 활성화 시 glob을 변경하세요.

### 핵심 내용 요약
| 항목 | 값 |
|---|---|
| 적용 대상 (활성화 시) | `**/*.sh` |
| 현재 상태 | disabled |
| 활성화 방법 | `applyTo: "**/*.sh"` 로 변경 후 COPILOT-SETUP.md 상태 업데이트 |
