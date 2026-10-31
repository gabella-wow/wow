// Overflow check: text sticking out of its box, clipped text, horizontal page scroll.
// Pages come from sitemap.xml; each is opened in headless Chrome per language / width / theme,
// then the open states are checked too: "More", the character sheet (every class), search, the language menu, radio.
//   node tests/overflow_check.mjs --quick            key pages x 9 languages x 2 widths, dark theme (used by run_all)
//   node tests/overflow_check.mjs --full             every page x 9 languages x 360/768/1280/1920 x both themes
//   options: --langs ru,uk  --widths 360,1280  --themes dark  --pages classes/,tools/  --jobs 6  --shots DIR  --json FILE
//   the top bar on its own (every page load checks it too): home, tools/ and a build page x 9 languages x the laptop widths
//   1100-1800 where the menu, the subtitle and the buttons share one row (es at 1280 cut the theme button by 2 px);
//   on in --quick and --full, --no-header skips it, --header-widths 1280,1366 picks the widths (with --pages: only if given)
// Exit code 1 if anything is found. Lists: page / language / width / theme / state / selector / text.
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { existsSync, mkdtempSync, readFileSync, statSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf('--' + n); return i < 0 ? d : (argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : true); };
const FULL = argv.includes('--full');
const ALL_LANGS = ['ru', 'uk', 'en', 'de', 'fr', 'es', 'pt', 'it', 'pl'];
const langs = (opt('langs', '') || ALL_LANGS.join(',')).split(',');
const widths = (opt('widths', '') || (FULL ? '360,768,1280,1920' : '360,1280')).split(',').map(Number);
const themes = (opt('themes', '') || (FULL ? 'light,dark' : 'dark')).split(',');   // layout is the same in both themes; --quick checks dark only
const jobs = +opt('jobs', 8);
const shotsDir = opt('shots', '');
const KEY = ['', 'classes/', 'classes/warlock/', 'races/', 'guides/', 'guides/leveling/', 'tools/', 'character/', 'play/', 'guides/builds/', 'guides/news/'];
const only = (opt('pages', '') || '').split(',').filter(Boolean).map(o => o === 'home' ? '' : o);   // 'home' = the home page
const onlyHome = (opt('pages', '') || '').split(',').includes('home');
const HEADER_PAGES = ['', 'tools/', 'guides/builds-paladin/'];
const headerWidths = argv.includes('--no-header') || (opt('pages', '') && !opt('header-widths', '')) ? [] : String(opt('header-widths', '') || '1100,1200,1261,1280,1300,1366,1440,1600,1800').split(',').map(Number);

// ---- pages from the sitemap: {lang, path}
const sm = readFileSync(join(ROOT, 'sitemap.xml'), 'utf8');
const locs = [...sm.matchAll(/<url><loc>https:\/\/gabella\.site\/wow\/([^<]*)<\/loc>/g)].map(m => m[1]);
const pages = [], headerPages = [];
for (const p of locs) {
  const m = p.match(/^(en|uk|de|fr|es|pt|it|pl)\/(.*)$/);
  const lang = m ? m[1] : 'ru', sub = m ? m[2] : p;
  if (!langs.includes(lang)) continue;
  if (HEADER_PAGES.includes(sub)) headerPages.push({ lang, sub, url: p });
  if (only.length || onlyHome ? !only.some(o => o === '' ? sub === '' : sub === o || sub.startsWith(o)) : (!FULL && !KEY.includes(sub))) continue;
  pages.push({ lang, sub, url: p });
}
if (!pages.length) { console.error('no pages'); process.exit(2); }

