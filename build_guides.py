"""Сборка гайдов: guide.src.html + content/guides.py -> guides/[slug/]index.html, en/…, uk/….
Обвязка шаблона переводится через i18n/{ru,en,uk}.txt + i18n/guides.*.txt (строка в строку);
тело подставляется ПОСЛЕ перевода — тексты гайдов уже на трёх языках, translate() их не видит.
Запуск: python build_guides.py [--list]  (--list печатает русские фрагменты обвязки без перевода)"""
import json, os, re, sys
from html import escape
from urllib.parse import quote

import build
import seo
import talents
import tod
from build import LANGS, SITE, page_dir, rel, localize, translate
import langs
from content import hero as HERO, looks as LK
from content import spec_cheats
from content import dungeon_pages
from content.guides import BUILDS_HUB_TILE, CLASS_HUB_TILE, GUIDES, HUB, HUBS, NEWS, NEWS_SO, NOT_FOUND, ORDER, PAGES, PLAY_MILESTONES, PLAY_TX

HERE = build.HERE

_ru, _en, _uk = (build.load(f'guides.{l}.txt') for l in langs.OLD)
assert len(_ru) == len(_en) == len(_uk), (len(_ru), len(_en), len(_uk))
build.T.update({r: (e, u) for r, e, u in zip(_ru, _en, _uk)})
langs.fill([GUIDES, HUB, HUBS, NEWS, NEWS_SO, NOT_FOUND, PAGES, CLASS_HUB_TILE, BUILDS_HUB_TILE, HERO.TX, HERO.BEST])   # new languages of every guide text: i18n/<lang>.json by the English one

SS_TILE = next(g for g in GUIDES if g['slug'] == 'server-status')['tile']   # «Статус, очередь на вход, слои, техработы»: the launch card on Launch day
TIP = {'ru': 'Совет', 'en': 'Tip', 'uk': 'Порада'}
THIS_PAGE = {'ru': 'Эта страница', 'en': 'This page', 'uk': 'Ця сторінка'}
MORE_H = {'ru': 'Другие гайды', 'en': 'Other guides', 'uk': 'Інші гайди'}
MORE_SITE = {'ru': 'Ещё на сайте', 'en': 'More on the site', 'uk': 'Ще на сайті'}
# Extra tiles under the classes/ and races/ pages: the guides hub and the tools page
SITE_TILES = [
    {'t': HUB['title'], 'href': 'guides/', 'art': 'hero_guides',
     'd': {'ru': 'Прокачка, подземелья, профессии и ответы', 'en': 'Leveling, dungeons, professions and answers', 'uk': 'Прокачка, підземелля, професії та відповіді'}},
    {'t': {'ru': 'Конструктор группы и подборщик', 'en': 'Group builder and picker', 'uk': 'Конструктор групи та підбірник'}, 'href': 'tools/', 'art': 'hero_tools',
     'd': {'ru': 'Раса и класс под роль, рамки группы и рейда', 'en': 'Race and class for a role, party and raid frames', 'uk': 'Раса й клас під роль, рамки групи та рейду'}},
    {'t': {'ru': 'В игре', 'en': 'In game', 'uk': 'У грі'}, 'href': 'play/', 'art': 'hero_campfire',
     'd': {'ru': 'Второй экран: радио, уровень, таймеры', 'en': 'Second screen: radio, level, timers', 'uk': 'Другий екран: радіо, рівень, таймери'}},
]
# Wide hero art; everything else is a class/race portrait cut at 360/600/896/1344
WIDTHS = {'hero_dawn': (960, 1440, 1920, 2560, 3840), 'hero_campfire': (960, 1600, 2560),
          'hero_tools': (960, 1440, 1920, 2560)}   # the tools scene is also the Tools tile
FX = {'hero_dawn': 'dawn'}   # living art (assets/living/living.js) over these heroes
# A guide with 'hero' gets the full-screen inner page hero (.thero, like roster and tools): its own scene, living art,
# a portrait cut on phones (tools/make_images.py INNER, CUTS); 'art' stays for the tiles and the share preview.
THERO = {'hero_guides': 'guides', 'hero_dungeons': 'dungeons', 'hero_professions': 'professions', 'hero_faq': 'faq',
         'hero_news': 'news', 'hero_leveling': 'leveling', 'hero_classes': 'classes', 'hero_races': 'races',
         'hero_ukrainian': 'ukrainian', 'hero_requirements': None, 'hero_roster': 'roster',
         'hero_bestrace': 'bestrace', 'hero_tierlist': 'tierlist', 'hero_night': None, 'hero_dusk': None}   # hero_night: the home night scene (Launch day); hero_dusk: Name reservation
THERO_CUT = {'hero_bestrace': '.5', 'hero_tierlist': '.65'}   # phone cut other than .9 (tools/make_images.CUTS)
THERO_W = (960, 1440, 1920, 2560)
THERO_BIG = THERO_W + (3840,)   # the hero picture itself: 3440 and 4K screens take the 3840
WIDTHS.update({h: THERO_W for h in THERO})   # a page's own scene is also its tile (cut 4:3 by the tile) and share preview


LAUNCH_UTC = '23:00 UTC'
YOUR = {'ru': 'по вашему времени', 'en': 'your time', 'uk': 'за вашим часом', 'de': 'deine Zeit', 'fr': 'votre heure',
        'es': 'tu hora', 'pt': 'seu horário', 'it': 'ora locale', 'pl': 'twój czas'}
LOCAL_JS = """<script>
document.querySelectorAll('time.lt').forEach(t => {
  const s = new Intl.DateTimeFormat(document.documentElement.lang, { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).format(new Date(t.dateTime));
  t.after(` (@@YOUR@@: ${s})`);
});
</script>
"""


def L(x, lang):
    return x[lang] if isinstance(x, dict) else x


def E(x, lang):
    return escape(L(x, lang), quote=True)


def check_langs(obj, path=''):
    """Paths of trilingual fields that miss ru/en/uk (or are empty); the new languages are derived from en by langs.fill."""
    gaps = []
    if isinstance(obj, dict) and (obj.get('only') or obj.get('langs')):   # one-language guide, ru/uk-only section
        return gaps
    if isinstance(obj, dict):
        if set(obj) & set(langs.OLD) and set(obj) <= set(langs.ALL):
            gaps += [f'{path}.{l}' for l in langs.OLD if not obj.get(l)]
        else:
            for k, v in obj.items():
                gaps += check_langs(v, f'{path}.{k}')
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            gaps += check_langs(v, f'{path}[{i}]')
    return gaps


def art_sets(art, root, big=False):
    """(avif srcset, webp srcset, fallback src). big: hero fallback = widest, else a tile-sized one."""
    ws = WIDTHS.get(art, (360, 600, 896, 1344))
    src = lambda ext: ', '.join(f'{root}assets/art/{art}-{w}.{ext} {w}w' for w in ws)
    fb = ws[-1] if big else (ws[0] if art in WIDTHS else 600)
    return src('avif'), src('webp'), f'{root}assets/art/{art}-{fb}.webp'


def thero(sec, hero):
    """The guide's art band rewritten as the full-screen hero: same crumbs, title, lead and pills (still untranslated)."""
    m = lambda ext: ', '.join(f'@@ROOT@@assets/art/{hero}-m-{w}.{ext} {w}w' for w in (600, 800, 1000))   # noqa: E731
    big = lambda ext: ', '.join(f'@@ROOT@@assets/art/{hero}-{w}.{ext} {w}w' for w in THERO_BIG)   # noqa: E731
    phone = 'media="(max-width: 719px) and (max-aspect-ratio: 2/3)"'
    fx = f' data-fx="{THERO[hero]}" data-cut="{THERO_CUT.get(hero, ".9")}"' if THERO[hero] else ''   # living layer only where a mask exists
    pic = (f'<img class="thero-amb" src="@@ROOT@@assets/art/{hero}-960.webp" width="960" height="536" alt="" aria-hidden="true" loading="lazy" decoding="async">\n  '   # ultrawide sides
           f'<picture class="thero-art" aria-hidden="true"{fx}>\n'
           f'    <source {phone} type="image/avif" srcset="{m("avif")}" sizes="100vw">\n'
           f'    <source {phone} type="image/webp" srcset="{m("webp")}" sizes="100vw">\n'
           f'    <source type="image/avif" srcset="{big("avif")}" sizes="(max-aspect-ratio: 16/9) 180vh, 100vw">\n'
           f'    <source type="image/webp" srcset="{big("webp")}" sizes="(max-aspect-ratio: 16/9) 180vh, 100vw">\n'
           f'    <img src="@@ROOT@@assets/art/{hero}-1920.webp" width="1920" height="1072" alt="" fetchpriority="high" decoding="async">\n'
           '  </picture>')
    sec = re.sub(r'@@HERO@@|<picture class="stband-art".*?</picture>', lambda _: pic, sec, count=1, flags=re.S)   # the template's slot
    return (sec.replace('<section class="stband ghero" id="top">', '<section class="thero" id="top">', 1)
               .replace('<div class="wrap">', '<div class="wrap thero-in">', 1).replace('class="glead"', 'class="lead"', 1))


def por_band(cid):
    """A guide of one class ('por': guides/builds-<class>/): the portrait of that class instead of a shared scene, the same
    picture and side as the class page (.chero): "{<class>}" is the portrait of the reader's side (build.por_js), filled in
    by the script right under it, so only one side is ever fetched. Behind it the portrait's own blurred backdrop (~1 KB)."""
    s = lambda ext: ', '.join(f'@@ROOT@@assets/art/{{{cid}}}-{w}.{ext} {w}w' for w in (600, 896, 1344))   # noqa: E731
    sizes = '(max-width: 719px) 285px, clamp(405px, 57vh, 540px)'   # 3:4 at the band height (guide.src.html --hh)
    return (f'<picture class="pband-bg" aria-hidden="true"><img data-por-src="@@ROOT@@assets/art/{{{cid}}}-bg.webp" width="480" height="270" alt="" decoding="async"></picture>'
            f'<picture class="pband-por" aria-hidden="true"><source type="image/avif" data-por-srcset="{s("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" data-por-srcset="{s("webp")}" sizes="{sizes}">'
            f'<img data-por-src="@@ROOT@@assets/art/{{{cid}}}-896.webp" width="896" height="1200" alt="" fetchpriority="high" decoding="async"></picture>'
            '<script>GabellaPor.fill(document.currentScript.parentNode)</script>')


def tile_links(tiles, lang, root):
    """root: path to the language home (links); art always from the site root via @@ROOT@@."""
    out = []
    for s in tiles:
        avif, webp, img = art_sets(s['art'], '@@ROOT@@')
        cls, sz = ('ttile wide', '(min-width: 1280px) 1240px, 100vw') if s.get('wide') else ('ttile', '(min-width: 2200px) 560px, 320px')   # 4K: tiles grow to ~550 px
        out.append(f'<a class="{cls}" href="{root}{s["href"]}"><picture><source type="image/avif" srcset="{avif}" sizes="{sz}">'
                   f'<img src="{img}" srcset="{webp}" sizes="{sz}" alt="" loading="lazy" decoding="async"></picture>'
                   f'<b>{E(s["t"], lang)}</b><span>{E(s["d"], lang)}</span></a>')   # the update date is on the page itself
    return ''.join(out)


def li_id(step):
    """id attribute of a numbered-list item that other pages link to (class anchors on «Лучшая раса»)."""
    return f' id="{step["id"]}"' if 'id' in step else ''


class Raw(str):
    """A table cell that is ready HTML (the races of both sides in the tier list): cell() puts it in as is."""


def cell(c, lang, root):
    """A table cell: text, or (text, href) when the class name of a «Class · spec» cell links to its guide."""
    if isinstance(c, Raw):
        return str(c)
    if not isinstance(c, tuple):
        return E(c, lang)
    if c[1].startswith('http'):                                   # an addon on CurseForge: a new tab, like the sources
        return f'<a href="{escape(c[1])}" target="_blank" rel="noopener">{E(c[0], lang)}</a>'
    name, sep, rest = L(c[0], lang).partition(' · ')
    cid = CLS_HREF.search(c[1])
    if cid:
        return clink(cid.group(1), escape(name, quote=True), f'{root}{c[1]}', escape(rest, quote=True))
    return f'<a href="{root}{c[1]}">{escape(name, quote=True)}</a>{escape(sep + rest, quote=True)}'


CLS_HREF = re.compile(r'(?:^|[/-])(' + '|'.join(build.COLOR) + r')/(?:#[\w-]*)?$')   # classes/mage/, guides/leveling-mage/


def clink(cid, name, href, spec=''):
    """A class name in a table or a list: its game colour and a small portrait (index.src.html .clink).
    With a spec it is a two-line chip: the name over the spec, one icon size, one baseline."""
    if spec:
        return (f'<a class="clink two" href="{href}" style="--cc:{build.COLOR[cid]}"><span class="av">{face_img(cid)}</span>'
                f'<span class="cn"><b>{name}</b><small>{spec}</small></span></a>')
    return (f'<a class="clink" href="{href}" style="--cc:{build.COLOR[cid]}"><span class="av">{face_img(cid)}</span>{name}</a>')


def face_img(cid):
    """The round face of a class: the portrait of the reader's side (build.portraits; the Alliance one in the page,
    GabellaPor swaps it for the Horde before it loads, build.por_js)."""
    return build.class_face(cid)


def cpick(lang, root, title, href='classes/{}/'):
    """Phones, /classes/ and /guides/builds/: the nine classes as one grid under the hero lead, so a class is one tap from the
    first screen (css in guide.src.html .cpick; hidden from 720 px: the table or the spec list below does this job on a wide screen)."""
    items = ''.join(f'<a href="{root}{href.format(c["id"])}" style="--cc:{build.COLOR[c["id"]]}"><span class="av">{face_img(c["id"])}</span>'
                    f'<b>{escape(build.tr(c["n"], lang))}</b></a>' for c in build.CLASSES)
    return f'<nav class="cpick" aria-label="{escape(title, quote=True)}">{items}</nav>'


def spec_jump(g, lang):
    """Phones and tablets, a spec sheet: its sections (build, talents, leveling, group, rotation; gear once it is shown) as one row
    of links in the hero, so the talents are one tap from the first screen (the contents column shows from 1024 px)."""
    links = ''.join(f'<a href="#{s["id"]}">{E(s["title"], lang)}</a>' for s in g['sections']
                    if s['id'] not in ('answer', 'faq', 'related') and lang in s.get('langs', (lang,)))
    return f'<nav class="gjump" aria-label="{escape(THIS_PAGE[lang], quote=True)}">{links}</nav>'


CLS_ID = {c['n']: c['id'] for c in build.CLASSES}   # «Паладин» -> paladin
TIERS = ('S', 'A', 'B', 'C')


def cls_cells(blocks):
    """Tier list: every «Class · spec» or «Class» cell links its class page (the leveling table links the class guides),
    so the class name is a link in every table of the page. Returns new blocks, the content stays as is."""
    def cell_(c):
        cid = isinstance(c, dict) and CLS_ID.get(c['ru'].split(' · ')[0])
        return (c, f'classes/{cid}/') if cid else c
    out = []
    for kind, data in blocks:
        if kind == 'table':
            data = dict(data, rows=[[cell_(c) for c in r] for r in data['rows']])
        elif kind == 'tabs':
            data = [dict(x, blocks=cls_cells(x['blocks'])) for x in data]
        out.append((kind, data))
    return out


def tier_grid(table, lang, root):
    """I2: the «Whole classes» table as a tier grid — S/A/B/C rows of class portraits, one tab per column
    (Leveling / PvE / PvP). A star: the sources differ by two letters or more."""
    head = [E(h, lang) for h in table['head']]
    ids = [CLS_ID[r[0]['ru']] for r in table['rows']]
    name = {c['id']: escape(build.tr(c['n'], lang)) for c in build.CLASSES}
    btns, panels = '', ''
    for i, col in enumerate((1, 2, 3)):
        rows = ''
        for t in TIERS:
            got = [(cid, r[col]) for cid, r in zip(ids, table['rows']) if r[col].rstrip('*') == t]
            if not got:
                continue
            faces = ''.join(f'<a class="tgc" href="{root}classes/{cid}/" style="--cc:{build.COLOR[cid]}">'
                            '<span class="av">' + face_img(cid) + '</span>'
                            f'<span class="tgn">{name[cid]}{"<sup>*</sup>" if v.endswith("*") else ""}</span></a>'
                            for cid, v in got)
            rows += f'<li><b class="tgl t{t}">{t}</b><div class="tgr">{faces}</div></li>'
        first = i == 0
        btns += (f'<button type="button" class="pill" role="tab" data-tab="tg{col}" aria-selected="{"true" if first else "false"}"'
                 + ('' if first else ' tabindex="-1"') + f'>{head[col]}</button>')
        panels += f'<div role="tabpanel" data-tab="tg{col}"' + ('' if first else ' hidden') + f'><ol class="tgrid">{rows}</ol></div>'
    return f'<div class="gtabs tgbox"><div role="tablist" aria-label="{head[0]}">{btns}</div>{panels}</div>'


SIDES = ('alliance', 'horde')
_RACE_LIST = []


def race_list():
    if not _RACE_LIST:
        _RACE_LIST.extend(build.parse_races(home_src()))
    return _RACE_LIST


def side_races(cid, lang):
    """The races of a class on each side, the best for PvE first with a star (content/hero.BEST, the Best Race guide).
    Both sides are in the page; html[data-side] (side_switch) shows one."""
    out = ''
    for f in SIDES:
        best = HERO.BEST[cid][f]['*'][0]
        ids = [r['id'] for r in race_list() if r['f'] == f and cid in r['can']]
        ids = [r for r in best if r in ids] + [r for r in ids if r not in best]
        name = {r['id']: escape(build.tr(r['n'], lang)) for r in race_list()}
        out += (f'<a class="frc" data-f="{f}" href="../best-race/#{cid}">'   # the races open the class' section of the Best race guide
                + ', '.join(f'<b>{name[r]}<i aria-hidden="true">★</i></b>' if r in best else name[r] for r in ids) + '</a>')
    return Raw(out)


def side_switch(d, lang, root):
    """Tier list: one Alliance / Horde switch for the whole page. The side is the site's one (build.por_js GabellaPor:
    gabella-side, else the hero's race, else the time of day); a tap stores it with GabellaPor.set, which swaps every class
    portrait on the page, and html[data-side] shows the races of that side. The script runs right after the markup, before
    the table is painted, and follows the other places of the site (the gabella-side / gabella-me events, other tabs)."""
    btns = ''.join(f'<button type="button" data-f="{f}" aria-pressed="false">{E(d[f], lang)}</button>' for f in SIDES)
    return (f'<div class="fsw"><div class="fswb"><span class="fswl" aria-hidden="true">{E(d["label"], lang)}</span>'
            f'<div class="fsws" id="fsw" role="group" aria-label="{E(d["label"], lang)}">{btns}</div></div>'
            f'<p class="fswn">{E(d["note"], lang)} {E(d["star"], lang)} <a href="{root}guides/best-race/">{E(d["guide"], lang)}</a>.</p></div>'
            '<script>(function(){var b=document.getElementById("fsw"),P=window.GabellaPor;if(!P)return;'
            'var B=[].slice.call(b.querySelectorAll("[data-f]"));'
            'function show(){var f=P.fac();document.documentElement.setAttribute("data-side",f);'
            'B.forEach(function(x){x.setAttribute("aria-pressed",x.getAttribute("data-f")==f?"true":"false")})}'
            'B.forEach(function(x){x.addEventListener("click",function(){if(x.getAttribute("aria-pressed")!="true")P.set(x.getAttribute("data-f"));show()})});'
            'addEventListener("gabella-side",show);addEventListener("gabella-me",show);document.addEventListener("gabella:tod",show);show()})()</script>')


def with_races(blocks, side, lang):
    """The «Best classes» table of the tier list with the races of the chosen side as the last column."""
    out = []
    for kind, data in blocks:
        if kind == 'table':
            rows = [r + [side_races(CLS_ID[(r[0][0] if isinstance(r[0], tuple) else r[0])['ru']], lang)] for r in data['rows']]
            data = dict(data, head=data['head'] + [side['races']], rows=rows)
        out.append((kind, data))
    return out


