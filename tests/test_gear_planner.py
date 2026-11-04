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

// our build: best per cell within the level, a second ring other than the first, two-hander against main + off;
// the other cells by the spec's stats from the whole catalog, marked as a stat pick
const ours = C.fill(items, [1, 2, 4, 5, 7, 8, 9], { c: 'mage', l: 30 }, w, [16, 30]);
assert.deepStrictEqual(ours.g, { head: 1, finger1: 8, finger2: 9, main: 4 });   // the wand has nothing of int, sta: no stat pick
assert.deepStrictEqual(ours.auto, []);
assert.deepStrictEqual(C.fill(items, [1, 8], { c: 'mage', l: 30 }, { int: 1, sp: 1 }, [16, 30]).auto, ['main', 'ranged']);   // with spell power: staff and wand
assert.strictEqual(ours.ours, 4);
assert.ok(!ours.out);
let r = C.fill(items, [1, 8], { c: 'mage', l: 16 }, w, [16, 30]);
assert.deepStrictEqual(r.g, { head: 1 });                             // Ring A needs 22: nothing else fits 16 with these weights
assert.deepStrictEqual(r.auto, []);

// «Fill» at every level 1–60 gives something sensible: the catalog fills what our build lacks, the level, armor and side hold
const F = { k: D.k, sl: D.sl, src: {}, b: {}, fa: { 21: 'a', 22: 'h' },
  it: [[20, 7, 1, 5, 1, 4, 1, 1, 'Starter Belt', [2, 1]],             // common cloth belt lvl 1
       [21, 7, 2, 12, 8, 4, 1, 1, 'Alliance Belt', [3, 4]],           // uncommon, Alliance only
       [22, 7, 2, 12, 8, 4, 1, 1, 'Horde Belt', [3, 3]],              // uncommon, Horde only
       [23, 7, 2, 25, 20, 4, 1, 1, 'Belt 20', [3, 6]],
       [24, 7, 3, 50, 45, 4, 1, 1, 'Belt 45', [3, 10]],
       [25, 7, 3, 65, 60, 4, 1, 1, 'Belt 60', [3, 14]],
       [26, 7, 4, 70, 60, 4, 1, 1, 'Epic Belt', [3, 30]],             // epic: not in an automatic pick
       [27, 7, 3, 50, 45, 4, 4, 1, 'Plate Belt', [3, 40]],            // plate: never for a mage
       [28, 7, 2, 30, 25, 4, 1, 1, 'Our Belt', [3, 1]]] };            // our build, weak on stats but ours
const fi = C.unpack(F), fb = {}; fi.forEach(i => fb[i.id] = i);
const belt = (l, f, ids) => C.fill(fi, ids || [28], { c: 'mage', l: l, f: f }, w, [16, 30]);
assert.strictEqual(belt(1, 'a').g.waist, 20);                          // level 1: common is fine
assert.deepStrictEqual(belt(1, 'a').auto, ['waist']);
assert.strictEqual(belt(10, 'a').g.waist, 21);                        // the Alliance belt for a gnome
assert.strictEqual(belt(10, 'h').g.waist, 22);                        // the Horde one for an orc
assert.strictEqual(belt(10, '').g.waist, 21);                         // no race: both sides
assert.strictEqual(belt(20, 'h').g.waist, 23);
assert.strictEqual(belt(30, 'h').g.waist, 28);                        // in our range our item wins
assert.deepStrictEqual(belt(30, 'h').auto, []);
assert.strictEqual(belt(45, 'h').g.waist, 24);                        // above it (30 + 5): a stat pick, not our old belt
assert.ok(belt(45, 'h').out && belt(45, 'h').auto.indexOf('waist') > -1);
assert.strictEqual(belt(60, 'a').g.waist, 25);                        // no epic, no plate
for (const l of [1, 10, 20, 45, 60]) assert.ok(Object.keys(belt(l, 'h').g).length, l);
// the picker hides the other side's items
assert.deepStrictEqual(C.cands(fi, 'waist', { c: 'mage', l: 10, f: 'h' }, f, w).map(i => i.id), [22, 20]);
assert.deepStrictEqual(C.cands(fi, 'waist', { c: 'mage', l: 10, f: 'a' }, f, w).map(i => i.id), [21, 20]);
assert.deepStrictEqual(C.cands(fi, 'waist', { c: 'warrior', l: 45, f: 'a' }, f, w).map(i => i.id)[0], 27);   // plate for a warrior from 40

