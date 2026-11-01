"""Сборка гида: index.src.html, class.src.html, race.src.html (русские исходники) + content/classes.py, content/races.py
+ i18n/{ru,en,uk}.txt (переводы, строка в строку)
-> index.html, en/index.html, uk/index.html, classes/<id>/index.html и races/<slug>/index.html на трёх языках.
Запуск: python build.py [--list]  (--list печатает русские фрагменты без перевода)
Сборка идёт в копии дерева .build/, на место переносятся только изменённые файлы: упавшая сборка ничего не трогает."""
import datetime, hashlib, html as _html, json, os, posixpath, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if '--missing' in sys.argv:          # python build.py --missing de: build de without its json, print what it lacks, write nothing
    os.environ['WF_LANG'] = sys.argv[sys.argv.index('--missing') + 1]
    sys.argv.append('--list')
sys.path.insert(0, os.path.join(HERE, 'content'))
from classes import CLASSES, SOURCES  # noqa: E402
from races import RACES_PAGE, SOURCES as RACE_SOURCES, NEW_RACIALS  # noqa: E402
import langs  # noqa: E402
from content.hero import SPEC_IDS  # noqa: E402
import tod  # noqa: E402
import looks as LK  # noqa: E402
from langs import LANGS, AUTONYM, HREFLANG, LOCALE, NAMED  # noqa: E402


def load(name):
    with open(os.path.join(HERE, 'i18n', name), encoding='utf-8') as f:
        return f.read().splitlines()


_ru, _en, _uk = load('ru.txt'), load('en.txt'), load('uk.txt')
assert len(_ru) == len(_en) == len(_uk), (len(_ru), len(_en), len(_uk))
T = {r: (e, u) for r, e, u in zip(_ru, _en, _uk)}

CYR = r'А-Яа-яЁё'
SEG = re.compile(r'(?:(?!\$\{)[^<>"\'`{}\n])*[' + CYR + r'](?:(?!\$\{)[^<>"\'`{}\n])*')
SITE = 'https://gabella.site/wow/'


def t_of(ru, lang):
    """Translation of a Russian fragment known to T: en/uk from the line files, new languages via the English one."""
    en, uk = T[ru]
    return en if lang == 'en' else uk if lang == 'uk' else langs.ov(en, lang)


def split_ws(seg):
    core = seg.strip()
    i = seg.index(core)
    return seg[:i], core, seg[i + len(core):]


def translate(src, lang):
    missing = []

    def sub(m):
        lead, core, tail = split_ws(m.group(0))
        if lang == 'ru':
            return m.group(0)
        if core not in T:
            missing.append(core)
            return m.group(0)
        return lead + t_of(core, lang) + tail
    return SEG.sub(sub, src), missing


def tr(s, lang):
    return s if lang == 'ru' or s not in T else t_of(s, lang)


def page_dir(lang, sub=''):
    """Site-relative directory of a page, e.g. 'en/classes/mage/'."""
    return ('' if lang == 'ru' else lang + '/') + sub


def rel(from_dir, to_dir):
    r = posixpath.relpath(to_dir or '.', from_dir.rstrip('/') or '.')
    return './' if r == '.' else r + '/'


CONTACT = 'contact@gabella.site'   # Cloudflare Email Routing -> почта Вячеслава
DISCORD = 'https://discord.gg/ZGpznkX3Zw'   # постоянное приглашение на сервер Gabella · WoW Forever (EN/UK/RU, без срока и лимита)
# Места ссылки: все ведут на сервер сайта одним приглашением (замер по местам был на Gabella Team).
DISCORD_AT = {place: DISCORD for place in ('menu', 'guide', 'home', 'faq', 'profile', 'footer')}
TELEGRAM = 'https://t.me/gabella_wow'   # публичный канал новостей Gabella (создан 23.10)
LEGAL = {
    'ru': ('Фанатский сайт Gabella. Сайт не связан с Blizzard Entertainment и не одобрен ею. World of Warcraft, Warcraft и Blizzard Entertainment — '
           'товарные знаки или зарегистрированные товарные знаки Blizzard Entertainment, Inc. в США и/или других странах.', 'Конфиденциальность', 'Связь', 'Карта сайта'),
    'en': ('Gabella is a fan site. Not affiliated with or endorsed by Blizzard Entertainment. World of Warcraft, Warcraft and Blizzard Entertainment are '
           'trademarks or registered trademarks of Blizzard Entertainment, Inc. in the U.S. and/or other countries.', 'Privacy', 'Contact', 'Site map'),
    'uk': ('Фанатський сайт Gabella. Сайт не пов’язаний з Blizzard Entertainment і не схвалений нею. World of Warcraft, Warcraft і Blizzard Entertainment — '
           'торгові марки або зареєстровані торгові марки Blizzard Entertainment, Inc. у США та/або інших країнах.', 'Конфіденційність', 'Зв’язок', 'Мапа сайту'),
}


langs.derive(LEGAL)


TOOLS_T = langs.derive({'ru': 'Инструменты', 'en': 'Tools', 'uk': 'Інструменти'})


def site_map(lang, home):
    """Footer site map of every page: classes, races, guides, tools. home: path to the language home."""
    from content.guides import GUIDES, HUB, HUBS, ORDER, PLAY
    langs.fill([HUB, HUBS, PLAY] + GUIDES)
    if not _RACES:
        _RACES.extend(parse_races(open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()))
    slug = {r['id']: r['slug'] for r in RACES_PAGE}
    hub = {h['slug']: h for h in HUBS}
    guides = sorted((g for g in GUIDES if g.get('only', lang) == lang and (g.get('hub') is not False or g.get('footer'))), key=lambda g: ORDER.index(g['slug']) if g['slug'] in ORDER else len(ORDER))   # hub False (the nine class guides): off the footer too
    cols = [
        (hub['classes']['title'], 'classes/', [(f'classes/{c["id"]}/', tr(c['n'], lang)) for c in CLASSES]),
        (hub['races']['title'], 'races/', [(f'races/{slug[r["id"]]}/', tr(r['n'], lang)) for r in _RACES]),
        (HUB['title'], 'guides/', [(f'guides/{g["slug"]}/', g['title'][lang]) for g in guides]),
        (TOOLS_T, 'tools/', [('tools/', TOOLS_T[lang]), ('play/', PLAY['title'][lang])]),
    ]
    out = ''.join(f'<div><a class="fh" href="{home}{href}">{esc(h[lang])}</a><ul>'
                  + ''.join(f'<li><a href="{home}{u}">{esc(n)}</a></li>' for u, n in links) + '</ul></div>'
                  for h, href, links in cols)
    return f'<nav class="fmap" aria-label="{esc(LEGAL[lang][3])}">{out}</nav>'


def legal(lang, root):
    """Footer block of every page (@@LEGAL@@): site map, trademarks, ©, privacy page, Discord, contact."""
    text, privacy, contact = LEGAL[lang][:3]
    return site_map(lang, root + page_dir(lang)) + (f'<div class="legal"><p>{text}</p><p>© 2026 Gabella<span aria-hidden="true"> · </span>'
            f'<a href="{root}{page_dir(lang, "privacy/")}">{privacy}</a><span aria-hidden="true"> · </span>'
            f'{discord_link("footer")}<span aria-hidden="true"> · </span>'
            f'<a href="{TELEGRAM}" target="_blank" rel="noopener">Telegram</a><span aria-hidden="true"> · </span>'
            f'{contact}: <a href="mailto:{CONTACT}">{CONTACT}</a></p></div>')


def only_lang(sub):
    """Language of a page built in one language only (a guide with 'only': 'uk'), else None."""
    from content.guides import GUIDES
    return next((g['only'] for g in GUIDES if g.get('only') and sub == f'guides/{g["slug"]}/'), None)


def alternates(sub):
    """hreflang links of a page (site-relative directory sub, '' = home) in every built language; x-default = Russian
    (a one-language page: only its own language, which is also x-default)."""
    only = only_lang(sub)
    alt = '\n'.join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{SITE}{page_dir(l, sub)}">' for l in ([only] if only else LANGS))
    return alt + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{page_dir(only, sub) if only else sub}">'


# Browser-language hint, in the visitor's language: (text, link, close button)
HINT = {
    'ru': ('Эта страница есть на русском', 'Читать по-русски', 'Закрыть'),
    'en': ('This page is available in English', 'Read in English', 'Close'),
    'uk': ('Ця сторінка є українською', 'Читати українською', 'Закрити'),
    'de': ('Diese Seite gibt es auch auf Deutsch', 'Auf Deutsch lesen', 'Schließen'),
    'fr': ('Cette page existe aussi en français', 'Lire en français', 'Fermer'),
    'es': ('Esta página también está en español', 'Leer en español', 'Cerrar'),
    'pt': ('Esta página também está em português', 'Ler em português', 'Fechar'),
    'it': ('Questa pagina è disponibile anche in italiano', 'Leggi in italiano', 'Chiudi'),
    'pl': ('Ta strona jest dostępna po polsku', 'Czytaj po polsku', 'Zamknij'),
}

LANG_JS = """<script>
(() => {
  const KEY = 'gabella-lang-hint', store = l => { try { localStorage.setItem(KEY, '1'); if (l) localStorage.setItem('gabella-lang', l); } catch (e) {} };
  const keepHash = a => a.addEventListener('click', () => { store(a.dataset.lang); a.href = a.getAttribute('href').split('#')[0] + location.hash; });
  document.querySelectorAll('.langlist a, .langgrid a').forEach(keepHash);
  const sel = document.querySelector('.langsel'), btn = sel && sel.querySelector('.langbtn'), list = sel && sel.querySelector('.langlist');
  if (btn) {
    const links = [...list.querySelectorAll('a')];
    const shut = focus => { if (list.hidden) return; list.hidden = true; btn.setAttribute('aria-expanded', 'false'); if (focus) btn.focus(); };
    btn.addEventListener('click', e => {
      e.stopPropagation();
      list.hidden = !list.hidden; btn.setAttribute('aria-expanded', String(!list.hidden));
      if (!list.hidden) (list.querySelector('[aria-current]') || links[0]).focus();
    });
    document.addEventListener('click', e => { if (!sel.contains(e.target)) shut(); });
    sel.addEventListener('keydown', e => {
      if (e.key === 'Escape') return shut(true);
      const i = links.indexOf(document.activeElement);
      if (i < 0 || !['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(e.key)) return;
      e.preventDefault();
      const n = e.key === 'Home' ? 0 : e.key === 'End' ? links.length - 1 : (i + (e.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length;
      links[n].focus();
    });
    sel.addEventListener('focusout', e => { if (!sel.contains(e.relatedTarget)) shut(); });
  }
  let seen = '1';
  try { seen = localStorage.getItem(KEY); } catch (e) {}
  if (seen) return;
  const H = @@HINT@@, cur = document.documentElement.lang.split('-')[0];
  const want = (navigator.languages || [navigator.language]).map(x => String(x || '').toLowerCase().split('-')[0])
    .find(x => x in H && !(cur === 'uk' && x === 'ru'));   // a Ukrainian page never offers Russian
  const to = want && want !== cur && document.querySelector(`.langlist a[data-lang="${want}"]:not([data-list])`);
  if (!to) return;
  const bar = document.createElement('div');
  bar.className = 'langhint'; bar.lang = want; bar.setAttribute('role', 'status');
  bar.innerHTML = `<div class="lhin"><span>${H[want][0]}</span><a href="${to.getAttribute('href')}" hreflang="${to.hreflang}" data-lang="${want}">${H[want][1]}</a>`
    + `<button type="button" aria-label="${H[want][2]}"><svg class="ico" aria-hidden="true"><use href="#i-x"/></svg></button></div>`;
  keepHash(bar.querySelector('a'));
  // The strip sits in the page flow under the top bar: the body makes room for its height (--lh), nothing is covered.
  const root = document.documentElement, head = document.getElementById('topbar');
  const fit = () => { const h = bar.offsetHeight, was = parseFloat(root.style.getPropertyValue('--lh')) || 0; root.style.setProperty('--lh', h + 'px'); if (scrollY > 0) scrollBy(0, h - was); };
  bar.querySelector('button').addEventListener('click', () => {
    store(); bar.remove(); removeEventListener('resize', fit);
    const h = parseFloat(root.style.getPropertyValue('--lh')) || 0;
    root.classList.remove('langon'); root.style.removeProperty('--lh'); if (scrollY > 0) scrollBy(0, -h);
  });
  if (head) head.after(bar); else document.body.prepend(bar);
  root.classList.add('langon'); fit(); addEventListener('resize', fit);
})();
</script>
"""

# Root /wow/ only: the visitor's language before the page draws. A saved choice (gabella-lang, set by the language menu
# here and on the hub) wins; otherwise the browser languages, English for the rest. Bots, search results and links
# from inside the site stay on the Russian page, so search engines index it as is.
AUTO_JS = r"""<script>
(function () {
  if (window.wfMoved || /bot|crawl|spider|slurp|lighthouse|headless|google-|preview/i.test(navigator.userAgent) || navigator.webdriver) return;
  var P = @@PATHS@@, A = { be: 'ru', kk: 'ru' }, w = null, r = document.referrer;
  try { w = localStorage.getItem('gabella-lang'); } catch (e) {}
  if (!(w in P)) {
    w = null;
    if (r && (r.indexOf(location.origin + '/') === 0 || /^https?:\/\/([^\/]*\.)?(google|bing|yandex|ya|duckduckgo|yahoo|baidu|ecosia|naver|qwant|seznam)\.[^\/]+\//.test(r))) return;
    var L = navigator.languages || [navigator.language];
    for (var i = 0; i < L.length && !w; i++) { var b = String(L[i] || '').toLowerCase().split('-')[0]; b = A[b] || b; if (b in P) w = b; }
    w = w || 'en';
  }
  if (w !== 'ru') location.replace(P[w] + location.search + location.hash);
})();
</script>
"""


def auto_lang(html):
    paths = json.dumps({l: page_dir(l) or './' for l in LANGS})
    return html.replace('<meta name="viewport"', AUTO_JS.replace('@@PATHS@@', paths) + '<meta name="viewport"', 1)


def lang_menu(html, lang, here):
    """@@LANGSEL@@ (top bar: button + dropdown list) and @@LANGSHEET@@ (phone sheet: 3x3 grid) — the same page in every language."""
    sub = here[len(page_dir(lang)):]
    only = only_lang(sub)
    label = tr('Язык', lang)
    def link(l, inner):
        cur = ' aria-current="page"' if l == lang else ''
        to = 'guides/' if only and l != only else sub            # a one-language guide: other languages open their guide list
        lst = ' data-list' if to != sub else ''                   # not this page in that language: no browser-language hint
        return f'<a href="{rel(here, page_dir(l, to))}" data-lang="{l}" hreflang="{HREFLANG[l]}" lang="{HREFLANG[l]}"{cur}{lst}>{inner}</a>'
    items = ''.join(f'<li>{link(l, f"<span>{AUTONYM[l]}</span><small>{l.upper()}</small>")}</li>' for l in LANGS)
    sel = (f'<div class="langsel"><button type="button" class="langbtn" aria-haspopup="true" aria-expanded="false" '
           f'>{lang.upper()}<span class="sr">, {label}: {AUTONYM[lang]}</span></button><ul class="langlist" hidden>{items}</ul></div>')
    sheet = f'<div class="langgrid" role="group" aria-label="{label}">{"".join(link(l, AUTONYM[l]) for l in LANGS)}</div>'
    hint = json.dumps({l: HINT[l] for l in LANGS}, ensure_ascii=False)
    return html.replace('@@LANGSEL@@', sel).replace('@@LANGSHEET@@', sheet).replace('</body>', LANG_JS.replace('@@HINT@@', hint) + '</body>', 1)


