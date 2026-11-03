/* Site search of the guide: the header button .srchbtn (put in by build.py pwa()), Ctrl+K / ⌘K or "/" open a dialog over the page.
   The first open (or the pointer over the button) loads the index assets/search/<lang>.json (made by search.py from the built
   pages) and the engine assets/search/engine.js, which finds the entries: pages, sections with anchors, FAQ questions,
   dungeons. Text matches show a short excerpt. An empty query and a query with no answer show the popular links.
   Without the network the dialog says so and loads when the network is back.
   Arrows move the selection, Enter opens it, Esc closes. */
(() => {
  const SCRIPT = document.currentScript, ROOT = SCRIPT.dataset.root || './';
  const V = (SCRIPT.src.match(/[?&]v=(\w+)/) || [])[1] || '';
  const btn = document.querySelector('.srchbtn');
  if (!btn) return;
  const LANG = (l => ['ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl'].includes(l) ? l : 'en')(document.documentElement.lang.split('-')[0]);
  const L = {
    ru: { title: 'Поиск по сайту', ph: 'Класс, раса, подземелье, вопрос…', none: 'Ничего не нашлось.', pop: 'Популярное', go: 'Разделы', nav: 'выбрать', open: 'открыть', close: 'закрыть', err: 'Поиск не загрузился. Проверьте сеть и откройте ещё раз.', off: 'Нет сети. Поиск загрузится, когда она вернётся.', load: 'Загрузка…', found: n => `Найдено: ${n}` },
    en: { title: 'Search the site', ph: 'Class, race, dungeon, question…', none: 'Nothing found.', pop: 'Popular', go: 'Sections', nav: 'select', open: 'open', close: 'close', err: 'Search did not load. Check your connection and open it again.', off: 'No connection. Search will load when it is back.', load: 'Loading…', found: n => `Found: ${n}` },
    uk: { title: 'Пошук по сайту', ph: 'Клас, раса, підземелля, питання…', none: 'Нічого не знайшлося.', pop: 'Популярне', go: 'Розділи', nav: 'вибрати', open: 'відкрити', close: 'закрити', err: 'Пошук не завантажився. Перевірте мережу й відкрийте ще раз.', off: 'Немає мережі. Пошук завантажиться, коли вона повернеться.', load: 'Завантаження…', found: n => `Знайдено: ${n}` },
    de: { title: 'Seite durchsuchen', ph: 'Klasse, Volk, Dungeon, Frage…', none: 'Nichts gefunden.', pop: 'Beliebt', go: 'Bereiche', nav: 'wählen', open: 'öffnen', close: 'schließen', err: 'Die Suche wurde nicht geladen. Prüf die Verbindung und öffne sie erneut.', off: 'Keine Verbindung. Die Suche lädt, sobald sie zurück ist.', load: 'Wird geladen…', found: n => `Gefunden: ${n}` },
    fr: { title: 'Rechercher sur le site', ph: 'Classe, race, donjon, question…', none: 'Aucun résultat.', pop: 'Populaire', go: 'Rubriques', nav: 'choisir', open: 'ouvrir', close: 'fermer', err: 'La recherche ne s’est pas chargée. Vérifiez la connexion et rouvrez-la.', off: 'Pas de connexion. La recherche se chargera à son retour.', load: 'Chargement…', found: n => `Résultats : ${n}` },
    es: { title: 'Buscar en el sitio', ph: 'Clase, raza, mazmorra, pregunta…', none: 'Sin resultados.', pop: 'Populares', go: 'Secciones', nav: 'elegir', open: 'abrir', close: 'cerrar', err: 'La búsqueda no se cargó. Revisa la conexión y vuelve a abrirla.', off: 'Sin conexión. La búsqueda se cargará cuando vuelva.', load: 'Cargando…', found: n => `Resultados: ${n}` },
    pt: { title: 'Pesquisar no site', ph: 'Classe, raça, masmorra, pergunta…', none: 'Nada encontrado.', pop: 'Populares', go: 'Seções', nav: 'escolher', open: 'abrir', close: 'fechar', err: 'A pesquisa não carregou. Verifique a conexão e abra de novo.', off: 'Sem conexão. A pesquisa vai carregar quando ela voltar.', load: 'Carregando…', found: n => `Resultados: ${n}` },
    it: { title: 'Cerca nel sito', ph: 'Classe, razza, dungeon, domanda…', none: 'Nessun risultato.', pop: 'Popolari', go: 'Sezioni', nav: 'scegli', open: 'apri', close: 'chiudi', err: 'La ricerca non si è caricata. Controlla la connessione e riaprila.', off: 'Nessuna connessione. La ricerca si caricherà quando torna.', load: 'Caricamento…', found: n => `Risultati: ${n}` },
    pl: { title: 'Szukaj w serwisie', ph: 'Klasa, rasa, dungeon, pytanie…', none: 'Nic nie znaleziono.', pop: 'Popularne', go: 'Działy', nav: 'wybierz', open: 'otwórz', close: 'zamknij', err: 'Wyszukiwarka się nie wczytała. Sprawdź połączenie i otwórz ją ponownie.', off: 'Brak połączenia. Wyszukiwarka wczyta się, gdy wróci.', load: 'Wczytywanie…', found: n => `Znaleziono: ${n}` },
  }[LANG];
  const MAC = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
  const KEY = MAC ? '⌘K' : 'Ctrl K';
  btn.title = `${btn.getAttribute('aria-label')} (${KEY})`;
  btn.setAttribute('aria-keyshortcuts', MAC ? 'Meta+K' : 'Control+K');
  const kb = btn.querySelector('kbd');
  if (kb) kb.textContent = KEY;

  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  let eng = null, items = null, popular = [], loading = null;
  let dlg, input, list, foot, live, sel = -1, shown = [], opener = null;

  const script = src => new Promise((ok, no) => { const el = document.createElement('script'); el.src = src; el.onload = ok; el.onerror = no; document.head.append(el); });

  // the index and the engine (engine.js) come together on the first open: the page itself carries only this dialog
  function load() {
    if (loading) return loading;
    const ctl = typeof AbortController === 'function' ? new AbortController() : null, q = V ? '?v=' + V : '';
    let late = false;
    const slow = setTimeout(() => { late = true; if (ctl) ctl.abort(); }, 8000);   // a stalled request (no network behind the service worker) ends in a message
    loading = Promise.all([
      fetch(`${ROOT}assets/search/${LANG}.json${q}`, ctl ? { signal: ctl.signal } : {}).then(r => { if (!r.ok) throw r; return r.json(); }),
      globalThis.gabellaSearchEngine || script(`${ROOT}assets/search/engine.js${q}`),
    ]).then(([d]) => {
      if (late) throw new Error('late');
      clearTimeout(slow);
      eng = globalThis.gabellaSearchEngine(LANG, d);
      ({ items, popular } = eng);
      render();
    }).catch(() => { clearTimeout(slow); loading = null; if (dlg && dlg.open) msg(navigator.onLine === false || late ? L.off : L.err); });
    return loading;
  }
  addEventListener('online', () => { if (!items && dlg && dlg.open) load(); });

  function build() {
    dlg = document.createElement('dialog');
    dlg.className = 'srch';
    dlg.setAttribute('aria-label', L.title);
    dlg.innerHTML = `<div class="srch-in"><div class="srch-f"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>
<input type="search" role="combobox" aria-expanded="true" aria-controls="srchList" aria-autocomplete="list" autocomplete="off" spellcheck="false" enterkeyhint="go" placeholder="${esc(L.ph)}" aria-label="${esc(L.title)}">
<button type="button" class="srch-x" aria-label="${esc(L.close)}"><kbd>Esc</kbd><svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button></div>
<ul class="srch-l" id="srchList" role="listbox" aria-label="${esc(L.title)}"></ul>
<p class="srch-h" aria-hidden="true"><span><kbd>↑</kbd><kbd>↓</kbd> ${esc(L.nav)}</span><span><kbd>Enter</kbd> ${esc(L.open)}</span><span><kbd>Esc</kbd> ${esc(L.close)}</span></p>
<p class="sr" aria-live="polite"></p></div>`;
    document.body.append(dlg);
    input = dlg.querySelector('input'); list = dlg.querySelector('.srch-l'); foot = dlg.querySelector('.srch-h'); live = dlg.querySelector('.sr');
    input.addEventListener('input', () => render());
    input.addEventListener('keydown', key);
    dlg.querySelector('.srch-x').onclick = close;
    dlg.addEventListener('click', e => { if (e.target === dlg) close(); });   // click on the backdrop
    dlg.addEventListener('close', () => { document.documentElement.classList.remove('srch-on'); if (opener) opener.focus({ preventScroll: true }); });
    list.addEventListener('click', e => { if (e.target.closest('a')) dlg.close(); });
    list.addEventListener('mousemove', e => { const li = e.target.closest('[role="option"]'); if (li) pick(+li.dataset.i, false); });
  }

  function open() {
    if (!dlg) build();
    if (dlg.open) { input.select(); return; }
    opener = document.activeElement;
    load();
    render();
    dlg.showModal();
    document.documentElement.classList.add('srch-on');
    input.select();
  }
  function close() { if (dlg && dlg.open) dlg.close(); }

  function mark(text, ntext, toks) {
    const hits = [];
    const W = /[\p{L}\p{N}]/u;   // the mark covers the whole word ("магия" for "маг"), not a cut piece of it
    for (const t of toks) if (t) for (let i = ntext.indexOf(t); i >= 0; i = ntext.indexOf(t, i + t.length)) {
      let a = i, b = i + t.length;
      while (a > 0 && W.test(ntext[a - 1])) a--;
      while (b < ntext.length && W.test(ntext[b])) b++;
      hits.push([a, b]);
    }
    hits.sort((a, b) => a[0] - b[0]);
    let o = '', p = 0;
    for (const [a, b] of hits) { if (a < p) continue; o += esc(text.slice(p, a)) + '<mark>' + esc(text.slice(a, b)) + '</mark>'; p = b; }
    return o + esc(text.slice(p));
  }

  // The text holds one line per block (paragraph, list item, card). The excerpt is the line of sentence length with the most
  // query words, cut to ~150 characters around the first of them; short lines (card labels, chips) are matched but never shown.
  function excerpt(it, toks) {
    if (!toks || !it.x || toks.every(t => it.nt.includes(t))) return '';
    let best = null;
    for (let a = 0, b; a < it.x.length; a = b + 1) {
      b = it.x.indexOf('\n', a);
      if (b < 0) b = it.x.length;
      const line = it.nx.slice(a, b), n = toks.filter(t => line.includes(t)).length;
      if (n && b - a >= 40 && (!best || n > best[2])) best = [a, b, n];
    }
    if (!best) return '';
    const [s, e] = best, at = Math.min(...toks.map(t => it.nx.indexOf(t, s)).filter(i => i >= 0 && i < e));
    let a = Math.max(s, at - 40), b = Math.min(e, at + 110);
    if (a > s) a = it.x.indexOf(' ', a) + 1 || a;
    if (b < e) b = it.x.lastIndexOf(' ', b) > at ? it.x.lastIndexOf(' ', b) : b;
    return (a > s ? '…' : '') + mark(it.x.slice(a, b), it.nx.slice(a, b), toks) + (b < e ? '…' : '');
  }

  const ICON = ['<path d="M4 5h16v14H4zM4 9h16"/>', '<path d="M5 7h14M5 12h14M5 17h9"/>', '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5V14M12 17.5h.01"/>',
    '<path d="M4 20V10l8-6 8 6v10M9 20v-5h6v5"/>'];

  function row(it, i, toks) {
    const ex = excerpt(it, toks);
    return `<li role="presentation"><a role="option" id="sr-${i}" data-i="${i}" aria-selected="false" href="${esc(ROOT + it.u)}" tabindex="-1">`
      + `<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${ICON[it.k]}</svg>`
      + `<span class="srch-t"><b>${toks ? mark(it.t, it.nt, toks) : esc(it.t)}</b>${it.s ? `<small>${esc(it.s)}</small>` : ''}${ex ? `<span class="srch-x2">${ex}</span>` : ''}</span></a></li>`;
  }

  function msg(text) { list.innerHTML = `<li class="srch-m">${esc(text)}</li>`; shown = []; sel = -1; input.removeAttribute('aria-activedescendant'); live.textContent = text; }

  const group = (label, from, rows, toks) => `<li class="srch-g" role="presentation">${esc(label)}</li>` + rows.map((it, i) => row(it, from + i, toks)).join('');

  function render() {
    if (!dlg) return;
    const q = input.value;
    if (!items) { msg(L.load); return; }
    if (!q.trim()) {
      const go = items.filter(it => {
        const rel = (LANG === 'ru' ? it.u : it.u.slice(LANG.length + 1)).split('/').filter(Boolean);
        return it.k === 0 && (rel.length === 1 && rel[0] !== 'privacy' || rel.length === 2 && rel[0] === 'guides') && !popular.some(p => p.u === it.u);
      });
      shown = [...popular, ...go];
      list.innerHTML = group(L.pop, 0, popular, null) + group(L.go, popular.length, go.map(it => ({ ...it, s: '' })), null);   // no «Home» under every section
      live.textContent = '';
      pick(0, false);
      return;
    }
    shown = eng.find(q);
    if (!shown.length) {   // nothing: the popular questions instead of a dead end
      shown = popular;
      list.innerHTML = `<li class="srch-m">${esc(L.none)}</li>` + group(L.pop, 0, popular, null);
      live.textContent = L.none;
      pick(-1, false);
      return;
    }
    const toks = [...new Set(eng.terms(shown.used).flatMap(t => t.alts.flatMap(a => a.toks)))];
    list.innerHTML = shown.map((it, i) => row(it, i, toks)).join('');
    live.textContent = L.found(shown.length);
    pick(0, false);
  }

  function pick(i, scroll = true) {
    if (sel >= 0) { const o = list.querySelector(`#sr-${sel}`); if (o) o.setAttribute('aria-selected', 'false'); }
    sel = i;
    const li = i >= 0 && list.querySelector(`#sr-${i}`);
    if (!li) { input.removeAttribute('aria-activedescendant'); return; }
    li.setAttribute('aria-selected', 'true');
    input.setAttribute('aria-activedescendant', li.id);
    if (scroll) li.scrollIntoView({ block: 'nearest' });
  }

  function key(e) {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      if (shown.length) pick((sel + (e.key === 'ArrowDown' ? 1 : -1) + shown.length) % shown.length);
    } else if (e.key === 'Enter' && sel >= 0) {
      e.preventDefault();
      const a = list.querySelector(`#sr-${sel}`);
      if (e.ctrlKey || e.metaKey) { window.open(a.href, '_blank', 'noopener'); return; }
      dlg.close();
      a.click();
    }
  }

  globalThis.gabellaFind = q => load().then(() => (eng ? eng.find(q) : []));   // the same search for the FAQ filter (build_guides.py)
  btn.addEventListener('click', open);
  btn.addEventListener('pointerenter', () => { if (!items) load(); }, { once: true });
  addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && !e.altKey && !e.shiftKey && (e.code === 'KeyK' || e.key.toLowerCase() === 'k')) {
      e.preventDefault();
      open();
    } else if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey && !(dlg && dlg.open)) {
      const el = document.activeElement;
      if (el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName))) return;
      e.preventDefault();
      open();
    }
  });
})();
