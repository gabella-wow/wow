"""Second screen (play/): the portrait of the character matches the race and the class.
1) In every language the face map P.face has only keys "<race>.<class>" of a pair the race can play, and each points to
   assets/art/<class>-<race>-face.webp that exists: no bare class portrait (rogue-face is a Forsaken), no race art.
2) No pair drawn: P.kf gives the class face of the race's side (build.side_faces), never the other side or the bare
   <class>-face; the caption then names the class alone (the side is in the line below), not the race (03.11: a grey
   circle stood there for 38 of 56 pairs). The old journey portrait by class (<class>-600) is gone.
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
            self.assertNotIn('undead.rogue', face, pre)               # no Forsaken rogue drawn: not in the pair map
            P = json.JSONDecoder().raw_decode(page(pre)[page(pre).index('const P = ') + len('const P = '):])[0]
            self.assertEqual(P['kf'], build.side_faces(), pre)
            for r in races.values():   # every real pair has a face of its own side
                for c in r['can']:
                    art = face.get(f"{r['id']}.{c}") or P['kf'][c][P['racef'][r['id']]]
                    self.assertEqual(build.race_sides()[art.partition('-')[2]], r['f'], (pre, r['id'], c, art))

    def test_script_uses_pair(self):
        for pre in LANGS:
            html = page(pre)
            self.assertIn("own = P.face[m.race + '.' + cls] || ''", html, pre)
            self.assertIn("P.kf[cls][P.racef[m.race]]", html, pre)
            self.assertIn("(kf ? P.cn[cls] : [P.rn[m.race], P.cn[cls]]", html, pre)   # a face of another race: the class, not the race
            self.assertNotIn('P.face[m.race] ', html, pre)
            self.assertIsNone(re.search(r"me\.cls\}-600", html), pre)


if __name__ == '__main__':
    r = unittest.main(exit=False, verbosity=0).result
    print('OK' if r.wasSuccessful() else 'FAIL')
    sys.exit(0 if r.wasSuccessful() else 1)