# The social layer (Players page, achievement feed, the profile teaser) is hidden until 01.12.2026 (decision of 25.10):
# nothing is deleted. SOCIAL = True brings it all back: menu and sheet links, the home links, the feed, the teaser,
# roster/ back in the sitemap and indexed. Profile, login, u/ stay on either way (the mailing list and «Мой персонаж» use them).
SOCIAL = False
# Achievements, ranks, points and portrait frames are hidden everywhere (profile, u/, toasts, menu) except the «Founder» mark
# (decision of 25.10). Nothing is deleted: ACHIEVEMENTS = True brings it all back; the API and its tables are untouched.
ACHIEVEMENTS = False
SOCIAL_TAG = re.compile(r'<(\w+)\b[^>]*\sdata-social\b[^>]*>.*?</\1>', re.S)        # shown only with SOCIAL
NOSOCIAL_TAG = re.compile(r'<(\w+)\b[^>]*\sdata-nosocial\b[^>]*>.*?</\1>', re.S)    # shown only without it


def social(html):
    """Drops the elements of the hidden layer (data-social) or their stand-ins (data-nosocial); the marks go away."""
    html = (NOSOCIAL_TAG if SOCIAL else SOCIAL_TAG).sub('', html)
    return html.replace(' data-social', '').replace(' data-nosocial', '')


# Bottom tab bar on phones: the same tabs in the same order on every page (the profile button of the top bar is hidden there).
TABS = (('', 'home', 'Главная'), ('classes/', 'users', 'Классы'), ('guides/builds/', 'book', 'Билды'), ('guides/leveling/', 'up', 'Прокачка'))   # builds: question no. 1 of the readers; dungeons live in «Ещё»


def tabbar(cur=None, home='@@HOME@@', more=False):
    """Tab bar markup; cur — path of the current tab (a TABS path); home '' — the home page itself; more — the page lives in «Ещё»."""
    on = ' aria-current="true"'
    tabs = ''.join(f'\n  <a href="{home + p if home or p else "#top"}"{on if p == cur else ""}>'
                   f'<svg class="ico" aria-hidden="true"><use href="#i-{i}"/></svg>{t}</a>' for p, i, t in TABS)
    return (f'<nav class="tabbar" aria-label="Быстрые разделы">{tabs}\n  <button type="button" class="morebtn"{on if more else ""} aria-haspopup="dialog" aria-controls="moreDlg">'
            '<svg class="ico" aria-hidden="true"><use href="#i-dots"/></svg>Ещё</button>\n</nav>')


# Top menu: the same items in the same order on every page; anchors of the home page stay in its own «Ещё» group.
# Races, all articles and players live in «Ещё»; «Second screen» (play/) is in the menu since 29.10: people did not find it in «Ещё».
NAV = (('classes/', 'Классы'), ('guides/builds/', 'Билды и таланты'), ('guides/tier-list/', 'Тир-лист'), ('guides/legacy/', 'Legacy'),
       ('guides/leveling/', 'Прокачка'), ('guides/dungeons/', 'Подземелья'), ('tools/', 'Инструменты'), ('play/', 'Второй экран'))
# Sections sheet («Ещё»): (group, [(path from the language home, label)]); '#…' — a block of the home page.
# TAB_DUP: pages the phone tab bar already has — the sheet hides them below 720 px (the sheet keeps them for 720–1210 px, no menu there).
MORE = (
    ('Справочник', (('guides/builds/', 'Билды и таланты'), ('guides/tier-list/', 'Тир-лист'), ('guides/legacy/', 'Legacy'), ('guides/pvp/', 'PvP'), ('classes/', 'Классы'), ('classes/#choose', 'Какой класс выбрать'), ('races/', 'Расы'),
                    ('guides/leveling/', 'Прокачка 1–60'), ('guides/dungeons/', 'Подземелья и рейды'), ('guides/professions/', 'Профессии'),
                    ('guides/server-status/', 'Статус серверов'), ('guides/name-reservation/', 'Резерв имён'),
                    ('guides/faq/', 'FAQ и даты'), ('guides/news/', 'Новости'), ('guides/', 'Все статьи'))),
    ('Инструменты', (('talents/', 'Калькулятор талантов'), ('character/', 'Мой персонаж'),('tools/#picker', 'Раса и класс'), ('tools/#raid', 'Состав группы и LFG'), ('play/', 'Второй экран'))),
    ('Сообщество', (('discord', 'Discord'),) + ((('roster/', 'Игроки'),) if SOCIAL else ()) + (('profile/', 'Мой профиль'),)),
)
WIDE, NAV_WIDE = {'play/'}, ' class="nwide"'   # from 1440 px «Second screen» takes Discord's place (nine items do not fit); otherwise it is in «Ещё»
TALENTS, TL = 'guides/builds/', ' data-tl'   # the «Talents» item: hero.js points it at the saved character's spec tree
TAB_DUP = {p for p, _, _ in TABS if p}
TAB_SHORT = {'uk': {'Прокачування': 'Прокачка'}}   # a word too long for a fifth of a 320–375 px screen


def discord_link(src, text='Discord', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{DISCORD_AT[src]}" target="_blank" rel="noopener">{text}</a>'


def mainnav(cur=None, home='@@HOME@@'):
    """Top menu markup; cur — path of the current item (NAV), home '' — the home page itself."""
    on = ' aria-current="true"'
    links = ''.join(f'<a href="{home}{p}"{on if p == cur else ""}{TL if p == TALENTS else ""}{NAV_WIDE if p in WIDE else ""}>{t}</a>' for p, t in NAV)
    return f'<nav class="mainnav" aria-label="Разделы">\n    {links}{discord_link("menu", cls="nnarrow")}\n  </nav>'


def more_groups(home='@@HOME@@', cur=None):
    """Common groups of the sections sheet, after the page's own («Эта страница», list of classes or races)."""
    def a(p, t):
        if p == 'discord':
            return discord_link('menu', t)
        dup = ' class="tbd"' if p in TAB_DUP else ''
        now = ' aria-current="true"' if p == cur else ''
        return f'<a{dup}{TL if p == TALENTS else ""}{now} href="{home + p if home or (p and p[0] != "#") else (p or "#top")}">{t}</a>'
    return '\n    '.join(f'<div class="grp"><div class="gh">{g}</div>{"".join(a(p, t) for p, t in items)}</div>' for g, items in MORE)


def chrome(html, nav=None, tab=None, home='@@HOME@@'):
    """Menu, sections sheet and phone tab bar of a page (@@MAINNAV@@, @@MORENAV@@, @@TABBAR@@), before translate."""
    # the link name is its own text «Gabella · subtitle»: on 375–719 px the wordmark is only visually hidden (index.src.html), so no aria-label
    # that would differ from the visible text on wide screens (WCAG 2.5.3 label in name)
    return (html.replace('@@MAINNAV@@', mainnav(nav, home)).replace('@@MORENAV@@', more_groups(home, nav))
            .replace('@@TABBAR@@', tabbar(tab, home, more=bool(nav) and tab is None)))   # a page the tab bar lacks marks «Ещё» and its item in the sheet


_DIMS = {}


def webp_size(path):
    """(width, height) of a WebP file from its header: VP8X, VP8 (lossy) or VP8L (lossless)."""
    with open(path, 'rb') as f:
        b = f.read(30)
    kind = b[12:16]
    if kind == b'VP8X':
        return 1 + int.from_bytes(b[24:27], 'little'), 1 + int.from_bytes(b[27:30], 'little')
    if kind == b'VP8 ':
        return int.from_bytes(b[26:28], 'little') & 0x3fff, int.from_bytes(b[28:30], 'little') & 0x3fff
    if kind == b'VP8L':
        n = int.from_bytes(b[21:25], 'little')
        return (n & 0x3fff) + 1, ((n >> 14) & 0x3fff) + 1
    return None


IMG_NO_SIZE = re.compile(r'<img\b(?![^>]*\bwidth=)[^>]*\b(?:data-l)?src="[^"]*?assets/art/([\w.-]+\.webp)[^"]*"[^>]*>')


def img_dims(html):
    """K8: width and height on every art <img> that has none (tiles, cards): the browser keeps the box before the
    picture comes, so a late picture never shifts the page. Read from the file itself."""
    def add(m):
        name = m.group(1)
        if name not in _DIMS:
            f = os.path.join(HERE, 'assets', 'art', name)
            _DIMS[name] = webp_size(f) if os.path.isfile(f) else None
        if not _DIMS[name]:
            return m.group(0)
        w, h = _DIMS[name]
        return m.group(0).replace('<img ', f'<img width="{w}" height="{h}" ', 1)
    return IMG_NO_SIZE.sub(add, html)


# Skip link, the first Tab stop of every page with <main id="main">: past the top bar (logo, menu, search, radio, theme, language)
SKIP = {'ru': 'К содержанию', 'en': 'Skip to content', 'uk': 'До змісту', 'de': 'Zum Inhalt', 'fr': 'Aller au contenu',
        'es': 'Ir al contenido', 'pt': 'Ir para o conteúdo', 'it': 'Vai al contenuto', 'pl': 'Przejdź do treści'}


def localize(html, lang, here):
    """Language-specific attributes shared by all pages."""
    html = social(html.replace('@@LEGAL@@', legal(lang, rel(here, ''))))
    html = html.replace('@@ROOT@@', rel(here, ''))
    if '<main id="main">' in html:
        html = html.replace('<header class="topbar"', f'<a class="skip" href="#main">{SKIP[lang]}</a><header class="topbar"', 1)
    html = html.replace('@@DISCORD@@', DISCORD_AT['home']).replace('@@DISCORD_GUIDE@@', DISCORD_AT['guide'])
    html = lang_menu(html, lang, here)
    for word, short in TAB_SHORT.get(lang, {}).items():   # the phone tab bar: one short word per tab
        html = html.replace(f'</svg>{word}</a>', f'</svg>{short}</a>', 1) if '<nav class="tabbar"' in html else html
    if lang == 'ru':
        html = ru_names(html)
    else:
        html = html.replace('<html lang="ru">', f'<html lang="{HREFLANG[lang]}">')
        html = html.replace('content="ru_RU"', f'content="{LOCALE[lang]}"')
    if lang == 'en':
        html = en_dates(html)
    html = long_title(html)
    if lang not in ('ru', 'uk'):                                  # Latin-script pages: preload the fonts they draw first
        html = html.replace('-cyrillic.woff2" as="font"', '-latin.woff2" as="font"')
    else:
        html = cyr_fonts(html)
    html = html.replace('</head>', REVEAL_CSS + '</head>', 1).replace('</body>', REVEAL_JS + '</body>', 1)
    return img_dims(por(hero(me(pwa(html, lang, rel(here, '')), lang, here), lang, here)))


# the Latin of Russian and Ukrainian text: space, digits, punctuation, quotes, dashes, Latin words (WoW, Gabella)
CYR_FONT_CORE = 'U+0020-007E, U+00A0-00BF, U+00D7, U+00F7, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215'
CYR_FACE = re.compile(r'@font-face \{[^}]*assets/fonts/([\w-]+)-cyrillic\.woff2[^}]*\}\r?\n')


def cyr_fonts(html):
    """ru/uk pages: <family>-ru-uk.woff2 (Cyrillic + CYR_FONT_CORE, tools/subset_fonts.py) in place of the -cyrillic file.
    Its rule goes after the -latin one: of overlapping unicode-ranges the last rule wins, so the page draws its text from
    two font files instead of four before the first frame; the -latin file comes only for rarer characters (é, ñ)."""
    for m in list(CYR_FACE.finditer(html)):
        fam = m[1]
        rule = re.sub(r'unicode-range:([^;]*);', lambda r: f'unicode-range:{r[1]}, {CYR_FONT_CORE};',
                      m[0].replace(f'{fam}-cyrillic.woff2', f'{fam}-ru-uk.woff2'))
        html = html.replace(m[0], '', 1)
        lat = re.search(r'@font-face \{[^}]*assets/fonts/' + fam + r'-latin\.woff2[^}]*\}\r?\n', html)
        html = html[:lat.end()] + rule + html[lat.end():]
        html = html.replace(f'{fam}-cyrillic.woff2" as="font"', f'{fam}-ru-uk.woff2" as="font"')
    return html


EN_DATE = re.compile(r'(?<![\d.,:/\w-])(0[1-9]|[12]\d|3[01])\.(0[1-9]|1[0-2])(?:\.(20\d\d))?(?![\d\w]|\.\d)')
MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()


def en_dates(html):
    """English pages: 04.11 reads as April 11 to a US reader, so dd.mm(.yyyy) in the text becomes «Nov 4» («Nov 4, 2026»). Styles stay."""
    def one(m):
        d = f'{MONTHS[int(m[2]) - 1]} {int(m[1])}'
        return f'{d}, {m[3]}' if m[3] else d
    parts = re.split(r'(<style\b.*?</style>)', html, flags=re.S)
    return ''.join(p if p.startswith('<style') else EN_DATE.sub(one, p) for p in parts)


# Sections below the first screen fade in once when they scroll into view.
# Without JS, with reduced motion, in print or for what is already on screen nothing changes.
REVEAL_CSS = """<style>
.rv { opacity: 0; transform: translateY(18px); }
.rv.in { opacity: 1; transform: none; transition: opacity .6s var(--ease), transform .6s var(--ease); }
@media print { .rv { opacity: 1; transform: none; } }
.arrive body { visibility: hidden; }
</style>
<script>(function () {
  if (!/^#[A-Za-z0-9_-]+$/.test(location.hash)) return;
  var l = document.createElement('link'), d = document.documentElement;
  l.rel = 'expect'; l.href = location.hash; l.setAttribute('blocking', 'render'); document.head.append(l);
  d.classList.add('arrive'); setTimeout(function () { d.classList.remove('arrive'); }, 1500);
})();</script>
"""
REVEAL_JS = """<script>
(function () {
  // A page opened at #anchor (or by Back) lands mid-page. Its first frame is the anchor, not the top of the page flying by:
  // <head> keeps the page unpainted (rel=expect, .arrive) until here, the bar is solid from that frame, nothing there fades in.
  var d = document.documentElement, at = /^#[A-Za-z0-9_-]+$/.test(location.hash) && document.getElementById(location.hash.slice(1)), bar = document.getElementById('topbar');
  if (at && bar && at.getBoundingClientRect().top > 24) bar.classList.add('solid');
  if (at && scrollY < 25) at.scrollIntoView();
  requestAnimationFrame(function () { d.classList.remove('arrive'); });
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (location.hash.length > 1 || (performance.getEntriesByType('navigation')[0] || {}).type === 'back_forward') return;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('section.block, section.nband, section.stband:not(.ghero), .gsec, footer').forEach(function (s) {
    if (s.getBoundingClientRect().top > innerHeight) { s.classList.add('rv'); io.observe(s); }
  });
})();
</script>
"""


# Home page: the files the first screen does without (radio, search, profile, living art, time of day, analytics)
# wait in the page asleep, a <link> with data-rel and a <script> with data-src, and LATE_JS wakes them once the hero
# picture is painted, or at the first touch, key or scroll. Lighthouse counts every file that finishes before that paint.
# The manifest stays a plain <link> in <head>: the browser decides on the install prompt from it, and asleep it came too late.
LATE_JS = """<script>
(function () {
  var done = false;
  function wake() {
    if (done) return; done = true;
    var lf = document.getElementById('late-fonts');   // build.late_fonts
    if (lf) { lf.media = 'all'; try { localStorage.setItem('gab-fonts', '1'); } catch (e) {} }
    document.querySelectorAll('link[data-rel]').forEach(function (l) { l.rel = l.dataset.rel; });
    document.querySelectorAll('source[data-lsrcset]').forEach(function (x) { x.srcset = x.dataset.lsrcset; });   // build.sleep_art
    document.querySelectorAll('img[data-lsrc]').forEach(function (x) { x.src = x.dataset.lsrc; });
    document.querySelectorAll('script[data-src]').forEach(function (s) {
      var n = document.createElement('script');
      for (var i = 0; i < s.attributes.length; i++) if (s.attributes[i].name !== 'data-src') n.setAttribute(s.attributes[i].name, s.attributes[i].value);
      n.src = s.dataset.src; n.async = false;   // in page order: radio before the profile, as with defer
      s.replaceWith(n);
    });
  }
  ['pointerdown', 'keydown', 'touchstart', 'wheel', 'scroll'].forEach(function (t) { addEventListener(t, wake, { once: true, passive: true, capture: true }); });
  if (location.hash.length > 1) return wake();   // a link to a section: the blocks above it are drawn before the jump settles
  setTimeout(wake, 4000);   // a tab in the background paints nothing
  var img = document.querySelector('@@HERO@@');
  var lcp = window.PerformanceObserver && PerformanceObserver.supportedEntryTypes && PerformanceObserver.supportedEntryTypes.indexOf('largest-contentful-paint') >= 0;
  var armed = false;
  function later() {   // a wide screen, where the heading counts as the largest: a moment after the picture is drawn
    if (armed) return; armed = true;
    var go = function () { requestAnimationFrame(function () { setTimeout(wake, 500); }); };
    var start = function () { if (img && img.decode) img.decode().then(go, go); else go(); };
    if (document.readyState === 'complete') start(); else addEventListener('load', start, { once: true });
  }
  // The browser reports a paint only once the frame is on the screen: the phone wakes on the hero picture, a wide screen
  // starts its pause after the first one. A frame that comes late (a busy phone) then keeps the files waiting behind it.
  if (lcp)
    new PerformanceObserver(function (l) { if (img && l.getEntries().some(function (e) { return e.element === img; })) setTimeout(wake, 0); else later(); })
      .observe({ type: 'largest-contentful-paint', buffered: true });
  else later();
})();
</script>
"""
LATE_FILES = r'assets/(?:radio|search|me|hero|tod|living)/|static\.cloudflareinsights\.com/'


_CSS_TOK = re.compile(r'"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\'|url\([^)]*\)|/\*.*?\*/', re.S)


def min_css(html):
    """The inline <style> blocks without comments and the whitespace around { } ; , : (-20% of the style, -7 KB gzipped
    on a guide page; the first bytes of every page). Strings and url(...) stay as they are. Runs last (seo.main)."""
    def gap(g):
        g = re.sub(r'\s+', ' ', g)
        g = re.sub(r' ?([{};,]) ?', r'\1', g)
        return g.replace(': ', ':')

    def one(m):
        css, out, pos = m[2], [], 0
        for t in _CSS_TOK.finditer(css):
            out.append(gap(css[pos:t.start()]))
            out.append('' if t[0].startswith('/*') else t[0])
            pos = t.end()
        out.append(gap(css[pos:]))
        return m[1] + ''.join(out).strip().replace(';}', '}') + m[3]
    return re.sub(r'(<style[^>]*>)(.*?)(</style>)', one, html, flags=re.S)


PRUNE_JS = ('assets/me/me.js', 'assets/hero/hero.js', 'assets/search/search.js', 'assets/radio/radio.js', 'assets/living/living.js',
            'assets/tod/tod.js')   # scripts that add markup to any page: their words count as used
_PRUNE_WORDS = []


def prune_css(html):
    """The inline styles of a page without the rules no element of it can match: a selector is dropped only when a class or id it
    needs (outside :not()/:is()/[...] and other brackets) is not a word anywhere in the page (markup, inline scripts) or in the
    shared scripts of PRUNE_JS. Every page carries the whole home and guide stylesheet; a light page (the talent calculator) needs
    a fifth of it, and the browser's style work before the first frame is what holds its first paint back on a phone."""
    if not _PRUNE_WORDS:
        words = set()
        for f in PRUNE_JS:
            p = os.path.join(HERE, f)
            if os.path.isfile(p):
                words |= set(re.findall(r'[A-Za-z_][\w-]*', open(p, encoding='utf-8').read()))
        _PRUNE_WORDS.append(words)
    words = _PRUNE_WORDS[0] | set(re.findall(r'[A-Za-z_][\w-]*', re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.S)))

    def need(sel):
        s = sel
        while True:                                            # brackets out, innermost first: :not(.x) does not need .x
            t = re.sub(r'\([^()]*\)|\[[^\[\]]*\]', ' ', s)
            if t == s:
                break
            s = t
        return all(w in words for w in re.findall(r'[.#]([A-Za-z_][\w-]*)', s))

    def block(css, i):
        """End of the {…} block that opens at css[i] (strings and comments skipped)."""
        depth = 0
        while i < len(css):
            c = css[i]
            if c in '"\'':
                i = css.index(c, i + 1)
            elif css.startswith('/*', i):
                i = css.index('*/', i) + 1
            elif c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if not depth:
                    return i
            i += 1
        raise ValueError('unbalanced css')

    def walk(css):
        out, i = [], 0
        while i < len(css):
            j = css.find('{', i)
            k = css.find(';', i)
            if j < 0:
                out.append(css[i:])
                break
            if 0 <= k < j and css[i:k].strip().startswith('@'):   # @import, @charset
                out.append(css[i:k + 1])
                i = k + 1
                continue
            end = block(css, j)
            pre, body = css[i:j], css[j + 1:end]
            head = re.sub(r'/\*.*?\*/', '', pre, flags=re.S).strip()
            if re.match(r'@(media|supports|container|layer)\b', head):
                inner = walk(body)
                if inner.strip():
                    out.append(f'{pre}{{{inner}}}')
            elif head.startswith('@') or not head:
                out.append(css[i:end + 1])
            else:
                sels, depth, cur = [], 0, ''
                for ch in head:                                # selector list, commas inside brackets kept
                    depth += ch in '([' and 1 or (ch in ')]' and -1 or 0)
                    if ch == ',' and not depth:
                        sels.append(cur)
                        cur = ''
                    else:
                        cur += ch
                sels.append(cur)
                keep = [x.strip() for x in sels if need(x)]
                if keep:
                    out.append(f'\n{", ".join(keep)} {{{body}}}')
            i = end + 1
        return ''.join(out)
    return re.sub(r'(<style(?![^>]*media="print")[^>]*>)(.*?)(</style>)', lambda m: m[1] + walk(m[2]) + m[3], html, flags=re.S)


