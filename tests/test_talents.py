"""Talent trees (talents.py, tools/talent_import.py). Run: python tests/test_talents.py"""
import json, os, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_guides  # noqa: F401  (attaches the tree blocks to the spec pages)
import talents
import talent_import
from content.spec_builds import SPEC_BUILDS

FIX = os.path.join(ROOT, 'tests', 'fixtures', 'talents', 'GabellaTalents.lua')


def fixture():
    db = talent_import.parse_lua(open(FIX, encoding='utf-8').read())['GabellaTalentsDB']
    return talent_import.convert('paladin', db['PALADIN'], fixture=True)


def tree_blocks(cid=None):
    for g in SPEC_BUILDS:
        for s in g['sections']:
            for k, x in s['blocks']:
                if k == 'tree' and (cid is None or x['cls'] == cid):
                    yield s, x


def test_one_tree_per_spec():
    import importlib
    from content import guides
    importlib.reload(guides)                                     # build.py and build_guides both load the guides: no second tree
    for g in SPEC_BUILDS:
        for s in g['sections']:
            assert sum(k == 'tree' for k, _ in s['blocks']) <= 1, (g['slug'], s['id'])


def test_import_fixture():
    d = fixture()
    assert [t['key'] for t in d['trees']] == ['holy', 'protection', 'retribution']
    assert sum(len(t['talents']) for t in d['trees']) == 51
    prot = {t['n']['en']: t for t in d['trees'][1]['talents']}
    assert prot['Redoubt']['n']['ru'] == 'Оплот' and (prot['Redoubt']['r'], prot['Redoubt']['c'], prot['Redoubt']['m']) == (1, 3, 5)
    assert prot['Shield Specialization']['req'] == prot['Redoubt']['id']
    assert prot['Holy Shield']['req'] == prot['Blessing of Sanctuary']['id']


def test_plan_protection():
    d = fixture()
    s, x = next(tree_blocks('paladin'))
    picked, steps, spent, unknown = talents.plan(d, [(r[0], r[1]) for r in x['rows']])
    assert unknown == []
    got = [(t['n']['en'] if t else None, n, a, b) for t, n, a, b in steps]
    assert got == [('Redoubt', 5, 10, 14), ('Precision', 3, 15, 17), ('Improved Seal of Fury', 1, 18, 18), (None, 1, 19, 19),
                   ('Shield Specialization', 3, 20, 22), (None, 8, 23, 30)], got   # row 3 needs 10 points: one point is free


def test_render_fixture():
    d = fixture()
    real = talents.load
    talents.load = lambda cid: d
    try:
        s, x = next(tree_blocks('paladin'))
        html = talents.render('paladin', s['id'], x['rows'], x['titles'], 'ru', '../../')
    finally:
        talents.load = real
    assert html.count('role="group"') == 3 and '<section' not in html          # search.py cuts sections at the first </section>
    assert 'class="tt-tree on" data-t="protection"' in html
    assert html.count('class="tt-t on"') == 4 + 4                                # 4 talents in the tree, 4 in the order by level
    assert '>Защита<span class=on>12</span>' in html and '@@BETA@@' in html
    assert '<span>10–14</span>' in html and '&quot;protection-2&quot;:[5,10,14,&quot;Шанс блока после ударов по вам&quot;]' in html
    assert talents.PAGE[('paladin', 'ru')]['t']['protection-2'][:3] == ['Оплот', 5, 1]
    assert talents.PAGE[('paladin', 'ru')]['u']['lv'] == 'ур. {a}'
    assert 'assets/talents/paladin.webp' in html


def test_no_data_no_tree():
    real = talents.load
    talents.load = lambda cid: None
    try:
        s, x = next(tree_blocks('paladin'))
        assert talents.render('paladin', s['id'], x['rows'], x['titles'], 'ru', '') == ''
    finally:
        talents.load = real