def short(c, lang):
    """A cell of up to five letters («S», «A*», «10–14», «5»): on a phone it sits in a line with its label."""
    return len(re.sub(r'<[^>]+>', '', str(L(c[0] if isinstance(c, tuple) else c, lang))).strip()) <= 5


def tier_letter(c, lang):
    return isinstance(c, str) and re.fullmatch(r'[SABC]\*?', c.strip()) is not None


def td(h, html, i, row, lang):
    """T1, phones: a row is one compact card — the first cell (and the second after a short first, «S · Hunter · BM»)
    without a label, short cells in a line with theirs, long ones under it; an empty «—» is not shown at all."""
    cls = []
    if i == 0 or (i == 1 and tier_letter(row[0], lang)):
        cls.append('k')
    if short(row[i], lang):
        cls.append('s')
        if tier_letter(row[i], lang):
            cls.append('t')                                       # a tier letter: the big one at the start of the card
    if html.strip() in ('—', '-', ''):
        cls.append('nil')
    elif 'k' not in cls and 's' not in cls and all(j == 0 or short(row[j], lang) or (j == 1 and tier_letter(row[0], lang)) for j in range(i)):
        cls.append('m')                                           # the first long text of the row («Why»): no label over it
    return f'<td data-l="{h}"' + (f' class="{" ".join(cls)}"' if cls else '') + f'>{html}</td>'


def render_block(kind, data, lang, root, inner=False):
    """inner: a block inside a tab panel. A tip there is the word only, no plate and no icon: one boxed tip per section."""
    if kind == 'text':
        return ''.join(f'<p>{E(p, lang)}</p>' for p in data)
    if kind == 'list':
        return '<ul>' + ''.join(f'<li>{E(p, lang)}</li>' for p in data) + '</ul>'
    if kind == 'steps':
        cards = ''.join(f'<li{li_id(s)}><span class="n">{i}</span><div><b>{E(s["t"], lang)}</b><p>{E(s["d"], lang)}</p></div></li>'
                        for i, s in enumerate(data, 1))
        return f'<ol class="steps-c">{cards}</ol>'
    if kind == 'tiles':
        return f'<div class="ttiles gtiles">{tile_links(data, lang, root)}</div>'
    if kind == 'anchors':                                         # class ids -> chips to the sections of this page (#warlock)
        name = {c['id']: escape(build.tr(c['n'], lang)) for c in build.CLASSES}
        return build.spec_list([build.spec_plate(f'#{c}', name[c], '', c, face=True) for c in data], 'cls9')
    if kind == 'table':
        head = [E(h, lang) for h in data['head']]
        th = ''.join(f'<th scope="col">{h}</th>' for h in head)
        rows = ''.join('<tr>' + ''.join(td(h, cell(c, lang, root), i, r, lang) for i, (h, c) in enumerate(zip(head, r))) + '</tr>'
                       for r in data['rows'])
        return f'<table class="gtable"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>'
    if kind == 'picks':                                           # table whose second column links class pages
        head = [E(h, lang) for h in data['head']]
        name = {c['id']: build.tr(c['n'], lang) for c in build.CLASSES}
        def cls(ids):
            return '<span class="clinks">' + ''.join(clink(i, escape(name[i]), f'{root}classes/{i}/') for i in ids) + '</span>'
        rows = ''.join(f'<tr><td data-l="{head[0]}">{E(r[0], lang)}</td><td data-l="{head[1]}">{cls(r[1])}</td>'
                       + ''.join(f'<td data-l="{h}">{E(c, lang)}</td>' for h, c in zip(head[2:], r[2:])) + '</tr>'
                       for r in data['rows'])
        th = ''.join(f'<th scope="col">{h}</th>' for h in head)
        return f'<table class="gtable picks"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>'
    if kind == 'tabs':
        btns = ''.join(f'<button type="button" class="pill" role="tab" data-tab="{x["id"]}" aria-selected="{"true" if i == 0 else "false"}">'
                       f'{E(x["t"], lang)}</button>' for i, x in enumerate(data))
        panels = ''.join(f'<div role="tabpanel" data-tab="{x["id"]}"{"" if i == 0 else " hidden"}>'
                         + ''.join(render_block(k, d, lang, root, True) for k, d in x['blocks']) + '</div>'
                         for i, x in enumerate(data))
        return f'<div class="gtabs"><div role="tablist">{btns}</div>{panels}</div>'
    if kind == 'faq':
        ext = lambda u: u.startswith('http')   # noqa: E731  external link: new tab and an arrow, a guide page: same tab
        items = ''.join(f'<details id="{q["id"]}"><summary>{E(q["q"], lang)}</summary>'
                        + ''.join(f'<p>{E(a, lang)}</p>' for a in q['a'])
                        + (f'<p class="gbtns"><a class="btn ghost" href="{q["link"][1]}"'
                           + (f' target="_blank" rel="noopener">{E(q["link"][0], lang)} ↗' if ext(q['link'][1]) else f'>{E(q["link"][0], lang)}')
                           + '</a></p>' if q.get('link') else '') + '</details>' for q in data)
        return f'<div class="gfaq">{items}</div>'
    if kind == 'tip' and inner:
        return f'<p class="tipl"><span class="tl">{TIP[lang]}</span>{E(data, lang)}</p>'
    if kind == 'tip':
        return (f'<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg>'
                f'<p><span class="tl">{TIP[lang]}</span>{E(data, lang)}</p></div>')
    if kind == 'play':                                            # Leveling: the in-game page in one line
        return (f'<a class="gplay frame" href="{root}play/"><span><b>{E(data["h"], lang)}</b> {E(data["d"], lang)}</span>'
                f'<span class="btn ghost">{E(data["go"], lang)}</span></a>')
    if kind == 'calc':                                            # Builds: the talent calculator in one line
        return (f'<a class="gplay frame" href="{root}talents/"><span><b>{E(data["h"], lang)}</b> {E(data["d"], lang)}</span>'
                f'<span class="btn ghost">{E(data["go"], lang)}</span></a>')
    if kind == 'tree':                                            # spec guides: the talent tree with our path (talents.py)
        return talents.render(data['cls'], data['spec'], data['rows'], data['titles'], lang, root)
    if kind == 'raw':
        return L(data, lang)
    if kind == 'news':                                            # our notes from NEWS, newest first
        items = ''.join(f'<a class="nitem" href="{escape(n["url"])}" target="_blank" rel="noopener"' + (f' data-cls="{n["cls"]}"' if n.get('cls') else '') + '>'
                        f'<time datetime="{n["date"]}">{".".join(reversed(n["date"].split("-")))}</time>'
                        f'<b>{E(n["title"], lang)}</b><p>{E(n["text"], lang)}</p>'
                        + (f'<p>{E(NEWS_SO, lang)}. {E(n["so"], lang)}</p>' if n.get('so') else '') + '</a>'
                        for n in sorted(NEWS, key=lambda n: n['date'], reverse=True))
        return f'<div class="nlist">{items}</div>'
    if kind == 'profs':
        return render_block('table', {'head': PROF_HEAD, 'rows': profs_table(home_src())}, lang, root)
    if kind == 'ckbar':                                           # launch checklist: ticks counter, filled by JS['checklist']
        return (f'<div class="dbar" id="ckBar" hidden><span>{E(data["done"], lang)} <b id="ckN">0</b> / <span id="ckT">0</span></span>'
                f'<span class="dmeter" aria-hidden="true"><i id="ckFill"></i></span>'
                f'<button type="button" class="pill" id="ckReset" hidden>{E(data["reset"], lang)}</button></div>')
    if kind == 'checks':                                          # launch checklist: a tick, the step, a link to our page
        items = [x for x in data if lang in x.get('langs', (lang,))]
        return '<ul class="dchk">' + ''.join(
            f'<li><input type="checkbox" id="ck-{x["id"]}" data-ck="{x["id"]}"><label for="ck-{x["id"]}">{E(x["t"], lang)}</label>'
            f'<p>{E(x["d"], lang)}</p><a class="dgo" href="{root}{x["href"]}">{E(x["go"], lang)}</a></li>' for x in items) + '</ul>'
    if kind == 'launch':                                          # Launch day: the countdown in the reader's time, filled by JS['launchday']
        units = ''.join(f'<div><b id="lc{k.upper()}">–</b><span>{E(data[k], lang)}</span></div>' for k in ('d', 'h', 'm'))
        ev = L(data['ev'], lang)
        ics = '\r\n'.join(('BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Gabella//WoW Forever//EN', 'BEGIN:VEVENT',
                           'UID:wow-forever-launch-2026@gabella.site', 'DTSTAMP:20261027T000000Z',
                           'DTSTART:20261104T230000Z', 'DTEND:20261105T000000Z', f'SUMMARY:{ev}',
                           'URL:https://gabella.site/wow/guides/launch-day/',
                           'BEGIN:VALARM', 'ACTION:DISPLAY', f'DESCRIPTION:{ev}', 'TRIGGER:-PT30M', 'END:VALARM',
                           'END:VEVENT', 'END:VCALENDAR', ''))
        gcal = ('https://calendar.google.com/calendar/render?action=TEMPLATE&dates=20261104T230000Z/20261105T000000Z&text='
                + quote(ev) + '&details=' + quote('https://gabella.site/wow/guides/launch-day/'))
        return (f'<div class="lcd" id="lcd"><div class="lcu">{units}</div>'
                f'<div class="lcw"><span id="lcL" data-out="{E(data["out"], lang)}">{E(data["left"], lang)}</span>'
                f'<b id="lcWhen">04.11.2026, 23:00 UTC</b><span id="lcY" hidden>{E(data["your"], lang)}</span></div></div>'
                f'<p class="gbtns lcal"><a class="btn ghost" href="data:text/calendar;charset=utf-8,{quote(ics)}" download="wow-forever-launch.ics">'
                f'{E(data["cal"], lang)}</a><a class="btn ghost" href="{escape(gcal)}" target="_blank" rel="noopener">{E(data["gcal"], lang)} ↗</a></p>')
    if kind == 'lgcalc':                                          # Legacy counter: static markup, state and sums by JS['legacy']
        return lgcalc(data, lang)
    raise ValueError(f'unknown block {kind!r}')


def lgcalc(d, lang):
    """The Legacy counter. Tick order = bit order of the share link (#l=): do not reorder. Perks: a stepper per perk."""
    ui = {k: E(v, lang) for k, v in d['ui'].items()}
    def chip(label, aria):
        return (f'<label class="lgp"><input type="checkbox" aria-label="{escape(aria, quote=True)}"><span>'
                + (escape(label) if label else '') + '</span></label>')
    groups, total = '', 0
    for g in d['groups']:
        rows, n = '', 0
        for r in g['rows']:
            if 'classes' in r:
                for c in build.CLASSES:
                    nm = build.tr(c['n'], lang)
                    rows += (f'<div class="lgr"><span class="lgn">{escape(nm)}</span><div class="lgcs">'
                             + ''.join(chip(x, f'{nm} {x}') for x in r['classes']) + '</div></div>')
                    n += len(r['classes'])
                continue
            lab = L(r['l'], lang) if r.get('l') else ''
            name = f"{lab} {r['k']}" if r.get('k') else lab
            cs = ''
            for i, c in enumerate(r['chips'], 1):
                txt = L(c, lang) if c else ''
                cs += chip(txt, f'{name} {txt}'.strip() if txt else f'{name}, #{i}')
            rows += f'<div class="lgr"><span class="lgn">{escape(name)}</span><div class="lgcs">{cs}</div></div>' if name else f'<div class="lgr"><div class="lgcs">{cs}</div></div>'
            n += len(r['chips'])
        total += n
        note = f'<p class="lgs">{E(d["ui"][g["note"]], lang)}</p>' if g.get('note') else ''
        groups += (f'<div class="lgg" data-g="{g["id"]}"><h4>{E(g["t"], lang)} <span class="lgcnt" data-n="{n}">0 / {n}</span></h4>{note}{rows}</div>')
    trees = ''
    for tr_ in d['trees']:
        ps = ''.join(
            f'<div class="lgk" data-max="{mx}"><span class="lgn">{escape(nm)}</span><div class="lgst">'
            f'<button type="button" class="lgb" data-d="-1" aria-label="{escape(nm)}: {ui["less"]}">−</button>'
            f'<output class="lgv">0 / {mx}</output>'
            f'<button type="button" class="lgb" data-d="1" aria-label="{escape(nm)}: {ui["more"]}">+</button></div></div>'
            for nm, mx in tr_['perks'])
        trees += f'<div class="lgg lgt"><h4>{E(tr_["t"], lang)}</h4>{ps}</div>'
    rw = ''.join(f'<li data-th="{th}"><b>{th}</b><span>{E(x, lang)}</span><em></em></li>' for th, x in d['rewards'])
    return (f'<div class="lgc" id="lgc" data-total="{total}">'
            f'<p>{ui["intro"]}</p>'
            f'<div class="lgsum"><div><span class="lgl">{ui["earned"]}</span><b id="lgE">0</b> / {total}<span class="dmeter" aria-hidden="true"><i id="lgEF"></i></span></div>'
            f'<div><span class="lgl">{ui["spent"]}</span><b id="lgS">0</b> / 16<span class="dmeter" aria-hidden="true"><i id="lgSF"></i></span></div></div>'
            f'<p class="lgs">{ui["cap"]}</p><p class="lgwarn" id="lgW" role="status"></p>'
            f'<h3>{ui["ch"]}</h3><p class="lgs">{ui["src"]}</p><div class="lggrid">{groups}</div>'
            f'<h3>{ui["pk"]}</h3><p class="lgs">{ui["pksrc"]}</p><div class="lggrid">{trees}</div>'
            f'<h3>{ui["rw"]}</h3><p class="lgs">{ui["rwsrc"]}</p><ul class="lgrw" id="lgRW">{rw}</ul>'
            f'<div class="lgshare"><label for="lgLink" class="lgl">{ui["link"]}</label>'
            f'<div class="lgrow"><input id="lgLink" readonly><button type="button" class="btn" id="lgCopy">{ui["copy"]}</button>'
            f'<button type="button" class="btn ghost" id="lgReset">{ui["reset"]}</button>'
            f'<button type="button" class="btn ghost" id="lgBack" hidden></button></div>'
            f'<p class="lgs" id="lgMsg" role="status"></p></div></div>')



PROF_HEAD = [{'ru': 'Профессия', 'en': 'Profession', 'uk': 'Професія'},
             {'ru': 'Объект лагеря', 'en': 'Camp object', 'uk': 'Об’єкт табору'},
             {'ru': 'Похож на бафф', 'en': 'Similar buff', 'uk': 'Схожий на бафф'}]


def home_src():
    return open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()


def profs_table(src):
    """Camp table from PROFS of the home page: [name, object, effect]; names and effects via the home i18n."""
    tr = lambda x: langs.derive({'ru': x, 'en': build.T[x][0], 'uk': build.T[x][1]})
    return [[tr(name), obj, tr(eff)]
            for _id, name, _tier, obj, eff in re.findall(r"\['(\w+)', '([^']+)', (\d), '([^']+)', '([^']+)'\]", src)]


def inline_tiles(obj):
    """Links of the art tiles inside a guide's text (also inside tabs): those guides stay out of «Other guides» below."""
    if isinstance(obj, tuple) and len(obj) == 2 and obj[0] == 'tiles':
        return {x['href'].split('#')[0] for x in obj[1]}          # «Лучшая раса» #warrior is still that guide
    if isinstance(obj, (list, tuple)):
        return set().union(*map(inline_tiles, obj)) if obj else set()
    if isinstance(obj, dict):
        return inline_tiles(list(obj.values()))
    return set()


def inline_arts(obj):
    """Pictures of the art tiles inside a guide's text: «Other guides» below does not repeat them."""
    if isinstance(obj, tuple) and len(obj) == 2 and obj[0] == 'tiles':
        return {x['art'] for x in obj[1]}
    if isinstance(obj, (list, tuple)):
        return set().union(*map(inline_arts, obj)) if obj else set()
    if isinstance(obj, dict):
        return inline_arts(list(obj.values()))
    return set()


def render_guide(g, lang, root):
    sections = [s for s in g['sections'] if lang in s.get('langs', (lang,))]   # 'langs': a section only in these languages
    toc = ''.join(f'<a href="#{s["id"]}">{E(s["title"], lang)}</a>' for s in sections if not s.get('toc'))   # 'toc': lit by that entry
    tier = g['slug'] == 'tier-list'
    def blocks(s):
        bl = cls_cells(s['blocks']) if tier else s['blocks']
        if tier and s['id'] == 'classes' and g.get('side'):
            bl = with_races(bl, g['side'], lang)
        html = ''.join(render_block(k, d, lang, root) for k, d in bl)
        if tier and s['id'] == 'classes':                       # the switch and the grid open the section, the table with the reasons follows
            html = (side_switch(g['side'], lang, root) if g.get('side') else '') + tier_grid(next(d for k, d in s['blocks'] if k == 'table'), lang, root) + html
        return html
    body = '\n'.join(f'<section class="frame gsec" id="{s["id"]}"' + (f' data-toc="{s["toc"]}"' if s.get('toc') else '')
                     + f'><h2>{E(s["title"], lang)}</h2>' + blocks(s) + '</section>'
                      for s in sections)
    return toc, body


def guide_tiles(guides):
    # a tile shows the guide's own scene when it has one: portraits stay on the class and race pages, no picture twice on a page
    return [{'t': x['title'], 'd': x['tile'], 'href': f'guides/{x["slug"]}/', 'art': x.get('tile_art') or x.get('hero') or x['art']} for x in guides]


PINNED = ('launch-checklist', 'launch-day')   # «Other guides»: the two launch pages first, then the guides after this one


def more_order(others, slug):
    """«Other guides» in reading order: the launch pages, then the guides that follow this one in ORDER, wrapping round."""
    at = ORDER.index(slug) if slug in ORDER else 0
    return sorted(others, key=lambda x: (x['slug'] not in PINNED, (ORDER.index(x['slug']) - at) % len(ORDER)))


def full_rows(tiles):
    """Only as many tiles as fill whole rows of the .gtiles grid at 1280 px and wider: 12, 8 (4 columns), 9, 6 (3), 10, 5 (5)."""
    n = next((k for k in (12, 10, 9, 8, 6, 5) if len(tiles) >= k), len(tiles))
    return tiles[:n]


def section_tiles():
    return [{'t': x['title'], 'd': x['tile'], 'href': x['path'], 'art': x['art']} for x in HUBS]


def lang_guides(lang):
    """Guides of a language: a guide with 'only' exists in that one language."""
    return [g for g in GUIDES if g.get('only', lang) == lang]


def hub_body(lang, root):
    """Guides first, then the classes/ and races/ sections and the tools page. The nine class guides are one tile
    («Leveling by class», right after the leveling guide); they have a 'hub': False."""
    tiles = guide_tiles([g for g in lang_guides(lang) if g.get('hub', True)])
    at = next((i for i, x in enumerate(tiles) if x['href'] == 'guides/leveling/'), -1) + 1
    tiles[at:at] = [CLASS_HUB_TILE, BUILDS_HUB_TILE]   # «Builds by class» leads to /guides/builds/
    tiles += section_tiles() + SITE_TILES[1:]
    for href in ('guides/launch-day/', 'guides/launch-checklist/'):   # «Day 1» and «Launch day» head the page as two banners: the other 16 fill whole rows
        top = next((i for i, x in enumerate(tiles) if x['href'] == href), None)
        if top is not None:
            tiles.insert(0, dict(tiles.pop(top), wide=True))
    return '', f'<section class="gsec bare" id="all">{render_block("tiles", tiles, lang, root)}</section>'


JS = {}   # slug -> JS живой части; наполняется в задачах 3, 5, 7, 8, 9

