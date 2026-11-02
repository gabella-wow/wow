/* Profile pages (roster, profile, u): game data, the player card, the big card, achievement tiles, page chrome.
   Inlined by build_me.py before the page script; Russian strings are translated at build like the rest of the site.
   The pages talk to the API only through window.GabellaMe (me.js), which runs before DOMContentLoaded. */
const GD = @@GD@@;
const SOC = @@SOC@@;   // build.SOCIAL: the Players page and everything that points to it are hidden
const ACH = @@ACH@@;   // build.ACHIEVEMENTS: achievements, ranks, points and frames are hidden except the «Founder» mark
const ROOT = '@@ROOT@@', HOME = '@@HOME@@', LANG = '@@LANG@@', HL = document.documentElement.lang;
const PV = /*PV*/'', AV = /*AV*/'';   // ?v= of the class and race portraits (build.art_version) and of the achievement icons (build.me_version)
const $ = (s, el) => (el || document).querySelector(s), $$ = (s, el) => [...(el || document).querySelectorAll(s)];
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
const fill = (s, o) => s.replace(/%(\w)/g, (m, k) => (k in o ? o[k] : m));
const ROLE = { tank: 'Танк', heal: 'Лекарь', dps: 'Урон' };
const TIME = { morning: 'Утро', evening: 'Вечер', night: 'Ночь' };
const FACN = { alliance: 'Альянс', horde: 'Орда' };
const LFG = { dungeon: 'Подземелье', raid: 'Рейд', quest: 'Задания' };
const TICO = { morning: 'sun', evening: 'moon', night: 'moon' };
const ico = n => `<svg class="ico" aria-hidden="true"><use href="#i-${n}"/></svg>`;
const race = id => GD.races[id] || { f: 'alliance', n: id, slug: 'human', cls: [] };
const cls = id => GD.classes[id] || { n: id, color: '#c9a54a', roles: [] };
const lookOf = c => c.look || { sex: (GD.looks.races[c.race] || { sex: 'm' }).sex, bg: (GD.looks.races[c.race] || {}).bg || race(c.race).slug };
/** Character portrait: transparent base, portrait background, and the old race face in case loading fails. */
const pic = c => {
  const l = lookOf(c), s = race(c.race).slug, v = '?v=' + GD.looks.v;
  return { src: `${ROOT}assets/me/look/base/${s}-${l.sex}.webp${v}`, bg: `${ROOT}assets/me/look/bg/${l.bg}.webp${v}`, old: `${ROOT}assets/art/${s}-face.webp${PV}` };
};
const isFounder = p => p.frame === 'founder' || (p.achievements || []).some(a => a.id === 'founder');
const shownFrame = (frame, p) => (ACH ? frame : p && isFounder(p) || frame === 'founder' ? 'founder' : 'recruit');
const ring = (frame, p, extra) => {
  frame = shownFrame(frame);
  const o = typeof p === 'string' ? { src: p } : p;
  return `<span class="me-ring fr-${esc(frame || 'recruit')}${extra ? ' ' + extra : ''}"><img src="${o.src}" alt="" width="64" height="64" loading="lazy" decoding="async"${o.bg ? ` style="background-image:url('${o.bg}')" data-old="${o.old}"` : ''}></span>`;
};
// base failed to load: fall back to the old race face
document.addEventListener('error', e => {
  const i = e.target;
  if (i.tagName === 'IMG' && i.dataset && i.dataset.old) { i.src = i.dataset.old; i.style.backgroundImage = ''; delete i.dataset.old; }
}, true);
const subline = c => `${esc(race(c.race).n)} · ${esc(cls(c.class).n)}`;
const profLine = (c, hi) => [[c.prof1, c.prof1_skill], [c.prof2, c.prof2_skill]].filter(p => p[0])
  .map(([p, s]) => (p === hi ? '<b>' : '') + esc(GD.profs[p] || p) + (s ? ` ${s}` : '') + (p === hi ? '</b>' : '')).join(', ');
const playerUrl = id => `${HOME}u/#${id}`;
const achIcon = id => `${ROOT}assets/me/ach/${id}.webp${AV}`;   // painted icons; secret.webp hides an unfound secret
const dateOf = t => new Date(t).toLocaleDateString(HL);
const unit = (n, u) => new Intl.NumberFormat(HL, { style: 'unit', unit: u, unitDisplay: 'short', maximumFractionDigits: 0 }).format(n);
function ago(t) {
  const s = (t - Date.now()) / 1000, rtf = new Intl.RelativeTimeFormat(HL, { numeric: 'auto' });
  for (const [u, k] of [['day', 86400], ['hour', 3600], ['minute', 60]]) if (Math.abs(s) >= k) return rtf.format(Math.round(s / k), u);
  return rtf.format(0, 'minute');
}
function left(until) {
  const m = Math.max(1, Math.round((until - Date.now()) / 60000)), h = Math.floor(m / 60);
  return (h ? unit(h, 'hour') + ' ' : '') + (m % 60 ? unit(m % 60, 'minute') : '');
}

