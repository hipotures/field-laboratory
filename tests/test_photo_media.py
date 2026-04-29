import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import photo_media


class PhotoMediaTests(unittest.TestCase):
    def test_hashed_output_name_uses_source_hash_and_normalized_stem(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "Storm Frame 01.JPG"
            source.write_bytes(b"unique image bytes")

            name = photo_media.hashed_output_name(source, "jpg", hash_chars=8)

        self.assertEqual(name, "storm-frame-01.99ba39bd.jpg")

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
            )

        self.assertEqual(plan.album_dir, staging / "storm-2025-09-06")
        self.assertEqual(len(plan.items), 1)
        item = plan.items[0]
        self.assertEqual(item.outputs[600], staging / "storm-2025-09-06" / "600" / "img-0001.de703023.jpg")
        self.assertEqual(item.outputs[1600], staging / "storm-2025-09-06" / "1600" / "img-0001.de703023.jpg")

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
                        "variants": {},
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
                            "variants": {},
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
            ]
            with mock.patch("sys.argv", argv):
                result = photo_media.main()

            self.assertEqual(result, 0)
            content = index_path.read_text(encoding="utf-8")
            self.assertIn('manifest: "storm"', content)
            self.assertIn(f'cover_hash: "{source_hash}"', content)
            self.assertIn('  - "storm"', content)
            self.assertIn('  - "best"', content)


if __name__ == "__main__":
    unittest.main()