JS['faq'] = r'''/* FAQ: search over questions and answers, every word; when none has them all, the site search (synonyms, typos,
   known questions) picks this page's questions; #id opens the question */
const qIn = document.getElementById('faqQ');
const qs = [...document.querySelectorAll('.gfaq details')];
const qNone = document.getElementById('faqNone');
function showQs(hit) {   // hit(details) -> shown; null: all, folded back
  let n = 0;
  qs.forEach(d => {
    const h = !hit || hit(d); d.hidden = !h;
    if (hit && h) { n++; if (!d.open) { d.open = true; d.dataset.byq = '1'; } }
    if (!hit && d.dataset.byq) { d.open = false; delete d.dataset.byq; }   // clearing the field folds what the search opened
  });
  if (qNone) qNone.hidden = !hit || n > 0;
  return n;
}
if (qIn) qIn.addEventListener('input', () => {
  const v = qIn.value.trim().toLowerCase(), ws = v.split(/\s+/);
  if (!v) return showQs(null);
  if (showQs(d => { const t = d.textContent.toLowerCase(); return ws.every(w => t.includes(w)); }) || !window.gabellaFind) return;
  window.gabellaFind(v).then(rs => {
    if (qIn.value.trim().toLowerCase() !== v) return;
    const here = rs.map(r => r.u.split('#')).filter(([p, id]) => id && location.pathname.endsWith('/' + p.replace(/^.*?guides\//, 'guides/'))).map(r => r[1]);
    showQs(d => here.includes(d.id));
  });
});
function openHash() { let id = ''; try { id = decodeURIComponent(location.hash.slice(1)); } catch (e) { return; }   // a broken #%E0 is not an error
  const d = id && document.getElementById(id); if (d && d.tagName === 'DETAILS') { d.open = true; d.scrollIntoView(); } }
addEventListener('hashchange', openHash); openHash();'''


DG_TX = {
    'ru': {'h': ['Подземелье', 'Уровни', 'Где вход'], 'new': 'новое', 'shown': 'Показано', 'of': 'из',
           'none': 'Под этот уровень подземелий нет.', 'need': 'Укажите свой уровень, чтобы отфильтровать.',
           'only': {'alliance': 'Только Альянс', 'horde': 'Только Орда'}, 'side': {'alliance': 'Альянс, Орде далеко', 'horde': 'Орда, Альянсу далеко'}},
    'en': {'h': ['Dungeon', 'Levels', 'Entrance'], 'new': 'new', 'shown': 'Showing', 'of': 'of',
           'none': 'No dungeons for this level.', 'need': 'Enter your level to filter.',
           'only': {'alliance': 'Alliance only', 'horde': 'Horde only'}, 'side': {'alliance': 'Alliance; a long way for the Horde', 'horde': 'Horde; a long way for the Alliance'}},
    'uk': {'h': ['Підземелля', 'Рівні', 'Де вхід'], 'new': 'нове', 'shown': 'Показано', 'of': 'з',
           'none': 'Під цей рівень підземель немає.', 'need': 'Вкажіть свій рівень, щоб відфільтрувати.',
           'only': {'alliance': 'Лише Альянс', 'horde': 'Лише Орда'}, 'side': {'alliance': 'Альянс, Орді далеко', 'horde': 'Орда, Альянсу далеко'}},
}
DG_JS = r'''/* Dungeons: level filter seeded from "My hero" (read only, the hero is edited on the home page) */
const TX = @@TX@@;
const lvRange = d => d[1] === d[2] ? String(d[1]) : `${d[1]}–${d[2]}`;
const nearLvl = (d, lv) => lv >= d[1] - 3 && lv <= d[2] + 3;
const HORDE = ['orc', 'undead', 'tauren', 'troll', 'skyH'];
let dgLvl = 0, dgFac = '';
try { const m = JSON.parse(localStorage.getItem('gabella-wf-me')) || {}; dgLvl = +m.lvl || 0; dgFac = m.race ? (HORDE.includes(m.race) ? 'horde' : 'alliance') : ''; } catch (e) {}
let dgMode = dgLvl ? 'mine' : 'all';
const lvIn = $('#dgLvl');
function renderDg() {
  let rows = DUNGEONS;
  if (dgMode === 'new') rows = rows.filter(d => d[4]);
  if (dgMode === 'mine') rows = dgLvl ? rows.filter(d => nearLvl(d, dgLvl) && (!dgFac || !d[6] || d[6] === dgFac || d[7])) : [];
  $('#dgBody').innerHTML = rows.length ? rows.map(d => {
    const mine = dgLvl && nearLvl(d, dgLvl);
    const alt = (d[5] || []).map(a => `${a[0]}: ${a[1]}`).join(', ');
    const pg = TX.pg[DUNGEONS.indexOf(d)], nm = pg ? `<a href="${pg}">${esc(d[0])}</a>` : esc(d[0]);   /* a dungeon with its own page links to it */
    return `<tr class="${mine ? 'mine' : ''}"><td data-l="${TX.h[0]}">${nm}${d[4] ? ` <span class="tag new">${TX.new}</span>` : ''}</td>`
      + `<td data-l="${TX.h[1]}"><span class="lvl${mine ? ' gold' : ''}">${lvRange(d)}</span>${alt ? `<span class="alt">${esc(alt)}</span>` : ''}</td>`
      + `<td data-l="${TX.h[2]}">${esc(d[3])}${d[6] ? `<span class="alt">${(d[7] ? TX.side : TX.only)[d[6]]}</span>` : ''}</td></tr>`;
  }).join('') : `<tr><td colspan="3">${dgLvl ? TX.none : TX.need}</td></tr>`;
  $('#dgCount').textContent = `${TX.shown} ${rows.length} ${TX.of} ${DUNGEONS.length}`;
  document.querySelectorAll('#segD button').forEach(b => b.setAttribute('aria-pressed', b.dataset.v === dgMode));
  if (document.activeElement !== lvIn) lvIn.value = dgLvl || '';
}
$('#segD').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { dgMode = b.dataset.v; renderDg(); } });
lvIn.addEventListener('input', () => { const v = parseInt(lvIn.value, 10); dgLvl = v >= 1 && v <= 60 ? v : 0; dgMode = dgLvl ? 'mine' : 'all'; renderDg(); });
document.querySelectorAll('#dgBox .lvm, #dgBox .lvp').forEach(b => b.addEventListener('click', () => {
  const up = b.classList.contains('lvp');
  dgLvl = Math.max(1, Math.min(60, (dgLvl || (up ? 0 : 2)) + (up ? 1 : -1))); dgMode = 'mine'; renderDg();
}));
renderDg();'''
LG_TX = {
    'ru': {'over': 'Потрачено больше, чем заработано: не хватает %n', 'full': 'Достигнут лимит 16 очков на персонажа.', 'copied': 'Ссылка скопирована.',
           'fail': 'Не удалось скопировать: выделите ссылку и нажмите Ctrl+C.', 'fromLink': 'Открыт набор из ссылки. Ваши сохранённые отметки не тронуты.',
           'back': 'Вернуть мои отметки', 'got': 'есть', 'left': 'ещё %n'},
    'en': {'over': 'Spent more than earned: %n more needed', 'full': 'The limit of 16 points per character is reached.', 'copied': 'Link copied.',
           'fail': 'Could not copy: select the link and press Ctrl+C.', 'fromLink': 'A set from a link is open. Your saved marks are untouched.',
           'back': 'Back to my marks', 'got': 'unlocked', 'left': '%n to go'},
    'uk': {'over': 'Витрачено більше, ніж зароблено: бракує %n', 'full': 'Досягнуто ліміт 16 очок на персонажа.', 'copied': 'Посилання скопійовано.',
           'fail': 'Не вдалося скопіювати: виділіть посилання й натисніть Ctrl+C.', 'fromLink': 'Відкрито набір із посилання. Ваші збережені позначки не чіпали.',
           'back': 'Повернути мої позначки', 'got': 'є', 'left': 'ще %n'},
}
LG_JS = r"""/* Legacy counter: ticks and perk ranks live in this browser ("gabella-legacy" = {c: hex of the ticks, p: digits of the ranks}),
   the link carries the same as #l=hex.digits. The order of ticks and perks in the markup is the order in the link. */
const TX = @@TX@@, LGK = 'gabella-legacy', CAP = 16;
const box = $('#lgc'), cks = [...box.querySelectorAll('input[type=checkbox]')], pks = [...box.querySelectorAll('.lgk')];
const maxs = pks.map(k => +k.dataset.max);
let bits = cks.map(() => 0), ranks = pks.map(() => 0), fromLink = false;
const toHex = a => { let o = ''; for (let i = 0; i < a.length; i += 4) o += (a[i] * 8 + (a[i + 1] || 0) * 4 + (a[i + 2] || 0) * 2 + (a[i + 3] || 0)).toString(16); return o; };
const fromHex = h => cks.map((_, i) => (parseInt(h[i >> 2] || '0', 16) >> (3 - (i & 3))) & 1);
const fromDig = p => { let left = CAP; return maxs.map((m, i) => { const v = Math.min(+(p[i] || 0) || 0, m, left); left -= v; return v; }); };
const pack = () => ({ c: toHex(bits), p: ranks.join('') });
const hashOf = o => '#l=' + o.c + '.' + o.p;
function readLink() { const m = location.hash.match(/^#l=([0-9a-f]+)\.([0-9]+)$/); return m ? { c: m[1], p: m[2] } : null; }
function readSaved() { try { const o = JSON.parse(localStorage.getItem(LGK)); return o && typeof o.c === 'string' && typeof o.p === 'string' ? o : null; } catch (e) { return null; } }
function apply(o) { bits = fromHex(o.c); ranks = fromDig(o.p); }
function save() { try { localStorage.setItem(LGK, JSON.stringify(pack())); } catch (e) {} }
const sum = a => a.reduce((x, y) => x + y, 0), put = (id, v) => { $(id).textContent = v; };
function paint() {
  cks.forEach((c, i) => { c.checked = !!bits[i]; });
  box.querySelectorAll('.lgg[data-g]').forEach(g => {
    const n = g.querySelectorAll('input:checked').length, c = g.querySelector('.lgcnt'); c.textContent = n + ' / ' + c.dataset.n;
  });
  pks.forEach((k, i) => { k.querySelector('.lgv').textContent = ranks[i] + ' / ' + maxs[i]; });
  const e = sum(bits), s = sum(ranks), tot = cks.length;
  put('#lgE', e); put('#lgS', s);
  $('#lgEF').style.width = e * 100 / tot + '%'; $('#lgSF').style.width = s * 100 / CAP + '%';
  $('#lgW').textContent = s > e ? TX.over.replace('%n', s - e) : s >= CAP ? TX.full : '';
  box.querySelectorAll('#lgRW li').forEach(li => {
    const th = +li.dataset.th, ok = e >= th; li.classList.toggle('got', ok);
    li.querySelector('em').textContent = ok ? TX.got : TX.left.replace('%n', th - e);
  });
  $('#lgLink').value = location.origin + location.pathname + location.search + hashOf(pack());
  $('#lgBack').hidden = !fromLink;
  $('#lgMsg').textContent = fromLink ? TX.fromLink : '';
}
cks.forEach((c, i) => c.addEventListener('change', () => { bits[i] = c.checked ? 1 : 0; fromLink = false; save(); paint(); }));
pks.forEach((k, i) => k.addEventListener('click', ev => {
  const b = ev.target.closest('.lgb'); if (!b) return;
  const v = ranks[i] + +b.dataset.d;
  if (v < 0 || v > maxs[i] || sum(ranks) - ranks[i] + v > CAP) return;   // a button at its end stays focusable and does nothing
  ranks[i] = v; fromLink = false; save(); paint();
}));
$('#lgCopy').addEventListener('click', async () => {
  const f = $('#lgLink'); let ok = true;
  try { await navigator.clipboard.writeText(f.value); } catch (e) { ok = false; f.select(); }
  $('#lgMsg').textContent = ok ? TX.copied : TX.fail;
});
$('#lgReset').addEventListener('click', () => { bits = cks.map(() => 0); ranks = pks.map(() => 0); fromLink = false; save(); paint(); });
$('#lgBack').textContent = TX.back;
$('#lgBack').addEventListener('click', () => { const o = readSaved(); if (o) apply(o); else { bits = cks.map(() => 0); ranks = pks.map(() => 0); } fromLink = false; paint(); });
addEventListener('storage', e => { if (e.key === LGK && !fromLink) { const o = readSaved(); if (o) { apply(o); paint(); } } });
const lk = readLink(), sv = readSaved();
if (lk) { apply(lk); fromLink = true; } else if (sv) apply(sv);
paint();
if (lk) box.scrollIntoView({ block: 'start' });"""
BETA_TX = {'ru': 'по данным беты', 'en': 'per beta data', 'uk': 'за даними бети'}   # {beta} in a guide text: the site's one beta mark (build.BETA_SPAN)
langs.fill([LG_TX, BETA_TX, TIP, THIS_PAGE, MORE_H, MORE_SITE, SITE_TILES, PROF_HEAD, DG_TX, PLAY_TX, PLAY_MILESTONES])
JS['legacy'] = {l: LG_JS.replace('@@TX@@', json.dumps(LG_TX[l], ensure_ascii=False)) for l in LANGS}
JS['dungeons'] = {l: DG_JS.replace('@@TX@@', json.dumps(dict(DG_TX[l], pg=dungeon_pages.table_links()), ensure_ascii=False)) for l in LANGS}


def dungeons_data(src, lang=None):
    """Only the DUNGEONS array of the home page: the rest of its data is Russian and not needed here."""
    i = src.index('const DUNGEONS = [')
    return src[i:src.index('\n];', i) + 3]


JS['professions'] = r'''/* Professions: open the tab of the class from the link (#pairs=mage, class pages and the compare tool) or from "My hero" */
try {
  const link = (location.hash.match(/^#pairs=(\w+)$/) || [])[1];
  const cls = link || (JSON.parse(localStorage.getItem('gabella-wf-me')) || {}).cls;
  const tab = cls && document.querySelector(`#pairs [role="tab"][data-tab="${cls}"]`);
  if (tab) tab.click();
  if (link) document.getElementById('pairs').scrollIntoView();
} catch (e) {}'''


JS['buildshare'] = r'''/* Builds of a class: «Share» under the heading of every spec. The link is the card page b/<race>-<class>-<spec>/ (its preview shows the
   name of the build). The race: your hero's when he is of this class, else the best Alliance race of the spec (the Best race guide).
   Phone: the share sheet, otherwise the link goes to the clipboard. */
(function () {
  const cls = (location.pathname.match(/builds-(\w+)\/?$/) || [])[1];
  if (!cls || !HC.sid[cls]) return;
  const hero = readHero(), mine = hero && hero.cls === cls && HC.rf[hero.race] ? hero : null, BS = { skyA: 'skyborne-a', skyH: 'skyborne-h' };
  HC.sid[cls].forEach((spec, i) => {
    const h = (document.getElementById(spec) || {}).querySelector ? document.getElementById(spec).querySelector('h2') : null;
    if (!h) return;
    const wrap = document.createElement('p'), b = document.createElement('button'), msg = document.createElement('span');
    wrap.className = 'bshare'; b.type = 'button'; b.className = 'btn ghost'; b.textContent = HC.tx.share;
    msg.className = 'small'; msg.setAttribute('role', 'status'); wrap.append(b, ' ', msg); h.after(wrap);
    b.onclick = async () => {
      const fac = mine ? HC.rf[mine.race] : window.GabellaPor ? GabellaPor.fac() : 'alliance', best = bestOf(cls, fac, spec) || bestOf(cls, fac === 'alliance' ? 'horde' : 'alliance', spec),
        race = mine ? mine.race : best && best[0][0];
      if (!race) return;
      const url = new URL('../../b/' + (BS[race] || race) + '-' + cls + '-' + spec + '/', location.href).href;
      const title = HC.rn[race] + ' · ' + HC.cn[cls] + ' · ' + HC.sn[cls][i];
      if (navigator.share && matchMedia('(pointer: coarse)').matches) {
        try { await navigator.share({ title, url }); return; } catch (e) { if (e && e.name === 'AbortError') return; }
      }
      try { await navigator.clipboard.writeText(url); msg.textContent = HC.tx.linkCopied; } catch (e) { msg.textContent = url; }
    };
  });
})();'''


JS['cheat'] = r'''/* Spec cheat sheet: the «answer in 5 seconds» block (race strip, best races, buttons). #race=<race> comes from the card page b/<race>-<class>-<spec>/ (build_cards.py):
   the strip names the race and the picker link carries it. «Share» gives the card link of the build: the race from the link,
   else your hero's (same class), else the best Alliance race of the spec; phone: the share sheet, else the clipboard. */
(function () {
  const box = document.getElementById('cheat'); if (!box) return;
  const cls = box.dataset.cls, spec = box.dataset.spec, i = HC.sid[cls].indexOf(spec), BS = { skyA: 'skyborne-a', skyH: 'skyborne-h' };
  const hero = readHero(), mine = hero && hero.cls === cls && HC.rf[hero.race] ? hero : null;
  const asked = (location.hash.match(/(?:^#|&)race=(\w+)/) || [])[1], fromLink = asked && HC.rf[asked] ? asked : '';
  const pick = document.getElementById('cheatPick'), strip = document.getElementById('cheatRace');
  if (fromLink) {
    strip.textContent = box.dataset.from + ': ' + HC.rn[fromLink] + ' · ' + HC.fn[HC.rf[fromLink]]; strip.hidden = false;
    pick.href = '../../tools/#pick=' + fromLink + '.' + cls + '.' + spec;
  }
  document.getElementById('cheatShare').onclick = async () => {
    const msg = document.getElementById('cheatMsg'), fac = fromLink ? HC.rf[fromLink] : mine ? HC.rf[mine.race] : window.GabellaPor ? GabellaPor.fac() : 'alliance';
    const best = bestOf(cls, fac, spec) || bestOf(cls, fac === 'alliance' ? 'horde' : 'alliance', spec);
    const race = fromLink || (mine ? mine.race : best && best[0][0]);
    if (!race) return;
    const url = new URL('../../b/' + (BS[race] || race) + '-' + cls + '-' + spec + '/', location.href).href;
    const title = HC.rn[race] + ' · ' + HC.cn[cls] + ' · ' + HC.sn[cls][i];
    if (navigator.share && matchMedia('(pointer: coarse)').matches) {
      try { await navigator.share({ title, url }); return; } catch (e) { if (e && e.name === 'AbortError') return; }
    }
    try { await navigator.clipboard.writeText(url); msg.textContent = HC.tx.linkCopied; } catch (e) { msg.textContent = url; }
  };
  const best = document.getElementById('cheatBest'), b = HC.best[cls];   // best race of the spec for each faction, from the Best race guide
  const names = ['alliance', 'horde'].map(f => { const x = bestOf(cls, f, spec); return x && x[0] ? HC.rn[x[0][0]] + ' (' + HC.fn[f] + ')' : ''; }).filter(Boolean);
  if (b && names.length) best.firstChild.textContent = best.dataset.l + ': ' + names.join(', ');   // the link to the class' section of the Best race guide stays
})();
/* Gear 13–30 (content/spec_cheats.gear_html): faction, my level and my professions hide rows; the start is the hero of this browser.
   A row: data-s slot, data-lv required level, data-f the one faction of its quests, data-p the professions it is made by. */
(function () {
  const box = document.getElementById('gearBox'); if (!box) return;
  if (box.dataset.gsp) {   // the icon sprite only when the list comes near the screen
    const go = () => box.style.setProperty('--gsp', 'url("' + box.dataset.gsp + '")');
    if ('IntersectionObserver' in window) { const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { io.disconnect(); go(); } }, { rootMargin: '800px 0px' }); io.observe(box); } else go();
  }
  const rows = [...box.querySelectorAll('tbody tr[data-s]')], seg = document.getElementById('gearF'), lvIn = document.getElementById('gearLvl');
  const pb = document.getElementById('gearProf'), hero = readHero();
  let fac = hero && hero.fac ? hero.fac : 'all', lv = hero && +hero.lvl > 0 && +hero.lvl < 60 ? +hero.lvl : 0, only = false;
  const mineP = hero ? [hero.p1, hero.p2].filter(Boolean) : [];
  if (mineP.length && rows.some(r => r.dataset.p)) pb.hidden = false;
  function draw() {
    let n = 0, last = '';
    rows.forEach(r => {
      const p = r.dataset.p ? r.dataset.p.split(' ') : [];
      const off = (fac !== 'all' && r.dataset.f && r.dataset.f !== fac) || (lv && +r.dataset.lv > lv) || (only && p.length && !p.some(x => mineP.includes(x)));
      r.hidden = off;
      if (!off) { n++; r.classList.toggle('cont', r.dataset.s === last); last = r.dataset.s; }
    });
    document.getElementById('gearNone').hidden = n > 0;
    document.getElementById('gearCount').textContent = box.dataset.shown.replace('%n', n).replace('%t', rows.length);
    seg.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', b.dataset.v === fac ? 'true' : 'false'));
    pb.setAttribute('aria-pressed', only ? 'true' : 'false');
    if (document.activeElement !== lvIn) lvIn.value = lv || '';
  }
  seg.addEventListener('click', e => { const b = e.target.closest('button'); if (b) { fac = b.dataset.v; draw(); } });
  pb.addEventListener('click', () => { only = !only; draw(); });
  lvIn.addEventListener('input', () => { const v = parseInt(lvIn.value, 10); lv = v >= 1 && v <= 60 ? v : 0; draw(); });
  box.querySelectorAll('.lvm, .lvp').forEach(b => b.addEventListener('click', () => {
    const up = b.classList.contains('lvp');
    lv = Math.max(1, Math.min(60, (lv || (up ? 0 : 31)) + (up ? 1 : -1))); draw();
  }));
  draw();
})();'''


