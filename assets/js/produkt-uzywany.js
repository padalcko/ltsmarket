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

  function changeMainImage(thumbnail) {
    const newImage = thumbnail.dataset.image;

    const newAlt = thumbnail.dataset.alt || "";

    if (!newImage) {
      return;
    }

    if (mainImage.getAttribute("src") === newImage) {
      setActiveThumbnail(thumbnail);

      return;
    }

    mainImage.style.opacity = "0";

    window.setTimeout(() => {
      mainImage.src = newImage;
      mainImage.alt = newAlt;

      mainImage.onload = () => {
        mainImage.style.opacity = "1";
      };
    }, 120);

    setActiveThumbnail(thumbnail);
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
