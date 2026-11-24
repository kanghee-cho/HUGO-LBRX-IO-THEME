# Architecture

Start with the [Theme Guide](./THEME-GUIDE.md) for installation, configuration,
content authoring, customization, and troubleshooting. This document covers
implementation details and design decisions.

## Overview

`lbrx-io` is a custom Hugo theme for a literary personal brand site (LBRX.IO).  
It is built around four content sections with a Tailwind CSS build pipeline, Hugo Pipes for asset processing, Pagefind for static search, and Hugo's native i18n for bilingual (Korean/English) support.

---

## Theme Installation

### Prerequisites

| Requirement | Version |
|---|---|
| Hugo Extended | Current release; metadata minimum v0.120.0 |
| Node.js | v20+ |
| npm | v9+ |
| Git | any |

### Step 1 — Add Theme as Git Submodule

```bash
# From your Hugo site root
git submodule add https://github.com/kanghee-cho/HUGO-LBRX-IO-THEME.git themes/lbrx-io
git submodule update --init --recursive
```

Or clone directly (without submodule):
```bash
git clone https://github.com/kanghee-cho/HUGO-LBRX-IO-THEME.git themes/lbrx-io
```

### Step 2 — Install Dependencies and Build CSS

```bash
cd themes/lbrx-io
npm ci
npm run css:build   # generates assets/css/main.min.css
cd ../..
```

> ⚠️ `assets/css/main.min.css` is gitignored. Run `npm run css:build` after every fresh clone or theme update.

### Step 3 — Configure `hugo.toml`

Copy and customize the example config:
```bash
cp themes/lbrx-io/exampleSite/hugo.toml hugo.toml
```

After copying, change `theme` to `lbrx-io` to match the installation directory
and replace the demonstration site parameters. Use a Hugo release supporting
the example's `[pagination]` table.

Minimum required settings:
```toml
baseURL = "https://yoursite.com/"
title   = "Your Site Title"
theme   = "lbrx-io"

defaultContentLanguage = "ko"  # or "en"
disableKinds = ["taxonomy", "term"]

[params]
  description = "Books, editions, and fiction."
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
    ├── _index.md
    ├── serials/
    │   └── _index.md       # layout: "fiction-serials"
    ├── my-serial/
    │   ├── _index.md       # fiction_type: "serial", layout: "series"
    │   └── chapter-01.md
    └── standalone/
        ├── _index.md       # layout: "fiction-standalone"
        └── my-story.md
```

### Step 5 — About Page Setup

`content/about/index.md` must include `type: "about"` and the member list for the attribution chip system:
```yaml
---
title: "About"
type: "about"
outputs: ["HTML"]
space:
  ready: false
members:
  - id: "your-id"          # stable slug — used in credited_to fields
    name: "Display Name"
    photo: "members/photo.jpg"  # relative to assets/
    bio: "A short introduction."
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
cd themes/lbrx-io && npm run css:watch
# Terminal 2
hugo server -D

# Production build
cd themes/lbrx-io && npm run css:build && cd ../..
hugo --minify
```

