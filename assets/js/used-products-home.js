document.addEventListener("DOMContentLoaded", () => {
  const homeUsedGrid = document.querySelector("#used-products-home");

  if (!homeUsedGrid) {
    return;
  }

  if (typeof usedProducts === "undefined" || !Array.isArray(usedProducts)) {
    console.error("LTS Market: usedProducts nie zostało załadowane.");
    return;
  }

  const path = window.location.pathname;

  let language = "pl";
  let rootPrefix = "";

  if (path.includes("/en/")) {
    language = "en";
    rootPrefix = "../";
  } else if (path.includes("/ru/")) {
    language = "ru";
    rootPrefix = "../";
  }

  const labels = {
    pl: {
      badge: "UŻYWANY",
      link: "Zobacz urządzenie →",
    },

    en: {
      badge: "USED",
      link: "View equipment →",
    },

    ru: {
      badge: "Б/У",
      link: "Смотреть оборудование →",
    },
  };

  const productsToShow = usedProducts.slice(0, 3);

  homeUsedGrid.innerHTML = productsToShow
    .map((product) => {
      const productName = product.name[language] || product.name.pl;

      const category =
        product.categoryLabel[language] || product.categoryLabel.pl;

      const description =
        product.description[language] || product.description.pl;

      const image = `${rootPrefix}${product.image}`;

      /*
       * На даний момент окремі сторінки товарів існують польською.
       * Тому EN/RU головні ведуть на польську картку товару.
       * Коли створимо EN/RU product pages, змінимо це централізовано.
       */
      const productUrl = `${rootPrefix}uzywane/${product.slug}.html`;

      return `
        <article class="product-card">
          <a
            href="${productUrl}"
            class="product-card-image"
            aria-label="${productName}"
          >
            <span class="product-badge">
              ${labels[language].badge}
            </span>

            <img
              src="${image}"
              alt="${productName}"
              width="600"
              height="600"
              loading="lazy"
            />
          </a>

          <div class="product-card-body">
            <span class="product-card-category">
              ${category}
            </span>

            <h3>
              ${productName}
            </h3>

            <p>
              ${description}
            </p>

            <div class="product-card-price">
              ${product.priceLabel}
            </div>

            <a
              href="${productUrl}"
              class="product-card-link"
            >
              ${labels[language].link}
            </a>
          </div>
        </article>
      `;
    })
    .join("");
});
