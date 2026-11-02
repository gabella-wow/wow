/* Search engine of the site search (search.js loads it with the index on the first open; tests/search_eval.js runs it in node).
   gabellaSearchEngine(lang, index) -> { items, popular, find(q), terms(q), norm(s) }.
   The index (search.py): entries (pages, sections with anchors, FAQ questions, dungeons), aliases (other names -> the name on
   these pages), questions (phrase -> answer), the popular links and the stop words.
   Every word of the query but the stop words must match, through any of its variants: itself, its stem, its cut start
   ("прокачать" -> "прокач"), an alias, the other alphabet ("kak prokachat" -> "как прокачат", "легаси" -> "legasi") and,
   when no word of the site starts with it, the nearest word of the site (one typo up to 6 letters, two from 7, swapped
   neighbours count as one). The start of a word in the title scores most, then the keys (where the entry is, page title
   and description, other names of a dungeon), inside a word, the text. A query that is a known question puts its answer
   first. A level number (24, "dungeons 24") lists the dungeons for that level. A query typed in the wrong keyboard layout
   (vfu -> маг) is retried in the other one when nothing matches. */
globalThis.gabellaSearchEngine = (LANG, d) => {
  // lower case without accents, ё -> е; one output character per input character, so positions match the original text
  const norm = s => {
    let o = '';
    for (const ch of s) {
      const c = ch.toLowerCase().normalize('NFD')[0];
      o += (c === 'ё' ? 'е' : c === 'ї' ? 'і' : c) + (ch.length > 1 ? ' ' : '');
    }
    return o;
  };
  const SPLIT = /[\s\-–—.,:;!?()«»"“”„'’/·]+/;
  const words = s => s.split(SPLIT).filter(Boolean);
  const EN = '`qwertyuiop[]asdfghjkl;\'zxcvbnm,.', RU = 'ёйцукенгшщзхъфывапролджэячсмитьбю', UK = 'ʼйцукенгшщзхїфівапролджєячсмитьбю';
  const swap = (s, from, to) => [...s].map(c => { const i = from.indexOf(c); return i < 0 ? c : to[i]; }).join('');
  // endings cut off for the stem ("мага" -> "маг", "choosing" -> "choos"); the stem keeps at least 3 letters
  const END = {
    ru: 'ями ами ого его ому ему ыми ими ой ей ий ый ая яя ое ее ые ие ую юю ов ев ам ям ах ях ом ем а я о е ы и у ю ь',
    uk: 'ями ами ого ому ими ою ею ій ий ая яя ее ие ів ам ям ах ях ом ем а я о е и і у ю ь',
    en: 'ing ers ies es ed er s e', de: 'en er es e n s', fr: 'es s e', es: 'es os as s a o e', pt: 'es os as s a o e',
    it: 'i e a o', pl: 'ami ach ow om ego emu ej a e y i u o',
  }[LANG].split(' ').map(e => norm(e));   // normalized like the text: -ий is -ии after й -> и
  // the other alphabet: Latin typed on the ru/uk pages, Cyrillic spellings of English words on every page
  const LAT = Object.entries(LANG === 'uk'
    ? { shch: 'щ', zh: 'ж', kh: 'х', ch: 'ч', sh: 'ш', ts: 'ц', ye: 'є', yi: 'і', yu: 'ю', ya: 'я', ia: 'я', iu: 'ю', a: 'а', b: 'б', v: 'в', h: 'г', g: 'г', d: 'д', e: 'е', z: 'з', y: 'и', i: 'і', j: 'и', k: 'к', l: 'л', m: 'м', n: 'н', o: 'о', p: 'п', r: 'р', s: 'с', t: 'т', u: 'у', f: 'ф', c: 'ц', w: 'в', x: 'кс', q: 'к' }
    : { shch: 'щ', sch: 'щ', zh: 'ж', kh: 'х', ch: 'ч', sh: 'ш', ts: 'ц', yu: 'ю', ya: 'я', yo: 'е', ju: 'ю', ja: 'я', a: 'а', b: 'б', v: 'в', g: 'г', d: 'д', e: 'е', z: 'з', i: 'и', y: 'ы', j: 'и', k: 'к', l: 'л', m: 'м', n: 'н', o: 'о', p: 'п', r: 'р', s: 'с', t: 'т', u: 'у', f: 'ф', h: 'х', c: 'ц', w: 'в', x: 'кс', q: 'к' });
  const CYR = { а: 'a', б: 'b', в: 'v', г: 'g', ґ: 'g', д: 'd', е: 'e', є: 'ye', ж: 'zh', з: 'z', и: 'i', і: 'i', к: 'k', л: 'l', м: 'm', н: 'n', о: 'o', п: 'p', р: 'r', с: 's', т: 't', у: 'u', ф: 'f', х: 'h', ц: 'c', ч: 'ch', ш: 'sh', щ: 'sch', ъ: '', ы: 'y', ь: '', э: 'e', ю: 'yu', я: 'ya' };
  function translit(t) {
    if (/^[a-z]+$/.test(t)) {
      if (LANG !== 'ru' && LANG !== 'uk') return t;
      let o = '';
      for (let i = 0; i < t.length;) {
        const [k, v] = LAT.find(([k]) => t.startsWith(k, i)) || ['', ''];
        o += k === 'y' && LANG === 'ru' && /[aeiou]/.test(t[i - 1] || '') ? 'и' : v;   // "kakoy": й after a vowel (norm keeps й as и)
        i += k.length || 1;
      }
      return o || t;
    }
    return /^[а-яіє]+$/.test(t) ? [...t].map(c => CYR[c] ?? c).join('') || t : t;   // "ььь" has no latin form: an empty token would match everything
  }

  const items = d.i.map(([t, s, u, k, keys, x]) => ({ t, s, u, k, x, nt: norm(t), nk: norm(s + ' ' + keys), nx: norm(x) }));
  for (const it of items) it.ntw = words(it.nt).join(' ');
  const alias = {};
  for (const [a, v] of Object.entries(d.a)) alias[norm(a)] = v.split('|').map(words);
  const asks = d.q.map(([u, ph]) => [items.find(it => it.u === u), ph.split('|').map(p => words(norm(p)))]);
  const popular = d.p.map(([t, u]) => { const it = items.find(x => x.u === u); return { ...it, t, nt: norm(t), x: '', s: it.k ? it.s : '' }; });
  const stop = new Set(words(norm(d.s)));
  // every word of the site, for typos: names, keys, aliases and the text
  const vw = new Set([...Object.keys(alias), ...Object.values(d.a)].flatMap(x => words(norm(x))));
  for (const it of items) for (const x of words(it.nt + ' ' + it.nk + ' ' + it.nx)) if (x.length > 2 && !/\d/.test(x)) vw.add(x);
  const vocab = [...vw].sort();

  // where a token is in a string: 2 at the start of a word, 1 inside a word, 0 nowhere
  function at(s, t) {
    let i = s.indexOf(t);
    if (i < 0) return 0;
    for (; i >= 0; i = s.indexOf(t, i + 1)) if (i === 0 || SPLIT.test(s[i - 1])) return 2;
    return 1;
  }

  // one token against an entry: [score, matched the name or the keys]
  function hit(it, t) {
    const a = at(it.nt, t);
    if (a === 2) return [10, true];
    const b = at(it.nk, t);
    if (b === 2) return [5, true];
    if (a && t.length > 3) return [3, true];   // inside a word: "мак" is not "Шамана"
    if (b && t.length > 3) return [2, true];
    const c = at(it.nx, t);
    return c === 2 || (c && t.length > 4) ? [1, false] : [0, false];
  }

  const stem = t => { if (t.length > 3) for (const e of END) if (t.endsWith(e) && t.length - e.length >= 3) return t.slice(0, -e.length); return t; };
  const cut = t => (t.length >= 6 ? t.slice(0, Math.max(4, Math.round(t.length * 0.65))) : t);   // other forms of a long word: "прокачать" -> "прокач"
  const names = new Set(items.filter(it => it.k === 0 && /(?:classes|races)\/[\w-]+\/$/.test(it.u)).flatMap(it => words(it.nt).map(stem)));   // class and race names

  // a word of the site starts with the token (binary search in the sorted vocabulary)
  function known(t) {
    let a = 0, b = vocab.length;
    while (a < b) { const m = (a + b) >> 1; if (vocab[m] < t) a = m + 1; else b = m; }
    return a < vocab.length && vocab[a].startsWith(t);
  }

  // edit distance (with swapped neighbours) from a to the nearest start of b; more than k -> k + 1
  function dist(a, b, k) {
    const n = a.length, m = Math.min(b.length, n + k);
    if (m < n - k) return k + 1;
    let p2 = null, p = Array.from({ length: m + 1 }, (_, j) => j);
    for (let i = 1; i <= n; i++) {
      const c = [i];
      let low = i;
      for (let j = 1; j <= m; j++) {
        let v = Math.min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
        if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) v = Math.min(v, p2[j - 2] + 1);
        c.push(v);
        if (v < low) low = v;
      }
      if (low > k) return k + 1;
      p2 = p; p = c;
    }
    return Math.min(...p.slice(Math.max(0, n - k)));
  }

  // a typo: the site words nearest to the token, only when no word starts with it; loose: a spelling in the other
  // alphabet ("legasi" for "legacy") is allowed one change more
  const seen = new Map();   // typing repeats the words already typed: each is looked up once
  function fuzzy(t, loose) {
    const key = t + (loose ? '+' : '');
    if (!seen.has(key)) seen.set(key, near(t, loose));
    return seen.get(key);
  }
  function near(t, loose) {
    if (t.length < 4 || /\d/.test(t) || known(t)) return [];
    const k = (t.length >= 7 ? 2 : 1) + (loose && t.length >= 5 ? 1 : 0);
    let best = k + 1, out = [];
    for (const w of vocab) {
      if (w.length < t.length - k) continue;
      const dd = dist(t, w, Math.min(k, best));
      if (dd < best) { best = dd; out = [w]; } else if (dd === best && dd <= k && out.length < 6) out.push(w);
    }
    return best <= k ? out : [];
  }

  // the variants of one word
  function variants(t) {
    const out = [{ toks: [t], w: 1 }];
    const more = (k, w) => { for (const x of alias[k] || alias[stem(k)] || []) out.push({ toks: x, w }); };   // "рогу" -> «рога»
    more(t, 0.9);
    const tr = translit(t), base = [[t, 1]], named = alias[t] || alias[stem(t)];   // a word with an alias is no typo: "надеть" is not "nadet" ~ "nachtelf"
    if (tr !== t) { base.push([tr, 0.85]); out.push({ toks: [tr], w: 0.85 }); more(tr, 0.8); }
    for (const [x, w] of base) {
      const s = stem(x), c = cut(x);
      if (s !== x) out.push({ toks: [s], w: w * 0.9 });   // another form of the same word
      if (c !== x && c !== s) out.push({ toks: [c], w: w * 0.7 });
      if (!alias[x] && !named) for (const f of fuzzy(x, x !== t)) { out.push({ toks: [f], w: w * 0.7 }); more(f, w * 0.65); }
    }
    return out;
  }

  // the query as terms; a term is met by any of its variants, a variant is a list of tokens that all have to match
  function terms(q) {
    const raw = words(norm(q)), out = [];
    for (let i = 0; i < raw.length;) {
      let n = Math.min(3, raw.length - i);
      while (n > 1 && !alias[raw.slice(i, i + n).join(' ')]) n--;
      const t = raw.slice(i, i + n), key = t.join(' ');
      i += n;
      const alts = n === 1 ? variants(key) : [{ toks: t, w: 1 }, ...alias[key].map(x => ({ toks: x, w: 0.9 }))];
      out.push({ alts, stop: n === 1 && stop.has(key) });
    }
    const keep = out.filter(x => !x.stop);
    return keep.length ? keep : out;
  }

  function score(it, T, whole, raw = []) {
    let s = 0, miss = 0, named = false;
    for (let i = 1; i < raw.length; i++) if (` ${it.ntw} `.includes(` ${raw[i - 1]} ${raw[i]} `)) s += 6;   // two words side by side in the name: «раса для»
    for (const term of T) {
      let best = 0, nm = false;
      for (const a of term.alts) {
        let sum = 0, n = false;
        for (const t of a.toks) { const [v, x] = hit(it, t); if (!v) { sum = 0; break; } sum += v; n = n || x; }
        let v = sum / a.toks.length * a.w;
        if (v && T.length === 1 && a.toks.join(' ') === it.ntw) v += 20 * a.w;   // the name itself: "warrior" -> «Воин», not «Прокачка Воина»
        else if (v && T.length === 1 && a.w < 1 && it.ntw.startsWith(a.toks.join(' ') + ' ')) v += 12 * a.w;   // another word for the start of the name, as a query that starts the name: "bis" -> «Gear 13–30» before «Honor gear»
        if (v > best) { best = v; nm = n; }
      }
      if (best) { s += best; named = named || nm; } else miss++;
    }
    if (it.nt === whole) s += 30;
    else if (it.nt.startsWith(whole)) s += 12;
    return [s + (named ? [3, 1, 2, 2][it.k] : 0), miss, named];   // pages go first only when their name matches, not just their text
  }

  function level(lv) {   // the dungeons for a level
    return items.filter(it => {
      const m = it.k === 3 && it.s.match(/ (\d+)(?:–(\d+))? · /);
      return m && +m[1] <= lv && lv <= +(m[2] || m[1]);
    });
  }

  // a known question: its answer, when its phrases cover every word of the query but the stop words and the words that
  // name no class, race or alias ("what class should i play"); a query that names one stays with the ranking
  // ("как прокачать" -> leveling, "как прокачать вара" -> the warrior's leveling guide)
  function asked(q) {
    const raw = words(norm(q)), last = raw[raw.length - 1];
    const forms = t => [t, translit(t)];
    const fits = (t, p) => forms(t).some(x => x.startsWith(p) || (t === last && x.length > 2 && p.startsWith(x)));
    const named = t => [t, translit(t)].some(x => x.length > 1 && (alias[x] || alias[stem(x)] || names.has(stem(x))));
    const out = [];
    for (const [it, phs] of asks) {
      const met = phs.filter(ph => ph.every(p => raw.some(t => fits(t, p))));
      if (met.length && raw.every(t => stop.has(t) || /^\d+$/.test(t) || !named(t) || met.some(ph => ph.some(p => fits(t, p)))))
        out.push([it, Math.max(...met.map(ph => ph.length))]);
    }
    return out.sort((a, b) => b[1] - a[1]).map(r => r[0]).filter((x, i, a) => a.indexOf(x) === i).slice(0, 2);
  }

  function search(q) {
    const whole = norm(q).trim(), raw = words(whole);
    if (!raw.length || !/[\p{L}\p{N}]/u.test(whole)) return [];
    if (/^\d{1,2}$/.test(whole)) return level(+whole);
    const T = terms(q), lv = raw.find(t => /^\d{1,2}$/.test(t)), top = asked(q);
    const rows = items.map(it => [it, ...score(it, T, whole, raw)]);
    let hits = rows.filter(r => r[1] && !r[2]);
    if (hits.length < (T.length > 2 ? 3 : 1) && T.length > 1)   // few or none with every word: add those with all words but one
      hits = hits.concat(rows.filter(r => r[2] === 1 && r[3]).map(r => [r[0], r[1] - 5]));
    hits = hits.sort((a, b) => b[1] - a[1] || a[0].t.length - b[0].t.length).map(r => r[0]);
    if (lv && +lv <= 60) {   // "подземелья 20": the dungeons of the level right after the list itself
      const rest = T.filter(t => !t.alts.some(a => a.toks.includes(lv)));
      const dg = items.find(it => it.k === 0 && it.u.endsWith('guides/dungeons/'));
      if (rest.length && dg && !score(dg, rest, '')[1]) top.push(dg, ...level(+lv));
    }
    return [...new Set([...top, ...hits])].slice(0, 40);
  }

  // the search as the dialog runs it: when nothing matches, the query is retried in the other keyboard layout (vfu -> маг, ьфп -> mag)
  function find(q) {
    let shown = search(q), used = q;
    if (!shown.length && /\p{L}/u.test(q)) {
      const lo = q.toLowerCase();
      used = /[а-яёієїʼ]/.test(lo) ? swap(lo, /[ієї]/.test(lo) ? UK : RU, EN) : ['ru', 'uk'].includes(LANG) ? swap(lo, EN, LANG === 'uk' ? UK : RU) : q;
      if (used !== q) shown = search(used);
    }
    return Object.assign(shown, { used });
  }

  return { items, popular, find, terms, norm };
};
