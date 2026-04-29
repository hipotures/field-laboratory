import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
