# MEDIflex US450 — звіт, 29.10.2026

Реалізовано локально в LTS Market та Laser Tech Service. Commit, push і deploy не виконувалися.

## Факти та зміст

- MEDIflex — комерційна назва; US450 — модель за табличкою. Рік 2022, ціна 40 000 PLN, стан б/у, справний, у хорошому технічному стані.
- 755/808/1064 nm; заявлена потужність діода 2000 W. **Максимальна споживана потужність 5000 W** — фото IMG_7740 та явне підтвердження користувача замість первісних 6000 W. Живлення AC 220 V, 50/60 Hz.
- Обслуговування Laser Tech Service 15.10.2026: усі фільтри, повна заміна рідини, внутрішнє очищення, огляд маніпули, заміна охолоджувального елемента та перевірка працездатності.
- Книжка з інформацією про апарат і сервіс. Гарантія 6 місяців **лише на виконані роботи**, явно відокремлена від гарантії на весь апарат; гарантії у Product/Offer не додано.
- Дві маніпули показані на реальних фото; їх наявність у комплектації не обіцяється. Непідтверджених вимірювань, ресурсу, калібрування або заміни діода немає.

## URL після публікації

- https://ltsmarket.pl/uzywane/mediflex-us450.html
- https://ltsmarket.pl/en/uzywane/mediflex-us450.html
- https://ltsmarket.pl/ru/uzywane/mediflex-us450.html

Усі три маршрути перевірено локально HTTP 200. Публікації нових сторінок ще не було.

## Позиція та дизайн

Перший товар на головних PL/EN/RU та в усіх трьох каталогах. Після нього порядок збережено:
3D CONTOUR → MEDILASE PRO → Chungwoo ELLISYS PLUS → DaeYang CARBO 3000.
Старі картки, 12 існуючих товарних сторінок і header/footer шести змінених списків побайтово збігаються з HEAD.
Використано шаблон MEDILASE PRO, наявні класи та js/uzywane.js. CSS, шрифти, кольори, спільна навігація, webhook і GA4 loader не змінювалися.

## Фотографії

Усі 10 оригіналів HEIC перетворені без ретуші або кадрування. Орієнтація врахована; співвідношення 9:16 збережене.
Повні WebP: 1080×1920; мініатюри: 135×240; картка головного фото: 360×640. Якість WebP 88, загалом 21 файл / 1 976 384 байти (~1,88 MiB).
У кожного ракурсу унікальний ALT на PL/EN/RU. Основне фото — IMG_7722.

| Оригінал | WebP у assets/img/uzywane/mediflex-us450/ |
|---|---|
| IMG_7722.heic | mediflex-us450-laser-diodowy-front.webp |
| IMG_7728.heic | mediflex-us450-panel-sterowania.webp |
| IMG_7736.heic | mediflex-us450-parametry-pracy.webp |
| IMG_7737.heic | mediflex-us450-widok-przod.webp |
| IMG_7738.heic | mediflex-us450-widok-bok.webp |
| IMG_7739.heic | mediflex-us450-widok-tyl.webp |
| IMG_7740.heic | mediflex-us450-tabliczka-znamionowa.webp |
| IMG_7741.heic | mediflex-us450-glowica-laserowa.webp |
| IMG_7742.heic | mediflex-us450-okno-glowicy.webp |
| IMG_7743.heic | mediflex-us450-druga-glowica.webp |

Для кожного файлу також створено `-thumb.webp`; для першого — `-card.webp`. Повне зіставлення та ALT: `scripts/mediflex-images.json`.

## SEO та AI

PASS: унікальні title/description, один H1, H2, canonical, взаємні PL/EN/RU hreflang і x-default, Open Graph/Twitter з правильними розмірами фото; Product, Offer і BreadcrumbList валідно парсяться.
Offer: 40000 PLN, UsedCondition, InStock. Немає вигаданих рейтингів або відгуків.
Sitemap містить три нові URL та мовні альтернативи; локальні посилання й якорі перевірені.
У цьому checkout раніше не було ai-catalog.json/llms.txt. Додано генератор із наявного HTML та 15 мовних записів для п'яти вживаних товарів. MEDIflex перший у кожній мові, з точними технічними/сервісними фактами й обмеженням гарантії. Перевірка актуальності пройшла.
robots.txt залишено без змін. Наявний blog generator не замінено.
Валідатори оновлено для п'ятого товару, URL-елементів BreadcrumbList та службового Google verification HTML, який не є контентною сторінкою.

## Двосторонні посилання