def late(html, hero='.hero-art img'):
    """Puts the files of LATE_FILES to sleep on a home page and adds LATE_JS (seo.apply calls it after the analytics tag).
    Inner pages (seo.LATE_INNER) do the same and wait for their own hero picture."""
    link =lambda m: f'<link data-rel="{m[1]}" href="{m[2]}">' if re.search(LATE_FILES, m[2]) else m[0]
    html = re.sub(r'<link rel="(stylesheet|manifest)" href="([^"]+)"(?: media="print" onload="[^"]*")?>', link, html)
    script = lambda m: f'<script{m[1] or ""} data-src="{m[2]}"{m[3].replace(" defer", "")}></script>' if re.search(LATE_FILES, m[2]) else m[0]
    html = re.sub(r'<script( type="module")? src="([^"]+)"([^>]*)></script>', script, html)
    return html if 'link[data-rel]' in html else html.replace('</body>', LATE_JS.replace('@@HERO@@', hero) + '</body>', 1)



# Home page: the display face (Spectral SC: titles, brand, big figures) is not among the bytes before the hero picture.
# Its @font-face rules sit in a <style media="print"> the browser does not apply, LATE_JS switches it on with the other
# late files, and the titles change from the Georgia fallback to Spectral SC then. A visitor who has it already
# (localStorage gab-fonts, the worker keeps the file) gets it from the first frame.
LATE_FONTS = 'spectral-sc'
LATE_FONTS_JS = ("<script>try { if (localStorage.getItem('gab-fonts')) document.getElementById('late-fonts').media = 'all'; }"
                 " catch (e) {}</script>\n")


def late_fonts(html):
    face = re.compile(r'@font-face \{[^}]*assets/fonts/' + LATE_FONTS + r'-[\w-]+\.woff2[^}]*\}\r?\n')
    rules = ''.join(face.findall(html))
    html = face.sub('', html)
    html = re.sub(r'<link rel="preload" href="[^"]*assets/fonts/' + LATE_FONTS + r'-[^"]*"[^>]*>\r?\n', '', html)
    return html.replace('<style>', f'<style id="late-fonts" media="print">\n{rules}</style>\n{LATE_FONTS_JS}<style>', 1)


# ---------- installable site (PWA): manifest, icons, service worker sw.js ----------

APP = {
    'ru': {'name': 'WoW Forever — справочник Gabella', 'desc': 'Классы, расы, подземелья, прокачка и сборка группы для WoW Forever.',
           'install': 'Установить', 'install_l': 'Установить справочник как приложение',
           'short': [('В игре', 'play/'), ('Билды', 'guides/builds/'), ('Подземелья', 'guides/dungeons/'), ('Инструменты', 'tools/'), ('Классы', 'classes/')]},
    'en': {'name': 'WoW Forever — Gabella reference', 'desc': 'Classes, races, dungeons, leveling and party building for WoW Forever.',
           'install': 'Install', 'install_l': 'Install the reference as an app',
           'short': [('In game', 'play/'), ('Builds', 'guides/builds/'), ('Dungeons', 'guides/dungeons/'), ('Tools', 'tools/'), ('Classes', 'classes/')]},
    'uk': {'name': 'WoW Forever — довідник Gabella', 'desc': 'Класи, раси, підземелля, прокачування та збір групи для WoW Forever.',
           'install': 'Встановити', 'install_l': 'Встановити довідник як застосунок',
           'short': [('У грі', 'play/'), ('Білди', 'guides/builds/'), ('Підземелля', 'guides/dungeons/'), ('Інструменти', 'tools/'), ('Класи', 'classes/')]},
}
langs.derive(APP)


def brand_src(path):
    """assets/... path of a brand image with ?v=<hash of the file> (manifests; brand_version() does the same in the pages)."""
    f = os.path.join(HERE, path)
    return path + ('?v=' + hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8] if os.path.isfile(f) else '')