JS['news'] = r'''/* News: official Blizzard notes from data/official.json (level 1 of the news automation) on top of our notes */
fetch(ROOT + 'data/official.json').then(r => r.ok ? r.json() : []).then(items => {
  const list = document.querySelector('#ours .nlist');
  if (!list || !Array.isArray(items) || !items.length) return;
  const lang = (document.documentElement.lang || 'en').slice(0, 2);
  const pk = u => ((u || '').match(/\/t\/(?:[^/]+\/)?(\d+)\/(\d+)/) || []).slice(1).join('-') || u;   /* forum post: topic-post, any slug */
  const have = new Set([...list.querySelectorAll('.nitem')].map(a => pk(a.getAttribute('href'))));
  const html = items.filter(x => /^https:\/\//.test(x.url) && x.t && !have.has(pk(x.url))).map(x => {
    const t = x.t[lang] || x.t.en;
    return `<a class="nitem" href="${esc(x.url)}" target="_blank" rel="noopener" data-off="${esc(x.id)}"><time datetime="${esc(x.date)}">${esc(x.date.split('-').reverse().join('.'))}</time>`
      + (t.en ? `<b lang="en">${esc(t.h)}</b>` : `<b>${esc(t.h)}</b><p lang="en">${esc(x.title_en)}</p>`) + `<p>${esc(t.upd ? t.src + ' · ' + t.upd : t.src)}</p></a>`;
  });
  if (!html.length) return;
  /* merged by date with our notes: newest first */
  const all = [...list.querySelectorAll('.nitem')].map(a => [a.querySelector('time').getAttribute('datetime'), a.outerHTML]);
  html.forEach(h => all.push([h.match(/datetime="([^"]+)"/)[1], h]));
  list.innerHTML = all.sort((a, b) => (a[0] < b[0] ? 1 : a[0] > b[0] ? -1 : 0)).map(x => x[1]).join('');
  markMine();
}).catch(() => {});
/* News: automatic Wowhead feed from assets/news.json; no file -> the list stays hidden */
fetch(ROOT + 'assets/news.json').then(r => r.ok ? r.json() : []).then(items => {
  const box = document.getElementById('feedList');
  if (!box || !items.length) return;
  let day = '';   // grouped by day: the date once as a heading, the entries under it as plain lines
  box.innerHTML = items.filter(n => /^https:\/\//.test(n.url)).map(n => (n.date !== day ? `<h3 class="nday">${esc((day = n.date).split('-').reverse().join('.'))}</h3>` : '')
    + `<a class="nitem" href="${esc(n.url)}" target="_blank" rel="noopener"><b>${esc(n.title)}</b></a>`).join('');
  box.hidden = false;
  markMine();
}).catch(() => {});
/* «About your class»: our notes by their data-cls ('all' or class ids), the English feed by the class name in the title */
function markMine() {
  const h = readHero(); if (!h) return;
  const rx = new RegExp('\\b' + HC.cen[h.cls] + 's?\\b', 'i');
  document.querySelectorAll('.nitem').forEach(a => {
    const c = a.dataset.cls, b = a.querySelector('b');
    const mine = c ? c === 'all' || c.split(' ').includes(h.cls) : rx.test(b ? b.textContent : '');
    if (mine && b && !a.querySelector('.nmine')) b.insertAdjacentHTML('afterend', `<span class="nmine">${esc(HC.tx.mine)}: ${esc(h.clsN)}</span>`);
  });
  /* the class's notes and headlines once more on top of the page (#mine: the «News» button of the home block) */
  const items = [...document.querySelectorAll('.gsec:not(#mine) .nitem')].filter(a => a.querySelector('.nmine'));
  let top = document.getElementById('mine');
  if (!items.length) { if (top) top.remove(); return; }
  if (!top) {
    top = document.createElement('section'); top.className = 'gsec'; top.id = 'mine';
    const first = document.querySelector('.gsec'); first.parentNode.insertBefore(top, first);
  }
  top.innerHTML = `<h2>${esc(HC.tx.mine)}: ${esc(h.clsN)}</h2><div class="nlist">${items.map(a => a.outerHTML).join('')}</div>`;
  top.querySelectorAll('.nmine').forEach(x => x.remove());
  if (location.hash === '#mine' && !top.dataset.seen) { top.dataset.seen = '1'; top.scrollIntoView(); }
}
markMine();'''


def ref_js(src, lang):
    """Classes/races data and the comparison-table helpers of the home page (ref:start…ref:end), translated like the home page."""
    i, j = src.index('/* ref:start'), src.index('/* ref:end */')
    js = src[i:j].replace('@@RACE_LEAD@@', json.dumps({r['id']: r['lead'] for r in build.RACES_PAGE}, ensure_ascii=False))
    js = js.replace('@@RACE_SLUG@@', json.dumps({r['id']: r['slug'] for r in build.RACES_PAGE}))
    return translate(js, lang)[0]


JS['checklist'] = r'''/* Launch checklist: the ticks live in this browser ("gabella-day1" = {id: 1}), other tabs follow through the storage event */
const CK = 'gabella-day1', ckBoxes = [...document.querySelectorAll('.dchk input[data-ck]')];
const ckRead = () => { try { return JSON.parse(localStorage.getItem(CK)) || {}; } catch (e) { return {}; } };
let ckState = ckRead();
function ckSave() { try { localStorage.setItem(CK, JSON.stringify(ckState)); } catch (e) {} }
function ckPaint() {
  ckBoxes.forEach(b => { b.checked = !!ckState[b.dataset.ck]; });
  const n = ckBoxes.filter(b => b.checked).length;
  $('#ckN').textContent = n; $('#ckT').textContent = ckBoxes.length;
  $('#ckFill').style.width = (ckBoxes.length ? n * 100 / ckBoxes.length : 0) + '%';
  $('#ckReset').hidden = !n; $('#ckBar').hidden = false;
}
ckBoxes.forEach(b => b.addEventListener('change', () => {
  if (b.checked) ckState[b.dataset.ck] = 1; else delete ckState[b.dataset.ck];
  ckSave(); ckPaint();
}));
$('#ckReset').addEventListener('click', () => { ckState = {}; ckSave(); ckPaint(); });
addEventListener('storage', e => { if (e.key === CK) { ckState = ckRead(); ckPaint(); } });
ckPaint();
/* The hero of this browser: a line with its own link under the class, race, professions, start and ping steps */
(() => {
  const h = readHero(); if (!h) return;
  const T = HC.tx, f = (s, o) => s.replace(/%(\w)/g, (m, k) => (k in o ? o[k] : m)), best = bestOf(h.cls, h.fac, h.spec);
  const add = (id, text, href) => { const i = document.querySelector(`.dchk input[data-ck="${id}"]`); if (i && text) i.closest('li').insertAdjacentHTML('beforeend', `<p class="dme"><a href="${HOME}${href}">${esc(text)}</a></p>`); };
  add('class', h.spec ? f(T.ckClass, { s: h.specN }) : '', `guides/builds-${h.cls}/#${h.spec}`);
  if (best && h.raceN) add('race', best[0].includes(h.race) ? f(T.ckRaceOk, { r: h.raceN }) : f(T.ckRaceAlt, { r: best[0].map(r => HC.rn[r]).join(` ${T.or} `) }), `guides/best-race/#${h.cls}`);
  add('profs', f(T.ckProfs, { s: h.clsN }), `guides/professions/#pairs=${h.cls}`);
  add('start', f(T.ckStart, { s: h.clsN }), `guides/leveling-${h.cls}/`);
  if (T.regs[h.reg]) add('ping', f(T.ckPing, { s: T.regs[h.reg] }), 'tools/#ping');
  const list = document.querySelector('.dchk');
  if (list) list.insertAdjacentHTML('beforebegin', `<p class="dmehead"><b>${esc(T.day1Mine)}:</b> <a href="${HOME}character/">${esc([h.raceN, h.clsN, h.specN].filter(Boolean).join(' · '))}</a></p>`);
})();'''
JS['launchday'] = r'''/* Launch day: days, hours and minutes to 23:00 UTC 04.11 and the moment in the reader's own time zone */
const lcAt = new Date('2026-11-04T23:00:00Z');
function lcPaint() {
  const ms = lcAt - new Date(), p = x => String(x).padStart(2, '0');
  $('#lcWhen').textContent = new Intl.DateTimeFormat(document.documentElement.lang, { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZoneName: 'short' }).format(lcAt);
  $('#lcY').hidden = false;
  if (ms <= 0) { $('#lcd').classList.add('out'); $('#lcL').textContent = $('#lcL').dataset.out; return; }
  $('#lcD').textContent = Math.floor(ms / 864e5); $('#lcH').textContent = p(Math.floor(ms % 864e5 / 36e5)); $('#lcM').textContent = p(Math.floor(ms % 36e5 / 6e4));
}
lcPaint();
setInterval(lcPaint, 30000);'''
JS['classref'] = 'renderClassRef();'
JS['raceref'] = 'renderRaceRef();'

# ---------- /play/ «В игре»: compact page, a second screen while playing ----------

def leveling_parts():
    """From the Leveling guide: zone route {faction: [(lo, hi, text)]} and the tip of the pace section."""
    g = next(x for x in GUIDES if x['slug'] == 'leveling')
    sec = {s['id']: s for s in g['sections']}
    tabs = next(d for k, d in sec['route']['blocks'] if k == 'tabs')
    route = {}
    for tab in tabs:
        steps = next(d for k, d in tab['blocks'] if k == 'steps')
        route[tab['id']] = [(*map(int, L(x['t'], 'ru').split('–')), x['d']) for x in steps]
    tip = next(d for k, d in sec['pace']['blocks'] if k == 'tip')
    return route, tip


def play_data(src, lang):
    """Language data of the page script: route, milestones, labels, race -> faction and race/class names."""
    route, _ = leveling_parts()
    races = build.parse_races(src)
    art = os.path.join(HERE, 'assets', 'art')
    has = lambda n: os.path.isfile(os.path.join(art, f'{n}-face.webp'))   # noqa: E731
    slug = {r['id']: r['slug'] for r in build.RACES_PAGE}
    face = {}   # the face of the level block: race + class if drawn, else the race alone, else none (no other race's face)
    for r in races:
        if has(slug.get(r['id'], r['id'])):
            face[r['id']] = slug.get(r['id'], r['id'])
        for c in r['can']:
            n = f'{c}-{r["id"]}' if has(f'{c}-{r["id"]}') else face.get(r['id'])
            if n:
                face[f'{r["id"]}.{c}'] = n
    slugs = {g['slug'] for g in GUIDES if lang in g.get('langs', (lang,))}
    pages = {c['id']: [1, int(f'builds-{c["id"]}' in slugs), int(f'leveling-{c["id"]}' in slugs)] for c in build.CLASSES}   # class page, builds, class leveling
    data = {
        'route': {f: [[lo, hi, L(d, lang)] for lo, hi, d in rows] for f, rows in route.items()},
        'miles': [[lv, L(x, lang)] for lv, x in PLAY_MILESTONES],
        'tx': {k: L(v, lang) for k, v in PLAY_TX.items()},
        'racef': {r['id']: r['f'] for r in races},
        'rn': {r['id']: build.tr(r['n'], lang) for r in races},
        'cn': {c['id']: build.tr(c['n'], lang) for c in build.CLASSES},
        'face': face, 'col': build.COLOR, 'pages': pages,
    }
    return dungeons_data(src) + '\nconst P = ' + json.dumps(data, ensure_ascii=False) + ';\n'


def play_head(lang):
    """Title and lead on the left, the screen buttons on the right (each shows up only where the browser can do it)."""
    x = lambda k: E(PLAY_TX[k], lang)
    road = lambda ext, n='hero_road': ', '.join(f'@@ROOT@@assets/art/{n}-{w}.{ext} {w}w' for w in (960, 1600, 2560))   # noqa: E731
    fire = 'hero_campfire'
    # the evening road (Alliance) by default; the side of the hero (or the time of day, GabellaPor) Horde: the Horde campfire.
    # Both sets are in the markup (data-h-*) so build.art_version tags each with its own ?v=
    art = (f'<img class="phead-amb" src="@@ROOT@@assets/art/hero_road-960.webp" data-h-src="@@ROOT@@assets/art/{fire}-960.webp" width="960" height="536" alt="" aria-hidden="true" loading="lazy" decoding="async">'   # ultrawide sides
           '<picture class="phead-art" aria-hidden="true">'
           f'<source type="image/avif" srcset="{road("avif")}" data-h-srcset="{road("avif", fire)}" sizes="min(100vw, 1620px)"><source type="image/webp" srcset="{road("webp")}" data-h-srcset="{road("webp", fire)}" sizes="min(100vw, 1620px)">'
           f'<img src="@@ROOT@@assets/art/hero_road-1600.webp" data-h-src="@@ROOT@@assets/art/{fire}-1600.webp" width="1600" height="893" alt="" fetchpriority="high" decoding="async"></picture>'
           '<script>try{if(window.GabellaPor&&GabellaPor.fac()==="horde")document.querySelectorAll(".phead [data-h-srcset],.phead [data-h-src]").forEach(function(e){'
           'if(e.dataset.hSrcset)e.setAttribute("srcset",e.dataset.hSrcset);if(e.dataset.hSrc)e.setAttribute("src",e.dataset.hSrc)})}catch(e){}</script>')
    return ('<section class="phead" id="top">' + art + '<div class="wrap"><div class="ptitle"><h1>@@TITLE@@</h1><p class="glead">@@LEAD@@</p></div>'
            '</div></section>'
            f'<div class="wrap"><section class="frame pway" id="pWay" aria-label="{x("profile")}"><p class="pnote">{x("guest")}</p><a class="btn ghost" href="@@ROOT@@profile/">{x("login")}</a></section></div>'
            # the guest line is in the page from the start (no jump when me.js comes); signed in on this device: hidden at once
            '<script>try{if(localStorage.getItem("gabella-me")==="1")document.getElementById("pWay").hidden=true}catch(e){}</script>')


def play_body(lang, root):
    x = lambda k: E(PLAY_TX[k], lang)
    _, tip = leveling_parts()
    fac = ''.join(f'<button type="button" class="pill" data-f="{f}" aria-pressed="false">{x(f)}</button>' for f in ('alliance', 'horde'))
    presets = (f'<button type="button" class="pill" data-min="15" data-name="{x("food")}" title="{x("foodNote")}">{x("food")} · 15 {x("min")}</button>'
               + ''.join(f'<button type="button" class="pill" data-min="{m}">{m} {x("min")}</button>' for m in (5, 10, 30)))
    day1 = (f'<a class="gplay frame pday" href="{root}guides/launch-checklist/"><span><b>{x("day1")}</b> {x("day1d")}</span>'   # launch checklist, one line
            f'<span class="btn ghost">{x("day1go")}</span></a>')
    htx = deep(HERO.TX, lang)
    # the character line: a race-true face, «race · class», «spec · side», the hero sheet of hero.js (class -> spec -> race in
    # three taps; until hero.js has loaded the link opens character/), and the class pages once a class is set
    return day1 + f'''<div class="pgrid"><div class="pcol">
<section class="frame psec" id="level" aria-labelledby="hLvl">
  <div class="phero"><h2 id="hLvl">{x("lvl")}</h2><a href="{root}character/">{E(htx["allSet"], lang)}</a></div>
  <div class="pme"><img id="pFace" src="data:," alt="" width="56" height="56" hidden><div class="pwho"><b id="pWho">{x("noHero")}</b><span id="pSub"></span></div>
    <a class="btn ghost" id="pPick" href="{root}character/" data-hero-open>{E(htx["collect"], lang)}</a></div>
  <nav class="plinks" id="pLinks" aria-label="{x("clsGuide")}" hidden></nav>
  <div class="pchars" id="pChars" role="group" aria-label="{x("chars")}" hidden></div>
  <div class="pfac" id="pFac" role="group" aria-label="{x("fac")}">{fac}</div>
  <div class="plv"><button type="button" class="lvb" id="lvDown" aria-label="{x("lvDown")}">−</button><input id="lvIn" type="number" min="1" max="60" step="1" inputmode="numeric" enterkeyhint="done" placeholder="—" aria-label="{x("lvIn")}"><button type="button" class="lvb" id="lvUp" aria-label="{x("lvUp")}">+</button></div>
  <div class="plvq" id="lvQuick" role="group" aria-label="{x("lvQuick")}">{"".join(f'<button type="button" class="pill" data-lv="{n}" aria-pressed="false">{n}</button>' for n in (10, 20, 30, 40, 50, 60))}</div>
  <div id="pNow"></div>
  {render_block('tip', tip, lang, root)}
  <a class="pmore" href="{root}guides/leveling/#route">{x("route")}</a>
</section>
<section class="frame psec" id="dung" aria-labelledby="hDg"><h2 id="hDg">{x("dung")}</h2><ul class="pdg" id="pDg"></ul>
  <a class="pmore" href="{root}guides/dungeons/#list">{x("all")}</a></section>
</div><div class="pcol">
<section class="frame psec" id="radio" aria-labelledby="hRadio"><h2 id="hRadio">{x("radio")}</h2><div id="radioDock"><div class="rskel" aria-hidden="true"><i class="ra"></i><i class="rl"></i><span class="rc"><i></i><i></i><i></i><i class="rv"></i></span><i class="rl rs"></i><span class="rt"><i></i><i></i><i></i><i></i><i></i></span></div></div></section>
<section class="frame psec" id="timers" aria-labelledby="hT"><h2 id="hT">{x("timers")}</h2>
  <div class="ppre" id="tPre">{presets}</div>
  <form class="pform" id="tForm" novalidate><input id="tName" maxlength="40" placeholder="{x("name")}" aria-label="{x("name")}">
    <input id="tMin" type="number" min="1" max="600" inputmode="numeric" placeholder="{x("minutes")}" aria-label="{x("minutes")}">
    <button type="submit" class="pill gold">{x("start")}</button></form>
  <ul class="ptl" id="tList" aria-live="polite"></ul>
  <label class="pnotify" id="tNotify" hidden><input type="checkbox"> {x("notify")}</label>
  <p class="pnote" id="tReset" hidden></p>
</section>
</div></div>'''


