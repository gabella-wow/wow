"""A catalog of Classic Era items with icons, before the addon dump of 05.11: data/items_catalog.json + assets/gear/catalog-*.webp.
The build does not read it yet (wiring it into build.py and the pages is a separate step).

    python tools/item_catalog.py           # all steps; answers are cached in tools/.gear-api, a second run needs no network
    python tools/item_catalog.py --dry     # counts only, writes nothing

Source: Blizzard Game Data API, namespace static-classic1x-eu (the Classic Era client, the vanilla values Forever starts from,
as in tools/gear_api.py). The item search (data/wow/search/item, orderby=id, windows of 1000 ids: one query returns at most
1000 results) gives id, names, class, subclass, inventory type, quality and levels; data/wow/item/<id> (locale en_US) gives the
stats and the «Use:» text that tells a potion from food (in Era every consumable has subclass 0); data/wow/media/item/<id>
gives the icon file id. Pictures: render.worldofwarcraft.com by file id (tools/talent_icons.picture, cache tools/.talent-icons).
Only ids below 30000: the API's 120000+ and 200000+ items are Season of Discovery / later Era items, not vanilla.
Key file and rules as in tools/talent_icons.py: read-only client_credentials calls, never print the values.
Never Wowhead (wow.zamimg.com) or other sites: their terms forbid it. The API answers 429 when it is asked too fast: the
worker waits and asks again (8 workers, about 40 calls a second, under the 100/s and 36000/h of the key).

Kept: equipment (weapons and armor of a slot below, quality common and up, every level), consumables (potion, elixir, flask,
food, drink, bandage, poison: found by the name and the «Use:» text; scrolls and the rest are left out), reagents (class 5) and
trade goods (class 7). Test and placeholder items (Monster -, Deprecated, [PH], ...) are left out.

Schema (data/items_catalog.json, compact, no spaces):
  {"schema": 1, "date": "YYYY-MM-DD", "source": "Blizzard Game Data API, static-classic1x-eu", "langs": ["en","ru","de","fr","es","pt","it"],
   "cell": 36, "cols": 64,
   "sprites": {"all": {"file": "assets/gear/catalog.webp", "n": <icons>}},  # one sprite while it is under 1.5 MB, else
                                                            # {"equip": {"file": ".../catalog-equip.webp"}, "use": {...}}
   "sprite_of": {<category>: <sprite name>},
   "icons": {"all": [<file id>, ...]},                       # icon i of a sprite: file id icons[sprite][i]
   "items": {"<id>": {"c": <category>, "n": [<name per langs; "" = the same as en>], "q": <quality 0-5>, "il": <item level>,
                      "lvl": <required level, absent if none>, "k": [<item class>, <subclass>],
                      "s": <slot, equipment only>, "st": {<stats as in gear_api>}, "i": <index in the sprite of the category>}}}
  Categories: equip potion elixir flask food drink bandage poison reagent trade (equip -> "equip", the rest -> "use" when split).
  Slots as tools/gear_api.SLOT plus "relic". Cell i of a sprite: x = (i % cols) * cell, y = (i // cols) * cell; 36 px cells
  drawn at 18 px, the same cells as assets/gear/icons.webp (that one is a single row)."""
import argparse, concurrent.futures as cf, datetime, io, json, os, re, sys, threading, time, urllib.error

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import talent_icons as ti  # noqa: E402  token(), get(), the CDN
from gear_api import SLOT, QUAL, STAT, CELL, LOCS, CACHE  # noqa: E402
from gear_import import TIP_STATS  # noqa: E402

NS = 'static-classic1x-eu'
OUT = os.path.join(HERE, 'data', 'items_catalog.json')
SPRITE = 'assets/gear/catalog.webp'
SPLIT = {'equip': 'assets/gear/catalog-equip.webp', 'use': 'assets/gear/catalog-use.webp'}
MAX_SPRITE = 1536 * 1024
COLS = 64
MAX_ID = 30000
WINDOW = 1000
WORKERS = 8
LANGS = list(LOCS)                                            # en ru de fr es pt it
SLOTS = {**SLOT, 'RELIC': 'relic'}
JUNK = re.compile(r"(?i)^(monster -|deprecated|old |tst |zz|npc equip|qa|unused|placeholder|shawn's )|"
                  r"\b(deprecated|unused|nyi|dnd|ph|jefftest)\b|\[(ph|dnd|nyi)\]|(?<!high )\btest(ing)?\b")
_lock = threading.Lock()
_last = [0.0]