def manifest(lang):
    a, home = APP[lang], page_dir(lang)
    icons = [{'src': brand_src(f'assets/icons/icon-{s}.png'), 'sizes': f'{s}x{s}', 'type': 'image/png', 'purpose': 'any'} for s in (192, 512)]
    icons.append({'src': brand_src('assets/icons/icon-maskable-512.png'), 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'})
    return json.dumps({
        'id': './', 'name': a['name'], 'short_name': 'Gabella WoW', 'description': a['desc'], 'lang': HREFLANG[lang], 'dir': 'ltr',
        'start_url': './' + home, 'scope': './', 'display': 'standalone', 'orientation': 'any',
        'background_color': '#050505', 'theme_color': '#050505', 'categories': ['games', 'entertainment'], 'icons': icons,
        'shortcuts': [{'name': n, 'url': './' + home + u} for n, u in a['short']],
    }, ensure_ascii=False, indent=1)


PWA_JS = """<script>
if ('serviceWorker' in navigator) addEventListener('load', () => navigator.serviceWorker.register('@@R@@sw.js').catch(() => {}));
addEventListener('beforeinstallprompt', e => {
  e.preventDefault();
  const opts = document.querySelector('.sheet .opts');
  if (!opts || opts.querySelector('.installbtn')) return;
  const b = document.createElement('button');
  b.className = 'iconbtn installbtn'; b.type = 'button'; b.style.padding = '0 14px';
  b.setAttribute('aria-label', '@@L@@');
  b.innerHTML = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11m-5-5 5 5 5-5M5 20h14"/></svg><span>@@T@@</span>';
  b.onclick = async () => { e.prompt(); await e.userChoice; b.remove(); };
  opts.append(b);
});
</script>
"""


TEXT_EXT = ('.js', '.css', '.json', '.webmanifest', '.svg', '.txt', '.html', '.xml', '.vtt', '.md')


def read_norm(path):
    """File bytes with CRLF turned into LF for text files, so hashes are the same on LF and CRLF checkouts (autocrlf)."""
    b = open(path, 'rb').read()
    return b.replace(b'\r\n', b'\n') if path.endswith(TEXT_EXT) else b


def sw_version():
    """sw.js VERSION = short hash of assets/ (without the news feed, the worker fetches it fresh) and the manifests."""
    h = hashlib.sha1()
    files = [os.path.join(d, f) for d, _, fs in os.walk(os.path.join(HERE, 'assets')) for f in fs if f != 'news.json']
    files += [os.path.join(HERE, f'manifest-{l}.webmanifest') for l in LANGS]
    for f in sorted(files):
        h.update(os.path.relpath(f, HERE).replace(os.sep, '/').encode())
        h.update(read_norm(f))
    sw = os.path.join(HERE, 'sw.js')
    assert '<<<<<<<' not in open(sw, encoding='utf-8').read(), 'sw.js: unresolved merge conflict'
    js = re.sub(r"const VERSION = '[^']*';", f"const VERSION = '{h.hexdigest()[:10]}';", open(sw, encoding='utf-8').read(), count=1)
    open(sw, 'w', encoding='utf-8', newline='\n').write(js)


RADIO = langs.derive({'ru': 'Радио', 'en': 'Radio', 'uk': 'Радіо'})
RADIO_BTN = ('<button class="iconbtn radiobtn" type="button" aria-label="@@L@@" title="@@L@@" aria-expanded="false" aria-controls="radioPanel" aria-pressed="false">'
             '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
             '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/></svg>'
             '<span class="rdo-eq" aria-hidden="true"><i></i><i></i><i></i></span></button>\n    ')


SEARCH = {'ru': 'Поиск по сайту', 'en': 'Search the site', 'uk': 'Пошук по сайту', 'de': 'Suche auf der Website', 'fr': 'Rechercher sur le site',
          'es': 'Buscar en el sitio', 'pt': 'Pesquisar no site', 'it': 'Cerca nel sito', 'pl': 'Szukaj w serwisie'}
SEARCH_SHORT = {'ru': 'Поиск', 'en': 'Search', 'uk': 'Пошук', 'de': 'Suche', 'fr': 'Recherche', 'es': 'Buscar', 'pt': 'Pesquisar', 'it': 'Cerca', 'pl': 'Szukaj'}
SEARCH_BTN = ('<button class="iconbtn srchbtn" type="button" aria-label="@@L@@" aria-haspopup="dialog">'
              '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
              '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg><span class="sl">@@S@@</span><kbd>Ctrl K</kbd></button>\n    ')


def search(html, lang, root):
    """Site search (assets/search/, search.py): button before the radio button, styles without blocking the page, script.
    search.py adds ?v=<hash> to both files after the index is written."""
    html = html.replace('<button class="iconbtn radiobtn"', SEARCH_BTN.replace('@@L@@', SEARCH[lang]).replace('@@S@@', SEARCH_SHORT[lang]) + '<button class="iconbtn radiobtn"', 1)
    head = f'<link rel="stylesheet" href="{root}assets/search/search.css" media="print" onload="this.media=\'all\'">\n</head>'
    js = f'<script src="{root}assets/search/search.js" data-root="{root}" defer></script>\n</body>'
    return html.replace('</head>', head, 1).replace('</body>', js, 1)


def radio(html, lang, root):
    """Radio (assets/radio/, tools/make_radio.py): button before the theme button of the top bar, styles without blocking the page, script."""
    html = html.replace('<button class="iconbtn themebtn"', RADIO_BTN.replace('@@L@@', RADIO[lang]) + '<button class="iconbtn themebtn"', 1)
    head = (f'<link rel="stylesheet" href="{root}assets/radio/radio.css" media="print" onload="this.media=\'all\'">\n</head>')
    js = f'<script src="{root}assets/radio/radio.js" data-root="{root}" defer></script>\n</body>'
    return html.replace('</head>', head, 1).replace('</body>', js, 1)


TEASER = langs.derive({'ru': 'Профиль хранит ваших персонажей, достижения и рамки', 'en': 'Your profile keeps your characters, achievements and frames',
                       'uk': 'Профіль зберігає ваших персонажів, досягнення й рамки'})   # the line for signed-out readers; same words as MORE['teaser']


def me(html, lang, here):
    """Profiles (assets/me/, build_me.py): after the radio, so its events are heard. data-page is the path under the language
    home (guides/leveling/, tools/, play/; the 404 page swaps in 404) — me.js finds the page it is on without parsing URLs."""
    root, home = rel(here, ''), rel(here, page_dir(lang))
    page = here[len(page_dir(lang)):]
    solo = ' data-solo="1"' if only_lang(page) else ''   # a language-only guide is not in the guide set of game.json: me.js skips it
    label = _html.escape(tr('Мой профиль', lang))   # drawn with the page, like search and radio; me.js swaps in the portrait once signed in
    html = html.replace('<button class="iconbtn themebtn"', f'<a class="iconbtn mebtn" href="{home}profile/" aria-label="{label}" title="{label}">'
                        '<svg class="ico" aria-hidden="true"><use href="#i-user"/></svg></a>\n    <button class="iconbtn themebtn"', 1)
    head = f'<link rel="stylesheet" href="{root}assets/me/me.css" media="print" onload="this.media=\'all\'">\n</head>'
    js = f'<script src="{root}assets/me/me.js" data-root="{root}" data-home="{home}" data-lang="{lang}" data-ach="{int(ACHIEVEMENTS)}" data-teaser="{_html.escape(TEASER[lang]) if SOCIAL else ''}" data-close="{_html.escape(tr('Закрыть', lang))}" data-page="{page}" data-look="{LK.V}"{solo} defer></script>\n</body>'
    return html.replace('</head>', head, 1).replace('</body>', js, 1)


SIDES = ('alliance', 'horde')
_POR, _PORJS = {}, []


def portraits():
    """Class portrait of each side (decision 26.10): the first best race of content/hero.BEST[class][side]['*'] that has a
    picture assets/art/<class>-<race>-face.webp (tools/make_images.py cuts it); none drawn yet: the old class portrait <class>.
    The names follow the data of the best-race guide, nothing is set by hand here."""
    if not _POR:
        from content import hero as H
        d = os.path.join(HERE, 'assets', 'art')
        for c in CLASSES:
            _POR[c['id']] = {f: next((f'{c["id"]}-{r}' for r in H.BEST[c['id']][f]['*'][0]
                                      if os.path.isfile(os.path.join(d, f'{c["id"]}-{r}-face.webp'))), c['id']) for f in SIDES}
    return _POR


def race_sides():
    if not _RACES:
        _RACES.extend(parse_races(open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()))
    return {r['id']: r['f'] for r in _RACES}


def por_js():
    """window.GabellaPor in <head> of every page: which side's class portraits the reader sees. The side of the hero of this
    browser (gabella-wf-me), else the home hero's time of day: dawn and day — the Alliance, dusk and night — the Horde
    (as on the home page). Art names "{<class>}" in data-por-src / data-por-srcset (and in page JS through url()) become
    the portrait of that side; build.art_version tags them with one ?v= over both files. A side chosen by hand (the home switch,
    gabella-side) beats the time of day but lasts only for the hero it was made with: a new hero brings his own side back.
    A new hero (the switch sheet, another tab), the switch or another time of day on the home page swaps them at once."""
    if _PORJS:
        return _PORJS[0]
    data = json.dumps({'m': portraits(), 'r': race_sides(), 'b': tod.bounds()}, separators=(',', ':'))
    _PORJS.append('<script>(function(){var D=' + data + ',M=D.m,R=D.r,B=D.b,K="gabella-side";'
            'function rd(k){var v=null;try{v=JSON.parse(localStorage.getItem(k))}catch(e){}return v}'
            'function st(h){return h&&R[h.race]?h.race+"."+h.cls:""}'
            'function fac(){var h=rd("gabella-wf-me"),m=rd(K);'
            'if(m&&(m.f=="alliance"||m.f=="horde")&&m.h===st(h))return m.f;if(h&&R[h.race])return R[h.race];'
            'var t=document.documentElement.getAttribute("data-tod"),s=null;if(!t){try{s=localStorage.getItem("gabella-tod")}catch(e){}'
            'var H=new Date().getHours();t=/^(dawn|day|dusk|night)$/.test(s)?s:H>=B[0]&&H<B[2]?"day":"night"}'
            'return t=="dusk"||t=="night"?"horde":"alliance"}'
            'function id(c,f){return M[c]?M[c][f||fac()]:c}'
            r'function url(s,f){return s.replace(/\{(\w+)\}/g,function(x,c){return M[c]?id(c,f):x})}'
            'function fill(el,f){el=el||document;el.querySelectorAll("[data-por-srcset]").forEach(function(e){var v=url(e.getAttribute("data-por-srcset"),f);if(e.getAttribute("srcset")!==v)e.setAttribute("srcset",v)});'
            'el.querySelectorAll("[data-por-src]").forEach(function(e){var v=url(e.getAttribute("data-por-src"),f);if(e.getAttribute("src")!==v)e.setAttribute("src",v)})}'
            'function set(f){try{localStorage.setItem(K,JSON.stringify({f:f,h:st(rd("gabella-wf-me"))}))}catch(e){}'
            'fill();dispatchEvent(new Event("gabella-side"))}'
            'window.GabellaPor={map:M,side:R,fac:fac,id:id,url:url,fill:fill,set:set};'
            'var re=function(){fill()};document.addEventListener("DOMContentLoaded",re);addEventListener("gabella-me",re);document.addEventListener("gabella:tod",re);'
            'addEventListener("storage",function(e){if(e.key=="gabella-wf-me"||e.key==K){re();dispatchEvent(new Event("gabella-side"))}})})();</script>\n')
    return _PORJS[0]


def por(html):
    """GabellaPor in <head> before any script of the page that draws a class portrait: after the font preloads (they stay
    in the first bytes, tests/test_audit.py), else right after the viewport meta."""
    head = html[:html.find('</head>')]
    fonts = list(re.finditer(r'<link rel="preload"[^>]*as="font"[^>]*>\n?', head))
    if fonts:
        i = fonts[-1].end()
        return html[:i] + por_js() + html[i:]
    return re.sub(r'(<meta name="viewport"[^>]*>\n?)', lambda m: m.group(1) + por_js(), html, count=1)


def hero(html, lang, here):
    """My character (assets/hero/): the switch behind the top-bar profile button of a reader without a login, and the home
    block. After me.js (it hands the button over); the texts and game data are assets/hero/<lang>.json (build_guides.hero_json)."""
    root, home = rel(here, ''), rel(here, page_dir(lang))
    head = f'<link rel="stylesheet" href="{root}assets/hero/hero.css" media="print" onload="this.media=\'all\'">\n</head>'
    js = (f'<script src="{root}assets/hero/hero.js" data-root="{root}" data-home="{home}" data-data="{root}assets/hero/{lang}.json" '
          f'defer></script>\n</body>')
    return html.replace('</head>', head, 1).replace('</body>', js, 1)


def hero_version():
    script_version('hero', ['hero.js', 'hero.css'] + [f'{l}.json' for l in LANGS])


def css_version():
    """?v=<hash of the file> on every url(file) of the stylesheets under assets/ (the painted frames of me.css and the like):
    the picture is fetched by the stylesheet, so its address must change with it. A stylesheet is hashed after this pass
    (me_version, script_version), so a frame redrawn under the same name moves the stylesheet's own address too."""
    rx = re.compile(r"url\((['\"]?)([^)'\"?#]+)(?:\?v=\w+)?\1\)")
    n = 0
    for d, _, fs in os.walk(os.path.join(HERE, 'assets')):
        for f in fs:
            if not f.endswith('.css'):
                continue
            p = os.path.join(d, f)

            def tag(m):
                u = m.group(2)
                if re.match(r'(?:[a-z]+:|//)', u):
                    return m.group(0)
                t = os.path.normpath(os.path.join(d, u))
                if not os.path.isfile(t):
                    return m.group(0)
                return f'url({m.group(1)}{u}?v={hashlib.sha1(open(t, "rb").read()).hexdigest()[:8]}{m.group(1)})'
            was = open(p, encoding='utf-8').read()
            new = rx.sub(tag, was)
            if new != was:
                open(p, 'w', encoding='utf-8', newline='\n').write(new)
                n += 1
    print(f'css: {n} stylesheets', file=sys.stderr)


def me_version():
    """?v=<hash> on me.js/me.css in every page: Cloudflare keeps /wow/assets/ for 30 days, a new address skips that cache.
    The achievement icons (assets/me/ach/) are drawn by me.js and the profile pages by name: one version over the folder,
    put into /*AV*/ of me.js and of the pages."""
    d = os.path.join(HERE, 'assets', 'me')
    av = hashlib.sha1()
    ad = os.path.join(d, 'ach')
    for f in sorted(os.listdir(ad)):
        av.update(f.encode() + open(os.path.join(ad, f), 'rb').read())
    av = '?v=' + av.hexdigest()[:8]
    mp = os.path.join(d, 'me.js')
    js = open(mp, encoding='utf-8').read()
    new = re.sub(r"/\*AV\*/'[^']*'", f"/*AV*/'{av}'", js)
    if new != js:
        open(mp, 'w', encoding='utf-8', newline='\n').write(new)
    h = hashlib.sha1()
    for f in sorted(os.listdir(d)):
        if f in ('me.js', 'me.css') or f.startswith('i18n-'):   # me.js passes the same version on to the texts
            h.update(read_norm(os.path.join(d, f)))
    v = h.hexdigest()[:10]
    n = 0
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules')]
        for f in files:
            if f.endswith('.html') and not f.endswith('.src.html'):
                p = os.path.join(root, f)
                html = open(p, encoding='utf-8').read()
                new = re.sub(r"/\*AV\*/'[^']*'", f"/*AV*/'{av}'", html)   # achievement icons in the page JS
                new = re.sub(r'(assets/me/me\.(?:js|css))(?:\?v=\w+)?', rf'\1?v={v}', new)
                if new != html:
                    open(p, 'w', encoding='utf-8', newline='\n').write(new)
                    n += 1
    print(f'me: {n} pages, v={v}', file=sys.stderr)


def script_version(folder, names):
    """?v=<hash of assets/<folder>/*> on the given files of that folder in every built page, like me_version."""
    d = os.path.join(HERE, 'assets', folder)
    h = hashlib.sha1()
    for f in sorted(os.listdir(d)):
        h.update(read_norm(os.path.join(d, f)))
    v = h.hexdigest()[:10]
    rx = re.compile(rf'(assets/{folder}/(?:{"|".join(re.escape(n) for n in names)}))(?:\?v=\w+)?')
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules')]
        for f in files:
            if f.endswith('.html') and not f.endswith('.src.html'):
                p = os.path.join(root, f)
                html = open(p, encoding='utf-8').read()
                new = rx.sub(rf'\1?v={v}', html)
                if new != html:
                    open(p, 'w', encoding='utf-8', newline='\n').write(new)
    print(f'{folder}: v={v}', file=sys.stderr)


def living_version():
    """?v=<hash> on assets/living/living.js (art masks included; the script passes the version on to them)."""
    script_version('living', ['living.js'])


def radio_version():
    """?v=<hash> on radio.js/css; the script passes it on to stations.json (track lists change with tools/make_radio.py)."""
    script_version('radio', ['radio.js', 'radio.css'])


def tod_version():
    script_version('tod', ['tod.js', 'tod.css'])


def art_version():
    """?v=<hash> on every assets/art/<file> address in the pages: Cloudflare and the browser keep /wow/assets/ for days
    (7 in the browser, plus the service worker), so a picture redrawn under the same name would otherwise stay old
    for returning visitors while living.js and its masks (versioned) already move on — water off its place."""
    d = os.path.join(HERE, 'assets', 'art')
    ver = {}

    def tag(m):
        name = m.group(2)
        if name not in ver:
            # hero_{tod}-<w>.<ext> (tod.py) is filled in by the browser: one version over all four times of day
            fs = [os.path.join(d, name.replace('{tod}', t)) for t in tod.PARTS] if '{tod}' in name else [os.path.join(d, name)]
            pm = re.fullmatch(r'\{(\w+)\}(.*)', name)
            if pm and pm.group(1) in portraits():   # {<class>}-<w>.<ext> (por_js): the portrait of the reader's side, one version over both
                fs = [os.path.join(d, portraits()[pm.group(1)][f] + pm.group(2)) for f in SIDES]
            h = hashlib.sha1()
            for f in fs:
                if os.path.isfile(f):
                    h.update(open(f, 'rb').read())
            ver[name] = h.hexdigest()[:8] if any(os.path.isfile(f) for f in fs) else ''
        return m.group(1) + (f'?v={ver[name]}' if ver[name] else '')
    scenes = {f: '?v=' + hashlib.sha1(open(os.path.join(d, f), 'rb').read()).hexdigest()[:8]
              for f in sorted(os.listdir(d)) if f.startswith('hero_')}
    # page JS draws class and race portraits by id (face, cards, picker): one version over all of them
    pv = hashlib.sha1()
    for f in sorted(os.listdir(d)):
        if not f.startswith(('hero_', 'scene-')):
            pv.update(f.encode() + open(os.path.join(d, f), 'rb').read())
    pv = '?v=' + pv.hexdigest()[:8]
    # pic() in page JS draws only the scenes the script names in quotes ('hero_dawn-960'): the map carries just those
    artv = lambda html, extra='': '/*ARTV*/' + json.dumps({f: v for f, v in scenes.items()
                                                          if f"'{f.rsplit('.', 1)[0]}'" in html or f'"{f.rsplit(".", 1)[0]}"' in extra}, separators=(',', ':'))
    # scripts of assets/ draw portraits and scenes by name too: me.js (the small portrait), radio.js (the cover is the art of a
    # station, named in stations.json). They are hashed after this pass (me_version, radio_version).
    for js, named in (('me/me.js', ''), ('hero/hero.js', ''), ('radio/radio.js', open(os.path.join(HERE, 'assets', 'radio', 'stations.json'), encoding='utf-8').read())):
        p = os.path.join(HERE, 'assets', js)
        was = open(p, encoding='utf-8').read()
        new = re.sub(r"/\*PV\*/'[^']*'", f"/*PV*/'{pv}'", re.sub(r'/\*ARTV\*/\{[^}]*\}', lambda _: artv(was, named), was))
        if new != was:
            open(p, 'w', encoding='utf-8', newline='\n').write(new)
    n = 0
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules')]
        for f in files:
            if f.endswith('.html') and not f.endswith('.src.html'):
                p = os.path.join(root, f)
                was = html = open(p, encoding='utf-8').read()
                html = re.sub(r'/\*ARTV\*/\{[^}]*\}', lambda _: artv(html), html)   # pic() in page JS
                html = re.sub(r"/\*PV\*/'[^']*'", f"/*PV*/'{pv}'", html)   # portraits in page JS
                new = re.sub(r'(assets/art/([A-Za-z0-9_.{}-]+\.(?:avif|webp|jpg|png)))(?:\?v=\w+)?', tag, html)
                if new != was:
                    open(p, 'w', encoding='utf-8', newline='\n').write(new)
                    n += 1
    print(f'art: {n} pages, {len(ver)} files', file=sys.stderr)


def og_version():
    """?v=<hash> on every assets/og/<file>.jpg address (og:image, twitter:image): Cloudflare and the networks keep a
    share preview under its name, so a card laid out again by tools/make_og.py would otherwise stay old."""
    d = os.path.join(HERE, 'assets', 'og')
    ver = {}

    def tag(m):
        name = m.group(2)
        if name not in ver:
            f = os.path.join(d, name)
            ver[name] = hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8] if os.path.isfile(f) else ''
        return m.group(1) + (f'?v={ver[name]}' if ver[name] else '')
    n = 0
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules')]
        for f in files:
            if f.endswith('.html') and not f.endswith('.src.html'):
                p = os.path.join(root, f)
                was = open(p, encoding='utf-8').read()
                new = re.sub(r'(assets/og/([A-Za-z0-9_./-]+\.jpg))(?:\?v=\w+)?', tag, was)
                if new != was:
                    open(p, 'w', encoding='utf-8', newline='\n').write(new)
                    n += 1
    print(f'og:{n} pages, {len(ver)} files', file=sys.stderr)


def brand_version():
    """?v=<hash> on the brand images that had no version: header mark, favicons, apple-touch-icon, PWA icons (pages, JSON-LD,
    me.js, the worker's PRECACHE) and the site cards assets/og-<lang>.jpg (og:image, twitter:image). Cloudflare and browsers
    keep these under their names, so a logo redrawn by tools/make_logo.py, make_icons.py or make_og.py would stay old."""
    ver = {}
    rx = re.compile(r'(assets/(?:brand/mark\.webp|icons/[A-Za-z0-9-]+\.(?:png|ico)|og-[a-z]{2}\.jpg))(?:\?v=\w+)?')

    def tag(m):
        name = m.group(1)
        if name not in ver:
            f = os.path.join(HERE, name)
            ver[name] = hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8] if os.path.isfile(f) else ''
        return name + (f'?v={ver[name]}' if ver[name] else '')
    n = 0
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules')]
        for f in files:
            if f.endswith('.html') and not f.endswith('.src.html') or root == HERE and f == 'sw.js':
                p = os.path.join(root, f)
                was = open(p, encoding='utf-8').read()
                new = rx.sub(tag, was)
                if new != was:
                    open(p, 'w', encoding='utf-8', newline='\n').write(new)
                    n += 1
    p = os.path.join(HERE, 'assets', 'me', 'me.js')   # the profile script draws the mark by itself
    was = open(p, encoding='utf-8').read()
    new = rx.sub(tag, was)
    if new != was:
        open(p, 'w', encoding='utf-8', newline='\n').write(new)
        n += 1
    print(f'brand: {n} files, {len(ver)} images', file=sys.stderr)