def journey(src, lang):
    """/play/: game stages and my character (journey.src.html, on the home page until 25.10) with the home data (classes,
    races, camp objects) and the home i18n -> (section, script). The script goes after the page script: it reads DUNGEONS."""
    import build_tools
    jsrc = open(os.path.join(HERE, 'journey.src.html'), encoding='utf-8').read()
    jsrc = jsrc[jsrc.index('-->') + 4:]
    i = src.index('const PROFS = [')
    j = src.index('\n', src.index('const PR = ', i))
    data = build.js_names(build_tools.home_data(src, build_tools.HOME_JS[:1]), lang) + '\n' + src[i:j]
    html, missing = translate(jsrc.replace('@@DATA@@', data), lang)
    k = html.index('<script>')
    return html[:k], html[k:], missing


JS['play'] = r'''/* In game: level -> zones and the next milestones (data from the Leveling guide), dungeons near the level, timers,
   the mini window. Level, race and class are the shared hero "gabella-wf-me" of the home page (the level is
   written back); signed in, the hero is one of the profile characters and the level is saved to it. The chosen character,
   the faction without a race, the timers and the notification choice live in "gabella-play". */
const TX = P.tx, MEKEY = 'gabella-wf-me', PKEY = 'gabella-play';
const rd = k => { try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; } };
const wr = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} if (k === MEKEY) dispatchEvent(new CustomEvent('gabella-me', { detail: 'play' })); };
const ps = Object.assign({ fac: window.GabellaPor ? GabellaPor.fac() : 'alliance', timers: [], notify: false }, rd(PKEY));
if (!Array.isArray(ps.timers)) ps.timers = [];
const saveP = () => wr(PKEY, ps);
const GM = () => window.GabellaMe;   // me.js: the profile client, there on every page once it has loaded
let meNow = null, saveT = 0, pending = false, firstMe = true;
function chars() { return (meNow && meNow.characters) || []; }
function curChar() { const cs = chars(); return cs.find(c => c.id === ps.char) || cs.find(c => c.is_main) || cs[0] || null; }
function useChar(c) { const m = rd(MEKEY); m.race = c.race; m.cls = c.class; m.lvl = c.level; wr(MEKEY, m); }
const lvOf = m => Math.max(0, Math.min(60, parseInt(m.lvl, 10) || 0));
const lvRange = d => d[1] === d[2] ? String(d[1]) : `${d[1]}–${d[2]}`;
const nearLvl = (d, lv) => lv >= d[1] - 3 && lv <= d[2] + 3;
function setLvl(v) {
  const m = rd(MEKEY), c = curChar();
  m.lvl = Math.max(1, Math.min(60, v)); wr(MEKEY, m);
  if (c) { c.level = m.lvl; pending = true; saveLvl(); }
  renderLvl();
}
/* The level goes to the profile 1.5 s after the last tap: one request for a run of taps. While it is on its way the level on
   the screen wins over the one the profile answers with */
function saveLvl() {
  clearTimeout(saveT);
  saveT = setTimeout(() => {
    const c = curChar(), lv = lvOf(rd(MEKEY));
    if (!c || !GM()) { pending = false; return; }
    GM().api('/characters/' + c.id, { method: 'PUT', body: Object.assign({}, c, { level: lv }) }).then(r => {
      const s = ((r.me && r.me.characters) || []).find(x => x.id === c.id);
      if (s && s.level === lvOf(rd(MEKEY))) pending = false; else saveLvl();
      GM().took(r);
    }, () => { pending = false; });
  }, 1500);
}

const PV = /*PV*/'';   // ?v= of the portraits (build.art_version)
/* The character line: race-true face (P.face: race + class, else the race; none: no picture), spec from the hero, the class pages */
function renderWho(m) {
  const h = readHero() || {}, cls = P.cn[m.cls] ? m.cls : '', face = P.face[m.race + '.' + cls] || P.face[m.race] || '', img = $('#pFace');
  $('#pWho').textContent = P.rn[m.race] || cls ? [P.rn[m.race], P.cn[cls]].filter(Boolean).join(' · ') : TX.noHero;
  $('#pSub').textContent = [h.specN, TX[P.racef[m.race]]].filter(Boolean).join(' · ');
  img.hidden = !face;
  if (face) { const src = `${ROOT}assets/art/${face}-face.webp${PV}`; if (img.getAttribute('src') !== src) img.src = src; img.style.setProperty('--cc', P.col[cls] || ''); }
  const pick = $('#pPick');
  pick.hidden = !!meNow;
  pick.textContent = (HC.tx || {})[cls ? 'change' : 'collect'] || pick.textContent;
  const pg = P.pages[cls], L = [];
  if (pg) {
    if (pg[1]) L.push([`guides/builds-${cls}/${h.spec ? '#' + h.spec : ''}`, TX.myTal]);
    if (pg[0]) L.push([`classes/${cls}/`, TX.clsGuide]);
    if (pg[2]) L.push([`guides/leveling-${cls}/`, TX.clsLvl]);
  }
  $('#pLinks').innerHTML = L.map(([u, t]) => `<a href="${HOME}${u}">${esc(t)}</a>`).join('');
  $('#pLinks').hidden = !L.length;
}
function renderLvl() {
  const m = rd(MEKEY), lv = lvOf(m), raceF = P.racef[m.race], fac = raceF || ps.fac;
  renderWho(m);
  const cs = chars(), cur = curChar(), box = $('#pChars');
  box.hidden = !meNow;
  if (meNow) box.innerHTML = cs.length ? cs.map(c => `<button type="button" class="pill" data-c="${c.id}" aria-pressed="${c === cur}"><b>${esc(c.name)}</b>${c.level}</button>`).join('')
    : `<a href="${ROOT}profile/">${esc(TX.addChar)}</a>`;
  const all = $('#level .phero a');
  all.href = meNow ? ROOT + 'profile/' : HOME + 'character/';
  all.textContent = meNow ? TX.profile : (HC.tx || {}).allSet || all.textContent;
  $('#pFac').hidden = !!raceF;
  document.querySelectorAll('#pFac button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.f === fac)));
  if (document.activeElement !== $('#lvIn')) $('#lvIn').value = lv || '';
  document.querySelectorAll('#lvQuick button').forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.lv === lv)));
  if (!lv) {
    $('#pNow').innerHTML = `<p class="pnote">${esc(TX.needLvl)}</p>`;
    $('#pDg').innerHTML = `<li class="pnote">${esc(TX.needLvl)}</li>`;
    return;
  }
  const route = P.route[fac], nx = route.find(r => r[0] > lv), ms = P.miles.find(x => x[0] >= lv);
  let h = route.filter(r => lv >= r[0] && lv <= r[1]).map(r => `<div class="pnow"><span class="lvl gold">${r[0]}–${r[1]}</span><p>${esc(r[2])}</p></div>`).join('');
  const next = (nx ? `<li><b>${TX.from} ${nx[0]}</b>${esc(nx[2])}</li>` : '') + (ms ? `<li><b>${ms[0] === lv ? TX.now : TX.at + ' ' + ms[0]}</b>${esc(ms[1])}</li>` : '');
  if (next) h += `<h3 class="ph">${TX.next}</h3><ul class="pnext">${next}</ul>`;
  $('#pNow').innerHTML = h;
  const dg = DUNGEONS.filter(d => nearLvl(d, lv) && (!d[6] || d[6] === fac))
    .sort((a, b) => Math.abs(a[1] + a[2] - 2 * lv) - Math.abs(b[1] + b[2] - 2 * lv)).slice(0, 6).sort((a, b) => a[1] - b[1] || a[2] - b[2]);
  $('#pDg').innerHTML = dg.length ? dg.map(d => `<li><span><b>${esc(d[0])}</b>${d[4] ? ` <span class="tag new">${TX.new}</span>` : ''}<small>${esc(d[3])}</small></span>`
    + `<span class="lvl${lv >= d[1] && lv <= d[2] ? ' gold' : ''}">${lvRange(d)}</span></li>`).join('') : dgSoon(lv, fac);
}
/* Below the first dungeon: the three nearest ones above the level, not an empty «none» */
function dgSoon(lv, fac) {
  const up = DUNGEONS.filter(d => d[1] > lv && (!d[6] || d[6] === fac)).sort((a, b) => a[1] - b[1] || a[2] - b[2]).slice(0, 3);
  return `<li class="pnote">${TX.dungNone}</li>` + up.map(d => `<li><span><b>${esc(d[0])}</b><small>${esc(d[3])}</small></span><span class="lvl">${lvRange(d)}</span></li>`).join('');
}
$('#lvDown').addEventListener('click', () => setLvl((lvOf(rd(MEKEY)) || 2) - 1));
$('#lvUp').addEventListener('click', () => setLvl(lvOf(rd(MEKEY)) + 1));
$('#lvQuick').addEventListener('click', e => { const b = e.target.closest('button[data-lv]'); if (b) setLvl(+b.dataset.lv); });
/* The level typed in: taken on Enter or when the field is left; out of 1–60 or empty: the saved level comes back */
const lvIn = $('#lvIn');
lvIn.addEventListener('change', () => { const v = parseInt(lvIn.value, 10); if (v >= 1 && v <= 60) setLvl(v); else lvIn.value = lvOf(rd(MEKEY)) || ''; });
lvIn.addEventListener('keydown', e => { if (e.key === 'Enter') lvIn.blur(); });
lvIn.addEventListener('focus', () => lvIn.select());
$('#pChars').addEventListener('click', e => {
  const b = e.target.closest('button[data-c]'), c = b && chars().find(x => String(x.id) === b.dataset.c);
  if (!c) return;
  clearTimeout(saveT); pending = false;
  ps.char = c.id; saveP(); useChar(c); renderLvl();
});
$('#pFac').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { ps.fac = b.dataset.f; saveP(); renderLvl(); } });
addEventListener('keydown', e => {   // + / − on the keyboard: level up or down, outside text fields
  if (e.ctrlKey || e.metaKey || e.altKey || e.target.closest('input, textarea, select')) return;
  if (e.key === '+' || e.key === '=') setLvl(lvOf(rd(MEKEY)) + 1);
  else if (e.key === '-' || e.key === '_') setLvl((lvOf(rd(MEKEY)) || 2) - 1);
});
addEventListener('storage', e => { if (e.key === MEKEY) renderLvl(); });
addEventListener('gabella-me', e => { if (e.detail !== 'play') renderLvl(); });   // the character form below (journey.src.html)
renderLvl();

/* A guest gets one line with the login; a signed-in player has the characters in the level block already */
function renderWay() {
  const w = $('#pWay');
  w.hidden = !!meNow;
  if (!meNow) w.innerHTML = `<p class="pnote">${esc(TX.guest)}</p><a class="btn ghost" href="${ROOT}profile/">${esc(TX.login)}</a>`;
}
function gotMe(m) {
  if (!m && GM().logged()) return;   // signed in on this device: wait for the profile, no guest line in between
  meNow = m;
  const c = curChar();
  if (c && firstMe) {   // the level played here as a guest of the same hero is newer than the profile: keep it and save it
    const h = rd(MEKEY);
    if (h.race === c.race && h.cls === c.class && lvOf(h) > c.level) { c.level = lvOf(h); pending = true; saveLvl(); }
  }
  if (c) { if (pending) c.level = lvOf(rd(MEKEY)); else useChar(c); }
  if (m) firstMe = false;
  renderLvl(); renderWay();
}
function hookMe() { if (!GM()) return false; GM().onMe(gotMe); GM().me(); return true; }
if (!hookMe()) addEventListener('load', hookMe, { once: true });

/* Timers: the end time is stored, so they keep going after a reload. When one ends: three beeps, a blinking tab title
   and, if the visitor asked for it, a notification while the tab is in the background */
let actx = null;
function unlock() {   // the sound context has to start from a tap or a key
  try { actx = actx || new (window.AudioContext || window.webkitAudioContext)(); if (actx.state === 'suspended') actx.resume(); } catch (e) {}
}
function beep() {
  if (!actx) return;
  [0, .35, .7].forEach(t => {
    const o = actx.createOscillator(), g = actx.createGain(), s = actx.currentTime + t;
    o.frequency.value = 880; o.connect(g).connect(actx.destination);
    g.gain.setValueAtTime(.0001, s); g.gain.exponentialRampToValueAtTime(.3, s + .02); g.gain.exponentialRampToValueAtTime(.0001, s + .25);
    o.start(s); o.stop(s + .3);
  });
}
function notify(x) {
  if (!ps.notify || !document.hidden || !('Notification' in window) || Notification.permission !== 'granted') return;
  const opt = { body: TX.done, icon: ROOT + 'assets/icons/icon-192.png', tag: 'play-' + x.id };
  try { new Notification(x.name, opt); }
  catch (e) { if (navigator.serviceWorker) navigator.serviceWorker.ready.then(r => r.showNotification(x.name, opt)).catch(() => {}); }
}
const fmtT = ms => {
  const s = Math.max(0, Math.ceil(ms / 1000)), m = Math.floor(s / 60), ss = String(s % 60).padStart(2, '0');
  return m >= 60 ? `${Math.floor(m / 60)}:${String(m % 60).padStart(2, '0')}:${ss}` : `${m}:${ss}`;
};
const AGAIN = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7"/></svg>';
function renderTimers() {
  $('#tList').innerHTML = ps.timers.length ? ps.timers.map(x => `<li data-id="${esc(x.id)}"><span class="tn">${esc(x.name)}</span><span class="tt"></span>`
    + `<button type="button" class="iconbtn" data-act="again" aria-label="${esc(TX.again)}: ${esc(x.name)}">${AGAIN}</button>`
    + `<button type="button" class="iconbtn" data-act="rm" aria-label="${esc(TX.remove)}: ${esc(x.name)}"><svg class="ico" aria-hidden="true"><use href="#i-x"/></svg></button></li>`).join('')
    : `<li class="pnote">${esc(TX.noTimers)}</li>`;
  tick();
}
const baseTitle = document.title;
let blink = false;
function tick() {
  const now = Date.now();
  let soonest = Infinity, rung = null, changed = false;
  ps.timers.forEach(x => {
    const left = x.end - now;
    if (left <= 0 && !x.rang) { x.rang = true; changed = true; beep(); notify(x); }
    if (left > 0) soonest = Math.min(soonest, left); else rung = rung || x;
    const li = document.querySelector(`#tList li[data-id="${CSS.escape(x.id)}"]`);
    if (li) { li.classList.toggle('done', left <= 0); li.querySelector('.tt').textContent = left > 0 ? fmtT(left) : TX.done; }
  });
  if (changed) saveP();
  blink = !blink;
  document.title = rung ? (document.hidden && blink ? `⏰ ${TX.done}` : `⏰ ${rung.name} · ${baseTitle}`)
    : soonest < Infinity ? `${fmtT(soonest)} · ${baseTitle}` : baseTitle;
}
function addTimer(name, min) {
  unlock();
  ps.timers.push({ id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), name, min, end: Date.now() + min * 60000, rang: false });
  saveP(); renderTimers();
}
ps.timers.forEach(x => { if (x.end < Date.now() - 60000) x.rang = true; });   // ended while the page was closed: no beep now
$('#tPre').addEventListener('click', e => {
  const b = e.target.closest('button[data-min]');
  if (b) addTimer(b.dataset.name || `${b.dataset.min} ${TX.min}`, +b.dataset.min);
});
$('#tForm').addEventListener('submit', e => {
  e.preventDefault();
  const min = parseInt($('#tMin').value, 10);
  if (!(min >= 1 && min <= 600)) { $('#tMin').focus(); return; }
  addTimer($('#tName').value.trim() || `${TX.timer} · ${min} ${TX.min}`, min);
  $('#tName').value = ''; $('#tMin').value = '';
});
$('#tList').addEventListener('click', e => {
  const b = e.target.closest('button[data-act]');
  if (!b) return;
  const id = b.closest('li').dataset.id, x = ps.timers.find(t => t.id === id);
  if (!x) return;
  if (b.dataset.act === 'again') { unlock(); x.end = Date.now() + x.min * 60000; x.rang = false; }
  else ps.timers = ps.timers.filter(t => t !== x);
  saveP(); renderTimers();
});
addEventListener('pointerdown', unlock, { once: true });
const nBox = $('#tNotify'), nIn = nBox.querySelector('input');
if ('Notification' in window) {
  nBox.hidden = false;
  nIn.checked = ps.notify && Notification.permission === 'granted';
  nIn.addEventListener('change', () => {
    if (!nIn.checked) { ps.notify = false; saveP(); return; }
    Promise.resolve(Notification.requestPermission()).then(p => { ps.notify = p === 'granted'; nIn.checked = ps.notify; saveP(); });
  });
}
renderTimers();
setInterval(tick, 500);
/* The weekly reset of the region set on «My character» (the time Forever will use is not announced: said so) */
function renderReset() {
  const h = readHero(), T = HC.tx, box = $('#tReset');
  if (!h || !h.reg || !T.regs[h.reg]) { box.hidden = true; return; }
  const r = nextReset(h.reg);
  box.innerHTML = `<b>${esc(T.resetH)} · ${esc(T.regs[h.reg])}</b> ${esc(r ? T.resetIn.replace('%s', leftTxt(r - new Date())) : T.resetUnk)}${r ? `<br><small>${esc(T.resetNote)}</small>` : ''}`;
  box.hidden = false;
}
renderReset();
setInterval(renderReset, 60000);
addEventListener('storage', e => { if (e.key === MEKEY) renderReset(); });
'''

# ---------- character/ «Мой персонаж»: the hero of this browser (gabella-wf-me) without a login, content/hero.py ----------