For search, run the installed Pagefind CLI against the consuming site's
generated output after a successful Hugo build. See the
[production build instructions](./THEME-GUIDE.md#production-build-with-search).

---

## Tech Stack

| Component | Choice | Rationale |
|---|---|---|
| SSG | Hugo (Extended) | Fast builds, excellent i18n, powerful templating, Hugo Pipes |
| CSS Framework | Tailwind CSS v4 | CSS-first configuration, class-based dark mode, explicit source detection |
| CSS Processing | `@tailwindcss/cli` | Standalone compilation with built-in imports and vendor prefixing; PostCSS is used only by regression checks |
| Search | Pagefind | Static-site native, zero server required, tiny JS bundle |
| JS | Vanilla JS | Theme toggle, navigation, search, and daily shelf selection without a framework |
| Language | Korean (primary) + English | Hugo built-in i18n; separate language content directories in the example |
| Dark Mode | Tailwind `class` strategy | Controlled by JS, defaults to system preference |

---

## Directory Structure

```
HUGO-LBRX-IO-THEME/
├── theme.toml                         # Hugo theme metadata
├── package.json                       # Node deps: Tailwind v4 CLI, Typography, Pagefind, PostCSS test parser
├── tests/css.test.cjs                 # Compiled CSS regression checks
├── .gitignore
├── README.md                          # Korean-language project readme
│
├── docs/
│   ├── THEME-GUIDE.md                # Installation, configuration, and authoring
│   └── ARCHITECTURE.md               # Implementation reference
│
├── layouts/
│   ├── index.html                    # Homepage layout
│   ├── _default/
│   │   ├── baseof.html               # HTML shell — wires head, header, main block, footer
│   │   ├── list.html                 # Generic section list
│   │   └── single.html               # Generic single content page
│   ├── partials/
│   │   ├── head.html                 # <head>: charset, viewport, title, CSS, OG meta
│   │   ├── header.html               # Site header + nav (data-pagefind-ignore)
│   │   ├── footer.html               # Site footer (data-pagefind-ignore)
│   │   ├── nav.html                  # Navigation — desktop CSS-only dropdown, mobile indented sub-items
│   │   ├── search-modal.html         # Pagefind Cmd+K modal overlay
│   │   ├── shelf-pagination.html     # Reusable pagination nav component
│   │   ├── status-badge.html         # Reading status badge (read/reading/wishlist/abandoned)
│   │   ├── star-rating.html          # Half-star rating display
│   │   ├── member-chip.html          # Attribution by stable member ID
│   │   └── edition-palette.html      # Twelve edition accent palettes
│   ├── shelf/
│   │   ├── list.html                 # Bookshelf index page
│   │   └── single.html              # Single book entry (data-pagefind-body)
│   ├── editions/
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
│   │   ├── fonts.css                 # Self-hosted font declarations
│   │   └── main.css                  # Tailwind import, sources, theme, dark variant, Typography, custom styles
│   └── js/
│       ├── theme-toggle.js           # Dark/light mode: reads localStorage → system pref
│       ├── nav.js                    # Mobile navigation
│       ├── shelf-daily.js            # Daily bookshelf selection
│       └── search.js                 # Pagefind modal: Cmd+K, lazy-load, debounce, render
│
├── static/
│   ├── fonts/                        # WOFF2 assets and license notices
│   ├── favicon.svg
│   ├── favicon.ico
│   ├── apple-touch-icon.png
│   ├── android-chrome-192x192.png
│   ├── android-chrome-512x512.png
│   └── site.webmanifest
│
├── i18n/
│   ├── ko.yaml                        # Korean UI strings (primary)
│   └── en.yaml                        # English UI strings
│
├── archetypes/
│   ├── default.md
│   ├── shelf.md                       # Book entry front matter
│   ├── editions.md                   # Edition entry front matter
│   ├── fiction.md                    # Standalone story front matter
│   ├── fiction-series.md             # Serial index front matter
│   └── fiction-episode.md            # Episode front matter
│
└── exampleSite/
    ├── hugo.toml                       # References theme, sets defaultContentLanguage = "ko"
    ├── assets/                       # Site-specific logos and member images
    └── content/
        ├── shelf/
        ├── editions/
        ├── fiction/_index.md
        └── about/index.md
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
hugo new fiction/standalone/my-story.md --kind fiction
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
- Array of `{id, name, photo, bio, email}`; `id` is the stable attribution key
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

The default LBRX Press icon combines a geometric **L**, a folded
paper sheet, and two printing-press rails. Pine (`#246958`), Paper (`#F3F4EC`),
and the light selection color (`#D8E6DA`) match the brand palette. The SVG uses
paths instead of text, so it has no font dependency.

All default assets are bundled in the theme's `static/` directory:

| Asset | Size / purpose |
|---|---|
| `favicon.svg` | Scalable browser icon; canonical design |
| `favicon.ico` | 16px, 32px, and 48px browser fallback frames |
| `apple-touch-icon.png` | 180px Apple touch icon |
| `android-chrome-192x192.png` | 192px manifest icon |
| `android-chrome-512x512.png` | 512px manifest icon |
| `site.webmanifest` | Names, colors, and relative PNG icon URLs |

`layouts/partials/head.html` links the assets using Hugo's `relURL`, including
sites hosted under a URL subpath. A consuming site's own `static/` files can
override these defaults. Raster files are generated from the SVG with resvg;
the ICO contains independently rendered frames for legibility at small sizes.
No icon-generation tools or additional dependencies are required to build
the theme.

`site.webmanifest` theme color: `#246958` (Pine), background: `#F3F4EC` (Paper).

### Brand Colors and Typography

The brand palette and font stacks follow `themes/lbrx.toml` from the
`lbrx-integrated-theme` project. This theme contains its own values and font
assets; builds do not depend on that checkout or an absolute local path.

| Role | Light | Dark |
|---|---|---|
| Background | `#F3F4EC` | `#19231F` |
| Surface and code blocks | `#E8EDE4` | `#25332C` |
| Text and headings | `#24362F` | `#DCE6DB` |
| Accent and links | `#246958` | `#84C7AC` |
| Muted text | `#52655B` | `#A3B5A9` |
| Inline code | `#80516A` | `#D4A8BD` |

`assets/css/main.css` defines light/dark `--brand-*` role variables and exposes
them through Tailwind's inline `--color-brand-*` theme tokens. Use semantic
utilities such as `bg-brand-background`, `text-brand-text`, and
`text-brand-accent` rather than a numbered brand color scale. The existing
`.dark` class switches the role values. Accent-filled controls use
`text-brand-on-accent` to preserve contrast in both modes. The twelve
edition-specific accent palettes remain unchanged.

Fonts are self-hosted WOFF2 assets in `static/fonts/`, declared in
`assets/css/fonts.css`, and imported by the main CSS entry point:

- Body/UI: `"LINE Seed Sans", "LINE Seed Sans KR", "LINE Seed JP_TTF", sans-serif`,
  with a 16px base size and 1.65 line height.
- Code: `"D2Coding ligature", monospace`, with a 14px size and 1.45 line height.
- Each family ships Regular (400) and Bold (700). Requests for light (300) and
  medium (500) map to 400; semibold (600) maps to 700 through Tailwind theme
  weight variables. No additional weights are downloaded.
- Font faces use `font-display: swap`. No external font CDN or OS font
  installation is required. Japanese and code fonts load only when needed.
- The eight web fonts are lossless WOFF2 conversions of the LINE Seed
  Regular/Bold TTF files and the two D2Coding ligature faces from the reference
  project's TTC collection. Glyphs and font metadata are retained, without
  subsetting. Conversion used FontTools' WOFF2 support (`font.flavor = "woff2"`).
  Embedded copyright/trademark notices and the complete SIL Open Font License
  1.1 are bundled in `static/fonts/LICENSE.txt`.

For code highlighting, consuming sites must use class-based Hugo output:

```toml
[markup.highlight]
  noClasses = false
```

The example site already enables this setting. Chroma tokens, code-block
backgrounds, and prose/code text selection use the corresponding brand roles.

---

## Build Pipeline

### Development
```bash
npm run dev
# Builds CSS first, then runs Hugo and npm run css:watch concurrently.
# Stops the other process if either development process fails.
# Must be run from theme root (HUGO-LBRX-IO-THEME/)
# NOTE: Pagefind search index is NOT generated in dev mode.
```

### Production
```bash
npm run build
# Builds CSS first via the npm prebuild lifecycle hook.
# Runs: hugo --source exampleSite --themesDir=.. --theme=. --minify
# Then: pagefind --site exampleSite/public
# Outputs to: exampleSite/public/
# Pagefind index written to: exampleSite/public/pagefind/
```

These commands build the bundled example site. For a consuming Hugo site, build
the theme CSS with `npm run css:build`, then run Hugo from that site's root.
The example-site commands resolve this repository as the theme with
`--themesDir=.. --theme=.`, independently of the checkout directory's name or case.
`npm run css` owns the shared Tailwind CLI input/output arguments;
`css:build` and `css:watch` supply only the compilation mode. npm uses the
installed local CLI rather than downloading a missing executable through `npx`.

### CSS Regression Baseline

Run `npm run test:css` from the theme root. It compiles fresh CSS and uses the
Node.js built-in test runner and the existing PostCSS dependency to check
responsive grids, every safelisted utility, class-based dark mode, semantic brand colors,
local font assets and weight mapping, Typography, all twelve edition palettes, JavaScript-generated search
classes, and custom fiction/book-cover rules. Additional checks preserve arbitrary
shelf grid tracks, renamed utility geometry, accessible outlines, button cursors,
and Typography cascade ordering. The checks assert v4 declarations and CSS
variables rather than requiring byte-identical v3 output.

### Tailwind CSS v4 Configuration

Tailwind and `@tailwindcss/cli` use matching v4 releases. Node.js 20+ is required.
Supported browser minimums are Safari 16.4, Chrome 111, and Firefox 128; v3-era
browser compatibility is no longer supported.

| Area | Implementation |
|---|---|
| CLI | `@tailwindcss/cli` supplies the local `tailwindcss` binary used by the shared `css` command. |
| CSS entry point | `assets/css/main.css` imports Tailwind with `source(none)` and registers `@tailwindcss/typography` with `@plugin`. |
| Theme | `@theme` defines the local font stacks and Regular/Bold weight mapping; `@theme inline` exposes the semantic light/dark brand roles. There is no JavaScript Tailwind configuration. |
| Source detection | `@source "../../layouts"` and `@source "../js"` resolve relative to the CSS entry point, not the shell's working directory. Keep complete utility strings in templates and JavaScript. |
| Safelist | `@source inline()` retains every former JavaScript safelist entry, including responsive grid classes associated with Bug #195. |
| Dark mode | `@custom-variant dark (&:where(.dark, .dark *))` preserves the existing JavaScript-controlled `.dark` strategy. |
| Typography | `@utility prose` extends the plugin's base utility with the custom `70ch` width, font family, and semantic light/dark brand roles. Utility generation keeps `dark:prose-invert` and `max-w-none` later in the cascade. |
| PostCSS | The unused v3 `postcss.config.js` and Autoprefixer dependency are removed. PostCSS remains a development dependency for parsing compiled CSS in tests, not for the build pipeline. |
| Custom CSS | Chroma tokens, code typography, and fiction ornaments use brand role variables. Existing unlayered book-cover effects and fiction rules remain outside Tailwind's layers. |

Utility migrations preserve intended v3 sizing: `shadow-sm` becomes `shadow-xs`,
`rounded-sm` becomes `rounded-xs`, bare `rounded` becomes `rounded-sm`, and
`backdrop-blur-sm` becomes `backdrop-blur-xs`. Deprecated `flex-shrink-0` becomes
`shrink-0`. `outline-hidden` retains the previous invisible-outline accessibility
behavior. Shelf grid arbitrary values use underscores for track separators, such
as `grid-cols-[6rem_1fr]`, instead of commas.

Buttons retain a pointer cursor through a small base-layer rule. Hover variants
use v4's hover-capable-device behavior; the separate mobile navigation does not
depend on hover. Search and mobile menu scripts remove the `hidden` attribute
when opening, so the v4 hidden-attribute precedence remains compatible.

The framework's standard palette, spacing/divider selectors, and Preflight
otherwise follow v4 defaults. Browser-based visual acceptance should cover home,
shelf, editions, fiction, about, and search in light/dark mode at mobile and desktop
widths, including Safari and Firefox. Existing pipeline YAML requires explicit
approval before modification; this migration does not deploy the site.

Reference: [Tailwind CSS upgrade guide](https://tailwindcss.com/docs/upgrade-guide).

---

## Pagefind Integration

Pagefind is a static search library that indexes the built Hugo output.

### Indexing

- In the theme repository, `pagefind --site exampleSite/public` runs after the example-site Hugo build and writes the search index to `exampleSite/public/pagefind/`.
- Content templates use `data-pagefind-body` on the `<article>` element to mark indexable content.
- Header and footer partials use `data-pagefind-ignore` to exclude chrome from the index.
- Single layouts include `data-pagefind-meta` tags for `title`, `section`, and `language`.

### Search UI

- **Trigger:** `Cmd+K` (macOS) / `Ctrl+K` (Windows/Linux), or a search icon button in the nav.
- **Modal:** A fixed overlay styled with Tailwind, controlled through `hidden` and `aria-hidden`. Closes on `Esc` or click-outside.
- **JS (`search.js`):**
  1. Lazily imports `/pagefind/pagefind.js` on first modal open (avoids loading on every page).
  2. Debounces the search input (300 ms).
  3. Calls `pagefind.search(query)` and renders result cards (title, URL, excerpt) into `#search-results`.
- **Styling:** Fully Tailwind-styled with `dark:` variants. No Pagefind default CSS (`pagefind-ui.css`) is used.

> ⚠️ Pagefind does not work with `hugo server`. Run `npm run build` and serve the `exampleSite/public/` directory to test search locally.

The current JavaScript import is domain-root-relative. A site served only under
a URL subpath needs an adjusted Pagefind import path.

---

## Dark Mode

**Strategy:** Tailwind CSS `class` strategy.

| Priority | Source |
|---|---|
| 1st | `localStorage` value set by the toggle button |
| 2nd | `prefers-color-scheme` media query (system preference) |

**Implementation:**
- An inline script in `head.html` applies the stored/system preference before
  paint. `theme-toggle.js` loads with `defer` and handles the toggle button.
- Toggling adds or removes the `dark` class on `<html>`.
- The toggle button state is updated to reflect the current mode.

---

## i18n

Hugo's built-in i18n system is used.

| Setting | Value |
|---|---|
| Default language | `ko` (Korean) |
| Secondary language | `en` (English) |
| Example content directories | Korean: `content`; English: `content.en` |
| Translated pages | Matching relative paths across configured content directories |

Translation strings (nav labels, section headings, search placeholder, "no results" text, etc.) live in `i18n/ko.yaml` and `i18n/en.yaml`. Templates reference them via `{{ i18n "key" }}`.

---

## Key Design Decisions

| Decision | Choice | Why |
|---|---|---|
| Dark mode implementation | `class` strategy + JS | Full control; system pref as default; no flash |
| Search UI | Custom (Pagefind JS API) | Tailwind-compatible; avoids CSS conflicts with pagefind-ui.css |
| Search trigger | Cmd+K modal | Modern UX; doesn't interrupt reading flow |
| JS framework | None (Vanilla JS) | Small interaction scripts do not require a framework |
| CSS framework | Tailwind v4 | CSS-first theme and explicit source detection fit Hugo's template-centric workflow |
| i18n approach | Hugo built-in | Zero extra dependencies; separate language content directories in the example |
| Archetypes | Per section | Ensures correct front matter for each content type |
| RSS strategy | Hugo built-in feeds | Home and section feeds enabled through output configuration |
| Book grid breakpoints | `grid-cols-3 sm:grid-cols-4 lg:grid-cols-6` | Matches shelf grid for visual consistency across all book-display contexts |
| Edition accent palette | Dynamic class strings in `edition-palette.html` | Tailwind JIT detects full class strings; palette partial returns a dict |
| Fiction sub-navigation | Separate `/fiction/serials/` + `/fiction/standalone/` pages | Enables per-section pagination; Hugo `.Paginate` requires a list/section page, not a single page |
| Status badge style | Outline/border style for all 4 statuses | Visually distinct without heavy background fills; olive outline for `read` signals completion |
| Standalone stories in sub-folder | `content/fiction/standalone/` + `url` override | Required to enable `.Paginate` on the standalone section page while preserving clean `/fiction/slug/` URLs |

---

## RSS Feeds

Hugo auto-generates RSS at build time — no extra tooling required.

### Feed Endpoints

| URL | Content | Format |
|---|---|---|
| `/index.xml` | Default-language home feed | Hugo built-in RSS |
| `/shelf/index.xml` | Shelf section | Hugo built-in RSS |
| `/editions/index.xml` | Editions section | Hugo built-in RSS |
| `/fiction/index.xml` | Fiction section | Hugo built-in RSS |
| `/en/index.xml` | English home feed, when content exists | Hugo built-in RSS |

Language prefixes depend on the consuming site's multilingual configuration.
The example does not enable `defaultContentLanguageInSubdir`, so Korean is
served at the root rather than `/ko/`.

The About page is a leaf bundle (`about/index.md`); use `outputs: ["HTML"]`
to keep it HTML-only.

### Content Strategy

There is no custom `layouts/_default/rss.xml` in the theme. Feed item selection
and summaries follow the installed Hugo release's built-in RSS template.
Full-content fiction feeds and edition cover-image markup are not implemented
by a theme-specific RSS template.

### Implementation

**`exampleSite/hugo.toml`** `[outputs]` block:
```toml
[outputs]
  home    = ["HTML", "RSS"]
  section = ["HTML", "RSS"]
  page    = ["HTML"]
```

**`content/about/index.md`** front matter:
```yaml
outputs: ["HTML"]   # Disable RSS for About
```