def font_version():
    """?v=<hash> on every assets/fonts/<file>.woff2 address in the pages (@font-face and preload: the same address, or the
    preload is fetched twice) and in the worker's PRECACHE. Fonts cut again by tools/subset_fonts.py keep their names."""
    d = os.path.join(HERE, 'assets', 'fonts')
    ver = {f: hashlib.sha1(open(os.path.join(d, f), 'rb').read()).hexdigest()[:8] for f in os.listdir(d) if f.endswith('.woff2')}
    rx = re.compile(r'(assets/fonts/([\w-]+\.woff2))(?:\?v=\w+)?')
    tag = lambda m: m.group(1) + (f'?v={ver[m.group(2)]}' if m.group(2) in ver else '')
    n = 0
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('assets', 'content', 'i18n', 'tests', 'node_modules')]
        for f in files:
            if f.endswith('.html') and not f.endswith('.src.html') or root == HERE and f == 'sw.js':
                p = os.path.join(root, f)
                was = open(p, encoding='utf-8').read()
                new = rx.sub(tag, was)
                if new != was:
                    open(p, 'w', encoding='utf-8', newline='\n').write(new)
                    n += 1
    print(f'fonts: {n} files', file=sys.stderr)


def home_js():
    """The page script of each language home (all but the first-screen script before it) -> assets/home/<lang>.js?v=<hash>,
    asleep in the page like the LATE_FILES. Last of the page passes (after art_version), so its texts and addresses are final."""
    d = os.path.join(HERE, 'assets', 'home')
    os.makedirs(d, exist_ok=True)
    for lang in LANGS:
        p = os.path.join(HERE, page_dir(lang), 'index.html')
        html = open(p, encoding='utf-8').read()
        m = re.search(r"<script>\n(const HOME = ''.*?)</script>\n", html, re.S)
        assert m, p
        open(os.path.join(d, f'{lang}.js'), 'w', encoding='utf-8', newline='\n').write(m[1])
        v = hashlib.sha1(m[1].encode('utf-8')).hexdigest()[:10]
        tag = f'<script data-src="{rel(page_dir(lang), "")}assets/home/{lang}.js?v={v}"></script>\n'
        open(p, 'w', encoding='utf-8', newline='\n').write(html[:m.start()] + tag + html[m.end():])
    print(f'home: {len(LANGS)} scripts', file=sys.stderr)


def tools_js():
    """The page script of the tools page (tools.src.html <script data-js="tools">) -> assets/tools/<lang>.js?v=<hash>:
    the HTML is ~70 KB lighter and the script is kept by the browser and the worker between visits. Loaded with defer
    from <head>: fetched from the first bytes, run after the whole page is parsed and before every other deferred file
    (radio, search, me, hero, living), the order the inline script at the end of <body> had. Last of the page passes
    with home_js (after art_version), so its texts and addresses are final."""
    d = os.path.join(HERE, 'assets', 'tools')
    os.makedirs(d, exist_ok=True)
    for lang in LANGS:
        here = page_dir(lang, 'tools/')
        p = os.path.join(HERE, here, 'index.html')
        html = open(p, encoding='utf-8').read()
        m = re.search(r'<script data-js="tools">\n(.*?)</script>\n', html, re.S)
        assert m, p
        open(os.path.join(d, f'{lang}.js'), 'w', encoding='utf-8', newline='\n').write(m[1])
        v = hashlib.sha1(m[1].encode('utf-8')).hexdigest()[:10]
        html = html[:m.start()] + html[m.end():]
        assert html.count('</head>') == 1, p
        html = html.replace('</head>', f'<script src="{rel(here, "")}assets/tools/{lang}.js?v={v}" defer></script>\n</head>')
        open(p, 'w', encoding='utf-8', newline='\n').write(html)
    print(f'tools: {len(LANGS)} scripts', file=sys.stderr)


def pwa(html, lang, root):
    a = APP[lang]
    head = (f'<link rel="manifest" href="{root}manifest-{lang}.webmanifest">\n'
            f'<link rel="apple-touch-icon" href="{root}assets/icons/apple-touch-icon.png">\n'
            '<meta name="apple-mobile-web-app-title" content="Gabella WoW">\n</head>')
    js = PWA_JS.replace('@@R@@', root).replace('@@L@@', a['install_l']).replace('@@T@@', a['install'])
    return search(radio(html.replace('</head>', head, 1).replace('</body>', js + '</body>', 1), lang, root), lang, root)


# ---------- home page ----------

# «Обновлено <date>» under the title of a guide, class, race or tools page and dateModified in its JSON-LD: the day the
# page's content sources last changed. Today while one of them has uncommitted changes, else the date of its last commit.
GIT_ROOT = os.path.dirname(HERE) if os.environ.get('WF_STAGED') else HERE   # the staged build runs in .build/, git is one level up
UPD_SRC = {'guides/leveling-': ('content/class_guides.py',),   # the nine class guides: their own texts (the order is checked first)
           'guides/builds-': ('content/spec_builds.py',),
           'guides/spec-': ('content/spec_cheats.py', 'content/spec_builds.py', 'content/class_guides.py', 'data/gear30.json'),
           'guides/dungeons/': ('content/dungeon_pages.py', 'content/guides.py'),   # the list and the pages of single dungeons
           'guides/': ('content/guides.py', 'i18n/guides.ru.txt', 'i18n/guides.en.txt', 'i18n/guides.uk.txt'),
           'classes/': ('content/classes.py',), 'races/': ('content/races.py',),
           'talents/': ('talents.py', 'content/talents'),   # the calculator: the engine and the trees
           'tools/': ('tools.src.html', 'i18n/tools.ru.txt', 'content/classes.py', 'content/races.py')}
NO_UPD = {'guides/news/'}   # the news feed refreshes itself
_SRC_DATES = {}


def src_date(files):
    """'dd.mm.yyyy' of the last change to these files (paths from the repo root)."""
    if files not in _SRC_DATES:
        git = lambda *a: subprocess.run(['git', '-C', GIT_ROOT, *a, '--', *files], capture_output=True, text=True, check=True).stdout.strip()  # noqa: E731
        try:
            day = '' if git('status', '--porcelain') else git('log', '-1', '--format=%cs')
        except (OSError, subprocess.CalledProcessError):
            day = ''
        _SRC_DATES[files] = (datetime.date.fromisoformat(day) if day else datetime.date.today()).strftime('%d.%m.%Y')
    return _SRC_DATES[files]


def page_updated(path):
    """Update date of a page (site-relative directory, 'guides/faq/'), None for pages without one (home, news, play, privacy)."""
    if path in NO_UPD:
        return None
    return next((src_date(f) for pre, f in UPD_SRC.items() if path.startswith(pre)), None)


def set_updated(html, path):
    """Fill the «Обновлено @@UPDATED@@» line (already translated) of a page, or drop it when the page has no date."""
    d = page_updated(path)
    if not d:
        return re.sub(r'\n?[ \t]*<p class="upd">.*?</p>', '', html, count=1, flags=re.S)
    return html.replace('@@UPDATED@@', f'<time datetime="{"-".join(reversed(d.split(".")))}">{d}</time>')

# ru/uk home: one quiet line above the footer on how to play in the language; once closed (or followed), never again.
GAME_HINT = {'ru': ('В игре есть русский язык.', 'Как включить', 'guides/faq/#language', 'Закрыть'),
             'uk': ('Українською грають з аддоном.', 'Як встановити', 'guides/ukrainian/', 'Закрити')}
GAME_JS = """<script>
(function () {
  var KEY = 'gabella-game-lang', bar = document.getElementById('gamehint'), seen = '1';
  try { seen = localStorage.getItem(KEY); } catch (e) {}
  if (seen) return;
  var done = function () { try { localStorage.setItem(KEY, '1'); } catch (e) {} };
  bar.hidden = false;
  bar.querySelector('a').addEventListener('click', done);
  bar.querySelector('button').addEventListener('click', function () { done(); bar.remove(); });
})();
</script>
"""


def game_hint(lang):
    text, link, href, close = GAME_HINT[lang]
    return (f'<div class="gamehint" id="gamehint" hidden><span>{text} <a href="{href}">{link}</a></span>'
            f'<button type="button" aria-label="{close}"><svg class="ico" aria-hidden="true"><use href="#i-x"/></svg></button></div>\n'
            + GAME_JS)


def fresh(lang):
    """«Свежее» at the bottom of the home hero: the three newest of our notes on the game (content.guides.NEWS), in the page
    language and their source; each opens its place on the news page. The page script merges the newest Wowhead headlines in (assets/news.json).
    The site updates (updates.json) stay the Discord feed and the news page."""
    from content.guides import NEWS
    langs.fill(NEWS)
    items = sorted(((n['date'], n['title'][lang], n['url']) for n in NEWS), key=lambda x: x[0], reverse=True)   # same day: the order of NEWS (newest first)
    host = lambda u: re.sub(r'^www\.', '', u.split('/')[2])   # the source of the note, like «Wowhead» on the feed cards
    return ''.join(f'<a class="nc" href="guides/news/#ours" data-u="{esc(u)}"><time datetime="{d}">{d[8:10]}.{d[5:7]}</time><b>{esc(RU_MARK.sub(r"\1", t))}</b><span>{host(u)}</span></a>'
                   for d, t, u in items[:3])


DATA_SRC = ('content', 'i18n/names.json')   # the game data of the site: its last commit dates the «Данные: … · обновлено» home line


