// Local QA. Every production webhook request is intercepted; no real leads are sent.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.TEST_BASE_URL || 'http://127.0.0.1:8791';
const routes={pl:'/nowe/lumos/',en:'/en/new/lumos/',ru:'/ru/novye/lumos/'};
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 const page=await browser.newPage({reducedMotion:"reduce"});
 await page.addInitScript(()=>{window.qaVitals={cls:0,lcp:0};new PerformanceObserver(list=>{for(const x of list.getEntries())if(!x.hadRecentInput)window.qaVitals.cls+=x.value;}).observe({type:'layout-shift',buffered:true});new PerformanceObserver(list=>{for(const x of list.getEntries())window.qaVitals.lcp=x.startTime;}).observe({type:'largest-contentful-paint',buffered:true});}); const errors=[],failures=[];let payload,mode='success',posts=0;
 page.on('pageerror',e=>errors.push(String(e)));
 page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)failures.push(r.url());});
 await page.route(/google-analytics|googletagmanager/,r=>r.abort());
 await page.route('**/webhook/lts-market-lead',async r=>{posts++;payload=r.request().postDataJSON();await r.fulfill({status:mode==='success'?200:500,contentType:'application/json',body:'{}'});});
 fs.mkdirSync('/tmp/lumos-qa',{recursive:true});
 for(const [lang,route] of Object.entries(routes).filter(([lang])=>!process.env.TEST_LANG || process.env.TEST_LANG===lang)){
  for(const width of [320,375,430,768,1024,1440]){
   await page.setViewportSize({width,height:900});
   const response=await page.goto(base+route);assert.equal(response.status(),200);
   await page.evaluate(()=>document.fonts.ready);
   await page.locator('.nowe-hero__visual img').evaluate(i=>i.decode());
   await page.waitForTimeout(300);
   console.log('LOCAL VITALS',lang,width,await page.evaluate(()=>window.qaVitals));
   const overflow=await page.evaluate(()=>[...document.querySelectorAll("body *")].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>({tag:e.tagName,class:e.className,width:e.getBoundingClientRect().width,scroll:e.scrollWidth,text:e.textContent.slice(0,80)})));
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${lang} overflow ${width}: ${JSON.stringify(overflow)}`);
   for(const [index,id] of ['wavelengths','power','cooling','fac','neodez','software'].entries()){
    const copy=await page.locator(`#${id} .lumos-feature__copy`).boundingBox();
    const diagram=await page.locator(`#${id} .lumos-diagram`).boundingBox();
    if(width>=1024){
     assert(Math.abs(copy.width-diagram.width)<2,`${lang} ${id} column widths`);
     assert(Math.abs(copy.height-diagram.height)<2,`${lang} ${id} column heights`);
     assert(Math.abs(copy.y-diagram.y)<2,`${lang} ${id} alignment`);
     assert(index%2===1?copy.x<diagram.x:copy.x>diagram.x,`${lang} ${id} alternation`);
    }else{assert(copy.y<diagram.y,`${lang} ${id} mobile order`);}
    if(lang==='ru' && [375,1440].includes(width))await page.locator(`#${id}`).screenshot({path:`/tmp/lumos-qa/${lang}-${width}-${id}.png`});
   }
   assert.equal(await page.locator('#reading').count(),0);
   assert.equal(await page.locator('#offer-benefits .nowe-support__card').count(),4);
   assert.equal(await page.locator('#offer-benefits a[href="https://raccoon-studio.com.ua/pl/"]').count(),1);
   assert.deepEqual(await page.locator('.lumos-gallery a').evaluateAll(xs=>xs.map(x=>Number(x.dataset.lumosImage))),[0,10,11,12,13,9,4,8,5,6,7,1,2,3,14,15]);
   if(lang==='ru' && [375,1440].includes(width))for(const id of ['crm','updates','dermatoscope','offer-benefits']){await page.locator('#'+id).scrollIntoViewIfNeeded();for(const img of await page.locator('#'+id+' img').all())await img.evaluate(i=>i.decode());await page.locator('#'+id).screenshot({path:`/tmp/lumos-qa/refined-${id}-${width}.png`});}
   assert.equal(await page.locator('h1').count(),1);assert.equal(await page.locator('#faq details').count(),13);
   assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),'https://ltsmarket.pl'+route);
   await page.locator('a[href="#specification"]').click();assert(await page.locator('#specification').isVisible());
   await page.locator('#faq summary').first().click();assert(await page.locator('#faq details').first().getAttribute('open')!==null);
   for(const cta of await page.locator('a[href="#contact-form"]').all()){await cta.click();}assert(await page.locator('#contact-form').isVisible());
   for(const l of Object.keys(routes)){
    assert.equal(await page.locator(`.language-switcher__menu a[lang=${l}]`).getAttribute('href'),routes[l]);
    assert.equal(await page.locator(`.mobile-menu__languages-list a[lang=${l}]`).getAttribute('href'),routes[l]);
   }
   const images=await page.locator('main img:not(dialog img)').evaluateAll(imgs=>imgs.map(i=>({src:i.src,alt:i.alt,w:i.width,h:i.height})));
   assert(images.every(i=>i.alt&&i.w>0&&i.h>0));
   for(const img of await page.locator('main img:not(dialog img)').all()){await img.scrollIntoViewIfNeeded();await img.evaluate(i=>i.decode());}
   if(width===375||width===1440){await page.screenshot({path:`/tmp/lumos-qa/${lang}-${width}.png`,fullPage:true});}
   if(width===375||width===1440){
    await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));await page.screenshot({path:`/tmp/lumos-qa/${lang}-${width}-hero.png`});
    await page.locator('#service').scrollIntoViewIfNeeded();await page.screenshot({path:`/tmp/lumos-qa/${lang}-${width}-service.png`});
   }
   if(width===375){await page.locator('#menu-toggle').click();assert(await page.locator('#mobile-menu').isVisible());await page.locator('#menu-toggle').click();}
  }
  await page.goto(base+route);await page.locator('#language-button').click();assert(await page.locator('#language-menu').isVisible());await page.locator(`#language-menu a[lang=${lang==='pl'?'en':'pl'}]`).click();assert.equal(new URL(page.url()).pathname,routes[lang==='pl'?'en':'pl']);
  await page.goto(base+route);
  await page.locator('#gallery a').first().click();assert(await page.locator('dialog').isVisible());await page.keyboard.press('ArrowRight');assert.equal(await page.locator('[data-count]').innerText(),'2 / 16');await page.keyboard.press('Escape');assert(!await page.locator('dialog').isVisible());
  await page.locator('#gallery a').first().click();await page.locator('dialog img').evaluate(el=>{for(const [type,x] of [['touchstart',200],['touchend',80]])el.dispatchEvent(new TouchEvent(type,{changedTouches:[new Touch({identifier:1,target:el,clientX:x})]}));});assert.equal(await page.locator('[data-count]').innerText(),'2 / 16');await page.keyboard.press('Escape');
  const before=posts;await page.locator('#contact-form button[type=submit]').click();assert.equal(posts,before);assert(await page.locator('#contact-form-status').evaluate(e=>e.classList.contains('is-error')));
  await page.locator('[name=name]').fill('Local QA');await page.locator('[name=phone]').fill('+48123456789');await page.locator('[name=email]').fill('qa@example.com');await page.locator('[name=message]').fill('Edited Lumos enquiry');await page.locator('[name=consent]').check();
  mode='failure';await page.locator('#contact-form button[type=submit]').click();await page.waitForFunction(()=>document.querySelector('#contact-form-status').classList.contains('is-error'));assert.equal(await page.locator('[name=message]').inputValue(),'Edited Lumos enquiry');
  mode='success';await page.locator('#contact-form button[type=submit]').click();await page.waitForFunction(()=>document.querySelector('#contact-form-status').classList.contains('is-success'));
  assert.equal(payload.productName,'Lumos');assert.equal(payload.productUrl,'https://ltsmarket.pl'+route);assert.equal(payload.pageUrl,base+route);assert.equal(payload.language,lang);assert.equal(payload.message,'Edited Lumos enquiry');assert.equal(payload.equipment,'nowe-urzadzenie');assert.equal(payload.consent,true);assert.equal(payload.phone,'+48123456789');
  assert.equal(await page.locator('[name=message]').inputValue(),'Lumos');
  console.log('PASS',lang,'6 widths, navigation, gallery, FAQ, form validation + mocked error/success payload');
 }
 const blog=JSON.parse(fs.readFileSync('scripts/blog-posts.json')).posts.find(p=>p.pl.slug.startsWith('lumos-'));
 for(const lang of Object.keys(routes))for(const width of [320,375,430,768,1024,1440]){await page.setViewportSize({width,height:900});await page.goto(base+(lang==='pl'?'':'/'+lang)+'/blog/'+blog[lang].slug+'/');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.equal(await page.locator('h1').count(),1);assert.equal(await page.locator('.blog-prose section').count(),16);}
 console.log('PASS articles PL/EN/RU at six widths');
 assert.deepEqual(errors,[]);assert.deepEqual(failures,[]);
 // Shared handler change must retain existing MEDIflex enquiry context.
 for(const lang of Object.keys(routes)){
  const prefix=lang==='pl'?'':'/'+lang;await page.goto(base+prefix+'/kontakt.html?product=mediflex-us450');assert.equal(await page.locator('[name=message]').inputValue(),'MEDIflex US450');
  await page.locator('[name=name]').fill('Local QA');await page.locator('[name=phone]').fill('+48123456789');await page.locator('[name=consent]').check();await page.locator('#contact-form button[type=submit]').click();await page.waitForFunction(()=>document.querySelector('#contact-form-status').classList.contains('is-success'));assert.equal(payload.productName,'MEDIflex US450');assert.equal(payload.productUrl,'https://ltsmarket.pl'+prefix+'/uzywane/mediflex-us450.html');
 }
 console.log('PASS existing MEDIflex contact flow PL/EN/RU; no page errors or local failed assets');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
