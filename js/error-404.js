/* One error document: preserve the failed URL while switching languages. */
(() => {
  'use strict';
  const copy = {
  "pl": {
    "title": "Ojej, coś poszło nie tak.",
    "message": "Takiej strony nie ma. Zaraz wyślę urządzenie do kupującego i to naprawię.",
    "home": "Wróć na stronę główną",
    "catalog": "Zobacz urządzenia",
    "new": "Nowe urządzenia",
    "used": "Używane urządzenia",
    "contact": "Kontakt",
    "choose": "Może tego szukasz?",
    "caption": "Ilustracja: szop z urządzeniami Lumos i Alpha",
    "alt": "Szop w garniturze stoi pomiędzy białym urządzeniem Lumos a czarnym Alpha.",
    "skip": "Przejdź do treści",
    "language": "Wybierz język",
    "error": "Nie znaleziono strony"
  },
  "en": {
    "title": "Oops, something went wrong.",
    "message": "This page doesn’t exist. I’ll send the device to the buyer and then fix this.",
    "home": "Back to homepage",
    "catalog": "Explore equipment",
    "new": "New equipment",
    "used": "Pre-owned equipment",
    "contact": "Contact",
    "choose": "Looking for something?",
    "caption": "Illustration: a raccoon with Lumos and Alpha devices",
    "alt": "A raccoon in a suit stands between a white Lumos device and a black Alpha.",
    "skip": "Skip to content",
    "language": "Choose language",
    "error": "Page not found"
  },
  "ru": {
    "title": "Ой, что-то пошло не так.",
    "message": "Такой страницы нет. Сейчас отправлю покупателю аппарат и всё починю.",
    "home": "Вернуться на главную",
    "catalog": "Посмотреть аппараты",
    "new": "Новые аппараты",
    "used": "Подержанные аппараты",
    "contact": "Контакты",
    "choose": "Возможно, вы ищете это?",
    "caption": "Иллюстрация: енот с аппаратами Lumos и Alpha",
    "alt": "Енот в костюме стоит между белым аппаратом Lumos и чёрным Alpha.",
    "skip": "Перейти к содержимому",
    "language": "Выбрать язык",
    "error": "Страница не найдена"
  }
};
  const chrome = {
  "pl": {
    "header": "<header class=\"site-header\" id=\"site-header\">\n      <div class=\"container header__container\">\n        <a class=\"brand\" href=\"/\" aria-label=\"LTS Market — strona główna\">\n          <span class=\"brand__name\"> LTS <strong>MARKET</strong> </span>\n\n          <span class=\"brand__subtitle\"> PROFESSIONAL BEAUTY EQUIPMENT </span>\n        </a>\n\n        <nav class=\"desktop-nav\" aria-label=\"Główna nawigacja\">\n          <a class=\"desktop-nav__link\" href=\"/\"> Market </a>\n\n          <a class=\"desktop-nav__link\" href=\"/nowe.html\"> Nowe </a>\n\n          <a class=\"desktop-nav__link\" href=\"/uzywane.html\"> Używane </a>\n\n          <a class=\"desktop-nav__link\" href=\"/leasing.html\"> Leasing </a>\n\n          <a class=\"desktop-nav__link\" href=\"https://lasertechservice.pl/\">\n            Serwis\n            <span aria-hidden=\"true\">↗</span>\n          </a>\n\n          <a class=\"desktop-nav__link\" href=\"/blog/\"> Blog </a>\n\n          <a class=\"desktop-nav__link\" href=\"/kontakt.html\"> Kontakt </a>\n        </nav>\n\n        <div class=\"language-switcher\">\n          <button class=\"language-switcher__button\" id=\"language-button\" type=\"button\" aria-expanded=\"false\" aria-controls=\"language-menu\"><span aria-hidden=\"true\">🇵🇱</span><span>PL</span><span class=\"language-switcher__chevron\" aria-hidden=\"true\">▾</span></button>\n\n          <div class=\"language-switcher__menu\" id=\"language-menu\" hidden>\n            <a class=\"language-switcher__option is-active\" href=\"#main-content\" lang=\"pl\" aria-current=\"page\">\n              <span aria-hidden=\"true\">🇵🇱</span>\n              <span>PL</span>\n            </a>\n\n            <a class=\"language-switcher__option\" href=\"#main-content\" lang=\"en\">\n              <span aria-hidden=\"true\">🇬🇧</span>\n              <span>EN</span>\n            </a>\n\n            <a class=\"language-switcher__option\" href=\"#main-content\" lang=\"ru\">\n              <span aria-hidden=\"true\">🇷🇺</span>\n              <span>RU</span>\n            </a>\n          </div>\n        </div>\n\n        <button class=\"menu-toggle\" id=\"menu-toggle\" type=\"button\" aria-label=\"Otwórz menu\" aria-expanded=\"false\" aria-controls=\"mobile-menu\">\n          <span></span>\n          <span></span>\n          <span></span>\n        </button>\n      </div>\n\n      <div class=\"mobile-menu\" id=\"mobile-menu\" hidden>\n        <nav class=\"mobile-menu__nav\" aria-label=\"Menu mobilne\">\n          <a href=\"/\">Market</a>\n          <a href=\"/nowe.html\">Nowe</a>\n          <a href=\"/uzywane.html\">Używane</a>\n          <a href=\"/leasing.html\">Leasing</a>\n\n          <a href=\"https://lasertechservice.pl/\">\n            Serwis\n            <span aria-hidden=\"true\">↗</span>\n          </a>\n\n          <a href=\"/blog/\">Blog</a>\n          <a href=\"/kontakt.html\">Kontakt</a>\n        </nav>\n\n        <div class=\"mobile-menu__languages\">\n          <span class=\"mobile-menu__languages-label\"> Język </span>\n\n          <div class=\"mobile-menu__languages-list\">\n            <a class=\"is-active\" href=\"#main-content\" lang=\"pl\" aria-current=\"page\"> 🇵🇱 PL </a>\n\n            <a href=\"#main-content\" lang=\"en\" class=\"\"> 🇬🇧 EN </a>\n\n            <a href=\"#main-content\" lang=\"ru\" class=\"\"> 🇷🇺 RU </a>\n          </div>\n        </div>\n      </div>\n    </header>",
    "footer": "<footer class=\"site-footer\">\n      <div class=\"container\">\n        <div class=\"footer__grid\">\n\n          <div class=\"footer__brand\">\n            <a class=\"brand brand--footer\" href=\"/\" aria-label=\"LTS Market\">\n              <span class=\"brand__name\"> LTS <strong>MARKET</strong> </span>\n\n              <span class=\"brand__subtitle\">\n                PROFESSIONAL BEAUTY EQUIPMENT\n              </span>\n            </a>\n\n            <p>\n              Profesjonalne urządzenia dla branży beauty. Nowe, używane, leasing\n              i wsparcie techniczne.\n            </p>\n          </div>\n\n          <nav class=\"footer__column\" aria-label=\"LTS Market\">\n            <h2>Market</h2>\n\n            <a href=\"/nowe.html\"> Nowe urządzenia </a>\n\n            <a href=\"/uzywane.html\"> Używane urządzenia </a>\n\n            <a href=\"/leasing.html\"> Leasing </a>\n\n            <a href=\"/blog/\"> Blog </a>\n\n            <a href=\"/kontakt.html\"> Kontakt </a>\n          </nav>\n\n          <nav class=\"footer__column\" aria-label=\"Laser Tech Service\">\n            <h2>LTS</h2>\n\n            <a href=\"https://lasertechservice.pl/\"> Laser Tech Service </a>\n\n            <a href=\"https://lasertechservice.pl/uslugi/\"> Serwis urządzeń </a>\n\n            <a href=\"https://lasertechservice.pl/realizacje/\"> Realizacje </a>\n\n            <a href=\"https://lasertechservice.pl/blog/\">\n              Blog Laser Tech Service\n            </a>\n\n            <a href=\"https://lasertechservice.pl/kontakt/\"> Kontakt </a>\n          </nav>\n\n          <nav class=\"footer__column\" aria-label=\"Wybór języka\">\n            <h2>Język</h2>\n\n            <a class=\"is-active\" href=\"#main-content\" lang=\"pl\" aria-current=\"page\"> 🇵🇱 Polski </a>\n\n            <a href=\"#main-content\" lang=\"en\" class=\"\"> 🇬🇧 English </a>\n\n            <a href=\"#main-content\" lang=\"ru\" class=\"\"> 🇷🇺 Русский </a>\n          </nav>\n\n          <div class=\"footer__column\">\n            <h2>Kontakt</h2>\n\n            <a href=\"tel:+48575254431\"> +48 575 254 431 </a>\n\n            <a href=\"mailto:sales@ltsmarket.pl\"> sales@ltsmarket.pl </a>\n\n            <span> Polska </span>\n          </div>\n        </div>\n\n        <div class=\"footer__bottom\">\n          <div class=\"footer__legal\">\n            <span> LTS Market © 2026 </span>\n\n            <a href=\"/polityka-prywatnosci.html\"> Informacje o prywatności </a>\n          </div>\n\n          <div class=\"footer__creator\">\n            Created by\n\n            <a href=\"https://raccoon-studio.com.ua/\" target=\"_blank\" rel=\"noopener noreferrer\">\n              Raccoon Studio\n            </a>\n\n            © 2026\n          </div>\n        </div>\n      </div>\n    </footer>"
  },
  "en": {
    "header": "<header class=\"site-header\" id=\"site-header\">\n      <div class=\"container header__container\">\n        <a class=\"brand\" href=\"/en/\" aria-label=\"LTS Market — home\">\n          <span class=\"brand__name\"> LTS <strong>MARKET</strong> </span>\n\n          <span class=\"brand__subtitle\"> PROFESSIONAL BEAUTY EQUIPMENT </span>\n        </a>\n\n        <nav class=\"desktop-nav\" aria-label=\"Main navigation\">\n          <a class=\"desktop-nav__link\" href=\"/en/\"> Market </a>\n\n          <a class=\"desktop-nav__link\" href=\"/en/nowe.html\"> New </a>\n\n          <a class=\"desktop-nav__link\" href=\"/en/uzywane.html\"> Pre-owned </a>\n\n          <a class=\"desktop-nav__link\" href=\"/en/leasing.html\"> Leasing </a>\n\n          <a class=\"desktop-nav__link\" href=\"https://lasertechservice.pl/\">\n            Service\n            <span aria-hidden=\"true\">↗</span>\n          </a>\n\n          <a class=\"desktop-nav__link\" href=\"/en/blog/\"> Blog </a>\n\n          <a class=\"desktop-nav__link\" href=\"/en/kontakt.html\"> Contact </a>\n        </nav>\n\n        <div class=\"language-switcher\">\n          <button class=\"language-switcher__button\" id=\"language-button\" type=\"button\" aria-expanded=\"false\" aria-controls=\"language-menu\"><span aria-hidden=\"true\">🇬🇧</span><span>EN</span><span class=\"language-switcher__chevron\" aria-hidden=\"true\">▾</span></button>\n\n          <div class=\"language-switcher__menu\" id=\"language-menu\" hidden>\n            <a class=\"language-switcher__option\" href=\"#main-content\" lang=\"pl\">\n              <span aria-hidden=\"true\">🇵🇱</span>\n              <span>PL</span>\n            </a>\n\n            <a class=\"language-switcher__option is-active\" href=\"#main-content\" lang=\"en\" aria-current=\"page\">\n              <span aria-hidden=\"true\">🇬🇧</span>\n              <span>EN</span>\n            </a>\n\n            <a class=\"language-switcher__option\" href=\"#main-content\" lang=\"ru\">\n              <span aria-hidden=\"true\">🇷🇺</span>\n              <span>RU</span>\n            </a>\n          </div>\n        </div>\n\n        <button class=\"menu-toggle\" id=\"menu-toggle\" type=\"button\" aria-label=\"Open menu\" aria-expanded=\"false\" aria-controls=\"mobile-menu\">\n          <span></span>\n          <span></span>\n          <span></span>\n        </button>\n      </div>\n\n      <div class=\"mobile-menu\" id=\"mobile-menu\" hidden>\n        <nav class=\"mobile-menu__nav\" aria-label=\"Mobile menu\">\n          <a href=\"/en/\">Market</a>\n          <a href=\"/en/nowe.html\">New</a>\n          <a href=\"/en/uzywane.html\">Pre-owned</a>\n          <a href=\"/en/leasing.html\">Leasing</a>\n\n          <a href=\"https://lasertechservice.pl/\">\n            Service\n            <span aria-hidden=\"true\">↗</span>\n          </a>\n\n          <a href=\"/en/blog/\">Blog</a>\n          <a href=\"/en/kontakt.html\">Contact</a>\n        </nav>\n\n        <div class=\"mobile-menu__languages\">\n          <span class=\"mobile-menu__languages-label\"> Language </span>\n\n          <div class=\"mobile-menu__languages-list\">\n            <a class=\"\" href=\"#main-content\" lang=\"pl\"> 🇵🇱 PL </a>\n\n            <a href=\"#main-content\" lang=\"en\" class=\"is-active\" aria-current=\"page\"> 🇬🇧 EN </a>\n\n            <a href=\"#main-content\" lang=\"ru\" class=\"\"> 🇷🇺 RU </a>\n          </div>\n        </div>\n      </div>\n    </header>",
    "footer": "<footer class=\"site-footer\">\n      <div class=\"container\">\n        <div class=\"footer__grid\">\n\n          <div class=\"footer__brand\">\n            <a class=\"brand brand--footer\" href=\"/en/\" aria-label=\"LTS Market\">\n              <span class=\"brand__name\"> LTS <strong>MARKET</strong> </span>\n\n              <span class=\"brand__subtitle\">\n                PROFESSIONAL BEAUTY EQUIPMENT\n              </span>\n            </a>\n\n            <p>\n              Professional equipment for the beauty industry. New and pre-owned equipment, leasing and technical support.\n            </p>\n          </div>\n\n          <nav class=\"footer__column\" aria-label=\"LTS Market\">\n            <h2>Market</h2>\n\n            <a href=\"/en/nowe.html\"> New equipment </a>\n\n            <a href=\"/en/uzywane.html\"> Pre-owned equipment </a>\n\n            <a href=\"/en/leasing.html\"> Leasing </a>\n\n            <a href=\"/en/blog/\"> Blog </a>\n\n            <a href=\"/en/kontakt.html\"> Contact </a>\n          </nav>\n\n          <nav class=\"footer__column\" aria-label=\"Laser Tech Service\">\n            <h2>LTS</h2>\n\n            <a href=\"https://lasertechservice.pl/\"> Laser Tech Service </a>\n\n            <a href=\"https://lasertechservice.pl/uslugi/\"> Equipment servicing </a>\n\n            <a href=\"https://lasertechservice.pl/realizacje/\"> Our work </a>\n\n            <a href=\"https://lasertechservice.pl/blog/\">\n              Laser Tech Service blog\n            </a>\n\n            <a href=\"https://lasertechservice.pl/kontakt/\"> Contact </a>\n          </nav>\n\n          <nav class=\"footer__column\" aria-label=\"Language selection\">\n            <h2>Language</h2>\n\n            <a class=\"\" href=\"#main-content\" lang=\"pl\"> 🇵🇱 Polski </a>\n\n            <a href=\"#main-content\" lang=\"en\" class=\"is-active\" aria-current=\"page\"> 🇬🇧 English </a>\n\n            <a href=\"#main-content\" lang=\"ru\" class=\"\"> 🇷🇺 Русский </a>\n          </nav>\n\n          <div class=\"footer__column\">\n            <h2>Contact</h2>\n\n            <a href=\"tel:+48575254431\"> +48 575 254 431 </a>\n\n            <a href=\"mailto:sales@ltsmarket.pl\"> sales@ltsmarket.pl </a>\n\n            <span> Poland </span>\n          </div>\n        </div>\n\n        <div class=\"footer__bottom\">\n          <div class=\"footer__legal\">\n            <span> LTS Market © 2026 </span>\n\n            <a href=\"/en/polityka-prywatnosci.html\"> Privacy information </a>\n          </div>\n\n          <div class=\"footer__creator\">\n            Created by\n\n            <a href=\"https://raccoon-studio.com.ua/\" target=\"_blank\" rel=\"noopener noreferrer\">\n              Raccoon Studio\n            </a>\n\n            © 2026\n          </div>\n        </div>\n      </div>\n    </footer>"
  },
  "ru": {
    "header": "<header class=\"site-header\" id=\"site-header\">\n      <div class=\"container header__container\">\n        <a class=\"brand\" href=\"/ru/\" aria-label=\"LTS Market — главная\">\n          <span class=\"brand__name\"> LTS <strong>MARKET</strong> </span>\n\n          <span class=\"brand__subtitle\"> PROFESSIONAL BEAUTY EQUIPMENT </span>\n        </a>\n\n        <nav class=\"desktop-nav\" aria-label=\"Основная навигация\">\n          <a class=\"desktop-nav__link\" href=\"/ru/\"> Магазин </a>\n\n          <a class=\"desktop-nav__link\" href=\"/ru/nowe.html\"> Новое </a>\n\n          <a class=\"desktop-nav__link\" href=\"/ru/uzywane.html\"> Б/у </a>\n\n          <a class=\"desktop-nav__link\" href=\"/ru/leasing.html\"> Лизинг </a>\n\n          <a class=\"desktop-nav__link\" href=\"https://lasertechservice.pl/\">\n            Сервис\n            <span aria-hidden=\"true\">↗</span>\n          </a>\n\n          <a class=\"desktop-nav__link\" href=\"/ru/blog/\"> Блог </a>\n\n          <a class=\"desktop-nav__link\" href=\"/ru/kontakt.html\"> Контакты </a>\n        </nav>\n\n        <div class=\"language-switcher\">\n          <button class=\"language-switcher__button\" id=\"language-button\" type=\"button\" aria-expanded=\"false\" aria-controls=\"language-menu\"><span aria-hidden=\"true\">🇷🇺</span><span>RU</span><span class=\"language-switcher__chevron\" aria-hidden=\"true\">▾</span></button>\n\n          <div class=\"language-switcher__menu\" id=\"language-menu\" hidden>\n            <a class=\"language-switcher__option\" href=\"#main-content\" lang=\"pl\">\n              <span aria-hidden=\"true\">🇵🇱</span>\n              <span>PL</span>\n            </a>\n\n            <a class=\"language-switcher__option\" href=\"#main-content\" lang=\"en\">\n              <span aria-hidden=\"true\">🇬🇧</span>\n              <span>EN</span>\n            </a>\n\n            <a class=\"language-switcher__option is-active\" href=\"#main-content\" lang=\"ru\" aria-current=\"page\">\n              <span aria-hidden=\"true\">🇷🇺</span>\n              <span>RU</span>\n            </a>\n          </div>\n        </div>\n\n        <button class=\"menu-toggle\" id=\"menu-toggle\" type=\"button\" aria-label=\"Открыть меню\" aria-expanded=\"false\" aria-controls=\"mobile-menu\">\n          <span></span>\n          <span></span>\n          <span></span>\n        </button>\n      </div>\n\n      <div class=\"mobile-menu\" id=\"mobile-menu\" hidden>\n        <nav class=\"mobile-menu__nav\" aria-label=\"Мобильное меню\">\n          <a href=\"/ru/\">Магазин</a>\n          <a href=\"/ru/nowe.html\">Новое</a>\n          <a href=\"/ru/uzywane.html\">Б/у</a>\n          <a href=\"/ru/leasing.html\">Лизинг</a>\n\n          <a href=\"https://lasertechservice.pl/\">\n            Сервис\n            <span aria-hidden=\"true\">↗</span>\n          </a>\n\n          <a href=\"/ru/blog/\">Блог</a>\n          <a href=\"/ru/kontakt.html\">Контакты</a>\n        </nav>\n\n        <div class=\"mobile-menu__languages\">\n          <span class=\"mobile-menu__languages-label\"> Язык </span>\n\n          <div class=\"mobile-menu__languages-list\">\n            <a class=\"\" href=\"#main-content\" lang=\"pl\"> 🇵🇱 PL </a>\n\n            <a href=\"#main-content\" lang=\"en\" class=\"\"> 🇬🇧 EN </a>\n\n            <a href=\"#main-content\" lang=\"ru\" class=\"is-active\" aria-current=\"page\"> 🇷🇺 RU </a>\n          </div>\n        </div>\n      </div>\n    </header>",
    "footer": "<footer class=\"site-footer\">\n      <div class=\"container\">\n        <div class=\"footer__grid\">\n\n          <div class=\"footer__brand\">\n            <a class=\"brand brand--footer\" href=\"/ru/\" aria-label=\"LTS Market\">\n              <span class=\"brand__name\"> LTS <strong>MARKET</strong> </span>\n\n              <span class=\"brand__subtitle\">\n                PROFESSIONAL BEAUTY EQUIPMENT\n              </span>\n            </a>\n\n            <p>\n              Профессиональное оборудование для индустрии красоты. Новые и б/у аппараты, лизинг и техническая поддержка.\n            </p>\n          </div>\n\n          <nav class=\"footer__column\" aria-label=\"LTS Market\">\n            <h2>Магазин</h2>\n\n            <a href=\"/ru/nowe.html\"> Новое оборудование </a>\n\n            <a href=\"/ru/uzywane.html\"> Б/у оборудование </a>\n\n            <a href=\"/ru/leasing.html\"> Лизинг </a>\n\n            <a href=\"/ru/blog/\"> Блог </a>\n\n            <a href=\"/ru/kontakt.html\"> Контакты </a>\n          </nav>\n\n          <nav class=\"footer__column\" aria-label=\"Laser Tech Service\">\n            <h2>LTS</h2>\n\n            <a href=\"https://lasertechservice.pl/\"> Laser Tech Service </a>\n\n            <a href=\"https://lasertechservice.pl/uslugi/\"> Сервис оборудования </a>\n\n            <a href=\"https://lasertechservice.pl/realizacje/\"> Наши работы </a>\n\n            <a href=\"https://lasertechservice.pl/blog/\">\n              Блог Laser Tech Service\n            </a>\n\n            <a href=\"https://lasertechservice.pl/kontakt/\"> Контакты </a>\n          </nav>\n\n          <nav class=\"footer__column\" aria-label=\"Выбор языка\">\n            <h2>Язык</h2>\n\n            <a class=\"\" href=\"#main-content\" lang=\"pl\"> 🇵🇱 Polski </a>\n\n            <a href=\"#main-content\" lang=\"en\" class=\"\"> 🇬🇧 English </a>\n\n            <a href=\"#main-content\" lang=\"ru\" class=\"is-active\" aria-current=\"page\"> 🇷🇺 Русский </a>\n          </nav>\n\n          <div class=\"footer__column\">\n            <h2>Контакты</h2>\n\n            <a href=\"tel:+48575254431\"> +48 575 254 431 </a>\n\n            <a href=\"mailto:sales@ltsmarket.pl\"> sales@ltsmarket.pl </a>\n\n            <span> Польша </span>\n          </div>\n        </div>\n\n        <div class=\"footer__bottom\">\n          <div class=\"footer__legal\">\n            <span> LTS Market © 2026 </span>\n\n            <a href=\"/ru/polityka-prywatnosci.html\"> Информация о конфиденциальности </a>\n          </div>\n\n          <div class=\"footer__creator\">\n            Created by\n\n            <a href=\"https://raccoon-studio.com.ua/\" target=\"_blank\" rel=\"noopener noreferrer\">\n              Raccoon Studio\n            </a>\n\n            © 2026\n          </div>\n        </div>\n      </div>\n    </footer>"
  }
};
  function setLanguage(lang) {
    const text = copy[lang];
    const prefix = lang === 'pl' ? '/' : '/' + lang + '/';
    const routes = {home: prefix, new: prefix + 'nowe.html', used: prefix + 'uzywane.html', contact: prefix + 'kontakt.html'};
    document.documentElement.lang = lang;
    document.title = '404 — ' + text.error + ' | LTS Market';
    document.querySelector('meta[name="description"]').content = text.title + ' ' + text.message;
    document.querySelectorAll('[data-copy]').forEach(el => { el.textContent = text[el.dataset.copy]; });
    document.querySelectorAll('[data-route]').forEach(el => { el.href = routes[el.dataset.route]; });
    document.querySelector('.error-visual img').alt = text.alt;
    document.querySelector('.site-header').outerHTML = chrome[lang].header;
    document.querySelector('.site-footer').outerHTML = chrome[lang].footer;
    document.querySelectorAll('a[lang]').forEach(el => { el.href = location.pathname + location.search + location.hash; });
    document.body.classList.remove('menu-open');
    updateHeader();
  }
  function updateHeader() {
    document.querySelector('.site-header').classList.toggle('is-scrolled', scrollY > 20);
  }
  function closeMenus() {
    document.querySelector('#language-menu').hidden = true;
    document.querySelector('#language-button').setAttribute('aria-expanded', 'false');
    document.querySelector('#mobile-menu').hidden = true;
    const toggle = document.querySelector('#menu-toggle');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.classList.remove('is-active');
    toggle.setAttribute('aria-label', {pl:'Otwórz menu', en:'Open menu', ru:'Открыть меню'}[document.documentElement.lang]);
    document.body.classList.remove('menu-open');
  }
  document.addEventListener('click', event => {
    const language = event.target.closest('a[lang]');
    if (language && copy[language.lang]) {
      event.preventDefault();
      const desktop = Boolean(language.closest('#language-menu'));
      setLanguage(language.lang);
      if (desktop) document.querySelector('#language-button').focus();
      return;
    }
    if (event.target.closest('#language-button')) {
      const menu = document.querySelector('#language-menu');
      menu.hidden = !menu.hidden;
      document.querySelector('#language-button').setAttribute('aria-expanded', String(!menu.hidden));
      return;
    }
    if (event.target.closest('#menu-toggle')) {
      const menu = document.querySelector('#mobile-menu');
      const toggle = document.querySelector('#menu-toggle');
      menu.hidden = !menu.hidden;
      toggle.setAttribute('aria-expanded', String(!menu.hidden));
      toggle.classList.toggle('is-active', !menu.hidden);
      toggle.setAttribute('aria-label', (menu.hidden ? {pl:'Otwórz menu',en:'Open menu',ru:'Открыть меню'} : {pl:'Zamknij menu',en:'Close menu',ru:'Закрыть меню'})[document.documentElement.lang]);
      document.body.classList.toggle('menu-open', !menu.hidden);
      return;
    }
    if (!event.target.closest('.language-switcher')) {
      document.querySelector('#language-menu').hidden = true;
      document.querySelector('#language-button').setAttribute('aria-expanded', 'false');
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    const target = !document.querySelector('#language-menu').hidden ? '#language-button' : !document.querySelector('#mobile-menu').hidden ? '#menu-toggle' : null;
    closeMenus();
    if (target) document.querySelector(target).focus();
  });
  window.addEventListener('scroll', updateHeader, {passive:true});
  matchMedia('(min-width: 1024px)').addEventListener('change', event => { if (event.matches) closeMenus(); });
  setLanguage(location.pathname.match(/^\/(en|ru)(?:\/|$)/)?.[1] || 'pl');
})();