def call(path, tok, tries=8):
    """One API answer as JSON (None for 404), with a short gap between calls and a pause on 429 / 5xx."""
    url = f'{ti.API}{path}{"&" if "?" in path else "?"}namespace={NS}'
    for n in range(tries):
        with _lock:                                            # ~40 calls a second over all workers
            wait = _last[0] + 0.025 - time.time()
            if wait > 0:
                time.sleep(wait)
            _last[0] = time.time()
        try:
            b = ti.get(url, tok)
            return json.loads(b) if b else None
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                time.sleep(min(30, 2 ** n))
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(min(30, 2 ** n))
    raise RuntimeError(f'no answer after {tries} tries: {path.split("?")[0]}')


def cached(name, path, tok):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name + '.json')
    if os.path.isfile(p):
        return json.load(open(p, encoding='utf-8'))
    j = call(path, tok)
    tmp = p + '.tmp'
    json.dump(j, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False)
    os.replace(tmp, p)
    return j


def search(tok):
    """Every item of ids 1..MAX_ID: the search data of each (names in all languages, class, levels)."""
    out = []
    for a in range(1, MAX_ID, WINDOW):
        b = min(a + WINDOW - 1, MAX_ID - 1)
        j = cached(f'search-{a}-{b}', f'/data/wow/search/item?orderby=id&_pageSize=1000&_page=1&id=[{a},{b}]', tok)
        res = (j or {}).get('results') or []
        assert len(res) < 1000 or b - a + 1 <= 1000, f'window {a}-{b} is capped'
        out += [r['data'] for r in res]
    return out


def name_en(d):
    return ((d.get('name') or {}).get('en_US') or '').strip()


def first_kind(d):
    """What the search alone says: equip, use (needs the item text), reagent, trade or None."""
    cls = (d.get('item_class') or {}).get('id')
    if not name_en(d) or JUNK.search(name_en(d)) or (d.get('required_level') or 0) > 60:
        return None
    q = QUAL.get((d.get('quality') or {}).get('type'), 0)
    if cls in (2, 4):
        inv = (d.get('inventory_type') or {}).get('type')
        return 'equip' if inv in SLOTS and q >= 1 else None
    if cls == 0:
        return 'use'
    if cls == 5:
        return 'reagent'
    if cls == 7:
        return 'trade'
    return None


def use_text(j):
    out = []
    for sp in ((j or {}).get('preview_item') or {}).get('spells') or []:
        d = sp.get('description') or ''
        out.append(d.get('en_US', '') if isinstance(d, dict) else d)
    return ' '.join(out)


def consumable(name, text):
    """Era has one subclass for every consumable: the kind from the name and the «Use:» text, or None (scrolls, the rest)."""
    if re.search(r'\bFlask\b', name):
        return 'flask'
    if re.search(r'\bElixir\b', name):
        return 'elixir'
    if re.search(r'\bBandage\b', name) and 'Heals' in text:
        return 'bandage'
    if re.search(r'Coats a weapon', text) or (re.search(r'\bPoison\b', name) and 'weapon' in text):
        return 'poison'
    if 'while eating' in text:
        return 'food'
    if 'while drinking' in text:
        return 'drink'
    if re.search(r'\b(Potion|Draught)\b', name):
        return 'potion'
    return None


def stats(j):
    p = (j or {}).get('preview_item') or {}
    st = {}
    for s in p.get('stats') or []:
        k = STAT.get((s.get('type') or {}).get('type'))
        if k and s.get('value'):
            st[k] = st.get(k, 0) + s['value']
    if (p.get('armor') or {}).get('value'):
        st['armor'] = p['armor']['value']
    dps = ((p.get('weapon') or {}).get('dps') or {}).get('value')
    if dps:
        st['dps'] = round(dps, 1)
    text = use_text(j)
    for rx, keys in TIP_STATS:
        x = re.search(rx, text)
        if x:
            for k in keys:
                st[k] = max(st.get(k, 0), int(x.group(1)))
    return st


def icon_of(m):
    return next((a.get('file_data_id') for a in (m or {}).get('assets', []) if a.get('key') == 'icon'), None)


def pmap(fn, xs, label):
    out, t0 = {}, time.time()
    with cf.ThreadPoolExecutor(WORKERS) as ex:
        futs = {ex.submit(fn, x): x for x in xs}
        for n, f in enumerate(cf.as_completed(futs), 1):
            out[futs[f]] = f.result()
            if n % 2000 == 0:
                print(f'  {label}: {n}/{len(xs)} ({time.time() - t0:.0f} s)', flush=True)
    return out


