"""Сборщик экипировки character/gear/ (gear_planner.py, assets/gear/planner.js): ядро скрипта в node (hash туда-обратно, фильтр по классу
и уровню, двуручное оружие, сумма статов, «наша сборка»), файлы данных и страница во всех языках. Запуск: python tests/test_gear_planner.py"""
import gzip, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import langs  # noqa: E402

JS = r'''
const C = require(process.argv[1]), assert = require('assert');
const D = { k: ['str','agi','sta','int','spi','armor','sp','hp','ap','crit','hit','mp5','def','dps'],
  sl: ['head','neck','shoulder','back','chest','wrist','hands','waist','legs','feet','finger','trinket','main','two','off','ranged','relic'],
  it: [[1, 0, 2, 20, 15, 4, 1, 3, 'Cloth Hat', [3, 5, 2, 2]],          // cloth head lvl 15: +5 int +2 sta
       [2, 0, 3, 30, 25, 4, 4, 4, 'Plate Helm', [0, 8, 5, 300]],       // plate head lvl 25 (worn from 40)
       [3, 0, 2, 50, 45, 4, 4, 5, 'High Plate Helm', [0, 12]],        // plate head lvl 45
       [4, 13, 3, 30, 25, 2, 10, 6, 'Staff', [3, 10, 13, 20]],        // two-hand staff
       [5, 12, 2, 25, 20, 2, 15, 7, 'Dagger', [1, 4, 13, 12]],        // one-hand dagger
       [6, 14, 2, 25, 20, 4, 6, 8, 'Shield', [5, 400]],               // shield
       [7, 14, 2, 25, 20, 4, 0, 9, 'Orb', [3, 6]],                    // held in off hand
       [8, 10, 3, 28, 22, 4, 0, 10, 'Ring A', [3, 4]], [9, 10, 2, 22, 18, 4, 0, 11, 'Ring B', [2, 3]],
       [10, 15, 2, 25, 20, 2, 19, 12, 'Wand', [6, 5, 13, 15]]],
  src: { 1: [0, 'Boss · Dungeon'], 4: [1, 'Quest: X'] }, b: {} };
const items = C.unpack(D), by = {}; items.forEach(i => by[i.id] = i);

// the address, both ways
const S = { c: 'mage', s: 'frost', r: 'gnome', l: 24, g: { head: 1, main: 4, finger1: 8, finger2: 9 }, t: '0-5-3' };
const h = C.enc(S);
assert.strictEqual(h, 'c=mage&s=frost&r=gnome&l=24&g=head:1,finger1:8,finger2:9,main:4&t=0-5-3');
assert.deepStrictEqual(C.dec('#' + h), S);
assert.deepStrictEqual(C.dec('#c=MAGE&l=99&g=head:x,nope:5,neck:7&t=<b>').g, { neck: 7 });   // junk is dropped
assert.strictEqual(C.dec('#l=99').l, 0);

// class and level: a mage sees cloth only, a warrior plate from 40, the level filter hides higher items
const f = { lvl: true, arm: true };
assert.deepStrictEqual(C.cands(items, 'head', { c: 'mage', l: 30 }, f, null).map(i => i.id), [1]);
assert.deepStrictEqual(C.cands(items, 'head', { c: 'warrior', l: 30 }, f, null).map(i => i.id), [1]);
assert.deepStrictEqual(C.cands(items, 'head', { c: 'warrior', l: 40 }, f, null).map(i => i.id), [2, 1]);
assert.deepStrictEqual(C.cands(items, 'head', { c: 'warrior', l: 60 }, f, null).map(i => i.id), [3, 2, 1]);
assert.deepStrictEqual(C.cands(items, 'head', { c: 'mage', l: 10 }, { lvl: false, arm: false }, null).map(i => i.id), [3, 2, 1]);
assert.deepStrictEqual(C.cands(items, 'head', { c: 'mage', l: 60 }, { q: 'HAT' }, null).map(i => i.id), [1]);
assert.deepStrictEqual(C.cands(items, 'head', { c: 'mage', l: 60 }, { drop: true }, null).map(i => i.id), [1]);
// spec weights sort: int first for a caster
const w = { int: 1, sta: .1 };
assert.strictEqual(C.cands(items, 'main', { c: 'mage', l: 30 }, f, w)[0].id, 4);
// the main hand takes one- and two-handers; the off hand: a shield only for its classes, a weapon only for dual wielders
assert.deepStrictEqual(C.cands(items, 'main', { c: 'mage', l: 30 }, f, null).map(i => i.id).sort(), [4, 5]);
assert.deepStrictEqual(C.cands(items, 'off', { c: 'mage', l: 30 }, f, null).map(i => i.id), [7]);
assert.deepStrictEqual(C.cands(items, 'off', { c: 'warrior', l: 30 }, f, null).map(i => i.id).sort(), [5, 6, 7]);
assert.deepStrictEqual(C.cands(items, 'off', { c: 'rogue', l: 30 }, f, null).map(i => i.id).sort(), [5, 7]);
assert.deepStrictEqual(C.cands(items, 'ranged', { c: 'mage', l: 30 }, f, null).map(i => i.id), [10]);
assert.deepStrictEqual(C.cands(items, 'ranged', { c: 'warrior', l: 30 }, f, null).map(i => i.id), []);

// a two-hander empties and locks the off hand
let g = C.equip({ off: 7 }, 'main', by[4]);
assert.deepStrictEqual(g, { main: 4 });
assert.ok(C.offLocked(g, by));
g = C.equip(g, 'main', by[5]);
assert.ok(!C.offLocked(g, by));
assert.deepStrictEqual(C.equip(g, 'main', null), {});

// the sum: stats of every slot, weapon dps of the main hand only
const t = C.sum([{ cell: 'head', it: by[1] }, { cell: 'main', it: by[5] }, { cell: 'ranged', it: by[10] }, null]);
assert.deepStrictEqual(t, { int: 5, sta: 2, agi: 4, dps: 12, sp: 5 });

// our build: best per cell within the level, a second ring other than the first, two-hander against main + off
const ours = C.fill(items, [1, 2, 4, 5, 7, 8, 9], { c: 'mage', l: 30 }, w);
assert.deepStrictEqual(ours, { head: 1, finger1: 8, finger2: 9, main: 4 });
assert.deepStrictEqual(C.fill(items, [1, 8], { c: 'mage', l: 16 }, w), { head: 1 });
console.log('core ok');
'''


