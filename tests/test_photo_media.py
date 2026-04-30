import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import photo_media


def test_variants(name: str = "image.webp") -> dict[str, dict[str, object]]:
    return {
        "320": {"file": name, "width": 320, "height": 213, "url": f"https://example.com/320/{name}"},
        "1600": {"file": name, "width": 1600, "height": 1067, "url": f"https://example.com/1600/{name}"},
        "3840": {"file": name, "width": 3840, "height": 2560, "url": f"https://example.com/3840/{name}"},
    }


class PhotoMediaTests(unittest.TestCase):
    def test_default_variants_and_qualities_are_explicit(self):
        self.assertEqual(photo_media.DEFAULT_SIZES, [320, 1600, 3840])
        self.assertEqual(photo_media.DEFAULT_QUALITIES, {320: 84, 1600: 90, 3840: 95})
        self.assertEqual(photo_media.DEFAULT_WEBP_EFFORT, 6)

    def test_parse_size_qualities_requires_every_requested_size(self):
        self.assertEqual(
            photo_media.parse_size_qualities("320:84,1600:90,3840:95", [320, 1600, 3840]),
            {320: 84, 1600: 90, 3840: 95},
        )

        with self.assertRaisesRegex(ValueError, "Missing quality"):
            photo_media.parse_size_qualities("320:78,1600:82", [320, 1600, 3840])

        with self.assertRaisesRegex(ValueError, "Quality configured for unused size"):
            photo_media.parse_size_qualities("320:78,1600:82,3840:84,600:86", [320, 1600, 3840])

    def test_uniform_quality_override_applies_to_all_sizes(self):
        self.assertEqual(
            photo_media.build_quality_map(sizes=[320, 1600, 3840], quality=80, qualities="320:78"),
            {320: 80, 1600: 80, 3840: 80},
        )

    def test_sequenced_output_name_uses_album_date_sequence_and_hash(self):
        name = photo_media.sequenced_output_name(
            album_date_prefix="20250325",
            sequence=7,
            source_hash="99ba39bd",
            image_format="jpg",
        )

        self.assertEqual(name, "20250325-0007.99ba39bd.jpg")

    def test_album_plan_uses_size_directories_and_same_name_for_each_size(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "IMG_0001.jpg"
            source.write_bytes(b"image bytes")
            staging = root / "stage"

            plan = photo_media.build_album_plan(
                album="storm-2025-09-06",
                sources=[source],
                staging_root=staging,
                sizes=[600, 1600],
                image_format="jpg",
                hash_chars=8,
                album_date_prefix="20250906",
                sequence_start=3,
            )

        self.assertEqual(plan.album_dir, staging / "storm-2025-09-06")
        self.assertEqual(len(plan.items), 1)
        item = plan.items[0]
        self.assertEqual(item.sequence, 3)
        self.assertEqual(item.outputs[600], staging / "storm-2025-09-06" / "600" / "20250906-0003.de703023.jpg")
        self.assertEqual(item.outputs[1600], staging / "storm-2025-09-06" / "1600" / "20250906-0003.de703023.jpg")

    def test_build_manifest_does_not_publish_source_filenames(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "private original name.jpg"
            source.write_bytes(b"image bytes")
            staging = root / "stage"
            plan = photo_media.build_album_plan(
                album="storm",
                sources=[source],
                staging_root=staging,
                sizes=[600],
                image_format="webp",
                hash_chars=8,
                album_date_prefix="20250906",
                sequence_start=1,
            )
            item = plan.items[0]
            generated = {item.outputs[600]: (600, 400)}

            manifest = photo_media.build_manifest(plan, generated, "https://media.example/photos")

        self.assertNotIn("source", manifest["images"][0])
        self.assertEqual(manifest["images"][0]["sequence"], 1)
        self.assertEqual(manifest["images"][0]["name"], "20250906-0001.de703023.webp")

    def test_generate_album_variants_uses_size_specific_quality_and_worker_count(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "source.jpg"
            source.write_bytes(b"image bytes")
            staging = root / "stage"
            plan = photo_media.build_album_plan(
                album="storm",
                sources=[source],
                staging_root=staging,
                sizes=[320, 1600],
                image_format="webp",
                hash_chars=8,
                album_date_prefix="20250906",
                sequence_start=1,
            )
            calls = []

            def fake_generate(source_path: Path, destination: Path, size: int, quality: int) -> tuple[int, int]:
                calls.append((source_path, destination, size, quality))
                return size, size // 2

            with mock.patch.object(photo_media, "generate_variant", fake_generate):
                generated = photo_media.generate_album_variants(
                    plan,
                    qualities={320: 78, 1600: 82},
                    resize_workers=2,
                )

        self.assertEqual(
            sorted((size, quality) for _, _, size, quality in calls),
            [(320, 78), (1600, 82)],
        )
        self.assertEqual(generated[plan.items[0].outputs[320]], (320, 160))
        self.assertEqual(generated[plan.items[0].outputs[1600]], (1600, 800))

    def test_album_date_prefix_accepts_date_and_datetime(self):
        self.assertEqual(photo_media.album_date_prefix("2025-03-25"), "20250325")
        self.assertEqual(photo_media.album_date_prefix("2025-03-25T18:23:08+01:00"), "20250325")
        self.assertEqual(photo_media.album_date_prefix("2025:03:25"), "20250325")

    def test_next_sequence_uses_existing_sequence_or_image_count(self):
        self.assertEqual(
            photo_media.next_sequence({"images": [{"sequence": 4}, {"sequence": 9}]}),
            10,
        )
        self.assertEqual(
            photo_media.next_sequence({"images": [{"hash": "old"}, {"hash": "older"}]}),
            3,
        )

    def test_public_manifest_removes_legacy_source_and_backfills_sequence(self):
        manifest = {
            "images": [
                {"source": "private-name.jpg", "hash": "oldhash", "name": "old.webp"},
                {"source": "other-private-name.jpg", "hash": "newhash", "sequence": 8, "name": "new.webp"},
            ]
        }

        public = photo_media.public_manifest(manifest)

        self.assertNotIn("source", public["images"][0])
        self.assertNotIn("source", public["images"][1])
        self.assertEqual(public["images"][0]["sequence"], 1)
        self.assertEqual(public["images"][1]["sequence"], 8)

    def test_existing_manifest_must_include_every_requested_size(self):
        manifest = {
            "images": [
                {
                    "hash": "oldhash",
                    "variants": {
                        "600": {"url": "https://example.com/old-600.webp"},
                        "1600": {"url": "https://example.com/old-1600.webp"},
                    },
                }
            ]
        }

        with self.assertRaisesRegex(ValueError, "missing variants"):
            photo_media.validate_manifest_variants(manifest, [320, 1600, 3840])

    def test_rsync_command_appends_album_without_delete_by_default(self):
        command = photo_media.build_rsync_command(
            album_dir=Path("/tmp/stage/storm"),
            remote_base="deploy@armum.eu:/srv/www/media/field-laboratory/photos",
            dry_run=False,
        )

        self.assertEqual(
            command,
            [
                "rsync",
                "-az",
                "--progress",
                "/tmp/stage/storm/",
                "deploy@armum.eu:/srv/www/media/field-laboratory/photos/storm/",
            ],
        )
        self.assertNotIn("--delete", command)

    def test_rsync_command_can_dry_run_without_deleting_remote_files(self):
        command = photo_media.build_rsync_command(
            album_dir=Path("/tmp/stage/storm"),
            remote_base="deploy@armum.eu:/srv/www/media/field-laboratory/photos/",
            dry_run=True,
        )

        self.assertIn("-n", command)
        self.assertNotIn("--delete", command)

    def test_remote_manifest_command_reads_album_manifest_without_delete(self):
        command = photo_media.build_remote_manifest_command(
            album="storm",
            remote_base="deploy@armum.eu:/srv/www/media/field-laboratory/photos/",
            destination=Path("/tmp/storm.json"),
        )

        self.assertEqual(
            command,
            [
                "rsync",
                "-az",
                "deploy@armum.eu:/srv/www/media/field-laboratory/photos/storm/manifest.json",
                "/tmp/storm.json",
            ],
        )
        self.assertNotIn("--delete", command)

    def test_sources_with_hashes_already_in_manifest_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            old_source = root / "old.jpg"
            new_source = root / "new.jpg"
            old_source.write_bytes(b"old image")
            new_source.write_bytes(b"new image")
            existing = {
                "images": [
                    {
                        "source": "old.jpg",
                        "hash": photo_media.file_hash(old_source, 8),
                        "name": "old.existing.webp",
                        "variants": test_variants(),
                    }
                ]
            }

            remaining = photo_media.filter_new_sources(
                [old_source, new_source],
                existing,
                hash_chars=8,
            )

        self.assertEqual(remaining, [new_source])

    def test_merge_manifest_keeps_old_images_and_appends_new_images(self):
        existing = {
            "album": "storm",
            "images": [
                {
                    "source": "old.jpg",
                    "hash": "oldhash",
                    "name": "old.oldhash.webp",
                    "variants": {"600": {"url": "https://example.com/old.webp"}},
                }
            ],
        }
        new = {
            "album": "storm",
            "images": [
                {
                    "source": "new.jpg",
                    "hash": "newhash",
                    "name": "new.newhash.webp",
                    "variants": {"600": {"url": "https://example.com/new.webp"}},
                }
            ],
            "sizes": [600, 1600],
            "format": "webp",
        }

        merged = photo_media.merge_manifest(existing, new)

        self.assertEqual([item["hash"] for item in merged["images"]], ["oldhash", "newhash"])
        self.assertEqual(merged["sizes"], [600, 1600])
        self.assertEqual(merged["format"], "webp")

    def test_render_album_index_includes_gallery_metadata_and_album_tags(self):
        content = photo_media.render_album_index(
            title="Burza 2025-09-06",
            date="2025-09-06",
            description="Nocne zdjęcia burzy.",
            manifest="storm-2025-09-06",
            cover_hash="85e0ae2ac1",
            tags=["storm", "night", "best"],
            body="Krótki album z nocnej obserwacji burzy.",
        )

        self.assertEqual(
            content,
            """---\n"""
            """title: "Burza 2025-09-06"\n"""
            """date: 2025-09-06\n"""
            """description: "Nocne zdjęcia burzy."\n"""
            """manifest: "storm-2025-09-06"\n"""
            """cover_hash: "85e0ae2ac1"\n"""
            """tags:\n"""
            """  - "storm"\n"""
            """  - "night"\n"""
            """  - "best"\n"""
            """---\n"""
            """\n"""
            """Krótki album z nocnej obserwacji burzy.\n""",
        )

    def test_album_index_creation_does_not_overwrite_existing_file_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            index_path = Path(tmpdir) / "content" / "photos" / "storm" / "index.md"
            index_path.parent.mkdir(parents=True)
            index_path.write_text("manual content\n", encoding="utf-8")

            written = photo_media.write_album_index(
                path=index_path,
                content="generated content\n",
                overwrite=False,
            )

            self.assertFalse(written)
            self.assertEqual(index_path.read_text(encoding="utf-8"), "manual content\n")

    def test_select_cover_hash_uses_cover_source_or_first_manifest_image(self):
        manifest = {
            "images": [
                {"source": "first.jpg", "hash": "firsthash"},
                {"source": "selected.jpg", "hash": "selectedhash"},
            ]
        }

        self.assertEqual(
            photo_media.select_cover_hash(manifest, cover_source="selected.jpg", cover_hash=None),
            "selectedhash",
        )
        self.assertEqual(
            photo_media.select_cover_hash(manifest, cover_source=None, cover_hash=None),
            "firsthash",
        )

    def test_main_can_create_index_from_existing_manifest_without_regenerating_images(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "source"
            source_dir.mkdir()
            source = source_dir / "first.jpg"
            source.write_bytes(b"existing image")
            source_hash = photo_media.file_hash(source, 10)
            manifest_path = root / "data" / "photos" / "storm.json"
            photo_media.write_manifest(
                manifest_path,
                {
                    "album": "storm",
                    "images": [
                        {
                            "source": "first.jpg",
                            "hash": source_hash,
                            "name": f"first.{source_hash}.webp",
                            "variants": test_variants(),
                        }
                    ],
                },
            )
            index_path = root / "content" / "photos" / "storm" / "index.md"

            argv = [
                "photo_media.py",
                "--album",
                "storm",
                "--source",
                str(source_dir),
                "--manifest-output",
                str(manifest_path),
                "--index-output",
                str(index_path),
                "--title",
                "Storm",
                "--date",
                "2025-09-06",
                "--tags",
                "storm,best",
                "--body",
                "Storm album.",
                "--no-publish",
                "--skip-remote-manifest",
            ]
            with mock.patch("sys.argv", argv):
                result = photo_media.main()

            self.assertEqual(result, 0)
            content = index_path.read_text(encoding="utf-8")
            self.assertIn('manifest: "storm"', content)
            self.assertIn(f'cover_hash: "{source_hash}"', content)
            self.assertIn('  - "storm"', content)
            self.assertIn('  - "best"', content)

    def test_main_uses_remote_manifest_when_local_manifest_is_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "source"
            source_dir.mkdir()
            source = source_dir / "first.jpg"
            source.write_bytes(b"existing image")
            source_hash = photo_media.file_hash(source, 10)
            remote_manifest = {
                "album": "storm",
                "images": [
                    {
                        "source": "first.jpg",
                        "hash": source_hash,
                        "name": f"first.{source_hash}.webp",
                        "variants": test_variants(),
                    }
                ],
            }
            manifest_path = root / "data" / "photos" / "storm.json"
            index_path = root / "content" / "photos" / "storm" / "index.md"

            def fake_fetch(*, album: str, remote_base: str, destination: Path) -> bool:
                self.assertEqual(album, "storm")
                photo_media.write_manifest(destination, remote_manifest)
                return True

            argv = [
                "photo_media.py",
                "--album",
                "storm",
                "--source",
                str(source_dir),
                "--manifest-output",
                str(manifest_path),
                "--index-output",
                str(index_path),
                "--title",
                "Storm",
                "--no-publish",
            ]
            with mock.patch("sys.argv", argv), mock.patch.object(photo_media, "fetch_remote_manifest", fake_fetch):
                with mock.patch.object(photo_media, "generate_variant") as generate:
                    result = photo_media.main()

            self.assertEqual(result, 0)
            generate.assert_not_called()
            self.assertEqual(photo_media.read_manifest(manifest_path), photo_media.public_manifest(remote_manifest))
            self.assertTrue(index_path.exists())

    def test_main_publishes_repo_changes_by_default_after_index_generation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "source"
            source_dir.mkdir()
            source = source_dir / "first.jpg"
            source.write_bytes(b"existing image")
            source_hash = photo_media.file_hash(source, 10)
            manifest_path = root / "data" / "photos" / "storm.json"
            photo_media.write_manifest(
                manifest_path,
                {
                    "album": "storm",
                    "images": [
                        {
                            "source": "first.jpg",
                            "hash": source_hash,
                            "name": f"first.{source_hash}.webp",
                            "variants": test_variants(),
                        }
                    ],
                },
            )
            index_path = root / "content" / "photos" / "storm" / "index.md"

            argv = [
                "photo_media.py",
                "--album",
                "storm",
                "--source",
                str(source_dir),
                "--manifest-output",
                str(manifest_path),
                "--index-output",
                str(index_path),
                "--title",
                "Storm",
                "--skip-remote-manifest",
            ]
            with mock.patch("sys.argv", argv), mock.patch.object(photo_media, "publish_repo_changes") as publish:
                result = photo_media.main()

            self.assertEqual(result, 0)
            publish.assert_called_once()
            _, kwargs = publish.call_args
            self.assertEqual(kwargs["paths"], [manifest_path, index_path])
            self.assertEqual(kwargs["commit_message"], "Publish storm photo album")

    def test_main_can_skip_github_publication(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "source"
            source_dir.mkdir()
            source = source_dir / "first.jpg"
            source.write_bytes(b"existing image")
            source_hash = photo_media.file_hash(source, 10)
            manifest_path = root / "data" / "photos" / "storm.json"
            photo_media.write_manifest(
                manifest_path,
                {
                    "album": "storm",
                    "images": [
                        {
                            "source": "first.jpg",
                            "hash": source_hash,
                            "name": f"first.{source_hash}.webp",
                            "variants": test_variants(),
                        }
                    ],
                },
            )
            index_path = root / "content" / "photos" / "storm" / "index.md"

            argv = [
                "photo_media.py",
                "--album",
                "storm",
                "--source",
                str(source_dir),
                "--manifest-output",
                str(manifest_path),
                "--index-output",
                str(index_path),
                "--title",
                "Storm",
                "--no-publish",
                "--skip-remote-manifest",
            ]
            with mock.patch("sys.argv", argv), mock.patch.object(photo_media, "publish_repo_changes") as publish:
                result = photo_media.main()

            self.assertEqual(result, 0)
            publish.assert_not_called()

    def test_main_refuses_publish_when_new_images_are_not_synced(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "source"
            source_dir.mkdir()
            (source_dir / "first.jpg").write_bytes(b"new image")
            manifest_path = root / "data" / "photos" / "storm.json"

            argv = [
                "photo_media.py",
                "--album",
                "storm",
                "--source",
                str(source_dir),
                "--manifest-output",
                str(manifest_path),
                "--skip-rsync",
                "--skip-remote-manifest",
            ]
            with mock.patch("sys.argv", argv):
                with self.assertRaisesRegex(ValueError, "Refusing to publish"):
                    photo_media.main()


if __name__ == "__main__":
    unittest.main()
