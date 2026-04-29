import PhotoSwipeLightbox from '/vendor/photoswipe/photoswipe-lightbox.esm.min.js';

const gallery = document.querySelector('.photo-gallery');
const thumbnailSizeStorageKey = 'field-photo-lightbox-thumbnail-size';
let largeThumbnails = readThumbnailSizePreference();
const photoswipeControlLabels = {
  '.pswp__button--close': 'labelClose',
  '.pswp__button--zoom': 'labelZoom',
  '.pswp__button--arrow--prev': 'labelPrevious',
  '.pswp__button--arrow--next': 'labelNext'
};

function readThumbnailSizePreference() {
  try {
    return window.localStorage?.getItem(thumbnailSizeStorageKey) === 'large';
  } catch {
    return false;
  }
}

function writeThumbnailSizePreference(isLarge) {
  try {
    window.localStorage?.setItem(thumbnailSizeStorageKey, isLarge ? 'large' : 'small');
  } catch {
    // Local storage can be unavailable in private or restricted contexts.
  }
}

function applyThumbnailSize(pswp, button) {
  pswp?.element?.classList.toggle('field-photo-lightbox--large-thumbnails', largeThumbnails);
  if (button) {
    const icon = button.querySelector('i');
    const label = largeThumbnails ? gallery.dataset.labelThumbnailSmall : gallery.dataset.labelThumbnailLarge;
    button.classList.toggle('is-large', largeThumbnails);
    button.setAttribute('aria-label', label);
    button.setAttribute('title', label);
    icon?.classList.toggle('fa-th', !largeThumbnails);
    icon?.classList.toggle('fa-th-large', largeThumbnails);
  }
}

function applyPhotoswipeLabels(pswp) {
  Object.entries(photoswipeControlLabels).forEach(([selector, labelKey]) => {
    const element = pswp.element?.querySelector(selector);
    if (!element) {
      return;
    }
    const label = gallery.dataset[labelKey];
    element.setAttribute('aria-label', label);
    element.setAttribute('title', label);
  });
}

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

function normalizeIndex(index, total) {
  if (index < 0) {
    return total - 1;
  }
  if (index >= total) {
    return 0;
  }
  return index;
}

function setActiveThumbnail(buttons, strip, index) {
  buttons.forEach((button, buttonIndex) => {
    button.classList.toggle('is-active', buttonIndex === index);
  });
  revealThumbnail(strip, buttons[index]);
}

if (gallery) {
  const lightbox = new PhotoSwipeLightbox({
    gallery: '.photo-gallery',
    children: 'a.photo-gallery-link',
    pswpModule: () => import('/vendor/photoswipe/photoswipe.esm.min.js'),
    mainClass: 'field-photo-lightbox',
    showHideAnimationType: 'zoom',
    spacing: 0.5,
    bgOpacity: 1,
    paddingFn: (viewportSize) => ({
      top: viewportSize.y < 720 ? 48 : 72,
      bottom: largeThumbnails
        ? (viewportSize.y < 720 ? 148 : 188)
        : (viewportSize.y < 720 ? 96 : 126),
      left: viewportSize.x < 760 ? 12 : 28,
      right: viewportSize.x < 760 ? 12 : 28
    }),
    imageClickAction: 'zoom-or-close',
    tapAction: 'toggle-controls',
    arrowKeys: false,
    wheelToZoom: true,
    errorMsg: gallery.dataset.labelLoadError
  });

  lightbox.on('uiRegister', () => {
    lightbox.pswp.ui.registerElement({
      name: 'download-button',
      order: 8,
      isButton: true,
      tagName: 'a',
      ariaLabel: gallery.dataset.labelDownload,
      html: {
        isCustomSVG: true,
        inner: '<path d="M20.5 14.3 17.1 18V10h-2.2v7.9l-3.4-3.6L10 16l6 6.1 6-6.1ZM23 23H9v2h14Z" id="pswp__icn-download"/>',
        outlineID: 'pswp__icn-download'
      },
      onInit: (el, pswp) => {
        el.setAttribute('download', '');
        el.setAttribute('target', '_blank');
        el.setAttribute('rel', 'noopener');
        el.setAttribute('title', gallery.dataset.labelDownload);

        pswp.on('change', () => {
          const currentElement = pswp.currSlide.data.element;
          el.href = currentElement?.dataset.downloadUrl || pswp.currSlide.data.src;
        });
      }
    });

    lightbox.pswp.ui.registerElement({
      name: 'theme-button',
      ariaLabel: gallery.dataset.labelTheme,
      order: 9,
      isButton: true,
      html: '<i class="fa-solid fa-adjust fa-fw" aria-hidden="true"></i>',
      onClick: () => {
        document.getElementById('dark-mode-toggle')?.click();
      }
    });

    lightbox.pswp.ui.registerElement({
      name: 'thumbnail-size-button',
      ariaLabel: gallery.dataset.labelThumbnailLarge,
      order: 10,
      isButton: true,
      html: '<i class="fa-solid fa-th fa-fw" aria-hidden="true"></i>',
      onInit: (el, pswp) => {
        applyThumbnailSize(pswp, el);
      },
      onClick: (_event, el) => {
        const pswp = lightbox.pswp;
        if (!pswp) {
          return;
        }
        largeThumbnails = !largeThumbnails;
        writeThumbnailSizePreference(largeThumbnails);
        applyThumbnailSize(pswp, el);
        pswp.updateSize(true);
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
        let previewIndex = null;
        const links = Array.from(gallery.querySelectorAll('a.photo-gallery-link'));
        const buttons = links.map((link, index) => {
          const button = document.createElement('button');
          const img = link.querySelector('img');
          button.type = 'button';
          button.className = 'pswp__thumbnail-button';
          button.setAttribute('aria-label', `${gallery.dataset.labelThumbnailItem} ${index + 1}`);
          button.style.backgroundImage = `url("${link.dataset.thumbSrc || img?.src || link.href}")`;
          button.addEventListener('click', () => {
            previewIndex = null;
            pswp.goTo(index);
          });
          el.appendChild(button);
          return button;
        });

        lightbox.on('keydown', ({ originalEvent }) => {
          if (originalEvent.key !== 'ArrowRight' && originalEvent.key !== 'ArrowLeft') {
            return;
          }
          if (originalEvent.altKey || originalEvent.ctrlKey || originalEvent.metaKey || originalEvent.shiftKey) {
            return;
          }

          originalEvent.preventDefault();
          const direction = originalEvent.key === 'ArrowRight' ? 1 : -1;
          const baseIndex = previewIndex ?? pswp.currIndex;
          previewIndex = normalizeIndex(baseIndex + direction, pswp.getNumItems());
          setActiveThumbnail(buttons, el, previewIndex);
        });

        pswp.events.add(document, 'keyup', (event) => {
          if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') {
            return;
          }
          if (previewIndex === null) {
            return;
          }

          event.preventDefault();
          const targetIndex = previewIndex;
          previewIndex = null;
          pswp.goTo(targetIndex);
        });

        pswp.on('change', () => {
          if (previewIndex === null) {
            setActiveThumbnail(buttons, el, pswp.currIndex);
          }
        });
      }
    });

    lightbox.pswp.on('afterInit', () => {
      applyPhotoswipeLabels(lightbox.pswp);
    });
  });

  lightbox.init();
}
