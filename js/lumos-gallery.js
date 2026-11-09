(() => {
  const gallery = document.querySelector('.lumos-gallery');
  if (!gallery) return;
  const links = [...gallery.querySelectorAll('a')];
  const dialog = document.querySelector('.lumos-lightbox');
  const image = dialog.querySelector('img');
  let index = 0, origin, startX;
  function show(next) {
    index = (next + links.length) % links.length;
    const source = links[index].querySelector('img');
    image.removeAttribute('srcset');
    image.src = links[index].href;
    image.alt = source.alt;
    image.width = source.width; image.height = source.height;
    dialog.querySelector('figcaption').textContent = source.alt;
    dialog.querySelector('[data-count]').textContent = `${index + 1} / ${links.length}`;
  }
  links.forEach((link, i) => link.addEventListener('click', event => {
    event.preventDefault(); origin = link; show(i); dialog.showModal();
    document.documentElement.classList.add('lumos-modal-open');
  }));
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-prev]').addEventListener('click', () => show(index - 1));
  dialog.querySelector('[data-next]').addEventListener('click', () => show(index + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault(); show(index + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => {
    document.documentElement.classList.remove('lumos-modal-open'); origin?.focus();
  });
  image.addEventListener('touchstart', event => { startX = event.changedTouches[0].clientX; }, {passive:true});
  image.addEventListener('touchend', event => {
    const delta = event.changedTouches[0].clientX - startX;
    if (Math.abs(delta) > 45) show(index + (delta < 0 ? 1 : -1));
  }, {passive:true});
})();
