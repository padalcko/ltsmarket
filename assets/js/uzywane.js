/* ==========================================================
   LTS MARKET
   UŻYWANE
   uzywane.js

   AUTOMATIC PRODUCT RENDERING
   + MULTI-SELECT FILTERS
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  /* ======================================================
     ELEMENTS
     ====================================================== */

  const productsGrid = document.querySelector("[data-products-grid]");

  const filterButtons = Array.from(
    document.querySelectorAll(".catalog-filter"),
  );

  const emptyState = document.querySelector("[data-catalog-empty]");

  /* ======================================================
     CHECK PRODUCT DATA
     ====================================================== */

  if (!productsGrid) {
    console.error("LTS Market: nie znaleziono kontenera [data-products-grid].");

    return;
  }

  if (typeof usedProducts === "undefined" || !Array.isArray(usedProducts)) {
    console.error("LTS Market: usedProducts nie zostało załadowane.");

    return;
  }

  /* ======================================================
     HELPERS
     ====================================================== */

  function getPolishValue(value) {
    if (value && typeof value === "object" && !Array.isArray(value)) {
      return value.pl || "";
    }

    return value || "";
  }

  function escapeHTML(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  /* ======================================================
     RENDER PRODUCTS
     ====================================================== */

  function renderProducts() {
    productsGrid.innerHTML = usedProducts
      .map((product) => {
        const name = getPolishValue(product.name);

        const categoryLabel = getPolishValue(product.categoryLabel);

        const description = getPolishValue(product.description);

        const condition = getPolishValue(product.condition);

        const service = getPolishValue(product.service);

        const slug = product.slug || "";

        const category = product.category || "";

        const image = product.image || "";

        const priceLabel = product.priceLabel || "";

        const year = product.year || "";

        const productUrl = `uzywane/${slug}.html`;

        return `
          <article
            class="used-product-card"
            data-category="${escapeHTML(category)}"
          >
            <a
              href="${escapeHTML(productUrl)}"
              class="used-product-image"
              aria-label="${escapeHTML(name)}"
            >
              <span class="used-product-status">
                UŻYWANY
              </span>

              <img
                src="${escapeHTML(image)}"
                alt="${escapeHTML(
                  `${name} – używane urządzenie dostępne w LTS Market`,
                )}"
                width="600"
                height="600"
                loading="lazy"
              />
            </a>

            <div class="used-product-body">
              <span class="used-product-category">
                ${escapeHTML(categoryLabel)}
              </span>

              <h2>
                <a href="${escapeHTML(productUrl)}">
                  ${escapeHTML(name)}
                </a>
              </h2>

              ${
                description
                  ? `
                    <p class="used-product-description">
                      ${escapeHTML(description)}
                    </p>
                  `
                  : ""
              }

              <div class="used-product-meta">
                ${
                  year
                    ? `
                      <span>
                        Rok

                        <strong>
                          ${escapeHTML(year)}
                        </strong>
                      </span>
                    `
                    : ""
                }

                ${
                  condition
                    ? `
                      <span>
                        Stan

                        <strong>
                          ${escapeHTML(condition)}
                        </strong>
                      </span>
                    `
                    : ""
                }

                ${
                  service
                    ? `
                      <span>
                        Serwis

                        <strong>
                          ${escapeHTML(service)}
                        </strong>
                      </span>
                    `
                    : ""
                }
              </div>

              <div class="used-product-footer">
                <div class="used-product-price">
                  <span>
                    Cena
                  </span>

                  <strong>
                    ${escapeHTML(priceLabel)}
                  </strong>
                </div>

                <a
                  href="${escapeHTML(productUrl)}"
                  class="used-product-arrow"
                  aria-label="${escapeHTML(`Zobacz ${name}`)}"
                >
                  →
                </a>
              </div>
            </div>
          </article>
        `;
      })
      .join("");
  }

  renderProducts();

  /* ======================================================
     PRODUCT CARDS
     ====================================================== */

  const productCards = Array.from(
    productsGrid.querySelectorAll(".used-product-card"),
  );

  /* ======================================================
     ACTIVE FILTERS
     ====================================================== */

  const activeFilters = new Set();

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
       * Karta może mieć jedną lub kilka kategorii:
       *
       * data-category="rf"
       *
       * albo:
       *
       * data-category="rf nd-yag"
       */

      const categories = (card.dataset.category || "")
        .split(/\s+/)
        .filter(Boolean);

      /*
       * Brak aktywnych filtrów:
       * pokazujemy wszystkie urządzenia.
       *
       * Kilka aktywnych filtrów:
       * urządzenie jest widoczne, jeśli należy
       * do co najmniej jednej wybranej kategorii.
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
       * Czyści wszystkie wybrane filtry.
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
       * Ponowne kliknięcie tej samej kategorii
       * wyłącza filtr.
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
