// Local integration QA; Google scripts are mocked, no analytics hits are sent.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert=require('node:assert/strict');
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true});let requests=[];const errors=[];
page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(r.url().includes('googletagmanager.com')) requests.push(r.url())});
await page.route(/googletagmanager.com|google-analytics.com/,r=>r.fulfill({status:200,body:'',contentType:'application/javascript'}));
for(const prefix of ['', '/en','/ru']) for(const route of ['/', '/nowe.html','/uzywane.html','/leasing.html','/kontakt.html','/blog/']){
requests=[];await page.goto((process.env.TEST_BASE_URL || 'http://127.0.0.1:8798')+prefix+route);await page.waitForLoadState('networkidle');
assert.equal(requests.filter(u=>u.includes('/gtm.js?id=GTM-T9T228H6')).length,1);
assert.equal(requests.filter(u=>u.includes('/gtag/js?id=G-1Z98BZS3WW')).length,1);
const state=await page.evaluate(()=>({starts:dataLayer.filter(x=>x.event==='gtm.js').length,configs:dataLayer.filter(x=>x[0]==='config').length,phones:[...document.querySelectorAll('a[href^="tel:"]')].map(x=>x.getAttribute('href'))}));assert.equal(state.starts,1);assert.equal(state.configs,1);assert(state.phones.length);assert(state.phones.every(x=>x==='tel:+48575254431'));
await page.locator('a[href^="tel:"]').first().evaluate(el=>el.addEventListener('click',e=>{e.preventDefault();window.qaTel=e.currentTarget.href},{once:true}));await page.locator('a[href^="tel:"]').first().click();assert.equal(await page.evaluate(()=>window.qaTel),'tel:+48575254431');
console.log('PASS',prefix+route);
}assert.deepEqual(errors,[]);await browser.close();console.log('PASS mobile clicks, single GTM request/start and GA4 config; external scripts mocked, not GA delivery');})();
