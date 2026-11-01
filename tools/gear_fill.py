"""Fill the empty slots of the specs with fewer than 6 slots in data/gear30.json, from the same saved guide pages. No network.

    python tools/gear_fill.py [--cache <folder of tools/gear_api.py answers>] [--dry]

The pages of 7 specs (holy and protection paladin, holy and discipline priest, enhancement shaman, arms and fury warrior)
recommend mostly Forever's own items (ids 200000+) that the API does not know: no slot, level, stats or ru name, so
tools/gear_api.py took them out ("dropped") and these specs kept 3-5 slots. Here a slot the spec has no item for gets the
best 2-3 items for it from the lists of the other 26 pages, picked by the spec's stat priority (gear_import.weights/score,
the same pick as for the addon dump) and the armour and weapon types of the class (gear_import.allowed):
  - only items already in the file (facts from the API, sources from the pages), never a new or made-up item;
  - the item keeps every source the pages give for it; an item without a source is not taken;
  - a quest reward that only one other class's pages list is taken for no one else (class quests: Whirlwind Weapon ...);
  - the entry says where the pick came from: "pick": "stats", "pages": [the specs whose page lists it].
Item class and subclass (armour type, weapon type) come from the cached API answers of tools/gear_api.py (item-<id>.json)
and are kept in the item as "cls"/"sub", so the next run needs no cache. Slots with no fitting item stay empty and are
printed; a spec still under 6 slots stays in "partial".
uk and pl names: the game has no Ukrainian or Polish client, and the site keeps game names (items, quests, bosses) in
English in these two languages (i18n/uk.txt, i18n/pl.json, content/dungeon_pages.py), so names.uk = names.pl = names.en."""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'tools'))
import gear_import as gi  # noqa: E402

OUT = os.path.join(HERE, 'data', 'gear30.json')
CACHE = os.path.join(HERE, 'tools', '.gear-api')
MIN_SLOTS = 6
PER_SLOT = 3


def kinds(data, cache):
    """cls/sub of every item: kept in the file, else from the cached API answer."""
    miss = []
    for k, it in data['items'].items():
        if 'cls' in it and 'sub' in it:
            continue
        p = os.path.join(cache, f'item-{k}.json')
        if not os.path.isfile(p):
            miss.append(k)
            continue
        j = json.load(open(p, encoding='utf-8'))
        it['cls'], it['sub'] = (j.get('item_class') or {}).get('id'), (j.get('item_subclass') or {}).get('id')
    return miss


def fits(it, w, spec):
    """The item is made of the spec's stats: at least one of the leading priority stats (weight 0.5+, stamina and armour
    aside), and no more points of stats outside the priority than inside it (a cloth intellect hood is no enhancement pick,
    an agility cloak no healer's). Shields only for tanks and healers, held-in-off-hand items only for casters and healers."""
    lead = {k for k, v in w.items() if v >= 0.5 and k not in ('sta', 'armor', 'dps')}
    prio = {k for k in w if k not in ('sta', 'armor', 'dps')}
    st = {k: v for k, v in (it.get('stats') or {}).items() if k not in ('sta', 'armor', 'dps')}
    pct = lambda k, v: v * 10 if k in gi.PCT else v  # noqa: E731  1% hit or crit counts as 10 points, as in gear_import.score
    top = sum(pct(k, v) for k, v in st.items() if k in lead)
    inside = sum(pct(k, v) for k, v in st.items() if k in prio)
    outside = sum(pct(k, v) for k, v in st.items() if k not in prio)
    if it['slot'] == 'off' and it.get('cls') == 4:
        caster = 'dps' not in w
        if it.get('sub') == 6 and spec not in gi.TANKS | gi.HEALERS:
            return False
        if it.get('sub') != 6 and not caster:
            return False
    if it['slot'] in ('main', 'two', 'off', 'ranged') and 'dps' in w and (it.get('stats') or {}).get('dps'):
        return outside <= inside                         # a weapon of a melee spec: its damage counts, foreign stats must not lead
    return top > 0 and outside <= inside


def skip_hand(spec, slot, have):
    """Hands that do not fit the spec's weapon set: no one-hand or off hand next to a two-hander of a melee spec
    (arms, enhancement), no two-hander for a tank (one-hand and shield)."""
    if spec in gi.TANKS:
        return slot == 'two'
    melee = spec in ('warrior-arms', 'shaman-enhancement', 'paladin-retribution', 'druid-feral')
    return melee and 'two' in have and slot in ('main', 'off')


