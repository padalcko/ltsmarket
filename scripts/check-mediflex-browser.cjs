// Run against the repository served at http://127.0.0.1:8790. All webhook POSTs are mocked.
require('node:fs').mkdirSync('/tmp/mediflex',{recursive:true});
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 const page=await browser.newPage();let errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.route(/google-analytics|googletagmanager|fonts.googleapis|fonts.gstatic/,route=>route.abort());
 for(const prefix of ['','/en','/ru']) {
  const lang=prefix.slice(1)||'pl';
  for(const width of [320,375,430,768,1440]) {
   await page.setViewportSize({width,height:900});
   for(const route of ['/','/uzywane.html','/uzywane/mediflex-us450.html']) {
    const response=await page.goto('http://127.0.0.1:8790'+prefix+route);assert.equal(response.status(),200);
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${prefix}${route} overflow ${width}`);
    if(route.includes('mediflex')) {
     assert.equal(await page.locator('h1').count(),1);
     assert.equal(await page.locator('[data-image]').count(),10);
     if(width===375) {
      for(let i=0;i<10;i++) {const button=page.locator('[data-image]').nth(i);await button.click();await page.waitForFunction(i=>document.querySelectorAll('[data-image]')[i].getAttribute('aria-pressed')==='true',i);assert(await page.locator('[data-gallery-main]').evaluate(img=>img.complete&&img.naturalWidth>0));}
      await page.locator('[data-image]').first().click();
      await page.locator('#menu-toggle').click();assert(await page.locator('#mobile-menu').isVisible());
      for(const l of ['pl','en','ru'])assert((await page.locator('#mobile-menu a[lang="'+l+'"]').getAttribute('href')).endsWith('/uzywane/mediflex-us450.html'));
      await page.locator('#menu-toggle').click();
      await page.screenshot({path:`/tmp/mediflex/${lang}-375.png`,fullPage:true});
     }
     if(width===1440)await page.screenshot({path:`/tmp/mediflex/${lang}-1440.png`,fullPage:true});
    } else {
     const scope=route==='/'?'#uzywane ':'';
     const urls=await page.locator(scope+'a.product-card').evaluateAll(a=>a.map(x=>x.getAttribute('href')));
     assert.deepEqual(urls.map(x=>x.split('/').pop()),['mediflex-us450.html','3d-contour.html','medilase-pro.html','ellisys-plus.html','daeyang-carbo-3000.html']);
     if(width===375)await page.screenshot({path:`/tmp/mediflex/${lang}-${route==='/'?'home':'catalog'}-375.png`,fullPage:true});
    }
   }
  }
  // Actual localized contact UI with intercepted transport: no production lead.
  let payload;
  await page.route('**/webhook/lts-market-lead',async route=>{payload=route.request().postDataJSON();await route.fulfill({status:200,contentType:'application/json',body:'{"ok":true}'});});
  await page.goto('http://127.0.0.1:8790'+prefix+'/uzywane/mediflex-us450.html');
  await page.locator('a.button--primary').first().click();
  assert.equal(await page.locator('[name=message]').inputValue(),'MEDIflex US450');
  await page.locator('[name=name]').fill('Local QA');await page.locator('[name=phone]').fill('+48123456789');await page.locator('[name=email]').fill('qa@example.com');
  await page.locator('[name=message]').fill('Buyer edited message');await page.locator('[name=consent]').check();await page.locator('#contact-form button[type=submit]').click();
  await page.waitForFunction(()=>document.querySelector('#contact-form-status').classList.contains('is-success'));
  assert.equal(payload.productName,'MEDIflex US450');assert.equal(payload.productUrl,'https://ltsmarket.pl'+prefix+'/uzywane/mediflex-us450.html');assert.equal(payload.language,lang);assert.equal(payload.message,'Buyer edited message');assert.equal(payload.equipment,'uzywane-urzadzenie');assert.equal(payload.consent,true);
  console.log('PASS',lang,'15 responsive routes, 10 gallery images, language switch, card order, mocked form payload');
 }
 assert.deepEqual(errors,[]);await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
