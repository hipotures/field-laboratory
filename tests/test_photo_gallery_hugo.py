import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PhotoGalleryHugoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(
            ["hugo", "--destination", "public-test-gallery", "--cleanDestinationDir"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def read_public(self, relative_path: str) -> str:
        return (ROOT / "public-test-gallery" / relative_path).read_text(encoding="utf-8")

    def test_thumbnail_strip_does_not_smooth_scroll_on_slide_change(self):
        script = (ROOT / "static/js/photo-gallery.js").read_text(encoding="utf-8")

        self.assertNotIn("behavior: 'smooth'", script)
        self.assertIn("revealThumbnail", script)

    def test_arrow_key_hold_previews_thumbnails_before_loading_slide(self):
        script = (ROOT / "static/js/photo-gallery.js").read_text(encoding="utf-8")

        self.assertIn("arrowKeys: false", script)
        self.assertIn("lightbox.on('keydown'", script)
        self.assertIn("pswp.events.add(document, 'keyup'", script)
        self.assertIn("previewIndex", script)

    def test_photos_index_links_first_album_and_preserves_theme_toggle(self):
        html = self.read_public("photos/index.html")

        self.assertIn('href="/photos/storm-2025-09-06/"', html)
        self.assertIn("Burza 2025-09-06", html)
        self.assertIn('href="/photos/dwc/"', html)
        self.assertIn("DWC", html)
        self.assertIn("100 zdjęć", html)
        self.assertIn('id="dark-mode-toggle"', html)

    def test_dwc_album_page_renders_large_manifest(self):
        html = self.read_public("photos/dwc/index.html")

        self.assertIn('class="photo-gallery"', html)
        self.assertEqual(html.count('class="photo-gallery-link no-lightbox"'), 100)
        self.assertIn("https://media.armum.eu/field-laboratory/photos/dwc/600/", html)
        self.assertIn("https://media.armum.eu/field-laboratory/photos/dwc/1600/", html)

    def test_album_page_renders_manifest_gallery_for_photoswipe(self):
        html = self.read_public("photos/storm-2025-09-06/index.html")

        self.assertIn('class="photo-gallery"', html)
        self.assertIn('data-pswp-width="', html)
        self.assertIn('data-pswp-height="', html)
        self.assertIn('class="photo-gallery-link no-lightbox"', html)
        self.assertIn("https://media.armum.eu/field-laboratory/photos/storm-2025-09-06/600/", html)
        self.assertIn("https://media.armum.eu/field-laboratory/photos/storm-2025-09-06/1600/", html)
        self.assertIn('data-download-url="https://media.armum.eu/field-laboratory/photos/storm-2025-09-06/1600/', html)

    def test_album_page_loads_local_photoswipe_assets(self):
        html = self.read_public("photos/storm-2025-09-06/index.html")

        self.assertIn('href="/vendor/photoswipe/photoswipe.css"', html)
        self.assertIn('src="/js/photo-gallery.js"', html)


if __name__ == "__main__":
    unittest.main()
