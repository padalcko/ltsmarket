/* ==========================================================
   LTS MARKET
   kontakt.js
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  /* ======================================================
     01. MOBILE MENU
     ====================================================== */

  const menuToggle = document.querySelector(".menu-toggle");

  const mobileMenu = document.querySelector(".mobile-menu");

  if (menuToggle && mobileMenu) {
    const closeMenu = () => {
      mobileMenu.classList.remove("is-open");

      menuToggle.classList.remove("is-active");

      menuToggle.setAttribute("aria-expanded", "false");

      menuToggle.setAttribute("aria-label", "Otwórz menu");
    };

    menuToggle.addEventListener("click", () => {
      const isOpen = mobileMenu.classList.toggle("is-open");

      menuToggle.classList.toggle("is-active", isOpen);

      menuToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");

      menuToggle.setAttribute(
        "aria-label",
        isOpen ? "Zamknij menu" : "Otwórz menu",
      );
    });

    mobileMenu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeMenu();
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 1180) {
        closeMenu();
      }
    });
  }

  /* ======================================================
     02. HEADER SCROLL
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

  /* ======================================================
     03. CONTACT FORM
     ====================================================== */

  const contactForm = document.querySelector("#contact-form");

  const formStatus = document.querySelector("#form-status");

  if (contactForm && formStatus) {
    contactForm.addEventListener("submit", (event) => {
      event.preventDefault();

      /* VALIDATION */

      if (!contactForm.checkValidity()) {
        contactForm.reportValidity();

        showStatus("Sprawdź wymagane pola formularza.", "error");

        return;
      }

      const formData = new FormData(contactForm);

      const name = String(formData.get("name") || "").trim();

      const company = String(formData.get("company") || "").trim();

      const email = String(formData.get("email") || "").trim();

      const phone = String(formData.get("phone") || "").trim();

      const subject = String(formData.get("subject") || "").trim();

      const message = String(formData.get("message") || "").trim();

      const subjectLabels = {
        "nowe-urzadzenie": "Nowe urządzenie",

        "uzywane-urzadzenie": "Używane urządzenie",

        leasing: "Leasing / finansowanie",

        wspolpraca: "Współpraca",

        inne: "Inne",
      };

      const readableSubject = subjectLabels[subject] || "Zapytanie";

      const emailSubject = encodeURIComponent(
        `LTS Market - ${readableSubject}`,
      );

      const emailBody = encodeURIComponent(
        [
          "Zapytanie ze strony LTS Market",
          "",
          `Imię i nazwisko: ${name}`,
          `Firma: ${company || "-"}`,
          `E-mail: ${email}`,
          `Telefon: ${phone || "-"}`,
          `Temat: ${readableSubject}`,
          "",
          "Wiadomość:",
          message,
        ].join("\n"),
      );

      const mailtoURL =
        "mailto:sales@ltsmarket.pl" +
        `?subject=${emailSubject}` +
        `&body=${emailBody}`;

      showStatus("Otwieramy wiadomość e-mail.", "success");

      window.location.href = mailtoURL;
    });

    /* REMOVE STATUS WHEN EDITING */

    contactForm.querySelectorAll("input, textarea, select").forEach((field) => {
      const clearStatus = () => {
        formStatus.classList.remove("is-visible", "is-success", "is-error");
      };

      field.addEventListener("input", clearStatus);

      field.addEventListener("change", clearStatus);
    });
  }

  /* ======================================================
     04. STATUS FUNCTION
     ====================================================== */

  function showStatus(message, type) {
    if (!formStatus) {
      return;
    }

    formStatus.textContent = message;

    formStatus.classList.remove("is-success", "is-error");

    if (type === "success") {
      formStatus.classList.add("is-success");
    }

    if (type === "error") {
      formStatus.classList.add("is-error");
    }

    formStatus.classList.add("is-visible");
  }
});
