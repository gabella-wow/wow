"""Юнит-тесты сборки гайдов. Запуск: python tests/test_guides.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import build_guides as bg
from content import guides as cg

T = {'ru': 'Привет', 'en': 'Hello', 'uk': 'Привіт'}

def test_hubs_complete_and_pathed():
    assert [h['path'] for h in cg.HUBS] == ['classes/', 'races/']
    for h in cg.HUBS:
        assert bg.check_langs(h) == [], bg.check_langs(h)[:5]

def test_ref_js_translated():
    js_en = bg.ref_js(bg.home_src(), 'en')
    assert 'function renderClassRef' in js_en and 'function renderRaceRef' in js_en
    assert 'Прокачка' not in js_en and '@@RACE_SLUG@@' not in js_en
    assert 'const $' not in js_en and 'function esc' not in js_en   # the guide template defines them

def test_news_block_newest_first():
    html = bg.render_block('news', None, 'en', '')
    assert html.count('class="nitem"') == len(cg.NEWS) > 0
    dates = [n['date'] for n in cg.NEWS]
    first = '.'.join(reversed(max(dates).split('-')))
    assert html.index(first) < html.index('.'.join(reversed(min(dates).split('-'))))

def test_L():
    assert bg.L(T, 'uk') == 'Привіт'
    assert bg.L('Blackrock Depths', 'ru') == 'Blackrock Depths'

def test_text_escapes():
    html = bg.render_block('text', [{'ru': 'a < b', 'en': 'a < b', 'uk': 'a < b'}], 'ru', '')
    assert '<p>a &lt; b</p>' in html

def test_steps_numbered():
    html = bg.render_block('steps', [{'t': T, 'd': T}, {'t': T, 'd': T}], 'en', '')
    assert 'steps-c' in html and '<span class="n">1</span>' in html and '<span class="n">2</span>' in html and 'Hello' in html
    assert '01' not in html   # plain figures, not the 01-06 landing cards

def test_table_has_labels_for_mobile():
    html = bg.render_block('table', {'head': [T, 'Lvl'], 'rows': [['Deadmines', '15–22']]}, 'en', '')
    assert 'data-l="Hello"' in html and 'data-l="Lvl"' in html and '<table' in html

def test_faq_details_with_id():
    html = bg.render_block('faq', [{'id': 'release', 'q': T, 'a': [T]}], 'ru', '')
    assert '<details' in html and 'id="release"' in html and 'Привет' in html

def test_tip_uses_fire_and_word():
    html = bg.render_block('tip', T, 'ru', '')
    assert 'tipbox' in html and '#i-fire' in html and 'Совет' in html
    assert 'Tip' in bg.render_block('tip', T, 'en', '')

def test_tabs():
    html = bg.render_block('tabs', [{'id': 'alliance', 't': T, 'blocks': [('text', [T])]},
                                    {'id': 'horde', 't': T, 'blocks': [('text', [T])]}], 'ru', '')
    assert 'role="tablist"' in html and 'data-tab="horde"' in html and html.count('role="tabpanel"') == 2

def test_tiles_link_and_art():
    html = bg.render_block('tiles', [{'t': T, 'd': T, 'href': 'guides/faq/', 'art': 'mage'}], 'uk', '../')
    assert 'href="../guides/faq/"' in html and '@@ROOT@@assets/art/mage-600.webp' in html and 'Привіт' in html

def test_raw_by_lang():
    assert bg.render_block('raw', T, 'en', '') == 'Hello'
    assert bg.render_block('raw', '<div id="x"></div>', 'uk', '') == '<div id="x"></div>'

def test_unknown_block_fails():
    try:
        bg.render_block('nope', [], 'ru', '')
    except ValueError:
        return
    raise AssertionError('unknown block must raise ValueError')

def test_check_langs_finds_gap():
    bad = {'title': {'ru': 'x', 'en': '', 'uk': 'y'}, 'blocks': [('text', [{'ru': 'a', 'en': 'b'}])]}
    gaps = bg.check_langs(bad)
    assert any('title' in g for g in gaps) and len(gaps) == 2

def test_content_complete():
    assert bg.check_langs(cg.HUB) == []
    for g in cg.GUIDES:
        assert bg.check_langs(g) == [], (g['slug'], bg.check_langs(g)[:5])
    for n in cg.NEWS:
        assert bg.check_langs(n) == []

def test_ids_unique():
    taken = {'top', 'more', 'sources', 'all', 'topbar', 'moreDlg', 'moreClose'}   # ids of the template itself
    for g in cg.GUIDES:
        ids = bg.page_ids(g)
        assert len(ids) == len(set(ids)), (g['slug'], sorted(i for i in ids if ids.count(i) > 1))
        assert not taken & set(ids), (g['slug'], taken & set(ids))

def test_profs_table():
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.src.html'), encoding='utf-8').read()
    rows = bg.profs_table(src)
    assert len(rows) == 12, len(rows)
    assert [bg.L(c, 'ru') for c in rows[0]] == ['Алхимия', 'Mana Well', 'как Благословение мудрости'], rows[0]
    assert bg.L(rows[0][2], 'en') == 'like Blessing of Wisdom'
    html = bg.render_block('profs', None, 'uk', '')
    assert 'Mana Well' in html and 'Алхімія' in html and 'data-l=' in html

def test_sources_translated():
    for g in cg.GUIDES:
        assert g['sources'], g['slug']
        for n, u in g['sources']:
            assert u.startswith('https://'), u
            assert g.get('only') or bg.L(n, 'en').isascii(), (g['slug'], n)

def test_play_route_from_leveling():
    route, tip = bg.leveling_parts()
    assert set(route) == {'alliance', 'horde'}
    for f, rows in route.items():
        assert rows[0][0] == 1 and rows[-1][1] == 60, (f, rows[0][:2], rows[-1][:2])
        for (lo, hi, _), (lo2, _h, _d) in zip(rows, rows[1:]):
            assert lo < hi and lo2 <= hi, (f, lo, hi, lo2)   # no gap in levels between brackets
    assert bg.check_langs(tip) == []

def test_play_data_per_language():
    import json, re
    src = bg.home_src()
    for lang in ('ru', 'en', 'uk'):
        js = bg.play_data(src, lang)
        assert js.startswith('const DUNGEONS = [')
        p = json.loads(js[js.index('const P = ') + 10:].rstrip().rstrip(';'))
        assert p['racef']['human'] == 'alliance' and p['racef']['orc'] == 'horde', p['racef']
        assert len(p['cn']) == 9 and len(p['rn']) == 10 and all(p['tx'].values())
        assert [m[0] for m in p['miles']] == sorted(m[0] for m in p['miles'])
        if lang == 'en':
            text = json.dumps([p['route'], p['miles'], p['tx'], p['cn'], p['rn']], ensure_ascii=False)
            assert not re.search('[А-Яа-яЁё]', text), re.findall('[А-Яа-яЁё]+', text)[:5]

def test_play_page_built():
    for d in ('', 'en/', 'uk/'):
        html = open(os.path.join(bg.HERE, d + 'play', 'index.html'), encoding='utf-8').read()
        assert 'id="radioDock"' in html and 'const P = ' in html and '<body class="compact">' in html
        assert 'class="stband ghero"' not in html and 'wakeLock' not in html and 'wakeBtn' not in html
        assert 'assets/radio/radio.js' in html

def test_next_block():
    nb = bg.build.next_block
    assert nb(None, 'en', '../') == '' and nb([], 'ru', '') == ''   # no field, no block
    items = [('guides/builds/', T), ('guides/leveling/', T), ('guides/dungeons/', T), ('guides/faq/', T)]
    html = nb(items, 'en', '../')
    assert html.count('<a href="../guides/') == 3 and 'faq' not in html   # three links at most
    assert '>Next step<' in html and '<span>Hello</span>' in html
    assert '>Nächster Schritt<' in nb(items[:1], 'de', '')
    for d in ('', 'en/', 'de/'):   # the placeholder never reaches a page
        for p in ('guides/leveling/', 'classes/mage/', 'races/orc/'):
            assert '@@NEXT@@' not in open(os.path.join(bg.HERE, d + p, 'index.html'), encoding='utf-8').read()

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')


def gear_problems(data, min_slots, strict=True):
    """The rules of data/gear30.json: names, slot, level up to 30, a provenance, sources of a known kind, no item twice in a spec.
    strict=False for data not yet accepted (hidden in the build): an en name is enough, slot may be unknown, no slot minimum.
    The slot minimum is waived on purpose for the specs listed in "partial" (31.10: shown with the mark «incomplete»);
    a listed spec that has reached the minimum is an error too, so the mark never stays on a full list."""
    from content import spec_cheats as sc
    bad = []
    for k, it in data.get('items', {}).items():
        if not it.get('names', {}).get('en') or (strict and not it['names'].get('ru')):
            bad.append(f'{k}: en and ru names')
        if it.get('slot') not in sc.GSLOTS and (strict or it.get('slot') is not None):
            bad.append(f'{k}: slot {it.get("slot")}')
        if it.get('lvl') is not None and not 1 <= it['lvl'] <= 30:
            bad.append(f'{k}: level {it["lvl"]}')
        if it.get('provenance') not in ('wowhead-forever-guide', 'client-dump'):
            bad.append(f'{k}: provenance {it.get("provenance")}')
    bad += [f'{spec}: partial, no items' for spec in data.get('partial', []) if not data.get('specs', {}).get(spec)]
    for spec, entries in data.get('specs', {}).items():
        if spec not in sc.HAS_CHEAT:
            bad.append(f'{spec}: no such spec')
        ids = [e['id'] for e in entries]
        if len(ids) != len(set(ids)):
            bad.append(f'{spec}: an item twice')
        n = len({data['items'][str(i)]['slot'] for i in ids if str(i) in data['items']})
        partial = spec in data.get('partial', [])
        if strict and entries and n < min_slots and not partial:
            bad.append(f'{spec}: fewer than {min_slots} slots')
        if partial and n >= min_slots:
            bad.append(f'{spec}: listed as partial with {n} slots')
        bad += [f'{spec} {e["id"]}: source {s.get("kind")}' for e in entries for s in e.get('src', []) if s.get('kind') not in ('drop', 'quest', 'craft')]
        bad += [f'{spec} {e["id"]}: not in items' for e in entries if str(e['id']) not in data['items']]
    return bad


def test_gear30_data():
    """The real file: never test data; accepted data: every spec on 6+ slots, en and ru names; not accepted: the loose rules,
    and the build does not use it. No file or an empty one: fine (the section stays hidden)."""
    from content import spec_cheats as sc
    p = os.path.join(bg.HERE, 'data', 'gear30.json')
    if os.path.isfile(p):
        data = sc.load_gear30(p)
        assert not data.get('fixture'), 'test data in data/gear30.json'
        strict = bool(data.get('approved'))
        assert gear_problems(data, sc.GEAR_MIN_SLOTS, strict) == [], gear_problems(data, sc.GEAR_MIN_SLOTS, strict)[:10]
        if strict and os.path.abspath(sc.GEAR30_PATH) == os.path.abspath(p):
            gear_marks(sc, data)
        if not strict:
            assert sc.GEAR30 == {'items': {}, 'specs': {}} or os.path.abspath(sc.GEAR30_PATH) != os.path.abspath(p)
            prov = data.get('provenance') or {}
            if data.get('specs') and any(it.get('provenance') == 'wowhead-forever-guide' for it in data['items'].values()):
                assert prov.get('saved') and prov.get('temporary') and set(prov.get('files', {})) == set(data['specs'])
    fx = sc.load_gear30(os.path.join(FIX, 'gear30.json'))
    assert fx['fixture'] and gear_problems(fx, 5) == [], gear_problems(fx, 5)


def test_gear30_strict():
    """The accepted file, with no waiver: each of the 27 specs has 6+ slots, at most 3 items per slot among the picks of
    tools/gear_fill.py, a source on every item of a pick, names in uk and pl, and the «incomplete» list empty."""
    from content import spec_cheats as sc
    p = os.path.join(bg.HERE, 'data', 'gear30.json')
    data = sc.load_gear30(p)
    if not data.get('approved'):
        return
    assert data.get('partial') == [], data.get('partial')
    assert set(data['specs']) == set(sc.HAS_CHEAT), set(sc.HAS_CHEAT) ^ set(data['specs'])
    items = data['items']
    for spec, entries in data['specs'].items():
        slots = {items[str(e['id'])]['slot'] for e in entries}
        assert len(slots) >= sc.GEAR_MIN_SLOTS, (spec, sorted(slots))
        picks = [e for e in entries if e.get('pick')]
        assert all(e['pick'] == 'stats' for e in picks), spec
        assert not [e['id'] for e in entries if 'pages' in e and not e.get('pick')], spec   # provenance comes with the pick mark
        for slot in {items[str(e['id'])]['slot'] for e in picks}:
            n = sum(1 for e in picks if items[str(e['id'])]['slot'] == slot)
            assert n <= 3, (spec, slot, n)
        own = {items[str(e['id'])]['slot'] for e in entries if not e.get('pick')}
        for e in picks:
            assert e.get('src') and e.get('pages') and spec not in e['pages'], (spec, e['id'])
            fn = {'alliance': 'A', 'horde': 'H'}
            for lang in ('ru', 'en'):   # every source of a pick names something on the page: no «—», no bare «Quest:»
                got = [sc._src_html(s, lang, lambda a, b: a, fn) for s in e['src']]
                assert all(g and not g.endswith(': ') for g in got) and len(set(got)) == len(got), (spec, e['id'], got)
            assert items[str(e['id'])]['slot'] not in own, (spec, e['id'])   # a pick fills an empty slot only
    for k, it in items.items():
        assert it['names'].get('uk') and it['names'].get('pl'), k


def gear_marks(sc, data):
    """Accepted data in the build: every spec with items shows the section with the beta mark in 9 languages (while the items come
    from the Wowhead import); the «incomplete» mark exactly on the specs listed in "partial"; the built pages carry the same."""
    from html import escape
    tr = lambda s, l: s   # noqa: E731
    fn = {'alliance': 'A', 'horde': 'H'}
    beta = any(it.get('provenance') == 'wowhead-forever-guide' for it in data['items'].values())
    for key in data['specs']:
        part = key in data.get('partial', [])
        for lang in sc.LANGS9:
            html = sc.gear_html(key, lang, tr, fn)
            temp, inc = sc.G_TEMP[lang].split(':')[0], sc.G_PART[lang].split(':')[0]
            assert 'class="gnote"' in html and (f'<b>{temp}:</b>' in html) == beta, (key, lang)
            assert (f'<b>{inc}:</b>' in html) == part, (key, lang)
            assert (sc.G_PART_S[lang] in sc.gear_answer(key, lang)) == part, (key, lang)
            # a pick by stats (tools/gear_fill.py) is marked on its row, on top of the section and next to the source
            picks = sum(1 for e in data['specs'][key] if e.get('pick'))
            pick = escape(sc.G_PICK_NOTE[lang].split(':')[0])
            assert html.count('class="gpick"') == picks and (f'<b>{pick}:</b>' in html) == bool(picks), (key, lang)
            assert (escape(sc.G_SRC_PICK[lang]) in html) == bool(picks), (key, lang)
        for d in ('', 'en/', 'uk/', 'pl/'):
            page = os.path.join(bg.HERE, d + 'guides', f'spec-{key}', 'index.html')
            html = open(page, encoding='utf-8').read()
            lang = d.strip('/') or 'ru'
            assert 'id="gearBox"' in html and 'class="gnote"' in html, page
            assert (escape(sc.G_PART[lang].split(':')[0]) + ':</b>' in html) == part, page
            assert html.count('class="gpick"') == sum(1 for e in data['specs'][key] if e.get('pick')), page


def test_gear_import_pages():
    """Saved guide pages -> items with names of both languages, required level up to 30, the three kinds of source."""
    sys.path.insert(0, os.path.join(bg.HERE, 'tools'))
    import gear_import as gi
    specs, items = gi.from_pages(os.path.join(FIX, 'gear_pages'))
    ids = [e['id'] for e in specs['mage-frost']]
    assert len(ids) == 11 and 900022 not in ids and 900012 not in ids   # over level 30; a table after the three parts
    assert items[900001]['names'] == {'en': 'Test Sorcerer Collar', 'ru': 'Тестовый воротник чародея'}
    assert items[900001]['slot'] == 'neck' and items[900001]['lvl'] == 17 and items[900001]['stats'] == {'int': 2, 'spi': 2}
    assert items[900004]['slot'] == 'two' and items[900004]['stats']['dps'] == 18.5 and items[900002]['stats']['sp'] == 6
    src = {e['id']: e['src'][0] for e in specs['mage-frost']}
    assert src[900002] == {'kind': 'drop', 'boss': {'en': 'Test Boss Glacius', 'ru': 'Тестовый босс Гласиус'}, 'dungeon': {'en': 'Test Hollow', 'ru': 'Тестовая пещера'}}
    assert src[900001]['faction'] == 'alliance' and src[900007]['faction'] == 'horde'
    assert src[900010] == {'kind': 'craft', 'prof': 'tailoring'} and src[900011]['prof'] == 'tailoring'   # by word and by [skill=]
    assert {e['id']: e['src'][0] for e in specs['paladin-holy']}[900001]['faction'] is None              # «Both factions»
    assert all(it['provenance'] == 'wowhead-forever-guide' for it in items.values())


def test_gear_import_singlefile():
    """SingleFile saves of the Wowhead level-30 guides: links and table cells only (no guide text), slot only from a Slot
    column, not-gear rows and spell links left out, an unclear quest pairing kept as «a quest», the file per spec."""
    sys.path.insert(0, os.path.join(bg.HERE, 'tools'))
    import gear_import as gi
    specs, items, files, issues = gi.from_singlefile(os.path.join(FIX, 'gear_singlefile'))
    assert list(specs) == ['mage-frost'] and files['mage-frost']['saved'] == '2026-10-30 07:49'
    src = {e['id']: e['src'] for e in specs['mage-frost']}
    assert sorted(src) == [900201, 900202, 900203, 900204, 900205, 900206, 900207, 900209, 900210, 900212]   # no bread, no #900208, nothing after the parts
    assert src[900201] == [{'kind': 'drop', 'boss': {'en': 'Test Boss Glacius'}, 'dungeon': {'en': 'Test Hollow'}}]
    assert src[900202][0]['trash'] and src[900202][0]['boss'] == {}
    assert [s['boss']['en'] for s in src[900203]] == ['Test Lich', 'Test Ghoul'] and src[900203][0]['dungeon'] == {'en': 'Test Crypt'}
    assert src[900204] == [{'kind': 'quest', 'quest': {'en': 'Test Ashes', 'id': 900301}, 'faction': 'horde'}]
    assert src[900205][0]['faction'] == 'alliance'
    assert src[900206] == [{'kind': 'quest', 'quest': {}, 'faction': None}]                   # two quests, two items: not on the page which
    assert src[900209] == [{'kind': 'craft', 'prof': 'tailoring'}] and items[900209]['slot'] == 'head'
    assert items[900210]['slot'] is None and items[900201]['slot'] is None and items[900201]['lvl'] is None
    assert src[900212][0]['world'] and src[900212][0]['suffix'] == 'of the Falcon'
    assert items[900201] == {'slot': None, 'lvl': None, 'il': None, 'q': 3, 'names': {'en': 'Test Collar'}, 'stats': {},
                             'provenance': 'wowhead-forever-guide'}
    text = json.dumps([specs, items], ensure_ascii=False)
    assert 'note of the guide' not in text and 'sentence of the guide' not in text and 'Talent text' not in text
    assert any('spell 900401' in x for x in issues) and any('900208' in x for x in issues) and any('food' in x for x in issues)


def test_gear_import_addon():
    """The addon dump: no item over level 30, armor of the class only, sources kept, provenance client-dump."""
    sys.path.insert(0, os.path.join(bg.HERE, 'tools'))
    import gear_import as gi
    specs, items = gi.from_addon(os.path.join(FIX, 'gear_dump.lua'))
    assert 900105 not in items and 900102 not in items                       # level 35; plate before 40
    war = [e['id'] for e in specs['warrior-protection']]
    assert 900103 in war and 900102 not in war
    holy = {e['id']: e['src'] for e in specs['priest-holy']}
    assert 900103 not in holy and holy[900106] == [{'kind': 'craft', 'prof': 'tailoring'}]    # mail is not for a priest; a recipe in Russian
    assert items[900101]['stats']['hp'] == 9 and items[900101]['provenance'] == 'client-dump'   # the «Equip:» line of the tooltip
    assert 900107 in war and 900107 not in holy                             # v2: iclass / isub instead of cls / sub
    assert not {900108, 900109, 900110} & set(items)                         # consumables and trade goods are not gear


def test_gear_import_addon_v2():
    """Dump v2: every kept item with its kind, icon file id, names and tooltip; v1 fields still read."""
    sys.path.insert(0, os.path.join(bg.HERE, 'tools'))
    import gear_import as gi
    al = gi.addon_items(os.path.join(FIX, 'gear_dump.lua'))
    assert al[900108] == {'kind': 'consumable', 'iclass': 0, 'isub': 0, 'slot': None, 'lvl': 15, 'il': 25, 'q': 1, 'icon': 134831,
                          'names': {'en': 'Test Healing Potion', 'ru': 'Тестовое лечебное зелье'}, 'stats': {},
                          'tip': {'en': ['Test Healing Potion', 'Use: Restores 140 to 180 health.']}}
    assert al[900109]['kind'] == 'trade' and al[900109]['lvl'] is None and al[900109]['names'] == {'ru': 'Тестовая ткань'}
    assert al[900110]['lvl'] == 50                                         # up to 60 in v2
    assert al[900101]['kind'] == 'armor' and al[900101]['isub'] == 1 and al[900101]['icon'] is None    # v1 item: cls / sub
    assert al[900107]['slot'] == 'INVTYPE_WAIST' and al[900107]['stats'] == {'str': 6, 'sta': 5}


def test_gear_section():
    """With data: the table by slot, one slot name per group, the faction of the quests, the source line, the answer row.
    Without: no section and no answer row."""
    from content import spec_cheats as sc
    fx = sc.load_gear30(os.path.join(FIX, 'gear30.json'))
    tr = lambda s, l: s   # noqa: E731
    fn = {'alliance': 'Альянс', 'horde': 'Орда'}
    html = sc.gear_html('mage-frost', 'ru', tr, fn, fx)
    assert html.count('<tr data-s=') == 11 and 'class="gtest"' in html and 'гайды Wowhead Forever, данные беты на' in html
    assert '<b>Временно:</b> данные беты, обновим после старта игры.' in html and 'Неполно' not in html
    assert 'data-f="horde"' in html and 'data-p="tailoring"' in html and 'Квест: Тестовый квест: прах к праху' in html
    assert sc.gear_html('mage-frost', 'ru', tr, fn, {'items': {}, 'specs': {}}) == ''
    assert sc.gear_html('rogue-combat', 'ru', tr, fn, fx) == ''
    assert 'Предметов: 11 · ур. 17–28 · данные беты.' in sc.gear_answer('mage-frost', 'ru', fx)
    one = json.loads(json.dumps(fx))                                  # level 1 = no required level: «—» in the table, not the low end of the span
    k = str(next(e['id'] for e in one['specs']['mage-frost']))
    one['items'][k]['lvl'] = 1
    h1 = sc.gear_html('mage-frost', 'ru', tr, fn, one)
    assert '>1</td>' not in h1 and f'data-lv="0"' in h1 and ' 1–' not in sc.gear_answer('mage-frost', 'ru', one)
    part = dict(fx, partial=['mage-frost'])
    html = sc.gear_html('mage-frost', 'ru', tr, fn, part)
    assert '<b>Неполно:</b> предметы есть только для' in html and 'данные беты, неполно.' in sc.gear_answer('mage-frost', 'ru', part)
    empty = not sc.GEAR30.get('specs')
    for d in ('', 'en/', 'uk/'):
        page = os.path.join(bg.HERE, d + 'guides', 'spec-mage-frost', 'index.html')
        if os.path.isfile(page) and empty:
            assert 'id="gearBox"' not in open(page, encoding='utf-8').read()

def test_dungeon_pages():
    """guides/dungeons/<slug>/: every record matches DUNGEONS, the page carries the facts, roles and quests; loot only with data."""
    from content import dungeon_pages as dp
    reg, order = dp.registry()
    links = dp.table_links()
    for p in dp.DUNGEON_PAGES:
        assert p['name'] in reg, p['name']
        assert links[order.index(p['name'])] == p['slug'] + '/'
        assert reg[p['name']][5] in ('alliance', 'horde', None), p['name']            # the side of the entrance; none = open to both ('both' breaks the filters)
        assert all(b.get(k) for b in p['bosses'] for k in ('name', 'abil', 'tank', 'heal', 'dps')), p['name']
        assert sum(1 for b in p['bosses'] if b.get('last')) == 1, p['name']
        assert all(s in ('alliance', 'horde', 'both') for _, _, s in p['quests']), p['name']
        g = next(x for x in cg.GUIDES if x['slug'] == f'dungeons/{p["slug"]}')
        assert g['hub'] is False and g['others'] is False and [s['id'] for s in g['sections']] == ['about', 'group', 'bosses', 'quests']
        for d in ('', 'en/', 'pl/'):
            html = open(os.path.join(bg.HERE, d + f'guides/dungeons/{p["slug"]}/', 'index.html'), encoding='utf-8').read()
            assert 'class="dgboss"' in html and html.count('<li><h3>') == len(p['bosses']) and 'id="loot"' not in html
            assert all(b['name'] in html for b in p['bosses'])
    dg = open(os.path.join(bg.HERE, 'en/guides/dungeons/', 'index.html'), encoding='utf-8').read()
    assert all(f'href="{p["slug"]}/"' in dg for p in dp.DUNGEON_PAGES)                 # the list links its pages


def test_dungeon_loot_index():
    """Loot by boss: the reverse index of the gear list (data/gear30.json schema), only drops of this dungeon."""
    from content import dungeon_pages as dp
    data = {'items': {'1': {'slot': 'neck', 'lvl': 17, 'q': 2, 'names': {'en': 'Test Choker'}, 'stats': {}},
                      '2': {'slot': 'two', 'lvl': 18, 'q': 3, 'names': {'en': 'Test Stave', 'ru': 'Тестовый посох'}, 'stats': {}},
                      '3': {'slot': 'feet', 'lvl': 20, 'q': 2, 'names': {'en': 'Elsewhere Boots'}, 'stats': {}}},
            'specs': {'mage-frost': [{'id': 2, 'src': [{'kind': 'drop', 'boss': {'en': 'Plunder'}, 'dungeon': {'en': 'Hall of Thanes'}}]},
                                     {'id': 1, 'src': [{'kind': 'drop', 'boss': {'en': 'Faldrim Anvilmar'}, 'dungeon': {'en': 'Hall of Thanes'}}]}],
                      'priest-holy': [{'id': 2, 'src': [{'kind': 'drop', 'boss': {'en': 'Plunder'}, 'dungeon': {'en': 'Hall of Thanes'}}]},
                                      {'id': 3, 'src': [{'kind': 'drop', 'boss': {'en': 'Witherfang'}, 'dungeon': {'en': 'Ruins of Lordaeron'}}]}]}}
    idx = dp.loot_index('Hall of Thanes', data)
    assert set(idx) == {'Plunder', 'Faldrim Anvilmar'}
    assert idx['Plunder'][0][0] == '2' and idx['Plunder'][0][2] == ['mage-frost', 'priest-holy']
    assert dp.loot_index('Hall of Thanes', {'items': {}, 'specs': {}}) == {}
    html = dp._loot(dp.BY_NAME['Hall of Thanes'], idx, 'ru')
    assert 'Тестовый посох' in html and 'Маг · Лёд' in html and 'Elsewhere' not in html


def test_level_jump_targets_exist():
    """«My level» of the leveling guides: every chip of every built page (all languages) leads to an id of the very page,
    and the chips are the level ranges of the zone route."""
    import re, langs
    root = os.path.dirname(os.path.abspath(__file__)) + '/..'
    steps, _ = bg.leveling_parts()
    ranges = list(dict.fromkeys((lo, hi) for rows in steps.values() for lo, hi, _d in rows))
    slugs = ['leveling'] + [g['slug'] for g in bg.GUIDES if g['slug'].startswith('leveling-')]
    seen = 0
    for lang in ('',) + tuple(l for l in langs.LANGS if l != 'ru'):
        for slug in slugs:
            f = os.path.join(root, lang, 'guides', slug, 'index.html')
            if not os.path.isfile(f):
                continue
            html = open(f, encoding='utf-8').read()
            nav = re.search(r'<nav class="gjump lvl".*?</nav>', html, re.S)
            if not nav:
                continue
            hrefs = re.findall(r'href="#([^"]+)"', nav.group(0))
            assert len(hrefs) == len(ranges), (f, hrefs)
            for h in hrefs:
                assert f'id="{h}"' in html, f'{f}: no #{h}'
            seen += 1
    assert seen >= 10, seen


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
