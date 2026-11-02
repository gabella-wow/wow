"""Проверки собранных страниц: язык браузера на корне, ссылки на классы и расы без JS, время старта,
404 на языке адреса, шрифты под письмо языка. Запуск после python build.py: python tests/test_audit.py"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from langs import LANGS  # noqa: E402


def page(*parts):
    if not parts or not parts[-1].endswith('.html'):
        parts += ('index.html',)
    return open(os.path.join(ROOT, *parts), encoding='utf-8').read()


def home_js(lang):
    return open(os.path.join(ROOT, 'assets', 'home', f'{lang}.js'), encoding='utf-8').read()


def tools_js(lang):
    return open(os.path.join(ROOT, 'assets', 'tools', f'{lang}.js'), encoding='utf-8').read()


def lang_dir(lang):
    return () if lang == 'ru' else (lang,)


def test_auto_lang_only_on_russian_root():
    ru = page('index.html')
    assert ru.index("getItem('gabella-lang')") < ru.index('<title>')
    assert all(f'"{l}": "{"./" if l == "ru" else l + "/"}"' in ru for l in LANGS)
    for lang in LANGS[1:]:
        assert "getItem('gabella-lang')" not in page(lang), lang
    assert "getItem('gabella-lang')" not in page('classes', 'mage')


def test_language_menu_saves_choice():
    assert "localStorage.setItem('gabella-lang', l)" in page('guides', 'faq')


def test_class_and_race_links_without_js():
    for lang in LANGS:
        home = page(*lang_dir(lang))
        roster = re.search(r'id="roster">(.*?)</div>', home).group(1)
        assert roster.count('href="classes/') == 9, lang
        assert re.search(r'id="rosterA">(.*?)</div>', home).group(1).count('href="races/') == 5, lang
        assert page(*lang_dir(lang), 'classes').count('href="../classes/') >= 9, lang
        assert page(*lang_dir(lang), 'races').count('href="../races/') >= 10, lang


def test_launch_time_local_not_kyiv():
    for lang in LANGS:
        faq = page(*lang_dir(lang), 'guides', 'faq')
        assert faq.count('<time class="lt" datetime="2026-11-04T23:00:00Z">') == 2, lang
        assert "querySelectorAll('time.lt')" in faq
        assert not re.search(r'01:00[^<]{0,40}(Kyiv|Kiew|Kijowie|Киеве|Києві)', faq), lang


def test_not_found_per_language():
    """Root 404.html (GitHub Pages serves it for any bad address): a light page, no redirect, a block of text per language that shows
    without JS; the head script only picks the block of the address or the browser. <lang>/404.html: the full page, noindex."""
    root = page('404.html')
    assert 'noindex' in root and 'location.replace' not in root and 'sessionStorage' not in root
    assert len(root.encode('utf-8')) < 8000, len(root)
    assert re.findall(r'<section lang="[^"]+" data-k="(\w+)"', root) == list(LANGS)
    for lang in LANGS:
        assert f':root[data-l="{lang}"] section[data-k="{lang}"]' in root, lang
        assert re.search(rf'data-k="{lang}"><h1>[^<]+</h1><p class="why">[^<]+\.</p><p><a href="/wow/{"" if lang == "ru" else lang + "/"}">', root), lang
    assert "localStorage.getItem('gabella-lang')" in root and "l = l || 'en'" in root   # as the guide root: saved choice, else English
    # the chosen language also sets <html lang> and the tab title (screen readers read the page in its language)
    titles = json.loads(re.search(r'var T = (\{.*?\}), d = ', root).group(1))
    assert list(titles) == list(LANGS) and all(len(v) == 2 and v[1] for v in titles.values()), titles
    assert 'd.lang = T[l][0]' in root and 'document.title = T[l][1]' in root
    for lang in LANGS[1:]:
        nf = page(lang, '404.html')
        assert f'<base href="/wow/{lang}/">' in nf and 'noindex' in nf and 'location.replace(' not in nf, lang
        links = re.search(r'<p class="nf-langs">(.*?)</p>', nf).group(1)   # "where next": absolute links to every home, not ./en/ under <base>
        assert re.findall(r'href="([^"]+)"', links) == ['/wow/'] + [f'/wow/{l}/' for l in LANGS[1:]], lang


def test_home_waits_for_the_hero():
    """Home: only the first screen comes with the page; its script, radio, search, profile, living art, time of day,
    analytics sleep until the hero is painted (build.late, build.home_js); the manifest stays a plain link (P-1)."""
    for lang in LANGS:
        home = page(*lang_dir(lang))
        assert "const HOME = ''" not in home and 'function renderCountdown()' in home, lang
        root = './' if lang == 'ru' else '../'
        assert re.search(rf'<script data-src="{re.escape(root)}assets/home/{lang}\.js\?v=\w{{10}}"></script>', home), lang
        assert "const HOME = ''" in home_js(lang), lang
        assert not re.search(r'<script[^>]* src="[^"]*(?:assets/(?:radio|search|me|tod|living|home)/|cloudflareinsights)', home), lang
        assert not re.search(r'<link rel="[^"]+" href="[^"]*assets/(?:radio|search|me|tod)/', home), lang
        assert re.search(r'<link rel="manifest" href="[^"]*manifest-%s\.webmanifest">' % lang, home), lang
        assert home.count("document.querySelectorAll('script[data-src]')") == 1, lang
        assert home.index('assets/home/') < home.index('assets/radio/radio.js') < home.index('assets/me/me.js'), lang
    other = page('tools')                                     # pages outside seo.LATE_INNER load them as before
    assert re.search(r'<script src="\.\./assets/radio/radio\.js\?v=\w{10}" data-root="\.\./" defer>', other) and '<script data-src=' not in other
    for parts in (('guides', 'leveling'), ('play',)):           # inner pages wait for their hero picture like the home
        inner = page(*parts)
        assert re.search(r'<script data-src="[^"]*assets/radio/radio\.js\?v=\w{10}"', inner) and 'cloudflareinsights' in inner, parts
        assert not re.search(r'<script[^>]* src="[^"]*(?:assets/(?:radio|search|me|living)/|cloudflareinsights)', inner), parts
        assert "document.querySelector('img[fetchpriority=\"high\"]')" in inner and 'rel="manifest" href=' in inner, parts


def test_launch_countdown_at_23_utc():
    for lang in LANGS:
        home = page(*lang_dir(lang)) + home_js(lang)   # the page script lives in assets/home/ (build.home_js)
        assert "rel = new Date('2026-11-04T23:00:00Z')" in home and 'hd-line' not in home, lang
        assert "const D_REL = new Date('2026-11-04T23:00:00Z')" in page(*lang_dir(lang), 'play'), lang   # the game stages live on /play/
    for lang in LANGS:
        faq = page(*lang_dir(lang), 'guides', 'faq')
        assert not re.search(r'(не подтвердила|not yet confirmed|не підтвердила)', faq), lang


def test_guide_heroes_own_scenes():
    for slug, fx in (('', 'guides'), ('dungeons', 'dungeons'), ('faq', 'faq'), ('professions', 'professions')):
        for lang in LANGS:
            html = page(*lang_dir(lang), 'guides', *((slug,) if slug else ()))
            assert f'<picture class="thero-art" aria-hidden="true" data-fx="{fx}"' in html, (lang, slug)
            assert '@@HERO@@' not in html and 'assets/living/living.js' in html, (lang, slug)


def test_share_card_not_the_old_one():
    for lang in LANGS:
        for sub in ('profile', 'roster', 'u'):
            html = page(*lang_dir(lang), sub)
            assert 'assets/og.png' not in html and f'assets/og-{lang}.jpg' in html, (lang, sub)


def test_no_tool_names_in_sources():
    import codecs, subprocess
    files = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout.splitlines()
    bad = re.compile(codecs.decode(r'trzvav|anab onanan|naguebcvp|bcranv|(?<!\.)pynhqr|pb-nhguberq-ol', 'rot13'), re.I)   # tool names stay out of the public sources, this list too
    hits = []
    for f in files:
        if not f.endswith(('.py', '.txt', '.json', '.md', '.js', '.css', '.sh', '.yml', '.mjs', '.webmanifest')) and not f.endswith('.src.html'):
            continue
        try:
            text = open(os.path.join(ROOT, f), encoding='utf-8').read()
        except (OSError, UnicodeDecodeError):
            continue
        hits += [f for _ in bad.finditer(text)][:1]
    assert not hits, hits


def test_fonts_preloaded_for_the_script():
    for lang in LANGS:
        head = page(*lang_dir(lang))[:6000]
        want, other = ('ru-uk', 'latin') if lang in ('ru', 'uk') else ('latin', 'ru-uk')
        pre = lambda s: re.search(rf'golos-text-{s}\.woff2(\?v=\w+)?" as="font"', head)
        assert pre(want) and not pre(other), lang


def painted_pairs():
    import make_build_cards as MC
    return [f'{c}-{r}' for c in MC.BG.HERO.SPEC_IDS for r in MC.GAME['races'] if os.path.isfile(os.path.join(ROOT, 'assets', 'art', f'{c}-{r}-360.webp'))]


def test_portraits_match_the_race():
    """What the player chose and forwards (build cards b/, the raid frame, the picker): a portrait stands next to a race name only if it
    shows that race. Every race has its own portrait; every b/ card draws the race of its caption; the picker puts no class face
    (another race's painting) beside a race and the raid frame never takes the best race of a side (guides keep that, 26.10)."""
    sys.path[:0] = [os.path.join(ROOT, 'tools'), os.path.join(ROOT, 'content')]
    import make_build_cards as MC
    for rid, r in MC.GAME['races'].items():
        for kind in ('face', '896', 'bg'):
            assert os.path.isfile(os.path.join(ROOT, 'assets', 'art', f'{r["slug"]}-{kind}.webp')), (rid, kind)
        assert MC.portrait_race(f'assets/art/{r["slug"]}-896.webp') == rid
    for race, cls, spec in MC.combos():
        por, bg = MC.portrait_for(race, cls)
        assert MC.portrait_race(por) == race and MC.portrait_race(bg.replace('-bg', '-896')) == race, (race, cls, por)
    # the checker sees the old rule (class x faction): a dwarf hunter got hunter-nightelf
    assert MC.portrait_race('assets/art/hunter-nightelf-896.webp') == 'nightelf' != 'dwarf'
    for lang in LANGS:
        card = page(*lang_dir(lang), 'b', 'dwarf-hunter-beast-mastery')
        assert 'assets/og/b/dwarf-hunter-beast-mastery-%s.jpg' % lang in card, lang
    tools = open(os.path.join(ROOT, 'tools.src.html'), encoding='utf-8').read()
    assert "face(c.id, CCOL[c.id], '', '', r.f)" not in tools
    assert 'art(p.cls' not in tools and 'unitArt(p' in tools
    painted = re.search(r'PAINTED\s*=\s*(\[[^\]]*\])', tools_js('ru'))
    assert painted and sorted(json.loads(painted[1])) == sorted(painted_pairs()), painted and painted[1]


def test_tools_script_is_a_cached_file():
    """The tools page script lives in assets/tools/<lang>.js?v=<hash of the file>, deferred from <head> (build.tools_js):
    before every other deferred file, so it runs first after the parse, as the inline script at the end of <body> did."""
    import hashlib
    for lang in LANGS:
        html = page(*lang_dir(lang), 'tools')
        js = tools_js(lang)
        v = hashlib.sha1(js.encode('utf-8')).hexdigest()[:10]
        root = '../' if lang == 'ru' else '../../'
        tag = f'<script src="{root}assets/tools/{lang}.js?v={v}" defer></script>'
        assert tag in html, lang
        assert html.index(tag) < html.index('</head>') and 'data-js="tools"' not in html and 'const CPROF' not in html, lang
        assert not re.search(r'<script[^>]* src="[^"]*"[^>]*\bdefer\b', html[:html.index(tag)]), lang
        assert 'const CPROF = {' in js and 'renderRaid(fromLink)' in js and '@@' not in js, lang
        assert len(html.encode('utf-8')) < 170_000, (lang, len(html.encode('utf-8')))


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
    print('OK')
