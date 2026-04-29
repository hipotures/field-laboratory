import PhotoSwipeLightbox from '/vendor/photoswipe/photoswipe-lightbox.esm.min.js';

const gallery = document.querySelector('.photo-gallery');

function revealThumbnail(strip, thumbnail) {
  if (!thumbnail) {
    return;
  }

  const stripRect = strip.getBoundingClientRect();
  const thumbnailRect = thumbnail.getBoundingClientRect();

  if (thumbnailRect.left >= stripRect.left && thumbnailRect.right <= stripRect.right) {
    return;
  }

  const centeredOffset = thumbnail.offsetLeft - ((strip.clientWidth - thumbnail.offsetWidth) / 2);
  strip.scrollLeft = Math.max(0, centeredOffset);
}

if (gallery) {
  const lightbox = new PhotoSwipeLightbox({
    gallery: '.photo-gallery',
    children: 'a.photo-gallery-link',
    pswpModule: () => import('/vendor/photoswipe/photoswipe.esm.min.js'),
    mainClass: 'field-photo-lightbox',
    bgOpacity: 1,
    paddingFn: (viewportSize) => ({
      top: viewportSize.y < 720 ? 48 : 72,
      bottom: viewportSize.y < 720 ? 96 : 126,
      left: viewportSize.x < 760 ? 12 : 28,
      right: viewportSize.x < 760 ? 12 : 28
    }),
    imageClickAction: 'zoom-or-close',
    tapAction: 'toggle-controls',
    wheelToZoom: true
  });

  lightbox.on('uiRegister', () => {
    lightbox.pswp.ui.registerElement({
      name: 'download-button',
      order: 8,
      isButton: true,
      tagName: 'a',
      html: {
        isCustomSVG: true,
        inner: '<path d="M20.5 14.3 17.1 18V10h-2.2v7.9l-3.4-3.6L10 16l6 6.1 6-6.1ZM23 23H9v2h14Z" id="pswp__icn-download"/>',
        outlineID: 'pswp__icn-download'
      },
      onInit: (el, pswp) => {
        el.setAttribute('download', '');
        el.setAttribute('target', '_blank');
        el.setAttribute('rel', 'noopener');

        pswp.on('change', () => {
          const currentElement = pswp.currSlide.data.element;
          el.href = currentElement?.dataset.downloadUrl || pswp.currSlide.data.src;
        });
      }
    });

    lightbox.pswp.ui.registerElement({
      name: 'theme-button',
      ariaLabel: 'Zmień motyw',
      order: 9,
      isButton: true,
      html: '<i class="fa-solid fa-adjust fa-fw" aria-hidden="true"></i>',
      onClick: () => {
        document.getElementById('dark-mode-toggle')?.click();
      }
    });

    lightbox.pswp.ui.registerElement({
      name: 'custom-caption',
      order: 11,
      isButton: false,
      appendTo: 'root',
      html: '',
      onInit: (el, pswp) => {
        pswp.on('change', () => {
          const currentElement = pswp.currSlide.data.element;
          const caption = currentElement?.dataset.caption || currentElement?.querySelector('img')?.getAttribute('alt') || '';
          el.textContent = caption;
          el.hidden = !caption;
        });
      }
    });

    lightbox.pswp.ui.registerElement({
      name: 'thumbnail-strip',
      className: 'pswp__thumbnail-strip',
      appendTo: 'root',
      onInit: (el, pswp) => {
        const links = Array.from(gallery.querySelectorAll('a.photo-gallery-link'));
        const buttons = links.map((link, index) => {
          const button = document.createElement('button');
          const img = link.querySelector('img');
          button.type = 'button';
          button.className = 'pswp__thumbnail-button';
          button.setAttribute('aria-label', `Pokaż zdjęcie ${index + 1}`);
          button.style.backgroundImage = `url("${link.dataset.thumbSrc || img?.src || link.href}")`;
          button.addEventListener('click', () => pswp.goTo(index));
          el.appendChild(button);
          return button;
        });

        pswp.on('change', () => {
          buttons.forEach((button, index) => {
            button.classList.toggle('is-active', index === pswp.currIndex);
          });
          revealThumbnail(el, buttons[pswp.currIndex]);
        });
      }
    });
  });

  lightbox.init();
}
