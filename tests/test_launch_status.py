"""Карточка дня старта «Серверы и очередь» (data/launch.json, build.launch_card). Запуск: python tests/test_launch_status.py
Флаг выключен: карточки нет ни на главной, ни в шапке «Дня старта» (9 языков). Флаг включён: одна карточка на каждой из этих
страниц, первой строкой над кнопками героя, ведёт на guides/server-status/ своего языка; в окне from–until видна, вне окна скрыта."""
import json, os, posixpath, re, subprocess, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import build, build_guides, langs  # noqa: E402



def read(*p):
    with open(os.path.join(ROOT, *p), encoding='utf-8') as f:
        return f.read()


SRC, TPL = read('index.src.html'), read('guide.src.html')
BASE_CSS = SRC[SRC.index('<style>') + 7:SRC.index('</style>')].strip('\n')
S0 = SRC.index('<svg width="0" height="0"')
SPRITE = SRC[S0:SRC.index('</svg>', S0) + 6]
LD = next(g for g in build_guides.GUIDES if g['slug'] == 'launch-day')
CARD = re.compile(r'<a class="lstat" href="([^"]+)" data-from="([^"]+)" data-until="([^"]+)" hidden><span class="lst-t"><b>([^<]+)</b><span>([^<]+)</span></span>')
ON = {'status_card': True, 'from': '2026-11-04T16:00:00Z', 'until': '2026-11-08T22:00:00Z'}


def pages(cfg):
    """{(lang, page): html} for the home and the Launch day guide of every language, built with this launch config."""
    old = build.LAUNCH
    build.LAUNCH = cfg
    try:
        out = {}
        for lang in langs.ALL:
            out[lang, ''] = build.build_home(lang, SRC)[1]
            out[lang, 'guides/launch-day/'] = build_guides.build_page(LD, lang, TPL, BASE_CSS, SPRITE, SRC)[1]
        return out
    finally:
        build.LAUNCH = old


class LaunchStatus(unittest.TestCase):
    def test_off_no_card(self):
        for (lang, page), html in pages({**ON, 'status_card': False}).items():
            self.assertNotIn('class="lstat"', html, (lang, page))
            self.assertNotIn('@@LAUNCH@@', html, (lang, page))

    def test_on_card_leads_to_server_status(self):
        for (lang, page), html in pages(ON).items():
            cards = CARD.findall(html)
            self.assertEqual(len(cards), 1, (lang, page))
            href, frm, until, title, sub = cards[0]
            here = build.page_dir(lang, page)
            target = posixpath.normpath(posixpath.join(here, href)) + '/'
            self.assertEqual(target, build.page_dir(lang, 'guides/server-status/'), (lang, page, href))
            self.assertTrue(os.path.isfile(os.path.join(ROOT, target, 'index.html')), target)   # the built page it opens
            self.assertEqual((title, sub), tuple(build.esc(x) for x in build.LAUNCH_TX[lang]), (lang, page))
            self.assertEqual((frm, until), (ON['from'], ON['until']))
            if lang not in ('ru', 'uk'):
                self.assertFalse(re.search('[А-Яа-яЁёЇїІіЄєҐґ]', title + sub), (lang, title, sub))
            if page == '':   # the first screen on a phone: above the six goal buttons of the hero
                self.assertLess(html.index('class="lstat"'), html.index('class="htasks"'), lang)

    def test_built_pages_follow_the_config(self):
        on = bool(build.LAUNCH.get('status_card'))
        for lang in langs.ALL:
            for page in ('', 'guides/launch-day/'):
                p = build.page_dir(lang, page) + 'index.html'
                self.assertEqual('class="lstat"' in read(p), on, (p, 'run python build.py'))

    def test_shown_only_inside_the_window(self):
        js = ("const res = {};\nfor (const now of process.argv.slice(1)) {\n"
              "  Date.now = () => Date.parse(now);\n"
              f"  const a = {{ hidden: true, dataset: {{ from: '{ON['from']}', until: '{ON['until']}' }} }};\n"
              "  const document = { currentScript: { previousElementSibling: a } };\n"
              f"  {build.LAUNCH_JS[8:-9]}\n"
              "  res[now] = a.hidden;\n}\nconsole.log(JSON.stringify(res));")
        times = {'2026-11-04T15:59:00Z': True, '2026-11-04T16:00:00Z': False, '2026-11-04T23:00:00Z': False,
                 '2026-11-08T21:59:00Z': False, '2026-11-08T22:00:00Z': True, '2026-11-01T12:00:00Z': True}
        out = subprocess.run(['node', '-e', js, '--', *times], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(out.stdout), times)

    def test_config_file(self):
        cfg = json.loads(read('data', 'launch.json'))
        self.assertIsInstance(cfg['status_card'], bool)
        self.assertLess(cfg['from'], cfg['until'])
        self.assertTrue(all(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', cfg[k]) for k in ('from', 'until')))
        self.assertEqual(set(build.LAUNCH_TX), set(langs.ALL))


if __name__ == '__main__':
    unittest.main(verbosity=1)
