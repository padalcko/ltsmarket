/* ==========================================================
   LTS MARKET
   UŻYWANE
   uzywane.js
   MULTI-SELECT FILTERS
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  const filterButtons = Array.from(
    document.querySelectorAll(".catalog-filter"),
  );

  const productCards = Array.from(
    document.querySelectorAll(".used-product-card"),
  );

  const emptyState = document.querySelector("[data-catalog-empty]");

  if (!filterButtons.length) {
    return;
  }

  /* ======================================================
     ACTIVE FILTERS
     ====================================================== */

  const activeFilters = new Set();

  const allButton = filterButtons.find(
    (button) => button.dataset.filter === "all",
  );

  /* ======================================================
     EMPTY STATE
     ====================================================== */

  function updateEmptyState(visibleCardsCount) {
    if (!emptyState) {
      return;
    }

    emptyState.classList.toggle("is-hidden", visibleCardsCount > 0);
  }

  /* ======================================================
     BUTTON STATE
     ====================================================== */

  function updateButtons() {
    filterButtons.forEach((button) => {
      const filter = button.dataset.filter;

      let isActive = false;

      if (filter === "all") {
        isActive = activeFilters.size === 0;
      } else {
        isActive = activeFilters.has(filter);
      }

      button.classList.toggle("is-active", isActive);

      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
  }

  /* ======================================================
     FILTER PRODUCTS
     ====================================================== */

  function filterProducts() {
    let visibleCardsCount = 0;

    productCards.forEach((card) => {
      /*
       * Картка може мати одну або кілька категорій:
       *
       * data-category="nd-yag"
       *
       * або:
       *
       * data-category="nd-yag rf"
       */

      const categories = (card.dataset.category || "")
        .split(/\s+/)
        .filter(Boolean);

      /*
       * Якщо нічого не вибрано:
       * показуємо всі товари.
       *
       * Якщо вибрано кілька категорій:
       * товар показується, якщо він належить
       * хоча б до однієї з них.
       */

      const shouldShow =
        activeFilters.size === 0 ||
        categories.some((category) => activeFilters.has(category));

      card.hidden = !shouldShow;

      if (shouldShow) {
        visibleCardsCount += 1;
      }
    });

    updateEmptyState(visibleCardsCount);
  }

  /* ======================================================
     FILTER CLICK
     ====================================================== */

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;

      if (!filter) {
        return;
      }

      /*
       * WSZYSTKIE
       *
       * Скидає всі вибрані категорії.
       */

      if (filter === "all") {
        activeFilters.clear();

        updateButtons();
        filterProducts();

        return;
      }

      /*
       * CATEGORY
       *
       * Повторне натискання:
       * вимикає категорію.
       */

      if (activeFilters.has(filter)) {
        activeFilters.delete(filter);
      } else {
        activeFilters.add(filter);
      }

      updateButtons();
      filterProducts();
    });
  });

  /* ======================================================
     INITIAL STATE
     ====================================================== */

  activeFilters.clear();

  updateButtons();
  filterProducts();
});
