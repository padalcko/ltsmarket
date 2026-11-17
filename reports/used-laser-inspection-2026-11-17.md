# Стаття про підбір уживаного лазера — 17.11.2026

Інтегровано дослівні PL/RU/EN тексти з наданого завдання через чинні `scripts/blog-posts.json` і `scripts/build-blog.py`. Дата: 17.11.2026; локалізоване авторство: LTS Market у співпраці з Laser Tech Service.

## Нові статті

- `blog/zakup-uzywanego-lasera-diagnostyka/index.html`
- `ru/blog/pokupka-bu-lazera-diagnostika/index.html`
- `en/blog/used-aesthetic-laser-inspection/index.html`

Для кожної створено `index.md`. Чинна пагінація по чотири картки автоматично додала `blog/page/2/index.html`, `ru/blog/page/2/index.html`, `en/blog/page/2/index.html` і відповідні Markdown-файли.

## Підготовлені URL

- https://ltsmarket.pl/blog/zakup-uzywanego-lasera-diagnostyka/
- https://ltsmarket.pl/ru/blog/pokupka-bu-lazera-diagnostika/
- https://ltsmarket.pl/en/blog/used-aesthetic-laser-inspection/

Польська версія відповідає чинній структурі без `/pl/`.

## Зміни

Оновлено три списки блогу, sitemap та похідні AI-ресурси (`llms.txt`, `llms-full.txt`, `ai-catalog.json`, Markdown, `_headers`). Генератор отримав опційну підтримку HTML-списків, вступу, авторства, дати та вимкнення додаткового шаблонного CTA. Обробник AI-ресурсів і валідатор підтримують запитані регіональні hreflang `pl-PL` / `ru-RU`.

CSS, JS, хедер, футер, старі статті й товарні сторінки не змінені. Нових залежностей і зображень немає; соціальні метадані використовують наявне стандартне зображення шаблону. Завершальні URL з авторського тексту збережені; контекстні посилання ведуть до відповідного каталогу LTS Market і мовних сторінок Laser Tech Service.

## Перевірки

- Дослівність: PL 65, RU 67, EN 74 блоки — повний збіг із вкладенням, включно із заголовками, списками, ціною та гарантією.
- Унікальні title/description/H1, self-canonical, взаємні hreflang і x-default; Open Graph, Twitter Card без дублів.
- BlogPosting + BreadcrumbList, дата й авторство; без вигаданого FAQ або рейтингів.
- Нові URL та відповідні hreflang у sitemap; усі локальні посилання існують.
- `check-ai-search.py`: PASS, 66 сторінок.
- `check-seo.py`: PASS, 67 HTML-сторінок.
- `audit-site.py`: 0 помилок.
- `git diff --check`: PASS.
- Chrome/Playwright: PL/RU/EN × 320, 375, 430, 768, 1440 px — 15/15 PASS, без горизонтального прокручування. Перевірено десктопні мовні посилання та фактичний перехід до іншої мовної версії; списки блогу перевірено на 320 px. Знімки: `/tmp/lts-inspection/`.

## Публікація

Зміни лише локальні. Commit, push та production-deploy не виконувалися. У репозиторії немає налаштованого доступного каналу деплою; публікація та індексація нових URL не підтверджені.