// races of an address: the site's addresses (night-elf) and the old ids (nightelf, skyA) both read; the address writes the site's one
const R = [['nightelf', 'Night Elf', 'alliance', [], 'night-elf'], ['skyA', 'Skyborne', 'alliance', [], 'skyborne-alliance'], ['orc', 'Orc', 'horde', [], 'orc']];
assert.strictEqual(C.race('night-elf', R), 'nightelf');
assert.strictEqual(C.race('nightelf', R), 'nightelf');
assert.strictEqual(C.race('skyA', R), 'skyA');
assert.strictEqual(C.race('skyborne-alliance', R), 'skyA');
assert.strictEqual(C.race('SKYA', R), 'skyA');
assert.strictEqual(C.race('elf', R), '');
assert.strictEqual(C.dec('#c=hunter&r=skyA').r, 'skyA');                // the old id with its capital letter survives the address
assert.strictEqual(C.dec('#c=hunter&r=night-elf').r, 'night-elf');
assert.strictEqual(C.enc({ c: 'hunter', r: 'nightelf' }, { nightelf: 'night-elf' }), 'c=hunter&r=night-elf');
// the picker compares with the item of THIS cell only: an empty cell has nothing to unequip and every change is a plus
const gw = { head: 1, finger1: 8, trinket1: 0 };
assert.strictEqual(C.worn(gw, 'feet', by), null);
assert.strictEqual(C.worn(gw, 'head', by).id, 1);
assert.strictEqual(C.worn(gw, 'finger1', by).id, 8);
assert.strictEqual(C.worn(gw, 'finger2', by), null);                  // ring 2 is its own cell
assert.strictEqual(C.worn({ feet: 1 }, 'feet', by), null);            // a head item under «feet» counts as nothing
assert.deepStrictEqual(C.diff(by[9], null), { sta: 3 });              // empty cell: all plus
assert.deepStrictEqual(C.diff(by[9], C.worn(gw, 'finger1', by)), { int: -4, sta: 3 });
assert.deepStrictEqual(C.diff(by[8], C.worn(gw, 'finger2', by)), { int: 4 });
// an address with an item in a foreign cell, an unknown id and a shield beside a two-hander: cleaned
assert.deepStrictEqual(C.clean({ feet: 1, head: 1, neck: 999, main: 4, off: 6, finger2: 9 }, by, 'warrior'), { head: 1, main: 4, finger2: 9 });
assert.deepStrictEqual(C.clean({ off: 5 }, by, 'mage'), {});          // a dagger in the off hand: dual wielders only
assert.deepStrictEqual(C.clean({ off: 5 }, by, 'rogue'), { off: 5 });
console.log('core ok');
'''


def main():
    out = subprocess.run(['node', '-e', JS, os.path.join(ROOT, 'assets', 'gear', 'planner.js')], capture_output=True, text=True, encoding='utf-8')
    assert out.returncode == 0, out.stderr[-2000:]
    import gear_planner as gp
    from content import play_card as pc
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
        assert d['cv'] == [pc.GEAR_LO, pc.GEAR_HI], d['cv']
        by = {a[0]: a for a in d['it']}
        assert d['fa'].get('20126') == 'a' and d['fa'].get('20207') == 'h', lang     # Highlander's / Defiler's Plate Girdle 28
        assert not d['fa'].get('1156'), lang                                       # a Deadmines drop: both sides
        assert 12064 not in by and 8350 not in by, lang                           # Gamemaster Hood, The 1 Ring
        assert by[20126][5:7] == [4, 3], lang   # the level-28 «plate» girdle of Arathi Basin is mail in the catalog: a warrior may wear it before 40
        assert all(len(r) == 5 for r in cfg_races(lang)), lang
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


def cfg_races(lang):
    html = open(os.path.join(ROOT, build_dir(lang), 'character', 'gear', 'index.html'), encoding='utf-8').read()
    return json.loads(re.search(r'<script type="application/json" id="gpData">(.*?)</script>', html, re.S)[1])['races']


def build_dir(lang):
    return '' if lang == 'ru' else lang


if __name__ == '__main__':
    main()
