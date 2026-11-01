"""Second screen (play/): the portrait of the character matches the race and the class.
1) In every language the face map P.face has only keys "<race>.<class>" of a pair the race can play, and each points to
   assets/art/<class>-<race>-face.webp that exists: no bare class portrait (rogue-face is a Forsaken), no race art.
2) The page script takes the face by the pair only (no fallback to the class or the race) and the old journey portrait
   by class (<class>-600) is gone.
Run: python tests/test_play_portrait.py (after python build.py)"""
import json, os, re, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import build  # noqa: E402

LANGS = ['', 'en/', 'uk/', 'de/', 'fr/', 'es/', 'pt/', 'it/', 'pl/']


def read(*p):
    with open(os.path.join(ROOT, *p), encoding='utf-8') as f:
        return f.read()


def page(pre):
    return read(pre, 'play', 'index.html')


def face_map(html):
    i = html.index('const P = ') + len('const P = ')
    return json.JSONDecoder().raw_decode(html[i:])[0]['face']


class PlayPortrait(unittest.TestCase):
    def test_pairs_only(self):
        races = {r['id']: r for r in build.parse_races(read('index.src.html'))}
        for pre in LANGS:
            face = face_map(page(pre))
            self.assertTrue(face, pre)
            for key, art in face.items():
                race, _, cls = key.partition('.')
                self.assertIn(race, races, (pre, key))
                self.assertIn(cls, races[race]['can'], (pre, key))
                self.assertEqual(art, f'{cls}-{race}', (pre, key))   # the picture of this race and class, nothing else
                self.assertTrue(os.path.isfile(os.path.join(ROOT, 'assets', 'art', art + '-face.webp')), (pre, art))
            self.assertEqual(face['orc.rogue'], 'rogue-orc', pre)   # the reported case: Orc Rogue showed a Forsaken
            self.assertNotIn('undead.rogue', face, pre)               # no Forsaken rogue drawn: badge, not the orc one

    def test_script_uses_pair(self):
        for pre in LANGS:
            html = page(pre)
            self.assertIn("P.face[m.race + '.' + cls] || ''", html, pre)
            self.assertNotIn('P.face[m.race] ', html, pre)
            self.assertIsNone(re.search(r"me\.cls\}-600", html), pre)


if __name__ == '__main__':
    r = unittest.main(exit=False, verbosity=0).result
    print('OK' if r.wasSuccessful() else 'FAIL')
    sys.exit(0 if r.wasSuccessful() else 1)
