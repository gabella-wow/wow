"""Share pages of a talent build: t/<class>-<spec>/ in every language (27 x 9 = 243 light pages).
«Copy build link» in a spec guide and in the calculator (talents.py) gives t/<class>-<spec>/#<code>: a chat reads this page and
shows the class and spec in og:title with the spec card assets/og/spec-<class>-<spec>-<lang>.jpg (tools/make_og.py, the class
portrait); a visitor is sent on to talents/<class>/#<code>, the same build in our calculator. Without a code in the address the
page opens our build of that spec. noindex, outside sitemap.xml (like b/, build_cards.py). Run after build_guides, before seo."""
import json, os, sys
from html import escape

import build
from build import LANGS, SITE, page_dir
import langs
import talents
import build_guides as BG
from content.spec_cheats import CHEATS, n9

HERE = build.HERE
LOCALE = {'ru': 'ru_RU', 'uk': 'uk_UA', 'en': 'en_US', 'de': 'de_DE', 'fr': 'fr_FR', 'es': 'es_ES', 'it': 'it_IT', 'pt': 'pt_BR', 'pl': 'pl_PL'}
# the spec the way the spec guides name it in their h1 (spec_cheats.H1_T without «guide»): «Маг Лёд», «Frost Mage»
NAME_T = n9('{c} {s}', '{s} {c}', '{c} {s}', '{c} {s}', '{c} {s}', '{c} {s}', '{c} {s}', '{c} {s}', '{s} {c}')
TITLE_T = n9('{n}: билд талантов WoW Forever', '{n} Talent Build · WoW Forever', '{n}: білд талантів WoW Forever',
             '{n}: Talent-Build · WoW Forever', 'Build de talents {n} · WoW Forever', 'Build de talentos de {n} · WoW Forever',
             'Build de talentos de {n} · WoW Forever', 'Build di talenti {n} · WoW Forever', '{n}: build talentów · WoW Forever')
DESC = n9('Билд талантов из калькулятора Gabella: ссылка открывает то же дерево с теми же очками.',
          'A talent build from the Gabella calculator: the link opens the same tree with the same points.',
          'Білд талантів із калькулятора Gabella: посилання відкриває те саме дерево з тими самими очками.',
          'Ein Talent-Build aus dem Gabella-Talentrechner: Der Link öffnet denselben Baum mit denselben Punkten.',
          'Un build de talents du calculateur Gabella : le lien ouvre le même arbre avec les mêmes points.',
          'Una build de talentos de la calculadora de Gabella: el enlace abre el mismo árbol con los mismos puntos.',
          'Uma build de talentos da calculadora da Gabella: o link abre a mesma árvore com os mesmos pontos.',
          'Una build di talenti dal calcolatore Gabella: il link apre lo stesso albero con gli stessi punti.',
          'Build talentów z kalkulatora Gabella: link otwiera to samo drzewo z tymi samymi punktami.')
KIND = n9('Билд талантов', 'Talent build', 'Білд талантів', 'Talent-Build', 'Build de talents', 'Build de talentos', 'Build de talentos',
          'Build di talenti', 'Build talentów')
IMG_ALT = n9('Карточка: {t}', 'Card: {t}', 'Картка: {t}', 'Karte: {t}', 'Carte : {t}', 'Tarjeta: {t}', 'Cartão: {t}', 'Scheda: {t}', 'Karta: {t}')


def spec_name(cid, spec, lang):
    n = BG.hero_core(lang)
    return NAME_T[lang].format(c=n['cn'][cid], s=n['sn'][cid][n['sid'][cid].index(spec)])


def og_title(cid, spec, lang):
    return TITLE_T[lang].format(n=spec_name(cid, spec, lang))


