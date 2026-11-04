"""data/items_catalog.json + assets/gear/catalog-*.webp (tools/item_catalog.py): the format the pages will read. No network."""
import json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import item_catalog as ic  # noqa: E402

CATS = {'equip', 'potion', 'elixir', 'flask', 'food', 'drink', 'bandage', 'poison', 'reagent', 'trade'}
SLOTS = set(ic.SLOTS.values())
STATS = {'str', 'agi', 'sta', 'int', 'spi', 'armor', 'sp', 'hp', 'mp5', 'hit', 'crit', 'def', 'ap', 'dps'}


def load():
    p = os.path.join(HERE, 'data', 'items_catalog.json')
    return json.load(open(p, encoding='utf-8')), os.path.getsize(p)


def test_consumable_kinds():
    k = ic.consumable
    assert k('Major Mana Potion', 'Use: Restores 1350 to 2250 mana. (2 Mins Cooldown)') == 'potion'
    assert k('Morning Glory Dew', 'Use: Restores 2821 mana over 30 sec.  Must remain seated while drinking.') == 'drink'
    assert k('Roasted Quail', 'Use: Restores 1392 health over 27 sec.  Must remain seated while eating.') == 'food'
    assert k('Linen Bandage', 'Use: Heals 66 damage over 6 sec.') == 'bandage'
    assert k('Instant Poison', 'Use: Coats a weapon with poison that lasts for 30 minutes.') == 'poison'
    assert k('Flask of the Titans', 'Use: Increases the player\'s maximum health by 400 for 2 hrs.') == 'flask'
    assert k('Elixir of the Mongoose', 'Use: Increases Agility by 25 for 1 hour.') == 'elixir'
    assert k('Scroll of Agility', 'Use: Increases Agility by 5 for 30 min.') is None
    assert ic.JUNK.search('Monster - Sword, Long') and ic.JUNK.search('Deprecated Tauren Recruit\'s Shirt')
    assert not ic.JUNK.search('Thunderfury, Blessed Blade of the Windseeker')


def test_catalog_format():
    d, size = load()
    assert d['schema'] == 1 and d['langs'] == ['en', 'ru', 'de', 'fr', 'es', 'pt', 'it'] and d['cell'] == 36
    assert 'static-classic1x-eu' in d['source']
    assert size <= 3 * 1024 * 1024, f'{size} bytes'
    cols, cell = d['cols'], d['cell']
    assert set(d['sprites']) == set(d['icons']) in ({'all'}, {'equip', 'use'})
    assert set(d['sprite_of']) == CATS and set(d['sprite_of'].values()) == set(d['sprites'])
    for sp, s in d['sprites'].items():
        assert s['n'] == len(d['icons'][sp]) == len(set(d['icons'][sp])) > 0
        assert all(isinstance(f, int) and f > 0 for f in d['icons'][sp])
        p = os.path.join(HERE, s['file'])
        assert os.path.getsize(p) <= 1536 * 1024, f'{s["file"]}: {os.path.getsize(p)} bytes'
        from PIL import Image
        w, h = Image.open(p).size
        assert (w, h) == (cols * cell, -(-s['n'] // cols) * cell), (s['file'], w, h)
    by = {}
    for k, it in d['items'].items():
        assert k.isdigit() and 0 < int(k) < ic.MAX_ID
        assert it['c'] in CATS, (k, it['c'])
        by[it['c']] = by.get(it['c'], 0) + 1
        assert len(it['n']) == 7 and it['n'][0], k
        assert 0 <= it['q'] <= 5 and isinstance(it['il'], int) and 1 <= it.get('lvl', 1) <= 60
        assert isinstance(it['k'], list) and len(it['k']) == 2
        if it['c'] == 'equip':
            assert it['s'] in SLOTS and it['k'][0] in (2, 4) and it['q'] >= 1
            assert set(it.get('st', {})) <= STATS, (k, it.get('st'))
        else:
            assert 's' not in it and 'st' not in it
            assert it['k'][0] == {'reagent': 5, 'trade': 7}.get(it['c'], 0), (k, it)
        if 'i' in it:
            assert 0 <= it['i'] < d['sprites'][d['sprite_of'][it['c']]]['n']
    assert by.get('equip', 0) > 5000 and all(by.get(c, 0) > 0 for c in CATS), by
    with_icon = sum(1 for it in d['items'].values() if 'i' in it)
    assert with_icon >= 0.95 * len(d['items']), (with_icon, len(d['items']))
    text = json.dumps(d)
    assert 'zamimg' not in text and 'wowhead' not in text.lower()
    # names a reader knows
    assert d['items']['13444']['c'] == 'potion' and d['items']['13444']['n'][0] == 'Major Mana Potion'
    assert d['items']['1251']['c'] == 'bandage' and d['items']['19019']['s'] == 'main'


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('items catalog: OK')