// ---- tiny static server (no dependency)
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.avif': 'image/avif', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.webmanifest': 'application/manifest+json', '.xml': 'application/xml', '.ico': 'image/x-icon' };
const server = createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0].replace(/^\/wow\//, '/'));
  let f = join(ROOT, p);
  if (!f.startsWith(ROOT)) { res.writeHead(403).end(); return; }
  if (existsSync(f) && statSync(f).isDirectory()) f = join(f, 'index.html');
  if (!existsSync(f)) { res.writeHead(404).end('404'); return; }
  res.writeHead(200, { 'content-type': MIME[extname(f)] || 'application/octet-stream' });
  res.end(readFileSync(f));
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}/`;

// ---- Chrome over CDP
const CHROME = [process.env.CHROME_PATH, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', '/usr/bin/google-chrome', '/usr/bin/chromium', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'].find(p => p && existsSync(p));
if (!CHROME) { console.error('Chrome not found (set CHROME_PATH)'); process.exit(2); }
const port = 9600 + Math.floor(Math.random() * 300);
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, '--no-first-run', '--disable-gpu', '--hide-scrollbars', `--user-data-dir=${mkdtempSync(join(tmpdir(), 'ovf-'))}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws;
for (let i = 0; i < 80 && !ws; i++) {
  try { const v = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); ws = new WebSocket(v.webSocketDebuggerUrl); } catch { await sleep(250); }
}
await new Promise(r => ws.onopen = r);
let seq = 0; const pend = new Map();
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { const [ok, bad] = pend.get(m.id); pend.delete(m.id); m.error ? bad(new Error(m.error.message)) : ok(m.result); } };
const send = (method, params = {}, sessionId) => new Promise((ok, bad) => { const id = ++seq; pend.set(id, [ok, bad]); ws.send(JSON.stringify({ id, method, params, sessionId })); });

// ---- the probe, runs in the page. Scope = document or the open dialog/popup.
const PROBE = `(scopeSel) => {
  const root = scopeSel ? document.querySelector(scopeSel) : document.body;
  const out = [], W = document.documentElement.clientWidth;
  if (!root) return out;
  if (!scopeSel && document.documentElement.scrollWidth > W + 1) out.push(['PAGE', 'scrollWidth ' + document.documentElement.scrollWidth + ' > ' + W, '']);
  const nm = e => { let s = '', n = e; for (let i = 0; n && n !== document.body && i < 3; i++, n = n.parentElement) s = (n.tagName.toLowerCase() + (n.id ? '#' + n.id : '') + (typeof n.className === 'string' && n.className.trim() ? '.' + n.className.trim().split(/\\s+/).slice(0, 2).join('.') : '')) + (s ? ' > ' + s : ''); return s; };
  const ownText = e => [...e.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim());
  const scroller = e => { for (let p = e; p && p !== document.documentElement; p = p.parentElement) if (/auto|scroll/.test(getComputedStyle(p).overflowX)) return p; return null; };
  const hidden = e => { const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) return true; const r = e.getBoundingClientRect(); if (r.width <= 1 || r.height <= 1) return true; for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { if (getComputedStyle(p).clipPath === 'none') continue; const b = p.getBoundingClientRect(); if (b.width <= 1 || b.height <= 1) return true; } return false; };   // clipped away on purpose (the wordmark at 375–719 px)
  const isCard = (p, cs) => cs.display !== 'inline' && (parseFloat(cs.borderLeftWidth) > 0 || parseFloat(cs.borderTopWidth) > 0 || (cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent') || cs.backgroundImage !== 'none' || cs.boxShadow !== 'none') ;
  const els = [root, ...root.querySelectorAll('*')];
  for (const e of els) {
    if (/^(SCRIPT|STYLE|SVG|PATH|USE|IMG|PICTURE|SOURCE|VIDEO|AUDIO|CANVAS)$/i.test(e.tagName) || e.closest('svg,[aria-hidden="true"],.sr,[hidden],.sr-only')) continue;
    const texts = ownText(e); if (!texts.length || hidden(e)) continue;
    if (e.closest('.skip, .skiplink, a[href="#main"]')) continue;
    // text that is entirely outside a clipping ancestor is not visible (collapsed cards, carousels): not an overflow
    const rg0 = document.createRange(); rg0.selectNodeContents(texts[0]); const r0 = rg0.getBoundingClientRect();
    let invisible = false;
    for (let p = e.parentElement; p && p !== document.documentElement; p = p.parentElement) {
      const ps = getComputedStyle(p); if (+ps.opacity === 0) { invisible = true; break; }
      if (/hidden|clip/.test(ps.overflowX)) { const b = p.getBoundingClientRect(); if (r0.left >= b.right - 0.5 || r0.right <= b.left + 0.5) { invisible = true; break; } }
    }
    if (invisible) continue;
    const cs = getComputedStyle(e);
    const label = (e.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 40);
    const sc = scroller(e);
    // 1. own box: the content is wider than the box and nothing scrolls it
    if (cs.display !== 'inline' && !/auto|scroll/.test(cs.overflowX) && e.scrollWidth > e.clientWidth + 1 && e.clientWidth > 0) out.push([nm(e), 'scrollWidth ' + e.scrollWidth + ' > clientWidth ' + e.clientWidth, label]);
    // 2. the text itself against the nearest card / clipping ancestor
    const rg = document.createRange(); let tl = 1e9, tr = -1e9;
    for (const n of texts) { rg.selectNodeContents(n); for (const r of rg.getClientRects()) { if (r.width < 1) continue; tl = Math.min(tl, r.left); tr = Math.max(tr, r.right); } }
    if (tr < 0) continue;
    let card = null, clip = null;
    for (let p = e; p && p !== document.documentElement; p = p.parentElement) {
      const ps = getComputedStyle(p);
      if (!clip && p !== e && /hidden|clip/.test(ps.overflowX)) clip = p;
      if (!card && p !== document.body && (p === e ? false : isCard(p, ps) || p.matches('button,a,.btn,li,dialog'))) card = p;
      if (/auto|scroll/.test(ps.overflowX) && p !== e) break;
    }
    if (e.matches('button,a,.btn') && !card) card = e;
    else if (e.matches('button,.btn') && isCard(e, cs)) card = e;
    const own = card || null;
    if (own && own !== e || (own === e)) {
      const b = own.getBoundingClientRect(), bs = getComputedStyle(own);
      const pl = parseFloat(bs.paddingLeft) || 0, pr = parseFloat(bs.paddingRight) || 0;
      if (tr > b.right + 1 + 0 && tl < b.right + 400) out.push([nm(e), 'text sticks out of ' + nm(own) + ' by ' + Math.round(tr - b.right) + 'px', label]);
      else if (tl < b.left - 1 && tr > b.left - 400) out.push([nm(e), 'text sticks out of ' + nm(own) + ' on the left by ' + Math.round(b.left - tl) + 'px', label]);
    }
    if (clip && clip !== root.parentElement) {
      const b = clip.getBoundingClientRect();
      if (tr > b.right + 1 && tl < b.right) out.push([nm(e), 'text clipped by ' + nm(clip) + ' by ' + Math.round(tr - b.right) + 'px', label]);
    }
    // 3. outside the screen (not inside a scroller)
    if (!sc && (tr > W + 1 && tl < W + 1 || tl < -1 && tr > 0)) out.push([nm(e), 'text beyond the screen edge (' + Math.round(tl) + '..' + Math.round(tr) + ' of ' + W + ')', label]);
  }
  const seen = new Set();
  return out.filter(o => { const k = o[0] + '|' + o[1].replace(/\\d+/g, 'N') + '|' + o[2]; if (seen.has(k)) return false; seen.add(k); return true; }).slice(0, 40);
}`;

