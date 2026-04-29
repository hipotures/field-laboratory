#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}
DEFAULT_REMOTE_BASE = "deploy@armum.eu:/srv/www/media/field-laboratory/photos"
DEFAULT_MEDIA_BASE_URL = "https://media.armum.eu/field-laboratory/photos"


@dataclass(frozen=True)
class PlannedImage:
    source: Path
    output_name: str
    source_hash: str
    outputs: dict[int, Path]


@dataclass(frozen=True)
class AlbumPlan:
    album: str
    album_dir: Path
    items: list[PlannedImage]
    sizes: list[int]
    image_format: str


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "image"


def file_hash(path: Path, chars: int) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:chars]


def normalize_format(value: str) -> str:
    value = value.lower().strip().lstrip(".")
    if value in {"jpeg", "jpg"}:
        return "jpg"
    if value == "webp":
        return "webp"
    raise ValueError(f"Unsupported output format: {value}")


def hashed_output_name(source: Path, image_format: str, hash_chars: int = 10) -> str:
    output_format = normalize_format(image_format)
    source_hash = file_hash(source, hash_chars)
    return f"{slugify(source.stem)}.{source_hash}.{output_format}"


def parse_sizes(value: str) -> list[int]:
    sizes: list[int] = []
    for raw in value.split(","):
        raw = raw.strip()
        if not raw:
            continue
        size = int(raw)
        if size <= 0:
            raise ValueError(f"Image size must be positive: {size}")
        sizes.append(size)
    if not sizes:
        raise ValueError("At least one image size is required")
    return sorted(dict.fromkeys(sizes))


def list_sources(source_dir: Path) -> list[Path]:
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_dir}")
    sources = [
        path
        for path in source_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(sources, key=lambda path: path.name.lower())


def build_album_plan(
    *,
    album: str,
    sources: list[Path],
    staging_root: Path,
    sizes: list[int],
    image_format: str,
    hash_chars: int,
) -> AlbumPlan:
    album_slug = slugify(album)
    output_format = normalize_format(image_format)
    album_dir = staging_root / album_slug
    items: list[PlannedImage] = []
    for source in sources:
        source_hash = file_hash(source, hash_chars)
        output_name = f"{slugify(source.stem)}.{source_hash}.{output_format}"
        outputs = {size: album_dir / str(size) / output_name for size in sizes}
        items.append(
            PlannedImage(
                source=source,
                output_name=output_name,
                source_hash=source_hash,
                outputs=outputs,
            )
        )
    return AlbumPlan(
        album=album_slug,
        album_dir=album_dir,
        items=items,
        sizes=sizes,
        image_format=output_format,
    )


def default_staging_root() -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return Path("tmp") / "photo-media" / stamp


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True)