def covers(t, s):
    """Source t says all that s says and more (the same quest with its dungeon; the same drop with the boss or the wing)."""
    if t == s or t['kind'] != s['kind']:
        return False
    if s['kind'] == 'quest':
        return all(t.get(k) == v for k, v in s.items() if k != 'dungeon') and (not s.get('dungeon') or s['dungeon'] == t.get('dungeon'))
    if s['kind'] == 'drop':
        sb, tb = (s.get('boss') or {}).get('en'), (t.get('boss') or {}).get('en')
        sd, td = (s.get('dungeon') or {}).get('en') or '', (t.get('dungeon') or {}).get('en') or ''
        return (not sb or sb == tb) and td.startswith(sd) and (bool(tb) > bool(sb) or len(td) > len(sd))
    return False


def merged(srcs):
    return [s for s in srcs if not any(covers(t, s) for t in srcs)]


def fill(data):
    items, specs = data['items'], data['specs']
    for spec in specs:                                             # a new run starts from the pages' own lists
        specs[spec] = [e for e in specs[spec] if not e.get('pick')]
    srcs, pages = {}, {}
    for spec, entries in specs.items():
        for e in entries:
            if e.get('pick'):
                continue                                           # an earlier fill: not a page of the spec
            pages.setdefault(e['id'], []).append(spec)
            for s in e.get('src') or []:
                if s not in srcs.setdefault(e['id'], []):
                    srcs[e['id']].append(s)
    added, short = {}, {}
    for spec in sorted(specs):
        have = {items[str(e['id'])]['slot'] for e in specs[spec]}
        if len(have) >= MIN_SLOTS:
            continue
        cls, w = spec.split('-')[0], gi.weights(spec)
        own = {e['id'] for e in specs[spec]}
        for slot in gi.SLOTS:
            if slot in have or skip_hand(spec, slot, have):
                continue
            cand = []
            for k, it in items.items():
                num = int(k)
                if num in own or it['slot'] != slot or not srcs.get(num) or not gi.allowed(it, cls):
                    continue
                classes = {p.split('-')[0] for p in pages.get(num, [])}
                if all(s['kind'] == 'quest' for s in srcs[num]) and len(classes) == 1 and cls not in classes:
                    continue                                       # a class quest of another class
                if not fits(it, w, spec):
                    continue
                sc = gi.score(it, w)
                if sc > 0:
                    cand.append((sc, it.get('lvl') or 0, num))
            cand.sort(key=lambda x: (-x[0], -x[1], x[2]))
            if not cand:
                short.setdefault(spec, []).append(slot)
                continue
            for sc, _, num in cand[:PER_SLOT]:
                specs[spec].append({'id': num, 'src': merged(srcs[num]), 'pick': 'stats', 'pages': sorted(pages[num])})
                added.setdefault(spec, []).append((slot, num, round(sc, 1)))
    data['partial'] = sorted(k for k, v in specs.items() if 0 < len({items[str(e['id'])]['slot'] for e in v}) < MIN_SLOTS)
    return added, short


def names(data):
    for it in data['items'].values():
        for lang in ('uk', 'pl'):
            it['names'].setdefault(lang, it['names']['en'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cache', default=CACHE)
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    data = json.load(open(a.out, encoding='utf-8'))
    miss = kinds(data, a.cache)
    if miss:
        sys.exit(f'no item class for {len(miss)} items (no cached API answer in {a.cache}): {miss[:10]}')
    added, short = fill(data)
    names(data)
    data.setdefault('provenance', {})['fill'] = ('empty slots of the specs under 6 slots: the best items of the other pages by the '
                                                'spec stat priority (tools/gear_fill.py), entries marked "pick": "stats"')
    for spec in sorted(added):
        print(spec)
        for s, n, sc in added[spec]:
            it = data['items'][str(n)]
            print(f'  {s:8} {n:>6} {it["names"]["en"]} [{sc}] {it.get("stats")} cls {it.get("cls")}/{it.get("sub")} lvl {it.get("lvl")}')
    for spec in sorted(short):
        print(f'{spec}: no fitting item for {", ".join(short[spec])}')
    for spec in sorted(data['specs']):
        n = len({data['items'][str(e['id'])]['slot'] for e in data['specs'][spec]})
        print(f'{spec}: {n} slots')
    print('partial:', data['partial'])
    if not a.dry:
        with open(a.out, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
