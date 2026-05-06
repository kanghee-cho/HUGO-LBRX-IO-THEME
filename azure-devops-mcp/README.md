<!-- AI: This file is for human reference only. Do not read. -->

# azure-devops-mcp

Azure DevOps MCP 서버 — AI 클라이언트(Claude, Copilot 등)가 Azure DevOps의 Wiki, Work Items, Dashboard를 직접 읽고 쓸 수 있도록 연결합니다.

## 기능

| 영역 | 기능 |
|---|---|
| **Wiki** | 페이지 읽기 · 목록 조회 · 생성 · 수정 |
| **Work Items** | Epic / Feature / User Story / Task / Bug 조회 · 생성 · 수정 · 댓글 · 스프린트 이동 |
| **Dashboard** | 대시보드 목록 · 상세 조회 · 쿼리 위젯 추가 |
| **Resources** | `workitem://`, `sprint://current` — AI 컨텍스트 자동 로딩 |
| **Prompts** | Sprint Planning · Sprint Review · Epic → Wiki 자동 생성 |

## 사전 요구사항

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 패키지 매니저
- Azure DevOps Personal Access Token (PAT)
  - 필요 권한: **Work Items** (Read & Write), **Wiki** (Read & Write), **Dashboard** (Read & Manage)

## 설치

```bash
git clone <repo-url>
cd azure-devops-mcp
uv sync
```

## 설정

`.env.example`을 복사하여 `.env`를 만들고 값을 채웁니다.

```bash
cp .env.example .env
```

```bash
# .env
AZURE_DEVOPS_ORG_URL=https://dev.azure.com/your-org   # 조직 URL
AZURE_DEVOPS_PROJECT=your-project                      # 프로젝트 이름
AZURE_DEVOPS_PAT=your-personal-access-token            # PAT (절대 커밋하지 마세요)
AZURE_DEVOPS_WIKI_ID=your-project.wiki                 # Wiki ID (보통 {project}.wiki)
LOG_LEVEL=INFO
REQUEST_TIMEOUT=30
```

> **Wiki ID 확인 방법**: Azure DevOps → Project Settings → Wiki → URL에서 `wikiIdentifier` 값

## 실행

### stdio 모드 (Claude Desktop / Claude Code)

```bash
uv run python main.py
```

### HTTP 모드 (원격 배포)

```bash
uv run python main.py --http
```

## AI 클라이언트 등록

### Claude Code

```bash
claude mcp add azure-devops-mcp -- uv run python main.py
```

또는 프로젝트 루트의 `.claude/mcp.json`에 직접 추가:

```json
{
  "mcpServers": {
    "azure-devops-mcp": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/azure-devops-mcp"
    }
  }
}
```

### Claude Desktop

`claude_desktop_config.json`에 추가:

```json
{
  "mcpServers": {
    "azure-devops-mcp": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/azure-devops-mcp",
      "env": {
        "AZURE_DEVOPS_ORG_URL": "https://dev.azure.com/your-org",
        "AZURE_DEVOPS_PROJECT": "your-project",
        "AZURE_DEVOPS_PAT": "your-pat",
        "AZURE_DEVOPS_WIKI_ID": "your-project.wiki"
      }
    }
  }
}
```

### GitHub Copilot (VS Code)

워크스페이스 루트의 `.vscode/mcp.json`에 추가:

```json
{
  "servers": {
    "azure-devops-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/absolute/path/to/azure-devops-mcp"
    }
  }
}
```

> VS Code가 파일을 자동 감지하여 활성화 프롬프트를 표시합니다. Claude와 달리 키 이름이 `"servers"`이고 `"type": "stdio"` 필드가 필수입니다.

### Gemini CLI

`~/.gemini/settings.json`에 추가:

```json
{
  "mcpServers": {
    "azure-devops-mcp": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/absolute/path/to/azure-devops-mcp",
      "env": {
        "AZURE_DEVOPS_ORG_URL": "https://dev.azure.com/your-org",
        "AZURE_DEVOPS_PROJECT": "your-project",
        "AZURE_DEVOPS_PAT": "your-pat",
        "AZURE_DEVOPS_WIKI_ID": "your-project.wiki"
      }
    }
  }
}
```

> `.env` 파일을 사용하는 경우 `"env"` 블록은 생략 가능합니다.

## 도구 목록

### Wiki

| 도구 | 설명 |
|---|---|
| `read_wiki_page` | 페이지 내용 읽기 |
| `list_wiki_pages` | 경로 아래 페이지 목록 조회 |
| `create_wiki_page` | 새 페이지 생성 |
| `update_wiki_page` | 기존 페이지 수정 |

### Work Items

| 도구 | 설명 |
|---|---|
| `get_work_item` | 단일 Work Item 전체 필드 조회 |
| `list_work_items` | WIQL 기반 필터 조회 (타입, 상태, 스프린트, 담당자) |
| `get_work_item_children` | 직속 자식 Work Item 목록 조회 |
| `create_work_item` | Epic / Feature / User Story / Task / Bug 생성 |
| `update_work_item` | 필드 수정 (상태, 스토리 포인트, 스프린트 등) |
| `add_work_item_comment` | 댓글 추가 |
| `move_work_item_to_sprint` | 스프린트 이동 |

### Dashboard

| 도구 | 설명 |
|---|---|
| `list_dashboards` | 프로젝트 대시보드 목록 |
| `get_dashboard` | 대시보드 상세 및 위젯 목록 |
| `add_query_widget` | 저장된 쿼리 결과 위젯 추가 |

## 리소스

| URI | 내용 |
|---|---|
| `wiki://{page_path}` | Wiki 페이지 내용을 AI 컨텍스트로 로딩 |
| `workitem://{id}` | Work Item 전체 필드를 AI 컨텍스트로 로딩 |
| `sprint://current` | 현재 스프린트 메타데이터 로딩 |

## 프롬프트

| 프롬프트 | 설명 |
|---|---|
| `sprint_planning` | 스프린트 계획 수립 워크플로 실행 |
| `sprint_review` | 스프린트 리뷰 작성 및 Wiki 저장 |
| `generate_wiki_from_epic` | Epic 계층 구조를 Wiki 문서로 자동 생성 |

## 개발

### 테스트 실행

```bash
uv run pytest
```

### 서버 초기화 확인

```bash
uv run python -c "from server import mcp; print('OK')"
```

### 프로젝트 구조

```
azure-devops-mcp/
├── main.py           # 진입점 (transport 선택)
├── server.py         # FastMCP 인스턴스 및 모듈 등록
├── config.py         # 환경변수 설정 (pydantic-settings)
├── exceptions.py     # 커스텀 예외
├── tools/            # AI가 호출하는 도구 함수
├── resources/        # AI 컨텍스트로 로딩되는 리소스
├── prompts/          # 표준화된 AI 워크플로 프롬프트
├── client/           # Azure DevOps API HTTP 클라이언트
└── tests/            # 단위 테스트
```

## 주의사항

- `.env` 파일은 절대 커밋하지 마세요 (`.gitignore`에 포함되어 있습니다).
- AI가 Work Item 상태를 `Done`으로 변경하지 않도록 서버 `instructions`에 명시되어 있습니다. `Done` 설정은 사람이 직접 합니다.
- Dashboard API는 Azure DevOps의 팀 컨텍스트가 필요합니다. 기본 팀 설정이 없으면 일부 API가 동작하지 않을 수 있습니다.
