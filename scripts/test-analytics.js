function assert(ok, message) { if (!ok) throw new Error(message); }
var scripts = [];
var window = {};
var localStorage = {getItem:function(){throw Error('Analytics must not depend on storage');}};
var document = {
  head:{append:function(el){scripts.push(el);}},
  createElement:function(tag){assert(tag === 'script', 'No consent UI'); return {};}
};
load('js/analytics.js');
assert(scripts.length === 1, 'Immediate loading without interaction');
assert(scripts[0].async && scripts[0].src === 'https://www.googletagmanager.com/gtag/js?id=G-1Z98BZS3WW', 'GA4 script');
assert(window.dataLayer.length === 2 && window.dataLayer[1][0] === 'config' && window.dataLayer[1][1] === 'G-1Z98BZS3WW', 'Automatic page view configuration');
load('js/analytics.js');
assert(scripts.length === 1 && window.dataLayer.length === 2, 'No duplicate script or configuration');
print('PASS: automatic GA4 startup, no consent UI/storage dependency, no duplicate loading');
