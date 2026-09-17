"use strict";
(() => {
  const language = document.documentElement.lang;
  const words = {
    pl: ["Ustawienia prywatności", "Czy zezwalasz na Google Analytics? Analityka jest opcjonalna. Wybór możesz zmienić w stopce.", "Zezwól na analitykę", "Odmów", "Zamknij"],
    en: ["Privacy settings", "Allow Google Analytics? Analytics is optional. You can change your choice in the footer.", "Allow analytics", "Decline", "Close"],
    ru: ["Настройки конфиденциальности", "Разрешить Google Analytics? Аналитика необязательна. Выбор можно изменить внизу страницы.", "Разрешить аналитику", "Отказаться", "Закрыть"]
  }[language] || ["Privacy settings", "Allow optional analytics?", "Allow", "Decline", "Close"];
  const key = "lts-analytics-consent-v1";
  const measurement = "G-1Z98BZS3WW";
  let choice = null;
  let loaded = false;
  try { choice = localStorage.getItem(key); } catch (_) {}
  function apply(allowed) {
    window["ga-disable-" + measurement] = !allowed;
    if (!allowed || loaded) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", measurement);
    const script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + measurement;
    document.head.append(script);
  }
  apply(choice === "granted");
  const dialog = document.createElement("dialog");
  dialog.className = "privacy-dialog";
  dialog.setAttribute("aria-labelledby", "privacy-title");
  const title = document.createElement("h2"); title.id = "privacy-title"; title.textContent = words[0];
  const text = document.createElement("p"); text.textContent = words[1];
  const actions = document.createElement("div"); actions.className = "privacy-dialog__actions";
  [true, false].forEach((allowed, index) => {
    const button = document.createElement("button");
    button.type = "button"; button.className = "button button--primary"; button.textContent = words[index + 2];
    button.addEventListener("click", () => {
      choice = allowed ? "granted" : "denied";
      try { localStorage.setItem(key, choice); } catch (_) {}
      apply(allowed); dialog.close();
    });
    actions.append(button);
  });
  const close = document.createElement("button"); close.type = "button"; close.className = "button button--outline"; close.textContent = words[4];
  close.addEventListener("click", () => dialog.close()); actions.append(close);
  dialog.append(title, text, actions); document.body.append(dialog);
  document.getElementById("privacy-settings")?.addEventListener("click", () => dialog.showModal());
  // No popup on arrival; analytics stays disabled until explicitly enabled.
})();
