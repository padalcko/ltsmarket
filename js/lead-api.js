/* Shared transport for all PL/EN/RU enquiry forms. */
(() => {
  "use strict";
  const WEBHOOK_URL = "https://n8n.raccoon-studio.com.ua/webhook/lts-market-lead";
  const REQUEST_TIMEOUT_MS = 15000;

  window.LTSLead = {
    async send(data) {
      const now = new Date().toISOString();
      const accepted = data.privacy === "accepted" || data.consent === true;
      const payload = {
        ...data,
        createdAt: data.createdAt || now,
        submittedAt: data.submittedAt || now,
        city: data.city || "",
        salon: data.salon || "",
        source: window.location.hostname || "ltsmarket.pl",
        page: `${window.location.pathname}${window.location.search}`,
        pageUrl: window.location.href,
        language: document.documentElement.lang || "pl",
        privacy: accepted ? "accepted" : "",
        consent: accepted,
      };
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
      try {
        const response = await fetch(WEBHOOK_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
          signal: controller.signal,
        });
        if (!response.ok) throw new Error(`Webhook error: ${response.status}`);
        return { configured: true };
      } finally {
        clearTimeout(timer);
      }
    },
  };
})();