// ---- the top bar: every visible control whole on the screen and inside the bar, no part of the row on top of
// another, the buttons of the row one height (44 px below 2200 px), the menu links unclipped
const HEADER_PROBE = `() => {
  const out = [], W = document.documentElement.clientWidth, bar = document.querySelector('.topbar .in');
  if (!bar) return out;
  if (document.documentElement.scrollWidth > W + 1) out.push(['PAGE', 'scrollWidth ' + document.documentElement.scrollWidth + ' > ' + W, '']);
  const vis = e => { const cs = getComputedStyle(e), r = e.getBoundingClientRect(); return cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 1 && r.height > 1 && !(cs.position === 'absolute' && r.width <= 1); };
  const nm = e => e.tagName.toLowerCase() + (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\\s+/).slice(0, 2).join('.') : '');
  const lab = e => (e.getAttribute('aria-label') || e.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 30);
  const bs = getComputedStyle(bar), bb = bar.getBoundingClientRect();
  // the row starts at the content edge (the logo over the page text); on a wide screen it may run past the 1240 px
  // column into the side margin (1600: the search field), never into the 20 px gutter (16 px on a phone) or off the screen
  const g = W < 720 ? 16 : 20;
  const left = Math.max(0, bb.left + parseFloat(bs.paddingLeft)) - 0.5, right = Math.max(bb.right - parseFloat(bs.paddingRight), W - g) + 0.5;
  const ctl = [...bar.querySelectorAll('a, button')].filter(vis);
  for (const e of ctl) {
    const r = e.getBoundingClientRect();
    if (r.right > right || r.left < left) out.push([nm(e), 'outside the bar (' + Math.round(r.left) + '..' + Math.round(r.right) + ' of ' + Math.round(left) + '..' + Math.round(right) + ')', lab(e)]);
    if (e.closest('.mainnav') && e.scrollWidth > e.clientWidth + 1) out.push([nm(e), 'menu link clipped ' + e.scrollWidth + ' > ' + e.clientWidth, lab(e)]);
  }
  const parts = [bar.querySelector('.brand'), bar.querySelector('.mainnav'), bar.querySelector('.tools')].filter(e => e && vis(e));
  for (let i = 1; i < parts.length; i++) {
    const a = parts[i - 1].getBoundingClientRect(), b = parts[i].getBoundingClientRect();
    if (a.right > b.left + 0.5) out.push([nm(parts[i - 1]), 'runs into ' + nm(parts[i]) + ' by ' + Math.round(a.right - b.left) + 'px', '']);
  }
  const brand = bar.querySelector('.brand .bt');
  if (brand && vis(brand)) for (const t of brand.children) if (vis(t) && t.scrollWidth > t.clientWidth + 1) out.push([nm(t), 'subtitle clipped', lab(t)]);
  const btns = [...bar.querySelectorAll('.tools > button, .tools > .langsel > button, .tools > a')].filter(vis);
  const hs = [...new Set(btns.map(e => Math.round(e.getBoundingClientRect().height)))];
  if (hs.length > 1) out.push(['.tools', 'button heights differ: ' + hs.join(', '), '']);
  if (W >= 360 && W < 2200 && hs.length && hs[0] !== 44) out.push(['.tools', 'button height ' + hs[0] + ' != 44', '']);
  return out;
}`;

