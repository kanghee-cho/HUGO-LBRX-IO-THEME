# Theme Guide

`lbrx-io` is a Hugo theme for a literary site with a bookshelf, curated
editions, original fiction, and an About page. This guide covers installation,
configuration, content authoring, customization, and local verification.

## Documentation Map

| Document | Purpose |
|---|---|
| [Theme Guide](./THEME-GUIDE.md) | Start here to run or use the theme. |
| [Architecture](./ARCHITECTURE.md) | Template structure, brand tokens, font assets, CSS pipeline, search, and design decisions. |
| [Example configuration](../exampleSite/hugo.toml) | Complete bilingual configuration and navigation menus. |
| [Archetypes](../archetypes) | Front matter defaults for each content type. |

## 1. Prerequisites

- A current Hugo Extended release. Theme metadata declares `0.120.0` as the
  minimum; use a release that supports the example configuration's
  `[pagination]` table.
- Node.js 20 or newer and npm.
- Git.
- A browser compatible with Tailwind CSS v4: Safari 16.4+, Chrome 111+, or
  Firefox 128+.

## 2. Run the Bundled Example

Run these commands in PowerShell:

```powershell
git clone https://github.com/kanghee-cho/HUGO-LBRX-IO-THEME.git
Set-Location HUGO-LBRX-IO-THEME
npm ci
npm run dev
```

Open the local URL printed by Hugo. The development command builds CSS before
starting Hugo and the CSS watcher. The command resolves the theme explicitly,
so the checkout directory does not have to match the theme name.

The example includes demonstration content. Review and replace its site
parameters, social links, content, logos, and member information before using
it for your own site.

### Command Reference

Run these commands from the theme repository root:

| Command | Result |
|---|---|
| `npm run dev` | Build CSS, then run the example site's Hugo server and CSS watcher. |
| `npm run css:build` | Compile and minify CSS into `assets/css/main.min.css`. |
| `npm run css:watch` | Watch theme templates and JavaScript for CSS changes. |
| `npm run build` | Build CSS, generate the example site, then generate its Pagefind index. |
| `npm run test:css` | Build CSS and run the compiled CSS regression checks. |

`npm run build` writes to `exampleSite/public`. It is a local build, not a
deployment. Draft content is excluded by default. For draft preview, run
`npm run css:build`, then:

```powershell
hugo server --source exampleSite --themesDir=.. --theme=. --disableFastRender -D
```

## 3. Install in an Existing Hugo Site

From your Hugo site root:

```powershell
git submodule add https://github.com/kanghee-cho/HUGO-LBRX-IO-THEME.git themes\lbrx-io
git submodule update --init --recursive
Push-Location themes\lbrx-io
npm ci
npm run css:build
Pop-Location
```

Set `theme = "lbrx-io"` in the site's configuration. The directory name under
`themes` must match this value; the example configuration uses a different
theme name and should not be copied unchanged.

Compiled CSS is gitignored. Rebuild it after a fresh clone, dependency update,
or theme update. Installing the submodule alone does not generate CSS.

For development, run `hugo server -D` from the site root. If you edit theme
styles or templates, also run `npm run css:watch` from the theme directory in
a separate terminal.

### Production Build with Search

The repository's `npm run build` targets the bundled example, not your site.
For a consuming site, run the following from the site root:

```powershell
Push-Location themes\lbrx-io
npm run css:build
Pop-Location
hugo --minify
& .\themes\lbrx-io\node_modules\.bin\pagefind.cmd --site public
```

Use your configured output directory instead of `public` if you changed
Hugo's destination. Generate Pagefind only after a successful Hugo build.
Publish the generated search directory alongside the site's HTML and assets.

## 4. Configure the Site

Use the [example configuration](../exampleSite/hugo.toml) as a reference and
replace demonstration values. The following is a single-language baseline:

```toml
baseURL = "https://example.com/"
title = "My Literary Site"
theme = "lbrx-io"
defaultContentLanguage = "en"
disableKinds = ["taxonomy", "term"]

[pagination]
  pagerSize = 12

[params]
  nickname = "READER"
  description = "Books, editions, and fiction."
  author = "Editorial Team"

[outputs]
  home = ["HTML", "RSS"]
  section = ["HTML", "RSS"]
  page = ["HTML"]

[markup.highlight]
  noClasses = false

[markup.goldmark.renderer]
  unsafe = false

[[menus.main]]
  name = "Shelf"
  url = "/shelf/"
  weight = 1

[[menus.main]]
  name = "Editions"
  url = "/editions/"
  weight = 2

[[menus.main]]
  name = "Fiction"
  identifier = "fiction"
  url = "/fiction/"
  weight = 3

[[menus.main]]
  name = "Serials"
  parent = "fiction"
  url = "/fiction/serials/"
  weight = 1

[[menus.main]]
  name = "Standalone"
  parent = "fiction"
  url = "/fiction/standalone/"
  weight = 2

[[menus.main]]
  name = "About"
  url = "/about/"
  weight = 4
```

