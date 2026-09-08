/* ==========================================================
   LTS MARKET
   kontakt.js

   Contact form only.
   Global navigation / header logic is handled by main.js.
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  /* ======================================================
     01. ELEMENTS
     ====================================================== */

  const contactForm = document.querySelector("#contact-form");
  const formStatus = document.querySelector("#form-status");

  if (!contactForm) {
    return;
  }

  /* ======================================================
     02. LANGUAGE
     ====================================================== */

  const pageLang = document.documentElement.lang?.toLowerCase() || "pl";

  const lang = pageLang.startsWith("en")
    ? "en"
    : pageLang.startsWith("ru")
      ? "ru"
      : "pl";

  /* ======================================================
     03. TRANSLATIONS
     ====================================================== */

  const translations = {
    pl: {
      validationError: "Sprawdź wymagane pola formularza.",

      consentError: "Zaznacz zgodę na kontakt.",

      openingEmail:
        "Otwieramy wiadomość e-mail. Jeśli program pocztowy nie uruchomi się automatycznie, napisz bezpośrednio na sales@ltsmarket.pl.",

      mailTitle: "Zapytanie ze strony LTS Market",

      fields: {
        name: "Imię i nazwisko",
        company: "Firma",
        email: "E-mail",
        phone: "Telefon",
        subject: "Temat",
        message: "Wiadomość",
      },

      subjects: {
        "nowe-urzadzenie": "Nowe urządzenie",
        "uzywane-urzadzenie": "Używane urządzenie",
        leasing: "Leasing / finansowanie",
        serwis: "Serwis urządzenia",
        wspolpraca: "Współpraca",
        inne: "Inne",
      },

      fallbackSubject: "Zapytanie",
    },

    en: {
      validationError: "Please check the required form fields.",

      consentError: "Please agree to be contacted.",

      openingEmail:
        "We are opening your e-mail application. If it does not open automatically, write directly to sales@ltsmarket.pl.",

      mailTitle: "Enquiry from the LTS Market website",

      fields: {
        name: "Full name",
        company: "Company",
        email: "E-mail",
        phone: "Phone",
        subject: "Subject",
        message: "Message",
      },

      subjects: {
        "nowe-urzadzenie": "New equipment",
        "uzywane-urzadzenie": "Used equipment",
        leasing: "Leasing / financing",
        serwis: "Equipment service",
        wspolpraca: "Cooperation",
        inne: "Other",
      },

      fallbackSubject: "Enquiry",
    },

    ru: {
      validationError: "Проверьте обязательные поля формы.",

      consentError: "Подтвердите согласие на контакт.",

      openingEmail:
        "Открываем почтовое приложение. Если оно не запустилось автоматически, напишите напрямую на sales@ltsmarket.pl.",

      mailTitle: "Запрос с сайта LTS Market",

      fields: {
        name: "Имя и фамилия",
        company: "Компания",
        email: "E-mail",
        phone: "Телефон",
        subject: "Тема",
        message: "Сообщение",
      },

      subjects: {
        "nowe-urzadzenie": "Новое оборудование",
        "uzywane-urzadzenie": "Б/у оборудование",
        leasing: "Лизинг / финансирование",
        serwis: "Сервис оборудования",
        wspolpraca: "Сотрудничество",
        inne: "Другое",
      },

      fallbackSubject: "Запрос",
    },
  };

  const t = translations[lang];

  /* ======================================================
     04. STATUS
     ====================================================== */

  function showStatus(message, type = "") {
    if (!formStatus) {
      return;
    }

    formStatus.textContent = message;

    formStatus.classList.remove("is-visible", "is-success", "is-error");

    if (type === "success") {
      formStatus.classList.add("is-success");
    }

    if (type === "error") {
      formStatus.classList.add("is-error");
    }

    formStatus.classList.add("is-visible");
  }

  function clearStatus() {
    if (!formStatus) {
      return;
    }

    formStatus.textContent = "";

    formStatus.classList.remove("is-visible", "is-success", "is-error");
  }

  /* ======================================================
     05. VALIDATION
     ====================================================== */

  function validateForm() {
    if (!contactForm.checkValidity()) {
      contactForm.reportValidity();

      showStatus(t.validationError, "error");

      return false;
    }

    return true;
  }

  /* ======================================================
     06. GET FORM DATA
     ====================================================== */

  function getFormValues() {
    const formData = new FormData(contactForm);

    return {
      name: String(formData.get("name") || "").trim(),

      company: String(formData.get("company") || "").trim(),

      email: String(formData.get("email") || "").trim(),

      phone: String(formData.get("phone") || "").trim(),

      subject: String(formData.get("subject") || "").trim(),

      message: String(formData.get("message") || "").trim(),

      consent: formData.get("consent") === "1",
    };
  }

  /* ======================================================
     07. BUILD MAILTO
     Temporary transport until n8n is connected.
     ====================================================== */

  function buildMailtoUrl(data) {
    const readableSubject = t.subjects[data.subject] || t.fallbackSubject;

    const emailSubject = encodeURIComponent(`LTS Market — ${readableSubject}`);

    const emailBody = encodeURIComponent(
      [
        t.mailTitle,
        "",
        `${t.fields.name}: ${data.name}`,
        `${t.fields.company}: ${data.company || "-"}`,
        `${t.fields.email}: ${data.email}`,
        `${t.fields.phone}: ${data.phone || "-"}`,
        `${t.fields.subject}: ${readableSubject}`,
        "",
        `${t.fields.message}:`,
        data.message,
      ].join("\n"),
    );

    return (
      "mailto:sales@ltsmarket.pl" +
      `?subject=${emailSubject}` +
      `&body=${emailBody}`
    );
  }

  /* ======================================================
     08. SUBMIT
     ====================================================== */

  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();

    clearStatus();

    if (!validateForm()) {
      return;
    }

    const data = getFormValues();

    if (!data.consent) {
      showStatus(t.consentError, "error");

      return;
    }

    const mailtoUrl = buildMailtoUrl(data);

    showStatus(t.openingEmail, "success");

    window.location.href = mailtoUrl;
  });

  /* ======================================================
     09. CLEAR STATUS WHILE EDITING
     ====================================================== */

  contactForm.querySelectorAll("input, textarea, select").forEach((field) => {
    field.addEventListener("input", clearStatus);

    field.addEventListener("change", clearStatus);
  });
});
