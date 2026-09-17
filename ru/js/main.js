"use strict";

/* ============================================================
   LTS MARKET
   ru/js/main.js
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
     04. HEADER ON SCROLL
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
     05. MOBILE MENU
     ========================================================== */

  const openMobileMenu = () => {
    if (!menuToggle || !mobileMenu) {
      return;
    }

    mobileMenu.hidden = false;

    menuToggle.classList.add("is-active");

    menuToggle.setAttribute("aria-expanded", "true");
    menuToggle.setAttribute("aria-label", "Закрыть меню");

    body.classList.add("menu-open");
  };

  const closeMobileMenu = () => {
    if (!menuToggle || !mobileMenu) {
      return;
    }

    mobileMenu.hidden = true;

    menuToggle.classList.remove("is-active");

    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Открыть меню");

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
     06. CLOSE MOBILE MENU AFTER DESKTOP BREAKPOINT
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
     07. LANGUAGE DROPDOWN
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
     08. ESCAPE KEY
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
     09. INTERNAL ANCHORS
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
     10. ACTIVE NAVIGATION FOR HOMEPAGE SECTIONS
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
     11. CONTACT FORM — HELPERS
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
     12. CONTACT FORM VALIDATION
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
      setFormStatus("Заполните все обязательные поля.", "error");

      return false;
    }

    if (email && !email.checkValidity()) {
      setFormStatus("Введите корректный адрес электронной почты.", "error");

      email.focus();

      return false;
    }

    const phoneValue = getTrimmedValue(phone);

    const phonePattern = /^[0-9]{7,15}$/;

    if (!phonePattern.test(phoneValue.replace(/[\s()+-]/g, ""))) {
      setFormStatus("Введите корректный номер телефона.", "error");

      phone.focus();

      return false;
    }

    if (!privacy || !privacy.checked) {
      setFormStatus(
        "Для отправки запроса подтвердите согласие на обработку данных.",
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
     13. CONTACT FORM SUBMIT
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
        "Отправка через сайт пока недоступна. Напишите на sales@ltsmarket.pl или позвоните +48 575 254 431.",
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
     14. EXTERNAL LINKS
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
     15. INITIAL HASH
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
