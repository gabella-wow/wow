"""Сторож «выбрано → показано»: раса и фракция игрока главнее времени суток и «Альянс по умолчанию».
1) GabellaPor (build.por_js) в node: 9 классов × Орда/Альянс × любое время суток → сторона расы героя, портрет по BEST этой стороны.
2) Руками выбранная сторона (gabella-side) главнее времени суток, но живёт только для своего героя.
3) Страницы, у которых была своя сторона «Альянс» по умолчанию, берут её у GabellaPor.fac().
Запуск: python tests/test_faction.py"""
import json, os, re, subprocess, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import build  # noqa: E402

HARNESS = r'''
const store = {}, attrs = {};
global.localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); } };
global.document = { documentElement: { getAttribute: k => attrs[k] || null }, addEventListener() {}, querySelectorAll: () => [] };
global.addEventListener = () => {}; global.dispatchEvent = () => {}; global.Event = function () {};
global.window = global;
const cases = JSON.parse(process.argv[1]), out = [];
eval(process.argv[2].replace(/^<script>/, '').replace(/<\/script>\s*$/, ''));
for (const c of cases) {
  for (const k of Object.keys(store)) delete store[k];
  for (const k of Object.keys(attrs)) delete attrs[k];
  if (c.me) store['gabella-wf-me'] = JSON.stringify(c.me);
  if (c.side) store['gabella-side'] = JSON.stringify(c.side);
  if (c.tod) attrs['data-tod'] = c.tod;
  out.push({ fac: GabellaPor.fac(), id: GabellaPor.id(c.cls), pre: GabellaPor.pre ? GabellaPor.pre(c.cls) : null });
}
console.log(JSON.stringify(out));
'''


def run(cases):
    r = subprocess.run(['node', '-e', HARNESS, json.dumps(cases), build.por_js()], capture_output=True, text=True, encoding='utf-8')
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def read(*p):
    return open(os.path.join(ROOT, *p), encoding='utf-8').read()


class Porter(unittest.TestCase):
    def test_race_beats_time_of_day_for_every_class(self):
        sides, por = build.race_sides(), build.portraits()
        races = {'alliance': 'human', 'horde': 'undead'}
        cases = [{'me': {'race': races[f], 'cls': c}, 'cls': c, 'tod': t}
                 for c in por for f in races for t in ('dawn', 'day', 'dusk', 'night')]
        self.assertEqual(len(cases), 9 * 2 * 4)
        for case, got in zip(cases, run(cases)):
            want = sides[case['me']['race']]
            self.assertEqual(got['fac'], want, case)
            self.assertEqual(got['id'], por[case['cls']][want], case)

    def test_hand_side_beats_tod_but_only_for_its_hero(self):
        hero = {'race': 'undead', 'cls': 'rogue'}
        got = run([{'me': hero, 'cls': 'rogue', 'tod': 'day', 'side': {'f': 'alliance', 'h': 'undead.rogue'}},
                   {'me': hero, 'cls': 'rogue', 'tod': 'day', 'side': {'f': 'alliance', 'h': 'human.rogue'}},
                   {'cls': 'rogue', 'tod': 'day', 'side': {'f': 'horde', 'h': ''}}])
        self.assertEqual([g['fac'] for g in got], ['alliance', 'horde', 'horde'])


class Pages(unittest.TestCase):
    """Источники страниц: сторона не зашита «Альянсом», её отдаёт GabellaPor.fac() (игрок, потом время суток)."""

    def test_guide_tabs_open_the_players_side(self):
        js = read('guide.src.html')
        self.assertTrue('sideTab' in js, 'вкладки Альянс/Орда открываются на стороне игрока')

    def test_raid_frames_start_on_the_players_side(self):
        self.assertFalse(re.search(r"const R = \{ f: 'alliance'", read('tools.src.html')), 'рамки стартуют с Альянса')

    def test_picker_choice_is_remembered_as_the_side(self):
        src = read('tools.src.html')
        self.assertTrue('GabellaPor.set(' in src, 'выбор расы в подборщике запоминается как сторона')

    def test_play_side_default_is_the_players(self):
        self.assertFalse("{ fac: 'alliance', timers" in read('build_guides.py'), '/play: сторона по умолчанию Альянс')

    def test_best_race_share_falls_back_to_the_players_side(self):
        src = read('build_guides.py')
        bad = re.search(r"mine \? HC\.rf\[mine\.race\] : 'alliance'", src)
        self.assertFalse(bad, 'Поделиться: сторона по умолчанию Альянс')


    def test_mixed_tiles_before_a_hero(self):
        """No hero and no hand-picked side: the class tiles of the hero sheet take build.PRE_SIDE (both sides at any time
        of day, 03.11 «all Horde faces at night»); a hero or a hand-picked side: its side for every class."""
        self.assertTrue(build.PRE_SIDE)
        self.assertEqual(set(build.PRE_SIDE), set(build.portraits()))
        self.assertEqual(set(build.PRE_SIDE.values()), {'alliance', 'horde'})
        cases = [{'cls': c, 'tod': t} for c in build.PRE_SIDE for t in ('day', 'night')]
        for case, got in zip(cases, run(cases)):
            self.assertEqual(got['pre'], build.PRE_SIDE[case['cls']], case)
        got = run([{'me': {'race': 'orc', 'cls': 'warrior'}, 'cls': 'paladin', 'tod': 'day'},
                   {'cls': 'paladin', 'tod': 'day', 'side': {'f': 'horde', 'h': ''}}])
        self.assertEqual([g['pre'] for g in got], ['horde', 'horde'])

if __name__ == '__main__':
    unittest.main()
