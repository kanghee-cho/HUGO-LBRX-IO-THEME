# Architecture

## Overview

`lbrx-io` is a custom Hugo theme for a literary personal brand site (LBRX.IO).  
It is built around four content sections with a Tailwind CSS build pipeline, Hugo Pipes for asset processing, Pagefind for static search, and Hugo's native i18n for bilingual (Korean/English) support.

---

## Theme Installation

### Prerequisites

| Requirement | Version |
|---|---|
| Hugo Extended | v0.115.0+ |
| Node.js | v18+ |
| npm | v9+ |
| Git | any |

### Step 1 — Add Theme as Git Submodule

```bash
# From your Hugo site root
git submodule add https://dev.azure.com/lbrx/_git/HUGO-LBRX-IO-THEME themes/lbrx-io
git submodule update --init --recursive
```

Or clone directly (without submodule):
```bash
git clone https://dev.azure.com/lbrx/_git/HUGO-LBRX-IO-THEME themes/lbrx-io
```

### Step 2 — Install Dependencies and Build CSS

```bash
cd themes/lbrx-io
npm install
npm run css:build   # generates assets/css/main.min.css
cd ../..
```

> ⚠️ `assets/css/main.min.css` is gitignored. Run `npm run css:build` after every fresh clone or theme update.

### Step 3 — Configure `hugo.toml`

Copy and customize the example config:
```bash
cp themes/lbrx-io/exampleSite/hugo.toml hugo.toml
```

Minimum required settings:
```toml
baseURL = "https://yoursite.com/"
title   = "Your Site Title"
theme   = "lbrx-io"

defaultContentLanguage = "ko"  # or "en"
disableKinds = ["taxonomy", "term"]

[params]
  description = "짧은 사이트 소개"
  author      = "Your Name"
  email       = "you@example.com"

[pagination]
  pagerSize = 12
```

For full menu and bilingual config, see `exampleSite/hugo.toml`.

### Step 4 — Content Directory Structure

```
content/
├── about/
│   └── index.md        # type: "about" required in front matter
├── shelf/
│   └── my-book.md
├── editions/
│   ├── _index.md
│   └── edition-01/
│       └── index.md
└── fiction/
    ├── serials/
    │   └── my-serial/
    │       ├── _index.md   # fiction_type: "serial" required
    │       └── chapter-01.md
    └── standalone/
        └── my-story.md
```

### Step 5 — About Page Setup

`content/about/index.md` must include `type: "about"` and the member list for the attribution chip system:
```yaml
---
title: "소개"
type: "about"
space:
  ready: false
members:
  - id: "your-id"          # stable slug — used in credited_to fields
    name: "표시 이름"
    photo: "members/photo.jpg"  # relative to assets/
    bio: "소개글"
    email: "you@example.com"
brand:
  colors: []
  fonts: []
---
```

### Step 6 — Member Attribution

Add `credited_to` to any shelf/edition/fiction content file using the member's `id`:
```yaml
credited_to: "your-id"
```

The `member-chip` partial looks up `id` in the About page front matter and displays the member's `name`. Changing the name in `about/index.md` updates all chips site-wide without touching content files.

### Step 7 — Development and Build

```bash
# Development (Hugo only — CSS already built)
hugo server -D

# Development with CSS hot-reload (two terminals)
# Terminal 1
cd themes/lbrx-io && npx tailwindcss -i ./assets/css/main.css -o ./assets/css/main.min.css --watch
# Terminal 2
hugo server -D

# Production build
cd themes/lbrx-io && npm run css:build && cd ../..
hugo --minify
```

---

## Tech Stack

| Component | Choice | Rationale |
|---|---|---|
| SSG | Hugo (Extended) | Fast builds, excellent i18n, powerful templating, Hugo Pipes |
| CSS Framework | Tailwind CSS v3 | Utility-first, `class`-based dark mode, purges unused CSS |
| CSS Processing | PostCSS + Autoprefixer | Standard Tailwind pipeline integrated via npm |
| Search | Pagefind | Static-site native, zero server required, tiny JS bundle |
| JS | Vanilla JS | No framework overhead; only two scripts (theme toggle, search) |
| Language | Korean (primary) + English | Hugo built-in i18n, bilingual posts via file suffix |
| Dark Mode | Tailwind `class` strategy | Controlled by JS, defaults to system preference |

---

## Directory Structure

