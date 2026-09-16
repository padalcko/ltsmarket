/* ==========================================================
   LTS MARKET
   main.js
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  /* ======================================================
     01. MOBILE MENU
     ====================================================== */

  const language = document.documentElement.lang.split("-")[0];
  const labels = ({
    pl: { open: "Otwórz menu", close: "Zamknij menu", pause: "Wstrzymaj slajdy", play: "Wznów slajdy" },
    en: { open: "Open menu", close: "Close menu", pause: "Pause slides", play: "Resume slides" },
    ru: { open: "Открыть меню", close: "Закрыть меню", pause: "Остановить слайды", play: "Продолжить слайды" },
  })[language] || { open: "Open menu", close: "Close menu", pause: "Pause slides", play: "Resume slides" };
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const menuToggle = document.querySelector(".menu-toggle");
  const mobileMenu = document.querySelector(".mobile-menu");

  if (menuToggle && mobileMenu) {
    const closeMenu = () => {
      mobileMenu.classList.remove("is-open");
      menuToggle.classList.remove("is-active");

      menuToggle.setAttribute("aria-expanded", "false");

      menuToggle.setAttribute("aria-label", labels.open);
    };

    menuToggle.addEventListener("click", () => {
      const isOpen = mobileMenu.classList.toggle("is-open");

      menuToggle.classList.toggle("is-active", isOpen);

      menuToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");

      menuToggle.setAttribute(
        "aria-label",
        isOpen ? labels.close : labels.open,
      );
    });

    mobileMenu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && mobileMenu.classList.contains("is-open")) {
        closeMenu();
        menuToggle.focus();
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 1180) {
        closeMenu();
      }
    });
  }

  /* ======================================================
     02. HERO SLIDER
     ====================================================== */

  const slider = document.querySelector("[data-product-slider]");

  if (slider) {
    const slides = Array.from(slider.querySelectorAll(".hero-product"));

    const prevButton = document.querySelector("[data-slider-prev]");

    const nextButton = document.querySelector("[data-slider-next]");

    const dots = Array.from(document.querySelectorAll(".slider-dot"));

    let currentIndex = 0;

    let autoplayTimer = null;

    const autoplayDelay = 5000;
    let pausedByUser = false;
    let hovered = false;
    let touching = false;
    const heroVisual = slider.closest(".hero-visual") || slider.parentElement;
    const pauseButton = document.querySelector("[data-slider-pause]");
    function syncPauseButton() {
      if (!pauseButton) return;
      pauseButton.textContent = pausedByUser ? labels.play : labels.pause;
      pauseButton.setAttribute("aria-pressed", String(pausedByUser));
    }
    if (pauseButton) {
      pauseButton.hidden = reducedMotion.matches;
      pauseButton.addEventListener("click", () => {
        pausedByUser = !pausedByUser;
        syncPauseButton();
        startAutoplay();
      });
      syncPauseButton();
    }
    reducedMotion.addEventListener("change", () => {
      if (pauseButton) pauseButton.hidden = reducedMotion.matches;
      startAutoplay();
    });

    function showSlide(index) {
      if (!slides.length) {
        return;
      }

      if (index < 0) {
        index = slides.length - 1;
      }

      if (index >= slides.length) {
        index = 0;
      }

      currentIndex = index;

      slides.forEach((slide, slideIndex) => {
        const isActive = slideIndex === currentIndex;

        slide.classList.toggle("active", isActive);

        slide.setAttribute("aria-hidden", isActive ? "false" : "true");
      });

      dots.forEach((dot, dotIndex) => {
        const isActive = dotIndex === currentIndex;

        dot.classList.toggle("active", isActive);

        dot.setAttribute("aria-current", isActive ? "true" : "false");
      });
    }

    function nextSlide() {
      showSlide(currentIndex + 1);
    }

    function previousSlide() {
      showSlide(currentIndex - 1);
    }

    function stopAutoplay() {
      if (autoplayTimer) {
        window.clearInterval(autoplayTimer);

        autoplayTimer = null;
      }
    }

    function startAutoplay() {
      stopAutoplay();

      if (pausedByUser || reducedMotion.matches || document.hidden || hovered || touching || heroVisual?.contains(document.activeElement)) return;
      autoplayTimer = window.setInterval(nextSlide, autoplayDelay);
    }

    function restartAutoplay() {
      stopAutoplay();
      startAutoplay();
    }

    if (nextButton) {
      nextButton.addEventListener("click", () => {
        nextSlide();
        restartAutoplay();
      });
    }

    if (prevButton) {
      prevButton.addEventListener("click", () => {
        previousSlide();
        restartAutoplay();
      });
    }

    dots.forEach((dot, index) => {
      dot.addEventListener("click", () => {
        showSlide(index);
        restartAutoplay();
      });
    });

    if (heroVisual) {
      heroVisual.addEventListener("mouseenter", () => { hovered = true; stopAutoplay(); });
      heroVisual.addEventListener("mouseleave", () => { hovered = false; startAutoplay(); });
      heroVisual.addEventListener("focusin", stopAutoplay);
      heroVisual.addEventListener("focusout", () => window.setTimeout(startAutoplay, 0));
    }

    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        stopAutoplay();
      } else {
        startAutoplay();
      }
    });

    let touchStartX = 0;
    let touchEndX = 0;

    const minSwipeDistance = 50;

    slider.addEventListener(
      "touchstart",
      (event) => {
        touching = true;
        touchStartX = event.changedTouches[0].screenX;

        stopAutoplay();
      },
      {
        passive: true,
      },
    );

    slider.addEventListener(
      "touchend",
      (event) => {
        touching = false;
        touchEndX = event.changedTouches[0].screenX;

        const distance = touchEndX - touchStartX;

        if (Math.abs(distance) >= minSwipeDistance) {
          if (distance < 0) {
            nextSlide();
          } else {
            previousSlide();
          }
        }

        startAutoplay();
      },
      {
        passive: true,
      },
    );

    slider.addEventListener("touchcancel", () => { touching = false; startAutoplay(); }, { passive: true });
    showSlide(0);

    startAutoplay();
  }

  /* ======================================================
     03. SMOOTH SCROLL
     ====================================================== */

  const anchorLinks = document.querySelectorAll('a[href^="#"]');

  anchorLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      const href = link.getAttribute("href");

      if (!href || href === "#") {
        return;
      }

      let id;
      try { id = decodeURIComponent(href.slice(1)); } catch { return; }
      const target = document.getElementById(id);

      if (!target) {
        return;
      }

      event.preventDefault();

      target.scrollIntoView({
        behavior: reducedMotion.matches ? "auto" : "smooth",
        block: "start",
      });
    });
  });

  /* ======================================================
     04. HEADER SCROLL
     ====================================================== */

  const header = document.querySelector(".site-header");

  function updateHeaderState() {
    if (!header) {
      return;
    }

    header.classList.toggle("is-scrolled", window.scrollY > 20);
  }

  updateHeaderState();

  window.addEventListener("scroll", updateHeaderState, {
    passive: true,
  });
});
