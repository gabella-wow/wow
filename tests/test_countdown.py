"""Отсчёт на главной (решение Р4): строки про резерв имён нет (убрана 02.11, чистка главной), у рейдов отсчёта нет. Запуск: python tests/test_countdown.py
Функция renderCountdown вырезается из собранной главной каждого языка и исполняется в node с замороженными часами (TZ=UTC)."""
import json, os, re, subprocess, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import langs

R1, R2 = '2026-10-27T17:00:00Z', '2026-10-27T20:00:00Z'   # резерв имён: Европа 17:00 UTC, Америка 20:00 UTC
REL = '2026-11-04T23:00:00Z'   # старт игры 15:00 PT = 23:00 UTC
RSV = "{ day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }"


def home(lang):
    p = os.path.join(ROOT, 'index.html' if lang == 'ru' else f'{lang}/index.html')
    return open(p, encoding='utf-8').read()


def render(html, lang, now):
    """HTML блока #cd и подпись датами, как их видит читатель в UTC в указанный момент."""
    fn = re.search(r'function renderCountdown\(\) \{.*?\n\}\n', html, re.S).group(0)
    js = (f"const Real = Date; const NOW = new Real('{now}'); globalThis.Date = class extends Real {{ constructor(...a) {{ super(...(a.length ? a : [NOW])); }} }};\n"
          f"let out = ''; const $ = () => ({{ set innerHTML(v) {{ out = v; }} }});\n"
          f"const document = {{ documentElement: {{ lang: '{lang}' }}, querySelectorAll: () => [] }};\n{fn}\nrenderCountdown();\n"
          f"const f = d => new Real(d).toLocaleString('{lang}', {RSV});\n"
          "console.log(JSON.stringify({ html: out, r1: f('" + R1 + "'), r2: f('" + R2 + "') }));")
    out = subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True, env=dict(os.environ, TZ='UTC'))
    return json.loads(out.stdout)


class Countdown(unittest.TestCase):
    def test_before_launch_shows_units_and_no_reserve_line(self):
        for lang in langs.ALL:
            h = home(lang)
            self.assertNotIn('r1 = new Date', h, lang)
            self.assertNotIn('hd-line', h, lang)
            r = render(h, lang, '2026-10-26T12:00:00Z')
            self.assertIn('class="units"', r['html'], lang)
            self.assertEqual(r['html'].count('class="u"'), 3, lang)
            self.assertNotIn(r['r1'], r['html'], lang)
            self.assertNotIn(r['r2'], r['html'], lang)

    def test_start_time_in_page_source(self):
        for lang in langs.ALL:
            self.assertIn(f"rel = new Date('{REL}')", home(lang), lang)

    def test_countdown_digits_follow_start_time(self):
        for lang in langs.ALL:
            h = home(lang)
            for now, dhm in (('2026-11-04T21:30:00Z', ('0', '01', '30')), ('2026-10-26T12:00:00Z', ('9', '11', '00'))):
                nums = re.findall(r'<div class="u"><b>(\d+)</b>', render(h, lang, now)['html'])
                self.assertEqual(tuple(nums), dhm, (lang, now))

    def test_raids_have_no_countdown(self):
        for lang in langs.ALL:
            for now in ('2026-11-20T12:00:00Z', '2026-12-08T12:00:00Z'):
                r = render(home(lang), lang, now)
                self.assertNotIn('class="units"', r['html'], (lang, now))
                self.assertNotIn('class="u"', r['html'], (lang, now))
                self.assertTrue(r['html'].startswith('<div class="what">'), (lang, now))   # только дата, текст на языке читателя


if __name__ == '__main__':
    unittest.main()
