// Narrow phone check (audit X6, 02.11): /play/ and /classes/ at 320/360/375 px, both themes, 9 languages.
// /play/ is opened twice: with no hero (the empty state) and with a saved hero (an Orc Shaman at level 24, the card «My class at
// level N» shows). Fails when
//   - the page scrolls sideways (scrollWidth > clientWidth), or a block of the page sticks out past the screen edge;
//   - /classes/: the class comparison cards are not all one height (the spec names ran to 3 lines on Shaman and Warlock);
//   - /classes/: a chip / tile of «Which class to pick» is wider than its column (the Warlock chip ran 26 px out);
//   - the top bar «More» button lacks aria-haspopup / aria-expanded, or the search button's name carries the Ctrl K hint.
//   node tests/narrow_check.mjs            all of it (used by run_all)
//   each load twice: phone emulation and a plain window of that width (the phone viewport stretches to wide content, so the top bar
//   running off at 320 did not show there)
//   options: --langs ru,de  --widths 320  --themes light  --pages play/  --modes window  --json FILE  --shots DIR
// Exit code 1 if anything is found; prints ПРОЙДЕНО / УПАЛО.
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { existsSync, mkdtempSync, readFileSync, statSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(process.env.NARROW_ROOT || join(dirname(fileURLToPath(import.meta.url)), '..'));
const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf('--' + n); return i < 0 ? d : (argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : true); };
const ALL_LANGS = ['ru', 'uk', 'en', 'de', 'fr', 'es', 'pt', 'it', 'pl'];
const langs = String(opt('langs', '') || ALL_LANGS.join(',')).split(',');
const widths = String(opt('widths', '') || '320,360,375').split(',').map(Number);
const themes = String(opt('themes', '') || 'light,dark').split(',');
const subs = String(opt('pages', '') || 'play/,classes/,tools/').split(',');
const shotsDir = opt('shots', '');
const modes = String(opt('modes', '') || 'phone,window').split(',');   // phone: mobile emulation (the layout viewport may stretch to the content); window: a desktop window of that width (no stretch)
const jobs = +opt('jobs', 8);
const HERO = { race: 'orc', cls: 'shaman', spec: 'enhancement', role: 'dps', lvl: 24 };

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.avif': 'image/avif', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.webmanifest': 'application/manifest+json', '.xml': 'application/xml', '.ico': 'image/x-icon' };
const server = createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0].replace(/^\/wow\//, '/'));
  let f = join(ROOT, p);
  if (!f.startsWith(ROOT)) { res.writeHead(403).end(); return; }
  if (existsSync(f) && statSync(f).isDirectory()) f = join(f, 'index.html');
  if (!existsSync(f)) { res.writeHead(404).end('404'); return; }
  res.writeHead(200, { 'content-type': MIME[extname(f)] || 'application/octet-stream' });
  res.end(readFileSync(f));
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}/wow/`;

const CHROME = [process.env.CHROME_PATH, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', '/usr/bin/google-chrome', '/usr/bin/chromium', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'].find(p => p && existsSync(p));
if (!CHROME) { console.error('Chrome not found (set CHROME_PATH)'); process.exit(2); }
const port = 9300 + Math.floor(Math.random() * 300);
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, '--no-first-run', '--disable-gpu', '--hide-scrollbars', `--user-data-dir=${mkdtempSync(join(tmpdir(), 'nrw-'))}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws;
for (let i = 0; i < 80 && !ws; i++) {
  try { const v = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); ws = new WebSocket(v.webSocketDebuggerUrl); } catch { await sleep(250); }
}
await new Promise(r => ws.onopen = r);
let seq = 0; const pend = new Map();
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { const [ok, bad] = pend.get(m.id); pend.delete(m.id); m.error ? bad(new Error(m.error.message)) : ok(m.result); } };
const send = (method, params = {}, sessionId) => new Promise((ok, bad) => { const id = ++seq; pend.set(id, [ok, bad]); ws.send(JSON.stringify({ id, method, params, sessionId })); });

