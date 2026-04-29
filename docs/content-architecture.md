# Field Laboratory content architecture

This document records the content model for the Hugo site so future changes do
not blur the difference between writing, projects, topics, images, and search.

## Navigation

The top navigation should stay small and content-oriented:

- `Teksty` links to `/posts/`.
- `Projekty` links to `/projects/`.
- `Zdjecia` is reserved for future photo galleries and is currently disabled.
- `Tematy` is reserved for taxonomy indexes and is currently disabled.
- `Szukaj` is reserved for future search and is currently disabled.

Do not add individual interests such as photography, astronomy, AI, poetry, or
Linux to the top navigation. Those belong in taxonomies.

## Content sections

Use these top-level content directories:

- `content/posts/` for essays, notes, technical writing, and other text posts.
- `content/projects/` for project pages generated from local CV/project data.
- `content/photos/` in the future for standalone photo galleries.

`posts` can contain both long essays and short notes. The distinction between a
finished essay and a working note should be expressed with tags/topics, not with
another top-level navigation item.

## Taxonomies

Hugo handles taxonomies natively. Keep taxonomies as the discovery layer below
the main sections.

Current taxonomy configuration:

```toml
[taxonomies]
  category = "categories"
  series = "series"
  tag = "tags"
  author = "authors"
```

Planned addition:

```toml
topic = "topics"
```

Use taxonomy fields like this:

- `tags`: specific labels, for example `llm`, `linux`, `hugo`, `gcp`,
  `fotografia`.
- `topics`: broad areas, for example `AI`, `Systemy`, `Fotografia`,
  `Astronomia`, `Eseje`, `Notatki`.
- `series`: ordered groups of related posts, for example `vibe-coding`.
- `categories`: coarse legacy grouping only if needed.

The homepage may show a manually curated small set of topics. It should not
render every tag. A full tag/topic index can live under `/tags/` and later
`/topics/`.

## Images in posts

Posts should use Hugo page bundles:

```text
content/posts/post-slug/
  index.md
  photos/
    001.jpg
  images/
    chart.png
  diagrams/
    pipeline.svg
```

Use directories by meaning:

- `photos/` for real photos that may appear in photo browsing.
- `images/` for charts, tables, screenshots, UI captures, generated report
  images, and article images.
- `diagrams/` for diagrams and architecture drawings.

Every bundle that contains images intended for future filtering should declare
resource metadata in frontmatter.

Example:

```yaml
resources:
  - src: "photos/*"
    params:
      gallery: true
      kind: photo

  - src: "images/*"
    params:
      gallery: false
      kind: image

  - src: "diagrams/*"
    params:
      gallery: false
      kind: diagram
```

The default rule is strict:

```text
missing gallery: true = do not show in any global photo gallery
```

Future photo browsing must include only resources where:

```text
gallery: true
kind: photo
```

This prevents screenshots, charts, tables, and diagrams from appearing in photo
views just because they are image files.

## Standalone photo galleries

Future standalone galleries should live under `content/photos/` as page bundles
for album metadata and descriptions only:

```text
content/photos/gallery-slug/
  index.md
```

Generated photo binaries are not stored in Git. The photo media pipeline creates
600px and 1600px WebP variants locally, syncs them to `media.armum.eu`, and
records dimensions and URLs in a manifest. See `docs/photo-media-pipeline.md`.

The gallery page can use `layout: gallery` and a local layout that reads album
metadata or manifests and renders a grid consistent with the Coder theme.

Do not switch the whole site to a gallery theme. The site remains based on
`hugo-coder`; gallery behavior should be implemented with local layouts,
partials, or shortcodes.

## Search

Search is not designed yet.

The likely future direction is Pagefind: build Hugo first, then run Pagefind
against `public/`, and deploy both the generated site and the search index.

The important constraint is that search should index rendered content, not
become a second source of truth for tags, projects, or image metadata.

## Local theme overrides

Do not edit files under `themes/hugo-coder/` directly.

Site-specific changes belong in:

- `layouts/` for local layout and partial overrides.
- `assets/scss/custom.scss` for minimal CSS.
- `content/` for source content.
- `scripts/` for generators.
