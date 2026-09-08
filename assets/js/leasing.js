/* ==========================================================
   LTS MARKET
   LEASING
   leasing.js
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  const faqItems = Array.from(document.querySelectorAll(".leasing-faq-item"));

  if (!faqItems.length) {
    return;
  }

  function closeItem(item) {
    const button = item.querySelector(".leasing-faq-question");

    if (!button) {
      return;
    }

    item.classList.remove("is-open");

    button.setAttribute("aria-expanded", "false");
  }

  function openItem(item) {
    const button = item.querySelector(".leasing-faq-question");

    if (!button) {
      return;
    }

    item.classList.add("is-open");

    button.setAttribute("aria-expanded", "true");
  }

  faqItems.forEach((item) => {
    const button = item.querySelector(".leasing-faq-question");

    if (!button) {
      return;
    }

    button.addEventListener("click", () => {
      const isOpen = item.classList.contains("is-open");

      faqItems.forEach((otherItem) => {
        if (otherItem !== item) {
          closeItem(otherItem);
        }
      });

      if (isOpen) {
        closeItem(item);
      } else {
        openItem(item);
      }
    });
  });
});
