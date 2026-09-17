/* ============================================================
   LTS MARKET
   CONTACT FORM
   File: js/kontakt.js
   ============================================================ */

"use strict";

/* ============================================================
   01. CONFIG
   ============================================================ */

/*
 * Тут пізніше вставимо production webhook з n8n.
 *
 * Приклад:
 * const N8N_WEBHOOK_URL =
 *   "https://n8n.example.com/webhook/lts-market-contact";
 *
 * Поки залишаємо порожнім.
 */

const N8N_WEBHOOK_URL = "";

/* ============================================================
   02. ELEMENTS
   ============================================================ */

const contactForm = document.getElementById("contact-form");
const contactFormStatus = document.getElementById("contact-form-status");

/* ============================================================
   03. HELPERS
   ============================================================ */

function showStatus(message, type = "") {
  if (!contactFormStatus) {
    return;
  }

  contactFormStatus.textContent = message;

  contactFormStatus.classList.remove("is-success", "is-error");

  if (type === "success") {
    contactFormStatus.classList.add("is-success");
  }

  if (type === "error") {
    contactFormStatus.classList.add("is-error");
  }

  contactFormStatus.hidden = false;
}

function hideStatus() {
  if (!contactFormStatus) {
    return;
  }

  contactFormStatus.hidden = true;
  contactFormStatus.textContent = "";

  contactFormStatus.classList.remove("is-success", "is-error");
}

function setFieldInvalid(field, invalid) {
  if (!field) {
    return;
  }

  field.classList.toggle("is-invalid", invalid);

  field.setAttribute("aria-invalid", invalid ? "true" : "false");
}

