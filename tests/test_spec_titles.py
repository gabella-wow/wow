"""Гиды спеков и «Лучшая раса» под запросы (NEXT-WAVE 01.11, п.2 и п.6), по собранным страницам (после python build.py):
  * 27 спеков × 9 языков = 243 страницы guides/spec-*: title ≤ 60 и с WoW Forever, все 243 разные, h1 «Frost Mage Guide»,
    description ≤ 160 со словами build / talents / gear на языке страницы; canonical и hreflang всех языков + x-default,
    каждая альтернатива ведёт на собранную страницу того же спека, и та ссылается обратно;
  * best-race: h2 с якорем на каждый класс («Best race for Warlock», #warlock), чипы классов ведут на эти якоря;
  * ссылки на якоря с тир-листа, builds-<класс> и гидов спеков открывают существующий id; title страниц классов с «Best Race».
Запуск: python tests/test_spec_titles.py"""
import html as H, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from langs import HREFLANG, LANGS  # noqa: E402
from content.spec_cheats import CHEATS  # noqa: E402

SITE = 'https://gabella.site/wow/'
CLASSES = list(dict.fromkeys(c for c, _ in CHEATS))
# the words a searcher types, in the language of the page (description)
WORDS = {'ru': ('билд', 'таланты', 'снаряжение'), 'en': ('build', 'talents', 'gear'), 'uk': ('білд', 'таланти', 'спорядження'),
         'de': ('Build', 'Talente', 'Ausrüstung'), 'fr': ('build', 'talents', 'équipement'), 'es': ('build', 'talentos', 'equipo'),
         'pt': ('build', 'talentos', 'equipamento'), 'it': ('build', 'talenti', 'equipaggiamento'), 'pl': ('build', 'talenty', 'ekwipunek')}
BEST_RACE = {'ru': 'лучшая раса', 'en': 'Best Race', 'uk': 'найкраща раса', 'de': 'bestes Volk', 'fr': 'meilleure race',
             'es': 'mejor raza', 'pt': 'melhor raça', 'it': 'razza migliore', 'pl': 'najlepsza rasa'}
_cache = {}


def sub(lang, path):
    return ('' if lang == 'ru' else lang + '/') + path


def page(rel):
    if rel not in _cache:
        with open(os.path.join(ROOT, rel, 'index.html'), encoding='utf-8') as f:
            _cache[rel] = f.read()
    return _cache[rel]


def one(rx, text, what):
    m = re.findall(rx, text, re.S)
    assert len(m) == 1, (what, len(m))
    return H.unescape(re.sub(r'<[^>]+>', '', m[0])).strip()


def ids(text):
    return set(re.findall(r'\sid="([^"]+)"', text))


def test_spec_titles():
    seen, n = {}, 0
    for lang in LANGS:
        h1s = set()
        for cid, spec in CHEATS:
            rel = sub(lang, f'guides/spec-{cid}-{spec}/')
            t = page(rel)
            title = one(r'<title>(.*?)</title>', t, rel)
            assert len(title) <= 60 and 'WoW Forever' in title, (rel, len(title), title)
            assert 'cheat sheet' not in title.lower() and 'шпора' not in title.lower(), (rel, title)
            assert title not in seen, ('title twice', title, rel, seen.get(title))
            seen[title] = rel
            og = re.search(r'<meta property="og:title" content="([^"]*)"', t)
            assert og and H.unescape(og[1]) == title, (rel, og and og[1])
            h1 = one(r'<h1[^>]*>(.*?)</h1>', t, rel)
            assert h1 and h1 not in h1s and len(h1) <= 45, (rel, h1)
            h1s.add(h1)
            if lang == 'en':
                assert h1.endswith(' Guide'), h1
            desc = H.unescape(re.search(r'<meta name="description" content="([^"]*)"', t)[1])
            assert 100 <= len(desc) <= 160 and 'WoW Forever' in desc, (rel, len(desc), desc)
            assert all(w in desc for w in WORDS[lang]), (rel, desc)
            n += 1
    assert n == 27 * len(LANGS) == len(seen), (n, len(seen))
    print(f'titles: {n} pages, {len(seen)} unique, longest {max(map(len, seen))}')