```
HUGO-LBRX-IO-THEME/
├── theme.toml                         # Hugo theme metadata
├── package.json                       # Node deps: Tailwind, PostCSS, Autoprefixer, Pagefind
├── tailwind.config.js                 # Tailwind config — dark mode: 'class', content paths
├── postcss.config.js                  # PostCSS config — tailwindcss + autoprefixer plugins
├── .gitignore
├── README.md                          # Korean-language project readme
│
├── docs/
│   └── ARCHITECTURE.md               # This file
│
├── layouts/
│   ├── _default/
│   │   ├── baseof.html               # HTML shell — wires head, header, main block, footer
│   │   ├── home.html                 # Homepage layout
│   │   ├── list.html                 # Generic section list
│   │   ├── single.html              # Generic single content page
│   │   └── rss.xml                  # Custom RSS feed template
│   ├── partials/
│   │   ├── head.html                 # <head>: charset, viewport, title, CSS, OG meta
│   │   ├── header.html               # Site header + nav (data-pagefind-ignore)
│   │   ├── footer.html               # Site footer (data-pagefind-ignore)
│   │   ├── nav.html                  # Navigation — desktop CSS-only dropdown, mobile indented sub-items
│   │   ├── theme-toggle.html         # Dark/light toggle button
│   │   ├── search-modal.html         # Pagefind Cmd+K modal overlay
│   │   ├── shelf-pagination.html     # Reusable pagination nav component
│   │   ├── status-badge.html         # Reading status badge (read/reading/wishlist/abandoned)
│   │   ├── book-card.html            # Reusable book card component
│   │   └── fiction-card.html         # Reusable fiction card component
│   ├── shelf/
│   │   ├── list.html                 # Bookshelf index page
│   │   └── single.html              # Single book entry (data-pagefind-body)
│   ├── Editions/
│   │   ├── list.html                 # Editions index page
│   │   └── single.html              # Single Edition entry (data-pagefind-body)
│   ├── fiction/
│   │   ├── list.html                 # Fiction index (overview: series + standalones)
│   │   ├── fiction-serials.html      # /fiction/serials/ — serial-only list
│   │   ├── fiction-standalone.html   # /fiction/standalone/ — standalone list with pagination
│   │   ├── series.html               # Serial series detail page (episode list)
│   │   └── single.html              # Single story or episode (data-pagefind-body)
│   ├── about/
│   │   └── single.html              # About me page
│   └── 404.html
│
├── assets/
│   ├── css/
│   │   └── main.css                  # @tailwind base/components/utilities entry point
│   └── js/
│       ├── theme-toggle.js           # Dark/light mode: reads localStorage → system pref
│       └── search.js                 # Pagefind modal: Cmd+K, lazy-load, debounce, render
│
├── static/
│   ├── fonts/
│   └── images/
│
├── i18n/
│   ├── ko.yaml                        # Korean UI strings (primary)
│   └── en.yaml                        # English UI strings
│
├── archetypes/
│   ├── default.md
│   ├── shelf.md                       # Book entry front matter
│   ├── Editions.md                   # Edition entry front matter
│   └── fiction.md                     # Fiction/story front matter
│
└── exampleSite/
    ├── hugo.toml                       # References theme, sets defaultContentLanguage = "ko"
    ├── content/
    │   ├── shelf/_index.md
    │   ├── Editions/_index.md
    │   ├── fiction/_index.md
    │   └── about/_index.md
    └── static/
```

---

## Content Types

### Shelf

Personal bookshelf. Each entry represents one book.

**Create a book entry:**
```bash
hugo new shelf/book-slug.md
# e.g. hugo new shelf/norwegian-wood.md
```

**Key front matter fields:**

| Field | Type | Description |
|---|---|---|
| `author` | string | Author name |
| `status` | string | `read` / `reading` / `wishlist` / `abandoned` |
| `rating` | float | `0.5`–`5.0` (half-star supported) |
| `cover` | string | Image URL or path |
| `genre` | string | Genre label |
| `read_date` | string | Completion date `YYYY-MM-DD` |
| `owned` | bool | Whether the physical book is owned |
| `call_number` | string | Library shelf number (e.g. `KOR-HAN-001`) |

The `slug` (filename without `.md`) is the identifier used when referencing the book in Editions.

---

### Editions

Curated book collections. Each entry lists selected shelf books with annotations.

**Create an edition:**
```bash
hugo new editions/2025-spring.md
```

