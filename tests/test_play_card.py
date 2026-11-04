"""Second screen (play/): the card «My class at level N» (content/play_card.py, JS play renderCard).
1) Every link of the card (talents, abilities, gear, class guide, dungeon pages) is a built page of that language and its anchor exists.
2) The data is the repo's data, not written by hand: per class and spec the talents are the order the builds page draws (talents.py),
   the abilities are the «Level / What to take» rows of the class leveling guide, the gear items are data/gear30.json items of that spec
   with their own level (16–30) and name, and the specs with holes (items marked "pick") get no list but the «no data yet» line.
3) No talent or item name is written into the page script or the card module.
Run: python tests/test_play_card.py (after python build.py)"""
import html, json, os, re, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import langs  # noqa: E402
import talents  # noqa: E402
from content import class_guides, spec_builds  # noqa: E402
from content.hero import SPEC_IDS  # noqa: E402
import gear_planner as GP  # noqa: E402

LANGS = {'ru': '', 'en': 'en/', 'uk': 'uk/', 'de': 'de/', 'fr': 'fr/', 'es': 'es/', 'pt': 'pt/', 'it': 'it/', 'pl': 'pl/'}
GEAR = json.load(open(os.path.join(ROOT, 'data', 'gear30.json'), encoding='utf-8'))


def read(*p):
    with open(os.path.join(ROOT, *p), encoding='utf-8') as f:
        return f.read()


def card(pre):
    html = read(pre, 'play', 'index.html')
    i = html.index('const P = ') + len('const P = ')
    return json.JSONDecoder().raw_decode(html[i:])[0]['card']


def exists(pre, url):
    """The page of a card link (relative to the language home) is built and has the anchor."""
    path, _, anchor = url.partition('#')
    f = os.path.join(ROOT, pre, path, 'index.html')
    if not os.path.isfile(f):
        return False
    return not anchor or f'id="{anchor}"' in read(f)


def links(c):
    out = list(c['dg'].values())
    for cid, x in c['cls'].items():
        out += [x['abU'], f'classes/{cid}/'] + [u for sp in x['sp'].values() for u in (sp['tU'], sp['gU'])]
    return [u for u in out if u]


class PlayCard(unittest.TestCase):
    def test_links_exist(self):
        for lang, pre in LANGS.items():
            c = card(pre)
            urls = links(c)
            self.assertGreater(len(urls), 9 * 7, lang)   # 9 classes × (abilities, class, 3 specs × talents and gear) + dungeons
            for u in urls:
                self.assertTrue(exists(pre, u), (lang, u))

    def test_abilities_from_class_guides(self):
        official = {l: {v[l] for v in langs.NAMES.values() if v.get(l)} for l in langs.NAMED}
        for lang, pre in LANGS.items():
            c = card(pre)
            for g in class_guides.CLASS_GUIDES:
                cid = g['slug'].split('-', 1)[1]
                sec = next(s for s in g['sections'] if s['id'] == 'abilities')
                rows = next(b for k, b in sec['blocks'] if k == 'table')['rows']
                got = c['cls'][cid]['ab']
                self.assertEqual([r[0] for r in got], [int(r[0]) for r in rows], (lang, cid))
                shown = html.unescape(re.sub(r'<[^>]+>', '', read(pre, 'guides', f'leveling-{cid}', 'index.html')))
                for r in got:   # the same words as the class leveling page of this language shows (its first mention may add «(English)»)
                    for part in re.split(r'[,;] ', r[1]) + [r[2]]:   # a whole script string that is a game name: its official name (build.js_names)
                        self.assertTrue(part in shown or part in official.get(lang, ()), (lang, cid, part))
                if lang in ('en', 'uk'):
                    self.assertEqual([r[1] for r in got], [r[1][lang] for r in rows], (lang, cid))

    def test_talents_from_builds_order(self):
        builds = {g['slug']: g for g in spec_builds.SPEC_BUILDS}
        for lang, pre in LANGS.items():
            c = card(pre)
            for cid, specs in SPEC_IDS.items():
                data = talents.load(cid)
                for spec in specs:
                    sp = c['cls'][cid]['sp'][spec]
                    b = talents.leveling(cid, spec, data)
                    if b:
                        steps, kind = b['steps'], 'lv'
                    else:
                        sec = next(s for s in builds[f'builds-{cid}']['sections'] if s['id'] == spec)
                        rows = [(r[0], r[1]) for r in next(x for k, x in sec['blocks'] if k == 'table' and x['head'] is spec_builds.H_TAL)['rows']]
                        steps, kind = talents.plan(data, rows, talents.FIRST_LEVEL - talents.perk(data, rows))[1], 'gen'
                    self.assertEqual(sp['k'], kind, (lang, cid, spec))
                    self.assertEqual([s[:2] for s in sp['t']], [[a, z] for _, _, a, z in steps], (lang, cid, spec))
                    self.assertEqual([s[2] for s in sp['t']], [talents.tname(t, lang) if t else '' for t, _, _, _ in steps], (lang, cid, spec))
                    self.assertEqual(sp['top'], steps[-1][3], (lang, cid, spec))
                    self.assertIn(sp['tU'].split('#')[1], (spec, f'{spec}-leveling'), (lang, cid, spec))

    def test_gear_from_gear30(self):
        holes = {k for k, v in GEAR['specs'].items() if any(e.get('pick') for e in v)}
        self.assertEqual(len(holes), 7, holes)
        for lang, pre in LANGS.items():
            c = card(pre)
            for cid, specs in SPEC_IDS.items():
                for spec in specs:
                    key, g = f'{cid}-{spec}', c['cls'][cid]['sp'][spec]['g']
                    if key in holes:
                        self.assertIsNone(g, (lang, key))
                        continue
                    ids = {str(e['id']) for e in GEAR['specs'][key]}
                    self.assertTrue(g, (lang, key))
                    for e in g:
                        iid = str(e[0])
                        self.assertIn(iid, ids, (lang, key, iid))
                        it, mine = GEAR['items'][iid], c['it'][iid]
                        self.assertEqual(mine[0], it['lvl'], (lang, iid))
                        self.assertTrue(16 <= mine[0] <= 30, (lang, iid))
                        self.assertEqual(mine[2], it['names'].get(lang) or it['names']['en'], (lang, iid))
            self.assertNotIn('gearHole', c['tx'], lang)                      # no «no data yet»: the planner instead
            self.assertEqual(c['tx']['gearGo'], GP.TX['go'][lang], lang)

    def test_no_names_in_code(self):
        code = read('build_guides.py')
        i = code.index("JS['play'] = r'''")
        play = code[i:code.index("'''", i + 20)] + read('content', 'play_card.py')   # the page script and the card module
        for it in GEAR['items'].values():
            for n in {it['names']['en'], it['names'].get('ru', '')} - {''}:
                self.assertNotIn(n, play, n)
        for cid in SPEC_IDS:
            for tr in talents.load(cid)['trees']:
                for t in tr['talents']:
                    for n in {t['n'].get('en', ''), t['n'].get('ru', '')} - {''}:
                        self.assertIsNone(re.search(r'\b' + re.escape(n) + r'\b', play), (cid, n))


if __name__ == '__main__':
    r = unittest.main(exit=False, verbosity=0).result
    print('OK' if r.wasSuccessful() else 'FAIL')
    sys.exit(0 if r.wasSuccessful() else 1)
