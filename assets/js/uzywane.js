/* ==========================================================
   LTS MARKET
   USED PRODUCTS CATALOG
   uzywane.js

   ONE CATALOG FOR:
   PL / EN / RU

   Product data:
   assets/js/used-products.js
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
     CHECKS
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
     LANGUAGE
  ====================================================== */

  const htmlLang = (document.documentElement.lang || "pl")
    .toLowerCase()
    .split("-")[0];

  const supportedLanguages = ["pl", "en", "ru"];

  const lang = supportedLanguages.includes(htmlLang) ? htmlLang : "pl";

  /* ======================================================
     TRANSLATIONS
  ====================================================== */

  const translations = {
    pl: {
      used: "UŻYWANY",
      year: "Rok",
      condition: "Stan",
      service: "Serwis",
      price: "Cena",
      show: "Zobacz",
      imageAltSuffix: "używane urządzenie dostępne w LTS Market",
    },

    en: {
      used: "PRE-OWNED",
      year: "Year",
      condition: "Condition",
      service: "Service",
      price: "Price",
      show: "View",
      imageAltSuffix: "pre-owned device available at LTS Market",
    },

    ru: {
      used: "Б/У",
      year: "Год",
      condition: "Состояние",
      service: "Сервис",
      price: "Цена",
      show: "Подробнее",
      imageAltSuffix: "б/у аппарат, доступный в LTS Market",
    },
  };

  const t = translations[lang];

  /* ======================================================
     HELPERS
  ====================================================== */

  function getLocalizedValue(value) {
    if (value && typeof value === "object" && !Array.isArray(value)) {
      return value[lang] || value.pl || value.en || value.ru || "";
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
     SORT PRODUCTS
     NEWEST ADDED FIRST
  ====================================================== */

  function getAddedTimestamp(product) {
    if (!product || !product.added) {
      return 0;
    }

    const timestamp = Date.parse(product.added);

    return Number.isNaN(timestamp) ? 0 : timestamp;
  }

  const sortedProducts = [...usedProducts].sort(
    (a, b) => getAddedTimestamp(b) - getAddedTimestamp(a),
  );

  /* ======================================================
     NORMALIZE IMAGE PATH
  ====================================================== */

  function getImageUrl(image) {
    if (!image) {
      return "";
    }

    /*
     * used-products.js stores paths like:
     *
     * assets/img/uzywane/...
     *
     * A leading slash is added so the image works from:
     *
     * /uzywane.html
     * /en/uzywane.html
     * /ru/uzywane.html
     */

    if (
      image.startsWith("http://") ||
      image.startsWith("https://") ||
      image.startsWith("/")
    ) {
      return image;
    }

    return `/${image}`;
  }

  /* ======================================================
     PRODUCT URL
  ====================================================== */

  function getProductUrl(slug) {
    /*
     * Product detail pages currently exist only in:
     *
     * /uzywane/
     *
     * EN / RU catalogues therefore lead to the existing
     * Polish product page instead of a 404.
     */

    return `/uzywane/${slug}.html`;
  }

  /* ======================================================
     SERVICE CONTENT
  ====================================================== */

  function renderServiceValue(product) {
    const service = getLocalizedValue(product.service);

    if (!service) {
      return "";
    }

    const serviceUrl = product.serviceUrl || "";

    /*
     * If no service URL exists,
     * display the normal escaped text.
     */

    if (!serviceUrl) {
      return escapeHTML(service);
    }

    /*
     * Make only "Laser Tech Service" clickable.
     *
     * Example:
     *
     * Po serwisie Laser Tech Service
     *
     * becomes:
     *
     * Po serwisie <a>Laser Tech Service</a>
     */

    const serviceName = "Laser Tech Service";

    const serviceNameIndex = service.indexOf(serviceName);

    if (serviceNameIndex === -1) {
      return `
        <a
          href="${escapeHTML(serviceUrl)}"
          target="_blank"
          rel="noopener noreferrer"
        >
          ${escapeHTML(service)}
        </a>
      `;
    }

    const before = service.slice(0, serviceNameIndex);

    const after = service.slice(serviceNameIndex + serviceName.length);

    return `
      ${escapeHTML(before)}

      <a
        href="${escapeHTML(serviceUrl)}"
        target="_blank"
        rel="noopener noreferrer"
        aria-label="Laser Tech Service"
      >
        ${escapeHTML(serviceName)}
      </a>

      ${escapeHTML(after)}
    `;
  }

  /* ======================================================
     RENDER PRODUCTS
  ====================================================== */

  function renderProducts() {
    productsGrid.innerHTML = sortedProducts
      .map((product) => {
        const name = getLocalizedValue(product.name);

        const categoryLabel = getLocalizedValue(product.categoryLabel);

        const description = getLocalizedValue(product.description);

        const condition = getLocalizedValue(product.condition);

        const service = getLocalizedValue(product.service);

        const slug = product.slug || "";

        const category = product.category || "";

        const image = getImageUrl(product.image || "");

        const priceLabel = product.priceLabel || "";

        const year = product.year || "";

        const productUrl = getProductUrl(slug);

        const imageAlt = `${name} – ${t.imageAltSuffix}`;

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
                ${escapeHTML(t.used)}
              </span>

              <img
                src="${escapeHTML(image)}"
                alt="${escapeHTML(imageAlt)}"
                width="600"
                height="600"
                loading="lazy"
                decoding="async"
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
                        ${escapeHTML(t.year)}

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
                        ${escapeHTML(t.condition)}

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
                        ${escapeHTML(t.service)}

                        <strong>
                          ${renderServiceValue(product)}
                        </strong>
                      </span>
                    `
                    : ""
                }
              </div>

              <div class="used-product-footer">
                <div class="used-product-price">
                  <span>
                    ${escapeHTML(t.price)}
                  </span>

                  <strong>
                    ${escapeHTML(priceLabel)}
                  </strong>
                </div>

                <a
                  href="${escapeHTML(productUrl)}"
                  class="used-product-arrow"
                  aria-label="${escapeHTML(`${t.show} ${name}`)}"
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
      const categories = (card.dataset.category || "")
        .split(/\s+/)
        .filter(Boolean);

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

      /* ALL */

      if (filter === "all") {
        activeFilters.clear();

        updateButtons();
        filterProducts();

        return;
      }

      /* CATEGORY */

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