def test_lua_parser():
    db = talent_import.parse_lua('A = {\n ["x"] = { 1, 2, nil, 4, }, -- [1]\n ["s"] = "a\\"b",\n y = true,\n}\n')
    assert db == {'A': {'x': [1, 2, None, 4], 's': 'a"b', 'y': True}}


def test_shipped_data():
    """content/talents: client data only, every row of our tables found, the order ends by level 30, the sprite in place."""
    for f in sorted(os.listdir(talents.DATA)) if os.path.isdir(talents.DATA) else []:
        cid = f[:-5]
        d = talents.load(cid)
        assert not d.get('fixture'), f'{f}: test data must not ship'
        assert [t['key'] for t in d['trees']] == talents.TREES[cid], f
        for s, x in tree_blocks(cid):
            rows = [(r[0], r[1]) for r in x['rows']]
            _, steps, _, unknown = talents.plan(d, rows, talents.FIRST_LEVEL - talents.perk(d, rows))
            assert unknown == [], (cid, s['id'], unknown)
            assert steps[-1][3] <= talents.CAP_LEVEL, (cid, s['id'], steps[-1])
        icons = [t['icon'] for tr in d['trees'] for t in tr['talents'] if t.get('icon') is not None]
        assert all(0 <= i < d['sprite'] for i in icons), f
        if icons:
            assert os.path.isfile(os.path.join(ROOT, 'assets', 'talents', f'{cid}.webp')), cid


def test_wowhead_links():
    """The calculator link of every spec is a legal build: each talent's row is open, its prerequisite is at full rank,
    and every talent of our table keeps its points (the calculator drops what is not legal)."""
    import re
    for f in sorted(os.listdir(talents.DATA)) if os.path.isdir(talents.DATA) else []:
        cid = f[:-5]
        d = talents.load(cid)
        for s, x in tree_blocks(cid):
            url = talents.wowhead(cid, d, [(r[0], r[1]) for r in x['rows']], 'ru')
            pk = talents.perk(d, [(r[0], r[1]) for r in x['rows']])
            assert url.startswith(f'https://www.wowhead.com/forever/ru/talent-calc/{cid}/v2') and url.endswith(f'_t{pk}'), url
            code = re.search(r'/v2(.*)_t\d$', url).group(1).split('-')
            pts = {}
            for tr, c in zip(d['trees'], code + [''] * 3):
                for t, n in zip(sorted(tr['talents'], key=lambda t: (t['r'], t['c'])), c):
                    pts[t['id']] = int(n)
            for tr in d['trees']:
                by = {t['id']: t for t in tr['talents']}
                for t in tr['talents']:
                    n = pts.get(t['id'], 0)
                    if not n:
                        continue
                    below = sum(pts.get(u['id'], 0) for u in tr['talents'] if u['r'] < t['r'])
                    assert below >= talents.ROW_POINTS * (t['r'] - 1), (cid, s['id'], t['n']['en'], below)
                    assert n <= t['m'], (cid, s['id'], t['n']['en'])
                    if t.get('req'):
                        assert pts.get(t['req'], 0) == by[t['req']]['m'], (cid, s['id'], t['n']['en'], 'prerequisite')
            for r in x['rows']:
                _, t = talents.match(d, r[0])
                assert pts.get(t['id'], 0) >= int(r[1]), (cid, s['id'], t['n']['en'])
            assert sum(pts.values()) <= talents.CAP_LEVEL - talents.FIRST_LEVEL + 1 + pk, (cid, s['id'], sum(pts.values()))