def data_updated():
    """<time> of the last change to the game data (DATA_SRC), dd.mm on the page."""
    d = src_date(DATA_SRC)
    return f'<time datetime="{"-".join(reversed(d.split(".")))}">{d[:5]}</time>'


SLEEP_ART = ('pickban', 'guides', 'camp')   # home blocks under the first screen


def sleep_art(html):
    """Pictures of the SLEEP_ART blocks wait asleep (data-lsrcset, data-lsrc) and LATE_JS wakes them with the other late files.
    The home is short now: lazy loading alone fetched them at once on a phone (Chrome loads lazy pictures up to 1250–2500 px
    below the screen), and they shared the line with the hero picture before it was painted: −2 Lighthouse points."""
    def nap(m):
        return re.sub(r'<img src="', '<img data-lsrc="', re.sub(r'<source([^>]*?) srcset="', r'<source\1 data-lsrcset="', m[0]))
    for sid in SLEEP_ART:
        html, n = re.subn(rf'<section class="[^"]*" id="{sid}">.*?</section>', nap, html, count=1, flags=re.S)
        assert n, sid
    return html


def home_specs():
    """Home «Билды и таланты»: nine classes, each with the chips of its three spec cheat sheets (Russian, translate() does the rest)."""
    rows = ''
    for c in CLASSES:
        chips = ''.join(f'<li><a href="guides/spec-{c["id"]}-{sid}/"><b>{esc(s["n"])}</b><span>{" · ".join(ROLE[r] for r in s["roles"])}</span></a></li>'
                        for s, sid in zip(c['specs'], SPEC_IDS[c['id']]))
        rows += f'<div class="spcls"><a class="spn" href="guides/builds-{c["id"]}/">{esc(c["n"])}</a><ul class="spchips">{chips}</ul></div>'
    return rows


def build_home(lang, src):
    src = src.replace('@@SPECS@@', home_specs())
    src = src.replace('@@RACE_LEAD@@', json.dumps({r['id']: r['lead'] for r in RACES_PAGE}, ensure_ascii=False))
    src = src.replace('@@RACE_SLUG@@', json.dumps({r['id']: r['slug'] for r in RACES_PAGE}))
    src = re.sub(r'/\* data:start .*?/\* data:end \*/\n', '', src, count=1, flags=re.S)   # read by the other builds, not used here
    src = chrome(src, tab='', home='')
    html, missing = translate(src, lang)
    html = html.replace('@@FRESH@@', fresh(lang)).replace('@@DATA_UPD@@', data_updated())
    html = sleep_art(html).replace('<b>Gruppenplaner</b>', '<b>Gruppen&shy;planer</b>')   # 320 px tile: a hyphen, not «Gruppenplane / r»
    html = tod.apply(html, lang, amb=True)   # the hero in the reader's time of day (tod.py)
    here = page_dir(lang)
    html = html.replace('@@ALTERNATES@@', alternates(''))
    html = localize(html, lang, here)
    html = static_links(html, lang, '')
    html = home_dungeons(html, lang)
    if lang in GAME_HINT:
        html = html.replace('<footer id="sources"', game_hint(lang) + '<footer id="sources"', 1)
    if lang == 'ru':
        html = auto_lang(html)
    if lang != 'ru':
        for tag in ('rel="canonical" href', 'property="og:url" content'):
            html = html.replace(tag + f'="{SITE}"', tag + f'="{SITE}{lang}/"')
        html = html.replace('assets/og-ru.jpg', f'assets/og-{lang}.jpg')
    return here + 'index.html', html, missing


# ---------- class pages ----------

RACE_RX = re.compile(r"\{ id:'(\w+)', n:'([^']+)', f:'(\w+)'(, paid:true)?(?:, name:'([^']+)')?,\s*cls:\[([^\]]*)\]")
ROLE = {'tank': 'Танк', 'heal': 'Лекарь', 'dps': 'Урон', 'tank?': 'Танк (под вопросом)'}
COLOR = {'warrior': '#c79c6e', 'paladin': '#f58cba', 'hunter': '#abd473', 'rogue': '#fff569', 'priest': '#e8e8e8', 'shaman': '#2f8cf0', 'mage': '#40c7eb', 'warlock': '#8788ee', 'druid': '#ff7d0a'}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


BETA_SPAN = '<span class="beta-note">по данным беты</span>'   # the one mark for facts the beta shows and Blizzard has not confirmed


def esc_b(s):
    """esc() plus: a {beta} marker in the text becomes the beta mark (the marker splits the translation segment, the key stays)."""
    return esc(s).replace('{beta}', BETA_SPAN)


# soft hyphen points for long spec names: the engraved caps font is wide and three spec tabs share a phone screen
HYPH = {w.replace('-', ''): w.replace('-', '&shy;') for w in (
    'Совер-шен-ство-вание', 'Вдо-ско-на-лен-ня', 'Не-по-міт-ність', 'Не-ис-тов-ство', 'Де-мо-но-ло-гия', 'Де-мо-но-ло-гія',
    'Лик-ви-да-ция', 'Лік-ві-да-ція', 'Раз-ру-ше-ние', 'Руй-ну-ван-ня', 'По-слу-ша-ние', 'Кол-дов-ство', 'Скрыт-ность',
    'Assas-si-na-tion', 'Marks-man-ship', 'Retri-bu-tion', 'Resto-ra-tion', 'Destruc-tion', 'Enhance-ment',
    'Afflic-tion', 'Demo-no-lo-gy', 'Disci-pline', 'Protec-tion',
    'Tier-herr-schaft', 'Treff-sicher-heit', 'Wieder-her-stel-lung', 'Ver-stär-kung', 'Gleich-ge-wicht', 'Dä-mo-no-lo-gie',
    'Zer-stö-rung', 'Ver-gel-tung',
    'Amé-lio-ra-tion', 'Res-tau-ra-tion', 'Dé-mo-no-lo-gie', 'Élé-men-taire', 'Assas-si-nat',
    'Demo-no-lo-gía', 'Des-truc-ción', 'Res-tau-ra-ción', 'Super-vi-ven-cia', 'Repren-sión', 'Equi-li-brio', 'Protec-ción', 'Disci-pli-na',
    'Aper-fei-ço-a-men-to', 'Assas-si-na-to', 'Demo-no-lo-gia', 'Des-trui-ção', 'Equi-lí-brio', 'Res-tau-ra-ção', 'Retri-bui-ção',
    'Sobre-vi-vên-cia', 'Sub-ter-fú-gio',
    'Af-fli-zio-ne', 'Ag-gres-so-re', 'As-sas-si-nio', 'Com-bat-ti-men-to', 'Di-stru-zio-ne', 'Ele-men-ta-le', 'Po-ten-zia-men-to',
    'Pre-ci-sio-ne', 'Pro-te-zio-ne', 'Ri-ge-ne-ra-zio-ne', 'Scal-trez-za', 'So-prav-vi-ven-za')}


def hyph_tabs(html):
    return re.sub(r'(role="tab"[^>]*>)([^<]+)', lambda m: m[1] + HYPH.get(m[2], m[2]), html)


def long_title(html):
    """A page title with an 11+ letter word gets class "long": on a phone it takes the next step of the scale (28)
    instead of breaking inside the word (the display caps are wide)."""
    def title(m):
        words = re.split(r'\s+', re.sub(r'<[^>]+>', ' ', m[2]).strip())   # a hyphenated word never breaks (HYPHENED below), so it counts whole
        n = max(map(len, words))
        return f'<h1{m[1]} class="long" style="--lw:{n}">' if n >= 11 and 'class=' not in m[1] else m[0]   # --lw: the CSS fits that word to the screen
    html = re.sub(r'<h1([^>]*)>(?=(.*?)</h1>)', title, html, count=1, flags=re.S)
    return re.sub(r'(<h1[^>]*>)(.*?)(</h1>)', lambda m: m[1] + HYPHENED.sub(r'<span style="white-space:nowrap">\1</span>', m[2]) + m[3], html, count=1, flags=re.S)


# «Чек-лист» in a title: the line breaks around the word, never at its hyphen («ЧЕК- / ЛИСТ» in the display caps); not inside a tag
HYPHENED = re.compile(r'(?<![\w-])([^\W\d_]+(?:-[^\W\d_]+)+)(?![^<>]*>)')


def mark_long(html):
    """Portrait cards: names with a 10+ letter word get class "long" and a smaller size (after translation, so every language)."""
    def name(m):
        return '<b class="long">' if max(len(w) for w in re.split(r'[\s-]+', m[1])) >= 10 else m[0]
    return re.sub(r'<a class="oc".*?</a>', lambda a: re.sub(r'<b>(?=([^<]+)</b>)', name, a[0]), html, flags=re.S)


def ability(ru, en, lang, tag='b'):
    """Ability name. ru: the ruRU client name (names.json, else the site's Russian) + the English original; de/fr/es/pt/it: the official name (i18n/names.json, Wowhead)
    + English; en/uk/pl: English only. tag wraps the main name; '' = bare text (race cards put it in their own h3)."""
    main = langs.NAMES.get(en, {}).get('ru') or ru if lang == 'ru' else langs.name(en, lang)
    if main == en:
        return f'<{tag or "span"} lang="en">{esc(en)}</{tag or "span"}>'
    head = f'<{tag}>{esc(main)}</{tag}>' if tag else esc(main)
    return f'{head}<span class="en" lang="en">{esc(en)}</span>'


JS_STR = re.compile(r"""'[^'\n]*'|"[^"\n]*\"""")


def js_quote(s, q):
    return q + s.replace(q, '’') + q


def js_names(js, lang):
    """English game names in quoted JS data (dungeons, zones, cities) -> official localized ones on de/fr/es/pt/it and
    the ruRU client names on ru (the English stays a search key). uk/en/pl keep English: there is no Ukrainian client."""
    if lang == 'ru':
        def one(m):                                                # names inside Russian text; an English string only as a whole
            s = m[0][1:-1]
            return js_quote(ru_plain(s) if re.search(f'[{CYR}]', s) else ru_word(s), m[0][0])

        def row(m):                                                # DUNGEONS row: «Мертвые копи (The Deadmines)», the rest in Russian
            ru = ru_word(m[2])
            return m[1] + js_quote(f'{ru} ({m[2]})' if ru != m[2] else ru, "'") + JS_STR.sub(one, m[3])
        e = js.find('const EN = {')                                # EN maps Russian names to English: keep its English
        if e >= 0:
            f = js.index('\n};', e)
            return js_names(js[:e], lang) + js[e:f] + js_names(js[f:], lang)
        i = js.find('const DUNGEONS = [')
        if i < 0:
            return JS_STR.sub(one, js)
        j = js.find('\n];', i) % (len(js) + 1)                     # home_dungeons passes the block without its end
        return JS_STR.sub(one, js[:i]) + re.sub(r"(?m)^(\s*\[)'([^'\n]*)'(.*)$", row, js[i:j]) + JS_STR.sub(one, js[j:])
    if lang not in NAMED:
        return js
    return JS_STR.sub(lambda m: js_quote(langs.name(m[0][1:-1], lang), m[0][0]), js)


RU_MARK = re.compile(r'\[\[([^\[\]|\n]+)\|([^\[\]|\n]+)\]\]')   # ru sources: [[Дуротаре|Durotar]] = the name in a case form
RU_SKIP = re.compile(r'<head\b.*?</head>|<script\b.*?</script>|<style\b.*?</style>|<(\w+)\b[^>]*\blang="en"[^>]*>.*?</\1>|<[^>]+>', re.S)
_ru_rx = []


def ru_word(en):
    """Russian client name of an English game name (names.json, Wowhead ruRU); English when the client has none."""
    return langs.NAMES.get(en, {}).get('ru') or en


def ru_rx():
    """[[форма|English]] markup (groups 1, 2) or a bare English name with a ruRU name (group 3), not inside a longer English phrase."""
    if not _ru_rx:
        names = sorted((en for en, v in langs.NAMES.items() if v.get('ru') and v['ru'] != en), key=len, reverse=True) or ['\0']
        _ru_rx.append(re.compile(RU_MARK.pattern + r'|(?<![A-Za-z’\'-])(?<![A-Za-z] )(?<!Mr\. )(' +'|'.join(map(re.escape, names))
                                 + r')(?![A-Za-z’-])(?! [A-Za-z])'))
    return _ru_rx[0]


JS_TEXT = re.compile(r"""'[^'\n]*'|"[^"\n]*"|`[^`]*`""")


def ru_plain(s):
    """Russian text outside the page flow (script strings, JSON-LD): names in the client's Russian, without the English."""
    def word(n):
        if n[3] and n.string[n.start() - 1:n.start()] == '(' and n.string[n.end():n.end() + 1] == ')':
            return n[0]                                            # «Мертвые копи (The Deadmines)»: the English stays
        return n[1] or ru_word(n[3])
    return ru_rx().sub(word, s)


def ru_names(html):
    """Russian pages: game names as the ruRU client shows them. The first mention on a page reads «Оргриммар (Orgrimmar)»,
    later ones «Оргриммар». Bare English names in the text are nominative; other cases come marked in the source
    as [[Оргриммаре|Orgrimmar]]. Head, scripts, attributes and lang="en" elements are left alone (markup there loses the English)."""
    rx = ru_rx()
    seen = set()

    def name(m):
        word, en = (m[1], m[2]) if m[1] else (ru_word(m[3]), m[3])
        s, a, b = m.string, m.start(), m.end()
        if s[:a].endswith('(') and s[:a - 1].rstrip().endswith(word):   # «Мертвые копи (The Deadmines)» as written, every time
            seen.add(en)
            return en
        if en in seen:
            return word
        if s[b:].lstrip(' ').startswith('(') or s[:a].endswith('('):   # not «(Hyjal Summit) (20)», «(Ремонтный робот (Repair Bot))»
            return word
        seen.add(en)
        return f'{word} ({en})'

    out, i = [], 0
    for m in RU_SKIP.finditer(html):
        out.append(rx.sub(name, html[i:m.start()]))
        block = m[0]
        if m[1]:                                                   # lang="en" element: its English counts as mentioned
            seen.add(re.sub(r'<[^>]+>', '', block).strip())
        elif block.startswith('<script'):                          # Russian strings in scripts: the client name, no English
            block = JS_TEXT.sub(lambda s: ru_plain(s[0]) if re.search(f'[{CYR}]', s[0]) else s[0], block)
        out.append(block)
        i = m.end()
    out.append(rx.sub(name, html[i:]))
    return RU_MARK.sub(r'\1', ''.join(out))


def home_dungeons(html, lang):
    """DUNGEONS on the home page: zone (and on de/fr/es/pt/it dungeon) names in the page language, as on the dungeon guide."""
    i = html.find('const DUNGEONS = [')
    if i < 0:
        return html
    j = html.index('\n];', i)
    return html[:i] + js_names(html[i:j], lang) + html[j:]


NEXT_H = langs.derive({'ru': 'Следующий шаг', 'en': 'Next step', 'uk': 'Наступний крок'})