def deep(x, lang):
    """A content value in one language: {'ru','en','uk',…} dicts become strings, lists and other dicts are walked."""
    if isinstance(x, dict):
        return x[lang] if set(langs.OLD) <= set(x) else {k: deep(v, lang) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [deep(v, lang) for v in x]
    return x


def hero_core(lang):
    """Language data every page that follows the hero needs: race/class/spec names, best races, labels (hero_js)."""
    src = home_src()
    races = build.parse_races(src)
    specs = {}
    for m in re.finditer(r"\{ id:'(\w+)'[^\n]*\n\s*specs:\[(.*?)\],\n", src[src.index('const CLASSES = ['):src.index('const ROLE_RU')]):
        specs[m.group(1)] = [build.tr(n, lang) for n in re.findall(r"\['([^']+)','[^']*',\[", m.group(2))]
    assert all(len(specs.get(c, ())) == 3 for c in HERO.SPEC_IDS), specs
    return {
        'tx': deep(HERO.TX, lang), 'best': deep(HERO.BEST, lang), 'sid': HERO.SPEC_IDS, 'sn': specs,
        'fn': {'alliance': build.tr('Альянс', lang), 'horde': build.tr('Орда', lang)}, 'reset': HERO.RESET,
        'rn': {r['id']: build.tr(r['n'], lang) for r in races}, 'rf': {r['id']: r['f'] for r in races},
        'cn': {c['id']: build.tr(c['n'], lang) for c in build.CLASSES}, 'cen': {c['id']: build.t_of(c['n'], 'en') if c['n'] in build.T else c['id'] for c in build.CLASSES},
    }


def hero_js(lang):
    """const HC = {…} and readHero(): the hero of this browser for the news, the checklist and the other pages that follow it.
    No localStorage (private mode, blocked): an empty hero, the page stays as it is."""
    return ('const HC = ' + json.dumps(hero_core(lang), ensure_ascii=False, separators=(',', ':')) + ';\n'
            + r'''function readHero() {
  let m = {};
  try { m = JSON.parse(localStorage.getItem('gabella-wf-me')) || {}; } catch (e) { m = {}; }
  if (!m || typeof m !== 'object' || !HC.cn[m.cls]) return null;
  const sid = HC.sid[m.cls], spec = sid.includes(m.spec) ? m.spec : '';
  return Object.assign({}, m, { spec, specN: spec ? HC.sn[m.cls][sid.indexOf(spec)] : '', clsN: HC.cn[m.cls], raceN: HC.rn[m.race] || '', fac: HC.rf[m.race] || '' });
}
function bestOf(cls, fac, spec) { const b = (HC.best[cls] || {})[fac]; return b ? (b[spec] || b['*']) : null; }
function nextReset(reg) {   // the region's weekly reset [weekday UTC, hour UTC] -> the next moment after now; null: not known
  const r = HC.reset[reg]; if (!r) return null;
  const now = new Date(), d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), r[1]));
  d.setUTCDate(d.getUTCDate() + (r[0] - d.getUTCDay() + 7) % 7);
  if (d <= now) d.setUTCDate(d.getUTCDate() + 7);
  return d;
}
function leftTxt(ms) {
  const u = (n, k) => new Intl.NumberFormat(document.documentElement.lang, { style: 'unit', unit: k, unitDisplay: 'short', maximumFractionDigits: 0 }).format(n);
  const m = Math.max(1, Math.round(ms / 6e4)), d = Math.floor(m / 1440), h = Math.floor(m % 1440 / 60);
  return d ? `${u(d, 'day')} ${u(h, 'hour')}` : h ? `${u(h, 'hour')} ${u(m % 60, 'minute')}` : u(m, 'minute');
}
''')


_ME_T = {}


def me_tr(ru, lang):
    """A Russian string of the profile pages (i18n/me.*.txt): the scene names of the portrait backgrounds."""
    if not _ME_T:
        _ME_T.update({r: (e, u) for r, e, u in zip(*(build.load(f'me.{l}.txt') for l in langs.OLD))})
    if lang == 'ru' or ru not in _ME_T:
        return ru
    en, uk = _ME_T[ru]
    return en if lang == 'en' else uk if lang == 'uk' else langs.ov(en, lang)


def hero_json(lang):
    """assets/hero/<lang>.json for assets/hero/hero.js (the top-bar switch on every page and the home block): the hero_js
    core plus what the switch draws without the page data — classes and their spec roles, races and what they can play,
    portrait slugs, the class profession pairs, the number of Day 1 steps."""
    src = home_src()
    core = hero_core(lang)
    roles = {}
    for m in re.finditer(r"\{ id:'(\w+)'[^\n]*\n\s*specs:\[(.*?)\],\n", src[src.index('const CLASSES = ['):src.index('const ROLE_RU')]):
        roles[m.group(1)] = [re.findall(r"'(tank|heal|dps)'", rs) for rs in re.findall(r"\['[^']*','[^']*',\[([^\]]*)\]\]", m.group(2))]
    assert all(len(roles.get(c, ())) == 3 for c in HERO.SPEC_IDS), roles
    ck = next(g for g in GUIDES if g['slug'] == 'launch-checklist')
    n = sum(1 for sec in ck['sections'] for k, d in sec['blocks'] if k == 'checks' for x in d if lang in x.get('langs', (lang,)))
    profs = {}
    for c in build.CLASSES:
        steps, why = build.class_profs(c['id'], lang)
        profs[c['id']] = [[label, pair] for label, pair, _ in steps] + [why]
    core.update({
        'cls': [c['id'] for c in build.CLASSES], 'color': build.COLOR, 'sr': roles,
        'role': {'tank': build.tr('Танк', lang), 'heal': build.tr('Лекарь', lang), 'dps': build.tr('Урон', lang)},
        'races': [[r['id'], r['f'], list(r['can']), int(r['paid'])] for r in build.parse_races(src)],
        'slug': {r['id']: r['slug'] for r in build.RACES_PAGE}, 'prof': profs, 'ck': n,
        'lfg': json.loads(__import__('build_tools').lfg_data(src, lang))['d'],
    })
    return json.dumps(core, ensure_ascii=False, separators=(',', ':'))


def hero_data(src, lang):
    """Script data of character/: the home classes, races, professions and dungeons (Russian, translated with the page),
    plus H: portraits and looks, the LFG names and the hero_js core."""
    import build_tools
    sys.path.insert(0, os.path.join(HERE, 'tools'))
    import export_game
    g = export_game.game()
    i = src.index('const PROFS = [')
    data = build.js_names(build_tools.home_data(src, build_tools.HOME_JS[:1]) + '\n' + dungeons_data(src), lang) + '\n' + src[i:src.index('\n', src.index('const PR = ', i))]
    scenes = dict(LK.SCENES)
    bgs = [[b, b] for b in g['backgrounds'] if not g['looks']['bg'][b]['lock']]
    rn = {r['id']: r['n'] for r in build.parse_races(src)}
    for x in bgs:   # portrait backgrounds: race arts by race name, scenes by their own
        b = x[0]
        rid = next((rid for rid, r in g['races'].items() if r['slug'] == b or (b == 'skyborne' and r['slug'].startswith('skyborne'))), None)
        x[1] = me_tr(scenes[b] if b in scenes else {'hero_dawn': 'Рассвет', 'hero_campfire': 'Привал'}[b], lang) if b in scenes or b.startswith('hero_') else build.tr(rn[rid], lang) if rid else b
    h = {
        'slug': {rid: r['slug'] for rid, r in g['races'].items()}, 'paid': [r['id'] for r in build.parse_races(src) if r.get('paid')],
        'look': {'v': g['looks']['v'], 'sexes': g['looks']['sexes'], 'races': g['looks']['races'], 'bgs': bgs},
        'lfg': json.loads(build_tools.lfg_data(src, lang)),
    }
    js, missing = translate(data, lang)
    return js + '\n' + hero_js(lang) + 'const H = ' + json.dumps(h, ensure_ascii=False, separators=(',', ':')) + ';\n', missing


HERO_CSS = '''<style>
.mhead { padding: calc(var(--top) + 28px) 0 8px; }
.mhead h1 { margin: 0; font-size: var(--fs-hero); line-height: 1.05; }
.mhead .glead { margin: 10px 0 0; max-width: 60ch; color: var(--muted); text-shadow: none; }   /* no hero art behind: the page colour, not the light ink over pictures (light theme) */
.mch { display: grid; gap: 18px; margin-top: 18px; }
.mcard { position: relative; isolation: isolate; overflow: hidden; display: grid; grid-template-columns: minmax(0, 1fr); align-content: end; min-height: 300px; padding: 22px; color: #f3efe6; background: #0a0a0a; }
.mcard > .bgi { position: absolute; inset: 0; z-index: -2; width: 100%; height: 100%; object-fit: cover; }
.mcard::after { content: ""; position: absolute; inset: 0; z-index: -1; background: linear-gradient(90deg, rgba(5,5,5,.92) 0%, rgba(5,5,5,.55) 55%, rgba(5,5,5,.15) 100%); }
.mcard .por { position: absolute; right: 4%; bottom: 0; z-index: -1; height: 112%; max-width: 46%; width: auto; object-fit: contain; object-position: bottom; }
.mcard .who { display: grid; gap: 6px; max-width: 34rem; }
.mcard .k { color: #e0c27a; font-size: var(--fs-14); font-weight: 600; letter-spacing: .02em; }
.mcard h2 { margin: 0; font-size: var(--fs-40); line-height: 1.05; }
.mcard .s { color: #d8d2c4; }
.mcard .row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
.mcard .btn.ghost { background: rgba(10,10,10,.6); color: #f3efe6; border-color: rgba(255,255,255,.18); }
.mcard .mnote { margin: 6px 0 0; color: #bdb6a6; font-size: var(--fs-13); }
.mwiz { padding: 20px; display: grid; gap: 16px; }
.mwiz[hidden], .mcard[hidden] { display: none; }
.msteps { display: flex; flex-wrap: wrap; gap: 6px 14px; margin: 0; padding: 0; list-style: none; font-size: var(--fs-14); color: var(--muted); }
.msteps button { all: unset; cursor: pointer; }
.msteps button:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }
.msteps [aria-current] { color: var(--gold-2); font-weight: 600; }
.mwiz h2 { margin: 0; font-size: var(--fs-28); }
.mwiz h3 { margin: 4px 0 0; font-size: var(--fs-18); }
.mpicks { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(112px, 100%), 1fr)); gap: 10px; }
.mpicks button { position: relative; display: grid; justify-items: center; gap: 8px; padding: 12px 8px; border: 1px solid var(--pline); border-radius: 10px; background: var(--panel-2); color: var(--fg); font: inherit; font-weight: 600; cursor: pointer; text-align: center; }
.mpicks button:hover { border-color: var(--gold); }
.mpicks button[aria-pressed="true"], .mpicks button[aria-checked="true"] { border-color: var(--gold); background: var(--seg-on); color: var(--gold-2); }
.mpicks img { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; background: #111 center / cover no-repeat; }
.mpicks small { color: var(--muted); font-weight: 500; font-size: var(--fs-13); }
.mpicks .star { position: absolute; top: 6px; right: 8px; color: var(--gold-2); }
.mfacs { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.mfacs button { position: relative; overflow: hidden; display: grid; align-content: end; min-height: 220px; padding: 16px; border: 1px solid var(--pline); border-radius: 10px; background: #0a0a0a; color: #f3efe6; font: inherit; font-size: var(--fs-22); font-weight: 600; cursor: pointer; text-align: left; }
.mfacs button img { position: absolute; inset: 0; z-index: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 20%; }
.mfacs button::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 40%, rgba(5,5,5,.9)); }
.mfacs button b { position: relative; z-index: 1; }
.mfacs button:hover, .mfacs button[aria-pressed="true"] { border-color: var(--gold); }
.mspec { display: flex; flex-wrap: wrap; gap: 8px; }
.mspec button { min-height: 44px; padding: 0 16px; border: 1px solid var(--pline); border-radius: 7px; background: var(--panel-2); color: var(--fg); font: inherit; cursor: pointer; }
.mspec button[aria-pressed="true"] { background: var(--seg-on); border-color: transparent; color: var(--gold-2); }
.mspec button small { color: var(--muted); margin-left: 6px; }
.mwhy { margin: 0; padding: 12px 14px; border-radius: 8px; background: var(--panel-2); }
.mwhy b { color: var(--gold-2); }
.mrow { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.mrow .sp { flex: 1; }
.mform { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(220px, 100%), 1fr)); gap: 14px; }
.mform label, .mform .fl { display: grid; gap: 6px; font-size: var(--fs-14); color: var(--muted); }
.mform select { min-height: 44px; padding: 0 10px; border: 1px solid var(--pline); border-radius: 7px; background: var(--panel-2); color: var(--fg); font: inherit; font-size: var(--fs-16); }
.mform .wide { grid-column: 1 / -1; }
.mlv { display: flex; align-items: center; gap: 14px; }
.mlv output { min-width: 2.4ch; text-align: center; font-family: var(--font-display); font-size: var(--fs-28); color: var(--gold-2); font-variant-numeric: lining-nums tabular-nums; }
.mlv button { width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--pline); background: var(--panel-2); color: var(--fg); font: inherit; font-size: var(--fs-22); cursor: pointer; }
.mout { display: grid; gap: 14px; grid-template-columns: minmax(0, 1fr); }
@media (min-width: 960px) { .mout { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); align-items: start; } .mout .wide { grid-column: 1 / -1; } }
.mlinks { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(260px, 100%), 1fr)); gap: 10px; }
.mlinks a { display: grid; gap: 4px; padding: 14px 16px; border: 1px solid var(--pline); border-radius: 10px; background: var(--panel-2); color: var(--fg); text-decoration: none; }
.mlinks a:hover { border-color: var(--gold); }
.mlinks a b { color: var(--gold-2); }
.mlinks a span { color: var(--muted); font-size: var(--fs-14); }
.mbox { padding: 16px 18px; display: grid; gap: 10px; align-content: start; }
.mbox h3 { margin: 0; font-size: var(--fs-22); }
.mbox p { margin: 0; }
.mbox .m { color: var(--muted); font-size: var(--fs-14); }
.mreset { font-size: var(--fs-28); font-weight: 600; color: var(--gold-2); font-variant-numeric: lining-nums tabular-nums; }
.mcopy { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 8px; }
.mcopy input { min-width: 0; min-height: 44px; padding: 0 12px; border: 1px solid var(--pline); border-radius: 7px; background: var(--panel-2); color: var(--fg); font: inherit; }
.mbox .pdg { margin: 0; }
.mbox .btn { white-space: normal; text-align: center; max-width: 100%; }
@media (max-width: 719px) {
  .mhead { padding-top: calc(var(--top) + 18px); }
  .mcard { min-height: 340px; padding: 18px; }
  .mcard::after { background: linear-gradient(180deg, rgba(5,5,5,.05) 20%, rgba(5,5,5,.94) 78%); }
  .mcard .por { right: 50%; transform: translateX(50%); height: 78%; max-width: 92%; top: 0; bottom: auto; object-position: top; }
  .mcard h2 { font-size: var(--fs-28); }
  .mfacs button { min-height: 170px; }
  .mwiz { padding: 16px; }
  .mpicks { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }
  .mpicks img { width: 60px; height: 60px; }
  .mcopy { grid-template-columns: minmax(0, 1fr); }
  .mlinks { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
  .mlinks a { padding: 12px; }
}
</style>'''


def hero_head(lang):
    return (f'<section class="mhead" id="top"><div class="wrap"><h1>@@TITLE@@</h1><p class="glead">@@LEAD@@</p></div></section>')


def hero_body(lang, root):
    """The card (or the empty one), the wizard and the blocks for the hero; all drawn by JS['hero'] from the hero of this browser."""
    tx = deep(HERO.TX, lang)
    return (HERO_CSS + '<div class="mch" id="hc">'
            f'<section class="frame mcard" id="hcCard" aria-live="polite"><div class="who"><span class="k">{escape(tx["title"])}</span>'
            f'<h2>{escape(tx["none"])}</h2><p class="mnote">{escape(tx["local"])}</p></div></section>'
            '<section class="frame mwiz" id="hcWiz" hidden></section>'
            '<div class="mout" id="hcOut"></div></div>')


JS['hero'] = r'''/* My character: the hero of this browser ("gabella-wf-me") made in a wizard without a login, and what the guide
   offers for it. The wizard: side -> class and spec -> race (the best one starred, from the Best race guide) -> look
   (sex and portrait background, the profile art) -> level, region, professions. #set=race.class.spec (the picker of
   tools/) makes a hero at once. No localStorage: the hero lives in this tab only, nothing breaks. */
const TX = HC.tx, MEKEY = 'gabella-wf-me';
const ME0 = { race: '', cls: '', spec: '', role: '', lvl: 0, p1: '', p2: '', sec: [], sex: '', bg: '', reg: '' };
let me = null, wiz = null;
function load() {
  let v = null;
  try { v = JSON.parse(localStorage.getItem(MEKEY) || 'null'); } catch (e) { v = null; }
  return v && typeof v === 'object' ? Object.assign({}, ME0, v) : null;
}
function save(h) {
  let all = {};
  try { all = JSON.parse(localStorage.getItem(MEKEY) || '{}') || {}; } catch (e) { all = {}; }
  me = Object.assign({}, all, h);
  try { localStorage.setItem(MEKEY, JSON.stringify(me)); } catch (e) {}
  dispatchEvent(new CustomEvent('gabella-me', { detail: 'hero' }));
}
const fill = (s, o) => s.replace(/%(\w)/g, (m, k) => (k in o ? o[k] : m));
const sidx = (c, s) => HC.sid[c].indexOf(s);
const specRoles = (c, s) => { const x = CL[c].specs[sidx(c, s)]; return x ? x[2].filter(r => !r.endsWith('?')) : []; };
const lookOf = h => ({ sex: h.sex || (H.look.races[h.race] || {}).sex || 'm', bg: h.bg || (H.look.races[h.race] || {}).bg || H.slug[h.race] });
const ver = '?v=' + H.look.v;   // the profile looks (content/looks.V)
const base = h => `${ROOT}assets/me/look/base/${H.slug[h.race]}-${lookOf(h).sex}.webp${ver}`;
const bgUrl = b => `${ROOT}assets/me/look/bg/${b}.webp${ver}`;
const face = (id, f) => `${ROOT}assets/art/${window.GabellaPor ? GabellaPor.id(id, f) : id}-face.webp${PV}`;   // a class: the portrait of side f (build.por_js)
const PV = /*PV*/'';
const valid = h => !!(h && CL[h.cls] && RC[h.race] && RC[h.race].can[h.cls]);
const bestRaces = (c, f, s) => { const b = bestOf(c, f, s); return b ? b[0] : []; };
function facOf(r) { return RC[r] ? RC[r].f : ''; }

/* ---------- the card ---------- */
function card() {
  const box = $('#hcCard');
  box.hidden = !!wiz;
  if (wiz) return;
  if (!valid(me)) {
    box.innerHTML = `<div class="who"><span class="k">${esc(TX.title)}</span><h2>${esc(TX.none)}</h2><p class="s">${esc(TX.plaqueD)}</p>`
      + `<div class="row"><button type="button" class="btn lg" data-go="1">${esc(TX.create)}</button></div><p class="mnote">${esc(TX.local)}</p></div>`;
    return;
  }
  const l = lookOf(me), sn = me.spec && sidx(me.cls, me.spec) >= 0 ? HC.sn[me.cls][sidx(me.cls, me.spec)] : '';
  const sub = [sn, me.role ? ROLE_RU[me.role] : '', facOf(me.race) === 'horde' ? H_FAC.horde : H_FAC.alliance,
    me.lvl ? fill(TX.levelN, { n: me.lvl }) : '', me.reg && TX.regs[me.reg] ? TX.regs[me.reg] : ''].filter(Boolean).join(' · ');
  box.style.setProperty('--cc', CCOL[me.cls]);
  box.innerHTML = `<img class="bgi" src="${bgUrl(l.bg)}" alt="" width="1600" height="900" fetchpriority="high" decoding="async">`
    + `<img class="por" src="${base(me)}" alt="" fetchpriority="high" decoding="async" onerror="this.remove()">`
    + `<div class="who"><span class="k">${esc(TX.title)}</span><h2>${esc(HC.rn[me.race])} · ${esc(HC.cn[me.cls])}</h2><span class="s">${esc(sub)}</span>`
    + `<div class="row"><button type="button" class="btn ghost" data-go="2">${esc(TX.edit)}</button><button type="button" class="btn ghost" data-go="5">${esc(TX.lvlReg)}</button></div>`
    + `<p class="mnote">${esc(TX.local)}</p></div>`;
}
const H_FAC = { alliance: '', horde: '' };

/* ---------- the wizard ---------- */
function openWiz(step) {
  const h = valid(me) ? me : {};
  wiz = Object.assign({}, ME0, h, { step, f: facOf(h.race) || '' });
  if (!wiz.f) wiz.step = 1;
  else if (step > 2 && !wiz.cls) wiz.step = 2;
  draw();
  const w = $('#hcWiz'); w.scrollIntoView({ block: 'start', behavior: 'auto' }); w.focus({ preventScroll: true });
}
function stepsBar() {
  const done = [!!wiz.f, !!(wiz.cls && wiz.spec), !!wiz.race, !!wiz.race, false];
  return `<ol class="msteps">${TX.steps.map((s, i) => {
    const n = i + 1, cur = n === wiz.step, can = n < wiz.step || done.slice(0, n - 1).every(Boolean);
    return `<li>${can && !cur ? `<button type="button" data-step="${n}">${n}. ${esc(s)}</button>` : `<span${cur ? ' aria-current="step"' : ''}>${n}. ${esc(s)}</span>`}</li>`;
  }).join('')}</ol>`;
}
function nav(next, doneBtn) {
  return `<div class="mrow">${wiz.step > 1 ? `<button type="button" class="btn ghost" data-back>${esc(TX.back)}</button>` : ''}`
    + (valid(me) ? `<button type="button" class="btn ghost" data-cancel>${esc(TX.cancel)}</button>` : '')
    + `<span class="sp"></span>${next ? `<button type="button" class="btn" data-next${next === 'off' ? ' disabled' : ''}>${esc(TX.next)}</button>` : ''}`
    + (doneBtn ? `<button type="button" class="btn" data-done${doneBtn === 'off' ? ' disabled' : ''}>${esc(TX.done)}</button>` : '') + '</div>';
}
function draw() {
  card();
  const w = $('#hcWiz');
  w.hidden = !wiz;
  out();
  if (!wiz) { w.innerHTML = ''; return; }
  w.setAttribute('aria-label', TX.title); w.tabIndex = -1;
  let b = '';
  if (wiz.step === 1) {
    b = `<h2>${esc(TX.side)}</h2><div class="mfacs">${['alliance', 'horde'].map(f => `<button type="button" data-f="${f}" aria-pressed="${wiz.f === f}">`
      + `<img src="${ROOT}assets/art/${f === 'alliance' ? 'human' : 'orc'}-600.webp${PV}" alt="" width="600" height="804" fetchpriority="high" decoding="async"><b>${esc(H_FAC[f])}</b></button>`).join('')}</div>` + nav(wiz.f ? 'on' : '', '');
  } else if (wiz.step === 2) {
    const cls = CLASSES.filter(c => RACES.some(r => r.f === wiz.f && r.can[c.id]));
    b = `<h2>${esc(TX.cls)}</h2><div class="mpicks" role="group" aria-label="${esc(TX.cls)}">${cls.map(c => `<button type="button" data-cls="${c.id}" aria-pressed="${wiz.cls === c.id}" style="color:${wiz.cls === c.id ? '' : CCOL[c.id]}">`
      + `<img src="${face(c.id, wiz.f)}" alt="" width="72" height="72" loading="lazy" decoding="async">${esc(HC.cn[c.id])}</button>`).join('')}</div>`;
    if (wiz.cls) b += `<h3>${esc(TX.spec)}</h3><div class="mspec" role="group" aria-label="${esc(TX.spec)}">${CL[wiz.cls].specs.map((s, i) => `<button type="button" data-spec="${HC.sid[wiz.cls][i]}" aria-pressed="${wiz.spec === HC.sid[wiz.cls][i]}">`
      + `${esc(HC.sn[wiz.cls][i])}<small>${esc(s[2].filter(r => !r.endsWith('?')).map(r => ROLE_RU[r]).join(', '))}</small></button>`).join('')}</div>`;
    b += nav(wiz.cls && wiz.spec ? 'on' : 'off', '');
  } else if (wiz.step === 3) {
    const best = bestRaces(wiz.cls, wiz.f, wiz.spec), bo = bestOf(wiz.cls, wiz.f, wiz.spec);
    const rs = RACES.filter(r => r.f === wiz.f && r.can[wiz.cls]).sort((a, c) => best.includes(c.id) - best.includes(a.id));
    const sn = HC.sn[wiz.cls][sidx(wiz.cls, wiz.spec)];
    b = `<h2>${esc(TX.race)}</h2>` + (bo ? `<p class="mwhy"><b>★ ${esc(fill(TX.bestFor, { s: sn }))}: ${esc(best.map(r => HC.rn[r]).join(` ${TX.or} `))}.</b> ${esc(bo[1])}</p>` : '')
      + `<div class="mpicks" role="group" aria-label="${esc(TX.race)}">${rs.map(r => `<button type="button" data-race="${r.id}" aria-pressed="${wiz.race === r.id}">`
      + (best.includes(r.id) ? `<span class="star" aria-hidden="true">★</span>` : '')
      + `<img src="${face(H.slug[r.id])}" alt="" width="72" height="72" loading="lazy" decoding="async">${esc(HC.rn[r.id])}`
      + (best.includes(r.id) ? `<small>${esc(TX.best)}</small>` : H.paid.includes(r.id) ? `<small>${esc(TX.paid)}</small>` : '') + '</button>').join('')}</div>`
      + nav(wiz.race ? 'on' : 'off', wiz.race ? 'on' : '');
  } else if (wiz.step === 4) {
    const l = lookOf(wiz);
    const tile = (k, v, name) => { const t = Object.assign({}, wiz, { [k]: v }), lt = lookOf(t);
      return `<button type="button" role="radio" aria-checked="${l[k] === v}" data-lk="${k}" data-v="${v}"><img src="${base(t)}" alt="" width="72" height="72" loading="lazy" decoding="async" style="background-image:url('${bgUrl(lt.bg)}')">${esc(name)}</button>`; };
    b = `<h2>${esc(TX.steps[3])}</h2><h3>${esc(TX.sex)}</h3><div class="mpicks" role="radiogroup" aria-label="${esc(TX.sex)}">${H.look.sexes.map(s => tile('sex', s, TX[s])).join('')}</div>`
      + `<h3>${esc(TX.bg)}</h3><div class="mpicks" role="radiogroup" aria-label="${esc(TX.bg)}">${H.look.bgs.map(([v, n]) => tile('bg', v, n)).join('')}</div>` + nav('on', 'on');
  } else {
    const prim = PROFS.filter(p => p[2]), opt = (v, list) => `<option value="">${esc(TX.noP)}</option>` + list.map(p => `<option value="${p[0]}"${p[0] === v ? ' selected' : ''}>${esc(p[1])}</option>`).join('');
    const ro = specRoles(wiz.cls, wiz.spec);
    b = `<h2>${esc(TX.steps[4])}</h2><p class="m small">${esc(TX.later)}</p><div class="mform">`
      + `<div class="fl"><span id="hLvL">${esc(TX.lvl)}</span><div class="mlv" role="group" aria-labelledby="hLvL"><button type="button" data-lv="-1" aria-label="−1">−</button><output id="hLv">${wiz.lvl || '—'}</output><button type="button" data-lv="1" aria-label="+1">+</button></div></div>`
      + `<label>${esc(TX.reg)}<select id="hReg"><option value="">—</option>${Object.keys(TX.regs).map(k => `<option value="${k}"${wiz.reg === k ? ' selected' : ''}>${esc(TX.regs[k])}</option>`).join('')}</select></label>`
      + (ro.length > 1 ? `<label>${esc(TX.role)}<select id="hRole">${ro.map(r => `<option value="${r}"${wiz.role === r ? ' selected' : ''}>${esc(ROLE_RU[r])}</option>`).join('')}</select></label>` : '')
      + `<label>${esc(TX.p1)}<select id="hP1">${opt(wiz.p1, prim.filter(p => p[0] !== wiz.p2))}</select></label>`
      + `<label>${esc(TX.p2)}<select id="hP2">${opt(wiz.p2, prim.filter(p => p[0] !== wiz.p1))}</select></label>`
      + `<div class="fl wide"><span id="hSecL">${esc(TX.secP)}</span><div class="chiprow" role="group" aria-labelledby="hSecL">${PROFS.filter(p => !p[2]).map(p => `<button type="button" data-sec="${p[0]}" aria-pressed="${(wiz.sec || []).includes(p[0])}">${esc(p[1])}</button>`).join('')}</div></div>`
      + '</div>' + nav('', 'on');
  }
  w.innerHTML = stepsBar() + b;
}
function finish() {
  const ro = specRoles(wiz.cls, wiz.spec);
  const h = { race: wiz.race, cls: wiz.cls, spec: wiz.spec, role: ro.includes(wiz.role) ? wiz.role : ro[0] || CL[wiz.cls].roles[0],
    lvl: Math.max(0, Math.min(60, +wiz.lvl || 0)), p1: wiz.p1 || '', p2: wiz.p2 || '', sec: wiz.sec || [], sex: wiz.sex || '', bg: wiz.bg || '', reg: wiz.reg || '' };
  wiz = null; save(h); draw();
  $('#hcCard').scrollIntoView({ block: 'start' });
}
document.addEventListener('click', e => {
  const go = e.target.closest('#hcCard [data-go]');
  if (go) return openWiz(+go.dataset.go);
  if (!wiz || !e.target.closest('#hcWiz')) return;
  const b = e.target.closest('button'); if (!b) return;
  const d = b.dataset;
  if (d.f) { if (wiz.f !== d.f) Object.assign(wiz, { race: '', cls: '', spec: '' }); wiz.f = d.f; wiz.step = 2; }
  else if (d.cls) { if (wiz.cls !== d.cls) wiz.spec = ''; wiz.cls = d.cls; if (wiz.race && !RC[wiz.race].can[wiz.cls]) wiz.race = ''; }
  else if (d.spec) { wiz.spec = d.spec; wiz.step = 3; }
  else if (d.race) { if (wiz.race !== d.race) { wiz.sex = ''; wiz.bg = ''; } wiz.race = d.race; wiz.step = 4; }
  else if (d.lk) { wiz[d.lk] = d.v; draw(); const t = $(`#hcWiz [data-lk="${d.lk}"][data-v="${d.v}"]`); if (t) t.focus(); return; }
  else if (d.lv) { wiz.lvl = Math.max(0, Math.min(60, (+wiz.lvl || (+d.lv > 0 ? 0 : 2)) + +d.lv)); $('#hLv').textContent = wiz.lvl || '—'; return; }
  else if (d.sec) { const s = wiz.sec || []; wiz.sec = s.includes(d.sec) ? s.filter(x => x !== d.sec) : s.concat(d.sec); b.setAttribute('aria-pressed', String(wiz.sec.includes(d.sec))); return; }
  else if (d.step) wiz.step = +d.step;
  else if ('back' in d) wiz.step--;
  else if ('next' in d) wiz.step++;
  else if ('done' in d) return finish();
  else if ('cancel' in d) wiz = null;
  else return;
  draw();
  if (wiz) { const w = $('#hcWiz'); if (w.getBoundingClientRect().top < 0) w.scrollIntoView({ block: 'start' }); }
});
document.addEventListener('change', e => {
  if (!wiz) return;
  const id = e.target.id;
  if (id === 'hReg') wiz.reg = e.target.value;
  else if (id === 'hRole') wiz.role = e.target.value;
  else if (id === 'hP1' || id === 'hP2') { wiz[id === 'hP1' ? 'p1' : 'p2'] = e.target.value; draw(); $('#' + id).focus(); }
});

/* ---------- what the guide offers for the hero ---------- */
function lfgText() {
  const lv = +me.lvl || 0, f = facOf(me.race);
  const ds = lv ? H.lfg.d.filter(d => lv >= d[1] - 2 && lv <= d[2] && (!d[3] || d[3] === f)) : [];
  const near = ds.sort((a, c) => Math.abs(a[1] + a[2] - 2 * lv) - Math.abs(c[1] + c[2] - 2 * lv))[0];
  return fill(near ? TX.lfgT : TX.lfgT0, { p: fill(TX.lfgP[me.role] || TX.lfgP.dps, { c: HC.cn[me.cls] }), d: near ? near[0] : '', l: lv });
}
function out() {
  const box = $('#hcOut');
  if (wiz || !valid(me)) { box.innerHTML = ''; return; }
  const c = me.cls, sn = me.spec && sidx(c, me.spec) >= 0 ? HC.sn[c][sidx(c, me.spec)] : '';
  const link = (href, t, d) => `<a href="${HOME}${href}"><b>${esc(t)}</b><span>${esc(d)}</span></a>`;
  let h = `<nav class="mlinks wide" aria-label="${esc(TX.title)}">`
    + link(`guides/builds-${c}/${me.spec ? '#' + me.spec : ''}`, TX.build, sn ? fill(TX.buildD, { s: sn }) : HC.cn[c])
    + link(`guides/professions/#pairs=${c}`, TX.pairs, TX.pairsD)
    + link(`guides/best-race/#${c}`, TX.bestR, TX.bestRD)
    + link(`guides/leveling-${c}/`, TX.lvlG, TX.lvlGD)
    + link('guides/launch-checklist/', TX.day1, TX.day1D)
    + link('play/', TX.play, TX.playD) + '</nav>';
  const lv = +me.lvl || 0, f = facOf(me.race);
  const ds = lv ? DUNGEONS.filter(d => lv >= d[1] - 3 && lv <= d[2] + 3 && (!d[6] || d[6] === f)).slice(0, 4) : [];
  h += `<section class="frame mbox"><h3>${esc(TX.dung)}</h3>` + (!lv ? `<p class="m">${esc(TX.dungNo)}</p>` : ds.length
    ? `<ul class="pdg">${ds.map(d => `<li><span><b>${esc(d[0])}</b><small>${esc(d[3])}</small></span><span class="lvl${lv >= d[1] && lv <= d[2] ? ' gold' : ''}">${d[1] === d[2] ? d[1] : d[1] + '–' + d[2]}</span></li>`).join('')}</ul>`
    : `<p class="m">${esc(TX.dungFirst)}</p>`) + `<a class="pmore" href="${HOME}guides/dungeons/#list">${esc(TX.allD)}</a></section>`;
  const nr = me.reg && nextReset(me.reg);
  h += `<section class="frame mbox" id="hReset"><h3>${esc(TX.resetH)}${me.reg && TX.regs[me.reg] ? ` · ${esc(TX.regs[me.reg])}` : ''}</h3>`
    + (!me.reg ? `<p class="m">${esc(TX.resetNoReg)}</p>` : !nr ? `<p class="m">${esc(TX.resetUnk)}</p>`
      : `<p class="mreset" id="hResetIn">${esc(fill(TX.resetIn, { s: leftTxt(nr - new Date()) }))}</p><p>${esc(new Intl.DateTimeFormat(document.documentElement.lang, { weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).format(nr))}</p><p class="m">${esc(TX.resetNote)}</p>`)
    + `<p class="m">${esc(TX.resetWhy)}</p></section>`;
  h += `<section class="frame mbox"><h3>${esc(TX.lfg)}</h3><p class="m">${esc(TX.lfgD)}</p><div class="mcopy"><input id="hLfg" readonly value="${esc(lfgText())}" aria-label="${esc(TX.lfg)}">`
    + `<button type="button" class="btn" id="hLfgCopy">${esc(TX.copy)}</button></div><p class="m" id="hLfgMsg" role="status"></p></section>`;
  h += `<section class="frame mbox" id="hSync"><h3>${esc(TX.sync)}</h3><p class="m">${esc(TX.syncD)}</p><div class="mrow"><a class="btn ghost" href="${ROOT}profile/#sync">${esc(TX.sync)}</a>`
    + `<span class="sp"></span><button type="button" class="btn ghost" id="hDel">${esc(TX.reset)}</button></div></section>`;
  box.innerHTML = h;
}
document.addEventListener('click', e => {
  if (e.target.id === 'hLfgCopy') {
    const v = $('#hLfg').value, done = () => { $('#hLfgMsg').textContent = TX.copied; };
    if (navigator.clipboard) navigator.clipboard.writeText(v).then(done, () => { $('#hLfg').select(); });
    else { $('#hLfg').select(); try { document.execCommand('copy'); done(); } catch (x) {} }
  } else if (e.target.id === 'hDel') {
    if (!confirm(TX.resetQ)) return;
    try { localStorage.removeItem(MEKEY); } catch (x) {}
    me = null; dispatchEvent(new CustomEvent('gabella-me', { detail: 'hero' })); draw();
  }
});
setInterval(() => { const n = $('#hResetIn'), r = me && me.reg && nextReset(me.reg); if (n && r) n.textContent = fill(TX.resetIn, { s: leftTxt(r - new Date()) }); }, 60000);

/* ---------- start: #set= from the picker, else the saved hero, else the wizard ---------- */
H_FAC.alliance = HC.fn.alliance; H_FAC.horde = HC.fn.horde;
me = load();
const set = location.hash.match(/^#set=(\w+)\.(\w+)(?:\.([\w-]+))?$/);
if (set && RC[set[1]] && RC[set[1]].can[set[2]]) {
  const spec = HC.sid[set[2]].includes(set[3]) ? set[3] : HC.sid[set[2]][0];
  const keep = me && me.race === set[1] && me.cls === set[2] ? me : {};
  save(Object.assign({}, ME0, keep, { race: set[1], cls: set[2], spec, role: specRoles(set[2], spec)[0] || '' }));
  history.replaceState(null, '', location.pathname + location.search);
}
if (!valid(me)) wiz = Object.assign({}, ME0, { step: 1, f: '' });
draw();
addEventListener('storage', e => { if (e.key === MEKEY && !wiz) { me = load(); draw(); } });'''


# ---------- Talent calculator: talents/ (the nine classes) and talents/<class>/ (talents.render_calc). Search texts: seo.CALC_* ----------
# A light page: a text heading instead of the art band (the first screen is the calculator, LCP is text), the bar of the editor in the
# page from the start, the class list under the tool.
CALC_TX = {'all': {'ru': 'Все классы', 'en': 'All classes', 'uk': 'Усі класи', 'de': 'Alle Klassen', 'fr': 'Toutes les classes',
                   'es': 'Todas las clases', 'pt': 'Todas as classes', 'it': 'Tutte le classi', 'pl': 'Wszystkie klasy'}}


def _calc_trees(cid):
    """(specs, titles) of guides/builds-<class>/: [(spec, talent table rows)] and {tree key: section title} for the calculator."""
    g = next(x for x in GUIDES if x['slug'] == f'builds-{cid}')
    blocks = [d for s in g['sections'] for k, d in s['blocks'] if k == 'tree']
    return [(d['spec'], d['rows']) for d in blocks], (blocks[0]['titles'] if blocks else {s['id']: s['title'] for s in g['sections']})


def calc_classes(lang, root, cur=None):
    """The nine classes as a row of plates: the class and its three trees; the current one marked."""
    out = []
    for c in build.CLASSES:
        data = talents.load(c['id'])
        if not data:
            continue
        titles = talents.tree_titles(_calc_trees(c['id'])[1], lang)
        trees = ' · '.join(escape(titles.get(t['key'], t['key'])) for t in data['trees'])
        out.append(build.spec_plate(f'{root}talents/{c["id"]}/', escape(build.tr(c['n'], lang)), trees, c['id'], face=True, cur=c['id'] == cur))
    return build.spec_list(out, 'cls9 calcl')


def calc_head(sec, g, lang):
    """The text heading of a calculator page from the translated art band: its crumbs and «updated» line, no picture."""
    crumbs = re.search(r'<nav class="crumbs".*?<span aria-hidden="true">/</span>', sec, re.S)[0]
    upd = re.search(r'<p class="upd">.*?</p>', sec, re.S)
    name = seo.CALC_NAME[lang]
    tail = (f'<a href="@@HOME@@talents/">{escape(name)}</a><span aria-hidden="true">/</span><span>{escape(build.tr(next(c["n"] for c in build.CLASSES if c["id"] == g["cls"]), lang))}</span>'
            if g['cls'] else f'<span>{escape(name)}</span>')
    return (f'<section class="chead" id="top"><div class="wrap">{crumbs}{tail}</nav><h1>@@TITLE@@</h1>'
            f'{upd[0] if upd else ""}<p class="glead">@@LEAD@@</p></div></section>')


def calc_body(g, lang, root):
    if not g['cls']:
        return f'<div class="frame gsec calcs">{calc_classes(lang, root)}</div>'
    specs, titles = _calc_trees(g['cls'])
    return (f'<div class="frame gsec calcs">{talents.render_calc(g["cls"], specs, titles, lang, root)}</div>'
            f'<section class="frame gsec" id="classes"><h2>{CALC_TX["all"][lang]}</h2>{calc_classes(lang, root, g["cls"])}</section>')


def calc_pages():
    """The ten calculator pages (PAGES records): titles, h1 and leads from seo.py."""
    hub = {'slug': 'talents', 'path': 'talents/', 'og': 'builds', 'art': 'paladin', 'compact': 'calc', 'more': False, 'cls': None,
           'title': {l: seo.CALC_HUB[l][1] for l in langs.ALL}, 'lead': {l: seo.CALC_HUB[l][3] for l in langs.ALL}, 'sections': [],
           'next': [('guides/builds/', next(x for x in GUIDES if x['slug'] == 'builds')['title'])]}
    out = [hub]
    for c in build.CLASSES:
        cid = c['id']
        if not talents.load(cid):
            continue
        by = {x['slug']: x for x in GUIDES}
        words = {l: seo.calc_words(cid, l) for l in LANGS}
        out.append({'slug': f'talents-{cid}', 'path': f'talents/{cid}/', 'og': f'builds-{cid}', 'art': cid, 'compact': 'calc', 'more': False,
                    'cls': cid, 'title': {l: seo.CALC_H1[l].format(**words[l]) for l in LANGS}, 'lead': {l: seo.CALC_LEAD[l] for l in LANGS},
                    'sections': [], 'next': [(f'guides/builds-{cid}/', by[f'builds-{cid}']['title']),
                                             (f'guides/leveling-{cid}/', by[f'leveling-{cid}']['title']), ('talents/', seo.CALC_NAME)]})
    return out


HERO_FOLLOW = ('news', 'checklist', 'play', 'buildshare', 'cheat')   # pages that follow the hero of this browser (hero_js before their script)
DATA = {'dungeons': dungeons_data, 'play': play_data}   # js key -> data blocks (from index.src.html and content)
REF = ('classref', 'raceref')        # js keys fed by ref_js (language-specific)


def page_ids(g):
    """Every id a guide puts on its page: sections, FAQ questions, raw blocks."""
    ids = [s['id'] for s in g['sections']]
    def walk(blocks):
        for k, d in blocks:
            if k == 'faq':
                ids.extend(q['id'] for q in d)
            elif k == 'tabs':
                for x in d:
                    walk(x['blocks'])
            elif k == 'raw':
                html = next(iter(d.values())) if isinstance(d, dict) else d   # raw ids are the same in every language
                ids.extend(re.findall(r'\sid="([^"]+)"', html))
    for s in g['sections']:
        walk(s['blocks'])
    return ids


def build_page(g, lang, tpl, base_css, sprite, src):
    if g['slug'].startswith('builds-'):   # a class' builds: the portrait of that class (por_band), not the shared leveling scene;
        g = {**g, 'por': True, 'hero': None}   # the tile on other pages keeps the scene. Set here, not in content: no new «Обновлено»
    sub = g['path'] if 'path' in g else (f'guides/{g["slug"]}/' if g['slug'] else 'guides/')   # path: classes/, races/, privacy/, '' (404)
    here = page_dir(lang, sub)
    html = tpl.replace('@@BASE_CSS@@', base_css).replace('@@SPRITE@@', sprite)
    nav = (g['path'] if g['path'] in ('classes/', 'races/', 'play/') else 'guides/builds/' if g.get('compact') == 'calc' else None) if 'path' in g else        (sub if g['slug'] in ('leveling', 'dungeons', 'tier-list', 'legacy') else 'guides/dungeons/' if g['slug'].startswith('dungeons/') else 'guides/leveling/' if g['slug'].startswith('leveling-') else 'guides/builds/' if g['slug'] == 'builds' or g['slug'].startswith(('builds-', 'spec-')) else 'guides/')   # privacy, 404: no current item
    tab = ('classes/' if g['slug'] == 'classes' else 'guides/builds/' if g.get('compact') == 'calc' else None) if 'path' in g else        'guides/leveling/' if g['slug'].startswith('leveling') else 'guides/builds/' if g['slug'] == 'builds' or g['slug'].startswith(('builds-', 'spec-')) else None   # builds, a class' builds, a spec sheet: the «Билды» tab
    html = build.chrome(html, nav=nav, tab=tab)
    if g.get('hero'):                                             # own full-screen scene instead of the art band
        html = re.sub(r'<section class="stband ghero" id="top">.*?</section>', lambda mt: thero(mt.group(0), g['hero']), html, count=1, flags=re.S)
    html, missing = translate(html, lang)                       # 1) обвязка
    root = rel(here, page_dir(lang))
    toc, body = render_guide(g, lang, root) if g['slug'] else hub_body(lang, root)
    if g.get('compact') == 'hero':                                # character/: a title line, the hero card is the picture
        html = re.sub(r'<section class="stband ghero" id="top">.*?</section>', lambda _: hero_head(lang), html, count=1, flags=re.S)
        html = html.replace('<body>', '<body class="compact">', 1).replace('<div class="wrap gbody', '<div class="wrap gbody play', 1)
        body = hero_body(lang, root)
        html = html.replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1)   # personal page, like profile/ (seo.NOINDEX)
    elif g.get('compact') == 'calc':                              # talents/: a text heading, the calculator is the first screen
        html = re.sub(r'<section class="stband ghero" id="top">.*?</section>', lambda mt: calc_head(mt.group(0), g, lang), html, count=1, flags=re.S)
        html = html.replace('<body>', '<body class="compact">', 1).replace('<div class="wrap gbody', '<div class="wrap gbody calcp', 1)
        body = calc_body(g, lang, root)
    elif g.get('compact'):                                        # /play/: small heading instead of the art band
        html = re.sub(r'<section class="stband ghero" id="top">.*?</section>', lambda _: play_head(lang), html, count=1, flags=re.S)
        html = html.replace('<body>', '<body class="compact">', 1).replace('<div class="wrap gbody', '<div class="wrap gbody play', 1)
        jsec, jscript, jmiss = journey(src, lang)
        body = play_body(lang, root) + jsec
        missing += jmiss
    if g is NOT_FOUND:                                            # 404: the six main sections, not every tile of the guide
        main = [x for x in section_tiles() if x['href'] in ('classes/', 'races/')]
        main += guide_tiles([x for slug in ('tier-list', 'launch-day', 'leveling', 'dungeons') for x in GUIDES if x['slug'] == slug])
        body += f'<section class="gsec bare" id="all">{render_block("tiles", main, lang, root)}</section>'
    if len(g.get('sections', ())) == 1:
        toc = ''                                                 # one section: no contents column
    section = 'path' in g                                         # classes/, races/, privacy/: not a guide
    if not g.get('more', True):
        others, more = [], ''
    elif section:
        others = [x for x in section_tiles() if x['href'] != g['path']] + SITE_TILES
        more = tile_links(others, lang, root)
    else:
        shown = inline_tiles(g.get('sections', []))                # one picture once on a page
        others = [x for x in lang_guides(lang) if x['slug'] != g['slug'] and f'guides/{x["slug"]}/' not in shown and x.get('others', True)
                  and not (g['slug'] == 'builds' and x['slug'].startswith('builds-'))] if g['slug'] else []   # builds: the class list above links them   # others: False, a page of one dungeon: reached from the dungeon list
        seen = {g.get('hero'), g['art']} | inline_arts(g.get('sections', []))   # a class art once: leveling-mage and builds-mage share it
        tiles = [x for x in guide_tiles(more_order(others, g['slug'])) if not (x['art'] in seen or seen.add(x['art']))]
        more = tile_links(full_rows(tiles), lang, root)
    avif, webp, img = art_sets(g['art'], '@@ROOT@@', big=True)
    crumb = (f'<a href="{root}guides/">{E(HUB["title"], lang)}</a><span aria-hidden="true">/</span><span>{E(g.get("crumb") or g["title"], lang)}</span>'
             if g['slug'] and not section else f'<span>{E(g["title"], lang)}</span>')
    toc_grp = f'<div class="grp"><div class="gh">{THIS_PAGE[lang]}</div>{toc}</div>' if toc else ''
    js = g.get('js')
    hero_js_data = ''
    if js == 'hero':
        hero_js_data, hmiss = hero_data(src, lang)
        missing += hmiss
    fx_attr = f' data-fx="{FX[g["art"]]}"' if g['art'] in FX else ''
    rep = {
        'HERO': (por_band(g['art']) if g.get('por') else
                 '@@TOD_HERO@@' if g['art'] == 'hero_dawn' else  # the leveling guide: the hero in the reader's time of day (tod.py)
                 (f'<img class="thero-amb" src="@@ROOT@@assets/art/{g["art"]}-960.webp" width="960" height="536" alt="" aria-hidden="true" loading="lazy" decoding="async">'   # ultrawide sides
                  if g['art'] in WIDTHS else '') +
                 f'<picture class="stband-art{"" if g["art"] in WIDTHS else " por"}" aria-hidden="true"{fx_attr}><source type="image/avif" srcset="{avif}" sizes="100vw">'
                 f'<img src="{img}" srcset="{webp}" sizes="100vw" alt="" decoding="async" fetchpriority="high"></picture>'),
        'TITLE': E(g['title'], lang), 'LEAD': E(g['lead'], lang), 'CRUMB': crumb,
        'PILLS': ' · '.join(E(p, lang) for p in g.get('pills', [])),   # one line of facts under the lead, no badges
        'TOC': toc, 'TOC_GRP': toc_grp, 'BODY': body, 'MORE': more, 'NEXT': build.next_block(g.get('next'), lang, root),
        'SOLO': '' if toc else ' solo', 'MORE_H': (MORE_SITE if section else MORE_H)[lang],
        # sources: a Wowhead page is cited, not recommended: nofollow, the reader's way goes to our pages (talents.WH_REL)
        'SOURCES': ''.join(f'<li><a href="{u}" target="_blank" rel="{talents.WH_REL if "wowhead.com" in u else "noopener"}">{E(n, lang)}</a></li>'
                           for n, u in g.get('sources', [])),
        'JS': ((hero_js_data + '\n' if js == 'hero' else hero_js(lang) + (build.js_names(DATA[js](src, lang), lang) + '\n' if js in DATA else '') if js in HERO_FOLLOW else build.js_names(DATA[js](src, lang), lang) + '\n' if js in DATA else ref_js(src, lang) + '\n' if js in REF else '') + L(JS[js], lang)) if js else '',
    }
    for k, v in rep.items():                                     # 2) тело
        html = html.replace(f'@@{k}@@', v)
    if g.get('por'):                                              # the class portrait band (por_band)
        html = html.replace('<section class="stband ghero" id="top">', '<section class="stband ghero pband" id="top">', 1)
    if g.get('path') == 'classes/':                              # phones: the class grid in the hero (cpick)
        html = html.replace('<p class="gfacts"></p>', '<p class="gfacts"></p>' + cpick(lang, root, E(g['title'], lang)), 1)
    elif g['slug'] == 'builds':                                   # phones: class -> its builds page in one tap from the first screen
        html = re.sub(r'(<p class="gfacts">.*?</p>)', lambda m: m[1] + cpick(lang, root, E(g['title'], lang), 'guides/builds-{}/'), html, count=1, flags=re.S)
    elif g['slug'].startswith('spec-'):                           # phones: the parts of a spec sheet as one row under the lead (gjump)
        html = re.sub(r'(<p class="gfacts">.*?</p>)', lambda m: m[1] + spec_jump(g, lang), html, count=1, flags=re.S)
    elif g['slug'] == 'launch-day' and build.LAUNCH.get('status_card'):   # launch day: the server status card under the facts (data/launch.json)
        html = re.sub(r'(<p class="gfacts">.*?</p>)', lambda m: m[1] + build.launch_card(lang, root, L(SS_TILE, lang)), html, count=1, flags=re.S)
    if g.get('compact') is True:
        html = html.replace('</body>', jscript + '</body>', 1)
    html = build.set_updated(html, sub)
    html = tod.apply(html, lang, root='@@ROOT@@', cls='stband-art', fx='dawn', mobile=True,
                     widths=WIDTHS['hero_dawn'], sizes='100vw', img_w=1920, img_h=1072, msizes='78vh')
    html = html.replace('\n    @@TOD_SW@@', '', 1)                # other guides: no switch
    if 'data-tod-art' in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="@@ROOT@@assets/tod/tod.css" media="print" onload="this.media=\'all\'">\n</head>', 1)
        html = html.replace('</body>', '<script src="@@ROOT@@assets/tod/tod.js" defer></script>\n</body>', 1)
    if not others:
        html = html.replace('<section id="more">', '<section id="more" hidden>')
    if not g.get('sources'):                                     # privacy, 404: footer without the sources list
        html = re.sub(r'<!--src-->.*?<!--/src-->', '', html, flags=re.S)
    html = html.replace('<!--src-->', '').replace('<!--/src-->', '')
    html = html.replace('@@HOME@@', root)
    html = build.static_links(html, lang, root)
    if LAUNCH_UTC in html:                                       # launch time: also in the reader's time zone
        html = re.sub(rf'{LAUNCH_UTC}(?=\.</(?:td|p)>)', f'<time class="lt" datetime="2026-11-04T23:00:00Z">{LAUNCH_UTC}</time>', html)
        html = html.replace('</body>', LOCAL_JS.replace('@@YOUR@@', YOUR[lang]) + '</body>', 1)
    if g['art'] in FX or g.get('hero'):
        html = html.replace('</body>', '<script src="@@ROOT@@assets/living/living.js" defer></script>\n</body>', 1)
    html = html.replace('@@CANON@@', SITE + here)
    html = html.replace('@@ALTERNATES@@', build.alternates(sub))
    html = html.replace('{beta}', f'<span class="beta-note">{BETA_TX[lang]}</span>')
    html = talents.page(html).replace('@@BETA@@', f'<span class="beta-note">{BETA_TX[lang]}</span>')
    html = localize(html, lang, here).replace('assets/og.png', f'assets/og/{g.get("og") or g["slug"] or "guides"}-{lang}.jpg')   # tools/make_og.py
    return here + 'index.html', html, missing


