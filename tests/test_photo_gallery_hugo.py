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

    def test_clicked_thumbnail_is_centered_in_strip(self):
        script = (ROOT / "static/js/photo-gallery.js").read_text(encoding="utf-8")

        self.assertIn("function centerThumbnail(strip, thumbnail", script)
        self.assertIn("centerThumbnail(el, button, 'smooth')", script)
        self.assertIn("behavior", script)
        self.assertIn("strip.scrollWidth - strip.clientWidth", script)

    def test_arrow_key_hold_previews_thumbnails_before_loading_slide(self):
        script = (ROOT / "static/js/photo-gallery.js").read_text(encoding="utf-8")

        self.assertIn("arrowKeys: false", script)
        self.assertIn("lightbox.on('keydown'", script)
        self.assertIn("pswp.events.add(document, 'keyup'", script)
        self.assertIn("previewIndex", script)

    def test_lightbox_uses_explicit_zoom_transition(self):
        script = (ROOT / "static/js/photo-gallery.js").read_text(encoding="utf-8")

        self.assertIn("showHideAnimationType: 'zoom'", script)
        self.assertIn("spacing: 0.5", script)

    def test_lightbox_has_thumbnail_size_toggle(self):
        script = (ROOT / "static/js/photo-gallery.js").read_text(encoding="utf-8")

        self.assertIn("thumbnail-size-button", script)
        self.assertIn("field-photo-lightbox--large-thumbnails", script)
        self.assertIn("labelThumbnailLarge", script)
        self.assertIn("fa-th", script)
        self.assertIn("fa-th-large", script)
        self.assertIn("const pswp = lightbox.pswp", script)
        self.assertIn("pswp.updateSize(true)", script)
        self.assertIn("centerActiveThumbnail", script)
        self.assertIn("activeThumbnail.offsetLeft", script)
        self.assertIn("querySelector('.pswp__thumbnail-strip')", script)

    def test_lightbox_ui_labels_come_from_hugo_i18n_data_attributes(self):
        script = (ROOT / "static/js/photo-gallery.js").read_text(encoding="utf-8")
        html = self.read_public("photos/storm-2025-09-06/index.html")

        self.assertIn("gallery.dataset.labelDownload", script)
        self.assertIn("gallery.dataset.labelLoadError", script)
        self.assertIn('data-label-download="Pobierz zdjęcie"', html)
        self.assertIn('data-label-thumbnail-large="Powiększ miniatury"', html)
        self.assertIn('data-label-load-error="Nie można wczytać zdjęcia"', html)
        self.assertNotIn("Pobierz zdjęcie", script)
        self.assertNotIn("Zamknij", script)
        self.assertNotIn("Powiększ miniatury", script)
        self.assertNotIn("The image cannot be loaded", script)

    def test_photos_index_links_first_album_and_preserves_theme_toggle(self):
        html = self.read_public("photos/index.html")

        self.assertIn('href="/photos/storm-2025-09-06/"', html)
        self.assertIn("Burza 2025-09-06", html)
        self.assertIn('href="/photos/dwc/"', html)
        self.assertIn("DWC", html)
        self.assertIn('id="dark-mode-toggle"', html)

    def test_album_page_does_not_generate_placeholder_alt_text(self):
        html = self.read_public("photos/storm-2025-09-06/index.html")

        self.assertNotIn("Zdjęcie z albumu", html)

    def test_album_page_renders_manifest_gallery_for_photoswipe(self):
        html = self.read_public("photos/storm-2025-09-06/index.html")

        self.assertIn('class="photo-gallery"', html)
        self.assertIn('data-pswp-width="', html)
        self.assertIn('data-pswp-height="', html)
        self.assertIn('class="photo-gallery-link no-lightbox"', html)
        self.assertIn("https://media.armum.eu/field-laboratory/photos/storm-2025-09-06/320/", html)
        self.assertIn("https://media.armum.eu/field-laboratory/photos/storm-2025-09-06/1600/", html)
        self.assertIn("https://media.armum.eu/field-laboratory/photos/storm-2025-09-06/3840/", html)
        self.assertIn('data-download-url="https://media.armum.eu/field-laboratory/photos/storm-2025-09-06/3840/', html)

    def test_lightbox_caption_does_not_fallback_to_alt_text(self):
        script = (ROOT / "static/js/photo-gallery.js").read_text(encoding="utf-8")

        self.assertIn("currentElement?.dataset.caption", script)
        self.assertNotIn("querySelector('img')?.getAttribute('alt')", script)

    def test_thumbnail_strip_has_theme_aware_framed_style(self):
        styles = (ROOT / "assets/scss/custom.scss").read_text(encoding="utf-8")

        self.assertIn("--photo-lightbox-strip-bg", styles)
        self.assertIn("--photo-lightbox-thumb-border", styles)
        self.assertIn("--photo-lightbox-thumb-active-border", styles)
        self.assertIn("--photo-lightbox-thumb-active-border: #0f62c9", styles)
        self.assertIn("--photo-lightbox-thumb-active-border: #67a8ff", styles)
        self.assertIn("--photo-lightbox-thumb-dim", styles)
        self.assertIn(".field-photo-lightbox .pswp__thumbnail-button::before", styles)
        self.assertIn("border-top: 1px solid var(--photo-lightbox-strip-border)", styles)
        self.assertIn("border: 2px solid var(--photo-lightbox-thumb-border)", styles)
        self.assertNotIn("opacity: 0.62", styles)

    def test_album_page_loads_local_photoswipe_assets(self):
        html = self.read_public("photos/storm-2025-09-06/index.html")

        self.assertIn('href="/vendor/photoswipe/photoswipe.css"', html)
        self.assertIn('src="/js/photo-gallery.js"', html)


if __name__ == "__main__":
    unittest.main()