def sprite(files, path):
    """A grid of COLS cells a row, in the order of `files` (each a file id the CDN has); returns the size in bytes."""
    from PIL import Image
    rows = max(1, -(-len(files) // COLS))
    img = Image.new('RGB', (CELL * COLS, CELL * rows), (22, 24, 28))
    for i, f in enumerate(files):
        img.paste(Image.open(ti.picture(str(f))).convert('RGB').resize((CELL, CELL), Image.LANCZOS), ((i % COLS) * CELL, (i // COLS) * CELL))
    buf = io.BytesIO()
    img.save(buf, 'WEBP', quality=80, method=6)
    os.makedirs(os.path.dirname(os.path.join(HERE, path)), exist_ok=True)
    open(os.path.join(HERE, path), 'wb').write(buf.getvalue())
    return len(buf.getvalue())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    tok = ti.token()
    found = search(tok)
    print(f'search: {len(found)} items with ids below {MAX_ID}')
    first = {d['id']: (d, first_kind(d)) for d in found}
    need = [i for i, (d, k) in first.items() if k in ('equip', 'use')]
    full = pmap(lambda i: cached(f'item-en-{i}', f'/data/wow/item/{i}?locale=en_US', tok), need, 'items')
    items = {}
    for i, (d, k) in sorted(first.items()):
        if not k:
            continue
        if k == 'use':
            k = consumable(name_en(d), use_text(full.get(i)))
            if not k:
                continue
        names = [((d.get('name') or {}).get(LOCS[l]) or '').strip() for l in LANGS]
        it = {'c': k, 'n': [names[0]] + ['' if v == names[0] else v for v in names[1:]],
              'q': QUAL.get((d.get('quality') or {}).get('type'), 1), 'il': d.get('level') or 0,
              'k': [(d.get('item_class') or {}).get('id'), (d.get('item_subclass') or {}).get('id')]}
        if d.get('required_level'):
            it['lvl'] = d['required_level']
        if k == 'equip':
            it['s'] = SLOTS[d['inventory_type']['type']]
            st = stats(full.get(i))
            if st:
                it['st'] = st
        items[i] = it
    media = pmap(lambda i: icon_of(cached(f'media-item-{i}', f'/data/wow/media/item/{i}', tok)), list(items), 'media')
    files = sorted({f for f in media.values() if f})
    pics = pmap(lambda f: bool(ti.picture(str(f))), files, 'pictures')
    by_cat = {}
    for k in ('equip', 'potion', 'elixir', 'flask', 'food', 'drink', 'bandage', 'poison', 'reagent', 'trade'):
        n = [i for i, it in items.items() if it['c'] == k]
        by_cat[k] = (len(n), sum(1 for i in n if pics.get(media.get(i))))
    print('items by category (with an icon):', ', '.join(f'{k} {n} ({w})' for k, (n, w) in by_cat.items()))
    print(f'total {len(items)} items, {len(files)} icon files, {sum(1 for v in pics.values() if not v)} not on the CDN')
    if a.dry:
        return
    cats = sorted({it['c'] for it in items.values()})

    def lay(of):
        icons, pos = {}, {}
        for i in sorted(items):
            f, sp = media.get(i), of[items[i]['c']]
            icons.setdefault(sp, []), pos.setdefault(sp, {})
            if f and pics.get(f):
                if f not in pos[sp]:
                    pos[sp][f] = len(icons[sp])
                    icons[sp].append(f)
                items[i]['i'] = pos[sp][f]
            else:
                items[i].pop('i', None)
        return icons
    of, files = {c: 'all' for c in cats}, {'all': SPRITE}
    icons = lay(of)
    sizes = {'all': sprite(icons['all'], SPRITE)}
    if sizes['all'] > MAX_SPRITE:                                  # too big for one: equipment and the rest apart
        os.remove(os.path.join(HERE, SPRITE))
        of, files = {c: 'equip' if c == 'equip' else 'use' for c in cats}, SPLIT
        icons = lay(of)
        sizes = {sp: sprite(icons[sp], SPLIT[sp]) for sp in icons}
    data = {'schema': 1, 'date': datetime.date.today().isoformat(), 'source': f'Blizzard Game Data API, {NS}', 'langs': LANGS,
            'cell': CELL, 'cols': COLS,
            'sprites': {sp: {'file': files[sp], 'n': len(icons[sp])} for sp in icons}, 'sprite_of': of,
            'icons': icons, 'items': {str(i): items[i] for i in sorted(items)}}
    s = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    open(OUT, 'w', encoding='utf-8', newline='\n').write(s + '\n')
    print(f'{OUT}: {len(s.encode()) // 1024} KB; ' + ', '.join(f'{files[sp]} {len(icons[sp])} icons {sizes[sp] // 1024} KB' for sp in icons))


if __name__ == '__main__':
    sys.exit(main())