// ---- the probe (runs in the page): [selector, why]
const PROBE = `() => {
  const out = [], de = document.documentElement, W = de.clientWidth;
  const nm = e => { let s = '', n = e; for (let i = 0; n && n !== document.body && i < 3; i++, n = n.parentElement) s = (n.tagName.toLowerCase() + (n.id ? '#' + n.id : '') + (typeof n.className === 'string' && n.className.trim() ? '.' + n.className.trim().split(/\\s+/).slice(0, 2).join('.') : '')) + (s ? ' > ' + s : ''); return s; };
  if (de.scrollWidth > W + 1) out.push(['PAGE', 'scrollWidth ' + de.scrollWidth + ' > clientWidth ' + W]);
  // blocks past the right edge, outside any horizontal scroller / clip; only the outermost offender of a branch is listed
  const shown = e => { const cs = getComputedStyle(e); return cs.display !== 'none' && cs.visibility !== 'hidden' && cs.position !== 'fixed'; };
  const inScroll = e => { for (let p = e.parentElement; p && p !== de; p = p.parentElement) { const o = getComputedStyle(p).overflowX; if (/auto|scroll|hidden|clip/.test(o)) return true; } return false; };
  const main = document.querySelector('main') || document.body;
  const bad = [];
  for (const e of main.querySelectorAll('*')) {
    if (e.closest('svg,dialog:not([open]),[hidden],.sr,.sr-only')) continue;
    const r = e.getBoundingClientRect();
    if (r.width < 1 || r.height < 1 || !shown(e)) continue;
    if (r.right > W + 1 && !inScroll(e) && !bad.some(b => b.contains(e))) bad.push(e);
  }
  for (const e of bad.slice(0, 6)) { const r = e.getBoundingClientRect(); out.push([nm(e), 'right edge ' + Math.round(r.right) + ' > ' + W + ' (width ' + Math.round(r.width) + ')']); }
  // classes/: a one-word class name on a tile is never broken in the middle («Чернокниж/ник»)
  for (const b of document.querySelectorAll('.cpick b')) {
    const t = b.textContent.trim(); if (!t || /[\\s-]/.test(t) || !b.getBoundingClientRect().width) continue;
    const rg = document.createRange(); rg.selectNodeContents(b);
    const tops = new Set([...rg.getClientRects()].filter(r => r.width > 1).map(r => Math.round(r.top)));
    if (tops.size > 1) out.push([nm(b), 'one word broken over ' + tops.size + ' lines "' + t + '"']);
  }
  // the top bar row and its buttons inside the screen (at 320 the row grew to 399 px with the page and pushed the language button off)
  for (const e of document.querySelectorAll('.topbar .in, .topbar .tools > *')) {
    const r = e.getBoundingClientRect(); if (r.width < 1 || !shown(e)) continue;
    if (r.right > W + 1) out.push([nm(e), 'top bar past the screen: right ' + Math.round(r.right) + ' > ' + W]);
  }
  // classes/: the class cards one height
  const rows = [...document.querySelectorAll('.cmp.cls .cmp-row')].filter(e => e.getBoundingClientRect().height > 0);
  if (rows.length) {
    const hs = rows.map(e => Math.round(e.getBoundingClientRect().height));
    const lo = Math.min(...hs), hi = Math.max(...hs);
    if (hi - lo > 1) out.push(['.cmp.cls .cmp-row', 'card heights differ ' + lo + '..' + hi + ': ' + rows.filter((e, i) => hs[i] !== lo).map(e => (e.querySelector('b') || e).textContent.trim()).join(', ')]);
  }
  // chips / tiles wider than their box (text cut or running out)
  for (const e of main.querySelectorAll('.chip, .pill, .clink, .ctile, .tile, .btn, a.tag')) {
    const r = e.getBoundingClientRect(); if (r.width < 1 || !shown(e) || e.closest('[class*="scroll"], .rdo-tiles')) continue;
    if (e.scrollWidth > e.clientWidth + 1 && !/auto|scroll/.test(getComputedStyle(e).overflowX)) out.push([nm(e), 'content ' + e.scrollWidth + ' > box ' + e.clientWidth + ' "' + e.textContent.trim().slice(0, 30) + '"']);
    let p = e.parentElement; while (p.parentElement && /^(inline|contents)$/.test(getComputedStyle(p).display)) p = p.parentElement;
    const pr = p.getBoundingClientRect(), ps = getComputedStyle(p);
    const right = pr.right - parseFloat(ps.paddingRight) - parseFloat(ps.borderRightWidth);
    if (r.right > right + 1 && !/auto|scroll/.test(ps.overflowX)) out.push([nm(e), 'runs ' + Math.round(r.right - right) + 'px out of its column "' + e.textContent.trim().slice(0, 30) + '"']);
  }
  // the top bar: «More» says it opens a dialog and whether it is open; search is named without the shortcut hint
  for (const b of document.querySelectorAll('[aria-controls="moreDlg"]')) {
    if (!b.hasAttribute('aria-haspopup')) out.push([nm(b), 'no aria-haspopup']);
    if (!b.hasAttribute('aria-expanded')) out.push([nm(b), 'no aria-expanded']);
  }
  for (const b of document.querySelectorAll('.srchbtn')) {
    const name = (b.getAttribute('aria-label') || b.textContent).replace(/\\s+/g, ' ');
    if (/ctrl|⌘|\\bK\\b/i.test(name)) out.push([nm(b), 'accessible name carries the shortcut: "' + name.trim() + '"']);
  }
  return out;
}`;