def test_leveling_build():
    """Leveling 10-60 (talents.leveling): 51 points, one per level, every step legal in the tree; a spec the source order does not
    fit (warlock: Soul Siphon without its prerequisite; mage: Arcane Focus is not in the tree) gets no tab; classes without data in the switcher show no switcher."""
    ok = []
    for cid, spec in talents.LEVEL_SPEC.items():
        d = talents.load(cid)
        b = talents.leveling(cid, spec, d)
        if b is None:
            assert cid in ('warlock', 'mage'), cid             # known to break (mage: the guide's «Arcane Focus» is not in the Forever tree); a new None must be looked at
            continue
        ok.append(cid)
        assert sum(b['picked'].values()) == 51 == sum(b['spent'].values()), cid
        assert b['steps'][0][2] == 10 and b['steps'][-1][3] == 60, cid
        assert b['main'] == spec or cid == 'warrior', (cid, b['main'])   # the guide's own spec is the main tree (warrior: 31/20)
        assert max(b['spent'], key=b['spent'].get) == b['main']
        url = talents.wowhead_ids(cid, d, b['picks'], 'en', 0)
        import re
        code = re.search(r'/v2(.*)_t0$', url).group(1).split('-')
        pts = {}
        for tr, c in zip(d['trees'], code + [''] * 3):
            for t, n in zip(sorted(tr['talents'], key=lambda t: (t['r'], t['c'])), c):
                pts[t['id']] = int(n)
        assert {k: v for k, v in pts.items() if v} == {k: v for k, v in b['picked'].items() if v}, cid          # the link carries exactly the order's points
    assert len(ok) == 7, ok               # 9 classes minus warlock and mage
    assert talents.leveling('druid', 'balance', talents.load('druid')) is None        # only the leveling spec of the class
    for s, x in tree_blocks('warlock'):
        assert 'tt-bs' not in talents.render('warlock', s['id'], x['rows'], x['titles'], 'en', '')


def test_switcher_render():
    for lang in ('ru', 'en', 'de'):
        s, x = next((s, x) for s, x in tree_blocks('druid') if s['id'] == 'feral')
        html = talents.render('druid', 'feral', x['rows'], x['titles'], lang, '../../')
        assert html.count('role="tab" class="tt-b"') == 2 and 'id="feral-leveling"' in html and 'id="feral-general"' in html
        assert html.count('<div class="tt-ow"') == 2 and html.count('data-b="leveling" hidden>') == 1 and '<section' not in html
        assert 'data-s="feral-' in html and '#talents' in html
        s2, x2 = next((s, x) for s, x in tree_blocks('druid') if s['id'] == 'balance')
        assert 'tt-bs' not in talents.render('druid', 'balance', x2['rows'], x2['titles'], lang, '')   # no data: no tab at all
    assert all(talents.UI['b_' + b][l] for b in ('leveling', 'dungeons', 'raid', 'pvp') for l in talents.UI['hint'])


def test_engine_extra_builds():
    """Dungeons / raid / pvp appear when a provider returns data and stay out otherwise (empty tabs are never shown)."""
    s, x = next((s, x) for s, x in tree_blocks('druid') if s['id'] == 'feral')
    d = talents.load('druid')
    base = talents.leveling('druid', 'feral', d)
    talents.PROVIDERS['raid'] = lambda cid, spec, data: dict(base)
    talents.PROVIDERS['pvp'] = lambda cid, spec, data: None
    try:
        html = talents.render('druid', 'feral', x['rows'], x['titles'], 'en', '../../')
    finally:
        del talents.PROVIDERS['raid'], talents.PROVIDERS['pvp']
    assert html.count('role="tab" class="tt-b"') == 3 and 'id="feral-raid"' in html and 'feral-pvp' not in html


