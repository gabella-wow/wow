/* Service worker of the guide (scope: the site root next to this file).
   Pages: network first, the saved copy when offline or the network is slow (3 s).
   assets/news.json and data/official.json: network first. Other files of the site (art, fonts, icons, manifests): the saved copy, fetched once.
   GitHub Pages lets browsers keep files only 10 minutes, so repeat visits come from here instead.
   VERSION is written by build.py from the contents of assets/ and the manifests: any changed file gives
   a new worker, which drops the old caches on activate. */
const VERSION = '9e20111fc0';
const PAGES = 'pages-' + VERSION, FILES = 'files-' + VERSION;
const PRECACHE = ['./', 'assets/fonts/spectral-sc-ru-uk.woff2?v=5fb5d8ed', 'assets/fonts/spectral-sc-latin.woff2?v=55dd1ea6',
  'assets/fonts/golos-text-ru-uk.woff2?v=14d5f312', 'assets/fonts/golos-text-latin.woff2?v=7df287d1', 'assets/icons/icon-192.png?v=d0ae3492'];
const MAX_FILES = 250, MAX_PAGES = 80;
const SLOW = 3000;

const OFFLINE = `<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WoW Forever</title><body style="margin:0;min-height:100vh;display:grid;place-items:center;background:#050505;color:#efe9da;font:17px/1.5 system-ui,sans-serif;text-align:center;padding:24px">
<div><p style="font:700 40px Georgia,serif;color:#c9a54a;margin:0">G</p><p>Нет сети, а эту страницу вы ещё не открывали.<br>No connection, and this page has not been saved yet.<br>Немає мережі, а цю сторінку ви ще не відкривали.</p>
<p><a href="./" style="color:#c9a54a">WoW Forever</a></p></div></body></html>`;

self.addEventListener('install', e => {
  e.waitUntil(caches.open(FILES).then(c => c.addAll(PRECACHE.slice(1)))
    .then(() => caches.open(PAGES)).then(c => c.add(PRECACHE[0])).catch(() => {}).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== PAGES && k !== FILES).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

async function trim(name, max) {
  const c = await caches.open(name), keys = await c.keys();
  for (let i = 0; i < keys.length - max; i++) await c.delete(keys[i]);
}

async function put(name, req, res, max) {
  if (!res || !res.ok || res.type === 'opaque') return;
  const c = await caches.open(name);
  await c.put(req, res);
  await trim(name, max);
}

async function page(e) {
  const req = e.request, net = fetch(req, { cache: 'no-cache' });   // revalidate: the HTML may sit in the HTTP cache for hours
  e.waitUntil(net.then(res => put(PAGES, req, res.clone(), MAX_PAGES)).catch(() => {}));
  const saved = await caches.match(req, { ignoreSearch: true });
  if (!saved) return net.catch(() => new Response(OFFLINE, { headers: { 'Content-Type': 'text/html; charset=utf-8' } }));
  const slow = new Promise(r => setTimeout(() => r(saved), SLOW));
  return Promise.race([net.catch(() => saved), slow]);
}

async function fresh(e) {
  const net = fetch(e.request);
  e.waitUntil(net.then(res => put(FILES, e.request, res.clone(), MAX_FILES)).catch(() => {}));
  try {
    return await net;
  } catch (err) {
    const saved = await caches.match(e.request);
    if (saved) return saved;
    throw err;
  }
}

async function file(e) {
  const saved = await caches.match(e.request);
  if (saved) return saved;
  const net = fetch(e.request);
  e.waitUntil(net.then(res => put(FILES, e.request, res.clone(), MAX_FILES)).catch(() => {}));
  return net;
}

self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin || !url.pathname.startsWith(new URL('./', location).pathname)) return;
  if (req.mode === 'navigate') return e.respondWith(page(e));
  if (url.pathname.endsWith('/news.json') || url.pathname.endsWith('/data/official.json')) return e.respondWith(fresh(e));
  if (req.headers.has('range')) return;
  e.respondWith(file(e));
});
