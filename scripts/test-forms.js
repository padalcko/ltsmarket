// Run with JavaScriptCore: jsc scripts/test-forms.js -- pl home
function assert(value, message) { if (!value) throw new Error(message); }
globalThis.console = { error() {} };
const lang = arguments[0] || 'pl';
const kind = arguments[1] || 'home';
function element(value = '') {
  const classes = new Set();
  return { value, checked: true, events: {}, attrs: {}, textContent: 'Send', hidden: false,
    classList: { add: (...x) => x.forEach(v => classes.add(v)), remove: (...x) => x.forEach(v => classes.delete(v)), contains: x => classes.has(x), toggle: (x,yes) => yes ? classes.add(x) : classes.delete(x) },
    setAttribute(k,v) { this.attrs[k]=v; }, removeAttribute(k) { delete this.attrs[k]; },
    addEventListener(k,v) { this.events[k]=v; }, checkValidity() { return true; }, focus() {},
    closest() { return wrapper; }
  };
}
const wrapper=element(), button=element(), status=element(), form=element();
form.elements={};
for (const [k,v] of Object.entries({name:'Test User',city:'Warszawa',email:'test@example.com',phone:'+48 123 456 789',salon:'Test salon',message:'Product enquiry',privacy:'accepted',consent:'accepted',equipment:'uzywane-urzadzenie',formType:'contact',page:'kontakt'})) form.elements[k]=element(v);
form.querySelector=s => s.includes('button') ? button : null;
let resets=0;
form.reset=() => resets++;
const pathname=(lang==='pl'?'':'/'+lang)+(kind==='home'?'/':'/kontakt.html');
globalThis.window={location:{pathname,search:'?product=medilase-pro',href:'https://ltsmarket.pl'+pathname+'?product=medilase-pro',hostname:'ltsmarket.pl',hash:''},scrollY:0,addEventListener(){},matchMedia(){return {matches:false,addEventListener(){}};}};
globalThis.document={documentElement:{lang},body:element(),getElementById(id){return id==='contact-form'?form:id===(kind==='home'?'form-status':'contact-form-status')?status:null;},querySelectorAll(){return [];},addEventListener(type,fn){if(type==='DOMContentLoaded')fn();}};
globalThis.FormData=class { constructor(f){this.f=f;} get(k){const e=this.f.elements[k];return e && (k==='consent'&&!e.checked?null:e.value);} };
globalThis.URLSearchParams=class { get(){return 'medilase-pro';} };
let timeoutCallback,cleared=0;
globalThis.setTimeout=fn => {timeoutCallback=fn;return 1;};
globalThis.clearTimeout=() => cleared++;
globalThis.AbortController=class {constructor(){this.signal={};} abort(){this.signal.aborted=true;if(this.signal.reject)this.signal.reject(new Error('aborted'));}};
let requests=[],resolveRequest;
globalThis.fetch=(url,options)=>{requests.push({url,options});return new Promise((resolve,reject)=>{resolveRequest=resolve;options.signal.reject=reject;});};
load('js/lead-api.js');
const prefix=lang==='pl'?'':lang+'/';
load(prefix+'js/main.js');
if(kind==='contact')load(prefix+'js/kontakt.js');
(async()=>{
 const submit=()=>form.events.submit({preventDefault(){}});
 form.elements.phone.value='invalid';await submit();assert(requests.length===0,'invalid phone must not send');form.elements.phone.value='+48 123 456 789';
 const consent=form.elements[kind==='home'?'privacy':'consent'];consent.checked=false;await submit();assert(requests.length===0,'consent required');consent.checked=true;
 const first=submit();await submit();assert(requests.length===1,'duplicate submission blocked');assert(button.disabled,'button disabled');
 const data=JSON.parse(requests[0].options.body);
 assert(data.language===lang && data.page===pathname+'?product=medilase-pro','language and actual page');
 assert(data.privacy==='accepted' && data.consent && data.createdAt && data.source==='ltsmarket.pl','shared webhook fields');
 if(kind==='contact')assert(data.equipment==='uzywane-urzadzenie','equipment retained');
 assert(requests[0].options.headers['Content-Type']==='application/json','JSON request');
 assert(resets===0,'no premature success');resolveRequest({ok:true});await first;
 assert(resets===1 && !button.disabled && status.classList.contains('is-success'),'success after HTTP OK');
 const failure=submit();resolveRequest({ok:false,status:500});await failure;
 assert(resets===1 && !button.disabled && status.classList.contains('is-error'),'HTTP failure retains form');
 const timeout=submit();timeoutCallback();await timeout;
 assert(resets===1 && !button.disabled && status.classList.contains('is-error'),'timeout retains form and unlocks');
 assert(cleared===3,'timers cleared');
 print('PASS: '+lang+' '+kind+' validation, payload, duplicate guard, success, HTTP failure and timeout');
})().catch(error=>{print('FAIL: '+error.stack);});