**Key front matter fields:**

| Field | Type | Description |
|---|---|---|
| `edition_number` | int | Display serial number (e.g. `3` → shown as `#3`) |
| `accent_color` | string | One of: `rose` `pink` `fuchsia` `violet` `indigo` `sky` `cyan` `teal` `emerald` `lime` `amber` `orange` |
| `books` | list | Array of `{slug, reason}` objects |

**`books` field example:**
```yaml
books:
  - slug: norwegian-wood      # shelf 파일명 (확장자 제외)
    reason: "상실의 시대를 관통하는 조용한 슬픔"
  - slug: the-great-gatsby
    reason: "꿈과 환멸 사이의 아름다운 비극"
```

**Layout features:**
- Accent color palette system (`edition-palette.html` partial) — 12 colors, each providing `cardBg`, `headerBg`, `title`, `meta`, `reason`, `border`, `strip`, `hoverBg` class sets
- List page: current edition (full book grid) + paginated archive list (5 per page) with responsive thumbnail strip
- Book grid breakpoints: `grid-cols-3 sm:grid-cols-4 lg:grid-cols-6` (matches shelf)
- Single page: header banner, book grid, editor's note prose, previous/next edition navigation
- Pagination uses `.Paginate $archiveAll 5`; current edition (index 0) is rendered outside the paginator

---

### Fiction

Original creative writing. Two types: **standalone** short stories and **serials** (multi-episode).

#### Standalone Short Story

```bash
hugo new fiction/my-story.md
```

**Key front matter fields:**

| Field | Type | Description |
|---|---|---|
| `fiction_type` | string | Always `standalone` |
| `genre` | string | Genre label (e.g. `단편소설`, `시`) |
| `word_count` | int | Approximate word/character count |

Use `---` in Markdown body to insert a `✦` ornament section separator.

#### Serial — Series Index

```bash
hugo new fiction/series-name/_index.md --kind fiction-series
```

**Key front matter fields:**

| Field | Type | Description |
|---|---|---|
| `fiction_type` | string | Always `serial` |
| `layout` | string | Always `series` |
| `status` | string | `ongoing` / `complete` |
| `genre` | string | Genre label |

#### Serial — Episode

```bash
hugo new fiction/series-name/episode-1.md --kind fiction-episode
```

**Key front matter fields:**

| Field | Type | Description |
|---|---|---|
| `episode` | int | Episode number (used for ordering and display) |
| `word_count` | int | Approximate word/character count |

Episodes are sorted by `episode` parameter ascending.  
The episode single page auto-detects its parent series and shows the series header + episode dropdown + prev/next episode navigation.

**Content directory structure:**
```
content/fiction/
  _index.md                       # Fiction section index (overview)
  serials/
    _index.md                     # /fiction/serials/ — serial list page (layout: fiction-serials)
  standalone/
    _index.md                     # /fiction/standalone/ — standalone list page (layout: fiction-standalone, paginated)
    standalone-story.md           # 단편 (url override: /fiction/standalone-story/)
    another-story.md
  my-series/
    _index.md                     # 연작 인덱스 (fiction_type: serial, layout: series)
    episode-1.md                  # 1화
    episode-2.md                  # 2화
```

> **URL override:** Standalone stories use `url: "/fiction/slug/"` in front matter to keep clean URLs (e.g. `/fiction/my-story/`) even though they are stored under `content/fiction/standalone/`.

**Fiction sub-navigation:**

The `픽션` nav item in `hugo.toml` has `identifier = "fiction"` with two child menu items:
- `연작` → `/fiction/serials/` (layout: `fiction-serials`, paginated 5/page)
- `단편` → `/fiction/standalone/` (layout: `fiction-standalone`, paginated 5/page)

`nav.html` renders a **CSS-only hover dropdown** on desktop (using Tailwind `group`/`group-hover`) and **always-visible indented sub-items** on mobile. No JavaScript required.

**Fiction index page (`/fiction/`) — overview layout:**

The main fiction page shows a curated preview with "전체 보기" links, not a full list:
- **최신연작** — 2 most recent serials (by Hugo default order) + link to `/fiction/serials/`
- **최신단편** — 3 most recent standalones + link to `/fiction/standalone/`
- "전체 보기" button appears only when total count exceeds the preview limit (>2 for serials, >3 for standalones)

**Pagination rules across Fiction layouts:**

