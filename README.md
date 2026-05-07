<!-- AI: This file is for human reference only. Do not read. -->
# LBRX.IO 테마

`lbrx-io`는 [Hugo](https://gohugo.io/) 정적 사이트 생성기를 위한 개인 브랜드 테마입니다.  
책과 글쓰기를 중심으로 한 문학적 개인 사이트를 위해 설계되었습니다.

---

## 사이트 구성

| 섹션 | 설명 |
|---|---|
| **서재 (Shelf)** | 읽은 책·읽고 있는 책을 관리하는 개인 책장 |
| **에디션 (Editions)** | 선별한 책 큐레이션. 회차별 이전/다음 네비게이션, 12가지 액센트 컬러, 아카이브 페이지네이션(5개/페이지) |
| **픽션 (Fiction)** | 단편 소설 및 연작 창작 글. 픽션 메인(최신연작 2편+최신단편 3편 미리보기), 연작 전체목록(/serials/, 5개/페이지), 단편 전체목록(/standalone/, 5개/페이지), 회차 6화 이상 시 회차 페이지네이션 |
| **소개 (About)** | 공간(주소·영업시간·지도), 브랜드/CI(로고·색상·서체), 함께하는 사람(사진·소개·이메일) 3개 섹션 구성. 데이터는 front matter YAML로 관리 |

---

## 기술 스택

| 구성 요소 | 선택 |
|---|---|
| 정적 사이트 생성기 | Hugo Extended |
| CSS 프레임워크 | Tailwind CSS (Node.js + npm 빌드 파이프라인) |
| 검색 | Pagefind (Cmd+K 모달, 커스텀 UI) |
| 다국어 | 한국어 우선, 영어 병행 (Hugo i18n) |
| 다크 모드 | 시스템 환경설정 우선 + 토글 버튼 |

---

## 시작하기

### 사전 요구 사항

- [Hugo](https://gohugo.io/installation/) Extended 버전
- [Node.js](https://nodejs.org/) v18 이상
- npm

### 설치 및 실행

```bash
# 1. 의존성 설치
npm install

# 2. 개발 서버 실행 (Tailwind 자동 빌드 포함)
npm run dev

# 3. 프로덕션 빌드 (Tailwind + Hugo + Pagefind 인덱스 생성)
npm run build
```

> ⚠️ `hugo server`만 단독 실행하면 CSS가 반영되지 않습니다. 반드시 **테마 루트**에서 `npm run dev`를 사용하세요.  
> ⚠️ `npm run dev`는 내부적으로 `--source exampleSite --themesDir=../..` 옵션으로 실행되므로, exampleSite 폴더에서 별도 실행할 필요가 없습니다.

---

## 콘텐츠 작성 방법

### 📚 서재 — 책 추가

```bash
hugo new shelf/책-파일명.md
# 예: hugo new shelf/norwegian-wood.md
```

파일명(슬러그)이 에디션에서 책을 참조할 때 사용되므로 의미 있는 영문 이름을 사용하세요.

| 필드 | 설명 |
|---|---|
| `author` | 저자 |
| `status` | `read` / `reading` / `wishlist` / `abandoned` |
| `rating` | `0.5`–`5.0` (반별 지원) |
| `cover` | 커버 이미지 URL 또는 경로 |
| `genre` | 장르 |
| `read_date` | 완독일 `YYYY-MM-DD` |
| `owned` | 소장 여부 `true` / `false` |

---

### 📖 에디션 — 큐레이션 추가

```bash
hugo new editions/2025-spring.md
```

| 필드 | 설명 |
|---|---|
| `edition_number` | 표시용 번호 (예: `3` → `#3`) |
| `accent_color` | `rose` `pink` `fuchsia` `violet` `indigo` `sky` `cyan` `teal` `emerald` `lime` `amber` `orange` 중 하나 |
| `books` | `{slug, reason}` 배열 |

```yaml
books:
  - slug: norwegian-wood        # shelf 파일명 (확장자 제외)
    reason: "상실의 시대를 관통하는 조용한 슬픔"
  - slug: the-great-gatsby
    reason: "꿈과 환멸 사이의 아름다운 비극"
```

---

### ✍️ 픽션 — 단편 추가

단편은 `content/fiction/standalone/` 하위에 생성합니다.  
URL은 `url` 프론트매터로 `/fiction/글-파일명/` 형태로 유지할 수 있습니다.

```bash
hugo new fiction/standalone/글-파일명.md
```

| 필드 | 설명 |
|---|---|
| `fiction_type` | `standalone` (기본값) |
| `url` | `/fiction/글-파일명/` (URL 유지용, 필수) |
| `genre` | 장르 (예: `단편소설`, `시`) |
| `word_count` | 분량 (글자 수) |

본문에서 `---`를 사용하면 `✦` 장식 구분선으로 표시됩니다.

### ✍️ 픽션 — 연작 추가

연작 시리즈는 `content/fiction/` 하위에 디렉터리로 생성합니다. `_index.md`에 반드시 `fiction_type: "serial"`을 지정해야 연작 목록에 표시됩니다.

```bash
# 1. 시리즈 인덱스 생성
hugo new fiction/시리즈명/_index.md --kind fiction-series

# 2. 회차 생성
hugo new fiction/시리즈명/episode-1.md --kind fiction-episode
hugo new fiction/시리즈명/episode-2.md --kind fiction-episode
```

| 필드 | 설명 |
|---|---|
| `fiction_type` | `serial` (반드시 명시 — 연작 목록 필터링에 사용) |
| `status` | (인덱스) `ongoing` / `complete` |
| `episode` | (회차) 회차 번호 — 정렬 및 표시에 사용 |

회차는 `episode` 번호 오름차순으로 정렬됩니다.

---

## 프로젝트 구조

```
.
├── layouts/
│   ├── _default/           # 기본 레이아웃
│   ├── partials/           # 재사용 컴포넌트 (nav, status-badge, shelf-pagination 등)
│   ├── shelf/              # 서재 레이아웃
│   ├── editions/           # 에디션 레이아웃
│   └── fiction/            # 픽션 레이아웃
│       ├── list.html               # 픽션 메인 (최신연작 2편 + 최신단편 3편 미리보기)
│       ├── fiction-serials.html    # /fiction/serials/ — 연작 전체목록 (5개/페이지)
│       ├── fiction-standalone.html # /fiction/standalone/ — 단편 전체목록 (5개/페이지)
│       ├── series.html             # 연작 시리즈 상세 (6화+ 시 회차 페이지네이션)
│       └── single.html             # 단편·회차 본문
├── assets/css/             # Tailwind CSS 진입점
├── i18n/                   # 한국어·영어 번역 문자열
├── archetypes/             # 콘텐츠 타입별 프론트매터 템플릿
│   ├── shelf.md
│   ├── editions.md
│   ├── fiction.md          # 단편
│   ├── fiction-series.md   # 연작 인덱스
│   └── fiction-episode.md  # 회차
└── exampleSite/            # 예시 사이트
    └── content/fiction/
        ├── standalone/     # 단편 저장 디렉터리
        └── [시리즈명]/    # 연작 디렉터리
```

---

## 다크 모드

시스템 환경설정(`prefers-color-scheme`)을 우선 적용하며, 우측 상단 토글 버튼으로 수동 변경 가능합니다.  
선택한 모드는 `localStorage`에 저장되어 다음 방문 시에도 유지됩니다.

---

## 검색

- `Cmd+K` / `Ctrl+K`로 검색 모달을 엽니다.
- [Pagefind](https://pagefind.app/) JS API 기반 커스텀 UI. 다크 모드 완벽 지원.

---

## 다국어 지원

한국어(`ko`)가 기본 언어이며 영어(`en`) 병행 제공.  
이중 언어 포스트: 파일 이름 접미사로 구분 (예: `post.en.md`).

---

## 소개(About) 페이지 구성

`content/about/index.md` front matter YAML로 모든 데이터를 관리합니다.

### 공간 섹션

```yaml
space:
  ready: false          # false면 "준비중" 배너만 표시
  name: "LBRX 서재"
  address: "서울특별시 ..."
  hours:
    - day: "화–금"
      time: "13:00 – 19:00"
  map_embed: "https://www.google.com/maps/embed?pb=..."  # Google Maps 퍼가기 URL
```

지도 embed URL: Google Maps → 공유 → **지도 퍼가기** → `<iframe src="..."` 의 `src` 값만 복사.

### 브랜드/CI 섹션

```yaml
brand:
  logo_light: "brand/logo-light.svg"   # exampleSite/assets/ 기준 경로
  logo_dark: "brand/logo-dark.svg"
  colors:
    - name: "Olive 600"
      hex: "#6b7c2d"
      desc: "주색상 — 링크, 강조"
  fonts:
    - role: "본문·UI"
      name: "Pretendard Variable"
      stack: "Pretendard Variable, Noto Sans JP, sans-serif"
```

### 함께하는 사람 섹션

```yaml
members:
  - name: "이름"
    photo: "members/photo.jpg"   # exampleSite/assets/ 기준 경로
    bio: "간략한 소개"
    email: "email@example.com"   # mailto 링크 없이 텍스트 표시
```

---

## 파비콘

`layouts/partials/head.html`에 4가지 형식 지원:

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

파일은 `exampleSite/static/`에 배치. [realfavicongenerator.net](https://realfavicongenerator.net)에서 `favicon.svg` 업로드 시 전체 세트 생성 가능.

| 파일 | 용도 |
|---|---|
| `favicon.ico` | 구형 브라우저 32×32 |
| `favicon.svg` | 모던 브라우저 (권장) |
| `apple-touch-icon.png` | iOS 홈화면 180×180 |
| `site.webmanifest` | PWA 메타데이터 |

---

## RSS

| 피드 | 내용 |
|---|---|
| `/index.xml` | 전체 |
| `/fiction/index.xml` | 픽션 전문 (전체 본문) |
| `/editions/index.xml` | 에디션 요약 |
| `/ko/index.xml` | 한국어 피드 |
| `/en/index.xml` | 영어 피드 |

---

## 라이선스

MIT
