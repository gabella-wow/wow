"""SavedVariables of the GabellaTalents addon (tools/talent_dump) -> content/talents/<class>.json for talents.py.

    python tools/talent_import.py "<WoW>/_forever_/WTF/Account/<account>/SavedVariables/GabellaTalents.lua" [--out DIR] [--fixture]

Rows, columns, arrows, ranks and the icon file id come from the client (the addon API); the names and tooltip lines from every
client language that was dumped (languages missing from a re-import keep their previous text). Icon names and the sprite are added later by tools/talent_icons.py and survive a re-import.
tid: the game's own id of a talent, the dump's talentID (in Forever the C_Traits node id); the in-game addon finds the talent by it.
--fixture marks test data (tests/fixtures/talents): tests refuse such a file in content/talents."""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from talents import TREES  # noqa: E402

LOCALES = {'ruRU': 'ru', 'enUS': 'en', 'enGB': 'en', 'deDE': 'de', 'esES': 'es', 'esMX': 'es', 'frFR': 'fr', 'itIT': 'it', 'ptBR': 'pt'}


def parse_lua(src):
    """The subset of Lua that SavedVariables use: tables, ["key"] = / [1] = / list items, strings, numbers, booleans, nil, -- comments."""
    src = re.sub(r'--[^\n]*', '', src)
    pos = 0

    def ws():
        nonlocal pos
        while pos < len(src) and src[pos] in ' \t\r\n':
            pos += 1

    def value():
        nonlocal pos
        ws()
        ch = src[pos]
        if ch == '{':
            pos += 1
            out, arr = {}, []
            while True:
                ws()
                if src[pos] == '}':
                    pos += 1
                    break
                if src[pos] == '[':
                    pos += 1
                    k = value()
                    ws()
                    assert src[pos] == ']', src[pos - 20:pos + 20]
                    pos += 1
                    ws()
                    assert src[pos] == '='
                    pos += 1
                    out[k] = value()
                else:
                    m = re.match(r'([A-Za-z_]\w*)\s*=(?!=)', src[pos:])
                    if m:
                        pos += m.end()
                        out[m.group(1)] = value()
                    else:
                        arr.append(value())
                ws()
                if src[pos] in ',;':
                    pos += 1
            if arr:
                for i, v in enumerate(arr, 1):
                    out.setdefault(i, v)
            if out and all(isinstance(k, int) for k in out):
                return [out.get(i) for i in range(1, max(out) + 1)]
            return out
        if ch == '"':
            pos += 1
            buf = []
            while src[pos] != '"':
                if src[pos] == '\\':
                    pos += 1
                    buf.append({'n': '\n', 't': '\t'}.get(src[pos], src[pos]))
                else:
                    buf.append(src[pos])
                pos += 1
            pos += 1
            return ''.join(buf)
        m = re.match(r'-?\d+(\.\d+)?', src[pos:])
        if m:
            pos += m.end()
            return float(m.group(0)) if m.group(1) else int(m.group(0))
        for word, v in (('true', True), ('false', False), ('nil', None)):
            if src.startswith(word, pos):
                pos += len(word)
                return v
        raise ValueError(f'lua at {pos}: {src[pos:pos + 40]!r}')

    out = {}
    while True:
        ws()
        if pos >= len(src):
            return out
        m = re.match(r'([A-Za-z_]\w*)\s*=', src[pos:])
        assert m, src[pos:pos + 40]
        pos += m.end()
        out[m.group(1)] = value()


def _fix(v, med):
    """The Forever client keeps a few node positions with an extra zero (10x the real one)."""
    return v / 10 if med > 0 and v > 3 * med else v


