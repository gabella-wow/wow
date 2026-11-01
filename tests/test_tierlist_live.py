"""Тир-лист «по бете» → «по живой игре»: один переключатель data/tierlist.json (NEXT-WAVE 01.11, п.5).
  * title ≤60 с «WoW Forever», description ≤160 на 9 языках при любой дате 10.2026–01.2027 и обоих статусах;
  * тестовая копия данных (WF_TIERLIST, без правки шаблонов): beta → live меняет на всех 9 языках title, description,
    строку фактов и хвост лида первого экрана, совет «Как читать» и подпись плитки; дата в каждом из них;
    заметка «что изменилось» появляется блоком id="changes" первым разделом и в оглавлении, без заметок блока нет;
    у live нет непереведённых строк (langs.MISSING);
  * собранные страницы (после python build.py) показывают статус и дату из data/tierlist.json.
Запуск: python tests/test_tierlist_live.py"""
import datetime, html as H, json, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from content import tierlist_live as TL  # noqa: E402

ALL = TL.ALL
NOTE = {'ru': 'Пример: Охотник в PvE — A → S.', 'en': 'Example: Hunter in PvE — A → S.', 'uk': 'Приклад: Мисливець у PvE — A → S.',
        'de': 'Beispiel: Jäger im PvE — A → S.', 'fr': 'Exemple : Chasseur en JcE — A → S.', 'es': 'Ejemplo: Cazador en JcE — A → S.',
        'pt': 'Exemplo: Caçador no PvE — A → S.', 'it': 'Esempio: Cacciatore in PvE — A → S.', 'pl': 'Przykład: Hunter w PvE — A → S.'}

# what one build of the tier list page gives in every language (run with WF_TIERLIST=<copy>)
PROBE = r'''
import json, os, re, sys
sys.argv = sys.argv[:1] + ['--list']
sys.path.insert(0, os.getcwd())
import build_guides as BG, seo, langs
from content.guides import GUIDES
src = open('index.src.html', encoding='utf-8').read()
tpl = open('guide.src.html', encoding='utf-8').read()
base_css = src[src.index('<style>') + 7:src.index('</style>')].strip('\n')
s0 = src.index('<svg width="0" height="0"'); sprite = src[s0:src.index('</svg>', s0) + 6]
g = next(x for x in GUIDES if x['slug'] == 'tier-list')
meta = seo.page_meta()['guides/tier-list/']
out = {}
for lang in langs.LANGS:
    _, html, missing = BG.build_page(g, lang, tpl, base_css, sprite, src)
    out[lang] = {'title': meta[lang][0], 'desc': meta[lang][1], 'html': html, 'missing': missing,
                 'tile': g['tile'][lang], 'unknown': sorted(set(langs.MISSING.get(lang, [])))}
sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps(out, ensure_ascii=False))
'''


def probe(status):
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, 'tierlist.json')
        json.dump(status, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        r = subprocess.run([sys.executable, '-c', PROBE], cwd=ROOT, capture_output=True, text=True, encoding='utf-8',
                           env=dict(os.environ, WF_TIERLIST=p, PYTHONUTF8='1'))
    assert r.returncode == 0, r.stderr[-3000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def first_screen(html):
    """h1 .. the facts line: what a reader sees before scrolling."""
    i = html.index('<h1')
    return html[i:html.index('</p>', html.index('<p class="gfacts">', i)) + 4]


def plain(s):
    return H.unescape(re.sub(r'<[^>]+>', '', s))


def test_lengths():
    d = datetime.date(2026, 10, 1)
    while d < datetime.date(2027, 2, 1):
        for src in TL.SOURCES:
            st = {'source': src, 'date': d.isoformat(), 'changes': []}
            title = TL.title(st)
            for l in ALL:
                assert len(title[l]) <= 60 and 'WoW Forever' in title[l], (l, len(title[l]), title[l])
            if src == 'live':
                desc = TL.meta(st)[1]
                assert all(len(desc[l]) <= 160 for l in ALL), [(l, len(desc[l])) for l in ALL if len(desc[l]) > 160]
        d += datetime.timedelta(days=1)
    print('title <=60 and description <=160: 9 languages, both sources, every date Oct 2026 - Jan 2027')


def test_switch():
    beta = probe({'source': 'beta', 'date': '2026-10-23', 'changes': []})
    live = probe({'source': 'live', 'date': '2026-11-06', 'changes': [{'date': '2026-11-06', 'text': NOTE}]})
    assert set(beta) == set(live) == set(ALL), (sorted(beta), sorted(live))
    for l in ALL:
        b, v = beta[l], live[l]
        assert not v['missing'] and not v['unknown'], (l, v['missing'][:3], v['unknown'][:3])
        bd, vd = TL.day('2026-10-23', l), TL.day('2026-11-06', l)
        # title: the mark and the date
        assert b['title'] == TL.TITLE[l].format(m=TL.SHORT['beta'][l], d=bd), (l, b['title'])
        assert v['title'] == TL.TITLE[l].format(m=TL.SHORT['live'][l], d=vd), (l, v['title'])
        assert b['desc'] != v['desc'] and vd in v['desc'], (l, v['desc'])
        # first screen: the facts line and the lead
        bs, vs = plain(first_screen(b['html'])), plain(first_screen(v['html']))
        assert TL.MARK['beta'][l].format(d=bd) in bs and TL.MARK['live'][l].format(d=vd) not in bs, (l, bs)
        assert TL.MARK['live'][l].format(d=vd) in vs and TL.MARK['beta'][l].format(d=bd) not in vs, (l, vs)
        assert TL.LEAD_TAIL_LIVE[l].format(d=vd) in vs, (l, vs)
        assert bs != vs, l
        # «Как читать», the tile
        assert TL.TIP_LIVE[l].format(d=vd) in plain(v['html']) and TL.TIP_LIVE[l].format(d=vd) not in plain(b['html']), l
        assert b['tile'] != v['tile'] and v['tile'] == TL.TILE_LIVE[l], (l, v['tile'])
        # «Что изменилось»: only with a note, the first section, in the contents
        assert 'id="changes"' not in b['html'] and 'href="#changes"' not in b['html'], l
        secs = re.findall(r'<section class="frame gsec" id="([\w-]+)"', v['html'])
        assert secs[0] == 'changes', (l, secs[:3])
        assert 'href="#changes"' in v['html'] and H.escape(NOTE[l]) in v['html'], l
        assert f'<time datetime="2026-11-06">{vd}</time>' in v['html'], l
        assert TL.CHANGES_H[l] in v['html'], l
    print(f'switch beta -> live on a test copy: title, description, first screen, tip, tile and the changes block differ in all {len(ALL)} languages')


def test_built():
    """The built pages follow data/tierlist.json (run after python build.py)."""
    st = TL.load()
    title, _ = TL.meta(st)
    for l in ALL:
        rel = ('' if l == 'ru' else l + '/') + 'guides/tier-list/index.html'
        html = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        assert f'<title>{H.escape(title[l], quote=True)}</title>' in html, (l, re.search(r'<title>(.*?)</title>', html)[1])
        assert TL.MARK[st['source']][l].format(d=TL.day(st['date'], l)) in plain(first_screen(html)), l
        assert ('id="changes"' in html) == bool(st.get('changes')), l
    print(f'built tier list: {st["source"]}, {st["date"]}, {len(st.get("changes", []))} notes, 9 languages')


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