def test_editor_render():
    """The editor: its bar in every tree block (hidden until the script runs), the start build (data-w) in the calculator's format
    and the rules it checks come from the data file (#ttData q/o/cap), every UI line in all 9 languages."""
    import re
    for cid in talents.TREES:
        d = talents.load(cid)
        if not d:
            continue
        for s, x in tree_blocks(cid):
            html = talents.render(cid, s['id'], x['rows'], x['titles'], 'pl', '../../')
            assert html.count('<template class="tt-edt"><div class="tt-ed">') == 1 and f'data-sp="{s["id"]}"' in html, (cid, s['id'])
            assert html.count('class="tt-ow" data-b="general"') == 1, (cid, s['id'])
            code = re.search(r'data-w="([0-9-]*)"', html).group(1)
            assert code == re.search(r'/v2([0-9-]*)_t\d', talents.wowhead(cid, d, [(r[0], r[1]) for r in x['rows']], 'pl')).group(1)
            assert html.count('data-s="') == html.count('class="tt-ar'), (cid, 'every line knows its ends')
        pg = talents.PAGE[(cid, 'pl')]
        assert pg['cap'] == 51 and pg['rp'] == talents.ROW_POINTS
        assert [len(o) for o in pg['o']] == [len(tr['talents']) for tr in d['trees']]
        assert all(pg['t'][q] for q in pg['q'].values())
    for k in ('ed', 'ed_x', 'cnt', 'add', 'del', 'reset', 'share', 'copied', 'nocopy', 'eh', 'rank', 'e_cap', 'e_row', 'e_req', 'e_keep'):
        assert all(talents.UI[k].get(l) for l in talents.UI['hint']), k
    assert all(k in talents.PAGE[('mage', 'pl')]['u'] for k in ('ed', 'ed_x', 'cnt', 'rank', 'e_cap', 'e_row', 'e_req', 'e_keep', 'copied'))


def test_calc_render():
    """The calculator page talents/<class>/: the same tree and editor, open from the start (bar in the page, no template, no build
    of ours drawn), one «start from our build» link per spec in the editor's own code, every new UI line in all 9 languages."""
    import re
    for cid in talents.TREES:
        d = talents.load(cid)
        if not d:
            continue
        blocks = list(tree_blocks(cid))
        specs = [(s['id'], x['rows']) for s, x in blocks]
        html = talents.render_calc(cid, specs, blocks[0][1]['titles'], 'de', '../../')
        assert 'tt-edt' not in html and 'data-calc="1"' in html and 'class="tt calc ed"' in html, cid
        assert html.count('role="group"') == 3 and 'class="tt-t on"' not in html and '<section' not in html, cid
        assert 'class="tt-eb" hidden' in html and 'class="tt-ec"' in html and 'tt-ow' not in html, cid
        assert re.search(r'class="tt-cn">Punkte: 0 von 51<', html), cid
        codes = re.findall(r'<a href="#([0-9-]+)" data-t="([a-z-]+)">', html)
        assert [t for _, t in codes] == [s for s, _ in specs], (cid, codes)
        for (code, spec), (_, rows) in zip(codes, specs):
            assert code == talents.build_code(d, talents.table_picks(d, [(r[0], r[1]) for r in rows])), (cid, spec)
        assert 'href="../../guides/builds-' + cid + '/"' in html
        g = talents.render(cid, specs[0][0], specs[0][1], blocks[0][1]['titles'], 'de', '../../')
        assert f'href="../../talents/{cid}/#' in g and 'class="tt-cl"' in g, cid   # the guide links its build to the calculator
    assert talents.page('<html><head><style></style></head><body><div class="tt calc ed" id="calc" data-c="mage" data-l="de"></div></body>').count('id="ttData"') == 1
    for k in ('calc', 'ours', 'gd'):
        assert all(talents.UI[k].get(l) for l in talents.UI['hint']), k


def test_reimport_keeps_other_languages():
    """A re-import of one language (ruRU) keeps the other languages' names and tooltips from the previous file."""
    db = talent_import.parse_lua(open(FIX, encoding='utf-8').read())['GabellaTalentsDB']['PALADIN']
    full = talent_import.convert('paladin', db, fixture=True)
    ru_only = {'ruRU': db['ruRU']}
    again = talent_import.convert('paladin', ru_only, full, True)
    assert again['trees'] == full['trees']
    fresh = talent_import.convert('paladin', ru_only, fixture=True)
    assert all('en' not in t['n'] for tr in fresh['trees'] for t in tr['talents'])


if __name__ == '__main__':
    n = 0
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
            n += 1
    print(f'talents: {n} tests OK')