def image_dimensions(path: Path) -> tuple[int, int]:
    result = subprocess.run(
        ["identify", "-format", "%w %h", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width_raw, height_raw = result.stdout.strip().split()
    return int(width_raw), int(height_raw)


def generate_variant(source: Path, destination: Path, size: int, quality: int) -> tuple[int, int]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "magick",
        str(source),
        "-auto-orient",
        "-resize",
        f"{size}x{size}>",
        "-strip",
        "-quality",
        str(quality),
        str(destination),
    ]
    run_command(command)
    return image_dimensions(destination)


def build_manifest(
    plan: AlbumPlan,
    generated: dict[Path, tuple[int, int]],
    media_base_url: str,
) -> dict[str, object]:
    media_base_url = media_base_url.rstrip("/")
    images: list[dict[str, object]] = []
    for item in plan.items:
        variants: dict[str, object] = {}
        for size, path in item.outputs.items():
            width, height = generated[path]
            variants[str(size)] = {
                "file": item.output_name,
                "width": width,
                "height": height,
                "url": f"{media_base_url}/{plan.album}/{size}/{item.output_name}",
            }
        images.append(
            {
                "source": item.source.name,
                "hash": item.source_hash,
                "name": item.output_name,
                "variants": variants,
            }
        )
    return {
        "album": plan.album,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "media_base_url": media_base_url,
        "sizes": plan.sizes,
        "format": plan.image_format,
        "images": images,
    }


def write_manifest(path: Path, manifest: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_manifest(path: Path | None) -> dict[str, object]:
    if path is None or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Manifest root must be an object: {path}")
    return data


def manifest_hashes(manifest: dict[str, object]) -> set[str]:
    hashes: set[str] = set()
    images = manifest.get("images", [])
    if not isinstance(images, list):
        return hashes
    for image in images:
        if not isinstance(image, dict):
            continue
        value = image.get("hash")
        if isinstance(value, str) and value:
            hashes.add(value)
    return hashes


def filter_new_sources(
    sources: list[Path],
    existing_manifest: dict[str, object],
    hash_chars: int,
) -> list[Path]:
    known_hashes = manifest_hashes(existing_manifest)
    return [source for source in sources if file_hash(source, hash_chars) not in known_hashes]


def merge_manifest(existing: dict[str, object], new: dict[str, object]) -> dict[str, object]:
    merged = dict(existing)
    known_hashes = manifest_hashes(existing)
    images: list[object] = []
    existing_images = existing.get("images", [])
    if isinstance(existing_images, list):
        images.extend(existing_images)
    new_images = new.get("images", [])
    if isinstance(new_images, list):
        for image in new_images:
            if not isinstance(image, dict):
                continue
            image_hash = image.get("hash")
            if isinstance(image_hash, str) and image_hash in known_hashes:
                continue
            images.append(image)
            if isinstance(image_hash, str):
                known_hashes.add(image_hash)
    merged.update(new)
    merged["images"] = images
    return merged


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def parse_tags(value: str | None) -> list[str]:
    if not value:
        return []
    tags: list[str] = []
    seen: set[str] = set()
    for raw in value.split(","):
        tag = raw.strip()
        if not tag or tag in seen:
            continue
        tags.append(tag)
        seen.add(tag)
    return tags


def read_body(args: argparse.Namespace) -> str:
    if args.body and args.body_file:
        raise ValueError("Use either --body or --body-file, not both")
    if args.body_file:
        return args.body_file.read_text(encoding="utf-8").strip()
    return (args.body or "").strip()


def default_index_output(album: str) -> Path:
    return Path("content") / "photos" / slugify(album) / "index.md"


def default_manifest_output(album: str) -> Path:
    return Path("data") / "photos" / f"{slugify(album)}.json"


def select_cover_hash(
    manifest: dict[str, object],
    *,
    cover_source: str | None,
    cover_hash: str | None,
) -> str | None:
    if cover_hash:
        return cover_hash
    images = manifest.get("images", [])
    if not isinstance(images, list):
        return None
    if cover_source:
        for image in images:
            if not isinstance(image, dict):
                continue
            if image.get("source") == cover_source:
                value = image.get("hash")
                return value if isinstance(value, str) else None
        raise ValueError(f"Cover source not found in manifest: {cover_source}")
    for image in images:
        if not isinstance(image, dict):
            continue
        value = image.get("hash")
        if isinstance(value, str) and value:
            return value
    return None


def render_album_index(
    *,
    title: str,
    date: str,
    description: str,
    manifest: str,
    cover_hash: str | None,
    tags: list[str],
    body: str,
) -> str:
    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        f"date: {date}",
    ]
    if description:
        lines.append(f"description: {yaml_quote(description)}")
    lines.append(f"manifest: {yaml_quote(manifest)}")
    if cover_hash:
        lines.append(f"cover_hash: {yaml_quote(cover_hash)}")
    if tags:
        lines.append("tags:")
        lines.extend(f"  - {yaml_quote(tag)}" for tag in tags)
    lines.extend(["---", ""])
    if body:
        lines.append(body)
    return "\n".join(lines).rstrip() + "\n"


def write_album_index(path: Path, content: str, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        print(f"index exists, not overwriting: {path}")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"index: {path}")
    return True


def default_commit_message(album: str) -> str:
    return f"Publish {slugify(album)} photo album"


def git_pathspec(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def publish_repo_changes(paths: list[Path], commit_message: str) -> bool:
    pathspecs = [git_pathspec(path) for path in dict.fromkeys(paths) if path.exists()]
    if not pathspecs:
        print("publish: no repository files to commit")
        return False

    run_command(["hugo", "--minify", "--gc", "--cleanDestinationDir"])
    run_command(["git", "add", *pathspecs])
    diff = subprocess.run(
        ["git", "diff", "--cached", "--quiet", "--", *pathspecs],
        check=False,
        text=True,
    )
    if diff.returncode == 0:
        print("publish: no repository changes to commit")
        return False
    if diff.returncode != 1:
        raise subprocess.CalledProcessError(diff.returncode, diff.args)

    run_command(["git", "commit", "-m", commit_message, "--", *pathspecs])
    run_command(["git", "push"])
    return True


def build_rsync_command(album_dir: Path, remote_base: str, dry_run: bool) -> list[str]:
    remote_base = remote_base.rstrip("/")
    remote_target = f"{remote_base}/{album_dir.name}/"
    command = ["rsync", "-az", "--progress"]
    if dry_run:
        command.append("-n")
    command.extend([f"{album_dir}/", remote_target])
    return command


def sync_album(album_dir: Path, remote_base: str, dry_run: bool) -> None:
    run_command(build_rsync_command(album_dir, remote_base, dry_run))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate hashed 600/1600 photo variants and sync them to the media host."
    )
    parser.add_argument("--album", required=True, help="Album slug, e.g. storm-2025-09-06.")
    parser.add_argument("--source", type=Path, required=True, help="Directory with original images.")
    parser.add_argument("--sizes", default="600,1600", help="Comma-separated square-fit sizes.")
    parser.add_argument("--format", default="webp", help="Output format: webp or jpg.")
    parser.add_argument("--quality", type=int, default=86)
    parser.add_argument("--hash-chars", type=int, default=10)
    parser.add_argument("--staging-root", type=Path, default=None)
    parser.add_argument("--remote-base", default=DEFAULT_REMOTE_BASE)
    parser.add_argument("--media-base-url", default=DEFAULT_MEDIA_BASE_URL)
    parser.add_argument("--manifest-output", type=Path, default=None)
    parser.add_argument(
        "--write-index",
        action="store_true",
        help="Create a Hugo photo album index.md after media sync succeeds.",
    )
    parser.add_argument(
        "--index-output",
        type=Path,
        default=None,
        help="Album index path. Defaults to content/photos/<album>/index.md when --write-index is used.",
    )
    parser.add_argument("--title", default=None, help="Album title for generated index.md.")
    parser.add_argument(
        "--date",
        default=None,
        help="Album date for generated index.md. Defaults to today's local date.",
    )
    parser.add_argument("--description", default="", help="Album description for generated index.md.")
    parser.add_argument("--tags", default=None, help="Comma-separated album tags for generated index.md.")
    parser.add_argument("--body", default="", help="Album body text for generated index.md.")
    parser.add_argument("--body-file", type=Path, default=None, help="Read album body text from a file.")
    parser.add_argument("--cover-source", default=None, help="Original source filename to use as album cover.")
    parser.add_argument("--cover-hash", default=None, help="Existing image hash to use as album cover.")
    parser.add_argument(
        "--overwrite-index",
        action="store_true",
        help="Overwrite an existing generated index.md.",
    )
    parser.add_argument("--skip-rsync", action="store_true", help="Generate files only.")
    parser.add_argument("--dry-run-rsync", action="store_true", help="Run rsync with -n.")
    parser.add_argument(
        "--cleanup-after-sync",
        action="store_true",
        help="Remove staging directory after successful non-dry-run rsync.",
    )
    parser.add_argument(
        "--no-publish",
        action="store_true",
        help="Do not commit and push generated Hugo files after a successful run.",
    )
    parser.add_argument(
        "--commit-message",
        default=None,
        help="Git commit message used when publishing. Defaults to 'Publish <album> photo album'.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sizes = parse_sizes(args.sizes)
    staging_root = args.staging_root or default_staging_root()
    album_slug = slugify(args.album)
    if args.index_output:
        args.write_index = True
    manifest_output = args.manifest_output
    if args.write_index and manifest_output is None:
        manifest_output = default_manifest_output(album_slug)
    body_text = read_body(args)

    existing_manifest = read_manifest(manifest_output)
    sources = filter_new_sources(
        list_sources(args.source),
        existing_manifest,
        args.hash_chars,
    )
    if not sources and not args.write_index:
        print("no new images to process")
        return 0
    if not sources and args.write_index and not existing_manifest:
        print("no new images to process")
        raise ValueError("Cannot create index.md without an existing manifest or new images")
    if sources and args.skip_rsync and not args.no_publish:
        raise ValueError("Refusing to publish new image metadata when --skip-rsync was used. Use --no-publish.")

    manifest = existing_manifest
    plan: AlbumPlan | None = None
    if sources:
        plan = build_album_plan(
            album=album_slug,
            sources=sources,
            staging_root=staging_root,
            sizes=sizes,
            image_format=args.format,
            hash_chars=args.hash_chars,
        )

        generated: dict[Path, tuple[int, int]] = {}
        for item in plan.items:
            for size, destination in item.outputs.items():
                print(f"generate {size}: {item.source} -> {destination}")
                generated[destination] = generate_variant(item.source, destination, size, args.quality)

        new_manifest = build_manifest(plan, generated, args.media_base_url)
        manifest = merge_manifest(existing_manifest, new_manifest)
        staging_manifest = plan.album_dir / "manifest.json"
        write_manifest(staging_manifest, manifest)
        print(f"manifest: {staging_manifest}")

    if plan and not args.skip_rsync:
        command = build_rsync_command(plan.album_dir, args.remote_base, args.dry_run_rsync)
        print("rsync:", " ".join(command))
        sync_album(plan.album_dir, args.remote_base, args.dry_run_rsync)

    can_write_repo_files = not args.dry_run_rsync
    repo_paths_to_publish: list[Path] = []
    index_output: Path | None = None
    index_content: str | None = None
    if can_write_repo_files and args.write_index:
        index_output = args.index_output or default_index_output(album_slug)
        title = args.title or album_slug.replace("-", " ").title()
        index_content = render_album_index(
            title=title,
            date=args.date or datetime.now().astimezone().date().isoformat(),
            description=args.description,
            manifest=album_slug,
            cover_hash=select_cover_hash(
                manifest,
                cover_source=args.cover_source,
                cover_hash=args.cover_hash,
            ),
            tags=parse_tags(args.tags),
            body=body_text,
        )

    if can_write_repo_files and manifest_output:
        write_manifest(manifest_output, manifest)
        print(f"manifest copy: {manifest_output}")
        repo_paths_to_publish.append(manifest_output)

    if index_output and index_content:
        write_album_index(index_output, index_content, args.overwrite_index)
        repo_paths_to_publish.append(index_output)

    if not args.no_publish and can_write_repo_files:
        publish_repo_changes(
            paths=repo_paths_to_publish,
            commit_message=args.commit_message or default_commit_message(album_slug),
        )

    if plan and args.cleanup_after_sync and not args.skip_rsync and not args.dry_run_rsync:
        shutil.rmtree(plan.album_dir)
        print(f"removed staging album: {plan.album_dir}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
