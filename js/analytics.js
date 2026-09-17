"use strict";
(() => {
  if (window.ltsAnalyticsLoaded) return;
  window.ltsAnalyticsLoaded = true;
  const measurement = "G-1Z98BZS3WW";
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag("js", new Date());
  window.gtag("config", measurement);
  const script = document.createElement("script");
  script.async = true;
  script.src = "https://www.googletagmanager.com/gtag/js?id=" + measurement;
  document.head.append(script);
})();
