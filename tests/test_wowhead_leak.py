"""Билд ведёт в наш калькулятор, Wowhead только сверка; ссылка на билд показывает класс и спек (NEXT-WAVE 01.11, п.3 и п.9).
По собранным страницам (после python build.py):
  * guides/builds-<класс>/ и talents/<класс>/ на 9 языках: ни одной кнопки (class="btn") на wowhead.com, у каждой ссылки на
    wowhead.com rel="nofollow noopener"; ссылка на калькулятор Wowhead только мелкой строкой «Сверить у Wowhead» (.tt-whc / .tt-whl);
  * у каждого блока билда главная кнопка .tt-go ведёт в talents/<класс>/#<код> с тем же кодом, что у блока (data-w), и стоит
    раньше строки Wowhead; код совпадает с кодом нашей таблицы талантов;
  * «Скопировать ссылку на билд» даёт t/<класс>-<спек>/#<код> (data-sh у блока и в скрипте);
  * t/<класс>-<спек>/ на 9 языках (243): noindex, вне sitemap.xml, og:title и twitter:title с классом и спеком на языке страницы,
    og:image = карточка спека этого языка (файл есть), summary_large_image, ссылка ведёт в калькулятор класса на наш билд спека;
  * карточки спеков assets/og/spec-*: 27 разных картинок на язык, ни одна не совпадает с общей карточкой билдов класса.
Запуск: python tests/test_wowhead_leak.py"""
import hashlib, html as H, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from langs import LANGS  # noqa: E402
from content.spec_cheats import CHEATS  # noqa: E402
import talents  # noqa: E402

CLASSES = list(dict.fromkeys(c for c, _ in CHEATS))
A_WH = re.compile(r'<a\b([^>]*\bhref="https://(?:www\.)?wowhead\.com[^"]*"[^>]*)>(.*?)</a>', re.S)


def sub(lang, path):
    return ('' if lang == 'ru' else lang + '/') + path


def read(rel):
    with open(os.path.join(ROOT, rel, 'index.html'), encoding='utf-8') as f:
        return f.read()


def test_no_wowhead_buttons():
    n = 0
    for lang in LANGS:
        for cid in CLASSES:
            for rel in (sub(lang, f'guides/builds-{cid}/'), sub(lang, f'talents/{cid}/')):
                t = read(rel)
                for attrs, text in A_WH.findall(t):
                    n += 1
                    assert 'rel="nofollow noopener"' in attrs, (rel, attrs)
                    assert not re.search(r'class="[^"]*\bbtn\b', attrs), ('a button to Wowhead', rel, attrs)
                    if 'talent-calc/' in attrs and 'talent-calc/' + cid + '"' not in attrs:   # a build on their calculator: the small line only
                        assert H.unescape(text).strip() == talents.UI['wh'][lang] + ' ↗', (rel, text)
                # the small line sits in its own paragraph or the editor bar, never next to our button
                for m in re.finditer(r'<p class="tt-go">(.*?)</p>', t, re.S):
                    assert 'wowhead.com' not in m[1], rel
    print(f'wowhead links: {n} on builds and talents pages, all nofollow, no button')


def test_go_button():
    import build_talent_links as TL
    n = 0
    ours = {cid: TL.our_codes(cid) for cid in CLASSES}
    for lang in LANGS:
        for cid in CLASSES:
            rel = sub(lang, f'guides/builds-{cid}/')
            t = read(rel)
            blocks = re.findall(r'<div class="tt" data-c="([a-z]+)" data-l="[a-z]+" data-sp="([a-z-]+)" data-w="([0-9-]*)" [^>]*data-sh="([^"]+)"'
                                r'(.*?)<div class="tt-ow" data-b="general">(.*?)</div>', t, re.S)
            assert len(blocks) == 3, (rel, len(blocks))
            for c, spec, code, sh, _, ow in blocks:
                assert c == cid and sh.endswith(f't/{cid}-'), (rel, c, sh)
                go = re.search(r'<p class="tt-go"><a class="btn" href="([^"]+)">([^<]+)</a></p>', ow)
                assert go, (rel, spec)
                assert go[1] == f'../../talents/{cid}/#{code}' and code == ours[cid][spec], (rel, spec, go[1], code)
                assert go[2] == talents.UI['go'][lang], (rel, go[2])
                assert ow.index('tt-go') < ow.index('tt-whc'), (rel, spec, 'the Wowhead line goes under our button')
                n += 1
    print(f'go buttons: {n} builds open in our calculator with their own code')


def test_share_page():
    js = talents.JS
    assert "w.dataset.sh + sp + '/#' + code" in js, 'copy link: t/<class>-<spec>/#<code>'
    sitemap = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    import build_talent_links as TL
    import build_guides as BG
    n = 0
    for cid in CLASSES:
        codes = TL.our_codes(cid)
        for lang in LANGS:
            calc = read(sub(lang, f'talents/{cid}/'))
            assert f'data-sh="../../t/{cid}-"' in calc, (lang, cid)   # the calculator copies the same kind of link
            for spec in [s for c, s in CHEATS if c == cid]:
                rel = sub(lang, f't/{cid}-{spec}/')
                t = read(rel)
                assert '<meta name="robots" content="noindex,follow">' in t and f'/wow/{rel}<' not in sitemap, rel
                n_ = BG.hero_core(lang)
                cname, sname = n_['cn'][cid], n_['sn'][cid][n_['sid'][cid].index(spec)]
                for prop in ('property="og:title"', 'name="twitter:title"'):
                    m = re.search(r'<meta %s content="([^"]+)"' % prop, t)
                    title = H.unescape(m[1])
                    assert cname in title and sname in title, (rel, prop, title)
                img = re.search(r'<meta property="og:image" content="https://gabella\.site/wow/(assets/og/[^"?]+)(?:\?v=\w+)?"', t)
                assert img and img[1] == f'assets/og/spec-{cid}-{spec}-{lang}.jpg', (rel, img and img[1])
                assert os.path.isfile(os.path.join(ROOT, img[1])), img[1]
                assert re.search(r'<meta name="twitter:image" content="[^"]*spec-%s-%s-%s\.jpg' % (cid, spec, lang), t), rel
                assert '<meta name="twitter:card" content="summary_large_image">' in t, rel
                go = re.search(r'<a id="go" href="([^"]+)">', t)[1]
                assert go.endswith(f'talents/{cid}/#{codes[spec]}') and codes[spec], (rel, go)
                assert os.path.isfile(os.path.normpath(os.path.join(ROOT, rel, go.split('#')[0], 'index.html'))), (rel, go)
                assert 'location.hash' in t and 'location.replace' in t, rel   # the shared code wins over ours
                n += 1
    print(f'share pages t/: {n}, class and spec in the card title, spec card picture')


def test_spec_cards():
    for lang in LANGS:
        seen = {}
        for cid, spec in CHEATS:
            f = os.path.join(ROOT, 'assets', 'og', f'spec-{cid}-{spec}-{lang}.jpg')
            h = hashlib.md5(open(f, 'rb').read()).hexdigest()
            assert h not in seen, ('the same card twice', lang, cid, spec, seen.get(h))
            seen[h] = (cid, spec)
        common = {hashlib.md5(open(os.path.join(ROOT, 'assets', 'og', f'builds-{c}-{lang}.jpg'), 'rb').read()).hexdigest() for c in CLASSES}
        assert not common & set(seen), lang
    print(f'spec cards: {len(CHEATS)} different pictures in each of {len(LANGS)} languages')


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