def next_block(items, lang, home, cls=''):
    """«Next step» above «More on the site»: 1–3 descriptive links from the record's `next` field
    [(path from the language home, label)]; no field, no block. A label is a Russian string (translated as the page is)
    or a {'ru','en','uk'} dict. Class and race pages call it in Russian, before translate()."""
    if not items:
        return ''
    lab = lambda t: esc(langs.derive(dict(t))[lang] if isinstance(t, dict) else tr(t, lang))
    links = ''.join(f'<a href="{home}{h}"><span>{lab(t)}</span>{ico("arrow")}</a>' for h, t in items[:3])
    return (f'<section class="gnext{cls}" id="next"><div class="sec-head"><h2>{NEXT_H[lang]}</h2></div>'
            f'<nav class="nextl" aria-label="{NEXT_H[lang]}">{links}</nav></section>')


def ico(name):
    return f'<svg class="ico" aria-hidden="true"><use href="#i-{name}"/></svg>'


def ri(role):
    return f'<svg class="ri" aria-hidden="true"><use href="#i-{role.rstrip("?")}"/></svg>'


def parse_races(src):
    """RACES of the home page: classes, racial abilities [(a|p, name, what)] and the tip."""
    out = []
    block = src[src.index('const RACES = ['):]
    block = block[:block.index('\n];')]
    for m in RACE_RX.finditer(block):
        rid, n, fac, paid, name, cls = m.groups()
        can = {}
        for c in re.findall(r"'(\w+\*?)'", cls):
            can[c.rstrip('*')] = 'new' if c.endswith('*') else 'ok'
        rest = block[m.end():]
        nxt = RACE_RX.search(rest)
        body = rest[:nxt.start()] if nxt else rest
        rac = re.findall(r"\['([ap])','([^']+)','([^']+)'\]", body)
        tip = re.search(r"tip:'([^']+)'", body).group(1)
        out.append({'id': rid, 'n': name or n, 'f': fac, 'paid': bool(paid), 'can': can, 'rac': rac, 'tip': tip})
    return out


_RACES = []


def static_links(html, lang, home):
    """Plain links inside the class and race blocks the page script draws (home rosters, /classes/, /races/):
    the script replaces them, crawlers and readers without JS follow them."""
    if not _RACES:
        _RACES.extend(parse_races(open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()))
    slug = {r['id']: r['slug'] for r in RACES_PAGE}
    cls = ''.join(f'<a href="{home}classes/{c["id"]}/">{esc(tr(c["n"], lang))}</a>' for c in CLASSES)
    rac = lambda f=None: ''.join(f'<a href="{home}races/{slug[r["id"]]}/">{esc(tr(r["n"], lang))}</a>' for r in _RACES if f in (None, r['f']))
    for box, links in (('roster', cls), ('classRef', cls), ('rosterA', rac('alliance')), ('rosterH', rac('horde')), ('raceRef', rac())):
        html = html.replace(f' id="{box}"></div>', f' id="{box}">{links}</div>', 1)
    return html


def parse_en(src):
    """English names of specs and racial abilities from the EN map of the home page."""
    block = src[src.index('const EN = {'):]
    block = block[:block.index('};')]
    return {ru: a or b for ru, a, b in re.findall(r"'([^']+)':(?:'([^']+)'|\"([^\"]+)\")", block)}


def pic(cid, root, widths, sizes, cls='', lazy=True, side=None):
    """A class or race portrait. A class with side='alliance'/'horde': the portrait of that side (portraits());
    side='': the reader's side — the Alliance one in the page, swapped by GabellaPor (por_js) for the Horde before it loads."""
    art = portraits()[cid][side or 'alliance'] if cid in portraits() and side is not None else cid
    tpl = lambda ext, n: ', '.join(f'{root}assets/art/{n}-{w}.{ext} {w}w' for w in widths)
    swap = side == '' and cid in portraits()
    srcs = ''.join(f'<source type="image/{ext}" srcset="{tpl(ext, art)}"' + (f' data-por-srcset="{tpl(ext, "{" + cid + "}")}"' if swap else '') + f' sizes="{sizes}">' for ext in ('avif', 'webp'))
    load = ' loading="lazy"' if lazy else ''
    dsrc = f' data-por-src="{root}assets/art/{{{cid}}}-{widths[-1]}.webp"' if swap else ''
    return f'<picture{cls}>{srcs}<img src="{root}assets/art/{art}-{widths[-1]}.webp"{dsrc} width="896" height="1200" alt=""{load} decoding="async"></picture>'


# ---------- professions on a class page and in the compare tool: pairs of the Professions guide + camp objects of the home PROFS ----------

PROF_T = langs.fill({
    'h': {'ru': 'Профессии', 'en': 'Professions', 'uk': 'Професії'},
    'camp': {'ru': 'В лагере', 'en': 'In camp', 'uk': 'У таборі'},
    'note': {'ru': 'Пассивных бонусов у профессий в Forever нет: характеристики дают вещи, зелья и чары, которые вы делаете, и баффы объектов лагеря.',
             'en': 'Professions in Forever have no passive bonuses: stats come from the gear, potions and enchants you make, and from camp object buffs.',
             'uk': 'Пасивних бонусів у професій у Forever немає: характеристики дають речі, зілля й чари, які ви робите, і баффи об’єктів табору.'},
    'more': {'ru': 'Все пары, объекты лагеря и прокачка навыка', 'en': 'All pairs, camp objects and skill leveling',
             'uk': 'Усі пари, об’єкти табору й прокачування навички'},
})
_CAMP = {}


def camp_objects():
    """{profession id: (camp object, Russian effect)} from PROFS of the home page."""
    if not _CAMP:
        src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
        _CAMP.update({pid: (obj, eff) for pid, _n, _tier, obj, eff in re.findall(r"\['(\w+)', '([^']+)', (\d), '([^']+)', '([^']+)'\]", src)})
    return _CAMP


def class_profs(cid, lang):
    """Recommended pairs of a class in lang: ([(step label, pair, [(camp object, effect), …])] for leveling and level 60, why)."""
    from content.guides import CLASS_PAIRS, PAIR_HEAD
    L = lambda d: langs.derive(d)[lang]
    camp = camp_objects()
    _c, _n, lvl, cap, why = next(p for p in CLASS_PAIRS if p[0] == cid)
    steps = [(L(PAIR_HEAD[i]), L(pair[0]), [(camp[x][0], camp[x][1] if lang == 'ru' else t_of(camp[x][1], lang)) for x in pair[1]])
             for i, pair in ((1, lvl), (2, cap))]
    return steps, L(why)


def class_profs_short(cid, lang):
    """Compare tool: [[«step: pair», ''], [«step: pair», why]] — the shared reason goes under the last pair."""
    steps, why = class_profs(cid, lang)
    return [[f'{label}: {pair}', why if i == len(steps) - 1 else ''] for i, (label, pair, _camp) in enumerate(steps)]


def profs_panel(cid, lang):
    """Class page panel «Профессии»: pairs for leveling and level 60, why, their camp buffs, the no-passives note and a link to this class in the guide."""
    tx = {k: v[lang] for k, v in PROF_T.items()}
    steps, why = class_profs(cid, lang)
    items = ''.join(f'<li><b>{esc(label)}: {esc(pair)}</b>'
                    f'<span class="pcamp"><svg class="ico" aria-hidden="true"><use href="#i-fire"/></svg><span>{tx["camp"]}: '
                    + '; '.join(f'{esc(o)} — {esc(e)}' for o, e in camp) + '</span></span></li>'
                    for label, pair, camp in steps)
    return (f'<div class="panel cprofs" id="profs"><h3>{tx["h"]}</h3><ul class="cpairs">{items}</ul>'
            f'<p class="cwhy">{esc(why)}</p><p class="small">{esc(tx["note"])}</p>'
            f'<a class="pmore" href="@@HOME@@guides/professions/#pairs={cid}">{tx["more"]}{ico("arrow")}</a></div>')


def render_class(c, races, lang):
    i = next(k for k, x in enumerate(CLASSES) if x['id'] == c['id'])
    roles = ''.join(f'<a href="@@HOME@@guides/spec-{c["id"]}-{sid}/">{ri(s["roles"][0])}<b>{esc(s["n"])}</b><small>{" · ".join(ROLE[r] for r in s["roles"] if not r.endswith("?"))}</small></a>'
                    for s, sid in zip(c['specs'], SPEC_IDS[c['id']]))   # the hero: the three spec sheets (build, talents) one tap from the first screen
    facts = ''.join(f'<div><dt>{k}</dt><dd>{esc_b(v)}</dd></div>' for k, v in (('Броня', c['armor']), ('Вооружение', c['weapons']), ('Ресурс', c['resource']), ('Прокачка', c['lvl'])))
    tabs, panels = [], []
    for k, s in enumerate(c['specs']):
        on = k == 0
        tabs.append(f'<button type="button" role="tab" id="tab-{k}" aria-controls="spec-{k}" aria-selected="{"true" if on else "false"}" tabindex="{0 if on else -1}">{esc(s["n"])}<small>{" · ".join(ROLE[r] for r in s["roles"])}</small></button>')
        keys = ''.join(f'<li><div>{ability(ru, en, lang)}</div><span class="d">{esc(d)}</span></li>' for ru, en, d in s['keys'])
        panels.append(f'<div class="spanel" role="tabpanel" id="spec-{k}" aria-labelledby="tab-{k}" tabindex="0"{"" if on else " hidden"}>'
                      f'<div class="about"><p class="what">{"".join(ri(r) for r in s["roles"])}{esc(s["what"])}</p><p class="style">{esc(s["style"])}</p>'
                      f'<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Совет</span>{esc(s["tip"])}</p></div>'
                      f'<div class="sbtns"><a class="btn ghost ttree" href="@@HOME@@guides/builds-{c["id"]}/#{SPEC_IDS[c["id"]][k]}">Дерево талантов</a>'
                      f'<a class="btn ghost ttree" href="@@HOME@@guides/spec-{c["id"]}-{SPEC_IDS[c["id"]][k]}/">Шпора спека</a></div></div>'
                      f'<ul class="keys" aria-label="Ключевые способности">{keys}</ul></div>')
    news = ''.join(f'<li><span>{esc(x)}</span></li>' for x in c['news'])   # one grid cell next to the number
    side = []
    for fac, title in (('alliance', 'Альянс'), ('horde', 'Орда')):
        items = []
        for r in races:
            if r['f'] != fac or c['id'] not in r['can']:
                continue
            tags = ('<span class="tag new">новое</span>' if r['can'][c['id']] == 'new' else '') + ('<span class="tag paid">платная</span>' if r['paid'] else '')
            items.append(f'<li><a href="@@HOME@@tools/#pick={r["id"]}.{c["id"]}"><span class="rn">{esc(r["n"])}</span>{tags}<span class="go">В подборщик{ico("arrow")}</span></a></li>')
        body = f'<ul>{"".join(items)}</ul>' if items else '<p class="none">Нет доступных рас</p>'
        side.append(f'<div class="fside {fac}"><h3>{title}</h3>{body}</div>')
    group = ''.join(f'<li>{esc(x)}</li>' for x in c['group'])
    pros = ''.join(f'<li>{esc(x)}</li>' for x in c['pros'])
    cons = ''.join(f'<li>{esc(x)}</li>' for x in c['cons'])
    return {
        'ID': c['id'], 'COLOR': COLOR[c['id']], 'DESC': esc(c['desc']), 'ROLES': roles, 'FACTS': facts,
        'TABS': ''.join(tabs), 'PANELS': ''.join(panels), 'NEWS': news, 'RACES': ''.join(side),
        'RACES_TIP': esc(c['races_tip']), 'GROUP': group, 'LVL': esc(c['lvl']), 'BEST_RACE': esc(c['best_race']),
        'PROS': pros, 'CONS': cons,
        'PREV': CLASSES[i - 1], 'NEXT': CLASSES[(i + 1) % len(CLASSES)],
    }


def class_guide_title(cid, lang):
    """Title of the class leveling guide (guides/leveling-<class>/) in the page language."""
    from content.guides import GUIDES
    g = next(x for x in GUIDES if x['slug'] == f'leveling-{cid}')
    return langs.fill(g['title'])[lang]


QS = {   # I3 «Quick start» plate on a class page: heading, then the four labels
    'ru': ('Быстрый старт', 'Спек для прокачки', 'Профессии на прокачке', 'Раса за Альянс', 'Раса за Орду'),
    'en': ('Quick start', 'Leveling spec', 'Leveling professions', 'Alliance race', 'Horde race'),
    'uk': ('Швидкий старт', 'Спек для прокачування', 'Професії на прокачуванні', 'Раса за Альянс', 'Раса за Орду'),
    'de': ('Schnellstart', 'Skillung zum Leveln', 'Berufe beim Leveln', 'Volk der Allianz', 'Volk der Horde'),
    'fr': ('Démarrage rapide', 'Spé pour monter', 'Métiers pour monter', 'Race de l’Alliance', 'Race de la Horde'),
    'es': ('Inicio rápido', 'Espec. para subir', 'Profesiones para subir', 'Raza de la Alianza', 'Raza de la Horda'),
    'it': ('Avvio rapido', 'Spec per livellare', 'Professioni per livellare', 'Razza dell’Alleanza', 'Razza dell’Orda'),
    'pt': ('Início rápido', 'Espec. para upar', 'Profissões para upar', 'Raça da Aliança', 'Raça da Horda'),
    'pl': ('Szybki start', 'Spec do levelowania', 'Profesje do levelowania', 'Rasa Alliance', 'Rasa Horde'),
}


def quick_start(cid, lang):
    """I3: one plate under the class hero — the leveling spec (tier list), the best race of each faction for PvE
    (best-race summary), the leveling professions (Professions guide) and the links to the class guides.
    Everything comes from the guides themselves, so the plate never disagrees with them."""
    from content.guides import GUIDES
    g = {x['slug']: x for x in GUIDES}
    L = lambda d: langs.derive(d)[lang] if isinstance(d, dict) else d   # noqa: E731
    def rows(slug, sec):
        for kind, data in next(x for x in g[slug]['sections'] if x['id'] == sec)['blocks']:
            if kind == 'table':
                return data['rows']
    lvl = next(r[1] for r in rows('tier-list', 'leveling') if isinstance(r[1], tuple) and r[1][1] == f'guides/leveling-{cid}/')
    spec = L(lvl[0]).partition(' · ')[2]
    race = next(r for r in rows('best-race', 'table') if r[0]['ru'] == next(c['n'] for c in CLASSES if c['id'] == cid))
    steps, _why = class_profs(cid, lang)
    h, *labels = QS[lang]
    vals = (spec, steps[0][1], L(race[1]), L(race[2]))
    dl = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in zip(labels, vals))
    links = [(f'guides/leveling-{cid}/', class_guide_title(cid, lang))]
    b = next((x for x in GUIDES if x['slug'] == f'builds-{cid}'), None)
    if b:
        links.append((f'guides/builds-{cid}/', langs.fill(b['title'])[lang]))
    links.append((f'guides/best-race/#{cid}', langs.fill(g['best-race']['crumb'])[lang]))
    a = ''.join(f'<a href="@@HOME@@{u}">{esc(t)}</a>' for u, t in links)
    return (f'<section class="wrap qstart" aria-labelledby="hQs"><div class="panel qs"><h2 id="hQs">{esc(h)}</h2>'
            f'<dl class="qsl">{dl}</dl><p class="qsa">{a}</p></div></section>')


