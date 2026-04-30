# Photo media pipeline

This document describes the local media workflow for photo albums. The goal is
to keep the Git repository small while still publishing optimized photo assets
to the production media host.

## Source of truth

Git stores site code, layouts, text, and lightweight metadata.

Git does not store generated photo binaries.

Original photos stay local, for example in `tmp/photos/<album>/` during current
work. Generated web variants are staged under `tmp/` by default and are synced
to the media server with `rsync`.

The production media root is:

```text
https://media.armum.eu/field-laboratory/photos/
```

The matching server path is:

```text
/srv/www/media/field-laboratory/photos/
```

## Script

Use:

```bash
python scripts/photo_media.py --album storm-2025-09-06 --source tmp/photos/burza
```

By default the script:

1. Reads supported image files from `--source`.
2. If `--manifest-output` is active, tries to pull the existing
   `manifest.json` from the media host.
3. Reads the existing manifest from `--manifest-output`, if that file exists.
4. Skips source files whose hash already exists in that manifest.
5. Generates resized variants for new images into
   `tmp/photo-media/<timestamp>/<album>/`.
6. Writes a merged `manifest.json` into the staging album directory.
7. Runs `rsync` to the media host.
8. If repository files were written, runs a local Hugo build, commits those
   files, and pushes to GitHub.

When `--write-index` is used, the script can also create the Hugo album page
after media sync succeeds. In that mode, if `--manifest-output` is not provided,
the repository manifest path defaults to:

```text
data/photos/<album>.json
```

and the album page path defaults to:

```text
content/photos/<album>/index.md
```

The default remote target is:

```text
deploy@armum.eu:/srv/www/media/field-laboratory/photos/<album>/
```

The script appends files. It does not pass `--delete` to `rsync`. Old files can
remain on the server and may be cleaned later by a separate orphan cleanup tool.

The manifest follows the same append model. Existing images are preserved, new
hashes are appended, and duplicate hashes are skipped.

When a local repository manifest is missing but media still exists on the
server, the remote `manifest.json` is used to restore the local manifest before
hash comparison. This lets an album be republished without regenerating images
whose original hashes are already present on the media host.

## Generated variants

The default variants are:

```text
320   thumbnail strip and small grid preview
1600  album grid, mobile, and fast lightbox preview
3840  full lightbox image for 4K screens and download target
```

The default output format is WebP:

```text
--format webp
```

The default per-size WebP quality is:

```text
--qualities 320:84,1600:90,3840:95
```

Use `--quality <value>` only when you intentionally want one quality for every
generated size.

Photo variants are generated with libvips through `pyvips`, not ImageMagick.
The default worker count is:

```text
--resize-workers 16
```

WebP uses effort `6` by default to reduce visible artifacts in dark, noisy
photo backgrounds.

Every configured size must have an explicit quality entry. The gallery expects
the exact `320`, `1600`, and `3840` variants; it does not fall back to older
`600`-pixel manifests.

JPEG is still available when needed:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --format jpg
```

## File names

Generated file names use the album date, the source-file sort order, and a
prefix of the SHA-256 hash of the original source file:

```text
20250906-0001.ca8236a31b.webp
20250906-0002.4d930e659e.webp
```

The date part comes from `--date` when provided, or from the current local date
when it is omitted. It does not come from EXIF or the source file name.

The sequence part comes from the source file order after sorting by file name.
When appending to an existing manifest, new images continue after the largest
existing sequence number. If old manifest entries do not yet have a sequence,
the script continues after the current manifest length.

The same file name is used in each size directory:

```text
320/20250906-0001.ca8236a31b.webp
1600/20250906-0001.ca8236a31b.webp
3840/20250906-0001.ca8236a31b.webp
```

This gives stable, cache-friendly URLs. If the source file changes, the hash
changes and the generated URL changes.

## Manifest

Each staging album contains:

```text
manifest.json
```

The manifest records:

- album slug,
- media base URL,
- generated sizes,
- output format,
- source hash prefixes,
- source-order sequence numbers,
- generated file names,
- width, height, and public URL for every variant.

The public manifest does not store original source file names. Older remote
manifests may still contain `source` fields from earlier pipeline versions, but
the script removes them when writing a new local or synced manifest.

The manifest is also synced to the media host. A later Hugo gallery layout can
copy or transform this metadata into versioned site data.

## Important ordering

Media sync must happen before committing and pushing the Hugo content that links
to the media files.

The script follows this order by default:

```text
1. Generate and rsync photo media.
2. Update local Hugo content or manifests.
3. Run a local Hugo build.
4. Commit only the generated album files.
5. Push to GitHub.
```

This prevents GitHub Actions from deploying HTML that points to missing media.

Use `--no-publish` to stop after writing local files without committing or
pushing. If new images are generated with `--skip-rsync`, publishing is refused
unless `--no-publish` is also passed.

Use `--skip-remote-manifest` only when you intentionally do not want to read
the media-host manifest before processing sources.

## Useful commands

Generate and sync with defaults:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza
```