async function newWorker() {
  const { browserContextId } = await send('Target.createBrowserContext');
  const { targetId } = await send('Target.createTarget', { url: 'about:blank', browserContextId });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const S = (m, p) => send(m, p, sessionId);
  await S('Page.enable'); await S('Runtime.enable');
  const ev = async expr => {
    const r = await S('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    return r.result.value;
  };
  return { S, ev, script: null };
}

const found = [];
async function check(w, job) {
  const { S, ev } = w;
  const { lang, sub, width, theme, hero, mode } = job;
  await S('Emulation.setDeviceMetricsOverride', { width, height: 800, deviceScaleFactor: 1, mobile: mode === 'phone' && width < 720 });
  if (w.script) await S('Page.removeScriptToEvaluateOnNewDocument', { identifier: w.script });
  const ls = `localStorage.clear();localStorage.setItem('wf-theme','${theme}');localStorage.setItem('gabella-lang','${lang}');` + (hero ? `localStorage.setItem('gabella-wf-me',${JSON.stringify(JSON.stringify(HERO))});` : '');
  w.script = (await S('Page.addScriptToEvaluateOnNewDocument', { source: `try{${ls}}catch(e){}` })).identifier;
  await S('Page.navigate', { url: base + (lang === 'ru' ? '' : lang + '/') + sub });
  for (let i = 0; i < 80; i++) { if (await ev(`document.readyState`) === 'complete') break; await sleep(100); }
  await ev(`document.fonts.ready.then(()=>1)`);
  await sleep(sub.startsWith('play') ? 700 : 300);
  if (hero && !(await ev(`!!document.querySelector('.pcard:not([hidden])')`))) found.push({ ...job, sel: '.pcard', why: 'the card «My class at level N» did not show for the saved hero' });
  for (const [sel, why] of await ev(`(${PROBE})()`)) found.push({ ...job, sel, why });
  if (opt('eval', '')) console.log(`/${sub} ${lang} ${width} ${theme} ${hero ? 'hero' : 'empty'}:`, JSON.stringify(await ev(String(opt('eval')))));   // debugging: --eval "<expression>"
  if (shotsDir) {
    const { cssContentSize } = await S('Page.getLayoutMetrics');
    const r = await S('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: Math.max(width, Math.ceil(cssContentSize.width)), height: Math.min(Math.ceil(cssContentSize.height), 6000), scale: 1 } });
    mkdirSync(shotsDir, { recursive: true });
    writeFileSync(join(shotsDir, `${sub.replace(/\W/g, '') || 'home'}-${lang}-${width}-${theme}${hero ? '-hero' : ''}${mode === 'window' ? '-win' : ''}.png`), Buffer.from(r.data, 'base64'));
  }
}

const queue = [];
for (const sub of subs) for (const lang of langs) for (const width of widths) for (const theme of themes)
  for (const hero of sub.startsWith('play') || argv.includes('--hero') ? [false, true] : [false]) for (const mode of modes) queue.push({ sub, lang, width, theme, hero, mode });
const total = queue.length, t0 = Date.now();
const workers = await Promise.all(Array.from({ length: Math.min(jobs, total) }, newWorker));
await Promise.all(workers.map(async w => {
  while (queue.length) {
    const job = queue.shift();
    try { await check(w, job); } catch (e) { found.push({ ...job, sel: 'ERROR', why: String(e.message).slice(0, 120) }); }
  }
}));
for (const f of found.slice(0, 120)) console.log(`/${f.sub} | ${f.lang} | ${f.width} | ${f.theme} | ${f.mode} | ${f.hero ? 'hero' : 'empty'} | ${f.sel} | ${f.why}`);
if (found.length > 120) console.log(`... and ${found.length - 120} more`);
if (opt('json', '')) writeFileSync(opt('json', ''), JSON.stringify(found, null, 1));
console.log(`narrow: ${found.length ? 'УПАЛО' : 'ПРОЙДЕНО'} — ${found.length} found in ${total} page loads (${subs.join(' ')} x ${langs.length} languages x ${widths.join('/')} px x ${themes.join('/')} x ${modes.join('/')}), ${Math.round((Date.now() - t0) / 1000)}s`);
try { await send('Browser.close'); } catch {}
chrome.kill(); server.close();
process.exit(found.length ? 1 : 0);
