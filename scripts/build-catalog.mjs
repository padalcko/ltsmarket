// Regenerate static product cards from the same data and renderers used by the browser.
// Run: node scripts/build-catalog.mjs
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
for (const lang of ["pl", "en", "ru"]) {
  for (const home of [false, true]) {
    const prefix = lang === "pl" ? "" : lang + "/";
    const filename = prefix + (home ? "index.html" : "uzywane.html");
    const grid = { innerHTML: "", querySelectorAll: () => [] };
    const selector = home ? "#used-products-home" : "[data-products-grid]";
    const context = vm.createContext({
      console,
      window: { location: { pathname: "/" + filename } },
      document: {
        documentElement: { lang },
        addEventListener: (_, callback) => callback(),
        querySelector: (query) => query === selector ? grid : null,
        querySelectorAll: () => [],
      },
    });
    vm.runInContext(fs.readFileSync(path.join(root, "assets/js/used-products.js"), "utf8"), context);
    vm.runInContext(fs.readFileSync(path.join(root, `assets/js/${home ? "used-products-home" : "uzywane"}.js`), "utf8"), context);
    const file = path.join(root, filename);
    let html = fs.readFileSync(file, "utf8");
    const start = "<!-- generated:products:start -->";
    const end = "<!-- generated:products:end -->";
    const content = `${start}\n${grid.innerHTML}\n${end}`;
    if (html.includes(start)) {
      html = html.slice(0, html.indexOf(start)) + content + html.slice(html.indexOf(end) + end.length);
    } else {
      const opening = home ? '<div class="products-grid" id="used-products-home">' : '<div class="used-products-grid" data-products-grid>';
      const emptyGrid = home
        ? /<div\s+class="products-grid"\s+id="used-products-home"\s*>\s*<\/div>/
        : /<div\s+class="used-products-grid"\s+data-products-grid\s*>\s*<\/div>/;
      if (!emptyGrid.test(html)) throw new Error(`Missing grid in ${filename}`);
      html = html.replace(emptyGrid, opening + content + "</div>");
    }
    fs.writeFileSync(file, html.replace(/[ \t]+$/gm, ""));
    console.log(filename);
  }
}
