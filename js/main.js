"use strict";

/* ============================================================
   LTS MARKET
   main.js
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
  /* ==========================================================
     01. ELEMENTS
     ========================================================== */

  const body = document.body;

  const siteHeader = document.getElementById("site-header");

  const menuToggle = document.getElementById("menu-toggle");
  const mobileMenu = document.getElementById("mobile-menu");

  const languageButton = document.getElementById("language-button");
  const languageMenu = document.getElementById("language-menu");

  const contactForm = document.getElementById("contact-form");
  const formStatus = document.getElementById("form-status");

  /* ==========================================================
     02. HOMEPAGE VISUAL FIX
     HERO ICONS + MARKET DIRECTIONS
     ========================================================== */

  const heroBenefitIcons = document.querySelectorAll(".hero-benefit__icon");

  const heroIcons = [
    `
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M12 3l7 3v5c0 4.8-2.9 8.1-7 10-4.1-1.9-7-5.2-7-10V6l7-3z"></path>
        <path d="M9 12l2 2 4-5"></path>
      </svg>
    `,
    `
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M14.7 6.3a4 4 0 0 1-5 5L4 17l3 3 5.7-5.7a4 4 0 0 0 5-5l-3 3-3-3 3-3z"></path>
      </svg>
    `,
    `
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <rect x="5" y="3" width="14" height="18" rx="1"></rect>
        <path d="M8 8h8"></path>
        <path d="M8 12h8"></path>
        <path d="M8 16h5"></path>
      </svg>
    `,
    `
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M3 7h11v10H3z"></path>
        <path d="M14 10h4l3 3v4h-7z"></path>
        <circle cx="7" cy="18" r="2"></circle>
        <circle cx="18" cy="18" r="2"></circle>
      </svg>
    `,
  ];

  heroBenefitIcons.forEach((icon, index) => {
    if (heroIcons[index]) {
      icon.innerHTML = heroIcons[index];
    }
  });

  /* ==========================================================
     03. HOMEPAGE GEOMETRY
     ========================================================== */

  const homepageVisualStyles = document.createElement("style");

  homepageVisualStyles.id = "homepage-visual-fixes";

  homepageVisualStyles.textContent = `
    /* HERO BENEFITS */

    .hero-benefit {
      display: grid;
      grid-template-columns: 44px minmax(0, 1fr);
      align-items: center;
      column-gap: 16px;
    }

    .hero-benefit__icon {
      display: flex;
      align-items: center;
      justify-content: center;

      flex: none;

      width: 44px;
      height: 44px;

      color: var(--color-blue);
    }

    .hero-benefit__icon svg {
      display: block;

      width: 32px;
      height: 32px;
      max-width: none;

      overflow: visible;

      fill: none;
      stroke: currentColor;
      stroke-width: 1.5;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    .hero-benefit__text {
      min-width: 0;
      line-height: 1.35;
    }


    /* MARKET DIRECTIONS */

    .direction-card {
      grid-template-columns:
        96px minmax(0, 1fr) 28px;

      align-items: center;

      gap: 20px;
    }

    .direction-card__visual {
      display: flex;
      align-items: center;
      justify-content: center;

      flex: none;

      width: 96px;
      height: 96px;

      overflow: hidden;

      background: #e9eef3;
    }

    .direction-card__visual img {
      display: block;

      width: 100%;
      height: 100%;

      object-fit: contain;
      object-position: center;

      transition: transform 260ms ease;
    }

    .direction-card:hover .direction-card__visual img {
      transform: scale(1.035);
    }

    .direction-card__visual--icon {
      color: var(--color-blue);
      background: #e9eef3;
    }

    .direction-card__visual--icon svg {
      display: block;

      width: 48px;
      height: 48px;
      max-width: none;

      overflow: visible;

      fill: none;
      stroke: currentColor;
      stroke-width: 1.35;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    .direction-card__content {
      min-width: 0;
    }

    .direction-card__arrow {
      display: flex;
      align-items: center;
      justify-content: center;

      width: 28px;
      height: 28px;
    }


    /* TABLET */

    @media (min-width: 640px) {
      .hero-benefit {
        grid-template-columns:
          44px minmax(0, 1fr);

        column-gap: 16px;
      }

      .direction-card {
        grid-template-columns:
          96px minmax(0, 1fr) 28px;

        gap: 22px;
      }

      .direction-card__visual {
        width: 96px;
        height: 96px;
      }
    }


    /* DESKTOP */

    @media (min-width: 1024px) {
      .hero-benefit {
        grid-template-columns:
          44px minmax(0, 1fr);

        column-gap: 16px;
      }

      .hero-benefit__icon {
        width: 44px;
        height: 44px;
      }

      .hero-benefit__icon svg {
        width: 32px;
        height: 32px;
      }

      .direction-card {
        grid-template-columns:
          96px minmax(0, 1fr) 28px;

        gap: 22px;
      }

      .direction-card__visual {
        width: 96px;
        height: 96px;
      }

      .direction-card__visual--icon svg {
        width: 48px;
        height: 48px;
      }
    }
  `;

  document.head.appendChild(homepageVisualStyles);

  /* ==========================================================
     04. LEASING ICON
     ========================================================== */

  const leasingDirectionIcon = document.querySelector(
    ".direction-card__visual--icon",
  );

  if (leasingDirectionIcon) {
    leasingDirectionIcon.innerHTML = `
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <rect x="10" y="5" width="28" height="38" rx="2"></rect>
        <path d="M16 15h16"></path>
        <path d="M16 22h16"></path>
        <path d="M16 29h10"></path>
        <path d="M30 35l3 3 6-7"></path>
      </svg>
    `;
  }

  /* ==========================================================
     05. HEADER ON SCROLL
     ========================================================== */

  const updateHeader = () => {
    if (!siteHeader) {
      return;
    }

    if (window.scrollY > 20) {
      siteHeader.classList.add("is-scrolled");
    } else {
      siteHeader.classList.remove("is-scrolled");
    }
  };

  updateHeader();

  window.addEventListener("scroll", updateHeader, {
    passive: true,
  });

  /* ==========================================================
     06. MOBILE MENU
     ========================================================== */

  const openMobileMenu = () => {
    if (!menuToggle || !mobileMenu) {
      return;
    }

    mobileMenu.hidden = false;

    menuToggle.classList.add("is-active");

    menuToggle.setAttribute("aria-expanded", "true");
    menuToggle.setAttribute("aria-label", "Zamknij menu");

    body.classList.add("menu-open");
  };

  const closeMobileMenu = () => {
    if (!menuToggle || !mobileMenu) {
      return;
    }

    mobileMenu.hidden = true;

    menuToggle.classList.remove("is-active");

    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Otwórz menu");

    body.classList.remove("menu-open");
  };

  const toggleMobileMenu = () => {
    if (!menuToggle || !mobileMenu) {
      return;
    }

    const isOpen = menuToggle.getAttribute("aria-expanded") === "true";

    if (isOpen) {
      closeMobileMenu();
    } else {
      openMobileMenu();
    }
  };

  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener("click", toggleMobileMenu);

    const mobileLinks = mobileMenu.querySelectorAll("a");

    mobileLinks.forEach((link) => {
      link.addEventListener("click", () => {
        closeMobileMenu();
      });
    });
  }

  /* ==========================================================
     07. DESKTOP BREAKPOINT
     ========================================================== */

  const desktopMedia = window.matchMedia("(min-width: 1024px)");

  const handleDesktopChange = (event) => {
    if (event.matches) {
      closeMobileMenu();
    }
  };

  if (typeof desktopMedia.addEventListener === "function") {
    desktopMedia.addEventListener("change", handleDesktopChange);
  } else if (typeof desktopMedia.addListener === "function") {
    desktopMedia.addListener(handleDesktopChange);
  }

  /* ==========================================================
     08. LANGUAGE DROPDOWN
     ========================================================== */

  const openLanguageMenu = () => {
    if (!languageButton || !languageMenu) {
      return;
    }

    languageMenu.hidden = false;
    languageButton.setAttribute("aria-expanded", "true");
  };

  const closeLanguageMenu = () => {
    if (!languageButton || !languageMenu) {
      return;
    }

    languageMenu.hidden = true;
    languageButton.setAttribute("aria-expanded", "false");
  };

  const toggleLanguageMenu = () => {
    if (!languageButton || !languageMenu) {
      return;
    }

    const isOpen = languageButton.getAttribute("aria-expanded") === "true";

    if (isOpen) {
      closeLanguageMenu();
    } else {
      openLanguageMenu();
    }
  };

  if (languageButton && languageMenu) {
    languageButton.addEventListener("click", (event) => {
      event.stopPropagation();
      toggleLanguageMenu();
    });

    languageMenu.addEventListener("click", (event) => {
      event.stopPropagation();
    });

    document.addEventListener("click", () => {
      closeLanguageMenu();
    });
  }

  /* ==========================================================
     09. ESCAPE
     ========================================================== */

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") {
      return;
    }

    if (
      languageButton &&
      languageButton.getAttribute("aria-expanded") === "true"
    ) {
      closeLanguageMenu();
      languageButton.focus();
    }

    if (menuToggle && menuToggle.getAttribute("aria-expanded") === "true") {
      closeMobileMenu();
      menuToggle.focus();
    }
  });

  /* ==========================================================
     10. INTERNAL ANCHORS
     ========================================================== */

  const internalAnchorLinks = document.querySelectorAll(
    'a[href^="#"]:not([href="#"])',
  );

  internalAnchorLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      const targetSelector = link.getAttribute("href");

      if (!targetSelector) {
        return;
      }

      let target;

      try {
        target = document.querySelector(targetSelector);
      } catch (error) {
        return;
      }

      if (!target) {
        return;
      }

      event.preventDefault();

      const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)",
      ).matches;

      target.scrollIntoView({
        behavior: reduceMotion ? "auto" : "smooth",
        block: "start",
      });

      if (menuToggle && menuToggle.getAttribute("aria-expanded") === "true") {
        closeMobileMenu();
      }

      if (window.history && typeof window.history.pushState === "function") {
        window.history.pushState(null, "", targetSelector);
      }
    });
  });

  /* ==========================================================
     11. ACTIVE HOMEPAGE SECTION
     ========================================================== */

  const observedSections = [
    {
      id: "nowe",
      selector: 'a[href="#nowe"]',
    },
    {
      id: "uzywane",
      selector: 'a[href="#uzywane"]',
    },
    {
      id: "leasing",
      selector: 'a[href="#leasing"]',
    },
    {
      id: "kontakt",
      selector: 'a[href="#kontakt"]',
    },
  ];

  if ("IntersectionObserver" in window) {
    const sectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) {
            return;
          }

          const sectionId = entry.target.id;

          document.querySelectorAll(".hero-benefit").forEach((link) => {
            link.classList.remove("is-current");
          });

          const matchingItem = observedSections.find(
            (item) => item.id === sectionId,
          );

          if (!matchingItem) {
            return;
          }

          const matchingLink = document.querySelector(matchingItem.selector);

          if (matchingLink) {
            matchingLink.classList.add("is-current");
          }
        });
      },
      {
        root: null,
        rootMargin: "-30% 0px -55% 0px",
        threshold: 0,
      },
    );

    observedSections.forEach((item) => {
      const section = document.getElementById(item.id);

      if (section) {
        sectionObserver.observe(section);
      }
    });
  }

  /* ==========================================================
     12. CONTACT FORM HELPERS
     ========================================================== */

  const setFormStatus = (message = "", type = "") => {
    if (!formStatus) {
      return;
    }

    formStatus.textContent = message;

    formStatus.classList.remove("is-success", "is-error", "is-info");

    if (type) {
      formStatus.classList.add(`is-${type}`);
    }
  };

  const getTrimmedValue = (field) => {
    if (!field) {
      return "";
    }

    return field.value.trim();
  };

  /* ==========================================================
     13. CONTACT FORM VALIDATION
     ========================================================== */

  const validateContactForm = () => {
    if (!contactForm) {
      return false;
    }

    const name = contactForm.elements["name"];
    const city = contactForm.elements["city"];
    const email = contactForm.elements["email"];
    const phone = contactForm.elements["phone"];
    const privacy = contactForm.elements["privacy"];

    if (
      !getTrimmedValue(name) ||
      !getTrimmedValue(city) ||
      !getTrimmedValue(email) ||
      !getTrimmedValue(phone)
    ) {
      setFormStatus("Uzupełnij wszystkie wymagane pola.", "error");

      return false;
    }

    if (email && !email.checkValidity()) {
      setFormStatus("Podaj poprawny adres e-mail.", "error");

      email.focus();

      return false;
    }

    const phoneValue = getTrimmedValue(phone);

    const phonePattern = /^[+()0-9\s-]{7,25}$/;

    if (!phonePattern.test(phoneValue)) {
      setFormStatus("Podaj poprawny numer telefonu.", "error");

      phone.focus();

      return false;
    }

    if (!privacy || !privacy.checked) {
      setFormStatus(
        "Aby wysłać zapytanie, zaakceptuj zgodę na przetwarzanie danych.",
        "error",
      );

      if (privacy) {
        privacy.focus();
      }

      return false;
    }

    return true;
  };

  /* ==========================================================
     14. CONTACT FORM SUBMIT
     ========================================================== */

  if (contactForm && formStatus) {
    contactForm.addEventListener("submit", (event) => {
      event.preventDefault();

      setFormStatus();

      const isValid = validateContactForm();

      if (!isValid) {
        return;
      }

      setFormStatus(
        "Formularz jest gotowy. Wysyłkę uruchomimy po podłączeniu systemu zgłoszeń.",
        "info",
      );
    });

    contactForm.addEventListener("input", () => {
      if (formStatus && formStatus.classList.contains("is-error")) {
        setFormStatus();
      }
    });
  }

  /* ==========================================================
     15. EXTERNAL LINKS
     ========================================================== */

  const externalLinks = document.querySelectorAll('a[href^="http"]');

  externalLinks.forEach((link) => {
    let url;

    try {
      url = new URL(link.href, window.location.href);
    } catch (error) {
      return;
    }

    if (url.hostname === window.location.hostname) {
      return;
    }

    if (link.getAttribute("target") === "_blank") {
      const currentRel = link.getAttribute("rel") || "";

      const relValues = new Set(currentRel.split(/\s+/).filter(Boolean));

      relValues.add("noopener");
      relValues.add("noreferrer");

      link.setAttribute("rel", Array.from(relValues).join(" "));
    }
  });

  /* ==========================================================
     16. INITIAL HASH
     ========================================================== */

  const scrollToInitialHash = () => {
    if (!window.location.hash) {
      return;
    }

    let target;

    try {
      target = document.querySelector(window.location.hash);
    } catch (error) {
      return;
    }

    if (!target) {
      return;
    }

    window.requestAnimationFrame(() => {
      target.scrollIntoView({
        behavior: "auto",
        block: "start",
      });
    });
  };

  scrollToInitialHash();
});
