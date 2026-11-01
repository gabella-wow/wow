"""The hero button of the top bar (assets/hero/hero.js) and the home card «Your <class>» show the face of the hero's own race and
class, as play/ does (tests/test_play_portrait.py):
1) the map /*FACES*/ in hero.js (build.pair_faces) has only keys "<race>.<class>" of a pair the race can play, each pointing to
   assets/art/<class>-<race>-face.webp that exists; the class colours are build.COLOR;
2) run in node, heroFace() gives the pair's picture, and with no pair drawn the class badge (colour + role icon), never
   another race (the reported case: an Undead Rogue got the Orc one);
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
        self.assertEqual(fm['c'], build.COLOR)
        for key, art in fm['f'].items():
            race, _, cls = key.partition('.')
            self.assertIn(cls, races[race]['can'], key)
            self.assertEqual(art, f'{cls}-{race}', key)
            self.assertTrue(os.path.isfile(os.path.join(ROOT, 'assets', 'art', art + '-face.webp')), art)
        self.assertEqual(fm['f']['orc.rogue'], 'rogue-orc')
        self.assertNotIn('undead.rogue', fm['f'])

    def test_script(self):
        js = read(JS)
        self.assertNotIn('face(h.cls', js)   # the side portrait (best race of the side) is not the hero's face
        self.assertIn('heroFace(h, 30)', js)
        self.assertIn("heroFace(h, 96, 'mh-face')", js)

    @unittest.skipUnless(shutil.which('node'), 'node not found')
    def test_render(self):
        js = read(JS)
        fm = js[js.index('const FM = '):js.index('\n', js.index('const FM = '))]
        fn = js[js.index('  function heroFace('):js.index('\n  }\n', js.index('  function heroFace(')) + 4]
        cases = [['orc', 'rogue', 'dps'], ['undead', 'rogue', 'dps'], ['human', 'mage', 'dps'], ['tauren', 'shaman', 'heal'],
                 ['tauren', 'druid', 'tank'], ['undead', 'rogue', 'x']]
        prog = (f"const ROOT='./', PV='?v=1';\n{fm}\n{fn}\n"
                f"console.log(JSON.stringify({json.dumps(cases)}.map(([race, cls, role]) => heroFace({{race, cls, role}}, 30))));")
        out = json.loads(subprocess.run(['node', '-e', prog], capture_output=True, text=True, check=True).stdout)
        orc, undead, human, tsham, tdru, bad = out
        self.assertIn('assets/art/rogue-orc-face.webp?v=1', orc)
        self.assertIn('assets/art/druid-tauren-face.webp?v=1', tdru)
        for html, ico, col in ((undead, 'dps', 'rogue'), (human, 'dps', 'mage'), (tsham, 'heal', 'shaman'), (bad, 'user', 'rogue')):
            self.assertNotIn('<img', html)
            self.assertIn(f'#i-{ico}', html)
            self.assertIn(f'--cc:{build.COLOR[col]}', html)

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
