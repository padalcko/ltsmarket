import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";
import path from "node:path";
import { fileURLToPath } from "node:url";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
function run(file, globals) {
  vm.runInNewContext(fs.readFileSync(path.join(root, file), "utf8"), globals);
}
class Element {
  constructor() { this.events = {}; this.attrs = {}; this.dataset = {}; this.children = []; this.classes = new Set(); this.style = {}; this.classList = { add: c => this.classes.add(c), remove: (...cs) => cs.forEach(c => this.classes.delete(c)), contains: c => this.classes.has(c), toggle: (c, v = !this.classes.has(c)) => { v ? this.classes.add(c) : this.classes.delete(c); return v; } }; }
  addEventListener(name, fn) { (this.events[name] ||= []).push(fn); }
  fire(name, event = {}) { (this.events[name] || []).forEach(fn => fn(event)); }
  setAttribute(k,v) { this.attrs[k] = v; }
  getAttribute(k) { return this.attrs[k]; }
  removeAttribute(k) { delete this.attrs[k]; }
  append(el) { this.children.push(el); }
  focus() { this.focused = true; }
  querySelector(selector) { return this.nodes?.[selector] || null; }
}
// Gallery: a failed load retains the last good photo; a late load cannot override the newest request.
{
  const gallery = new Element(); const main = new Element(); main.attrs.src = 'original.webp'; main.closest = () => gallery;
  const thumbs = ['original.webp','one.webp','two.webp'].map(url => { const e = new Element(); e.dataset = { image: url, alt: url }; return e; });
  thumbs[0].classes.add('is-active');
  const pending = [];
  const document = { addEventListener: (_, fn) => fn(), querySelector: () => main, querySelectorAll: () => thumbs, createElement: () => new Element() };
  run('assets/js/produkt-uzywany.js', { document, Image: class { constructor() { pending.push(this); } } });
  thumbs[1].fire('click'); pending[0].onerror();
  assert.equal(main.attrs.src, 'original.webp'); assert.match(gallery.children[0].textContent, /Nie udało/);
  thumbs[1].fire('click'); thumbs[2].fire('click');
  pending[2].onload(); pending[1].onload();
  assert.equal(main.src, 'two.webp'); assert.equal(thumbs[2].attrs['aria-pressed'], 'true');
  console.log('PASS: gallery errors and out-of-order image responses');
}
// Consent: no analytics before opt-in; refusal persists; withdrawal disables and unloads analytics.
for (const saved of [null, 'denied', 'granted']) {
  const head = new Element(); const body = new Element(); const settings = new Element();
  const nodes = Object.fromEntries(['h2','p','a','[data-reject]','[data-accept]'].map(k => [k,new Element()]));
  const panel = new Element(); panel.nodes = nodes;
  const stored = new Map(saved ? [['lts-analytics-consent-v1',saved]] : []);
  let reloads = 0;
  const window = { addEventListener() {} };
  const document = { documentElement: {lang:'en'}, cookie:'_ga=old; _ga_1Z98BZS3WW=old', head, body, addEventListener: (_,fn) => fn(), createElement: tag => tag === 'section' ? panel : new Element(), querySelectorAll: () => [settings] };
  run('assets/js/privacy.js', { window, document, location: { hostname:'ltsmarket.pl', reload() { reloads++; } }, localStorage: {getItem:k=>stored.get(k),setItem:(k,v)=>stored.set(k,v)} });
  assert.equal(head.children.length, saved === 'granted' ? 1 : 0);
  if (saved !== 'granted') {
    nodes['[data-reject]'].fire('click');
    assert.equal(head.children.length,0); assert.equal(stored.get('lts-analytics-consent-v1'),'denied');
    settings.fire('click'); nodes['[data-accept]'].fire('click');
    assert.equal(head.children.length,1); assert.equal(window['ga-disable-G-1Z98BZS3WW'],false);
  }
  settings.fire('click'); nodes['[data-reject]'].fire('click');
  assert.equal(window['ga-disable-G-1Z98BZS3WW'],true); assert.equal(reloads,1);
}
console.log('PASS: analytics opt-in, refusal, saved choices and withdrawal');
// Carousel: reduced motion, keyboard focus and user pause all prevent autoplay.
for (const reduced of [false, true]) {
  const slider = new Element(), visual = new Element(), pause = new Element();
  const slides = [new Element(),new Element(),new Element()];
  slider.querySelectorAll = () => slides; slider.closest = () => visual;
  let active = null; visual.contains = el => el === pause;
  let timers = new Set(), nextTimer = 0;
  const media = {matches:reduced,addEventListener(){}};
  const document = {hidden:false, get activeElement(){return active;}, addEventListener(name,fn){if(name==='DOMContentLoaded')fn();}, documentElement:{lang:'en'}, querySelector: q => ({'[data-product-slider]':slider,'[data-slider-pause]':pause})[q] || null, querySelectorAll:()=>[]};
  const window = { matchMedia:()=>media, addEventListener(){}, setTimeout:fn=>fn(), setInterval:()=>{timers.add(++nextTimer);return nextTimer;}, clearInterval:id=>timers.delete(id), scrollY:0 };
  run('assets/js/main.js',{document,window});
  assert.equal(timers.size,reduced?0:1);
  if (!reduced) {
    pause.fire('click'); assert.equal(timers.size,0);
    pause.fire('click'); assert.equal(timers.size,1);
    active=pause;visual.fire('focusin');assert.equal(timers.size,0);
    active=null;visual.fire('focusout');assert.equal(timers.size,1);
    visual.fire('mouseenter'); assert.equal(timers.size,0);
    visual.fire('mouseleave'); assert.equal(timers.size,1);
  }
}
console.log('PASS: carousel reduced motion, manual pause, focus and hover');
