// Local QA. Every production webhook request is intercepted; no real leads are sent.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.TEST_BASE_URL || 'http://127.0.0.1:8791';
const routes={pl:'/nowe/alpha-mini/',en:'/en/new/alpha-mini/',ru:'/ru/novye/alpha-mini/'};
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 const page=await browser.newPage({reducedMotion:"reduce"}); const errors=[],failures=[];let payload,mode='success',posts=0;
 page.on('pageerror',e=>errors.push(String(e)));
 page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)failures.push(r.url());});
 await page.route(/google-analytics|googletagmanager/,r=>r.abort());
 await page.route('**/webhook/lts-market-lead',async r=>{posts++;payload=r.request().postDataJSON();await r.fulfill({status:mode==='success'?200:500,contentType:'application/json',body:'{}'});});
 fs.mkdirSync('/tmp/alpha-mini-qa',{recursive:true});
 for(const [lang,route] of Object.entries(routes).filter(([lang])=>!process.env.TEST_LANG || process.env.TEST_LANG===lang)){
  for(const width of [320,375,430,768,1024,1440]){
   await page.setViewportSize({width,height:900});
   const response=await page.goto(base+route);assert.equal(response.status(),200);
   await page.evaluate(()=>document.fonts.ready);
   const overflow=await page.evaluate(()=>[...document.querySelectorAll("body *")].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>({tag:e.tagName,class:e.className,width:e.getBoundingClientRect().width,scroll:e.scrollWidth,text:e.textContent.slice(0,80)})));
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${lang} overflow ${width}: ${JSON.stringify(overflow)}`);
   assert.equal(await page.locator('h1').count(),1);assert.equal(await page.locator('#faq details').count(),10);
   assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),'https://ltsmarket.pl'+route);
   await page.locator('a[href="#specification"]').click();assert(await page.locator('#specification').isVisible());
   await page.locator('#faq summary').first().click();assert(await page.locator('#faq details').first().getAttribute('open')!==null);
   await page.locator('a[href="#contact-form"]').click();assert(await page.locator('#contact-form').isVisible());
   for(const l of Object.keys(routes)){
    assert.equal(await page.locator(`.language-switcher__menu a[lang=${l}]`).getAttribute('href'),routes[l]);
    assert.equal(await page.locator(`.mobile-menu__languages-list a[lang=${l}]`).getAttribute('href'),routes[l]);
   }
   const images=await page.locator('main img').evaluateAll(imgs=>imgs.map(i=>({src:i.src,alt:i.alt,w:i.width,h:i.height})));
   assert(images.every(i=>i.alt&&i.w>0&&i.h>0));
   for(const img of await page.locator('main img').all()){await img.scrollIntoViewIfNeeded();await img.evaluate(i=>i.decode());}
   if(width===375||width===1440){await page.screenshot({path:`/tmp/alpha-mini-qa/${lang}-${width}.png`,fullPage:true});}
   if(width===375||width===1440){
    await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));await page.screenshot({path:`/tmp/alpha-mini-qa/${lang}-${width}-hero.png`});
    await page.locator('#service').scrollIntoViewIfNeeded();await page.screenshot({path:`/tmp/alpha-mini-qa/${lang}-${width}-service.png`});
   }
   if(width===375){await page.locator('#menu-toggle').click();assert(await page.locator('#mobile-menu').isVisible());await page.locator('#menu-toggle').click();}
  }
  await page.goto(base+route);await page.locator('#language-button').click();assert(await page.locator('#language-menu').isVisible());await page.locator(`#language-menu a[lang=${lang==='pl'?'en':'pl'}]`).click();assert.equal(new URL(page.url()).pathname,routes[lang==='pl'?'en':'pl']);
  await page.goto(base+route);
  await page.locator('#gallery a').click();assert(new URL(page.url()).pathname.endsWith('alpha-mini.webp'));await page.goBack();
  const before=posts;await page.locator('#contact-form button[type=submit]').click();assert.equal(posts,before);assert(await page.locator('#contact-form-status').evaluate(e=>e.classList.contains('is-error')));
  await page.locator('[name=name]').fill('Local QA');await page.locator('[name=phone]').fill('+48123456789');await page.locator('[name=email]').fill('qa@example.com');await page.locator('[name=message]').fill('Edited Alpha enquiry');await page.locator('[name=consent]').check();
  mode='failure';await page.locator('#contact-form button[type=submit]').click();await page.waitForFunction(()=>document.querySelector('#contact-form-status').classList.contains('is-error'));assert.equal(await page.locator('[name=message]').inputValue(),'Edited Alpha enquiry');
  mode='success';await page.locator('#contact-form button[type=submit]').click();await page.waitForFunction(()=>document.querySelector('#contact-form-status').classList.contains('is-success'));
  assert.equal(payload.productName,'Alpha Mini');assert.equal(payload.productUrl,'https://ltsmarket.pl'+route);assert.equal(payload.pageUrl,base+route);assert.equal(payload.language,lang);assert.equal(payload.message,'Edited Alpha enquiry');assert.equal(payload.equipment,'nowe-urzadzenie');assert.equal(payload.consent,true);assert.equal(payload.phone,'+48123456789');
  assert.equal(await page.locator('[name=message]').inputValue(),'Alpha Mini');
  console.log('PASS',lang,'6 widths, navigation, gallery, FAQ, form validation + mocked error/success payload');
 }
 assert.deepEqual(errors,[]);assert.deepEqual(failures,[]);
 // Shared handler change must retain existing MEDIflex enquiry context.
 for(const lang of Object.keys(routes)){
  const prefix=lang==='pl'?'':'/'+lang;await page.goto(base+prefix+'/kontakt.html?product=mediflex-us450');assert.equal(await page.locator('[name=message]').inputValue(),'MEDIflex US450');
  await page.locator('[name=name]').fill('Local QA');await page.locator('[name=phone]').fill('+48123456789');await page.locator('[name=consent]').check();await page.locator('#contact-form button[type=submit]').click();await page.waitForFunction(()=>document.querySelector('#contact-form-status').classList.contains('is-success'));assert.equal(payload.productName,'MEDIflex US450');assert.equal(payload.productUrl,'https://ltsmarket.pl'+prefix+'/uzywane/mediflex-us450.html');
 }
 console.log('PASS existing MEDIflex contact flow PL/EN/RU; no page errors or local failed assets');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