- Кожна сторінка MEDIflex → https://lasertechservice.pl/ або відповідна /en/, /ru/.
- Laser Tech Service /partnerzy/ → https://ltsmarket.pl/uzywane.html
- Laser Tech Service /en/partners/ → https://ltsmarket.pl/en/uzywane.html
- Laser Tech Service /ru/partnerzy/ → https://ltsmarket.pl/ru/uzywane.html

Усі шість цільових зовнішніх URL фактично повернули HTTP 200. Звичайні HTML-посилання без nofollow/sponsored. Зворотні блоки використовують існуючий темний стиль partners-hero; header/footer та картки партнерів не змінені. Окремих SEO-сторінок і масових посилань не створено.

## Форми та перевірки

- `audit-site.py`: 48 сторінок, 0 помилок.
- `check-seo.py`: 48 сторінок, 3 ItemList, 27 Product, GA4 та зображення — PASS.
- `check-mediflex.py`: 3 товарні сторінки, 6 перших карток, усі зображення, схема та AI — PASS.
- `build-ai-catalog.py --check`: PASS.
- `test-analytics.js`, `test-ui.js`, `test-forms.js` для всіх 6 форм — PASS: валідація, payload, подвійне надсилання, HTTP failure, тайм-аут і success.
- Chrome/Playwright: 45 комбінацій сторінка/ширина (9 сторінок × 320/375/430/768/1440), без горизонтального overflow. Перемикання усіх 10 фото для кожної мови, мобільне меню, мовні URL, порядок карток — PASS. Додатково перевірено завантаження фото всіх п'яти карток на шести списках.
- Клієнтський тест справжньої форми PL/EN/RU з перехопленим POST: назва MEDIflex US450, абсолютний productUrl, language, source, категорія вживаної техніки та дані покупця. Редагування message не втрачає productName/productUrl.
- CORS production n8n: OPTIONS → HTTP 204, Allow-Origin https://ltsmarket.pl, дозволено POST та content-type.
- Laser Tech Service: check-ai-search.py та check-geo-seo.py — без issues; check-ai-catalog.py завершився PASS. Оновлено три Markdown-копії партнерів та llms-full.txt; build-ai-search.py --check перевіряє актуальність. Браузер: три додані блоки при 375/1440 px.
- `git diff --check` — PASS в обох репозиторіях.

## Межі перевірки

Реальний POST у production n8n не надсилався: доставка листа/заявки та виконання workflow не підтверджені. GA4 Realtime, Google Rich Results Test, Lighthouse/CWV та індексація пошуковиками не перевірялися. Браузерна перевірка виконана локально в Chrome, не на фізичному смартфоні. Нові сторінки ще не опубліковані.

## Нові файли LTS Market

- `ai-catalog.json`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-druga-glowica-thumb.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-druga-glowica.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-glowica-laserowa-thumb.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-glowica-laserowa.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-laser-diodowy-front-card.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-laser-diodowy-front-thumb.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-laser-diodowy-front.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-okno-glowicy-thumb.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-okno-glowicy.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-panel-sterowania-thumb.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-panel-sterowania.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-parametry-pracy-thumb.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-parametry-pracy.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-tabliczka-znamionowa-thumb.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-tabliczka-znamionowa.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-widok-bok-thumb.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-widok-bok.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-widok-przod-thumb.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-widok-przod.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-widok-tyl-thumb.webp`
- `assets/img/uzywane/mediflex-us450/mediflex-us450-widok-tyl.webp`
- `en/uzywane/mediflex-us450.html`
- `llms.txt`
- `ru/uzywane/mediflex-us450.html`
- `scripts/build-ai-catalog.py`
- `scripts/check-mediflex-browser.cjs`
- `scripts/check-mediflex.py`
- `scripts/mediflex-images.json`
- `uzywane/mediflex-us450.html`
- `reports/mediflex-us450.md` (цей звіт)

## Змінені файли LTS Market

- `README.md`
- `en/index.html`
- `en/js/kontakt.js`
- `en/uzywane.html`
- `index.html`
- `js/kontakt.js`
- `ru/index.html`
- `ru/js/kontakt.js`
- `ru/uzywane.html`
- `scripts/audit-site.py`
- `scripts/check-seo.py`
- `sitemap.xml`
- `uzywane.html`

## Змінені файли Laser Tech Service

- `en/partners/index.html`
- `en/partners/index.md`
- `llms-full.txt`
- `partnerzy/index.html`
- `partnerzy/index.md`
- `ru/partnerzy/index.html`
- `ru/partnerzy/index.md`
