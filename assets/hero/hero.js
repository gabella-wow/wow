/* My character on every page: the top-bar button of a reader without a login opens a sheet to make or switch the hero of this
   browser (class, spec, race) in a tap, and the home page shows «Your <class>» with talents, leveling, group and news.
   The hero lives in localStorage "gabella-wf-me" (character/ edits all of it); no storage: it lives in this tab only.
   A signed-in reader keeps the profile portrait and menu of me.js. Texts and game data: assets/hero/<lang>.json (build_guides.hero_json). */
(function () {
  const S = document.currentScript;
  const ROOT = S.dataset.root, HOME = S.dataset.home, DATA = S.dataset.data;
  const PV = /*PV*/'?v=03c9d4a0';   // ?v= of the class portraits (build.art_version)
  const KEY = 'gabella-wf-me', DAY1 = 'gabella-day1';
  let mem = null, D = null, sheet = null;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
  const fill = (s, o) => s.replace(/%(\w)/g, (m, k) => (k in o ? o[k] : m));
  function read() {
    try { const v = JSON.parse(localStorage.getItem(KEY)); return v && typeof v === 'object' ? v : null; } catch (e) { return mem; }
  }
  function write(h) {
    const all = Object.assign({}, read() || {}, h);
    mem = all;
    try { localStorage.setItem(KEY, JSON.stringify(all)); } catch (e) { /* private mode: this tab only */ }
    dispatchEvent(new CustomEvent('gabella-me', { detail: 'hero' }));
    paint();
  }
  const signedIn = () => { try { return localStorage.getItem('gabella-me') === '1'; } catch (e) { return false; } };
  const data = () => (D ? Promise.resolve(D) : fetch(DATA).then(r => r.json()).then(j => (D = j)));
  const raceOf = id => D.races.find(r => r[0] === id);
  const valid = h => !!(h && D.cn[h.cls] && raceOf(h.race) && raceOf(h.race)[2].includes(h.cls));
  const specIx = h => D.sid[h.cls].indexOf(h.spec);
  // a class face: the portrait of side f (the best race of that side, build.portraits), else of the reader's side (build.por_js)
  const face = (id, f) => `${ROOT}assets/art/${window.GabellaPor ? GabellaPor.id(id, f || undefined) : id}-face.webp${PV}`;
  /* the hero's own face (as play/): only a picture drawn for this very race and class (<class>-<race>-face.webp, build.pair_faces);
     none drawn — the neutral class badge (class colour + role icon), never another race. FM: f = the pairs, c = class colours */
  const FM = /*FACES*/{"f":{"dwarf.shaman":"shaman-dwarf","gnome.mage":"mage-gnome","gnome.priest":"priest-gnome","gnome.warlock":"warlock-gnome","human.paladin":"paladin-human","human.warrior":"warrior-human","nightelf.druid":"druid-nightelf","nightelf.hunter":"hunter-nightelf","nightelf.rogue":"rogue-nightelf","orc.hunter":"hunter-orc","orc.mage":"mage-orc","orc.rogue":"rogue-orc","orc.shaman":"shaman-orc","orc.warlock":"warlock-orc","orc.warrior":"warrior-orc","tauren.druid":"druid-tauren","undead.paladin":"paladin-undead","undead.priest":"priest-undead"},"c":{"warrior":"#c79c6e","paladin":"#f58cba","hunter":"#abd473","rogue":"#fff569","priest":"#e8e8e8","shaman":"#2f8cf0","mage":"#40c7eb","warlock":"#8788ee","druid":"#ff7d0a"}};
  function heroFace(h, size, cls) {
    const n = h && FM.f[h.race + '.' + h.cls];
    if (n) return `<img${cls ? ` class="${cls}"` : ''} src="${ROOT}assets/art/${n}-face.webp${PV}" alt="" width="${size}" height="${size}">`;
    const ico = ['tank', 'heal', 'dps'].includes(h && h.role) ? h.role : 'user';
    return `<span class="hface${cls ? ' ' + cls : ''}" style="--cc:${FM.c[h && h.cls] || ''}"><svg class="ico" aria-hidden="true"><use href="#i-${ico}"/></svg></span>`;
  }
  const bestOf = (c, f, s) => { const b = (D.best[c] || {})[f]; return b ? (b[s] || b['*']) : null; };

  /* ---------- the top-bar button: a reader without a login ---------- */
  let btn = null;
  function paintBtn(el) {
    if (el) btn = el;
    btn = btn || document.querySelector('.topbar .mebtn');
    if (!btn || signedIn()) return;
    const h = read();
    btn.href = HOME + 'character/';
    btn.classList.add('herobtn');
    btn.innerHTML = h && FM.c[h.cls] ? heroFace(h, 30) : '<svg class="ico" aria-hidden="true"><use href="#i-user"/></svg>';
    btn.onclick = e => { e.preventDefault(); open(); };
    if (D) { const t = valid(h) ? fill(D.tx.yourCls, { s: D.cn[h.cls] }) : D.tx.collect; btn.setAttribute('aria-label', t); btn.title = t; }
    btn.setAttribute('aria-haspopup', 'dialog');
  }

  /* ---------- the sheet: class -> spec -> race, every tap saved at once ---------- */
  let draft = null;
  function open() {
    data().then(() => {
      const h = read();
      draft = valid(h) ? { race: h.race, cls: h.cls, spec: D.sid[h.cls].includes(h.spec) ? h.spec : '', f: raceOf(h.race)[1] } : { race: '', cls: '', spec: '', f: '' };
      if (!sheet) {
        sheet = document.createElement('dialog');
        sheet.className = 'hsheet';
        sheet.addEventListener('click', onSheet);
        sheet.addEventListener('close', () => { draft = null; });
        document.body.append(sheet);
      }
      drawSheet();
      if (sheet.showModal) sheet.showModal(); else sheet.setAttribute('open', '');
      fitNames();
    });
  }
  function save() {   // a full combination only: the role follows the spec (a two-role spec keeps the chosen one)
    if (!draft.race || !draft.cls || !draft.spec) return;
    const old = read() || {}, roles = D.sr[draft.cls][D.sid[draft.cls].indexOf(draft.spec)];
    write({ race: draft.race, cls: draft.cls, spec: draft.spec, role: roles.includes(old.role) && old.cls === draft.cls ? old.role : roles[0] });
  }
  function pickRace() {   // the race keeps the side: the best one of the class and spec, else the first that can play it
    const f = draft.f || (draft.race && raceOf(draft.race)[1]) || (window.GabellaPor ? GabellaPor.fac() : 'alliance');   // no side yet: the side whose portraits the tiles show (by the time of day, as the home page)
    if (draft.race && raceOf(draft.race)[2].includes(draft.cls) && (!f || raceOf(draft.race)[1] === f)) return;
    const b = f && bestOf(draft.cls, f, draft.spec), can = D.races.filter(r => r[2].includes(draft.cls) && (!f || r[1] === f) && !r[3]);
    draft.race = (b && b[0][0]) || (can[0] || [''])[0];
  }
  function drawSheet() {
    const T = D.tx, d = draft, has = valid(read());
    const cls = D.cls.map(c => `<button type="button" data-c="${c}" aria-pressed="${d.cls === c}" style="--cc:${D.color[c]}"><img src="${face(c, d.f)}" alt="" width="48" height="48" loading="lazy"><span class="hs-n">${esc(D.cn[c])}</span></button>`).join('');
    let h = `<div class="hs-h"><b>${esc(has ? T.change : T.collect)}</b><button type="button" class="iconbtn" data-x aria-label="${esc(T.close)}"><svg class="ico" aria-hidden="true"><use href="#i-x"/></svg></button></div>`
      + (has ? '' : `<p class="hs-d">${esc(T.collectD)}</p>`)
      + `<div class="hs-l">${esc(T.cls)}</div><div class="hs-cls">${cls}</div>`;
    if (d.cls) {
      h += `<div class="hs-l">${esc(T.spec)}</div><div class="hs-row">${D.sid[d.cls].map((s, i) => `<button type="button" data-s="${s}" aria-pressed="${d.spec === s}">${esc(D.sn[d.cls][i])}<small>${esc(D.sr[d.cls][i].map(r => D.role[r]).join(', '))}</small></button>`).join('')}</div>`;
    }
    if (d.cls && d.spec) {
      const rs = D.races.filter(r => r[2].includes(d.cls));
      h += `<div class="hs-l">${esc(T.race)}</div><div class="hs-row">${rs.map(r => { const b = bestOf(d.cls, r[1], d.spec), star = b && b[0].includes(r[0]);
        return `<button type="button" data-r="${r[0]}" aria-pressed="${d.race === r[0]}"><span class="hs-f ${r[1]}"></span>${esc(D.rn[r[0]])}${star ? ' <span class="hs-star" title="' + esc(T.best) + '">★</span>' : ''}</button>`; }).join('')}</div>`;
      const b = d.race && bestOf(d.cls, raceOf(d.race)[1], d.spec);
      if (b) h += `<p class="hs-why"><b>★ ${esc(fill(T.bestFor, { s: D.sn[d.cls][specIx(d)] }))}: ${esc(b[0].map(r => D.rn[r]).join(' ' + T.or + ' '))}.</b> ${esc(b[1])}</p>`;
    }
    h += `<div class="hs-a"><a href="${HOME}character/">${esc(T.allSet)}</a><button type="button" class="btn" data-x${d.cls && d.spec ? '' : ' disabled'}>${esc(T.done)}</button></div>`;
    sheet.innerHTML = h;
    sheet.setAttribute('aria-label', has ? T.change : T.collect);
    if (sheet.open) fitNames();
  }
  /* Class names fit their tile: the font shrinks to the longest word (measured in the real font), never below 10.5px; below that the word may break at a syllable */
  function fitNames() {
    const els = sheet.querySelectorAll('.hs-cls .hs-n');
    if (!els.length) return;
    const m = document.createElement('span');
    m.style.cssText = 'position:absolute;left:-9999px;top:0;visibility:hidden;white-space:pre;line-height:1;font-size:100px';
    document.body.append(m);
    els.forEach(el => {
      const b = el.parentElement, cs = getComputedStyle(b), base = parseFloat(cs.fontSize);
      m.style.fontFamily = cs.fontFamily; m.style.fontWeight = cs.fontWeight;
      const k = Math.max(...(el.textContent.match(/[^\s-]+-?/g) || ['']).map(t => (m.textContent = t, m.getBoundingClientRect().width / 100)));
      const room = b.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) - parseFloat(cs.borderLeftWidth) - parseFloat(cs.borderRightWidth);
      const fs = Math.max(10.5, Math.min(base, room * .98 / k));
      el.style.fontSize = fs.toFixed(2) + 'px';
    });
    m.remove();
  }
  window.addEventListener('resize', () => { if (sheet && sheet.open) fitNames(); });
  if (document.fonts) document.fonts.addEventListener('loadingdone', () => { if (sheet && sheet.open) fitNames(); });
  function onSheet(e) {
    if (e.target === sheet) return sheet.close();
    const b = e.target.closest('button'); if (!b) return;
    const k = b.dataset;
    if ('x' in k) return sheet.close();
    if (k.c) { if (draft.cls !== k.c) { draft.cls = k.c; const ro = (read() || {}).role; const i = D.sr[k.c].findIndex(r => r.includes(ro)); draft.spec = D.sid[k.c][i >= 0 ? i : 0]; } pickRace(); }
    else if (k.s) { draft.spec = k.s; pickRace(); }
    else if (k.r) { draft.race = k.r; draft.f = raceOf(k.r)[1]; }
    else return;
    save(); drawSheet();
    const again = sheet.querySelector(`[data-${k.c ? 'c' : k.s ? 's' : 'r'}="${k.c || k.s || k.r}"]`); if (again) again.focus();
  }

  /* ---------- home: «Your <class>» above the rest, or one button to build a character ---------- */
  function lfg(h) {
    const T = D.tx, p = fill(T.lfgP[h.role] || T.lfgP.dps, { c: D.cn[h.cls] }), lv = +h.lvl || 0, f = raceOf(h.race)[1];
    const near = lv ? (D.lfg || []).filter(x => lv >= x[1] - 2 && lv <= x[2] && (!x[3] || x[3] === f)).sort((a, b) => Math.abs(a[1] + a[2] - 2 * lv) - Math.abs(b[1] + b[2] - 2 * lv))[0] : null;
    return fill(near ? T.lfgT : T.lfgT0, { p, d: near ? near[0] : '', l: lv });
  }
  function day1() { try { return Object.keys(JSON.parse(localStorage.getItem(DAY1)) || {}).length; } catch (e) { return 0; } }
  function paintHome() {
    const box = document.getElementById('myHome'), plaque = document.getElementById('pickban');
    if (!box) return;
    const h = read();
    if (!valid(h)) { box.hidden = true; box.innerHTML = ''; if (plaque) plaque.hidden = false; return; }
    const T = D.tx, i = specIx(h), sn = i >= 0 ? D.sn[h.cls][i] : '', pr = D.prof[h.cls], r = h.reg && nextReset(h.reg);
    const meta = [D.rn[h.race], sn, h.role && D.role[h.role], h.lvl ? fill(T.levelN, { n: h.lvl }) : ''].filter(Boolean).join(' · ');
    const a = (href, t, cls) => `<a class="btn${cls || ' ghost'}" href="${HOME}${href}">${esc(t)}</a>`;
    const facts = [`<span><b>${esc(T.profsL)}:</b> ${pr.slice(0, -1).map(x => `${esc(x[0])}: ${esc(x[1])}`).join('. ')}. <a href="${HOME}guides/professions/#pairs=${h.cls}">${esc(T.pairs)}</a></span>`,
      `<a href="${HOME}guides/launch-checklist/">${esc(fill(T.day1n, { n: day1(), t: D.ck }))}</a>`];
    if (r) facts.push(`<span>${esc(T.resetH)} · ${esc(T.regs[h.reg])}: ${esc(fill(T.resetIn, { s: leftTxt(r - new Date()) }))}</span>`);
    box.innerHTML = `<div class="mh frame" style="--cc:${D.color[h.cls]}">${heroFace(h, 96, 'mh-face')}`
      + `<div class="mh-t"><h2>${esc(fill(T.yourCls, { s: D.cn[h.cls] }))}</h2><p class="mh-s">${esc(meta)}</p></div>`
      + `<button type="button" class="mh-ch" data-hero-open>${esc(T.change)}</button>`
      + `<nav class="mh-b" aria-label="${esc(fill(T.yourCls, { s: D.cn[h.cls] }))}">${a(`guides/builds-${h.cls}/${i >= 0 ? '#' + h.spec : ''}`, T.bTalents, ' ')}${a('play/', T.bLevel)}`
      + `<button type="button" class="btn ghost" data-lfg>${esc(T.bGroup)}</button>${a('guides/news/#mine', T.bNews)}</nav>`
      + `<p class="mh-lfg" role="status" hidden></p><div class="mh-f">${facts.join('')}</div></div>`;
    box.hidden = false;
    if (plaque) plaque.hidden = true;
  }
  function nextReset(reg) {
    const v = D.reset[reg]; if (!v) return null;
    const now = new Date(), d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), v[1]));
    d.setUTCDate(d.getUTCDate() + (v[0] - d.getUTCDay() + 7) % 7);
    if (d <= now) d.setUTCDate(d.getUTCDate() + 7);
    return d;
  }
  function leftTxt(ms) {
    const u = (n, k) => new Intl.NumberFormat(document.documentElement.lang, { style: 'unit', unit: k, unitDisplay: 'short', maximumFractionDigits: 0 }).format(n);
    const m = Math.max(1, Math.round(ms / 6e4)), d = Math.floor(m / 1440), h = Math.floor(m % 1440 / 60);
    return d ? `${u(d, 'day')} ${u(h, 'hour')}` : h ? `${u(h, 'hour')} ${u(m % 60, 'minute')}` : u(m, 'minute');
  }
  document.addEventListener('click', e => {
    if (e.target.closest('[data-hero-open]')) { e.preventDefault(); return open(); }
    const g = e.target.closest('#myHome [data-lfg]');
    if (g) {
      const t = lfg(read()), out = document.querySelector('#myHome .mh-lfg'), shown = () => { out.textContent = fill(D.tx.copiedT, { s: t }); out.hidden = false; };
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(shown, () => { out.textContent = t; out.hidden = false; }); else { out.textContent = t; out.hidden = false; }
    }
  });

  /* «Talents» in the menu and the sheet: the tree of the saved spec, else the list of all builds */
  function paintTalents() {
    const h = read(), ok = h && D && valid(h);
    document.querySelectorAll('a[data-tl]').forEach(a => {
      a.dataset.tl = a.dataset.tl || a.getAttribute('href');
      a.setAttribute('href', ok ? `${HOME}guides/builds-${h.cls}/${D.sid[h.cls].includes(h.spec) ? '#' + h.spec : ''}` : a.dataset.tl);
    });
  }
  function paint() { paintBtn(); paintTalents(); if (document.getElementById('myHome')) data().then(paintHome, () => {}); }
  window.GabellaHero = { btn: paintBtn, open };
  addEventListener('storage', e => { if (e.key === KEY || e.key === DAY1) paint(); });
  addEventListener('gabella-me', e => { if (e.detail !== 'hero') paint(); });
  paint();
  data().then(() => { paintBtn(); paintTalents(); }, () => {});

  /* a counter without cookies or ids: once a day per browser one beacon «visit», plus «char» if a hero is saved (the share of visits with a character) */
  function beacon() {
    try {
      const day = new Date().toISOString().slice(0, 10);
      if (localStorage.getItem('gabella-cnt') === day) return;
      localStorage.setItem('gabella-cnt', day);
      const h = read(), send = k => navigator.sendBeacon('https://report.gabella.site/c', new Blob([JSON.stringify({ k })], { type: 'text/plain' }));
      send('visit');
      if (h && h.cls && h.race) send('char');
    } catch (e) { /* no storage or no beacon: not counted */ }
  }
  addEventListener('load', () => (window.requestIdleCallback ? requestIdleCallback(beacon, { timeout: 5000 }) : setTimeout(beacon, 3000)));
})();