def main():
    out = subprocess.run(['node', '-e', JS, os.path.join(ROOT, 'assets', 'gear', 'planner.js')], capture_output=True, text=True, encoding='utf-8')
    assert out.returncode == 0, out.stderr[-2000:]
    import gear_planner as gp
    w = gp.weights('sp crit hit int')
    assert w['sp'] == 1 and w['int'] == .5 * gp.UNIT['int'] and w['crit'] > w['hit'], w
    sizes = {}
    for lang in langs.LANGS:
        p = os.path.join(ROOT, 'assets', 'gear', f'planner-{lang}.json')
        raw = open(p, 'rb').read()
        sizes[lang] = len(gzip.compress(raw, 9))
        d = json.loads(raw)
        assert len(d['it']) > 8000 and d['k'] == gp.K and d['sl'] == gp.SL, lang
        assert all(a[4] <= 60 for a in d['it']), lang
        assert len(d['b']) == 27, (lang, len(d['b']))
        html = open(os.path.join(ROOT, build_dir(lang), 'character', 'gear', 'index.html'), encoding='utf-8').read()
        assert 'id="gpData"' in html and 'assets/gear/planner.js?v=' in html, lang
        cfg = json.loads(re.search(r'<script type="application/json" id="gpData">(.*?)</script>', html, re.S)[1])
        assert cfg['data'].endswith(f'planner-{lang}.json?v={gp.vhash(p)}'), (lang, cfg['data'])
        assert len(cfg['cls']) == 9 and len(cfg['cells']) == 17, lang
        assert 'wowhead' not in html.split('<footer')[0].lower() and 'zamimg' not in html, lang   # no Wowhead links or pictures in the planner
        assert re.search(r'href="[^"]*character/gear/"', open(os.path.join(ROOT, build_dir(lang), 'character', 'index.html'), encoding='utf-8').read()), lang
        spec = open(os.path.join(ROOT, build_dir(lang), 'guides', 'spec-mage-frost', 'index.html'), encoding='utf-8').read()
        assert 'character/gear/#c=mage&amp;s=frost' in spec, lang
    ru = json.load(open(os.path.join(ROOT, 'assets', 'gear', 'planner-ru.json'), encoding='utf-8'))
    assert any(re.search('[а-я]', a[8]) for a in ru['it'][:200]), 'ru item names'
    assert max(sizes.values()) < 400 * 1024, sizes
    print(f'OK gear planner: core, {len(sizes)} languages, data gzip {min(sizes.values()) // 1024}–{max(sizes.values()) // 1024} KB')


def build_dir(lang):
    return '' if lang == 'ru' else lang


if __name__ == '__main__':
    main()