def test_spec_hreflang():
    for cid, spec in CHEATS:
        path = f'guides/spec-{cid}-{spec}/'
        want = {HREFLANG[l]: SITE + sub(l, path) for l in LANGS} | {'x-default': SITE + path}
        for lang in LANGS:
            t = page(sub(lang, path))
            got = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', t))
            assert got == want, (lang, path, set(got.items()) ^ set(want.items()))
            canon = re.search(r'<link rel="canonical" href="([^"]+)"', t)
            assert canon and canon[1] == SITE + sub(lang, path), (lang, path, canon and canon[1])
            assert f'<html lang="{HREFLANG[lang]}"' in t, (lang, path)
            for href in want.values():                             # every alternative is a built page of the same spec
                assert os.path.exists(os.path.join(ROOT, href[len(SITE):], 'index.html')), href
    sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    for cid, spec in CHEATS:
        for lang in LANGS:
            assert f'<loc>{SITE + sub(lang, f"guides/spec-{cid}-{spec}/")}</loc>' in sm, (lang, cid, spec)
    print(f'hreflang: {27 * len(LANGS)} pages, {len(LANGS)} + x-default each, sitemap has all')


def test_best_race_anchors():
    for lang in LANGS:
        rel = sub(lang, 'guides/best-race/')
        t = page(rel)
        for cid in CLASSES:
            m = re.search(rf'<section class="frame gsec" id="{cid}" data-toc="classes"><h2>([^<]+)</h2>', t)
            assert m, (rel, cid)
            assert re.search(rf'<a class="spp" href="#{cid}"', t), (rel, cid, 'chip')   # the class plate (build.spec_plate)
        if lang == 'en':
            assert '<h2>Best race for Warlock</h2>' in t and '<h2>Best race for Mage</h2>' in t
        assert t.count('data-toc="classes"') == len(CLASSES), rel
        assert '<a href="#classes">' in t, (rel, 'toc entry')
    print(f'best-race: {len(CLASSES)} h2 anchors × {len(LANGS)} languages')


def resolve(src_rel, href):
    """A relative href with #anchor from the page src_rel -> (page dir, anchor)."""
    path, _, anchor = href.partition('#')
    import posixpath
    return posixpath.normpath(posixpath.join(src_rel, path)) + '/', anchor


def test_links_to_anchors():
    for lang in LANGS:
        target = sub(lang, 'guides/best-race/')
        have = ids(page(target))
        checked = set()
        sources = [sub(lang, 'guides/tier-list/')] + [sub(lang, f'guides/builds-{c}/') for c in CLASSES] + \
                  [sub(lang, f'guides/spec-{c}-{s}/') for c, s in CHEATS]
        for src in sources:
            hrefs = [h for h in re.findall(r'href="([^"]*best-race/#[^"]+)"', page(src))]
            assert hrefs, (src, 'no link to a best-race anchor')
            for h in hrefs:
                d, a = resolve(src, h)
                assert d == target and a in have, (src, h, d, a)
                checked.add((src.split('/guides/')[-1] if '/guides/' in src else src, a))
        tier = page(sub(lang, 'guides/tier-list/'))
        assert {a for a in re.findall(r'href="\.\./best-race/#([a-z]+)"', tier)} == set(CLASSES), (lang, 'tier-list')
        for c in CLASSES:
            assert f'best-race/#{c}"' in page(sub(lang, f'guides/builds-{c}/')), (lang, c, 'builds')
    print(f'anchors: tier-list, 9 builds and 27 specs link the best-race sections in {len(LANGS)} languages')


def test_class_titles_best_race():
    for lang in LANGS:
        for c in CLASSES:
            rel = sub(lang, f'classes/{c}/')
            title = one(r'<title>(.*?)</title>', page(rel), rel)
            assert len(title) <= 60 and BEST_RACE[lang].lower() in title.lower(), (rel, title)
    print(f'class pages: «best race» in {len(CLASSES) * len(LANGS)} titles')


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