async function newWorker() {
  const { browserContextId } = await send('Target.createBrowserContext');
  const { targetId } = await send('Target.createTarget', { url: 'about:blank', browserContextId });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const S = (m, p) => send(m, p, sessionId);
  await S('Page.enable'); await S('Runtime.enable');
  const ev = async (expr, awaitP = true) => {
    const r = await S('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: awaitP });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    return r.result.value;
  };
  return { S, ev, targetId, browserContextId };
}

const STATES = [
  { name: 'more', click: '.menubtn, .morebtn', scope: '#moreDlg' },
  { name: 'radio', click: '.radiobtn', scope: '#radioPanel' },
  { name: 'lang', click: '.langbtn', scope: '.langsel' },
];
const found = [];
let done = 0;

async function checkPage(w, job) {
  const { S, ev } = w;
  const { lang, sub, url, width, theme } = job;
  await S('Emulation.setDeviceMetricsOverride', { width, height: width < 700 ? 800 : 900, deviceScaleFactor: 1, mobile: width < 700 });
  await S('Page.addScriptToEvaluateOnNewDocument', { source: `try{localStorage.setItem('wf-theme','${theme}');localStorage.setItem('gabella-lang','${lang}')}catch(e){}` });
  await S('Page.navigate', { url: base + url });
  for (let i = 0; i < 80; i++) { if (await ev(`document.readyState`) === 'complete') break; await sleep(100); }
  await ev(`document.fonts.ready.then(()=>1)`);
  for (let i = 0; i < 20; i++) { if (await ev(`!!document.querySelector('.mebtn.herobtn')`)) break; await sleep(100); }
  await sleep(150);
  const add = (state, list) => { for (const [sel, why, text] of list) found.push({ page: '/' + sub, lang, width, theme, state, selector: sel, why, text }); };
  const probe = scope => ev(`(${PROBE})(${JSON.stringify(scope)})`);
  const shot = async name => { if (!shotsDir) return; const r = await S('Page.captureScreenshot', { format: 'png' }); mkdirSync(shotsDir, { recursive: true }); writeFileSync(join(shotsDir, `${name}.png`), Buffer.from(r.data, 'base64')); };
  add('header', await ev(`(${HEADER_PROBE})()`));
  if (job.headerOnly) return;
  add('page', await probe(''));
  const close = async () => { await S('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 }); await S('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 }); await ev(`document.querySelectorAll('dialog[open]').forEach(d=>d.close());document.querySelectorAll('[aria-expanded="true"]').forEach(b=>b.click());0`); await sleep(60); };
  // click-opened states
  for (const st of STATES) {
    const ok = await ev(`(()=>{const b=[...document.querySelectorAll(${JSON.stringify(st.click)})].find(b=>b.getBoundingClientRect().width>0);if(!b)return false;b.click();return true})()`);
    if (!ok) continue;
    await sleep(200);
    add(st.name, await probe(st.scope));
    if (st.name === 'more') await shot(`${lang}-${width}-${theme}-more`);
    await close();
  }
  // search: Ctrl+K and a short query
  await S('Input.dispatchKeyEvent', { type: 'keyDown', key: 'k', code: 'KeyK', modifiers: 2, windowsVirtualKeyCode: 75 });
  await S('Input.dispatchKeyEvent', { type: 'keyUp', key: 'k', code: 'KeyK', modifiers: 2, windowsVirtualKeyCode: 75 });
  await sleep(500);
  if (await ev(`!!document.querySelector('dialog[open]')`)) {
    await S('Input.insertText', { text: /^(ru|uk)$/.test(lang) ? 'а' : 'e' }); await sleep(500);
    add('search', await probe('dialog[open]'));
    await close();
  }
  // the character sheet: guest, then every class in turn (the spec and race rows appear)
  const hasBtn = await ev(`(()=>{const b=document.querySelector('.topbar .mebtn.herobtn');if(!b||getComputedStyle(b).display==='none'||!b.getBoundingClientRect().width)return false;b.click();return true})()`);
  if (hasBtn) {
    await sleep(500);
    add('sheet', await probe('dialog.hsheet'));
    if (job.shot) await shot(`${lang}-${width}-${theme}-sheet`);
    const n = await ev(`document.querySelectorAll('dialog.hsheet .hs-cls button').length`);
    for (let i = 0; i < n; i++) {
      await ev(`document.querySelectorAll('dialog.hsheet .hs-cls button')[${i}].click()`); await sleep(80);
      add('sheet-class' + i, await probe('dialog.hsheet'));
    }
    if (job.shot) await shot(`${lang}-${width}-${theme}-sheet-spec`);
    await close();
  }
}

