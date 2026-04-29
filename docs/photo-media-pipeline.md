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
2. Reads the existing manifest from `--manifest-output`, if that file exists.
3. Skips source files whose hash already exists in that manifest.
4. Generates resized variants for new images into
   `tmp/photo-media/<timestamp>/<album>/`.
5. Writes a merged `manifest.json` into the staging album directory.
6. Runs `rsync` to the media host.

The default remote target is:

```text
deploy@armum.eu:/srv/www/media/field-laboratory/photos/<album>/
```

The script appends files. It does not pass `--delete` to `rsync`. Old files can
remain on the server and may be cleaned later by a separate orphan cleanup tool.

The manifest follows the same append model. Existing images are preserved, new
hashes are appended, and duplicate hashes are skipped.

## Generated variants

The default variants are:

```text
600   grid thumbnail
1600  PhotoSwipe image and download target
```

The default output format is WebP:

```text
--format webp
```

The default quality is:

```text
--quality 86
```

JPEG is still available when needed:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --format jpg
```

## File names

Every generated file name includes a prefix of the SHA-256 hash of the original
source file:

```text
20250906-013852-000-35126178.ca8236a31b.webp
```

The same file name is used in each size directory:

```text
600/20250906-013852-000-35126178.ca8236a31b.webp
1600/20250906-013852-000-35126178.ca8236a31b.webp
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
- source file names,
- source hash prefixes,
- generated file names,
- width, height, and public URL for every variant.

The manifest is also synced to the media host. A later Hugo gallery layout can
copy or transform this metadata into versioned site data.

## Important ordering

Media sync must happen before committing and pushing the Hugo content that links
to the media files.

Correct order:

```text
1. Generate and rsync photo media.
2. Verify media URLs.
3. Update local Hugo content or manifests.
4. Run a local Hugo build.
5. Commit and push the site.
```

This prevents GitHub Actions from deploying HTML that points to missing media.

## Useful commands

Generate and sync with defaults:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza
```

Generate only, without `rsync`:

```bash
python scripts/photo_media.py \
  --album storm-2025-09-06 \
  --source tmp/photos/burza \
  --skip-rsync
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
  --staging-root tmp/photo-media-verification
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
images are added to the end of the manifest.

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
```

`magick` and `identify` come from ImageMagick. `rsync` uses the local SSH
configuration. Locally, no explicit `-i` key argument is required if
`deploy@armum.eu` already works via SSH config or agent.