The current browser title uses `params.nickname` followed by `.LBRX.IO`;
changing `title` alone does not change that branded suffix.

Add footer social links using repeated `[[params.social]]` entries with `name`
and `url`. For bilingual sites, the example separates Korean content into
`content` and English content into `content.en`, with menus under
`languages.ko.menus` and `languages.en.menus`. Keep equivalent translated pages
at matching relative paths. UI translations are maintained in
[Korean](../i18n/ko.yaml) and [English](../i18n/en.yaml) translation files.

## 5. Organize Content

Recommended structure:

```text
content\
  about\
    index.md
  shelf\
    book-slug.md
  editions\
    edition-001.md
  fiction\
    _index.md
    serials\
      _index.md
    standalone\
      _index.md
      story-slug.md
    series-slug\
      _index.md
      episode-1.md
      episode-2.md
```

Run the following content commands from a consuming site's root. If working
on the bundled example instead, add `--source exampleSite --themesDir=..
--theme=.` to each `hugo new` command.

Archetypes create drafts. Complete the front matter and set `draft: false`
when a page is ready for publication.

### Shelf: Book Entries

```powershell
hugo new shelf\book-slug.md
```

The [shelf archetype](../archetypes/shelf.md) includes:

- Bibliographic information: `author`, `publisher`, `publish_year`, `isbn`,
  `pages`, `translator`, and `original_title`.
- Library information: `call_number`, `owned`, and `condition`.
- Reading information: `status`, `rating`, and `read_date`.
- Classification: `genre`, `mood_tags`, `recommended_for`, and `tags`.
- Presentation: `cover`, `description`, and optional `credited_to`.

Use `read`, `reading`, `wishlist`, or `abandoned` for `status`. Ratings support
half-star increments from `0.5` to `5.0`; the archetype's `0.0` represents an
unrated entry. Use `YYYY-MM-DD` for `read_date`.

### Editions: Curated Book Collections

```powershell
hugo new editions\edition-001.md
```

Set `edition_number`, `description`, and `accent_color`, then reference shelf
entries by slug:

```yaml
edition_number: 1
accent_color: "emerald"
books:
  - slug: book-slug
    reason: "A thoughtful introduction to the collection."
```

Create the referenced shelf entries before publishing the edition. Supported
accent palettes are `rose`, `pink`, `fuchsia`, `violet`, `indigo`, `sky`,
`cyan`, `teal`, `emerald`, `lime`, `amber`, and `orange`.

The Markdown body becomes the editor's note. The editions index displays the
current edition separately from the archive, which is paginated five per page.

### Fiction: Standalone Stories

```powershell
hugo new fiction\standalone\story-slug.md --kind fiction
```

Use `fiction_type: "standalone"`, plus `genre`, `description`, and `word_count`.
Optionally set `url: "/fiction/story-slug/"` to retain a shorter public URL.

Create the standalone section index with:

```yaml
---
title: "Standalone Stories"
layout: "fiction-standalone"
---
```

### Fiction: Serials and Episodes

```powershell
hugo new fiction\series-slug\_index.md --kind fiction-series
hugo new fiction\series-slug\episode-1.md --kind fiction-episode
```

The series index needs `fiction_type: "serial"` and `layout: "series"`.
Use `status: "ongoing"` or `status: "complete"`. Each episode needs its
ascending `episode` number; episode pages must be direct children of the
series directory.

Create `fiction/serials/_index.md` with `layout: "fiction-serials"` for the
serials listing. Keep the actual series directories directly under `fiction`,
as in the example. Create `fiction/_index.md` for the overview page.