// ---- run everything with a pool of workers
const queue = [];
for (const p of pages) for (const width of widths) for (const theme of themes) queue.push({ ...p, width, theme, shot: !!shotsDir && p.sub === '' });
for (const p of headerPages) for (const width of headerWidths) if (!widths.includes(width) || !pages.some(q => q.url === p.url)) queue.push({ ...p, width, theme: themes[0], headerOnly: true });
const total = queue.length;
const t0 = Date.now();
const workers = await Promise.all(Array.from({ length: Math.min(jobs, total) }, newWorker));
await Promise.all(workers.map(async w => {
  while (queue.length) {
    const job = queue.shift();
    try { await checkPage(w, job); }
    catch (e) { found.push({ page: '/' + job.sub, lang: job.lang, width: job.width, theme: job.theme, state: 'run', selector: 'ERROR', why: String(e.message).slice(0, 120), text: '' }); }
    if (++done % 50 === 0 && process.stderr.isTTY) process.stderr.write(`  ${done}/${total}  ${Math.round((Date.now() - t0) / 1000)}s\n`);
  }
}));

// ---- report
const uniq = new Map();
for (const f of found) { const k = [f.page, f.lang, f.width, f.theme, f.state.replace(/\d+$/, ''), f.selector, f.text].join('|'); if (!uniq.has(k)) uniq.set(k, f); }
const rows = [...uniq.values()];
if (opt('json', '')) writeFileSync(opt('json', ''), JSON.stringify(rows, null, 1));
const byLang = {}; for (const r of rows) byLang[r.lang] = (byLang[r.lang] || 0) + 1;
for (const r of rows.slice(0, +opt('max', 200))) console.log(`${r.page} | ${r.lang} | ${r.width} | ${r.theme} | ${r.state} | ${r.selector} | ${r.why} | "${r.text}"`);
if (rows.length > +opt('max', 200)) console.log(`... and ${rows.length - +opt('max', 200)} more (use --json FILE)`);
console.log(`overflow: ${rows.length} found in ${total} page loads (${pages.length} pages x ${widths.length} widths x ${themes.length} themes + top bar ${headerPages.length} pages x ${headerWidths.length} widths), ${Math.round((Date.now() - t0) / 1000)}s` + (rows.length ? '; by language: ' + Object.entries(byLang).map(([l, n]) => `${l} ${n}`).join(', ') : ''));
try { await send('Browser.close'); } catch {}
chrome.kill(); server.close();
process.exit(rows.length ? 1 : 0);
