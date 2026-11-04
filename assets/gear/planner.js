/* Gear planner (character/gear/, gear_planner.py): the doll of 17 slots, the picker on the reader's level, armor and spec,
   the sum of the item stats, «Fill with our build», the build in the address (#c=&s=&r=&l=&g=slot:id,…&t=) and in this browser
   (gabella-gear). Items come from assets/gear/planner-<lang>.json on the first need; icons from one sprite (catalog.webp, 64
   columns), set only when an icon is drawn. The pure part (Core) runs in node for tests/test_gear_planner.py. */
(function (root) {
  'use strict';
  var CELLS = ['head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'hands', 'waist', 'legs', 'feet', 'finger1', 'finger2',
    'trinket1', 'trinket2', 'main', 'off', 'ranged'];
  // armor: subclass -> who wears it (Classic: mail for hunters and shamans and plate for warriors and paladins from 40)
  var WEAP = {   // weapon subclasses a class can learn (Classic trainers)
    warrior: [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 13, 14, 15, 16, 18], paladin: [0, 1, 4, 5, 6, 7, 8, 14],
    hunter: [0, 1, 2, 3, 6, 7, 8, 10, 13, 14, 15, 16, 18], rogue: [2, 3, 4, 7, 13, 14, 15, 16, 18],
    priest: [4, 10, 14, 15, 19], shaman: [0, 1, 4, 5, 10, 13, 14, 15], mage: [7, 10, 14, 15, 19],
    warlock: [7, 10, 14, 15, 19], druid: [4, 5, 10, 13, 14, 15]
  };
  var DUAL = { warrior: 1, rogue: 1, hunter: 1 };
  var SLOT_OF = { finger1: ['finger'], finger2: ['finger'], trinket1: ['trinket'], trinket2: ['trinket'], main: ['main', 'two'],
    off: ['off', 'main'], ranged: ['ranged', 'relic'] };

  function canWear(it, c, l) {
    var a = it.kc, b = it.ks;
    if (a === 4) {
      if (b === 0 || b === 1) return true;
      if (b === 2) return c !== 'mage' && c !== 'priest' && c !== 'warlock';
      if (b === 3) return c === 'warrior' || c === 'paladin' || ((c === 'hunter' || c === 'shaman') && l >= 40);
      if (b === 4) return (c === 'warrior' || c === 'paladin') && l >= 40;
      if (b === 6) return c === 'warrior' || c === 'paladin' || c === 'shaman';
      if (b === 7) return c === 'paladin';
      if (b === 8) return c === 'druid';
      if (b === 9) return c === 'shaman';
      return true;
    }
    if (a === 2) return (WEAP[c] || []).indexOf(b) > -1;
    return true;
  }
  /* may this item go into this cell at all (its slot), and for this class (off hand: a weapon only for dual wielders) */
  function fits(it, cell, c) {
    var slots = SLOT_OF[cell] || [cell];
    if (slots.indexOf(it.s) < 0) return false;
    if (cell === 'off' && it.kc === 2 && !DUAL[c]) return false;
    if (cell === 'ranged' && it.s === 'relic' && c && !canWear(it, c, 60)) return false;
    return true;
  }
  /* the level an item needs: its required level; none in the catalog (quest rewards, old items): about its item level less 5 */
  function need(it) { return it.lv || Math.max(0, it.il - 5); }
  function score(it, w) {
    if (!w) return 0;
    var s = 0;
    for (var k in it.st) if (w[k]) s += w[k] * it.st[k];
    return s;
  }
  /* the candidates of a cell: f = {lvl, arm, rare, drop, quest, craft, q} filters, st = {c, l} */
  function cands(items, cell, st, f, w) {
    var src = [f.drop, f.quest, f.craft], anySrc = src[0] || src[1] || src[2], q = norm(f.q || '');
    var out = [];
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      if (!fits(it, cell, st.c)) continue;
      if (f.lvl && need(it) > st.l) continue;
      if (f.arm && !canWear(it, st.c, st.l)) continue;
      if (f.rare && it.q < 3) continue;
      if (anySrc && !(it.src && src[it.src[0]])) continue;
      if (q && it.low.indexOf(q) < 0 && String(it.id) !== q) continue;
      out.push(it);
    }
    out.sort(function (a, b) { return (score(b, w) - score(a, w)) || (b.il - a.il) || (b.lv - a.lv) || (a.id - b.id); });
    return out;
  }
  function norm(s) { return String(s).toLowerCase().replace(/ё/g, 'е').trim(); }
  function sum(items) {   /* item list -> {stat: total} (dps: the main hand only, as the character sheet shows) */
    var t = {};
    items.forEach(function (x) {
      if (!x) return;
      for (var k in x.it.st) {
        if (k === 'dps' && x.cell !== 'main') continue;
        t[k] = Math.round(((t[k] || 0) + x.it.st[k]) * 10) / 10;
      }
    });
    return t;
  }
  /* equip: the new gear map after putting `it` into `cell` (a two-hander empties the off hand) */
  function equip(g, cell, it) {
    var n = {};
    for (var k in g) n[k] = g[k];
    if (!it) { delete n[cell]; return n; }
    n[cell] = it.id;
    if (cell === 'main' && it.s === 'two') delete n.off;
    return n;
  }
  /* the item worn in THIS cell (finger1 and finger2, trinket1 and trinket2 apart), or null: an id that does not fit the cell counts as nothing */
  function worn(g, cell, byId, c) { var it = g[cell] && byId[g[cell]]; return it && fits(it, cell, c || '') ? it : null; }
  /* gear of an address: ids the catalog lacks or that do not fit their cell are dropped, a two-hander empties the off hand */
  function clean(g, byId, c) {
    var n = {};
    for (var k in g) if (CELLS.indexOf(k) > -1 && worn(g, k, byId, c)) n[k] = g[k];
    if (offLocked(n, byId)) delete n.off;
    return n;
  }
  /* stat changes from `was` (null: an empty cell) to `it`: {stat: difference}, zeros left out */
  function diff(it, was) {
    var d = {}, ks = {}, k;
    for (k in it.st) ks[k] = 1;
    if (was) for (k in was.st) ks[k] = 1;
    for (k in ks) { var v = Math.round(((it.st[k] || 0) - (was ? was.st[k] || 0 : 0)) * 10) / 10; if (v) d[k] = v; }
    return d;
  }
  function offLocked(g, byId) { var m = g.main && byId[g.main]; return !!(m && m.s === 'two'); }
  /* address <-> state: #c=mage&s=frost&r=gnome&l=24&g=head:1234,neck:5678&t=<talent code> */
  function enc(S) {
    var p = [];
    if (S.c) p.push('c=' + S.c);
    if (S.s) p.push('s=' + S.s);
    if (S.r) p.push('r=' + S.r);
    if (S.l) p.push('l=' + S.l);
    var g = CELLS.filter(function (c) { return S.g && S.g[c]; }).map(function (c) { return c + ':' + S.g[c]; }).join(',');
    if (g) p.push('g=' + g);
    if (S.t) p.push('t=' + S.t);
    return p.join('&');
  }
  function dec(h) {
    var S = { c: '', s: '', r: '', l: 0, g: {}, t: '' };
    String(h || '').replace(/^#/, '').split('&').forEach(function (kv) {
      var i = kv.indexOf('='), k = kv.slice(0, i), v = kv.slice(i + 1);
      if (i < 1) return;
      if (k === 'c' || k === 's' || k === 'r') { if (/^[a-z-]{2,20}$/.test(v)) S[k] = v; }
      else if (k === 'l') { var n = parseInt(v, 10); if (n >= 1 && n <= 60) S.l = n; }
      else if (k === 't') { if (/^[0-9-]{1,120}$/.test(v)) S.t = v; }
      else if (k === 'g') v.split(',').forEach(function (p) {
        var m = /^([a-z]+[12]?):(\d{1,7})$/.exec(p);
        if (m && CELLS.indexOf(m[1]) > -1) S.g[m[1]] = +m[2];
      });
    });
    return S;
  }
  function unpack(D) {   /* the data file -> item objects */
    var K = D.k, SL = D.sl;
    return D.it.map(function (a) {
      var st = {};
      for (var i = 0; i < a[9].length; i += 2) st[K[a[9][i]]] = a[9][i + 1];
      return { id: a[0], s: SL[a[1]], q: a[2], il: a[3], lv: a[4], kc: a[5], ks: a[6], ic: a[7], n: a[8], low: norm(a[8]), st: st,
        src: D.src[a[0]] || null };
    });
  }
  /* our build of a spec for a level: the best of its list in every cell (two-hander against main + off) */
  function fill(items, ids, st, w) {
    var set = {}, g = {};
    ids.forEach(function (id) { set[id] = 1; });
    var pool = items.filter(function (it) { return set[it.id] && need(it) <= st.l && canWear(it, st.c, st.l); });
    var val = function (it) { return w ? score(it, w) : it.il; };
    var best = function (cell, skip) {
      var c = pool.filter(function (it) { return fits(it, cell, st.c) && it.id !== skip; });
      c.sort(function (a, b) { return (val(b) - val(a)) || (b.il - a.il); });
      return c[0] || null;
    };
    CELLS.forEach(function (cell) {
      if (cell === 'main' || cell === 'off') return;
      var skip = cell === 'finger2' ? g.finger1 : cell === 'trinket2' ? g.trinket1 : 0;
      var it = best(cell, skip);
      if (it) g[cell] = it.id;
    });
    var one = pool.filter(function (it) { return it.s === 'main' && fits(it, 'main', st.c); }).sort(function (a, b) { return val(b) - val(a); })[0];
    var two = pool.filter(function (it) { return it.s === 'two' && fits(it, 'main', st.c); }).sort(function (a, b) { return val(b) - val(a); })[0];
    var off = best('off', one ? one.id : 0);
    if (two && (!one || val(two) >= val(one) + (off ? val(off) : 0))) g.main = two.id;
    else { if (one) g.main = one.id; if (off) g.off = off.id; }
    return g;
  }
  var Core = { CELLS: CELLS, canWear: canWear, fits: fits, need: need, score: score, cands: cands, sum: sum, equip: equip, offLocked: offLocked,
    worn: worn, clean: clean, diff: diff, enc: enc, dec: dec, unpack: unpack, fill: fill, norm: norm };
  if (typeof module !== 'undefined' && module.exports) module.exports = Core;
  if (typeof document === 'undefined' || !document.getElementById('gpData')) return;

  /* ---------- the page ---------- */
  var C = JSON.parse(document.getElementById('gpData').textContent), T = C.tx, KEY = 'gabella-gear', ROW = 56;
  var $ = function (id) { return document.getElementById(id); };
  var gp = $('gp'), selC = $('gpC'), selS = $('gpS'), selR = $('gpR'), inL = $('gpL'), dlg = $('gpK'), list = $('gpList'), inner = $('gpIn');
  var items = null, byId = {}, loading = null, S, cur = null, rows = [], F = { lvl: true, arm: true };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (x) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[x]; }); };
  var fmt = function (s, o) { return s.replace(/\{(\w)\}/g, function (_, k) { return o[k]; }); };
  var num = function (v) { return String(v).replace('.', C.dec); };
  var clsOk = function (c) { return C.cls.some(function (x) { return x[0] === c; }); };

  function readJSON(k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } }
  function start() {
    var h = dec(location.hash), saved = readJSON(KEY), me = readJSON('gabella-wf-me') || {};
    var base = clsOk(h.c) ? h : (saved && clsOk(saved.c) ? saved : null);
    S = base ? { c: base.c, s: base.s || '', r: base.r || '', l: base.l || 0, g: base.g || {}, t: base.t || '' }
      : { c: clsOk(me.cls) ? me.cls : 'warrior', s: me.spec || '', r: me.race || '', l: +me.lvl || 0, g: {}, t: '' };
    if (base === h && !h.l && me.cls === h.c && +me.lvl) S.l = +me.lvl;
    if (!S.l) S.l = 30;
    if (base === h && !h.r && me.race) S.r = me.race;
    fix();
  }
  function cleanS() { S.g = clean(S.g, byId, S.c); }
  function fix() {   /* spec and race that belong to the class */
    var cl = C.cls.filter(function (x) { return x[0] === S.c; })[0];
    if (cl[2].indexOf(S.s) < 0) S.s = '';
    var ok = C.races.filter(function (r) { return r[3].indexOf(S.c) > -1; });
    if (!ok.some(function (r) { return r[0] === S.r; })) S.r = ok.length ? ok[0][0] : '';
  }
  function save() {
    var h = enc(S);
    try { history.replaceState(null, '', location.pathname + location.search + '#' + h); } catch (e) {}
    try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {}
  }
  function opts(sel, list, val) {
    sel.innerHTML = list.map(function (o) { return '<option value="' + esc(o[0]) + '"' + (o[0] === val ? ' selected' : '') + '>' + esc(o[1]) + '</option>'; }).join('');
  }
  function bar() {
    opts(selC, C.cls.map(function (x) { return [x[0], x[1]]; }), S.c);
    var cl = C.cls.filter(function (x) { return x[0] === S.c; })[0];
    opts(selS, [['', T.nospec]].concat(cl[2].map(function (s, i) { return [s, cl[3][i]]; })), S.s);
    opts(selR, C.races.filter(function (r) { return r[3].indexOf(S.c) > -1; }).map(function (r) { return [r[0], r[1]]; }), S.r);
    inL.value = S.l;
  }
  function weights() { return S.s ? C.w[S.c + '-' + S.s] || null : null; }
  function load() {
    if (items) return Promise.resolve(items);
    if (!loading) loading = fetch(C.data).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (D) {
      items = unpack(D);
      items.forEach(function (it) { byId[it.id] = it; });
      cleanS();
      C.b = D.b;
      gp.style.setProperty('--gsp', 'url("' + C.sprite + '")');
      dlg.style.setProperty('--gsp', 'url("' + C.sprite + '")');
      return items;
    });
    loading.catch(function () { loading = null; });
    return loading;
  }
  function icon(it, inner) {
    return '<span class="gpi ' + (it.ic < 0 ? 'no' : 'ic') + ' q' + it.q + '"' + (it.ic < 0 ? '' : ' style="--ix:' + (it.ic % 64) + ';--iy:' + Math.floor(it.ic / 64) + '"') +
      ' aria-hidden="true">' + (inner || '') + '</span>';
  }
  function outline(cell) { return '<svg viewBox="0 0 24 24"><path d="' + C.icons[cell] + '"/></svg>'; }
  function statLine(st) {
    var out = [];
    if (st.dps) out.push(num(st.dps) + ' ' + C.short.dps);
    if (st.armor) out.push(st.armor + ' ' + C.short.armor);
    ['str', 'agi', 'sta', 'int', 'spi', 'sp', 'hp', 'ap', 'crit', 'hit', 'mp5', 'def'].forEach(function (k) {
      if (st[k]) out.push('+' + st[k] + (k === 'crit' || k === 'hit' ? '%' : '') + ' ' + C.short[k]);
    });
    return out.join(' · ');
  }
  function ours(it) { var b = S.s && C.b && C.b[S.c + '-' + S.s]; return !!(b && b.indexOf(it.id) > -1); }
  function srcLine(it) { return [it.src ? it.src[1] : '', ours(it) ? T.ours : ''].filter(Boolean).join(' · '); }
  function drawCell(cell) {
    var w = gp.querySelector('[data-cell="' + cell + '"]'), it = worn(S.g, cell, byId, S.c), name = C.slot[cell];
    var lock = cell === 'off' && offLocked(S.g, byId);
    if (!it) {
      w.className = 'gpsw';
      w.innerHTML = '<button class="gpsl empty" type="button" aria-haspopup="dialog"' + (lock ? ' disabled' : '') + '><span class="gpi" aria-hidden="true">' + outline(cell) +
        '</span><span class="gptx"><b class="gpn">' + esc(name) + ' · ' + esc(lock ? T.locked : T.pick) + '</b></span></button>';
      return;
    }
    var meta = srcLine(it), sl = statLine(it.st);
    w.className = 'gpsw on';
    w.innerHTML = '<button class="gpsl" type="button" aria-haspopup="dialog" aria-label="' + esc(name + ': ' + it.n + '. ' + fmt(T.il, { n: it.il }) + '. ' + T.change) + '">' +
      icon(it, '<b>' + it.il + '</b>') + '<span class="gptx"><span class="gpkk">' + esc(name) + '</span><b class="gpn iq' + it.q + '">' + esc(it.n) + '</b>' +
      (sl ? '<span class="gpss">' + esc(sl) + '</span>' : '') + (meta ? '<span class="gpsr">' + esc(meta) + '</span>' : '') +
      '</span></button><button class="gpx" type="button" aria-label="' + esc(T.remove + ': ' + it.n) + '">✕</button>';
  }
  function drawStats() {
    var eq = CELLS.map(function (c) { var it = worn(S.g, c, byId, S.c); return it ? { cell: c, it: it } : null; });
    var t = sum(eq), keys = ['str', 'agi', 'sta', 'int', 'spi', 'armor'];
    Object.keys(C.long).forEach(function (k) { if (keys.indexOf(k) < 0 && t[k]) keys.push(k); });
    $('gpStL').innerHTML = keys.map(function (k) {
      return '<div data-k="' + k + '"><dt>' + esc(C.long[k]) + '</dt><dd>' + num(t[k] || 0) + (k === 'crit' || k === 'hit' ? '%' : '') + '</dd></div>';
    }).join('');
  }
  function draw() {
    if (!items) return;   /* the static empty slots stand until the items have come */
    CELLS.forEach(drawCell);
    drawStats();
  }
  function changed() { fix(); bar(); draw(); save(); if (dlg.open) render(true); }

  /* ---------- the picker ---------- */
  var openCell = '', lastBtn = null;
  function place(btn) {   /* wide screens: next to the slot, inside the window */
    if (matchMedia('(max-width: 719px)').matches) { dlg.style.left = dlg.style.top = ''; return; }
    var r = btn.getBoundingClientRect(), w = dlg.offsetWidth, h = dlg.offsetHeight;
    var x = r.right + 8 + w <= innerWidth - 16 ? r.right + 8 : Math.max(16, r.left - 8 - w);
    if (x + w > innerWidth - 16) x = Math.max(16, (innerWidth - w) / 2);
    var y = Math.min(Math.max(16, r.top - 40), innerHeight - h - 16);
    dlg.style.left = x + 'px'; dlg.style.top = Math.max(16, y) + 'px';
  }
  function open(cell, btn) {
    openCell = cell; lastBtn = btn;
    $('gpKh').textContent = C.slot[cell];
    $('gpQ').value = '';
    dlg.showModal();
    place(btn);
    $('gpKm').textContent = T.loading;
    inner.innerHTML = ''; $('gpOff').innerHTML = '';
    load().then(function () { render(true); }, function () { $('gpKm').textContent = T.loadErr; });
    if (!matchMedia('(pointer: coarse)').matches) $('gpQ').focus();
  }
  function delta(it, was) {
    var w = weights(), d = diff(it, was), k;
    var wt = function (k) { return w ? (w[k] || 0) : (k === 'armor' ? .02 : k === 'dps' ? .5 : 1); };
    var keys = Object.keys(d).sort(function (a, b) { return Math.abs(d[b] * wt(b)) - Math.abs(d[a] * wt(a)); }).slice(0, 2);
    var tot = 0;
    for (k in d) tot += d[k] * wt(k);
    if (!keys.length || Math.abs(tot) < 1e-6) return { cls: '', txt: '', aria: '' };
    var txt = keys.map(function (k) { return (d[k] > 0 ? '+' : '−') + num(Math.abs(d[k])) + (k === 'crit' || k === 'hit' ? '%' : '') + ' ' + C.short[k]; }).join(' ');
    return { cls: tot > 0 ? 'up' : 'dn', txt: (tot > 0 ? '▲ ' : '▼ ') + txt, aria: (tot > 0 ? T.better : T.worse) + ': ' + txt };
  }
  function row(it, i, was) {
    var d = delta(it, was), lv = it.lv ? fmt(T.lv, { n: it.lv }) : '', meta = [lv, srcLine(it)].filter(Boolean).join(' · ');
    var isCur = was && was.id === it.id;
    return '<button class="gpr' + (isCur ? ' cur' : '') + '" type="button" data-i="' + i + '" style="top:' + i * ROW + 'px" aria-label="' +
      esc(it.n + '. ' + fmt(T.il, { n: it.il }) + (meta ? '. ' + meta : '') + (isCur ? '. ' + T.worn : d.aria ? '. ' + d.aria : '')) + '">' + icon(it) +
      '<span class="gpt"><span class="gpn iq' + it.q + '">' + esc(it.n) + '</span><span class="gpm">' + esc(meta) + '</span></span>' +
      '<span class="gpdl ' + d.cls + '" aria-hidden="true">' + esc(isCur ? T.worn : d.txt) + '</span></button>';
  }
  var drawn = [-1, -1];
  function paint(force) {
    var h = list.clientHeight || 400, top = list.scrollTop, a = Math.max(0, Math.floor(top / ROW) - 6), b = Math.min(rows.length, Math.ceil((top + h) / ROW) + 6);
    if (!force && a === drawn[0] && b === drawn[1]) return;
    var focus = document.activeElement && document.activeElement.dataset && document.activeElement.dataset.i;
    drawn = [a, b];
    var was = worn(S.g, openCell, byId, S.c), html = '';
    for (var i = a; i < b; i++) html += row(rows[i], i, was);
    inner.innerHTML = html;
    if (focus !== undefined && focus !== null) { var f = inner.querySelector('[data-i="' + focus + '"]'); if (f) f.focus({ preventScroll: true }); }
  }
  function render(reset) {
    if (!items || !dlg.open) return;
    var f = { lvl: F.lvl, arm: F.arm, rare: F.rare, drop: F.drop, quest: F.quest, craft: F.craft, q: $('gpQ').value };
    rows = cands(items, openCell, S, f, weights());
    inner.style.height = rows.length * ROW + 'px';
    var w = weights(), sn = S.s ? C.cls.filter(function (x) { return x[0] === S.c; })[0] : null;
    var note = !S.s ? T.sortNone : w ? fmt(T.sortSpec, { s: sn[3][sn[2].indexOf(S.s)] }) : T.sortIl;
    $('gpKm').textContent = (rows.length ? fmt(T.count, { n: rows.length }) : T.none.replace(/[.。]$/, '')) + '. ' + note;
    var was = worn(S.g, openCell, byId, S.c);   /* «Unequip» only when this very cell has an item */
    $('gpOff').innerHTML = was ? '<button class="gpr off" type="button" data-off="1"><span class="gpi no" aria-hidden="true">✕</span><span class="gpt"><span class="gpn">' +
      esc(T.remove) + '</span><span class="gpm">' + esc(was.n) + '</span></span></button>' : '';
    if (reset) list.scrollTop = 0;
    paint(true);
  }
  function choose(it) {
    S.g = equip(S.g, openCell, it);
    dlg.close();
    draw(); save();
  }
  list.addEventListener('scroll', function () { paint(false); }, { passive: true });
  list.addEventListener('click', function (e) { var b = e.target.closest('.gpr'); if (b) choose(rows[+b.dataset.i]); });
  list.addEventListener('keydown', function (e) {
    var b = e.target.closest('.gpr'); if (!b) return;
    var i = +b.dataset.i, n = e.key === 'ArrowDown' ? i + 1 : e.key === 'ArrowUp' ? i - 1 : e.key === 'Home' ? 0 : e.key === 'End' ? rows.length - 1 : -2;
    if (n === -2) return;
    e.preventDefault();
    if (n < 0) { $('gpQ').focus(); return; }
    n = Math.min(n, rows.length - 1);
    if (n * ROW < list.scrollTop) list.scrollTop = n * ROW;
    else if ((n + 1) * ROW > list.scrollTop + list.clientHeight) list.scrollTop = (n + 1) * ROW - list.clientHeight;
    paint(true);
    var t = inner.querySelector('[data-i="' + n + '"]'); if (t) t.focus({ preventScroll: true });
  });
  $('gpQ').addEventListener('input', function () { render(true); });
  $('gpQ').addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown' && rows.length) { e.preventDefault(); list.scrollTop = 0; paint(true); var t = inner.querySelector('[data-i="0"]'); if (t) t.focus(); }
    if (e.key === 'Enter' && rows.length) { e.preventDefault(); choose(rows[0]); }
  });
  $('gpOff').addEventListener('click', function (e) { if (e.target.closest('[data-off]')) choose(null); });
  dlg.querySelector('.gpch').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    F[b.dataset.f] = !F[b.dataset.f];
    b.setAttribute('aria-pressed', F[b.dataset.f] ? 'true' : 'false');
    render(true);
  });
  $('gpKx').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });   /* a tap on the backdrop */
  dlg.addEventListener('close', function () { if (lastBtn && lastBtn.isConnected) lastBtn.focus(); else { var b = gp.querySelector('[data-cell="' + openCell + '"] .gpsl'); if (b) b.focus(); } });
  addEventListener('resize', function () { if (dlg.open && lastBtn && lastBtn.isConnected) place(lastBtn); });

  /* ---------- the doll and the bar ---------- */
  $('gpD').addEventListener('click', function (e) {
    var w = e.target.closest('.gpsw'); if (!w) return;
    var cell = w.dataset.cell;
    if (e.target.closest('.gpx')) {
      S.g = equip(S.g, cell, null); draw(); save();
      var b = w.querySelector('.gpsl'); if (b) b.focus();
      return;
    }
    var btn = e.target.closest('.gpsl'); if (btn && !btn.disabled) open(cell, btn);
  });
  selC.addEventListener('change', function () { S.c = selC.value; S.s = ''; changed(); });
  selS.addEventListener('change', function () { S.s = selS.value; changed(); });
  selR.addEventListener('change', function () { S.r = selR.value; changed(); });
  function setL(v) { v = Math.max(1, Math.min(60, parseInt(v, 10) || S.l)); if (v !== S.l) { S.l = v; changed(); } else inL.value = S.l; }
  inL.addEventListener('change', function () { setL(inL.value); });
  $('gpLm').addEventListener('click', function () { setL(S.l - 1); });
  $('gpLp').addEventListener('click', function () { setL(S.l + 1); });
  var tt = 0;
  function toast(s) { var t = $('gpT'); t.textContent = s; t.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { t.classList.remove('on'); }, 2600); }
  $('gpFill').addEventListener('click', function () {
    if (!S.s) { toast(T.needSpec); selS.focus(); return; }
    load().then(function () {
      var ids = (C.b || {})[S.c + '-' + S.s] || [], g = fill(items, ids, S, weights()), n = Object.keys(g).length;
      if (!n) { toast(T.fillNone); return; }
      S.g = g; draw(); save(); toast(fmt(T.filled, { n: n }));
    }, function () { toast(T.loadErr); });
  });
  $('gpClear').addEventListener('click', function () { S.g = {}; draw(); save(); toast(T.cleared); });
  $('gpCopy').addEventListener('click', function () {
    save();
    var url = location.href.split('#')[0] + '#' + enc(S);
    var no = function () {
      var a = document.createElement('textarea'), done = false;
      a.value = url; a.setAttribute('readonly', ''); a.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
      document.body.appendChild(a); a.select();
      try { done = document.execCommand('copy'); } catch (x) {}
      a.remove();
      toast(done ? T.copied : T.nocopy);
    };
    try { navigator.clipboard.writeText(url).then(function () { toast(T.copied); }, no); } catch (x) { no(); }
  });
  addEventListener('hashchange', function () {
    var h = dec(location.hash);
    if (!clsOk(h.c) || enc(h) === enc(S)) return;
    S = { c: h.c, s: h.s, r: h.r, l: h.l || S.l, g: h.g, t: h.t };
    if (items) cleanS();
    changed();
    if (Object.keys(S.g).length) load().then(draw);
  });
  /* the items come on the first wish to pick: a pointer over the doll, a focus inside it, or a saved build to draw */
  var warm = function () { load().then(function () { draw(); save(); }, function () {}); };
  ['pointerover', 'focusin', 'touchstart'].forEach(function (ev) { gp.addEventListener(ev, warm, { once: true, passive: true }); });

  start(); bar();
  if (Object.keys(S.g).length) warm();
})(this);