| Layout | Trigger | Per page |
|---|---|---|
| `fiction/list.html` (index) | Preview only — no pagination | 2 serials + 3 standalones |
| `fiction-serials.html` | Always paginated | 5 serials/page |
| `fiction-standalone.html` | Always paginated | 5 standalones/page |
| `series.html` (episode list) | >5 episodes | 5 episodes/page |

**i18n keys for Fiction index section headings:**

| Key | ko | en |
|---|---|---|
| `fiction_serial_recent` | 최신연작 | Latest Serials |
| `fiction_standalone_recent` | 최신단편 | Latest Stories |

---

### About

`about/index.md` — type: `"about"`, mapped to `layouts/about/single.html`.

Structured into 3 sections, all data managed via front matter YAML:

**Space section** (`space.*`):
- `ready: false` → shows "준비중" banner only
- `ready: true` → renders name, address, hours table, Google Maps iframe
- `map_embed`: Google Maps embed URL (from 공유 → 지도 퍼가기 → `src` value)

**Brand/CI section** (`brand.*`):
- `logo_light` / `logo_dark`: SVG/PNG paths relative to `exampleSite/assets/`
- `colors`: array of `{name, hex, desc}` — renders as color swatches
- `fonts`: array of `{role, name, stack}` — renders font name in its own stack

**Members section** (`members.*`):
- Array of `{name, photo, bio, email}`
- `photo`: path relative to `exampleSite/assets/`
- `email`: displayed as plain selectable text (no `mailto:` link)

**i18n keys** (about section):

| Key | ko | en |
|---|---|---|
| `about_space` | 공간 | Space |
| `about_space_coming_soon` | 준비 중입니다 | Coming soon |
| `about_space_address` | 주소 | Address |
| `about_space_hours` | 영업시간 | Hours |
| `about_space_map` | 지도 | Map |
| `about_brand` | 브랜드 | Brand |
| `about_brand_colors` | 색상 | Colors |
| `about_brand_fonts` | 서체 | Typography |
| `about_members` | 함께하는 사람 | People |
| `about_contact` | 연락처 | Contact |

---

### Favicon

`layouts/partials/head.html` supports 4 favicon formats:

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