// texts of achievements, ranks and frames (assets/me/i18n-<lang>.json), loaded once by ready()
let T = { ui: {}, cats: {}, ranks: {}, frames: {}, ach: {}, pts: {}, secret: [], g: {} };
const achName = id => (T.ach[id] ? T.ach[id][0] : id);
const rankName = id => T.ranks[id] || id;
const frameName = id => T.frames[id] || id;
const rankPts = id => (GD.ranks.find(r => r.id === id) || { pts: 0 }).pts;
const nextRank = pts => GD.ranks.find(r => r.pts > pts) || null;
const rankOf = pts => GD.ranks.filter(r => r.pts <= pts).pop().id;

/** Runs the page once me.js is there and the texts are loaded; M is null when me.js did not load. */
function ready(cb) {
  addEventListener('DOMContentLoaded', () => {
    const M = window.GabellaMe;
    if (!M) return cb(null);
    M.texts().then(t => { T = t; cb(M); }, () => cb(M));
  });
}

/** Level badge on a portrait; a check mark after a level an admin has confirmed. c: {level, verified}. */
const lvBadge = c => `<span class="lv${c.verified ? ' ver' : ''}" aria-label="Уровень ${c.level}${c.verified ? ', ' + esc(tg('verified')) : ''}">${c.level}${c.verified ? '<i aria-hidden="true">✓</i>' : ''}</span>`;

/** Player card of the roster and the character lists. p: {id, nick, frame, rank, lfg, main, alts}. */
function pcard(p, o) {
  o = o || {};
  const c = p.main, f = race(c.race).f;
  const meta = [`<span>${ico(c.role)}${esc(ROLE[c.role] || '')}</span>`];
  const pl = profLine(c, o.prof);
  if (pl) meta.push(`<span>${pl}</span>`);
  meta.push(`<span>${ico(TICO[c.playtime] || 'moon')}${esc(TIME[c.playtime] || '')}</span>`);
  if (p.lfg) meta.push(`<span class="lfg">${esc(LFG[p.lfg.kind] || '')} · ${esc(left(p.lfg.until))}</span>`);
  const name = o.link === false ? `<b>${esc(c.name)}</b>` : `<a href="${playerUrl(p.id)}">${esc(c.name)}</a>`;
  const alts = (p.alts || []).length ? `<div class="alts">Твинки: ${p.alts.map(a => `<i style="--ac:${cls(a.class).color}">${esc(a.name)}</i>`).join(', ')}</div>` : '';
  return `<article class="pcard${o.cls ? ' ' + o.cls : ''}" style="--cc:${cls(c.class).color}"${o.attrs || ''}>
    <span class="pic">${ring(shownFrame(p.frame || p.rank, p), pic(c))}${lvBadge(c)}</span>
    <span class="fx ${f}">${esc(o.tag || FACN[f])}</span>
    <div class="nm">${name}</div>
    <span class="sub">${subline(c)}</span>
    <div class="meta">${meta.join('')}</div>${alts}${p.member || p.nick ? `<div class="nick">${p.member ? `<span class="team"><img src="${ROOT}assets/brand/mark.webp" alt="" width="14" height="14">Gabella Team</span>` : ''}${p.nick ? `<span>${esc(p.nick)}</span>` : ''}</div>` : ''}${o.after || ''}
  </article>`;
}

/** Check mark after a level an admin has confirmed. */
const verMark = c => (c.verified ? `<span class="g-ver" role="img" aria-label="${esc(tg('verified'))}" title="${esc(tg('verified'))}">✓</span>` : '');

/** Card menu («…» with the report item) for signed-in people looking at somebody else. */
const cardMenu = (id, cls) => `<details class="g-menu${cls ? ' ' + cls : ''}"><summary aria-label="${esc(tg('menu'))}" title="${esc(tg('menu'))}">⋯</summary><button type="button" data-report="${esc(id)}">${esc(tg('report'))}</button></details>`;