def _axis(values):
    """One axis of a trait tree -> (first line, step); nodes may sit a few units off their line."""
    med = sorted(values)[len(values) // 2]
    vs = sorted(_fix(v, med) for v in values)
    gaps = [b - a for a, b in zip(vs, vs[1:]) if b - a > 0]
    if not gaps:
        return vs[0], 1, med
    big = max(gaps)
    step = min(g for g in gaps if g > 0.3 * big)
    return vs[0], step, med


def _line(v, first, step, med):
    return int((_fix(v, med) - first) / step + 0.5)


def from_traits(d, old_keys=None):
    """A Forever dump (api = traits: node positions and edges) -> the classic shape (row, col from 1, req as [row, col]),
    talents in row-major order."""
    out = dict(d, trees=[], grid=True)
    for tree in d['trees']:
        ts = list(tree['talents'].values()) if isinstance(tree['talents'], dict) else list(tree['talents'])
        mx = sorted(t['posX'] for t in ts)[len(ts) // 2]
        my = sorted(t['posY'] for t in ts)[len(ts) // 2]
        # a node with an extra zero in its position (10x) is not in the game's window: checked in the client 06.11
        # (hunter: a second Lightning Reflexes, a Serpent Sting node that no tree shows)
        ts = [t for t in ts if _fix(t['posX'], mx) == t['posX'] and _fix(t['posY'], my) == t['posY']]
        x0, dx, xl = _axis([t['posX'] for t in ts])
        y0, dy, yl = _axis([t['posY'] for t in ts])
        pos = {}
        for t in ts:
            t = dict(t, col=_line(t['posX'], x0, dx, xl) + 1, row=_line(t['posY'], y0, dy, yl) + 1,
                     tip=[l for l in (t.get('tip') or []) if l not in ('SpellID', 'IconID')])  # labels another addon adds
            pos[t['talentID']] = t
        for t in list(pos.values()):
            edges = t.get('edges') or []
            for target in (edges.values() if isinstance(edges, dict) else edges):
                if target in pos:
                    pos[target]['req'] = [t['row'], t['col']]
        out['trees'].append({'info': tree.get('info'), 'talents': sorted(pos.values(), key=lambda t: (t['row'], t['col']))})
    return out


def convert(cid, by_locale, old=None, fixture=False):
    """One class: the dumps of each client language -> our JSON (old: the previous file, its icons are kept)."""
    keys = TREES[cid]
    by_locale = {loc: (from_traits(d) if d.get('api') == 'traits' and not d.get('grid') else d) for loc, d in by_locale.items()}
    by_pos = {(tr['key'], t['r'], t['c']): t['id'] for tr in (old or {}).get('trees', []) for t in tr['talents']}
    base = by_locale.get('enUS') or next(iter(by_locale.values()))
    prev = {t['id']: t for tr in (old or {}).get('trees', []) for t in tr['talents']}
    icons = {i: (t.get('icon'), t.get('iname')) for i, t in prev.items()}
    trees = []
    for ti, tree in enumerate(base['trees']):
        key = keys[ti]
        talents = []
        ids = {}       # traits dumps: the same talent (its spell, else its place) keeps its id, icon and old texts
        if base.get('api') == 'traits':
            olds = next((tr['talents'] for tr in (old or {}).get('trees', []) if tr['key'] == key), [])
            by_spell = {s: o['id'] for o in olds for s in o.get('spells') or []}
            spells_of = {o['id']: set(o.get('spells') or []) for o in olds}
            free = 1 + max([int(o['id'].rsplit('-', 1)[1]) for o in olds] or [0])
            later = []
            for t in tree['talents']:                   # first by spell
                rc = (int(t['row']), int(t['col']))
                tid = by_spell.get(t.get('spellId'))
                if tid and tid not in ids.values():
                    ids[rc] = tid
                else:
                    later.append((rc, t))
            for rc, t in later:                         # then by place, when the old talent there had no other spell
                tid = by_pos.get((key, *rc))
                if not tid or tid in ids.values() or (spells_of.get(tid) and t.get('spellId') not in spells_of[tid]):
                    tid, free = f'{key}-{free}', free + 1   # a new talent: a new number
                ids[rc] = tid
        for i, t in enumerate(tree['talents'], 1):
            tid = ids.get((int(t['row']), int(t['col'])), f'{key}-{i}')
            x = {'id': tid, 'n': {}, 'r': int(t['row']), 'c': int(t['col']), 'm': int(t['maxRank']),
                 'spells': [t['spellId']] if t.get('spellId') else [], 'file': t.get('icon'), 'tip': {}}
            if t.get('talentID'):   # the game's own id of the talent (Forever: the C_Traits node id): the in-game addon finds it by it
                x['tid'] = int(t['talentID'])
            for loc, d in by_locale.items():
                lang = LOCALES.get(loc)
                tt = d['trees'][ti]['talents'][i - 1]
                if lang:
                    x['n'][lang] = tt['name']
                    x['tip'][lang] = tt.get('tip') or []
            for lang, nm in prev.get(tid, {}).get('n', {}).items():   # a language not dumped this time keeps its old text
                if lang not in x['n']:
                    x['n'][lang] = nm
                    x['tip'][lang] = prev[tid].get('tip', {}).get(lang) or []
            if t.get('req'):
                pr, pc = t['req']
                j = next(j for j, s in enumerate(tree['talents'], 1) if int(s['row']) == pr and int(s['col']) == pc)
                x['req'] = ids.get((int(pr), int(pc)), f'{key}-{j}')
            icon, iname = icons.get(tid, (None, None))
            if icon is not None:
                x['icon'], x['iname'] = icon, iname
            talents.append(x)
        trees.append({'key': key, 'talents': talents})
    out = {'class': cid, 'client': base.get('build'), 'source': 'GabellaTalents addon (client addon API)',
           'trees': trees, 'sprite': (old or {}).get('sprite', 0)}
    if fixture:
        out['fixture'] = True
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('saved')
    ap.add_argument('--out', default=os.path.join(HERE, 'content', 'talents'))
    ap.add_argument('--fixture', action='store_true')
    a = ap.parse_args()
    db = parse_lua(open(a.saved, encoding='utf-8').read())['GabellaTalentsDB']
    os.makedirs(a.out, exist_ok=True)
    for cls, by_locale in db.items():
        cid = cls.lower()
        p = os.path.join(a.out, f'{cid}.json')
        old = json.load(open(p, encoding='utf-8')) if os.path.isfile(p) else None
        data = convert(cid, by_locale, old, a.fixture)
        json.dump(data, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
        n = sum(len(t['talents']) for t in data['trees'])
        print(f'{cid}: {n} talents, languages {sorted(LOCALES[l] for l in by_locale if l in LOCALES)} -> {p}')


if __name__ == '__main__':
    main()
