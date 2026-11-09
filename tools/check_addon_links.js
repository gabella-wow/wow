// Проверка ссылок аддона: каждый url из assets/addon/gabella-guide.json отдаёт 200 с локального сервера, якорь есть на странице,
// а ссылка на скрытую вкладку (#lvl-horde-…) открывает её. Запуск из корня репо: node tools/check_addon_links.js <путь к playwright>
const http = require('http'), fs = require('fs'), path = require('path');
const root = process.cwd(), SITE = 'https://gabella.site/wow/';
const data = JSON.parse(fs.readFileSync('assets/addon/gabella-guide.json', 'utf8'));
const urls = [...data.dungeons.map(d => d.url), ...Object.values(data.dungeons_by_area), ...data.levels.map(l => l.url), ...Object.values(data.route).flat().flatMap(s => [s.url, s.url_hunter])];
const srv = http.createServer((q, r) => {
  let p = path.join(root, decodeURIComponent(q.url.split('?')[0].replace(/^\/wow\//, '/')));
  if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
  if (!fs.existsSync(p)) { r.writeHead(404); return r.end('no'); }
  r.writeHead(200, { 'content-type': p.endsWith('.html') ? 'text/html; charset=utf-8' : 'application/octet-stream' }); fs.createReadStream(p).pipe(r);
}).listen(8799, '127.0.0.1', async () => {
  let bad = 0, n = 0;
  const {chromium} = require(process.argv[2]);
  const b = await chromium.launch({executablePath: process.argv[3]});
  const ctx = await b.newContext({viewport: {width: 1280, height: 800}});
  for (const u of [...new Set(urls)]) {
    const [pg, hash] = u.replace(SITE, '').split('#');
    const p = await ctx.newPage();
    const resp = await p.goto(`http://127.0.0.1:8799/wow/${pg}${hash ? '#' + hash : ''}`, {waitUntil: 'load'});
    let ok = resp.status() === 200, note = '';
    if (ok && hash) {
      const el = await p.$('#' + hash);
      ok = !!el;
      if (ok) {   // the target is visible (its tab is open) and scrolled into the viewport
        await p.waitForTimeout(150);
        const st = await p.evaluate(h => { const e = document.getElementById(h), r = e.getBoundingClientRect(); const panel = e.closest('[role=tabpanel]');
          return {inView: r.top >= 0 && r.top < innerHeight, hidden: !!(panel && panel.hidden)}; }, hash);
        ok = st.inView && !st.hidden; note = JSON.stringify(st);
      } else note = 'нет якоря';
    }
    n++; if (!ok) bad++;
    console.log((ok ? 'OK  ' : 'FAIL') + ' ' + resp.status() + ' ' + u + ' ' + note);
    await p.close();
  }
  console.log(`проверено ${n} ссылок, ошибок ${bad}`);
  await b.close(); srv.close(); process.exit(bad ? 1 : 0);
});
