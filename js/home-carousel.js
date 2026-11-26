(() => {
  const carousel = document.querySelector('.home-page [data-carousel]');
  if (!carousel) return;

  const track = carousel.querySelector('.home-clients__track');
  const slides = [...track.children];
  const prev = carousel.querySelector('[data-prev]');
  const next = carousel.querySelector('[data-next]');
  const pause = carousel.querySelector('[data-pause]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0;
  let timer;
  let paused = false;
  let hovering = false;
  let focused = false;
  let touchStart = null;

  slides.slice(0, 4).forEach((slide) => {
    const clone = slide.cloneNode(true);
    clone.setAttribute('aria-hidden', 'true');
    clone.setAttribute('inert', '');
    track.append(clone);
  });

  const position = (animate = true) => {
    track.style.transition = animate && !reducedMotion.matches ? '' : 'none';
    track.style.transform = `translateX(-${track.children[index].offsetLeft - track.children[0].offsetLeft}px)`;
  };

  const stop = () => {
    window.clearInterval(timer);
    timer = undefined;
  };

  const start = () => {
    stop();
    if (!paused && !hovering && !focused && !reducedMotion.matches && !document.hidden) {
      timer = window.setInterval(() => move(1), 5000);
    }
  };

  const move = (step) => {
    if (index >= slides.length) index = 0;
    if (step < 0 && index === 0) {
      index = slides.length;
      position(false);
      // Force the reset to take effect before animating to the last image.
      track.getBoundingClientRect();
    }
    index += step;
    position();
    start();
  };

  track.addEventListener('transitionend', (event) => {
    if (event.propertyName !== 'transform' || index < slides.length) return;
    index = 0;
    position(false);
  });

  prev.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  pause.addEventListener('click', () => {
    paused = !paused;
    pause.setAttribute('aria-pressed', String(paused));
    pause.setAttribute('aria-label', pause.dataset[paused ? 'resumeLabel' : 'pauseLabel']);
    pause.textContent = paused ? '▶' : 'Ⅱ';
    start();
  });
  carousel.addEventListener('mouseenter', () => { hovering = true; stop(); });
  carousel.addEventListener('mouseleave', () => { hovering = false; start(); });
  carousel.addEventListener('focusin', () => { focused = true; stop(); });
  carousel.addEventListener('focusout', () => {
    window.requestAnimationFrame(() => {
      focused = carousel.contains(document.activeElement);
      start();
    });
  });
  carousel.addEventListener('touchstart', (event) => {
    touchStart = event.changedTouches[0].clientX;
    stop();
  }, { passive: true });
  carousel.addEventListener('touchend', (event) => {
    if (touchStart === null) return;
    const delta = event.changedTouches[0].clientX - touchStart;
    touchStart = null;
    if (Math.abs(delta) > 40) move(delta < 0 ? 1 : -1);
    else start();
  }, { passive: true });
  window.addEventListener('resize', () => position(false));
  document.addEventListener('visibilitychange', start);
  reducedMotion.addEventListener('change', () => { position(false); start(); });
  position(false);
  start();
})();
