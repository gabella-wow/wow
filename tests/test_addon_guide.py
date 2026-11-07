"""Данные гида для аддона в игре: assets/addon/gabella-guide.json (tools/export_addon.py, build.py пишет его при каждой сборке).
Схема договорена с аддоном: подземелья, маршрут по зонам, снаряжение и таланты спека. Запуск: python tests/test_addon_guide.py"""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, os.path.join(ROOT, 'content'))
sys.path.insert(0, ROOT)
PATH = os.path.join(ROOT, 'assets', 'addon', 'gabella-guide.json')

# the agreed value sets (the addon switches on them): sides, item slots of the gear planner + ammo, kinds of an item source
SIDES = {'horde', 'alliance', 'both'}
SLOTS = {'head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'hands', 'waist', 'legs', 'feet', 'finger', 'trinket',
         'main', 'two', 'off', 'ranged', 'relic', 'ammo'}
SOURCES = {'boss', 'quest', 'recipe', 'vendor', 'world'}
SPEC = re.compile(r'^[a-z]+-[a-z]+(?:-[a-z]+)*$')
CYR = re.compile('[А-Яа-яЁё]')


def load():
    with open(PATH, encoding='utf-8') as f:
        return json.load(f)


def is_id(x):
    return type(x) is int and x > 0


def opt_str(x):
    return x is None or (isinstance(x, str) and x.strip() == x and x != '')


def test_file_is_lf_json_and_published():
    raw = open(PATH, 'rb').read()
    assert raw.endswith(b'\n') and b'\r' not in raw, 'LF only, newline at the end'
    json.loads(raw.decode('utf-8'))
    # GitHub Pages serves the main branch as it is (.nojekyll): a file git ignores never reaches gabella.site
    ignored = subprocess.run(['git', 'check-ignore', '-q', 'assets/addon/gabella-guide.json'], cwd=ROOT).returncode == 0
    assert not ignored, 'assets/addon/gabella-guide.json is git-ignored'
    assert os.path.isfile(os.path.join(ROOT, '.nojekyll'))


