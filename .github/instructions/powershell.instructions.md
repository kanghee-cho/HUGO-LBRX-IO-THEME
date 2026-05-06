---
applyTo: "__disabled__"
---

# PowerShell Coding Conventions

## Naming
- Functions: `Verb-Noun` using approved PowerShell verbs (`Get-`, `Set-`, `New-`, `Remove-`)
- Variables: `$PascalCase` for script-scope, `$camelCase` for local
- Parameters: `PascalCase`

## Code Style
- Always use `[CmdletBinding()]` on advanced functions
- Declare parameter types explicitly: `[string]$Name`, `[int]$Count`
- Use `Write-Verbose` for diagnostic output — never `Write-Host` in scripts meant for pipelines
- Prefer pipeline-friendly output — emit objects, not formatted strings

## Error Handling
- Set `$ErrorActionPreference = 'Stop'` at script top for fail-fast behavior
- Use `try/catch/finally` blocks around external calls
- Always test with `-WhatIf` support where destructive actions are involved

## Security
- Never hardcode credentials — use `SecureString` or environment variables
- Validate and sanitize all external inputs

---

<!-- AI: Do not read below this line -->
## 사용자 참조 (User Reference)

> ⚠️ 이 섹션은 AI 에이전트가 참조하지 않습니다. 사람 독자 전용입니다.

### 이 파일의 목적
PowerShell 스크립트 파일(`**/*.ps1`)에 적용되는 코딩 컨벤션 instruction 파일입니다.
현재 `applyTo: "__disabled__"` 상태이며, 활성화 시 glob을 변경하세요.

### 핵심 내용 요약
| 항목 | 값 |
|---|---|
| 적용 대상 (활성화 시) | `**/*.ps1` |
| 현재 상태 | disabled |
| 활성화 방법 | `applyTo: "**/*.ps1"` 로 변경 후 COPILOT-SETUP.md 상태 업데이트 |
