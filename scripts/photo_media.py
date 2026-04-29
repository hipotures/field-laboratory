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
    parser.add_argument("--skip-rsync", action="store_true", help="Generate files only.")
    parser.add_argument("--dry-run-rsync", action="store_true", help="Run rsync with -n.")
    parser.add_argument(
        "--cleanup-after-sync",
        action="store_true",
        help="Remove staging directory after successful non-dry-run rsync.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sizes = parse_sizes(args.sizes)
    staging_root = args.staging_root or default_staging_root()
    sources = list_sources(args.source)
    if not sources:
        raise ValueError(f"No supported image files found in {args.source}")

    plan = build_album_plan(
        album=args.album,
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

    manifest = build_manifest(plan, generated, args.media_base_url)
    staging_manifest = plan.album_dir / "manifest.json"
    write_manifest(staging_manifest, manifest)
    print(f"manifest: {staging_manifest}")

    if args.manifest_output:
        write_manifest(args.manifest_output, manifest)
        print(f"manifest copy: {args.manifest_output}")

    if not args.skip_rsync:
        command = build_rsync_command(plan.album_dir, args.remote_base, args.dry_run_rsync)
        print("rsync:", " ".join(command))
        sync_album(plan.album_dir, args.remote_base, args.dry_run_rsync)

    if args.cleanup_after_sync and not args.skip_rsync and not args.dry_run_rsync:
        shutil.rmtree(plan.album_dir)
        print(f"removed staging album: {plan.album_dir}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