def test_top_level_and_version_from_content():
    d = load()
    assert list(d) == ['version', 'dungeons', 'route', 'gear', 'talents'], list(d)
    rest = {k: v for k, v in d.items() if k != 'version'}
    want = hashlib.sha1(json.dumps(rest, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()[:12]
    assert d['version'] == want, (d['version'], want)   # the hash of the content: the same sources give the same file


def test_file_is_fresh_and_deterministic():
    import export_addon
    a, b = export_addon.payload(), export_addon.payload()
    assert a == b, 'two runs on the same sources differ'
    assert load() == a, 'assets/addon/gabella-guide.json is stale: run python build.py'


def test_dungeons():
    import dungeon_pages
    d = load()['dungeons']
    _, order = dungeon_pages.registry()
    assert [x['en'] for x in d] == order, 'every DUNGEONS row, in the table order'
    keys = [x['key'] for x in d]
    assert len(set(keys)) == len(keys), keys
    for x in d:
        assert set(x) >= {'key', 'en', 'ru', 'min', 'max', 'zone_en', 'zone_ru', 'uiMapID', 'side', 'verified'}, x
        assert re.fullmatch(r'[a-z0-9]+(?:_[a-z0-9]+)*', x['key']), x['key']
        assert isinstance(x['en'], str) and x['en'] and opt_str(x['ru']), x
        assert type(x['min']) is int and type(x['max']) is int and 1 <= x['min'] <= x['max'] <= 60, x
        assert isinstance(x['zone_en'], str) and x['zone_en'] and opt_str(x['zone_ru']), x
        assert x['uiMapID'] is None or is_id(x['uiMapID']), x
        assert x['side'] in SIDES and x.get('entrance') in {'horde', 'alliance', None}, x
        assert x['entrance'] is None or x['side'] in {x['entrance'], 'both'}, x
        assert type(x['verified']) is bool, x
        assert (x['ru'] is None or CYR.search(x['ru'])) and (x['zone_ru'] is None or CYR.search(x['zone_ru'])), x   # Russian or nothing


def test_route():
    import langs
    r = load()['route']
    assert set(r) == {'horde', 'alliance'}, set(r)
    for side, steps in r.items():
        assert steps, side
        assert steps[0]['from'] == 1 and steps[-1]['to'] == 60, side   # the whole way from 1 to 60
        assert [s['from'] for s in steps] == sorted(s['from'] for s in steps), side
        for s in steps:
            assert set(s) >= {'from', 'to', 'uiMapIDs', 'zones_ru', 'zones_en', 'text_ru', 'verified'}, s
            assert type(s['from']) is int and type(s['to']) is int and 1 <= s['from'] < s['to'] <= 60, s
            assert isinstance(s['uiMapIDs'], list) and all(is_id(i) for i in s['uiMapIDs']), s
            assert s['zones_ru'] and all(isinstance(z, str) and z for z in s['zones_ru']), s
            assert len(s['zones_ru']) == len(set(s['zones_ru'])) == len(s['zones_en']), s
            for ru, en in zip(s['zones_ru'], s['zones_en']):   # the client's Russian name of the zone, its English one when there is none
                assert ru == ((langs.NAMES.get(en) or {}).get('ru') or en), (ru, en)
            assert isinstance(s['text_ru'], str) and CYR.search(s['text_ru']) and not re.search(r'\[\[|\||\{', s['text_ru']), s   # no markup left
            assert type(s['verified']) is bool, s


def test_gear():
    data = load()
    keys = {x['key'] for x in data['dungeons']}
    g = data['gear']
    assert g.get('hunter-beast-mastery'), 'the hunter Beast Mastery list'
    for spec, items in g.items():
        assert SPEC.fullmatch(spec), spec
        ids = [x['itemID'] for x in items]
        assert len(set(ids)) == len(ids), spec
        for x in items:
            assert set(x) >= {'slot', 'level', 'itemID', 'ru', 'source', 'verified'}, x
            assert x['slot'] in SLOTS, x
            assert x['level'] is None or (type(x['level']) is int and 2 <= x['level'] <= 60), x   # none = no required level
            assert is_id(x['itemID']), x
            assert isinstance(x['ru'], str) and x['ru'], x
            s = x['source']
            assert isinstance(s, dict) and set(s) >= {'type', 'ru', 'dungeon'}, x
            assert s['type'] in SOURCES and opt_str(s['ru']), x
            assert s['dungeon'] is None or s['dungeon'] in keys, x
            assert s['dungeon'] is None or s['type'] == 'boss', x
            assert x.get('side', 'both') in SIDES and type(x['verified']) is bool, x


def test_talents():
    t = load()['talents']
    rows = t.get('hunter-beast-mastery')
    assert rows, 'the hunter Beast Mastery order'
    for spec, rows in t.items():
        assert SPEC.fullmatch(spec), spec
        assert [x['level'] for x in rows] == list(range(10, 10 + len(rows))) and rows[-1]['level'] <= 60, spec   # one point a level from 10
        rank = {}
        for x in rows:
            assert set(x) >= {'level', 'talentID', 'spellID', 'rank', 'ru', 'verified'}, x
            assert x['talentID'] is None or is_id(x['talentID']), x
            assert x['spellID'] is None or is_id(x['spellID']), x
            assert isinstance(x['ru'], str) and CYR.search(x['ru']), x
            k = x['spellID'] or x['ru']
            assert type(x['rank']) is int and x['rank'] == rank.get(k, 0) + 1, x   # ranks go up one point at a time
            rank[k] = x['rank']
            assert type(x['verified']) is bool, x
    assert len(t['hunter-beast-mastery']) == 51 and all(is_id(x['spellID']) for x in t['hunter-beast-mastery'])   # the client tree has every spell


def test_dungeon_key_and_side():
    import export_addon as E
    assert E.key_of('Ragefire Chasm') == 'ragefire_chasm'
    assert E.key_of("Zul'Farrak") == 'zulfarrak' and E.key_of('Shaper’s Terrace') == 'shapers_terrace'
    assert E.key_of('Scarlet Monastery: Graveyard') == 'scarlet_monastery_graveyard'
    assert E.side_of('horde', 0) == 'horde'      # the entrance in Orgrimmar, the Alliance cannot go (Ragefire Chasm)
    assert E.side_of('alliance', 1) == 'both'    # the entrance on the Alliance side, the Horde can go too (Hall of Thanes)
    assert E.side_of(None, None) == 'both'


def test_zones_of_a_route_step():
    import export_addon as E
    # a «between A and B» clause places a zone on the map, it does not send you there; a continent is not a zone
    assert E.zones_of('С 35: новая зона Riverglades между [[Красногорьем|Redridge Mountains]] и [[Пылающими степями|Burning Steppes]], '
                      'Dustwallow Marsh, Badlands.') == ['Riverglades', 'Dustwallow Marsh', 'Badlands']
    assert E.zones_of('Duskwood и Wetlands, в [[Калимдоре|Kalimdor]] Stonetalon Mountains.') == ['Duskwood', 'Wetlands', 'Stonetalon Mountains']
    assert E.zones_of('с 48 [[Кратер Ун’Горо|Un’Goro Crater]] и Felwood.') == ["Un'Goro Crater", 'Felwood']   # the names file spells it with '
    assert E.zones_of('Люди: Elwynn Forest. Высшие скайборны: Zephras Isle, до 12.') == ['Elwynn Forest', 'Zephras Isle']


def test_item_source():
    import export_addon as E
    keys = {'scarlet_monastery_graveyard', 'razorfen_kraul'}
    assert E.source_of([{'kind': 'drop', 'boss': {}, 'dungeon': {'en': 'Razorfen Kraul', 'zone': 491}}], keys) == \
        {'type': 'boss', 'ru': 'Лабиринты Иглошкурых', 'dungeon': 'razorfen_kraul'}
    assert E.source_of([{'kind': 'drop', 'boss': {}, 'dungeon': {'en': 'Scarlet Monastery', 'zone': 796}}], keys)['dungeon'] is None   # no wing
    assert E.source_of([{'kind': 'drop', 'boss': {}, 'dungeon': {}, 'world': True}], keys) == {'type': 'world', 'ru': None, 'dungeon': None}
    assert E.source_of([{'kind': 'quest', 'quest': {'en': 'Rig Wars', 'id': 2841}, 'faction': None},
                        {'kind': 'quest', 'quest': {'en': 'The Grand Betrayal', 'id': 2929}, 'faction': None}], keys) == \
        {'type': 'quest', 'ru': 'Rig Wars / The Grand Betrayal', 'dungeon': None}
    assert E.source_of([{'kind': 'craft', 'prof': 'leatherworking'}], keys) == {'type': 'recipe', 'ru': 'Кожевничество', 'dungeon': None}


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK addon guide data')
