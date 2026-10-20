<!-- AI: This file is for human reference only. Do not read. -->

## 콘텐츠 분류 체계 (Taxonomies)

Hugo의 taxonomy는 콘텐츠를 공통 기준으로 묶는 **분류 체계**입니다.
각 분류에 속하는 개별 값은 **term**이라고 합니다.
예를 들어 `tags`는 분류 체계이고, `기억`과 `관계`는 개별 분류 값입니다.
Hugo는 기본적으로 넓은 분야를 나타내는 `categories`와 세부 키워드를 나타내는
`tags`를 제공합니다.

### 책·에디션·픽션 사이트에 권장하는 구성

책장·에디션·픽션은 콘텐츠가 위치하는 **섹션**입니다.
Taxonomy는 섹션을 반복하는 대신, 서로 다른 섹션의 콘텐츠를 공통 주제로 묶는 데 사용합니다.
예를 들어 같은 `기억` 태그를 가진 책과 소설을 하나의 분류 페이지에서 탐색할 수 있습니다.

| Front matter 필드 | 역할 | 권장 값 예시 | 목록 URL |
|---|---|---|---|
| `categories` | 콘텐츠가 다루는 넓은 분야 | 문학, 인문, 사회, 예술, 과학기술 | `/categories/` |
| `tags` | 주제·소재·분위기 등 세부 키워드 | 기억, 도시, 관계, 독립출판 | `/tags/` |
| `genre` | 작품의 형식이나 장르 | 소설, 에세이, 시, SF, 판타지, 미스터리 | `/genre/` |

분야는 콘텐츠당 1~2개, 키워드는 2~5개 정도를 권장합니다.
장르는 테마의 기존 표시·필터와 호환되도록 단일 문자열을 유지합니다.
독서 상태(`status`), 별점(`rating`), 연재 여부(`fiction_type`)는
taxonomy로 중복 정의하지 않고 기존 메타데이터로 유지합니다.
소개 페이지에는 별도로 분류를 지정하지 않아도 됩니다.

### 사이트 설정

다음은 사이트에서 선택해 적용하는 구성 예시이며, 테마 기본 설정을 변경하지는 않습니다.
사이트 루트의 `hugo.toml`에 추가합니다.

```toml
[taxonomies]
  category = "categories"
  tag      = "tags"
  genre    = "genre"
```

Hugo는 위 설정의 오른쪽 값을 front matter 필드명과 URL 경로로 사용합니다.
장르는 테마에서 이미 사용하는 `genre` 필드를 재사용하기 위해
`genre = "genre"`로 설정합니다.
사용자 정의 taxonomy를 지정할 때는 유지할 기본 분류인 `categories`와 `tags`도 함께 명시합니다.

분류 페이지를 생성하려면 기존 설정에서 다음 항목을 제거합니다.

```toml
disableKinds = ["taxonomy", "term"]
```

다른 종류의 페이지도 비활성화하고 있다면 해당 배열에서 `"taxonomy"`와 `"term"`만 제거합니다.
`disableKinds`는 `[pagination]` 등 다른 테이블 안이 아닌 최상위 설정으로 관리합니다.

분류 목록과 개별 분류의 콘텐츠 목록을 HTML로만 출력하려면 기존 `[outputs]`에
다음 두 항목을 병합합니다. 기존 `home`, `section` 등의 설정은 유지합니다.

```toml
[outputs]
  taxonomy = ["HTML"]
  term     = ["HTML"]
```

### 콘텐츠 작성 예시

일반 콘텐츠의 YAML front matter에 필요한 분류를 추가합니다.

```yaml
---
title: "콘텐츠 제목"
categories: ["문학"]
tags: ["기억", "관계"]
genre: "소설"
---
```

이 콘텐츠는 다음 분류 페이지에 연결됩니다.

- `/categories/문학/`
- `/tags/기억/`
- `/tags/관계/`
- `/genre/소설/`

설정 파일은 분류의 **종류**를 정의하고, 개별 분류 **값**은 콘텐츠에서 사용할 때 생성됩니다.
분류를 추가하기 위해 설정 파일에 모든 키워드를 미리 등록할 필요는 없습니다.
같은 개념에는 일관된 표기를 사용해 유사한 분류가 중복 생성되지 않도록 합니다.

현재 테마의 태그 배지는 링크가 아니므로, taxonomy 설정만으로 배지에 이동 기능이
추가되지는 않습니다. 생성된 분류 페이지는 해당 URL로 직접 접근할 수 있습니다.

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

## 내 사이트에 테마 적용하기

### 사전 준비

- Hugo Extended v0.115.0 이상
- Node.js v18 이상, npm v9 이상
- Git

### 1단계 — 테마 추가

```bash
# Hugo 사이트 루트에서
git submodule add https://dev.azure.com/lbrx/_git/HUGO-LBRX-IO-THEME themes/lbrx-io
git submodule update --init --recursive
```

또는 직접 클론:
```bash
git clone https://dev.azure.com/lbrx/_git/HUGO-LBRX-IO-THEME themes/lbrx-io
```

### 2단계 — CSS 빌드

```bash
cd themes/lbrx-io
npm install
npm run css:build   # assets/css/main.min.css 생성
cd ../..
```

> ⚠️ `assets/css/main.min.css`는 `.gitignore`에 포함되어 있습니다.  
> **클론 또는 테마 업데이트 후 반드시 `npm run css:build`를 실행하세요.**

### 3단계 — `hugo.toml` 설정

```bash
cp themes/lbrx-io/exampleSite/hugo.toml hugo.toml  # 예시 설정 복사
```

최소 필수 설정:
```toml
baseURL = "https://yoursite.com/"
title   = "사이트 제목"
theme   = "lbrx-io"

defaultContentLanguage = "ko"
disableKinds = ["taxonomy", "term"]

[params]
  description = "사이트 소개"
  author      = "이름"
  email       = "you@example.com"

[pagination]
  pagerSize = 12
```

전체 메뉴 및 다국어 설정은 `exampleSite/hugo.toml` 참고.

### 4단계 — 콘텐츠 구조 생성

```
content/
├── about/index.md        # type: "about" 필수
├── shelf/
├── editions/
└── fiction/
    ├── serials/
    └── standalone/
```

### 5단계 — 소개 페이지 (`about/index.md`)

```yaml
---
title: "소개"
type: "about"
space:
  ready: false
members:
  - id: "my-id"          # credited_to에서 참조하는 고유 ID
    name: "표시 이름"
    photo: "members/photo.jpg"
    bio: "소개글"
    email: "you@example.com"
brand:
  colors: []
  fonts: []
---
```

### 6단계 — 작성자 표시 (`credited_to`)

책장·에디션·픽션 파일에 `credited_to: "my-id"` 추가하면  
소개 페이지의 `id`로 멤버를 찾아 이름·사진을 자동 표시합니다.  
소개 페이지에서 이름을 바꾸면 전체 사이트에 즉시 반영됩니다.

### 7단계 — 실행 및 빌드

```bash
# 개발 서버
hugo server -D

# CSS 변경 시 (터미널 2개)
# 터미널 1 — CSS 감시
cd themes/lbrx-io && npx tailwindcss -i ./assets/css/main.css -o ./assets/css/main.min.css --watch

# 터미널 2 — Hugo 서버
hugo server -D

# 프로덕션 빌드
cd themes/lbrx-io && npm run css:build && cd ../..
hugo --minify
```

---

## 라이선스

MIT