PAGE = '''<!doctype html>
<html lang="@@HL@@">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex,follow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESC@@">
<meta name="theme-color" content="#050505">
@@ALT@@
<link rel="canonical" href="@@URL@@">
<link rel="icon" type="image/png" sizes="48x48" href="@@ROOT@@assets/icons/favicon-48.png">
<link rel="manifest" href="@@ROOT@@manifest-@@LANG@@.webmanifest">
<meta property="og:type" content="website">
<meta property="og:locale" content="@@LOCALE@@">
<meta property="og:site_name" content="Gabella">
<meta property="og:title" content="@@TITLE@@">
<meta property="og:description" content="@@DESC@@">
<meta property="og:url" content="@@URL@@">
<meta property="og:image" content="@@IMG@@">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="@@ALTT@@">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="@@TITLE@@">
<meta name="twitter:description" content="@@DESC@@">
<meta name="twitter:image" content="@@IMG@@">
<meta name="twitter:image:alt" content="@@ALTT@@">
<script type="application/ld+json">@@LD@@</script>
<style>
:root { color-scheme: dark light; --bg: #050505; --fg: #ece6d8; --muted: #a8a294; --gold: #c9a54a; --line: #2a2820; }
@media (prefers-color-scheme: light) { :root { --bg: #f6f1e6; --fg: #1d1a14; --muted: #5f594b; --gold: #7a5a14; --line: #d8cfba; } }
* { box-sizing: border-box; }
body { margin: 0; min-height: 100vh; display: grid; place-items: center; padding: 24px 16px; background: var(--bg); color: var(--fg); font: 1rem/1.5 Georgia, "Times New Roman", serif; }
main { width: 100%; max-width: 520px; }
.brand { display: flex; align-items: center; gap: 10px; margin: 0 0 20px; font-size: .85rem; letter-spacing: .14em; text-transform: uppercase; color: var(--gold); }
.brand img { width: 32px; height: 32px; }
section { padding: 14px 0; border-top: 1px solid var(--line); }
h1 { margin: 0 0 4px; font-size: 1.5rem; font-weight: 600; line-height: 1.2; }
p { margin: 0 0 6px; }
.m { color: var(--muted); }
a { color: var(--gold); text-underline-offset: 3px; }
</style>
</head>
<body>
<main>
<p class="brand"><img src="@@ROOT@@assets/brand/mark.webp" width="32" height="32" alt="">Gabella · WoW Forever</p>
<section>
<h1>@@NAME@@</h1>
<p class="m">@@KIND@@</p>
<p><a id="go" href="@@CALC@@">@@OPEN@@</a></p>
</section>
</main>
<script>var a = document.getElementById('go'); if (/^#[0-9-]+$/.test(location.hash)) a.hash = location.hash; location.replace(a.href);</script>
<script>if ('serviceWorker' in navigator) addEventListener('load', () => navigator.serviceWorker.register('@@ROOT@@sw.js').catch(() => {}));</script>
</body>
</html>
'''


def our_codes(cid):
    """{spec: the build code of our talent table} of guides/builds-<class>/ (the calculator's own format)."""
    data = talents.load(cid)
    specs, _ = BG._calc_trees(cid)
    return {spec: talents.build_code(data, talents.table_picks(data, [(r[0], r[1]) for r in rows])) for spec, rows in specs}


def render(cid, spec, lang, code):
    sub = f't/{cid}-{spec}/'
    here = page_dir(lang, sub)
    root = build.rel(here, '')
    title, name = og_title(cid, spec, lang), spec_name(cid, spec, lang)
    url = SITE + here
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'WebPage', 'name': title, 'url': url, 'inLanguage': langs.HREFLANG[lang],
                     'isPartOf': {'@type': 'WebSite', 'name': 'Gabella', 'url': SITE}}, ensure_ascii=False)
    rep = {'HL': langs.HREFLANG[lang], 'LANG': lang, 'TITLE': escape(title), 'DESC': escape(DESC[lang]), 'ALT': build.alternates(sub), 'URL': url,
           'ROOT': root, 'LOCALE': LOCALE[lang], 'IMG': f'{SITE}assets/og/spec-{cid}-{spec}-{lang}.jpg', 'ALTT': escape(IMG_ALT[lang].format(t=name)),
           'LD': ld.replace('</', '<\\/'), 'NAME': escape(name), 'KIND': KIND[lang], 'OPEN': talents.UI['go'][lang],
           'CALC': f'{build.rel(here, page_dir(lang))}talents/{cid}/' + (f'#{code}' if code else '')}
    html = PAGE
    for k, v in rep.items():
        html = html.replace(f'@@{k}@@', v)
    assert '@@' not in html, (sub, lang)
    return here + 'index.html', html


def main():
    if '--list' in sys.argv:
        return
    n = 0
    codes = {}
    for cid, spec in CHEATS:
        if cid not in codes:
            codes[cid] = our_codes(cid) if talents.load(cid) else {}
        for lang in LANGS:
            assert os.path.isfile(os.path.join(HERE, 'assets', 'og', f'spec-{cid}-{spec}-{lang}.jpg')), (cid, spec, lang, 'python tools/make_og.py')
            path, html = render(cid, spec, lang, codes[cid].get(spec, ''))
            full = os.path.join(HERE, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'w', encoding='utf-8', newline='\n') as f:
                f.write(html)
            n += 1
    print(f'talent links: {n} pages', file=sys.stderr)


if __name__ == '__main__':
    main()