def build_class(c, lang, tpl, base_css, sprite, races):
    here = page_dir(lang, f'classes/{c["id"]}/')
    root = rel(here, '')
    home = rel(here, page_dir(lang))
    v = render_class(c, races, lang)
    html = chrome(tpl.replace('@@BASE_CSS@@', base_css).replace('@@SPRITE@@', sprite), nav='classes/', tab='classes/')
    html = html.replace('@@POR_A@@', portraits()[c['id']]['alliance'])   # no JS: the Alliance portrait
    for k in ('ID', 'COLOR', 'DESC', 'ROLES', 'FACTS', 'TABS', 'PANELS', 'NEWS', 'RACES', 'RACES_TIP', 'GROUP', 'LVL', 'BEST_RACE', 'PROS', 'CONS'):
        html = html.replace(f'@@{k}@@', v[k])
    others = ''.join(f'<a class="oc" href="../{o["id"]}/" style="--cc:{COLOR[o["id"]]}">{pic(o["id"], root, (360,), "132px", side="")}<b>{esc(o["n"])}</b></a>' for o in CLASSES if o['id'] != c['id'])
    pager = (f'<a class="prev" href="../{v["PREV"]["id"]}/">{ico("arrow")}{esc(v["PREV"]["n"])}</a>'
             f'<a class="next" href="../{v["NEXT"]["id"]}/">{esc(v["NEXT"]["n"])}{ico("arrow")}</a>')
    toc = ''.join(f'<a href="../{o["id"]}/"{" aria-current=\"page\"" if o["id"] == c["id"] else ""}>{esc(o["n"])}</a>' for o in CLASSES)
    links = [(n, s.format(id=c['id'])) for n, s in SOURCES]
    sources = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in links)
    html = html.replace('@@OTHERS@@', others).replace('@@PAGER@@', pager).replace('@@TOC_CLASSES@@', toc).replace('@@SOURCES@@', sources)
    html = html.replace('@@NEXT@@', next_block(c.get('next'), 'ru', home, ' block wrap'))

    html, missing = translate(html, lang)
    html = set_updated(html, f'classes/{c["id"]}/')
    html = html.replace('@@QSTART@@', quick_start(c['id'], lang))
    html = html.replace('@@PROFS@@', profs_panel(c['id'], lang))   # already in lang: the pairs come from the Professions guide
    html = html.replace('@@NAME@@', esc(tr(c['n'], lang)))
    html = mark_long(hyph_tabs(html))
    html = html.replace('@@HOME@@', home)
    html = html.replace('@@CANON@@', SITE + here)
    html = html.replace('@@ALTERNATES@@', alternates(f'classes/{c["id"]}/'))
    html = localize(html, lang, here)
    return here + 'index.html', html, missing


# ---------- race pages ----------

FAC = {'alliance': 'Альянс', 'horde': 'Орда'}
FHERO = {'alliance': '#86a6d8', 'horde': '#d98a84'}
NCLS = {4: 'Четыре класса', 5: 'Пять классов', 6: 'Шесть классов', 7: 'Семь классов'}
SKY_SUB = {'skyA': 'Скайборн за Альянс', 'skyH': 'Скайборн за Орду'}


PLACE_FACTS = ('Столица', 'Стартовая зона', 'Репутация')


def fact_ru(k, v):
    """Russian race page: places and factions by their English game name, which ru_names turns into the ruRU client name
    + (English); the Russian source stays the translation key. Site-named factions (Высший орден) keep their Russian name."""
    if k in PLACE_FACTS and v in T and t_of(v, 'uk') == t_of(v, 'en'):
        return t_of(v, 'en')
    return v


def build_race(rp, lang, tpl, base_css, class_css, sprite, races, en):
    r = next(x for x in races if x['id'] == rp['id'])
    slug = {x['id']: x['slug'] for x in RACES_PAGE}
    i = next(k for k, x in enumerate(RACES_PAGE) if x['id'] == rp['id'])
    here = page_dir(lang, f'races/{rp["slug"]}/')
    root = rel(here, '')
    home = rel(here, page_dir(lang))
    classes_dir = rel(here, page_dir(lang, 'classes/'))

    facts = ''.join(f'<div><dt>{k}</dt><dd>{esc(fact_ru(k, v) if lang == "ru" else v)}</dd></div>' for k, v in rp['facts'])
    cards = []
    for kind, ru, what in r['rac']:
        name = ability(ru, en.get(ru, ru), lang, tag='')
        new = '<span class="tag new">новое</span>' if ru in NEW_RACIALS else ''
        cards.append(f'<article class="rcard"><div class="rt"><span class="k{" a" if kind == "a" else ""}">{"Активная" if kind == "a" else "Пассивная"}</span>{new}</div><h3>{name}</h3><p>{esc_b(what)}</p></article>')
    priest = ''
    if rp['priest']:
        sp = ', '.join(ability(n, n, lang) + (' <span class="tag new">новое</span>' if nw else '') for n, nw in rp['priest'])
        priest = f'<p class="pspells">Свои заклинания жреца: {sp}.</p>'

    cls_cards = []
    for c in CLASSES:
        if c['id'] not in r['can']:
            continue
        tags = '<span class="tags"><span class="tag new">новое</span></span>' if r['can'][c['id']] == 'new' else ''
        cls_cards.append(f'<a class="oc" href="@@HOME@@tools/#pick={r["id"]}.{c["id"]}" style="--cc:{COLOR[c["id"]]}">{pic(c["id"], root, (360,), "132px", side=r["f"])}{tags}<b>{esc(c["n"])}</b><span class="go">В подборщик</span></a>')
    nope = [c['n'] for c in CLASSES if c['id'] not in r['can']]
    nope_html = ('<p class="nope">Недоступны: ' + ', '.join(f'<span>{esc(n)}</span>' for n in nope) + '.</p>') if nope else ''

    news = ''.join(f'<li><span>{esc_b(x)}</span></li>' for x in rp['news'])
    cn = {c['id']: c['n'] for c in CLASSES}
    best = ''.join(f'<li><a href="{classes_dir}{cid}/">{esc(cn[cid])}</a><span>{esc(why)}</span></li>' for cid, why in rp['best'])

    others = ''
    for fac in ('alliance', 'horde'):
        cards_o = ''.join(f'<a class="oc" href="../{slug[o["id"]]}/" style="--cc:var(--{fac})">{pic(slug[o["id"]], root, (360,), "132px")}<b>{esc(o["n"])}</b></a>'
                          for o in races if o['f'] == fac and o['id'] != r['id'])
        others += f'<div class="ofac {fac}"><h3>{FAC[fac]}</h3><div class="others">{cards_o}</div></div>'
    prev, nxt = RACES_PAGE[i - 1], RACES_PAGE[(i + 1) % len(RACES_PAGE)]
    rn = {x['id']: x['n'] for x in races}
    pager = (f'<a class="prev" href="../{prev["slug"]}/">{ico("arrow")}{esc(rn[prev["id"]])}</a>'
             f'<a class="next" href="../{nxt["slug"]}/">{esc(rn[nxt["id"]])}{ico("arrow")}</a>')
    cur = ' aria-current="page"'
    toc = ''.join(f'<a href="../{slug[o["id"]]}/"{cur if o["id"] == r["id"] else ""}>{esc(o["n"])}</a>' for o in races)
    sources = ''.join(f'<li><a href="{u.format(wt=rp["wt"])}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in RACE_SOURCES)

    v = {
        'ID': r['id'], 'ART': rp['slug'], 'FCOLOR': f'var(--{r["f"]})', 'FHERO': FHERO[r['f']], 'FACTION': FAC[r['f']],
        'PAID': ' <span class="tag paid">платная</span>' if r['paid'] else '',
        'SUB': f'<p class="sub">{SKY_SUB[r["id"]]}</p>' if r['id'] in SKY_SUB else '',
        'DESC': esc(rp['lead']), 'FACTS': facts, 'BEST': rp['best'][0][0], 'RACIALS': ''.join(cards), 'PRIEST': priest,
        'NCLS': NCLS[len(r['can'])], 'CLASSES': ''.join(cls_cards), 'NOPE': nope_html, 'NEWS': news,
        'LORE': esc(rp['lore']), 'TIP': esc(r['tip']), 'BESTLIST': best, 'OTHERS': others, 'PAGER': pager,
        'TOC_RACES': toc, 'SOURCES': sources, 'NEXT': next_block(rp.get('next'), 'ru', home, ' block wrap'),
    }
    html = tpl.replace('@@BASE_CSS@@', base_css).replace('@@CLASS_CSS@@', class_css).replace('@@SPRITE@@', sprite)
    html = chrome(html, nav='races/')
    for k, val in v.items():
        html = html.replace(f'@@{k}@@', val)
    html, missing = translate(html, lang)
    html = set_updated(html, f'races/{rp["slug"]}/')
    html = html.replace('@@NAME@@', esc(tr(r['n'], lang)))
    html = mark_long(html)
    html = html.replace('@@HOME@@', home)
    html = html.replace('@@CANON@@', SITE + here)
    html = html.replace('@@ALTERNATES@@', alternates(f'races/{rp["slug"]}/'))
    html = localize(html, lang, here)
    return here + 'index.html', html, missing


def main():
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    tpl = open(os.path.join(HERE, 'class.src.html'), encoding='utf-8').read()
    rtpl = open(os.path.join(HERE, 'race.src.html'), encoding='utf-8').read()
    class_css = tpl[tpl.index('/* Class page'):tpl.index('</style>')].strip('\n')
    base_css = src[src.index('<style>') + 7:src.index('</style>')].strip('\n')
    s0 = src.index('<svg width="0" height="0"')
    sprite = src[s0:src.index('</svg>', s0) + 6]
    races = parse_races(src)
    assert len(races) == 10 and all(len(r['rac']) == 4 for r in races), [(r['id'], len(r['rac'])) for r in races]
    assert [r['id'] for r in races] == [r['id'] for r in RACES_PAGE]
    en = parse_en(src)

    pages, allmissing = [], []
    for lang in LANGS:
        for path, html, missing in [build_home(lang, src)] + [build_class(c, lang, tpl, base_css, sprite, races) for c in CLASSES] \
                + [build_race(rp, lang, rtpl, base_css, class_css, sprite, races, en) for rp in RACES_PAGE]:
            assert '@@' not in html, (path, re.findall(r'@@\w+@@', html)[:5])
            pages.append((path, html))
            allmissing += missing

    listing = '--list' in sys.argv
    if not listing:
        for path, html in pages:
            full = os.path.join(HERE, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, 'w', encoding='utf-8', newline='\n').write(html)
        for lang in LANGS:
            open(os.path.join(HERE, f'manifest-{lang}.webmanifest'), 'w', encoding='utf-8', newline='\n').write(manifest(lang) + '\n')
        sw_version()
    uniq = list(dict.fromkeys(allmissing))
    if listing and '--missing' not in sys.argv:
        print('\n'.join(uniq))
    print(f'pages: {len(pages)}, missing: {len(uniq)}', file=sys.stderr)
    if uniq and not listing:
        sys.exit(1)

    sys.path.insert(0, os.path.join(HERE, 'tools'))
    import export_game  # game rules for profiles -> assets/game.json (the API copies it with npm run sync)
    export_game.main()
    import build_me  # profile texts -> assets/me/i18n-<lang>.json
    build_me.main()
    import build_tools  # the tools page has its own builder and translations
    build_tools.main()
    import build_guides  # guides: own builder, texts already in three languages
    build_guides.main()
    import build_cards  # share pages b/<race>-<class>-<spec>/ of built characters (noindex, outside sitemap.xml)
    build_cards.main()
    import build_talent_links  # share pages t/<class>-<spec>/ of a talent build (noindex, outside sitemap.xml)
    build_talent_links.main()
    import seo  # last: titles/descriptions for search, JSON-LD, analytics, sitemap.xml over the built pages
    from content import spec_cheats  # noqa: E402
    seo.META.update(spec_cheats.SEO)   # the four spec cheat sheets: title and description for the search
    seo.main()
    report_new_langs()
    if not listing:
        import search  # site search index over the finished pages; it changes assets/, so the worker version is taken again
        search.main()
        brand_version()
        css_version()   # before the stylesheets are hashed
        art_version()   # before me.js and radio.js are hashed: it fills in their portrait versions
        me_version()
        living_version()
        radio_version()
        tod_version()
        hero_version()
        og_version()
        font_version()
        home_js()
        tools_js()
        sw_version()


def report_new_langs():
    """New languages: bad characters in translations fail the build; --missing prints the translator template,
    otherwise untranslated strings fail the build (the page would show English in their place)."""
    bad = [(l, en, x) for l in langs.NEW for en, x in langs.OV[l].items() if not langs.check_chars(en, x)]
    assert not bad, bad[:5]
    if '--missing' in sys.argv:
        lang = os.environ['WF_LANG']
        sys.stdout.reconfigure(encoding='utf-8')
        print(langs.missing_json(lang, langs.MISSING[lang]))
        return
    gaps = {l: len(set(langs.MISSING[l])) for l in langs.NEW if langs.MISSING[l]}
    if gaps:
        print(f'untranslated: {gaps} (python build.py --missing <lang>)', file=sys.stderr)
        sys.exit(1)


STAGE = '.build'
STAGE_SKIP = {'docs', 'node_modules', '__pycache__'}   # and every dot folder: git, local tools, the stage itself


def staged():
    """Build in a copy of the tree (.build/), then move the files that changed into place. A build that fails halfway
    (an untranslated fragment, a failed check) used to leave 180 half-built pages in the tree; now it leaves nothing."""
    tmp = os.path.join(HERE, STAGE)
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.copytree(HERE, tmp, ignore=lambda d, names: [n for n in names if n in STAGE_SKIP or n.startswith('.')])
    try:
        code = subprocess.run([sys.executable, os.path.join(tmp, 'build.py')] + sys.argv[1:], env={**os.environ, 'WF_STAGED': '1'}).returncode
        if code:
            print(f'build failed (exit {code}): the tree is untouched', file=sys.stderr)
            sys.exit(code)
        n = 0
        for d, dirs, files in os.walk(tmp):
            dirs[:] = [x for x in dirs if x != '__pycache__']   # the inner run's bytecode is not a build result
            for f in files:
                src = os.path.join(d, f)
                dst = os.path.join(HERE, os.path.relpath(src, tmp))
                if os.path.isfile(dst) and read_norm(dst) == read_norm(src):
                    continue
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                os.replace(src, dst)
                n += 1
        print(f'staged: {n} files changed', file=sys.stderr)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main() if os.environ.get('WF_STAGED') else staged()