Files go in `exampleSite/static/`. `favicon.svg` and `site.webmanifest` are included as placeholders. PNG/ICO files can be generated at [realfavicongenerator.net](https://realfavicongenerator.net).

`site.webmanifest` theme color: `#6b7c2d` (olive-600), background: `#fafaf5` (olive-50).

---

## Build Pipeline

### Development
```bash
npm run dev
# Runs: hugo server --source exampleSite --themesDir=../.. + Tailwind CSS watch (concurrently)
# Must be run from theme root (HUGO-LBRX-IO-THEME/)
# NOTE: Pagefind search index is NOT generated in dev mode.
```

### Production
```bash
npm run build
# Runs: hugo --minify && pagefind --site public
# Outputs to: public/
# Pagefind index written to: public/pagefind/
```

---

## Pagefind Integration

Pagefind is a static search library that indexes the built Hugo output.

### Indexing

- `pagefind --site public` runs after `hugo --minify` and writes the search index to `public/pagefind/`.
- Content templates use `data-pagefind-body` on the `<article>` element to mark indexable content.
- Header and footer partials use `data-pagefind-ignore` to exclude chrome from the index.
- Single layouts include `data-pagefind-meta` tags for `title`, `section`, and `language`.

### Search UI

- **Trigger:** `Cmd+K` (macOS) / `Ctrl+K` (Windows/Linux), or a search icon button in the nav.
- **Modal:** A fixed overlay `<dialog>` element styled with Tailwind. Closes on `Esc` or click-outside.
- **JS (`search.js`):**
  1. Lazily imports `/pagefind/pagefind.js` on first modal open (avoids loading on every page).
  2. Debounces the search input (300 ms).
  3. Calls `pagefind.search(query)` and renders result cards (title, URL, excerpt) into `#search-results`.
- **Styling:** Fully Tailwind-styled with `dark:` variants. No Pagefind default CSS (`pagefind-ui.css`) is used.

> ⚠️ Pagefind does not work with `hugo server`. Run `npm run build` and serve the `public/` directory to test search locally.

---

## Dark Mode

**Strategy:** Tailwind CSS `class` strategy.

| Priority | Source |
|---|---|
| 1st | `localStorage` value set by the toggle button |
| 2nd | `prefers-color-scheme` media query (system preference) |

**Implementation:**
- `theme-toggle.js` runs inline in `<head>` (before paint) to avoid flash of wrong theme.
- Toggling adds or removes the `dark` class on `<html>`.
- The toggle button state is updated to reflect the current mode.

---

## i18n

Hugo's built-in i18n system is used.

| Setting | Value |
|---|---|
| Default language | `ko` (Korean) |
| Secondary language | `en` (English) |
| Bilingual posts | Use file suffix: `post.ko.md` / `post.en.md` |

Translation strings (nav labels, section headings, search placeholder, "no results" text, etc.) live in `i18n/ko.yaml` and `i18n/en.yaml`. Templates reference them via `{{ i18n "key" }}`.

---

## Key Design Decisions

| Decision | Choice | Why |
|---|---|---|
| Dark mode implementation | `class` strategy + JS | Full control; system pref as default; no flash |
| Search UI | Custom (Pagefind JS API) | Tailwind-compatible; avoids CSS conflicts with pagefind-ui.css |
| Search trigger | Cmd+K modal | Modern UX; doesn't interrupt reading flow |
| JS framework | None (Vanilla JS) | Two tiny scripts don't justify a framework |
| CSS framework | Tailwind v3 | Utility-first fits Hugo's template-centric workflow |
| i18n approach | Hugo built-in | Zero extra dependencies; file-suffix bilingual posts |
| Archetypes | Per section | Ensures correct front matter for each content type |
| RSS strategy | Global + Fiction + Editions | Fiction readers & book curation subscribers have separate feeds |
| Book grid breakpoints | `grid-cols-3 sm:grid-cols-4 lg:grid-cols-6` | Matches shelf grid for visual consistency across all book-display contexts |
| Edition accent palette | Dynamic class strings in `edition-palette.html` | Tailwind JIT detects full class strings; palette partial returns a dict |
| Fiction sub-navigation | Separate `/fiction/serials/` + `/fiction/standalone/` pages | Enables per-section pagination; Hugo `.Paginate` requires a list/section page, not a single page |
| Status badge style | Outline/border style for all 4 statuses | Visually distinct without heavy background fills; olive outline for `read` signals completion |
| Standalone stories in sub-folder | `content/fiction/standalone/` + `url` override | Required to enable `.Paginate` on the standalone section page while preserving clean `/fiction/slug/` URLs |
| Fiction sub-navigation | Separate `/fiction/serials/` + `/fiction/standalone/` pages | Enables per-section pagination; Hugo `.Paginate` requires a list/section page, not a single page |
| Status badge style | Outline/border style for all 4 statuses | Visually distinct without heavy background fills; olive outline for `read` signals completion |
| Standalone stories in sub-folder | `content/fiction/standalone/` + `url` override | Required to enable `.Paginate` on the standalone section page while preserving clean `/fiction/slug/` URLs |

---

## RSS Feeds

Hugo auto-generates RSS at build time — no extra tooling required.

### Feed Endpoints

| URL | Content | Format |
|---|---|---|
| `/index.xml` | All sections combined | Summary |
| `/fiction/index.xml` | Fiction only | **Full content** |
| `/Editions/index.xml` | Editions only | Summary + cover image |
| `/ko/index.xml` | Korean content | Auto via multilingual mode |
| `/en/index.xml` | English content | Auto via multilingual mode |

> **About** section is excluded from RSS via `outputs` front matter in `about/_index.md`.

### Content Strategy per Section

| Section | RSS Content | Reason |
|---|---|---|
| Fiction | Full `.Content` | Short stories should be readable directly in feed readers |
| Editions | Summary + cover image meta | Teaser to visit the site; images add visual context |
| Shelf | Summary only | Individual book entries can be noisy; keep it brief |

### Implementation

**`layouts/_default/rss.xml`** (custom template):
- `xml:lang` set from Hugo's `.Site.Language.Lang`
- `<author>` tag from `hugo.toml` `[author]` config
- `<category>` from `.Section`
- Fiction feed: `{{ .Content }}` (full)
- Others: `{{ .Summary }}`

**`exampleSite/hugo.toml`** `[outputs]` block:
```toml
[outputs]
  home    = ["HTML", "RSS"]
  section = ["HTML", "RSS"]
  taxonomy = ["HTML"]
```

**`content/about/_index.md`** front matter:
```yaml
outputs: ["HTML"]   # Disable RSS for About
```