/** Report dialog: what is wrong (name, other), an optional reason, POST /reports; success is a quiet toast. */
function reportDialog(M, target, name) {
  const opts = ['name', 'other'].map(k => [k, tg('report_' + k)]);
  const d = document.createElement('dialog');
  d.className = 'g-dlg';
  d.setAttribute('aria-labelledby', 'repH');
  d.innerHTML = `<form class="g-rf"><h2 id="repH">${esc(tg('report'))}: ${esc(name)}</h2>
    <fieldset><legend>${esc(tg('report_field'))}</legend>${opts.map(([k, label], i) => `<label class="g-rr"><input type="radio" name="f" value="${k}"${i ? '' : ' checked'}>${esc(label)}</label>`).join('')}</fieldset>
    <label class="g-rl">${esc(tg('report_reason'))}<input type="text" name="r" maxlength="80" autocomplete="off"></label>
    <p class="msg err" role="alert"></p>
    <div class="row"><button type="submit" class="btn">${esc(tg('report_send'))}</button><button type="button" class="btn ghost" data-x>${esc(tg('report_cancel'))}</button></div></form>`;
  document.body.append(d);
  const f = $('form', d), msg = $('.msg', d), ok = $('[type=submit]', d);
  const close = () => { d.close ? d.close() : d.removeAttribute('open'); };
  d.addEventListener('close', () => d.remove());
  $('[data-x]', d).onclick = close;
  d.addEventListener('click', e => { if (e.target === d) close(); });
  f.onsubmit = e => {
    e.preventDefault();
    const field = f.elements.f.value, reason = f.elements.r.value.trim() || opts.find(o => o[0] === field)[1];   // the API wants a reason: the field's own name when none is typed
    ok.disabled = true; msg.textContent = '';
    M.api('/reports', { body: { target, field, reason } }).then(() => { close(); M.toast({ kind: 'note', id: 'report_sent' }); }, err => {
      ok.disabled = false;
      msg.textContent = tg(err.code === 'report_limit' ? 'report_limit' : 'err_report');
    });
  };
  if (d.showModal) d.showModal(); else d.setAttribute('open', '');
  f.elements.f.focus();
}

/** Rank block of the big card: points, rank, bar to the next one. */
function rankBlock(pts) {
  const r = rankOf(pts), nx = nextRank(pts), from = rankPts(r);
  const pct = nx ? Math.round(100 * (pts - from) / (nx.pts - from)) : 100;
  return `<div class="rk"><span class="pts"><span class="shield" aria-hidden="true">★</span>${pts}</span>
    <span class="rn">Ранг: ${esc(rankName(r))}</span><span class="bar"><i style="width:${pct}%"></i></span>
    <small>${nx ? esc(fill('До ранга «%r»: %n', { n: nx.pts - pts, r: rankName(nx.id) })) : 'Высший ранг'}</small></div>`;
}

/** The big card, «how others see you». p: player shape plus points, joined or since. */
function bcard(p, o) {
  o = o || {};
  const c = p.main, src = `${ROOT}assets/art/${race(c.race).slug}-896.webp${PV}`;
  const who = [];
  if (!ACH && isFounder(p)) who.push(esc(frameName('founder')));
  if (p.nick) who.push(esc(p.nick));
  if (p.joined) who.push(esc(fill('В Gabella Team с %d', { d: dateOf(p.joined) })));
  else if (p.member) who.push('Gabella Team');
  else if (p.since) who.push(esc(fill('На сайте с %d', { d: dateOf(p.since) })));
  const h = o.h || 'h1';
  return `<section class="bcard" style="--cc:${cls(c.class).color}" aria-label="Карточка игрока">
    <img class="bg" src="${src}" alt="" decoding="async">
    <div class="in">${ring(shownFrame(p.frame || p.rank, p), pic(c), o.reveal ? 'reveal' : '')}
      <div><${h}>${esc(c.name)}</${h}>
        <span class="sub">${subline(c)} · ${c.level}${verMark(c)} · ${esc(ROLE[c.role] || '')}</span>
        ${who.length ? `<p class="who">${who.join(' · ')}</p>` : ''}</div>
      ${ACH ? rankBlock(p.points || 0) : ''}</div></section>`;
}

/** Progress of an achievement toward its goal: {v, goal, text} or null when it is all-or-nothing.
    ctx: {progress, user, chars, have:Set}; user and chars are known only for the person themself. */
function achProgress(a, ctx) {
  const r = a.rule || {}, P = (ctx.progress || {})[r.key] || { value: 0, items: [] };
  let v = null, goal = null;
  if (a.kind === 'progress' && r.key) {
    if (r.items) return null;
    if (r.all) { goal = (GD.sets[r.key] || []).length; v = (P.items || []).filter(x => GD.sets[r.key].includes(x)).length; }
    else { goal = r.goal; v = r.set ? (P.items || []).length : P.value || 0; }
    if (goal <= 1) return null;
  } else if (ctx.user) {
    const u = ctx.user;
    if (r.days && u.joined_guild_at) { goal = r.days; v = Math.floor((Date.now() - u.joined_guild_at) / 86400000); }
    else if (r.refs) { goal = r.refs; v = u.refs || 0; }
    else if (r.streak) { goal = r.streak; v = u.streak || 0; }
    else if (a.id === 'three_chars') { goal = 3; v = (ctx.chars || []).length; }
    else if (r.all_cat) { const ids = GD.ach.filter(x => x.cat === r.all_cat && x.id !== a.id).map(x => x.id); goal = ids.length; v = ids.filter(x => ctx.have.has(x)).length; }
  }
  if (goal === null) return null;
  v = Math.max(0, Math.min(v, goal));
  const text = r.key === 'radio_min' ? `${unit(Math.floor(v / 60), 'hour')} / ${unit(goal / 60, 'hour')}` : fill('%v из %g', { v, g: goal });
  return { v, goal, text };
}