This syncs media, but does not create a gallery page unless `--write-index` or
`--manifest-output` is used. With no repository files to commit, the publish
step is a no-op.

Generate and sync without committing or pushing:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --no-publish
```

Skip the media-host manifest lookup:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --write-index \
  --skip-remote-manifest
```

Generate only, without `rsync`:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --skip-rsync \
  --no-publish
```

Run `rsync` as a dry run:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --dry-run-rsync
```

Remove the staging album after a successful non-dry-run sync:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --cleanup-after-sync
```

Use a custom staging directory:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --staging-root tmp/photo-media-verification \
  --resize-workers 8
```

Write an extra manifest copy into the repository:
This is the normal mode for gallery publishing because the Hugo gallery reads
the lightweight manifest from Git.

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --manifest-output data/photos/storm-2025-09-06.json
```

If `data/photos/storm-2025-09-06.json` already exists, the script reads it
first. Images whose source hash is already present are not regenerated. New
images are added to the end of the manifest. When changing the size set for an
existing album, regenerate from a clean manifest and sync the new media before
publishing the Hugo data.

Create a full gallery entry in one run:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --write-index \
  --title "Burza 2025-09-06" \
  --date 2025-09-06 \
  --description "Nocne zdjęcia burzy." \
  --tags storm,night,best \
  --body "Krótki album z nocnej obserwacji burzy."
```

This is the normal publishing command. It syncs media first, writes
`data/photos/storm-2025-09-06.json` and
`content/photos/storm-2025-09-06/index.md`, runs `hugo`, commits those files,
and pushes to GitHub.

Use a custom commit message:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --write-index \
  --title "Burza 2025-09-06" \
  --commit-message "Add storm photo album"
```

The generated front matter contains the album metadata used by the gallery:

```yaml
---
title: "Burza 2025-09-06"
date: 2025-09-06
description: "Nocne zdjęcia burzy."
manifest: "storm-2025-09-06"
cover_hash: "..."
tags:
  - "storm"
  - "night"
  - "best"
---
```

`--date` accepts a plain Hugo date such as `2025-09-06`. If omitted, the script
uses the current local date. It does not read EXIF dates by default.

Use `--cover-hash` when selecting a specific album cover:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --write-index \
  --cover-hash ca8236a31b
```

`--cover-source` is legacy-only and works only with older manifests that still
store original source file names:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --write-index \
  --cover-source 20250906_030919_000_35561485.jpg
```

In both cases the generated index stores only `cover_hash`.

If `index.md` already exists, the script leaves it untouched by default. This
protects manual body text and per-photo metadata. Use `--overwrite-index` only
when replacing that file is intentional.

## Local testing

The production-like local test uses the real media host:

1. Run the script and sync media to `media.armum.eu`.
2. Generate or update the Hugo album page or manifest.
3. Run `hugo server`.
4. Open the local Hugo page and let the browser load media from
   `https://media.armum.eu/...`.

This matches production behavior and avoids keeping generated media in Git.

## Dependencies

The script expects these commands to be available:

```text
magick
identify
rsync
ssh
hugo
git
```

`magick` and `identify` come from ImageMagick. `rsync` uses the local SSH
configuration. Locally, no explicit `-i` key argument is required if
`deploy@armum.eu` already works via SSH config or agent.
