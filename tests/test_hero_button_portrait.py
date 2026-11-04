"""The hero button of the top bar (assets/hero/hero.js) and the home card «Your <class>» show the face of the hero's own race and
class, as play/ does (tests/test_play_portrait.py):
1) the map /*FACES*/ in hero.js (build.pair_faces) has only keys "<race>.<class>" of a pair the race can play, each pointing to
   assets/art/<class>-<race>-face.webp that exists; the class colours are build.COLOR;
2) run in node, heroFace() gives the pair's picture; with no pair drawn the class face of the race's side (build.side_faces),
   never a face of the other side and never the grey badge for a real pair (03.11: «Your <class>» showed a grey circle for
   38 of 56 pairs); the badge stays for an unknown race or class. heroMeta(): next to a face of another race the caption
   names the side, not the race;
3) every built page of the 9 languages that has hero.js loads the current hero.js and its language's data.
Run: python tests/test_hero_button_portrait.py (after python build.py)"""
import json, os, re, shutil, subprocess, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import build  # noqa: E402

LANGS = ['ru', 'en', 'uk', 'de', 'fr', 'es', 'pt', 'it', 'pl']
JS = os.path.join(ROOT, 'assets', 'hero', 'hero.js')


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def face_map():
    js = read(JS)
    i = js.index('/*FACES*/') + len('/*FACES*/')
    return json.JSONDecoder().raw_decode(js[i:])[0]


