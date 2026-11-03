# Підготовка LTS Market для ШІ

Дата: 2026-11-03. Зміни виконано локально, без commit, push або deploy.

## Перевірений приклад

Прочитано чинну локальну реалізацію `/Users/macbookpro/Documents/GitHub/laser-tech-service`: `scripts/build-ai-search.py`, `scripts/build-ai-catalog.py`, `scripts/check-ai-search.py`, `scripts/build-site.py`, `llms.txt`, `_headers` та структуру вихідних ресурсів. Репозиторій Laser Tech Service не змінювався. Це порівняння локальних реалізацій, а не аудит production-відповідей сайтів.

## Порівняння і результат

| Механізм у Laser Tech Service | Реалізація в LTS Market |
|---|---|
| HTML як джерело істини | Поточний локальний HTML; без нових рекламних чи технічних тверджень |
| Published registry + sitemap | Чинний sitemap + перевірка canonical/hreflang; окремий дубль маршрутів не створено |
| Markdown кожної сторінки | 60 файлів: по 20 PL/EN/RU |
| llms.txt | Категоризований індекс усіх 60 сторінок, HTML і Markdown |
| llms-full.txt | Повний зміст сторінок із джерелами та мовними відповідниками |
| AI Catalog | 60 записів сторінок та 27 товарних записів: 12 нових + 15 вживаних мовних версій |
| Discovery в HTML | rel=alternate type=text/markdown та rel=describedby /llms.txt у head |
| HTTP canonical/MIME | `_headers` з точними адресами Markdown, canonical на HTML, Content-Type та nosniff |
| Автоматична перевірка | Актуальність, зміст, посилання, таблиці/FAQ, мови, robots та локальний HTTP |
| Єдиний build | `python3 scripts/build-site.py` |

## Джерела, вміст і маршрути

Markdown зберігає заголовки, описи, абзаци, ціни, технічні таблиці, FAQ, посилання та змістовні зображення. Навігація, форми, поля вводу, приховані елементи, кнопки та декоративні SVG-схеми не потрапляють до машинної версії. JSON-каталог копіює наявні Product та інші структуровані дані, додає URL джерела, Markdown, мову, мовні відповідники й SHA-256 згенерованого змісту. Наявні owner/nameplate verifiedFacts MEDIflex та позиції вживаних товарів збережені.

Приклади:

- `/` → `/index.md`
- `/leasing.html` → `/leasing.md`
- `/en/kontakt.html` → `/en/kontakt.md`
- `/uzywane/mediflex-us450.html` → `/uzywane/mediflex-us450.md`
- `/nowe/alpha/` → `/nowe/alpha/index.md`
- `/ru/novye/ray/` → `/ru/novye/ray/index.md`
- статті блогу → сусідній `index.md`

Публічні допоміжні ресурси після майбутнього розгортання: `/llms.txt`, `/llms-full.txt`, `/ai-catalog.json`.

Списки не містять README, звітів, файлу підтвердження Google або сторінок поза sitemap. Markdown не додано до sitemap; основними залишаються HTML URL. Застарілі Markdown від видалених маршрутів позначаються для ручного перегляду, не видаляються автоматично.

## Збережені межі

Порівняно 82 початкові файли HTML/CSS/JS/robots/sitemap із знімком перед цією задачею. У HTML змінився лише блок discovery у head; весь видимий HTML, заголовки, посилання у body, форми, аналітика, CSS та JS збережені. Вилучені раніше блоки схожих апаратів не повернулися. Посилання Laser Tech Service у заголовках не відновлено.

Не змінено URL, canonical/hreflang, sitemap, robots, ціни, характеристики або наявні JSON-LD. Дані Laser Tech Service як продавця не копіювалися: LTS Market залишається продавцем, сервісні згадки залишаються такими, як у вихідних сторінках.

## Перевірки

- `python3 scripts/build-site.py`: PASS.
- `python3 scripts/build-ai-search.py --check`: PASS, 60 Markdown актуальні.
- `python3 scripts/build-ai-catalog.py --check`: PASS.
- `python3 scripts/check-ai-search.py`: PASS — 2 430 змістових блоків, 600 перевірок доступу ботів для HTML/Markdown, 819 внутрішніх посилань у Markdown/LLM-ресурсах.
- Поточний robots дозволяє Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, PerplexityBot. Політика robots залишена без змін.
- `python3 scripts/check-ai-search.py --http http://127.0.0.1:8793`: PASS — 123 ресурси повертають HTTP 200 та точно відповідають згенерованим байтам.
- `python3 scripts/audit-site.py`: 60 HTML, 0 помилок.
- `python3 scripts/check-seo.py`: 60 HTML, 39 Product-об’єктів разом із каталогами, PASS.
- `python3 scripts/check-alpha-ray.py`: 478 авторських текстових блоків збережені, PASS.
- Генератори Alpha/Ray, Lumos і Alpha Mini пройшли `--check`; discovery підтримується спільним `site_content.py`.
- Тимчасовий тест нового товару: три нові локалізовані маршрути автоматично потрапили до Markdown, llms, llms-full і headers без ручного списку. Тестові сторінки не додані до сайту.
- `git diff --check`: PASS.

Окремий візуальний браузерний прогін для цієї задачі не потрібен і не виконувався: байтове порівняння підтвердило незмінність body/CSS/JS. HTTP перевірки виконано через простий локальний сервер, який не застосовує `_headers`: MIME/canonical-конфігурація перевірена статично, її застосування на production не підтверджене. `_headers` призначений для сумісного хостингу (як Netlify); інший сервер потребує відповідної конфігурації.

Наявність цих ресурсів не гарантує індексацію чи цитування відповідями ШІ. Live-індексацію, відповіді ШІ та production заголовки не перевіряли.

## Файли та подальша робота

Нові: `scripts/ai_resources.py`, `scripts/build-ai-search.py`, `scripts/check-ai-search.py`, `scripts/build-site.py`, `_headers`, `llms-full.txt`, 60 сусідніх Markdown-файлів і цей звіт.

Оновлені: `scripts/build-ai-catalog.py`, `scripts/site_content.py`, `scripts/check-alpha-ray.py`, `llms.txt`, `ai-catalog.json`, discovery у head 60 HTML-сторінок, README та уточнення попереднього звіту Alpha/Ray.

Після зміни джерела товару чи блогу спочатку запустити відповідний генератор контенту, потім:

```sh
python3 scripts/build-site.py
```

Не редагувати Markdown/llms/AI JSON вручну. Для нової сторінки достатньо HTML з коректними мовними зв’язками та запису в sitemap. Build оновлює похідні ресурси й перевіряє сайт; нічого не комітить і не публікує.