/** Achievement tile. st: {at} when owned; marks: [[label, on]] for the comparison. */
function achTile(a, st, ctx, marks) {
  const own = !!st, hide = a.secret && !own && !(marks && marks.some(m => m[1]));
  const t = T.ach[a.id] || [a.id, ''];
  const name = hide ? 'Секрет' : t[0];
  const desc = hide ? fill('Подсказка: %h', { h: t[2] || '?' }) : t[1];
  let foot = '';
  if (marks) foot = `<span class="marks">${marks.map(([l, on]) => `<span class="${on ? 'on' : ''}">${esc(l)}</span>`).join('')}</span>`;
  else if (own) foot = `<span class="when">${esc(fill('Получено %d', { d: dateOf(st.at) }))}</span>`;
  else if (ctx && !hide) {
    const pr = achProgress(a, ctx);
    if (pr) foot = `<span class="prog"><span class="bar"><i style="width:${Math.round(100 * pr.v / pr.goal)}%"></i></span>${esc(pr.text)}</span>`;
  }
  return `<div class="ach${own || (marks && marks.some(m => m[1])) ? '' : ' lock'}${hide ? ' secret' : ''}">
    <span class="ic"><img src="${achIcon(hide ? 'secret' : a.id)}" alt="" width="46" height="46" loading="lazy"></span><b>${esc(name)}</b>
    <span class="shield" aria-label="${a.pts} ${esc(T.ui.pts || '')}">${a.pts}</span><p>${esc(desc)}</p>${foot}</div>`;
}


/* ---------- texts of the MORE set (T.g): {n}, {x} ... are filled from o ---------- */
const tg = (k, o) => Object.keys(o || {}).reduce((s, x) => s.split('{' + x + '}').join(o[x]), (T.g || {})[k] || k);

/** Team feed line: who got what. */
function feedLine(x) {
  const who = `<a href="${playerUrl(x.user)}">${esc(x.name)}</a>`;
  const what = x.kind === 'rank' ? fill(esc('%n достигает ранга «%r»'), { n: who, r: `<em>${esc(rankName(x.ref))}</em>` })
    : x.ref === 'secret' ? fill(esc('%n находит секрет'), { n: who })
    : fill(esc('%n получает «%a»'), { n: who, a: `<em>${esc(achName(x.ref))}</em>` });
  return `<div class="it">${ring(x.frame || 'recruit', pic(x))}<span>${what}</span><small>${esc(ago(x.at))}</small></div>`;
}

async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; } catch (e) { return false; }
}

/* ---------- page chrome: theme, top bar, menu sheet ---------- */
const themeBtns = document.querySelectorAll('.themebtn');
function paintTheme() { const t = document.documentElement.getAttribute('data-theme'); themeBtns.forEach(b => b.querySelector('use').setAttribute('href', t === 'light' ? '#i-moon' : '#i-sun')); const m = document.querySelector('meta[name="theme-color"]'); if (m) m.setAttribute('content', t === 'light' ? '#fbfaf7' : '#050505'); }
themeBtns.forEach(b => b.onclick = () => { const t = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light'; document.documentElement.setAttribute('data-theme', t); try { localStorage.setItem('wf-theme', t); } catch (e) {} paintTheme(); });
paintTheme();
const topbar = $('#topbar');
let barTick = false;
const overArt = !!document.querySelector('.thero');   // without hero art under it the bar stays solid
function paintBar() { topbar.classList.toggle('solid', !overArt || window.scrollY > 24); barTick = false; }
window.addEventListener('scroll', () => { if (!barTick) { barTick = true; requestAnimationFrame(paintBar); } }, { passive: true });
paintBar();
const moreDlg = $('#moreDlg');
const moreX = on => document.querySelectorAll('[aria-controls="moreDlg"]').forEach(b => b.setAttribute('aria-expanded', on));
document.querySelectorAll('.menubtn, .morebtn').forEach(b => b.onclick = () => { if (moreDlg.showModal) moreDlg.showModal(); else moreDlg.setAttribute('open', ''); moreX(true); });
moreDlg.addEventListener('close', () => moreX(false));
$('#moreClose').onclick = () => moreDlg.close();
moreDlg.addEventListener('click', e => { if (e.target === moreDlg || e.target.closest('.toc a')) moreDlg.close(); });