class HeroButtonPortrait(unittest.TestCase):
    def test_pairs_only(self):
        fm = face_map()
        races = {r['id']: r for r in build.parse_races(read(os.path.join(ROOT, 'index.src.html')))}
        self.assertTrue(fm['f'])
        self.assertEqual(fm['f'], build.pair_faces())
        self.assertEqual(fm['k'], build.side_faces())
        self.assertEqual(fm['r'], build.race_sides())
        self.assertEqual(fm['c'], build.COLOR)
        for key, art in fm['f'].items():
            race, _, cls = key.partition('.')
            self.assertIn(cls, races[race]['can'], key)
            self.assertEqual(art, f'{cls}-{race}', key)
            self.assertTrue(os.path.isfile(os.path.join(ROOT, 'assets', 'art', art + '-face.webp')), art)
        self.assertEqual(fm['f']['orc.rogue'], 'rogue-orc')
        self.assertNotIn('undead.rogue', fm['f'])
        for cls, by in fm['k'].items():   # the class face of a side shows a race of that side
            self.assertEqual(set(by), {'alliance', 'horde'}, cls)
            for side, art in by.items():
                c, _, race = art.partition('-')
                self.assertEqual((c, fm['r'][race]), (cls, side), art)
                self.assertTrue(os.path.isfile(os.path.join(ROOT, 'assets', 'art', art + '-face.webp')), art)

    def test_script(self):
        js = read(JS)
        self.assertNotIn('face(h.cls', js)   # the side portrait (best race of the side) is not the hero's face
        self.assertIn('heroFace(h, 30)', js)
        self.assertIn("heroFace(h, 96, 'mh-face')", js)
        self.assertIn('const meta = heroMeta(h);', js)
        self.assertIn('face(c, d.f || pre(c))', js)   # the class tiles before a choice: the mixed set (build.PRE_SIDE)

    @unittest.skipUnless(shutil.which('node'), 'node not found')
    def test_render(self):
        js = read(JS)
        part = lambda a, b: js[js.index(a):js.index(b, js.index(a))]   # noqa: E731
        code = part('  const FM = ', '  const bestOf')
        races = build.parse_races(read(os.path.join(ROOT, 'index.src.html')))
        D = json.loads(read(os.path.join(ROOT, 'assets', 'hero', 'ru.json')))
        pairs = [[r['id'], c, D['sr'][c][0][0]] for r in races for c in r['can']]
        cases = pairs + [['', 'rogue', 'dps'], ['undead', 'rogue', 'x'], ['xx', 'mage', 'heal']]
        prog = (f"const ROOT='./', PV='?v=1', D={json.dumps(D, ensure_ascii=False)};\n"
                r"const fill = (s, o) => s.replace(/%(\w)/g, (m, k) => (k in o ? o[k] : m)), specIx = h => D.sid[h.cls].indexOf(h.spec);" "\n"
                f"{code}\n"
                f"console.log(JSON.stringify({json.dumps(cases)}.map(([race, cls, role]) => {{ const h = {{race, cls, role, spec: D.sid[cls][0], lvl: 20}};"
                " return [heroFace(h, 30), heroMeta(h)]; })));")
        r = subprocess.run(['node', '-e', prog], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        sides = build.race_sides()
        own = 0
        self.assertEqual(len(pairs), 56)
        for (race, cls, _), (html, meta) in zip(pairs, out[:len(pairs)]):
            m = re.search(r'<img src="\./assets/art/(\w+)-(\w+)-face\.webp\?v=1"', html)
            self.assertTrue(m, (race, cls, html))   # a real pair never gets the grey badge
            self.assertEqual(m.group(1), cls, (race, cls))
            self.assertEqual(sides[m.group(2)], sides[race], (race, cls, html))   # never a face of the other side
            if m.group(2) == race:
                own += 1
                self.assertTrue(meta.startswith(D['rn'][race] + ' · '), (race, cls, meta))
            else:   # a face of another race: the caption names the side, the race name is not next to it
                self.assertIn(f'data-side="{sides[race]}"', html)
                self.assertNotIn(D['rn'][race], meta, (race, cls, meta))
                self.assertTrue(meta.startswith(D['fn'][sides[race]] + ' · '), (race, cls, meta))
        self.assertEqual(own, len(build.pair_faces()))
        got = dict(zip([f'{r}.{c}' for r, c, _ in pairs], [h for h, _ in out]))
        self.assertIn('assets/art/rogue-orc-face.webp?v=1', got['orc.rogue'])
        self.assertIn('assets/art/rogue-orc-face.webp?v=1', got['undead.rogue'])   # Forsaken rogue: the Horde rogue face
        self.assertIn('assets/art/mage-gnome-face.webp?v=1', got['human.mage'])
        self.assertIn('assets/art/warrior-human-face.webp?v=1', got['skyA.warrior'])
        self.assertIn('assets/art/shaman-orc-face.webp?v=1', got['tauren.shaman'])
        for html, ico, col in ((out[-3][0], 'dps', 'rogue'), (out[-1][0], 'heal', 'mage')):   # no race known: the badge
            self.assertNotIn('<img', html)
            self.assertIn(f'#i-{ico}', html)
            self.assertIn(f'--cc:{build.COLOR[col]}', html)
        self.assertIn('rogue-orc-face', out[-2][0])

    def test_all_pages(self):
        v = re.search(r'assets/hero/hero\.js\?v=(\w+)', read(os.path.join(ROOT, 'index.html'))).group(1)
        n = {l: 0 for l in LANGS}
        for d, dirs, fs in os.walk(ROOT):
            dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules', 'tools')]
            for f in fs:
                if not f.endswith('.html') or f.endswith('.src.html'):
                    continue
                p = os.path.join(d, f)
                html = read(p)
                m = re.search(r'assets/hero/hero\.js\?v=(\w+)"[^>]*data-data="[^"]*assets/hero/(\w+)\.json', html)
                if not m:
                    continue
                top = os.path.relpath(p, ROOT).split(os.sep)[0]
                lang = top if top in LANGS else 'ru'
                self.assertEqual(m.group(1), v, p)
                self.assertEqual(m.group(2), lang, p)
                n[lang] += 1
        for lang in LANGS:
            self.assertGreater(n[lang], 0, lang)
        print(f'hero.js pages: {n}')


if __name__ == '__main__':
    r = unittest.main(exit=False, verbosity=0).result
    print('OK' if r.wasSuccessful() else 'FAIL')
    sys.exit(0 if r.wasSuccessful() else 1)
