# Architecture

## Overview

`lbrx-io` is a custom Hugo theme for a literary personal brand site (LBRX.IO).  
It is built around four content sections with a Tailwind CSS build pipeline, Hugo Pipes for asset processing, Pagefind for static search, and Hugo's native i18n for bilingual (Korean/English) support.

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
│   │   ├── nav.html                  # Navigation links + search trigger button
│   │   ├── theme-toggle.html         # Dark/light toggle button
│   │   ├── search-modal.html         # Pagefind Cmd+K modal overlay
│   │   ├── book-card.html            # Reusable book card component
│   │   └── fiction-card.html         # Reusable fiction card component
│   ├── shelf/
│   │   ├── list.html                 # Bookshelf index page
│   │   └── single.html              # Single book entry (data-pagefind-body)
│   ├── Editions/
│   │   ├── list.html                 # Editions index page
│   │   └── single.html              # Single Edition entry (data-pagefind-body)
│   ├── fiction/
│   │   ├── list.html                 # Fiction index (stories + series)
│   │   └── single.html              # Single story or chapter (data-pagefind-body)
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
Personal bookshelf. Each entry represents one book with front matter fields for title, author, status (reading / finished / want-to-read), rating, cover image, and tags.

### Editions
Curated book Editions. Each entry is a content file listing selected books with short annotations. Editions can be organized by any theme or criteria (season, mood, topic, etc.).

### Fiction
Original creative writing. Supports both standalone short stories and multi-part series. Series use Hugo's page bundle convention: a directory with `_index.md` as the series root and numbered chapter files inside.

### About
A single-page section (`about/_index.md`). No list view. Mapped to `layouts/about/single.html`.

---

## Build Pipeline

### Development
```bash
npm run dev
# Runs: hugo server + Tailwind CSS watch (concurrently)
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
