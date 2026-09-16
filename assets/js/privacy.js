/* Optional analytics: no Google request is made before consent. */
document.addEventListener("DOMContentLoaded", () => {
  const key = "lts-analytics-consent-v1";
  const measurementId = "G-1Z98BZS3WW";
  const lang = document.documentElement.lang.split("-")[0];
  const t = ({
    pl: { title: "Ustawienia prywatności", text: "Możesz zezwolić na Google Analytics, aby pomóc nam zrozumieć korzystanie z witryny. Bez zgody analityka pozostaje wyłączona. Wybór zapisujemy w tej przeglądarce. Możesz go zmienić w stopce.", accept: "Zezwól na analitykę", reject: "Bez analityki", link: "Informacje o prywatności", url: "/prywatnosc.html" },
    en: { title: "Privacy settings", text: "You can allow Google Analytics to help us understand website usage. Analytics stays off without your consent. Your choice is saved in this browser and can be changed in the footer.", accept: "Allow analytics", reject: "Without analytics", link: "Privacy information", url: "/en/prywatnosc.html" },
    ru: { title: "Настройки конфиденциальности", text: "Вы можете разрешить Google Analytics для анализа посещений сайта. Без согласия аналитика отключена. Выбор сохраняется в этом браузере; его можно изменить внизу страницы.", accept: "Разрешить аналитику", reject: "Без аналитики", link: "Информация о конфиденциальности", url: "/ru/prywatnosc.html" },
  })[lang] || null;
  if (!t) return;
  window[`ga-disable-${measurementId}`] = true;
  let consent;
  let loaded = false;
  try { consent = localStorage.getItem(key); } catch { /* Storage is optional. */ }
  function enableAnalytics() {
    window[`ga-disable-${measurementId}`] = false;
    if (loaded) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", measurementId, { send_page_view: true });
    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    document.head.append(script);
  }
  function removeAnalyticsCookies() {
    const domains = ["", location.hostname, "." + location.hostname, ".ltsmarket.pl"];
    document.cookie.split(";").forEach((cookie) => {
      const name = cookie.split("=")[0].trim();
      if (name !== "_ga" && !name.startsWith("_ga_")) return;
      domains.forEach((domain) => {
        document.cookie = `${name}=; Max-Age=0; path=/; SameSite=Lax${domain ? "; domain=" + domain : ""}`;
      });
    });
  }
  const panel = document.createElement("section");
  panel.className = "privacy-panel";
  panel.setAttribute("aria-labelledby", "privacy-title");
  panel.innerHTML = `<h2 id="privacy-title"></h2><p></p><p><a></a></p><div class="privacy-actions"><button type="button" data-reject></button><button type="button" data-accept></button></div>`;
  panel.querySelector("h2").textContent = t.title;
  panel.querySelector("p").textContent = t.text;
  const link = panel.querySelector("a");
  link.href = t.url;
  link.textContent = t.link;
  const reject = panel.querySelector("[data-reject]");
  const accept = panel.querySelector("[data-accept]");
  reject.textContent = t.reject;
  accept.textContent = t.accept;
  let returnFocus;
  function choose(value) {
    const wasEnabled = consent === "granted";
    consent = value;
    try { localStorage.setItem(key, value); } catch { /* Choice applies to this page. */ }
    panel.hidden = true;
    if (value === "granted") enableAnalytics();
    else {
      window[`ga-disable-${measurementId}`] = true;
      removeAnalyticsCookies();
    }
    returnFocus?.focus();
    // Reload only to unload an already-running third-party script after withdrawal.
    if (wasEnabled && value === "denied") location.reload();
  }
  reject.addEventListener("click", () => choose("denied"));
  accept.addEventListener("click", () => choose("granted"));
  panel.hidden = consent === "granted" || consent === "denied";
  document.body.append(panel);
  document.querySelectorAll("[data-privacy-settings]").forEach((button) => {
    button.hidden = false;
    button.addEventListener("click", () => { returnFocus = button; panel.hidden = false; reject.focus(); });
  });
  window.addEventListener("storage", (event) => {
    if (event.key === key) location.reload();
  });
  if (consent === "granted") enableAnalytics();
});
