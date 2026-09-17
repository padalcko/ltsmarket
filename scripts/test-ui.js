function assert(ok,message){if(!ok)throw Error(message);}
['js/main.js','en/js/main.js','ru/js/main.js'].forEach(function(file){
 function el(){return {hidden:true,attrs:{},events:{},classList:{add:function(){},remove:function(){},contains:function(){return false;}},setAttribute:function(k,v){this.attrs[k]=v;},getAttribute:function(k){return this.attrs[k];},addEventListener:function(k,v){this.events[k]=v;},querySelectorAll:function(){return [];},focus:function(){this.focused=true;}};}
 var menu=el(),toggle=el(),language=el(),languages=el(),header=el();
 var els={'site-header':header,'menu-toggle':toggle,'mobile-menu':menu,'language-button':language,'language-menu':languages};
 var events={};
 document={body:el(),getElementById:function(id){return els[id]||null;},querySelectorAll:function(){return [];},addEventListener:function(event,fn){if(event==='DOMContentLoaded')fn();else events[event]=fn;}};
 window={location:{hash:"",hostname:"localhost"},scrollY:0,addEventListener:function(){},matchMedia:function(){return {matches:false,addEventListener:function(){}};}};
 load(file);
 toggle.events.click(); assert(!menu.hidden && toggle.attrs['aria-expanded']==='true',file+' menu opens');
 events.keydown({key:'Escape'}); assert(menu.hidden && toggle.focused,file+' escape closes menu');
 language.events.click({stopPropagation:function(){}}); assert(!languages.hidden,file+' language opens');
 events.click();assert(languages.hidden,file+' outside click closes');
});
var pending=[],main={closest:function(){return link;}},link={};
var buttons=[0,1].map(function(i){return {dataset:{image:'image-'+i},addEventListener:function(e,fn){this.click=fn;},querySelector:function(){return {alt:'photo-'+i};},setAttribute:function(k,v){this[k]=v;}};});
var gallery={querySelector:function(){return main;},querySelectorAll:function(){return buttons;}};
document={querySelectorAll:function(){return [gallery];}};
Image=function(){pending.push(this);this.naturalWidth=640;this.naturalHeight=480;};
load('js/uzywane.js'); buttons[0].click();buttons[1].click(); pending[1].onload();pending[0].onload();
assert(main.src==='image-1' && link.href==='image-1','Latest gallery selection wins');
assert(buttons[1]['aria-pressed']==='true' && main.width===640,'Gallery selection and dimensions');
buttons[0].click();assert(main.src==='image-1','Failed/pending load retains current image');
print('PASS: PL/EN/RU menus and language controls; gallery load races and retained image');
