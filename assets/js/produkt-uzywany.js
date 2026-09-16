/* ==========================================================
   LTS MARKET
   PRODUKT UŻYWANY
   produkt-uzywany.js
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  const mainImage = document.querySelector("[data-product-main-image]");

  const thumbnails = Array.from(
    document.querySelectorAll(".product-thumbnail"),
  );

  if (!mainImage || !thumbnails.length) {
    return;
  }

  function setActiveThumbnail(activeThumbnail) {
    thumbnails.forEach((thumbnail) => {
      const isActive = thumbnail === activeThumbnail;

      thumbnail.classList.toggle("is-active", isActive);

      thumbnail.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
  }

  const language = document.documentElement.lang.split("-")[0];
  const imageError = ({
    pl: "Nie udało się wczytać zdjęcia. Spróbuj ponownie lub wybierz inne zdjęcie.",
    en: "The photo could not be loaded. Try again or choose another photo.",
    ru: "Не удалось загрузить фото. Повторите попытку или выберите другое фото.",
  })[language] || "The photo could not be loaded. Please try again.";
  let imageRequest = 0;
  const status = document.createElement("p");
  status.setAttribute("role", "status");
  status.className = "gallery-status";
  mainImage.closest(".product-gallery").append(status);

  function changeMainImage(thumbnail) {
    const newImage = thumbnail.dataset.image;
    if (!newImage) return;
    const request = ++imageRequest;
    status.textContent = "";
    if (mainImage.getAttribute("src") === newImage) {
      setActiveThumbnail(thumbnail);
      return;
    }
    const candidate = new Image();
    candidate.onload = () => {
      if (request !== imageRequest) return;
      mainImage.removeAttribute("srcset");
      mainImage.removeAttribute("sizes");
      mainImage.src = newImage;
      mainImage.alt = thumbnail.dataset.alt || "";
      setActiveThumbnail(thumbnail);
    };
    candidate.onerror = () => {
      if (request !== imageRequest) return;
      status.textContent = imageError;
    };
    candidate.src = newImage;
  }

  thumbnails.forEach((thumbnail) => {
    thumbnail.setAttribute(
      "aria-pressed",
      thumbnail.classList.contains("is-active") ? "true" : "false",
    );

    thumbnail.addEventListener("click", () => {
      changeMainImage(thumbnail);
    });
  });

  /* ======================================================
     KEYBOARD NAVIGATION
     ====================================================== */

  thumbnails.forEach((thumbnail, index) => {
    thumbnail.addEventListener("keydown", (event) => {
      let nextIndex = null;

      if (event.key === "ArrowRight" || event.key === "ArrowDown") {
        nextIndex = (index + 1) % thumbnails.length;
      }

      if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
        nextIndex = (index - 1 + thumbnails.length) % thumbnails.length;
      }

      if (nextIndex === null) {
        return;
      }

      event.preventDefault();

      const nextThumbnail = thumbnails[nextIndex];

      nextThumbnail.focus();

      changeMainImage(nextThumbnail);
    });
  });
});