function validateEmail(email) {
  if (!email) {
    return true;
  }

  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validatePhone(phone) {
  const normalizedPhone = phone.replace(/[\s()+-]/g, "");

  return /^[0-9]{7,15}$/.test(normalizedPhone);
}

/* ============================================================
   04. VALIDATION
   ============================================================ */

function validateForm() {
  if (!contactForm) {
    return false;
  }

  const nameField = contactForm.elements["name"];

  const phoneField = contactForm.elements["phone"];

  const emailField = contactForm.elements["email"];

  const consentField = contactForm.elements["consent"];

  let isValid = true;

  /* NAME */

  const nameValue = nameField.value.trim();

  if (nameValue.length < 2) {
    setFieldInvalid(nameField, true);
    isValid = false;
  } else {
    setFieldInvalid(nameField, false);
  }

  /* PHONE */

  const phoneValue = phoneField.value.trim();

  if (!phoneValue || !validatePhone(phoneValue)) {
    setFieldInvalid(phoneField, true);
    isValid = false;
  } else {
    setFieldInvalid(phoneField, false);
  }

  /* EMAIL */

  const emailValue = emailField.value.trim();

  if (!validateEmail(emailValue)) {
    setFieldInvalid(emailField, true);
    isValid = false;
  } else {
    setFieldInvalid(emailField, false);
  }

  /* CONSENT */

  const consentWrapper = consentField.closest(".contact-form__consent");

  if (!consentField.checked) {
    consentWrapper?.classList.add("is-invalid");

    consentField.setAttribute("aria-invalid", "true");

    isValid = false;
  } else {
    consentWrapper?.classList.remove("is-invalid");

    consentField.setAttribute("aria-invalid", "false");
  }

  return isValid;
}

/* ============================================================
   05. BUILD PAYLOAD
   ============================================================ */

function buildPayload() {
  const formData = new FormData(contactForm);

  return {
    name: formData.get("name")?.trim() || "",

    phone: formData.get("phone")?.trim() || "",

    email: formData.get("email")?.trim() || "",

    equipment: formData.get("equipment") || "",

    message: formData.get("message")?.trim() || "",

    consent: formData.get("consent") === "accepted",

    formType: formData.get("formType") || "contact",

    page: formData.get("page") || "kontakt",

    pageUrl: window.location.href,

    language: document.documentElement.lang || "pl",

    submittedAt: new Date().toISOString(),
  };
}

/* ============================================================
   06. SEND TO N8N
   ============================================================ */

async function sendToN8n(payload) {
  if (!N8N_WEBHOOK_URL) {
    /*
     * Webhook jeszcze nie jest podłączony.
     * Nie wykonujemy żadnego requestu.
     */

    return {
      configured: false,
    };
  }

  const response = await fetch(N8N_WEBHOOK_URL, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }

  return {
    configured: true,
  };
}

/* ============================================================
   07. SUBMIT
   ============================================================ */

async function handleSubmit(event) {
  event.preventDefault();

  hideStatus();

  /* VALIDATION */

  const isValid = validateForm();

  if (!isValid) {
    showStatus("Sprawdź wymagane pola i popraw dane w formularzu.", "error");

    const firstInvalid = contactForm.querySelector(
      ".is-invalid, [aria-invalid='true']",
    );

    firstInvalid?.focus();

    return;
  }

  /* PAYLOAD */

  const payload = buildPayload();

  /* SUBMIT BUTTON */

  const submitButton = contactForm.querySelector('button[type="submit"]');

  const originalButtonText = submitButton?.textContent;

  if (submitButton) {
    submitButton.disabled = true;
    submitButton.textContent = "Wysyłanie...";
  }

  try {
    const result = await sendToN8n(payload);

    /*
     * Dopóki webhook nie jest podłączony,
     * NIE pokazujemy użytkownikowi fałszywego
     * komunikatu "wysłano".
     */

    if (!result.configured) {
      showStatus(
        "Wysyłka online jest obecnie niedostępna. Napisz na sales@ltsmarket.pl lub zadzwoń: +48 575 254 431.",
        "",
      );

      return;
    }

    /* SUCCESS */

    showStatus(
      "Dziękujemy. Twoje zapytanie zostało wysłane. Skontaktujemy się z Tobą.",
      "success",
    );

    contactForm.reset();

    /*
     * GA4 event
     */

    if (typeof window.gtag === "function") {
      window.gtag("event", "generate_lead", {
        form_name: "lts_market_contact",

        form_type: payload.formType,

        page: payload.page,
      });
    }
  } catch (error) {
    console.error("LTS Market contact form error:", error);

    showStatus(
      "Nie udało się wysłać formularza. Spróbuj ponownie lub skontaktuj się z nami telefonicznie.",
      "error",
    );
  } finally {
    if (submitButton) {
      submitButton.disabled = false;

      submitButton.textContent = originalButtonText;
    }
  }
}

/* ============================================================
   08. CLEAR VALIDATION ON INPUT
   ============================================================ */

function handleFieldInput(event) {
  const field = event.target;

  if (field.matches("input, select, textarea")) {
    setFieldInvalid(field, false);
  }

  if (field.name === "consent") {
    field.closest(".contact-form__consent")?.classList.remove("is-invalid");
  }

  hideStatus();
}

/* ============================================================
   09. INIT
   ============================================================ */

if (contactForm) {
  contactForm.addEventListener("submit", handleSubmit);

  contactForm.addEventListener("input", handleFieldInput);

  contactForm.addEventListener("change", handleFieldInput);
}

// Carry the selected product into the enquiry without changing form behavior.
if (contactForm) {
  const products = { "3d-contour": "3D CONTOUR", "medilase-pro": "MEDILASE PRO", "ellisys-plus": "Chungwoo ELLISYS PLUS", "daeyang-carbo-3000": "DaeYang CARBO 3000" };
  const product = products[new URLSearchParams(window.location.search).get("product")];
  if (product) {
    const message = contactForm.elements["message"];
    if (message && !message.value) message.value = product;
    contactForm.elements["equipment"].value = "uzywane-urzadzenie";
  }
}
