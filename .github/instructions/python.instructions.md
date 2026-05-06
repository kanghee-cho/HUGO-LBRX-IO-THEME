---
applyTo: "__disabled__"
---

# Python Coding Conventions

## Naming
- Modules, functions, variables: `snake_case`
- Classes: `PascalCase`
- Constants: `SCREAMING_SNAKE_CASE`
- Private members: `_single_leading_underscore`

## Type Annotations
- All function signatures must include type hints
- Use `from __future__ import annotations` for forward references
- Prefer `X | None` over `Optional[X]` (Python 3.10+)
- Use `TypeAlias` for complex type definitions

## Code Style
- Follow PEP 8 — line length ≤ 88 characters (Black formatter)
- Prefer dataclasses or Pydantic models over plain dicts for structured data
- Use f-strings for string formatting — never `%` or `.format()`
- Keep imports ordered: stdlib → third-party → local (isort)

## Error Handling
- Define custom exceptions in a dedicated `exceptions.py` module
- Use specific exception types — never bare `except:`
- Use context managers (`with`) for resource management

## Project Structure
- Use `src/` layout: `src/{package}/`
- Keep `__init__.py` files minimal
- Place configuration in `pyproject.toml`

---

<!-- AI: Do not read below this line -->
## 사용자 참조 (User Reference)

> ⚠️ 이 섹션은 AI 에이전트가 참조하지 않습니다. 사람 독자 전용입니다.

### 이 파일의 목적
Python 파일(`**/*.py`)에 적용되는 코딩 컨벤션 instruction 파일입니다.
현재 `applyTo: "__disabled__"` 상태이며, 활성화 시 glob을 변경하세요.

### 핵심 내용 요약
| 항목 | 값 |
|---|---|
| 적용 대상 (활성화 시) | `**/*.py` |
| 현재 상태 | disabled |
| 활성화 방법 | `applyTo: "**/*.py"` 로 변경 후 COPILOT-SETUP.md 상태 업데이트 |
