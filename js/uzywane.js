"use strict";
document.querySelectorAll("[data-gallery]").forEach((gallery) => {
  const main = gallery.querySelector("[data-gallery-main]");
  const link = main.closest("a");
  let request = 0;
  gallery.querySelectorAll("[data-image]").forEach((button) => {
    button.addEventListener("click", () => {
      const current = ++request;
      const image = new Image();
      image.onload = () => {
        if (current !== request) return;
        main.src = image.src;
        main.alt = button.querySelector("img").alt;
        link.href = image.src;
        gallery.querySelectorAll("[data-image]").forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
      };
      image.src = button.dataset.image;
    });
  });
});