Use a Markdown thematic break (`---`) in story bodies for the theme's
ornamental section separator. See [Fiction architecture](./ARCHITECTURE.md#fiction)
for preview counts and pagination behavior.

### About and Attribution

Create `about/index.md` with `type: "about"` and `outputs: ["HTML"]`.
Its Markdown body is the introduction; structured front matter controls
Space, Members, and Brand sections:

```yaml
---
title: "About"
type: "about"
outputs: ["HTML"]
space:
  ready: false
members:
  - id: "editor"
    name: "Editorial Team"
    photo: "members/editor.jpg"
    bio: "Stories and reading notes."
brand:
  logo_light: "brand/logo-light.svg"
  logo_dark: "brand/logo-dark.svg"
  colors:
    - name: "Pine"
      hex: "#246958"
      desc: "Primary accent"
  fonts:
    - role: "Body"
      name: "LINE Seed Sans"
      stack: '"LINE Seed Sans", sans-serif'
---
```

Put photos and logos in the site's `assets` directory. When `space.ready` is
true, optional `name`, `address`, `hours` entries (`day` and `time`), and
`map_embed` supply venue details.

Add `credited_to: "editor"` to a book, edition, or story to resolve the
display name and avatar from `members[].id`. Keep IDs stable when names
change. Member email addresses, if configured, are publicly displayed.

## 6. Customize Appearance

- **Brand colors:** Edit semantic `--brand-*` variables in
  [main CSS](../assets/css/main.css). Use semantic utilities such as
  `bg-brand-background` and `text-brand-accent` in templates.
- **Typography:** Font faces are declared in
  [font CSS](../assets/css/fonts.css), with self-hosted WOFF2 files in
  [font assets](../static/fonts). Preserve bundled license notices.
- **About branding:** Front matter controls displayed logos, swatches, and
  font descriptions; it does not automatically change the site's CSS tokens.
- **Favicons:** Override the theme's icon files and `site.webmanifest` in your
  site's `static` directory. Replace all icon sizes together.
- **Templates:** Put overrides at matching paths in your site's `layouts`
  directory. If an override introduces new Tailwind classes, register its
  source path in the CSS entry point and rebuild; the default source scanning
  covers theme layouts and theme JavaScript, not consuming-site files.

See [Brand Colors and Typography](./ARCHITECTURE.md#brand-colors-and-typography)
for the complete light/dark palette, font stacks, and supported weights.

## 7. Search, Dark Mode, and RSS

- **Search:** Open with `Ctrl+K` on Windows/Linux or `Cmd+K` on macOS.
  Pagefind requires generated HTML and its search index; the normal Hugo
  development server does not generate that index.
- **Local search verification:** Run `npm run build`, then serve
  `exampleSite/public` with a static HTTP server. Opening HTML through
  `file:` URLs is not a valid search test.
- **Subpath limitation:** Search currently imports
  `/pagefind/pagefind.js` from the domain root. Hosting the whole site only
  under a URL subpath requires adapting that import; favicon subpath support
  does not imply search subpath support.
- **Dark mode:** An explicit choice in `localStorage` takes priority over the
  system color-scheme preference. The `.dark` class drives Tailwind variants.
- **RSS:** Hugo's built-in RSS template generates feeds where `outputs`
  includes `RSS`. Typical endpoints include `/index.xml`,
  `/shelf/index.xml`, `/editions/index.xml`, and `/fiction/index.xml`.
  Language prefixes depend on the multilingual configuration. No custom
  full-content fiction RSS template is currently bundled.

## 8. Verification and Troubleshooting

| Symptom | Check |
|---|---|
| Site has no theme styling | Run `npm run css:build`; confirm `assets/css/main.min.css` exists. |
| Theme cannot be found | Match the configuration's `theme` to the consuming site's theme directory, or use the example command's explicit flags. |
| New page is missing | Check `draft`, publication dates, and whether draft preview is enabled. |
| Fiction sub-navigation is empty | Check section index layouts and the placement of series and standalone content. |
| Edition book is missing | Check the referenced shelf slug and whether that book is published. |
| Attribution shows an ID rather than a name | Match `credited_to` to an About member's stable `id`. |
| Custom Tailwind classes are absent | Register the override directory with `@source` and rebuild CSS. |
| Search index is not found | Build Hugo first, then Pagefind, and serve the generated directory over HTTP. |

Before accepting a theme customization:

1. Run `npm run test:css` for CSS or template class changes.
2. Run `npm run build` to verify Hugo and Pagefind output.
3. Inspect home, shelf, editions, fiction, About, and search in light/dark
   mode at desktop and mobile widths.
4. Verify links, translated navigation, images, attribution, and RSS feeds
   relevant to the changed content.

These are local checks only; they do not publish or deploy the site.