# 404.html at the root: GitHub Pages serves it for any bad address, in one language for everybody. A light page (no site chrome, no
# redirect): every language holds its own block of text, a head script only picks one (path /wow/<lang>/..., saved choice, browser, en);
# without JS all blocks show as a short list. The full localized pages stay at <lang>/404.html. The link preview is the same for every
# language (assets/og/404.jpg: mark and name, no words of a language; tools/make_og.py), because one file answers every bad address.
NOT_FOUND_LIGHT = r"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@ · Gabella</title>
<meta property="og:type" content="website">
<meta property="og:site_name" content="Gabella">
<meta property="og:title" content="Gabella · WoW Forever">
<meta property="og:description" content="gabella.site/wow/">
<meta property="og:image" content="https://gabella.site/wow/assets/og/404.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="48x48" href="/wow/assets/icons/favicon-48.png">
<script>
(function () {
  // the same order as the guide root (build.AUTO_JS): the language of the address, the saved choice, the browser, else English
  var L = '@@LANGS@@'.split(' '), A = { be: 'ru', kk: 'ru' }, m = location.pathname.match(/^\/wow\/([a-z]{2})\//), l = m && L.indexOf(m[1]) > -1 ? m[1] : '';
  if (!l) { try { var w = localStorage.getItem('gabella-lang'); if (L.indexOf(w) > -1) l = w; } catch (e) {} }
  for (var i = 0, n = navigator.languages || [navigator.language || '']; !l && i < n.length; i++) { var c = String(n[i]).toLowerCase().split('-')[0]; c = A[c] || c; if (L.indexOf(c) > -1) l = c; }
  l = l || 'en';
  var T = @@TITLES@@, d = document.documentElement;   // the chosen language: lang and title of the page follow it (screen readers, tabs)
  if (l) { d.setAttribute('data-l', l); d.lang = T[l][0]; document.title = T[l][1] + ' · Gabella'; }
})();
</script>
<style>
:root { color-scheme: dark light; --bg: #050505; --fg: #ece6d8; --muted: #a8a294; --gold: #c9a54a; --line: #2a2820; }
@media (prefers-color-scheme: light) { :root { --bg: #f6f1e6; --fg: #1d1a14; --muted: #5f594b; --gold: #7a5a14; --line: #d8cfba; } }
* { box-sizing: border-box; }
body { margin: 0; min-height: 100vh; display: grid; place-items: center; padding: 24px 16px; background: var(--bg); color: var(--fg); font: 1rem/1.5 Georgia, "Times New Roman", serif; }
main { width: 100%; max-width: 520px; }
.brand { margin: 0 0 20px; font-size: .85rem; letter-spacing: .14em; text-transform: uppercase; color: var(--gold); }
section { padding: 14px 0; border-top: 1px solid var(--line); }
h1 { margin: 0 0 8px; font-size: 1.5rem; font-weight: 600; line-height: 1.2; }
section p { margin: 0 0 8px; }
.why { color: var(--muted); }
a { color: var(--gold); text-underline-offset: 3px; }
:root[data-l] section { display: none; border-top: 0; padding-top: 0; }
@@SHOW@@
</style>
</head>
<body>
<main>
<p class="brand">Gabella · WoW Forever</p>
@@BLOCKS@@
</main>
</body>
</html>
"""


def not_found_light():
    """The root 404.html: one block per language (title, why, the way home), see NOT_FOUND_LIGHT. The reason is the first
    sentence of the full page's lead (the rest points at sections the light page does not have)."""
    why = {l: re.split(r'(?<=\.)\s', NOT_FOUND['lead'][l], maxsplit=1)[0] for l in LANGS}
    blocks = '\n'.join(
        f'<section lang="{langs.HREFLANG[l]}" data-k="{l}"><h1>{NOT_FOUND["title"][l]}</h1><p class="why">{why[l]}</p><p><a href="/wow/{"" if l == "ru" else l + "/"}">{langs.AUTONYM[l]} · gabella.site/wow/</a></p></section>'
        for l in LANGS)
    titles = json.dumps({l: [langs.HREFLANG[l], NOT_FOUND['title'][l]] for l in LANGS}, ensure_ascii=False)
    html = NOT_FOUND_LIGHT.replace('@@TITLE@@', NOT_FOUND['title']['ru']).replace('@@LANGS@@', ' '.join(LANGS)).replace('@@BLOCKS@@', blocks).replace('@@TITLES@@', titles)
    html = html.replace('@@SHOW@@', '\n'.join(f':root[data-l="{l}"] section[data-k="{l}"] {{ display: block; }}' for l in LANGS))
    return html


def not_found_page(tpl, base_css, sprite, src, lang='ru'):
    """404.html at the root: the light page for every language (GitHub Pages serves it at any depth under /wow/).
    <lang>/404.html: the full page per language, noindex, not canonical; <base> keeps its relative links working."""
    if lang == 'ru':
        return '404.html', not_found_light(), []
    _, html, missing = build_page(NOT_FOUND, lang, tpl, base_css, sprite, src)
    html = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n', '', html)
    html = re.sub(r'<meta property="og:[^>]*>\n', '', html)
    html = html.replace('<head>', f'<head>\n<base href="/wow/{page_dir(lang)}">\n<meta name="robots" content="noindex">', 1)
    html = html.replace('data-page=""', 'data-page="404"', 1)   # me.js: the secret for getting lost
    return page_dir(lang, '404.html'), html, missing


spec_cheats.finish(GUIDES, hero_core, langs)   # the four spec cheat sheets: names in every language
CALC_PAGES = calc_pages()


def main():
    gaps = (check_langs(HUB, 'HUB') + [p for g in GUIDES + HUBS + PAGES + [NOT_FOUND] for p in check_langs(g, g['slug'])]
            + check_langs(NEWS, 'NEWS') + check_langs(SITE_TILES, 'SITE_TILES')
            + check_langs(CLASS_HUB_TILE, 'CLASS_HUB_TILE') + check_langs(BUILDS_HUB_TILE, 'BUILDS_HUB_TILE') + check_langs(PLAY_TX, 'PLAY_TX') + check_langs(PLAY_MILESTONES, 'PLAY_MILESTONES'))
    assert not gaps, gaps[:10]
    src = open(os.path.join(HERE, 'index.src.html'), encoding='utf-8').read()
    tpl = open(os.path.join(HERE, 'guide.src.html'), encoding='utf-8').read()
    base_css = src[src.index('<style>') + 7:src.index('</style>')].strip('\n')
    s0 = src.index('<svg width="0" height="0"')
    sprite = src[s0:src.index('</svg>', s0) + 6]

    pages, allmissing = [], []
    for lang in LANGS:
        pages.append((f'assets/hero/{lang}.json', hero_json(lang)))   # assets/hero/hero.js: the top-bar switch and the home block
        for g in [HUB] + lang_guides(lang) + HUBS + PAGES + CALC_PAGES:
            path, html, missing = build_page(g, lang, tpl, base_css, sprite, src)
            assert '@@' not in html, (path, re.findall(r'@@\w+@@', html)[:5])
            pages.append((path, html))
            allmissing += missing
    for lang in LANGS:
        path, html, missing = not_found_page(tpl, base_css, sprite, src, lang)
        assert '@@' not in html, (path, re.findall(r'@@\w+@@', html)[:5])
        pages.append((path, html))
        allmissing += missing

    listing = '--list' in sys.argv
    if not listing:
        for path, html in pages:
            full = os.path.join(HERE, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, 'w', encoding='utf-8', newline='\n').write(html)
    uniq = list(dict.fromkeys(allmissing))
    if listing and '--missing' not in sys.argv:
        print('\n'.join(uniq))
    print(f'guides: {len(pages)}, missing: {len(uniq)}', file=sys.stderr)
    if uniq and not listing:
        sys.exit(1)


if __name__ == '__main__':
    main()
